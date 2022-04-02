# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\dist.py
__all__ = ['Distribution']
import io, sys, re, os, warnings, numbers, distutils.log, distutils.core, distutils.cmd, distutils.dist, distutils.command
from distutils.util import strtobool
from distutils.debug import DEBUG
from distutils.fancy_getopt import translate_longopt
import itertools
from collections import defaultdict
from email import message_from_file
from distutils.errors import DistutilsOptionError, DistutilsSetupError
from distutils.util import rfc822_escape
from distutils.version import StrictVersion
from setuptools.extern import packaging
from setuptools.extern import ordered_set
from . import SetuptoolsDeprecationWarning
import setuptools, setuptools.command
from setuptools import windows_support
from setuptools.monkey import get_unpatched
from setuptools.config import parse_configuration
import pkg_resources
__import__('setuptools.extern.packaging.specifiers')
__import__('setuptools.extern.packaging.version')

def _get_unpatched(cls):
    warnings.warn('Do not call this function', DistDeprecationWarning)
    return get_unpatched(cls)


def get_metadata_version--- This code section failed: ---

 L.  49         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'self'
                4  LOAD_STR                 'metadata_version'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'mv'

 L.  51        12  LOAD_FAST                'mv'
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE   148  'to 148'

 L.  52        20  LOAD_FAST                'self'
               22  LOAD_ATTR                long_description_content_type
               24  POP_JUMP_IF_TRUE     32  'to 32'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                provides_extras
               30  POP_JUMP_IF_FALSE    42  'to 42'
             32_0  COME_FROM            24  '24'

 L.  53        32  LOAD_GLOBAL              StrictVersion
               34  LOAD_STR                 '2.1'
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'mv'
               40  JUMP_FORWARD        142  'to 142'
             42_0  COME_FROM            30  '30'

 L.  54        42  LOAD_FAST                'self'
               44  LOAD_ATTR                maintainer
               46  LOAD_CONST               None
               48  COMPARE_OP               is-not
               50  POP_JUMP_IF_TRUE     84  'to 84'

 L.  55        52  LOAD_FAST                'self'
               54  LOAD_ATTR                maintainer_email
               56  LOAD_CONST               None
               58  COMPARE_OP               is-not

 L.  54        60  POP_JUMP_IF_TRUE     84  'to 84'

 L.  56        62  LOAD_GLOBAL              getattr
               64  LOAD_FAST                'self'
               66  LOAD_STR                 'python_requires'
               68  LOAD_CONST               None
               70  CALL_FUNCTION_3       3  ''
               72  LOAD_CONST               None
               74  COMPARE_OP               is-not

 L.  54        76  POP_JUMP_IF_TRUE     84  'to 84'

 L.  57        78  LOAD_FAST                'self'
               80  LOAD_ATTR                project_urls

 L.  54        82  POP_JUMP_IF_FALSE    94  'to 94'
             84_0  COME_FROM            76  '76'
             84_1  COME_FROM            60  '60'
             84_2  COME_FROM            50  '50'

 L.  58        84  LOAD_GLOBAL              StrictVersion
               86  LOAD_STR                 '1.2'
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'mv'
               92  JUMP_FORWARD        142  'to 142'
             94_0  COME_FROM            82  '82'

 L.  59        94  LOAD_FAST                'self'
               96  LOAD_ATTR                provides
               98  POP_JUMP_IF_TRUE    124  'to 124'
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                requires
              104  POP_JUMP_IF_TRUE    124  'to 124'
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                obsoletes
              110  POP_JUMP_IF_TRUE    124  'to 124'

 L.  60       112  LOAD_FAST                'self'
              114  LOAD_ATTR                classifiers

 L.  59       116  POP_JUMP_IF_TRUE    124  'to 124'

 L.  60       118  LOAD_FAST                'self'
              120  LOAD_ATTR                download_url

 L.  59       122  POP_JUMP_IF_FALSE   134  'to 134'
            124_0  COME_FROM           116  '116'
            124_1  COME_FROM           110  '110'
            124_2  COME_FROM           104  '104'
            124_3  COME_FROM            98  '98'

 L.  61       124  LOAD_GLOBAL              StrictVersion
              126  LOAD_STR                 '1.1'
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'mv'
              132  JUMP_FORWARD        142  'to 142'
            134_0  COME_FROM           122  '122'

 L.  63       134  LOAD_GLOBAL              StrictVersion
              136  LOAD_STR                 '1.0'
              138  CALL_FUNCTION_1       1  ''
              140  STORE_FAST               'mv'
            142_0  COME_FROM           132  '132'
            142_1  COME_FROM            92  '92'
            142_2  COME_FROM            40  '40'

 L.  65       142  LOAD_FAST                'mv'
              144  LOAD_FAST                'self'
              146  STORE_ATTR               metadata_version
            148_0  COME_FROM            18  '18'

 L.  67       148  LOAD_FAST                'mv'
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 92


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
    else:
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


def single_line(val):
    if '\n' in val:
        warnings.warn('newlines not allowed and will break in the future')
        val = val.replace('\n', ' ')
    return val


def write_pkg_file(self, file):
    """Write the PKG-INFO format data to a file object.
    """
    version = self.get_metadata_version()

    def write_field(key, value):
        file.write('%s: %s\n' % (key, value))

    write_field('Metadata-Version', str(version))
    write_field('Name', self.get_name())
    write_field('Version', self.get_version())
    write_field('Summary', single_line(self.get_description()))
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
                elif version >= StrictVersion('1.2'):
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
    except (TypeError, ValueError, AttributeError, AssertionError) as e:
        try:
            raise DistutilsSetupError("%r must be importable 'module:attrs' string (got %r)" % (
             attr, value)) from e
        finally:
            e = None
            del e


def assert_string_list(dist, attr, value):
    """Verify that value is a string list"""
    try:
        assert isinstance(value, (list, tuple))
        assert ''.join(value) != value
    except (TypeError, ValueError, AttributeError, AssertionError) as e:
        try:
            raise DistutilsSetupError('%r must be a list of strings (got %r)' % (attr, value)) from e
        finally:
            e = None
            del e


def check_nsp(dist, attr, value):
    """Verify that namespace packages are valid"""
    ns_packages = value
    assert_string_list(dist, attr, ns_packages)
    for nsp in ns_packages:
        if not dist.has_contents_for(nsp):
            raise DistutilsSetupError('Distribution contains no modules or packages for ' + 'namespace package %r' % nsp)
        parent, sep, child = nsp.rpartition('.')
        if parent and parent not in ns_packages:
            distutils.log.warn('WARNING: %r is declared as a package namespace, but %r is not: please correct this in setup.py', nsp, parent)


def check_extras(dist, attr, value):
    """Verify that extras_require mapping is valid"""
    try:
        list(itertools.starmap(_check_extra, value.items()))
    except (TypeError, ValueError, AttributeError) as e:
        try:
            raise DistutilsSetupError("'extras_require' must be a dictionary whose values are strings or lists of strings containing valid project/version requirement specifiers.") from e
        finally:
            e = None
            del e


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
            raise DistutilsSetupError(tmpl.format(attr=attr, error=error)) from error
        finally:
            error = None
            del error


def check_specifier(dist, attr, value):
    """Verify that value is a valid version specifier"""
    try:
        packaging.specifiers.SpecifierSet(value)
    except (packaging.specifiers.InvalidSpecifier, AttributeError) as error:
        try:
            tmpl = '{attr!r} must be a string containing valid version specifiers; {error}'
            raise DistutilsSetupError(tmpl.format(attr=attr, error=error)) from error
        finally:
            error = None
            del error


def check_entry_points(dist, attr, value):
    """Verify that entry_points map is parseable"""
    try:
        pkg_resources.EntryPoint.parse_map(value)
    except ValueError as e:
        try:
            raise DistutilsSetupError(e) from e
        finally:
            e = None
            del e


def check_test_suite(dist, attr, value):
    if not isinstance(value, str):
        raise DistutilsSetupError('test_suite must be a string')


def check_package_data(dist, attr, value):
    """Verify that value is a dictionary of package names to glob lists"""
    if not isinstance(value, dict):
        raise DistutilsSetupError('{!r} must be a dictionary mapping package names to lists of string wildcard patterns'.format(attr))
    for k, v in value.items():
        if not isinstance(k, str):
            raise DistutilsSetupError('keys of {!r} dict must be strings (got {!r})'.format(attr, k))
        assert_string_list(dist, 'values of {!r} dict'.format(attr), v)


def check_packages(dist, attr, value):
    for pkgname in value:
        if not re.match('\\w+(\\.\\w+)*', pkgname):
            distutils.log.warn('WARNING: %r not a valid package name; please use only .-separated package names in setup.py', pkgname)


_Distribution = get_unpatched(distutils.core.Distribution)

class Distribution(_Distribution):
    __doc__ = 'Distribution with support for tests and package data\n\n    This is an enhanced version of \'distutils.dist.Distribution\' that\n    effectively adds the following new optional keyword arguments to \'setup()\':\n\n     \'install_requires\' -- a string or sequence of strings specifying project\n        versions that the distribution requires when installed, in the format\n        used by \'pkg_resources.require()\'.  They will be installed\n        automatically when the package is installed.  If you wish to use\n        packages that are not available in PyPI, or want to give your users an\n        alternate download location, you can add a \'find_links\' option to the\n        \'[easy_install]\' section of your project\'s \'setup.cfg\' file, and then\n        setuptools will scan the listed web pages for links that satisfy the\n        requirements.\n\n     \'extras_require\' -- a dictionary mapping names of optional "extras" to the\n        additional requirement(s) that using those extras incurs. For example,\n        this::\n\n            extras_require = dict(reST = ["docutils>=0.3", "reSTedit"])\n\n        indicates that the distribution can optionally provide an extra\n        capability called "reST", but it can only be used if docutils and\n        reSTedit are installed.  If the user installs your package using\n        EasyInstall and requests one of your extras, the corresponding\n        additional requirements will be installed if needed.\n\n     \'test_suite\' -- the name of a test suite to run for the \'test\' command.\n        If the user runs \'python setup.py test\', the package will be installed,\n        and the named test suite will be run.  The format is the same as\n        would be used on a \'unittest.py\' command line.  That is, it is the\n        dotted name of an object to import and call to generate a test suite.\n\n     \'package_data\' -- a dictionary mapping package names to lists of filenames\n        or globs to use to find data files contained in the named packages.\n        If the dictionary has filenames or globs listed under \'""\' (the empty\n        string), those names will be searched for in every package, in addition\n        to any names for the specific package.  Data files found using these\n        names/globs will be installed along with the package, in the same\n        location as the package.  Note that globs are allowed to reference\n        the contents of non-package subdirectories, as long as you use \'/\' as\n        a path separator.  (Globs are automatically converted to\n        platform-specific paths at runtime.)\n\n    In addition to these new keywords, this class also has several new methods\n    for manipulating the distribution\'s contents.  For example, the \'include()\'\n    and \'exclude()\' methods can be thought of as in-place add and subtract\n    commands that add or remove packages, modules, extensions, and so on from\n    the distribution.\n    '
    _DISTUTILS_UNSUPPORTED_METADATA = {'long_description_content_type':None, 
     'project_urls':dict, 
     'provides_extras':ordered_set.OrderedSet, 
     'license_files':ordered_set.OrderedSet}
    _patched_dist = None

    def patch_missing_pkg_info(self, attrs):
        if not attrs or 'name' not in attrs or 'version' not in attrs:
            return
            key = pkg_resources.safe_name(str(attrs['name'])).lower()
            dist = pkg_resources.working_set.by_key.get(key)
            if dist is not None:
                if not dist.has_metadata('PKG-INFO'):
                    dist._version = pkg_resources.safe_version(str(attrs['version']))
                    self._patched_dist = dist

    def __init__--- This code section failed: ---

 L. 422         0  LOAD_GLOBAL              hasattr
                2  LOAD_DEREF               'self'
                4  LOAD_STR                 'package_data'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'have_package_data'

 L. 423        10  LOAD_FAST                'have_package_data'
               12  POP_JUMP_IF_TRUE     20  'to 20'

 L. 424        14  BUILD_MAP_0           0 
               16  LOAD_DEREF               'self'
               18  STORE_ATTR               package_data
             20_0  COME_FROM            12  '12'

 L. 425        20  LOAD_FAST                'attrs'
               22  JUMP_IF_TRUE_OR_POP    26  'to 26'
               24  BUILD_MAP_0           0 
             26_0  COME_FROM            22  '22'
               26  STORE_FAST               'attrs'

 L. 426        28  BUILD_LIST_0          0 
               30  LOAD_DEREF               'self'
               32  STORE_ATTR               dist_files

 L. 428        34  LOAD_FAST                'attrs'
               36  LOAD_METHOD              pop
               38  LOAD_STR                 'src_root'
               40  LOAD_CONST               None
               42  CALL_METHOD_2         2  ''
               44  LOAD_DEREF               'self'
               46  STORE_ATTR               src_root

 L. 429        48  LOAD_DEREF               'self'
               50  LOAD_METHOD              patch_missing_pkg_info
               52  LOAD_FAST                'attrs'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L. 430        58  LOAD_FAST                'attrs'
               60  LOAD_METHOD              pop
               62  LOAD_STR                 'dependency_links'
               64  BUILD_LIST_0          0 
               66  CALL_METHOD_2         2  ''
               68  LOAD_DEREF               'self'
               70  STORE_ATTR               dependency_links

 L. 431        72  LOAD_FAST                'attrs'
               74  LOAD_METHOD              pop
               76  LOAD_STR                 'setup_requires'
               78  BUILD_LIST_0          0 
               80  CALL_METHOD_2         2  ''
               82  LOAD_DEREF               'self'
               84  STORE_ATTR               setup_requires

 L. 432        86  LOAD_GLOBAL              pkg_resources
               88  LOAD_METHOD              iter_entry_points
               90  LOAD_STR                 'distutils.setup_keywords'
               92  CALL_METHOD_1         1  ''
               94  GET_ITER         
               96  FOR_ITER            120  'to 120'
               98  STORE_FAST               'ep'

 L. 433       100  LOAD_GLOBAL              vars
              102  LOAD_DEREF               'self'
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_METHOD              setdefault
              108  LOAD_FAST                'ep'
              110  LOAD_ATTR                name
              112  LOAD_CONST               None
              114  CALL_METHOD_2         2  ''
              116  POP_TOP          
              118  JUMP_BACK            96  'to 96'

 L. 434       120  LOAD_GLOBAL              _Distribution
              122  LOAD_METHOD              __init__
              124  LOAD_DEREF               'self'
              126  LOAD_CLOSURE             'self'
              128  BUILD_TUPLE_1         1 
              130  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              132  LOAD_STR                 'Distribution.__init__.<locals>.<dictcomp>'
              134  MAKE_FUNCTION_8          'closure'

 L. 435       136  LOAD_FAST                'attrs'
              138  LOAD_METHOD              items
              140  CALL_METHOD_0         0  ''

 L. 434       142  GET_ITER         
              144  CALL_FUNCTION_1       1  ''
              146  CALL_METHOD_2         2  ''
              148  POP_TOP          

 L. 442       150  LOAD_DEREF               'self'
              152  LOAD_ATTR                _DISTUTILS_UNSUPPORTED_METADATA
              154  LOAD_METHOD              items
              156  CALL_METHOD_0         0  ''
              158  GET_ITER         
              160  FOR_ITER            236  'to 236'
              162  UNPACK_SEQUENCE_2     2 
              164  STORE_FAST               'option'
              166  STORE_FAST               'default'

 L. 443       168  LOAD_DEREF               'self'
              170  LOAD_ATTR                metadata
              172  LOAD_ATTR                __dict__
              174  LOAD_FAST                'attrs'
              176  BUILD_TUPLE_2         2 
              178  GET_ITER         
            180_0  COME_FROM           190  '190'
              180  FOR_ITER            206  'to 206'
              182  STORE_FAST               'source'

 L. 444       184  LOAD_FAST                'option'
              186  LOAD_FAST                'source'
              188  COMPARE_OP               in
              190  POP_JUMP_IF_FALSE   180  'to 180'

 L. 445       192  LOAD_FAST                'source'
              194  LOAD_FAST                'option'
              196  BINARY_SUBSCR    
              198  STORE_FAST               'value'

 L. 446       200  POP_TOP          
              202  BREAK_LOOP          220  'to 220'
              204  JUMP_BACK           180  'to 180'

 L. 448       206  LOAD_FAST                'default'
              208  POP_JUMP_IF_FALSE   216  'to 216'
              210  LOAD_FAST                'default'
              212  CALL_FUNCTION_0       0  ''
              214  JUMP_FORWARD        218  'to 218'
            216_0  COME_FROM           208  '208'
              216  LOAD_CONST               None
            218_0  COME_FROM           214  '214'
              218  STORE_FAST               'value'

 L. 449       220  LOAD_GLOBAL              setattr
              222  LOAD_DEREF               'self'
              224  LOAD_ATTR                metadata
              226  LOAD_FAST                'option'
              228  LOAD_FAST                'value'
              230  CALL_FUNCTION_3       3  ''
              232  POP_TOP          
              234  JUMP_BACK           160  'to 160'

 L. 451       236  LOAD_DEREF               'self'
              238  LOAD_METHOD              _normalize_version

 L. 452       240  LOAD_DEREF               'self'
              242  LOAD_METHOD              _validate_version
              244  LOAD_DEREF               'self'
              246  LOAD_ATTR                metadata
              248  LOAD_ATTR                version
              250  CALL_METHOD_1         1  ''

 L. 451       252  CALL_METHOD_1         1  ''
              254  LOAD_DEREF               'self'
              256  LOAD_ATTR                metadata
              258  STORE_ATTR               version

 L. 453       260  LOAD_DEREF               'self'
              262  LOAD_METHOD              _finalize_requires
              264  CALL_METHOD_0         0  ''
              266  POP_TOP          

Parse error at or near `LOAD_DICTCOMP' instruction at offset 130

    @staticmethod
    def _normalize_version(version):
        if isinstance(version, setuptools.sic) or version is None:
            return version
        normalized = str(packaging.version.Version(version))
        if version != normalized:
            tmpl = "Normalizing '{version}' to '{normalized}'"
            warnings.warn((tmpl.format)(**))
            return normalized
        return version

    @staticmethod
    def _validate_version(version):
        if isinstance(version, numbers.Number):
            version = str(version)
        if version is not None:
            try:
                packaging.version.Version(version)
            except (packaging.version.InvalidVersion, TypeError):
                warnings.warn('The version specified (%r) is an invalid version, this may not work as expected with newer versions of setuptools, pip, and PyPI. Please see PEP 440 for more details.' % version)
                return setuptools.sic(version)

        return version

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
        complex_reqs = itertools.filterfalse(is_simple_req, inst_reqs)
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
        from configparser import ConfigParser
        ignore_options = [] if sys.prefix == sys.base_prefix else [
         'install-base', 'install-platbase', 'install-lib',
         'install-platlib', 'install-purelib', 'install-headers',
         'install-scripts', 'install-data', 'prefix', 'exec-prefix',
         'home', 'user', 'root']
        ignore_options = frozenset(ignore_options)
        if filenames is None:
            filenames = self.find_config_files()
        if DEBUG:
            self.announce('Distribution.parse_config_files():')
        parser = ConfigParser
        parser.optionxform = str
        for filename in filenames:
            with io.open(filename, encoding='utf-8') as (reader):
                if DEBUG:
                    self.announce(('  reading {filename}'.format)(**))
                parser.read_file(reader)

        for section in parser.sections():
            options = parser.options(section)
            opt_dict = self.get_option_dict(section)
            for opt in options:
                if not opt == '__name__':
                    if opt in ignore_options:
                        pass
                    else:
                        val = parser.get(section, opt)
                        opt = self.warn_dash_deprecation(opt, section)
                        opt = self.make_option_lowercase(opt, section)
                        opt_dict[opt] = (filename, val)
            else:
                parser.__init__()

        else:
            if 'global' not in self.command_options:
                return
            for opt, (src, val) in self.command_options['global'].items():
                alias = self.negative_opt.get(opt)
                if alias:
                    val = not strtobool(val)
                else:
                    if opt in ('verbose', 'dry_run'):
                        val = strtobool(val)
                    try:
                        setattr(self, alias or opt, val)
                    except ValueError as e:
                        try:
                            raise DistutilsOptionError(e) from e
                        finally:
                            e = None
                            del e

    def warn_dash_deprecation(self, opt, section):
        if section in ('options.extras_require', 'options.data_files'):
            return opt
        underscore_opt = opt.replace('-', '_')
        commands = distutils.command.__all__ + setuptools.command.__all__
        if not section.startswith('options'):
            if section != 'metadata':
                if section not in commands:
                    return underscore_opt
        if '-' in opt:
            warnings.warn("Usage of dash-separated '%s' will not be supported in future versions. Please use the underscore name '%s' instead" % (
             opt, underscore_opt))
        return underscore_opt

    def make_option_lowercase(self, opt, section):
        if section != 'metadata' or opt.islower():
            return opt
        lowercase_opt = opt.lower()
        warnings.warn("Usage of uppercase key '%s' in '%s' will be deprecated in future versions. Please use lowercase '%s' instead" % (
         opt, section, lowercase_opt))
        return lowercase_opt

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
                        is_string = isinstance(value, str)
                        if option in neg_opt and is_string:
                            setattr(command_obj, neg_opt[option], not strtobool(value))
                        else:
                            if option in bool_opts and is_string:
                                setattr(command_obj, option, strtobool(value))
                            else:
                                if hasattr(command_obj, option):
                                    setattr(command_obj, option, value)
                                else:
                                    raise DistutilsOptionError("error in %s: command '%s' has no such option '%s'" % (
                                     source, command_name, option))
                    except ValueError as e:
                        try:
                            raise DistutilsOptionError(e) from e
                        finally:
                            e = None
                            del e

    def parse_config_files(self, filenames=None, ignore_option_errors=False):
        """Parses configuration files from various levels
        and loads configuration.

        """
        self._parse_config_files(filenames=filenames)
        parse_configuration(self, (self.command_options), ignore_option_errors=ignore_option_errors)
        self._finalize_requires()

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
        """
        Allow plugins to apply arbitrary operations to the
        distribution. Each hook may optionally define a 'order'
        to influence the order of execution. Smaller numbers
        go first and the default is 0.
        """
        group = 'setuptools.finalize_distribution_options'

        def by_order(hook):
            return getattr(hook, 'order', 0)

        eps = map(lambda e: e.load(), pkg_resources.iter_entry_points(group))
        for ep in sorted(eps, key=by_order):
            ep(self)

    def _finalize_setup_keywords(self):
        for ep in pkg_resources.iter_entry_points('distutils.setup_keywords'):
            value = getattr(self, ep.name, None)
            if value is not None:
                ep.require(installer=(self.fetch_build_egg))
                ep.load()(self, ep.name, value)

    def _finalize_2to3_doctests(self):
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
            with open(readme_txt_filename, 'w') as (f):
                f.write('This directory contains eggs that were downloaded by setuptools to build, test, and run plug-ins.\n\n')
                f.write('This directory caches those eggs to prevent repeated downloads.\n\n')
                f.write('However, it is safe to delete this directory.\n\n')
        return egg_cache_dir

    def fetch_build_egg(self, req):
        """Fetch an egg needed for building"""
        from setuptools.installer import fetch_build_egg
        return fetch_build_egg(self, req)

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
            return _Distribution.print_commands(self)

    def get_command_list(self):
        for ep in pkg_resources.iter_entry_points('distutils.commands'):
            if ep.name not in self.cmdclass:
                cmdclass = ep.resolve()
                self.cmdclass[ep.name] = cmdclass
            return _Distribution.get_command_list(self)

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
            if p == package or p.startswith(pfx):
                return True

    def _exclude_misc(self, name, value):
        """Handle 'exclude()' for list/tuple attrs without a special handler"""
        if not isinstance(value, sequence):
            raise DistutilsSetupError('%s: setting must be a list or tuple (%r)' % (name, value))
        try:
            old = getattr(self, name)
        except AttributeError as e:
            try:
                raise DistutilsSetupError('%s: No such distribution setting' % name) from e
            finally:
                e = None
                del e

        if old is not None and not isinstance(old, sequence):
            raise DistutilsSetupError(name + ': this setting cannot be changed via include/exclude')
        else:
            if old:
                setattr(self, name, [item for item in old if item not in value])

    def _include_misc(self, name, value):
        """Handle 'include()' for list/tuple attrs without a special handler"""
        if not isinstance(value, sequence):
            raise DistutilsSetupError('%s: setting must be a list (%r)' % (name, value))
        else:
            try:
                old = getattr(self, name)
            except AttributeError as e:
                try:
                    raise DistutilsSetupError('%s: No such distribution setting' % name) from e
                finally:
                    e = None
                    del e

            else:
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
        while command in aliases:
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

                    else:
                        if val == 1:
                            val = None
                    d.setdefault(cmd, {})[opt] = val
            else:
                return d

    def iter_distribution_names(self):
        """Yield all packages, modules, and extension names in distribution"""
        for pkg in self.packages or ():
            (yield pkg)
        else:
            for module in self.py_modules or ():
                (yield module)
            else:
                for ext in self.ext_modules or ():
                    if isinstance(ext, tuple):
                        name, buildinfo = ext
                    else:
                        name = ext.name
                    if name.endswith('module'):
                        name = name[:-6]
                    (yield name)

    def handle_display_options(self, option_order):
        """If there were any non-global "display-only" options
        (--help-commands or the metadata display options) on the command
        line, display the requested info and return true; else return
        false.
        """
        import sys
        if self.help_commands:
            return _Distribution.handle_display_options(self, option_order)
        else:
            return isinstance(sys.stdout, io.TextIOWrapper) or _Distribution.handle_display_options(self, option_order)
        if sys.stdout.encoding.lower() in ('utf-8', 'utf8'):
            return _Distribution.handle_display_options(self, option_order)
        encoding = sys.stdout.encoding
        errors = sys.stdout.errors
        newline = sys.platform != 'win32' and '\n' or None
        line_buffering = sys.stdout.line_buffering
        sys.stdout = io.TextIOWrapper(sys.stdout.detach(), 'utf-8', errors, newline, line_buffering)
        try:
            return _Distribution.handle_display_options(self, option_order)
        finally:
            sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding, errors, newline, line_buffering)


class DistDeprecationWarning(SetuptoolsDeprecationWarning):
    __doc__ = 'Class for warning about deprecations in dist in\n    setuptools. Not ignored by default, unlike DeprecationWarning.'