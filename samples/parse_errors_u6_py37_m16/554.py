# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.11 (default, Sep  3 2021, 20:46:09) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\dist.py
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


def get_metadata_version--- This code section failed: ---

 L.  50         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'self'
                4  LOAD_STR                 'metadata_version'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  '3 positional arguments'
               10  STORE_FAST               'mv'

 L.  52        12  LOAD_FAST                'mv'
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE   148  'to 148'

 L.  53        20  LOAD_FAST                'self'
               22  LOAD_ATTR                long_description_content_type
               24  POP_JUMP_IF_TRUE     32  'to 32'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                provides_extras
               30  POP_JUMP_IF_FALSE    42  'to 42'
             32_0  COME_FROM            24  '24'

 L.  54        32  LOAD_GLOBAL              StrictVersion
               34  LOAD_STR                 '2.1'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  STORE_FAST               'mv'
               40  JUMP_FORWARD        142  'to 142'
             42_0  COME_FROM            30  '30'

 L.  55        42  LOAD_FAST                'self'
               44  LOAD_ATTR                maintainer
               46  LOAD_CONST               None
               48  COMPARE_OP               is-not
               50  POP_JUMP_IF_TRUE     84  'to 84'

 L.  56        52  LOAD_FAST                'self'
               54  LOAD_ATTR                maintainer_email
               56  LOAD_CONST               None
               58  COMPARE_OP               is-not
               60  POP_JUMP_IF_TRUE     84  'to 84'

 L.  57        62  LOAD_GLOBAL              getattr
               64  LOAD_FAST                'self'
               66  LOAD_STR                 'python_requires'
               68  LOAD_CONST               None
               70  CALL_FUNCTION_3       3  '3 positional arguments'
               72  LOAD_CONST               None
               74  COMPARE_OP               is-not
               76  POP_JUMP_IF_TRUE     84  'to 84'

 L.  58        78  LOAD_FAST                'self'
               80  LOAD_ATTR                project_urls
               82  POP_JUMP_IF_FALSE    94  'to 94'
             84_0  COME_FROM            76  '76'
             84_1  COME_FROM            60  '60'
             84_2  COME_FROM            50  '50'

 L.  59        84  LOAD_GLOBAL              StrictVersion
               86  LOAD_STR                 '1.2'
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  STORE_FAST               'mv'
               92  JUMP_FORWARD        142  'to 142'
             94_0  COME_FROM            82  '82'

 L.  60        94  LOAD_FAST                'self'
               96  LOAD_ATTR                provides
               98  POP_JUMP_IF_TRUE    124  'to 124'
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                requires
              104  POP_JUMP_IF_TRUE    124  'to 124'
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                obsoletes
              110  POP_JUMP_IF_TRUE    124  'to 124'

 L.  61       112  LOAD_FAST                'self'
              114  LOAD_ATTR                classifiers
              116  POP_JUMP_IF_TRUE    124  'to 124'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                download_url
              122  POP_JUMP_IF_FALSE   134  'to 134'
            124_0  COME_FROM           116  '116'
            124_1  COME_FROM           110  '110'
            124_2  COME_FROM           104  '104'
            124_3  COME_FROM            98  '98'

 L.  62       124  LOAD_GLOBAL              StrictVersion
              126  LOAD_STR                 '1.1'
              128  CALL_FUNCTION_1       1  '1 positional argument'
              130  STORE_FAST               'mv'
              132  JUMP_FORWARD        142  'to 142'
            134_0  COME_FROM           122  '122'

 L.  64       134  LOAD_GLOBAL              StrictVersion
              136  LOAD_STR                 '1.0'
              138  CALL_FUNCTION_1       1  '1 positional argument'
              140  STORE_FAST               'mv'
            142_0  COME_FROM           132  '132'
            142_1  COME_FROM            92  '92'
            142_2  COME_FROM            40  '40'

 L.  66       142  LOAD_FAST                'mv'
              144  LOAD_FAST                'self'
              146  STORE_ATTR               metadata_version
            148_0  COME_FROM            18  '18'

 L.  68       148  LOAD_FAST                'mv'
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

    write_field('License', self.get_license())
    if self.download_url:
        write_field('Download-URL', self.download_url)
    for project_url in self.project_urls.items():
        write_field('Project-URL', '%s, %s' % project_url)

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


sequence = (tuple, list)

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
        parent, sep, child = nsp.rpartition('.')
        if parent and parent not in ns_packages:
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
        if not attrs or 'name' not in attrs or 'version' not in attrs:
            return
            key = pkg_resources.safe_name(str(attrs['name'])).lower()
            dist = pkg_resources.working_set.by_key.get(key)
            if dist is not None:
                if not dist.has_metadata('PKG-INFO'):
                    dist._version = pkg_resources.safe_version(str(attrs['version']))
                    self._patched_dist = dist

    def __init__(self, attrs=None):
        have_package_data = hasattr(self, 'package_data')
        if not have_package_data:
            self.package_data = {}
        attrs = attrs or {}
        if 'features' in attrs or 'require_features' in attrs:
            Feature.warn_deprecated()
        self.require_features = []
        self.features = {}
        self.dist_files = []
        self.src_root = attrs.pop('src_root', None)
        self.patch_missing_pkg_info(attrs)
        self.dependency_links = attrs.pop('dependency_links', [])
        self.setup_requires = attrs.pop('setup_requires', [])
        for ep in pkg_resources.iter_entry_points('distutils.setup_keywords'):
            vars(self).setdefault(ep.name, None)

        _Distribution.__init__(self, {k:v for k, v in attrs.items() if k not in self._DISTUTILS_UNSUPPORTED_METADATA})
        for option, default in self._DISTUTILS_UNSUPPORTED_METADATA.items():
            for source in (self.metadata.__dict__, attrs):
                if option in source:
                    value = source[option]
                    break
            else:
                value = default() if default else None

            setattr(self.metadata, option, value)

        if isinstance(self.metadata.version, numbers.Number):
            self.metadata.version = str(self.metadata.version)
        if self.metadata.version is not None:
            try:
                ver = packaging.version.Version(self.metadata.version)
                normalized_version = str(ver)
                if self.metadata.version != normalized_version:
                    warnings.warn("Normalizing '%s' to '%s'" % (
                     self.metadata.version,
                     normalized_version))
                    self.metadata.version = normalized_version
            except (packaging.version.InvalidVersion, TypeError):
                warnings.warn('The version specified (%r) is an invalid version, this may not work as expected with newer versions of setuptools, pip, and PyPI. Please see PEP 440 for more details.' % self.metadata.version)

        self._finalize_requires()

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

        self.extras_require = dict(((k,
         [str(r) for r in map(self._clean_req, v)]) for k, v in self._tmp_extras_require.items()))

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
        parser = ConfigParser()
        for filename in filenames:
            with io.open(filename, encoding='utf-8') as (reader):
                if DEBUG:
                    self.announce(('  reading {filename}'.format)(**locals()))
                parser.read_file if six.PY3 else parser.readfp(reader)
            for section in parser.sections():
                options = parser.options(section)
                opt_dict = self.get_option_dict(section)
                for opt in options:
                    if opt != '__name__' and opt not in ignore_options:
                        val = self._try_str(parser.get(section, opt))
                        opt = opt.replace('-', '_')
                        opt_dict[opt] = (filename, val)

            parser.__init__()

        if 'global' in self.command_options:
            for opt, (src, val) in self.command_options['global'].items():
                alias = self.negative_opt.get(opt)
                try:
                    if alias:
                        setattr(self, alias, not strtobool(val))
                    else:
                        if opt in ('verbose', 'dry_run'):
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
    def _try_str(val):
        """
        On Python 2, much of distutils relies on string values being of
        type 'str' (bytes) and not unicode text. If the value can be safely
        encoded to bytes using the default encoding, prefer that.

        Why the default encoding? Because that value can be implicitly
        decoded back to text if needed.

        Ref #1653
        """
        if six.PY3:
            return val
        try:
            return val.encode()
        except UnicodeEncodeError:
            pass

        return val

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

            try:
                neg_opt = command_obj.negative_opt
            except AttributeError:
                neg_opt = {}

            try:
                is_string = isinstance(value, six.string_types)
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

        return resolved_dists

    def finalize_options(self):
        _Distribution.finalize_options(self)
        if self.features:
            self._set_global_opts_from_features()
        else:
            for ep in pkg_resources.iter_entry_points('distutils.setup_keywords'):
                value = getattr(self, ep.name, None)
                if value is not None:
                    ep.require(installer=(self.fetch_build_egg))
                    ep.load()(self, ep.name, value)

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
        import setuptools.command.easy_install as easy_install
        dist = self.__class__({'script_args': ['easy_install']})
        opts = dist.get_option_dict('easy_install')
        opts.clear()
        opts.update(((k, v) for k, v in self.get_option_dict('easy_install').items() if k in ('find_links',
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
                new = (
                 (
                  'with-' + name, None, 'include ' + descr + incdef),
                 (
                  'without-' + name, None, 'exclude ' + descr + excdef))
                go.extend(new)
                no['without-' + name] = 'with-' + name

        self.global_options = self.feature_options = go + self.global_options
        self.negative_opt = self.feature_negopt = no

    def _finalize_features(self):
        """Add/remove features and resolve dependencies between them"""
        for name, feature in self.features.items():
            enabled = self.feature_is_included(name)
            if not enabled:
                if not enabled is None or feature.include_by_default():
                    feature.include_in(self)
                    self._set_feature(name, 1)

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
        else:
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
            if p == package or p.startswith(pfx):
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
            except AttributeError:
                raise DistutilsSetupError('%s: No such distribution setting' % name)

            if old is None:
                setattr(self, name, value)
            else:
                if not isinstance(old, sequence):
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

    def get_cmdline_options--- This code section failed: ---

 L.1041         0  BUILD_MAP_0           0 
                2  STORE_FAST               'd'

 L.1043         4  SETUP_LOOP          200  'to 200'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                command_options
               10  LOAD_METHOD              items
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  GET_ITER         
               16  FOR_ITER            198  'to 198'
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'cmd'
               22  STORE_FAST               'opts'

 L.1045        24  SETUP_LOOP          196  'to 196'
               26  LOAD_FAST                'opts'
               28  LOAD_METHOD              items
               30  CALL_METHOD_0         0  '0 positional arguments'
               32  GET_ITER         
               34  FOR_ITER            194  'to 194'
               36  UNPACK_SEQUENCE_2     2 
               38  STORE_FAST               'opt'
               40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'src'
               44  STORE_FAST               'val'

 L.1047        46  LOAD_FAST                'src'
               48  LOAD_STR                 'command line'
               50  COMPARE_OP               !=
               52  POP_JUMP_IF_FALSE    56  'to 56'

 L.1048        54  CONTINUE             34  'to 34'
             56_0  COME_FROM            52  '52'

 L.1050        56  LOAD_FAST                'opt'
               58  LOAD_METHOD              replace
               60  LOAD_STR                 '_'
               62  LOAD_STR                 '-'
               64  CALL_METHOD_2         2  '2 positional arguments'
               66  STORE_FAST               'opt'

 L.1052        68  LOAD_FAST                'val'
               70  LOAD_CONST               0
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE   164  'to 164'

 L.1053        76  LOAD_FAST                'self'
               78  LOAD_METHOD              get_command_obj
               80  LOAD_FAST                'cmd'
               82  CALL_METHOD_1         1  '1 positional argument'
               84  STORE_FAST               'cmdobj'

 L.1054        86  LOAD_FAST                'self'
               88  LOAD_ATTR                negative_opt
               90  LOAD_METHOD              copy
               92  CALL_METHOD_0         0  '0 positional arguments'
               94  STORE_FAST               'neg_opt'

 L.1055        96  LOAD_FAST                'neg_opt'
               98  LOAD_METHOD              update
              100  LOAD_GLOBAL              getattr
              102  LOAD_FAST                'cmdobj'
              104  LOAD_STR                 'negative_opt'
              106  BUILD_MAP_0           0 
              108  CALL_FUNCTION_3       3  '3 positional arguments'
              110  CALL_METHOD_1         1  '1 positional argument'
              112  POP_TOP          

 L.1056       114  SETUP_LOOP          176  'to 176'
              116  LOAD_FAST                'neg_opt'
              118  LOAD_METHOD              items
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  GET_ITER         
            124_0  COME_FROM           138  '138'
              124  FOR_ITER            152  'to 152'
              126  UNPACK_SEQUENCE_2     2 
              128  STORE_FAST               'neg'
              130  STORE_FAST               'pos'

 L.1057       132  LOAD_FAST                'pos'
              134  LOAD_FAST                'opt'
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   124  'to 124'

 L.1058       140  LOAD_FAST                'neg'
              142  STORE_FAST               'opt'

 L.1059       144  LOAD_CONST               None
              146  STORE_FAST               'val'

 L.1060       148  BREAK_LOOP       
              150  JUMP_BACK           124  'to 124'
              152  POP_BLOCK        

 L.1062       154  LOAD_GLOBAL              AssertionError
              156  LOAD_STR                 "Shouldn't be able to get here"
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  RAISE_VARARGS_1       1  'exception instance'
              162  JUMP_FORWARD        176  'to 176'
            164_0  COME_FROM            74  '74'

 L.1064       164  LOAD_FAST                'val'
              166  LOAD_CONST               1
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   176  'to 176'

 L.1065       172  LOAD_CONST               None
              174  STORE_FAST               'val'
            176_0  COME_FROM           170  '170'
            176_1  COME_FROM           162  '162'
            176_2  COME_FROM_LOOP      114  '114'

 L.1067       176  LOAD_FAST                'val'
              178  LOAD_FAST                'd'
              180  LOAD_METHOD              setdefault
              182  LOAD_FAST                'cmd'
              184  BUILD_MAP_0           0 
              186  CALL_METHOD_2         2  '2 positional arguments'
              188  LOAD_FAST                'opt'
              190  STORE_SUBSCR     
              192  JUMP_BACK            34  'to 34'
              194  POP_BLOCK        
            196_0  COME_FROM_LOOP       24  '24'
              196  JUMP_BACK            16  'to 16'
              198  POP_BLOCK        
            200_0  COME_FROM_LOOP        4  '4'

 L.1069       200  LOAD_FAST                'd'
              202  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 176

    def iter_distribution_names(self):
        """Yield all packages, modules, and extension names in distribution"""
        for pkg in self.packages or ():
            yield pkg

        for module in self.py_modules or ():
            yield module

        for ext in self.ext_modules or ():
            if isinstance(ext, tuple):
                name, buildinfo = ext
            else:
                name = ext.name
            if name.endswith('module'):
                name = name[:-6]
            yield name

    def handle_display_options(self, option_order):
        """If there were any non-global "display-only" options
        (--help-commands or the metadata display options) on the command
        line, display the requested info and return true; else return
        false.
        """
        import sys
        if six.PY2 or self.help_commands:
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
        if not remove:
            if not require_features:
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