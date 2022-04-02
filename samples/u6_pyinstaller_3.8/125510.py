# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\config.py
from __future__ import absolute_import, unicode_literals
import ast, io, os, sys, warnings, functools, importlib
from collections import defaultdict
from functools import partial
from functools import wraps
import contextlib
from distutils.errors import DistutilsOptionError, DistutilsFileError
from setuptools.extern.packaging.version import LegacyVersion, parse
from setuptools.extern.packaging.specifiers import SpecifierSet
from setuptools.extern.six import string_types, PY3
__metaclass__ = type

class StaticModule:
    __doc__ = '\n    Attempt to load the module by the name\n    '

    def __init__(self, name):
        spec = importlib.util.find_spec(name)
        with open(spec.origin) as (strm):
            src = strm.read()
        module = ast.parse(src)
        vars(self).update(locals())
        del self.self

    def __getattr__(self, attr):
        try:
            return next((ast.literal_eval(statement.value) for statement in self.module.body if isinstance(statement, ast.Assign) for target in statement.targets))
            except Exception as e:
            try:
                raise AttributeError(('{self.name} has no attribute {attr}'.format)(**locals())) from e
            finally:
                e = None
                del e


@contextlib.contextmanager
def patch_path(path):
    """
    Add path to front of sys.path for the duration of the context.
    """
    try:
        sys.path.insert(0, path)
        (yield)
    finally:
        sys.path.remove(path)


def read_configuration(filepath, find_others=False, ignore_option_errors=False):
    """Read given configuration file and returns options from it as a dict.

    :param str|unicode filepath: Path to configuration file
        to get options from.

    :param bool find_others: Whether to search for other configuration files
        which could be on in various places.

    :param bool ignore_option_errors: Whether to silently ignore
        options, values of which could not be resolved (e.g. due to exceptions
        in directives such as file:, attr:, etc.).
        If False exceptions are propagated as expected.

    :rtype: dict
    """
    from setuptools.dist import Distribution, _Distribution
    filepath = os.path.abspath(filepath)
    if not os.path.isfile(filepath):
        raise DistutilsFileError('Configuration file %s does not exist.' % filepath)
    current_directory = os.getcwd()
    os.chdir(os.path.dirname(filepath))
    try:
        dist = Distribution()
        filenames = dist.find_config_files() if find_others else []
        if filepath not in filenames:
            filenames.append(filepath)
        _Distribution.parse_config_files(dist, filenames=filenames)
        handlers = parse_configuration(dist,
          (dist.command_options), ignore_option_errors=ignore_option_errors)
    finally:
        os.chdir(current_directory)

    return configuration_to_dict(handlers)


def _get_option(target_obj, key):
    """
    Given a target object and option key, get that option from
    the target object, either through a get_{key} method or
    from an attribute directly.
    """
    getter_name = ('get_{key}'.format)(**locals())
    by_attribute = functools.partial(getattr, target_obj, key)
    getter = getattr(target_obj, getter_name, by_attribute)
    return getter()


def configuration_to_dict(handlers):
    """Returns configuration data gathered by given handlers as a dict.

    :param list[ConfigHandler] handlers: Handlers list,
        usually from parse_configuration()

    :rtype: dict
    """
    config_dict = defaultdict(dict)
    for handler in handlers:
        for option in handler.set_options:
            value = _get_option(handler.target_obj, option)
            config_dict[handler.section_prefix][option] = value
        else:
            return config_dict


def parse_configuration(distribution, command_options, ignore_option_errors=False):
    """Performs additional parsing of configuration options
    for a distribution.

    Returns a list of used option handlers.

    :param Distribution distribution:
    :param dict command_options:
    :param bool ignore_option_errors: Whether to silently ignore
        options, values of which could not be resolved (e.g. due to exceptions
        in directives such as file:, attr:, etc.).
        If False exceptions are propagated as expected.
    :rtype: list
    """
    options = ConfigOptionsHandler(distribution, command_options, ignore_option_errors)
    options.parse()
    meta = ConfigMetadataHandler(distribution.metadata, command_options, ignore_option_errors, distribution.package_dir)
    meta.parse()
    return (
     meta, options)


class ConfigHandler:
    __doc__ = 'Handles metadata supplied in configuration files.'
    section_prefix = None
    aliases = {}

    def __init__(self, target_obj, options, ignore_option_errors=False):
        sections = {}
        section_prefix = self.section_prefix
        for section_name, section_options in options.items():
            if not section_name.startswith(section_prefix):
                pass
            else:
                section_name = section_name.replace(section_prefix, '').strip('.')
                sections[section_name] = section_options
        else:
            self.ignore_option_errors = ignore_option_errors
            self.target_obj = target_obj
            self.sections = sections
            self.set_options = []

    @property
    def parsers(self):
        """Metadata item name to parser function mapping."""
        raise NotImplementedError('%s must provide .parsers property' % self.__class__.__name__)

    def __setitem__(self, option_name, value):
        unknown = tuple()
        target_obj = self.target_obj
        option_name = self.aliases.get(option_name, option_name)
        current_value = getattr(target_obj, option_name, unknown)
        if current_value is unknown:
            raise KeyError(option_name)
        elif current_value:
            return
            skip_option = False
            parser = self.parsers.get(option_name)
            if parser:
                try:
                    value = parser(value)
                except Exception:
                    skip_option = True
                    if not self.ignore_option_errors:
                        raise

            if skip_option:
                return
            setter = getattr(target_obj, 'set_%s' % option_name, None)
            if setter is None:
                setattr(target_obj, option_name, value)
        else:
            setter(value)
        self.set_options.append(option_name)

    @classmethod
    def _parse_list(cls, value, separator=','):
        """Represents value as a list.

        Value is split either by separator (defaults to comma) or by lines.

        :param value:
        :param separator: List items separator character.
        :rtype: list
        """
        if isinstance(value, list):
            return value
        elif '\n' in value:
            value = value.splitlines()
        else:
            value = value.split(separator)
        return [chunk.strip() for chunk in value if chunk.strip()]

    @classmethod
    def _parse_dict(cls, value):
        """Represents value as a dict.

        :param value:
        :rtype: dict
        """
        separator = '='
        result = {}
        for line in cls._parse_list(value):
            key, sep, val = line.partition(separator)
            if sep != separator:
                raise DistutilsOptionError('Unable to parse option value to dict: %s' % value)
            result[key.strip()] = val.strip()
        else:
            return result

    @classmethod
    def _parse_bool(cls, value):
        """Represents value as boolean.

        :param value:
        :rtype: bool
        """
        value = value.lower()
        return value in ('1', 'true', 'yes')

    @classmethod
    def _exclude_files_parser(cls, key):
        """Returns a parser function to make sure field inputs
        are not files.

        Parses a value after getting the key so error messages are
        more informative.

        :param key:
        :rtype: callable
        """

        def parser(value):
            exclude_directive = 'file:'
            if value.startswith(exclude_directive):
                raise ValueError('Only strings are accepted for the {0} field, files are not accepted'.format(key))
            return value

        return parser

    @classmethod
    def _parse_file(cls, value):
        """Represents value as a string, allowing including text
        from nearest files using `file:` directive.

        Directive is sandboxed and won't reach anything outside
        directory with setup.py.

        Examples:
            file: README.rst, CHANGELOG.md, src/file.txt

        :param str value:
        :rtype: str
        """
        include_directive = 'file:'
        if not isinstance(value, string_types):
            return value
        else:
            return value.startswith(include_directive) or value
        spec = value[len(include_directive):]
        filepaths = (os.path.abspath(path.strip()) for path in spec.split(','))
        return '\n'.join((cls._read_file(path) for path in filepaths if cls._assert_local(path) or os.path.isfile(path)))

    @staticmethod
    def _assert_local(filepath):
        if not filepath.startswith(os.getcwd()):
            raise DistutilsOptionError('`file:` directive can not access %s' % filepath)

    @staticmethod
    def _read_file--- This code section failed: ---

 L. 350         0  LOAD_GLOBAL              io
                2  LOAD_ATTR                open
                4  LOAD_FAST                'filepath'
                6  LOAD_STR                 'utf-8'
                8  LOAD_CONST               ('encoding',)
               10  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               12  SETUP_WITH           36  'to 36'
               14  STORE_FAST               'f'

 L. 351        16  LOAD_FAST                'f'
               18  LOAD_METHOD              read
               20  CALL_METHOD_0         0  ''
               22  POP_BLOCK        
               24  ROT_TWO          
               26  BEGIN_FINALLY    
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  POP_FINALLY           0  ''
               34  RETURN_VALUE     
             36_0  COME_FROM_WITH       12  '12'
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 24

    @classmethod
    def _parse_attr--- This code section failed: ---

 L. 364         0  LOAD_STR                 'attr:'
                2  STORE_FAST               'attr_directive'

 L. 365         4  LOAD_FAST                'value'
                6  LOAD_METHOD              startswith
                8  LOAD_FAST                'attr_directive'
               10  CALL_METHOD_1         1  ''
               12  POP_JUMP_IF_TRUE     18  'to 18'

 L. 366        14  LOAD_FAST                'value'
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L. 368        18  LOAD_FAST                'value'
               20  LOAD_METHOD              replace
               22  LOAD_FAST                'attr_directive'
               24  LOAD_STR                 ''
               26  CALL_METHOD_2         2  ''
               28  LOAD_METHOD              strip
               30  CALL_METHOD_0         0  ''
               32  LOAD_METHOD              split
               34  LOAD_STR                 '.'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'attrs_path'

 L. 369        40  LOAD_FAST                'attrs_path'
               42  LOAD_METHOD              pop
               44  CALL_METHOD_0         0  ''
               46  STORE_FAST               'attr_name'

 L. 371        48  LOAD_STR                 '.'
               50  LOAD_METHOD              join
               52  LOAD_FAST                'attrs_path'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'module_name'

 L. 372        58  LOAD_FAST                'module_name'
               60  JUMP_IF_TRUE_OR_POP    64  'to 64'
               62  LOAD_STR                 '__init__'
             64_0  COME_FROM            60  '60'
               64  STORE_FAST               'module_name'

 L. 374        66  LOAD_GLOBAL              os
               68  LOAD_METHOD              getcwd
               70  CALL_METHOD_0         0  ''
               72  STORE_FAST               'parent_path'

 L. 375        74  LOAD_FAST                'package_dir'
               76  POP_JUMP_IF_FALSE   194  'to 194'

 L. 376        78  LOAD_FAST                'attrs_path'
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'package_dir'
               86  COMPARE_OP               in
               88  POP_JUMP_IF_FALSE   164  'to 164'

 L. 378        90  LOAD_FAST                'package_dir'
               92  LOAD_FAST                'attrs_path'
               94  LOAD_CONST               0
               96  BINARY_SUBSCR    
               98  BINARY_SUBSCR    
              100  STORE_FAST               'custom_path'

 L. 379       102  LOAD_FAST                'custom_path'
              104  LOAD_METHOD              rsplit
              106  LOAD_STR                 '/'
              108  LOAD_CONST               1
              110  CALL_METHOD_2         2  ''
              112  STORE_FAST               'parts'

 L. 380       114  LOAD_GLOBAL              len
              116  LOAD_FAST                'parts'
              118  CALL_FUNCTION_1       1  ''
              120  LOAD_CONST               1
              122  COMPARE_OP               >
              124  POP_JUMP_IF_FALSE   158  'to 158'

 L. 381       126  LOAD_GLOBAL              os
              128  LOAD_ATTR                path
              130  LOAD_METHOD              join
              132  LOAD_GLOBAL              os
              134  LOAD_METHOD              getcwd
              136  CALL_METHOD_0         0  ''
              138  LOAD_FAST                'parts'
              140  LOAD_CONST               0
              142  BINARY_SUBSCR    
              144  CALL_METHOD_2         2  ''
              146  STORE_FAST               'parent_path'

 L. 382       148  LOAD_FAST                'parts'
              150  LOAD_CONST               1
              152  BINARY_SUBSCR    
              154  STORE_FAST               'module_name'
              156  JUMP_ABSOLUTE       194  'to 194'
            158_0  COME_FROM           124  '124'

 L. 384       158  LOAD_FAST                'custom_path'
              160  STORE_FAST               'module_name'
              162  JUMP_FORWARD        194  'to 194'
            164_0  COME_FROM            88  '88'

 L. 385       164  LOAD_STR                 ''
              166  LOAD_FAST                'package_dir'
              168  COMPARE_OP               in
              170  POP_JUMP_IF_FALSE   194  'to 194'

 L. 387       172  LOAD_GLOBAL              os
              174  LOAD_ATTR                path
              176  LOAD_METHOD              join
              178  LOAD_GLOBAL              os
              180  LOAD_METHOD              getcwd
              182  CALL_METHOD_0         0  ''
              184  LOAD_FAST                'package_dir'
              186  LOAD_STR                 ''
              188  BINARY_SUBSCR    
              190  CALL_METHOD_2         2  ''
              192  STORE_FAST               'parent_path'
            194_0  COME_FROM           170  '170'
            194_1  COME_FROM           162  '162'
            194_2  COME_FROM            76  '76'

 L. 389       194  LOAD_GLOBAL              patch_path
              196  LOAD_FAST                'parent_path'
              198  CALL_FUNCTION_1       1  ''
              200  SETUP_WITH          270  'to 270'
              202  POP_TOP          

 L. 390       204  SETUP_FINALLY       234  'to 234'

 L. 392       206  LOAD_GLOBAL              getattr
              208  LOAD_GLOBAL              StaticModule
              210  LOAD_FAST                'module_name'
              212  CALL_FUNCTION_1       1  ''
              214  LOAD_FAST                'attr_name'
              216  CALL_FUNCTION_2       2  ''
              218  POP_BLOCK        
              220  POP_BLOCK        
              222  ROT_TWO          
              224  BEGIN_FINALLY    
              226  WITH_CLEANUP_START
              228  WITH_CLEANUP_FINISH
              230  POP_FINALLY           0  ''
              232  RETURN_VALUE     
            234_0  COME_FROM_FINALLY   204  '204'

 L. 393       234  DUP_TOP          
              236  LOAD_GLOBAL              Exception
              238  COMPARE_OP               exception-match
          240_242  POP_JUMP_IF_FALSE   264  'to 264'
              244  POP_TOP          
              246  POP_TOP          
              248  POP_TOP          

 L. 395       250  LOAD_GLOBAL              importlib
              252  LOAD_METHOD              import_module
              254  LOAD_FAST                'module_name'
              256  CALL_METHOD_1         1  ''
              258  STORE_FAST               'module'
              260  POP_EXCEPT       
              262  JUMP_FORWARD        266  'to 266'
            264_0  COME_FROM           240  '240'
              264  END_FINALLY      
            266_0  COME_FROM           262  '262'
              266  POP_BLOCK        
              268  BEGIN_FINALLY    
            270_0  COME_FROM_WITH      200  '200'
              270  WITH_CLEANUP_START
              272  WITH_CLEANUP_FINISH
              274  END_FINALLY      

 L. 397       276  LOAD_GLOBAL              getattr
              278  LOAD_FAST                'module'
              280  LOAD_FAST                'attr_name'
              282  CALL_FUNCTION_2       2  ''
              284  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 220

    @classmethod
    def _get_parser_compound(cls, *parse_methods):
        """Returns parser function to represents value as a list.

        Parses a value applying given methods one after another.

        :param parse_methods:
        :rtype: callable
        """

        def parse(value):
            parsed = value
            for method in parse_methods:
                parsed = method(parsed)
            else:
                return parsed

        return parse

    @classmethod
    def _parse_section_to_dict(cls, section_options, values_parser=None):
        """Parses section options into a dictionary.

        Optionally applies a given parser to values.

        :param dict section_options:
        :param callable values_parser:
        :rtype: dict
        """
        value = {}
        values_parser = values_parser or (lambda val: val)
        for key, (_, val) in section_options.items():
            value[key] = values_parser(val)
        else:
            return value

    def parse_section(self, section_options):
        """Parses configuration file section.

        :param dict section_options:
        """
        for name, (_, value) in section_options.items():
            try:
                self[name] = value
            except KeyError:
                pass

    def parse(self):
        """Parses configuration file items from one
        or more related sections.

        """
        for section_name, section_options in self.sections.items():
            method_postfix = ''
            if section_name:
                method_postfix = '_%s' % section_name
            section_parser_method = getattr(self, ('parse_section%s' % method_postfix).replace('.', '__'), None)
            if section_parser_method is None:
                raise DistutilsOptionError('Unsupported distribution option section: [%s.%s]' % (
                 self.section_prefix, section_name))
            section_parser_method(section_options)

    def _deprecated_config_handler(self, func, msg, warning_class):
        """ this function will wrap around parameters that are deprecated

        :param msg: deprecation message
        :param warning_class: class of warning exception to be raised
        :param func: function to be wrapped around
        """

        @wraps(func)
        def config_handler(*args, **kwargs):
            warnings.warn(msg, warning_class)
            return func(*args, **kwargs)

        return config_handler


class ConfigMetadataHandler(ConfigHandler):
    section_prefix = 'metadata'
    aliases = {'home_page':'url', 
     'summary':'description', 
     'classifier':'classifiers', 
     'platform':'platforms'}
    strict_mode = False

    def __init__(self, target_obj, options, ignore_option_errors=False, package_dir=None):
        super(ConfigMetadataHandler, self).__init__(target_obj, options, ignore_option_errors)
        self.package_dir = package_dir

    @property
    def parsers(self):
        """Metadata item name to parser function mapping."""
        parse_list = self._parse_list
        parse_file = self._parse_file
        parse_dict = self._parse_dict
        exclude_files_parser = self._exclude_files_parser
        return {'platforms':parse_list, 
         'keywords':parse_list, 
         'provides':parse_list, 
         'requires':self._deprecated_config_handler(parse_list, 'The requires parameter is deprecated, please use install_requires for runtime dependencies.', DeprecationWarning), 
         'obsoletes':parse_list, 
         'classifiers':self._get_parser_compound(parse_file, parse_list), 
         'license':exclude_files_parser('license'), 
         'license_files':parse_list, 
         'description':parse_file, 
         'long_description':parse_file, 
         'version':self._parse_version, 
         'project_urls':parse_dict}

    def _parse_version(self, value):
        """Parses `version` option value.

        :param value:
        :rtype: str

        """
        version = self._parse_file(value)
        if version != value:
            version = version.strip()
            if isinstance(parse(version), LegacyVersion):
                tmpl = 'Version loaded from {value} does not comply with PEP 440: {version}'
                raise DistutilsOptionError((tmpl.format)(**locals()))
            return version
        version = self._parse_attr(value, self.package_dir)
        if callable(version):
            version = version()
        elif (isinstance(version, string_types) or hasattr)(version, '__iter__'):
            version = '.'.join(map(str, version))
        else:
            version = '%s' % version
        return version


class ConfigOptionsHandler(ConfigHandler):
    section_prefix = 'options'

    @property
    def parsers(self):
        """Metadata item name to parser function mapping."""
        parse_list = self._parse_list
        parse_list_semicolon = partial((self._parse_list), separator=';')
        parse_bool = self._parse_bool
        parse_dict = self._parse_dict
        return {'zip_safe':parse_bool, 
         'use_2to3':parse_bool, 
         'include_package_data':parse_bool, 
         'package_dir':parse_dict, 
         'use_2to3_fixers':parse_list, 
         'use_2to3_exclude_fixers':parse_list, 
         'convert_2to3_doctests':parse_list, 
         'scripts':parse_list, 
         'eager_resources':parse_list, 
         'dependency_links':parse_list, 
         'namespace_packages':parse_list, 
         'install_requires':parse_list_semicolon, 
         'setup_requires':parse_list_semicolon, 
         'tests_require':parse_list_semicolon, 
         'packages':self._parse_packages, 
         'entry_points':self._parse_file, 
         'py_modules':parse_list, 
         'python_requires':SpecifierSet}

    def _parse_packages(self, value):
        """Parses `packages` option value.

        :param value:
        :rtype: list
        """
        find_directives = [
         'find:', 'find_namespace:']
        trimmed_value = value.strip()
        if trimmed_value not in find_directives:
            return self._parse_list(value)
        findns = trimmed_value == find_directives[1]
        if findns:
            if not PY3:
                raise DistutilsOptionError('find_namespace: directive is unsupported on Python < 3.3')
        else:
            find_kwargs = self.parse_section_packages__find(self.sections.get('packages.find', {}))
            if findns:
                from setuptools import find_namespace_packages as find_packages
            else:
                from setuptools import find_packages
        return find_packages(**find_kwargs)

    def parse_section_packages__find(self, section_options):
        """Parses `packages.find` configuration file section.

        To be used in conjunction with _parse_packages().

        :param dict section_options:
        """
        section_data = self._parse_section_to_dict(section_options, self._parse_list)
        valid_keys = [
         'where', 'include', 'exclude']
        find_kwargs = dict([(
         k, v) for k, v in section_data.items() if k in valid_keys if v])
        where = find_kwargs.get('where')
        if where is not None:
            find_kwargs['where'] = where[0]
        return find_kwargs

    def parse_section_entry_points(self, section_options):
        """Parses `entry_points` configuration file section.

        :param dict section_options:
        """
        parsed = self._parse_section_to_dict(section_options, self._parse_list)
        self['entry_points'] = parsed

    def _parse_package_data(self, section_options):
        parsed = self._parse_section_to_dict(section_options, self._parse_list)
        root = parsed.get('*')
        if root:
            parsed[''] = root
            del parsed['*']
        return parsed

    def parse_section_package_data(self, section_options):
        """Parses `package_data` configuration file section.

        :param dict section_options:
        """
        self['package_data'] = self._parse_package_data(section_options)

    def parse_section_exclude_package_data(self, section_options):
        """Parses `exclude_package_data` configuration file section.

        :param dict section_options:
        """
        self['exclude_package_data'] = self._parse_package_data(section_options)

    def parse_section_extras_require(self, section_options):
        """Parses `extras_require` configuration file section.

        :param dict section_options:
        """
        parse_list = partial((self._parse_list), separator=';')
        self['extras_require'] = self._parse_section_to_dict(section_options, parse_list)

    def parse_section_data_files(self, section_options):
        """Parses `data_files` configuration file section.

        :param dict section_options:
        """
        parsed = self._parse_section_to_dict(section_options, self._parse_list)
        self['data_files'] = [(k, v) for k, v in parsed.items()]