# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\setuptools\pep425tags.py
"""Generate and work with PEP 425 Compatibility Tags."""
from __future__ import absolute_import
import distutils.util
from distutils import log
import platform, re, sys, sysconfig, warnings
from collections import OrderedDict
from .extern import six
from . import glibc
_osx_arch_pat = re.compile('(.+)_(\\d+)_(\\d+)_(.+)')

def get_config_var--- This code section failed: ---

 L.  23         0  SETUP_FINALLY        14  'to 14'

 L.  24         2  LOAD_GLOBAL              sysconfig
                4  LOAD_METHOD              get_config_var
                6  LOAD_FAST                'var'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  25        14  DUP_TOP          
               16  LOAD_GLOBAL              IOError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    70  'to 70'
               22  POP_TOP          
               24  STORE_FAST               'e'
               26  POP_TOP          
               28  SETUP_FINALLY        58  'to 58'

 L.  26        30  LOAD_GLOBAL              warnings
               32  LOAD_METHOD              warn
               34  LOAD_STR                 '{}'
               36  LOAD_METHOD              format
               38  LOAD_FAST                'e'
               40  CALL_METHOD_1         1  ''
               42  LOAD_GLOBAL              RuntimeWarning
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L.  27        48  POP_BLOCK        
               50  POP_EXCEPT       
               52  CALL_FINALLY         58  'to 58'
               54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'
             58_1  COME_FROM_FINALLY    28  '28'
               58  LOAD_CONST               None
               60  STORE_FAST               'e'
               62  DELETE_FAST              'e'
               64  END_FINALLY      
               66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
             70_0  COME_FROM            20  '20'
               70  END_FINALLY      
             72_0  COME_FROM            68  '68'

Parse error at or near `POP_EXCEPT' instruction at offset 50


def get_abbr_impl():
    """Return abbreviated implementation name."""
    if hasattr(sys, 'pypy_version_info'):
        pyimpl = 'pp'
    elif sys.platform.startswith('java'):
        pyimpl = 'jy'
    elif sys.platform == 'cli':
        pyimpl = 'ip'
    else:
        pyimpl = 'cp'
    return pyimpl


def get_impl_ver():
    """Return implementation version."""
    impl_ver = get_config_var('py_version_nodot')
    if not impl_ver or get_abbr_impl() == 'pp':
        impl_ver = ''.join(map(str, get_impl_version_info()))
    return impl_ver


def get_impl_version_info():
    """Return sys.version_info-like tuple for use in decrementing the minor
    version."""
    if get_abbr_impl() == 'pp':
        return (
         sys.version_info[0], sys.pypy_version_info.major,
         sys.pypy_version_info.minor)
    return (
     sys.version_info[0], sys.version_info[1])


def get_impl_tag():
    """
    Returns the Tag for this specific implementation.
    """
    return '{}{}'.formatget_abbr_impl()get_impl_ver()


def get_flag(var, fallback, expected=True, warn=True):
    """Use a fallback method for determining SOABI flags if the needed config
    var is unset or unavailable."""
    val = get_config_var(var)
    if val is None:
        if warn:
            log.debug"Config variable '%s' is unset, Python ABI tag may be incorrect"var
        return fallback()
    return val == expected


def get_abi_tag():
    """Return the ABI tag based on SOABI (if available) or emulate SOABI
    (CPython 2, PyPy)."""
    soabi = get_config_var('SOABI')
    impl = get_abbr_impl()
    if (soabi or impl) in frozenset({'cp', 'pp'}) and hasattr(sys, 'maxunicode'):
        d = ''
        m = ''
        u = ''
        if get_flag('Py_DEBUG', (lambda: hasattr(sys, 'gettotalrefcount')),
          warn=(impl == 'cp')):
            d = 'd'
        if get_flag('WITH_PYMALLOC', (lambda: impl == 'cp'),
          warn=(impl == 'cp')):
            m = 'm'
        if get_flag('Py_UNICODE_SIZE', (lambda: sys.maxunicode == 1114111),
          expected=4,
          warn=(impl == 'cp' and six.PY2)):
            if six.PY2:
                u = 'u'
        abi = '%s%s%s%s%s' % (impl, get_impl_ver(), d, m, u)
    elif soabi and soabi.startswith('cpython-'):
        abi = 'cp' + soabi.split('-')[1]
    elif soabi:
        abi = soabi.replace'.''_'.replace'-''_'
    else:
        abi = None
    return abi


def _is_running_32bit():
    return sys.maxsize == 2147483647


def get_platform():
    """Return our platform name 'win32', 'linux_x86_64'"""
    if sys.platform == 'darwin':
        release, _, machine = platform.mac_ver()
        split_ver = release.split('.')
        if machine == 'x86_64' and _is_running_32bit():
            machine = 'i386'
        elif machine == 'ppc64':
            if _is_running_32bit():
                machine = 'ppc'
        return 'macosx_{}_{}_{}'.format(split_ver[0], split_ver[1], machine)
    result = distutils.util.get_platform().replace'.''_'.replace'-''_'
    if result == 'linux_x86_64':
        if _is_running_32bit():
            result = 'linux_i686'
    return result


def is_manylinux1_compatible--- This code section failed: ---

 L. 147         0  LOAD_GLOBAL              get_platform
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_CONST               frozenset({'linux_x86_64', 'linux_i686'})
                6  COMPARE_OP               not-in
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 148        10  LOAD_CONST               False
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 151        14  SETUP_FINALLY        36  'to 36'

 L. 152        16  LOAD_CONST               0
               18  LOAD_CONST               None
               20  IMPORT_NAME              _manylinux
               22  STORE_FAST               '_manylinux'

 L. 153        24  LOAD_GLOBAL              bool
               26  LOAD_FAST                '_manylinux'
               28  LOAD_ATTR                manylinux1_compatible
               30  CALL_FUNCTION_1       1  ''
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY    14  '14'

 L. 154        36  DUP_TOP          
               38  LOAD_GLOBAL              ImportError
               40  LOAD_GLOBAL              AttributeError
               42  BUILD_TUPLE_2         2 
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    58  'to 58'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 156        54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            46  '46'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'

 L. 159        60  LOAD_GLOBAL              glibc
               62  LOAD_METHOD              have_compatible_glibc
               64  LOAD_CONST               2
               66  LOAD_CONST               5
               68  CALL_METHOD_2         2  ''
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 58_0


def get_darwin_arches(major, minor, machine):
    """Return a list of supported arches (including group arches) for
    the given major, minor and machine architecture of a macOS machine.
    """
    arches = []

    def _supports_arch(major, minor, arch):
        if arch == 'ppc':
            return (major, minor) <= (10, 5)
        if arch == 'ppc64':
            return (major, minor) == (10, 5)
        if arch == 'i386':
            return (major, minor) >= (10, 4)
        if arch == 'x86_64':
            return (major, minor) >= (10, 5)
        if arch in groups:
            for garch in groups[arch]:
                if _supports_arch(major, minor, garch):
                    return True

            return False

    groups = OrderedDict([
     ('fat', ('i386', 'ppc')),
     ('intel', ('x86_64', 'i386')),
     ('fat64', ('x86_64', 'ppc64')),
     ('fat32', ('x86_64', 'i386', 'ppc'))])
    if _supports_arch(major, minor, machine):
        arches.append(machine)
    for garch in groups:
        if machine in groups[garch]:
            if _supports_arch(major, minor, garch):
                arches.append(garch)
    else:
        arches.append('universal')
        return arches


def get_supported(versions=None, noarch=False, platform=None, impl=None, abi=None):
    """Return a list of supported tags for each version specified in
    `versions`.

    :param versions: a list of string versions, of the form ["33", "32"],
        or None. The first version will be assumed to support our ABI.
    :param platform: specify the exact platform you want valid
        tags for, or None. If None, use the local system platform.
    :param impl: specify the exact implementation you want valid
        tags for, or None. If None, use the local interpreter impl.
    :param abi: specify the exact abi you want valid
        tags for, or None. If None, use the local interpreter abi.
    """
    supported = []
    if versions is None:
        versions = []
        version_info = get_impl_version_info()
        major = version_info[:-1]
        for minor in range(version_info[(-1)], -1, -1):
            versions.append(''.join(map(str, major + (minor,))))
        else:
            impl = impl or get_abbr_impl()
            abis = []
            abi = abi or get_abi_tag()
            if abi:
                abis[0:0] = [
                 abi]

    abi3s = set()
    import imp
    for suffix in imp.get_suffixes():
        if suffix[0].startswith('.abi'):
            abi3s.add(suffix[0].split'.'2[1])
    else:
        abis.extend(sorted(list(abi3s)))
        abis.append('none')
        arch = noarch or platform or get_platform()
        if arch.startswith('macosx'):
            match = _osx_arch_pat.match(arch)
            if match:
                name, major, minor, actual_arch = match.groups()
                tpl = '{}_{}_%i_%s'.formatnamemajor
                arches = []
                for m in reversed(range(int(minor) + 1)):
                    for a in get_darwin_arches(int(major), m, actual_arch):
                        arches.append(tpl % (m, a))

            else:
                arches = [
                 arch]
        elif platform is None and is_manylinux1_compatible():
            arches = [
             arch.replace'linux''manylinux1', arch]
        else:
            arches = [
             arch]

    for abi in abis:
        for arch in arches:
            supported.append(('%s%s' % (impl, versions[0]), abi, arch))

    else:
        for version in versions[1:]:
            if version in frozenset({'31', '30'}):
                break
            else:
                for abi in abi3s:
                    for arch in arches:
                        supported.append(('%s%s' % (impl, version), abi, arch))

        else:
            for arch in arches:
                supported.append(('py%s' % versions[0][0], 'none', arch))
            else:
                supported.append(('%s%s' % (impl, versions[0]), 'none', 'any'))
                supported.append(('%s%s' % (impl, versions[0][0]), 'none', 'any'))
                for i, version in enumerate(versions):
                    supported.append(('py%s' % (version,), 'none', 'any'))
                    if i == 0:
                        supported.append(('py%s' % version[0], 'none', 'any'))
                else:
                    return supported


implementation_tag = get_impl_tag()