# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: _bootsubprocess.py
"""
Basic subprocess implementation for POSIX which only uses os functions. Only
implement features required by setup.py to build C extension modules when
subprocess is unavailable. setup.py is not used on Windows.
"""
import os

class Popen:

    def __init__(self, cmd, env=None):
        self._cmd = cmd
        self._env = env
        self.returncode = None

    def wait--- This code section failed: ---

 L.  18         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              fork
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'pid'

 L.  19         8  LOAD_FAST                'pid'
               10  LOAD_CONST               0
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_FALSE   102  'to 102'

 L.  21        16  SETUP_FINALLY        88  'to 88'

 L.  22        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _env
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    54  'to 54'

 L.  23        28  LOAD_GLOBAL              os
               30  LOAD_METHOD              execve
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _cmd
               36  LOAD_CONST               0
               38  BINARY_SUBSCR    
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _cmd
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _env
               48  CALL_METHOD_3         3  ''
               50  POP_TOP          
               52  JUMP_FORWARD         74  'to 74'
             54_0  COME_FROM            26  '26'

 L.  25        54  LOAD_GLOBAL              os
               56  LOAD_METHOD              execv
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _cmd
               62  LOAD_CONST               0
               64  BINARY_SUBSCR    
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _cmd
               70  CALL_METHOD_2         2  ''
               72  POP_TOP          
             74_0  COME_FROM            52  '52'
               74  POP_BLOCK        

 L.  27        76  LOAD_GLOBAL              os
               78  LOAD_METHOD              _exit
               80  LOAD_CONST               1
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
               86  JUMP_ABSOLUTE       130  'to 130'
             88_0  COME_FROM_FINALLY    16  '16'
               88  LOAD_GLOBAL              os
               90  LOAD_METHOD              _exit
               92  LOAD_CONST               1
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
               98  <48>             
              100  JUMP_FORWARD        130  'to 130'
            102_0  COME_FROM            14  '14'

 L.  30       102  LOAD_GLOBAL              os
              104  LOAD_METHOD              waitpid
              106  LOAD_FAST                'pid'
              108  LOAD_CONST               0
              110  CALL_METHOD_2         2  ''
              112  UNPACK_SEQUENCE_2     2 
              114  STORE_FAST               '_'
              116  STORE_FAST               'status'

 L.  31       118  LOAD_GLOBAL              os
              120  LOAD_METHOD              waitstatus_to_exitcode
              122  LOAD_FAST                'status'
              124  CALL_METHOD_1         1  ''
              126  LOAD_FAST                'self'
              128  STORE_ATTR               returncode
            130_0  COME_FROM           100  '100'

 L.  33       130  LOAD_FAST                'self'
              132  LOAD_ATTR                returncode
              134  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24


def _check_cmd--- This code section failed: ---

 L.  38         0  BUILD_LIST_0          0 
                2  STORE_FAST               'safe_chars'

 L.  39         4  LOAD_CONST               (('a', 'z'), ('A', 'Z'), ('0', '9'))
                6  GET_ITER         
                8  FOR_ITER             60  'to 60'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'first'
               14  STORE_FAST               'last'

 L.  40        16  LOAD_GLOBAL              range
               18  LOAD_GLOBAL              ord
               20  LOAD_FAST                'first'
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_GLOBAL              ord
               26  LOAD_FAST                'last'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               1
               32  BINARY_ADD       
               34  CALL_FUNCTION_2       2  ''
               36  GET_ITER         
               38  FOR_ITER             58  'to 58'
               40  STORE_FAST               'ch'

 L.  41        42  LOAD_FAST                'safe_chars'
               44  LOAD_METHOD              append
               46  LOAD_GLOBAL              chr
               48  LOAD_FAST                'ch'
               50  CALL_FUNCTION_1       1  ''
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
               56  JUMP_BACK            38  'to 38'
               58  JUMP_BACK             8  'to 8'

 L.  42        60  LOAD_FAST                'safe_chars'
               62  LOAD_METHOD              append
               64  LOAD_STR                 './-'
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L.  43        70  LOAD_STR                 ''
               72  LOAD_METHOD              join
               74  LOAD_FAST                'safe_chars'
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'safe_chars'

 L.  45        80  LOAD_GLOBAL              isinstance
               82  LOAD_FAST                'cmd'
               84  LOAD_GLOBAL              tuple
               86  LOAD_GLOBAL              list
               88  BUILD_TUPLE_2         2 
               90  CALL_FUNCTION_2       2  ''
               92  POP_JUMP_IF_FALSE   100  'to 100'

 L.  46        94  LOAD_FAST                'cmd'
               96  STORE_FAST               'check_strs'
               98  JUMP_FORWARD        122  'to 122'
            100_0  COME_FROM            92  '92'

 L.  47       100  LOAD_GLOBAL              isinstance
              102  LOAD_FAST                'cmd'
              104  LOAD_GLOBAL              str
              106  CALL_FUNCTION_2       2  ''
              108  POP_JUMP_IF_FALSE   118  'to 118'

 L.  48       110  LOAD_FAST                'cmd'
              112  BUILD_LIST_1          1 
              114  STORE_FAST               'check_strs'
              116  JUMP_FORWARD        122  'to 122'
            118_0  COME_FROM           108  '108'

 L.  50       118  LOAD_CONST               False
              120  RETURN_VALUE     
            122_0  COME_FROM           116  '116'
            122_1  COME_FROM            98  '98'

 L.  52       122  LOAD_FAST                'check_strs'
              124  GET_ITER         
              126  FOR_ITER            184  'to 184'
              128  STORE_FAST               'arg'

 L.  53       130  LOAD_GLOBAL              isinstance
              132  LOAD_FAST                'arg'
              134  LOAD_GLOBAL              str
              136  CALL_FUNCTION_2       2  ''
              138  POP_JUMP_IF_TRUE    146  'to 146'

 L.  54       140  POP_TOP          
              142  LOAD_CONST               False
              144  RETURN_VALUE     
            146_0  COME_FROM           138  '138'

 L.  55       146  LOAD_FAST                'arg'
              148  POP_JUMP_IF_TRUE    156  'to 156'

 L.  57       150  POP_TOP          
              152  LOAD_CONST               False
              154  RETURN_VALUE     
            156_0  COME_FROM           148  '148'

 L.  58       156  LOAD_FAST                'arg'
              158  GET_ITER         
            160_0  COME_FROM           170  '170'
              160  FOR_ITER            182  'to 182'
              162  STORE_FAST               'ch'

 L.  59       164  LOAD_FAST                'ch'
              166  LOAD_FAST                'safe_chars'
              168  <118>                 1  ''
              170  POP_JUMP_IF_FALSE   160  'to 160'

 L.  60       172  POP_TOP          
              174  POP_TOP          
              176  LOAD_CONST               False
              178  RETURN_VALUE     
              180  JUMP_BACK           160  'to 160'
              182  JUMP_BACK           126  'to 126'

 L.  62       184  LOAD_CONST               True
              186  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 168


def check_output--- This code section failed: ---

 L.  67         0  LOAD_FAST                'kwargs'
                2  POP_JUMP_IF_FALSE    16  'to 16'

 L.  68         4  LOAD_GLOBAL              NotImplementedError
                6  LOAD_GLOBAL              repr
                8  LOAD_FAST                'kwargs'
               10  CALL_FUNCTION_1       1  ''
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             2  '2'

 L.  70        16  LOAD_GLOBAL              _check_cmd
               18  LOAD_FAST                'cmd'
               20  CALL_FUNCTION_1       1  ''
               22  POP_JUMP_IF_TRUE     38  'to 38'

 L.  71        24  LOAD_GLOBAL              ValueError
               26  LOAD_STR                 'unsupported command: '
               28  LOAD_FAST                'cmd'
               30  FORMAT_VALUE          2  '!r'
               32  BUILD_STRING_2        2 
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            22  '22'

 L.  73        38  LOAD_STR                 'check_output.tmp'
               40  STORE_FAST               'tmp_filename'

 L.  74        42  LOAD_GLOBAL              isinstance
               44  LOAD_FAST                'cmd'
               46  LOAD_GLOBAL              str
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_TRUE     62  'to 62'

 L.  75        52  LOAD_STR                 ' '
               54  LOAD_METHOD              join
               56  LOAD_FAST                'cmd'
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'cmd'
             62_0  COME_FROM            50  '50'

 L.  76        62  LOAD_FAST                'cmd'
               64  FORMAT_VALUE          0  ''
               66  LOAD_STR                 ' >'
               68  LOAD_FAST                'tmp_filename'
               70  FORMAT_VALUE          0  ''
               72  BUILD_STRING_3        3 
               74  STORE_FAST               'cmd'

 L.  78        76  SETUP_FINALLY       238  'to 238'

 L.  80        78  LOAD_GLOBAL              os
               80  LOAD_METHOD              system
               82  LOAD_FAST                'cmd'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'status'

 L.  81        88  LOAD_GLOBAL              os
               90  LOAD_METHOD              waitstatus_to_exitcode
               92  LOAD_FAST                'status'
               94  CALL_METHOD_1         1  ''
               96  STORE_FAST               'exitcode'

 L.  82        98  LOAD_FAST                'exitcode'
              100  POP_JUMP_IF_FALSE   122  'to 122'

 L.  83       102  LOAD_GLOBAL              ValueError
              104  LOAD_STR                 'Command '
              106  LOAD_FAST                'cmd'
              108  FORMAT_VALUE          2  '!r'
              110  LOAD_STR                 ' returned non-zero exit status '

 L.  84       112  LOAD_FAST                'exitcode'

 L.  83       114  FORMAT_VALUE          2  '!r'
              116  BUILD_STRING_4        4 
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           100  '100'

 L.  86       122  SETUP_FINALLY       178  'to 178'

 L.  87       124  LOAD_GLOBAL              open
              126  LOAD_FAST                'tmp_filename'
              128  LOAD_STR                 'rb'
              130  CALL_FUNCTION_2       2  ''
              132  SETUP_WITH          158  'to 158'
              134  STORE_FAST               'fp'

 L.  88       136  LOAD_FAST                'fp'
              138  LOAD_METHOD              read
              140  CALL_METHOD_0         0  ''
              142  STORE_FAST               'stdout'
              144  POP_BLOCK        
              146  LOAD_CONST               None
              148  DUP_TOP          
              150  DUP_TOP          
              152  CALL_FUNCTION_3       3  ''
              154  POP_TOP          
              156  JUMP_FORWARD        174  'to 174'
            158_0  COME_FROM_WITH      132  '132'
              158  <49>             
              160  POP_JUMP_IF_TRUE    164  'to 164'
              162  <48>             
            164_0  COME_FROM           160  '160'
              164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          
              170  POP_EXCEPT       
              172  POP_TOP          
            174_0  COME_FROM           156  '156'
              174  POP_BLOCK        
              176  JUMP_FORWARD        200  'to 200'
            178_0  COME_FROM_FINALLY   122  '122'

 L.  89       178  DUP_TOP          
              180  LOAD_GLOBAL              FileNotFoundError
              182  <121>               198  ''
              184  POP_TOP          
              186  POP_TOP          
              188  POP_TOP          

 L.  90       190  LOAD_CONST               b''
              192  STORE_FAST               'stdout'
              194  POP_EXCEPT       
              196  JUMP_FORWARD        200  'to 200'
              198  <48>             
            200_0  COME_FROM           196  '196'
            200_1  COME_FROM           176  '176'
              200  POP_BLOCK        

 L.  92       202  SETUP_FINALLY       218  'to 218'

 L.  93       204  LOAD_GLOBAL              os
              206  LOAD_METHOD              unlink
              208  LOAD_FAST                'tmp_filename'
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          
              214  POP_BLOCK        
              216  JUMP_FORWARD        236  'to 236'
            218_0  COME_FROM_FINALLY   202  '202'

 L.  94       218  DUP_TOP          
              220  LOAD_GLOBAL              OSError
              222  <121>               234  ''
              224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L.  95       230  POP_EXCEPT       
              232  JUMP_FORWARD        236  'to 236'
              234  <48>             
            236_0  COME_FROM           232  '232'
            236_1  COME_FROM           216  '216'
              236  JUMP_FORWARD        276  'to 276'
            238_0  COME_FROM_FINALLY    76  '76'

 L.  92       238  SETUP_FINALLY       254  'to 254'

 L.  93       240  LOAD_GLOBAL              os
              242  LOAD_METHOD              unlink
              244  LOAD_FAST                'tmp_filename'
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          
              250  POP_BLOCK        
              252  JUMP_FORWARD        274  'to 274'
            254_0  COME_FROM_FINALLY   238  '238'

 L.  94       254  DUP_TOP          
              256  LOAD_GLOBAL              OSError
          258_260  <121>               272  ''
              262  POP_TOP          
              264  POP_TOP          
              266  POP_TOP          

 L.  95       268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
              272  <48>             
            274_0  COME_FROM           270  '270'
            274_1  COME_FROM           252  '252'
              274  <48>             
            276_0  COME_FROM           236  '236'

 L.  97       276  LOAD_FAST                'stdout'
              278  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 148