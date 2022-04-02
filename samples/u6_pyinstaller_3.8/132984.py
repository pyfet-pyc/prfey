# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: importlib\metadata.py
import io, os, re, abc, csv, sys, email, pathlib, zipfile, operator, functools, itertools, posixpath, collections
from configparser import ConfigParser
from contextlib import suppress
from importlib import import_module
from importlib.abc import MetaPathFinder
from itertools import starmap
__all__ = [
 'Distribution',
 'DistributionFinder',
 'PackageNotFoundError',
 'distribution',
 'distributions',
 'entry_points',
 'files',
 'metadata',
 'requires',
 'version']

class PackageNotFoundError(ModuleNotFoundError):
    __doc__ = 'The package was not found.'


class EntryPoint(collections.namedtuple('EntryPointBase', 'name value group')):
    __doc__ = 'An entry point as defined by Python packaging conventions.\n\n    See `the packaging docs on entry points\n    <https://packaging.python.org/specifications/entry-points/>`_\n    for more information.\n    '
    pattern = re.compile('(?P<module>[\\w.]+)\\s*(:\\s*(?P<attr>[\\w.]+))?\\s*(?P<extras>\\[.*\\])?\\s*$')

    def load(self):
        """Load the entry point from its definition. If only a module
        is indicated by the value, return that module. Otherwise,
        return the named object.
        """
        match = self.pattern.match(self.value)
        module = import_module(match.group('module'))
        attrs = filter(None, (match.group('attr') or '').split('.'))
        return functools.reduce(getattr, attrs, module)

    @property
    def extras(self):
        match = self.pattern.match(self.value)
        return list(re.finditer('\\w+', match.group('extras') or ''))

    @classmethod
    def _from_config(cls, config):
        return [cls(name, value, group) for group in config.sections() for name, value in config.items(group)]

    @classmethod
    def _from_text(cls, text):
        config = ConfigParser(delimiters='=')
        config.optionxform = str
        try:
            config.read_string(text)
        except AttributeError:
            config.readfp(io.StringIO(text))
        else:
            return EntryPoint._from_config(config)

    def __iter__(self):
        """
        Supply iter so one may construct dicts of EntryPoints easily.
        """
        return iter((self.name, self))

    def __reduce__(self):
        return (
         self.__class__,
         (
          self.name, self.value, self.group))


class PackagePath(pathlib.PurePosixPath):
    __doc__ = 'A reference to a path in a package'

    def read_text--- This code section failed: ---

 L. 123         0  LOAD_FAST                'self'
                2  LOAD_METHOD              locate
                4  CALL_METHOD_0         0  ''
                6  LOAD_ATTR                open
                8  LOAD_FAST                'encoding'
               10  LOAD_CONST               ('encoding',)
               12  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               14  SETUP_WITH           38  'to 38'
               16  STORE_FAST               'stream'

 L. 124        18  LOAD_FAST                'stream'
               20  LOAD_METHOD              read
               22  CALL_METHOD_0         0  ''
               24  POP_BLOCK        
               26  ROT_TWO          
               28  BEGIN_FINALLY    
               30  WITH_CLEANUP_START
               32  WITH_CLEANUP_FINISH
               34  POP_FINALLY           0  ''
               36  RETURN_VALUE     
             38_0  COME_FROM_WITH       14  '14'
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 26

    def read_binary--- This code section failed: ---

 L. 127         0  LOAD_FAST                'self'
                2  LOAD_METHOD              locate
                4  CALL_METHOD_0         0  ''
                6  LOAD_METHOD              open
                8  LOAD_STR                 'rb'
               10  CALL_METHOD_1         1  ''
               12  SETUP_WITH           36  'to 36'
               14  STORE_FAST               'stream'

 L. 128        16  LOAD_FAST                'stream'
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

    def locate(self):
        """Return a path-like object for this path"""
        return self.dist.locate_file(self)


class FileHash:

    def __init__(self, spec):
        self.mode, _, self.value = spec.partition('=')

    def __repr__(self):
        return '<FileHash mode: {} value: {}>'.format(self.mode, self.value)


class Distribution:
    __doc__ = 'A Python distribution package.'

    @abc.abstractmethod
    def read_text(self, filename):
        """Attempt to load metadata file given by the name.

        :param filename: The name of the file in the distribution info.
        :return: The text if found, otherwise None.
        """
        pass

    @abc.abstractmethod
    def locate_file(self, path):
        """
        Given a path to a file in this distribution, return a path
        to it.
        """
        pass

    @classmethod
    def from_name(cls, name):
        """Return the Distribution for the given package name.

        :param name: The name of the distribution package to search for.
        :return: The Distribution instance (or subclass thereof) for the named
            package, if found.
        :raises PackageNotFoundError: When the named package's distribution
            metadata cannot be found.
        """
        for resolver in cls._discover_resolvers():
            dists = resolver(DistributionFinder.Context(name=name))
            dist = next(dists, None)
            if dist is not None:
                return dist
        else:
            raise PackageNotFoundError(name)

    @classmethod
    def discover(cls, **kwargs):
        """Return an iterable of Distribution objects for all packages.

        Pass a ``context`` or pass keyword arguments for constructing
        a context.

        :context: A ``DistributionFinder.Context`` object.
        :return: Iterable of Distribution objects for all packages.
        """
        context = kwargs.pop('context', None)
        if context:
            if kwargs:
                raise ValueError('cannot accept context and kwargs')
        context = context or (DistributionFinder.Context)(**kwargs)
        return itertools.chain.from_iterable((resolver(context) for resolver in cls._discover_resolvers()))

    @staticmethod
    def at(path):
        """Return a Distribution for the indicated metadata path

        :param path: a string or path-like object
        :return: a concrete Distribution instance for the path
        """
        return PathDistribution(pathlib.Path(path))

    @staticmethod
    def _discover_resolvers():
        """Search the meta_path for resolvers."""
        declared = (getattr(finder, 'find_distributions', None) for finder in sys.meta_path)
        return filter(None, declared)

    @property
    def metadata(self):
        """Return the parsed metadata for this Distribution.

        The returned object will have keys that name the various bits of
        metadata.  See PEP 566 for details.
        """
        text = self.read_text('METADATA') or self.read_text('PKG-INFO') or self.read_text('')
        return email.message_from_string(text)

    @property
    def version(self):
        """Return the 'Version' metadata for the distribution package."""
        return self.metadata['Version']

    @property
    def entry_points(self):
        return EntryPoint._from_text(self.read_text('entry_points.txt'))

    @property
    def files(self):
        """Files in this distribution.

        :return: List of PackagePath for this distribution or None

        Result is `None` if the metadata file that enumerates files
        (i.e. RECORD for dist-info or SOURCES.txt for egg-info) is
        missing.
        Result may be empty if the metadata exists but is empty.
        """
        file_lines = self._read_files_distinfo() or self._read_files_egginfo()

        def make_file(name, hash=None, size_str=None):
            result = PackagePath(name)
            result.hash = FileHash(hash) if hash else None
            result.size = int(size_str) if size_str else None
            result.dist = self
            return result

        return file_lines and list(starmap(make_file, csv.reader(file_lines)))

    def _read_files_distinfo(self):
        """
        Read the lines of RECORD
        """
        text = self.read_text('RECORD')
        return text and text.splitlines()

    def _read_files_egginfo(self):
        """
        SOURCES.txt might contain literal commas, so wrap each line
        in quotes.
        """
        text = self.read_text('SOURCES.txt')
        return text and map('"{}"'.format, text.splitlines())

    @property
    def requires(self):
        """Generated requirements specified for this Distribution"""
        reqs = self._read_dist_info_reqs() or self._read_egg_info_reqs()
        return reqs and list(reqs)

    def _read_dist_info_reqs(self):
        return self.metadata.get_all('Requires-Dist')

    def _read_egg_info_reqs(self):
        source = self.read_text('requires.txt')
        return source and self._deps_from_requires_text(source)

    @classmethod
    def _deps_from_requires_text(cls, source):
        section_pairs = cls._read_sections(source.splitlines())
        sections = {list(map(operator.itemgetter('line'), results)):section for section, results in itertools.groupby(section_pairs, operator.itemgetter('section'))}
        return cls._convert_egg_info_reqs_to_simple_reqs(sections)

    @staticmethod
    def _read_sections(lines):
        section = None
        for line in filter(None, lines):
            section_match = re.match('\\[(.*)\\]$', line)
            if section_match:
                section = section_match.group(1)
            else:
                (yield locals())

    @staticmethod
    def _convert_egg_info_reqs_to_simple_reqs(sections):
        """
        Historically, setuptools would solicit and store 'extra'
        requirements, including those with environment markers,
        in separate sections. More modern tools expect each
        dependency to be defined separately, with any relevant
        extras and environment markers attached directly to that
        requirement. This method converts the former to the
        latter. See _test_deps_from_requires_text for an example.
        """

        def make_condition(name):
            return name and 'extra == "{name}"'.format(name=name)

        def parse_condition(section):
            section = section or ''
            extra, sep, markers = section.partition(':')
            if extra:
                if markers:
                    markers = '({markers})'.format(markers=markers)
            conditions = list(filter(None, [markers, make_condition(extra)]))
            if conditions:
                return '; ' + ' and '.join(conditions)
            return ''

        for section, deps in sections.items():
            for dep in deps:
                (yield dep + parse_condition(section))


class DistributionFinder(MetaPathFinder):
    __doc__ = '\n    A MetaPathFinder capable of discovering installed distributions.\n    '

    class Context:
        __doc__ = '\n        Keyword arguments presented by the caller to\n        ``distributions()`` or ``Distribution.discover()``\n        to narrow the scope of a search for distributions\n        in all DistributionFinders.\n\n        Each DistributionFinder may expect any parameters\n        and should attempt to honor the canonical\n        parameters defined below when appropriate.\n        '
        name = None

        def __init__(self, **kwargs):
            vars(self).update(kwargs)

        @property
        def path(self):
            """
            The path that a distribution finder should search.

            Typically refers to Python package paths and defaults
            to ``sys.path``.
            """
            return vars(self).get('path', sys.path)

    @abc.abstractmethod
    def find_distributions(self, context=Context()):
        """
        Find distributions.

        Return an iterable of all Distribution instances capable of
        loading the metadata for packages matching the ``context``,
        a DistributionFinder.Context instance.
        """
        pass


class FastPath:
    __doc__ = '\n    Micro-optimized class for searching a path for\n    children.\n    '

    def __init__(self, root):
        self.root = root
        self.base = os.path.basename(root).lower()

    def joinpath(self, child):
        return pathlib.Path(self.root, child)

    def children--- This code section failed: ---

 L. 400         0  LOAD_GLOBAL              suppress
                2  LOAD_GLOBAL              Exception
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           38  'to 38'
                8  POP_TOP          

 L. 401        10  LOAD_GLOBAL              os
               12  LOAD_METHOD              listdir
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                root
               18  JUMP_IF_TRUE_OR_POP    22  'to 22'
               20  LOAD_STR                 ''
             22_0  COME_FROM            18  '18'
               22  CALL_METHOD_1         1  ''
               24  POP_BLOCK        
               26  ROT_TWO          
               28  BEGIN_FINALLY    
               30  WITH_CLEANUP_START
               32  WITH_CLEANUP_FINISH
               34  POP_FINALLY           0  ''
               36  RETURN_VALUE     
             38_0  COME_FROM_WITH        6  '6'
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  END_FINALLY      

 L. 402        44  LOAD_GLOBAL              suppress
               46  LOAD_GLOBAL              Exception
               48  CALL_FUNCTION_1       1  ''
               50  SETUP_WITH           74  'to 74'
               52  POP_TOP          

 L. 403        54  LOAD_FAST                'self'
               56  LOAD_METHOD              zip_children
               58  CALL_METHOD_0         0  ''
               60  POP_BLOCK        
               62  ROT_TWO          
               64  BEGIN_FINALLY    
               66  WITH_CLEANUP_START
               68  WITH_CLEANUP_FINISH
               70  POP_FINALLY           0  ''
               72  RETURN_VALUE     
             74_0  COME_FROM_WITH       50  '50'
               74  WITH_CLEANUP_START
               76  WITH_CLEANUP_FINISH
               78  END_FINALLY      

 L. 404        80  BUILD_LIST_0          0 
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 26

    def zip_children(self):
        zip_path = zipfile.Path(self.root)
        names = zip_path.root.namelist()
        self.joinpath = zip_path.joinpath
        return dict.fromkeys((child.split(posixpath.sep, 1)[0] for child in names))

    def is_egg(self, search):
        base = self.base
        return base == search.versionless_egg_name or base.startswith(search.prefix) and base.endswith('.egg')

    def search--- This code section failed: ---

 L. 424         0  LOAD_FAST                'self'
                2  LOAD_METHOD              children
                4  CALL_METHOD_0         0  ''
                6  GET_ITER         
              8_0  COME_FROM            70  '70'
              8_1  COME_FROM            62  '62'
                8  FOR_ITER             86  'to 86'
               10  STORE_FAST               'child'

 L. 425        12  LOAD_FAST                'child'
               14  LOAD_METHOD              lower
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'n_low'

 L. 426        20  LOAD_FAST                'n_low'
               22  LOAD_FAST                'name'
               24  LOAD_ATTR                exact_matches
               26  COMPARE_OP               in
               28  POP_JUMP_IF_TRUE     72  'to 72'

 L. 427        30  LOAD_FAST                'n_low'
               32  LOAD_METHOD              startswith
               34  LOAD_FAST                'name'
               36  LOAD_ATTR                prefix
               38  CALL_METHOD_1         1  ''

 L. 426        40  POP_JUMP_IF_FALSE    54  'to 54'

 L. 428        42  LOAD_FAST                'n_low'
               44  LOAD_METHOD              endswith
               46  LOAD_FAST                'name'
               48  LOAD_ATTR                suffixes
               50  CALL_METHOD_1         1  ''

 L. 426        52  POP_JUMP_IF_TRUE     72  'to 72'
             54_0  COME_FROM            40  '40'

 L. 430        54  LOAD_FAST                'self'
               56  LOAD_METHOD              is_egg
               58  LOAD_FAST                'name'
               60  CALL_METHOD_1         1  ''

 L. 426        62  POP_JUMP_IF_FALSE     8  'to 8'

 L. 430        64  LOAD_FAST                'n_low'
               66  LOAD_STR                 'egg-info'
               68  COMPARE_OP               ==

 L. 426        70  POP_JUMP_IF_FALSE     8  'to 8'
             72_0  COME_FROM            52  '52'
             72_1  COME_FROM            28  '28'

 L. 431        72  LOAD_FAST                'self'
               74  LOAD_METHOD              joinpath
               76  LOAD_FAST                'child'
               78  CALL_METHOD_1         1  ''
               80  YIELD_VALUE      
               82  POP_TOP          
               84  JUMP_BACK             8  'to 8'

Parse error at or near `POP_TOP' instruction at offset 82


class Prepared:
    __doc__ = '\n    A prepared search for metadata on a possibly-named package.\n    '
    normalized = ''
    prefix = ''
    suffixes = ('.dist-info', '.egg-info')
    exact_matches = [''][:0]
    versionless_egg_name = ''

    def __init__(self, name):
        self.name = name
        if name is None:
            return
        self.normalized = name.lower().replace('-', '_')
        self.prefix = self.normalized + '-'
        self.exact_matches = [self.normalized + suffix for suffix in self.suffixes]
        self.versionless_egg_name = self.normalized + '.egg'


class MetadataPathFinder(DistributionFinder):

    @classmethod
    def find_distributions(cls, context=DistributionFinder.Context()):
        """
        Find distributions.

        Return an iterable of all Distribution instances capable of
        loading the metadata for packages matching ``context.name``
        (or all names if ``None`` indicated) along the paths in the list
        of directories ``context.path``.
        """
        found = cls._search_paths(context.name, context.path)
        return map(PathDistribution, found)

    @classmethod
    def _search_paths(cls, name, paths):
        """Find metadata directories in paths heuristically."""
        return itertools.chain.from_iterable((path.search(Prepared(name)) for path in map(FastPath, paths)))


class PathDistribution(Distribution):

    def __init__(self, path):
        """Construct a distribution from a path to the metadata directory.

        :param path: A pathlib.Path or similar object supporting
                     .joinpath(), __div__, .parent, and .read_text().
        """
        self._path = path

    def read_text--- This code section failed: ---

 L. 488         0  LOAD_GLOBAL              suppress
                2  LOAD_GLOBAL              FileNotFoundError
                4  LOAD_GLOBAL              IsADirectoryError
                6  LOAD_GLOBAL              KeyError

 L. 489         8  LOAD_GLOBAL              NotADirectoryError

 L. 489        10  LOAD_GLOBAL              PermissionError

 L. 488        12  CALL_FUNCTION_5       5  ''
               14  SETUP_WITH           50  'to 50'
               16  POP_TOP          

 L. 490        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _path
               22  LOAD_METHOD              joinpath
               24  LOAD_FAST                'filename'
               26  CALL_METHOD_1         1  ''
               28  LOAD_ATTR                read_text
               30  LOAD_STR                 'utf-8'
               32  LOAD_CONST               ('encoding',)
               34  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               36  POP_BLOCK        
               38  ROT_TWO          
               40  BEGIN_FINALLY    
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  POP_FINALLY           0  ''
               48  RETURN_VALUE     
             50_0  COME_FROM_WITH       14  '14'
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 38

    read_text.__doc__ = Distribution.read_text.__doc__

    def locate_file(self, path):
        return self._path.parent / path


def distribution(distribution_name):
    """Get the ``Distribution`` instance for the named package.

    :param distribution_name: The name of the distribution package as a string.
    :return: A ``Distribution`` instance (or subclass thereof).
    """
    return Distribution.from_name(distribution_name)


def distributions(**kwargs):
    """Get all ``Distribution`` instances in the current environment.

    :return: An iterable of ``Distribution`` instances.
    """
    return (Distribution.discover)(**kwargs)


def metadata(distribution_name):
    """Get the metadata for the named package.

    :param distribution_name: The name of the distribution package to query.
    :return: An email.Message containing the parsed metadata.
    """
    return Distribution.from_name(distribution_name).metadata


def version(distribution_name):
    """Get the version string for the named package.

    :param distribution_name: The name of the distribution package to query.
    :return: The version string for the package as defined in the package's
        "Version" metadata key.
    """
    return distribution(distribution_name).version


def entry_points():
    """Return EntryPoint objects for all installed packages.

    :return: EntryPoint objects for all installed packages.
    """
    eps = itertools.chain.from_iterable((dist.entry_points for dist in distributions()))
    by_group = operator.attrgetter('group')
    ordered = sorted(eps, key=by_group)
    grouped = itertools.groupby(ordered, by_group)
    return {tuple(eps):group for group, eps in grouped}


def files(distribution_name):
    """Return a list of files for the named package.

    :param distribution_name: The name of the distribution package to query.
    :return: List of files composing the distribution.
    """
    return distribution(distribution_name).files


def requires(distribution_name):
    """
    Return a list of requirements for the named package.

    :return: An iterator of requirements, suitable for
    packaging.requirement.Requirement.
    """
    return distribution(distribution_name).requires