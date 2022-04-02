# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\command\py36compat.py
import os
from glob import glob
from distutils.util import convert_path
from distutils.command import sdist
from setuptools.extern.six.moves import filter

class sdist_add_defaults:
    __doc__ = '\n    Mix-in providing forward-compatibility for functionality as found in\n    distutils on Python 3.7.\n\n    Do not edit the code in this class except to update functionality\n    as implemented in distutils. Instead, override in the subclass.\n    '

    def add_defaults(self):
        """Add all the default files to self.filelist:
          - README or README.txt
          - setup.py
          - test/test*.py
          - all pure Python modules mentioned in setup script
          - all files pointed by package_data (build_py)
          - all files defined in data_files.
          - all files defined as scripts.
          - all C sources listed as part of extensions or C libraries
            in the setup script (doesn't catch C headers!)
        Warns if (README or README.txt) or setup.py are missing; everything
        else is optional.
        """
        self._add_defaults_standards()
        self._add_defaults_optional()
        self._add_defaults_python()
        self._add_defaults_data_files()
        self._add_defaults_ext()
        self._add_defaults_c_libs()
        self._add_defaults_scripts()

    @staticmethod
    def _cs_path_exists--- This code section failed: ---

 L.  50         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              exists
                6  LOAD_FAST                'fspath'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L.  51        12  LOAD_CONST               False
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L.  53        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              abspath
               22  LOAD_FAST                'fspath'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'abspath'

 L.  54        28  LOAD_GLOBAL              os
               30  LOAD_ATTR                path
               32  LOAD_METHOD              split
               34  LOAD_FAST                'abspath'
               36  CALL_METHOD_1         1  ''
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'directory'
               42  STORE_FAST               'filename'

 L.  55        44  LOAD_FAST                'filename'
               46  LOAD_GLOBAL              os
               48  LOAD_METHOD              listdir
               50  LOAD_FAST                'directory'
               52  CALL_METHOD_1         1  ''
               54  <118>                 0  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 54

    def _add_defaults_standards(self):
        standards = [
         self.READMES, self.distribution.script_name]
        for fn in standards:
            if isinstance(fn, tuple):
                alts = fn
                got_it = False
                for fn in alts:
                    if self._cs_path_existsfn:
                        got_it = True
                        self.filelist.appendfn
                        break

                if not got_it:
                    self.warn('standard file not found: should have one of ' + ', '.joinalts)
                else:
                    if self._cs_path_existsfn:
                        self.filelist.appendfn
            else:
                self.warn("standard file '%s' not found" % fn)

    def _add_defaults_optional(self):
        optional = [
         'test/test*.py', 'setup.cfg']
        for pattern in optional:
            files = filter(os.path.isfile, glob(pattern))
            self.filelist.extendfiles

    def _add_defaults_python(self):
        build_py = self.get_finalized_command'build_py'
        if self.distribution.has_pure_modules():
            self.filelist.extendbuild_py.get_source_files()
        for pkg, src_dir, build_dir, filenames in build_py.data_files:
            for filename in filenames:
                self.filelist.appendos.path.join(src_dir, filename)

    def _add_defaults_data_files(self):
        if self.distribution.has_data_files():
            for item in self.distribution.data_files:
                if isinstance(item, str):
                    item = convert_path(item)
                    if os.path.isfileitem:
                        self.filelist.appenditem
                else:
                    dirname, filenames = item

            for f in filenames:
                f = convert_path(f)
                if os.path.isfilef:
                    self.filelist.appendf

    def _add_defaults_ext(self):
        if self.distribution.has_ext_modules():
            build_ext = self.get_finalized_command'build_ext'
            self.filelist.extendbuild_ext.get_source_files()

    def _add_defaults_c_libs(self):
        if self.distribution.has_c_libraries():
            build_clib = self.get_finalized_command'build_clib'
            self.filelist.extendbuild_clib.get_source_files()

    def _add_defaults_scripts(self):
        if self.distribution.has_scripts():
            build_scripts = self.get_finalized_command'build_scripts'
            self.filelist.extendbuild_scripts.get_source_files()


if hasattr(sdist.sdist, '_add_defaults_standards'):

    class sdist_add_defaults:
        pass