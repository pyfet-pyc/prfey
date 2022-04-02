# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\__init__.py
"""Extensions to the 'distutils' for large or complex distributions"""
from fnmatch import fnmatchcase
import functools, os, re, _distutils_hack.override, distutils.core
from distutils.errors import DistutilsOptionError
from distutils.util import convert_path
from ._deprecation_warning import SetuptoolsDeprecationWarning
import setuptools.version
from setuptools.extension import Extension
from setuptools.dist import Distribution
from setuptools.depends import Require
from . import monkey
__all__ = [
 'setup', 'Distribution', 'Command', 'Extension', 'Require',
 'SetuptoolsDeprecationWarning',
 'find_packages', 'find_namespace_packages']
__version__ = setuptools.version.__version__
bootstrap_install_from = None
run_2to3_on_doctests = True
lib2to3_fixer_packages = [
 'lib2to3.fixes']

class PackageFinder:
    __doc__ = '\n    Generate a list of all Python packages found within a directory\n    '

    @classmethod
    def find(cls, where='.', exclude=(), include=('*',)):
        """Return a list all Python packages found within directory 'where'

        'where' is the root directory which will be searched for packages.  It
        should be supplied as a "cross-platform" (i.e. URL-style) path; it will
        be converted to the appropriate local path syntax.

        'exclude' is a sequence of package names to exclude; '*' can be used
        as a wildcard in the names, such that 'foo.*' will exclude all
        subpackages of 'foo' (but not 'foo' itself).

        'include' is a sequence of package names to include.  If it's
        specified, only the named packages will be included.  If it's not
        specified, all found packages will be included.  'include' can contain
        shell style wildcard patterns just like 'exclude'.
        """
        return list(cls._find_packages_iter(convert_path(where), (cls._build_filter)(*('ez_setup',
                                                                                       '*__pycache__'), *exclude), (cls._build_filter)(*include)))

    @classmethod
    def _find_packages_iter(cls, where, exclude, include):
        """
        All the packages found in 'where' that pass the 'include' filter, but
        not the 'exclude' filter.
        """
        for root, dirs, files in os.walk(where, followlinks=True):
            all_dirs = dirs[:]
            dirs[:] = []
            for dir in all_dirs:
                full_path = os.path.join(root, dir)
                rel_path = os.path.relpath(full_path, where)
                package = rel_path.replace(os.path.sep, '.')
                if not '.' in dir:
                    if not cls._looks_like_package(full_path):
                        continue
                    if include(package):
                        if not exclude(package):
                            yield package
                        dirs.append(dir)

    @staticmethod
    def _looks_like_package(path):
        """Does a directory look like a package?"""
        return os.path.isfile(os.path.join(path, '__init__.py'))

    @staticmethod
    def _build_filter(*patterns):
        """
        Given a list of patterns, return a callable that will be true only if
        the input matches at least one of the patterns.
        """
        return --- This code section failed: ---

 L. 107         0  LOAD_GLOBAL              any
                2  LOAD_CLOSURE             'name'
                4  BUILD_TUPLE_1         1 
                6  LOAD_GENEXPR             '<code_object <genexpr>>'
                8  LOAD_STR                 'PackageFinder._build_filter.<locals>.<lambda>.<locals>.<genexpr>'
               10  MAKE_FUNCTION_8          'closure'
               12  LOAD_DEREF               'patterns'
               14  GET_ITER         
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1


class PEP420PackageFinder(PackageFinder):

    @staticmethod
    def _looks_like_package(path):
        return True


find_packages = PackageFinder.find
find_namespace_packages = PEP420PackageFinder.find

def _install_setup_requires(attrs):

    class MinimalDistribution(distutils.core.Distribution):
        __doc__ = '\n        A minimal version of a distribution for supporting the\n        fetch_build_eggs interface.\n        '

        def __init__(self, attrs):
            _incl = ('dependency_links', 'setup_requires')
            filtered = {k:attrs[k] for k in set(_incl) & set(attrs)}
            distutils.core.Distribution.__init__(self, filtered)

        def finalize_options(self):
            """
            Disable finalize_options to avoid building the working set.
            Ref #2158.
            """
            pass

    dist = MinimalDistribution(attrs)
    dist.parse_config_files(ignore_option_errors=True)
    if dist.setup_requires:
        dist.fetch_build_eggs(dist.setup_requires)


def setup(**attrs):
    _install_setup_requires(attrs)
    return (distutils.core.setup)(**attrs)


setup.__doc__ = distutils.core.setup.__doc__
_Command = monkey.get_unpatched(distutils.core.Command)

class Command(_Command):
    __doc__ = _Command.__doc__
    command_consumes_arguments = False

    def __init__(self, dist, **kw):
        """
        Construct the command for dist, updating
        vars(self) with any keyword parameters.
        """
        _Command.__init__(self, dist)
        vars(self).update(kw)

    def _ensure_stringlike(self, option, what, default=None):
        val = getattr(self, option)
        if val is None:
            setattr(self, option, default)
            return default
        if not isinstance(val, str):
            raise DistutilsOptionError("'%s' must be a %s (got `%s`)" % (
             option, what, val))
        return val

    def ensure_string_list(self, option):
        r"""Ensure that 'option' is a list of strings.  If 'option' is
        currently a string, we split it either on /,\s*/ or /\s+/, so
        "foo bar baz", "foo,bar,baz", and "foo,   bar baz" all become
        ["foo", "bar", "baz"].
        """
        val = getattr(self, option)
        if val is None:
            return
        if isinstance(val, str):
            setattr(self, option, re.split(',\\s*|\\s+', val))
        else:
            if isinstance(val, list):
                ok = all((isinstance(v, str) for v in val))
            else:
                ok = False
            if not ok:
                raise DistutilsOptionError("'%s' must be a list of strings (got %r)" % (
                 option, val))

    def reinitialize_command(self, command, reinit_subcommands=0, **kw):
        cmd = _Command.reinitialize_command(self, command, reinit_subcommands)
        vars(cmd).update(kw)
        return cmd


def _find_all_simple(path):
    """
    Find all files under 'path'
    """
    results = (os.path.join(base, file) for base, dirs, files in os.walk(path, followlinks=True) for file in files)
    return filter(os.path.isfile, results)


def findall(dir=os.curdir):
    """
    Find all files under 'dir' and return the list of full filenames.
    Unless dir is '.', return full filenames with dir prepended.
    """
    files = _find_all_simple(dir)
    if dir == os.curdir:
        make_rel = functools.partial((os.path.relpath), start=dir)
        files = map(make_rel, files)
    return list(files)


class sic(str):
    __doc__ = 'Treat this string as-is (https://en.wikipedia.org/wiki/Sic)'


monkey.patch_all()