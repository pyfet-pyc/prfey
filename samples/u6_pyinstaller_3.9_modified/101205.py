# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\file_util.py
"""distutils.file_util

Utility functions for operating on single files.
"""
import os
from distutils.errors import DistutilsFileError
from distutils import log
_copy_action = {None:'copying', 
 'hard':'hard linking', 
 'sym':'symbolically linking'}

def _copy_file_contents--- This code section failed: ---

 L.  25         0  LOAD_CONST               None
                2  STORE_FAST               'fsrc'

 L.  26         4  LOAD_CONST               None
                6  STORE_FAST               'fdst'

 L.  27      8_10  SETUP_FINALLY       422  'to 422'

 L.  28        12  SETUP_FINALLY        28  'to 28'

 L.  29        14  LOAD_GLOBAL              open
               16  LOAD_FAST                'src'
               18  LOAD_STR                 'rb'
               20  CALL_FUNCTION_2       2  ''
               22  STORE_FAST               'fsrc'
               24  POP_BLOCK        
               26  JUMP_FORWARD         82  'to 82'
             28_0  COME_FROM_FINALLY    12  '12'

 L.  30        28  DUP_TOP          
               30  LOAD_GLOBAL              OSError
               32  <121>                80  ''
               34  POP_TOP          
               36  STORE_FAST               'e'
               38  POP_TOP          
               40  SETUP_FINALLY        72  'to 72'

 L.  31        42  LOAD_GLOBAL              DistutilsFileError
               44  LOAD_STR                 "could not open '%s': %s"
               46  LOAD_FAST                'src'
               48  LOAD_FAST                'e'
               50  LOAD_ATTR                strerror
               52  BUILD_TUPLE_2         2 
               54  BINARY_MODULO    
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
               60  POP_BLOCK        
               62  POP_EXCEPT       
               64  LOAD_CONST               None
               66  STORE_FAST               'e'
               68  DELETE_FAST              'e'
               70  JUMP_FORWARD         82  'to 82'
             72_0  COME_FROM_FINALLY    40  '40'
               72  LOAD_CONST               None
               74  STORE_FAST               'e'
               76  DELETE_FAST              'e'
               78  <48>             
               80  <48>             
             82_0  COME_FROM            70  '70'
             82_1  COME_FROM            26  '26'

 L.  33        82  LOAD_GLOBAL              os
               84  LOAD_ATTR                path
               86  LOAD_METHOD              exists
               88  LOAD_FAST                'dst'
               90  CALL_METHOD_1         1  ''
               92  POP_JUMP_IF_FALSE   164  'to 164'

 L.  34        94  SETUP_FINALLY       110  'to 110'

 L.  35        96  LOAD_GLOBAL              os
               98  LOAD_METHOD              unlink
              100  LOAD_FAST                'dst'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          
              106  POP_BLOCK        
              108  JUMP_FORWARD        164  'to 164'
            110_0  COME_FROM_FINALLY    94  '94'

 L.  36       110  DUP_TOP          
              112  LOAD_GLOBAL              OSError
              114  <121>               162  ''
              116  POP_TOP          
              118  STORE_FAST               'e'
              120  POP_TOP          
              122  SETUP_FINALLY       154  'to 154'

 L.  37       124  LOAD_GLOBAL              DistutilsFileError

 L.  38       126  LOAD_STR                 "could not delete '%s': %s"
              128  LOAD_FAST                'dst'
              130  LOAD_FAST                'e'
              132  LOAD_ATTR                strerror
              134  BUILD_TUPLE_2         2 
              136  BINARY_MODULO    

 L.  37       138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
              142  POP_BLOCK        
              144  POP_EXCEPT       
              146  LOAD_CONST               None
              148  STORE_FAST               'e'
              150  DELETE_FAST              'e'
              152  JUMP_FORWARD        164  'to 164'
            154_0  COME_FROM_FINALLY   122  '122'
              154  LOAD_CONST               None
              156  STORE_FAST               'e'
              158  DELETE_FAST              'e'
              160  <48>             
              162  <48>             
            164_0  COME_FROM           152  '152'
            164_1  COME_FROM           108  '108'
            164_2  COME_FROM            92  '92'

 L.  40       164  SETUP_FINALLY       180  'to 180'

 L.  41       166  LOAD_GLOBAL              open
              168  LOAD_FAST                'dst'
              170  LOAD_STR                 'wb'
              172  CALL_FUNCTION_2       2  ''
              174  STORE_FAST               'fdst'
              176  POP_BLOCK        
              178  JUMP_FORWARD        234  'to 234'
            180_0  COME_FROM_FINALLY   164  '164'

 L.  42       180  DUP_TOP          
              182  LOAD_GLOBAL              OSError
              184  <121>               232  ''
              186  POP_TOP          
              188  STORE_FAST               'e'
              190  POP_TOP          
              192  SETUP_FINALLY       224  'to 224'

 L.  43       194  LOAD_GLOBAL              DistutilsFileError

 L.  44       196  LOAD_STR                 "could not create '%s': %s"
              198  LOAD_FAST                'dst'
              200  LOAD_FAST                'e'
              202  LOAD_ATTR                strerror
              204  BUILD_TUPLE_2         2 
              206  BINARY_MODULO    

 L.  43       208  CALL_FUNCTION_1       1  ''
              210  RAISE_VARARGS_1       1  'exception instance'
              212  POP_BLOCK        
              214  POP_EXCEPT       
              216  LOAD_CONST               None
              218  STORE_FAST               'e'
              220  DELETE_FAST              'e'
              222  JUMP_FORWARD        234  'to 234'
            224_0  COME_FROM_FINALLY   192  '192'
              224  LOAD_CONST               None
              226  STORE_FAST               'e'
              228  DELETE_FAST              'e'
              230  <48>             
              232  <48>             
            234_0  COME_FROM           222  '222'
            234_1  COME_FROM           178  '178'

 L.  47       234  SETUP_FINALLY       250  'to 250'

 L.  48       236  LOAD_FAST                'fsrc'
              238  LOAD_METHOD              read
              240  LOAD_FAST                'buffer_size'
              242  CALL_METHOD_1         1  ''
              244  STORE_FAST               'buf'
              246  POP_BLOCK        
              248  JUMP_FORWARD        306  'to 306'
            250_0  COME_FROM_FINALLY   234  '234'

 L.  49       250  DUP_TOP          
              252  LOAD_GLOBAL              OSError
          254_256  <121>               304  ''
              258  POP_TOP          
              260  STORE_FAST               'e'
              262  POP_TOP          
              264  SETUP_FINALLY       296  'to 296'

 L.  50       266  LOAD_GLOBAL              DistutilsFileError

 L.  51       268  LOAD_STR                 "could not read from '%s': %s"
              270  LOAD_FAST                'src'
              272  LOAD_FAST                'e'
              274  LOAD_ATTR                strerror
              276  BUILD_TUPLE_2         2 
              278  BINARY_MODULO    

 L.  50       280  CALL_FUNCTION_1       1  ''
              282  RAISE_VARARGS_1       1  'exception instance'
              284  POP_BLOCK        
              286  POP_EXCEPT       
              288  LOAD_CONST               None
              290  STORE_FAST               'e'
              292  DELETE_FAST              'e'
              294  JUMP_FORWARD        306  'to 306'
            296_0  COME_FROM_FINALLY   264  '264'
              296  LOAD_CONST               None
              298  STORE_FAST               'e'
              300  DELETE_FAST              'e'
              302  <48>             
              304  <48>             
            306_0  COME_FROM           294  '294'
            306_1  COME_FROM           248  '248'

 L.  53       306  LOAD_FAST                'buf'
          308_310  POP_JUMP_IF_TRUE    316  'to 316'

 L.  54   312_314  BREAK_LOOP          390  'to 390'
            316_0  COME_FROM           308  '308'

 L.  56       316  SETUP_FINALLY       332  'to 332'

 L.  57       318  LOAD_FAST                'fdst'
              320  LOAD_METHOD              write
              322  LOAD_FAST                'buf'
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          
              328  POP_BLOCK        
              330  JUMP_BACK           234  'to 234'
            332_0  COME_FROM_FINALLY   316  '316'

 L.  58       332  DUP_TOP          
              334  LOAD_GLOBAL              OSError
          336_338  <121>               386  ''
              340  POP_TOP          
              342  STORE_FAST               'e'
              344  POP_TOP          
              346  SETUP_FINALLY       378  'to 378'

 L.  59       348  LOAD_GLOBAL              DistutilsFileError

 L.  60       350  LOAD_STR                 "could not write to '%s': %s"
              352  LOAD_FAST                'dst'
              354  LOAD_FAST                'e'
              356  LOAD_ATTR                strerror
              358  BUILD_TUPLE_2         2 
              360  BINARY_MODULO    

 L.  59       362  CALL_FUNCTION_1       1  ''
              364  RAISE_VARARGS_1       1  'exception instance'
              366  POP_BLOCK        
              368  POP_EXCEPT       
              370  LOAD_CONST               None
              372  STORE_FAST               'e'
              374  DELETE_FAST              'e'
              376  JUMP_BACK           234  'to 234'
            378_0  COME_FROM_FINALLY   346  '346'
              378  LOAD_CONST               None
              380  STORE_FAST               'e'
              382  DELETE_FAST              'e'
              384  <48>             
              386  <48>             
              388  JUMP_BACK           234  'to 234'
              390  POP_BLOCK        

 L.  62       392  LOAD_FAST                'fdst'
          394_396  POP_JUMP_IF_FALSE   406  'to 406'

 L.  63       398  LOAD_FAST                'fdst'
              400  LOAD_METHOD              close
              402  CALL_METHOD_0         0  ''
              404  POP_TOP          
            406_0  COME_FROM           394  '394'

 L.  64       406  LOAD_FAST                'fsrc'
          408_410  POP_JUMP_IF_FALSE   452  'to 452'

 L.  65       412  LOAD_FAST                'fsrc'
              414  LOAD_METHOD              close
              416  CALL_METHOD_0         0  ''
              418  POP_TOP          
              420  JUMP_FORWARD        452  'to 452'
            422_0  COME_FROM_FINALLY     8  '8'

 L.  62       422  LOAD_FAST                'fdst'
          424_426  POP_JUMP_IF_FALSE   436  'to 436'

 L.  63       428  LOAD_FAST                'fdst'
              430  LOAD_METHOD              close
              432  CALL_METHOD_0         0  ''
              434  POP_TOP          
            436_0  COME_FROM           424  '424'

 L.  64       436  LOAD_FAST                'fsrc'
          438_440  POP_JUMP_IF_FALSE   450  'to 450'

 L.  65       442  LOAD_FAST                'fsrc'
              444  LOAD_METHOD              close
              446  CALL_METHOD_0         0  ''
              448  POP_TOP          
            450_0  COME_FROM           438  '438'
              450  <48>             
            452_0  COME_FROM           420  '420'
            452_1  COME_FROM           408  '408'

Parse error at or near `<121>' instruction at offset 32


def copy_file--- This code section failed: ---

 L. 100         0  LOAD_CONST               0
                2  LOAD_CONST               ('newer',)
                4  IMPORT_NAME_ATTR         distutils.dep_util
                6  IMPORT_FROM              newer
                8  STORE_FAST               'newer'
               10  POP_TOP          

 L. 101        12  LOAD_CONST               0
               14  LOAD_CONST               ('ST_ATIME', 'ST_MTIME', 'ST_MODE', 'S_IMODE')
               16  IMPORT_NAME              stat
               18  IMPORT_FROM              ST_ATIME
               20  STORE_FAST               'ST_ATIME'
               22  IMPORT_FROM              ST_MTIME
               24  STORE_FAST               'ST_MTIME'
               26  IMPORT_FROM              ST_MODE
               28  STORE_FAST               'ST_MODE'
               30  IMPORT_FROM              S_IMODE
               32  STORE_FAST               'S_IMODE'
               34  POP_TOP          

 L. 103        36  LOAD_GLOBAL              os
               38  LOAD_ATTR                path
               40  LOAD_METHOD              isfile
               42  LOAD_FAST                'src'
               44  CALL_METHOD_1         1  ''
               46  POP_JUMP_IF_TRUE     60  'to 60'

 L. 104        48  LOAD_GLOBAL              DistutilsFileError

 L. 105        50  LOAD_STR                 "can't copy '%s': doesn't exist or not a regular file"
               52  LOAD_FAST                'src'
               54  BINARY_MODULO    

 L. 104        56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            46  '46'

 L. 107        60  LOAD_GLOBAL              os
               62  LOAD_ATTR                path
               64  LOAD_METHOD              isdir
               66  LOAD_FAST                'dst'
               68  CALL_METHOD_1         1  ''
               70  POP_JUMP_IF_FALSE   100  'to 100'

 L. 108        72  LOAD_FAST                'dst'
               74  STORE_FAST               'dir'

 L. 109        76  LOAD_GLOBAL              os
               78  LOAD_ATTR                path
               80  LOAD_METHOD              join
               82  LOAD_FAST                'dst'
               84  LOAD_GLOBAL              os
               86  LOAD_ATTR                path
               88  LOAD_METHOD              basename
               90  LOAD_FAST                'src'
               92  CALL_METHOD_1         1  ''
               94  CALL_METHOD_2         2  ''
               96  STORE_FAST               'dst'
               98  JUMP_FORWARD        112  'to 112'
            100_0  COME_FROM            70  '70'

 L. 111       100  LOAD_GLOBAL              os
              102  LOAD_ATTR                path
              104  LOAD_METHOD              dirname
              106  LOAD_FAST                'dst'
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'dir'
            112_0  COME_FROM            98  '98'

 L. 113       112  LOAD_FAST                'update'
              114  POP_JUMP_IF_FALSE   154  'to 154'
              116  LOAD_FAST                'newer'
              118  LOAD_FAST                'src'
              120  LOAD_FAST                'dst'
              122  CALL_FUNCTION_2       2  ''
              124  POP_JUMP_IF_TRUE    154  'to 154'

 L. 114       126  LOAD_FAST                'verbose'
              128  LOAD_CONST               1
              130  COMPARE_OP               >=
              132  POP_JUMP_IF_FALSE   146  'to 146'

 L. 115       134  LOAD_GLOBAL              log
              136  LOAD_METHOD              debug
              138  LOAD_STR                 'not copying %s (output up-to-date)'
              140  LOAD_FAST                'src'
              142  CALL_METHOD_2         2  ''
              144  POP_TOP          
            146_0  COME_FROM           132  '132'

 L. 116       146  LOAD_FAST                'dst'
              148  LOAD_CONST               0
              150  BUILD_TUPLE_2         2 
              152  RETURN_VALUE     
            154_0  COME_FROM           124  '124'
            154_1  COME_FROM           114  '114'

 L. 118       154  SETUP_FINALLY       168  'to 168'

 L. 119       156  LOAD_GLOBAL              _copy_action
              158  LOAD_FAST                'link'
              160  BINARY_SUBSCR    
              162  STORE_FAST               'action'
              164  POP_BLOCK        
              166  JUMP_FORWARD        198  'to 198'
            168_0  COME_FROM_FINALLY   154  '154'

 L. 120       168  DUP_TOP          
              170  LOAD_GLOBAL              KeyError
              172  <121>               196  ''
              174  POP_TOP          
              176  POP_TOP          
              178  POP_TOP          

 L. 121       180  LOAD_GLOBAL              ValueError
              182  LOAD_STR                 "invalid value '%s' for 'link' argument"
              184  LOAD_FAST                'link'
              186  BINARY_MODULO    
              188  CALL_FUNCTION_1       1  ''
              190  RAISE_VARARGS_1       1  'exception instance'
              192  POP_EXCEPT       
              194  JUMP_FORWARD        198  'to 198'
              196  <48>             
            198_0  COME_FROM           194  '194'
            198_1  COME_FROM           166  '166'

 L. 123       198  LOAD_FAST                'verbose'
              200  LOAD_CONST               1
              202  COMPARE_OP               >=
          204_206  POP_JUMP_IF_FALSE   266  'to 266'

 L. 124       208  LOAD_GLOBAL              os
              210  LOAD_ATTR                path
              212  LOAD_METHOD              basename
              214  LOAD_FAST                'dst'
              216  CALL_METHOD_1         1  ''
              218  LOAD_GLOBAL              os
              220  LOAD_ATTR                path
              222  LOAD_METHOD              basename
              224  LOAD_FAST                'src'
              226  CALL_METHOD_1         1  ''
              228  COMPARE_OP               ==
              230  POP_JUMP_IF_FALSE   250  'to 250'

 L. 125       232  LOAD_GLOBAL              log
              234  LOAD_METHOD              info
              236  LOAD_STR                 '%s %s -> %s'
              238  LOAD_FAST                'action'
              240  LOAD_FAST                'src'
              242  LOAD_FAST                'dir'
              244  CALL_METHOD_4         4  ''
              246  POP_TOP          
              248  JUMP_FORWARD        266  'to 266'
            250_0  COME_FROM           230  '230'

 L. 127       250  LOAD_GLOBAL              log
              252  LOAD_METHOD              info
              254  LOAD_STR                 '%s %s -> %s'
              256  LOAD_FAST                'action'
              258  LOAD_FAST                'src'
              260  LOAD_FAST                'dst'
              262  CALL_METHOD_4         4  ''
              264  POP_TOP          
            266_0  COME_FROM           248  '248'
            266_1  COME_FROM           204  '204'

 L. 129       266  LOAD_FAST                'dry_run'
          268_270  POP_JUMP_IF_FALSE   280  'to 280'

 L. 130       272  LOAD_FAST                'dst'
              274  LOAD_CONST               1
              276  BUILD_TUPLE_2         2 
              278  RETURN_VALUE     
            280_0  COME_FROM           268  '268'

 L. 134       280  LOAD_FAST                'link'
              282  LOAD_STR                 'hard'
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   366  'to 366'

 L. 135       290  LOAD_GLOBAL              os
              292  LOAD_ATTR                path
              294  LOAD_METHOD              exists
              296  LOAD_FAST                'dst'
              298  CALL_METHOD_1         1  ''
          300_302  POP_JUMP_IF_FALSE   320  'to 320'
              304  LOAD_GLOBAL              os
              306  LOAD_ATTR                path
              308  LOAD_METHOD              samefile
              310  LOAD_FAST                'src'
              312  LOAD_FAST                'dst'
              314  CALL_METHOD_2         2  ''
          316_318  POP_JUMP_IF_TRUE    426  'to 426'
            320_0  COME_FROM           300  '300'

 L. 136       320  SETUP_FINALLY       344  'to 344'

 L. 137       322  LOAD_GLOBAL              os
              324  LOAD_METHOD              link
              326  LOAD_FAST                'src'
              328  LOAD_FAST                'dst'
              330  CALL_METHOD_2         2  ''
              332  POP_TOP          

 L. 138       334  LOAD_FAST                'dst'
              336  LOAD_CONST               1
              338  BUILD_TUPLE_2         2 
              340  POP_BLOCK        
              342  RETURN_VALUE     
            344_0  COME_FROM_FINALLY   320  '320'

 L. 139       344  DUP_TOP          
              346  LOAD_GLOBAL              OSError
          348_350  <121>               362  ''
              352  POP_TOP          
              354  POP_TOP          
              356  POP_TOP          

 L. 143       358  POP_EXCEPT       
              360  JUMP_FORWARD        364  'to 364'
              362  <48>             
            364_0  COME_FROM           360  '360'
              364  JUMP_FORWARD        426  'to 426'
            366_0  COME_FROM           286  '286'

 L. 144       366  LOAD_FAST                'link'
              368  LOAD_STR                 'sym'
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   426  'to 426'

 L. 145       376  LOAD_GLOBAL              os
              378  LOAD_ATTR                path
              380  LOAD_METHOD              exists
              382  LOAD_FAST                'dst'
              384  CALL_METHOD_1         1  ''
          386_388  POP_JUMP_IF_FALSE   406  'to 406'
              390  LOAD_GLOBAL              os
              392  LOAD_ATTR                path
              394  LOAD_METHOD              samefile
              396  LOAD_FAST                'src'
              398  LOAD_FAST                'dst'
              400  CALL_METHOD_2         2  ''
          402_404  POP_JUMP_IF_TRUE    426  'to 426'
            406_0  COME_FROM           386  '386'

 L. 146       406  LOAD_GLOBAL              os
              408  LOAD_METHOD              symlink
              410  LOAD_FAST                'src'
              412  LOAD_FAST                'dst'
              414  CALL_METHOD_2         2  ''
              416  POP_TOP          

 L. 147       418  LOAD_FAST                'dst'
              420  LOAD_CONST               1
              422  BUILD_TUPLE_2         2 
              424  RETURN_VALUE     
            426_0  COME_FROM           402  '402'
            426_1  COME_FROM           372  '372'
            426_2  COME_FROM           364  '364'
            426_3  COME_FROM           316  '316'

 L. 151       426  LOAD_GLOBAL              _copy_file_contents
              428  LOAD_FAST                'src'
              430  LOAD_FAST                'dst'
              432  CALL_FUNCTION_2       2  ''
              434  POP_TOP          

 L. 152       436  LOAD_FAST                'preserve_mode'
          438_440  POP_JUMP_IF_TRUE    448  'to 448'
              442  LOAD_FAST                'preserve_times'
          444_446  POP_JUMP_IF_FALSE   514  'to 514'
            448_0  COME_FROM           438  '438'

 L. 153       448  LOAD_GLOBAL              os
              450  LOAD_METHOD              stat
              452  LOAD_FAST                'src'
              454  CALL_METHOD_1         1  ''
              456  STORE_FAST               'st'

 L. 157       458  LOAD_FAST                'preserve_times'
          460_462  POP_JUMP_IF_FALSE   488  'to 488'

 L. 158       464  LOAD_GLOBAL              os
              466  LOAD_METHOD              utime
              468  LOAD_FAST                'dst'
              470  LOAD_FAST                'st'
              472  LOAD_FAST                'ST_ATIME'
              474  BINARY_SUBSCR    
              476  LOAD_FAST                'st'
              478  LOAD_FAST                'ST_MTIME'
              480  BINARY_SUBSCR    
              482  BUILD_TUPLE_2         2 
              484  CALL_METHOD_2         2  ''
              486  POP_TOP          
            488_0  COME_FROM           460  '460'

 L. 159       488  LOAD_FAST                'preserve_mode'
          490_492  POP_JUMP_IF_FALSE   514  'to 514'

 L. 160       494  LOAD_GLOBAL              os
              496  LOAD_METHOD              chmod
              498  LOAD_FAST                'dst'
              500  LOAD_FAST                'S_IMODE'
              502  LOAD_FAST                'st'
              504  LOAD_FAST                'ST_MODE'
              506  BINARY_SUBSCR    
              508  CALL_FUNCTION_1       1  ''
              510  CALL_METHOD_2         2  ''
              512  POP_TOP          
            514_0  COME_FROM           490  '490'
            514_1  COME_FROM           444  '444'

 L. 162       514  LOAD_FAST                'dst'
              516  LOAD_CONST               1
              518  BUILD_TUPLE_2         2 
              520  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 172


def move_file--- This code section failed: ---

 L. 177         0  LOAD_CONST               0
                2  LOAD_CONST               ('exists', 'isfile', 'isdir', 'basename', 'dirname')
                4  IMPORT_NAME_ATTR         os.path
                6  IMPORT_FROM              exists
                8  STORE_FAST               'exists'
               10  IMPORT_FROM              isfile
               12  STORE_FAST               'isfile'
               14  IMPORT_FROM              isdir
               16  STORE_FAST               'isdir'
               18  IMPORT_FROM              basename
               20  STORE_FAST               'basename'
               22  IMPORT_FROM              dirname
               24  STORE_FAST               'dirname'
               26  POP_TOP          

 L. 178        28  LOAD_CONST               0
               30  LOAD_CONST               None
               32  IMPORT_NAME              errno
               34  STORE_FAST               'errno'

 L. 180        36  LOAD_FAST                'verbose'
               38  LOAD_CONST               1
               40  COMPARE_OP               >=
               42  POP_JUMP_IF_FALSE    58  'to 58'

 L. 181        44  LOAD_GLOBAL              log
               46  LOAD_METHOD              info
               48  LOAD_STR                 'moving %s -> %s'
               50  LOAD_FAST                'src'
               52  LOAD_FAST                'dst'
               54  CALL_METHOD_3         3  ''
               56  POP_TOP          
             58_0  COME_FROM            42  '42'

 L. 183        58  LOAD_FAST                'dry_run'
               60  POP_JUMP_IF_FALSE    66  'to 66'

 L. 184        62  LOAD_FAST                'dst'
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'

 L. 186        66  LOAD_FAST                'isfile'
               68  LOAD_FAST                'src'
               70  CALL_FUNCTION_1       1  ''
               72  POP_JUMP_IF_TRUE     86  'to 86'

 L. 187        74  LOAD_GLOBAL              DistutilsFileError
               76  LOAD_STR                 "can't move '%s': not a regular file"
               78  LOAD_FAST                'src'
               80  BINARY_MODULO    
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            72  '72'

 L. 189        86  LOAD_FAST                'isdir'
               88  LOAD_FAST                'dst'
               90  CALL_FUNCTION_1       1  ''
               92  POP_JUMP_IF_FALSE   114  'to 114'

 L. 190        94  LOAD_GLOBAL              os
               96  LOAD_ATTR                path
               98  LOAD_METHOD              join
              100  LOAD_FAST                'dst'
              102  LOAD_FAST                'basename'
              104  LOAD_FAST                'src'
              106  CALL_FUNCTION_1       1  ''
              108  CALL_METHOD_2         2  ''
              110  STORE_FAST               'dst'
              112  JUMP_FORWARD        138  'to 138'
            114_0  COME_FROM            92  '92'

 L. 191       114  LOAD_FAST                'exists'
              116  LOAD_FAST                'dst'
              118  CALL_FUNCTION_1       1  ''
              120  POP_JUMP_IF_FALSE   138  'to 138'

 L. 192       122  LOAD_GLOBAL              DistutilsFileError

 L. 193       124  LOAD_STR                 "can't move '%s': destination '%s' already exists"

 L. 194       126  LOAD_FAST                'src'
              128  LOAD_FAST                'dst'
              130  BUILD_TUPLE_2         2 

 L. 193       132  BINARY_MODULO    

 L. 192       134  CALL_FUNCTION_1       1  ''
              136  RAISE_VARARGS_1       1  'exception instance'
            138_0  COME_FROM           120  '120'
            138_1  COME_FROM           112  '112'

 L. 196       138  LOAD_FAST                'isdir'
              140  LOAD_FAST                'dirname'
              142  LOAD_FAST                'dst'
              144  CALL_FUNCTION_1       1  ''
              146  CALL_FUNCTION_1       1  ''
              148  POP_JUMP_IF_TRUE    166  'to 166'

 L. 197       150  LOAD_GLOBAL              DistutilsFileError

 L. 198       152  LOAD_STR                 "can't move '%s': destination '%s' not a valid path"

 L. 199       154  LOAD_FAST                'src'
              156  LOAD_FAST                'dst'
              158  BUILD_TUPLE_2         2 

 L. 198       160  BINARY_MODULO    

 L. 197       162  CALL_FUNCTION_1       1  ''
              164  RAISE_VARARGS_1       1  'exception instance'
            166_0  COME_FROM           148  '148'

 L. 201       166  LOAD_CONST               False
              168  STORE_FAST               'copy_it'

 L. 202       170  SETUP_FINALLY       188  'to 188'

 L. 203       172  LOAD_GLOBAL              os
              174  LOAD_METHOD              rename
              176  LOAD_FAST                'src'
              178  LOAD_FAST                'dst'
              180  CALL_METHOD_2         2  ''
              182  POP_TOP          
              184  POP_BLOCK        
              186  JUMP_FORWARD        270  'to 270'
            188_0  COME_FROM_FINALLY   170  '170'

 L. 204       188  DUP_TOP          
              190  LOAD_GLOBAL              OSError
          192_194  <121>               268  ''
              196  POP_TOP          
              198  STORE_FAST               'e'
              200  POP_TOP          
              202  SETUP_FINALLY       260  'to 260'

 L. 205       204  LOAD_FAST                'e'
              206  LOAD_ATTR                args
              208  UNPACK_SEQUENCE_2     2 
              210  STORE_FAST               'num'
              212  STORE_FAST               'msg'

 L. 206       214  LOAD_FAST                'num'
              216  LOAD_FAST                'errno'
              218  LOAD_ATTR                EXDEV
              220  COMPARE_OP               ==
              222  POP_JUMP_IF_FALSE   230  'to 230'

 L. 207       224  LOAD_CONST               True
              226  STORE_FAST               'copy_it'
              228  JUMP_FORWARD        248  'to 248'
            230_0  COME_FROM           222  '222'

 L. 209       230  LOAD_GLOBAL              DistutilsFileError

 L. 210       232  LOAD_STR                 "couldn't move '%s' to '%s': %s"
              234  LOAD_FAST                'src'
              236  LOAD_FAST                'dst'
              238  LOAD_FAST                'msg'
              240  BUILD_TUPLE_3         3 
              242  BINARY_MODULO    

 L. 209       244  CALL_FUNCTION_1       1  ''
              246  RAISE_VARARGS_1       1  'exception instance'
            248_0  COME_FROM           228  '228'
              248  POP_BLOCK        
              250  POP_EXCEPT       
              252  LOAD_CONST               None
              254  STORE_FAST               'e'
              256  DELETE_FAST              'e'
              258  JUMP_FORWARD        270  'to 270'
            260_0  COME_FROM_FINALLY   202  '202'
              260  LOAD_CONST               None
              262  STORE_FAST               'e'
              264  DELETE_FAST              'e'
              266  <48>             
              268  <48>             
            270_0  COME_FROM           258  '258'
            270_1  COME_FROM           186  '186'

 L. 212       270  LOAD_FAST                'copy_it'
          272_274  POP_JUMP_IF_FALSE   410  'to 410'

 L. 213       276  LOAD_GLOBAL              copy_file
              278  LOAD_FAST                'src'
              280  LOAD_FAST                'dst'
              282  LOAD_FAST                'verbose'
              284  LOAD_CONST               ('verbose',)
              286  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              288  POP_TOP          

 L. 214       290  SETUP_FINALLY       306  'to 306'

 L. 215       292  LOAD_GLOBAL              os
              294  LOAD_METHOD              unlink
              296  LOAD_FAST                'src'
              298  CALL_METHOD_1         1  ''
              300  POP_TOP          
              302  POP_BLOCK        
              304  JUMP_FORWARD        410  'to 410'
            306_0  COME_FROM_FINALLY   290  '290'

 L. 216       306  DUP_TOP          
              308  LOAD_GLOBAL              OSError
          310_312  <121>               408  ''
              314  POP_TOP          
              316  STORE_FAST               'e'
              318  POP_TOP          
              320  SETUP_FINALLY       400  'to 400'

 L. 217       322  LOAD_FAST                'e'
              324  LOAD_ATTR                args
              326  UNPACK_SEQUENCE_2     2 
              328  STORE_FAST               'num'
              330  STORE_FAST               'msg'

 L. 218       332  SETUP_FINALLY       348  'to 348'

 L. 219       334  LOAD_GLOBAL              os
              336  LOAD_METHOD              unlink
              338  LOAD_FAST                'dst'
              340  CALL_METHOD_1         1  ''
              342  POP_TOP          
              344  POP_BLOCK        
              346  JUMP_FORWARD        368  'to 368'
            348_0  COME_FROM_FINALLY   332  '332'

 L. 220       348  DUP_TOP          
              350  LOAD_GLOBAL              OSError
          352_354  <121>               366  ''
              356  POP_TOP          
              358  POP_TOP          
              360  POP_TOP          

 L. 221       362  POP_EXCEPT       
              364  JUMP_FORWARD        368  'to 368'
              366  <48>             
            368_0  COME_FROM           364  '364'
            368_1  COME_FROM           346  '346'

 L. 222       368  LOAD_GLOBAL              DistutilsFileError

 L. 223       370  LOAD_STR                 "couldn't move '%s' to '%s' by copy/delete: delete '%s' failed: %s"

 L. 225       372  LOAD_FAST                'src'
              374  LOAD_FAST                'dst'
              376  LOAD_FAST                'src'
              378  LOAD_FAST                'msg'
              380  BUILD_TUPLE_4         4 

 L. 223       382  BINARY_MODULO    

 L. 222       384  CALL_FUNCTION_1       1  ''
              386  RAISE_VARARGS_1       1  'exception instance'
              388  POP_BLOCK        
              390  POP_EXCEPT       
              392  LOAD_CONST               None
              394  STORE_FAST               'e'
              396  DELETE_FAST              'e'
              398  JUMP_FORWARD        410  'to 410'
            400_0  COME_FROM_FINALLY   320  '320'
              400  LOAD_CONST               None
              402  STORE_FAST               'e'
              404  DELETE_FAST              'e'
              406  <48>             
              408  <48>             
            410_0  COME_FROM           398  '398'
            410_1  COME_FROM           304  '304'
            410_2  COME_FROM           272  '272'

 L. 226       410  LOAD_FAST                'dst'
              412  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 192_194


def write_file--- This code section failed: ---

 L. 233         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'filename'
                4  LOAD_STR                 'w'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'f'

 L. 234        10  SETUP_FINALLY        48  'to 48'

 L. 235        12  LOAD_FAST                'contents'
               14  GET_ITER         
               16  FOR_ITER             36  'to 36'
               18  STORE_FAST               'line'

 L. 236        20  LOAD_FAST                'f'
               22  LOAD_METHOD              write
               24  LOAD_FAST                'line'
               26  LOAD_STR                 '\n'
               28  BINARY_ADD       
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          
               34  JUMP_BACK            16  'to 16'
               36  POP_BLOCK        

 L. 238        38  LOAD_FAST                'f'
               40  LOAD_METHOD              close
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          
               46  JUMP_FORWARD         58  'to 58'
             48_0  COME_FROM_FINALLY    10  '10'
               48  LOAD_FAST                'f'
               50  LOAD_METHOD              close
               52  CALL_METHOD_0         0  ''
               54  POP_TOP          
               56  <48>             
             58_0  COME_FROM            46  '46'

Parse error at or near `JUMP_FORWARD' instruction at offset 46