# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: configparser.py
"""Configuration file parser.

A configuration file consists of sections, lead by a "[section]" header,
and followed by "name: value" entries, with continuations and such in
the style of RFC 822.

Intrinsic defaults can be specified by passing them into the
ConfigParser constructor as a dictionary.

class:

ConfigParser -- responsible for parsing a list of
                    configuration files, and managing the parsed database.

    methods:

    __init__(defaults=None, dict_type=_default_dict, allow_no_value=False,
             delimiters=('=', ':'), comment_prefixes=('#', ';'),
             inline_comment_prefixes=None, strict=True,
             empty_lines_in_values=True, default_section='DEFAULT',
             interpolation=<unset>, converters=<unset>):
        Create the parser. When `defaults' is given, it is initialized into the
        dictionary or intrinsic defaults. The keys must be strings, the values
        must be appropriate for %()s string interpolation.

        When `dict_type' is given, it will be used to create the dictionary
        objects for the list of sections, for the options within a section, and
        for the default values.

        When `delimiters' is given, it will be used as the set of substrings
        that divide keys from values.

        When `comment_prefixes' is given, it will be used as the set of
        substrings that prefix comments in empty lines. Comments can be
        indented.

        When `inline_comment_prefixes' is given, it will be used as the set of
        substrings that prefix comments in non-empty lines.

        When `strict` is True, the parser won't allow for any section or option
        duplicates while reading from a single source (file, string or
        dictionary). Default is True.

        When `empty_lines_in_values' is False (default: True), each empty line
        marks the end of an option. Otherwise, internal empty lines of
        a multiline option are kept as part of the value.

        When `allow_no_value' is True (default: False), options without
        values are accepted; the value presented for these is None.

        When `default_section' is given, the name of the special section is
        named accordingly. By default it is called ``"DEFAULT"`` but this can
        be customized to point to any other valid section name. Its current
        value can be retrieved using the ``parser_instance.default_section``
        attribute and may be modified at runtime.

        When `interpolation` is given, it should be an Interpolation subclass
        instance. It will be used as the handler for option value
        pre-processing when using getters. RawConfigParser objects don't do
        any sort of interpolation, whereas ConfigParser uses an instance of
        BasicInterpolation. The library also provides a ``zc.buildbot``
        inspired ExtendedInterpolation implementation.

        When `converters` is given, it should be a dictionary where each key
        represents the name of a type converter and each value is a callable
        implementing the conversion from string to the desired datatype. Every
        converter gets its corresponding get*() method on the parser object and
        section proxies.

    sections()
        Return all the configuration section names, sans DEFAULT.

    has_section(section)
        Return whether the given section exists.

    has_option(section, option)
        Return whether the given option exists in the given section.

    options(section)
        Return list of configuration options for the named section.

    read(filenames, encoding=None)
        Read and parse the iterable of named configuration files, given by
        name.  A single filename is also allowed.  Non-existing files
        are ignored.  Return list of successfully read files.

    read_file(f, filename=None)
        Read and parse one configuration file, given as a file object.
        The filename defaults to f.name; it is only used in error
        messages (if f has no `name' attribute, the string `<???>' is used).

    read_string(string)
        Read configuration from a given string.

    read_dict(dictionary)
        Read configuration from a dictionary. Keys are section names,
        values are dictionaries with keys and values that should be present
        in the section. If the used dictionary type preserves order, sections
        and their keys will be added in order. Values are automatically
        converted to strings.

    get(section, option, raw=False, vars=None, fallback=_UNSET)
        Return a string value for the named option.  All % interpolations are
        expanded in the return values, based on the defaults passed into the
        constructor and the DEFAULT section.  Additional substitutions may be
        provided using the `vars' argument, which must be a dictionary whose
        contents override any pre-existing defaults. If `option' is a key in
        `vars', the value from `vars' is used.

    getint(section, options, raw=False, vars=None, fallback=_UNSET)
        Like get(), but convert value to an integer.

    getfloat(section, options, raw=False, vars=None, fallback=_UNSET)
        Like get(), but convert value to a float.

    getboolean(section, options, raw=False, vars=None, fallback=_UNSET)
        Like get(), but convert value to a boolean (currently case
        insensitively defined as 0, false, no, off for False, and 1, true,
        yes, on for True).  Returns False or True.

    items(section=_UNSET, raw=False, vars=None)
        If section is given, return a list of tuples with (name, value) for
        each option in the section. Otherwise, return a list of tuples with
        (section_name, section_proxy) for each section, including DEFAULTSECT.

    remove_section(section)
        Remove the given file section and all its options.

    remove_option(section, option)
        Remove the given option from the given section.

    set(section, option, value)
        Set the given option.

    write(fp, space_around_delimiters=True)
        Write the configuration state in .ini format. If
        `space_around_delimiters' is True (the default), delimiters
        between keys and values are surrounded by spaces.
"""
from collections.abc import MutableMapping
from collections import ChainMap as _ChainMap
import functools, io, itertools, os, re, sys, warnings
__all__ = [
 'NoSectionError', 'DuplicateOptionError', 'DuplicateSectionError',
 'NoOptionError', 'InterpolationError', 'InterpolationDepthError',
 'InterpolationMissingOptionError', 'InterpolationSyntaxError',
 'ParsingError', 'MissingSectionHeaderError',
 'ConfigParser', 'SafeConfigParser', 'RawConfigParser',
 'Interpolation', 'BasicInterpolation', 'ExtendedInterpolation',
 'LegacyInterpolation', 'SectionProxy', 'ConverterMapping',
 'DEFAULTSECT', 'MAX_INTERPOLATION_DEPTH']
_default_dict = dict
DEFAULTSECT = 'DEFAULT'
MAX_INTERPOLATION_DEPTH = 10

class Error(Exception):
    __doc__ = 'Base class for ConfigParser exceptions.'

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__


class NoSectionError(Error):
    __doc__ = 'Raised when no section matches a requested option.'

    def __init__(self, section):
        Error.__init__(self, 'No section: %r' % (section,))
        self.section = section
        self.args = (section,)


class DuplicateSectionError(Error):
    __doc__ = 'Raised when a section is repeated in an input source.\n\n    Possible repetitions that raise this exception are: multiple creation\n    using the API or in strict parsers when a section is found more than once\n    in a single input file, string or dictionary.\n    '

    def __init__(self, section, source=None, lineno=None):
        msg = [
         repr(section), ' already exists']
        if source is not None:
            message = [
             'While reading from ', repr(source)]
            if lineno is not None:
                message.append(' [line {0:2d}]'.format(lineno))
            message.append(': section ')
            message.extend(msg)
            msg = message
        else:
            msg.insert(0, 'Section ')
        Error.__init__(self, ''.join(msg))
        self.section = section
        self.source = source
        self.lineno = lineno
        self.args = (section, source, lineno)


class DuplicateOptionError(Error):
    __doc__ = 'Raised by strict parsers when an option is repeated in an input source.\n\n    Current implementation raises this exception only when an option is found\n    more than once in a single file, string or dictionary.\n    '

    def __init__(self, section, option, source=None, lineno=None):
        msg = [
         repr(option), ' in section ', repr(section),
         ' already exists']
        if source is not None:
            message = [
             'While reading from ', repr(source)]
            if lineno is not None:
                message.append(' [line {0:2d}]'.format(lineno))
            message.append(': option ')
            message.extend(msg)
            msg = message
        else:
            msg.insert(0, 'Option ')
        Error.__init__(self, ''.join(msg))
        self.section = section
        self.option = option
        self.source = source
        self.lineno = lineno
        self.args = (section, option, source, lineno)


class NoOptionError(Error):
    __doc__ = 'A requested option was not found.'

    def __init__(self, option, section):
        Error.__init__(self, 'No option %r in section: %r' % (
         option, section))
        self.option = option
        self.section = section
        self.args = (option, section)


class InterpolationError(Error):
    __doc__ = 'Base class for interpolation-related exceptions.'

    def __init__(self, option, section, msg):
        Error.__init__(self, msg)
        self.option = option
        self.section = section
        self.args = (option, section, msg)


class InterpolationMissingOptionError(InterpolationError):
    __doc__ = 'A string substitution required a setting which was not available.'

    def __init__(self, option, section, rawval, reference):
        msg = 'Bad value substitution: option {!r} in section {!r} contains an interpolation key {!r} which is not a valid option name. Raw value: {!r}'.format(option, section, reference, rawval)
        InterpolationError.__init__(self, option, section, msg)
        self.reference = reference
        self.args = (option, section, rawval, reference)


class InterpolationSyntaxError(InterpolationError):
    __doc__ = 'Raised when the source text contains invalid syntax.\n\n    Current implementation raises this exception when the source text into\n    which substitutions are made does not conform to the required syntax.\n    '


class InterpolationDepthError(InterpolationError):
    __doc__ = 'Raised when substitutions are nested too deeply.'

    def __init__(self, option, section, rawval):
        msg = 'Recursion limit exceeded in value substitution: option {!r} in section {!r} contains an interpolation key which cannot be substituted in {} steps. Raw value: {!r}'.format(option, section, MAX_INTERPOLATION_DEPTH, rawval)
        InterpolationError.__init__(self, option, section, msg)
        self.args = (option, section, rawval)


class ParsingError(Error):
    __doc__ = 'Raised when a configuration file does not follow legal syntax.'

    def __init__(self, source=None, filename=None):
        if filename and source:
            raise ValueError("Cannot specify both `filename' and `source'. Use `source'.")
        elif not (filename or source):
            raise ValueError("Required argument `source' not given.")
        elif filename:
            source = filename
        Error.__init__(self, 'Source contains parsing errors: %r' % source)
        self.source = source
        self.errors = []
        self.args = (source,)

    @property
    def filename(self):
        """Deprecated, use `source'."""
        warnings.warn("The 'filename' attribute will be removed in future versions.  Use 'source' instead.",
          DeprecationWarning,
          stacklevel=2)
        return self.source

    @filename.setter
    def filename(self, value):
        """Deprecated, user `source'."""
        warnings.warn("The 'filename' attribute will be removed in future versions.  Use 'source' instead.",
          DeprecationWarning,
          stacklevel=2)
        self.source = value

    def append(self, lineno, line):
        self.errors.append((lineno, line))
        self.message += '\n\t[line %2d]: %s' % (lineno, line)


class MissingSectionHeaderError(ParsingError):
    __doc__ = 'Raised when a key-value pair is found before any section header.'

    def __init__(self, filename, lineno, line):
        Error.__init__(self, 'File contains no section headers.\nfile: %r, line: %d\n%r' % (
         filename, lineno, line))
        self.source = filename
        self.lineno = lineno
        self.line = line
        self.args = (filename, lineno, line)


_UNSET = object()

class Interpolation:
    __doc__ = 'Dummy interpolation that passes the value through with no changes.'

    def before_get(self, parser, section, option, value, defaults):
        return value

    def before_set(self, parser, section, option, value):
        return value

    def before_read(self, parser, section, option, value):
        return value

    def before_write(self, parser, section, option, value):
        return value


class BasicInterpolation(Interpolation):
    __doc__ = 'Interpolation as implemented in the classic ConfigParser.\n\n    The option values can contain format strings which refer to other values in\n    the same section, or values in the special default section.\n\n    For example:\n\n        something: %(dir)s/whatever\n\n    would resolve the "%(dir)s" to the value of dir.  All reference\n    expansions are done late, on demand. If a user needs to use a bare % in\n    a configuration file, she can escape it by writing %%. Other % usage\n    is considered a user error and raises `InterpolationSyntaxError\'.'
    _KEYCRE = re.compile('%\\(([^)]+)\\)s')

    def before_get(self, parser, section, option, value, defaults):
        L = []
        self._interpolate_some(parser, option, L, value, section, defaults, 1)
        return ''.join(L)

    def before_set(self, parser, section, option, value):
        tmp_value = value.replace('%%', '')
        tmp_value = self._KEYCRE.sub('', tmp_value)
        if '%' in tmp_value:
            raise ValueError('invalid interpolation syntax in %r at position %d' % (
             value, tmp_value.find('%')))
        return value

    def _interpolate_some(self, parser, option, accum, rest, section, map, depth):
        rawval = parser.get(section, option, raw=True, fallback=rest)
        if depth > MAX_INTERPOLATION_DEPTH:
            raise InterpolationDepthError(option, section, rawval)
            while True:
                if rest:
                    p = rest.find('%')
                    if p < 0:
                        accum.append(rest)
                        return
                    if p > 0:
                        accum.append(rest[:p])
                        rest = rest[p:]
                    c = rest[1:2]
                    if c == '%':
                        accum.append('%')
                        rest = rest[2:]
                    else:
                        if c == '(':
                            m = self._KEYCRE.match(rest)
                            if m is None:
                                raise InterpolationSyntaxError(option, section, 'bad interpolation variable reference %r' % rest)
                            var = parser.optionxform(m.group(1))
                            rest = rest[m.end():]
                            try:
                                v = map[var]
                            except KeyError:
                                raise InterpolationMissingOptionError(option, section, rawval, var) from None

                            if '%' in v:
                                self._interpolate_some(parser, option, accum, v, section, map, depth + 1)
                            else:
                                accum.append(v)
                        else:
                            raise InterpolationSyntaxError(option, section, "'%%' must be followed by '%%' or '(', found: %r" % (
                             rest,))


class ExtendedInterpolation(Interpolation):
    __doc__ = "Advanced variant of interpolation, supports the syntax used by\n    `zc.buildout'. Enables interpolation between sections."
    _KEYCRE = re.compile('\\$\\{([^}]+)\\}')

    def before_get(self, parser, section, option, value, defaults):
        L = []
        self._interpolate_some(parser, option, L, value, section, defaults, 1)
        return ''.join(L)

    def before_set(self, parser, section, option, value):
        tmp_value = value.replace('$$', '')
        tmp_value = self._KEYCRE.sub('', tmp_value)
        if '$' in tmp_value:
            raise ValueError('invalid interpolation syntax in %r at position %d' % (
             value, tmp_value.find('$')))
        return value

    def _interpolate_some(self, parser, option, accum, rest, section, map, depth):
        rawval = parser.get(section, option, raw=True, fallback=rest)
        if depth > MAX_INTERPOLATION_DEPTH:
            raise InterpolationDepthError(option, section, rawval)
            while True:
                if rest:
                    p = rest.find('$')
                    if p < 0:
                        accum.append(rest)
                        return
                    if p > 0:
                        accum.append(rest[:p])
                        rest = rest[p:]
                    c = rest[1:2]
                    if c == '$':
                        accum.append('$')
                        rest = rest[2:]
                    else:
                        if c == '{':
                            m = self._KEYCRE.match(rest)
                            if m is None:
                                raise InterpolationSyntaxError(option, section, 'bad interpolation variable reference %r' % rest)
                            path = m.group(1).split(':')
                            rest = rest[m.end():]
                            sect = section
                            opt = option
                            try:
                                if len(path) == 1:
                                    opt = parser.optionxform(path[0])
                                    v = map[opt]
                                elif len(path) == 2:
                                    sect = path[0]
                                    opt = parser.optionxform(path[1])
                                    v = parser.get(sect, opt, raw=True)
                                else:
                                    raise InterpolationSyntaxError(option, section, "More than one ':' found: %r" % (rest,))
                            except (KeyError, NoSectionError, NoOptionError):
                                raise InterpolationMissingOptionError(option, section, rawval, ':'.join(path)) from None

                            if '$' in v:
                                self._interpolate_some(parser, opt, accum, v, sect, dict(parser.items(sect, raw=True)), depth + 1)
                            else:
                                accum.append(v)
                        else:
                            raise InterpolationSyntaxError(option, section, "'$' must be followed by '$' or '{', found: %r" % (
                             rest,))


class LegacyInterpolation(Interpolation):
    __doc__ = 'Deprecated interpolation used in old versions of ConfigParser.\n    Use BasicInterpolation or ExtendedInterpolation instead.'
    _KEYCRE = re.compile('%\\(([^)]*)\\)s|.')

    def before_get--- This code section failed: ---

 L. 529         0  LOAD_FAST                'value'
                2  STORE_FAST               'rawval'

 L. 530         4  LOAD_GLOBAL              MAX_INTERPOLATION_DEPTH
                6  STORE_FAST               'depth'
              8_0  COME_FROM           136  '136'
              8_1  COME_FROM           132  '132'

 L. 531         8  LOAD_FAST                'depth'
               10  POP_JUMP_IF_FALSE   138  'to 138'

 L. 532        12  LOAD_FAST                'depth'
               14  LOAD_CONST               1
               16  INPLACE_SUBTRACT 
               18  STORE_FAST               'depth'

 L. 533        20  LOAD_FAST                'value'
               22  POP_JUMP_IF_FALSE   138  'to 138'
               24  LOAD_STR                 '%('
               26  LOAD_FAST                'value'
               28  COMPARE_OP               in
               30  POP_JUMP_IF_FALSE   138  'to 138'

 L. 534        32  LOAD_GLOBAL              functools
               34  LOAD_ATTR                partial
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _interpolation_replace

 L. 535        40  LOAD_FAST                'parser'

 L. 534        42  LOAD_CONST               ('parser',)
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  STORE_FAST               'replace'

 L. 536        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _KEYCRE
               52  LOAD_METHOD              sub
               54  LOAD_FAST                'replace'
               56  LOAD_FAST                'value'
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'value'

 L. 537        62  SETUP_FINALLY        76  'to 76'

 L. 538        64  LOAD_FAST                'value'
               66  LOAD_FAST                'vars'
               68  BINARY_MODULO    
               70  STORE_FAST               'value'
               72  POP_BLOCK        
               74  JUMP_FORWARD        136  'to 136'
             76_0  COME_FROM_FINALLY    62  '62'

 L. 539        76  DUP_TOP          
               78  LOAD_GLOBAL              KeyError
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE   130  'to 130'
               84  POP_TOP          
               86  STORE_FAST               'e'
               88  POP_TOP          
               90  SETUP_FINALLY       118  'to 118'

 L. 540        92  LOAD_GLOBAL              InterpolationMissingOptionError

 L. 541        94  LOAD_FAST                'option'

 L. 541        96  LOAD_FAST                'section'

 L. 541        98  LOAD_FAST                'rawval'

 L. 541       100  LOAD_FAST                'e'
              102  LOAD_ATTR                args
              104  LOAD_CONST               0
              106  BINARY_SUBSCR    

 L. 540       108  CALL_FUNCTION_4       4  ''

 L. 541       110  LOAD_CONST               None

 L. 540       112  RAISE_VARARGS_2       2  'exception instance with __cause__'
              114  POP_BLOCK        
              116  BEGIN_FINALLY    
            118_0  COME_FROM_FINALLY    90  '90'
              118  LOAD_CONST               None
              120  STORE_FAST               'e'
              122  DELETE_FAST              'e'
              124  END_FINALLY      
              126  POP_EXCEPT       
              128  JUMP_FORWARD        136  'to 136'
            130_0  COME_FROM            82  '82'
              130  END_FINALLY      
              132  JUMP_BACK             8  'to 8'

 L. 543       134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM           128  '128'
            136_1  COME_FROM            74  '74'
              136  JUMP_BACK             8  'to 8'
            138_0  COME_FROM           134  '134'
            138_1  COME_FROM            30  '30'
            138_2  COME_FROM            22  '22'
            138_3  COME_FROM            10  '10'

 L. 544       138  LOAD_FAST                'value'
              140  POP_JUMP_IF_FALSE   162  'to 162'
              142  LOAD_STR                 '%('
              144  LOAD_FAST                'value'
              146  COMPARE_OP               in
              148  POP_JUMP_IF_FALSE   162  'to 162'

 L. 545       150  LOAD_GLOBAL              InterpolationDepthError
              152  LOAD_FAST                'option'
              154  LOAD_FAST                'section'
              156  LOAD_FAST                'rawval'
              158  CALL_FUNCTION_3       3  ''
              160  RAISE_VARARGS_1       1  'exception instance'
            162_0  COME_FROM           148  '148'
            162_1  COME_FROM           140  '140'

 L. 546       162  LOAD_FAST                'value'
              164  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 134

    def before_set(self, parser, section, option, value):
        return value

    @staticmethod
    def _interpolation_replace(match, parser):
        s = match.group(1)
        if s is None:
            return match.group()
        return '%%(%s)s' % parser.optionxform(s)


class RawConfigParser(MutableMapping):
    __doc__ = 'ConfigParser that does not do interpolation.'
    _SECT_TMPL = '\n        \\[                                 # [\n        (?P<header>[^]]+)                  # very permissive!\n        \\]                                 # ]\n        '
    _OPT_TMPL = '\n        (?P<option>.*?)                    # very permissive!\n        \\s*(?P<vi>{delim})\\s*              # any number of space/tab,\n                                           # followed by any of the\n                                           # allowed delimiters,\n                                           # followed by any space/tab\n        (?P<value>.*)$                     # everything up to eol\n        '
    _OPT_NV_TMPL = '\n        (?P<option>.*?)                    # very permissive!\n        \\s*(?:                             # any number of space/tab,\n        (?P<vi>{delim})\\s*                 # optionally followed by\n                                           # any of the allowed\n                                           # delimiters, followed by any\n                                           # space/tab\n        (?P<value>.*))?$                   # everything up to eol\n        '
    _DEFAULT_INTERPOLATION = Interpolation()
    SECTCRE = re.compile(_SECT_TMPL, re.VERBOSE)
    OPTCRE = re.compile(_OPT_TMPL.format(delim='=|:'), re.VERBOSE)
    OPTCRE_NV = re.compile(_OPT_NV_TMPL.format(delim='=|:'), re.VERBOSE)
    NONSPACECRE = re.compile('\\S')
    BOOLEAN_STATES = {'1':True, 
     'yes':True,  'true':True,  'on':True,  '0':False, 
     'no':False,  'false':False,  'off':False}

    def __init__(self, defaults=None, dict_type=_default_dict, allow_no_value=False, *, delimiters=('=', ':'), comment_prefixes=('#', ';'), inline_comment_prefixes=None, strict=True, empty_lines_in_values=True, default_section=DEFAULTSECT, interpolation=_UNSET, converters=_UNSET):
        self._dict = dict_type
        self._sections = self._dict()
        self._defaults = self._dict()
        self._converters = ConverterMapping(self)
        self._proxies = self._dict()
        self._proxies[default_section] = SectionProxy(self, default_section)
        self._delimiters = tuple(delimiters)
        if delimiters == ('=', ':'):
            self._optcre = self.OPTCRE_NV if allow_no_value else self.OPTCRE
        else:
            d = '|'.join((re.escape(d) for d in delimiters))
            if allow_no_value:
                self._optcre = re.compile(self._OPT_NV_TMPL.format(delim=d), re.VERBOSE)
            else:
                self._optcre = re.compile(self._OPT_TMPL.format(delim=d), re.VERBOSE)
        self._comment_prefixes = tuple(comment_prefixes or ())
        self._inline_comment_prefixes = tuple(inline_comment_prefixes or ())
        self._strict = strict
        self._allow_no_value = allow_no_value
        self._empty_lines_in_values = empty_lines_in_values
        self.default_section = default_section
        self._interpolation = interpolation
        if self._interpolation is _UNSET:
            self._interpolation = self._DEFAULT_INTERPOLATION
        if self._interpolation is None:
            self._interpolation = Interpolation()
        if converters is not _UNSET:
            self._converters.update(converters)
        if defaults:
            self._read_defaults(defaults)

    def defaults(self):
        return self._defaults

    def sections(self):
        """Return a list of section names, excluding [DEFAULT]"""
        return list(self._sections.keys())

    def add_section(self, section):
        """Create a new section in the configuration.

        Raise DuplicateSectionError if a section by the specified name
        already exists. Raise ValueError if name is DEFAULT.
        """
        if section == self.default_section:
            raise ValueError('Invalid section name: %r' % section)
        if section in self._sections:
            raise DuplicateSectionError(section)
        self._sections[section] = self._dict()
        self._proxies[section] = SectionProxy(self, section)

    def has_section(self, section):
        """Indicate whether the named section is present in the configuration.

        The DEFAULT section is not acknowledged.
        """
        return section in self._sections

    def options(self, section):
        """Return a list of option names for the given section name."""
        try:
            opts = self._sections[section].copy()
        except KeyError:
            raise NoSectionError(section) from None
        else:
            opts.update(self._defaults)
            return list(opts.keys())

    def read--- This code section failed: ---

 L. 691         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'filenames'
                4  LOAD_GLOBAL              str
                6  LOAD_GLOBAL              bytes
                8  LOAD_GLOBAL              os
               10  LOAD_ATTR                PathLike
               12  BUILD_TUPLE_3         3 
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    24  'to 24'

 L. 692        18  LOAD_FAST                'filenames'
               20  BUILD_LIST_1          1 
               22  STORE_FAST               'filenames'
             24_0  COME_FROM            16  '16'

 L. 693        24  BUILD_LIST_0          0 
               26  STORE_FAST               'read_ok'

 L. 694        28  LOAD_FAST                'filenames'
               30  GET_ITER         
             32_0  COME_FROM           134  '134'
             32_1  COME_FROM            94  '94'
               32  FOR_ITER            136  'to 136'
               34  STORE_FAST               'filename'

 L. 695        36  SETUP_FINALLY        78  'to 78'

 L. 696        38  LOAD_GLOBAL              open
               40  LOAD_FAST                'filename'
               42  LOAD_FAST                'encoding'
               44  LOAD_CONST               ('encoding',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  SETUP_WITH           68  'to 68'
               50  STORE_FAST               'fp'

 L. 697        52  LOAD_FAST                'self'
               54  LOAD_METHOD              _read
               56  LOAD_FAST                'fp'
               58  LOAD_FAST                'filename'
               60  CALL_METHOD_2         2  ''
               62  POP_TOP          
               64  POP_BLOCK        
               66  BEGIN_FINALLY    
             68_0  COME_FROM_WITH       48  '48'
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  END_FINALLY      
               74  POP_BLOCK        
               76  JUMP_FORWARD        102  'to 102'
             78_0  COME_FROM_FINALLY    36  '36'

 L. 698        78  DUP_TOP          
               80  LOAD_GLOBAL              OSError
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE   100  'to 100'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 699        92  POP_EXCEPT       
               94  JUMP_BACK            32  'to 32'
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            84  '84'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            76  '76'

 L. 700       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                'filename'
              106  LOAD_GLOBAL              os
              108  LOAD_ATTR                PathLike
              110  CALL_FUNCTION_2       2  ''
              112  POP_JUMP_IF_FALSE   124  'to 124'

 L. 701       114  LOAD_GLOBAL              os
              116  LOAD_METHOD              fspath
              118  LOAD_FAST                'filename'
              120  CALL_METHOD_1         1  ''
              122  STORE_FAST               'filename'
            124_0  COME_FROM           112  '112'

 L. 702       124  LOAD_FAST                'read_ok'
              126  LOAD_METHOD              append
              128  LOAD_FAST                'filename'
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          
              134  JUMP_BACK            32  'to 32'
            136_0  COME_FROM            32  '32'

 L. 703       136  LOAD_FAST                'read_ok'
              138  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 100_0

    def read_file(self, f, source=None):
        """Like read() but the argument must be a file-like object.

        The `f' argument must be iterable, returning one line at a time.
        Optional second argument is the `source' specifying the name of the
        file being read. If not given, it is taken from f.name. If `f' has no
        `name' attribute, `<???>' is used.
        """
        if source is None:
            try:
                source = f.name
            except AttributeError:
                source = '<???>'

        self._read(f, source)

    def read_string(self, string, source='<string>'):
        """Read configuration from a given string."""
        sfile = io.StringIO(string)
        self.read_file(sfile, source)

    def read_dict(self, dictionary, source='<dict>'):
        """Read configuration from a dictionary.

        Keys are section names, values are dictionaries with keys and values
        that should be present in the section. If the used dictionary type
        preserves order, sections and their keys will be added in order.

        All types held in the dictionary are converted to strings during
        reading, including section names, option names and keys.

        Optional second argument is the `source' specifying the name of the
        dictionary being read.
        """
        elements_added = set()
        for section, keys in dictionary.items():
            section = str(section)
            try:
                self.add_section(section)
            except (DuplicateSectionError, ValueError):
                if self._strict:
                    if section in elements_added:
                        raise
            else:
                elements_added.add(section)
                for key, value in keys.items():
                    key = self.optionxform(str(key))
                    if value is not None:
                        value = str(value)
                    else:
                        if self._strict:
                            if (section, key) in elements_added:
                                raise DuplicateOptionError(section, key, source)
                        elements_added.add((section, key))
                        self.set(section, key, value)

    def readfp(self, fp, filename=None):
        """Deprecated, use read_file instead."""
        warnings.warn("This method will be removed in future versions.  Use 'parser.read_file()' instead.",
          DeprecationWarning,
          stacklevel=2)
        self.read_file(fp, source=filename)

    def get(self, section, option, *, raw=False, vars=None, fallback=_UNSET):
        """Get an option value for a given section.

        If `vars' is provided, it must be a dictionary. The option is looked up
        in `vars' (if provided), `section', and in `DEFAULTSECT' in that order.
        If the key is not found and `fallback' is provided, it is used as
        a fallback value. `None' can be provided as a `fallback' value.

        If interpolation is enabled and the optional argument `raw' is False,
        all interpolations are expanded in the return values.

        Arguments `raw', `vars', and `fallback' are keyword only.

        The section DEFAULT is special.
        """
        try:
            d = self._unify_values(section, vars)
        except NoSectionError:
            if fallback is _UNSET:
                raise
            else:
                return fallback
        else:
            option = self.optionxform(option)
            try:
                value = d[option]
            except KeyError:
                if fallback is _UNSET:
                    raise NoOptionError(option, section)
                else:
                    return fallback
            else:
                if raw or (value is None):
                    return value
                return self._interpolation.before_get(self, section, option, value, d)

    def _get(self, section, conv, option, **kwargs):
        return conv((self.get)(section, option, **kwargs))

    def _get_conv(self, section, option, conv, *, raw=False, vars=None, fallback=_UNSET, **kwargs):
        try:
            return (self._get)(section, conv, option, raw=raw, vars=vars, **kwargs)
        except (NoSectionError, NoOptionError):
            if fallback is _UNSET:
                raise
            return fallback

    def getint(self, section, option, *, raw=False, vars=None, fallback=_UNSET, **kwargs):
        return (self._get_conv)(section, option, int, raw=raw, vars=vars, fallback=fallback, **kwargs)

    def getfloat(self, section, option, *, raw=False, vars=None, fallback=_UNSET, **kwargs):
        return (self._get_conv)(section, option, float, raw=raw, vars=vars, fallback=fallback, **kwargs)

    def getboolean(self, section, option, *, raw=False, vars=None, fallback=_UNSET, **kwargs):
        return (self._get_conv)(section, option, self._convert_to_boolean, raw=raw, 
         vars=vars, fallback=fallback, **kwargs)

    def items(self, section=_UNSET, raw=False, vars=None):
        """Return a list of (name, value) tuples for each option in a section.

        All % interpolations are expanded in the return values, based on the
        defaults passed into the constructor, unless the optional argument
        `raw' is true.  Additional substitutions may be provided using the
        `vars' argument, which must be a dictionary whose contents overrides
        any pre-existing defaults.

        The section DEFAULT is special.
        """
        if section is _UNSET:
            return super().items()
        d = self._defaults.copy()
        try:
            d.update(self._sections[section])
        except KeyError:
            if section != self.default_section:
                raise NoSectionError(section)
        else:
            orig_keys = list(d.keys())
            if vars:
                for key, value in vars.items():
                    d[self.optionxform(key)] = value
                else:
                    value_getter = lambda option: self._interpolation.before_get(self, section, option, d[option], d)
                    if raw:
                        value_getter = lambda option: d[option]
                    else:
                        return [(
                         option, value_getter(option)) for option in orig_keys]

    def popitem(self):
        """Remove a section from the parser and return it as
        a (section_name, section_proxy) tuple. If no section is present, raise
        KeyError.

        The section DEFAULT is never returned because it cannot be removed.
        """
        for key in self.sections():
            value = self[key]
            del self[key]
            return (
             key, value)

        raise KeyError

    def optionxform(self, optionstr):
        return optionstr.lower()

    def has_option(self, section, option):
        """Check for the existence of a given option in a given section.
        If the specified `section' is None or an empty string, DEFAULT is
        assumed. If the specified `section' does not exist, returns False."""
        if not section or section == self.default_section:
            option = self.optionxform(option)
            return option in self._defaults
        if section not in self._sections:
            return False
        option = self.optionxform(option)
        return option in self._sections[section] or option in self._defaults

    def set(self, section, option, value=None):
        """Set an option."""
        if value:
            value = self._interpolation.before_set(self, section, option, value)
        if not section or section == self.default_section:
            sectdict = self._defaults
        else:
            pass
        try:
            sectdict = self._sections[section]
        except KeyError:
            raise NoSectionError(section) from None
        else:
            sectdict[self.optionxform(option)] = value

    def write(self, fp, space_around_delimiters=True):
        """Write an .ini-format representation of the configuration state.

        If `space_around_delimiters' is True (the default), delimiters
        between keys and values are surrounded by spaces.
        """
        if space_around_delimiters:
            d = ' {} '.format(self._delimiters[0])
        else:
            d = self._delimiters[0]
        if self._defaults:
            self._write_section(fp, self.default_section, self._defaults.items(), d)
        for section in self._sections:
            self._write_section(fp, section, self._sections[section].items(), d)

    def _write_section(self, fp, section_name, section_items, delimiter):
        """Write a single section to the specified `fp'."""
        fp.write('[{}]\n'.format(section_name))
        for key, value in section_items:
            value = self._interpolation.before_write(self, section_name, key, value)
            if value is not None or not self._allow_no_value:
                value = delimiter + str(value).replace('\n', '\n\t')
            else:
                value = ''
            fp.write('{}{}\n'.format(key, value))
        else:
            fp.write('\n')

    def remove_option(self, section, option):
        """Remove an option."""
        if not section or section == self.default_section:
            sectdict = self._defaults
        else:
            pass
        try:
            sectdict = self._sections[section]
        except KeyError:
            raise NoSectionError(section) from None
        else:
            option = self.optionxform(option)
            existed = option in sectdict
            if existed:
                del sectdict[option]
            else:
                return existed

    def remove_section(self, section):
        """Remove a file section."""
        existed = section in self._sections
        if existed:
            del self._sections[section]
            del self._proxies[section]
        return existed

    def __getitem__(self, key):
        if key != self.default_section:
            if not self.has_section(key):
                raise KeyError(key)
            return self._proxies[key]

    def __setitem__(self, key, value):
        if key in self:
            if self[key] is value:
                return
        if key == self.default_section:
            self._defaults.clear()
        elif key in self._sections:
            self._sections[key].clear()
        self.read_dict({key: value})

    def __delitem__(self, key):
        if key == self.default_section:
            raise ValueError('Cannot remove the default section.')
        if not self.has_section(key):
            raise KeyError(key)
        self.remove_section(key)

    def __contains__(self, key):
        return key == self.default_section or self.has_section(key)

    def __len__(self):
        return len(self._sections) + 1

    def __iter__(self):
        return itertools.chain((self.default_section,), self._sections.keys())

    def _read(self, fp, fpname):
        """Parse a sectioned configuration file.

        Each section in a configuration file contains a header, indicated by
        a name in square brackets (`[]'), plus key/value options, indicated by
        `name' and `value' delimited with a specific substring (`=' or `:' by
        default).

        Values can span multiple lines, as long as they are indented deeper
        than the first line of the value. Depending on the parser's mode, blank
        lines may be treated as parts of multiline values or ignored.

        Configuration files may include comments, prefixed by specific
        characters (`#' and `;' by default). Comments may appear on their own
        in an otherwise empty line or may be entered in lines holding values or
        section names.
        """
        elements_added = set()
        cursect = None
        sectname = None
        optname = None
        lineno = 0
        indent_level = 0
        e = None
        for lineno, line in enumerate(fp, start=1):
            comment_start = sys.maxsize
            inline_prefixes = {-1:p for p in self._inline_comment_prefixes}
            while comment_start == sys.maxsize:
                if inline_prefixes:
                    next_prefixes = {}
                    for prefix, index in inline_prefixes.items():
                        index = line.find(prefix, index + 1)
                        if index == -1:
                            pass
                        else:
                            next_prefixes[prefix] = index
                            if not index == 0:
                                if index > 0:
                                    if line[(index - 1)].isspace():
                                        pass
                            comment_start = min(comment_start, index)
                        inline_prefixes = next_prefixes

            for prefix in self._comment_prefixes:
                if line.strip().startswith(prefix):
                    comment_start = 0
                    break
                if comment_start == sys.maxsize:
                    comment_start = None
                else:
                    value = line[:comment_start].strip()
                if not value:
                    if self._empty_lines_in_values:
                        if not comment_start is None or cursect is not None:
                            if optname and cursect[optname] is not None:
                                cursect[optname].append('')
                            else:
                                indent_level = sys.maxsize
                else:
                    first_nonspace = self.NONSPACECRE.search(line)
                    cur_indent_level = first_nonspace.start() if first_nonspace else 0
                    if cursect is not None:
                        if optname and cur_indent_level > indent_level:
                            cursect[optname].append(value)
                        else:
                            indent_level = cur_indent_level
                            mo = self.SECTCRE.match(value)
                    if mo:
                        sectname = mo.group('header')
                        if sectname in self._sections:
                            if self._strict:
                                if sectname in elements_added:
                                    raise DuplicateSectionError(sectname, fpname, lineno)
                            cursect = self._sections[sectname]
                            elements_added.add(sectname)
                        elif sectname == self.default_section:
                            cursect = self._defaults
                        else:
                            cursect = self._dict()
                            self._sections[sectname] = cursect
                            self._proxies[sectname] = SectionProxy(self, sectname)
                            elements_added.add(sectname)
                        optname = None
                    elif cursect is None:
                        raise MissingSectionHeaderError(fpname, lineno, line)
            else:
                mo = self._optcre.match(value)

            if mo:
                optname, vi, optval = mo.group('option', 'vi', 'value')
                if not optname:
                    e = self._handle_error(e, fpname, lineno, line)
                optname = self.optionxform(optname.rstrip())
                if self._strict:
                    if (
                     sectname, optname) in elements_added:
                        raise DuplicateOptionError(sectname, optname, fpname, lineno)
                elements_added.add((sectname, optname))
                if optval is not None:
                    optval = optval.strip()
                    cursect[optname] = [optval]
                else:
                    cursect[optname] = None
            else:
                e = self._handle_error(e, fpname, lineno, line)
        else:
            self._join_multiline_values()
            if e:
                raise e

    def _join_multiline_values(self):
        defaults = (
         self.default_section, self._defaults)
        all_sections = itertools.chain((defaults,), self._sections.items())
        for section, options in all_sections:
            for name, val in options.items():
                if isinstance(val, list):
                    val = '\n'.join(val).rstrip()
                else:
                    options[name] = self._interpolation.before_read(self, section, name, val)

    def _read_defaults(self, defaults):
        """Read the defaults passed in the initializer.
        Note: values can be non-string."""
        for key, value in defaults.items():
            self._defaults[self.optionxform(key)] = value

    def _handle_error(self, exc, fpname, lineno, line):
        if not exc:
            exc = ParsingError(fpname)
        exc.append(lineno, repr(line))
        return exc

    def _unify_values(self, section, vars):
        """Create a sequence of lookups with 'vars' taking priority over
        the 'section' which takes priority over the DEFAULTSECT.

        """
        sectiondict = {}
        try:
            sectiondict = self._sections[section]
        except KeyError:
            if section != self.default_section:
                raise NoSectionError(section) from None
        else:
            vardict = {}
            if vars:
                for key, value in vars.items():
                    if value is not None:
                        value = str(value)
                    else:
                        vardict[self.optionxform(key)] = value

                return _ChainMap(vardict, sectiondict, self._defaults)

    def _convert_to_boolean(self, value):
        """Return a boolean value translating from other types if necessary.
        """
        if value.lower() not in self.BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % value)
        return self.BOOLEAN_STATES[value.lower()]

    def _validate_value_types(self, *, section='', option='', value=''):
        """Raises a TypeError for non-string values.

        The only legal non-string value if we allow valueless
        options is None, so we need to check if the value is a
        string if:
        - we do not allow valueless options, or
        - we allow valueless options but the value is not None

        For compatibility reasons this method is not used in classic set()
        for RawConfigParsers. It is invoked in every case for mapping protocol
        access and in ConfigParser.set().
        """
        if not isinstance(section, str):
            raise TypeError('section names must be strings')
        if not isinstance(option, str):
            raise TypeError('option keys must be strings')
        if not self._allow_no_value or value:
            if not isinstance(value, str):
                raise TypeError('option values must be strings')

    @property
    def converters(self):
        return self._converters


class ConfigParser(RawConfigParser):
    __doc__ = 'ConfigParser implementing interpolation.'
    _DEFAULT_INTERPOLATION = BasicInterpolation()

    def set(self, section, option, value=None):
        """Set an option.  Extends RawConfigParser.set by validating type and
        interpolation syntax on the value."""
        self._validate_value_types(option=option, value=value)
        super().set(section, option, value)

    def add_section(self, section):
        self._validate_value_types(section=section)
        super().add_section(section)

    def _read_defaults(self, defaults):
        """Reads the defaults passed in the initializer, implicitly converting
        values to strings like the rest of the API.

        Does not perform interpolation for backwards compatibility.
        """
        try:
            hold_interpolation = self._interpolation
            self._interpolation = Interpolation()
            self.read_dict({self.default_section: defaults})
        finally:
            self._interpolation = hold_interpolation


class SafeConfigParser(ConfigParser):
    __doc__ = 'ConfigParser alias for backwards compatibility purposes.'

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        warnings.warn('The SafeConfigParser class has been renamed to ConfigParser in Python 3.2. This alias will be removed in future versions. Use ConfigParser directly instead.',
          DeprecationWarning,
          stacklevel=2)


class SectionProxy(MutableMapping):
    __doc__ = 'A proxy for a single section from a parser.'

    def __init__(self, parser, name):
        """Creates a view on a section of the specified `name` in `parser`."""
        self._parser = parser
        self._name = name
        for conv in parser.converters:
            key = 'get' + conv
            getter = functools.partial((self.get), _impl=(getattr(parser, key)))
            setattr(self, key, getter)

    def __repr__(self):
        return '<Section: {}>'.format(self._name)

    def __getitem__(self, key):
        if not self._parser.has_option(self._name, key):
            raise KeyError(key)
        return self._parser.get(self._name, key)

    def __setitem__(self, key, value):
        self._parser._validate_value_types(option=key, value=value)
        return self._parser.set(self._name, key, value)

    def __delitem__(self, key):
        if not (self._parser.has_option(self._name, key) and self._parser.remove_option(self._name, key)):
            raise KeyError(key)

    def __contains__(self, key):
        return self._parser.has_option(self._name, key)

    def __len__(self):
        return len(self._options())

    def __iter__(self):
        return self._options().__iter__()

    def _options(self):
        if self._name != self._parser.default_section:
            return self._parser.options(self._name)
        return self._parser.defaults()

    @property
    def parser(self):
        return self._parser

    @property
    def name(self):
        return self._name

    def get(self, option, fallback=None, *, raw=False, vars=None, _impl=None, **kwargs):
        """Get an option value.

        Unless `fallback` is provided, `None` will be returned if the option
        is not found.

        """
        if not _impl:
            _impl = self._parser.get
        return _impl(self._name, option, raw=raw, vars=vars, fallback=fallback, **kwargs)


class ConverterMapping(MutableMapping):
    __doc__ = 'Enables reuse of get*() methods between the parser and section proxies.\n\n    If a parser class implements a getter directly, the value for the given\n    key will be ``None``. The presence of the converter name here enables\n    section proxies to find and use the implementation on the parser class.\n    '
    GETTERCRE = re.compile('^get(?P<name>.+)$')

    def __init__(self, parser):
        self._parser = parser
        self._data = {}
        for getter in dir(self._parser):
            m = self.GETTERCRE.match(getter)
            if m:
                if not callable(getattr(self._parser, getter)):
                    pass
                else:
                    self._data[m.group('name')] = None

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        try:
            k = 'get' + key
        except TypeError:
            raise ValueError('Incompatible key: {} (type: {})'.format(key, type(key)))
        else:
            if k == 'get':
                raise ValueError('Incompatible key: cannot use "" as a name')
            self._data[key] = value
            func = functools.partial((self._parser._get_conv), conv=value)
            func.converter = value
            setattr(self._parser, k, func)
            for proxy in self._parser.values():
                getter = functools.partial((proxy.get), _impl=func)
                setattr(proxy, k, getter)

    def __delitem__--- This code section failed: ---

 L.1346         0  SETUP_FINALLY        18  'to 18'

 L.1347         2  LOAD_STR                 'get'
                4  LOAD_FAST                'key'
                6  JUMP_IF_TRUE_OR_POP    10  'to 10'
                8  LOAD_CONST               None
             10_0  COME_FROM             6  '6'
               10  BINARY_ADD       
               12  STORE_FAST               'k'
               14  POP_BLOCK        
               16  JUMP_FORWARD         46  'to 46'
             18_0  COME_FROM_FINALLY     0  '0'

 L.1348        18  DUP_TOP          
               20  LOAD_GLOBAL              TypeError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    44  'to 44'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.1349        32  LOAD_GLOBAL              KeyError
               34  LOAD_FAST                'key'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
               40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            24  '24'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'
             46_1  COME_FROM            16  '16'

 L.1350        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _data
               50  LOAD_FAST                'key'
               52  DELETE_SUBSCR    

 L.1351        54  LOAD_GLOBAL              itertools
               56  LOAD_METHOD              chain
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _parser
               62  BUILD_TUPLE_1         1 
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _parser
               68  LOAD_METHOD              values
               70  CALL_METHOD_0         0  ''
               72  CALL_METHOD_2         2  ''
               74  GET_ITER         
             76_0  COME_FROM           120  '120'
             76_1  COME_FROM           116  '116'
             76_2  COME_FROM           112  '112'
             76_3  COME_FROM            94  '94'
               76  FOR_ITER            122  'to 122'
               78  STORE_FAST               'inst'

 L.1352        80  SETUP_FINALLY        96  'to 96'

 L.1353        82  LOAD_GLOBAL              delattr
               84  LOAD_FAST                'inst'
               86  LOAD_FAST                'k'
               88  CALL_FUNCTION_2       2  ''
               90  POP_TOP          
               92  POP_BLOCK        
               94  JUMP_BACK            76  'to 76'
             96_0  COME_FROM_FINALLY    80  '80'

 L.1354        96  DUP_TOP          
               98  LOAD_GLOBAL              AttributeError
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   118  'to 118'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L.1357       110  POP_EXCEPT       
              112  JUMP_BACK            76  'to 76'
              114  POP_EXCEPT       
              116  JUMP_BACK            76  'to 76'
            118_0  COME_FROM           102  '102'
              118  END_FINALLY      
              120  JUMP_BACK            76  'to 76'
            122_0  COME_FROM            76  '76'

Parse error at or near `JUMP_BACK' instruction at offset 116

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)