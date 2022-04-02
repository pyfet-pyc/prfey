# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\command\sdist.py
from distutils import log
import distutils.command.sdist as orig
import os, sys, io, contextlib
from setuptools.extern import ordered_set
from .py36compat import sdist_add_defaults
import pkg_resources
_default_revctrl = list

def walk_revctrl(dirname=''):
    """Find all files under revision control"""
    for ep in pkg_resources.iter_entry_points('setuptools.file_finders'):
        for item in ep.load()(dirname):
            yield item


class sdist(sdist_add_defaults, orig.sdist):
    __doc__ = 'Smart sdist that finds anything supported by revision control'
    user_options = [
     ('formats=', None, 'formats for source distribution (comma-separated list)'),
     ('keep-temp', 'k', 'keep the distribution tree around after creating archive file(s)'),
     ('dist-dir=', 'd', 'directory to put the source distribution archive(s) in [default: dist]')]
    negative_opt = {}
    README_EXTENSIONS = [
     '', '.rst', '.txt', '.md']
    READMES = tuple(('README{0}'.format(ext) for ext in README_EXTENSIONS))

    def run(self):
        self.run_command('egg_info')
        ei_cmd = self.get_finalized_command('egg_info')
        self.filelist = ei_cmd.filelist
        self.filelist.append(os.path.join(ei_cmd.egg_info, 'SOURCES.txt'))
        self.check_readme()
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)
        else:
            self.make_distribution()
            dist_files = getattr(self.distribution, 'dist_files', [])
            for file in self.archive_files:
                data = (
                 'sdist', '', file)
                if data not in dist_files:
                    dist_files.append(data)

    def initialize_options(self):
        orig.sdist.initialize_options(self)
        self._default_to_gztar()

    def _default_to_gztar(self):
        if sys.version_info >= (3, 6, 0, 'beta', 1):
            return
        self.formats = [
         'gztar']

    def make_distribution(self):
        """
        Workaround for #516
        """
        with self._remove_os_link():
            orig.sdist.make_distribution(self)

    @staticmethod
    @contextlib.contextmanager
    def _remove_os_link():
        """
        In a context, remove and restore os.link if it exists
        """

        class NoValue:
            pass

        orig_val = getattr(os, 'link', NoValue)
        try:
            del os.link
        except Exception:
            pass
        else:
            try:
                yield
            finally:
                if orig_val is not NoValue:
                    setattr(os, 'link', orig_val)

    def _add_defaults_optional(self):
        super()._add_defaults_optional()
        if os.path.isfile('pyproject.toml'):
            self.filelist.append('pyproject.toml')

    def _add_defaults_python(self):
        """getting python files"""
        if self.distribution.has_pure_modules():
            build_py = self.get_finalized_command('build_py')
            self.filelist.extend(build_py.get_source_files())
            self._add_data_files(self._safe_data_files(build_py))

    def _safe_data_files(self, build_py):
        """
        Extracting data_files from build_py is known to cause
        infinite recursion errors when `include_package_data`
        is enabled, so suppress it in that case.
        """
        if self.distribution.include_package_data:
            return ()
        return build_py.data_files

    def _add_data_files(self, data_files):
        """
        Add data files as found in build_py.data_files.
        """
        self.filelist.extend((os.path.join(src_dir, name) for _, src_dir, _, filenames in data_files for name in filenames))

    def _add_defaults_data_files(self):
        try:
            super()._add_defaults_data_files()
        except TypeError:
            log.warn('data_files contains unexpected objects')

    def check_readme(self):
        for f in self.READMES:
            if os.path.exists(f):
                return None
        else:
            self.warn('standard file not found: should have one of ' + ', '.join(self.READMES))

    def make_release_tree(self, base_dir, files):
        orig.sdist.make_release_tree(self, base_dir, files)
        dest = os.path.join(base_dir, 'setup.cfg')
        if hasattr(os, 'link'):
            if os.path.exists(dest):
                os.unlink(dest)
                self.copy_file('setup.cfg', dest)
        self.get_finalized_command('egg_info').save_version_info(dest)

    def _manifest_is_not_generated(self):
        if not os.path.isfile(self.manifest):
            return False
        with io.open(self.manifest, 'rb') as fp:
            first_line = fp.readline()
        return first_line != '# file GENERATED by distutils, do NOT edit\n'.encode()

    def read_manifest--- This code section failed: ---

 L. 177         0  LOAD_GLOBAL              log
                2  LOAD_METHOD              info
                4  LOAD_STR                 "reading manifest file '%s'"
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                manifest
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          

 L. 178        14  LOAD_GLOBAL              open
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                manifest
               20  LOAD_STR                 'rb'
               22  CALL_FUNCTION_2       2  ''
               24  STORE_FAST               'manifest'

 L. 179        26  LOAD_FAST                'manifest'
               28  GET_ITER         
             30_0  COME_FROM           124  '124'
             30_1  COME_FROM           110  '110'
             30_2  COME_FROM           104  '104'
             30_3  COME_FROM            80  '80'
               30  FOR_ITER            126  'to 126'
               32  STORE_FAST               'line'

 L. 181        34  SETUP_FINALLY        50  'to 50'

 L. 182        36  LOAD_FAST                'line'
               38  LOAD_METHOD              decode
               40  LOAD_STR                 'UTF-8'
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'line'
               46  POP_BLOCK        
               48  JUMP_FORWARD         88  'to 88'
             50_0  COME_FROM_FINALLY    34  '34'

 L. 183        50  DUP_TOP          
               52  LOAD_GLOBAL              UnicodeDecodeError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    86  'to 86'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 184        64  LOAD_GLOBAL              log
               66  LOAD_METHOD              warn
               68  LOAD_STR                 '%r not UTF-8 decodable -- skipping'
               70  LOAD_FAST                'line'
               72  BINARY_MODULO    
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L. 185        78  POP_EXCEPT       
               80  JUMP_BACK            30  'to 30'
               82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
             86_0  COME_FROM            56  '56'
               86  END_FINALLY      
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            48  '48'

 L. 187        88  LOAD_FAST                'line'
               90  LOAD_METHOD              strip
               92  CALL_METHOD_0         0  ''
               94  STORE_FAST               'line'

 L. 188        96  LOAD_FAST                'line'
               98  LOAD_METHOD              startswith
              100  LOAD_STR                 '#'
              102  CALL_METHOD_1         1  ''
              104  POP_JUMP_IF_TRUE_BACK    30  'to 30'
              106  LOAD_FAST                'line'
              108  POP_JUMP_IF_TRUE    112  'to 112'

 L. 189       110  JUMP_BACK            30  'to 30'
            112_0  COME_FROM           108  '108'

 L. 190       112  LOAD_FAST                'self'
              114  LOAD_ATTR                filelist
              116  LOAD_METHOD              append
              118  LOAD_FAST                'line'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
              124  JUMP_BACK            30  'to 30'
            126_0  COME_FROM            30  '30'

 L. 191       126  LOAD_FAST                'manifest'
              128  LOAD_METHOD              close
              130  CALL_METHOD_0         0  ''
              132  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 86_0

    def check_license(self):
        """Checks if license_file' or 'license_files' is configured and adds any
        valid paths to 'self.filelist'.
        """
        files = ordered_set.OrderedSet()
        opts = self.distribution.get_option_dict('metadata')
        _, license_file = opts.get('license_file', (None, None))
        if license_file is None:
            log.debug("'license_file' option was not specified")
        else:
            files.add(license_file)
        try:
            files.update(self.distribution.metadata.license_files)
        except TypeError:
            log.warn("warning: 'license_files' option is malformed")

        for f in files:
            if not os.path.exists(f):
                log.warn("warning: Failed to find the configured license file '%s'", f)
                files.remove(f)
        else:
            self.filelist.extend(files)