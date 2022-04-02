# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\wheel.py
"""Wheels support."""
from distutils.util import get_platform
from distutils import log
import email, itertools, os, posixpath, re, zipfile, pkg_resources, setuptools
from pkg_resources import parse_version
from setuptools.extern.packaging.tags import sys_tags
from setuptools.extern.packaging.utils import canonicalize_name
from setuptools.command.egg_info import write_requirements
WHEEL_NAME = re.compile('^(?P<project_name>.+?)-(?P<version>\\d.*?)\n    ((-(?P<build>\\d.*?))?-(?P<py_version>.+?)-(?P<abi>.+?)-(?P<platform>.+?)\n    )\\.whl$', re.VERBOSE).match
NAMESPACE_PACKAGE_INIT = "__import__('pkg_resources').declare_namespace(__name__)\n"

def unpack(src_dir, dst_dir):
    """Move everything under `src_dir` to `dst_dir`, and delete the former."""
    for dirpath, dirnames, filenames in os.walk(src_dir):
        subdir = os.path.relpath(dirpath, src_dir)
        for f in filenames:
            src = os.path.join(dirpath, f)
            dst = os.path.join(dst_dir, subdir, f)
            os.renames(src, dst)

    else:
        for n, d in reversed(list(enumerate(dirnames))):
            src = os.path.join(dirpath, d)
            dst = os.path.join(dst_dir, subdir, d)
            if not os.path.exists(dst):
                os.renames(src, dst)
                del dirnames[n]
        else:
            for dirpath, dirnames, filenames in os.walk(src_dir, topdown=True):
                assert not filenames
                os.rmdir(dirpath)


class Wheel:

    def __init__(self, filename):
        match = WHEEL_NAME(os.path.basename(filename))
        if match is None:
            raise ValueError('invalid wheel name: %r' % filename)
        self.filename = filename
        for k, v in match.groupdict().items():
            setattr(self, k, v)

    def tags(self):
        """List tags (py_version, abi, platform) supported by this wheel."""
        return itertools.product(self.py_version.split('.'), self.abi.split('.'), self.platform.split('.'))

    def is_compatible(self):
        """Is the wheel is compatible with the current platform?"""
        supported_tags = set(((
         t.interpreter, t.abi, t.platform) for t in sys_tags()))
        return next((True for t in self.tags() if t in supported_tags), False)

    def egg_name(self):
        return pkg_resources.Distribution(project_name=(self.project_name),
          version=(self.version),
          platform=(None if self.platform == 'any' else get_platform())).egg_name() + '.egg'

    def get_dist_info(self, zf):
        for member in zf.namelist():
            dirname = posixpath.dirname(member)
            if dirname.endswith('.dist-info') and canonicalize_name(dirname).startswith(canonicalize_name(self.project_name)):
                return dirname
        else:
            raise ValueError('unsupported wheel format. .dist-info not found')

    def install_as_egg(self, destination_eggdir):
        """Install wheel as an egg directory."""
        with zipfile.ZipFile(self.filename) as (zf):
            self._install_as_egg(destination_eggdir, zf)

    def _install_as_egg(self, destination_eggdir, zf):
        dist_basename = '%s-%s' % (self.project_name, self.version)
        dist_info = self.get_dist_info(zf)
        dist_data = '%s.data' % dist_basename
        egg_info = os.path.join(destination_eggdir, 'EGG-INFO')
        self._convert_metadata(zf, destination_eggdir, dist_info, egg_info)
        self._move_data_entries(destination_eggdir, dist_data)
        self._fix_namespace_packages(egg_info, destination_eggdir)

    @staticmethod
    def _convert_metadata--- This code section failed: ---

 L. 109         0  LOAD_CLOSURE             'dist_info'
                2  LOAD_CLOSURE             'zf'
                4  BUILD_TUPLE_2         2 
                6  LOAD_CODE                <code_object get_metadata>
                8  LOAD_STR                 'Wheel._convert_metadata.<locals>.get_metadata'
               10  MAKE_FUNCTION_8          'closure'
               12  STORE_FAST               'get_metadata'

 L. 114        14  LOAD_FAST                'get_metadata'
               16  LOAD_STR                 'WHEEL'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'wheel_metadata'

 L. 116        22  LOAD_GLOBAL              parse_version
               24  LOAD_FAST                'wheel_metadata'
               26  LOAD_METHOD              get
               28  LOAD_STR                 'Wheel-Version'
               30  CALL_METHOD_1         1  ''
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'wheel_version'

 L. 118        36  LOAD_GLOBAL              parse_version
               38  LOAD_STR                 '1.0'
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_FAST                'wheel_version'
               44  DUP_TOP          
               46  ROT_THREE        
               48  COMPARE_OP               <=
               50  JUMP_IF_FALSE_OR_POP    62  'to 62'
               52  LOAD_GLOBAL              parse_version
               54  LOAD_STR                 '2.0dev0'
               56  CALL_FUNCTION_1       1  ''
               58  COMPARE_OP               <
               60  JUMP_FORWARD         66  'to 66'
             62_0  COME_FROM            50  '50'
               62  ROT_TWO          
               64  POP_TOP          
             66_0  COME_FROM            60  '60'

 L. 117        66  STORE_FAST               'wheel_v1'

 L. 120        68  LOAD_FAST                'wheel_v1'
               70  POP_JUMP_IF_TRUE     84  'to 84'

 L. 121        72  LOAD_GLOBAL              ValueError

 L. 122        74  LOAD_STR                 'unsupported wheel format version: %s'
               76  LOAD_FAST                'wheel_version'
               78  BINARY_MODULO    

 L. 121        80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            70  '70'

 L. 124        84  LOAD_GLOBAL              os
               86  LOAD_METHOD              mkdir
               88  LOAD_FAST                'destination_eggdir'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 125        94  LOAD_DEREF               'zf'
               96  LOAD_METHOD              extractall
               98  LOAD_FAST                'destination_eggdir'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          

 L. 127       104  LOAD_GLOBAL              os
              106  LOAD_ATTR                path
              108  LOAD_METHOD              join
              110  LOAD_FAST                'destination_eggdir'
              112  LOAD_DEREF               'dist_info'
              114  CALL_METHOD_2         2  ''
              116  STORE_DEREF              'dist_info'

 L. 128       118  LOAD_GLOBAL              pkg_resources
              120  LOAD_ATTR                Distribution
              122  LOAD_ATTR                from_location

 L. 129       124  LOAD_FAST                'destination_eggdir'

 L. 129       126  LOAD_DEREF               'dist_info'

 L. 130       128  LOAD_GLOBAL              pkg_resources
              130  LOAD_METHOD              PathMetadata
              132  LOAD_FAST                'destination_eggdir'
              134  LOAD_DEREF               'dist_info'
              136  CALL_METHOD_2         2  ''

 L. 128       138  LOAD_CONST               ('metadata',)
              140  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              142  STORE_DEREF              'dist'

 L. 136       144  LOAD_CODE                <code_object raw_req>
              146  LOAD_STR                 'Wheel._convert_metadata.<locals>.raw_req'
              148  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              150  STORE_DEREF              'raw_req'

 L. 139       152  LOAD_GLOBAL              list
              154  LOAD_GLOBAL              sorted
              156  LOAD_GLOBAL              map
              158  LOAD_DEREF               'raw_req'
              160  LOAD_DEREF               'dist'
              162  LOAD_METHOD              requires
              164  CALL_METHOD_0         0  ''
              166  CALL_FUNCTION_2       2  ''
              168  CALL_FUNCTION_1       1  ''
              170  CALL_FUNCTION_1       1  ''
              172  STORE_DEREF              'install_requires'

 L. 140       174  LOAD_CLOSURE             'dist'
              176  LOAD_CLOSURE             'install_requires'
              178  LOAD_CLOSURE             'raw_req'
              180  BUILD_TUPLE_3         3 
              182  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              184  LOAD_STR                 'Wheel._convert_metadata.<locals>.<dictcomp>'
              186  MAKE_FUNCTION_8          'closure'

 L. 146       188  LOAD_DEREF               'dist'
              190  LOAD_ATTR                extras

 L. 140       192  GET_ITER         
              194  CALL_FUNCTION_1       1  ''
              196  STORE_FAST               'extras_require'

 L. 148       198  LOAD_GLOBAL              os
              200  LOAD_METHOD              rename
              202  LOAD_DEREF               'dist_info'
              204  LOAD_FAST                'egg_info'
              206  CALL_METHOD_2         2  ''
              208  POP_TOP          

 L. 149       210  LOAD_GLOBAL              os
              212  LOAD_METHOD              rename

 L. 150       214  LOAD_GLOBAL              os
              216  LOAD_ATTR                path
              218  LOAD_METHOD              join
              220  LOAD_FAST                'egg_info'
              222  LOAD_STR                 'METADATA'
              224  CALL_METHOD_2         2  ''

 L. 151       226  LOAD_GLOBAL              os
              228  LOAD_ATTR                path
              230  LOAD_METHOD              join
              232  LOAD_FAST                'egg_info'
              234  LOAD_STR                 'PKG-INFO'
              236  CALL_METHOD_2         2  ''

 L. 149       238  CALL_METHOD_2         2  ''
              240  POP_TOP          

 L. 153       242  LOAD_GLOBAL              setuptools
              244  LOAD_ATTR                Distribution

 L. 154       246  LOAD_GLOBAL              dict

 L. 155       248  LOAD_DEREF               'install_requires'

 L. 156       250  LOAD_FAST                'extras_require'

 L. 154       252  LOAD_CONST               ('install_requires', 'extras_require')
              254  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 153       256  LOAD_CONST               ('attrs',)
              258  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              260  STORE_FAST               'setup_dist'

 L. 160       262  LOAD_GLOBAL              log
              264  LOAD_ATTR                _global_log
              266  LOAD_ATTR                threshold
              268  STORE_FAST               'log_threshold'

 L. 161       270  LOAD_GLOBAL              log
              272  LOAD_METHOD              set_threshold
              274  LOAD_GLOBAL              log
              276  LOAD_ATTR                WARN
              278  CALL_METHOD_1         1  ''
              280  POP_TOP          

 L. 162       282  SETUP_FINALLY       316  'to 316'

 L. 163       284  LOAD_GLOBAL              write_requirements

 L. 164       286  LOAD_FAST                'setup_dist'
              288  LOAD_METHOD              get_command_obj
              290  LOAD_STR                 'egg_info'
              292  CALL_METHOD_1         1  ''

 L. 165       294  LOAD_CONST               None

 L. 166       296  LOAD_GLOBAL              os
              298  LOAD_ATTR                path
              300  LOAD_METHOD              join
              302  LOAD_FAST                'egg_info'
              304  LOAD_STR                 'requires.txt'
              306  CALL_METHOD_2         2  ''

 L. 163       308  CALL_FUNCTION_3       3  ''
              310  POP_TOP          
              312  POP_BLOCK        
              314  BEGIN_FINALLY    
            316_0  COME_FROM_FINALLY   282  '282'

 L. 169       316  LOAD_GLOBAL              log
              318  LOAD_METHOD              set_threshold
              320  LOAD_FAST                'log_threshold'
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          
              326  END_FINALLY      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 182

    @staticmethod
    def _move_data_entries(destination_eggdir, dist_data):
        """Move data entries to their correct location."""
        dist_data = os.path.join(destination_eggdir, dist_data)
        dist_data_scripts = os.path.join(dist_data, 'scripts')
        if os.path.exists(dist_data_scripts):
            egg_info_scripts = os.path.join(destination_eggdir, 'EGG-INFO', 'scripts')
            os.mkdir(egg_info_scripts)
            for entry in os.listdir(dist_data_scripts):
                if entry.endswith('.pyc'):
                    os.unlink(os.path.join(dist_data_scripts, entry))
                else:
                    os.rename(os.path.join(dist_data_scripts, entry), os.path.join(egg_info_scripts, entry))
            else:
                os.rmdir(dist_data_scripts)

        for subdir in filter(os.path.exists, (os.path.join(dist_data, d) for d in ('data',
                                                                                   'headers',
                                                                                   'purelib',
                                                                                   'platlib'))):
            unpack(subdir, destination_eggdir)
        else:
            if os.path.exists(dist_data):
                os.rmdir(dist_data)

    @staticmethod
    def _fix_namespace_packages(egg_info, destination_eggdir):
        namespace_packages = os.path.join(egg_info, 'namespace_packages.txt')
        if os.path.exists(namespace_packages):
            with open(namespace_packages) as (fp):
                namespace_packages = fp.read().split()
            for mod in namespace_packages:
                mod_dir = (os.path.join)(destination_eggdir, *mod.split('.'))
                mod_init = os.path.join(mod_dir, '__init__.py')
                if not os.path.exists(mod_dir):
                    os.mkdir(mod_dir)
                if not os.path.exists(mod_init):
                    with open(mod_init, 'w') as (fp):
                        fp.write(NAMESPACE_PACKAGE_INIT)