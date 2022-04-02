# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\_vendor\packaging\tags.py
from __future__ import absolute_import
import distutils.util
try:
    from importlib.machinery import EXTENSION_SUFFIXES
except ImportError:
    import imp
    EXTENSION_SUFFIXES = [x[0] for x in imp.get_suffixes()]
    del imp
else:
    import platform, re, sys, sysconfig, warnings
    INTERPRETER_SHORT_NAMES = {'python':'py', 
     'cpython':'cp', 
     'pypy':'pp', 
     'ironpython':'ip', 
     'jython':'jy'}
    _32_BIT_INTERPRETER = sys.maxsize <= 4294967296

    class Tag(object):
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
            return self.platform == other.platform and self.abi == other.abi and self.interpreter == other.interpreter

        def __hash__(self):
            return hash((self._interpreter, self._abi, self._platform))

        def __str__(self):
            return '{}-{}-{}'.format(self._interpreter, self._abi, self._platform)

        def __repr__(self):
            return '<{self} @ {self_id}>'.format(self=self, self_id=(id(self)))


    def parse_tag(tag):
        tags = set()
        interpreters, abis, platforms = tag.split('-')
        for interpreter in interpreters.split('.'):
            for abi in abis.split('.'):
                for platform_ in platforms.split('.'):
                    tags.add(Tag(interpreter, abi, platform_))

        else:
            return frozenset(tags)


    def _normalize_string(string):
        return string.replace('.', '_').replace('-', '_')


    def _cpython_interpreter(py_version):
        return 'cp{major}{minor}'.format(major=(py_version[0]), minor=(py_version[1]))


    def _cpython_abis(py_version):
        abis = []
        version = ('{}{}'.format)(*py_version[:2])
        debug = pymalloc = ucs4 = ''
        with_debug = sysconfig.get_config_var('Py_DEBUG')
        has_refcount = hasattr(sys, 'gettotalrefcount')
        has_ext = '_d.pyd' in EXTENSION_SUFFIXES
        if not with_debug or with_debug is None:
            if has_refcount or (has_ext):
                debug = 'd'
            if py_version < (3, 8):
                with_pymalloc = sysconfig.get_config_var('WITH_PYMALLOC')
                if with_pymalloc or (with_pymalloc is None):
                    pymalloc = 'm'
                if py_version < (3, 3):
                    unicode_size = sysconfig.get_config_var('Py_UNICODE_SIZE')
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


    def _cpython_tags(py_version, interpreter, abis, platforms):
        for abi in abis:
            for platform_ in platforms:
                yield Tag(interpreter, abi, platform_)

        else:
            for tag in (Tag(interpreter, 'abi3', platform_) for platform_ in platforms):
                yield tag
            else:
                for tag in (Tag(interpreter, 'none', platform_) for platform_ in platforms):
                    yield tag
                else:
                    for minor_version in range(py_version[1] - 1, 1, -1):
                        for platform_ in platforms:
                            interpreter = 'cp{major}{minor}'.format(major=(py_version[0]),
                              minor=minor_version)
                            yield Tag(interpreter, 'abi3', platform_)


    def _pypy_interpreter():
        return 'pp{py_major}{pypy_major}{pypy_minor}'.format(py_major=(sys.version_info[0]),
          pypy_major=(sys.pypy_version_info.major),
          pypy_minor=(sys.pypy_version_info.minor))


    def _generic_abi():
        abi = sysconfig.get_config_var('SOABI')
        if abi:
            return _normalize_string(abi)
        return 'none'


    def _pypy_tags(py_version, interpreter, abi, platforms):
        for tag in (Tag(interpreter, abi, platform) for platform in platforms):
            yield tag
        else:
            for tag in (Tag(interpreter, 'none', platform) for platform in platforms):
                yield tag


    def _generic_tags(interpreter, py_version, abi, platforms):
        for tag in (Tag(interpreter, abi, platform) for platform in platforms):
            yield tag
        else:
            if abi != 'none':
                tags = (Tag(interpreter, 'none', platform_) for platform_ in platforms)
                for tag in tags:
                    yield tag


    def _py_interpreter_range(py_version):
        """
    Yield Python versions in descending order.

    After the latest version, the major-only version will be yielded, and then
    all following versions up to 'end'.
    """
        yield 'py{major}{minor}'.format(major=(py_version[0]), minor=(py_version[1]))
        yield 'py{major}'.format(major=(py_version[0]))
        for minor in range(py_version[1] - 1, -1, -1):
            yield 'py{major}{minor}'.format(major=(py_version[0]), minor=minor)


    def _independent_tags(interpreter, py_version, platforms):
        """
    Return the sequence of tags that are consistent across implementations.

    The tags consist of:
    - py*-none-<platform>
    - <interpreter>-none-any
    - py*-none-any
    """
        for version in _py_interpreter_range(py_version):
            for platform_ in platforms:
                yield Tag(version, 'none', platform_)

        else:
            yield Tag(interpreter, 'none', 'any')
            for version in _py_interpreter_range(py_version):
                yield Tag(version, 'none', 'any')


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
        elif cpu_arch == 'i386':
            if version < (10, 4):
                return []
            formats.extend(['intel', 'fat32', 'fat'])
        elif cpu_arch == 'ppc64':
            if version > (10, 5) or (version < (10, 4)):
                return []
            formats.append('fat64')
        elif cpu_arch == 'ppc':
            if version > (10, 6):
                return []
            formats.extend(['fat32', 'fat'])
        formats.append('universal')
        return formats


    def _mac_platforms(version=None, arch=None):
        version_str, _, cpu_arch = platform.mac_ver()
        if version is None:
            version = tuple(map(int, version_str.split('.')[:2]))
        if arch is None:
            arch = _mac_arch(cpu_arch)
        platforms = []
        for minor_version in range(version[1], -1, -1):
            compat_version = (
             version[0], minor_version)
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                platforms.append('macosx_{major}_{minor}_{binary_format}'.format(major=(compat_version[0]),
                  minor=(compat_version[1]),
                  binary_format=binary_format))

        else:
            return platforms


    def _is_manylinux_compatible--- This code section failed: ---

 L. 267         0  SETUP_FINALLY        30  'to 30'

 L. 268         2  LOAD_CONST               0
                4  LOAD_CONST               None
                6  IMPORT_NAME              _manylinux
                8  STORE_FAST               '_manylinux'

 L. 270        10  LOAD_GLOBAL              bool
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

 L. 271        30  DUP_TOP          
               32  LOAD_GLOBAL              ImportError
               34  LOAD_GLOBAL              AttributeError
               36  BUILD_TUPLE_2         2 
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    52  'to 52'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 273        48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
             52_0  COME_FROM            40  '40'
               52  END_FINALLY      
             54_0  COME_FROM            50  '50'

 L. 275        54  LOAD_GLOBAL              _have_compatible_glibc
               56  LOAD_FAST                'glibc_version'
               58  CALL_FUNCTION_EX      0  'positional arguments only'
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 52_0


    def _glibc_version_string():
        import ctypes
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
            else:
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


    def _linux_platforms--- This code section failed: ---

 L. 334         0  LOAD_GLOBAL              _normalize_string
                2  LOAD_GLOBAL              distutils
                4  LOAD_ATTR                util
                6  LOAD_METHOD              get_platform
                8  CALL_METHOD_0         0  ''
               10  CALL_FUNCTION_1       1  ''
               12  STORE_DEREF              'linux'

 L. 335        14  LOAD_DEREF               'linux'
               16  LOAD_STR                 'linux_x86_64'
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    30  'to 30'
               22  LOAD_FAST                'is_32bit'
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 336        26  LOAD_STR                 'linux_i686'
               28  STORE_DEREF              'linux'
             30_0  COME_FROM            24  '24'
             30_1  COME_FROM            20  '20'

 L. 337        30  LOAD_CONST               (('manylinux2014', (2, 17)), ('manylinux2010', (2, 12)), ('manylinux1', (2, 5)))
               32  STORE_FAST               'manylinux_support'

 L. 342        34  LOAD_GLOBAL              iter
               36  LOAD_FAST                'manylinux_support'
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'manylinux_support_iter'

 L. 343        42  LOAD_FAST                'manylinux_support_iter'
               44  GET_ITER         
             46_0  COME_FROM            82  '82'
             46_1  COME_FROM            62  '62'
               46  FOR_ITER             84  'to 84'
               48  UNPACK_SEQUENCE_2     2 
               50  STORE_FAST               'name'
               52  STORE_FAST               'glibc_version'

 L. 344        54  LOAD_GLOBAL              _is_manylinux_compatible
               56  LOAD_FAST                'name'
               58  LOAD_FAST                'glibc_version'
               60  CALL_FUNCTION_2       2  ''
               62  POP_JUMP_IF_FALSE_BACK    46  'to 46'

 L. 345        64  LOAD_DEREF               'linux'
               66  LOAD_METHOD              replace
               68  LOAD_STR                 'linux'
               70  LOAD_FAST                'name'
               72  CALL_METHOD_2         2  ''
               74  BUILD_LIST_1          1 
               76  STORE_FAST               'platforms'

 L. 346        78  POP_TOP          
               80  BREAK_LOOP           88  'to 88'
               82  JUMP_BACK            46  'to 46'
             84_0  COME_FROM            46  '46'

 L. 348        84  BUILD_LIST_0          0 
               86  STORE_FAST               'platforms'
             88_0  COME_FROM            80  '80'

 L. 350        88  LOAD_FAST                'platforms'
               90  LOAD_CLOSURE             'linux'
               92  BUILD_TUPLE_1         1 
               94  LOAD_LISTCOMP            '<code_object <listcomp>>'
               96  LOAD_STR                 '_linux_platforms.<locals>.<listcomp>'
               98  MAKE_FUNCTION_8          'closure'
              100  LOAD_FAST                'manylinux_support_iter'
              102  GET_ITER         
              104  CALL_FUNCTION_1       1  ''
              106  INPLACE_ADD      
              108  STORE_FAST               'platforms'

 L. 351       110  LOAD_FAST                'platforms'
              112  LOAD_METHOD              append
              114  LOAD_DEREF               'linux'
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          

 L. 352       120  LOAD_FAST                'platforms'
              122  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 122


    def _generic_platforms():
        platform = _normalize_string(distutils.util.get_platform())
        return [
         platform]


    def _interpreter_name():
        name = platform.python_implementation().lower()
        return INTERPRETER_SHORT_NAMES.get(name) or name


    def _generic_interpreter(name, py_version):
        version = sysconfig.get_config_var('py_version_nodot')
        if not version:
            version = ''.join(map(str, py_version[:2]))
        return '{name}{version}'.format(name=name, version=version)


    def sys_tags():
        """
    Returns the sequence of tag triples for the running interpreter.

    The order of the sequence corresponds to priority order for the
    interpreter, from most to least important.
    """
        py_version = sys.version_info[:2]
        interpreter_name = _interpreter_name()
        if platform.system() == 'Darwin':
            platforms = _mac_platforms()
        elif platform.system() == 'Linux':
            platforms = _linux_platforms()
        else:
            platforms = _generic_platforms()
        if interpreter_name == 'cp':
            interpreter = _cpython_interpreter(py_version)
            abis = _cpython_abis(py_version)
            for tag in _cpython_tags(py_version, interpreter, abis, platforms):
                yield tag

        elif interpreter_name == 'pp':
            interpreter = _pypy_interpreter()
            abi = _generic_abi()
            for tag in _pypy_tags(py_version, interpreter, abi, platforms):
                yield tag

        else:
            interpreter = _generic_interpreter(interpreter_name, py_version)
            abi = _generic_abi()
        for tag in _generic_tags(interpreter, py_version, abi, platforms):
            yield tag
        else:
            for tag in _independent_tags(interpreter, py_version, platforms):
                yield tag