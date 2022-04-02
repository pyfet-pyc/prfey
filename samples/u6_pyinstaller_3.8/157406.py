# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\setuptools\command\sdist.py
from distutils import log
import distutils.command.sdist as orig
import os, sys, io, contextlib
from setuptools.extern import six
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

    def __read_template_hack(self):
        try:
            orig.sdist.read_template(self)
        except Exception:
            _, _, tb = sys.exc_info()
            tb.tb_next.tb_frame.f_locals['template'].close()
            raise

    has_leaky_handle = sys.version_info < (2, 7, 2) or (3, 0) <= sys.version_info < (3,
                                                                                     1,
                                                                                     4) or (3,
                                                                                            2) <= sys.version_info < (3,
                                                                                                                      2,
                                                                                                                      1)
    if has_leaky_handle:
        read_template = _sdist__read_template_hack

    def _add_defaults_python(self):
        """getting python files"""
        if self.distribution.has_pure_modules():
            build_py = self.get_finalized_command('build_py')
            self.filelist.extend(build_py.get_source_files())
            if not self.distribution.include_package_data:
                for _, src_dir, _, filenames in build_py.data_files:
                    self.filelist.extend([os.path.join(src_dir, filename) for filename in filenames])

    def _add_defaults_data_files(self):
        try:
            if six.PY2:
                sdist_add_defaults._add_defaults_data_files(self)
            else:
                super()._add_defaults_data_files()
        except TypeError:
            log.warn('data_files contains unexpected objects')

    def check_readme(self):
        for f in self.READMES:
            if os.path.exists(f):
                return
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
        with io.open(self.manifest, 'rb') as (fp):
            first_line = fp.readline()
        return first_line != '# file GENERATED by distutils, do NOT edit\n'.encode()

    def read_manifest--- This code section failed: ---

 L. 185         0  LOAD_GLOBAL              log
                2  LOAD_METHOD              info
                4  LOAD_STR                 "reading manifest file '%s'"
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                manifest
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          

 L. 186        14  LOAD_GLOBAL              open
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                manifest
               20  LOAD_STR                 'rb'
               22  CALL_FUNCTION_2       2  ''
               24  STORE_FAST               'manifest'

 L. 187        26  LOAD_FAST                'manifest'
               28  GET_ITER         
             30_0  COME_FROM           110  '110'
               30  FOR_ITER            132  'to 132'
               32  STORE_FAST               'line'

 L. 189        34  LOAD_GLOBAL              six
               36  LOAD_ATTR                PY3
               38  POP_JUMP_IF_FALSE    94  'to 94'

 L. 190        40  SETUP_FINALLY        56  'to 56'

 L. 191        42  LOAD_FAST                'line'
               44  LOAD_METHOD              decode
               46  LOAD_STR                 'UTF-8'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'line'
               52  POP_BLOCK        
               54  JUMP_FORWARD         94  'to 94'
             56_0  COME_FROM_FINALLY    40  '40'

 L. 192        56  DUP_TOP          
               58  LOAD_GLOBAL              UnicodeDecodeError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    92  'to 92'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 193        70  LOAD_GLOBAL              log
               72  LOAD_METHOD              warn
               74  LOAD_STR                 '%r not UTF-8 decodable -- skipping'
               76  LOAD_FAST                'line'
               78  BINARY_MODULO    
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          

 L. 194        84  POP_EXCEPT       
               86  JUMP_BACK            30  'to 30'
               88  POP_EXCEPT       
               90  JUMP_FORWARD         94  'to 94'
             92_0  COME_FROM            62  '62'
               92  END_FINALLY      
             94_0  COME_FROM            90  '90'
             94_1  COME_FROM            54  '54'
             94_2  COME_FROM            38  '38'

 L. 196        94  LOAD_FAST                'line'
               96  LOAD_METHOD              strip
               98  CALL_METHOD_0         0  ''
              100  STORE_FAST               'line'

 L. 197       102  LOAD_FAST                'line'
              104  LOAD_METHOD              startswith
              106  LOAD_STR                 '#'
              108  CALL_METHOD_1         1  ''
              110  POP_JUMP_IF_TRUE     30  'to 30'
              112  LOAD_FAST                'line'
              114  POP_JUMP_IF_TRUE    118  'to 118'

 L. 198       116  JUMP_BACK            30  'to 30'
            118_0  COME_FROM           114  '114'

 L. 199       118  LOAD_FAST                'self'
              120  LOAD_ATTR                filelist
              122  LOAD_METHOD              append
              124  LOAD_FAST                'line'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
              130  JUMP_BACK            30  'to 30'

 L. 200       132  LOAD_FAST                'manifest'
              134  LOAD_METHOD              close
              136  CALL_METHOD_0         0  ''
              138  POP_TOP          

Parse error at or near `POP_EXCEPT' instruction at offset 88

    def check_license(self):
        """Checks if license_file' is configured and adds it to
        'self.filelist' if the value contains a valid path.
        """
        opts = self.distribution.get_option_dict('metadata')
        _, license_file = opts.get('license_file', (None, None))
        if license_file is None:
            log.debug("'license_file' option was not specified")
            return None
        if not os.path.exists(license_file):
            log.warn("warning: Failed to find the configured license file '%s'", license_file)
            return None
        self.filelist.append(license_file)