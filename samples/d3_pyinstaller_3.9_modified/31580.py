# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: ctypes\_aix.py
"""
Lib/ctypes.util.find_library() support for AIX
Similar approach as done for Darwin support by using separate files
but unlike Darwin - no extension such as ctypes.macholib.*

dlopen() is an interface to AIX initAndLoad() - primary documentation at:
https://www.ibm.com/support/knowledgecenter/en/ssw_aix_61/com.ibm.aix.basetrf1/dlopen.htm
https://www.ibm.com/support/knowledgecenter/en/ssw_aix_61/com.ibm.aix.basetrf1/load.htm

AIX supports two styles for dlopen(): svr4 (System V Release 4) which is common on posix
platforms, but also a BSD style - aka SVR3.

From AIX 5.3 Difference Addendum (December 2004)
2.9 SVR4 linking affinity
Nowadays, there are two major object file formats used by the operating systems:
XCOFF: The COFF enhanced by IBM and others. The original COFF (Common
Object File Format) was the base of SVR3 and BSD 4.2 systems.
ELF:   Executable and Linking Format that was developed by AT&T and is a
base for SVR4 UNIX.

While the shared library content is identical on AIX - one is located as a filepath name
(svr4 style) and the other is located as a member of an archive (and the archive
is located as a filepath name).

The key difference arises when supporting multiple abi formats (i.e., 32 and 64 bit).
For svr4 either only one ABI is supported, or there are two directories, or there
are different file names. The most common solution for multiple ABI is multiple
directories.

For the XCOFF (aka AIX) style - one directory (one archive file) is sufficient
as multiple shared libraries can be in the archive - even sharing the same name.
In documentation the archive is also referred to as the "base" and the shared
library object is referred to as the "member".

For dlopen() on AIX (read initAndLoad()) the calls are similar.
Default activity occurs when no path information is provided. When path
information is provided dlopen() does not search any other directories.

For SVR4 - the shared library name is the name of the file expected: libFOO.so
For AIX - the shared library is expressed as base(member). The search is for the
base (e.g., libFOO.a) and once the base is found the shared library - identified by
member (e.g., libFOO.so, or shr.o) is located and loaded.

The mode bit RTLD_MEMBER tells initAndLoad() that it needs to use the AIX (SVR3)
naming style.
"""
__author__ = 'Michael Felt <aixtools@felt.demon.nl>'
import re
from os import environ, path
from sys import executable
from ctypes import c_void_p, sizeof
from subprocess import Popen, PIPE, DEVNULL
AIX_ABI = sizeof(c_void_p) * 8
from sys import maxsize

def _last_version(libnames, sep):

    def _num_version--- This code section failed: ---

 L.  64         0  LOAD_FAST                'libname'
                2  LOAD_METHOD              split
                4  LOAD_DEREF               'sep'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'parts'

 L.  65        10  BUILD_LIST_0          0 
               12  STORE_FAST               'nums'

 L.  66        14  SETUP_FINALLY        46  'to 46'
             16_0  COME_FROM            40  '40'

 L.  67        16  LOAD_FAST                'parts'
               18  POP_JUMP_IF_FALSE    42  'to 42'

 L.  68        20  LOAD_FAST                'nums'
               22  LOAD_METHOD              insert
               24  LOAD_CONST               0
               26  LOAD_GLOBAL              int
               28  LOAD_FAST                'parts'
               30  LOAD_METHOD              pop
               32  CALL_METHOD_0         0  ''
               34  CALL_FUNCTION_1       1  ''
               36  CALL_METHOD_2         2  ''
               38  POP_TOP          
               40  JUMP_BACK            16  'to 16'
             42_0  COME_FROM            18  '18'
               42  POP_BLOCK        
               44  JUMP_FORWARD         64  'to 64'
             46_0  COME_FROM_FINALLY    14  '14'

 L.  69        46  DUP_TOP          
               48  LOAD_GLOBAL              ValueError
               50  <121>                62  ''
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L.  70        58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
               62  <48>             
             64_0  COME_FROM            60  '60'
             64_1  COME_FROM            44  '44'

 L.  71        64  LOAD_FAST                'nums'
               66  JUMP_IF_TRUE_OR_POP    72  'to 72'
               68  LOAD_GLOBAL              maxsize
               70  BUILD_LIST_1          1 
             72_0  COME_FROM            66  '66'
               72  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 50

    return max((reversed(libnames)), key=_num_version)


def get_ld_header--- This code section failed: ---

 L.  76         0  LOAD_CONST               None
                2  STORE_FAST               'ld_header'

 L.  77         4  LOAD_FAST                'p'
                6  LOAD_ATTR                stdout
                8  GET_ITER         
             10_0  COME_FROM            52  '52'
             10_1  COME_FROM            36  '36'
             10_2  COME_FROM            28  '28'
               10  FOR_ITER             54  'to 54'
               12  STORE_FAST               'line'

 L.  78        14  LOAD_FAST                'line'
               16  LOAD_METHOD              startswith
               18  LOAD_CONST               ('/', './', '../')
               20  CALL_METHOD_1         1  ''
               22  POP_JUMP_IF_FALSE    30  'to 30'

 L.  79        24  LOAD_FAST                'line'
               26  STORE_FAST               'ld_header'
               28  JUMP_BACK            10  'to 10'
             30_0  COME_FROM            22  '22'

 L.  80        30  LOAD_STR                 'INDEX'
               32  LOAD_FAST                'line'
               34  <118>                 0  ''
               36  POP_JUMP_IF_FALSE_BACK    10  'to 10'

 L.  81        38  LOAD_FAST                'ld_header'
               40  LOAD_METHOD              rstrip
               42  LOAD_STR                 '\n'
               44  CALL_METHOD_1         1  ''
               46  ROT_TWO          
               48  POP_TOP          
               50  RETURN_VALUE     
               52  JUMP_BACK            10  'to 10'
             54_0  COME_FROM            10  '10'

Parse error at or near `<118>' instruction at offset 34


def get_ld_header_info(p):
    info = []
    for line in p.stdout:
        if re.match'[0-9]'line:
            info.appendline
        else:
            break
    else:
        return info


def get_ld_headers--- This code section failed: ---

 L. 107         0  BUILD_LIST_0          0 
                2  STORE_FAST               'ldr_headers'

 L. 108         4  LOAD_GLOBAL              Popen
                6  LOAD_STR                 '/usr/bin/dump'
                8  LOAD_STR                 '-X'
               10  LOAD_GLOBAL              AIX_ABI
               12  FORMAT_VALUE          0  ''
               14  BUILD_STRING_2        2 
               16  LOAD_STR                 '-H'
               18  LOAD_FAST                'file'
               20  BUILD_LIST_4          4 

 L. 109        22  LOAD_CONST               True
               24  LOAD_GLOBAL              PIPE
               26  LOAD_GLOBAL              DEVNULL

 L. 108        28  LOAD_CONST               ('universal_newlines', 'stdout', 'stderr')
               30  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               32  STORE_FAST               'p'
             34_0  COME_FROM            68  '68'
             34_1  COME_FROM            64  '64'

 L. 112        34  LOAD_GLOBAL              get_ld_header
               36  LOAD_FAST                'p'
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'ld_header'

 L. 113        42  LOAD_FAST                'ld_header'
               44  POP_JUMP_IF_FALSE    70  'to 70'

 L. 114        46  LOAD_FAST                'ldr_headers'
               48  LOAD_METHOD              append
               50  LOAD_FAST                'ld_header'
               52  LOAD_GLOBAL              get_ld_header_info
               54  LOAD_FAST                'p'
               56  CALL_FUNCTION_1       1  ''
               58  BUILD_TUPLE_2         2 
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          
               64  JUMP_BACK            34  'to 34'

 L. 116        66  JUMP_FORWARD         70  'to 70'
               68  JUMP_BACK            34  'to 34'
             70_0  COME_FROM            66  '66'
             70_1  COME_FROM            44  '44'

 L. 117        70  LOAD_FAST                'p'
               72  LOAD_ATTR                stdout
               74  LOAD_METHOD              close
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          

 L. 118        80  LOAD_FAST                'p'
               82  LOAD_METHOD              wait
               84  CALL_METHOD_0         0  ''
               86  POP_TOP          

 L. 119        88  LOAD_FAST                'ldr_headers'
               90  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 66


def get_shared--- This code section failed: ---

 L. 128         0  BUILD_LIST_0          0 
                2  STORE_FAST               'shared'

 L. 129         4  LOAD_FAST                'ld_headers'
                6  GET_ITER         
              8_0  COME_FROM            48  '48'
              8_1  COME_FROM            22  '22'
                8  FOR_ITER             50  'to 50'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'line'
               14  STORE_FAST               '_'

 L. 132        16  LOAD_STR                 '['
               18  LOAD_FAST                'line'
               20  <118>                 0  ''
               22  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L. 134        24  LOAD_FAST                'shared'
               26  LOAD_METHOD              append
               28  LOAD_FAST                'line'
               30  LOAD_FAST                'line'
               32  LOAD_METHOD              index
               34  LOAD_STR                 '['
               36  CALL_METHOD_1         1  ''
               38  LOAD_CONST               -1
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
               48  JUMP_BACK             8  'to 8'
             50_0  COME_FROM             8  '8'

 L. 135        50  LOAD_FAST                'shared'
               52  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 20


def get_one_match(expr, lines):
    """
    Must be only one match, otherwise result is None.
    When there is a match, strip leading "[" and trailing "]"
    """
    expr = f"\\[({expr})\\]"
    matches = list(filter(None, (re.searchexprline for line in lines)))
    if len(matches) == 1:
        return matches[0].group1
    return


def get_legacy(members):
    """
    This routine provides historical aka legacy naming schemes started
    in AIX4 shared library support for library members names.
    e.g., in /usr/lib/libc.a the member name shr.o for 32-bit binary and
    shr_64.o for 64-bit binary.
    """
    if AIX_ABI == 64:
        expr = 'shr4?_?64\\.o'
        member = get_one_match(expr, members)
        if member:
            return member
    else:
        for name in ('shr.o', 'shr4.o'):
            member = get_one_match(re.escapename, members)
            if member:
                return member


def get_version(name, members):
    """
    Sort list of members and return highest numbered version - if it exists.
    This function is called when an unversioned libFOO.a(libFOO.so) has
    not been found.

    Versioning for the member name is expected to follow
    GNU LIBTOOL conventions: the highest version (x, then X.y, then X.Y.z)
     * find [libFoo.so.X]
     * find [libFoo.so.X.Y]
     * find [libFoo.so.X.Y.Z]

    Before the GNU convention became the standard scheme regardless of
    binary size AIX packagers used GNU convention "as-is" for 32-bit
    archive members but used an "distinguishing" name for 64-bit members.
    This scheme inserted either 64 or _64 between libFOO and .so
    - generally libFOO_64.so, but occasionally libFOO64.so
    """
    exprs = [
     f"lib{name}\\.so\\.[0-9]+[0-9.]*",
     f"lib{name}_?64\\.so\\.[0-9]+[0-9.]*"]
    for expr in exprs:
        versions = []
        for line in members:
            m = re.searchexprline
            if m:
                versions.appendm.group0
            if versions:
                return _last_version(versions, '.')


def get_member(name, members):
    """
    Return an archive member matching the request in name.
    Name is the library name without any prefix like lib, suffix like .so,
    or version number.
    Given a list of members find and return the most appropriate result
    Priority is given to generic libXXX.so, then a versioned libXXX.so.a.b.c
    and finally, legacy AIX naming scheme.
    """
    expr = f"lib{name}\\.so"
    member = get_one_match(expr, members)
    if member:
        return member
    if AIX_ABI == 64:
        expr = f"lib{name}64\\.so"
        member = get_one_match(expr, members)
    if member:
        return member
    member = get_version(name, members)
    if member:
        return member
    return get_legacy(members)


def get_libpaths--- This code section failed: ---

 L. 250         0  LOAD_GLOBAL              environ
                2  LOAD_METHOD              get
                4  LOAD_STR                 'LD_LIBRARY_PATH'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'libpaths'

 L. 251        10  LOAD_FAST                'libpaths'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'

 L. 252        18  LOAD_GLOBAL              environ
               20  LOAD_METHOD              get
               22  LOAD_STR                 'LIBPATH'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'libpaths'
             28_0  COME_FROM            16  '16'

 L. 253        28  LOAD_FAST                'libpaths'
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    42  'to 42'

 L. 254        36  BUILD_LIST_0          0 
               38  STORE_FAST               'libpaths'
               40  JUMP_FORWARD         52  'to 52'
             42_0  COME_FROM            34  '34'

 L. 256        42  LOAD_FAST                'libpaths'
               44  LOAD_METHOD              split
               46  LOAD_STR                 ':'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'libpaths'
             52_0  COME_FROM            40  '40'

 L. 257        52  LOAD_GLOBAL              get_ld_headers
               54  LOAD_GLOBAL              executable
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'objects'

 L. 258        60  LOAD_FAST                'objects'
               62  GET_ITER         
             64_0  COME_FROM           118  '118'
               64  FOR_ITER            120  'to 120'
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               '_'
               70  STORE_FAST               'lines'

 L. 259        72  LOAD_FAST                'lines'
               74  GET_ITER         
             76_0  COME_FROM           116  '116'
             76_1  COME_FROM            98  '98'
               76  FOR_ITER            118  'to 118'
               78  STORE_FAST               'line'

 L. 261        80  LOAD_FAST                'line'
               82  LOAD_METHOD              split
               84  CALL_METHOD_0         0  ''
               86  LOAD_CONST               1
               88  BINARY_SUBSCR    
               90  STORE_FAST               'path'

 L. 262        92  LOAD_STR                 '/'
               94  LOAD_FAST                'path'
               96  <118>                 0  ''
               98  POP_JUMP_IF_FALSE_BACK    76  'to 76'

 L. 263       100  LOAD_FAST                'libpaths'
              102  LOAD_METHOD              extend
              104  LOAD_FAST                'path'
              106  LOAD_METHOD              split
              108  LOAD_STR                 ':'
              110  CALL_METHOD_1         1  ''
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
              116  JUMP_BACK            76  'to 76'
            118_0  COME_FROM            76  '76'
              118  JUMP_BACK            64  'to 64'
            120_0  COME_FROM            64  '64'

 L. 264       120  LOAD_FAST                'libpaths'
              122  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14


def find_shared(paths, name):
    """
    paths is a list of directories to search for an archive.
    name is the abbreviated name given to find_library().
    Process: search "paths" for archive, and if an archive is found
    return the result of get_member().
    If an archive is not found then return None
    """
    for dir in paths:
        if dir == '/lib':
            pass
        else:
            base = f"lib{name}.a"
            archive = path.joindirbase
            if path.existsarchive:
                members = get_shared(get_ld_headers(archive))
                member = get_member(re.escapename, members)
            if member != None:
                return (base, member)
            return (None, None)
    else:
        return (None, None)


def find_library(name):
    """AIX implementation of ctypes.util.find_library()
    Find an archive member that will dlopen(). If not available,
    also search for a file (or link) with a .so suffix.

    AIX supports two types of schemes that can be used with dlopen().
    The so-called SystemV Release4 (svr4) format is commonly suffixed
    with .so while the (default) AIX scheme has the library (archive)
    ending with the suffix .a
    As an archive has multiple members (e.g., 32-bit and 64-bit) in one file
    the argument passed to dlopen must include both the library and
    the member names in a single string.

    find_library() looks first for an archive (.a) with a suitable member.
    If no archive+member pair is found, look for a .so file.
    """
    libpaths = get_libpaths()
    base, member = find_shared(libpaths, name)
    if base != None:
        return f"{base}({member})"
    soname = f"lib{name}.so"
    for dir in libpaths:
        if dir == '/lib':
            pass
        else:
            shlib = path.joindirsoname
            if path.existsshlib:
                return soname