# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\distutils\npy_pkg_config.py
from __future__ import division, absolute_import, print_function
import sys, re, os
if sys.version_info[0] < 3:
    from ConfigParser import RawConfigParser
else:
    from configparser import RawConfigParser
__all__ = [
 'FormatError', 'PkgNotFound', 'LibraryInfo', 'VariableSet',
 'read_config', 'parse_flags']
_VAR = re.compile('\\$\\{([a-zA-Z0-9_-]+)\\}')

class FormatError(IOError):
    __doc__ = '\n    Exception thrown when there is a problem parsing a configuration file.\n\n    '

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class PkgNotFound(IOError):
    __doc__ = 'Exception raised when a package can not be located.'

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def parse_flags(line):
    """
    Parse a line from a config file containing compile flags.

    Parameters
    ----------
    line : str
        A single line containing one or more compile flags.

    Returns
    -------
    d : dict
        Dictionary of parsed flags, split into relevant categories.
        These categories are the keys of `d`:

        * 'include_dirs'
        * 'library_dirs'
        * 'libraries'
        * 'macros'
        * 'ignored'

    """
    d = {'include_dirs':[],  'library_dirs':[],  'libraries':[],  'macros':[],  'ignored':[]}
    flags = (' ' + line).split(' -')
    for flag in flags:
        flag = '-' + flag
        if len(flag) > 0:
            if flag.startswith('-I'):
                d['include_dirs'].append(flag[2:].strip())
            elif flag.startswith('-L'):
                d['library_dirs'].append(flag[2:].strip())
            elif flag.startswith('-l'):
                d['libraries'].append(flag[2:].strip())
            elif flag.startswith('-D'):
                d['macros'].append(flag[2:].strip())
            else:
                d['ignored'].append(flag)
        return d


def _escape_backslash(val):
    return val.replace('\\', '\\\\')


class LibraryInfo(object):
    __doc__ = '\n    Object containing build information about a library.\n\n    Parameters\n    ----------\n    name : str\n        The library name.\n    description : str\n        Description of the library.\n    version : str\n        Version string.\n    sections : dict\n        The sections of the configuration file for the library. The keys are\n        the section headers, the values the text under each header.\n    vars : class instance\n        A `VariableSet` instance, which contains ``(name, value)`` pairs for\n        variables defined in the configuration file for the library.\n    requires : sequence, optional\n        The required libraries for the library to be installed.\n\n    Notes\n    -----\n    All input parameters (except "sections" which is a method) are available as\n    attributes of the same name.\n\n    '

    def __init__(self, name, description, version, sections, vars, requires=None):
        self.name = name
        self.description = description
        if requires:
            self.requires = requires
        else:
            self.requires = []
        self.version = version
        self._sections = sections
        self.vars = vars

    def sections(self):
        """
        Return the section headers of the config file.

        Parameters
        ----------
        None

        Returns
        -------
        keys : list of str
            The list of section headers.

        """
        return list(self._sections.keys())

    def cflags(self, section='default'):
        val = self.vars.interpolate(self._sections[section]['cflags'])
        return _escape_backslash(val)

    def libs(self, section='default'):
        val = self.vars.interpolate(self._sections[section]['libs'])
        return _escape_backslash(val)

    def __str__(self):
        m = [
         'Name: %s' % self.name, 'Description: %s' % self.description]
        if self.requires:
            m.append('Requires:')
        else:
            m.append('Requires: %s' % ','.join(self.requires))
        m.append('Version: %s' % self.version)
        return '\n'.join(m)


class VariableSet(object):
    __doc__ = '\n    Container object for the variables defined in a config file.\n\n    `VariableSet` can be used as a plain dictionary, with the variable names\n    as keys.\n\n    Parameters\n    ----------\n    d : dict\n        Dict of items in the "variables" section of the configuration file.\n\n    '

    def __init__(self, d):
        self._raw_data = dict([(k, v) for k, v in d.items()])
        self._re = {}
        self._re_sub = {}
        self._init_parse()

    def _init_parse(self):
        for k, v in self._raw_data.items():
            self._init_parse_var(k, v)

    def _init_parse_var(self, name, value):
        self._re[name] = re.compile('\\$\\{%s\\}' % name)
        self._re_sub[name] = value

    def interpolate(self, value):

        def _interpolate(value):
            for k in self._re.keys():
                value = self._re[k].sub(self._re_sub[k], value)
            else:
                return value

        while _VAR.search(value):
            nvalue = _interpolate(value)
            if nvalue == value:
                break
            value = nvalue

        return value

    def variables(self):
        """
        Return the list of variable names.

        Parameters
        ----------
        None

        Returns
        -------
        names : list of str
            The names of all variables in the `VariableSet` instance.

        """
        return list(self._raw_data.keys())

    def __getitem__(self, name):
        return self._raw_data[name]

    def __setitem__(self, name, value):
        self._raw_data[name] = value
        self._init_parse_var(name, value)


def parse_meta(config):
    if not config.has_section('meta'):
        raise FormatError('No meta section found !')
    d = dict(config.items('meta'))
    for k in ('name', 'description', 'version'):
        if k not in d:
            raise FormatError('Option %s (section [meta]) is mandatory, but not found' % k)
        if 'requires' not in d:
            d['requires'] = []
        return d


def parse_variables(config):
    if not config.has_section('variables'):
        raise FormatError('No variables section found !')
    d = {}
    for name, value in config.items('variables'):
        d[name] = value
    else:
        return VariableSet(d)


def parse_sections(config):
    return (meta_d, r)


def pkg_to_filename(pkg_name):
    return '%s.ini' % pkg_name


def parse_config(filename, dirs=None):
    if dirs:
        filenames = [os.path.join(d, filename) for d in dirs]
    else:
        filenames = [
         filename]
    config = RawConfigParser()
    n = config.read(filenames)
    if not len(n) >= 1:
        raise PkgNotFound('Could not find file(s) %s' % str(filenames))
    meta = parse_meta(config)
    vars = {}
    if config.has_section('variables'):
        for name, value in config.items('variables'):
            vars[name] = _escape_backslash(value)

    secs = [s for s in config.sections() if s not in ('meta', 'variables')]
    sections = {}
    requires = {}
    for s in secs:
        d = {}
        if config.has_option(s, 'requires'):
            requires[s] = config.get(s, 'requires')
        for name, value in config.items(s):
            d[name] = value
        else:
            sections[s] = d

    else:
        return (
         meta, vars, sections, requires)


def _read_config_imp(filenames, dirs=None):

    def _read_config(f):
        meta, vars, sections, reqs = parse_config(f, dirs)
        for rname, rvalue in reqs.items():
            nmeta, nvars, nsections, nreqs = _read_config(pkg_to_filename(rvalue))
            for k, v in nvars.items():
                if k not in vars:
                    vars[k] = v
                for oname, ovalue in nsections[rname].items():
                    if ovalue:
                        sections[rname][oname] += ' %s' % ovalue
                else:
                    return (
                     meta, vars, sections, reqs)

    meta, vars, sections, reqs = _read_config(filenames)
    if 'pkgdir' not in vars:
        if 'pkgname' in vars:
            pkgname = vars['pkgname']
            if pkgname not in sys.modules:
                raise ValueError('You should import %s to get information on %s' % (
                 pkgname, meta['name']))
            mod = sys.modules[pkgname]
            vars['pkgdir'] = _escape_backslash(os.path.dirname(mod.__file__))
    return LibraryInfo(name=(meta['name']), description=(meta['description']), version=(meta['version']),
      sections=sections,
      vars=(VariableSet(vars)))


_CACHE = {}

def read_config--- This code section failed: ---

 L. 370         0  SETUP_FINALLY        12  'to 12'

 L. 371         2  LOAD_GLOBAL              _CACHE
                4  LOAD_FAST                'pkgname'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 372        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    56  'to 56'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 373        26  LOAD_GLOBAL              _read_config_imp
               28  LOAD_GLOBAL              pkg_to_filename
               30  LOAD_FAST                'pkgname'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_FAST                'dirs'
               36  CALL_FUNCTION_2       2  ''
               38  STORE_FAST               'v'

 L. 374        40  LOAD_FAST                'v'
               42  LOAD_GLOBAL              _CACHE
               44  LOAD_FAST                'pkgname'
               46  STORE_SUBSCR     

 L. 375        48  LOAD_FAST                'v'
               50  ROT_FOUR         
               52  POP_EXCEPT       
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'
               56  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 22


if __name__ == '__main__':
    import sys
    from optparse import OptionParser
    import glob
    parser = OptionParser()
    parser.add_option('--cflags', dest='cflags', action='store_true', help='output all preprocessor and compiler flags')
    parser.add_option('--libs', dest='libs', action='store_true', help='output all linker flags')
    parser.add_option('--use-section', dest='section', help='use this section instead of default for options')
    parser.add_option('--version', dest='version', action='store_true', help='output version')
    parser.add_option('--atleast-version', dest='min_version', help='Minimal version')
    parser.add_option('--list-all', dest='list_all', action='store_true', help='Minimal version')
    parser.add_option('--define-variable', dest='define_variable', help='Replace variable with the given value')
    options, args = parser.parse_args(sys.argv)
    if len(args) < 2:
        raise ValueError('Expect package name on the command line:')
    if options.list_all:
        files = glob.glob('*.ini')
        for f in files:
            info = read_config(f)
            print('%s\t%s - %s' % (info.name, info.name, info.description))

    else:
        pkg_name = args[1]
        d = os.environ.get('NPY_PKG_CONFIG_PATH')
        if d:
            info = read_config(pkg_name, ['numpy/core/lib/npy-pkg-config', '.', d])
        else:
            info = read_config(pkg_name, ['numpy/core/lib/npy-pkg-config', '.'])
        if options.section:
            section = options.section
        else:
            section = 'default'
        if options.define_variable:
            m = re.search('([\\S]+)=([\\S]+)', options.define_variable)
            if not m:
                raise ValueError('--define-variable option should be of the form --define-variable=foo=bar')
            else:
                name = m.group(1)
                value = m.group(2)
            info.vars[name] = value
        if options.cflags:
            print(info.cflags(section))
        if options.libs:
            print(info.libs(section))
        if options.version:
            print(info.version)
        if options.min_version:
            print(info.version >= options.min_version)