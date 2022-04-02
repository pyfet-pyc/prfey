# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: importlib\_bootstrap_external.py
"""Core implementation of path-based import.

This module is NOT meant to be directly imported! It has been designed such
that it can be bootstrapped into Python as the implementation of import. As
such it requires the injection of specific modules and attributes in order to
work. One should use importlib as the public-facing version of this module.

"""
_CASE_INSENSITIVE_PLATFORMS_STR_KEY = ('win', )
_CASE_INSENSITIVE_PLATFORMS_BYTES_KEY = ('cygwin', 'darwin')
_CASE_INSENSITIVE_PLATFORMS = _CASE_INSENSITIVE_PLATFORMS_BYTES_KEY + _CASE_INSENSITIVE_PLATFORMS_STR_KEY

def _make_relax_case():
    if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS):
        if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS_STR_KEY):
            key = 'PYTHONCASEOK'
        else:
            key = b'PYTHONCASEOK'

        def _relax_case--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                flags
                4  LOAD_ATTR                ignore_environment
                6  UNARY_NOT        
                8  JUMP_IF_FALSE_OR_POP    18  'to 18'
               10  LOAD_DEREF               'key'
               12  LOAD_GLOBAL              _os
               14  LOAD_ATTR                environ
               16  <118>                 0  ''
             18_0  COME_FROM             8  '8'
               18  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    else:

        def _relax_case():
            """True if filenames must be checked case-insensitively."""
            return False

    return _relax_case


def _pack_uint32(x):
    """Convert a 32-bit integer to little-endian."""
    return (int(x) & 4294967295).to_bytes(4, 'little')


def _unpack_uint32--- This code section failed: ---

 L.  53         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'data'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               4
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L.  54        16  LOAD_GLOBAL              int
               18  LOAD_METHOD              from_bytes
               20  LOAD_FAST                'data'
               22  LOAD_STR                 'little'
               24  CALL_METHOD_2         2  ''
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _unpack_uint16--- This code section failed: ---

 L.  58         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'data'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               2
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L.  59        16  LOAD_GLOBAL              int
               18  LOAD_METHOD              from_bytes
               20  LOAD_FAST                'data'
               22  LOAD_STR                 'little'
               24  CALL_METHOD_2         2  ''
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _path_join(*path_parts):
    """Replacement for os.path.join()."""
    return path_sep.join([part.rstrip(path_separators) for part in path_parts if part])


def _path_split--- This code section failed: ---

 L.  70         0  LOAD_GLOBAL              len
                2  LOAD_GLOBAL              path_separators
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               1
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    36  'to 36'

 L.  71        12  LOAD_FAST                'path'
               14  LOAD_METHOD              rpartition
               16  LOAD_GLOBAL              path_sep
               18  CALL_METHOD_1         1  ''
               20  UNPACK_SEQUENCE_3     3 
               22  STORE_FAST               'front'
               24  STORE_FAST               '_'
               26  STORE_FAST               'tail'

 L.  72        28  LOAD_FAST                'front'
               30  LOAD_FAST                'tail'
               32  BUILD_TUPLE_2         2 
               34  RETURN_VALUE     
             36_0  COME_FROM            10  '10'

 L.  73        36  LOAD_GLOBAL              reversed
               38  LOAD_FAST                'path'
               40  CALL_FUNCTION_1       1  ''
               42  GET_ITER         
             44_0  COME_FROM            54  '54'
               44  FOR_ITER             88  'to 88'
               46  STORE_FAST               'x'

 L.  74        48  LOAD_FAST                'x'
               50  LOAD_GLOBAL              path_separators
               52  <118>                 0  ''
               54  POP_JUMP_IF_FALSE    44  'to 44'

 L.  75        56  LOAD_FAST                'path'
               58  LOAD_ATTR                rsplit
               60  LOAD_FAST                'x'
               62  LOAD_CONST               1
               64  LOAD_CONST               ('maxsplit',)
               66  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'front'
               72  STORE_FAST               'tail'

 L.  76        74  LOAD_FAST                'front'
               76  LOAD_FAST                'tail'
               78  BUILD_TUPLE_2         2 
               80  ROT_TWO          
               82  POP_TOP          
               84  RETURN_VALUE     
               86  JUMP_BACK            44  'to 44'

 L.  77        88  LOAD_STR                 ''
               90  LOAD_FAST                'path'
               92  BUILD_TUPLE_2         2 
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 52


def _path_stat(path):
    """Stat the path.

    Made a separate function to make it easier to override in experiments
    (e.g. cache stat results).

    """
    return _os.stat(path)


def _path_is_mode_type--- This code section failed: ---

 L.  92         0  SETUP_FINALLY        14  'to 14'

 L.  93         2  LOAD_GLOBAL              _path_stat
                4  LOAD_FAST                'path'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'stat_info'
               10  POP_BLOCK        
               12  JUMP_FORWARD         34  'to 34'
             14_0  COME_FROM_FINALLY     0  '0'

 L.  94        14  DUP_TOP          
               16  LOAD_GLOBAL              OSError
               18  <121>                32  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  95        26  POP_EXCEPT       
               28  LOAD_CONST               False
               30  RETURN_VALUE     
               32  <48>             
             34_0  COME_FROM            12  '12'

 L.  96        34  LOAD_FAST                'stat_info'
               36  LOAD_ATTR                st_mode
               38  LOAD_CONST               61440
               40  BINARY_AND       
               42  LOAD_FAST                'mode'
               44  COMPARE_OP               ==
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 18


def _path_isfile(path):
    """Replacement for os.path.isfile."""
    return _path_is_mode_type(path, 32768)


def _path_isdir(path):
    """Replacement for os.path.isdir."""
    if not path:
        path = _os.getcwd()
    return _path_is_mode_type(path, 16384)


def _path_isabs--- This code section failed: ---

 L. 117         0  LOAD_FAST                'path'
                2  LOAD_METHOD              startswith
                4  LOAD_GLOBAL              path_separators
                6  CALL_METHOD_1         1  ''
                8  JUMP_IF_TRUE_OR_POP    24  'to 24'
               10  LOAD_FAST                'path'
               12  LOAD_CONST               1
               14  LOAD_CONST               3
               16  BUILD_SLICE_2         2 
               18  BINARY_SUBSCR    
               20  LOAD_GLOBAL              _pathseps_with_colon
               22  <118>                 0  ''
             24_0  COME_FROM             8  '8'
               24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _write_atomic--- This code section failed: ---

 L. 125         0  LOAD_STR                 '{}.{}'
                2  LOAD_METHOD              format
                4  LOAD_FAST                'path'
                6  LOAD_GLOBAL              id
                8  LOAD_FAST                'path'
               10  CALL_FUNCTION_1       1  ''
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'path_tmp'

 L. 126        16  LOAD_GLOBAL              _os
               18  LOAD_METHOD              open
               20  LOAD_FAST                'path_tmp'

 L. 127        22  LOAD_GLOBAL              _os
               24  LOAD_ATTR                O_EXCL
               26  LOAD_GLOBAL              _os
               28  LOAD_ATTR                O_CREAT
               30  BINARY_OR        
               32  LOAD_GLOBAL              _os
               34  LOAD_ATTR                O_WRONLY
               36  BINARY_OR        
               38  LOAD_FAST                'mode'
               40  LOAD_CONST               438
               42  BINARY_AND       

 L. 126        44  CALL_METHOD_3         3  ''
               46  STORE_FAST               'fd'

 L. 128        48  SETUP_FINALLY       120  'to 120'

 L. 131        50  LOAD_GLOBAL              _io
               52  LOAD_METHOD              FileIO
               54  LOAD_FAST                'fd'
               56  LOAD_STR                 'wb'
               58  CALL_METHOD_2         2  ''
               60  SETUP_WITH           88  'to 88'
               62  STORE_FAST               'file'

 L. 132        64  LOAD_FAST                'file'
               66  LOAD_METHOD              write
               68  LOAD_FAST                'data'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  LOAD_CONST               None
               78  DUP_TOP          
               80  DUP_TOP          
               82  CALL_FUNCTION_3       3  ''
               84  POP_TOP          
               86  JUMP_FORWARD        104  'to 104'
             88_0  COME_FROM_WITH       60  '60'
               88  <49>             
               90  POP_JUMP_IF_TRUE     94  'to 94'
               92  <48>             
             94_0  COME_FROM            90  '90'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          
              100  POP_EXCEPT       
              102  POP_TOP          
            104_0  COME_FROM            86  '86'

 L. 133       104  LOAD_GLOBAL              _os
              106  LOAD_METHOD              replace
              108  LOAD_FAST                'path_tmp'
              110  LOAD_FAST                'path'
              112  CALL_METHOD_2         2  ''
              114  POP_TOP          
              116  POP_BLOCK        
              118  JUMP_FORWARD        174  'to 174'
            120_0  COME_FROM_FINALLY    48  '48'

 L. 134       120  DUP_TOP          
              122  LOAD_GLOBAL              OSError
              124  <121>               172  ''
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L. 135       132  SETUP_FINALLY       148  'to 148'

 L. 136       134  LOAD_GLOBAL              _os
              136  LOAD_METHOD              unlink
              138  LOAD_FAST                'path_tmp'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  POP_BLOCK        
              146  JUMP_FORWARD        166  'to 166'
            148_0  COME_FROM_FINALLY   132  '132'

 L. 137       148  DUP_TOP          
              150  LOAD_GLOBAL              OSError
              152  <121>               164  ''
              154  POP_TOP          
              156  POP_TOP          
              158  POP_TOP          

 L. 138       160  POP_EXCEPT       
              162  JUMP_FORWARD        166  'to 166'
              164  <48>             
            166_0  COME_FROM           162  '162'
            166_1  COME_FROM           146  '146'

 L. 139       166  RAISE_VARARGS_0       0  'reraise'
              168  POP_EXCEPT       
              170  JUMP_FORWARD        174  'to 174'
              172  <48>             
            174_0  COME_FROM           170  '170'
            174_1  COME_FROM           118  '118'

Parse error at or near `DUP_TOP' instruction at offset 78


_code_type = type(_write_atomic.__code__)
MAGIC_NUMBER = (3425).to_bytes(2, 'little') + b'\r\n'
_RAW_MAGIC_NUMBER = int.from_bytes(MAGIC_NUMBER, 'little')
_PYCACHE = '__pycache__'
_OPT = 'opt-'
SOURCE_SUFFIXES = [
 '.py']
BYTECODE_SUFFIXES = [
 '.pyc']
DEBUG_BYTECODE_SUFFIXES = OPTIMIZED_BYTECODE_SUFFIXES = BYTECODE_SUFFIXES

def cache_from_source--- This code section failed: ---

 L. 319         0  LOAD_FAST                'debug_override'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    52  'to 52'

 L. 320         8  LOAD_GLOBAL              _warnings
               10  LOAD_METHOD              warn
               12  LOAD_STR                 "the debug_override parameter is deprecated; use 'optimization' instead"

 L. 321        14  LOAD_GLOBAL              DeprecationWarning

 L. 320        16  CALL_METHOD_2         2  ''
               18  POP_TOP          

 L. 322        20  LOAD_FAST                'optimization'
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    40  'to 40'

 L. 323        28  LOAD_STR                 'debug_override or optimization must be set to None'
               30  STORE_FAST               'message'

 L. 324        32  LOAD_GLOBAL              TypeError
               34  LOAD_FAST                'message'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            26  '26'

 L. 325        40  LOAD_FAST                'debug_override'
               42  POP_JUMP_IF_FALSE    48  'to 48'
               44  LOAD_STR                 ''
               46  JUMP_FORWARD         50  'to 50'
             48_0  COME_FROM            42  '42'
               48  LOAD_CONST               1
             50_0  COME_FROM            46  '46'
               50  STORE_FAST               'optimization'
             52_0  COME_FROM             6  '6'

 L. 326        52  LOAD_GLOBAL              _os
               54  LOAD_METHOD              fspath
               56  LOAD_FAST                'path'
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'path'

 L. 327        62  LOAD_GLOBAL              _path_split
               64  LOAD_FAST                'path'
               66  CALL_FUNCTION_1       1  ''
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'head'
               72  STORE_FAST               'tail'

 L. 328        74  LOAD_FAST                'tail'
               76  LOAD_METHOD              rpartition
               78  LOAD_STR                 '.'
               80  CALL_METHOD_1         1  ''
               82  UNPACK_SEQUENCE_3     3 
               84  STORE_FAST               'base'
               86  STORE_FAST               'sep'
               88  STORE_FAST               'rest'

 L. 329        90  LOAD_GLOBAL              sys
               92  LOAD_ATTR                implementation
               94  LOAD_ATTR                cache_tag
               96  STORE_FAST               'tag'

 L. 330        98  LOAD_FAST                'tag'
              100  LOAD_CONST               None
              102  <117>                 0  ''
              104  POP_JUMP_IF_FALSE   114  'to 114'

 L. 331       106  LOAD_GLOBAL              NotImplementedError
              108  LOAD_STR                 'sys.implementation.cache_tag is None'
              110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM           104  '104'

 L. 332       114  LOAD_STR                 ''
              116  LOAD_METHOD              join
              118  LOAD_FAST                'base'
              120  POP_JUMP_IF_FALSE   126  'to 126'
              122  LOAD_FAST                'base'
              124  JUMP_FORWARD        128  'to 128'
            126_0  COME_FROM           120  '120'
              126  LOAD_FAST                'rest'
            128_0  COME_FROM           124  '124'
              128  LOAD_FAST                'sep'
              130  LOAD_FAST                'tag'
              132  BUILD_LIST_3          3 
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'almost_filename'

 L. 333       138  LOAD_FAST                'optimization'
              140  LOAD_CONST               None
              142  <117>                 0  ''
              144  POP_JUMP_IF_FALSE   172  'to 172'

 L. 334       146  LOAD_GLOBAL              sys
              148  LOAD_ATTR                flags
              150  LOAD_ATTR                optimize
              152  LOAD_CONST               0
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   164  'to 164'

 L. 335       158  LOAD_STR                 ''
              160  STORE_FAST               'optimization'
              162  JUMP_FORWARD        172  'to 172'
            164_0  COME_FROM           156  '156'

 L. 337       164  LOAD_GLOBAL              sys
              166  LOAD_ATTR                flags
              168  LOAD_ATTR                optimize
              170  STORE_FAST               'optimization'
            172_0  COME_FROM           162  '162'
            172_1  COME_FROM           144  '144'

 L. 338       172  LOAD_GLOBAL              str
              174  LOAD_FAST                'optimization'
              176  CALL_FUNCTION_1       1  ''
              178  STORE_FAST               'optimization'

 L. 339       180  LOAD_FAST                'optimization'
              182  LOAD_STR                 ''
              184  COMPARE_OP               !=
              186  POP_JUMP_IF_FALSE   224  'to 224'

 L. 340       188  LOAD_FAST                'optimization'
              190  LOAD_METHOD              isalnum
              192  CALL_METHOD_0         0  ''
              194  POP_JUMP_IF_TRUE    210  'to 210'

 L. 341       196  LOAD_GLOBAL              ValueError
              198  LOAD_STR                 '{!r} is not alphanumeric'
              200  LOAD_METHOD              format
              202  LOAD_FAST                'optimization'
              204  CALL_METHOD_1         1  ''
              206  CALL_FUNCTION_1       1  ''
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           194  '194'

 L. 342       210  LOAD_STR                 '{}.{}{}'
              212  LOAD_METHOD              format
              214  LOAD_FAST                'almost_filename'
              216  LOAD_GLOBAL              _OPT
              218  LOAD_FAST                'optimization'
              220  CALL_METHOD_3         3  ''
              222  STORE_FAST               'almost_filename'
            224_0  COME_FROM           186  '186'

 L. 343       224  LOAD_FAST                'almost_filename'
              226  LOAD_GLOBAL              BYTECODE_SUFFIXES
              228  LOAD_CONST               0
              230  BINARY_SUBSCR    
              232  BINARY_ADD       
              234  STORE_FAST               'filename'

 L. 344       236  LOAD_GLOBAL              sys
              238  LOAD_ATTR                pycache_prefix
              240  LOAD_CONST               None
              242  <117>                 1  ''
          244_246  POP_JUMP_IF_FALSE   332  'to 332'

 L. 353       248  LOAD_GLOBAL              _path_isabs
              250  LOAD_FAST                'head'
              252  CALL_FUNCTION_1       1  ''
          254_256  POP_JUMP_IF_TRUE    272  'to 272'

 L. 354       258  LOAD_GLOBAL              _path_join
              260  LOAD_GLOBAL              _os
              262  LOAD_METHOD              getcwd
              264  CALL_METHOD_0         0  ''
              266  LOAD_FAST                'head'
              268  CALL_FUNCTION_2       2  ''
              270  STORE_FAST               'head'
            272_0  COME_FROM           254  '254'

 L. 359       272  LOAD_FAST                'head'
              274  LOAD_CONST               1
              276  BINARY_SUBSCR    
              278  LOAD_STR                 ':'
              280  COMPARE_OP               ==
          282_284  POP_JUMP_IF_FALSE   312  'to 312'
              286  LOAD_FAST                'head'
              288  LOAD_CONST               0
              290  BINARY_SUBSCR    
              292  LOAD_GLOBAL              path_separators
              294  <118>                 1  ''
          296_298  POP_JUMP_IF_FALSE   312  'to 312'

 L. 360       300  LOAD_FAST                'head'
              302  LOAD_CONST               2
              304  LOAD_CONST               None
              306  BUILD_SLICE_2         2 
              308  BINARY_SUBSCR    
              310  STORE_FAST               'head'
            312_0  COME_FROM           296  '296'
            312_1  COME_FROM           282  '282'

 L. 364       312  LOAD_GLOBAL              _path_join

 L. 365       314  LOAD_GLOBAL              sys
              316  LOAD_ATTR                pycache_prefix

 L. 366       318  LOAD_FAST                'head'
              320  LOAD_METHOD              lstrip
              322  LOAD_GLOBAL              path_separators
              324  CALL_METHOD_1         1  ''

 L. 367       326  LOAD_FAST                'filename'

 L. 364       328  CALL_FUNCTION_3       3  ''
              330  RETURN_VALUE     
            332_0  COME_FROM           244  '244'

 L. 369       332  LOAD_GLOBAL              _path_join
              334  LOAD_FAST                'head'
              336  LOAD_GLOBAL              _PYCACHE
              338  LOAD_FAST                'filename'
              340  CALL_FUNCTION_3       3  ''
              342  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def source_from_cache--- This code section failed: ---

 L. 381         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                implementation
                4  LOAD_ATTR                cache_tag
                6  LOAD_CONST               None
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 382        12  LOAD_GLOBAL              NotImplementedError
               14  LOAD_STR                 'sys.implementation.cache_tag is None'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 383        20  LOAD_GLOBAL              _os
               22  LOAD_METHOD              fspath
               24  LOAD_FAST                'path'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'path'

 L. 384        30  LOAD_GLOBAL              _path_split
               32  LOAD_FAST                'path'
               34  CALL_FUNCTION_1       1  ''
               36  UNPACK_SEQUENCE_2     2 
               38  STORE_FAST               'head'
               40  STORE_FAST               'pycache_filename'

 L. 385        42  LOAD_CONST               False
               44  STORE_FAST               'found_in_pycache_prefix'

 L. 386        46  LOAD_GLOBAL              sys
               48  LOAD_ATTR                pycache_prefix
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_FALSE   102  'to 102'

 L. 387        56  LOAD_GLOBAL              sys
               58  LOAD_ATTR                pycache_prefix
               60  LOAD_METHOD              rstrip
               62  LOAD_GLOBAL              path_separators
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'stripped_path'

 L. 388        68  LOAD_FAST                'head'
               70  LOAD_METHOD              startswith
               72  LOAD_FAST                'stripped_path'
               74  LOAD_GLOBAL              path_sep
               76  BINARY_ADD       
               78  CALL_METHOD_1         1  ''
               80  POP_JUMP_IF_FALSE   102  'to 102'

 L. 389        82  LOAD_FAST                'head'
               84  LOAD_GLOBAL              len
               86  LOAD_FAST                'stripped_path'
               88  CALL_FUNCTION_1       1  ''
               90  LOAD_CONST               None
               92  BUILD_SLICE_2         2 
               94  BINARY_SUBSCR    
               96  STORE_FAST               'head'

 L. 390        98  LOAD_CONST               True
              100  STORE_FAST               'found_in_pycache_prefix'
            102_0  COME_FROM            80  '80'
            102_1  COME_FROM            54  '54'

 L. 391       102  LOAD_FAST                'found_in_pycache_prefix'
              104  POP_JUMP_IF_TRUE    144  'to 144'

 L. 392       106  LOAD_GLOBAL              _path_split
              108  LOAD_FAST                'head'
              110  CALL_FUNCTION_1       1  ''
              112  UNPACK_SEQUENCE_2     2 
              114  STORE_FAST               'head'
              116  STORE_FAST               'pycache'

 L. 393       118  LOAD_FAST                'pycache'
              120  LOAD_GLOBAL              _PYCACHE
              122  COMPARE_OP               !=
              124  POP_JUMP_IF_FALSE   144  'to 144'

 L. 394       126  LOAD_GLOBAL              ValueError
              128  LOAD_GLOBAL              _PYCACHE
              130  FORMAT_VALUE          0  ''
              132  LOAD_STR                 ' not bottom-level directory in '

 L. 395       134  LOAD_FAST                'path'

 L. 394       136  FORMAT_VALUE          2  '!r'
              138  BUILD_STRING_3        3 
              140  CALL_FUNCTION_1       1  ''
              142  RAISE_VARARGS_1       1  'exception instance'
            144_0  COME_FROM           124  '124'
            144_1  COME_FROM           104  '104'

 L. 396       144  LOAD_FAST                'pycache_filename'
              146  LOAD_METHOD              count
              148  LOAD_STR                 '.'
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'dot_count'

 L. 397       154  LOAD_FAST                'dot_count'
              156  LOAD_CONST               frozenset({2, 3})
              158  <118>                 1  ''
              160  POP_JUMP_IF_FALSE   178  'to 178'

 L. 398       162  LOAD_GLOBAL              ValueError
              164  LOAD_STR                 'expected only 2 or 3 dots in '
              166  LOAD_FAST                'pycache_filename'
              168  FORMAT_VALUE          2  '!r'
              170  BUILD_STRING_2        2 
              172  CALL_FUNCTION_1       1  ''
              174  RAISE_VARARGS_1       1  'exception instance'
              176  JUMP_FORWARD        270  'to 270'
            178_0  COME_FROM           160  '160'

 L. 399       178  LOAD_FAST                'dot_count'
              180  LOAD_CONST               3
              182  COMPARE_OP               ==
          184_186  POP_JUMP_IF_FALSE   270  'to 270'

 L. 400       188  LOAD_FAST                'pycache_filename'
              190  LOAD_METHOD              rsplit
              192  LOAD_STR                 '.'
              194  LOAD_CONST               2
              196  CALL_METHOD_2         2  ''
              198  LOAD_CONST               -2
              200  BINARY_SUBSCR    
              202  STORE_FAST               'optimization'

 L. 401       204  LOAD_FAST                'optimization'
              206  LOAD_METHOD              startswith
              208  LOAD_GLOBAL              _OPT
              210  CALL_METHOD_1         1  ''
              212  POP_JUMP_IF_TRUE    228  'to 228'

 L. 402       214  LOAD_GLOBAL              ValueError
              216  LOAD_STR                 'optimization portion of filename does not start with '

 L. 403       218  LOAD_GLOBAL              _OPT

 L. 402       220  FORMAT_VALUE          2  '!r'
              222  BUILD_STRING_2        2 
              224  CALL_FUNCTION_1       1  ''
              226  RAISE_VARARGS_1       1  'exception instance'
            228_0  COME_FROM           212  '212'

 L. 404       228  LOAD_FAST                'optimization'
              230  LOAD_GLOBAL              len
              232  LOAD_GLOBAL              _OPT
              234  CALL_FUNCTION_1       1  ''
              236  LOAD_CONST               None
              238  BUILD_SLICE_2         2 
              240  BINARY_SUBSCR    
              242  STORE_FAST               'opt_level'

 L. 405       244  LOAD_FAST                'opt_level'
              246  LOAD_METHOD              isalnum
              248  CALL_METHOD_0         0  ''
          250_252  POP_JUMP_IF_TRUE    270  'to 270'

 L. 406       254  LOAD_GLOBAL              ValueError
              256  LOAD_STR                 'optimization level '
              258  LOAD_FAST                'optimization'
              260  FORMAT_VALUE          2  '!r'
              262  LOAD_STR                 ' is not an alphanumeric value'
              264  BUILD_STRING_3        3 
              266  CALL_FUNCTION_1       1  ''
              268  RAISE_VARARGS_1       1  'exception instance'
            270_0  COME_FROM           250  '250'
            270_1  COME_FROM           184  '184'
            270_2  COME_FROM           176  '176'

 L. 408       270  LOAD_FAST                'pycache_filename'
              272  LOAD_METHOD              partition
              274  LOAD_STR                 '.'
              276  CALL_METHOD_1         1  ''
              278  LOAD_CONST               0
              280  BINARY_SUBSCR    
              282  STORE_FAST               'base_filename'

 L. 409       284  LOAD_GLOBAL              _path_join
              286  LOAD_FAST                'head'
              288  LOAD_FAST                'base_filename'
              290  LOAD_GLOBAL              SOURCE_SUFFIXES
              292  LOAD_CONST               0
              294  BINARY_SUBSCR    
              296  BINARY_ADD       
              298  CALL_FUNCTION_2       2  ''
              300  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _get_sourcefile--- This code section failed: ---

 L. 419         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'bytecode_path'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               0
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 420        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 421        16  LOAD_FAST                'bytecode_path'
               18  LOAD_METHOD              rpartition
               20  LOAD_STR                 '.'
               22  CALL_METHOD_1         1  ''
               24  UNPACK_SEQUENCE_3     3 
               26  STORE_FAST               'rest'
               28  STORE_FAST               '_'
               30  STORE_FAST               'extension'

 L. 422        32  LOAD_FAST                'rest'
               34  POP_JUMP_IF_FALSE    56  'to 56'
               36  LOAD_FAST                'extension'
               38  LOAD_METHOD              lower
               40  CALL_METHOD_0         0  ''
               42  LOAD_CONST               -3
               44  LOAD_CONST               -1
               46  BUILD_SLICE_2         2 
               48  BINARY_SUBSCR    
               50  LOAD_STR                 'py'
               52  COMPARE_OP               !=
               54  POP_JUMP_IF_FALSE    60  'to 60'
             56_0  COME_FROM            34  '34'

 L. 423        56  LOAD_FAST                'bytecode_path'
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'

 L. 424        60  SETUP_FINALLY        74  'to 74'

 L. 425        62  LOAD_GLOBAL              source_from_cache
               64  LOAD_FAST                'bytecode_path'
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'source_path'
               70  POP_BLOCK        
               72  JUMP_FORWARD        108  'to 108'
             74_0  COME_FROM_FINALLY    60  '60'

 L. 426        74  DUP_TOP          
               76  LOAD_GLOBAL              NotImplementedError
               78  LOAD_GLOBAL              ValueError
               80  BUILD_TUPLE_2         2 
               82  <121>               106  ''
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 427        90  LOAD_FAST                'bytecode_path'
               92  LOAD_CONST               None
               94  LOAD_CONST               -1
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  STORE_FAST               'source_path'
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
              106  <48>             
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            72  '72'

 L. 428       108  LOAD_GLOBAL              _path_isfile
              110  LOAD_FAST                'source_path'
              112  CALL_FUNCTION_1       1  ''
              114  POP_JUMP_IF_FALSE   120  'to 120'
              116  LOAD_FAST                'source_path'
              118  RETURN_VALUE     
            120_0  COME_FROM           114  '114'
              120  LOAD_FAST                'bytecode_path'
              122  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 82


def _get_cached--- This code section failed: ---

 L. 432         0  LOAD_FAST                'filename'
                2  LOAD_METHOD              endswith
                4  LOAD_GLOBAL              tuple
                6  LOAD_GLOBAL              SOURCE_SUFFIXES
                8  CALL_FUNCTION_1       1  ''
               10  CALL_METHOD_1         1  ''
               12  POP_JUMP_IF_FALSE    46  'to 46'

 L. 433        14  SETUP_FINALLY        26  'to 26'

 L. 434        16  LOAD_GLOBAL              cache_from_source
               18  LOAD_FAST                'filename'
               20  CALL_FUNCTION_1       1  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    14  '14'

 L. 435        26  DUP_TOP          
               28  LOAD_GLOBAL              NotImplementedError
               30  <121>                42  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 436        38  POP_EXCEPT       
               40  JUMP_ABSOLUTE        68  'to 68'
               42  <48>             
               44  JUMP_FORWARD         68  'to 68'
             46_0  COME_FROM            12  '12'

 L. 437        46  LOAD_FAST                'filename'
               48  LOAD_METHOD              endswith
               50  LOAD_GLOBAL              tuple
               52  LOAD_GLOBAL              BYTECODE_SUFFIXES
               54  CALL_FUNCTION_1       1  ''
               56  CALL_METHOD_1         1  ''
               58  POP_JUMP_IF_FALSE    64  'to 64'

 L. 438        60  LOAD_FAST                'filename'
               62  RETURN_VALUE     
             64_0  COME_FROM            58  '58'

 L. 440        64  LOAD_CONST               None
               66  RETURN_VALUE     
             68_0  COME_FROM_EXCEPT_CLAUSE    44  '44'
             68_1  COME_FROM_EXCEPT_CLAUSE    40  '40'

Parse error at or near `<121>' instruction at offset 30


def _calc_mode--- This code section failed: ---

 L. 445         0  SETUP_FINALLY        16  'to 16'

 L. 446         2  LOAD_GLOBAL              _path_stat
                4  LOAD_FAST                'path'
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_ATTR                st_mode
               10  STORE_FAST               'mode'
               12  POP_BLOCK        
               14  JUMP_FORWARD         38  'to 38'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 447        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  <121>                36  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 448        28  LOAD_CONST               438
               30  STORE_FAST               'mode'
               32  POP_EXCEPT       
               34  JUMP_FORWARD         38  'to 38'
               36  <48>             
             38_0  COME_FROM            34  '34'
             38_1  COME_FROM            14  '14'

 L. 451        38  LOAD_FAST                'mode'
               40  LOAD_CONST               128
               42  INPLACE_OR       
               44  STORE_FAST               'mode'

 L. 452        46  LOAD_FAST                'mode'
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 20


def _check_name--- This code section failed: ---

 L. 463         0  LOAD_CONST               (None,)
                2  LOAD_CLOSURE             'method'
                4  BUILD_TUPLE_1         1 
                6  LOAD_CODE                <code_object _check_name_wrapper>
                8  LOAD_STR                 '_check_name.<locals>._check_name_wrapper'
               10  MAKE_FUNCTION_9          'default, closure'
               12  STORE_FAST               '_check_name_wrapper'

 L. 470        14  SETUP_FINALLY        26  'to 26'

 L. 471        16  LOAD_GLOBAL              _bootstrap
               18  LOAD_ATTR                _wrap
               20  STORE_FAST               '_wrap'
               22  POP_BLOCK        
               24  JUMP_FORWARD         52  'to 52'
             26_0  COME_FROM_FINALLY    14  '14'

 L. 472        26  DUP_TOP          
               28  LOAD_GLOBAL              NameError
               30  <121>                50  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 474        38  LOAD_CODE                <code_object _wrap>
               40  LOAD_STR                 '_check_name.<locals>._wrap'
               42  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               44  STORE_FAST               '_wrap'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
               50  <48>             
             52_0  COME_FROM            48  '48'
             52_1  COME_FROM            24  '24'

 L. 479        52  LOAD_FAST                '_wrap'
               54  LOAD_FAST                '_check_name_wrapper'
               56  LOAD_DEREF               'method'
               58  CALL_FUNCTION_2       2  ''
               60  POP_TOP          

 L. 480        62  LOAD_FAST                '_check_name_wrapper'
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 30


def _find_module_shim--- This code section failed: ---

 L. 493         0  LOAD_FAST                'self'
                2  LOAD_METHOD              find_loader
                4  LOAD_FAST                'fullname'
                6  CALL_METHOD_1         1  ''
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'loader'
               12  STORE_FAST               'portions'

 L. 494        14  LOAD_FAST                'loader'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    56  'to 56'
               22  LOAD_GLOBAL              len
               24  LOAD_FAST                'portions'
               26  CALL_FUNCTION_1       1  ''
               28  POP_JUMP_IF_FALSE    56  'to 56'

 L. 495        30  LOAD_STR                 'Not importing directory {}: missing __init__'
               32  STORE_FAST               'msg'

 L. 496        34  LOAD_GLOBAL              _warnings
               36  LOAD_METHOD              warn
               38  LOAD_FAST                'msg'
               40  LOAD_METHOD              format
               42  LOAD_FAST                'portions'
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  CALL_METHOD_1         1  ''
               50  LOAD_GLOBAL              ImportWarning
               52  CALL_METHOD_2         2  ''
               54  POP_TOP          
             56_0  COME_FROM            28  '28'
             56_1  COME_FROM            20  '20'

 L. 497        56  LOAD_FAST                'loader'
               58  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18


def _classify_pyc--- This code section failed: ---

 L. 516         0  LOAD_FAST                'data'
                2  LOAD_CONST               None
                4  LOAD_CONST               4
                6  BUILD_SLICE_2         2 
                8  BINARY_SUBSCR    
               10  STORE_FAST               'magic'

 L. 517        12  LOAD_FAST                'magic'
               14  LOAD_GLOBAL              MAGIC_NUMBER
               16  COMPARE_OP               !=
               18  POP_JUMP_IF_FALSE    64  'to 64'

 L. 518        20  LOAD_STR                 'bad magic number in '
               22  LOAD_FAST                'name'
               24  FORMAT_VALUE          2  '!r'
               26  LOAD_STR                 ': '
               28  LOAD_FAST                'magic'
               30  FORMAT_VALUE          2  '!r'
               32  BUILD_STRING_4        4 
               34  STORE_FAST               'message'

 L. 519        36  LOAD_GLOBAL              _bootstrap
               38  LOAD_METHOD              _verbose_message
               40  LOAD_STR                 '{}'
               42  LOAD_FAST                'message'
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 520        48  LOAD_GLOBAL              ImportError
               50  LOAD_FAST                'message'
               52  BUILD_TUPLE_1         1 
               54  BUILD_MAP_0           0 
               56  LOAD_FAST                'exc_details'
               58  <164>                 1  ''
               60  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            18  '18'

 L. 521        64  LOAD_GLOBAL              len
               66  LOAD_FAST                'data'
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_CONST               16
               72  COMPARE_OP               <
               74  POP_JUMP_IF_FALSE   106  'to 106'

 L. 522        76  LOAD_STR                 'reached EOF while reading pyc header of '
               78  LOAD_FAST                'name'
               80  FORMAT_VALUE          2  '!r'
               82  BUILD_STRING_2        2 
               84  STORE_FAST               'message'

 L. 523        86  LOAD_GLOBAL              _bootstrap
               88  LOAD_METHOD              _verbose_message
               90  LOAD_STR                 '{}'
               92  LOAD_FAST                'message'
               94  CALL_METHOD_2         2  ''
               96  POP_TOP          

 L. 524        98  LOAD_GLOBAL              EOFError
              100  LOAD_FAST                'message'
              102  CALL_FUNCTION_1       1  ''
              104  RAISE_VARARGS_1       1  'exception instance'
            106_0  COME_FROM            74  '74'

 L. 525       106  LOAD_GLOBAL              _unpack_uint32
              108  LOAD_FAST                'data'
              110  LOAD_CONST               4
              112  LOAD_CONST               8
              114  BUILD_SLICE_2         2 
              116  BINARY_SUBSCR    
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'flags'

 L. 527       122  LOAD_FAST                'flags'
              124  LOAD_CONST               -4
              126  BINARY_AND       
              128  POP_JUMP_IF_FALSE   162  'to 162'

 L. 528       130  LOAD_STR                 'invalid flags '
              132  LOAD_FAST                'flags'
              134  FORMAT_VALUE          2  '!r'
              136  LOAD_STR                 ' in '
              138  LOAD_FAST                'name'
              140  FORMAT_VALUE          2  '!r'
              142  BUILD_STRING_4        4 
              144  STORE_FAST               'message'

 L. 529       146  LOAD_GLOBAL              ImportError
              148  LOAD_FAST                'message'
              150  BUILD_TUPLE_1         1 
              152  BUILD_MAP_0           0 
              154  LOAD_FAST                'exc_details'
              156  <164>                 1  ''
              158  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              160  RAISE_VARARGS_1       1  'exception instance'
            162_0  COME_FROM           128  '128'

 L. 530       162  LOAD_FAST                'flags'
              164  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 58


def _validate_timestamp_pyc--- This code section failed: ---

 L. 552         0  LOAD_GLOBAL              _unpack_uint32
                2  LOAD_FAST                'data'
                4  LOAD_CONST               8
                6  LOAD_CONST               12
                8  BUILD_SLICE_2         2 
               10  BINARY_SUBSCR    
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_FAST                'source_mtime'
               16  LOAD_CONST               4294967295
               18  BINARY_AND       
               20  COMPARE_OP               !=
               22  POP_JUMP_IF_FALSE    62  'to 62'

 L. 553        24  LOAD_STR                 'bytecode is stale for '
               26  LOAD_FAST                'name'
               28  FORMAT_VALUE          2  '!r'
               30  BUILD_STRING_2        2 
               32  STORE_FAST               'message'

 L. 554        34  LOAD_GLOBAL              _bootstrap
               36  LOAD_METHOD              _verbose_message
               38  LOAD_STR                 '{}'
               40  LOAD_FAST                'message'
               42  CALL_METHOD_2         2  ''
               44  POP_TOP          

 L. 555        46  LOAD_GLOBAL              ImportError
               48  LOAD_FAST                'message'
               50  BUILD_TUPLE_1         1 
               52  BUILD_MAP_0           0 
               54  LOAD_FAST                'exc_details'
               56  <164>                 1  ''
               58  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            22  '22'

 L. 556        62  LOAD_FAST                'source_size'
               64  LOAD_CONST               None
               66  <117>                 1  ''
               68  POP_JUMP_IF_FALSE   116  'to 116'

 L. 557        70  LOAD_GLOBAL              _unpack_uint32
               72  LOAD_FAST                'data'
               74  LOAD_CONST               12
               76  LOAD_CONST               16
               78  BUILD_SLICE_2         2 
               80  BINARY_SUBSCR    
               82  CALL_FUNCTION_1       1  ''
               84  LOAD_FAST                'source_size'
               86  LOAD_CONST               4294967295
               88  BINARY_AND       
               90  COMPARE_OP               !=

 L. 556        92  POP_JUMP_IF_FALSE   116  'to 116'

 L. 558        94  LOAD_GLOBAL              ImportError
               96  LOAD_STR                 'bytecode is stale for '
               98  LOAD_FAST                'name'
              100  FORMAT_VALUE          2  '!r'
              102  BUILD_STRING_2        2 
              104  BUILD_TUPLE_1         1 
              106  BUILD_MAP_0           0 
              108  LOAD_FAST                'exc_details'
              110  <164>                 1  ''
              112  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              114  RAISE_VARARGS_1       1  'exception instance'
            116_0  COME_FROM            92  '92'
            116_1  COME_FROM            68  '68'

Parse error at or near `<164>' instruction at offset 56


def _validate_hash_pyc--- This code section failed: ---

 L. 578         0  LOAD_FAST                'data'
                2  LOAD_CONST               8
                4  LOAD_CONST               16
                6  BUILD_SLICE_2         2 
                8  BINARY_SUBSCR    
               10  LOAD_FAST                'source_hash'
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    38  'to 38'

 L. 579        16  LOAD_GLOBAL              ImportError

 L. 580        18  LOAD_STR                 "hash in bytecode doesn't match hash of source "
               20  LOAD_FAST                'name'
               22  FORMAT_VALUE          2  '!r'
               24  BUILD_STRING_2        2 

 L. 579        26  BUILD_TUPLE_1         1 
               28  BUILD_MAP_0           0 

 L. 581        30  LOAD_FAST                'exc_details'

 L. 579        32  <164>                 1  ''
               34  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            14  '14'

Parse error at or near `<164>' instruction at offset 32


def _compile_bytecode--- This code section failed: ---

 L. 587         0  LOAD_GLOBAL              marshal
                2  LOAD_METHOD              loads
                4  LOAD_FAST                'data'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'code'

 L. 588        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'code'
               14  LOAD_GLOBAL              _code_type
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 589        20  LOAD_GLOBAL              _bootstrap
               22  LOAD_METHOD              _verbose_message
               24  LOAD_STR                 'code object from {!r}'
               26  LOAD_FAST                'bytecode_path'
               28  CALL_METHOD_2         2  ''
               30  POP_TOP          

 L. 590        32  LOAD_FAST                'source_path'
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L. 591        40  LOAD_GLOBAL              _imp
               42  LOAD_METHOD              _fix_co_filename
               44  LOAD_FAST                'code'
               46  LOAD_FAST                'source_path'
               48  CALL_METHOD_2         2  ''
               50  POP_TOP          
             52_0  COME_FROM            38  '38'

 L. 592        52  LOAD_FAST                'code'
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 594        56  LOAD_GLOBAL              ImportError
               58  LOAD_STR                 'Non-code object in {!r}'
               60  LOAD_METHOD              format
               62  LOAD_FAST                'bytecode_path'
               64  CALL_METHOD_1         1  ''

 L. 595        66  LOAD_FAST                'name'
               68  LOAD_FAST                'bytecode_path'

 L. 594        70  LOAD_CONST               ('name', 'path')
               72  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               74  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 36


def _code_to_timestamp_pyc(code, mtime=0, source_size=0):
    """Produce the data for a timestamp-based pyc."""
    data = bytearray(MAGIC_NUMBER)
    data.extend(_pack_uint32(0))
    data.extend(_pack_uint32(mtime))
    data.extend(_pack_uint32(source_size))
    data.extend(marshal.dumps(code))
    return data


def _code_to_hash_pyc--- This code section failed: ---

 L. 610         0  LOAD_GLOBAL              bytearray
                2  LOAD_GLOBAL              MAGIC_NUMBER
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'data'

 L. 611         8  LOAD_CONST               1
               10  LOAD_FAST                'checked'
               12  LOAD_CONST               1
               14  BINARY_LSHIFT    
               16  BINARY_OR        
               18  STORE_FAST               'flags'

 L. 612        20  LOAD_FAST                'data'
               22  LOAD_METHOD              extend
               24  LOAD_GLOBAL              _pack_uint32
               26  LOAD_FAST                'flags'
               28  CALL_FUNCTION_1       1  ''
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L. 613        34  LOAD_GLOBAL              len
               36  LOAD_FAST                'source_hash'
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_CONST               8
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_TRUE     50  'to 50'
               46  <74>             
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            44  '44'

 L. 614        50  LOAD_FAST                'data'
               52  LOAD_METHOD              extend
               54  LOAD_FAST                'source_hash'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L. 615        60  LOAD_FAST                'data'
               62  LOAD_METHOD              extend
               64  LOAD_GLOBAL              marshal
               66  LOAD_METHOD              dumps
               68  LOAD_FAST                'code'
               70  CALL_METHOD_1         1  ''
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          

 L. 616        76  LOAD_FAST                'data'
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 46


def decode_source(source_bytes):
    """Decode bytes representing source code and return the string.

    Universal newline support is used in the decoding.
    """
    import tokenize
    source_bytes_readline = _io.BytesIO(source_bytes).readline
    encoding = tokenize.detect_encoding(source_bytes_readline)
    newline_decoder = _io.IncrementalNewlineDecoder(None, True)
    return newline_decoder.decode(source_bytes.decode(encoding[0]))


_POPULATE = object()

def spec_from_file_location--- This code section failed: ---

 L. 648         0  LOAD_FAST                'location'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    58  'to 58'

 L. 652         8  LOAD_STR                 '<unknown>'
               10  STORE_FAST               'location'

 L. 653        12  LOAD_GLOBAL              hasattr
               14  LOAD_FAST                'loader'
               16  LOAD_STR                 'get_filename'
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE    68  'to 68'

 L. 655        22  SETUP_FINALLY        38  'to 38'

 L. 656        24  LOAD_FAST                'loader'
               26  LOAD_METHOD              get_filename
               28  LOAD_FAST                'name'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'location'
               34  POP_BLOCK        
               36  JUMP_ABSOLUTE        68  'to 68'
             38_0  COME_FROM_FINALLY    22  '22'

 L. 657        38  DUP_TOP          
               40  LOAD_GLOBAL              ImportError
               42  <121>                54  ''
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 658        50  POP_EXCEPT       
               52  JUMP_ABSOLUTE        68  'to 68'
               54  <48>             
               56  JUMP_FORWARD         68  'to 68'
             58_0  COME_FROM             6  '6'

 L. 660        58  LOAD_GLOBAL              _os
               60  LOAD_METHOD              fspath
               62  LOAD_FAST                'location'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'location'
             68_0  COME_FROM_EXCEPT_CLAUSE    56  '56'
             68_1  COME_FROM_EXCEPT_CLAUSE    52  '52'
             68_2  COME_FROM_EXCEPT_CLAUSE    20  '20'

 L. 668        68  LOAD_GLOBAL              _bootstrap
               70  LOAD_ATTR                ModuleSpec
               72  LOAD_FAST                'name'
               74  LOAD_FAST                'loader'
               76  LOAD_FAST                'location'
               78  LOAD_CONST               ('origin',)
               80  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               82  STORE_FAST               'spec'

 L. 669        84  LOAD_CONST               True
               86  LOAD_FAST                'spec'
               88  STORE_ATTR               _set_fileattr

 L. 672        90  LOAD_FAST                'loader'
               92  LOAD_CONST               None
               94  <117>                 0  ''
               96  POP_JUMP_IF_FALSE   152  'to 152'

 L. 673        98  LOAD_GLOBAL              _get_supported_file_loaders
              100  CALL_FUNCTION_0       0  ''
              102  GET_ITER         
            104_0  COME_FROM           124  '124'
              104  FOR_ITER            148  'to 148'
              106  UNPACK_SEQUENCE_2     2 
              108  STORE_FAST               'loader_class'
              110  STORE_FAST               'suffixes'

 L. 674       112  LOAD_FAST                'location'
              114  LOAD_METHOD              endswith
              116  LOAD_GLOBAL              tuple
              118  LOAD_FAST                'suffixes'
              120  CALL_FUNCTION_1       1  ''
              122  CALL_METHOD_1         1  ''
              124  POP_JUMP_IF_FALSE   104  'to 104'

 L. 675       126  LOAD_FAST                'loader_class'
              128  LOAD_FAST                'name'
              130  LOAD_FAST                'location'
              132  CALL_FUNCTION_2       2  ''
              134  STORE_FAST               'loader'

 L. 676       136  LOAD_FAST                'loader'
              138  LOAD_FAST                'spec'
              140  STORE_ATTR               loader

 L. 677       142  POP_TOP          
              144  BREAK_LOOP          152  'to 152'
              146  JUMP_BACK           104  'to 104'

 L. 679       148  LOAD_CONST               None
              150  RETURN_VALUE     
            152_0  COME_FROM            96  '96'

 L. 682       152  LOAD_FAST                'submodule_search_locations'
              154  LOAD_GLOBAL              _POPULATE
              156  <117>                 0  ''
              158  POP_JUMP_IF_FALSE   216  'to 216'

 L. 684       160  LOAD_GLOBAL              hasattr
              162  LOAD_FAST                'loader'
              164  LOAD_STR                 'is_package'
              166  CALL_FUNCTION_2       2  ''
              168  POP_JUMP_IF_FALSE   222  'to 222'

 L. 685       170  SETUP_FINALLY       186  'to 186'

 L. 686       172  LOAD_FAST                'loader'
              174  LOAD_METHOD              is_package
              176  LOAD_FAST                'name'
              178  CALL_METHOD_1         1  ''
              180  STORE_FAST               'is_package'
              182  POP_BLOCK        
              184  JUMP_FORWARD        204  'to 204'
            186_0  COME_FROM_FINALLY   170  '170'

 L. 687       186  DUP_TOP          
              188  LOAD_GLOBAL              ImportError
              190  <121>               202  ''
              192  POP_TOP          
              194  POP_TOP          
              196  POP_TOP          

 L. 688       198  POP_EXCEPT       
              200  JUMP_ABSOLUTE       222  'to 222'
              202  <48>             
            204_0  COME_FROM           184  '184'

 L. 690       204  LOAD_FAST                'is_package'
              206  POP_JUMP_IF_FALSE   222  'to 222'

 L. 691       208  BUILD_LIST_0          0 
              210  LOAD_FAST                'spec'
              212  STORE_ATTR               submodule_search_locations
              214  JUMP_FORWARD        222  'to 222'
            216_0  COME_FROM           158  '158'

 L. 693       216  LOAD_FAST                'submodule_search_locations'
              218  LOAD_FAST                'spec'
              220  STORE_ATTR               submodule_search_locations
            222_0  COME_FROM_EXCEPT_CLAUSE   214  '214'
            222_1  COME_FROM_EXCEPT_CLAUSE   206  '206'
            222_2  COME_FROM_EXCEPT_CLAUSE   200  '200'
            222_3  COME_FROM_EXCEPT_CLAUSE   168  '168'

 L. 694       222  LOAD_FAST                'spec'
              224  LOAD_ATTR                submodule_search_locations
              226  BUILD_LIST_0          0 
              228  COMPARE_OP               ==
          230_232  POP_JUMP_IF_FALSE   264  'to 264'

 L. 695       234  LOAD_FAST                'location'
          236_238  POP_JUMP_IF_FALSE   264  'to 264'

 L. 696       240  LOAD_GLOBAL              _path_split
              242  LOAD_FAST                'location'
              244  CALL_FUNCTION_1       1  ''
              246  LOAD_CONST               0
              248  BINARY_SUBSCR    
              250  STORE_FAST               'dirname'

 L. 697       252  LOAD_FAST                'spec'
              254  LOAD_ATTR                submodule_search_locations
              256  LOAD_METHOD              append
              258  LOAD_FAST                'dirname'
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          
            264_0  COME_FROM           236  '236'
            264_1  COME_FROM           230  '230'

 L. 699       264  LOAD_FAST                'spec'
              266  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class WindowsRegistryFinder:
    __doc__ = 'Meta path finder for modules declared in the Windows registry.'
    REGISTRY_KEY = 'Software\\Python\\PythonCore\\{sys_version}\\Modules\\{fullname}'
    REGISTRY_KEY_DEBUG = 'Software\\Python\\PythonCore\\{sys_version}\\Modules\\{fullname}\\Debug'
    DEBUG_BUILD = False

    @classmethod
    def _open_registry--- This code section failed: ---

 L. 718         0  SETUP_FINALLY        18  'to 18'

 L. 719         2  LOAD_GLOBAL              winreg
                4  LOAD_METHOD              OpenKey
                6  LOAD_GLOBAL              winreg
                8  LOAD_ATTR                HKEY_CURRENT_USER
               10  LOAD_FAST                'key'
               12  CALL_METHOD_2         2  ''
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 720        18  DUP_TOP          
               20  LOAD_GLOBAL              OSError
               22  <121>                48  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 721        30  LOAD_GLOBAL              winreg
               32  LOAD_METHOD              OpenKey
               34  LOAD_GLOBAL              winreg
               36  LOAD_ATTR                HKEY_LOCAL_MACHINE
               38  LOAD_FAST                'key'
               40  CALL_METHOD_2         2  ''
               42  ROT_FOUR         
               44  POP_EXCEPT       
               46  RETURN_VALUE     
               48  <48>             

Parse error at or near `<121>' instruction at offset 22

    @classmethod
    def _search_registry--- This code section failed: ---

 L. 725         0  LOAD_FAST                'cls'
                2  LOAD_ATTR                DEBUG_BUILD
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L. 726         6  LOAD_FAST                'cls'
                8  LOAD_ATTR                REGISTRY_KEY_DEBUG
               10  STORE_FAST               'registry_key'
               12  JUMP_FORWARD         20  'to 20'
             14_0  COME_FROM             4  '4'

 L. 728        14  LOAD_FAST                'cls'
               16  LOAD_ATTR                REGISTRY_KEY
               18  STORE_FAST               'registry_key'
             20_0  COME_FROM            12  '12'

 L. 729        20  LOAD_FAST                'registry_key'
               22  LOAD_ATTR                format
               24  LOAD_FAST                'fullname'

 L. 730        26  LOAD_STR                 '%d.%d'
               28  LOAD_GLOBAL              sys
               30  LOAD_ATTR                version_info
               32  LOAD_CONST               None
               34  LOAD_CONST               2
               36  BUILD_SLICE_2         2 
               38  BINARY_SUBSCR    
               40  BINARY_MODULO    

 L. 729        42  LOAD_CONST               ('fullname', 'sys_version')
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  STORE_FAST               'key'

 L. 731        48  SETUP_FINALLY       108  'to 108'

 L. 732        50  LOAD_FAST                'cls'
               52  LOAD_METHOD              _open_registry
               54  LOAD_FAST                'key'
               56  CALL_METHOD_1         1  ''
               58  SETUP_WITH           88  'to 88'
               60  STORE_FAST               'hkey'

 L. 733        62  LOAD_GLOBAL              winreg
               64  LOAD_METHOD              QueryValue
               66  LOAD_FAST                'hkey'
               68  LOAD_STR                 ''
               70  CALL_METHOD_2         2  ''
               72  STORE_FAST               'filepath'
               74  POP_BLOCK        
               76  LOAD_CONST               None
               78  DUP_TOP          
               80  DUP_TOP          
               82  CALL_FUNCTION_3       3  ''
               84  POP_TOP          
               86  JUMP_FORWARD        104  'to 104'
             88_0  COME_FROM_WITH       58  '58'
               88  <49>             
               90  POP_JUMP_IF_TRUE     94  'to 94'
               92  <48>             
             94_0  COME_FROM            90  '90'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          
              100  POP_EXCEPT       
              102  POP_TOP          
            104_0  COME_FROM            86  '86'
              104  POP_BLOCK        
              106  JUMP_FORWARD        128  'to 128'
            108_0  COME_FROM_FINALLY    48  '48'

 L. 734       108  DUP_TOP          
              110  LOAD_GLOBAL              OSError
              112  <121>               126  ''
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 735       120  POP_EXCEPT       
              122  LOAD_CONST               None
              124  RETURN_VALUE     
              126  <48>             
            128_0  COME_FROM           106  '106'

 L. 736       128  LOAD_FAST                'filepath'
              130  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 78

    @classmethod
    def find_spec--- This code section failed: ---

 L. 740         0  LOAD_FAST                'cls'
                2  LOAD_METHOD              _search_registry
                4  LOAD_FAST                'fullname'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'filepath'

 L. 741        10  LOAD_FAST                'filepath'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 742        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 743        22  SETUP_FINALLY        36  'to 36'

 L. 744        24  LOAD_GLOBAL              _path_stat
               26  LOAD_FAST                'filepath'
               28  CALL_FUNCTION_1       1  ''
               30  POP_TOP          
               32  POP_BLOCK        
               34  JUMP_FORWARD         56  'to 56'
             36_0  COME_FROM_FINALLY    22  '22'

 L. 745        36  DUP_TOP          
               38  LOAD_GLOBAL              OSError
               40  <121>                54  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 746        48  POP_EXCEPT       
               50  LOAD_CONST               None
               52  RETURN_VALUE     
               54  <48>             
             56_0  COME_FROM            34  '34'

 L. 747        56  LOAD_GLOBAL              _get_supported_file_loaders
               58  CALL_FUNCTION_0       0  ''
               60  GET_ITER         
             62_0  COME_FROM            82  '82'
               62  FOR_ITER            116  'to 116'
               64  UNPACK_SEQUENCE_2     2 
               66  STORE_FAST               'loader'
               68  STORE_FAST               'suffixes'

 L. 748        70  LOAD_FAST                'filepath'
               72  LOAD_METHOD              endswith
               74  LOAD_GLOBAL              tuple
               76  LOAD_FAST                'suffixes'
               78  CALL_FUNCTION_1       1  ''
               80  CALL_METHOD_1         1  ''
               82  POP_JUMP_IF_FALSE    62  'to 62'

 L. 749        84  LOAD_GLOBAL              _bootstrap
               86  LOAD_ATTR                spec_from_loader
               88  LOAD_FAST                'fullname'

 L. 750        90  LOAD_FAST                'loader'
               92  LOAD_FAST                'fullname'
               94  LOAD_FAST                'filepath'
               96  CALL_FUNCTION_2       2  ''

 L. 751        98  LOAD_FAST                'filepath'

 L. 749       100  LOAD_CONST               ('origin',)
              102  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              104  STORE_FAST               'spec'

 L. 752       106  LOAD_FAST                'spec'
              108  ROT_TWO          
              110  POP_TOP          
              112  RETURN_VALUE     
              114  JUMP_BACK            62  'to 62'

Parse error at or near `<117>' instruction at offset 14

    @classmethod
    def find_module--- This code section failed: ---

 L. 761         0  LOAD_FAST                'cls'
                2  LOAD_METHOD              find_spec
                4  LOAD_FAST                'fullname'
                6  LOAD_FAST                'path'
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'spec'

 L. 762        12  LOAD_FAST                'spec'
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    26  'to 26'

 L. 763        20  LOAD_FAST                'spec'
               22  LOAD_ATTR                loader
               24  RETURN_VALUE     
             26_0  COME_FROM            18  '18'

 L. 765        26  LOAD_CONST               None
               28  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 16


class _LoaderBasics:
    __doc__ = 'Base class of common code needed by both SourceLoader and\n    SourcelessFileLoader.'

    def is_package(self, fullname):
        """Concrete implementation of InspectLoader.is_package by checking if
        the path returned by get_filename has a filename of '__init__.py'."""
        filename = _path_split(self.get_filename(fullname))[1]
        filename_base = filename.rsplit('.', 1)[0]
        tail_name = fullname.rpartition('.')[2]
        return filename_base == '__init__' and tail_name != '__init__'

    def create_module(self, spec):
        """Use default semantics for module creation."""
        pass

    def exec_module--- This code section failed: ---

 L. 786         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_code
                4  LOAD_FAST                'module'
                6  LOAD_ATTR                __name__
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'code'

 L. 787        12  LOAD_FAST                'code'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    36  'to 36'

 L. 788        20  LOAD_GLOBAL              ImportError
               22  LOAD_STR                 'cannot load module {!r} when get_code() returns None'
               24  LOAD_METHOD              format

 L. 789        26  LOAD_FAST                'module'
               28  LOAD_ATTR                __name__

 L. 788        30  CALL_METHOD_1         1  ''
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            18  '18'

 L. 790        36  LOAD_GLOBAL              _bootstrap
               38  LOAD_METHOD              _call_with_frames_removed
               40  LOAD_GLOBAL              exec
               42  LOAD_FAST                'code'
               44  LOAD_FAST                'module'
               46  LOAD_ATTR                __dict__
               48  CALL_METHOD_3         3  ''
               50  POP_TOP          

Parse error at or near `<117>' instruction at offset 16

    def load_module(self, fullname):
        """This module is deprecated."""
        return _bootstrap._load_module_shim(self, fullname)


class SourceLoader(_LoaderBasics):

    def path_mtime(self, path):
        """Optional method that returns the modification time (an int) for the
        specified path (a str).

        Raises OSError when the path cannot be handled.
        """
        raise OSError

    def path_stats(self, path):
        """Optional method returning a metadata dict for the specified
        path (a str).

        Possible keys:
        - 'mtime' (mandatory) is the numeric timestamp of last source
          code modification;
        - 'size' (optional) is the size in bytes of the source code.

        Implementing this method allows the loader to read bytecode files.
        Raises OSError when the path cannot be handled.
        """
        return {'mtime': self.path_mtime(path)}

    def _cache_bytecode(self, source_path, cache_path, data):
        """Optional method which writes data (bytes) to a file path (a str).

        Implementing this method allows for the writing of bytecode files.

        The source path is needed in order to correctly transfer permissions
        """
        return self.set_data(cache_path, data)

    def set_data(self, path, data):
        """Optional method which writes data (bytes) to a file path (a str).

        Implementing this method allows for the writing of bytecode files.
        """
        pass

    def get_source--- This code section failed: ---

 L. 840         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_filename
                4  LOAD_FAST                'fullname'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'path'

 L. 841        10  SETUP_FINALLY        26  'to 26'

 L. 842        12  LOAD_FAST                'self'
               14  LOAD_METHOD              get_data
               16  LOAD_FAST                'path'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'source_bytes'
               22  POP_BLOCK        
               24  JUMP_FORWARD         76  'to 76'
             26_0  COME_FROM_FINALLY    10  '10'

 L. 843        26  DUP_TOP          
               28  LOAD_GLOBAL              OSError
               30  <121>                74  ''
               32  POP_TOP          
               34  STORE_FAST               'exc'
               36  POP_TOP          
               38  SETUP_FINALLY        66  'to 66'

 L. 844        40  LOAD_GLOBAL              ImportError
               42  LOAD_STR                 'source not available through get_data()'

 L. 845        44  LOAD_FAST                'fullname'

 L. 844        46  LOAD_CONST               ('name',)
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 845        50  LOAD_FAST                'exc'

 L. 844        52  RAISE_VARARGS_2       2  'exception instance with __cause__'
               54  POP_BLOCK        
               56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  STORE_FAST               'exc'
               62  DELETE_FAST              'exc'
               64  JUMP_FORWARD         76  'to 76'
             66_0  COME_FROM_FINALLY    38  '38'
               66  LOAD_CONST               None
               68  STORE_FAST               'exc'
               70  DELETE_FAST              'exc'
               72  <48>             
               74  <48>             
             76_0  COME_FROM            64  '64'
             76_1  COME_FROM            24  '24'

 L. 846        76  LOAD_GLOBAL              decode_source
               78  LOAD_FAST                'source_bytes'
               80  CALL_FUNCTION_1       1  ''
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 30

    def source_to_code(self, data, path, *, _optimize=-1):
        """Return the code object compiled from source.

        The 'data' argument can be any object type that compile() supports.
        """
        return _bootstrap._call_with_frames_removed(compile, data, path, 'exec', dont_inherit=True,
          optimize=_optimize)

    def get_code--- This code section failed: ---

 L. 863         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_filename
                4  LOAD_FAST                'fullname'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'source_path'

 L. 864        10  LOAD_CONST               None
               12  STORE_FAST               'source_mtime'

 L. 865        14  LOAD_CONST               None
               16  STORE_FAST               'source_bytes'

 L. 866        18  LOAD_CONST               None
               20  STORE_FAST               'source_hash'

 L. 867        22  LOAD_CONST               False
               24  STORE_FAST               'hash_based'

 L. 868        26  LOAD_CONST               True
               28  STORE_FAST               'check_source'

 L. 869        30  SETUP_FINALLY        44  'to 44'

 L. 870        32  LOAD_GLOBAL              cache_from_source
               34  LOAD_FAST                'source_path'
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'bytecode_path'
               40  POP_BLOCK        
               42  JUMP_FORWARD         68  'to 68'
             44_0  COME_FROM_FINALLY    30  '30'

 L. 871        44  DUP_TOP          
               46  LOAD_GLOBAL              NotImplementedError
               48  <121>                66  ''
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 872        56  LOAD_CONST               None
               58  STORE_FAST               'bytecode_path'
               60  POP_EXCEPT       
            62_64  JUMP_FORWARD        364  'to 364'
               66  <48>             
             68_0  COME_FROM            42  '42'

 L. 874        68  SETUP_FINALLY        84  'to 84'

 L. 875        70  LOAD_FAST                'self'
               72  LOAD_METHOD              path_stats
               74  LOAD_FAST                'source_path'
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'st'
               80  POP_BLOCK        
               82  JUMP_FORWARD        104  'to 104'
             84_0  COME_FROM_FINALLY    68  '68'

 L. 876        84  DUP_TOP          
               86  LOAD_GLOBAL              OSError
               88  <121>               102  ''
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 877        96  POP_EXCEPT       
           98_100  JUMP_FORWARD        364  'to 364'
              102  <48>             
            104_0  COME_FROM            82  '82'

 L. 879       104  LOAD_GLOBAL              int
              106  LOAD_FAST                'st'
              108  LOAD_STR                 'mtime'
              110  BINARY_SUBSCR    
              112  CALL_FUNCTION_1       1  ''
              114  STORE_FAST               'source_mtime'

 L. 880       116  SETUP_FINALLY       132  'to 132'

 L. 881       118  LOAD_FAST                'self'
              120  LOAD_METHOD              get_data
              122  LOAD_FAST                'bytecode_path'
              124  CALL_METHOD_1         1  ''
              126  STORE_FAST               'data'
              128  POP_BLOCK        
              130  JUMP_FORWARD        150  'to 150'
            132_0  COME_FROM_FINALLY   116  '116'

 L. 882       132  DUP_TOP          
              134  LOAD_GLOBAL              OSError
              136  <121>               148  ''
              138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L. 883       144  POP_EXCEPT       
              146  JUMP_FORWARD        364  'to 364'
              148  <48>             
            150_0  COME_FROM           130  '130'

 L. 886       150  LOAD_FAST                'fullname'

 L. 887       152  LOAD_FAST                'bytecode_path'

 L. 885       154  LOAD_CONST               ('name', 'path')
              156  BUILD_CONST_KEY_MAP_2     2 
              158  STORE_FAST               'exc_details'

 L. 889       160  SETUP_FINALLY       310  'to 310'

 L. 890       162  LOAD_GLOBAL              _classify_pyc
              164  LOAD_FAST                'data'
              166  LOAD_FAST                'fullname'
              168  LOAD_FAST                'exc_details'
              170  CALL_FUNCTION_3       3  ''
              172  STORE_FAST               'flags'

 L. 891       174  LOAD_GLOBAL              memoryview
              176  LOAD_FAST                'data'
              178  CALL_FUNCTION_1       1  ''
              180  LOAD_CONST               16
              182  LOAD_CONST               None
              184  BUILD_SLICE_2         2 
              186  BINARY_SUBSCR    
              188  STORE_FAST               'bytes_data'

 L. 892       190  LOAD_FAST                'flags'
              192  LOAD_CONST               1
              194  BINARY_AND       
              196  LOAD_CONST               0
              198  COMPARE_OP               !=
              200  STORE_FAST               'hash_based'

 L. 893       202  LOAD_FAST                'hash_based'
          204_206  POP_JUMP_IF_FALSE   286  'to 286'

 L. 894       208  LOAD_FAST                'flags'
              210  LOAD_CONST               2
              212  BINARY_AND       
              214  LOAD_CONST               0
              216  COMPARE_OP               !=
              218  STORE_FAST               'check_source'

 L. 895       220  LOAD_GLOBAL              _imp
              222  LOAD_ATTR                check_hash_based_pycs
              224  LOAD_STR                 'never'
              226  COMPARE_OP               !=
          228_230  POP_JUMP_IF_FALSE   306  'to 306'

 L. 896       232  LOAD_FAST                'check_source'

 L. 895       234  POP_JUMP_IF_TRUE    248  'to 248'

 L. 897       236  LOAD_GLOBAL              _imp
              238  LOAD_ATTR                check_hash_based_pycs
              240  LOAD_STR                 'always'
              242  COMPARE_OP               ==

 L. 895   244_246  POP_JUMP_IF_FALSE   306  'to 306'
            248_0  COME_FROM           234  '234'

 L. 898       248  LOAD_FAST                'self'
              250  LOAD_METHOD              get_data
              252  LOAD_FAST                'source_path'
              254  CALL_METHOD_1         1  ''
              256  STORE_FAST               'source_bytes'

 L. 899       258  LOAD_GLOBAL              _imp
              260  LOAD_METHOD              source_hash

 L. 900       262  LOAD_GLOBAL              _RAW_MAGIC_NUMBER

 L. 901       264  LOAD_FAST                'source_bytes'

 L. 899       266  CALL_METHOD_2         2  ''
              268  STORE_FAST               'source_hash'

 L. 903       270  LOAD_GLOBAL              _validate_hash_pyc
              272  LOAD_FAST                'data'
              274  LOAD_FAST                'source_hash'
              276  LOAD_FAST                'fullname'

 L. 904       278  LOAD_FAST                'exc_details'

 L. 903       280  CALL_FUNCTION_4       4  ''
              282  POP_TOP          
              284  JUMP_FORWARD        306  'to 306'
            286_0  COME_FROM           204  '204'

 L. 906       286  LOAD_GLOBAL              _validate_timestamp_pyc

 L. 907       288  LOAD_FAST                'data'

 L. 908       290  LOAD_FAST                'source_mtime'

 L. 909       292  LOAD_FAST                'st'
              294  LOAD_STR                 'size'
              296  BINARY_SUBSCR    

 L. 910       298  LOAD_FAST                'fullname'

 L. 911       300  LOAD_FAST                'exc_details'

 L. 906       302  CALL_FUNCTION_5       5  ''
              304  POP_TOP          
            306_0  COME_FROM           284  '284'
            306_1  COME_FROM           244  '244'
            306_2  COME_FROM           228  '228'
              306  POP_BLOCK        
              308  JUMP_FORWARD        334  'to 334'
            310_0  COME_FROM_FINALLY   160  '160'

 L. 913       310  DUP_TOP          
              312  LOAD_GLOBAL              ImportError
              314  LOAD_GLOBAL              EOFError
              316  BUILD_TUPLE_2         2 
          318_320  <121>               332  ''
              322  POP_TOP          
              324  POP_TOP          
              326  POP_TOP          

 L. 914       328  POP_EXCEPT       
              330  JUMP_FORWARD        364  'to 364'
              332  <48>             
            334_0  COME_FROM           308  '308'

 L. 916       334  LOAD_GLOBAL              _bootstrap
              336  LOAD_METHOD              _verbose_message
              338  LOAD_STR                 '{} matches {}'
              340  LOAD_FAST                'bytecode_path'

 L. 917       342  LOAD_FAST                'source_path'

 L. 916       344  CALL_METHOD_3         3  ''
              346  POP_TOP          

 L. 918       348  LOAD_GLOBAL              _compile_bytecode
              350  LOAD_FAST                'bytes_data'
              352  LOAD_FAST                'fullname'

 L. 919       354  LOAD_FAST                'bytecode_path'

 L. 920       356  LOAD_FAST                'source_path'

 L. 918       358  LOAD_CONST               ('name', 'bytecode_path', 'source_path')
              360  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              362  RETURN_VALUE     
            364_0  COME_FROM           330  '330'
            364_1  COME_FROM           146  '146'
            364_2  COME_FROM            98  '98'
            364_3  COME_FROM            62  '62'

 L. 921       364  LOAD_FAST                'source_bytes'
              366  LOAD_CONST               None
              368  <117>                 0  ''
          370_372  POP_JUMP_IF_FALSE   384  'to 384'

 L. 922       374  LOAD_FAST                'self'
              376  LOAD_METHOD              get_data
              378  LOAD_FAST                'source_path'
              380  CALL_METHOD_1         1  ''
              382  STORE_FAST               'source_bytes'
            384_0  COME_FROM           370  '370'

 L. 923       384  LOAD_FAST                'self'
              386  LOAD_METHOD              source_to_code
              388  LOAD_FAST                'source_bytes'
              390  LOAD_FAST                'source_path'
              392  CALL_METHOD_2         2  ''
              394  STORE_FAST               'code_object'

 L. 924       396  LOAD_GLOBAL              _bootstrap
              398  LOAD_METHOD              _verbose_message
              400  LOAD_STR                 'code object from {}'
              402  LOAD_FAST                'source_path'
              404  CALL_METHOD_2         2  ''
              406  POP_TOP          

 L. 925       408  LOAD_GLOBAL              sys
              410  LOAD_ATTR                dont_write_bytecode
          412_414  POP_JUMP_IF_TRUE    532  'to 532'
              416  LOAD_FAST                'bytecode_path'
              418  LOAD_CONST               None
              420  <117>                 1  ''
          422_424  POP_JUMP_IF_FALSE   532  'to 532'

 L. 926       426  LOAD_FAST                'source_mtime'
              428  LOAD_CONST               None
              430  <117>                 1  ''

 L. 925   432_434  POP_JUMP_IF_FALSE   532  'to 532'

 L. 927       436  LOAD_FAST                'hash_based'
          438_440  POP_JUMP_IF_FALSE   476  'to 476'

 L. 928       442  LOAD_FAST                'source_hash'
              444  LOAD_CONST               None
              446  <117>                 0  ''
          448_450  POP_JUMP_IF_FALSE   462  'to 462'

 L. 929       452  LOAD_GLOBAL              _imp
              454  LOAD_METHOD              source_hash
              456  LOAD_FAST                'source_bytes'
              458  CALL_METHOD_1         1  ''
              460  STORE_FAST               'source_hash'
            462_0  COME_FROM           448  '448'

 L. 930       462  LOAD_GLOBAL              _code_to_hash_pyc
              464  LOAD_FAST                'code_object'
              466  LOAD_FAST                'source_hash'
              468  LOAD_FAST                'check_source'
              470  CALL_FUNCTION_3       3  ''
              472  STORE_FAST               'data'
              474  JUMP_FORWARD        492  'to 492'
            476_0  COME_FROM           438  '438'

 L. 932       476  LOAD_GLOBAL              _code_to_timestamp_pyc
              478  LOAD_FAST                'code_object'
              480  LOAD_FAST                'source_mtime'

 L. 933       482  LOAD_GLOBAL              len
              484  LOAD_FAST                'source_bytes'
              486  CALL_FUNCTION_1       1  ''

 L. 932       488  CALL_FUNCTION_3       3  ''
              490  STORE_FAST               'data'
            492_0  COME_FROM           474  '474'

 L. 934       492  SETUP_FINALLY       512  'to 512'

 L. 935       494  LOAD_FAST                'self'
              496  LOAD_METHOD              _cache_bytecode
              498  LOAD_FAST                'source_path'
              500  LOAD_FAST                'bytecode_path'
              502  LOAD_FAST                'data'
              504  CALL_METHOD_3         3  ''
              506  POP_TOP          
              508  POP_BLOCK        
              510  JUMP_FORWARD        532  'to 532'
            512_0  COME_FROM_FINALLY   492  '492'

 L. 936       512  DUP_TOP          
              514  LOAD_GLOBAL              NotImplementedError
          516_518  <121>               530  ''
              520  POP_TOP          
              522  POP_TOP          
              524  POP_TOP          

 L. 937       526  POP_EXCEPT       
              528  JUMP_FORWARD        532  'to 532'
              530  <48>             
            532_0  COME_FROM           528  '528'
            532_1  COME_FROM           510  '510'
            532_2  COME_FROM           432  '432'
            532_3  COME_FROM           422  '422'
            532_4  COME_FROM           412  '412'

 L. 938       532  LOAD_FAST                'code_object'
              534  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 48


class FileLoader:
    __doc__ = 'Base file loader class which implements the loader protocol methods that\n    require file system usage.'

    def __init__(self, fullname, path):
        """Cache the module name and the path to the file found by the
        finder."""
        self.name = fullname
        self.path = path

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.name) ^ hash(self.path)

    @_check_name
    def load_module(self, fullname):
        return super(FileLoader, self).load_module(fullname)

    @_check_name
    def get_filename(self, fullname):
        """Return the path to the source file as found by the finder."""
        return self.path

    def get_data--- This code section failed: ---

 L. 978         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'self'
                4  LOAD_GLOBAL              SourceLoader
                6  LOAD_GLOBAL              ExtensionFileLoader
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    70  'to 70'

 L. 979        14  LOAD_GLOBAL              _io
               16  LOAD_METHOD              open_code
               18  LOAD_GLOBAL              str
               20  LOAD_FAST                'path'
               22  CALL_FUNCTION_1       1  ''
               24  CALL_METHOD_1         1  ''
               26  SETUP_WITH           52  'to 52'
               28  STORE_FAST               'file'

 L. 980        30  LOAD_FAST                'file'
               32  LOAD_METHOD              read
               34  CALL_METHOD_0         0  ''
               36  POP_BLOCK        
               38  ROT_TWO          
               40  LOAD_CONST               None
               42  DUP_TOP          
               44  DUP_TOP          
               46  CALL_FUNCTION_3       3  ''
               48  POP_TOP          
               50  RETURN_VALUE     
             52_0  COME_FROM_WITH       26  '26'
               52  <49>             
               54  POP_JUMP_IF_TRUE     58  'to 58'
               56  <48>             
             58_0  COME_FROM            54  '54'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          
               64  POP_EXCEPT       
               66  POP_TOP          
               68  JUMP_FORWARD        122  'to 122'
             70_0  COME_FROM            12  '12'

 L. 982        70  LOAD_GLOBAL              _io
               72  LOAD_METHOD              FileIO
               74  LOAD_FAST                'path'
               76  LOAD_STR                 'r'
               78  CALL_METHOD_2         2  ''
               80  SETUP_WITH          106  'to 106'
               82  STORE_FAST               'file'

 L. 983        84  LOAD_FAST                'file'
               86  LOAD_METHOD              read
               88  CALL_METHOD_0         0  ''
               90  POP_BLOCK        
               92  ROT_TWO          
               94  LOAD_CONST               None
               96  DUP_TOP          
               98  DUP_TOP          
              100  CALL_FUNCTION_3       3  ''
              102  POP_TOP          
              104  RETURN_VALUE     
            106_0  COME_FROM_WITH       80  '80'
              106  <49>             
              108  POP_JUMP_IF_TRUE    112  'to 112'
              110  <48>             
            112_0  COME_FROM           108  '108'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          
              118  POP_EXCEPT       
              120  POP_TOP          
            122_0  COME_FROM            68  '68'

Parse error at or near `ROT_TWO' instruction at offset 38

    @_check_name
    def get_resource_reader(self, module):
        if self.is_package(module):
            return self

    def open_resource(self, resource):
        path = _path_join(_path_split(self.path)[0], resource)
        return _io.FileIO(path, 'r')

    def resource_path(self, resource):
        if not self.is_resource(resource):
            raise FileNotFoundError
        path = _path_join(_path_split(self.path)[0], resource)
        return path

    def is_resource--- This code section failed: ---

 L.1004         0  LOAD_GLOBAL              path_sep
                2  LOAD_FAST                'name'
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.1005         8  LOAD_CONST               False
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.1006        12  LOAD_GLOBAL              _path_join
               14  LOAD_GLOBAL              _path_split
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                path
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_CONST               0
               24  BINARY_SUBSCR    
               26  LOAD_FAST                'name'
               28  CALL_FUNCTION_2       2  ''
               30  STORE_FAST               'path'

 L.1007        32  LOAD_GLOBAL              _path_isfile
               34  LOAD_FAST                'path'
               36  CALL_FUNCTION_1       1  ''
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def contents(self):
        return iter(_os.listdir(_path_split(self.path)[0]))


class SourceFileLoader(FileLoader, SourceLoader):
    __doc__ = 'Concrete implementation of SourceLoader using the file system.'

    def path_stats(self, path):
        """Return the metadata for the path."""
        st = _path_stat(path)
        return {'mtime':st.st_mtime,  'size':st.st_size}

    def _cache_bytecode(self, source_path, bytecode_path, data):
        mode = _calc_mode(source_path)
        return self.set_data(bytecode_path, data, _mode=mode)

    def set_data--- This code section failed: ---

 L.1029         0  LOAD_GLOBAL              _path_split
                2  LOAD_FAST                'path'
                4  CALL_FUNCTION_1       1  ''
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'parent'
               10  STORE_FAST               'filename'

 L.1030        12  BUILD_LIST_0          0 
               14  STORE_FAST               'path_parts'

 L.1032        16  LOAD_FAST                'parent'
               18  POP_JUMP_IF_FALSE    52  'to 52'
               20  LOAD_GLOBAL              _path_isdir
               22  LOAD_FAST                'parent'
               24  CALL_FUNCTION_1       1  ''
               26  POP_JUMP_IF_TRUE     52  'to 52'

 L.1033        28  LOAD_GLOBAL              _path_split
               30  LOAD_FAST                'parent'
               32  CALL_FUNCTION_1       1  ''
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'parent'
               38  STORE_FAST               'part'

 L.1034        40  LOAD_FAST                'path_parts'
               42  LOAD_METHOD              append
               44  LOAD_FAST                'part'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
               50  JUMP_BACK            16  'to 16'
             52_0  COME_FROM            26  '26'
             52_1  COME_FROM            18  '18'

 L.1036        52  LOAD_GLOBAL              reversed
               54  LOAD_FAST                'path_parts'
               56  CALL_FUNCTION_1       1  ''
               58  GET_ITER         
               60  FOR_ITER            166  'to 166'
               62  STORE_FAST               'part'

 L.1037        64  LOAD_GLOBAL              _path_join
               66  LOAD_FAST                'parent'
               68  LOAD_FAST                'part'
               70  CALL_FUNCTION_2       2  ''
               72  STORE_FAST               'parent'

 L.1038        74  SETUP_FINALLY        90  'to 90'

 L.1039        76  LOAD_GLOBAL              _os
               78  LOAD_METHOD              mkdir
               80  LOAD_FAST                'parent'
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
               86  POP_BLOCK        
               88  JUMP_BACK            60  'to 60'
             90_0  COME_FROM_FINALLY    74  '74'

 L.1040        90  DUP_TOP          
               92  LOAD_GLOBAL              FileExistsError
               94  <121>               110  ''
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L.1042       102  POP_EXCEPT       
              104  JUMP_BACK            60  'to 60'
              106  POP_EXCEPT       
              108  JUMP_BACK            60  'to 60'

 L.1043       110  DUP_TOP          
              112  LOAD_GLOBAL              OSError
              114  <121>               162  ''
              116  POP_TOP          
              118  STORE_FAST               'exc'
              120  POP_TOP          
              122  SETUP_FINALLY       154  'to 154'

 L.1046       124  LOAD_GLOBAL              _bootstrap
              126  LOAD_METHOD              _verbose_message
              128  LOAD_STR                 'could not create {!r}: {!r}'

 L.1047       130  LOAD_FAST                'parent'
              132  LOAD_FAST                'exc'

 L.1046       134  CALL_METHOD_3         3  ''
              136  POP_TOP          

 L.1048       138  POP_BLOCK        
              140  POP_EXCEPT       
              142  LOAD_CONST               None
              144  STORE_FAST               'exc'
              146  DELETE_FAST              'exc'
              148  POP_TOP          
              150  LOAD_CONST               None
              152  RETURN_VALUE     
            154_0  COME_FROM_FINALLY   122  '122'
              154  LOAD_CONST               None
              156  STORE_FAST               'exc'
              158  DELETE_FAST              'exc'
              160  <48>             
              162  <48>             
              164  JUMP_BACK            60  'to 60'

 L.1049       166  SETUP_FINALLY       196  'to 196'

 L.1050       168  LOAD_GLOBAL              _write_atomic
              170  LOAD_FAST                'path'
              172  LOAD_FAST                'data'
              174  LOAD_FAST                '_mode'
              176  CALL_FUNCTION_3       3  ''
              178  POP_TOP          

 L.1051       180  LOAD_GLOBAL              _bootstrap
              182  LOAD_METHOD              _verbose_message
              184  LOAD_STR                 'created {!r}'
              186  LOAD_FAST                'path'
              188  CALL_METHOD_2         2  ''
              190  POP_TOP          
              192  POP_BLOCK        
              194  JUMP_FORWARD        248  'to 248'
            196_0  COME_FROM_FINALLY   166  '166'

 L.1052       196  DUP_TOP          
              198  LOAD_GLOBAL              OSError
          200_202  <121>               246  ''
              204  POP_TOP          
              206  STORE_FAST               'exc'
              208  POP_TOP          
              210  SETUP_FINALLY       238  'to 238'

 L.1054       212  LOAD_GLOBAL              _bootstrap
              214  LOAD_METHOD              _verbose_message
              216  LOAD_STR                 'could not create {!r}: {!r}'
              218  LOAD_FAST                'path'

 L.1055       220  LOAD_FAST                'exc'

 L.1054       222  CALL_METHOD_3         3  ''
              224  POP_TOP          
              226  POP_BLOCK        
              228  POP_EXCEPT       
              230  LOAD_CONST               None
              232  STORE_FAST               'exc'
              234  DELETE_FAST              'exc'
              236  JUMP_FORWARD        248  'to 248'
            238_0  COME_FROM_FINALLY   210  '210'
              238  LOAD_CONST               None
              240  STORE_FAST               'exc'
              242  DELETE_FAST              'exc'
              244  <48>             
              246  <48>             
            248_0  COME_FROM           236  '236'
            248_1  COME_FROM           194  '194'

Parse error at or near `<121>' instruction at offset 94


class SourcelessFileLoader(FileLoader, _LoaderBasics):
    __doc__ = 'Loader which handles sourceless file imports.'

    def get_code(self, fullname):
        path = self.get_filename(fullname)
        data = self.get_data(path)
        exc_details = {'name':fullname, 
         'path':path}
        _classify_pyc(data, fullname, exc_details)
        return _compile_bytecode((memoryview(data)[16:]),
          name=fullname,
          bytecode_path=path)

    def get_source(self, fullname):
        """Return None as there is no source code."""
        pass


EXTENSION_SUFFIXES = []

class ExtensionFileLoader(FileLoader, _LoaderBasics):
    __doc__ = 'Loader for extension modules.\n\n    The constructor is designed to work with FileFinder.\n\n    '

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.name) ^ hash(self.path)

    def create_module(self, spec):
        """Create an unitialized extension module"""
        module = _bootstrap._call_with_frames_removed(_imp.create_dynamic, spec)
        _bootstrap._verbose_message'extension module {!r} loaded from {!r}'spec.nameself.path
        return module

    def exec_module(self, module):
        """Initialize an extension module"""
        _bootstrap._call_with_frames_removed(_imp.exec_dynamic, module)
        _bootstrap._verbose_message'extension module {!r} executed from {!r}'self.nameself.path

    def is_package(self, fullname):
        """Return True if the extension module is a package."""
        file_name = _path_split(self.path)[1]
        return any((file_name == '__init__' + suffix for suffix in EXTENSION_SUFFIXES))

    def get_code(self, fullname):
        """Return None as an extension module cannot create a code object."""
        pass

    def get_source(self, fullname):
        """Return None as extension modules have no source code."""
        pass

    @_check_name
    def get_filename(self, fullname):
        """Return the path to the source file as found by the finder."""
        return self.path


class _NamespacePath:
    __doc__ = "Represents a namespace package's path.  It uses the module name\n    to find its parent module, and from there it looks up the parent's\n    __path__.  When this changes, the module's own path is recomputed,\n    using path_finder.  For top-level modules, the parent module's path\n    is sys.path."

    def __init__(self, name, path, path_finder):
        self._name = name
        self._path = path
        self._last_parent_path = tuple(self._get_parent_path())
        self._path_finder = path_finder

    def _find_parent_path_names(self):
        """Returns a tuple of (parent-module-name, parent-path-attr-name)"""
        parent, dot, me = self._name.rpartition('.')
        if dot == '':
            return ('sys', 'path')
        return (
         parent, '__path__')

    def _get_parent_path(self):
        parent_module_name, path_attr_name = self._find_parent_path_names()
        return getattr(sys.modules[parent_module_name], path_attr_name)

    def _recalculate--- This code section failed: ---

 L.1169         0  LOAD_GLOBAL              tuple
                2  LOAD_FAST                'self'
                4  LOAD_METHOD              _get_parent_path
                6  CALL_METHOD_0         0  ''
                8  CALL_FUNCTION_1       1  ''
               10  STORE_FAST               'parent_path'

 L.1170        12  LOAD_FAST                'parent_path'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _last_parent_path
               18  COMPARE_OP               !=
               20  POP_JUMP_IF_FALSE    74  'to 74'

 L.1171        22  LOAD_FAST                'self'
               24  LOAD_METHOD              _path_finder
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _name
               30  LOAD_FAST                'parent_path'
               32  CALL_METHOD_2         2  ''
               34  STORE_FAST               'spec'

 L.1174        36  LOAD_FAST                'spec'
               38  LOAD_CONST               None
               40  <117>                 1  ''
               42  POP_JUMP_IF_FALSE    68  'to 68'
               44  LOAD_FAST                'spec'
               46  LOAD_ATTR                loader
               48  LOAD_CONST               None
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE    68  'to 68'

 L.1175        54  LOAD_FAST                'spec'
               56  LOAD_ATTR                submodule_search_locations
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L.1176        60  LOAD_FAST                'spec'
               62  LOAD_ATTR                submodule_search_locations
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _path
             68_0  COME_FROM            58  '58'
             68_1  COME_FROM            52  '52'
             68_2  COME_FROM            42  '42'

 L.1177        68  LOAD_FAST                'parent_path'
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _last_parent_path
             74_0  COME_FROM            20  '20'

 L.1178        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _path
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 40

    def __iter__(self):
        return iter(self._recalculate())

    def __getitem__(self, index):
        return self._recalculate()[index]

    def __setitem__(self, index, path):
        self._path[index] = path

    def __len__(self):
        return len(self._recalculate())

    def __repr__(self):
        return '_NamespacePath({!r})'.format(self._path)

    def __contains__--- This code section failed: ---

 L.1196         0  LOAD_FAST                'item'
                2  LOAD_FAST                'self'
                4  LOAD_METHOD              _recalculate
                6  CALL_METHOD_0         0  ''
                8  <118>                 0  ''
               10  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def append(self, item):
        self._path.append(item)


class _NamespaceLoader:

    def __init__(self, name, path, path_finder):
        self._path = _NamespacePath(name, path, path_finder)

    @classmethod
    def module_repr(cls, module):
        """Return repr for the module.

        The method is deprecated.  The import machinery does the job itself.

        """
        return '<module {!r} (namespace)>'.format(module.__name__)

    def is_package(self, fullname):
        return True

    def get_source(self, fullname):
        return ''

    def get_code(self, fullname):
        return compile('', '<string>', 'exec', dont_inherit=True)

    def create_module(self, spec):
        """Use default semantics for module creation."""
        pass

    def exec_module(self, module):
        pass

    def load_module(self, fullname):
        """Load a namespace module.

        This method is deprecated.  Use exec_module() instead.

        """
        _bootstrap._verbose_message('namespace module loaded with path {!r}', self._path)
        return _bootstrap._load_module_shim(self, fullname)


class PathFinder:
    __doc__ = 'Meta path finder for sys.path and package __path__ attributes.'

    @classmethod
    def invalidate_caches--- This code section failed: ---

 L.1253         0  LOAD_GLOBAL              list
                2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                path_importer_cache
                6  LOAD_METHOD              items
                8  CALL_METHOD_0         0  ''
               10  CALL_FUNCTION_1       1  ''
               12  GET_ITER         
             14_0  COME_FROM            48  '48'
               14  FOR_ITER             60  'to 60'
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'name'
               20  STORE_FAST               'finder'

 L.1254        22  LOAD_FAST                'finder'
               24  LOAD_CONST               None
               26  <117>                 0  ''
               28  POP_JUMP_IF_FALSE    40  'to 40'

 L.1255        30  LOAD_GLOBAL              sys
               32  LOAD_ATTR                path_importer_cache
               34  LOAD_FAST                'name'
               36  DELETE_SUBSCR    
               38  JUMP_BACK            14  'to 14'
             40_0  COME_FROM            28  '28'

 L.1256        40  LOAD_GLOBAL              hasattr
               42  LOAD_FAST                'finder'
               44  LOAD_STR                 'invalidate_caches'
               46  CALL_FUNCTION_2       2  ''
               48  POP_JUMP_IF_FALSE    14  'to 14'

 L.1257        50  LOAD_FAST                'finder'
               52  LOAD_METHOD              invalidate_caches
               54  CALL_METHOD_0         0  ''
               56  POP_TOP          
               58  JUMP_BACK            14  'to 14'

Parse error at or near `<117>' instruction at offset 26

    @classmethod
    def _path_hooks--- This code section failed: ---

 L.1262         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                path_hooks
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'
               10  LOAD_GLOBAL              sys
               12  LOAD_ATTR                path_hooks
               14  POP_JUMP_IF_TRUE     28  'to 28'

 L.1263        16  LOAD_GLOBAL              _warnings
               18  LOAD_METHOD              warn
               20  LOAD_STR                 'sys.path_hooks is empty'
               22  LOAD_GLOBAL              ImportWarning
               24  CALL_METHOD_2         2  ''
               26  POP_TOP          
             28_0  COME_FROM            14  '14'
             28_1  COME_FROM             8  '8'

 L.1264        28  LOAD_GLOBAL              sys
               30  LOAD_ATTR                path_hooks
               32  GET_ITER         
               34  FOR_ITER             78  'to 78'
               36  STORE_FAST               'hook'

 L.1265        38  SETUP_FINALLY        54  'to 54'

 L.1266        40  LOAD_FAST                'hook'
               42  LOAD_FAST                'path'
               44  CALL_FUNCTION_1       1  ''
               46  POP_BLOCK        
               48  ROT_TWO          
               50  POP_TOP          
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY    38  '38'

 L.1267        54  DUP_TOP          
               56  LOAD_GLOBAL              ImportError
               58  <121>                74  ''
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.1268        66  POP_EXCEPT       
               68  JUMP_BACK            34  'to 34'
               70  POP_EXCEPT       
               72  JUMP_BACK            34  'to 34'
               74  <48>             
               76  JUMP_BACK            34  'to 34'

Parse error at or near `None' instruction at offset -1

    @classmethod
    def _path_importer_cache--- This code section failed: ---

 L.1280         0  LOAD_FAST                'path'
                2  LOAD_STR                 ''
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    42  'to 42'

 L.1281         8  SETUP_FINALLY        22  'to 22'

 L.1282        10  LOAD_GLOBAL              _os
               12  LOAD_METHOD              getcwd
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'path'
               18  POP_BLOCK        
               20  JUMP_FORWARD         42  'to 42'
             22_0  COME_FROM_FINALLY     8  '8'

 L.1283        22  DUP_TOP          
               24  LOAD_GLOBAL              FileNotFoundError
               26  <121>                40  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.1286        34  POP_EXCEPT       
               36  LOAD_CONST               None
               38  RETURN_VALUE     
               40  <48>             
             42_0  COME_FROM            20  '20'
             42_1  COME_FROM             6  '6'

 L.1287        42  SETUP_FINALLY        58  'to 58'

 L.1288        44  LOAD_GLOBAL              sys
               46  LOAD_ATTR                path_importer_cache
               48  LOAD_FAST                'path'
               50  BINARY_SUBSCR    
               52  STORE_FAST               'finder'
               54  POP_BLOCK        
               56  JUMP_FORWARD         96  'to 96'
             58_0  COME_FROM_FINALLY    42  '42'

 L.1289        58  DUP_TOP          
               60  LOAD_GLOBAL              KeyError
               62  <121>                94  ''
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L.1290        70  LOAD_FAST                'cls'
               72  LOAD_METHOD              _path_hooks
               74  LOAD_FAST                'path'
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'finder'

 L.1291        80  LOAD_FAST                'finder'
               82  LOAD_GLOBAL              sys
               84  LOAD_ATTR                path_importer_cache
               86  LOAD_FAST                'path'
               88  STORE_SUBSCR     
               90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
               94  <48>             
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            56  '56'

 L.1292        96  LOAD_FAST                'finder'
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 26

    @classmethod
    def _legacy_get_spec--- This code section failed: ---

 L.1298         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'finder'
                4  LOAD_STR                 'find_loader'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L.1299        10  LOAD_FAST                'finder'
               12  LOAD_METHOD              find_loader
               14  LOAD_FAST                'fullname'
               16  CALL_METHOD_1         1  ''
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'loader'
               22  STORE_FAST               'portions'
               24  JUMP_FORWARD         40  'to 40'
             26_0  COME_FROM             8  '8'

 L.1301        26  LOAD_FAST                'finder'
               28  LOAD_METHOD              find_module
               30  LOAD_FAST                'fullname'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'loader'

 L.1302        36  BUILD_LIST_0          0 
               38  STORE_FAST               'portions'
             40_0  COME_FROM            24  '24'

 L.1303        40  LOAD_FAST                'loader'
               42  LOAD_CONST               None
               44  <117>                 1  ''
               46  POP_JUMP_IF_FALSE    60  'to 60'

 L.1304        48  LOAD_GLOBAL              _bootstrap
               50  LOAD_METHOD              spec_from_loader
               52  LOAD_FAST                'fullname'
               54  LOAD_FAST                'loader'
               56  CALL_METHOD_2         2  ''
               58  RETURN_VALUE     
             60_0  COME_FROM            46  '46'

 L.1305        60  LOAD_GLOBAL              _bootstrap
               62  LOAD_METHOD              ModuleSpec
               64  LOAD_FAST                'fullname'
               66  LOAD_CONST               None
               68  CALL_METHOD_2         2  ''
               70  STORE_FAST               'spec'

 L.1306        72  LOAD_FAST                'portions'
               74  LOAD_FAST                'spec'
               76  STORE_ATTR               submodule_search_locations

 L.1307        78  LOAD_FAST                'spec'
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 44

    @classmethod
    def _get_spec--- This code section failed: ---

 L.1314         0  BUILD_LIST_0          0 
                2  STORE_FAST               'namespace_path'

 L.1315         4  LOAD_FAST                'path'
                6  GET_ITER         
              8_0  COME_FROM            44  '44'
                8  FOR_ITER            144  'to 144'
               10  STORE_FAST               'entry'

 L.1316        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'entry'
               16  LOAD_GLOBAL              str
               18  LOAD_GLOBAL              bytes
               20  BUILD_TUPLE_2         2 
               22  CALL_FUNCTION_2       2  ''
               24  POP_JUMP_IF_TRUE     28  'to 28'

 L.1317        26  JUMP_BACK             8  'to 8'
             28_0  COME_FROM            24  '24'

 L.1318        28  LOAD_FAST                'cls'
               30  LOAD_METHOD              _path_importer_cache
               32  LOAD_FAST                'entry'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'finder'

 L.1319        38  LOAD_FAST                'finder'
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE     8  'to 8'

 L.1320        46  LOAD_GLOBAL              hasattr
               48  LOAD_FAST                'finder'
               50  LOAD_STR                 'find_spec'
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_FALSE    70  'to 70'

 L.1321        56  LOAD_FAST                'finder'
               58  LOAD_METHOD              find_spec
               60  LOAD_FAST                'fullname'
               62  LOAD_FAST                'target'
               64  CALL_METHOD_2         2  ''
               66  STORE_FAST               'spec'
               68  JUMP_FORWARD         82  'to 82'
             70_0  COME_FROM            54  '54'

 L.1323        70  LOAD_FAST                'cls'
               72  LOAD_METHOD              _legacy_get_spec
               74  LOAD_FAST                'fullname'
               76  LOAD_FAST                'finder'
               78  CALL_METHOD_2         2  ''
               80  STORE_FAST               'spec'
             82_0  COME_FROM            68  '68'

 L.1324        82  LOAD_FAST                'spec'
               84  LOAD_CONST               None
               86  <117>                 0  ''
               88  POP_JUMP_IF_FALSE    92  'to 92'

 L.1325        90  JUMP_BACK             8  'to 8'
             92_0  COME_FROM            88  '88'

 L.1326        92  LOAD_FAST                'spec'
               94  LOAD_ATTR                loader
               96  LOAD_CONST               None
               98  <117>                 1  ''
              100  POP_JUMP_IF_FALSE   110  'to 110'

 L.1327       102  LOAD_FAST                'spec'
              104  ROT_TWO          
              106  POP_TOP          
              108  RETURN_VALUE     
            110_0  COME_FROM           100  '100'

 L.1328       110  LOAD_FAST                'spec'
              112  LOAD_ATTR                submodule_search_locations
              114  STORE_FAST               'portions'

 L.1329       116  LOAD_FAST                'portions'
              118  LOAD_CONST               None
              120  <117>                 0  ''
              122  POP_JUMP_IF_FALSE   132  'to 132'

 L.1330       124  LOAD_GLOBAL              ImportError
              126  LOAD_STR                 'spec missing loader'
              128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
            132_0  COME_FROM           122  '122'

 L.1335       132  LOAD_FAST                'namespace_path'
              134  LOAD_METHOD              extend
              136  LOAD_FAST                'portions'
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  JUMP_BACK             8  'to 8'

 L.1337       144  LOAD_GLOBAL              _bootstrap
              146  LOAD_METHOD              ModuleSpec
              148  LOAD_FAST                'fullname'
              150  LOAD_CONST               None
              152  CALL_METHOD_2         2  ''
              154  STORE_FAST               'spec'

 L.1338       156  LOAD_FAST                'namespace_path'
              158  LOAD_FAST                'spec'
              160  STORE_ATTR               submodule_search_locations

 L.1339       162  LOAD_FAST                'spec'
              164  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 42

    @classmethod
    def find_spec--- This code section failed: ---

 L.1347         0  LOAD_FAST                'path'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.1348         8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                path
               12  STORE_FAST               'path'
             14_0  COME_FROM             6  '6'

 L.1349        14  LOAD_FAST                'cls'
               16  LOAD_METHOD              _get_spec
               18  LOAD_FAST                'fullname'
               20  LOAD_FAST                'path'
               22  LOAD_FAST                'target'
               24  CALL_METHOD_3         3  ''
               26  STORE_FAST               'spec'

 L.1350        28  LOAD_FAST                'spec'
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L.1351        36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L.1352        40  LOAD_FAST                'spec'
               42  LOAD_ATTR                loader
               44  LOAD_CONST               None
               46  <117>                 0  ''
               48  POP_JUMP_IF_FALSE    92  'to 92'

 L.1353        50  LOAD_FAST                'spec'
               52  LOAD_ATTR                submodule_search_locations
               54  STORE_FAST               'namespace_path'

 L.1354        56  LOAD_FAST                'namespace_path'
               58  POP_JUMP_IF_FALSE    86  'to 86'

 L.1357        60  LOAD_CONST               None
               62  LOAD_FAST                'spec'
               64  STORE_ATTR               origin

 L.1358        66  LOAD_GLOBAL              _NamespacePath
               68  LOAD_FAST                'fullname'
               70  LOAD_FAST                'namespace_path'
               72  LOAD_FAST                'cls'
               74  LOAD_ATTR                _get_spec
               76  CALL_FUNCTION_3       3  ''
               78  LOAD_FAST                'spec'
               80  STORE_ATTR               submodule_search_locations

 L.1359        82  LOAD_FAST                'spec'
               84  RETURN_VALUE     
             86_0  COME_FROM            58  '58'

 L.1361        86  LOAD_CONST               None
               88  RETURN_VALUE     
               90  JUMP_FORWARD         96  'to 96'
             92_0  COME_FROM            48  '48'

 L.1363        92  LOAD_FAST                'spec'
               94  RETURN_VALUE     
             96_0  COME_FROM            90  '90'

Parse error at or near `None' instruction at offset -1

    @classmethod
    def find_module--- This code section failed: ---

 L.1373         0  LOAD_FAST                'cls'
                2  LOAD_METHOD              find_spec
                4  LOAD_FAST                'fullname'
                6  LOAD_FAST                'path'
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'spec'

 L.1374        12  LOAD_FAST                'spec'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L.1375        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L.1376        24  LOAD_FAST                'spec'
               26  LOAD_ATTR                loader
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    @classmethod
    def find_distributions--- This code section failed: ---

 L.1388         0  LOAD_CONST               0
                2  LOAD_CONST               ('MetadataPathFinder',)
                4  IMPORT_NAME_ATTR         importlib.metadata
                6  IMPORT_FROM              MetadataPathFinder
                8  STORE_FAST               'MetadataPathFinder'
               10  POP_TOP          

 L.1389        12  LOAD_FAST                'MetadataPathFinder'
               14  LOAD_ATTR                find_distributions
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22


class FileFinder:
    __doc__ = 'File-based finder.\n\n    Interactions with the file system are cached for performance, being\n    refreshed when the directory the finder is handling has been modified.\n\n    '

    def __init__(self, path, *loader_details):
        """Initialize with the path to search on and a variable number of
        2-tuples containing the loader and the file suffixes the loader
        recognizes."""
        loaders = []
        for loader, suffixes in loader_details:
            loaders.extend(((suffix, loader) for suffix in suffixes))
        else:
            self._loaders = loaders
            self.path = path or '.'
            self._path_mtime = -1
            self._path_cache = set()
            self._relaxed_path_cache = set()

    def invalidate_caches(self):
        """Invalidate the directory mtime."""
        self._path_mtime = -1

    find_module = _find_module_shim

    def find_loader--- This code section failed: ---

 L.1428         0  LOAD_FAST                'self'
                2  LOAD_METHOD              find_spec
                4  LOAD_FAST                'fullname'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'spec'

 L.1429        10  LOAD_FAST                'spec'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L.1430        18  LOAD_CONST               None
               20  BUILD_LIST_0          0 
               22  BUILD_TUPLE_2         2 
               24  RETURN_VALUE     
             26_0  COME_FROM            16  '16'

 L.1431        26  LOAD_FAST                'spec'
               28  LOAD_ATTR                loader
               30  LOAD_FAST                'spec'
               32  LOAD_ATTR                submodule_search_locations
               34  JUMP_IF_TRUE_OR_POP    38  'to 38'
               36  BUILD_LIST_0          0 
             38_0  COME_FROM            34  '34'
               38  BUILD_TUPLE_2         2 
               40  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def _get_spec(self, loader_class, fullname, path, smsl, target):
        loader = loader_class(fullname, path)
        return spec_from_file_location(fullname, path, loader=loader, submodule_search_locations=smsl)

    def find_spec--- This code section failed: ---

 L.1443         0  LOAD_CONST               False
                2  STORE_FAST               'is_namespace'

 L.1444         4  LOAD_FAST                'fullname'
                6  LOAD_METHOD              rpartition
                8  LOAD_STR                 '.'
               10  CALL_METHOD_1         1  ''
               12  LOAD_CONST               2
               14  BINARY_SUBSCR    
               16  STORE_FAST               'tail_module'

 L.1445        18  SETUP_FINALLY        44  'to 44'

 L.1446        20  LOAD_GLOBAL              _path_stat
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                path
               26  JUMP_IF_TRUE_OR_POP    34  'to 34'
               28  LOAD_GLOBAL              _os
               30  LOAD_METHOD              getcwd
               32  CALL_METHOD_0         0  ''
             34_0  COME_FROM            26  '26'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_ATTR                st_mtime
               38  STORE_FAST               'mtime'
               40  POP_BLOCK        
               42  JUMP_FORWARD         66  'to 66'
             44_0  COME_FROM_FINALLY    18  '18'

 L.1447        44  DUP_TOP          
               46  LOAD_GLOBAL              OSError
               48  <121>                64  ''
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L.1448        56  LOAD_CONST               -1
               58  STORE_FAST               'mtime'
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
               64  <48>             
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            42  '42'

 L.1449        66  LOAD_FAST                'mtime'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _path_mtime
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_FALSE    90  'to 90'

 L.1450        76  LOAD_FAST                'self'
               78  LOAD_METHOD              _fill_cache
               80  CALL_METHOD_0         0  ''
               82  POP_TOP          

 L.1451        84  LOAD_FAST                'mtime'
               86  LOAD_FAST                'self'
               88  STORE_ATTR               _path_mtime
             90_0  COME_FROM            74  '74'

 L.1453        90  LOAD_GLOBAL              _relax_case
               92  CALL_FUNCTION_0       0  ''
               94  POP_JUMP_IF_FALSE   112  'to 112'

 L.1454        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _relaxed_path_cache
              100  STORE_FAST               'cache'

 L.1455       102  LOAD_FAST                'tail_module'
              104  LOAD_METHOD              lower
              106  CALL_METHOD_0         0  ''
              108  STORE_FAST               'cache_module'
              110  JUMP_FORWARD        122  'to 122'
            112_0  COME_FROM            94  '94'

 L.1457       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _path_cache
              116  STORE_FAST               'cache'

 L.1458       118  LOAD_FAST                'tail_module'
              120  STORE_FAST               'cache_module'
            122_0  COME_FROM           110  '110'

 L.1460       122  LOAD_FAST                'cache_module'
              124  LOAD_FAST                'cache'
              126  <118>                 0  ''
              128  POP_JUMP_IF_FALSE   216  'to 216'

 L.1461       130  LOAD_GLOBAL              _path_join
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                path
              136  LOAD_FAST                'tail_module'
              138  CALL_FUNCTION_2       2  ''
              140  STORE_FAST               'base_path'

 L.1462       142  LOAD_FAST                'self'
              144  LOAD_ATTR                _loaders
              146  GET_ITER         
            148_0  COME_FROM           180  '180'
              148  FOR_ITER            208  'to 208'
              150  UNPACK_SEQUENCE_2     2 
              152  STORE_FAST               'suffix'
              154  STORE_FAST               'loader_class'

 L.1463       156  LOAD_STR                 '__init__'
              158  LOAD_FAST                'suffix'
              160  BINARY_ADD       
              162  STORE_FAST               'init_filename'

 L.1464       164  LOAD_GLOBAL              _path_join
              166  LOAD_FAST                'base_path'
              168  LOAD_FAST                'init_filename'
              170  CALL_FUNCTION_2       2  ''
              172  STORE_FAST               'full_path'

 L.1465       174  LOAD_GLOBAL              _path_isfile
              176  LOAD_FAST                'full_path'
              178  CALL_FUNCTION_1       1  ''
              180  POP_JUMP_IF_FALSE   148  'to 148'

 L.1466       182  LOAD_FAST                'self'
              184  LOAD_METHOD              _get_spec
              186  LOAD_FAST                'loader_class'
              188  LOAD_FAST                'fullname'
              190  LOAD_FAST                'full_path'
              192  LOAD_FAST                'base_path'
              194  BUILD_LIST_1          1 
              196  LOAD_FAST                'target'
              198  CALL_METHOD_5         5  ''
              200  ROT_TWO          
              202  POP_TOP          
              204  RETURN_VALUE     
              206  JUMP_BACK           148  'to 148'

 L.1470       208  LOAD_GLOBAL              _path_isdir
              210  LOAD_FAST                'base_path'
              212  CALL_FUNCTION_1       1  ''
              214  STORE_FAST               'is_namespace'
            216_0  COME_FROM           128  '128'

 L.1472       216  LOAD_FAST                'self'
              218  LOAD_ATTR                _loaders
              220  GET_ITER         
            222_0  COME_FROM           280  '280'
            222_1  COME_FROM           272  '272'
              222  FOR_ITER            306  'to 306'
              224  UNPACK_SEQUENCE_2     2 
              226  STORE_FAST               'suffix'
              228  STORE_FAST               'loader_class'

 L.1473       230  LOAD_GLOBAL              _path_join
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                path
              236  LOAD_FAST                'tail_module'
              238  LOAD_FAST                'suffix'
              240  BINARY_ADD       
              242  CALL_FUNCTION_2       2  ''
              244  STORE_FAST               'full_path'

 L.1474       246  LOAD_GLOBAL              _bootstrap
              248  LOAD_ATTR                _verbose_message
              250  LOAD_STR                 'trying {}'
              252  LOAD_FAST                'full_path'
              254  LOAD_CONST               2
              256  LOAD_CONST               ('verbosity',)
              258  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              260  POP_TOP          

 L.1475       262  LOAD_FAST                'cache_module'
              264  LOAD_FAST                'suffix'
              266  BINARY_ADD       
              268  LOAD_FAST                'cache'
              270  <118>                 0  ''
              272  POP_JUMP_IF_FALSE   222  'to 222'

 L.1476       274  LOAD_GLOBAL              _path_isfile
              276  LOAD_FAST                'full_path'
              278  CALL_FUNCTION_1       1  ''
              280  POP_JUMP_IF_FALSE   222  'to 222'

 L.1477       282  LOAD_FAST                'self'
              284  LOAD_METHOD              _get_spec
              286  LOAD_FAST                'loader_class'
              288  LOAD_FAST                'fullname'
              290  LOAD_FAST                'full_path'

 L.1478       292  LOAD_CONST               None
              294  LOAD_FAST                'target'

 L.1477       296  CALL_METHOD_5         5  ''
              298  ROT_TWO          
              300  POP_TOP          
              302  RETURN_VALUE     
              304  JUMP_BACK           222  'to 222'

 L.1479       306  LOAD_FAST                'is_namespace'
          308_310  POP_JUMP_IF_FALSE   348  'to 348'

 L.1480       312  LOAD_GLOBAL              _bootstrap
              314  LOAD_METHOD              _verbose_message
              316  LOAD_STR                 'possible namespace for {}'
              318  LOAD_FAST                'base_path'
              320  CALL_METHOD_2         2  ''
              322  POP_TOP          

 L.1481       324  LOAD_GLOBAL              _bootstrap
              326  LOAD_METHOD              ModuleSpec
              328  LOAD_FAST                'fullname'
              330  LOAD_CONST               None
              332  CALL_METHOD_2         2  ''
              334  STORE_FAST               'spec'

 L.1482       336  LOAD_FAST                'base_path'
              338  BUILD_LIST_1          1 
              340  LOAD_FAST                'spec'
              342  STORE_ATTR               submodule_search_locations

 L.1483       344  LOAD_FAST                'spec'
              346  RETURN_VALUE     
            348_0  COME_FROM           308  '308'

Parse error at or near `<121>' instruction at offset 48

    def _fill_cache--- This code section failed: ---

 L.1488         0  LOAD_FAST                'self'
                2  LOAD_ATTR                path
                4  STORE_FAST               'path'

 L.1489         6  SETUP_FINALLY        30  'to 30'

 L.1490         8  LOAD_GLOBAL              _os
               10  LOAD_METHOD              listdir
               12  LOAD_FAST                'path'
               14  JUMP_IF_TRUE_OR_POP    22  'to 22'
               16  LOAD_GLOBAL              _os
               18  LOAD_METHOD              getcwd
               20  CALL_METHOD_0         0  ''
             22_0  COME_FROM            14  '14'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'contents'
               26  POP_BLOCK        
               28  JUMP_FORWARD         58  'to 58'
             30_0  COME_FROM_FINALLY     6  '6'

 L.1491        30  DUP_TOP          
               32  LOAD_GLOBAL              FileNotFoundError
               34  LOAD_GLOBAL              PermissionError
               36  LOAD_GLOBAL              NotADirectoryError
               38  BUILD_TUPLE_3         3 
               40  <121>                56  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.1494        48  BUILD_LIST_0          0 
               50  STORE_FAST               'contents'
               52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
               56  <48>             
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            28  '28'

 L.1497        58  LOAD_GLOBAL              sys
               60  LOAD_ATTR                platform
               62  LOAD_METHOD              startswith
               64  LOAD_STR                 'win'
               66  CALL_METHOD_1         1  ''
               68  POP_JUMP_IF_TRUE     82  'to 82'

 L.1498        70  LOAD_GLOBAL              set
               72  LOAD_FAST                'contents'
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _path_cache
               80  JUMP_FORWARD        156  'to 156'
             82_0  COME_FROM            68  '68'

 L.1505        82  LOAD_GLOBAL              set
               84  CALL_FUNCTION_0       0  ''
               86  STORE_FAST               'lower_suffix_contents'

 L.1506        88  LOAD_FAST                'contents'
               90  GET_ITER         
               92  FOR_ITER            150  'to 150'
               94  STORE_FAST               'item'

 L.1507        96  LOAD_FAST                'item'
               98  LOAD_METHOD              partition
              100  LOAD_STR                 '.'
              102  CALL_METHOD_1         1  ''
              104  UNPACK_SEQUENCE_3     3 
              106  STORE_FAST               'name'
              108  STORE_FAST               'dot'
              110  STORE_FAST               'suffix'

 L.1508       112  LOAD_FAST                'dot'
              114  POP_JUMP_IF_FALSE   134  'to 134'

 L.1509       116  LOAD_STR                 '{}.{}'
              118  LOAD_METHOD              format
              120  LOAD_FAST                'name'
              122  LOAD_FAST                'suffix'
              124  LOAD_METHOD              lower
              126  CALL_METHOD_0         0  ''
              128  CALL_METHOD_2         2  ''
              130  STORE_FAST               'new_name'
              132  JUMP_FORWARD        138  'to 138'
            134_0  COME_FROM           114  '114'

 L.1511       134  LOAD_FAST                'name'
              136  STORE_FAST               'new_name'
            138_0  COME_FROM           132  '132'

 L.1512       138  LOAD_FAST                'lower_suffix_contents'
              140  LOAD_METHOD              add
              142  LOAD_FAST                'new_name'
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          
              148  JUMP_BACK            92  'to 92'

 L.1513       150  LOAD_FAST                'lower_suffix_contents'
              152  LOAD_FAST                'self'
              154  STORE_ATTR               _path_cache
            156_0  COME_FROM            80  '80'

 L.1514       156  LOAD_GLOBAL              sys
              158  LOAD_ATTR                platform
              160  LOAD_METHOD              startswith
              162  LOAD_GLOBAL              _CASE_INSENSITIVE_PLATFORMS
              164  CALL_METHOD_1         1  ''
              166  POP_JUMP_IF_FALSE   184  'to 184'

 L.1515       168  LOAD_SETCOMP             '<code_object <setcomp>>'
              170  LOAD_STR                 'FileFinder._fill_cache.<locals>.<setcomp>'
              172  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              174  LOAD_FAST                'contents'
              176  GET_ITER         
              178  CALL_FUNCTION_1       1  ''
              180  LOAD_FAST                'self'
              182  STORE_ATTR               _relaxed_path_cache
            184_0  COME_FROM           166  '166'

Parse error at or near `<121>' instruction at offset 40

    @classmethod
    def path_hook(cls, *loader_details):
        """A class method which returns a closure to use on sys.path_hook
        which will return an instance using the specified loaders and the path
        called on the closure.

        If the path called on the closure is not a directory, ImportError is
        raised.

        """

        def path_hook_for_FileFinder--- This code section failed: ---

 L.1529         0  LOAD_GLOBAL              _path_isdir
                2  LOAD_FAST                'path'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_TRUE     20  'to 20'

 L.1530         8  LOAD_GLOBAL              ImportError
               10  LOAD_STR                 'only directories are supported'
               12  LOAD_FAST                'path'
               14  LOAD_CONST               ('path',)
               16  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM             6  '6'

 L.1531        20  LOAD_DEREF               'cls'
               22  LOAD_FAST                'path'
               24  BUILD_LIST_1          1 
               26  LOAD_DEREF               'loader_details'
               28  CALL_FINALLY         31  'to 31'
               30  WITH_CLEANUP_FINISH
               32  CALL_FUNCTION_EX      0  'positional arguments only'
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 28

        return path_hook_for_FileFinder

    def __repr__(self):
        return 'FileFinder({!r})'.format(self.path)


def _fix_up_module--- This code section failed: ---

 L.1543         0  LOAD_FAST                'ns'
                2  LOAD_METHOD              get
                4  LOAD_STR                 '__loader__'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'loader'

 L.1544        10  LOAD_FAST                'ns'
               12  LOAD_METHOD              get
               14  LOAD_STR                 '__spec__'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'spec'

 L.1545        20  LOAD_FAST                'loader'
               22  POP_JUMP_IF_TRUE     66  'to 66'

 L.1546        24  LOAD_FAST                'spec'
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L.1547        28  LOAD_FAST                'spec'
               30  LOAD_ATTR                loader
               32  STORE_FAST               'loader'
               34  JUMP_FORWARD         66  'to 66'
             36_0  COME_FROM            26  '26'

 L.1548        36  LOAD_FAST                'pathname'
               38  LOAD_FAST                'cpathname'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    56  'to 56'

 L.1549        44  LOAD_GLOBAL              SourcelessFileLoader
               46  LOAD_FAST                'name'
               48  LOAD_FAST                'pathname'
               50  CALL_FUNCTION_2       2  ''
               52  STORE_FAST               'loader'
               54  JUMP_FORWARD         66  'to 66'
             56_0  COME_FROM            42  '42'

 L.1551        56  LOAD_GLOBAL              SourceFileLoader
               58  LOAD_FAST                'name'
               60  LOAD_FAST                'pathname'
               62  CALL_FUNCTION_2       2  ''
               64  STORE_FAST               'loader'
             66_0  COME_FROM            54  '54'
             66_1  COME_FROM            34  '34'
             66_2  COME_FROM            22  '22'

 L.1552        66  LOAD_FAST                'spec'
               68  POP_JUMP_IF_TRUE     84  'to 84'

 L.1553        70  LOAD_GLOBAL              spec_from_file_location
               72  LOAD_FAST                'name'
               74  LOAD_FAST                'pathname'
               76  LOAD_FAST                'loader'
               78  LOAD_CONST               ('loader',)
               80  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               82  STORE_FAST               'spec'
             84_0  COME_FROM            68  '68'

 L.1554        84  SETUP_FINALLY       122  'to 122'

 L.1555        86  LOAD_FAST                'spec'
               88  LOAD_FAST                'ns'
               90  LOAD_STR                 '__spec__'
               92  STORE_SUBSCR     

 L.1556        94  LOAD_FAST                'loader'
               96  LOAD_FAST                'ns'
               98  LOAD_STR                 '__loader__'
              100  STORE_SUBSCR     

 L.1557       102  LOAD_FAST                'pathname'
              104  LOAD_FAST                'ns'
              106  LOAD_STR                 '__file__'
              108  STORE_SUBSCR     

 L.1558       110  LOAD_FAST                'cpathname'
              112  LOAD_FAST                'ns'
              114  LOAD_STR                 '__cached__'
              116  STORE_SUBSCR     
              118  POP_BLOCK        
              120  JUMP_FORWARD        140  'to 140'
            122_0  COME_FROM_FINALLY    84  '84'

 L.1559       122  DUP_TOP          
              124  LOAD_GLOBAL              Exception
              126  <121>               138  ''
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L.1561       134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
              138  <48>             
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM           120  '120'

Parse error at or near `<121>' instruction at offset 126


def _get_supported_file_loaders():
    """Returns a list of file-based module loaders.

    Each item is a tuple (loader, suffixes).
    """
    extensions = (
     ExtensionFileLoader, _imp.extension_suffixes())
    source = (SourceFileLoader, SOURCE_SUFFIXES)
    bytecode = (SourcelessFileLoader, BYTECODE_SUFFIXES)
    return [extensions, source, bytecode]


def _setup--- This code section failed: ---

 L.1583         0  LOAD_FAST                '_bootstrap_module'
                2  STORE_GLOBAL             _bootstrap

 L.1584         4  LOAD_GLOBAL              _bootstrap
                6  LOAD_ATTR                sys
                8  STORE_GLOBAL             sys

 L.1585        10  LOAD_GLOBAL              _bootstrap
               12  LOAD_ATTR                _imp
               14  STORE_GLOBAL             _imp

 L.1587        16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                modules
               20  LOAD_GLOBAL              __name__
               22  BINARY_SUBSCR    
               24  STORE_FAST               'self_module'

 L.1590        26  LOAD_STR                 'posix'
               28  LOAD_STR                 '/'
               30  BUILD_LIST_1          1 
               32  BUILD_TUPLE_2         2 
               34  LOAD_STR                 'nt'
               36  LOAD_STR                 '\\'
               38  LOAD_STR                 '/'
               40  BUILD_LIST_2          2 
               42  BUILD_TUPLE_2         2 
               44  BUILD_TUPLE_2         2 
               46  STORE_FAST               'os_details'

 L.1591        48  LOAD_FAST                'os_details'
               50  GET_ITER         
               52  FOR_ITER            162  'to 162'
               54  UNPACK_SEQUENCE_2     2 
               56  STORE_FAST               'builtin_os'
               58  STORE_FAST               'path_separators'

 L.1593        60  LOAD_GLOBAL              all
               62  LOAD_GENEXPR             '<code_object <genexpr>>'
               64  LOAD_STR                 '_setup.<locals>.<genexpr>'
               66  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               68  LOAD_FAST                'path_separators'
               70  GET_ITER         
               72  CALL_FUNCTION_1       1  ''
               74  CALL_FUNCTION_1       1  ''
               76  POP_JUMP_IF_TRUE     82  'to 82'
               78  <74>             
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            76  '76'

 L.1594        82  LOAD_FAST                'path_separators'
               84  LOAD_CONST               0
               86  BINARY_SUBSCR    
               88  STORE_FAST               'path_sep'

 L.1595        90  LOAD_FAST                'builtin_os'
               92  LOAD_GLOBAL              sys
               94  LOAD_ATTR                modules
               96  <118>                 0  ''
               98  POP_JUMP_IF_FALSE   116  'to 116'

 L.1596       100  LOAD_GLOBAL              sys
              102  LOAD_ATTR                modules
              104  LOAD_FAST                'builtin_os'
              106  BINARY_SUBSCR    
              108  STORE_FAST               'os_module'

 L.1597       110  POP_TOP          
              112  BREAK_LOOP          170  'to 170'
              114  JUMP_BACK            52  'to 52'
            116_0  COME_FROM            98  '98'

 L.1599       116  SETUP_FINALLY       138  'to 138'

 L.1600       118  LOAD_GLOBAL              _bootstrap
              120  LOAD_METHOD              _builtin_from_name
              122  LOAD_FAST                'builtin_os'
              124  CALL_METHOD_1         1  ''
              126  STORE_FAST               'os_module'

 L.1601       128  POP_BLOCK        
              130  POP_TOP          
              132  JUMP_ABSOLUTE       170  'to 170'
              134  POP_BLOCK        
              136  JUMP_BACK            52  'to 52'
            138_0  COME_FROM_FINALLY   116  '116'

 L.1602       138  DUP_TOP          
              140  LOAD_GLOBAL              ImportError
              142  <121>               158  ''
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L.1603       150  POP_EXCEPT       
              152  JUMP_BACK            52  'to 52'
              154  POP_EXCEPT       
              156  JUMP_BACK            52  'to 52'
              158  <48>             
              160  JUMP_BACK            52  'to 52'

 L.1605       162  LOAD_GLOBAL              ImportError
              164  LOAD_STR                 'importlib requires posix or nt'
              166  CALL_FUNCTION_1       1  ''
              168  RAISE_VARARGS_1       1  'exception instance'

 L.1607       170  LOAD_GLOBAL              setattr
              172  LOAD_FAST                'self_module'
              174  LOAD_STR                 '_os'
              176  LOAD_FAST                'os_module'
              178  CALL_FUNCTION_3       3  ''
              180  POP_TOP          

 L.1608       182  LOAD_GLOBAL              setattr
              184  LOAD_FAST                'self_module'
              186  LOAD_STR                 'path_sep'
              188  LOAD_FAST                'path_sep'
              190  CALL_FUNCTION_3       3  ''
              192  POP_TOP          

 L.1609       194  LOAD_GLOBAL              setattr
              196  LOAD_FAST                'self_module'
              198  LOAD_STR                 'path_separators'
              200  LOAD_STR                 ''
              202  LOAD_METHOD              join
              204  LOAD_FAST                'path_separators'
              206  CALL_METHOD_1         1  ''
              208  CALL_FUNCTION_3       3  ''
              210  POP_TOP          

 L.1610       212  LOAD_GLOBAL              setattr
              214  LOAD_FAST                'self_module'
              216  LOAD_STR                 '_pathseps_with_colon'
              218  LOAD_SETCOMP             '<code_object <setcomp>>'
              220  LOAD_STR                 '_setup.<locals>.<setcomp>'
              222  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              224  LOAD_FAST                'path_separators'
              226  GET_ITER         
              228  CALL_FUNCTION_1       1  ''
              230  CALL_FUNCTION_3       3  ''
              232  POP_TOP          

 L.1613       234  BUILD_LIST_0          0 
              236  LOAD_CONST               ('_io', '_warnings', 'marshal')
              238  CALL_FINALLY        241  'to 241'
              240  STORE_FAST               'builtin_names'

 L.1614       242  LOAD_FAST                'builtin_os'
              244  LOAD_STR                 'nt'
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_FALSE   262  'to 262'

 L.1615       252  LOAD_FAST                'builtin_names'
              254  LOAD_METHOD              append
              256  LOAD_STR                 'winreg'
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          
            262_0  COME_FROM           248  '248'

 L.1616       262  LOAD_FAST                'builtin_names'
              264  GET_ITER         
              266  FOR_ITER            320  'to 320'
              268  STORE_FAST               'builtin_name'

 L.1617       270  LOAD_FAST                'builtin_name'
              272  LOAD_GLOBAL              sys
              274  LOAD_ATTR                modules
              276  <118>                 1  ''
          278_280  POP_JUMP_IF_FALSE   294  'to 294'

 L.1618       282  LOAD_GLOBAL              _bootstrap
              284  LOAD_METHOD              _builtin_from_name
              286  LOAD_FAST                'builtin_name'
              288  CALL_METHOD_1         1  ''
              290  STORE_FAST               'builtin_module'
              292  JUMP_FORWARD        304  'to 304'
            294_0  COME_FROM           278  '278'

 L.1620       294  LOAD_GLOBAL              sys
              296  LOAD_ATTR                modules
              298  LOAD_FAST                'builtin_name'
              300  BINARY_SUBSCR    
              302  STORE_FAST               'builtin_module'
            304_0  COME_FROM           292  '292'

 L.1621       304  LOAD_GLOBAL              setattr
              306  LOAD_FAST                'self_module'
              308  LOAD_FAST                'builtin_name'
              310  LOAD_FAST                'builtin_module'
              312  CALL_FUNCTION_3       3  ''
              314  POP_TOP          
          316_318  JUMP_BACK           266  'to 266'

 L.1624       320  LOAD_GLOBAL              setattr
              322  LOAD_FAST                'self_module'
              324  LOAD_STR                 '_relax_case'
              326  LOAD_GLOBAL              _make_relax_case
              328  CALL_FUNCTION_0       0  ''
              330  CALL_FUNCTION_3       3  ''
              332  POP_TOP          

 L.1625       334  LOAD_GLOBAL              EXTENSION_SUFFIXES
              336  LOAD_METHOD              extend
              338  LOAD_GLOBAL              _imp
              340  LOAD_METHOD              extension_suffixes
              342  CALL_METHOD_0         0  ''
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          

 L.1626       348  LOAD_FAST                'builtin_os'
              350  LOAD_STR                 'nt'
              352  COMPARE_OP               ==
          354_356  POP_JUMP_IF_FALSE   384  'to 384'

 L.1627       358  LOAD_GLOBAL              SOURCE_SUFFIXES
              360  LOAD_METHOD              append
              362  LOAD_STR                 '.pyw'
              364  CALL_METHOD_1         1  ''
              366  POP_TOP          

 L.1628       368  LOAD_STR                 '_d.pyd'
              370  LOAD_GLOBAL              EXTENSION_SUFFIXES
              372  <118>                 0  ''
          374_376  POP_JUMP_IF_FALSE   384  'to 384'

 L.1629       378  LOAD_CONST               True
              380  LOAD_GLOBAL              WindowsRegistryFinder
              382  STORE_ATTR               DEBUG_BUILD
            384_0  COME_FROM           374  '374'
            384_1  COME_FROM           354  '354'

Parse error at or near `<74>' instruction at offset 78


def _install(_bootstrap_module):
    """Install the path-based import components."""
    _setup(_bootstrap_module)
    supported_loaders = _get_supported_file_loaders()
    sys.path_hooks.extend([(FileFinder.path_hook)(*supported_loaders)])
    sys.meta_path.append(PathFinder)