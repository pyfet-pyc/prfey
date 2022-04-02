# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\distutils\mingw32ccompiler.py
"""
Support code for building Python extensions on Windows.

    # NT stuff
    # 1. Make sure libpython<version>.a exists for gcc.  If not, build it.
    # 2. Force windows to use gcc (we're struggling with MSVC and g77 support)
    # 3. Force windows to use g77

"""
import os, platform, sys, subprocess, re, textwrap, numpy.distutils.ccompiler
from numpy.distutils import log
import distutils.cygwinccompiler
from distutils.version import StrictVersion
from distutils.unixccompiler import UnixCCompiler
import distutils.msvccompiler as get_build_msvc_version
from distutils.errors import UnknownFileError
from numpy.distutils.misc_util import msvc_runtime_library, msvc_runtime_version, msvc_runtime_major, get_build_architecture

def get_msvcr_replacement():
    """Replacement for outdated version of get_msvcr from cygwinccompiler"""
    msvcr = msvc_runtime_library()
    if msvcr is None:
        return []
    return [msvcr]


distutils.cygwinccompiler.get_msvcr = get_msvcr_replacement
_START = re.compile('\\[Ordinal/Name Pointer\\] Table')
_TABLE = re.compile('^\\s+\\[([\\s*[0-9]*)\\] ([a-zA-Z0-9_]*)')

class Mingw32CCompiler(distutils.cygwinccompiler.CygwinCCompiler):
    __doc__ = ' A modified MingW32 compiler compatible with an MSVC built Python.\n\n    '
    compiler_type = 'mingw32'

    def __init__(self, verbose=0, dry_run=0, force=0):
        distutils.cygwinccompiler.CygwinCCompiler.__init__(self, verbose, dry_run, force)
        if self.gcc_version is None:
            try:
                out_string = subprocess.check_output(['gcc', '-dumpversion'])
            except (OSError, CalledProcessError):
                out_string = ''
            else:
                result = re.search('(\\d+\\.\\d+)', out_string)
                if result:
                    self.gcc_version = StrictVersion(result.group(1))
            if self.gcc_version <= '2.91.57':
                entry_point = '--entry _DllMain@12'
            else:
                entry_point = ''
            if self.linker_dll == 'dllwrap':
                self.linker = 'dllwrap'
            elif self.linker_dll == 'gcc':
                self.linker = 'g++'
            build_import_library()
            msvcr_success = build_msvcr_library()
            msvcr_dbg_success = build_msvcr_library(debug=True)
            if msvcr_success or (msvcr_dbg_success):
                self.define_macro('NPY_MINGW_USE_CUSTOM_MSVCR')
            msvcr_version = msvc_runtime_version()
            if msvcr_version:
                self.define_macro('__MSVCRT_VERSION__', '0x%04i' % msvcr_version)
        if get_build_architecture() == 'AMD64':
            if self.gcc_version < '4.0':
                self.set_executables(compiler='gcc -g -DDEBUG -DMS_WIN64 -mno-cygwin -O0 -Wall',
                  compiler_so='gcc -g -DDEBUG -DMS_WIN64 -mno-cygwin -O0 -Wall -Wstrict-prototypes',
                  linker_exe='gcc -g -mno-cygwin',
                  linker_so='gcc -g -mno-cygwin -shared')
            else:
                self.set_executables(compiler='gcc -g -DDEBUG -DMS_WIN64 -O0 -Wall',
                  compiler_so='gcc -g -DDEBUG -DMS_WIN64 -O0 -Wall -Wstrict-prototypes',
                  linker_exe='gcc -g',
                  linker_so='gcc -g -shared')
        elif self.gcc_version <= '3.0.0':
            self.set_executables(compiler='gcc -mno-cygwin -O2 -w',
              compiler_so='gcc -mno-cygwin -mdll -O2 -w -Wstrict-prototypes',
              linker_exe='g++ -mno-cygwin',
              linker_so=('%s -mno-cygwin -mdll -static %s' % (
             self.linker, entry_point)))
        elif self.gcc_version < '4.0':
            self.set_executables(compiler='gcc -mno-cygwin -O2 -Wall',
              compiler_so='gcc -mno-cygwin -O2 -Wall -Wstrict-prototypes',
              linker_exe='g++ -mno-cygwin',
              linker_so='g++ -mno-cygwin -shared')
        else:
            self.set_executables(compiler='gcc -O2 -Wall', compiler_so='gcc -O2 -Wall -Wstrict-prototypes',
              linker_exe='g++ ',
              linker_so='g++ -shared')
        self.compiler_cxx = [
         'g++']

    def link(self, target_desc, objects, output_filename, output_dir, libraries, library_dirs, runtime_library_dirs, export_symbols=None, debug=0, extra_preargs=None, extra_postargs=None, build_temp=None, target_lang=None):
        runtime_library = msvc_runtime_library()
        if runtime_library:
            if not libraries:
                libraries = []
            libraries.append(runtime_library)
        args = (
         self,
         target_desc,
         objects,
         output_filename,
         output_dir,
         libraries,
         library_dirs,
         runtime_library_dirs,
         None,
         debug,
         extra_preargs,
         extra_postargs,
         build_temp,
         target_lang)
        if self.gcc_version < '3.0.0':
            func = distutils.cygwinccompiler.CygwinCCompiler.link
        else:
            func = UnixCCompiler.link
        func(*args[:func.__code__.co_argcount])

    def object_filenames(self, source_filenames, strip_dir=0, output_dir=''):
        if output_dir is None:
            output_dir = ''
        obj_names = []
        for src_name in source_filenames:
            base, ext = os.path.splitext(os.path.normcase(src_name))
            drv, base = os.path.splitdrive(base)
            if drv:
                base = base[1:]
            if ext not in self.src_extensions + ['.rc', '.res']:
                raise UnknownFileError("unknown file type '%s' (from '%s')" % (
                 ext, src_name))
            if strip_dir:
                base = os.path.basename(base)
            if not ext == '.res' or ext == '.rc':
                obj_names.append(os.path.join(output_dir, base + ext + self.obj_extension))
            else:
                obj_names.append(os.path.join(output_dir, base + self.obj_extension))
        else:
            return obj_names


def find_python_dll():
    stems = [
     sys.prefix]
    if hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix:
        stems.append(sys.base_prefix)
    elif hasattr(sys, 'real_prefix'):
        if sys.real_prefix != sys.prefix:
            stems.append(sys.real_prefix)
    sub_dirs = [
     '', 'lib', 'bin']
    lib_dirs = []
    for stem in stems:
        for folder in sub_dirs:
            lib_dirs.append(os.path.join(stem, folder))

    else:
        if 'SYSTEMROOT' in os.environ:
            lib_dirs.append(os.path.join(os.environ['SYSTEMROOT'], 'System32'))
        major_version, minor_version = tuple(sys.version_info[:2])
        implementation = platform.python_implementation()
        if implementation == 'CPython':
            dllname = f"python{major_version}{minor_version}.dll"
        elif implementation == 'PyPy':
            dllname = f"libpypy{major_version}-c.dll"
        else:
            dllname = 'Unknown platform {implementation}'
        print('Looking for %s' % dllname)
        for folder in lib_dirs:
            dll = os.path.join(folder, dllname)
            if os.path.exists(dll):
                return dll
        else:
            raise ValueError('%s not found in %s' % (dllname, lib_dirs))


def dump_table(dll):
    st = subprocess.check_output(['objdump.exe', '-p', dll])
    return st.split(b'\n')


def generate_def--- This code section failed: ---

 L. 293         0  LOAD_GLOBAL              dump_table
                2  LOAD_FAST                'dll'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'dump'

 L. 294         8  LOAD_GLOBAL              range
               10  LOAD_GLOBAL              len
               12  LOAD_FAST                'dump'
               14  CALL_FUNCTION_1       1  ''
               16  CALL_FUNCTION_1       1  ''
               18  GET_ITER         
             20_0  COME_FROM            46  '46'
             20_1  COME_FROM            40  '40'
               20  FOR_ITER             48  'to 48'
               22  STORE_FAST               'i'

 L. 295        24  LOAD_GLOBAL              _START
               26  LOAD_METHOD              match
               28  LOAD_FAST                'dump'
               30  LOAD_FAST                'i'
               32  BINARY_SUBSCR    
               34  LOAD_METHOD              decode
               36  CALL_METHOD_0         0  ''
               38  CALL_METHOD_1         1  ''
               40  POP_JUMP_IF_FALSE_BACK    20  'to 20'

 L. 296        42  POP_TOP          
               44  BREAK_LOOP           56  'to 56'
               46  JUMP_BACK            20  'to 20'
             48_0  COME_FROM            20  '20'

 L. 298        48  LOAD_GLOBAL              ValueError
               50  LOAD_STR                 'Symbol table not found'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            44  '44'

 L. 300        56  BUILD_LIST_0          0 
               58  STORE_FAST               'syms'

 L. 301        60  LOAD_GLOBAL              range
               62  LOAD_FAST                'i'
               64  LOAD_CONST               1
               66  BINARY_ADD       
               68  LOAD_GLOBAL              len
               70  LOAD_FAST                'dump'
               72  CALL_FUNCTION_1       1  ''
               74  CALL_FUNCTION_2       2  ''
               76  GET_ITER         
             78_0  COME_FROM           144  '144'
             78_1  COME_FROM           138  '138'
               78  FOR_ITER            146  'to 146'
               80  STORE_FAST               'j'

 L. 302        82  LOAD_GLOBAL              _TABLE
               84  LOAD_METHOD              match
               86  LOAD_FAST                'dump'
               88  LOAD_FAST                'j'
               90  BINARY_SUBSCR    
               92  LOAD_METHOD              decode
               94  CALL_METHOD_0         0  ''
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'm'

 L. 303       100  LOAD_FAST                'm'
              102  POP_JUMP_IF_FALSE   140  'to 140'

 L. 304       104  LOAD_FAST                'syms'
              106  LOAD_METHOD              append
              108  LOAD_GLOBAL              int
              110  LOAD_FAST                'm'
              112  LOAD_METHOD              group
              114  LOAD_CONST               1
              116  CALL_METHOD_1         1  ''
              118  LOAD_METHOD              strip
              120  CALL_METHOD_0         0  ''
              122  CALL_FUNCTION_1       1  ''
              124  LOAD_FAST                'm'
              126  LOAD_METHOD              group
              128  LOAD_CONST               2
              130  CALL_METHOD_1         1  ''
              132  BUILD_TUPLE_2         2 
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
              138  JUMP_BACK            78  'to 78'
            140_0  COME_FROM           102  '102'

 L. 306       140  POP_TOP          
              142  BREAK_LOOP          146  'to 146'
              144  JUMP_BACK            78  'to 78'
            146_0  COME_FROM           142  '142'
            146_1  COME_FROM            78  '78'

 L. 308       146  LOAD_GLOBAL              len
              148  LOAD_FAST                'syms'
              150  CALL_FUNCTION_1       1  ''
              152  LOAD_CONST               0
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   172  'to 172'

 L. 309       158  LOAD_GLOBAL              log
              160  LOAD_METHOD              warn
              162  LOAD_STR                 'No symbols found in %s'
              164  LOAD_FAST                'dll'
              166  BINARY_MODULO    
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
            172_0  COME_FROM           156  '156'

 L. 311       172  LOAD_GLOBAL              open
              174  LOAD_FAST                'dfile'
              176  LOAD_STR                 'w'
              178  CALL_FUNCTION_2       2  ''
              180  SETUP_WITH          268  'to 268'
              182  STORE_FAST               'd'

 L. 312       184  LOAD_FAST                'd'
              186  LOAD_METHOD              write
              188  LOAD_STR                 'LIBRARY        %s\n'
              190  LOAD_GLOBAL              os
              192  LOAD_ATTR                path
              194  LOAD_METHOD              basename
              196  LOAD_FAST                'dll'
              198  CALL_METHOD_1         1  ''
              200  BINARY_MODULO    
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          

 L. 313       206  LOAD_FAST                'd'
              208  LOAD_METHOD              write
              210  LOAD_STR                 ';CODE          PRELOAD MOVEABLE DISCARDABLE\n'
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 314       216  LOAD_FAST                'd'
              218  LOAD_METHOD              write
              220  LOAD_STR                 ';DATA          PRELOAD SINGLE\n'
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          

 L. 315       226  LOAD_FAST                'd'
              228  LOAD_METHOD              write
              230  LOAD_STR                 '\nEXPORTS\n'
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          

 L. 316       236  LOAD_FAST                'syms'
              238  GET_ITER         
            240_0  COME_FROM           262  '262'
              240  FOR_ITER            264  'to 264'
              242  STORE_FAST               's'

 L. 318       244  LOAD_FAST                'd'
              246  LOAD_METHOD              write
              248  LOAD_STR                 '%s\n'
              250  LOAD_FAST                's'
              252  LOAD_CONST               1
              254  BINARY_SUBSCR    
              256  BINARY_MODULO    
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          
              262  JUMP_BACK           240  'to 240'
            264_0  COME_FROM           240  '240'
              264  POP_BLOCK        
              266  BEGIN_FINALLY    
            268_0  COME_FROM_WITH      180  '180'
              268  WITH_CLEANUP_START
              270  WITH_CLEANUP_FINISH
              272  END_FINALLY      

Parse error at or near `WITH_CLEANUP_FINISH' instruction at offset 270


def find_dll(dll_name):
    arch = {'AMD64':'amd64', 
     'Intel':'x86'}[get_build_architecture()]

    def _find_dll_in_winsxs(dll_name):
        winsxs_path = os.path.join(os.environ.get('WINDIR', 'C:\\WINDOWS'), 'winsxs')
        if not os.path.exists(winsxs_path):
            return
        for root, dirs, files in os.walk(winsxs_path):
            if dll_name in files:
                if arch in root:
                    return os.path.join(root, dll_name)

    def _find_dll_in_path(dll_name):
        for path in [
         sys.prefix] + os.environ['PATH'].split(';'):
            filepath = os.path.join(path, dll_name)
            if os.path.exists(filepath):
                return os.path.abspath(filepath)

    return _find_dll_in_winsxs(dll_name) or _find_dll_in_path(dll_name)


def build_msvcr_library(debug=False):
    if os.name != 'nt':
        return False
    msvcr_ver = msvc_runtime_major()
    if msvcr_ver is None:
        log.debug('Skip building import library: Runtime is not compiled with MSVC')
        return False
    if msvcr_ver < 80:
        log.debug('Skip building msvcr library: custom functionality not present')
        return False
    msvcr_name = msvc_runtime_library()
    if debug:
        msvcr_name += 'd'
    out_name = 'lib%s.a' % msvcr_name
    out_file = os.path.join(sys.prefix, 'libs', out_name)
    if os.path.isfile(out_file):
        log.debug('Skip building msvcr library: "%s" exists' % (
         out_file,))
        return True
    msvcr_dll_name = msvcr_name + '.dll'
    dll_file = find_dll(msvcr_dll_name)
    if not dll_file:
        log.warn('Cannot build msvcr library: "%s" not found' % msvcr_dll_name)
        return False
    def_name = 'lib%s.def' % msvcr_name
    def_file = os.path.join(sys.prefix, 'libs', def_name)
    log.info('Building msvcr library: "%s" (from %s)' % (
     out_file, dll_file))
    generate_def(dll_file, def_file)
    cmd = [
     'dlltool', '-d', def_file, '-l', out_file]
    retcode = subprocess.call(cmd)
    os.remove(def_file)
    return not retcode


def build_import_library():
    if os.name != 'nt':
        return
    arch = get_build_architecture()
    if arch == 'AMD64':
        return _build_import_library_amd64()
    if arch == 'Intel':
        return _build_import_library_x86()
    raise ValueError('Unhandled arch %s' % arch)


def _check_for_import_lib():
    """Check if an import library for the Python runtime already exists."""
    major_version, minor_version = tuple(sys.version_info[:2])
    patterns = [
     'libpython%d%d.a',
     'libpython%d%d.dll.a',
     'libpython%d.%d.dll.a']
    stems = [
     sys.prefix]
    if hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix:
        stems.append(sys.base_prefix)
    elif hasattr(sys, 'real_prefix'):
        if sys.real_prefix != sys.prefix:
            stems.append(sys.real_prefix)
    sub_dirs = ['libs', 'lib']
    candidates = []
    for pat in patterns:
        filename = pat % (major_version, minor_version)
        for stem_dir in stems:
            for folder in sub_dirs:
                candidates.append(os.path.join(stem_dir, folder, filename))

    else:
        for fullname in candidates:
            if os.path.isfile(fullname):
                return (
                 True, fullname)
        else:
            return (
             False, candidates[0])


def _build_import_library_amd64():
    out_exists, out_file = _check_for_import_lib()
    if out_exists:
        log.debug('Skip building import library: "%s" exists', out_file)
        return
    dll_file = find_python_dll()
    log.info('Building import library (arch=AMD64): "%s" (from %s)' % (
     out_file, dll_file))
    def_name = 'python%d%d.def' % tuple(sys.version_info[:2])
    def_file = os.path.join(sys.prefix, 'libs', def_name)
    generate_def(dll_file, def_file)
    cmd = [
     'dlltool', '-d', def_file, '-l', out_file]
    subprocess.check_call(cmd)


def _build_import_library_x86():
    """ Build the import libraries for Mingw32-gcc on Windows
    """
    out_exists, out_file = _check_for_import_lib()
    if out_exists:
        log.debug('Skip building import library: "%s" exists', out_file)
        return
    lib_name = 'python%d%d.lib' % tuple(sys.version_info[:2])
    lib_file = os.path.join(sys.prefix, 'libs', lib_name)
    if not os.path.isfile(lib_file):
        if hasattr(sys, 'base_prefix'):
            base_lib = os.path.join(sys.base_prefix, 'libs', lib_name)
        elif hasattr(sys, 'real_prefix'):
            base_lib = os.path.join(sys.real_prefix, 'libs', lib_name)
        else:
            base_lib = ''
        if os.path.isfile(base_lib):
            lib_file = base_lib
        else:
            log.warn('Cannot build import library: "%s" not found', lib_file)
            return
    log.info('Building import library (ARCH=x86): "%s"', out_file)
    from numpy.distutils import lib2def
    def_name = 'python%d%d.def' % tuple(sys.version_info[:2])
    def_file = os.path.join(sys.prefix, 'libs', def_name)
    nm_output = lib2def.getnm((lib2def.DEFAULT_NM + [lib_file]),
      shell=False)
    dlist, flist = lib2def.parse_nm(nm_output)
    with open(def_file, 'w') as fid:
        lib2def.output_def(dlist, flist, lib2def.DEF_HEADER, fid)
    dll_name = find_python_dll()
    cmd = [
     'dlltool',
     '--dllname', dll_name,
     '--def', def_file,
     '--output-lib', out_file]
    status = subprocess.check_output(cmd)
    if status:
        log.warn('Failed to build import library for gcc. Linking will fail.')


_MSVCRVER_TO_FULLVER = {}
if sys.platform == 'win32':
    try:
        import msvcrt
        _MSVCRVER_TO_FULLVER['80'] = '8.0.50727.42'
        _MSVCRVER_TO_FULLVER['90'] = '9.0.21022.8'
        _MSVCRVER_TO_FULLVER['100'] = '10.0.30319.460'
        _MSVCRVER_TO_FULLVER['140'] = '14.15.26726.0'
        if hasattr(msvcrt, 'CRT_ASSEMBLY_VERSION'):
            major, minor, rest = msvcrt.CRT_ASSEMBLY_VERSION.split('.', 2)
            _MSVCRVER_TO_FULLVER[major + minor] = msvcrt.CRT_ASSEMBLY_VERSION
            del major
            del minor
            del rest
    except ImportError:
        log.warn('Cannot import msvcrt: using manifest will not be possible')

def msvc_manifest_xml(maj, min):
    """Given a major and minor version of the MSVCR, returns the
    corresponding XML file."""
    try:
        fullver = _MSVCRVER_TO_FULLVER[str(maj * 10 + min)]
    except KeyError:
        raise ValueError('Version %d,%d of MSVCRT not supported yet' % (
         maj, min))
    else:
        template = textwrap.dedent('        <assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">\n          <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">\n            <security>\n              <requestedPrivileges>\n                <requestedExecutionLevel level="asInvoker" uiAccess="false"></requestedExecutionLevel>\n              </requestedPrivileges>\n            </security>\n          </trustInfo>\n          <dependency>\n            <dependentAssembly>\n              <assemblyIdentity type="win32" name="Microsoft.VC%(maj)d%(min)d.CRT" version="%(fullver)s" processorArchitecture="*" publicKeyToken="1fc8b3b9a1e18e3b"></assemblyIdentity>\n            </dependentAssembly>\n          </dependency>\n        </assembly>')
        return template % {'fullver':fullver,  'maj':maj,  'min':min}


def manifest_rc(name, type='dll'):
    """Return the rc file used to generate the res file which will be embedded
    as manifest for given manifest file name, of given type ('dll' or
    'exe').

    Parameters
    ----------
    name : str
            name of the manifest file to embed
    type : str {'dll', 'exe'}
            type of the binary which will embed the manifest

    """
    if type == 'dll':
        rctype = 2
    elif type == 'exe':
        rctype = 1
    else:
        raise ValueError('Type %s not supported' % type)
    return '#include "winuser.h"\n%d RT_MANIFEST %s' % (
     rctype, name)


def check_embedded_msvcr_match_linked(msver):
    """msver is the ms runtime version used for the MANIFEST."""
    maj = msvc_runtime_major()
    if maj:
        if not maj == int(msver):
            raise ValueError('Discrepancy between linked msvcr (%d) and the one about to be embedded (%d)' % (
             int(msver), maj))


def configtest_name(config):
    base = os.path.basename(config._gen_temp_sourcefile('yo', [], 'c'))
    return os.path.splitext(base)[0]


def manifest_name(config):
    root = configtest_name(config)
    exext = config.compiler.exe_extension
    return root + exext + '.manifest'


def rc_name(config):
    root = configtest_name(config)
    return root + '.rc'


def generate_manifest(config):
    msver = get_build_msvc_version()
    if msver is not None:
        if msver >= 8:
            check_embedded_msvcr_match_linked(msver)
            ma = int(msver)
            mi = int((msver - ma) * 10)
            manxml = msvc_manifest_xml(ma, mi)
            man = open(manifest_name(config), 'w')
            config.temp_files.append(manifest_name(config))
            man.write(manxml)
            man.close()