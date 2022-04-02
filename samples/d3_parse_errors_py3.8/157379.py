# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\setuptools\dist.py
__all__ = ['Distribution']
import io, sys, re, os, warnings, numbers, distutils.log, distutils.core, distutils.cmd, distutils.dist
from distutils.util import strtobool
from distutils.debug import DEBUG
from distutils.fancy_getopt import translate_longopt
import itertools
from collections import defaultdict
from email import message_from_file
from distutils.errors import DistutilsOptionError, DistutilsPlatformError, DistutilsSetupError
from distutils.util import rfc822_escape
from distutils.version import StrictVersion
from setuptools.extern import six
from setuptools.extern import packaging
from setuptools.extern.six.moves import map, filter, filterfalse
from . import SetuptoolsDeprecationWarning
from setuptools.depends import Require
from setuptools import windows_support
from setuptools.monkey import get_unpatched
from setuptools.config import parse_configuration
import pkg_resources
__import__('setuptools.extern.packaging.specifiers')
__import__('setuptools.extern.packaging.version')

def _get_unpatched(cls):
    warnings.warn('Do not call this function', DistDeprecationWarning)
    return get_unpatched(cls)


def get_metadata_version(self):
    mv = getattr(self, 'metadata_version', None)
    if mv is None:
        if self.long_description_content_type or self.provides_extras:
            mv = StrictVersion('2.1')
        elif self.maintainer is not None or self.maintainer_email is not None or getattr(self, 'python_requires', None) is not None or self.project_urls:
            mv = StrictVersion('1.2')
        elif self.provides or self.requires or self.obsoletes or self.classifiers or self.download_url:
            mv = StrictVersion('1.1')
        else:
            mv = StrictVersion('1.0')
        self.metadata_version = mv
    return mv


def read_pkg_file(self, file):
    """Reads the metadata values from a file object."""
    msg = message_from_file(file)

    def _read_field(name):
        value = msg[name]
        if value == 'UNKNOWN':
            return
        return value

    def _read_list(name):
        values = msg.get_all(name, None)
        if values == []:
            return
        return values

    self.metadata_version = StrictVersion(msg['metadata-version'])
    self.name = _read_field('name')
    self.version = _read_field('version')
    self.description = _read_field('summary')
    self.author = _read_field('author')
    self.maintainer = None
    self.author_email = _read_field('author-email')
    self.maintainer_email = None
    self.url = _read_field('home-page')
    self.license = _read_field('license')
    if 'download-url' in msg:
        self.download_url = _read_field('download-url')
    else:
        self.download_url = None
    self.long_description = _read_field('description')
    self.description = _read_field('summary')
    if 'keywords' in msg:
        self.keywords = _read_field('keywords').split(',')
    self.platforms = _read_list('platform')
    self.classifiers = _read_list('classifier')
    if self.metadata_version == StrictVersion('1.1'):
        self.requires = _read_list('requires')
        self.provides = _read_list('provides')
        self.obsoletes = _read_list('obsoletes')
    else:
        self.requires = None
        self.provides = None
        self.obsoletes = None


def write_pkg_file(self, file):
    """Write the PKG-INFO format data to a file object.
    """
    version = self.get_metadata_version()
    if six.PY2:

        def write_field(key, value):
            file.write('%s: %s\n' % (key, self._encode_field(value)))

    else:

        def write_field(key, value):
            file.write('%s: %s\n' % (key, value))

    write_field('Metadata-Version', str(version))
    write_field('Name', self.get_name())
    write_field('Version', self.get_version())
    write_field('Summary', self.get_description())
    write_field('Home-page', self.get_url())
    if version < StrictVersion('1.2'):
        write_field('Author', self.get_contact())
        write_field('Author-email', self.get_contact_email())
    else:
        optional_fields = (('Author', 'author'), ('Author-email', 'author_email'),
                           ('Maintainer', 'maintainer'), ('Maintainer-email', 'maintainer_email'))
    for field, attr in optional_fields:
        attr_val = getattr(self, attr)
        if attr_val is not None:
            write_field(field, attr_val)
    else:
        write_field('License', self.get_license())
        if self.download_url:
            write_field('Download-URL', self.download_url)
        for project_url in self.project_urls.items():
            write_field('Project-URL', '%s, %s' % project_url)
        else:
            long_desc = rfc822_escape(self.get_long_description())
            write_field('Description', long_desc)
            keywords = ','.join(self.get_keywords())
            if keywords:
                write_field('Keywords', keywords)
            if version >= StrictVersion('1.2'):
                for platform in self.get_platforms():
                    write_field('Platform', platform)

            else:
                self._write_list(file, 'Platform', self.get_platforms())
            self._write_list(file, 'Classifier', self.get_classifiers())
            self._write_list(file, 'Requires', self.get_requires())
            self._write_list(file, 'Provides', self.get_provides())
            self._write_list(file, 'Obsoletes', self.get_obsoletes())
            if hasattr(self, 'python_requires'):
                write_field('Requires-Python', self.python_requires)
            if self.long_description_content_type:
                write_field('Description-Content-Type', self.long_description_content_type)
            if self.provides_extras:
                for extra in self.provides_extras:
                    write_field('Provides-Extra', extra)


sequence = (
 tuple, list)

def check_importable(dist, attr, value):
    try:
        ep = pkg_resources.EntryPoint.parse('x=' + value)
        assert not ep.extras
    except (TypeError, ValueError, AttributeError, AssertionError):
        raise DistutilsSetupError("%r must be importable 'module:attrs' string (got %r)" % (
         attr, value))


def assert_string_list(dist, attr, value):
    """Verify that value is a string list"""
    try:
        assert isinstance(value, (list, tuple))
        assert ''.join(value) != value
    except (TypeError, ValueError, AttributeError, AssertionError):
        raise DistutilsSetupError('%r must be a list of strings (got %r)' % (attr, value))


def check_nsp(dist, attr, value):
    """Verify that namespace packages are valid"""
    ns_packages = value
    assert_string_list(dist, attr, ns_packages)
    for nsp in ns_packages:
        if not dist.has_contents_for(nsp):
            raise DistutilsSetupError('Distribution contains no modules or packages for ' + 'namespace package %r' % nsp)
        else:
            parent, sep, child = nsp.rpartition('.')
        if parent:
            if parent not in ns_packages:
                distutils.log.warn('WARNING: %r is declared as a package namespace, but %r is not: please correct this in setup.py', nsp, parent)


def check_extras(dist, attr, value):
    """Verify that extras_require mapping is valid"""
    try:
        list(itertools.starmap(_check_extra, value.items()))
    except (TypeError, ValueError, AttributeError):
        raise DistutilsSetupError("'extras_require' must be a dictionary whose values are strings or lists of strings containing valid project/version requirement specifiers.")


def _check_extra(extra, reqs):
    name, sep, marker = extra.partition(':')
    if marker:
        if pkg_resources.invalid_marker(marker):
            raise DistutilsSetupError('Invalid environment marker: ' + marker)
    list(pkg_resources.parse_requirements(reqs))


def assert_bool(dist, attr, value):
    """Verify that value is True, False, 0, or 1"""
    if bool(value) != value:
        tmpl = '{attr!r} must be a boolean value (got {value!r})'
        raise DistutilsSetupError(tmpl.format(attr=attr, value=value))


def check_requirements(dist, attr, value):
    """Verify that install_requires is a valid requirements list"""
    try:
        list(pkg_resources.parse_requirements(value))
        if isinstance(value, (dict, set)):
            raise TypeError('Unordered types are not allowed')
    except (TypeError, ValueError) as error:
        try:
            tmpl = '{attr!r} must be a string or list of strings containing valid project/version requirement specifiers; {error}'
            raise DistutilsSetupError(tmpl.format(attr=attr, error=error))
        finally:
            error = None
            del error


def check_specifier(dist, attr, value):
    """Verify that value is a valid version specifier"""
    try:
        packaging.specifiers.SpecifierSet(value)
    except packaging.specifiers.InvalidSpecifier as error:
        try:
            tmpl = '{attr!r} must be a string containing valid version specifiers; {error}'
            raise DistutilsSetupError(tmpl.format(attr=attr, error=error))
        finally:
            error = None
            del error


def check_entry_points(dist, attr, value):
    """Verify that entry_points map is parseable"""
    try:
        pkg_resources.EntryPoint.parse_map(value)
    except ValueError as e:
        try:
            raise DistutilsSetupError(e)
        finally:
            e = None
            del e


def check_test_suite(dist, attr, value):
    if not isinstance(value, six.string_types):
        raise DistutilsSetupError('test_suite must be a string')


def check_package_data(dist, attr, value):
    """Verify that value is a dictionary of package names to glob lists"""
    if not isinstance(value, dict):
        raise DistutilsSetupError('{!r} must be a dictionary mapping package names to lists of string wildcard patterns'.format(attr))
    for k, v in value.items():
        if not isinstance(k, six.string_types):
            raise DistutilsSetupError('keys of {!r} dict must be strings (got {!r})'.format(attr, k))
        else:
            assert_string_list(dist, 'values of {!r} dict'.format(attr), v)


def check_packages(dist, attr, value):
    for pkgname in value:
        if not re.match('\\w+(\\.\\w+)*', pkgname):
            distutils.log.warn('WARNING: %r not a valid package name; please use only .-separated package names in setup.py', pkgname)


_Distribution = get_unpatched(distutils.core.Distribution)

class Distribution(_Distribution):
    __doc__ = 'Distribution with support for features, tests, and package data\n\n    This is an enhanced version of \'distutils.dist.Distribution\' that\n    effectively adds the following new optional keyword arguments to \'setup()\':\n\n     \'install_requires\' -- a string or sequence of strings specifying project\n        versions that the distribution requires when installed, in the format\n        used by \'pkg_resources.require()\'.  They will be installed\n        automatically when the package is installed.  If you wish to use\n        packages that are not available in PyPI, or want to give your users an\n        alternate download location, you can add a \'find_links\' option to the\n        \'[easy_install]\' section of your project\'s \'setup.cfg\' file, and then\n        setuptools will scan the listed web pages for links that satisfy the\n        requirements.\n\n     \'extras_require\' -- a dictionary mapping names of optional "extras" to the\n        additional requirement(s) that using those extras incurs. For example,\n        this::\n\n            extras_require = dict(reST = ["docutils>=0.3", "reSTedit"])\n\n        indicates that the distribution can optionally provide an extra\n        capability called "reST", but it can only be used if docutils and\n        reSTedit are installed.  If the user installs your package using\n        EasyInstall and requests one of your extras, the corresponding\n        additional requirements will be installed if needed.\n\n     \'features\' **deprecated** -- a dictionary mapping option names to\n        \'setuptools.Feature\'\n        objects.  Features are a portion of the distribution that can be\n        included or excluded based on user options, inter-feature dependencies,\n        and availability on the current system.  Excluded features are omitted\n        from all setup commands, including source and binary distributions, so\n        you can create multiple distributions from the same source tree.\n        Feature names should be valid Python identifiers, except that they may\n        contain the \'-\' (minus) sign.  Features can be included or excluded\n        via the command line options \'--with-X\' and \'--without-X\', where \'X\' is\n        the name of the feature.  Whether a feature is included by default, and\n        whether you are allowed to control this from the command line, is\n        determined by the Feature object.  See the \'Feature\' class for more\n        information.\n\n     \'test_suite\' -- the name of a test suite to run for the \'test\' command.\n        If the user runs \'python setup.py test\', the package will be installed,\n        and the named test suite will be run.  The format is the same as\n        would be used on a \'unittest.py\' command line.  That is, it is the\n        dotted name of an object to import and call to generate a test suite.\n\n     \'package_data\' -- a dictionary mapping package names to lists of filenames\n        or globs to use to find data files contained in the named packages.\n        If the dictionary has filenames or globs listed under \'""\' (the empty\n        string), those names will be searched for in every package, in addition\n        to any names for the specific package.  Data files found using these\n        names/globs will be installed along with the package, in the same\n        location as the package.  Note that globs are allowed to reference\n        the contents of non-package subdirectories, as long as you use \'/\' as\n        a path separator.  (Globs are automatically converted to\n        platform-specific paths at runtime.)\n\n    In addition to these new keywords, this class also has several new methods\n    for manipulating the distribution\'s contents.  For example, the \'include()\'\n    and \'exclude()\' methods can be thought of as in-place add and subtract\n    commands that add or remove packages, modules, extensions, and so on from\n    the distribution.  They are used by the feature subsystem to configure the\n    distribution for the included and excluded features.\n    '
    _DISTUTILS_UNSUPPORTED_METADATA = {'long_description_content_type':None, 
     'project_urls':dict, 
     'provides_extras':set}
    _patched_dist = None

    def patch_missing_pkg_info(self, attrs):
        if attrs:
            if 'name' not in attrs or ('version' not in attrs):
                return
            key = pkg_resources.safe_name(str(attrs['name'])).lower()
            dist = pkg_resources.working_set.by_key.get(key)
            if dist is not None:
                if not dist.has_metadata('PKG-INFO'):
                    dist._version = pkg_resources.safe_version(str(attrs['version']))
                    self._patched_dist = dist

    def __init__--- This code section failed: ---

 L. 429         0  LOAD_GLOBAL              hasattr
                2  LOAD_DEREF               'self'
                4  LOAD_STR                 'package_data'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'have_package_data'

 L. 430        10  LOAD_FAST                'have_package_data'
               12  POP_JUMP_IF_TRUE     20  'to 20'

 L. 431        14  BUILD_MAP_0           0 
               16  LOAD_DEREF               'self'
               18  STORE_ATTR               package_data
             20_0  COME_FROM            12  '12'

 L. 432        20  LOAD_FAST                'attrs'
               22  JUMP_IF_TRUE_OR_POP    26  'to 26'
               24  BUILD_MAP_0           0 
             26_0  COME_FROM            22  '22'
               26  STORE_FAST               'attrs'

 L. 433        28  LOAD_STR                 'features'
               30  LOAD_FAST                'attrs'
               32  COMPARE_OP               in
               34  POP_JUMP_IF_TRUE     44  'to 44'
               36  LOAD_STR                 'require_features'
               38  LOAD_FAST                'attrs'
               40  COMPARE_OP               in
               42  POP_JUMP_IF_FALSE    52  'to 52'
             44_0  COME_FROM            34  '34'

 L. 434        44  LOAD_GLOBAL              Feature
               46  LOAD_METHOD              warn_deprecated
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          
             52_0  COME_FROM            42  '42'

 L. 435        52  BUILD_LIST_0          0 
               54  LOAD_DEREF               'self'
               56  STORE_ATTR               require_features

 L. 436        58  BUILD_MAP_0           0 
               60  LOAD_DEREF               'self'
               62  STORE_ATTR               features

 L. 437        64  BUILD_LIST_0          0 
               66  LOAD_DEREF               'self'
               68  STORE_ATTR               dist_files

 L. 439        70  LOAD_FAST                'attrs'
               72  LOAD_METHOD              pop
               74  LOAD_STR                 'src_root'
               76  LOAD_CONST               None
               78  CALL_METHOD_2         2  ''
               80  LOAD_DEREF               'self'
               82  STORE_ATTR               src_root

 L. 440        84  LOAD_DEREF               'self'
               86  LOAD_METHOD              patch_missing_pkg_info
               88  LOAD_FAST                'attrs'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 441        94  LOAD_FAST                'attrs'
               96  LOAD_METHOD              pop
               98  LOAD_STR                 'dependency_links'
              100  BUILD_LIST_0          0 
              102  CALL_METHOD_2         2  ''
              104  LOAD_DEREF               'self'
              106  STORE_ATTR               dependency_links

 L. 442       108  LOAD_FAST                'attrs'
              110  LOAD_METHOD              pop
              112  LOAD_STR                 'setup_requires'
              114  BUILD_LIST_0          0 
              116  CALL_METHOD_2         2  ''
              118  LOAD_DEREF               'self'
              120  STORE_ATTR               setup_requires

 L. 443       122  LOAD_GLOBAL              pkg_resources
              124  LOAD_METHOD              iter_entry_points
              126  LOAD_STR                 'distutils.setup_keywords'
              128  CALL_METHOD_1         1  ''
              130  GET_ITER         
            132_0  COME_FROM           154  '154'
              132  FOR_ITER            156  'to 156'
              134  STORE_FAST               'ep'

 L. 444       136  LOAD_GLOBAL              vars
              138  LOAD_DEREF               'self'
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_METHOD              setdefault
              144  LOAD_FAST                'ep'
              146  LOAD_ATTR                name
              148  LOAD_CONST               None
              150  CALL_METHOD_2         2  ''
              152  POP_TOP          
              154  JUMP_BACK           132  'to 132'
            156_0  COME_FROM           132  '132'

 L. 445       156  LOAD_GLOBAL              _Distribution
              158  LOAD_METHOD              __init__
              160  LOAD_DEREF               'self'
              162  LOAD_CLOSURE             'self'
              164  BUILD_TUPLE_1         1 
              166  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              168  LOAD_STR                 'Distribution.__init__.<locals>.<dictcomp>'
              170  MAKE_FUNCTION_8          'closure'

 L. 446       172  LOAD_FAST                'attrs'
              174  LOAD_METHOD              items
              176  CALL_METHOD_0         0  ''

 L. 445       178  GET_ITER         
              180  CALL_FUNCTION_1       1  ''
              182  CALL_METHOD_2         2  ''
              184  POP_TOP          

 L. 453       186  LOAD_DEREF               'self'
              188  LOAD_ATTR                _DISTUTILS_UNSUPPORTED_METADATA
              190  LOAD_METHOD              items
              192  CALL_METHOD_0         0  ''
              194  GET_ITER         
            196_0  COME_FROM           272  '272'
              196  FOR_ITER            274  'to 274'
              198  UNPACK_SEQUENCE_2     2 
              200  STORE_FAST               'option'
              202  STORE_FAST               'default'

 L. 454       204  LOAD_DEREF               'self'
              206  LOAD_ATTR                metadata
              208  LOAD_ATTR                __dict__
              210  LOAD_FAST                'attrs'
              212  BUILD_TUPLE_2         2 
              214  GET_ITER         
            216_0  COME_FROM           242  '242'
            216_1  COME_FROM           226  '226'
              216  FOR_ITER            244  'to 244'
              218  STORE_FAST               'source'

 L. 455       220  LOAD_FAST                'option'
              222  LOAD_FAST                'source'
              224  COMPARE_OP               in
              226  POP_JUMP_IF_FALSE_BACK   216  'to 216'

 L. 456       228  LOAD_FAST                'source'
              230  LOAD_FAST                'option'
              232  BINARY_SUBSCR    
              234  STORE_FAST               'value'

 L. 457       236  POP_TOP          
          238_240  BREAK_LOOP          258  'to 258'
              242  JUMP_BACK           216  'to 216'
            244_0  COME_FROM           216  '216'

 L. 459       244  LOAD_FAST                'default'
              246  POP_JUMP_IF_FALSE   254  'to 254'
              248  LOAD_FAST                'default'
              250  CALL_FUNCTION_0       0  ''
              252  JUMP_FORWARD        256  'to 256'
            254_0  COME_FROM           246  '246'
              254  LOAD_CONST               None
            256_0  COME_FROM           252  '252'
              256  STORE_FAST               'value'
            258_0  COME_FROM           238  '238'

 L. 460       258  LOAD_GLOBAL              setattr
              260  LOAD_DEREF               'self'
              262  LOAD_ATTR                metadata
              264  LOAD_FAST                'option'
              266  LOAD_FAST                'value'
              268  CALL_FUNCTION_3       3  ''
              270  POP_TOP          
              272  JUMP_BACK           196  'to 196'
            274_0  COME_FROM           196  '196'

 L. 462       274  LOAD_GLOBAL              isinstance
              276  LOAD_DEREF               'self'
              278  LOAD_ATTR                metadata
              280  LOAD_ATTR                version
              282  LOAD_GLOBAL              numbers
              284  LOAD_ATTR                Number
              286  CALL_FUNCTION_2       2  ''
          288_290  POP_JUMP_IF_FALSE   308  'to 308'

 L. 464       292  LOAD_GLOBAL              str
              294  LOAD_DEREF               'self'
              296  LOAD_ATTR                metadata
              298  LOAD_ATTR                version
              300  CALL_FUNCTION_1       1  ''
              302  LOAD_DEREF               'self'
              304  LOAD_ATTR                metadata
              306  STORE_ATTR               version
            308_0  COME_FROM           288  '288'

 L. 466       308  LOAD_DEREF               'self'
              310  LOAD_ATTR                metadata
              312  LOAD_ATTR                version
              314  LOAD_CONST               None
              316  COMPARE_OP               is-not
          318_320  POP_JUMP_IF_FALSE   444  'to 444'

 L. 467       322  SETUP_FINALLY       396  'to 396'

 L. 468       324  LOAD_GLOBAL              packaging
              326  LOAD_ATTR                version
              328  LOAD_METHOD              Version
              330  LOAD_DEREF               'self'
              332  LOAD_ATTR                metadata
              334  LOAD_ATTR                version
              336  CALL_METHOD_1         1  ''
              338  STORE_FAST               'ver'

 L. 469       340  LOAD_GLOBAL              str
              342  LOAD_FAST                'ver'
              344  CALL_FUNCTION_1       1  ''
              346  STORE_FAST               'normalized_version'

 L. 470       348  LOAD_DEREF               'self'
              350  LOAD_ATTR                metadata
              352  LOAD_ATTR                version
              354  LOAD_FAST                'normalized_version'
              356  COMPARE_OP               !=
          358_360  POP_JUMP_IF_FALSE   392  'to 392'

 L. 471       362  LOAD_GLOBAL              warnings
              364  LOAD_METHOD              warn

 L. 472       366  LOAD_STR                 "Normalizing '%s' to '%s'"

 L. 473       368  LOAD_DEREF               'self'
              370  LOAD_ATTR                metadata
              372  LOAD_ATTR                version

 L. 474       374  LOAD_FAST                'normalized_version'

 L. 472       376  BUILD_TUPLE_2         2 
              378  BINARY_MODULO    

 L. 471       380  CALL_METHOD_1         1  ''
              382  POP_TOP          

 L. 477       384  LOAD_FAST                'normalized_version'
              386  LOAD_DEREF               'self'
              388  LOAD_ATTR                metadata
              390  STORE_ATTR               version
            392_0  COME_FROM           358  '358'
              392  POP_BLOCK        
              394  JUMP_FORWARD        444  'to 444'
            396_0  COME_FROM_FINALLY   322  '322'

 L. 478       396  DUP_TOP          
              398  LOAD_GLOBAL              packaging
              400  LOAD_ATTR                version
              402  LOAD_ATTR                InvalidVersion
              404  LOAD_GLOBAL              TypeError
              406  BUILD_TUPLE_2         2 
              408  COMPARE_OP               exception-match
          410_412  POP_JUMP_IF_FALSE   442  'to 442'
              414  POP_TOP          
              416  POP_TOP          
              418  POP_TOP          

 L. 479       420  LOAD_GLOBAL              warnings
              422  LOAD_METHOD              warn

 L. 480       424  LOAD_STR                 'The version specified (%r) is an invalid version, this may not work as expected with newer versions of setuptools, pip, and PyPI. Please see PEP 440 for more details.'

 L. 483       426  LOAD_DEREF               'self'
              428  LOAD_ATTR                metadata
              430  LOAD_ATTR                version

 L. 480       432  BINARY_MODULO    

 L. 479       434  CALL_METHOD_1         1  ''
              436  POP_TOP          
              438  POP_EXCEPT       
              440  JUMP_FORWARD        444  'to 444'
            442_0  COME_FROM           410  '410'
              442  END_FINALLY      
            444_0  COME_FROM           440  '440'
            444_1  COME_FROM           394  '394'
            444_2  COME_FROM           318  '318'

 L. 485       444  LOAD_DEREF               'self'
              446  LOAD_METHOD              _finalize_requires
              448  CALL_METHOD_0         0  ''
              450  POP_TOP          

Parse error at or near `LOAD_GLOBAL' instruction at offset 274

    def _finalize_requires(self):
        """
        Set `metadata.python_requires` and fix environment markers
        in `install_requires` and `extras_require`.
        """
        if getattr(self, 'python_requires', None):
            self.metadata.python_requires = self.python_requires
        if getattr(self, 'extras_require', None):
            for extra in self.extras_require.keys():
                extra = extra.split(':')[0]
                if extra:
                    self.metadata.provides_extras.add(extra)

        self._convert_extras_requirements()
        self._move_install_requirements_markers()

    def _convert_extras_requirements(self):
        """
        Convert requirements in `extras_require` of the form
        `"extra": ["barbazquux; {marker}"]` to
        `"extra:{marker}": ["barbazquux"]`.
        """
        spec_ext_reqs = getattr(self, 'extras_require', None) or {}
        self._tmp_extras_require = defaultdict(list)
        for section, v in spec_ext_reqs.items():
            self._tmp_extras_require[section]
            for r in pkg_resources.parse_requirements(v):
                suffix = self._suffix_for(r)
                self._tmp_extras_require[(section + suffix)].append(r)

    @staticmethod
    def _suffix_for(req):
        """
        For a requirement, return the 'extras_require' suffix for
        that requirement.
        """
        if req.marker:
            return ':' + str(req.marker)
        return ''

    def _move_install_requirements_markers(self):
        """
        Move requirements in `install_requires` that are using environment
        markers `extras_require`.
        """

        def is_simple_req(req):
            return not req.marker

        spec_inst_reqs = getattr(self, 'install_requires', None) or ()
        inst_reqs = list(pkg_resources.parse_requirements(spec_inst_reqs))
        simple_reqs = filter(is_simple_req, inst_reqs)
        complex_reqs = filterfalse(is_simple_req, inst_reqs)
        self.install_requires = list(map(str, simple_reqs))
        for r in complex_reqs:
            self._tmp_extras_require[(':' + str(r.marker))].append(r)
        else:
            self.extras_require = dict(((
             k, [str(r) for r in map(self._clean_req, v)]) for k, v in self._tmp_extras_require.items()))

    def _clean_req(self, req):
        """
        Given a Requirement, remove environment markers and return it.
        """
        req.marker = None
        return req

    def _parse_config_files(self, filenames=None):
        """
        Adapted from distutils.dist.Distribution.parse_config_files,
        this method provides the same functionality in subtly-improved
        ways.
        """
        from setuptools.extern.six.moves.configparser import ConfigParser
        if six.PY3 and sys.prefix != sys.base_prefix:
            ignore_options = ['install-base', 'install-platbase', 'install-lib',
             'install-platlib', 'install-purelib', 'install-headers',
             'install-scripts', 'install-data', 'prefix', 'exec-prefix',
             'home', 'user', 'root']
        else:
            ignore_options = []
        ignore_options = frozenset(ignore_options)
        if filenames is None:
            filenames = self.find_config_files()
        if DEBUG:
            self.announce('Distribution.parse_config_files():')
        parser = ConfigParser
        for filename in filenames:
            with io.open(filename, encoding='utf-8') as reader:
                if DEBUG:
                    self.announce(('  reading {filename}'.format)(**))
                parser.read_file if six.PY3 else parser.readfp(reader)
            for section in parser.sections():
                options = parser.options(section)
                opt_dict = self.get_option_dict(section)
                for opt in options:
                    if opt != '__name__':
                        if opt not in ignore_options:
                            val = self._try_str(parser.get(section, opt))
                            opt = opt.replace('-', '_')
                            opt_dict[opt] = (filename, val)

            else:
                parser.__init__()

        else:
            if 'global' in self.command_options:
                for opt, (src, val) in self.command_options['global'].items():
                    alias = self.negative_opt.get(opt)
                    try:
                        if alias:
                            setattr(self, alias, not strtobool(val))
                        elif opt in ('verbose', 'dry_run'):
                            setattr(self, opt, strtobool(val))
                        else:
                            setattr(self, opt, val)
                    except ValueError as msg:
                        try:
                            raise DistutilsOptionError(msg)
                        finally:
                            msg = None
                            del msg

    @staticmethod
    def _try_str--- This code section failed: ---

 L. 637         0  LOAD_GLOBAL              six
                2  LOAD_ATTR                PY3
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 638         6  LOAD_FAST                'val'
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 639        10  SETUP_FINALLY        22  'to 22'

 L. 640        12  LOAD_FAST                'val'
               14  LOAD_METHOD              encode
               16  CALL_METHOD_0         0  ''
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY    10  '10'

 L. 641        22  DUP_TOP          
               24  LOAD_GLOBAL              UnicodeEncodeError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    40  'to 40'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 642        36  POP_EXCEPT       
               38  JUMP_FORWARD         42  'to 42'
             40_0  COME_FROM            28  '28'
               40  END_FINALLY      
             42_0  COME_FROM            38  '38'

 L. 643        42  LOAD_FAST                'val'
               44  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 40_0

    def _set_command_options(self, command_obj, option_dict=None):
        """
        Set the options for 'command_obj' from 'option_dict'.  Basically
        this means copying elements of a dictionary ('option_dict') to
        attributes of an instance ('command').

        'command_obj' must be a Command instance.  If 'option_dict' is not
        supplied, uses the standard option dictionary for this command
        (from 'self.command_options').

        (Adopted from distutils.dist.Distribution._set_command_options)
        """
        command_name = command_obj.get_command_name()
        if option_dict is None:
            option_dict = self.get_option_dict(command_name)
        if DEBUG:
            self.announce("  setting options for '%s' command:" % command_name)
        for option, (source, value) in option_dict.items():
            if DEBUG:
                self.announce('    %s = %s (from %s)' % (option, value,
                 source))
            else:
                try:
                    bool_opts = [translate_longopt(o) for o in command_obj.boolean_options]
                except AttributeError:
                    bool_opts = []
                else:
                    try:
                        neg_opt = command_obj.negative_opt
                    except AttributeError:
                        neg_opt = {}
                    else:
                        try:
                            is_string = isinstance(value, six.string_types)
                            if option in neg_opt and is_string:
                                setattr(command_obj, neg_opt[option], not strtobool(value))
                            elif option in bool_opts and is_string:
                                setattr(command_obj, option, strtobool(value))
                            elif hasattr(command_obj, option):
                                setattr(command_obj, option, value)
                            else:
                                raise DistutilsOptionError("error in %s: command '%s' has no such option '%s'" % (
                                 source, command_name, option))
                        except ValueError as msg:
                            try:
                                raise DistutilsOptionError(msg)
                            finally:
                                msg = None
                                del msg

    def parse_config_files(self, filenames=None, ignore_option_errors=False):
        """Parses configuration files from various levels
        and loads configuration.

        """
        self._parse_config_files(filenames=filenames)
        parse_configuration(self, (self.command_options), ignore_option_errors=ignore_option_errors)
        self._finalize_requires()

    def parse_command_line(self):
        """Process features after parsing command line options"""
        result = _Distribution.parse_command_line(self)
        if self.features:
            self._finalize_features()
        return result

    def _feature_attrname(self, name):
        """Convert feature name to corresponding option attribute name"""
        return 'with_' + name.replace('-', '_')

    def fetch_build_eggs(self, requires):
        """Resolve pre-setup requirements"""
        resolved_dists = pkg_resources.working_set.resolve((pkg_resources.parse_requirements(requires)),
          installer=(self.fetch_build_egg),
          replace_conflicting=True)
        for dist in resolved_dists:
            pkg_resources.working_set.add(dist, replace=True)
        else:
            return resolved_dists

    def finalize_options(self):
        _Distribution.finalize_options(self)
        if self.features:
            self._set_global_opts_from_features()
        for ep in pkg_resources.iter_entry_points('distutils.setup_keywords'):
            value = getattr(self, ep.name, None)
            if value is not None:
                ep.require(installer=(self.fetch_build_egg))
                ep.load()(self, ep.name, value)
        else:
            if getattr(self, 'convert_2to3_doctests', None):
                self.convert_2to3_doctests = [os.path.abspath(p) for p in self.convert_2to3_doctests]
            else:
                self.convert_2to3_doctests = []

    def get_egg_cache_dir(self):
        egg_cache_dir = os.path.join(os.curdir, '.eggs')
        if not os.path.exists(egg_cache_dir):
            os.mkdir(egg_cache_dir)
            windows_support.hide_file(egg_cache_dir)
            readme_txt_filename = os.path.join(egg_cache_dir, 'README.txt')
            with open(readme_txt_filename, 'w') as f:
                f.write('This directory contains eggs that were downloaded by setuptools to build, test, and run plug-ins.\n\n')
                f.write('This directory caches those eggs to prevent repeated downloads.\n\n')
                f.write('However, it is safe to delete this directory.\n\n')
        return egg_cache_dir

    def fetch_build_egg(self, req):
        """Fetch an egg needed for building"""
        import setuptools.command.easy_install as easy_install
        dist = self.__class__({'script_args': ['easy_install']})
        opts = dist.get_option_dict('easy_install')
        opts.clear()
        opts.update(((
         k, v) for k, v in self.get_option_dict('easy_install').items() if k in ('find_links',
                                                                                 'site_dirs',
                                                                                 'index_url',
                                                                                 'optimize',
                                                                                 'site_dirs',
                                                                                 'allow_hosts')))
        if self.dependency_links:
            links = self.dependency_links[:]
            if 'find_links' in opts:
                links = opts['find_links'][1] + links
            opts['find_links'] = (
             'setup', links)
        install_dir = self.get_egg_cache_dir()
        cmd = easy_install(dist,
          args=['x'], install_dir=install_dir, exclude_scripts=True,
          always_copy=False,
          build_directory=None,
          editable=False,
          upgrade=False,
          multi_version=True,
          no_report=True,
          user=False)
        cmd.ensure_finalized()
        return cmd.easy_install(req)

    def _set_global_opts_from_features(self):
        """Add --with-X/--without-X options based on optional features"""
        go = []
        no = self.negative_opt.copy()
        for name, feature in self.features.items():
            self._set_feature(name, None)
            feature.validate(self)
            if feature.optional:
                descr = feature.description
                incdef = ' (default)'
                excdef = ''
            if not feature.include_by_default():
                excdef, incdef = incdef, excdef
            else:
                new = (
                 (
                  'with-' + name, None, 'include ' + descr + incdef),
                 (
                  'without-' + name, None, 'exclude ' + descr + excdef))
                go.extend(new)
                no['without-' + name] = 'with-' + name
        else:
            self.global_options = self.feature_options = go + self.global_options
            self.negative_opt = self.feature_negopt = no

    def _finalize_features(self):
        """Add/remove features and resolve dependencies between them"""
        for name, feature in self.features.items():
            enabled = self.feature_is_included(name)
            if not enabled:
                if enabled is None:
                    if feature.include_by_default():
                        pass
            feature.include_in(self)
            self._set_feature(name, 1)
        else:
            for name, feature in self.features.items():
                if not self.feature_is_included(name):
                    feature.exclude_from(self)
                    self._set_feature(name, 0)

    def get_command_class(self, command):
        """Pluggable version of get_command_class()"""
        if command in self.cmdclass:
            return self.cmdclass[command]
        eps = pkg_resources.iter_entry_points('distutils.commands', command)
        for ep in eps:
            ep.require(installer=(self.fetch_build_egg))
            self.cmdclass[command] = cmdclass = ep.load()
            return cmdclass

        return _Distribution.get_command_class(self, command)

    def print_commands(self):
        for ep in pkg_resources.iter_entry_points('distutils.commands'):
            if ep.name not in self.cmdclass:
                cmdclass = ep.resolve()
                self.cmdclass[ep.name] = cmdclass
        else:
            return _Distribution.print_commands(self)

    def get_command_list(self):
        for ep in pkg_resources.iter_entry_points('distutils.commands'):
            if ep.name not in self.cmdclass:
                cmdclass = ep.resolve()
                self.cmdclass[ep.name] = cmdclass
        else:
            return _Distribution.get_command_list(self)

    def _set_feature(self, name, status):
        """Set feature's inclusion status"""
        setattr(self, self._feature_attrname(name), status)

    def feature_is_included(self, name):
        """Return 1 if feature is included, 0 if excluded, 'None' if unknown"""
        return getattr(self, self._feature_attrname(name))

    def include_feature(self, name):
        """Request inclusion of feature named 'name'"""
        if self.feature_is_included(name) == 0:
            descr = self.features[name].description
            raise DistutilsOptionError(descr + ' is required, but was excluded or is not available')
        self.features[name].include_in(self)
        self._set_feature(name, 1)

    def include(self, **attrs):
        """Add items to distribution that are named in keyword arguments

        For example, 'dist.include(py_modules=["x"])' would add 'x' to
        the distribution's 'py_modules' attribute, if it was not already
        there.

        Currently, this method only supports inclusion for attributes that are
        lists or tuples.  If you need to add support for adding to other
        attributes in this or a subclass, you can add an '_include_X' method,
        where 'X' is the name of the attribute.  The method will be called with
        the value passed to 'include()'.  So, 'dist.include(foo={"bar":"baz"})'
        will try to call 'dist._include_foo({"bar":"baz"})', which can then
        handle whatever special inclusion logic is needed.
        """
        for k, v in attrs.items():
            include = getattr(self, '_include_' + k, None)
            if include:
                include(v)
            else:
                self._include_misc(k, v)

    def exclude_package(self, package):
        """Remove packages, modules, and extensions in named package"""
        pfx = package + '.'
        if self.packages:
            self.packages = [p for p in self.packages if p != package if not p.startswith(pfx)]
        if self.py_modules:
            self.py_modules = [p for p in self.py_modules if p != package if not p.startswith(pfx)]
        if self.ext_modules:
            self.ext_modules = [p for p in self.ext_modules if p.name != package if not p.name.startswith(pfx)]

    def has_contents_for(self, package):
        """Return true if 'exclude_package(package)' would do something"""
        pfx = package + '.'
        for p in self.iter_distribution_names():
            if not p == package:
                if p.startswith(pfx):
                    pass
            return True

    def _exclude_misc(self, name, value):
        """Handle 'exclude()' for list/tuple attrs without a special handler"""
        if not isinstance(value, sequence):
            raise DistutilsSetupError('%s: setting must be a list or tuple (%r)' % (name, value))
        try:
            old = getattr(self, name)
        except AttributeError:
            raise DistutilsSetupError('%s: No such distribution setting' % name)

        if old is not None and not isinstance(old, sequence):
            raise DistutilsSetupError(name + ': this setting cannot be changed via include/exclude')
        elif old:
            setattr(self, name, [item for item in old if item not in value])

    def _include_misc(self, name, value):
        """Handle 'include()' for list/tuple attrs without a special handler"""
        if not isinstance(value, sequence):
            raise DistutilsSetupError('%s: setting must be a list (%r)' % (name, value))
        try:
            old = getattr(self, name)
        except AttributeError:
            raise DistutilsSetupError('%s: No such distribution setting' % name)

        if old is None:
            setattr(self, name, value)
        elif not isinstance(old, sequence):
            raise DistutilsSetupError(name + ': this setting cannot be changed via include/exclude')
        else:
            new = [item for item in value if item not in old]
            setattr(self, name, old + new)

    def exclude(self, **attrs):
        """Remove items from distribution that are named in keyword arguments

        For example, 'dist.exclude(py_modules=["x"])' would remove 'x' from
        the distribution's 'py_modules' attribute.  Excluding packages uses
        the 'exclude_package()' method, so all of the package's contained
        packages, modules, and extensions are also excluded.

        Currently, this method only supports exclusion from attributes that are
        lists or tuples.  If you need to add support for excluding from other
        attributes in this or a subclass, you can add an '_exclude_X' method,
        where 'X' is the name of the attribute.  The method will be called with
        the value passed to 'exclude()'.  So, 'dist.exclude(foo={"bar":"baz"})'
        will try to call 'dist._exclude_foo({"bar":"baz"})', which can then
        handle whatever special exclusion logic is needed.
        """
        for k, v in attrs.items():
            exclude = getattr(self, '_exclude_' + k, None)
            if exclude:
                exclude(v)
            else:
                self._exclude_misc(k, v)

    def _exclude_packages(self, packages):
        if not isinstance(packages, sequence):
            raise DistutilsSetupError('packages: setting must be a list or tuple (%r)' % (packages,))
        list(map(self.exclude_package, packages))

    def _parse_command_opts(self, parser, args):
        self.global_options = self.__class__.global_options
        self.negative_opt = self.__class__.negative_opt
        command = args[0]
        aliases = self.get_option_dict('aliases')
        while True:
            if command in aliases:
                src, alias = aliases[command]
                del aliases[command]
                import shlex
                args[:1] = shlex.split(alias, True)
                command = args[0]

        nargs = _Distribution._parse_command_opts(self, parser, args)
        cmd_class = self.get_command_class(command)
        if getattr(cmd_class, 'command_consumes_arguments', None):
            self.get_option_dict(command)['args'] = (
             'command line', nargs)
            if nargs is not None:
                return []
        return nargs

    def get_cmdline_options(self):
        """Return a '{cmd: {opt:val}}' map of all command-line options

        Option names are all long, but do not include the leading '--', and
        contain dashes rather than underscores.  If the option doesn't take
        an argument (e.g. '--quiet'), the 'val' is 'None'.

        Note that options provided by config files are intentionally excluded.
        """
        d = {}
        for cmd, opts in self.command_options.items():
            for opt, (src, val) in opts.items():
                if src != 'command line':
                    pass
                else:
                    opt = opt.replace('_', '-')
                    if val == 0:
                        cmdobj = self.get_command_obj(cmd)
                        neg_opt = self.negative_opt.copy()
                        neg_opt.update(getattr(cmdobj, 'negative_opt', {}))
                        for neg, pos in neg_opt.items():
                            if pos == opt:
                                opt = neg
                                val = None
                                break
                        else:
                            raise AssertionError("Shouldn't be able to get here")

                    elif val == 1:
                        val = None
                    d.setdefault(cmd, {})[opt] = val
            else:
                return d

    def iter_distribution_names(self):
        """Yield all packages, modules, and extension names in distribution"""
        for pkg in self.packages or ():
            yield pkg
        else:
            for module in self.py_modules or ():
                yield module
            else:
                for ext in self.ext_modules or ():
                    if isinstance(ext, tuple):
                        name, buildinfo = ext
                    else:
                        name = ext.name
                    if name.endswith('module'):
                        name = name[:-6]
                    else:
                        yield name

    def handle_display_options(self, option_order):
        """If there were any non-global "display-only" options
        (--help-commands or the metadata display options) on the command
        line, display the requested info and return true; else return
        false.
        """
        import sys
        if six.PY2 or (self.help_commands):
            return _Distribution.handle_display_options(self, option_order)
        if not isinstance(sys.stdout, io.TextIOWrapper):
            return _Distribution.handle_display_options(self, option_order)
        if sys.stdout.encoding.lower() in ('utf-8', 'utf8'):
            return _Distribution.handle_display_options(self, option_order)
        encoding = sys.stdout.encoding
        errors = sys.stdout.errors
        newline = (sys.platform != 'win32') and '\n' or None
        line_buffering = sys.stdout.line_buffering
        sys.stdout = io.TextIOWrapper(sys.stdout.detach(), 'utf-8', errors, newline, line_buffering)
        try:
            return _Distribution.handle_display_options(self, option_order)
        finally:
            sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding, errors, newline, line_buffering)


class Feature:
    __doc__ = '\n    **deprecated** -- The `Feature` facility was never completely implemented\n    or supported, `has reported issues\n    <https://github.com/pypa/setuptools/issues/58>`_ and will be removed in\n    a future version.\n\n    A subset of the distribution that can be excluded if unneeded/wanted\n\n    Features are created using these keyword arguments:\n\n      \'description\' -- a short, human readable description of the feature, to\n         be used in error messages, and option help messages.\n\n      \'standard\' -- if true, the feature is included by default if it is\n         available on the current system.  Otherwise, the feature is only\n         included if requested via a command line \'--with-X\' option, or if\n         another included feature requires it.  The default setting is \'False\'.\n\n      \'available\' -- if true, the feature is available for installation on the\n         current system.  The default setting is \'True\'.\n\n      \'optional\' -- if true, the feature\'s inclusion can be controlled from the\n         command line, using the \'--with-X\' or \'--without-X\' options.  If\n         false, the feature\'s inclusion status is determined automatically,\n         based on \'availabile\', \'standard\', and whether any other feature\n         requires it.  The default setting is \'True\'.\n\n      \'require_features\' -- a string or sequence of strings naming features\n         that should also be included if this feature is included.  Defaults to\n         empty list.  May also contain \'Require\' objects that should be\n         added/removed from the distribution.\n\n      \'remove\' -- a string or list of strings naming packages to be removed\n         from the distribution if this feature is *not* included.  If the\n         feature *is* included, this argument is ignored.  This argument exists\n         to support removing features that "crosscut" a distribution, such as\n         defining a \'tests\' feature that removes all the \'tests\' subpackages\n         provided by other features.  The default for this argument is an empty\n         list.  (Note: the named package(s) or modules must exist in the base\n         distribution when the \'setup()\' function is initially called.)\n\n      other keywords -- any other keyword arguments are saved, and passed to\n         the distribution\'s \'include()\' and \'exclude()\' methods when the\n         feature is included or excluded, respectively.  So, for example, you\n         could pass \'packages=["a","b"]\' to cause packages \'a\' and \'b\' to be\n         added or removed from the distribution as appropriate.\n\n    A feature must include at least one \'requires\', \'remove\', or other\n    keyword argument.  Otherwise, it can\'t affect the distribution in any way.\n    Note also that you can subclass \'Feature\' to create your own specialized\n    feature types that modify the distribution in other ways when included or\n    excluded.  See the docstrings for the various methods here for more detail.\n    Aside from the methods, the only feature attributes that distributions look\n    at are \'description\' and \'optional\'.\n    '

    @staticmethod
    def warn_deprecated():
        msg = 'Features are deprecated and will be removed in a future version. See https://github.com/pypa/setuptools/issues/65.'
        warnings.warn(msg, DistDeprecationWarning, stacklevel=3)

    def __init__(self, description, standard=False, available=True, optional=True, require_features=(), remove=(), **extras):
        self.warn_deprecated()
        self.description = description
        self.standard = standard
        self.available = available
        self.optional = optional
        if isinstance(require_features, (str, Require)):
            require_features = (
             require_features,)
        self.require_features = [r for r in require_features if isinstance(r, str)]
        er = [r for r in require_features if not isinstance(r, str)]
        if er:
            extras['require_features'] = er
        if isinstance(remove, str):
            remove = (
             remove,)
        self.remove = remove
        self.extras = extras
        if not (remove or require_features):
            if not extras:
                raise DistutilsSetupError("Feature %s: must define 'require_features', 'remove', or at least one of 'packages', 'py_modules', etc.")

    def include_by_default(self):
        """Should this feature be included by default?"""
        return self.available and self.standard

    def include_in(self, dist):
        """Ensure feature and its requirements are included in distribution

        You may override this in a subclass to perform additional operations on
        the distribution.  Note that this method may be called more than once
        per feature, and so should be idempotent.

        """
        if not self.available:
            raise DistutilsPlatformError(self.description + ' is required, but is not available on this platform')
        (dist.include)(**self.extras)
        for f in self.require_features:
            dist.include_feature(f)

    def exclude_from(self, dist):
        """Ensure feature is excluded from distribution

        You may override this in a subclass to perform additional operations on
        the distribution.  This method will be called at most once per
        feature, and only after all included features have been asked to
        include themselves.
        """
        (dist.exclude)(**self.extras)
        if self.remove:
            for item in self.remove:
                dist.exclude_package(item)

    def validate(self, dist):
        """Verify that feature makes sense in context of distribution

        This method is called by the distribution just before it parses its
        command line.  It checks to ensure that the 'remove' attribute, if any,
        contains only valid package/module names that are present in the base
        distribution when 'setup()' is called.  You may override it in a
        subclass to perform any other required validation of the feature
        against a target distribution.
        """
        for item in self.remove:
            if not dist.has_contents_for(item):
                raise DistutilsSetupError("%s wants to be able to remove %s, but the distribution doesn't contain any packages or modules under %s" % (
                 self.description, item, item))


class DistDeprecationWarning(SetuptoolsDeprecationWarning):
    __doc__ = 'Class for warning about deprecations in dist in\n    setuptools. Not ignored by default, unlike DeprecationWarning.'