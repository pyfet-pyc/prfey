# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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

    def __init__--- This code section failed: ---

 L.  29         0  LOAD_GLOBAL              importlib
                2  LOAD_ATTR                util
                4  LOAD_METHOD              find_spec
                6  LOAD_FAST                'name'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'spec'

 L.  30        12  LOAD_GLOBAL              open
               14  LOAD_FAST                'spec'
               16  LOAD_ATTR                origin
               18  CALL_FUNCTION_1       1  ''
               20  SETUP_WITH           46  'to 46'
               22  STORE_FAST               'strm'

 L.  31        24  LOAD_FAST                'strm'
               26  LOAD_METHOD              read
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'src'
               32  POP_BLOCK        
               34  LOAD_CONST               None
               36  DUP_TOP          
               38  DUP_TOP          
               40  CALL_FUNCTION_3       3  ''
               42  POP_TOP          
               44  JUMP_FORWARD         62  'to 62'
             46_0  COME_FROM_WITH       20  '20'
               46  <49>             
               48  POP_JUMP_IF_TRUE     52  'to 52'
               50  <48>             
             52_0  COME_FROM            48  '48'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          
               58  POP_EXCEPT       
               60  POP_TOP          
             62_0  COME_FROM            44  '44'

 L.  32        62  LOAD_GLOBAL              ast
               64  LOAD_METHOD              parse
               66  LOAD_FAST                'src'
               68  CALL_METHOD_1         1  ''
               70  STORE_FAST               'module'

 L.  33        72  LOAD_GLOBAL              vars
               74  LOAD_FAST                'self'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_METHOD              update
               80  LOAD_GLOBAL              locals
               82  CALL_FUNCTION_0       0  ''
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L.  34        88  LOAD_FAST                'self'
               90  DELETE_ATTR              self

Parse error at or near `DUP_TOP' instruction at offset 36

    def __getattr__--- This code section failed: ---

 L.  37         0  SETUP_FINALLY        30  'to 30'

 L.  38         2  LOAD_GLOBAL              next
                4  LOAD_CLOSURE             'attr'
                6  BUILD_TUPLE_1         1 
                8  LOAD_GENEXPR             '<code_object <genexpr>>'
               10  LOAD_STR                 'StaticModule.__getattr__.<locals>.<genexpr>'
               12  MAKE_FUNCTION_8          'closure'

 L.  40        14  LOAD_FAST                'self'
               16  LOAD_ATTR                module
               18  LOAD_ATTR                body

 L.  38        20  GET_ITER         
               22  CALL_FUNCTION_1       1  ''
               24  CALL_FUNCTION_1       1  ''
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY     0  '0'

 L.  45        30  DUP_TOP          
               32  LOAD_GLOBAL              Exception
               34  <121>                88  ''
               36  POP_TOP          
               38  STORE_FAST               'e'
               40  POP_TOP          
               42  SETUP_FINALLY        80  'to 80'

 L.  46        44  LOAD_GLOBAL              AttributeError

 L.  47        46  LOAD_STR                 '{self.name} has no attribute {attr}'
               48  LOAD_ATTR                format
               50  BUILD_TUPLE_0         0 
               52  BUILD_MAP_0           0 
               54  LOAD_GLOBAL              locals
               56  CALL_FUNCTION_0       0  ''
               58  <164>                 1  ''
               60  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L.  46        62  CALL_FUNCTION_1       1  ''

 L.  48        64  LOAD_FAST                'e'

 L.  46        66  RAISE_VARARGS_2       2  'exception instance with __cause__'
               68  POP_BLOCK        
               70  POP_EXCEPT       
               72  LOAD_CONST               None
               74  STORE_FAST               'e'
               76  DELETE_FAST              'e'
               78  JUMP_FORWARD         90  'to 90'
             80_0  COME_FROM_FINALLY    42  '42'
               80  LOAD_CONST               None
               82  STORE_FAST               'e'
               84  DELETE_FAST              'e'
               86  <48>             
               88  <48>             
             90_0  COME_FROM            78  '78'

Parse error at or near `<121>' instruction at offset 34


@contextlib.contextmanager
def patch_path--- This code section failed: ---

 L.  56         0  SETUP_FINALLY        38  'to 38'

 L.  57         2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                path
                6  LOAD_METHOD              insert
                8  LOAD_CONST               0
               10  LOAD_FAST                'path'
               12  CALL_METHOD_2         2  ''
               14  POP_TOP          

 L.  58        16  LOAD_CONST               None
               18  YIELD_VALUE      
               20  POP_TOP          
               22  POP_BLOCK        

 L.  60        24  LOAD_GLOBAL              sys
               26  LOAD_ATTR                path
               28  LOAD_METHOD              remove
               30  LOAD_FAST                'path'
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          
               36  JUMP_FORWARD         52  'to 52'
             38_0  COME_FROM_FINALLY     0  '0'
               38  LOAD_GLOBAL              sys
               40  LOAD_ATTR                path
               42  LOAD_METHOD              remove
               44  LOAD_FAST                'path'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
               50  <48>             
             52_0  COME_FROM            36  '36'

Parse error at or near `LOAD_GLOBAL' instruction at offset 24


def read_configuration--- This code section failed: ---

 L.  80         0  LOAD_CONST               0
                2  LOAD_CONST               ('Distribution', '_Distribution')
                4  IMPORT_NAME_ATTR         setuptools.dist
                6  IMPORT_FROM              Distribution
                8  STORE_FAST               'Distribution'
               10  IMPORT_FROM              _Distribution
               12  STORE_FAST               '_Distribution'
               14  POP_TOP          

 L.  82        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              abspath
               22  LOAD_FAST                'filepath'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'filepath'

 L.  84        28  LOAD_GLOBAL              os
               30  LOAD_ATTR                path
               32  LOAD_METHOD              isfile
               34  LOAD_FAST                'filepath'
               36  CALL_METHOD_1         1  ''
               38  POP_JUMP_IF_TRUE     52  'to 52'

 L.  85        40  LOAD_GLOBAL              DistutilsFileError

 L.  86        42  LOAD_STR                 'Configuration file %s does not exist.'
               44  LOAD_FAST                'filepath'
               46  BINARY_MODULO    

 L.  85        48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            38  '38'

 L.  88        52  LOAD_GLOBAL              os
               54  LOAD_METHOD              getcwd
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               'current_directory'

 L.  89        60  LOAD_GLOBAL              os
               62  LOAD_METHOD              chdir
               64  LOAD_GLOBAL              os
               66  LOAD_ATTR                path
               68  LOAD_METHOD              dirname
               70  LOAD_FAST                'filepath'
               72  CALL_METHOD_1         1  ''
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L.  91        78  SETUP_FINALLY       164  'to 164'

 L.  92        80  LOAD_FAST                'Distribution'
               82  CALL_FUNCTION_0       0  ''
               84  STORE_FAST               'dist'

 L.  94        86  LOAD_FAST                'find_others'
               88  POP_JUMP_IF_FALSE    98  'to 98'
               90  LOAD_FAST                'dist'
               92  LOAD_METHOD              find_config_files
               94  CALL_METHOD_0         0  ''
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            88  '88'
               98  BUILD_LIST_0          0 
            100_0  COME_FROM            96  '96'
              100  STORE_FAST               'filenames'

 L.  95       102  LOAD_FAST                'filepath'
              104  LOAD_FAST                'filenames'
              106  <118>                 1  ''
              108  POP_JUMP_IF_FALSE   120  'to 120'

 L.  96       110  LOAD_FAST                'filenames'
              112  LOAD_METHOD              append
              114  LOAD_FAST                'filepath'
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          
            120_0  COME_FROM           108  '108'

 L.  98       120  LOAD_FAST                '_Distribution'
              122  LOAD_ATTR                parse_config_files
              124  LOAD_FAST                'dist'
              126  LOAD_FAST                'filenames'
              128  LOAD_CONST               ('filenames',)
              130  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              132  POP_TOP          

 L. 100       134  LOAD_GLOBAL              parse_configuration

 L. 101       136  LOAD_FAST                'dist'
              138  LOAD_FAST                'dist'
              140  LOAD_ATTR                command_options

 L. 102       142  LOAD_FAST                'ignore_option_errors'

 L. 100       144  LOAD_CONST               ('ignore_option_errors',)
              146  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              148  STORE_FAST               'handlers'
              150  POP_BLOCK        

 L. 105       152  LOAD_GLOBAL              os
              154  LOAD_METHOD              chdir
              156  LOAD_FAST                'current_directory'
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          
              162  JUMP_FORWARD        176  'to 176'
            164_0  COME_FROM_FINALLY    78  '78'
              164  LOAD_GLOBAL              os
              166  LOAD_METHOD              chdir
              168  LOAD_FAST                'current_directory'
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          
              174  <48>             
            176_0  COME_FROM           162  '162'

 L. 107       176  LOAD_GLOBAL              configuration_to_dict
              178  LOAD_FAST                'handlers'
              180  CALL_FUNCTION_1       1  ''
              182  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 106


def _get_option--- This code section failed: ---

 L. 116         0  LOAD_STR                 'get_{key}'
                2  LOAD_ATTR                format
                4  BUILD_TUPLE_0         0 
                6  BUILD_MAP_0           0 
                8  LOAD_GLOBAL              locals
               10  CALL_FUNCTION_0       0  ''
               12  <164>                 1  ''
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  STORE_FAST               'getter_name'

 L. 117        18  LOAD_GLOBAL              functools
               20  LOAD_METHOD              partial
               22  LOAD_GLOBAL              getattr
               24  LOAD_FAST                'target_obj'
               26  LOAD_FAST                'key'
               28  CALL_METHOD_3         3  ''
               30  STORE_FAST               'by_attribute'

 L. 118        32  LOAD_GLOBAL              getattr
               34  LOAD_FAST                'target_obj'
               36  LOAD_FAST                'getter_name'
               38  LOAD_FAST                'by_attribute'
               40  CALL_FUNCTION_3       3  ''
               42  STORE_FAST               'getter'

 L. 119        44  LOAD_FAST                'getter'
               46  CALL_FUNCTION_0       0  ''
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


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
    options.parse
    meta = ConfigMetadataHandler(distribution.metadata, command_options, ignore_option_errors, distribution.package_dir)
    meta.parse
    return (
     meta, options)


class ConfigHandler:
    __doc__ = 'Handles metadata supplied in configuration files.'
    section_prefix = None
    aliases = {}

    def __init__(self, target_obj, options, ignore_option_errors=False):
        sections = {}
        section_prefix = self.section_prefix
        for section_name, section_options in options.items:
            if not section_name.startswithsection_prefix:
                pass
            else:
                section_name = section_name.replacesection_prefix''.strip'.'
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

    def __setitem__--- This code section failed: ---

 L. 206         0  LOAD_GLOBAL              tuple
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'unknown'

 L. 207         6  LOAD_FAST                'self'
                8  LOAD_ATTR                target_obj
               10  STORE_FAST               'target_obj'

 L. 210        12  LOAD_FAST                'self'
               14  LOAD_ATTR                aliases
               16  LOAD_METHOD              get
               18  LOAD_FAST                'option_name'
               20  LOAD_FAST                'option_name'
               22  CALL_METHOD_2         2  ''
               24  STORE_FAST               'option_name'

 L. 212        26  LOAD_GLOBAL              getattr
               28  LOAD_FAST                'target_obj'
               30  LOAD_FAST                'option_name'
               32  LOAD_FAST                'unknown'
               34  CALL_FUNCTION_3       3  ''
               36  STORE_FAST               'current_value'

 L. 214        38  LOAD_FAST                'current_value'
               40  LOAD_FAST                'unknown'
               42  <117>                 0  ''
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 215        46  LOAD_GLOBAL              KeyError
               48  LOAD_FAST                'option_name'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'

 L. 217        54  LOAD_FAST                'current_value'
               56  POP_JUMP_IF_FALSE    62  'to 62'

 L. 219        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            56  '56'

 L. 221        62  LOAD_CONST               False
               64  STORE_FAST               'skip_option'

 L. 222        66  LOAD_FAST                'self'
               68  LOAD_ATTR                parsers
               70  LOAD_METHOD              get
               72  LOAD_FAST                'option_name'
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'parser'

 L. 223        78  LOAD_FAST                'parser'
               80  POP_JUMP_IF_FALSE   126  'to 126'

 L. 224        82  SETUP_FINALLY        96  'to 96'

 L. 225        84  LOAD_FAST                'parser'
               86  LOAD_FAST                'value'
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'value'
               92  POP_BLOCK        
               94  JUMP_FORWARD        126  'to 126'
             96_0  COME_FROM_FINALLY    82  '82'

 L. 227        96  DUP_TOP          
               98  LOAD_GLOBAL              Exception
              100  <121>               124  ''
              102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          

 L. 228       108  LOAD_CONST               True
              110  STORE_FAST               'skip_option'

 L. 229       112  LOAD_FAST                'self'
              114  LOAD_ATTR                ignore_option_errors
              116  POP_JUMP_IF_TRUE    120  'to 120'

 L. 230       118  RAISE_VARARGS_0       0  'reraise'
            120_0  COME_FROM           116  '116'
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
              124  <48>             
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM            94  '94'
            126_2  COME_FROM            80  '80'

 L. 232       126  LOAD_FAST                'skip_option'
              128  POP_JUMP_IF_FALSE   134  'to 134'

 L. 233       130  LOAD_CONST               None
              132  RETURN_VALUE     
            134_0  COME_FROM           128  '128'

 L. 235       134  LOAD_GLOBAL              getattr
              136  LOAD_FAST                'target_obj'
              138  LOAD_STR                 'set_%s'
              140  LOAD_FAST                'option_name'
              142  BINARY_MODULO    
              144  LOAD_CONST               None
              146  CALL_FUNCTION_3       3  ''
              148  STORE_FAST               'setter'

 L. 236       150  LOAD_FAST                'setter'
              152  LOAD_CONST               None
              154  <117>                 0  ''
              156  POP_JUMP_IF_FALSE   172  'to 172'

 L. 237       158  LOAD_GLOBAL              setattr
              160  LOAD_FAST                'target_obj'
              162  LOAD_FAST                'option_name'
              164  LOAD_FAST                'value'
              166  CALL_FUNCTION_3       3  ''
              168  POP_TOP          
              170  JUMP_FORWARD        180  'to 180'
            172_0  COME_FROM           156  '156'

 L. 239       172  LOAD_FAST                'setter'
              174  LOAD_FAST                'value'
              176  CALL_FUNCTION_1       1  ''
              178  POP_TOP          
            180_0  COME_FROM           170  '170'

 L. 241       180  LOAD_FAST                'self'
              182  LOAD_ATTR                set_options
              184  LOAD_METHOD              append
              186  LOAD_FAST                'option_name'
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          

Parse error at or near `<117>' instruction at offset 42

    @classmethod
    def _parse_list--- This code section failed: ---

 L. 253         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              list
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 254        10  LOAD_FAST                'value'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 256        14  LOAD_STR                 '\n'
               16  LOAD_FAST                'value'
               18  <118>                 0  ''
               20  POP_JUMP_IF_FALSE    32  'to 32'

 L. 257        22  LOAD_FAST                'value'
               24  LOAD_METHOD              splitlines
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'value'
               30  JUMP_FORWARD         42  'to 42'
             32_0  COME_FROM            20  '20'

 L. 259        32  LOAD_FAST                'value'
               34  LOAD_METHOD              split
               36  LOAD_FAST                'separator'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'value'
             42_0  COME_FROM            30  '30'

 L. 261        42  LOAD_LISTCOMP            '<code_object <listcomp>>'
               44  LOAD_STR                 'ConfigHandler._parse_list.<locals>.<listcomp>'
               46  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               48  LOAD_FAST                'value'
               50  GET_ITER         
               52  CALL_FUNCTION_1       1  ''
               54  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 18

    @classmethod
    def _parse_dict(cls, value):
        """Represents value as a dict.

        :param value:
        :rtype: dict
        """
        separator = '='
        result = {}
        for line in cls._parse_listvalue:
            key, sep, val = line.partitionseparator
            if sep != separator:
                raise DistutilsOptionError('Unable to parse option value to dict: %s' % value)
            result[key.strip] = val.strip
        else:
            return result

    @classmethod
    def _parse_bool--- This code section failed: ---

 L. 288         0  LOAD_FAST                'value'
                2  LOAD_METHOD              lower
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'value'

 L. 289         8  LOAD_FAST                'value'
               10  LOAD_CONST               ('1', 'true', 'yes')
               12  <118>                 0  ''
               14  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 12

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
            if value.startswithexclude_directive:
                raise ValueError('Only strings are accepted for the {0} field, files are not accepted'.formatkey)
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
            return value.startswithinclude_directive or value
        spec = value[len(include_directive):]
        filepaths = (os.path.abspathpath.strip for path in spec.split',')
        return '\n'.join(cls._read_filepath for path in filepaths if cls._assert_localpath or os.path.isfilepath)

    @staticmethod
    def _assert_local(filepath):
        if not filepath.startswithos.getcwd:
            raise DistutilsOptionError('`file:` directive can not access %s' % filepath)

    @staticmethod
    def _read_file--- This code section failed: ---

 L. 350         0  LOAD_GLOBAL              io
                2  LOAD_ATTR                open
                4  LOAD_FAST                'filepath'
                6  LOAD_STR                 'utf-8'
                8  LOAD_CONST               ('encoding',)
               10  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               12  SETUP_WITH           38  'to 38'
               14  STORE_FAST               'f'

 L. 351        16  LOAD_FAST                'f'
               18  LOAD_METHOD              read
               20  CALL_METHOD_0         0  ''
               22  POP_BLOCK        
               24  ROT_TWO          
               26  LOAD_CONST               None
               28  DUP_TOP          
               30  DUP_TOP          
               32  CALL_FUNCTION_3       3  ''
               34  POP_TOP          
               36  RETURN_VALUE     
             38_0  COME_FROM_WITH       12  '12'
               38  <49>             
               40  POP_JUMP_IF_TRUE     44  'to 44'
               42  <48>             
             44_0  COME_FROM            40  '40'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          
               50  POP_EXCEPT       
               52  POP_TOP          

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
               86  <118>                 0  ''
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
              168  <118>                 0  ''
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
              200  SETUP_WITH          280  'to 280'
              202  POP_TOP          

 L. 390       204  SETUP_FINALLY       236  'to 236'

 L. 392       206  LOAD_GLOBAL              getattr
              208  LOAD_GLOBAL              StaticModule
              210  LOAD_FAST                'module_name'
              212  CALL_FUNCTION_1       1  ''
              214  LOAD_FAST                'attr_name'
              216  CALL_FUNCTION_2       2  ''
              218  POP_BLOCK        
              220  POP_BLOCK        
              222  ROT_TWO          
              224  LOAD_CONST               None
              226  DUP_TOP          
              228  DUP_TOP          
              230  CALL_FUNCTION_3       3  ''
              232  POP_TOP          
              234  RETURN_VALUE     
            236_0  COME_FROM_FINALLY   204  '204'

 L. 393       236  DUP_TOP          
              238  LOAD_GLOBAL              Exception
          240_242  <121>               264  ''
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
              264  <48>             
            266_0  COME_FROM           262  '262'
              266  POP_BLOCK        
              268  LOAD_CONST               None
              270  DUP_TOP          
              272  DUP_TOP          
              274  CALL_FUNCTION_3       3  ''
              276  POP_TOP          
              278  JUMP_FORWARD        298  'to 298'
            280_0  COME_FROM_WITH      200  '200'
              280  <49>             
          282_284  POP_JUMP_IF_TRUE    288  'to 288'
              286  <48>             
            288_0  COME_FROM           282  '282'
              288  POP_TOP          
              290  POP_TOP          
              292  POP_TOP          
              294  POP_EXCEPT       
              296  POP_TOP          
            298_0  COME_FROM           278  '278'

 L. 397       298  LOAD_GLOBAL              getattr
              300  LOAD_FAST                'module'
              302  LOAD_FAST                'attr_name'
              304  CALL_FUNCTION_2       2  ''
              306  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 86

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
        for key, (_, val) in section_options.items:
            value[key] = values_parser(val)
        else:
            return value

    def parse_section--- This code section failed: ---

 L. 439         0  LOAD_FAST                'section_options'
                2  LOAD_METHOD              items
                4  CALL_METHOD_0         0  ''
                6  GET_ITER         
                8  FOR_ITER             54  'to 54'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'name'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               '_'
               18  STORE_FAST               'value'

 L. 440        20  SETUP_FINALLY        34  'to 34'

 L. 441        22  LOAD_FAST                'value'
               24  LOAD_FAST                'self'
               26  LOAD_FAST                'name'
               28  STORE_SUBSCR     
               30  POP_BLOCK        
               32  JUMP_BACK             8  'to 8'
             34_0  COME_FROM_FINALLY    20  '20'

 L. 443        34  DUP_TOP          
               36  LOAD_GLOBAL              KeyError
               38  <121>                50  ''
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 444        46  POP_EXCEPT       
               48  JUMP_BACK             8  'to 8'
               50  <48>             
               52  JUMP_BACK             8  'to 8'

Parse error at or near `<121>' instruction at offset 38

    def parse--- This code section failed: ---

 L. 451         0  LOAD_FAST                'self'
                2  LOAD_ATTR                sections
                4  LOAD_METHOD              items
                6  CALL_METHOD_0         0  ''
                8  GET_ITER         
               10  FOR_ITER             94  'to 94'
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'section_name'
               16  STORE_FAST               'section_options'

 L. 453        18  LOAD_STR                 ''
               20  STORE_FAST               'method_postfix'

 L. 454        22  LOAD_FAST                'section_name'
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L. 455        26  LOAD_STR                 '_%s'
               28  LOAD_FAST                'section_name'
               30  BINARY_MODULO    
               32  STORE_FAST               'method_postfix'
             34_0  COME_FROM            24  '24'

 L. 457        34  LOAD_GLOBAL              getattr

 L. 458        36  LOAD_FAST                'self'

 L. 460        38  LOAD_STR                 'parse_section%s'
               40  LOAD_FAST                'method_postfix'
               42  BINARY_MODULO    
               44  LOAD_METHOD              replace
               46  LOAD_STR                 '.'
               48  LOAD_STR                 '__'
               50  CALL_METHOD_2         2  ''

 L. 461        52  LOAD_CONST               None

 L. 457        54  CALL_FUNCTION_3       3  ''
               56  STORE_FAST               'section_parser_method'

 L. 463        58  LOAD_FAST                'section_parser_method'
               60  LOAD_CONST               None
               62  <117>                 0  ''
               64  POP_JUMP_IF_FALSE    84  'to 84'

 L. 464        66  LOAD_GLOBAL              DistutilsOptionError

 L. 465        68  LOAD_STR                 'Unsupported distribution option section: [%s.%s]'

 L. 466        70  LOAD_FAST                'self'
               72  LOAD_ATTR                section_prefix
               74  LOAD_FAST                'section_name'

 L. 465        76  BUILD_TUPLE_2         2 
               78  BINARY_MODULO    

 L. 464        80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            64  '64'

 L. 468        84  LOAD_FAST                'section_parser_method'
               86  LOAD_FAST                'section_options'
               88  CALL_FUNCTION_1       1  ''
               90  POP_TOP          
               92  JUMP_BACK            10  'to 10'

Parse error at or near `<117>' instruction at offset 62

    def _deprecated_config_handler(self, func, msg, warning_class):
        """ this function will wrap around parameters that are deprecated

        :param msg: deprecation message
        :param warning_class: class of warning exception to be raised
        :param func: function to be wrapped around
        """

        @wraps(func)
        def config_handler--- This code section failed: ---

 L. 479         0  LOAD_GLOBAL              warnings
                2  LOAD_METHOD              warn
                4  LOAD_DEREF               'msg'
                6  LOAD_DEREF               'warning_class'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 480        12  LOAD_DEREF               'func'
               14  LOAD_FAST                'args'
               16  BUILD_MAP_0           0 
               18  LOAD_FAST                'kwargs'
               20  <164>                 1  ''
               22  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 20

        return config_handler


class ConfigMetadataHandler(ConfigHandler):
    section_prefix = 'metadata'
    aliases = {'home_page':'url', 
     'summary':'description', 
     'classifier':'classifiers', 
     'platform':'platforms'}
    strict_mode = False

    def __init__(self, target_obj, options, ignore_option_errors=False, package_dir=None):
        super(ConfigMetadataHandler, self).__init__target_objoptionsignore_option_errors
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
         'requires':self._deprecated_config_handlerparse_list'The requires parameter is deprecated, please use install_requires for runtime dependencies.'DeprecationWarning, 
         'obsoletes':parse_list, 
         'classifiers':self._get_parser_compoundparse_fileparse_list, 
         'license':exclude_files_parser('license'), 
         'license_files':parse_list, 
         'description':parse_file, 
         'long_description':parse_file, 
         'version':self._parse_version, 
         'project_urls':parse_dict}

    def _parse_version--- This code section failed: ---

 L. 542         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _parse_file
                4  LOAD_FAST                'value'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'version'

 L. 544        10  LOAD_FAST                'version'
               12  LOAD_FAST                'value'
               14  COMPARE_OP               !=
               16  POP_JUMP_IF_FALSE    70  'to 70'

 L. 545        18  LOAD_FAST                'version'
               20  LOAD_METHOD              strip
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'version'

 L. 548        26  LOAD_GLOBAL              isinstance
               28  LOAD_GLOBAL              parse
               30  LOAD_FAST                'version'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_GLOBAL              LegacyVersion
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_FALSE    66  'to 66'

 L. 550        40  LOAD_STR                 'Version loaded from {value} does not comply with PEP 440: {version}'

 L. 549        42  STORE_FAST               'tmpl'

 L. 553        44  LOAD_GLOBAL              DistutilsOptionError
               46  LOAD_FAST                'tmpl'
               48  LOAD_ATTR                format
               50  BUILD_TUPLE_0         0 
               52  BUILD_MAP_0           0 
               54  LOAD_GLOBAL              locals
               56  CALL_FUNCTION_0       0  ''
               58  <164>                 1  ''
               60  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            38  '38'

 L. 555        66  LOAD_FAST                'version'
               68  RETURN_VALUE     
             70_0  COME_FROM            16  '16'

 L. 557        70  LOAD_FAST                'self'
               72  LOAD_METHOD              _parse_attr
               74  LOAD_FAST                'value'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                package_dir
               80  CALL_METHOD_2         2  ''
               82  STORE_FAST               'version'

 L. 559        84  LOAD_GLOBAL              callable
               86  LOAD_FAST                'version'
               88  CALL_FUNCTION_1       1  ''
               90  POP_JUMP_IF_FALSE    98  'to 98'

 L. 560        92  LOAD_FAST                'version'
               94  CALL_FUNCTION_0       0  ''
               96  STORE_FAST               'version'
             98_0  COME_FROM            90  '90'

 L. 562        98  LOAD_GLOBAL              isinstance
              100  LOAD_FAST                'version'
              102  LOAD_GLOBAL              string_types
              104  CALL_FUNCTION_2       2  ''
              106  POP_JUMP_IF_TRUE    144  'to 144'

 L. 563       108  LOAD_GLOBAL              hasattr
              110  LOAD_FAST                'version'
              112  LOAD_STR                 '__iter__'
              114  CALL_FUNCTION_2       2  ''
              116  POP_JUMP_IF_FALSE   136  'to 136'

 L. 564       118  LOAD_STR                 '.'
              120  LOAD_METHOD              join
              122  LOAD_GLOBAL              map
              124  LOAD_GLOBAL              str
              126  LOAD_FAST                'version'
              128  CALL_FUNCTION_2       2  ''
              130  CALL_METHOD_1         1  ''
              132  STORE_FAST               'version'
              134  JUMP_FORWARD        144  'to 144'
            136_0  COME_FROM           116  '116'

 L. 566       136  LOAD_STR                 '%s'
              138  LOAD_FAST                'version'
              140  BINARY_MODULO    
              142  STORE_FAST               'version'
            144_0  COME_FROM           134  '134'
            144_1  COME_FROM           106  '106'

 L. 568       144  LOAD_FAST                'version'
              146  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 58


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

    def _parse_packages--- This code section failed: ---

 L. 610         0  LOAD_STR                 'find:'
                2  LOAD_STR                 'find_namespace:'
                4  BUILD_LIST_2          2 
                6  STORE_FAST               'find_directives'

 L. 611         8  LOAD_FAST                'value'
               10  LOAD_METHOD              strip
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'trimmed_value'

 L. 613        16  LOAD_FAST                'trimmed_value'
               18  LOAD_FAST                'find_directives'
               20  <118>                 1  ''
               22  POP_JUMP_IF_FALSE    34  'to 34'

 L. 614        24  LOAD_FAST                'self'
               26  LOAD_METHOD              _parse_list
               28  LOAD_FAST                'value'
               30  CALL_METHOD_1         1  ''
               32  RETURN_VALUE     
             34_0  COME_FROM            22  '22'

 L. 616        34  LOAD_FAST                'trimmed_value'
               36  LOAD_FAST                'find_directives'
               38  LOAD_CONST               1
               40  BINARY_SUBSCR    
               42  COMPARE_OP               ==
               44  STORE_FAST               'findns'

 L. 617        46  LOAD_FAST                'findns'
               48  POP_JUMP_IF_FALSE    62  'to 62'
               50  LOAD_GLOBAL              PY3
               52  POP_JUMP_IF_TRUE     62  'to 62'

 L. 618        54  LOAD_GLOBAL              DistutilsOptionError

 L. 619        56  LOAD_STR                 'find_namespace: directive is unsupported on Python < 3.3'

 L. 618        58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'
             62_1  COME_FROM            48  '48'

 L. 622        62  LOAD_FAST                'self'
               64  LOAD_METHOD              parse_section_packages__find

 L. 623        66  LOAD_FAST                'self'
               68  LOAD_ATTR                sections
               70  LOAD_METHOD              get
               72  LOAD_STR                 'packages.find'
               74  BUILD_MAP_0           0 
               76  CALL_METHOD_2         2  ''

 L. 622        78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'find_kwargs'

 L. 625        82  LOAD_FAST                'findns'
               84  POP_JUMP_IF_FALSE   100  'to 100'

 L. 626        86  LOAD_CONST               0
               88  LOAD_CONST               ('find_namespace_packages',)
               90  IMPORT_NAME              setuptools
               92  IMPORT_FROM              find_namespace_packages
               94  STORE_FAST               'find_packages'
               96  POP_TOP          
               98  JUMP_FORWARD        112  'to 112'
            100_0  COME_FROM            84  '84'

 L. 628       100  LOAD_CONST               0
              102  LOAD_CONST               ('find_packages',)
              104  IMPORT_NAME              setuptools
              106  IMPORT_FROM              find_packages
              108  STORE_FAST               'find_packages'
              110  POP_TOP          
            112_0  COME_FROM            98  '98'

 L. 630       112  LOAD_FAST                'find_packages'
              114  BUILD_TUPLE_0         0 
              116  BUILD_MAP_0           0 
              118  LOAD_FAST                'find_kwargs'
              120  <164>                 1  ''
              122  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 20

    def parse_section_packages__find--- This code section failed: ---

 L. 639         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _parse_section_to_dict

 L. 640         4  LOAD_FAST                'section_options'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _parse_list

 L. 639        10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'section_data'

 L. 642        14  BUILD_LIST_0          0 
               16  LOAD_CONST               ('where', 'include', 'exclude')
               18  CALL_FINALLY         21  'to 21'
               20  STORE_DEREF              'valid_keys'

 L. 644        22  LOAD_GLOBAL              dict

 L. 645        24  LOAD_CLOSURE             'valid_keys'
               26  BUILD_TUPLE_1         1 
               28  LOAD_LISTCOMP            '<code_object <listcomp>>'
               30  LOAD_STR                 'ConfigOptionsHandler.parse_section_packages__find.<locals>.<listcomp>'
               32  MAKE_FUNCTION_8          'closure'
               34  LOAD_FAST                'section_data'
               36  LOAD_METHOD              items
               38  CALL_METHOD_0         0  ''
               40  GET_ITER         
               42  CALL_FUNCTION_1       1  ''

 L. 644        44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'find_kwargs'

 L. 647        48  LOAD_FAST                'find_kwargs'
               50  LOAD_METHOD              get
               52  LOAD_STR                 'where'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'where'

 L. 648        58  LOAD_FAST                'where'
               60  LOAD_CONST               None
               62  <117>                 1  ''
               64  POP_JUMP_IF_FALSE    78  'to 78'

 L. 649        66  LOAD_FAST                'where'
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  LOAD_FAST                'find_kwargs'
               74  LOAD_STR                 'where'
               76  STORE_SUBSCR     
             78_0  COME_FROM            64  '64'

 L. 651        78  LOAD_FAST                'find_kwargs'
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 18

    def parse_section_entry_points(self, section_options):
        """Parses `entry_points` configuration file section.

        :param dict section_options:
        """
        parsed = self._parse_section_to_dictsection_optionsself._parse_list
        self['entry_points'] = parsed

    def _parse_package_data(self, section_options):
        parsed = self._parse_section_to_dictsection_optionsself._parse_list
        root = parsed.get'*'
        if root:
            parsed[''] = root
            del parsed['*']
        return parsed

    def parse_section_package_data(self, section_options):
        """Parses `package_data` configuration file section.

        :param dict section_options:
        """
        self['package_data'] = self._parse_package_datasection_options

    def parse_section_exclude_package_data(self, section_options):
        """Parses `exclude_package_data` configuration file section.

        :param dict section_options:
        """
        self['exclude_package_data'] = self._parse_package_datasection_options

    def parse_section_extras_require(self, section_options):
        """Parses `extras_require` configuration file section.

        :param dict section_options:
        """
        parse_list = partial((self._parse_list), separator=';')
        self['extras_require'] = self._parse_section_to_dictsection_optionsparse_list

    def parse_section_data_files(self, section_options):
        """Parses `data_files` configuration file section.

        :param dict section_options:
        """
        parsed = self._parse_section_to_dictsection_optionsself._parse_list
        self['data_files'] = [(k, v) for k, v in parsed.items]