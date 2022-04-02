# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: pkg_resources\_vendor\packaging\tags.py
from __future__ import absolute_import
import distutils.util
try:
    from importlib.machinery import EXTENSION_SUFFIXES
except ImportError:
    import imp
    EXTENSION_SUFFIXES = [x[0] for x in imp.get_suffixes()]
    del imp
else:
    import logging, os, platform, re, struct, sys, sysconfig, warnings
    from ._typing import TYPE_CHECKING, cast
    if TYPE_CHECKING:
        from typing import Dict, FrozenSet, IO, Iterable, Iterator, List, Optional, Sequence, Tuple, Union
        PythonVersion = Sequence[int]
        MacVersion = Tuple[(int, int)]
        GlibcVersion = Tuple[(int, int)]
    logger = logging.getLogger(__name__)
    INTERPRETER_SHORT_NAMES = {'python':'py', 
     'cpython':'cp', 
     'pypy':'pp', 
     'ironpython':'ip', 
     'jython':'jy'}
    _32_BIT_INTERPRETER = sys.maxsize <= 4294967296

    class Tag(object):
        __doc__ = '\n    A representation of the tag triple for a wheel.\n\n    Instances are considered immutable and thus are hashable. Equality checking\n    is also supported.\n    '
        __slots__ = [
         '_interpreter', '_abi', '_platform']

        def __init__(self, interpreter, abi, platform):
            self._interpreter = interpreter.lower()
            self._abi = abi.lower()
            self._platform = platform.lower()

        @property
        def interpreter(self):
            return self._interpreter

        @property
        def abi(self):
            return self._abi

        @property
        def platform(self):
            return self._platform

        def __eq__(self, other):
            if not isinstance(other, Tag):
                return NotImplemented
            return self.platform == other.platform and self.abi == other.abi and self.interpreter == other.interpreter

        def __hash__(self):
            return hash((self._interpreter, self._abi, self._platform))

        def __str__(self):
            return '{}-{}-{}'.format(self._interpreter, self._abi, self._platform)

        def __repr__(self):
            return '<{self} @ {self_id}>'.format(self=self, self_id=(id(self)))


    def parse_tag(tag):
        """
    Parses the provided tag (e.g. `py3-none-any`) into a frozenset of Tag instances.

    Returning a set is required due to the possibility that the tag is a
    compressed tag set.
    """
        tags = set()
        interpreters, abis, platforms = tag.split('-')
        for interpreter in interpreters.split('.'):
            for abi in abis.split('.'):
                for platform_ in platforms.split('.'):
                    tags.add(Tag(interpreter, abi, platform_))

            else:
                return frozenset(tags)


    def _warn_keyword_parameter(func_name, kwargs):
        """
    Backwards-compatibility with Python 2.7 to allow treating 'warn' as keyword-only.
    """
        if not kwargs:
            return False
        if len(kwargs) > 1 or 'warn' not in kwargs:
            kwargs.pop('warn', None)
            arg = next(iter(kwargs.keys()))
            raise TypeError('{}() got an unexpected keyword argument {!r}'.format(func_name, arg))
        return kwargs['warn']


    def _get_config_var(name, warn=False):
        value = sysconfig.get_config_var(name)
        if value is None:
            if warn:
                logger.debug("Config variable '%s' is unset, Python ABI tag may be incorrect", name)
        return value


    def _normalize_string(string):
        return string.replace('.', '_').replace('-', '_')


    def _abi3_applies(python_version):
        """
    Determine if the Python version supports abi3.

    PEP 384 was first implemented in Python 3.2.
    """
        return len(python_version) > 1 and tuple(python_version) >= (3, 2)


    def _cpython_abis(py_version, warn=False):
        py_version = tuple(py_version)
        abis = []
        version = _version_nodot(py_version[:2])
        debug = pymalloc = ucs4 = ''
        with_debug = _get_config_var('Py_DEBUG', warn)
        has_refcount = hasattr(sys, 'gettotalrefcount')
        has_ext = '_d.pyd' in EXTENSION_SUFFIXES
        if not with_debug:
            if with_debug is None:
                if has_refcount or has_ext:
                    debug = 'd'
            if py_version < (3, 8):
                with_pymalloc = _get_config_var('WITH_PYMALLOC', warn)
                if with_pymalloc or with_pymalloc is None:
                    pymalloc = 'm'
                if py_version < (3, 3):
                    unicode_size = _get_config_var('Py_UNICODE_SIZE', warn)
                    if not unicode_size == 4:
                        if not unicode_size is None or sys.maxunicode == 1114111:
                            ucs4 = 'u'
        elif debug:
            abis.append('cp{version}'.format(version=version))
        abis.insert(0, 'cp{version}{debug}{pymalloc}{ucs4}'.format(version=version,
          debug=debug,
          pymalloc=pymalloc,
          ucs4=ucs4))
        return abis


    def cpython_tags(python_version=None, abis=None, platforms=None, **kwargs):
        """
    Yields the tags for a CPython interpreter.

    The tags consist of:
    - cp<python_version>-<abi>-<platform>
    - cp<python_version>-abi3-<platform>
    - cp<python_version>-none-<platform>
    - cp<less than python_version>-abi3-<platform>  # Older Python versions down to 3.2.

    If python_version only specifies a major version then user-provided ABIs and
    the 'none' ABItag will be used.

    If 'abi3' or 'none' are specified in 'abis' then they will be yielded at
    their normal position and not at the beginning.
    """
        warn = _warn_keyword_parameter('cpython_tags', kwargs)
        if not python_version:
            python_version = sys.version_info[:2]
        else:
            interpreter = 'cp{}'.format(_version_nodot(python_version[:2]))
            if abis is None:
                if len(python_version) > 1:
                    abis = _cpython_abis(python_version, warn)
                else:
                    abis = []
        abis = list(abis)
        for explicit_abi in ('abi3', 'none'):
            try:
                abis.remove(explicit_abi)
            except ValueError:
                pass

        else:
            platforms = list(platforms or _platform_tags())
            for abi in abis:
                for platform_ in platforms:
                    (yield Tag(interpreter, abi, platform_))
                else:
                    if _abi3_applies(python_version):
                        for tag in (Tag(interpreter, 'abi3', platform_) for platform_ in platforms):
                            (yield tag)

        for tag in (Tag(interpreter, 'none', platform_) for platform_ in platforms):
            (yield tag)
        else:
            if _abi3_applies(python_version):
                for minor_version in range(python_version[1] - 1, 1, -1):
                    for platform_ in platforms:
                        interpreter = 'cp{version}'.format(version=(_version_nodot((python_version[0], minor_version))))
                        (yield Tag(interpreter, 'abi3', platform_))


    def _generic_abi():
        abi = sysconfig.get_config_var('SOABI')
        if abi:
            (yield _normalize_string(abi))


    def generic_tags(interpreter=None, abis=None, platforms=None, **kwargs):
        """
    Yields the tags for a generic interpreter.

    The tags consist of:
    - <interpreter>-<abi>-<platform>

    The "none" ABI will be added if it was not explicitly provided.
    """
        warn = _warn_keyword_parameter('generic_tags', kwargs)
        if not interpreter:
            interp_name = interpreter_name()
            interp_version = interpreter_version(warn=warn)
            interpreter = ''.join([interp_name, interp_version])
        if abis is None:
            abis = _generic_abi()
        platforms = list(platforms or _platform_tags())
        abis = list(abis)
        if 'none' not in abis:
            abis.append('none')
        for abi in abis:
            for platform_ in platforms:
                (yield Tag(interpreter, abi, platform_))


    def _py_interpreter_range(py_version):
        """
    Yields Python versions in descending order.

    After the latest version, the major-only version will be yielded, and then
    all previous versions of that major version.
    """
        if len(py_version) > 1:
            (yield 'py{version}'.format(version=(_version_nodot(py_version[:2]))))
        (yield 'py{major}'.format(major=(py_version[0])))
        if len(py_version) > 1:
            for minor in range(py_version[1] - 1, -1, -1):
                (yield 'py{version}'.format(version=(_version_nodot((py_version[0], minor)))))


    def compatible_tags(python_version=None, interpreter=None, platforms=None):
        """
    Yields the sequence of tags that are compatible with a specific version of Python.

    The tags consist of:
    - py*-none-<platform>
    - <interpreter>-none-any  # ... if `interpreter` is provided.
    - py*-none-any
    """
        if not python_version:
            python_version = sys.version_info[:2]
        platforms = list(platforms or _platform_tags())
        for version in _py_interpreter_range(python_version):
            for platform_ in platforms:
                (yield Tag(version, 'none', platform_))

        else:
            if interpreter:
                (yield Tag(interpreter, 'none', 'any'))
            for version in _py_interpreter_range(python_version):
                (yield Tag(version, 'none', 'any'))


    def _mac_arch(arch, is_32bit=_32_BIT_INTERPRETER):
        if not is_32bit:
            return arch
        if arch.startswith('ppc'):
            return 'ppc'
        return 'i386'


    def _mac_binary_formats(version, cpu_arch):
        formats = [
         cpu_arch]
        if cpu_arch == 'x86_64':
            if version < (10, 4):
                return []
            formats.extend(['intel', 'fat64', 'fat32'])
        else:
            if cpu_arch == 'i386':
                if version < (10, 4):
                    return []
                formats.extend(['intel', 'fat32', 'fat'])
            else:
                if cpu_arch == 'ppc64' and not version > (10, 5):
                    if version < (10, 4):
                        return []
                    formats.append('fat64')
                else:
                    if cpu_arch == 'ppc':
                        if version > (10, 6):
                            return []
                        formats.extend(['fat32', 'fat'])
        formats.append('universal')
        return formats


    def mac_platforms(version=None, arch=None):
        """
    Yields the platform tags for a macOS system.

    The `version` parameter is a two-item tuple specifying the macOS version to
    generate platform tags for. The `arch` parameter is the CPU architecture to
    generate platform tags for. Both parameters default to the appropriate value
    for the current system.
    """
        version_str, _, cpu_arch = platform.mac_ver()
        if version is None:
            version = cast('MacVersion', tuple(map(int, version_str.split('.')[:2])))
        else:
            version = version
        if arch is None:
            arch = _mac_arch(cpu_arch)
        else:
            arch = arch
        for minor_version in range(version[1], -1, -1):
            compat_version = (
             version[0], minor_version)
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                (yield 'macosx_{major}_{minor}_{binary_format}'.format(major=(compat_version[0]),
                  minor=(compat_version[1]),
                  binary_format=binary_format))


    def _is_manylinux_compatible--- This code section failed: ---

 L. 423         0  SETUP_FINALLY        30  'to 30'

 L. 424         2  LOAD_CONST               0
                4  LOAD_CONST               None
                6  IMPORT_NAME              _manylinux
                8  STORE_FAST               '_manylinux'

 L. 426        10  LOAD_GLOBAL              bool
               12  LOAD_GLOBAL              getattr
               14  LOAD_FAST                '_manylinux'
               16  LOAD_FAST                'name'
               18  LOAD_STR                 '_compatible'
               20  BINARY_ADD       
               22  CALL_FUNCTION_2       2  ''
               24  CALL_FUNCTION_1       1  ''
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY     0  '0'

 L. 427        30  DUP_TOP          
               32  LOAD_GLOBAL              ImportError
               34  LOAD_GLOBAL              AttributeError
               36  BUILD_TUPLE_2         2 
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    52  'to 52'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 429        48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
             52_0  COME_FROM            40  '40'
               52  END_FINALLY      
             54_0  COME_FROM            50  '50'

 L. 431        54  LOAD_GLOBAL              _have_compatible_glibc
               56  LOAD_FAST                'glibc_version'
               58  CALL_FUNCTION_EX      0  'positional arguments only'
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 44


    def _glibc_version_string():
        return _glibc_version_string_confstr() or _glibc_version_string_ctypes()


    def _glibc_version_string_confstr():
        """
    Primary implementation of glibc_version_string using os.confstr.
    """
        try:
            version_string = os.confstr('CS_GNU_LIBC_VERSION')
            assert version_string is not None
            _, version = version_string.split()
        except (AssertionError, AttributeError, OSError, ValueError):
            return
        else:
            return version


    def _glibc_version_string_ctypes():
        """
    Fallback implementation of glibc_version_string using ctypes.
    """
        try:
            import ctypes
        except ImportError:
            return
        else:
            process_namespace = ctypes.CDLL(None)
            try:
                gnu_get_libc_version = process_namespace.gnu_get_libc_version
            except AttributeError:
                return
            else:
                gnu_get_libc_version.restype = ctypes.c_char_p
                version_str = gnu_get_libc_version()
                if not isinstance(version_str, str):
                    version_str = version_str.decode('ascii')
                return version_str


    def _check_glibc_version(version_str, required_major, minimum_minor):
        m = re.match('(?P<major>[0-9]+)\\.(?P<minor>[0-9]+)', version_str)
        if not m:
            warnings.warn('Expected glibc version with 2 components major.minor, got: %s' % version_str, RuntimeWarning)
            return False
        return int(m.group('major')) == required_major and int(m.group('minor')) >= minimum_minor


    def _have_compatible_glibc(required_major, minimum_minor):
        version_str = _glibc_version_string()
        if version_str is None:
            return False
        return _check_glibc_version(version_str, required_major, minimum_minor)


    class _ELFFileHeader(object):

        class _InvalidELFFileHeader(ValueError):
            __doc__ = '\n        An invalid ELF file header was found.\n        '

        ELF_MAGIC_NUMBER = 2135247942
        ELFCLASS32 = 1
        ELFCLASS64 = 2
        ELFDATA2LSB = 1
        ELFDATA2MSB = 2
        EM_386 = 3
        EM_S390 = 22
        EM_ARM = 40
        EM_X86_64 = 62
        EF_ARM_ABIMASK = 4278190080
        EF_ARM_ABI_VER5 = 83886080
        EF_ARM_ABI_FLOAT_HARD = 1024

        def __init__(self, file):

            def unpack(fmt):
                try:
                    result, = struct.unpack(fmt, file.read(struct.calcsize(fmt)))
                except struct.error:
                    raise _ELFFileHeader._InvalidELFFileHeader()
                else:
                    return result

            self.e_ident_magic = unpack('>I')
            if self.e_ident_magic != self.ELF_MAGIC_NUMBER:
                raise _ELFFileHeader._InvalidELFFileHeader()
            self.e_ident_class = unpack('B')
            if self.e_ident_class not in {self.ELFCLASS32, self.ELFCLASS64}:
                raise _ELFFileHeader._InvalidELFFileHeader()
            self.e_ident_data = unpack('B')
            if self.e_ident_data not in {self.ELFDATA2LSB, self.ELFDATA2MSB}:
                raise _ELFFileHeader._InvalidELFFileHeader()
            self.e_ident_version = unpack('B')
            self.e_ident_osabi = unpack('B')
            self.e_ident_abiversion = unpack('B')
            self.e_ident_pad = file.read(7)
            format_h = '<H' if self.e_ident_data == self.ELFDATA2LSB else '>H'
            format_i = '<I' if self.e_ident_data == self.ELFDATA2LSB else '>I'
            format_q = '<Q' if self.e_ident_data == self.ELFDATA2LSB else '>Q'
            format_p = format_i if self.e_ident_class == self.ELFCLASS32 else format_q
            self.e_type = unpack(format_h)
            self.e_machine = unpack(format_h)
            self.e_version = unpack(format_i)
            self.e_entry = unpack(format_p)
            self.e_phoff = unpack(format_p)
            self.e_shoff = unpack(format_p)
            self.e_flags = unpack(format_i)
            self.e_ehsize = unpack(format_h)
            self.e_phentsize = unpack(format_h)
            self.e_phnum = unpack(format_h)
            self.e_shentsize = unpack(format_h)
            self.e_shnum = unpack(format_h)
            self.e_shstrndx = unpack(format_h)


    def _get_elf_header():
        try:
            with open(sys.executable, 'rb') as (f):
                elf_header = _ELFFileHeader(f)
        except (IOError, OSError, TypeError, _ELFFileHeader._InvalidELFFileHeader):
            return
        else:
            return elf_header


    def _is_linux_armhf():
        elf_header = _get_elf_header()
        if elf_header is None:
            return False
        result = elf_header.e_ident_class == elf_header.ELFCLASS32
        result &= elf_header.e_ident_data == elf_header.ELFDATA2LSB
        result &= elf_header.e_machine == elf_header.EM_ARM
        result &= elf_header.e_flags & elf_header.EF_ARM_ABIMASK == elf_header.EF_ARM_ABI_VER5
        result &= elf_header.e_flags & elf_header.EF_ARM_ABI_FLOAT_HARD == elf_header.EF_ARM_ABI_FLOAT_HARD
        return result


    def _is_linux_i686():
        elf_header = _get_elf_header()
        if elf_header is None:
            return False
        result = elf_header.e_ident_class == elf_header.ELFCLASS32
        result &= elf_header.e_ident_data == elf_header.ELFDATA2LSB
        result &= elf_header.e_machine == elf_header.EM_386
        return result


    def _have_compatible_manylinux_abi(arch):
        if arch == 'armv7l':
            return _is_linux_armhf()
        if arch == 'i686':
            return _is_linux_i686()
        return True


    def _linux_platforms(is_32bit=_32_BIT_INTERPRETER):
        linux = _normalize_string(distutils.util.get_platform())
        if is_32bit:
            if linux == 'linux_x86_64':
                linux = 'linux_i686'
            else:
                if linux == 'linux_aarch64':
                    linux = 'linux_armv7l'
        manylinux_support = []
        _, arch = linux.split('_', 1)
        if _have_compatible_manylinux_abi(arch):
            if arch in {'aarch64', 'x86_64', 'ppc64le', 's390x', 'ppc64', 'i686', 'armv7l'}:
                manylinux_support.append(('manylinux2014', (2, 17)))
            if arch in {'i686', 'x86_64'}:
                manylinux_support.append(('manylinux2010', (2, 12)))
                manylinux_support.append(('manylinux1', (2, 5)))
        manylinux_support_iter = iter(manylinux_support)
        for name, glibc_version in manylinux_support_iter:
            if _is_manylinux_compatible(name, glibc_version):
                (yield linux.replace('linux', name))
                break
            for name, _ in manylinux_support_iter:
                (yield linux.replace('linux', name))
            else:
                (yield linux)


    def _generic_platforms():
        (yield _normalize_string(distutils.util.get_platform()))


    def _platform_tags():
        """
    Provides the platform tags for this installation.
    """
        if platform.system() == 'Darwin':
            return mac_platforms()
        if platform.system() == 'Linux':
            return _linux_platforms()
        return _generic_platforms()


    def interpreter_name():
        """
    Returns the name of the running interpreter.
    """
        try:
            name = sys.implementation.name
        except AttributeError:
            name = platform.python_implementation().lower()
        else:
            return INTERPRETER_SHORT_NAMES.get(name) or name


    def interpreter_version(**kwargs):
        """
    Returns the version of the running interpreter.
    """
        warn = _warn_keyword_parameter('interpreter_version', kwargs)
        version = _get_config_var('py_version_nodot', warn=warn)
        if version:
            version = str(version)
        else:
            version = _version_nodot(sys.version_info[:2])
        return version


    def _version_nodot(version):
        if any((v >= 10 for v in version)):
            sep = '_'
        else:
            sep = ''
        return sep.join(map(str, version))


    def sys_tags(**kwargs):
        """
    Returns the sequence of tag triples for the running interpreter.

    The order of the sequence corresponds to priority order for the
    interpreter, from most to least important.
    """
        warn = _warn_keyword_parameter('sys_tags', kwargs)
        interp_name = interpreter_name()
        if interp_name == 'cp':
            for tag in cpython_tags(warn=warn):
                (yield tag)

        else:
            for tag in generic_tags():
                (yield tag)
            else:
                for tag in compatible_tags():
                    (yield tag)