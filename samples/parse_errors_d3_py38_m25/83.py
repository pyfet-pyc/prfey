# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: platform.py
""" This module tries to retrieve as much platform-identifying data as
    possible. It makes this information available via function APIs.

    If called from the command line, it prints the platform
    information concatenated as single string to stdout. The output
    format is useable as part of a filename.

"""
__copyright__ = '\n    Copyright (c) 1999-2000, Marc-Andre Lemburg; mailto:mal@lemburg.com\n    Copyright (c) 2000-2010, eGenix.com Software GmbH; mailto:info@egenix.com\n\n    Permission to use, copy, modify, and distribute this software and its\n    documentation for any purpose and without fee or royalty is hereby granted,\n    provided that the above copyright notice appear in all copies and that\n    both that copyright notice and this permission notice appear in\n    supporting documentation or portions thereof, including modifications,\n    that you make.\n\n    EGENIX.COM SOFTWARE GMBH DISCLAIMS ALL WARRANTIES WITH REGARD TO\n    THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND\n    FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,\n    INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING\n    FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,\n    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION\n    WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !\n\n'
__version__ = '1.0.8'
import collections, os, re, sys
_ver_stages = {'dev':10, 
 'alpha':20, 
 'a':20,  'beta':30, 
 'b':30,  'c':40, 
 'RC':50, 
 'rc':50,  'pl':200, 
 'p':200}
_component_re = re.compile('([0-9]+|[._+-])')

def _comparable_version(version):
    result = []
    for v in _component_re.split(version):
        if v not in '._+-':
            try:
                v = int(v, 10)
                t = 100
            except ValueError:
                t = _ver_stages.get(v, 0)
            else:
                result.extend((t, v))
    else:
        return result


_libc_search = re.compile(b'(__libc_init)|(GLIBC_([0-9.]+))|(libc(_\\w+)?\\.so(?:\\.(\\d[0-9.]*))?)', re.ASCII)

def libc_ver(executable=None, lib='', version='', chunksize=16384):
    """ Tries to determine the libc version that the file executable
        (which defaults to the Python interpreter) is linked against.

        Returns a tuple of strings (lib,version) which default to the
        given parameters in case the lookup fails.

        Note that the function has intimate knowledge of how different
        libc versions add symbols to the executable and thus is probably
        only useable for executables compiled using gcc.

        The file is read and scanned in chunks of chunksize bytes.

    """
    if executable is None:
        try:
            ver = os.confstr('CS_GNU_LIBC_VERSION')
            parts = ver.split(maxsplit=1)
            if len(parts) == 2:
                return tuple(parts)
        except (AttributeError, ValueError, OSError):
            pass
        else:
            executable = sys.executable
        V = _comparable_version
        if hasattr(os.path, 'realpath'):
            executable = os.path.realpath(executable)
        with open(executable, 'rb') as f:
            binary = f.read(chunksize)
            pos = 0
            while True:
                if pos < len(binary):
                    if b'libc' in binary or b'GLIBC' in binary:
                        m = _libc_search.search(binary, pos)
                    else:
                        m = None
                    if m:
                        if m.end() == len(binary):
                            chunk = f.read(chunksize)
                            if chunk:
                                binary = binary[max(pos, len(binary) - 1000):] + chunk
                                pos = 0
                        elif not m:
                            pass
                        else:
                            pass
                    libcinit, glibc, glibcversion, so, threads, soversion = [s.decode('latin1') if s is not None else s for s in m.groups()]
                    if libcinit and not lib:
                        lib = 'libc'
                    elif glibc:
                        if lib != 'glibc':
                            lib = 'glibc'
                            version = glibcversion
                        elif V(glibcversion) > V(version):
                            version = glibcversion
                    elif so:
                        if lib != 'glibc':
                            lib = 'libc'
                            if soversion:
                                if not version or V(soversion) > V(version):
                                    version = soversion
                            if threads:
                                if version[-len(threads):] != threads:
                                    version = version + threads
                    pos = m.end()

        return (
         lib, version)


def _norm_version(version, build=''):
    """ Normalize the version and build strings and return a single
        version string using the format major.minor.build (or patchlevel).
    """
    l = version.split('.')
    if build:
        l.append(build)
    try:
        ints = map(int, l)
    except ValueError:
        strings = l
    else:
        strings = list(map(str, ints))
    version = '.'.join(strings[:3])
    return version


_ver_output = re.compile('(?:([\\w ]+) ([\\w.]+) .*\\[.* ([\\d.]+)\\])')

def _syscmd_ver--- This code section failed: ---

 L. 274         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                platform
                4  LOAD_FAST                'supported_platforms'
                6  COMPARE_OP               not-in
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 275        10  LOAD_FAST                'system'
               12  LOAD_FAST                'release'
               14  LOAD_FAST                'version'
               16  BUILD_TUPLE_3         3 
               18  RETURN_VALUE     
             20_0  COME_FROM             8  '8'

 L. 278        20  LOAD_CONST               0
               22  LOAD_CONST               None
               24  IMPORT_NAME              subprocess
               26  STORE_FAST               'subprocess'

 L. 279        28  LOAD_CONST               ('ver', 'command /c ver', 'cmd /c ver')
               30  GET_ITER         
             32_0  COME_FROM           114  '114'
             32_1  COME_FROM           106  '106'
             32_2  COME_FROM            90  '90'
               32  FOR_ITER            116  'to 116'
               34  STORE_FAST               'cmd'

 L. 280        36  SETUP_FINALLY        62  'to 62'

 L. 281        38  LOAD_FAST                'subprocess'
               40  LOAD_ATTR                check_output
               42  LOAD_FAST                'cmd'

 L. 282        44  LOAD_FAST                'subprocess'
               46  LOAD_ATTR                DEVNULL

 L. 283        48  LOAD_CONST               True

 L. 284        50  LOAD_CONST               True

 L. 281        52  LOAD_CONST               ('stderr', 'text', 'shell')
               54  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               56  STORE_FAST               'info'
               58  POP_BLOCK        
               60  JUMP_FORWARD        110  'to 110'
             62_0  COME_FROM_FINALLY    36  '36'

 L. 285        62  DUP_TOP          
               64  LOAD_GLOBAL              OSError
               66  LOAD_FAST                'subprocess'
               68  LOAD_ATTR                CalledProcessError
               70  BUILD_TUPLE_2         2 
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE   108  'to 108'
               76  POP_TOP          
               78  STORE_FAST               'why'
               80  POP_TOP          
               82  SETUP_FINALLY        96  'to 96'

 L. 287        84  POP_BLOCK        
               86  POP_EXCEPT       
               88  CALL_FINALLY         96  'to 96'
               90  JUMP_BACK            32  'to 32'
               92  POP_BLOCK        
               94  BEGIN_FINALLY    
             96_0  COME_FROM            88  '88'
             96_1  COME_FROM_FINALLY    82  '82'
               96  LOAD_CONST               None
               98  STORE_FAST               'why'
              100  DELETE_FAST              'why'
              102  END_FINALLY      
              104  POP_EXCEPT       
              106  JUMP_BACK            32  'to 32'
            108_0  COME_FROM            74  '74'
              108  END_FINALLY      
            110_0  COME_FROM            60  '60'

 L. 289       110  POP_TOP          
              112  BREAK_LOOP          126  'to 126'
              114  JUMP_BACK            32  'to 32'
            116_0  COME_FROM            32  '32'

 L. 291       116  LOAD_FAST                'system'
              118  LOAD_FAST                'release'
              120  LOAD_FAST                'version'
              122  BUILD_TUPLE_3         3 
              124  RETURN_VALUE     
            126_0  COME_FROM           112  '112'

 L. 294       126  LOAD_FAST                'info'
              128  LOAD_METHOD              strip
              130  CALL_METHOD_0         0  ''
              132  STORE_FAST               'info'

 L. 295       134  LOAD_GLOBAL              _ver_output
              136  LOAD_METHOD              match
              138  LOAD_FAST                'info'
              140  CALL_METHOD_1         1  ''
              142  STORE_FAST               'm'

 L. 296       144  LOAD_FAST                'm'
              146  LOAD_CONST               None
              148  COMPARE_OP               is-not
              150  POP_JUMP_IF_FALSE   222  'to 222'

 L. 297       152  LOAD_FAST                'm'
              154  LOAD_METHOD              groups
              156  CALL_METHOD_0         0  ''
              158  UNPACK_SEQUENCE_3     3 
              160  STORE_FAST               'system'
              162  STORE_FAST               'release'
              164  STORE_FAST               'version'

 L. 299       166  LOAD_FAST                'release'
              168  LOAD_CONST               -1
              170  BINARY_SUBSCR    
              172  LOAD_STR                 '.'
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   190  'to 190'

 L. 300       178  LOAD_FAST                'release'
              180  LOAD_CONST               None
              182  LOAD_CONST               -1
              184  BUILD_SLICE_2         2 
              186  BINARY_SUBSCR    
              188  STORE_FAST               'release'
            190_0  COME_FROM           176  '176'

 L. 301       190  LOAD_FAST                'version'
              192  LOAD_CONST               -1
              194  BINARY_SUBSCR    
              196  LOAD_STR                 '.'
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   214  'to 214'

 L. 302       202  LOAD_FAST                'version'
              204  LOAD_CONST               None
              206  LOAD_CONST               -1
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  STORE_FAST               'version'
            214_0  COME_FROM           200  '200'

 L. 305       214  LOAD_GLOBAL              _norm_version
              216  LOAD_FAST                'version'
              218  CALL_FUNCTION_1       1  ''
              220  STORE_FAST               'version'
            222_0  COME_FROM           150  '150'

 L. 306       222  LOAD_FAST                'system'
              224  LOAD_FAST                'release'
              226  LOAD_FAST                'version'
              228  BUILD_TUPLE_3         3 
              230  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 90


_WIN32_CLIENT_RELEASES = {(5, 0):'2000', 
 (5, 1):'XP', 
 (5, 2):'2003Server', 
 (5, None):'post2003', 
 (6, 0):'Vista', 
 (6, 1):'7', 
 (6, 2):'8', 
 (6, 3):'8.1', 
 (6, None):'post8.1', 
 (10, 0):'10', 
 (10, None):'post10'}
_WIN32_SERVER_RELEASES = {(5, 2):'2003Server', 
 (6, 0):'2008Server', 
 (6, 1):'2008ServerR2', 
 (6, 2):'2012Server', 
 (6, 3):'2012ServerR2', 
 (6, None):'post2012ServerR2'}

def win32_is_iot():
    return win32_edition() in ('IoTUAP', 'NanoServer', 'WindowsCoreHeadless', 'IoTEdgeOS')


def win32_edition--- This code section failed: ---

 L. 341         0  SETUP_FINALLY        48  'to 48'

 L. 342         2  SETUP_FINALLY        16  'to 16'

 L. 343         4  LOAD_CONST               0
                6  LOAD_CONST               None
                8  IMPORT_NAME              winreg
               10  STORE_FAST               'winreg'
               12  POP_BLOCK        
               14  JUMP_FORWARD         44  'to 44'
             16_0  COME_FROM_FINALLY     2  '2'

 L. 344        16  DUP_TOP          
               18  LOAD_GLOBAL              ImportError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    42  'to 42'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 345        30  LOAD_CONST               0
               32  LOAD_CONST               None
               34  IMPORT_NAME              _winreg
               36  STORE_FAST               'winreg'
               38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
             42_0  COME_FROM            22  '22'
               42  END_FINALLY      
             44_0  COME_FROM            40  '40'
             44_1  COME_FROM            14  '14'
               44  POP_BLOCK        
               46  JUMP_FORWARD         68  'to 68'
             48_0  COME_FROM_FINALLY     0  '0'

 L. 346        48  DUP_TOP          
               50  LOAD_GLOBAL              ImportError
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    66  'to 66'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L. 347        62  POP_EXCEPT       
               64  JUMP_FORWARD        150  'to 150'
             66_0  COME_FROM            54  '54'
               66  END_FINALLY      
             68_0  COME_FROM            46  '46'

 L. 349        68  SETUP_FINALLY       130  'to 130'

 L. 350        70  LOAD_STR                 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion'
               72  STORE_FAST               'cvkey'

 L. 351        74  LOAD_FAST                'winreg'
               76  LOAD_METHOD              OpenKeyEx
               78  LOAD_FAST                'winreg'
               80  LOAD_ATTR                HKEY_LOCAL_MACHINE
               82  LOAD_FAST                'cvkey'
               84  CALL_METHOD_2         2  ''
               86  SETUP_WITH          120  'to 120'
               88  STORE_FAST               'key'

 L. 352        90  LOAD_FAST                'winreg'
               92  LOAD_METHOD              QueryValueEx
               94  LOAD_FAST                'key'
               96  LOAD_STR                 'EditionId'
               98  CALL_METHOD_2         2  ''
              100  LOAD_CONST               0
              102  BINARY_SUBSCR    
              104  POP_BLOCK        
              106  ROT_TWO          
              108  BEGIN_FINALLY    
              110  WITH_CLEANUP_START
              112  WITH_CLEANUP_FINISH
              114  POP_FINALLY           0  ''
              116  POP_BLOCK        
              118  RETURN_VALUE     
            120_0  COME_FROM_WITH       86  '86'
              120  WITH_CLEANUP_START
              122  WITH_CLEANUP_FINISH
              124  END_FINALLY      
              126  POP_BLOCK        
              128  JUMP_FORWARD        150  'to 150'
            130_0  COME_FROM_FINALLY    68  '68'

 L. 353       130  DUP_TOP          
              132  LOAD_GLOBAL              OSError
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   148  'to 148'
              138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L. 354       144  POP_EXCEPT       
              146  JUMP_FORWARD        150  'to 150'
            148_0  COME_FROM           136  '136'
              148  END_FINALLY      
            150_0  COME_FROM           146  '146'
            150_1  COME_FROM           128  '128'
            150_2  COME_FROM            64  '64'

Parse error at or near `POP_BLOCK' instruction at offset 116


def win32_ver(release='', version='', csd='', ptype=''):
    try:
        from sys import getwindowsversion
    except ImportError:
        return (
         release, version, csd, ptype)
    else:
        winver = getwindowsversion()
        maj, min, build = winver.platform_version or winver[:3]
        version = '{0}.{1}.{2}'.format(maj, min, build)
        release = _WIN32_CLIENT_RELEASES.get((maj, min)) or _WIN32_CLIENT_RELEASES.get((maj, None)) or release
        if winver[:2] == (maj, min):
            try:
                csd = 'SP{}'.format(winver.service_pack_major)
            except AttributeError:
                if csd[:13] == 'Service Pack ':
                    csd = 'SP' + csd[13:]

        if getattr(winver, 'product_type', None) == 3:
            release = _WIN32_SERVER_RELEASES.get((maj, min)) or _WIN32_SERVER_RELEASES.get((maj, None)) or release
        try:
            try:
                import winreg
            except ImportError:
                import _winreg as winreg

        except ImportError:
            pass
        else:
            try:
                cvkey = 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion'
                with winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, cvkey) as key:
                    ptype = winreg.QueryValueEx(key, 'CurrentType')[0]
            except OSError:
                pass
            else:
                return (release, version, csd, ptype)


def _mac_ver_xml():
    fn = '/System/Library/CoreServices/SystemVersion.plist'
    if not os.path.exists(fn):
        return
    try:
        import plistlib
    except ImportError:
        return
    else:
        with open(fn, 'rb') as f:
            pl = plistlib.load(f)
        release = pl['ProductVersion']
        versioninfo = ('', '', '')
        machine = os.uname().machine
        if machine in ('ppc', 'Power Macintosh'):
            machine = 'PowerPC'
        else:
            return (
             release, versioninfo, machine)


def mac_ver(release='', versioninfo=('', '', ''), machine=''):
    """ Get macOS version information and return it as tuple (release,
        versioninfo, machine) with versioninfo being a tuple (version,
        dev_stage, non_release_version).

        Entries which cannot be determined are set to the parameter values
        which default to ''. All tuple entries are strings.
    """
    info = _mac_ver_xml()
    if info is not None:
        return info
    return (
     release, versioninfo, machine)


def _java_getprop(name, default):
    from java.lang import System
    try:
        value = System.getProperty(name)
        if value is None:
            return default
        return value
    except AttributeError:
        return default


def java_ver(release='', vendor='', vminfo=('', '', ''), osinfo=('', '', '')):
    """ Version interface for Jython.

        Returns a tuple (release, vendor, vminfo, osinfo) with vminfo being
        a tuple (vm_name, vm_release, vm_vendor) and osinfo being a
        tuple (os_name, os_version, os_arch).

        Values which cannot be determined are set to the defaults
        given as parameters (which all default to '').

    """
    try:
        import java.lang
    except ImportError:
        return (
         release, vendor, vminfo, osinfo)
    else:
        vendor = _java_getprop('java.vendor', vendor)
        release = _java_getprop('java.version', release)
        vm_name, vm_release, vm_vendor = vminfo
        vm_name = _java_getprop('java.vm.name', vm_name)
        vm_vendor = _java_getprop('java.vm.vendor', vm_vendor)
        vm_release = _java_getprop('java.vm.version', vm_release)
        vminfo = (vm_name, vm_release, vm_vendor)
        os_name, os_version, os_arch = osinfo
        os_arch = _java_getprop('java.os.arch', os_arch)
        os_name = _java_getprop('java.os.name', os_name)
        os_version = _java_getprop('java.os.version', os_version)
        osinfo = (os_name, os_version, os_arch)
        return (
         release, vendor, vminfo, osinfo)


def system_alias(system, release, version):
    """ Returns (system, release, version) aliased to common
        marketing names used for some systems.

        It also does some reordering of the information in some cases
        where it would otherwise cause confusion.

    """
    if system == 'SunOS':
        if release < '5':
            return (
             system, release, version)
        l = release.split('.')
        if l:
            try:
                major = int(l[0])
            except ValueError:
                pass
            else:
                major = major - 3
                l[0] = str(major)
                release = '.'.join(l)
        if release < '6':
            system = 'Solaris'
        else:
            system = 'Solaris'
    elif system == 'IRIX64':
        system = 'IRIX'
        if version:
            version = version + ' (64bit)'
        else:
            version = '64bit'
    elif system in ('win32', 'win16'):
        system = 'Windows'
    return (
     system, release, version)


def _platform(*args):
    """ Helper to format the platform string in a filename
        compatible format e.g. "system-version-machine".
    """
    platform = '-'.join((x.strip() for x in filter(len, args)))
    platform = platform.replace(' ', '_')
    platform = platform.replace('/', '-')
    platform = platform.replace('\\', '-')
    platform = platform.replace(':', '-')
    platform = platform.replace(';', '-')
    platform = platform.replace('"', '-')
    platform = platform.replace('(', '-')
    platform = platform.replace(')', '-')
    platform = platform.replace('unknown', '')
    while True:
        cleaned = platform.replace('--', '-')
        if cleaned == platform:
            pass
        else:
            platform = cleaned

    while True:
        if platform[(-1)] == '-':
            platform = platform[:-1]

    return platform


def _node(default=''):
    """ Helper to determine the node name of this machine.
    """
    try:
        import socket
    except ImportError:
        return default
    else:
        try:
            return socket.gethostname()
        except OSError:
            return default


def _follow_symlinks(filepath):
    """ In case filepath is a symlink, follow it until a
        real file is reached.
    """
    filepath = os.path.abspath(filepath)
    while True:
        if os.path.islink(filepath):
            filepath = os.path.normpath(os.path.join(os.path.dirname(filepath), os.readlink(filepath)))

    return filepath


def _syscmd_uname(option, default=''):
    """ Interface to the system's uname command.
    """
    if sys.platform in ('dos', 'win32', 'win16'):
        return default
    import subprocess
    try:
        output = subprocess.check_output(('uname', option), stderr=(subprocess.DEVNULL),
          text=True)
    except (OSError, subprocess.CalledProcessError):
        return default
    else:
        return output.strip() or default


def _syscmd_file(target, default=''):
    """ Interface to the system's file command.

        The function uses the -b option of the file command to have it
        omit the filename in its output. Follow the symlinks. It returns
        default in case the command should fail.

    """
    if sys.platform in ('dos', 'win32', 'win16'):
        return default
    import subprocess
    target = _follow_symlinks(target)
    env = dict((os.environ), LC_ALL='C')
    try:
        output = subprocess.check_output(['file', '-b', target], stderr=(subprocess.DEVNULL),
          env=env)
    except (OSError, subprocess.CalledProcessError):
        return default
    else:
        if not output:
            return default
        else:
            return output.decode('latin-1')


_default_architecture = {'win32':('', 'WindowsPE'), 
 'win16':('', 'Windows'), 
 'dos':('', 'MSDOS')}

def architecture(executable=sys.executable, bits='', linkage=''):
    """ Queries the given executable (defaults to the Python interpreter
        binary) for various architecture information.

        Returns a tuple (bits, linkage) which contains information about
        the bit architecture and the linkage format used for the
        executable. Both values are returned as strings.

        Values that cannot be determined are returned as given by the
        parameter presets. If bits is given as '', the sizeof(pointer)
        (or sizeof(long) on Python version < 1.5.2) is used as
        indicator for the supported pointer size.

        The function relies on the system's "file" command to do the
        actual work. This is available on most if not all Unix
        platforms. On some non-Unix platforms where the "file" command
        does not exist and the executable is set to the Python interpreter
        binary defaults from _default_architecture are used.

    """
    if not bits:
        import struct
        size = struct.calcsize('P')
        bits = str(size * 8) + 'bit'
    if executable:
        fileout = _syscmd_file(executable, '')
    else:
        fileout = ''
    if not fileout:
        if executable == sys.executable:
            if sys.platform in _default_architecture:
                b, l = _default_architecture[sys.platform]
                if b:
                    bits = b
                if l:
                    linkage = l
            return (
             bits, linkage)
    if 'executable' not in fileout:
        if 'shared object' not in fileout:
            return (
             bits, linkage)
    if '32-bit' in fileout:
        bits = '32bit'
    elif 'N32' in fileout:
        bits = 'n32bit'
    elif '64-bit' in fileout:
        bits = '64bit'
    if 'ELF' in fileout:
        linkage = 'ELF'
    else:
        pass
    if 'PE' in fileout:
        if 'Windows' in fileout:
            linkage = 'WindowsPE'
        else:
            linkage = 'PE'
    elif 'COFF' in fileout:
        linkage = 'COFF'
    elif 'MS-DOS' in fileout:
        linkage = 'MSDOS'
    else:
        pass
    return (bits, linkage)


uname_result = collections.namedtuple('uname_result', 'system node release version machine processor')
_uname_cache = None

def uname():
    """ Fairly portable uname interface. Returns a tuple
        of strings (system, node, release, version, machine, processor)
        identifying the underlying platform.

        Note that unlike the os.uname function this also returns
        possible processor information as an additional tuple entry.

        Entries which cannot be determined are set to ''.

    """
    global _uname_cache
    no_os_uname = 0
    if _uname_cache is not None:
        return _uname_cache
    processor = ''
    try:
        system, node, release, version, machine = os.uname()
    except AttributeError:
        no_os_uname = 1

    if no_os_uname or not list(filter(None, (system, node, release, version, machine))):
        if no_os_uname:
            system = sys.platform
            release = ''
            version = ''
            node = _node()
            machine = ''
        use_syscmd_ver = 1
        if system == 'win32':
            release, version, csd, ptype = win32_ver()
            if release:
                if version:
                    use_syscmd_ver = 0
            if not machine:
                if 'PROCESSOR_ARCHITEW6432' in os.environ:
                    machine = os.environ.get('PROCESSOR_ARCHITEW6432', '')
                else:
                    machine = os.environ.get('PROCESSOR_ARCHITECTURE', '')
            if not processor:
                processor = os.environ.get('PROCESSOR_IDENTIFIER', machine)
            if use_syscmd_ver:
                system, release, version = _syscmd_ver(system)
                if system == 'Microsoft Windows':
                    system = 'Windows'
                elif system == 'Microsoft':
                    if release == 'Windows':
                        system = 'Windows'
                        if '6.0' == version[:3]:
                            release = 'Vista'
                        else:
                            release = ''
        if system in ('win32', 'win16'):
            if not version:
                if system == 'win32':
                    version = '32bit'
                else:
                    version = '16bit'
            system = 'Windows'
    else:
        if system[:4] == 'java':
            release, vendor, vminfo, osinfo = java_ver()
            system = 'Java'
            version = ', '.join(vminfo)
            if not version:
                version = vendor
            if system == 'OpenVMS':
                if not release or release == '0':
                    release = version
                    version = ''
                try:
                    import vms_lib
                except ImportError:
                    pass
                else:
                    csid, cpu_number = vms_lib.getsyi('SYI$_CPU', 0)
                    if cpu_number >= 128:
                        processor = 'Alpha'
                    else:
                        processor = 'VAX'
                if not processor:
                    processor = _syscmd_uname('-p', '')
                if system == 'unknown':
                    system = ''
                if node == 'unknown':
                    node = ''
                if release == 'unknown':
                    release = ''
                if version == 'unknown':
                    version = ''
                if machine == 'unknown':
                    machine = ''
                if processor == 'unknown':
                    processor = ''
                if system == 'Microsoft':
                    if release == 'Windows':
                        system = 'Windows'
                        release = 'Vista'
            _uname_cache = uname_result(system, node, release, version, machine, processor)
            return _uname_cache


def system():
    """ Returns the system/OS name, e.g. 'Linux', 'Windows' or 'Java'.

        An empty string is returned if the value cannot be determined.

    """
    return uname().system


def node():
    """ Returns the computer's network name (which may not be fully
        qualified)

        An empty string is returned if the value cannot be determined.

    """
    return uname().node


def release():
    """ Returns the system's release, e.g. '2.2.0' or 'NT'

        An empty string is returned if the value cannot be determined.

    """
    return uname().release


def version():
    """ Returns the system's release version, e.g. '#3 on degas'

        An empty string is returned if the value cannot be determined.

    """
    return uname().version


def machine():
    """ Returns the machine type, e.g. 'i386'

        An empty string is returned if the value cannot be determined.

    """
    return uname().machine


def processor():
    """ Returns the (true) processor name, e.g. 'amdk6'

        An empty string is returned if the value cannot be
        determined. Note that many platforms do not provide this
        information or simply return the same value as for machine(),
        e.g.  NetBSD does this.

    """
    return uname().processor


_sys_version_parser = re.compile('([\\w.+]+)\\s*\\(#?([^,]+)(?:,\\s*([\\w ]*)(?:,\\s*([\\w :]*))?)?\\)\\s*\\[([^\\]]+)\\]?', re.ASCII)
_ironpython_sys_version_parser = re.compile('IronPython\\s*([\\d\\.]+)(?: \\(([\\d\\.]+)\\))? on (.NET [\\d\\.]+)', re.ASCII)
_ironpython26_sys_version_parser = re.compile('([\\d.]+)\\s*\\(IronPython\\s*[\\d.]+\\s*\\(([\\d.]+)\\) on ([\\w.]+ [\\d.]+(?: \\(\\d+-bit\\))?)\\)')
_pypy_sys_version_parser = re.compile('([\\w.+]+)\\s*\\(#?([^,]+),\\s*([\\w ]+),\\s*([\\w :]+)\\)\\s*\\[PyPy [^\\]]+\\]?')
_sys_version_cache = {}

def _sys_version(sys_version=None):
    """ Returns a parsed version of Python's sys.version as tuple
        (name, version, branch, revision, buildno, builddate, compiler)
        referring to the Python implementation name, version, branch,
        revision, build number, build date/time as string and the compiler
        identification string.

        Note that unlike the Python sys.version, the returned value
        for the Python version will always include the patchlevel (it
        defaults to '.0').

        The function returns empty strings for tuple entries that
        cannot be determined.

        sys_version may be given to parse an alternative version
        string, e.g. if the version was read from a different Python
        interpreter.

    """
    if sys_version is None:
        sys_version = sys.version
    result = _sys_version_cache.get(sys_version, None)
    if result is not None:
        return result
    if 'IronPython' in sys_version:
        name = 'IronPython'
        if sys_version.startswith('IronPython'):
            match = _ironpython_sys_version_parser.match(sys_version)
        else:
            match = _ironpython26_sys_version_parser.match(sys_version)
        if match is None:
            raise ValueError('failed to parse IronPython sys.version: %s' % repr(sys_version))
        version, alt_version, compiler = match.groups()
        buildno = ''
        builddate = ''
    elif sys.platform.startswith('java'):
        name = 'Jython'
        match = _sys_version_parser.match(sys_version)
        if match is None:
            raise ValueError('failed to parse Jython sys.version: %s' % repr(sys_version))
        version, buildno, builddate, buildtime, _ = match.groups()
        if builddate is None:
            builddate = ''
        compiler = sys.platform
    elif 'PyPy' in sys_version:
        name = 'PyPy'
        match = _pypy_sys_version_parser.match(sys_version)
        if match is None:
            raise ValueError('failed to parse PyPy sys.version: %s' % repr(sys_version))
        version, buildno, builddate, buildtime = match.groups()
        compiler = ''
    else:
        match = _sys_version_parser.match(sys_version)
        if match is None:
            raise ValueError('failed to parse CPython sys.version: %s' % repr(sys_version))
        version, buildno, builddate, buildtime, compiler = match.groups()
        name = 'CPython'
        if builddate is None:
            builddate = ''
        elif buildtime:
            builddate = builddate + ' ' + buildtime
    if hasattr(sys, '_git'):
        _, branch, revision = sys._git
    elif hasattr(sys, '_mercurial'):
        _, branch, revision = sys._mercurial
    else:
        branch = ''
        revision = ''
    l = version.split('.')
    if len(l) == 2:
        l.append('0')
        version = '.'.join(l)
    result = (
     name, version, branch, revision, buildno, builddate, compiler)
    _sys_version_cache[sys_version] = result
    return result


def python_implementation():
    """ Returns a string identifying the Python implementation.

        Currently, the following implementations are identified:
          'CPython' (C implementation of Python),
          'IronPython' (.NET implementation of Python),
          'Jython' (Java implementation of Python),
          'PyPy' (Python implementation of Python).

    """
    return _sys_version()[0]


def python_version():
    """ Returns the Python version as string 'major.minor.patchlevel'

        Note that unlike the Python sys.version, the returned value
        will always include the patchlevel (it defaults to 0).

    """
    return _sys_version()[1]


def python_version_tuple():
    """ Returns the Python version as tuple (major, minor, patchlevel)
        of strings.

        Note that unlike the Python sys.version, the returned value
        will always include the patchlevel (it defaults to 0).

    """
    return tuple(_sys_version()[1].split('.'))


def python_branch():
    """ Returns a string identifying the Python implementation
        branch.

        For CPython this is the SCM branch from which the
        Python binary was built.

        If not available, an empty string is returned.

    """
    return _sys_version()[2]


def python_revision():
    """ Returns a string identifying the Python implementation
        revision.

        For CPython this is the SCM revision from which the
        Python binary was built.

        If not available, an empty string is returned.

    """
    return _sys_version()[3]


def python_build():
    """ Returns a tuple (buildno, builddate) stating the Python
        build number and date as strings.

    """
    return _sys_version()[4:6]


def python_compiler():
    """ Returns a string identifying the compiler used for compiling
        Python.

    """
    return _sys_version()[6]


_platform_cache = {}

def platform(aliased=0, terse=0):
    """ Returns a single string identifying the underlying platform
        with as much useful information as possible (but no more :).

        The output is intended to be human readable rather than
        machine parseable. It may look different on different
        platforms and this is intended.

        If "aliased" is true, the function will use aliases for
        various platforms that report system names which differ from
        their common names, e.g. SunOS will be reported as
        Solaris. The system_alias() function is used to implement
        this.

        Setting terse to true causes the function to return only the
        absolute minimum information needed to identify the platform.

    """
    result = _platform_cache.get((aliased, terse), None)
    if result is not None:
        return result
    system, node, release, version, machine, processor = uname()
    if machine == processor:
        processor = ''
    if aliased:
        system, release, version = system_alias(system, release, version)
    if system == 'Darwin':
        macos_release = mac_ver()[0]
        if macos_release:
            system = 'macOS'
            release = macos_release
    if system == 'Windows':
        rel, vers, csd, ptype = win32_ver(version)
        if terse:
            platform = _platform(system, release)
        else:
            platform = _platform(system, release, version, csd)
    elif system in ('Linux', ):
        libcname, libcversion = libc_ver(sys.executable)
        platform = _platform(system, release, machine, processor, 'with', libcname + libcversion)
    elif system == 'Java':
        r, v, vminfo, (os_name, os_version, os_arch) = java_ver()
        if terse or not os_name:
            platform = _platform(system, release, version)
        else:
            platform = _platform(system, release, version, 'on', os_name, os_version, os_arch)
    elif terse:
        platform = _platform(system, release)
    else:
        bits, linkage = architecture(sys.executable)
        platform = _platform(system, release, machine, processor, bits, linkage)
    _platform_cache[(aliased, terse)] = platform
    return platform


if __name__ == '__main__':
    terse = 'terse' in sys.argv or '--terse' in sys.argv
    aliased = 'nonaliased' not in sys.argv and '--nonaliased' not in sys.argv
    print(platform(aliased, terse))
    sys.exit(0)