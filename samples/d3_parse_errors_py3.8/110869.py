# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: ctypes\util.py
import os, shutil, subprocess, sys
if os.name == 'nt':

    def _get_build_version():
        """Return the version of MSVC that was used to build Python.

        For Python 2.3 and up, the version number is included in
        sys.version.  For earlier versions, assume the compiler is MSVC 6.
        """
        prefix = 'MSC v.'
        i = sys.version.find(prefix)
        if i == -1:
            return 6
        i = i + len(prefix)
        s, rest = sys.version[i:].split(' ', 1)
        majorVersion = int(s[:-2]) - 6
        if majorVersion >= 13:
            majorVersion += 1
        minorVersion = int(s[2:3]) / 10.0
        if majorVersion == 6:
            minorVersion = 0
        if majorVersion >= 6:
            return majorVersion + minorVersion


    def find_msvcrt():
        """Return the name of the VC runtime dll"""
        version = _get_build_version()
        if version is None:
            return
        if version <= 6:
            clibname = 'msvcrt'
        elif version <= 13:
            clibname = 'msvcr%d' % (version * 10)
        else:
            return
        import importlib.machinery
        if '_d.pyd' in importlib.machinery.EXTENSION_SUFFIXES:
            clibname += 'd'
        return clibname + '.dll'


    def find_library(name):
        if name in ('c', 'm'):
            return find_msvcrt()
        for directory in os.environ['PATH'].split(os.pathsep):
            fname = os.path.join(directory, name)
            if os.path.isfile(fname):
                return fname
            if fname.lower().endswith('.dll'):
                pass
            else:
                fname = fname + '.dll'
                if os.path.isfile(fname):
                    return fname


elif os.name == 'posix' and sys.platform == 'darwin':
    import ctypes.macholib.dyld as _dyld_find

    def find_library--- This code section failed: ---

 L.  73         0  LOAD_STR                 '@executable_path/../lib/lib%s.dylib'
                2  LOAD_FAST                'name'
                4  BINARY_MODULO    

 L.  74         6  LOAD_STR                 'lib%s.dylib'
                8  LOAD_FAST                'name'
               10  BINARY_MODULO    

 L.  75        12  LOAD_STR                 '%s.dylib'
               14  LOAD_FAST                'name'
               16  BINARY_MODULO    

 L.  76        18  LOAD_STR                 '%s.framework/%s'
               20  LOAD_FAST                'name'
               22  LOAD_FAST                'name'
               24  BUILD_TUPLE_2         2 
               26  BINARY_MODULO    

 L.  73        28  BUILD_LIST_4          4 
               30  STORE_FAST               'possible'

 L.  77        32  LOAD_FAST                'possible'
               34  GET_ITER         
             36_0  COME_FROM            80  '80'
             36_1  COME_FROM            76  '76'
             36_2  COME_FROM            72  '72'
               36  FOR_ITER             82  'to 82'
               38  STORE_FAST               'name'

 L.  78        40  SETUP_FINALLY        56  'to 56'

 L.  79        42  LOAD_GLOBAL              _dyld_find
               44  LOAD_FAST                'name'
               46  CALL_FUNCTION_1       1  ''
               48  POP_BLOCK        
               50  ROT_TWO          
               52  POP_TOP          
               54  RETURN_VALUE     
             56_0  COME_FROM_FINALLY    40  '40'

 L.  80        56  DUP_TOP          
               58  LOAD_GLOBAL              ValueError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    78  'to 78'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L.  81        70  POP_EXCEPT       
               72  JUMP_BACK            36  'to 36'
               74  POP_EXCEPT       
               76  JUMP_BACK            36  'to 36'
             78_0  COME_FROM            62  '62'
               78  END_FINALLY      
               80  JUMP_BACK            36  'to 36'
             82_0  COME_FROM            36  '36'

Parse error at or near `ROT_TWO' instruction at offset 50


elif sys.platform.startswith('aix'):
    from ctypes._aix import find_library
elif os.name == 'posix':
    import re, tempfile

    def _findLib_gcc--- This code section failed: ---

 L. 102         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              fsencode
                4  LOAD_STR                 '[^\\(\\)\\s]*lib%s\\.[^\\(\\)\\s]*'
                6  LOAD_GLOBAL              re
                8  LOAD_METHOD              escape
               10  LOAD_FAST                'name'
               12  CALL_METHOD_1         1  ''
               14  BINARY_MODULO    
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'expr'

 L. 104        20  LOAD_GLOBAL              shutil
               22  LOAD_METHOD              which
               24  LOAD_STR                 'gcc'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'c_compiler'

 L. 105        30  LOAD_FAST                'c_compiler'
               32  POP_JUMP_IF_TRUE     44  'to 44'

 L. 106        34  LOAD_GLOBAL              shutil
               36  LOAD_METHOD              which
               38  LOAD_STR                 'cc'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'c_compiler'
             44_0  COME_FROM            32  '32'

 L. 107        44  LOAD_FAST                'c_compiler'
               46  POP_JUMP_IF_TRUE     52  'to 52'

 L. 109        48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'

 L. 111        52  LOAD_GLOBAL              tempfile
               54  LOAD_METHOD              NamedTemporaryFile
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               'temp'

 L. 112        60  SETUP_FINALLY       192  'to 192'

 L. 113        62  LOAD_FAST                'c_compiler'
               64  LOAD_STR                 '-Wl,-t'
               66  LOAD_STR                 '-o'
               68  LOAD_FAST                'temp'
               70  LOAD_ATTR                name
               72  LOAD_STR                 '-l'
               74  LOAD_FAST                'name'
               76  BINARY_ADD       
               78  BUILD_LIST_5          5 
               80  STORE_FAST               'args'

 L. 115        82  LOAD_GLOBAL              dict
               84  LOAD_GLOBAL              os
               86  LOAD_ATTR                environ
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'env'

 L. 116        92  LOAD_STR                 'C'
               94  LOAD_FAST                'env'
               96  LOAD_STR                 'LC_ALL'
               98  STORE_SUBSCR     

 L. 117       100  LOAD_STR                 'C'
              102  LOAD_FAST                'env'
              104  LOAD_STR                 'LANG'
              106  STORE_SUBSCR     

 L. 118       108  SETUP_FINALLY       136  'to 136'

 L. 119       110  LOAD_GLOBAL              subprocess
              112  LOAD_ATTR                Popen
              114  LOAD_FAST                'args'

 L. 120       116  LOAD_GLOBAL              subprocess
              118  LOAD_ATTR                PIPE

 L. 121       120  LOAD_GLOBAL              subprocess
              122  LOAD_ATTR                STDOUT

 L. 122       124  LOAD_FAST                'env'

 L. 119       126  LOAD_CONST               ('stdout', 'stderr', 'env')
              128  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              130  STORE_FAST               'proc'
              132  POP_BLOCK        
              134  JUMP_FORWARD        162  'to 162'
            136_0  COME_FROM_FINALLY   108  '108'

 L. 123       136  DUP_TOP          
              138  LOAD_GLOBAL              OSError
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   160  'to 160'
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 124       150  POP_EXCEPT       
              152  POP_BLOCK        
              154  CALL_FINALLY        192  'to 192'
              156  LOAD_CONST               None
              158  RETURN_VALUE     
            160_0  COME_FROM           142  '142'
              160  END_FINALLY      
            162_0  COME_FROM           134  '134'

 L. 125       162  LOAD_FAST                'proc'
              164  SETUP_WITH          182  'to 182'
              166  POP_TOP          

 L. 126       168  LOAD_FAST                'proc'
              170  LOAD_ATTR                stdout
              172  LOAD_METHOD              read
              174  CALL_METHOD_0         0  ''
              176  STORE_FAST               'trace'
              178  POP_BLOCK        
              180  BEGIN_FINALLY    
            182_0  COME_FROM_WITH      164  '164'
              182  WITH_CLEANUP_START
              184  WITH_CLEANUP_FINISH
              186  END_FINALLY      
              188  POP_BLOCK        
              190  BEGIN_FINALLY    
            192_0  COME_FROM           154  '154'
            192_1  COME_FROM_FINALLY    60  '60'

 L. 128       192  SETUP_FINALLY       206  'to 206'

 L. 129       194  LOAD_FAST                'temp'
              196  LOAD_METHOD              close
              198  CALL_METHOD_0         0  ''
              200  POP_TOP          
              202  POP_BLOCK        
              204  JUMP_FORWARD        226  'to 226'
            206_0  COME_FROM_FINALLY   192  '192'

 L. 130       206  DUP_TOP          
              208  LOAD_GLOBAL              FileNotFoundError
              210  COMPARE_OP               exception-match
              212  POP_JUMP_IF_FALSE   224  'to 224'
              214  POP_TOP          
              216  POP_TOP          
              218  POP_TOP          

 L. 133       220  POP_EXCEPT       
              222  JUMP_FORWARD        226  'to 226'
            224_0  COME_FROM           212  '212'
              224  END_FINALLY      
            226_0  COME_FROM           222  '222'
            226_1  COME_FROM           204  '204'
              226  END_FINALLY      

 L. 134       228  LOAD_GLOBAL              re
              230  LOAD_METHOD              search
              232  LOAD_FAST                'expr'
              234  LOAD_FAST                'trace'
              236  CALL_METHOD_2         2  ''
              238  STORE_FAST               'res'

 L. 135       240  LOAD_FAST                'res'
              242  POP_JUMP_IF_TRUE    248  'to 248'

 L. 136       244  LOAD_CONST               None
              246  RETURN_VALUE     
            248_0  COME_FROM           242  '242'

 L. 137       248  LOAD_GLOBAL              os
              250  LOAD_METHOD              fsdecode
              252  LOAD_FAST                'res'
              254  LOAD_METHOD              group
              256  LOAD_CONST               0
              258  CALL_METHOD_1         1  ''
              260  CALL_METHOD_1         1  ''
              262  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 154


    if sys.platform == 'sunos5':

        def _get_soname(f):
            if not f:
                return
            try:
                proc = subprocess.Popen(('/usr/ccs/bin/dump', '-Lpv', f), stdout=(subprocess.PIPE),
                  stderr=(subprocess.DEVNULL))
            except OSError:
                return
            else:
                with proc:
                    data = proc.stdout.read()
                res = re.search(b'\\[.*\\]\\sSONAME\\s+([^\\s]+)', data)
                if not res:
                    return
                else:
                    return os.fsdecode(res.group(1))


    else:

        def _get_soname(f):
            if not f:
                return
            objdump = shutil.which('objdump')
            if not objdump:
                return
            try:
                proc = subprocess.Popen((objdump, '-p', '-j', '.dynamic', f), stdout=(subprocess.PIPE),
                  stderr=(subprocess.DEVNULL))
            except OSError:
                return
            else:
                with proc:
                    dump = proc.stdout.read()
                res = re.search(b'\\sSONAME\\s+([^\\s]+)', dump)
                if not res:
                    return
                else:
                    return os.fsdecode(res.group(1))


    if sys.platform.startswith(('freebsd', 'openbsd', 'dragonfly')):

        def _num_version(libname):
            parts = libname.split(b'.')
            nums = []
            try:
                while True:
                    if parts:
                        nums.insert(0, int(parts.pop()))

            except ValueError:
                pass
            else:
                return nums or [sys.maxsize]


        def find_library(name):
            ename = re.escape(name)
            expr = ':-l%s\\.\\S+ => \\S*/(lib%s\\.\\S+)' % (ename, ename)
            expr = os.fsencode(expr)
            try:
                proc = subprocess.Popen(('/sbin/ldconfig', '-r'), stdout=(subprocess.PIPE),
                  stderr=(subprocess.DEVNULL))
            except OSError:
                data = b''
            else:
                with proc:
                    data = proc.stdout.read()
            res = re.findall(expr, data)
            if not res:
                return _get_soname(_findLib_gcc(name))
            res.sort(key=_num_version)
            return os.fsdecode(res[(-1)])


    elif sys.platform == 'sunos5':

        def _findLib_crle(name, is64):
            if not os.path.exists('/usr/bin/crle'):
                return
            env = dict(os.environ)
            env['LC_ALL'] = 'C'
            if is64:
                args = ('/usr/bin/crle', '-64')
            else:
                args = ('/usr/bin/crle', )
            paths = None
            try:
                proc = subprocess.Popen(args, stdout=(subprocess.PIPE),
                  stderr=(subprocess.DEVNULL),
                  env=env)
            except OSError:
                return
            else:
                with proc:
                    for line in proc.stdout:
                        line = line.strip()
                        if line.startswith(b'Default Library Path (ELF):'):
                            paths = os.fsdecode(line).split()[4]

                if not paths:
                    return
                for dir in paths.split(':'):
                    libfile = os.path.join(dir, 'lib%s.so' % name)
                    if os.path.exists(libfile):
                        return libfile


        def find_library(name, is64=False):
            return _get_soname(_findLib_crle(name, is64) or _findLib_gcc(name))


    else:

        def _findSoname_ldconfig--- This code section failed: ---

 L. 259         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              struct
                6  STORE_FAST               'struct'

 L. 260         8  LOAD_FAST                'struct'
               10  LOAD_METHOD              calcsize
               12  LOAD_STR                 'l'
               14  CALL_METHOD_1         1  ''
               16  LOAD_CONST               4
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    38  'to 38'

 L. 261        22  LOAD_GLOBAL              os
               24  LOAD_METHOD              uname
               26  CALL_METHOD_0         0  ''
               28  LOAD_ATTR                machine
               30  LOAD_STR                 '-32'
               32  BINARY_ADD       
               34  STORE_FAST               'machine'
               36  JUMP_FORWARD         52  'to 52'
             38_0  COME_FROM            20  '20'

 L. 263        38  LOAD_GLOBAL              os
               40  LOAD_METHOD              uname
               42  CALL_METHOD_0         0  ''
               44  LOAD_ATTR                machine
               46  LOAD_STR                 '-64'
               48  BINARY_ADD       
               50  STORE_FAST               'machine'
             52_0  COME_FROM            36  '36'

 L. 265        52  LOAD_STR                 'libc6,x86-64'

 L. 266        54  LOAD_STR                 'libc6,64bit'

 L. 267        56  LOAD_STR                 'libc6,64bit'

 L. 268        58  LOAD_STR                 'libc6,64bit'

 L. 269        60  LOAD_STR                 'libc6,IA-64'

 L. 264        62  LOAD_CONST               ('x86_64-64', 'ppc64-64', 'sparc64-64', 's390x-64', 'ia64-64')
               64  BUILD_CONST_KEY_MAP_5     5 
               66  STORE_FAST               'mach_map'

 L. 271        68  LOAD_FAST                'mach_map'
               70  LOAD_METHOD              get
               72  LOAD_FAST                'machine'
               74  LOAD_STR                 'libc6'
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'abi_type'

 L. 274        80  LOAD_STR                 '\\s+(lib%s\\.[^\\s]+)\\s+\\(%s'
               82  STORE_FAST               'regex'

 L. 275        84  LOAD_GLOBAL              os
               86  LOAD_METHOD              fsencode
               88  LOAD_FAST                'regex'
               90  LOAD_GLOBAL              re
               92  LOAD_METHOD              escape
               94  LOAD_FAST                'name'
               96  CALL_METHOD_1         1  ''
               98  LOAD_FAST                'abi_type'
              100  BUILD_TUPLE_2         2 
              102  BINARY_MODULO    
              104  CALL_METHOD_1         1  ''
              106  STORE_FAST               'regex'

 L. 276       108  SETUP_FINALLY       214  'to 214'

 L. 277       110  LOAD_GLOBAL              subprocess
              112  LOAD_ATTR                Popen
              114  LOAD_STR                 '/sbin/ldconfig'
              116  LOAD_STR                 '-p'
              118  BUILD_LIST_2          2 

 L. 278       120  LOAD_GLOBAL              subprocess
              122  LOAD_ATTR                DEVNULL

 L. 279       124  LOAD_GLOBAL              subprocess
              126  LOAD_ATTR                DEVNULL

 L. 280       128  LOAD_GLOBAL              subprocess
              130  LOAD_ATTR                PIPE

 L. 281       132  LOAD_STR                 'C'
              134  LOAD_STR                 'C'
              136  LOAD_CONST               ('LC_ALL', 'LANG')
              138  BUILD_CONST_KEY_MAP_2     2 

 L. 277       140  LOAD_CONST               ('stdin', 'stderr', 'stdout', 'env')
              142  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              144  SETUP_WITH          204  'to 204'

 L. 281       146  STORE_FAST               'p'

 L. 282       148  LOAD_GLOBAL              re
              150  LOAD_METHOD              search
              152  LOAD_FAST                'regex'
              154  LOAD_FAST                'p'
              156  LOAD_ATTR                stdout
              158  LOAD_METHOD              read
              160  CALL_METHOD_0         0  ''
              162  CALL_METHOD_2         2  ''
              164  STORE_FAST               'res'

 L. 283       166  LOAD_FAST                'res'
              168  POP_JUMP_IF_FALSE   200  'to 200'

 L. 284       170  LOAD_GLOBAL              os
              172  LOAD_METHOD              fsdecode
              174  LOAD_FAST                'res'
              176  LOAD_METHOD              group
              178  LOAD_CONST               1
              180  CALL_METHOD_1         1  ''
              182  CALL_METHOD_1         1  ''
              184  POP_BLOCK        
              186  ROT_TWO          
              188  BEGIN_FINALLY    
              190  WITH_CLEANUP_START
              192  WITH_CLEANUP_FINISH
              194  POP_FINALLY           0  ''
              196  POP_BLOCK        
              198  RETURN_VALUE     
            200_0  COME_FROM           168  '168'
              200  POP_BLOCK        
              202  BEGIN_FINALLY    
            204_0  COME_FROM_WITH      144  '144'
              204  WITH_CLEANUP_START
              206  WITH_CLEANUP_FINISH
              208  END_FINALLY      
              210  POP_BLOCK        
              212  JUMP_FORWARD        234  'to 234'
            214_0  COME_FROM_FINALLY   108  '108'

 L. 285       214  DUP_TOP          
              216  LOAD_GLOBAL              OSError
              218  COMPARE_OP               exception-match
              220  POP_JUMP_IF_FALSE   232  'to 232'
              222  POP_TOP          
              224  POP_TOP          
              226  POP_TOP          

 L. 286       228  POP_EXCEPT       
              230  JUMP_FORWARD        234  'to 234'
            232_0  COME_FROM           220  '220'
              232  END_FINALLY      
            234_0  COME_FROM           230  '230'
            234_1  COME_FROM           212  '212'

Parse error at or near `POP_BLOCK' instruction at offset 196


        def _findLib_ld(name):
            expr = '[^\\(\\)\\s]*lib%s\\.[^\\(\\)\\s]*' % re.escape(name)
            cmd = ['ld', '-t']
            libpath = os.environ.get('LD_LIBRARY_PATH')
            if libpath:
                for d in libpath.split(':'):
                    cmd.extend(['-L', d])

            cmd.extend(['-o', os.devnull, '-l%s' % name])
            result = None
            try:
                p = subprocess.Popen(cmd, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE),
                  universal_newlines=True)
                out, _ = p.communicate()
                res = re.search(expr, os.fsdecode(out))
                if res:
                    result = res.group(0)
            except Exception as e:
                try:
                    pass
                finally:
                    e = None
                    del e

            else:
                return result


        def _findLib_prefix(name):
            if not name:
                return
            for fullname in (
             name, 'lib%s.so' % name):
                path = os.path.join(sys.prefix, 'lib', fullname)
                if os.path.exists(path):
                    return path


        def find_library(name):
            so_name = _get_soname(_findLib_prefix(name)) or name
            if so_name != name:
                return _findLib_prefix(so_name) or _findLib_prefix(name) or _findSoname_ldconfig(name) or _get_soname(_findLib_gcc(name) or _findLib_ld(name))
            return _findLib_prefix(name) or _findSoname_ldconfig(name) or _get_soname(_findLib_gcc(name) or _findLib_ld(name))


def test():
    from ctypes import cdll
    if os.name == 'nt':
        print(cdll.msvcrt)
        print(cdll.load('msvcrt'))
        print(find_library('msvcrt'))
    if os.name == 'posix':
        print(find_library('m'))
        print(find_library('c'))
        print(find_library('bz2'))
        if sys.platform == 'darwin':
            print(cdll.LoadLibrary('libm.dylib'))
            print(cdll.LoadLibrary('libcrypto.dylib'))
            print(cdll.LoadLibrary('libSystem.dylib'))
            print(cdll.LoadLibrary('System.framework/System'))
        elif sys.platform.startswith('aix'):
            from ctypes import CDLL
            if sys.maxsize < 4294967296:
                print(f"Using CDLL(name, os.RTLD_MEMBER): {CDLL('libc.a(shr.o)', os.RTLD_MEMBER)}")
                print(f"Using cdll.LoadLibrary(): {cdll.LoadLibrary('libc.a(shr.o)')}")
                print(find_library('rpm'))
                print(cdll.LoadLibrary('librpm.so'))
            else:
                print(f"Using CDLL(name, os.RTLD_MEMBER): {CDLL('libc.a(shr_64.o)', os.RTLD_MEMBER)}")
                print(f"Using cdll.LoadLibrary(): {cdll.LoadLibrary('libc.a(shr_64.o)')}")
            print(f"crypt\t:: {find_library('crypt')}")
            print(f"crypt\t:: {cdll.LoadLibrary(find_library('crypt'))}")
            print(f"crypto\t:: {find_library('crypto')}")
            print(f"crypto\t:: {cdll.LoadLibrary(find_library('crypto'))}")
        else:
            print(cdll.LoadLibrary('libm.so'))
            print(cdll.LoadLibrary('libcrypt.so'))
            print(find_library('crypt'))


if __name__ == '__main__':
    test()