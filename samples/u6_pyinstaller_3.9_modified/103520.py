# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\dir_util.py
"""distutils.dir_util

Utility functions for manipulating directories and directory trees."""
import os, errno
from distutils.errors import DistutilsFileError, DistutilsInternalError
from distutils import log
_path_created = {}

def mkpath--- This code section failed: ---

 L.  31         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'name'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     24  'to 24'

 L.  32        10  LOAD_GLOBAL              DistutilsInternalError

 L.  33        12  LOAD_STR                 "mkpath: 'name' must be a string (got %r)"
               14  LOAD_FAST                'name'
               16  BUILD_TUPLE_1         1 
               18  BINARY_MODULO    

 L.  32        20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM             8  '8'

 L.  40        24  LOAD_GLOBAL              os
               26  LOAD_ATTR                path
               28  LOAD_METHOD              normpath
               30  LOAD_FAST                'name'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'name'

 L.  41        36  BUILD_LIST_0          0 
               38  STORE_FAST               'created_dirs'

 L.  42        40  LOAD_GLOBAL              os
               42  LOAD_ATTR                path
               44  LOAD_METHOD              isdir
               46  LOAD_FAST                'name'
               48  CALL_METHOD_1         1  ''
               50  POP_JUMP_IF_TRUE     60  'to 60'
               52  LOAD_FAST                'name'
               54  LOAD_STR                 ''
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    64  'to 64'
             60_0  COME_FROM            50  '50'

 L.  43        60  LOAD_FAST                'created_dirs'
               62  RETURN_VALUE     
             64_0  COME_FROM            58  '58'

 L.  44        64  LOAD_GLOBAL              _path_created
               66  LOAD_METHOD              get
               68  LOAD_GLOBAL              os
               70  LOAD_ATTR                path
               72  LOAD_METHOD              abspath
               74  LOAD_FAST                'name'
               76  CALL_METHOD_1         1  ''
               78  CALL_METHOD_1         1  ''
               80  POP_JUMP_IF_FALSE    86  'to 86'

 L.  45        82  LOAD_FAST                'created_dirs'
               84  RETURN_VALUE     
             86_0  COME_FROM            80  '80'

 L.  47        86  LOAD_GLOBAL              os
               88  LOAD_ATTR                path
               90  LOAD_METHOD              split
               92  LOAD_FAST                'name'
               94  CALL_METHOD_1         1  ''
               96  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST               'head'
              100  STORE_FAST               'tail'

 L.  48       102  LOAD_FAST                'tail'
              104  BUILD_LIST_1          1 
              106  STORE_FAST               'tails'

 L.  50       108  LOAD_FAST                'head'
              110  POP_JUMP_IF_FALSE   158  'to 158'
              112  LOAD_FAST                'tail'
              114  POP_JUMP_IF_FALSE   158  'to 158'
              116  LOAD_GLOBAL              os
              118  LOAD_ATTR                path
              120  LOAD_METHOD              isdir
              122  LOAD_FAST                'head'
              124  CALL_METHOD_1         1  ''
              126  POP_JUMP_IF_TRUE    158  'to 158'

 L.  51       128  LOAD_GLOBAL              os
              130  LOAD_ATTR                path
              132  LOAD_METHOD              split
              134  LOAD_FAST                'head'
              136  CALL_METHOD_1         1  ''
              138  UNPACK_SEQUENCE_2     2 
              140  STORE_FAST               'head'
              142  STORE_FAST               'tail'

 L.  52       144  LOAD_FAST                'tails'
              146  LOAD_METHOD              insert
              148  LOAD_CONST               0
              150  LOAD_FAST                'tail'
              152  CALL_METHOD_2         2  ''
              154  POP_TOP          
              156  JUMP_BACK           108  'to 108'
            158_0  COME_FROM           126  '126'
            158_1  COME_FROM           114  '114'
            158_2  COME_FROM           110  '110'

 L.  57       158  LOAD_FAST                'tails'
              160  GET_ITER         
              162  FOR_ITER            356  'to 356'
              164  STORE_FAST               'd'

 L.  59       166  LOAD_GLOBAL              os
              168  LOAD_ATTR                path
              170  LOAD_METHOD              join
              172  LOAD_FAST                'head'
              174  LOAD_FAST                'd'
              176  CALL_METHOD_2         2  ''
              178  STORE_FAST               'head'

 L.  60       180  LOAD_GLOBAL              os
              182  LOAD_ATTR                path
              184  LOAD_METHOD              abspath
              186  LOAD_FAST                'head'
              188  CALL_METHOD_1         1  ''
              190  STORE_FAST               'abs_head'

 L.  62       192  LOAD_GLOBAL              _path_created
              194  LOAD_METHOD              get
              196  LOAD_FAST                'abs_head'
              198  CALL_METHOD_1         1  ''
              200  POP_JUMP_IF_FALSE   204  'to 204'

 L.  63       202  JUMP_BACK           162  'to 162'
            204_0  COME_FROM           200  '200'

 L.  65       204  LOAD_FAST                'verbose'
              206  LOAD_CONST               1
              208  COMPARE_OP               >=
              210  POP_JUMP_IF_FALSE   224  'to 224'

 L.  66       212  LOAD_GLOBAL              log
              214  LOAD_METHOD              info
              216  LOAD_STR                 'creating %s'
              218  LOAD_FAST                'head'
              220  CALL_METHOD_2         2  ''
              222  POP_TOP          
            224_0  COME_FROM           210  '210'

 L.  68       224  LOAD_FAST                'dry_run'
          226_228  POP_JUMP_IF_TRUE    346  'to 346'

 L.  69       230  SETUP_FINALLY       248  'to 248'

 L.  70       232  LOAD_GLOBAL              os
              234  LOAD_METHOD              mkdir
              236  LOAD_FAST                'head'
              238  LOAD_FAST                'mode'
              240  CALL_METHOD_2         2  ''
              242  POP_TOP          
              244  POP_BLOCK        
              246  JUMP_FORWARD        336  'to 336'
            248_0  COME_FROM_FINALLY   230  '230'

 L.  71       248  DUP_TOP          
              250  LOAD_GLOBAL              OSError
          252_254  <121>               334  ''
              256  POP_TOP          
              258  STORE_FAST               'exc'
              260  POP_TOP          
              262  SETUP_FINALLY       326  'to 326'

 L.  72       264  LOAD_FAST                'exc'
              266  LOAD_ATTR                errno
              268  LOAD_GLOBAL              errno
              270  LOAD_ATTR                EEXIST
              272  COMPARE_OP               ==
          274_276  POP_JUMP_IF_FALSE   292  'to 292'
              278  LOAD_GLOBAL              os
              280  LOAD_ATTR                path
              282  LOAD_METHOD              isdir
              284  LOAD_FAST                'head'
              286  CALL_METHOD_1         1  ''
          288_290  POP_JUMP_IF_TRUE    314  'to 314'
            292_0  COME_FROM           274  '274'

 L.  73       292  LOAD_GLOBAL              DistutilsFileError

 L.  74       294  LOAD_STR                 "could not create '%s': %s"
              296  LOAD_FAST                'head'
              298  LOAD_FAST                'exc'
              300  LOAD_ATTR                args
              302  LOAD_CONST               -1
              304  BINARY_SUBSCR    
              306  BUILD_TUPLE_2         2 
              308  BINARY_MODULO    

 L.  73       310  CALL_FUNCTION_1       1  ''
              312  RAISE_VARARGS_1       1  'exception instance'
            314_0  COME_FROM           288  '288'
              314  POP_BLOCK        
              316  POP_EXCEPT       
              318  LOAD_CONST               None
              320  STORE_FAST               'exc'
              322  DELETE_FAST              'exc'
              324  JUMP_FORWARD        336  'to 336'
            326_0  COME_FROM_FINALLY   262  '262'
              326  LOAD_CONST               None
              328  STORE_FAST               'exc'
              330  DELETE_FAST              'exc'
              332  <48>             
              334  <48>             
            336_0  COME_FROM           324  '324'
            336_1  COME_FROM           246  '246'

 L.  75       336  LOAD_FAST                'created_dirs'
              338  LOAD_METHOD              append
              340  LOAD_FAST                'head'
              342  CALL_METHOD_1         1  ''
              344  POP_TOP          
            346_0  COME_FROM           226  '226'

 L.  77       346  LOAD_CONST               1
              348  LOAD_GLOBAL              _path_created
              350  LOAD_FAST                'abs_head'
              352  STORE_SUBSCR     
              354  JUMP_BACK           162  'to 162'

 L.  78       356  LOAD_FAST                'created_dirs'
              358  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 252_254


def create_tree(base_dir, files, mode=511, verbose=1, dry_run=0):
    """Create all the empty directories under 'base_dir' needed to put 'files'
    there.

    'base_dir' is just the name of a directory which doesn't necessarily
    exist yet; 'files' is a list of filenames to be interpreted relative to
    'base_dir'.  'base_dir' + the directory portion of every file in 'files'
    will be created if it doesn't already exist.  'mode', 'verbose' and
    'dry_run' flags are as for 'mkpath()'.
    """
    need_dir = set()
    for file in files:
        need_dir.addos.path.joinbase_diros.path.dirnamefile
    else:
        for dir in sorted(need_dir):
            mkpath(dir, mode, verbose=verbose, dry_run=dry_run)


def copy_tree--- This code section failed: ---

 L. 120         0  LOAD_CONST               0
                2  LOAD_CONST               ('copy_file',)
                4  IMPORT_NAME_ATTR         distutils.file_util
                6  IMPORT_FROM              copy_file
                8  STORE_FAST               'copy_file'
               10  POP_TOP          

 L. 122        12  LOAD_FAST                'dry_run'
               14  POP_JUMP_IF_TRUE     40  'to 40'
               16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              isdir
               22  LOAD_FAST                'src'
               24  CALL_METHOD_1         1  ''
               26  POP_JUMP_IF_TRUE     40  'to 40'

 L. 123        28  LOAD_GLOBAL              DistutilsFileError

 L. 124        30  LOAD_STR                 "cannot copy tree '%s': not a directory"
               32  LOAD_FAST                'src'
               34  BINARY_MODULO    

 L. 123        36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            26  '26'
             40_1  COME_FROM            14  '14'

 L. 125        40  SETUP_FINALLY        56  'to 56'

 L. 126        42  LOAD_GLOBAL              os
               44  LOAD_METHOD              listdir
               46  LOAD_FAST                'src'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'names'
               52  POP_BLOCK        
               54  JUMP_FORWARD        120  'to 120'
             56_0  COME_FROM_FINALLY    40  '40'

 L. 127        56  DUP_TOP          
               58  LOAD_GLOBAL              OSError
               60  <121>               118  ''
               62  POP_TOP          
               64  STORE_FAST               'e'
               66  POP_TOP          
               68  SETUP_FINALLY       110  'to 110'

 L. 128        70  LOAD_FAST                'dry_run'
               72  POP_JUMP_IF_FALSE    80  'to 80'

 L. 129        74  BUILD_LIST_0          0 
               76  STORE_FAST               'names'
               78  JUMP_FORWARD         98  'to 98'
             80_0  COME_FROM            72  '72'

 L. 131        80  LOAD_GLOBAL              DistutilsFileError

 L. 132        82  LOAD_STR                 "error listing files in '%s': %s"
               84  LOAD_FAST                'src'
               86  LOAD_FAST                'e'
               88  LOAD_ATTR                strerror
               90  BUILD_TUPLE_2         2 
               92  BINARY_MODULO    

 L. 131        94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            78  '78'
               98  POP_BLOCK        
              100  POP_EXCEPT       
              102  LOAD_CONST               None
              104  STORE_FAST               'e'
              106  DELETE_FAST              'e'
              108  JUMP_FORWARD        120  'to 120'
            110_0  COME_FROM_FINALLY    68  '68'
              110  LOAD_CONST               None
              112  STORE_FAST               'e'
              114  DELETE_FAST              'e'
              116  <48>             
              118  <48>             
            120_0  COME_FROM           108  '108'
            120_1  COME_FROM            54  '54'

 L. 134       120  LOAD_FAST                'dry_run'
              122  POP_JUMP_IF_TRUE    136  'to 136'

 L. 135       124  LOAD_GLOBAL              mkpath
              126  LOAD_FAST                'dst'
              128  LOAD_FAST                'verbose'
              130  LOAD_CONST               ('verbose',)
              132  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              134  POP_TOP          
            136_0  COME_FROM           122  '122'

 L. 137       136  BUILD_LIST_0          0 
              138  STORE_FAST               'outputs'

 L. 139       140  LOAD_FAST                'names'
              142  GET_ITER         
              144  FOR_ITER            350  'to 350'
              146  STORE_FAST               'n'

 L. 140       148  LOAD_GLOBAL              os
              150  LOAD_ATTR                path
              152  LOAD_METHOD              join
              154  LOAD_FAST                'src'
              156  LOAD_FAST                'n'
              158  CALL_METHOD_2         2  ''
              160  STORE_FAST               'src_name'

 L. 141       162  LOAD_GLOBAL              os
              164  LOAD_ATTR                path
              166  LOAD_METHOD              join
              168  LOAD_FAST                'dst'
              170  LOAD_FAST                'n'
              172  CALL_METHOD_2         2  ''
              174  STORE_FAST               'dst_name'

 L. 143       176  LOAD_FAST                'n'
              178  LOAD_METHOD              startswith
              180  LOAD_STR                 '.nfs'
              182  CALL_METHOD_1         1  ''
              184  POP_JUMP_IF_FALSE   188  'to 188'

 L. 145       186  JUMP_BACK           144  'to 144'
            188_0  COME_FROM           184  '184'

 L. 147       188  LOAD_FAST                'preserve_symlinks'
          190_192  POP_JUMP_IF_FALSE   270  'to 270'
              194  LOAD_GLOBAL              os
              196  LOAD_ATTR                path
              198  LOAD_METHOD              islink
              200  LOAD_FAST                'src_name'
              202  CALL_METHOD_1         1  ''
          204_206  POP_JUMP_IF_FALSE   270  'to 270'

 L. 148       208  LOAD_GLOBAL              os
              210  LOAD_METHOD              readlink
              212  LOAD_FAST                'src_name'
              214  CALL_METHOD_1         1  ''
              216  STORE_FAST               'link_dest'

 L. 149       218  LOAD_FAST                'verbose'
              220  LOAD_CONST               1
              222  COMPARE_OP               >=
              224  POP_JUMP_IF_FALSE   240  'to 240'

 L. 150       226  LOAD_GLOBAL              log
              228  LOAD_METHOD              info
              230  LOAD_STR                 'linking %s -> %s'
              232  LOAD_FAST                'dst_name'
              234  LOAD_FAST                'link_dest'
              236  CALL_METHOD_3         3  ''
              238  POP_TOP          
            240_0  COME_FROM           224  '224'

 L. 151       240  LOAD_FAST                'dry_run'
          242_244  POP_JUMP_IF_TRUE    258  'to 258'

 L. 152       246  LOAD_GLOBAL              os
              248  LOAD_METHOD              symlink
              250  LOAD_FAST                'link_dest'
              252  LOAD_FAST                'dst_name'
              254  CALL_METHOD_2         2  ''
              256  POP_TOP          
            258_0  COME_FROM           242  '242'

 L. 153       258  LOAD_FAST                'outputs'
              260  LOAD_METHOD              append
              262  LOAD_FAST                'dst_name'
              264  CALL_METHOD_1         1  ''
              266  POP_TOP          
              268  JUMP_BACK           144  'to 144'
            270_0  COME_FROM           204  '204'
            270_1  COME_FROM           190  '190'

 L. 155       270  LOAD_GLOBAL              os
              272  LOAD_ATTR                path
              274  LOAD_METHOD              isdir
              276  LOAD_FAST                'src_name'
              278  CALL_METHOD_1         1  ''
          280_282  POP_JUMP_IF_FALSE   316  'to 316'

 L. 156       284  LOAD_FAST                'outputs'
              286  LOAD_METHOD              extend

 L. 157       288  LOAD_GLOBAL              copy_tree
              290  LOAD_FAST                'src_name'
              292  LOAD_FAST                'dst_name'
              294  LOAD_FAST                'preserve_mode'

 L. 158       296  LOAD_FAST                'preserve_times'
              298  LOAD_FAST                'preserve_symlinks'
              300  LOAD_FAST                'update'

 L. 159       302  LOAD_FAST                'verbose'
              304  LOAD_FAST                'dry_run'

 L. 157       306  LOAD_CONST               ('verbose', 'dry_run')
              308  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'

 L. 156       310  CALL_METHOD_1         1  ''
              312  POP_TOP          
              314  JUMP_BACK           144  'to 144'
            316_0  COME_FROM           280  '280'

 L. 161       316  LOAD_FAST                'copy_file'
              318  LOAD_FAST                'src_name'
              320  LOAD_FAST                'dst_name'
              322  LOAD_FAST                'preserve_mode'

 L. 162       324  LOAD_FAST                'preserve_times'
              326  LOAD_FAST                'update'
              328  LOAD_FAST                'verbose'

 L. 163       330  LOAD_FAST                'dry_run'

 L. 161       332  LOAD_CONST               ('verbose', 'dry_run')
              334  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              336  POP_TOP          

 L. 164       338  LOAD_FAST                'outputs'
              340  LOAD_METHOD              append
              342  LOAD_FAST                'dst_name'
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          
              348  JUMP_BACK           144  'to 144'

 L. 166       350  LOAD_FAST                'outputs'
              352  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 60


def _build_cmdtuple(path, cmdtuples):
    """Helper for remove_tree()."""
    for f in os.listdirpath:
        real_f = os.path.joinpathf
        if os.path.isdirreal_f:
            os.path.islinkreal_f or _build_cmdtuplereal_fcmdtuples
        else:
            cmdtuples.append(os.remove, real_f)
    else:
        cmdtuples.append(os.rmdir, path)


def remove_tree--- This code section failed: ---

 L. 186         0  LOAD_FAST                'verbose'
                2  LOAD_CONST               1
                4  COMPARE_OP               >=
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L. 187         8  LOAD_GLOBAL              log
               10  LOAD_METHOD              info
               12  LOAD_STR                 "removing '%s' (and everything under it)"
               14  LOAD_FAST                'directory'
               16  CALL_METHOD_2         2  ''
               18  POP_TOP          
             20_0  COME_FROM             6  '6'

 L. 188        20  LOAD_FAST                'dry_run'
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 189        24  LOAD_CONST               None
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L. 190        28  BUILD_LIST_0          0 
               30  STORE_FAST               'cmdtuples'

 L. 191        32  LOAD_GLOBAL              _build_cmdtuple
               34  LOAD_FAST                'directory'
               36  LOAD_FAST                'cmdtuples'
               38  CALL_FUNCTION_2       2  ''
               40  POP_TOP          

 L. 192        42  LOAD_FAST                'cmdtuples'
               44  GET_ITER         
               46  FOR_ITER            154  'to 154'
               48  STORE_FAST               'cmd'

 L. 193        50  SETUP_FINALLY       102  'to 102'

 L. 194        52  LOAD_FAST                'cmd'
               54  LOAD_CONST               0
               56  BINARY_SUBSCR    
               58  LOAD_FAST                'cmd'
               60  LOAD_CONST               1
               62  BINARY_SUBSCR    
               64  CALL_FUNCTION_1       1  ''
               66  POP_TOP          

 L. 196        68  LOAD_GLOBAL              os
               70  LOAD_ATTR                path
               72  LOAD_METHOD              abspath
               74  LOAD_FAST                'cmd'
               76  LOAD_CONST               1
               78  BINARY_SUBSCR    
               80  CALL_METHOD_1         1  ''
               82  STORE_FAST               'abspath'

 L. 197        84  LOAD_FAST                'abspath'
               86  LOAD_GLOBAL              _path_created
               88  <118>                 0  ''
               90  POP_JUMP_IF_FALSE    98  'to 98'

 L. 198        92  LOAD_GLOBAL              _path_created
               94  LOAD_FAST                'abspath'
               96  DELETE_SUBSCR    
             98_0  COME_FROM            90  '90'
               98  POP_BLOCK        
              100  JUMP_BACK            46  'to 46'
            102_0  COME_FROM_FINALLY    50  '50'

 L. 199       102  DUP_TOP          
              104  LOAD_GLOBAL              OSError
              106  <121>               150  ''
              108  POP_TOP          
              110  STORE_FAST               'exc'
              112  POP_TOP          
              114  SETUP_FINALLY       142  'to 142'

 L. 200       116  LOAD_GLOBAL              log
              118  LOAD_METHOD              warn
              120  LOAD_STR                 'error removing %s: %s'
              122  LOAD_FAST                'directory'
              124  LOAD_FAST                'exc'
              126  CALL_METHOD_3         3  ''
              128  POP_TOP          
              130  POP_BLOCK        
              132  POP_EXCEPT       
              134  LOAD_CONST               None
              136  STORE_FAST               'exc'
              138  DELETE_FAST              'exc'
              140  JUMP_BACK            46  'to 46'
            142_0  COME_FROM_FINALLY   114  '114'
              142  LOAD_CONST               None
              144  STORE_FAST               'exc'
              146  DELETE_FAST              'exc'
              148  <48>             
              150  <48>             
              152  JUMP_BACK            46  'to 46'

Parse error at or near `<118>' instruction at offset 88


def ensure_relative(path):
    """Take the full path 'path', and make it a relative path.

    This is useful to make 'path' the second argument to os.path.join().
    """
    drive, path = os.path.splitdrivepath
    if path[0:1] == os.sep:
        path = drive + path[1:]
    return path


# global _path_created ## Warning: Unused global