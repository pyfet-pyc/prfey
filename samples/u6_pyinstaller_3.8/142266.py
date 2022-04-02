# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\command\egg_info.py
"""setuptools.command.egg_info

Create a distribution's .egg-info directory and contents"""
import distutils.filelist as _FileList
from distutils.errors import DistutilsInternalError
from distutils.util import convert_path
from distutils import log
import distutils.errors, distutils.filelist, os, re, sys, io, warnings, time, collections
from setuptools.extern import six
from setuptools.extern.six.moves import map
from setuptools import Command
import setuptools.command.sdist as sdist
from setuptools.command.sdist import walk_revctrl
from setuptools.command.setopt import edit_config
from setuptools.command import bdist_egg
from pkg_resources import parse_requirements, safe_name, parse_version, safe_version, yield_lines, EntryPoint, iter_entry_points, to_filename
import setuptools.unicode_utils as unicode_utils
import setuptools.glob as glob
from setuptools.extern import packaging
from setuptools import SetuptoolsDeprecationWarning

def translate_pattern(glob):
    """
    Translate a file path glob like '*.txt' in to a regular expression.
    This differs from fnmatch.translate which allows wildcards to match
    directory separators. It also knows about '**/' which matches any number of
    directories.
    """
    pat = ''
    chunks = glob.split(os.path.sep)
    sep = re.escape(os.sep)
    valid_char = '[^%s]' % (sep,)
    for c, chunk in enumerate(chunks):
        last_chunk = c == len(chunks) - 1
        if chunk == '**':
            if last_chunk:
                pat += '.*'
            else:
                pat += '(?:%s+%s)*' % (valid_char, sep)
        else:
            i = 0
            chunk_len = len(chunk)
            if i < chunk_len:
                char = chunk[i]
                if char == '*':
                    pat += valid_char + '*'
                else:
                    if char == '?':
                        pat += valid_char
                    else:
                        if char == '[':
                            inner_i = i + 1
                            if inner_i < chunk_len:
                                if chunk[inner_i] == '!':
                                    inner_i = inner_i + 1
                            if inner_i < chunk_len:
                                if chunk[inner_i] == ']':
                                    inner_i = inner_i + 1
                            if inner_i < chunk_len:
                                if chunk[inner_i] != ']':
                                    inner_i = inner_i + 1
                            elif inner_i >= chunk_len:
                                pat += re.escape(char)
                            else:
                                inner = chunk[i + 1:inner_i]
                                char_class = ''
                                if inner[0] == '!':
                                    char_class = '^'
                                    inner = inner[1:]
                                char_class += re.escape(inner)
                                pat += '[%s]' % (char_class,)
                                i = inner_i
                        else:
                            pat += re.escape(char)
                i += 1
            else:
                if not last_chunk:
                    pat += sep
                pat += '\\Z'
                return re.compile(pat, flags=(re.MULTILINE | re.DOTALL))


class InfoCommon:
    tag_build = None
    tag_date = None

    @property
    def name(self):
        return safe_name(self.distribution.get_name())

    def tagged_version(self):
        version = self.distribution.get_version()
        if self.vtags:
            if version.endswith(self.vtags):
                return safe_version(version)
        return safe_version(version + self.vtags)

    def tags(self):
        version = ''
        if self.tag_build:
            version += self.tag_build
        if self.tag_date:
            version += time.strftime('-%Y%m%d')
        return version

    vtags = property(tags)


class egg_info(InfoCommon, Command):
    description = "create a distribution's .egg-info directory"
    user_options = [
     ('egg-base=', 'e', 'directory containing .egg-info directories (default: top of the source tree)'),
     ('tag-date', 'd', 'Add date stamp (e.g. 20050528) to version number'),
     ('tag-build=', 'b', 'Specify explicit tag to add to version number'),
     ('no-date', 'D', "Don't include date stamp [default]")]
    boolean_options = [
     'tag-date']
    negative_opt = {'no-date': 'tag-date'}

    def initialize_options(self):
        self.egg_base = None
        self.egg_name = None
        self.egg_info = None
        self.egg_version = None
        self.broken_egg_info = False

    @property
    def tag_svn_revision(self):
        pass

    @tag_svn_revision.setter
    def tag_svn_revision(self, value):
        pass

    def save_version_info(self, filename):
        """
        Materialize the value of date into the
        build tag. Install build keys in a deterministic order
        to avoid arbitrary reordering on subsequent builds.
        """
        egg_info = collections.OrderedDict()
        egg_info['tag_build'] = self.tags()
        egg_info['tag_date'] = 0
        edit_config(filename, dict(egg_info=egg_info))

    def finalize_options(self):
        self.egg_name = self.name
        self.egg_version = self.tagged_version()
        parsed_version = parse_version(self.egg_version)
        try:
            is_version = isinstance(parsed_version, packaging.version.Version)
            spec = '%s==%s' if is_version else '%s===%s'
            list(parse_requirements(spec % (self.egg_name, self.egg_version)))
        except ValueError as e:
            try:
                raise distutils.errors.DistutilsOptionError('Invalid distribution name or version syntax: %s-%s' % (
                 self.egg_name, self.egg_version)) from e
            finally:
                e = None
                del e

        else:
            if self.egg_base is None:
                dirs = self.distribution.package_dir
                self.egg_base = (dirs or {}).get('', os.curdir)
            self.ensure_dirname('egg_base')
            self.egg_info = to_filename(self.egg_name) + '.egg-info'
            if self.egg_base != os.curdir:
                self.egg_info = os.path.join(self.egg_base, self.egg_info)
            if '-' in self.egg_name:
                self.check_broken_egg_info()
            self.distribution.metadata.version = self.egg_version
            pd = self.distribution._patched_dist
            if pd is not None:
                if pd.key == self.egg_name.lower():
                    pd._version = self.egg_version
                    pd._parsed_version = parse_version(self.egg_version)
                    self.distribution._patched_dist = None

    def write_or_delete_file(self, what, filename, data, force=False):
        """Write `data` to `filename` or delete if empty

        If `data` is non-empty, this routine is the same as ``write_file()``.
        If `data` is empty but not ``None``, this is the same as calling
        ``delete_file(filename)`.  If `data` is ``None``, then this is a no-op
        unless `filename` exists, in which case a warning is issued about the
        orphaned file (if `force` is false), or deleted (if `force` is true).
        """
        if data:
            self.write_file(what, filename, data)
        else:
            if os.path.exists(filename):
                if data is None:
                    if not force:
                        log.warn('%s not set in setup(), but %s exists', what, filename)
                        return None
                self.delete_file(filename)

    def write_file(self, what, filename, data):
        """Write `data` to `filename` (if not a dry run) after announcing it

        `what` is used in a log message to identify what is being written
        to the file.
        """
        log.info('writing %s to %s', what, filename)
        if not six.PY2:
            data = data.encode('utf-8')
        if not self.dry_run:
            f = open(filename, 'wb')
            f.write(data)
            f.close()

    def delete_file(self, filename):
        """Delete `filename` (if not a dry run) after announcing it"""
        log.info('deleting %s', filename)
        if not self.dry_run:
            os.unlink(filename)

    def run(self):
        self.mkpath(self.egg_info)
        os.utime(self.egg_info, None)
        installer = self.distribution.fetch_build_egg
        for ep in iter_entry_points('egg_info.writers'):
            ep.require(installer=installer)
            writer = ep.resolve()
            writer(self, ep.name, os.path.join(self.egg_info, ep.name))
        else:
            nl = os.path.join(self.egg_info, 'native_libs.txt')
            if os.path.exists(nl):
                self.delete_file(nl)
            self.find_sources()

    def find_sources(self):
        """Generate SOURCES.txt manifest file"""
        manifest_filename = os.path.join(self.egg_info, 'SOURCES.txt')
        mm = manifest_maker(self.distribution)
        mm.manifest = manifest_filename
        mm.run()
        self.filelist = mm.filelist

    def check_broken_egg_info(self):
        bei = self.egg_name + '.egg-info'
        if self.egg_base != os.curdir:
            bei = os.path.join(self.egg_base, bei)
        if os.path.exists(bei):
            log.warn('------------------------------------------------------------------------------\nNote: Your current .egg-info directory has a \'-\' in its name;\nthis will not work correctly with "setup.py develop".\n\nPlease rename %s to %s to correct this problem.\n------------------------------------------------------------------------------', bei, self.egg_info)
            self.broken_egg_info = self.egg_info
            self.egg_info = bei


class FileList(_FileList):

    def process_template_line(self, line):
        action, patterns, dir, dir_pattern = self._parse_template_line(line)
        if action == 'include':
            self.debug_print('include ' + ' '.join(patterns))
            for pattern in patterns:
                if not self.include(pattern):
                    log.warn("warning: no files found matching '%s'", pattern)

        else:
            if action == 'exclude':
                self.debug_print('exclude ' + ' '.join(patterns))
                for pattern in patterns:
                    if not self.exclude(pattern):
                        log.warn("warning: no previously-included files found matching '%s'", pattern)

            else:
                if action == 'global-include':
                    self.debug_print('global-include ' + ' '.join(patterns))
                    for pattern in patterns:
                        if not self.global_include(pattern):
                            log.warn("warning: no files found matching '%s' anywhere in distribution", pattern)

                else:
                    if action == 'global-exclude':
                        self.debug_print('global-exclude ' + ' '.join(patterns))
                        for pattern in patterns:
                            if not self.global_exclude(pattern):
                                log.warn("warning: no previously-included files matching '%s' found anywhere in distribution", pattern)

                    else:
                        if action == 'recursive-include':
                            self.debug_print('recursive-include %s %s' % (
                             dir, ' '.join(patterns)))
                            for pattern in patterns:
                                if not self.recursive_include(dir, pattern):
                                    log.warn("warning: no files found matching '%s' under directory '%s'", pattern, dir)

                        else:
                            if action == 'recursive-exclude':
                                self.debug_print('recursive-exclude %s %s' % (
                                 dir, ' '.join(patterns)))
                                for pattern in patterns:
                                    if not self.recursive_exclude(dir, pattern):
                                        log.warn("warning: no previously-included files matching '%s' found under directory '%s'", pattern, dir)

                            else:
                                if action == 'graft':
                                    self.debug_print('graft ' + dir_pattern)
                                    self.graft(dir_pattern) or log.warn("warning: no directories found matching '%s'", dir_pattern)
                                else:
                                    if action == 'prune':
                                        self.debug_print('prune ' + dir_pattern)
                                        self.prune(dir_pattern) or log.warn("no previously-included directories found matching '%s'", dir_pattern)
                                    else:
                                        raise DistutilsInternalError("this cannot happen: invalid action '%s'" % action)

    def _remove_files(self, predicate):
        """
        Remove all files from the file list that match the predicate.
        Return True if any matching files were removed
        """
        found = False
        for i in range(len(self.files) - 1, -1, -1):
            if predicate(self.files[i]):
                self.debug_print(' removing ' + self.files[i])
                del self.files[i]
                found = True
            return found

    def include(self, pattern):
        """Include files that match 'pattern'."""
        found = [f for f in glob(pattern) if not os.path.isdir(f)]
        self.extend(found)
        return bool(found)

    def exclude(self, pattern):
        """Exclude files that match 'pattern'."""
        match = translate_pattern(pattern)
        return self._remove_files(match.match)

    def recursive_include(self, dir, pattern):
        """
        Include all files anywhere in 'dir/' that match the pattern.
        """
        full_pattern = os.path.join(dir, '**', pattern)
        found = [f for f in glob(full_pattern, recursive=True) if not os.path.isdir(f)]
        self.extend(found)
        return bool(found)

    def recursive_exclude(self, dir, pattern):
        """
        Exclude any file anywhere in 'dir/' that match the pattern.
        """
        match = translate_pattern(os.path.join(dir, '**', pattern))
        return self._remove_files(match.match)

    def graft(self, dir):
        """Include all files from 'dir/'."""
        found = [item for match_dir in glob(dir) for item in distutils.filelist.findall(match_dir)]
        self.extend(found)
        return bool(found)

    def prune(self, dir):
        """Filter out files from 'dir/'."""
        match = translate_pattern(os.path.join(dir, '**'))
        return self._remove_files(match.match)

    def global_include(self, pattern):
        """
        Include all files anywhere in the current directory that match the
        pattern. This is very inefficient on large file trees.
        """
        if self.allfiles is None:
            self.findall()
        match = translate_pattern(os.path.join('**', pattern))
        found = [f for f in self.allfiles if match.match(f)]
        self.extend(found)
        return bool(found)

    def global_exclude(self, pattern):
        """
        Exclude all files anywhere that match the pattern.
        """
        match = translate_pattern(os.path.join('**', pattern))
        return self._remove_files(match.match)

    def append(self, item):
        if item.endswith('\r'):
            item = item[:-1]
        path = convert_path(item)
        if self._safe_path(path):
            self.files.append(path)

    def extend(self, paths):
        self.files.extend(filter(self._safe_path, paths))

    def _repair(self):
        """
        Replace self.files with only safe paths

        Because some owners of FileList manipulate the underlying
        ``files`` attribute directly, this method must be called to
        repair those paths.
        """
        self.files = list(filter(self._safe_path, self.files))

    def _safe_path--- This code section failed: ---

 L. 496         0  LOAD_STR                 "'%s' not %s encodable -- skipping"
                2  STORE_FAST               'enc_warn'

 L. 499         4  LOAD_GLOBAL              unicode_utils
                6  LOAD_METHOD              filesys_decode
                8  LOAD_FAST                'path'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'u_path'

 L. 500        14  LOAD_FAST                'u_path'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    40  'to 40'

 L. 501        22  LOAD_GLOBAL              log
               24  LOAD_METHOD              warn
               26  LOAD_STR                 "'%s' in unexpected encoding -- skipping"
               28  LOAD_FAST                'path'
               30  BINARY_MODULO    
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 502        36  LOAD_CONST               False
               38  RETURN_VALUE     
             40_0  COME_FROM            20  '20'

 L. 505        40  LOAD_GLOBAL              unicode_utils
               42  LOAD_METHOD              try_encode
               44  LOAD_FAST                'u_path'
               46  LOAD_STR                 'utf-8'
               48  CALL_METHOD_2         2  ''
               50  STORE_FAST               'utf8_path'

 L. 506        52  LOAD_FAST                'utf8_path'
               54  LOAD_CONST               None
               56  COMPARE_OP               is
               58  POP_JUMP_IF_FALSE    78  'to 78'

 L. 507        60  LOAD_GLOBAL              log
               62  LOAD_METHOD              warn
               64  LOAD_FAST                'enc_warn'
               66  LOAD_FAST                'path'
               68  LOAD_STR                 'utf-8'
               70  CALL_METHOD_3         3  ''
               72  POP_TOP          

 L. 508        74  LOAD_CONST               False
               76  RETURN_VALUE     
             78_0  COME_FROM            58  '58'

 L. 510        78  SETUP_FINALLY       114  'to 114'

 L. 512        80  LOAD_GLOBAL              os
               82  LOAD_ATTR                path
               84  LOAD_METHOD              exists
               86  LOAD_FAST                'u_path'
               88  CALL_METHOD_1         1  ''
               90  POP_JUMP_IF_TRUE    104  'to 104'
               92  LOAD_GLOBAL              os
               94  LOAD_ATTR                path
               96  LOAD_METHOD              exists
               98  LOAD_FAST                'utf8_path'
              100  CALL_METHOD_1         1  ''
              102  POP_JUMP_IF_FALSE   110  'to 110'
            104_0  COME_FROM            90  '90'

 L. 513       104  POP_BLOCK        
              106  LOAD_CONST               True
              108  RETURN_VALUE     
            110_0  COME_FROM           102  '102'
              110  POP_BLOCK        
              112  JUMP_FORWARD        152  'to 152'
            114_0  COME_FROM_FINALLY    78  '78'

 L. 515       114  DUP_TOP          
              116  LOAD_GLOBAL              UnicodeEncodeError
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   150  'to 150'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L. 516       128  LOAD_GLOBAL              log
              130  LOAD_METHOD              warn
              132  LOAD_FAST                'enc_warn'
              134  LOAD_FAST                'path'
              136  LOAD_GLOBAL              sys
              138  LOAD_METHOD              getfilesystemencoding
              140  CALL_METHOD_0         0  ''
              142  CALL_METHOD_3         3  ''
              144  POP_TOP          
              146  POP_EXCEPT       
              148  JUMP_FORWARD        152  'to 152'
            150_0  COME_FROM           120  '120'
              150  END_FINALLY      
            152_0  COME_FROM           148  '148'
            152_1  COME_FROM           112  '112'

Parse error at or near `LOAD_CONST' instruction at offset 106


class manifest_maker(sdist):
    template = 'MANIFEST.in'

    def initialize_options(self):
        self.use_defaults = 1
        self.prune = 1
        self.manifest_only = 1
        self.force_manifest = 1

    def finalize_options(self):
        pass

    def run(self):
        self.filelist = FileList()
        if not os.path.exists(self.manifest):
            self.write_manifest()
        self.add_defaults()
        if os.path.exists(self.template):
            self.read_template()
        self.prune_file_list()
        self.filelist.sort()
        self.filelist.remove_duplicates()
        self.write_manifest()

    def _manifest_normalize(self, path):
        path = unicode_utils.filesys_decode(path)
        return path.replace(os.sep, '/')

    def write_manifest(self):
        """
        Write the file list in 'self.filelist' to the manifest file
        named by 'self.manifest'.
        """
        self.filelist._repair()
        files = [self._manifest_normalize(f) for f in self.filelist.files]
        msg = "writing manifest file '%s'" % self.manifest
        self.execute(write_file, (self.manifest, files), msg)

    def warn(self, msg):
        if not self._should_suppress_warning(msg):
            sdist.warn(self, msg)

    @staticmethod
    def _should_suppress_warning(msg):
        """
        suppress missing-file warnings from sdist
        """
        return re.match('standard file .*not found', msg)

    def add_defaults(self):
        sdist.add_defaults(self)
        self.check_license()
        self.filelist.append(self.template)
        self.filelist.append(self.manifest)
        rcfiles = list(walk_revctrl())
        if rcfiles:
            self.filelist.extend(rcfiles)
        else:
            if os.path.exists(self.manifest):
                self.read_manifest()
        if os.path.exists('setup.py'):
            self.filelist.append('setup.py')
        ei_cmd = self.get_finalized_command('egg_info')
        self.filelist.graft(ei_cmd.egg_info)

    def prune_file_list(self):
        build = self.get_finalized_command('build')
        base_dir = self.distribution.get_fullname()
        self.filelist.prune(build.build_base)
        self.filelist.prune(base_dir)
        sep = re.escape(os.sep)
        self.filelist.exclude_pattern(('(^|' + sep + ')(RCS|CVS|\\.svn)' + sep), is_regex=1)


def write_file(filename, contents):
    """Create a file with the specified name and write 'contents' (a
    sequence of strings without line terminators) to it.
    """
    contents = '\n'.join(contents)
    contents = contents.encode('utf-8')
    with open(filename, 'wb') as (f):
        f.write(contents)


def write_pkg_info(cmd, basename, filename):
    log.info('writing %s', filename)
    if not cmd.dry_run:
        metadata = cmd.distribution.metadata
        metadata.version, oldver = cmd.egg_version, metadata.version
        metadata.name, oldname = cmd.egg_name, metadata.name
        try:
            metadata.write_pkg_info(cmd.egg_info)
        finally:
            metadata.name, metadata.version = oldname, oldver

        safe = getattr(cmd.distribution, 'zip_safe', None)
        bdist_egg.write_safety_flag(cmd.egg_info, safe)


def warn_depends_obsolete(cmd, basename, filename):
    if os.path.exists(filename):
        log.warn("WARNING: 'depends.txt' is not used by setuptools 0.6!\nUse the install_requires/extras_require setup() args instead.")


def _write_requirements(stream, reqs):
    lines = yield_lines(reqs or ())

    def append_cr(line):
        return line + '\n'

    lines = map(append_cr, lines)
    stream.writelines(lines)


def write_requirements(cmd, basename, filename):
    dist = cmd.distribution
    data = six.StringIO()
    _write_requirements(data, dist.install_requires)
    extras_require = dist.extras_require or {}
    for extra in sorted(extras_require):
        data.write(('\n[{extra}]\n'.format)(**vars()))
        _write_requirements(data, extras_require[extra])
    else:
        cmd.write_or_delete_file('requirements', filename, data.getvalue())


def write_setup_requirements(cmd, basename, filename):
    data = io.StringIO()
    _write_requirements(data, cmd.distribution.setup_requires)
    cmd.write_or_delete_file('setup-requirements', filename, data.getvalue())


def write_toplevel_names(cmd, basename, filename):
    pkgs = dict.fromkeys([k.split('.', 1)[0] for k in cmd.distribution.iter_distribution_names()])
    cmd.write_file('top-level names', filename, '\n'.join(sorted(pkgs)) + '\n')


def overwrite_arg(cmd, basename, filename):
    write_arg(cmd, basename, filename, True)


def write_arg(cmd, basename, filename, force=False):
    argname = os.path.splitext(basename)[0]
    value = getattr(cmd.distribution, argname, None)
    if value is not None:
        value = '\n'.join(value) + '\n'
    cmd.write_or_delete_file(argname, filename, value, force)


def write_entries(cmd, basename, filename):
    ep = cmd.distribution.entry_points
    if isinstance(ep, six.string_types) or ep is None:
        data = ep
    else:
        if ep is not None:
            data = []
            for section, contents in sorted(ep.items()):
                if not isinstance(contents, six.string_types):
                    contents = EntryPoint.parse_group(section, contents)
                    contents = '\n'.join(sorted(map(str, contents.values())))
                data.append('[%s]\n%s\n\n' % (section, contents))
            else:
                data = ''.join(data)

    cmd.write_or_delete_file('entry points', filename, data, True)


def get_pkg_info_revision--- This code section failed: ---

 L. 709         0  LOAD_GLOBAL              warnings
                2  LOAD_METHOD              warn

 L. 710         4  LOAD_STR                 'get_pkg_info_revision is deprecated.'

 L. 710         6  LOAD_GLOBAL              EggInfoDeprecationWarning

 L. 709         8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 711        12  LOAD_GLOBAL              os
               14  LOAD_ATTR                path
               16  LOAD_METHOD              exists
               18  LOAD_STR                 'PKG-INFO'
               20  CALL_METHOD_1         1  ''
               22  POP_JUMP_IF_FALSE   102  'to 102'

 L. 712        24  LOAD_GLOBAL              io
               26  LOAD_METHOD              open
               28  LOAD_STR                 'PKG-INFO'
               30  CALL_METHOD_1         1  ''
               32  SETUP_WITH           96  'to 96'
               34  STORE_FAST               'f'

 L. 713        36  LOAD_FAST                'f'
               38  GET_ITER         
             40_0  COME_FROM            58  '58'
               40  FOR_ITER             92  'to 92'
               42  STORE_FAST               'line'

 L. 714        44  LOAD_GLOBAL              re
               46  LOAD_METHOD              match
               48  LOAD_STR                 'Version:.*-r(\\d+)\\s*$'
               50  LOAD_FAST                'line'
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'match'

 L. 715        56  LOAD_FAST                'match'
               58  POP_JUMP_IF_FALSE    40  'to 40'

 L. 716        60  LOAD_GLOBAL              int
               62  LOAD_FAST                'match'
               64  LOAD_METHOD              group
               66  LOAD_CONST               1
               68  CALL_METHOD_1         1  ''
               70  CALL_FUNCTION_1       1  ''
               72  ROT_TWO          
               74  POP_TOP          
               76  POP_BLOCK        
               78  ROT_TWO          
               80  BEGIN_FINALLY    
               82  WITH_CLEANUP_START
               84  WITH_CLEANUP_FINISH
               86  POP_FINALLY           0  ''
               88  RETURN_VALUE     
               90  JUMP_BACK            40  'to 40'
               92  POP_BLOCK        
               94  BEGIN_FINALLY    
             96_0  COME_FROM_WITH       32  '32'
               96  WITH_CLEANUP_START
               98  WITH_CLEANUP_FINISH
              100  END_FINALLY      
            102_0  COME_FROM            22  '22'

 L. 717       102  LOAD_CONST               0
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 76


class EggInfoDeprecationWarning(SetuptoolsDeprecationWarning):
    __doc__ = 'Deprecated behavior warning for EggInfo, bypassing suppression.'