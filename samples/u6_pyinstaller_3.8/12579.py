# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
        elif version <= 6:
            clibname = 'msvcrt'
        else:
            if version <= 13:
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


else:
    if os.name == 'posix' and sys.platform == 'darwin':
        import ctypes.macholib.dyld as _dyld_find

        def find_library--- This code section failed: ---

 L.  73         0  LOAD_STR                 'lib%s.dylib'
                2  LOAD_FAST                'name'
                4  BINARY_MODULO    

 L.  74         6  LOAD_STR                 '%s.dylib'
                8  LOAD_FAST                'name'
               10  BINARY_MODULO    

 L.  75        12  LOAD_STR                 '%s.framework/%s'
               14  LOAD_FAST                'name'
               16  LOAD_FAST                'name'
               18  BUILD_TUPLE_2         2 
               20  BINARY_MODULO    

 L.  73        22  BUILD_LIST_3          3 
               24  STORE_FAST               'possible'

 L.  76        26  LOAD_FAST                'possible'
               28  GET_ITER         
               30  FOR_ITER             76  'to 76'
               32  STORE_FAST               'name'

 L.  77        34  SETUP_FINALLY        50  'to 50'

 L.  78        36  LOAD_GLOBAL              _dyld_find
               38  LOAD_FAST                'name'
               40  CALL_FUNCTION_1       1  ''
               42  POP_BLOCK        
               44  ROT_TWO          
               46  POP_TOP          
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY    34  '34'

 L.  79        50  DUP_TOP          
               52  LOAD_GLOBAL              ValueError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    72  'to 72'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L.  80        64  POP_EXCEPT       
               66  JUMP_BACK            30  'to 30'
               68  POP_EXCEPT       
               70  JUMP_BACK            30  'to 30'
             72_0  COME_FROM            56  '56'
               72  END_FINALLY      
               74  JUMP_BACK            30  'to 30'

Parse error at or near `ROT_TWO' instruction at offset 44


    else:
        if sys.platform.startswith('aix'):
            from ctypes._aix import find_library
        else:
            if os.name == 'posix':
                import re, tempfile

                def _is_elf--- This code section failed: ---

 L.  98         0  LOAD_CONST               b'\x7fELF'
                2  STORE_FAST               'elf_header'

 L.  99         4  LOAD_GLOBAL              open
                6  LOAD_FAST                'filename'
                8  LOAD_STR                 'br'
               10  CALL_FUNCTION_2       2  ''
               12  SETUP_WITH           42  'to 42'
               14  STORE_FAST               'thefile'

 L. 100        16  LOAD_FAST                'thefile'
               18  LOAD_METHOD              read
               20  LOAD_CONST               4
               22  CALL_METHOD_1         1  ''
               24  LOAD_FAST                'elf_header'
               26  COMPARE_OP               ==
               28  POP_BLOCK        
               30  ROT_TWO          
               32  BEGIN_FINALLY    
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  POP_FINALLY           0  ''
               40  RETURN_VALUE     
             42_0  COME_FROM_WITH       12  '12'
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 30


                def _findLib_gcc--- This code section failed: ---

 L. 107         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              fsencode
                4  LOAD_STR                 '[^\\(\\)\\s]*lib%s\\.[^\\(\\)\\s]*'
                6  LOAD_GLOBAL              re
                8  LOAD_METHOD              escape
               10  LOAD_FAST                'name'
               12  CALL_METHOD_1         1  ''
               14  BINARY_MODULO    
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'expr'

 L. 109        20  LOAD_GLOBAL              shutil
               22  LOAD_METHOD              which
               24  LOAD_STR                 'gcc'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'c_compiler'

 L. 110        30  LOAD_FAST                'c_compiler'
               32  POP_JUMP_IF_TRUE     44  'to 44'

 L. 111        34  LOAD_GLOBAL              shutil
               36  LOAD_METHOD              which
               38  LOAD_STR                 'cc'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'c_compiler'
             44_0  COME_FROM            32  '32'

 L. 112        44  LOAD_FAST                'c_compiler'
               46  POP_JUMP_IF_TRUE     52  'to 52'

 L. 114        48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'

 L. 116        52  LOAD_GLOBAL              tempfile
               54  LOAD_METHOD              NamedTemporaryFile
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               'temp'

 L. 117        60  SETUP_FINALLY       192  'to 192'

 L. 118        62  LOAD_FAST                'c_compiler'
               64  LOAD_STR                 '-Wl,-t'
               66  LOAD_STR                 '-o'
               68  LOAD_FAST                'temp'
               70  LOAD_ATTR                name
               72  LOAD_STR                 '-l'
               74  LOAD_FAST                'name'
               76  BINARY_ADD       
               78  BUILD_LIST_5          5 
               80  STORE_FAST               'args'

 L. 120        82  LOAD_GLOBAL              dict
               84  LOAD_GLOBAL              os
               86  LOAD_ATTR                environ
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'env'

 L. 121        92  LOAD_STR                 'C'
               94  LOAD_FAST                'env'
               96  LOAD_STR                 'LC_ALL'
               98  STORE_SUBSCR     

 L. 122       100  LOAD_STR                 'C'
              102  LOAD_FAST                'env'
              104  LOAD_STR                 'LANG'
              106  STORE_SUBSCR     

 L. 123       108  SETUP_FINALLY       136  'to 136'

 L. 124       110  LOAD_GLOBAL              subprocess
              112  LOAD_ATTR                Popen
              114  LOAD_FAST                'args'

 L. 125       116  LOAD_GLOBAL              subprocess
              118  LOAD_ATTR                PIPE

 L. 126       120  LOAD_GLOBAL              subprocess
              122  LOAD_ATTR                STDOUT

 L. 127       124  LOAD_FAST                'env'

 L. 124       126  LOAD_CONST               ('stdout', 'stderr', 'env')
              128  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              130  STORE_FAST               'proc'
              132  POP_BLOCK        
              134  JUMP_FORWARD        162  'to 162'
            136_0  COME_FROM_FINALLY   108  '108'

 L. 128       136  DUP_TOP          
              138  LOAD_GLOBAL              OSError
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   160  'to 160'
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 129       150  POP_EXCEPT       
              152  POP_BLOCK        
              154  CALL_FINALLY        192  'to 192'
              156  LOAD_CONST               None
              158  RETURN_VALUE     
            160_0  COME_FROM           142  '142'
              160  END_FINALLY      
            162_0  COME_FROM           134  '134'

 L. 130       162  LOAD_FAST                'proc'
              164  SETUP_WITH          182  'to 182'
              166  POP_TOP          

 L. 131       168  LOAD_FAST                'proc'
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

 L. 133       192  SETUP_FINALLY       206  'to 206'

 L. 134       194  LOAD_FAST                'temp'
              196  LOAD_METHOD              close
              198  CALL_METHOD_0         0  ''
              200  POP_TOP          
              202  POP_BLOCK        
              204  JUMP_FORWARD        226  'to 226'
            206_0  COME_FROM_FINALLY   192  '192'

 L. 135       206  DUP_TOP          
              208  LOAD_GLOBAL              FileNotFoundError
              210  COMPARE_OP               exception-match
              212  POP_JUMP_IF_FALSE   224  'to 224'
              214  POP_TOP          
              216  POP_TOP          
              218  POP_TOP          

 L. 138       220  POP_EXCEPT       
              222  JUMP_FORWARD        226  'to 226'
            224_0  COME_FROM           212  '212'
              224  END_FINALLY      
            226_0  COME_FROM           222  '222'
            226_1  COME_FROM           204  '204'
              226  END_FINALLY      

 L. 139       228  LOAD_GLOBAL              re
              230  LOAD_METHOD              findall
              232  LOAD_FAST                'expr'
              234  LOAD_FAST                'trace'
              236  CALL_METHOD_2         2  ''
              238  STORE_FAST               'res'

 L. 140       240  LOAD_FAST                'res'
              242  POP_JUMP_IF_TRUE    248  'to 248'

 L. 141       244  LOAD_CONST               None
              246  RETURN_VALUE     
            248_0  COME_FROM           242  '242'

 L. 143       248  LOAD_FAST                'res'
              250  GET_ITER         
              252  FOR_ITER            284  'to 284'
              254  STORE_FAST               'file'

 L. 147       256  LOAD_GLOBAL              _is_elf
              258  LOAD_FAST                'file'
              260  CALL_FUNCTION_1       1  ''
          262_264  POP_JUMP_IF_TRUE    270  'to 270'

 L. 148   266_268  JUMP_BACK           252  'to 252'
            270_0  COME_FROM           262  '262'

 L. 149       270  LOAD_GLOBAL              os
              272  LOAD_METHOD              fsdecode
              274  LOAD_FAST                'file'
              276  CALL_METHOD_1         1  ''
              278  ROT_TWO          
              280  POP_TOP          
              282  RETURN_VALUE     

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
                            return os.fsdecode(res.group(1))


                else:

                    def _get_soname(f):
                        if not f:
                            return
                        else:
                            objdump = shutil.which('objdump')
                            return objdump or None
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
                            return os.fsdecode(res.group(1))


                if sys.platform.startswith(('freebsd', 'openbsd', 'dragonfly')):

                    def _num_version(libname):
                        parts = libname.split(b'.')
                        nums = []
                        try:
                            while parts:
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


                else:
                    if sys.platform == 'sunos5':

                        def _findLib_crle(name, is64):
                            if not os.path.exists('/usr/bin/crle'):
                                return
                            else:
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
                            return _get_soname(_findLib_crlenameis64 or _findLib_gcc(name))


                    else:

                        def _findSoname_ldconfig--- This code section failed: ---

 L. 271         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              struct
                6  STORE_FAST               'struct'

 L. 272         8  LOAD_FAST                'struct'
               10  LOAD_METHOD              calcsize
               12  LOAD_STR                 'l'
               14  CALL_METHOD_1         1  ''
               16  LOAD_CONST               4
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    38  'to 38'

 L. 273        22  LOAD_GLOBAL              os
               24  LOAD_METHOD              uname
               26  CALL_METHOD_0         0  ''
               28  LOAD_ATTR                machine
               30  LOAD_STR                 '-32'
               32  BINARY_ADD       
               34  STORE_FAST               'machine'
               36  JUMP_FORWARD         52  'to 52'
             38_0  COME_FROM            20  '20'

 L. 275        38  LOAD_GLOBAL              os
               40  LOAD_METHOD              uname
               42  CALL_METHOD_0         0  ''
               44  LOAD_ATTR                machine
               46  LOAD_STR                 '-64'
               48  BINARY_ADD       
               50  STORE_FAST               'machine'
             52_0  COME_FROM            36  '36'

 L. 277        52  LOAD_STR                 'libc6,x86-64'

 L. 278        54  LOAD_STR                 'libc6,64bit'

 L. 279        56  LOAD_STR                 'libc6,64bit'

 L. 280        58  LOAD_STR                 'libc6,64bit'

 L. 281        60  LOAD_STR                 'libc6,IA-64'

 L. 276        62  LOAD_CONST               ('x86_64-64', 'ppc64-64', 'sparc64-64', 's390x-64', 'ia64-64')
               64  BUILD_CONST_KEY_MAP_5     5 
               66  STORE_FAST               'mach_map'

 L. 283        68  LOAD_FAST                'mach_map'
               70  LOAD_METHOD              get
               72  LOAD_FAST                'machine'
               74  LOAD_STR                 'libc6'
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'abi_type'

 L. 286        80  LOAD_STR                 '\\s+(lib%s\\.[^\\s]+)\\s+\\(%s'
               82  STORE_FAST               'regex'

 L. 287        84  LOAD_GLOBAL              os
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

 L. 288       108  SETUP_FINALLY       214  'to 214'

 L. 289       110  LOAD_GLOBAL              subprocess
              112  LOAD_ATTR                Popen
              114  LOAD_STR                 '/sbin/ldconfig'
              116  LOAD_STR                 '-p'
              118  BUILD_LIST_2          2 

 L. 290       120  LOAD_GLOBAL              subprocess
              122  LOAD_ATTR                DEVNULL

 L. 291       124  LOAD_GLOBAL              subprocess
              126  LOAD_ATTR                DEVNULL

 L. 292       128  LOAD_GLOBAL              subprocess
              130  LOAD_ATTR                PIPE

 L. 293       132  LOAD_STR                 'C'
              134  LOAD_STR                 'C'
              136  LOAD_CONST               ('LC_ALL', 'LANG')
              138  BUILD_CONST_KEY_MAP_2     2 

 L. 289       140  LOAD_CONST               ('stdin', 'stderr', 'stdout', 'env')
              142  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              144  SETUP_WITH          204  'to 204'

 L. 293       146  STORE_FAST               'p'

 L. 294       148  LOAD_GLOBAL              re
              150  LOAD_METHOD              search
              152  LOAD_FAST                'regex'
              154  LOAD_FAST                'p'
              156  LOAD_ATTR                stdout
              158  LOAD_METHOD              read
              160  CALL_METHOD_0         0  ''
              162  CALL_METHOD_2         2  ''
              164  STORE_FAST               'res'

 L. 295       166  LOAD_FAST                'res'
              168  POP_JUMP_IF_FALSE   200  'to 200'

 L. 296       170  LOAD_GLOBAL              os
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

 L. 297       214  DUP_TOP          
              216  LOAD_GLOBAL              OSError
              218  COMPARE_OP               exception-match
              220  POP_JUMP_IF_FALSE   232  'to 232'
              222  POP_TOP          
              224  POP_TOP          
              226  POP_TOP          

 L. 298       228  POP_EXCEPT       
              230  JUMP_FORWARD        234  'to 234'
            232_0  COME_FROM           220  '220'
              232  END_FINALLY      
            234_0  COME_FROM           230  '230'
            234_1  COME_FROM           212  '212'

Parse error at or near `ROT_TWO' instruction at offset 186


                        def _findLib_ld--- This code section failed: ---

 L. 302         0  LOAD_STR                 '[^\\(\\)\\s]*lib%s\\.[^\\(\\)\\s]*'
                2  LOAD_GLOBAL              re
                4  LOAD_METHOD              escape
                6  LOAD_FAST                'name'
                8  CALL_METHOD_1         1  ''
               10  BINARY_MODULO    
               12  STORE_FAST               'expr'

 L. 303        14  LOAD_STR                 'ld'
               16  LOAD_STR                 '-t'
               18  BUILD_LIST_2          2 
               20  STORE_FAST               'cmd'

 L. 304        22  LOAD_GLOBAL              os
               24  LOAD_ATTR                environ
               26  LOAD_METHOD              get
               28  LOAD_STR                 'LD_LIBRARY_PATH'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'libpath'

 L. 305        34  LOAD_FAST                'libpath'
               36  POP_JUMP_IF_FALSE    68  'to 68'

 L. 306        38  LOAD_FAST                'libpath'
               40  LOAD_METHOD              split
               42  LOAD_STR                 ':'
               44  CALL_METHOD_1         1  ''
               46  GET_ITER         
               48  FOR_ITER             68  'to 68'
               50  STORE_FAST               'd'

 L. 307        52  LOAD_FAST                'cmd'
               54  LOAD_METHOD              extend
               56  LOAD_STR                 '-L'
               58  LOAD_FAST                'd'
               60  BUILD_LIST_2          2 
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
               66  JUMP_BACK            48  'to 48'
             68_0  COME_FROM            36  '36'

 L. 308        68  LOAD_FAST                'cmd'
               70  LOAD_METHOD              extend
               72  LOAD_STR                 '-o'
               74  LOAD_GLOBAL              os
               76  LOAD_ATTR                devnull
               78  LOAD_STR                 '-l%s'
               80  LOAD_FAST                'name'
               82  BINARY_MODULO    
               84  BUILD_LIST_3          3 
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L. 309        90  LOAD_CONST               None
               92  STORE_FAST               'result'

 L. 310        94  SETUP_FINALLY       186  'to 186'

 L. 311        96  LOAD_GLOBAL              subprocess
               98  LOAD_ATTR                Popen
              100  LOAD_FAST                'cmd'
              102  LOAD_GLOBAL              subprocess
              104  LOAD_ATTR                PIPE

 L. 312       106  LOAD_GLOBAL              subprocess
              108  LOAD_ATTR                PIPE

 L. 313       110  LOAD_CONST               True

 L. 311       112  LOAD_CONST               ('stdout', 'stderr', 'universal_newlines')
              114  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              116  STORE_FAST               'p'

 L. 314       118  LOAD_FAST                'p'
              120  LOAD_METHOD              communicate
              122  CALL_METHOD_0         0  ''
              124  UNPACK_SEQUENCE_2     2 
              126  STORE_FAST               'out'
              128  STORE_FAST               '_'

 L. 315       130  LOAD_GLOBAL              re
              132  LOAD_METHOD              findall
              134  LOAD_FAST                'expr'
              136  LOAD_GLOBAL              os
              138  LOAD_METHOD              fsdecode
              140  LOAD_FAST                'out'
              142  CALL_METHOD_1         1  ''
              144  CALL_METHOD_2         2  ''
              146  STORE_FAST               'res'

 L. 316       148  LOAD_FAST                'res'
              150  GET_ITER         
              152  FOR_ITER            182  'to 182'
              154  STORE_FAST               'file'

 L. 320       156  LOAD_GLOBAL              _is_elf
              158  LOAD_FAST                'file'
              160  CALL_FUNCTION_1       1  ''
              162  POP_JUMP_IF_TRUE    166  'to 166'

 L. 321       164  JUMP_BACK           152  'to 152'
            166_0  COME_FROM           162  '162'

 L. 322       166  LOAD_GLOBAL              os
              168  LOAD_METHOD              fsdecode
              170  LOAD_FAST                'file'
              172  CALL_METHOD_1         1  ''
              174  ROT_TWO          
              176  POP_TOP          
              178  POP_BLOCK        
              180  RETURN_VALUE     
              182  POP_BLOCK        
              184  JUMP_FORWARD        206  'to 206'
            186_0  COME_FROM_FINALLY    94  '94'

 L. 323       186  DUP_TOP          
              188  LOAD_GLOBAL              Exception
              190  COMPARE_OP               exception-match
              192  POP_JUMP_IF_FALSE   204  'to 204'
              194  POP_TOP          
              196  POP_TOP          
              198  POP_TOP          

 L. 324       200  POP_EXCEPT       
              202  JUMP_FORWARD        206  'to 206'
            204_0  COME_FROM           192  '192'
              204  END_FINALLY      
            206_0  COME_FROM           202  '202'
            206_1  COME_FROM           184  '184'

 L. 325       206  LOAD_FAST                'result'
              208  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 178


                        def find_library(name):
                            return _findSoname_ldconfig(name) or _get_soname(_findLib_gcc(name)) or _get_soname(_findLib_ld(name))


            def test():
                from ctypes import cdll
                if os.name == 'nt':
                    print(cdll.msvcrt)
                    print(cdll.load('msvcrt'))
                    print(find_library('msvcrt'))
                elif os.name == 'posix':
                    print(find_library('m'))
                    print(find_library('c'))
                    print(find_library('bz2'))
                    if sys.platform == 'darwin':
                        print(cdll.LoadLibrary('libm.dylib'))
                        print(cdll.LoadLibrary('libcrypto.dylib'))
                        print(cdll.LoadLibrary('libSystem.dylib'))
                        print(cdll.LoadLibrary('System.framework/System'))
                    else:
                        if sys.platform.startswith('aix'):
                            from ctypes import CDLL
                            if sys.maxsize < 4294967296:
                                print(f"Using CDLL(name, os.RTLD_MEMBER): {CDLL'libc.a(shr.o)'os.RTLD_MEMBER}")
                                print(f"Using cdll.LoadLibrary(): {cdll.LoadLibrary('libc.a(shr.o)')}")
                                print(find_library('rpm'))
                                print(cdll.LoadLibrary('librpm.so'))
                            else:
                                print(f"Using CDLL(name, os.RTLD_MEMBER): {CDLL'libc.a(shr_64.o)'os.RTLD_MEMBER}")
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