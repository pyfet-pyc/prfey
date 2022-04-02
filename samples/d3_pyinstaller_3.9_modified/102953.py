# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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


    def find_msvcrt--- This code section failed: ---

 L.  36         0  LOAD_GLOBAL              _get_build_version
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'version'

 L.  37         6  LOAD_FAST                'version'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    18  'to 18'

 L.  39        14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L.  40        18  LOAD_FAST                'version'
               20  LOAD_CONST               6
               22  COMPARE_OP               <=
               24  POP_JUMP_IF_FALSE    32  'to 32'

 L.  41        26  LOAD_STR                 'msvcrt'
               28  STORE_FAST               'clibname'
               30  JUMP_FORWARD         58  'to 58'
             32_0  COME_FROM            24  '24'

 L.  42        32  LOAD_FAST                'version'
               34  LOAD_CONST               13
               36  COMPARE_OP               <=
               38  POP_JUMP_IF_FALSE    54  'to 54'

 L.  43        40  LOAD_STR                 'msvcr%d'
               42  LOAD_FAST                'version'
               44  LOAD_CONST               10
               46  BINARY_MULTIPLY  
               48  BINARY_MODULO    
               50  STORE_FAST               'clibname'
               52  JUMP_FORWARD         58  'to 58'
             54_0  COME_FROM            38  '38'

 L.  47        54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'
             58_1  COME_FROM            30  '30'

 L.  50        58  LOAD_CONST               0
               60  LOAD_CONST               None
               62  IMPORT_NAME_ATTR         importlib.machinery
               64  STORE_FAST               'importlib'

 L.  51        66  LOAD_STR                 '_d.pyd'
               68  LOAD_FAST                'importlib'
               70  LOAD_ATTR                machinery
               72  LOAD_ATTR                EXTENSION_SUFFIXES
               74  <118>                 0  ''
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L.  52        78  LOAD_FAST                'clibname'
               80  LOAD_STR                 'd'
               82  INPLACE_ADD      
               84  STORE_FAST               'clibname'
             86_0  COME_FROM            76  '76'

 L.  53        86  LOAD_FAST                'clibname'
               88  LOAD_STR                 '.dll'
               90  BINARY_ADD       
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10


    def find_library--- This code section failed: ---

 L.  56         0  LOAD_FAST                'name'
                2  LOAD_CONST               ('c', 'm')
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.  57         8  LOAD_GLOBAL              find_msvcrt
               10  CALL_FUNCTION_0       0  ''
               12  RETURN_VALUE     
             14_0  COME_FROM             6  '6'

 L.  59        14  LOAD_GLOBAL              os
               16  LOAD_ATTR                environ
               18  LOAD_STR                 'PATH'
               20  BINARY_SUBSCR    
               22  LOAD_METHOD              split
               24  LOAD_GLOBAL              os
               26  LOAD_ATTR                pathsep
               28  CALL_METHOD_1         1  ''
               30  GET_ITER         
             32_0  COME_FROM           114  '114'
             32_1  COME_FROM           104  '104'
             32_2  COME_FROM            84  '84'
               32  FOR_ITER            116  'to 116'
               34  STORE_FAST               'directory'

 L.  60        36  LOAD_GLOBAL              os
               38  LOAD_ATTR                path
               40  LOAD_METHOD              join
               42  LOAD_FAST                'directory'
               44  LOAD_FAST                'name'
               46  CALL_METHOD_2         2  ''
               48  STORE_FAST               'fname'

 L.  61        50  LOAD_GLOBAL              os
               52  LOAD_ATTR                path
               54  LOAD_METHOD              isfile
               56  LOAD_FAST                'fname'
               58  CALL_METHOD_1         1  ''
               60  POP_JUMP_IF_FALSE    70  'to 70'

 L.  62        62  LOAD_FAST                'fname'
               64  ROT_TWO          
               66  POP_TOP          
               68  RETURN_VALUE     
             70_0  COME_FROM            60  '60'

 L.  63        70  LOAD_FAST                'fname'
               72  LOAD_METHOD              lower
               74  CALL_METHOD_0         0  ''
               76  LOAD_METHOD              endswith
               78  LOAD_STR                 '.dll'
               80  CALL_METHOD_1         1  ''
               82  POP_JUMP_IF_FALSE    86  'to 86'

 L.  64        84  JUMP_BACK            32  'to 32'
             86_0  COME_FROM            82  '82'

 L.  65        86  LOAD_FAST                'fname'
               88  LOAD_STR                 '.dll'
               90  BINARY_ADD       
               92  STORE_FAST               'fname'

 L.  66        94  LOAD_GLOBAL              os
               96  LOAD_ATTR                path
               98  LOAD_METHOD              isfile
              100  LOAD_FAST                'fname'
              102  CALL_METHOD_1         1  ''
              104  POP_JUMP_IF_FALSE_BACK    32  'to 32'

 L.  67       106  LOAD_FAST                'fname'
              108  ROT_TWO          
              110  POP_TOP          
              112  RETURN_VALUE     
              114  JUMP_BACK            32  'to 32'
            116_0  COME_FROM            32  '32'

Parse error at or near `None' instruction at offset -1


elif os.name == 'posix' and sys.platform == 'darwin':
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
             30_0  COME_FROM            72  '72'
             30_1  COME_FROM            68  '68'
             30_2  COME_FROM            64  '64'
               30  FOR_ITER             74  'to 74'
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
               54  <121>                70  ''
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.  80        62  POP_EXCEPT       
               64  JUMP_BACK            30  'to 30'
               66  POP_EXCEPT       
               68  JUMP_BACK            30  'to 30'
               70  <48>             
               72  JUMP_BACK            30  'to 30'
             74_0  COME_FROM            30  '30'

Parse error at or near `ROT_TWO' instruction at offset 44


elif sys.platform.startswith('aix'):
    from ctypes._aix import find_library
elif os.name == 'posix':
    import re, tempfile

    def _findLib_gcc--- This code section failed: ---

 L. 101         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              fsencode
                4  LOAD_STR                 '[^\\(\\)\\s]*lib%s\\.[^\\(\\)\\s]*'
                6  LOAD_GLOBAL              re
                8  LOAD_METHOD              escape
               10  LOAD_FAST                'name'
               12  CALL_METHOD_1         1  ''
               14  BINARY_MODULO    
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'expr'

 L. 103        20  LOAD_GLOBAL              shutil
               22  LOAD_METHOD              which
               24  LOAD_STR                 'gcc'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'c_compiler'

 L. 104        30  LOAD_FAST                'c_compiler'
               32  POP_JUMP_IF_TRUE     44  'to 44'

 L. 105        34  LOAD_GLOBAL              shutil
               36  LOAD_METHOD              which
               38  LOAD_STR                 'cc'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'c_compiler'
             44_0  COME_FROM            32  '32'

 L. 106        44  LOAD_FAST                'c_compiler'
               46  POP_JUMP_IF_TRUE     52  'to 52'

 L. 108        48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'

 L. 110        52  LOAD_GLOBAL              tempfile
               54  LOAD_METHOD              NamedTemporaryFile
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               'temp'

 L. 111        60  SETUP_FINALLY       274  'to 274'

 L. 112        62  LOAD_FAST                'c_compiler'
               64  LOAD_STR                 '-Wl,-t'
               66  LOAD_STR                 '-o'
               68  LOAD_FAST                'temp'
               70  LOAD_ATTR                name
               72  LOAD_STR                 '-l'
               74  LOAD_FAST                'name'
               76  BINARY_ADD       
               78  BUILD_LIST_5          5 
               80  STORE_FAST               'args'

 L. 114        82  LOAD_GLOBAL              dict
               84  LOAD_GLOBAL              os
               86  LOAD_ATTR                environ
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'env'

 L. 115        92  LOAD_STR                 'C'
               94  LOAD_FAST                'env'
               96  LOAD_STR                 'LC_ALL'
               98  STORE_SUBSCR     

 L. 116       100  LOAD_STR                 'C'
              102  LOAD_FAST                'env'
              104  LOAD_STR                 'LANG'
              106  STORE_SUBSCR     

 L. 117       108  SETUP_FINALLY       136  'to 136'

 L. 118       110  LOAD_GLOBAL              subprocess
              112  LOAD_ATTR                Popen
              114  LOAD_FAST                'args'

 L. 119       116  LOAD_GLOBAL              subprocess
              118  LOAD_ATTR                PIPE

 L. 120       120  LOAD_GLOBAL              subprocess
              122  LOAD_ATTR                STDOUT

 L. 121       124  LOAD_FAST                'env'

 L. 118       126  LOAD_CONST               ('stdout', 'stderr', 'env')
              128  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              130  STORE_FAST               'proc'
              132  POP_BLOCK        
              134  JUMP_FORWARD        190  'to 190'
            136_0  COME_FROM_FINALLY   108  '108'

 L. 122       136  DUP_TOP          
              138  LOAD_GLOBAL              OSError
              140  <121>               188  ''
              142  POP_TOP          
              144  POP_TOP          
              146  POP_TOP          

 L. 123       148  POP_EXCEPT       
              150  POP_BLOCK        

 L. 127       152  SETUP_FINALLY       166  'to 166'

 L. 128       154  LOAD_FAST                'temp'
              156  LOAD_METHOD              close
              158  CALL_METHOD_0         0  ''
              160  POP_TOP          
              162  POP_BLOCK        
              164  JUMP_FORWARD        184  'to 184'
            166_0  COME_FROM_FINALLY   152  '152'

 L. 129       166  DUP_TOP          
              168  LOAD_GLOBAL              FileNotFoundError
              170  <121>               182  ''
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L. 132       178  POP_EXCEPT       
              180  JUMP_FORWARD        184  'to 184'
              182  <48>             
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM           164  '164'

 L. 123       184  LOAD_CONST               None
              186  RETURN_VALUE     
              188  <48>             
            190_0  COME_FROM           134  '134'

 L. 124       190  LOAD_FAST                'proc'
              192  SETUP_WITH          220  'to 220'
              194  POP_TOP          

 L. 125       196  LOAD_FAST                'proc'
              198  LOAD_ATTR                stdout
              200  LOAD_METHOD              read
              202  CALL_METHOD_0         0  ''
              204  STORE_FAST               'trace'
              206  POP_BLOCK        
              208  LOAD_CONST               None
              210  DUP_TOP          
              212  DUP_TOP          
              214  CALL_FUNCTION_3       3  ''
              216  POP_TOP          
              218  JUMP_FORWARD        236  'to 236'
            220_0  COME_FROM_WITH      192  '192'
              220  <49>             
              222  POP_JUMP_IF_TRUE    226  'to 226'
              224  <48>             
            226_0  COME_FROM           222  '222'
              226  POP_TOP          
              228  POP_TOP          
              230  POP_TOP          
              232  POP_EXCEPT       
              234  POP_TOP          
            236_0  COME_FROM           218  '218'
              236  POP_BLOCK        

 L. 127       238  SETUP_FINALLY       252  'to 252'

 L. 128       240  LOAD_FAST                'temp'
              242  LOAD_METHOD              close
              244  CALL_METHOD_0         0  ''
              246  POP_TOP          
              248  POP_BLOCK        
              250  JUMP_FORWARD        272  'to 272'
            252_0  COME_FROM_FINALLY   238  '238'

 L. 129       252  DUP_TOP          
              254  LOAD_GLOBAL              FileNotFoundError
          256_258  <121>               270  ''
              260  POP_TOP          
              262  POP_TOP          
              264  POP_TOP          

 L. 132       266  POP_EXCEPT       
              268  JUMP_FORWARD        272  'to 272'
              270  <48>             
            272_0  COME_FROM           268  '268'
            272_1  COME_FROM           250  '250'
              272  JUMP_FORWARD        310  'to 310'
            274_0  COME_FROM_FINALLY    60  '60'

 L. 127       274  SETUP_FINALLY       288  'to 288'

 L. 128       276  LOAD_FAST                'temp'
              278  LOAD_METHOD              close
              280  CALL_METHOD_0         0  ''
              282  POP_TOP          
              284  POP_BLOCK        
              286  JUMP_FORWARD        308  'to 308'
            288_0  COME_FROM_FINALLY   274  '274'

 L. 129       288  DUP_TOP          
              290  LOAD_GLOBAL              FileNotFoundError
          292_294  <121>               306  ''
              296  POP_TOP          
              298  POP_TOP          
              300  POP_TOP          

 L. 132       302  POP_EXCEPT       
              304  JUMP_FORWARD        308  'to 308'
              306  <48>             
            308_0  COME_FROM           304  '304'
            308_1  COME_FROM           286  '286'
              308  <48>             
            310_0  COME_FROM           272  '272'

 L. 133       310  LOAD_GLOBAL              re
              312  LOAD_METHOD              search
              314  LOAD_FAST                'expr'
              316  LOAD_FAST                'trace'
              318  CALL_METHOD_2         2  ''
              320  STORE_FAST               'res'

 L. 134       322  LOAD_FAST                'res'
          324_326  POP_JUMP_IF_TRUE    332  'to 332'

 L. 135       328  LOAD_CONST               None
              330  RETURN_VALUE     
            332_0  COME_FROM           324  '324'

 L. 136       332  LOAD_GLOBAL              os
              334  LOAD_METHOD              fsdecode
              336  LOAD_FAST                'res'
              338  LOAD_METHOD              group
              340  LOAD_CONST               0
              342  CALL_METHOD_1         1  ''
              344  CALL_METHOD_1         1  ''
              346  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 140


    if sys.platform == 'sunos5':

        def _get_soname--- This code section failed: ---

 L. 142         0  LOAD_FAST                'f'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 143         4  LOAD_CONST               None
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 145         8  SETUP_FINALLY        40  'to 40'

 L. 146        10  LOAD_GLOBAL              subprocess
               12  LOAD_ATTR                Popen
               14  LOAD_STR                 '/usr/ccs/bin/dump'
               16  LOAD_STR                 '-Lpv'
               18  LOAD_FAST                'f'
               20  BUILD_TUPLE_3         3 

 L. 147        22  LOAD_GLOBAL              subprocess
               24  LOAD_ATTR                PIPE

 L. 148        26  LOAD_GLOBAL              subprocess
               28  LOAD_ATTR                DEVNULL

 L. 146        30  LOAD_CONST               ('stdout', 'stderr')
               32  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               34  STORE_FAST               'proc'
               36  POP_BLOCK        
               38  JUMP_FORWARD         60  'to 60'
             40_0  COME_FROM_FINALLY     8  '8'

 L. 149        40  DUP_TOP          
               42  LOAD_GLOBAL              OSError
               44  <121>                58  ''
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 150        52  POP_EXCEPT       
               54  LOAD_CONST               None
               56  RETURN_VALUE     
               58  <48>             
             60_0  COME_FROM            38  '38'

 L. 151        60  LOAD_FAST                'proc'
               62  SETUP_WITH           90  'to 90'
               64  POP_TOP          

 L. 152        66  LOAD_FAST                'proc'
               68  LOAD_ATTR                stdout
               70  LOAD_METHOD              read
               72  CALL_METHOD_0         0  ''
               74  STORE_FAST               'data'
               76  POP_BLOCK        
               78  LOAD_CONST               None
               80  DUP_TOP          
               82  DUP_TOP          
               84  CALL_FUNCTION_3       3  ''
               86  POP_TOP          
               88  JUMP_FORWARD        106  'to 106'
             90_0  COME_FROM_WITH       62  '62'
               90  <49>             
               92  POP_JUMP_IF_TRUE     96  'to 96'
               94  <48>             
             96_0  COME_FROM            92  '92'
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          
              102  POP_EXCEPT       
              104  POP_TOP          
            106_0  COME_FROM            88  '88'

 L. 153       106  LOAD_GLOBAL              re
              108  LOAD_METHOD              search
              110  LOAD_CONST               b'\\[.*\\]\\sSONAME\\s+([^\\s]+)'
              112  LOAD_FAST                'data'
              114  CALL_METHOD_2         2  ''
              116  STORE_FAST               'res'

 L. 154       118  LOAD_FAST                'res'
              120  POP_JUMP_IF_TRUE    126  'to 126'

 L. 155       122  LOAD_CONST               None
              124  RETURN_VALUE     
            126_0  COME_FROM           120  '120'

 L. 156       126  LOAD_GLOBAL              os
              128  LOAD_METHOD              fsdecode
              130  LOAD_FAST                'res'
              132  LOAD_METHOD              group
              134  LOAD_CONST               1
              136  CALL_METHOD_1         1  ''
              138  CALL_METHOD_1         1  ''
              140  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 44


    else:

        def _get_soname--- This code section failed: ---

 L. 160         0  LOAD_FAST                'f'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 161         4  LOAD_CONST               None
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 162         8  LOAD_GLOBAL              shutil
               10  LOAD_METHOD              which
               12  LOAD_STR                 'objdump'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'objdump'

 L. 163        18  LOAD_FAST                'objdump'
               20  POP_JUMP_IF_TRUE     26  'to 26'

 L. 165        22  LOAD_CONST               None
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 167        26  SETUP_FINALLY        62  'to 62'

 L. 168        28  LOAD_GLOBAL              subprocess
               30  LOAD_ATTR                Popen
               32  LOAD_FAST                'objdump'
               34  LOAD_STR                 '-p'
               36  LOAD_STR                 '-j'
               38  LOAD_STR                 '.dynamic'
               40  LOAD_FAST                'f'
               42  BUILD_TUPLE_5         5 

 L. 169        44  LOAD_GLOBAL              subprocess
               46  LOAD_ATTR                PIPE

 L. 170        48  LOAD_GLOBAL              subprocess
               50  LOAD_ATTR                DEVNULL

 L. 168        52  LOAD_CONST               ('stdout', 'stderr')
               54  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               56  STORE_FAST               'proc'
               58  POP_BLOCK        
               60  JUMP_FORWARD         82  'to 82'
             62_0  COME_FROM_FINALLY    26  '26'

 L. 171        62  DUP_TOP          
               64  LOAD_GLOBAL              OSError
               66  <121>                80  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 172        74  POP_EXCEPT       
               76  LOAD_CONST               None
               78  RETURN_VALUE     
               80  <48>             
             82_0  COME_FROM            60  '60'

 L. 173        82  LOAD_FAST                'proc'
               84  SETUP_WITH          112  'to 112'
               86  POP_TOP          

 L. 174        88  LOAD_FAST                'proc'
               90  LOAD_ATTR                stdout
               92  LOAD_METHOD              read
               94  CALL_METHOD_0         0  ''
               96  STORE_FAST               'dump'
               98  POP_BLOCK        
              100  LOAD_CONST               None
              102  DUP_TOP          
              104  DUP_TOP          
              106  CALL_FUNCTION_3       3  ''
              108  POP_TOP          
              110  JUMP_FORWARD        128  'to 128'
            112_0  COME_FROM_WITH       84  '84'
              112  <49>             
              114  POP_JUMP_IF_TRUE    118  'to 118'
              116  <48>             
            118_0  COME_FROM           114  '114'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          
              124  POP_EXCEPT       
              126  POP_TOP          
            128_0  COME_FROM           110  '110'

 L. 175       128  LOAD_GLOBAL              re
              130  LOAD_METHOD              search
              132  LOAD_CONST               b'\\sSONAME\\s+([^\\s]+)'
              134  LOAD_FAST                'dump'
              136  CALL_METHOD_2         2  ''
              138  STORE_FAST               'res'

 L. 176       140  LOAD_FAST                'res'
              142  POP_JUMP_IF_TRUE    148  'to 148'

 L. 177       144  LOAD_CONST               None
              146  RETURN_VALUE     
            148_0  COME_FROM           142  '142'

 L. 178       148  LOAD_GLOBAL              os
              150  LOAD_METHOD              fsdecode
              152  LOAD_FAST                'res'
              154  LOAD_METHOD              group
              156  LOAD_CONST               1
              158  CALL_METHOD_1         1  ''
              160  CALL_METHOD_1         1  ''
              162  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 66


    if sys.platform.startswith(('freebsd', 'openbsd', 'dragonfly')):

        def _num_version--- This code section failed: ---

 L. 184         0  LOAD_FAST                'libname'
                2  LOAD_METHOD              split
                4  LOAD_CONST               b'.'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'parts'

 L. 185        10  BUILD_LIST_0          0 
               12  STORE_FAST               'nums'

 L. 186        14  SETUP_FINALLY        46  'to 46'
             16_0  COME_FROM            40  '40'

 L. 187        16  LOAD_FAST                'parts'
               18  POP_JUMP_IF_FALSE    42  'to 42'

 L. 188        20  LOAD_FAST                'nums'
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

 L. 189        46  DUP_TOP          
               48  LOAD_GLOBAL              ValueError
               50  <121>                62  ''
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 190        58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
               62  <48>             
             64_0  COME_FROM            60  '60'
             64_1  COME_FROM            44  '44'

 L. 191        64  LOAD_FAST                'nums'
               66  JUMP_IF_TRUE_OR_POP    74  'to 74'
               68  LOAD_GLOBAL              sys
               70  LOAD_ATTR                maxsize
               72  BUILD_LIST_1          1 
             74_0  COME_FROM            66  '66'
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 50


        def find_library--- This code section failed: ---

 L. 194         0  LOAD_GLOBAL              re
                2  LOAD_METHOD              escape
                4  LOAD_FAST                'name'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'ename'

 L. 195        10  LOAD_STR                 ':-l%s\\.\\S+ => \\S*/(lib%s\\.\\S+)'
               12  LOAD_FAST                'ename'
               14  LOAD_FAST                'ename'
               16  BUILD_TUPLE_2         2 
               18  BINARY_MODULO    
               20  STORE_FAST               'expr'

 L. 196        22  LOAD_GLOBAL              os
               24  LOAD_METHOD              fsencode
               26  LOAD_FAST                'expr'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'expr'

 L. 198        32  SETUP_FINALLY        58  'to 58'

 L. 199        34  LOAD_GLOBAL              subprocess
               36  LOAD_ATTR                Popen
               38  LOAD_CONST               ('/sbin/ldconfig', '-r')

 L. 200        40  LOAD_GLOBAL              subprocess
               42  LOAD_ATTR                PIPE

 L. 201        44  LOAD_GLOBAL              subprocess
               46  LOAD_ATTR                DEVNULL

 L. 199        48  LOAD_CONST               ('stdout', 'stderr')
               50  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               52  STORE_FAST               'proc'
               54  POP_BLOCK        
               56  JUMP_FORWARD         80  'to 80'
             58_0  COME_FROM_FINALLY    32  '32'

 L. 202        58  DUP_TOP          
               60  LOAD_GLOBAL              OSError
               62  <121>                78  ''
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 203        70  LOAD_CONST               b''
               72  STORE_FAST               'data'
               74  POP_EXCEPT       
               76  JUMP_FORWARD        126  'to 126'
               78  <48>             
             80_0  COME_FROM            56  '56'

 L. 205        80  LOAD_FAST                'proc'
               82  SETUP_WITH          110  'to 110'
               84  POP_TOP          

 L. 206        86  LOAD_FAST                'proc'
               88  LOAD_ATTR                stdout
               90  LOAD_METHOD              read
               92  CALL_METHOD_0         0  ''
               94  STORE_FAST               'data'
               96  POP_BLOCK        
               98  LOAD_CONST               None
              100  DUP_TOP          
              102  DUP_TOP          
              104  CALL_FUNCTION_3       3  ''
              106  POP_TOP          
              108  JUMP_FORWARD        126  'to 126'
            110_0  COME_FROM_WITH       82  '82'
              110  <49>             
              112  POP_JUMP_IF_TRUE    116  'to 116'
              114  <48>             
            116_0  COME_FROM           112  '112'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          
              122  POP_EXCEPT       
              124  POP_TOP          
            126_0  COME_FROM           108  '108'
            126_1  COME_FROM            76  '76'

 L. 208       126  LOAD_GLOBAL              re
              128  LOAD_METHOD              findall
              130  LOAD_FAST                'expr'
              132  LOAD_FAST                'data'
              134  CALL_METHOD_2         2  ''
              136  STORE_FAST               'res'

 L. 209       138  LOAD_FAST                'res'
              140  POP_JUMP_IF_TRUE    154  'to 154'

 L. 210       142  LOAD_GLOBAL              _get_soname
              144  LOAD_GLOBAL              _findLib_gcc
              146  LOAD_FAST                'name'
              148  CALL_FUNCTION_1       1  ''
              150  CALL_FUNCTION_1       1  ''
              152  RETURN_VALUE     
            154_0  COME_FROM           140  '140'

 L. 211       154  LOAD_FAST                'res'
              156  LOAD_ATTR                sort
              158  LOAD_GLOBAL              _num_version
              160  LOAD_CONST               ('key',)
              162  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              164  POP_TOP          

 L. 212       166  LOAD_GLOBAL              os
              168  LOAD_METHOD              fsdecode
              170  LOAD_FAST                'res'
              172  LOAD_CONST               -1
              174  BINARY_SUBSCR    
              176  CALL_METHOD_1         1  ''
              178  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 62


    elif sys.platform == 'sunos5':

        def _findLib_crle--- This code section failed: ---

 L. 217         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              exists
                6  LOAD_STR                 '/usr/bin/crle'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L. 218        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 220        16  LOAD_GLOBAL              dict
               18  LOAD_GLOBAL              os
               20  LOAD_ATTR                environ
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'env'

 L. 221        26  LOAD_STR                 'C'
               28  LOAD_FAST                'env'
               30  LOAD_STR                 'LC_ALL'
               32  STORE_SUBSCR     

 L. 223        34  LOAD_FAST                'is64'
               36  POP_JUMP_IF_FALSE    44  'to 44'

 L. 224        38  LOAD_CONST               ('/usr/bin/crle', '-64')
               40  STORE_FAST               'args'
               42  JUMP_FORWARD         48  'to 48'
             44_0  COME_FROM            36  '36'

 L. 226        44  LOAD_CONST               ('/usr/bin/crle',)
               46  STORE_FAST               'args'
             48_0  COME_FROM            42  '42'

 L. 228        48  LOAD_CONST               None
               50  STORE_FAST               'paths'

 L. 229        52  SETUP_FINALLY        80  'to 80'

 L. 230        54  LOAD_GLOBAL              subprocess
               56  LOAD_ATTR                Popen
               58  LOAD_FAST                'args'

 L. 231        60  LOAD_GLOBAL              subprocess
               62  LOAD_ATTR                PIPE

 L. 232        64  LOAD_GLOBAL              subprocess
               66  LOAD_ATTR                DEVNULL

 L. 233        68  LOAD_FAST                'env'

 L. 230        70  LOAD_CONST               ('stdout', 'stderr', 'env')
               72  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               74  STORE_FAST               'proc'
               76  POP_BLOCK        
               78  JUMP_FORWARD        100  'to 100'
             80_0  COME_FROM_FINALLY    52  '52'

 L. 234        80  DUP_TOP          
               82  LOAD_GLOBAL              OSError
               84  <121>                98  ''
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 235        92  POP_EXCEPT       
               94  LOAD_CONST               None
               96  RETURN_VALUE     
               98  <48>             
            100_0  COME_FROM            78  '78'

 L. 236       100  LOAD_FAST                'proc'
              102  SETUP_WITH          168  'to 168'
              104  POP_TOP          

 L. 237       106  LOAD_FAST                'proc'
              108  LOAD_ATTR                stdout
              110  GET_ITER         
            112_0  COME_FROM           152  '152'
            112_1  COME_FROM           132  '132'
              112  FOR_ITER            154  'to 154'
              114  STORE_FAST               'line'

 L. 238       116  LOAD_FAST                'line'
              118  LOAD_METHOD              strip
              120  CALL_METHOD_0         0  ''
              122  STORE_FAST               'line'

 L. 239       124  LOAD_FAST                'line'
              126  LOAD_METHOD              startswith
              128  LOAD_CONST               b'Default Library Path (ELF):'
              130  CALL_METHOD_1         1  ''
              132  POP_JUMP_IF_FALSE_BACK   112  'to 112'

 L. 240       134  LOAD_GLOBAL              os
              136  LOAD_METHOD              fsdecode
              138  LOAD_FAST                'line'
              140  CALL_METHOD_1         1  ''
              142  LOAD_METHOD              split
              144  CALL_METHOD_0         0  ''
              146  LOAD_CONST               4
              148  BINARY_SUBSCR    
              150  STORE_FAST               'paths'
              152  JUMP_BACK           112  'to 112'
            154_0  COME_FROM           112  '112'
              154  POP_BLOCK        
              156  LOAD_CONST               None
              158  DUP_TOP          
              160  DUP_TOP          
              162  CALL_FUNCTION_3       3  ''
              164  POP_TOP          
              166  JUMP_FORWARD        184  'to 184'
            168_0  COME_FROM_WITH      102  '102'
              168  <49>             
              170  POP_JUMP_IF_TRUE    174  'to 174'
              172  <48>             
            174_0  COME_FROM           170  '170'
              174  POP_TOP          
              176  POP_TOP          
              178  POP_TOP          
              180  POP_EXCEPT       
              182  POP_TOP          
            184_0  COME_FROM           166  '166'

 L. 242       184  LOAD_FAST                'paths'
              186  POP_JUMP_IF_TRUE    192  'to 192'

 L. 243       188  LOAD_CONST               None
              190  RETURN_VALUE     
            192_0  COME_FROM           186  '186'

 L. 245       192  LOAD_FAST                'paths'
              194  LOAD_METHOD              split
              196  LOAD_STR                 ':'
              198  CALL_METHOD_1         1  ''
              200  GET_ITER         
            202_0  COME_FROM           244  '244'
            202_1  COME_FROM           234  '234'
              202  FOR_ITER            246  'to 246'
              204  STORE_FAST               'dir'

 L. 246       206  LOAD_GLOBAL              os
              208  LOAD_ATTR                path
              210  LOAD_METHOD              join
              212  LOAD_FAST                'dir'
              214  LOAD_STR                 'lib%s.so'
              216  LOAD_FAST                'name'
              218  BINARY_MODULO    
              220  CALL_METHOD_2         2  ''
              222  STORE_FAST               'libfile'

 L. 247       224  LOAD_GLOBAL              os
              226  LOAD_ATTR                path
              228  LOAD_METHOD              exists
              230  LOAD_FAST                'libfile'
              232  CALL_METHOD_1         1  ''
              234  POP_JUMP_IF_FALSE_BACK   202  'to 202'

 L. 248       236  LOAD_FAST                'libfile'
              238  ROT_TWO          
              240  POP_TOP          
              242  RETURN_VALUE     
              244  JUMP_BACK           202  'to 202'
            246_0  COME_FROM           202  '202'

Parse error at or near `<121>' instruction at offset 84


        def find_library(name, is64=False):
            return _get_soname(_findLib_crle(name, is64) or _findLib_gcc(name))


    else:

        def _findSoname_ldconfig--- This code section failed: ---

 L. 258         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              struct
                6  STORE_FAST               'struct'

 L. 259         8  LOAD_FAST                'struct'
               10  LOAD_METHOD              calcsize
               12  LOAD_STR                 'l'
               14  CALL_METHOD_1         1  ''
               16  LOAD_CONST               4
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    38  'to 38'

 L. 260        22  LOAD_GLOBAL              os
               24  LOAD_METHOD              uname
               26  CALL_METHOD_0         0  ''
               28  LOAD_ATTR                machine
               30  LOAD_STR                 '-32'
               32  BINARY_ADD       
               34  STORE_FAST               'machine'
               36  JUMP_FORWARD         52  'to 52'
             38_0  COME_FROM            20  '20'

 L. 262        38  LOAD_GLOBAL              os
               40  LOAD_METHOD              uname
               42  CALL_METHOD_0         0  ''
               44  LOAD_ATTR                machine
               46  LOAD_STR                 '-64'
               48  BINARY_ADD       
               50  STORE_FAST               'machine'
             52_0  COME_FROM            36  '36'

 L. 264        52  LOAD_STR                 'libc6,x86-64'

 L. 265        54  LOAD_STR                 'libc6,64bit'

 L. 266        56  LOAD_STR                 'libc6,64bit'

 L. 267        58  LOAD_STR                 'libc6,64bit'

 L. 268        60  LOAD_STR                 'libc6,IA-64'

 L. 263        62  LOAD_CONST               ('x86_64-64', 'ppc64-64', 'sparc64-64', 's390x-64', 'ia64-64')
               64  BUILD_CONST_KEY_MAP_5     5 
               66  STORE_FAST               'mach_map'

 L. 270        68  LOAD_FAST                'mach_map'
               70  LOAD_METHOD              get
               72  LOAD_FAST                'machine'
               74  LOAD_STR                 'libc6'
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'abi_type'

 L. 273        80  LOAD_STR                 '\\s+(lib%s\\.[^\\s]+)\\s+\\(%s'
               82  STORE_FAST               'regex'

 L. 274        84  LOAD_GLOBAL              os
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

 L. 275       108  SETUP_FINALLY       236  'to 236'

 L. 276       110  LOAD_GLOBAL              subprocess
              112  LOAD_ATTR                Popen
              114  LOAD_STR                 '/sbin/ldconfig'
              116  LOAD_STR                 '-p'
              118  BUILD_LIST_2          2 

 L. 277       120  LOAD_GLOBAL              subprocess
              122  LOAD_ATTR                DEVNULL

 L. 278       124  LOAD_GLOBAL              subprocess
              126  LOAD_ATTR                DEVNULL

 L. 279       128  LOAD_GLOBAL              subprocess
              130  LOAD_ATTR                PIPE

 L. 280       132  LOAD_STR                 'C'
              134  LOAD_STR                 'C'
              136  LOAD_CONST               ('LC_ALL', 'LANG')
              138  BUILD_CONST_KEY_MAP_2     2 

 L. 276       140  LOAD_CONST               ('stdin', 'stderr', 'stdout', 'env')
              142  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              144  SETUP_WITH          216  'to 216'

 L. 280       146  STORE_FAST               'p'

 L. 281       148  LOAD_GLOBAL              re
              150  LOAD_METHOD              search
              152  LOAD_FAST                'regex'
              154  LOAD_FAST                'p'
              156  LOAD_ATTR                stdout
              158  LOAD_METHOD              read
              160  CALL_METHOD_0         0  ''
              162  CALL_METHOD_2         2  ''
              164  STORE_FAST               'res'

 L. 282       166  LOAD_FAST                'res'
              168  POP_JUMP_IF_FALSE   202  'to 202'

 L. 283       170  LOAD_GLOBAL              os
              172  LOAD_METHOD              fsdecode
              174  LOAD_FAST                'res'
              176  LOAD_METHOD              group
              178  LOAD_CONST               1
              180  CALL_METHOD_1         1  ''
              182  CALL_METHOD_1         1  ''
              184  POP_BLOCK        
              186  ROT_TWO          
              188  LOAD_CONST               None
              190  DUP_TOP          
              192  DUP_TOP          
              194  CALL_FUNCTION_3       3  ''
              196  POP_TOP          
              198  POP_BLOCK        
              200  RETURN_VALUE     
            202_0  COME_FROM           168  '168'
              202  POP_BLOCK        
              204  LOAD_CONST               None
              206  DUP_TOP          
              208  DUP_TOP          
              210  CALL_FUNCTION_3       3  ''
              212  POP_TOP          
              214  JUMP_FORWARD        232  'to 232'
            216_0  COME_FROM_WITH      144  '144'
              216  <49>             
              218  POP_JUMP_IF_TRUE    222  'to 222'
              220  <48>             
            222_0  COME_FROM           218  '218'
              222  POP_TOP          
              224  POP_TOP          
              226  POP_TOP          
              228  POP_EXCEPT       
              230  POP_TOP          
            232_0  COME_FROM           214  '214'
              232  POP_BLOCK        
              234  JUMP_FORWARD        254  'to 254'
            236_0  COME_FROM_FINALLY   108  '108'

 L. 284       236  DUP_TOP          
              238  LOAD_GLOBAL              OSError
              240  <121>               252  ''
              242  POP_TOP          
              244  POP_TOP          
              246  POP_TOP          

 L. 285       248  POP_EXCEPT       
              250  JUMP_FORWARD        254  'to 254'
              252  <48>             
            254_0  COME_FROM           250  '250'
            254_1  COME_FROM           234  '234'

Parse error at or near `LOAD_CONST' instruction at offset 188


        def _findLib_ld--- This code section failed: ---

 L. 289         0  LOAD_STR                 '[^\\(\\)\\s]*lib%s\\.[^\\(\\)\\s]*'
                2  LOAD_GLOBAL              re
                4  LOAD_METHOD              escape
                6  LOAD_FAST                'name'
                8  CALL_METHOD_1         1  ''
               10  BINARY_MODULO    
               12  STORE_FAST               'expr'

 L. 290        14  LOAD_STR                 'ld'
               16  LOAD_STR                 '-t'
               18  BUILD_LIST_2          2 
               20  STORE_FAST               'cmd'

 L. 291        22  LOAD_GLOBAL              os
               24  LOAD_ATTR                environ
               26  LOAD_METHOD              get
               28  LOAD_STR                 'LD_LIBRARY_PATH'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'libpath'

 L. 292        34  LOAD_FAST                'libpath'
               36  POP_JUMP_IF_FALSE    68  'to 68'

 L. 293        38  LOAD_FAST                'libpath'
               40  LOAD_METHOD              split
               42  LOAD_STR                 ':'
               44  CALL_METHOD_1         1  ''
               46  GET_ITER         
             48_0  COME_FROM            66  '66'
               48  FOR_ITER             68  'to 68'
               50  STORE_FAST               'd'

 L. 294        52  LOAD_FAST                'cmd'
               54  LOAD_METHOD              extend
               56  LOAD_STR                 '-L'
               58  LOAD_FAST                'd'
               60  BUILD_LIST_2          2 
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
               66  JUMP_BACK            48  'to 48'
             68_0  COME_FROM            48  '48'
             68_1  COME_FROM            36  '36'

 L. 295        68  LOAD_FAST                'cmd'
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

 L. 296        90  LOAD_CONST               None
               92  STORE_FAST               'result'

 L. 297        94  SETUP_FINALLY       166  'to 166'

 L. 298        96  LOAD_GLOBAL              subprocess
               98  LOAD_ATTR                Popen
              100  LOAD_FAST                'cmd'
              102  LOAD_GLOBAL              subprocess
              104  LOAD_ATTR                PIPE

 L. 299       106  LOAD_GLOBAL              subprocess
              108  LOAD_ATTR                PIPE

 L. 300       110  LOAD_CONST               True

 L. 298       112  LOAD_CONST               ('stdout', 'stderr', 'universal_newlines')
              114  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              116  STORE_FAST               'p'

 L. 301       118  LOAD_FAST                'p'
              120  LOAD_METHOD              communicate
              122  CALL_METHOD_0         0  ''
              124  UNPACK_SEQUENCE_2     2 
              126  STORE_FAST               'out'
              128  STORE_FAST               '_'

 L. 302       130  LOAD_GLOBAL              re
              132  LOAD_METHOD              search
              134  LOAD_FAST                'expr'
              136  LOAD_GLOBAL              os
              138  LOAD_METHOD              fsdecode
              140  LOAD_FAST                'out'
              142  CALL_METHOD_1         1  ''
              144  CALL_METHOD_2         2  ''
              146  STORE_FAST               'res'

 L. 303       148  LOAD_FAST                'res'
              150  POP_JUMP_IF_FALSE   162  'to 162'

 L. 304       152  LOAD_FAST                'res'
              154  LOAD_METHOD              group
              156  LOAD_CONST               0
              158  CALL_METHOD_1         1  ''
              160  STORE_FAST               'result'
            162_0  COME_FROM           150  '150'
              162  POP_BLOCK        
              164  JUMP_FORWARD        184  'to 184'
            166_0  COME_FROM_FINALLY    94  '94'

 L. 305       166  DUP_TOP          
              168  LOAD_GLOBAL              Exception
              170  <121>               182  ''
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L. 306       178  POP_EXCEPT       
              180  JUMP_FORWARD        184  'to 184'
              182  <48>             
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM           164  '164'

 L. 307       184  LOAD_FAST                'result'
              186  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 170


        def find_library(name):
            return _findSoname_ldconfig(name) or _get_soname(_findLib_gcc(name) or _findLib_ld(name))


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