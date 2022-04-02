# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: distutils\cygwinccompiler.py
"""distutils.cygwinccompiler

Provides the CygwinCCompiler class, a subclass of UnixCCompiler that
handles the Cygwin port of the GNU C compiler to Windows.  It also contains
the Mingw32CCompiler class which handles the mingw32 port of GCC (same as
cygwin in no-cygwin mode).
"""
import os, sys, copy
from subprocess import Popen, PIPE, check_output
import re
from distutils.ccompiler import gen_preprocess_options, gen_lib_options
from distutils.unixccompiler import UnixCCompiler
from distutils.file_util import write_file
from distutils.errors import DistutilsExecError, CCompilerError, CompileError, UnknownFileError
from distutils import log
from distutils.version import LooseVersion
from distutils.spawn import find_executable

def get_msvcr():
    """Include the appropriate MSVC runtime library if Python was built
    with MSVC 7.0 or later.
    """
    msc_pos = sys.version.find('MSC v.')
    if msc_pos != -1:
        msc_ver = sys.version[msc_pos + 6:msc_pos + 10]
        if msc_ver == '1300':
            return ['msvcr70']
        if msc_ver == '1310':
            return ['msvcr71']
        if msc_ver == '1400':
            return ['msvcr80']
        if msc_ver == '1500':
            return ['msvcr90']
        if msc_ver == '1600':
            return ['msvcr100']
        raise ValueError('Unknown MS Compiler version %s ' % msc_ver)


class CygwinCCompiler(UnixCCompiler):
    __doc__ = ' Handles the Cygwin port of the GNU C compiler to Windows.\n    '
    compiler_type = 'cygwin'
    obj_extension = '.o'
    static_lib_extension = '.a'
    shared_lib_extension = '.dll'
    static_lib_format = 'lib%s%s'
    shared_lib_format = '%s%s'
    exe_extension = '.exe'

    def __init__(self, verbose=0, dry_run=0, force=0):
        UnixCCompiler.__init__(self, verbose, dry_run, force)
        status, details = check_config_h()
        self.debug_print("Python's GCC status: %s (details: %s)" % (
         status, details))
        if status is not CONFIG_H_OK:
            self.warn("Python's pyconfig.h doesn't seem to support your compiler. Reason: %s. Compiling may fail because of undefined preprocessor macros." % details)
        else:
            self.gcc_version, self.ld_version, self.dllwrap_version = get_versions()
            self.debug_print(self.compiler_type + ': gcc %s, ld %s, dllwrap %s\n' % (
             self.gcc_version,
             self.ld_version,
             self.dllwrap_version))
            if self.ld_version >= '2.10.90':
                self.linker_dll = 'gcc'
            else:
                self.linker_dll = 'dllwrap'
            if self.ld_version >= '2.13':
                shared_option = '-shared'
            else:
                shared_option = '-mdll -static'
            self.set_executables(compiler='gcc -mcygwin -O -Wall', compiler_so='gcc -mcygwin -mdll -O -Wall',
              compiler_cxx='g++ -mcygwin -O -Wall',
              linker_exe='gcc -mcygwin',
              linker_so=('%s -mcygwin %s' % (
             self.linker_dll, shared_option)))
            if self.gcc_version == '2.91.57':
                self.dll_libraries = [
                 'msvcrt']
                self.warn('Consider upgrading to a newer version of gcc')
            else:
                self.dll_libraries = get_msvcr()

    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        """Compiles the source by spawning GCC and windres if needed."""
        if ext == '.rc' or ext == '.res':
            try:
                self.spawn(['windres', '-i', src, '-o', obj])
            except DistutilsExecError as msg:
                try:
                    raise CompileError(msg)
                finally:
                    msg = None
                    del msg

        else:
            try:
                self.spawn(self.compiler_so + cc_args + [src, '-o', obj] + extra_postargs)
            except DistutilsExecError as msg:
                try:
                    raise CompileError(msg)
                finally:
                    msg = None
                    del msg

    def link(self, target_desc, objects, output_filename, output_dir=None, libraries=None, library_dirs=None, runtime_library_dirs=None, export_symbols=None, debug=0, extra_preargs=None, extra_postargs=None, build_temp=None, target_lang=None):
        """Link the objects."""
        extra_preargs = copy.copy(extra_preargs or [])
        libraries = copy.copy(libraries or [])
        objects = copy.copy(objects or [])
        libraries.extend(self.dll_libraries)
        if export_symbols is not None:
            if target_desc != self.EXECUTABLE or self.linker_dll == 'gcc':
                temp_dir = os.path.dirname(objects[0])
                dll_name, dll_extension = os.path.splitext(os.path.basename(output_filename))
                def_file = os.path.join(temp_dir, dll_name + '.def')
                lib_file = os.path.join(temp_dir, 'lib' + dll_name + '.a')
                contents = [
                 'LIBRARY %s' % os.path.basename(output_filename),
                 'EXPORTS']
                for sym in export_symbols:
                    contents.append(sym)
                else:
                    self.execute(write_file, (def_file, contents), 'writing %s' % def_file)

                if self.linker_dll == 'dllwrap':
                    extra_preargs.extend(['--output-lib', lib_file])
                    extra_preargs.extend(['--def', def_file])
            else:
                objects.append(def_file)
        if not debug:
            extra_preargs.append('-s')
        UnixCCompiler.link(self, target_desc, objects, output_filename, output_dir, libraries, library_dirs, runtime_library_dirs, None, debug, extra_preargs, extra_postargs, build_temp, target_lang)

    def object_filenames(self, source_filenames, strip_dir=0, output_dir=''):
        """Adds supports for rc and res files."""
        if output_dir is None:
            output_dir = ''
        obj_names = []
        for src_name in source_filenames:
            base, ext = os.path.splitext(os.path.normcase(src_name))
            if ext not in self.src_extensions + ['.rc', '.res']:
                raise UnknownFileError("unknown file type '%s' (from '%s')" % (
                 ext, src_name))
            if strip_dir:
                base = os.path.basename(base)
            if ext in ('.res', '.rc'):
                obj_names.append(os.path.join(output_dir, base + ext + self.obj_extension))
            else:
                obj_names.append(os.path.join(output_dir, base + self.obj_extension))
        else:
            return obj_names


class Mingw32CCompiler(CygwinCCompiler):
    __doc__ = ' Handles the Mingw32 port of the GNU C compiler to Windows.\n    '
    compiler_type = 'mingw32'

    def __init__(self, verbose=0, dry_run=0, force=0):
        CygwinCCompiler.__init__(self, verbose, dry_run, force)
        if self.ld_version >= '2.13':
            shared_option = '-shared'
        else:
            shared_option = '-mdll -static'
        if self.gcc_version <= '2.91.57':
            entry_point = '--entry _DllMain@12'
        else:
            entry_point = ''
        if is_cygwingcc():
            raise CCompilerError('Cygwin gcc cannot be used with --compiler=mingw32')
        self.set_executables(compiler='gcc -O -Wall', compiler_so='gcc -mdll -O -Wall',
          compiler_cxx='g++ -O -Wall',
          linker_exe='gcc',
          linker_so=('%s %s %s' % (
         self.linker_dll, shared_option,
         entry_point)))
        self.dll_libraries = []
        self.dll_libraries = get_msvcr()


CONFIG_H_OK = 'ok'
CONFIG_H_NOTOK = 'not ok'
CONFIG_H_UNCERTAIN = 'uncertain'

def check_config_h--- This code section failed: ---

 L. 349         0  LOAD_CONST               0
                2  LOAD_CONST               ('sysconfig',)
                4  IMPORT_NAME              distutils
                6  IMPORT_FROM              sysconfig
                8  STORE_FAST               'sysconfig'
               10  POP_TOP          

 L. 353        12  LOAD_STR                 'GCC'
               14  LOAD_GLOBAL              sys
               16  LOAD_ATTR                version
               18  COMPARE_OP               in
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 354        22  LOAD_GLOBAL              CONFIG_H_OK
               24  LOAD_STR                 "sys.version mentions 'GCC'"
               26  BUILD_TUPLE_2         2 
               28  RETURN_VALUE     
             30_0  COME_FROM            20  '20'

 L. 357        30  LOAD_FAST                'sysconfig'
               32  LOAD_METHOD              get_config_h_filename
               34  CALL_METHOD_0         0  ''
               36  STORE_FAST               'fn'

 L. 358        38  SETUP_FINALLY       116  'to 116'

 L. 359        40  LOAD_GLOBAL              open
               42  LOAD_FAST                'fn'
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'config_h'

 L. 360        48  SETUP_FINALLY       102  'to 102'

 L. 361        50  LOAD_STR                 '__GNUC__'
               52  LOAD_FAST                'config_h'
               54  LOAD_METHOD              read
               56  CALL_METHOD_0         0  ''
               58  COMPARE_OP               in
               60  POP_JUMP_IF_FALSE    80  'to 80'

 L. 362        62  LOAD_GLOBAL              CONFIG_H_OK
               64  LOAD_STR                 "'%s' mentions '__GNUC__'"
               66  LOAD_FAST                'fn'
               68  BINARY_MODULO    
               70  BUILD_TUPLE_2         2 
               72  POP_BLOCK        
               74  CALL_FINALLY        102  'to 102'
               76  POP_BLOCK        
               78  RETURN_VALUE     
             80_0  COME_FROM            60  '60'

 L. 364        80  LOAD_GLOBAL              CONFIG_H_NOTOK
               82  LOAD_STR                 "'%s' does not mention '__GNUC__'"
               84  LOAD_FAST                'fn'
               86  BINARY_MODULO    
               88  BUILD_TUPLE_2         2 
               90  POP_BLOCK        
               92  CALL_FINALLY        102  'to 102'
               94  POP_BLOCK        
               96  RETURN_VALUE     
               98  POP_BLOCK        
              100  BEGIN_FINALLY    
            102_0  COME_FROM            92  '92'
            102_1  COME_FROM            74  '74'
            102_2  COME_FROM_FINALLY    48  '48'

 L. 366       102  LOAD_FAST                'config_h'
              104  LOAD_METHOD              close
              106  CALL_METHOD_0         0  ''
              108  POP_TOP          
              110  END_FINALLY      
              112  POP_BLOCK        
              114  JUMP_FORWARD        172  'to 172'
            116_0  COME_FROM_FINALLY    38  '38'

 L. 367       116  DUP_TOP          
              118  LOAD_GLOBAL              OSError
              120  COMPARE_OP               exception-match
              122  POP_JUMP_IF_FALSE   170  'to 170'
              124  POP_TOP          
              126  STORE_FAST               'exc'
              128  POP_TOP          
              130  SETUP_FINALLY       158  'to 158'

 L. 368       132  LOAD_GLOBAL              CONFIG_H_UNCERTAIN

 L. 369       134  LOAD_STR                 "couldn't read '%s': %s"
              136  LOAD_FAST                'fn'
              138  LOAD_FAST                'exc'
              140  LOAD_ATTR                strerror
              142  BUILD_TUPLE_2         2 
              144  BINARY_MODULO    

 L. 368       146  BUILD_TUPLE_2         2 
              148  ROT_FOUR         
              150  POP_BLOCK        
              152  POP_EXCEPT       
              154  CALL_FINALLY        158  'to 158'
              156  RETURN_VALUE     
            158_0  COME_FROM           154  '154'
            158_1  COME_FROM_FINALLY   130  '130'
              158  LOAD_CONST               None
              160  STORE_FAST               'exc'
              162  DELETE_FAST              'exc'
              164  END_FINALLY      
              166  POP_EXCEPT       
              168  JUMP_FORWARD        172  'to 172'
            170_0  COME_FROM           122  '122'
              170  END_FINALLY      
            172_0  COME_FROM           168  '168'
            172_1  COME_FROM           114  '114'

Parse error at or near `CALL_FINALLY' instruction at offset 74


RE_VERSION = re.compile(b'(\\d+\\.\\d+(\\.\\d+)*)')

def _find_exe_version(cmd):
    """Find the version of an executable by running `cmd` in the shell.

    If the command is not found, or the output does not match
    `RE_VERSION`, returns None.
    """
    executable = cmd.split[0]
    if find_executable(executable) is None:
        return
    out = Popen(cmd, shell=True, stdout=PIPE).stdout
    try:
        out_string = out.read
    finally:
        out.close

    result = RE_VERSION.search(out_string)
    if result is None:
        return
    return LooseVersion(result.group(1).decode)


def get_versions():
    """ Try to find out the versions of gcc, ld and dllwrap.

    If not possible it returns None for it.
    """
    commands = [
     'gcc -dumpversion', 'ld -v', 'dllwrap --version']
    return tuple([_find_exe_version(cmd) for cmd in commands])


def is_cygwingcc():
    """Try to determine if the gcc that would be used is from cygwin."""
    out_string = check_output(['gcc', '-dumpmachine'])
    return out_string.strip.endswith(b'cygwin')