# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\command\bdist_egg.py
"""setuptools.command.bdist_egg

Build .egg distributions"""
from distutils.errors import DistutilsSetupError
from distutils.dir_util import remove_tree, mkpath
from distutils import log
from types import CodeType
import sys, os, re, textwrap, marshal, warnings
from setuptools.extern import six
from pkg_resources import get_build_platform, Distribution, ensure_directory
from pkg_resources import EntryPoint
from setuptools.extension import Library
from setuptools import Command, SetuptoolsDeprecationWarning
try:
    from sysconfig import get_path, get_python_version

    def _get_purelib():
        return get_path('purelib')


except ImportError:
    from distutils.sysconfig import get_python_lib, get_python_version

    def _get_purelib():
        return get_python_lib(False)


else:

    def strip_module(filename):
        if '.' in filename:
            filename = os.path.splitext(filename)[0]
        if filename.endswith('module'):
            filename = filename[:-6]
        return filename


    def sorted_walk(dir):
        """Do os.walk in a reproducible way,
    independent of indeterministic filesystem readdir order
    """
        for base, dirs, files in os.walk(dir):
            dirs.sort()
            files.sort()
            yield (base, dirs, files)


    def write_stub(resource, pyfile):
        _stub_template = textwrap.dedent('\n        def __bootstrap__():\n            global __bootstrap__, __loader__, __file__\n            import sys, pkg_resources\n            from importlib.machinery import ExtensionFileLoader\n            __file__ = pkg_resources.resource_filename(__name__, %r)\n            __loader__ = None; del __bootstrap__, __loader__\n            ExtensionFileLoader(__name__,__file__).load_module()\n        __bootstrap__()\n        ').lstrip()
        with open(pyfile, 'w') as f:
            f.write(_stub_template % resource)


    class bdist_egg(Command):
        description = 'create an "egg" distribution'
        user_options = [
         ('bdist-dir=', 'b', 'temporary directory for creating the distribution'),
         (
          'plat-name=', 'p',
          'platform name to embed in generated filenames (default: %s)' % get_build_platform()),
         ('exclude-source-files', None, 'remove all .py files from the generated egg'),
         ('keep-temp', 'k', 'keep the pseudo-installation tree around after creating the distribution archive'),
         ('dist-dir=', 'd', 'directory to put final built distributions in'),
         ('skip-build', None, 'skip rebuilding everything (for testing/debugging)')]
        boolean_options = [
         'keep-temp', 'skip-build', 'exclude-source-files']

        def initialize_options(self):
            self.bdist_dir = None
            self.plat_name = None
            self.keep_temp = 0
            self.dist_dir = None
            self.skip_build = 0
            self.egg_output = None
            self.exclude_source_files = None

        def finalize_options(self):
            ei_cmd = self.ei_cmd = self.get_finalized_command('egg_info')
            self.egg_info = ei_cmd.egg_info
            if self.bdist_dir is None:
                bdist_base = self.get_finalized_command('bdist').bdist_base
                self.bdist_dir = os.path.join(bdist_base, 'egg')
            if self.plat_name is None:
                self.plat_name = get_build_platform()
            self.set_undefined_options('bdist', ('dist_dir', 'dist_dir'))
            if self.egg_output is None:
                basename = Distribution(None, None, ei_cmd.egg_name, ei_cmd.egg_version, get_python_version(), self.distribution.has_ext_modules() and self.plat_name).egg_name()
                self.egg_output = os.path.join(self.dist_dir, basename + '.egg')

        def do_install_data(self):
            self.get_finalized_command('install').install_lib = self.bdist_dir
            site_packages = os.path.normcase(os.path.realpath(_get_purelib()))
            old, self.distribution.data_files = self.distribution.data_files, []
            for item in old:
                if isinstance(item, tuple):
                    if len(item) == 2 and os.path.isabs(item[0]):
                        realpath = os.path.realpath(item[0])
                        normalized = os.path.normcase(realpath)
                        if normalized == site_packages or (normalized.startswith(site_packages + os.sep)):
                            item = (realpath[len(site_packages) + 1:], item[1])
                        self.distribution.data_files.append(item)
                    else:
                        try:
                            log.info('installing package data to %s', self.bdist_dir)
                            self.call_command('install_data', force=0, root=None)
                        finally:
                            self.distribution.data_files = old

        def get_outputs(self):
            return [
             self.egg_output]

        def call_command(self, cmdname, **kw):
            """Invoke reinitialized command `cmdname` with keyword args"""
            for dirname in INSTALL_DIRECTORY_ATTRS:
                kw.setdefault(dirname, self.bdist_dir)
            else:
                kw.setdefault('skip_build', self.skip_build)
                kw.setdefault('dry_run', self.dry_run)
                cmd = (self.reinitialize_command)(cmdname, **kw)
                self.run_command(cmdname)
                return cmd

        def run(self):
            self.run_command('egg_info')
            log.info('installing library code to %s', self.bdist_dir)
            instcmd = self.get_finalized_command('install')
            old_root = instcmd.root
            instcmd.root = None
            if self.distribution.has_c_libraries():
                if not self.skip_build:
                    self.run_command('build_clib')
            cmd = self.call_command('install_lib', warn_dir=0)
            instcmd.root = old_root
            all_outputs, ext_outputs = self.get_ext_outputs()
            self.stubs = []
            to_compile = []
            for p, ext_name in enumerate(ext_outputs):
                filename, ext = os.path.splitext(ext_name)
                pyfile = os.path.join(self.bdist_dir, strip_module(filename) + '.py')
                self.stubs.append(pyfile)
                log.info('creating stub loader for %s', ext_name)
                if not self.dry_run:
                    write_stub(os.path.basename(ext_name), pyfile)
                else:
                    to_compile.append(pyfile)
                    ext_outputs[p] = ext_name.replace(os.sep, '/')
            else:
                if to_compile:
                    cmd.byte_compile(to_compile)
                if self.distribution.data_files:
                    self.do_install_data()
                archive_root = self.bdist_dir
                egg_info = os.path.join(archive_root, 'EGG-INFO')
                self.mkpath(egg_info)
                if self.distribution.scripts:
                    script_dir = os.path.join(egg_info, 'scripts')
                    log.info('installing scripts to %s', script_dir)
                    self.call_command('install_scripts', install_dir=script_dir, no_ep=1)
                self.copy_metadata_to(egg_info)
                native_libs = os.path.join(egg_info, 'native_libs.txt')
                if all_outputs:
                    log.info('writing %s', native_libs)
                    if not self.dry_run:
                        ensure_directory(native_libs)
                        libs_file = open(native_libs, 'wt')
                        libs_file.write('\n'.join(all_outputs))
                        libs_file.write('\n')
                        libs_file.close()
                else:
                    pass
                if os.path.isfile(native_libs):
                    log.info('removing %s', native_libs)
                    if not self.dry_run:
                        os.unlink(native_libs)
                    write_safety_flag(os.path.join(archive_root, 'EGG-INFO'), self.zip_safe())
                    if os.path.exists(os.path.join(self.egg_info, 'depends.txt')):
                        log.warn("WARNING: 'depends.txt' will not be used by setuptools 0.6!\nUse the install_requires/extras_require setup() args instead.")
                    if self.exclude_source_files:
                        self.zap_pyfiles()
                    make_zipfile((self.egg_output), archive_root, verbose=(self.verbose), dry_run=(self.dry_run),
                      mode=(self.gen_header()))
                    self.keep_temp or remove_tree((self.bdist_dir), dry_run=(self.dry_run))
                getattr(self.distribution, 'dist_files', []).append((
                 'bdist_egg', get_python_version(), self.egg_output))

        def zap_pyfiles--- This code section failed: ---

 L. 245         0  LOAD_GLOBAL              log
                2  LOAD_METHOD              info
                4  LOAD_STR                 'Removing .py files from temporary directory'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 246        10  LOAD_GLOBAL              walk_egg
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                bdist_dir
               16  CALL_FUNCTION_1       1  ''
               18  GET_ITER         
             20_0  COME_FROM           210  '210'
               20  FOR_ITER            212  'to 212'
               22  UNPACK_SEQUENCE_3     3 
               24  STORE_FAST               'base'
               26  STORE_FAST               'dirs'
               28  STORE_FAST               'files'

 L. 247        30  LOAD_FAST                'files'
               32  GET_ITER         
             34_0  COME_FROM           208  '208'
             34_1  COME_FROM            92  '92'
               34  FOR_ITER            210  'to 210'
               36  STORE_FAST               'name'

 L. 248        38  LOAD_GLOBAL              os
               40  LOAD_ATTR                path
               42  LOAD_METHOD              join
               44  LOAD_FAST                'base'
               46  LOAD_FAST                'name'
               48  CALL_METHOD_2         2  ''
               50  STORE_FAST               'path'

 L. 250        52  LOAD_FAST                'name'
               54  LOAD_METHOD              endswith
               56  LOAD_STR                 '.py'
               58  CALL_METHOD_1         1  ''
               60  POP_JUMP_IF_FALSE    84  'to 84'

 L. 251        62  LOAD_GLOBAL              log
               64  LOAD_METHOD              debug
               66  LOAD_STR                 'Deleting %s'
               68  LOAD_FAST                'path'
               70  CALL_METHOD_2         2  ''
               72  POP_TOP          

 L. 252        74  LOAD_GLOBAL              os
               76  LOAD_METHOD              unlink
               78  LOAD_FAST                'path'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
             84_0  COME_FROM            60  '60'

 L. 254        84  LOAD_FAST                'base'
               86  LOAD_METHOD              endswith
               88  LOAD_STR                 '__pycache__'
               90  CALL_METHOD_1         1  ''
               92  POP_JUMP_IF_FALSE_BACK    34  'to 34'

 L. 255        94  LOAD_FAST                'path'
               96  STORE_FAST               'path_old'

 L. 257        98  LOAD_STR                 '(?P<name>.+)\\.(?P<magic>[^.]+)\\.pyc'
              100  STORE_FAST               'pattern'

 L. 258       102  LOAD_GLOBAL              re
              104  LOAD_METHOD              match
              106  LOAD_FAST                'pattern'
              108  LOAD_FAST                'name'
              110  CALL_METHOD_2         2  ''
              112  STORE_FAST               'm'

 L. 259       114  LOAD_GLOBAL              os
              116  LOAD_ATTR                path
              118  LOAD_METHOD              join

 L. 260       120  LOAD_FAST                'base'

 L. 260       122  LOAD_GLOBAL              os
              124  LOAD_ATTR                pardir

 L. 260       126  LOAD_FAST                'm'
              128  LOAD_METHOD              group
              130  LOAD_STR                 'name'
              132  CALL_METHOD_1         1  ''
              134  LOAD_STR                 '.pyc'
              136  BINARY_ADD       

 L. 259       138  CALL_METHOD_3         3  ''
              140  STORE_FAST               'path_new'

 L. 261       142  LOAD_GLOBAL              log
              144  LOAD_METHOD              info

 L. 262       146  LOAD_STR                 'Renaming file from [%s] to [%s]'

 L. 263       148  LOAD_FAST                'path_old'
              150  LOAD_FAST                'path_new'
              152  BUILD_TUPLE_2         2 

 L. 262       154  BINARY_MODULO    

 L. 261       156  CALL_METHOD_1         1  ''
              158  POP_TOP          

 L. 264       160  SETUP_FINALLY       176  'to 176'

 L. 265       162  LOAD_GLOBAL              os
              164  LOAD_METHOD              remove
              166  LOAD_FAST                'path_new'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
              172  POP_BLOCK        
              174  JUMP_FORWARD        196  'to 196'
            176_0  COME_FROM_FINALLY   160  '160'

 L. 266       176  DUP_TOP          
              178  LOAD_GLOBAL              OSError
              180  COMPARE_OP               exception-match
              182  POP_JUMP_IF_FALSE   194  'to 194'
              184  POP_TOP          
              186  POP_TOP          
              188  POP_TOP          

 L. 267       190  POP_EXCEPT       
              192  BREAK_LOOP          196  'to 196'
            194_0  COME_FROM           182  '182'
              194  END_FINALLY      
            196_0  COME_FROM           192  '192'
            196_1  COME_FROM           174  '174'

 L. 268       196  LOAD_GLOBAL              os
              198  LOAD_METHOD              rename
              200  LOAD_FAST                'path_old'
              202  LOAD_FAST                'path_new'
              204  CALL_METHOD_2         2  ''
              206  POP_TOP          
              208  JUMP_BACK            34  'to 34'
            210_0  COME_FROM            34  '34'
              210  JUMP_BACK            20  'to 20'
            212_0  COME_FROM            20  '20'

Parse error at or near `END_FINALLY' instruction at offset 194

        def zip_safe(self):
            safe = getattr(self.distribution, 'zip_safe', None)
            if safe is not None:
                return safe
            log.warn('zip_safe flag not set; analyzing archive contents...')
            return analyze_egg(self.bdist_dir, self.stubs)

        def gen_header(self):
            epm = EntryPoint.parse_map(self.distribution.entry_points or '')
            ep = epm.get('setuptools.installation', {}).get('eggsecutable')
            if ep is None:
                return 'w'
            warnings.warn('Eggsecutables are deprecated and will be removed in a future version.', SetuptoolsDeprecationWarning)
            if not ep.attrs or ep.extras:
                raise DistutilsSetupError("eggsecutable entry point (%r) cannot have 'extras' or refer to a module" % (
                 ep,))
            pyver = ('{}.{}'.format)(*sys.version_info)
            pkg = ep.module_name
            full = '.'.join(ep.attrs)
            base = ep.attrs[0]
            basename = os.path.basename(self.egg_output)
            header = '#!/bin/sh\nif [ `basename $0` = "%(basename)s" ]\nthen exec python%(pyver)s -c "import sys, os; sys.path.insert(0, os.path.abspath(\'$0\')); from %(pkg)s import %(base)s; sys.exit(%(full)s())" "$@"\nelse\n  echo $0 is not the correct name for this egg file.\n  echo Please rename it back to %(basename)s and try again.\n  exec false\nfi\n' % locals()
            if not self.dry_run:
                mkpath((os.path.dirname(self.egg_output)), dry_run=(self.dry_run))
                f = open(self.egg_output, 'w')
                f.write(header)
                f.close()
            return 'a'

        def copy_metadata_to(self, target_dir):
            """Copy metadata (egg info) to the target_dir"""
            norm_egg_info = os.path.normpath(self.egg_info)
            prefix = os.path.join(norm_egg_info, '')
            for path in self.ei_cmd.filelist.files:
                if path.startswith(prefix):
                    target = os.path.join(target_dir, path[len(prefix):])
                    ensure_directory(target)
                    self.copy_file(path, target)

        def get_ext_outputs(self):
            """Get a list of relative paths to C extensions in the output distro"""
            all_outputs = []
            ext_outputs = []
            paths = {self.bdist_dir: ''}
            for base, dirs, files in sorted_walk(self.bdist_dir):
                for filename in files:
                    if os.path.splitext(filename)[1].lower() in NATIVE_EXTENSIONS:
                        all_outputs.append(paths[base] + filename)
                else:
                    for filename in dirs:
                        paths[os.path.join(base, filename)] = paths[base] + filename + '/'

            else:
                if self.distribution.has_ext_modules():
                    build_cmd = self.get_finalized_command('build_ext')
                    for ext in build_cmd.extensions:
                        if isinstance(ext, Library):
                            pass
                        else:
                            fullname = build_cmd.get_ext_fullname(ext.name)
                            filename = build_cmd.get_ext_filename(fullname)
                            if not os.path.basename(filename).startswith('dl-'):
                                if os.path.exists(os.path.join(self.bdist_dir, filename)):
                                    ext_outputs.append(filename)

                    return (
                     all_outputs, ext_outputs)


    NATIVE_EXTENSIONS = dict.fromkeys('.dll .so .dylib .pyd'.split())

    def walk_egg(egg_dir):
        """Walk an unpacked egg's contents, skipping the metadata directory"""
        walker = sorted_walk(egg_dir)
        base, dirs, files = next(walker)
        if 'EGG-INFO' in dirs:
            dirs.remove('EGG-INFO')
        yield (
         base, dirs, files)
        for bdf in walker:
            yield bdf


    def analyze_egg(egg_dir, stubs):
        for flag, fn in safety_flags.items():
            if os.path.exists(os.path.joinegg_dir'EGG-INFO'fn):
                return flag
        else:
            if not can_scan():
                return False
            safe = True
            for base, dirs, files in walk_egg(egg_dir):
                for name in files:
                    if not name.endswith('.py'):
                        if name.endswith('.pyw'):
                            continue
                        else:
                            if not name.endswith('.pyc'):
                                if name.endswith('.pyo'):
                                    pass
                            safe = scan_module(egg_dir, base, name, stubs) and safe

                return safe


    def write_safety_flag(egg_dir, safe):
        for flag, fn in safety_flags.items():
            fn = os.path.join(egg_dir, fn)
            if os.path.exists(fn):
                if not safe is None or bool(safe) != flag:
                    os.unlink(fn)
                else:
                    if safe is not None:
                        if bool(safe) == flag:
                            f = open(fn, 'wt')
                            f.write('\n')
                            f.close()


    safety_flags = {True:'zip-safe', 
     False:'not-zip-safe'}

    def scan_module(egg_dir, base, name, stubs):
        """Check whether module possibly uses unsafe-for-zipfile stuff"""
        filename = os.path.join(base, name)
        if filename[:-1] in stubs:
            return True
        pkg = base[len(egg_dir) + 1:].replace(os.sep, '.')
        module = pkg + pkg and '.' or '' + os.path.splitext(name)[0]
        if six.PY2:
            skip = 8
        elif sys.version_info < (3, 7):
            skip = 12
        else:
            skip = 16
        f = open(filename, 'rb')
        f.read(skip)
        code = marshal.load(f)
        f.close()
        safe = True
        symbols = dict.fromkeys(iter_symbols(code))
        for bad in ('__file__', '__path__'):
            if bad in symbols:
                log.warn'%s: module references %s'modulebad
                safe = False
        else:
            if 'inspect' in symbols:
                for bad in ('getsource', 'getabsfile', 'getsourcefile', 'getfilegetsourcelines',
                            'findsource', 'getcomments', 'getframeinfo', 'getinnerframes',
                            'getouterframes', 'stack', 'trace'):
                    if bad in symbols:
                        log.warn'%s: module MAY be using inspect.%s'modulebad
                        safe = False

                return safe


    def iter_symbols(code):
        """Yield names and strings used by `code` and its nested code objects"""
        for name in code.co_names:
            yield name
        else:
            for const in code.co_consts:
                if isinstance(const, six.string_types):
                    yield const
                else:
                    if isinstance(const, CodeType):
                        for name in iter_symbols(const):
                            yield name


    def can_scan():
        if not sys.platform.startswith('java'):
            if sys.platform != 'cli':
                return True
        log.warn('Unable to analyze compiled code on this platform.')
        log.warn("Please ask the author to include a 'zip_safe' setting (either True or False) in the package's setup.py")


    INSTALL_DIRECTORY_ATTRS = [
     'install_lib', 'install_dir', 'install_data', 'install_base']

    def make_zipfile(zip_filename, base_dir, verbose=0, dry_run=0, compress=True, mode='w'):
        """Create a zip file from all the files under 'base_dir'.  The output
    zip file will be named 'base_dir' + ".zip".  Uses either the "zipfile"
    Python module (if available) or the InfoZIP "zip" utility (if installed
    and found on the default search path).  If neither tool is available,
    raises DistutilsExecError.  Returns the name of the output zip file.
    """
        import zipfile
        mkpath((os.path.dirname(zip_filename)), dry_run=dry_run)
        log.info"creating '%s' and adding '%s' to it"zip_filenamebase_dir

        def visit(z, dirname, names):
            for name in names:
                path = os.path.normpath(os.path.join(dirname, name))
                if os.path.isfile(path):
                    p = path[len(base_dir) + 1:]
                    if not dry_run:
                        z.write(path, p)
                    else:
                        log.debug("adding '%s'", p)

        compression = zipfile.ZIP_DEFLATED if compress else zipfile.ZIP_STORED
        if not dry_run:
            z = zipfile.ZipFile(zip_filename, mode, compression=compression)
            for dirname, dirs, files in sorted_walk(base_dir):
                visit(z, dirname, files)
            else:
                z.close()

        else:
            pass
        for dirname, dirs, files in sorted_walk(base_dir):
            visit(None, dirname, files)
        else:
            return zip_filename