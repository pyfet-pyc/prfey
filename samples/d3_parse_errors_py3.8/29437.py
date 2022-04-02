# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\selenium\webdriver\remote\utils.py
import json, logging, os, tempfile, zipfile
LOGGER = logging.getLogger(__name__)

def format_json(json_struct):
    return json.dumps(json_struct, indent=4)


def dump_json(json_struct):
    return json.dumps(json_struct)


def load_json(s):
    return json.loads(s)


def unzip_to_temp_dir--- This code section failed: ---

 L.  45         0  LOAD_FAST                'zip_file_name'
                2  POP_JUMP_IF_FALSE    16  'to 16'
                4  LOAD_GLOBAL              os
                6  LOAD_ATTR                path
                8  LOAD_METHOD              exists
               10  LOAD_FAST                'zip_file_name'
               12  CALL_METHOD_1         1  ''
               14  POP_JUMP_IF_TRUE     20  'to 20'
             16_0  COME_FROM             2  '2'

 L.  46        16  LOAD_CONST               None
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L.  48        20  LOAD_GLOBAL              zipfile
               22  LOAD_METHOD              ZipFile
               24  LOAD_FAST                'zip_file_name'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'zf'

 L.  50        30  LOAD_FAST                'zf'
               32  LOAD_METHOD              testzip
               34  CALL_METHOD_0         0  ''
               36  LOAD_CONST               None
               38  COMPARE_OP               is-not
               40  POP_JUMP_IF_FALSE    46  'to 46'

 L.  51        42  LOAD_CONST               None
               44  RETURN_VALUE     
             46_0  COME_FROM            40  '40'

 L.  54        46  LOAD_GLOBAL              LOGGER
               48  LOAD_METHOD              info
               50  LOAD_STR                 'Extracting zipped file: %s'
               52  LOAD_FAST                'zip_file_name'
               54  BINARY_MODULO    
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L.  55        60  LOAD_GLOBAL              tempfile
               62  LOAD_METHOD              mkdtemp
               64  CALL_METHOD_0         0  ''
               66  STORE_FAST               'tempdir'

 L.  57     68_70  SETUP_FINALLY       330  'to 330'

 L.  59        72  LOAD_FAST                'zf'
               74  LOAD_METHOD              namelist
               76  CALL_METHOD_0         0  ''
               78  GET_ITER         
             80_0  COME_FROM           176  '176'
             80_1  COME_FROM           150  '150'
             80_2  COME_FROM           138  '138'
               80  FOR_ITER            178  'to 178'
               82  STORE_FAST               'zip_name'

 L.  63        84  LOAD_FAST                'zip_name'
               86  LOAD_METHOD              replace
               88  LOAD_STR                 '\\'
               90  LOAD_GLOBAL              os
               92  LOAD_ATTR                path
               94  LOAD_ATTR                sep
               96  CALL_METHOD_2         2  ''
               98  LOAD_METHOD              replace

 L.  64       100  LOAD_STR                 '/'

 L.  64       102  LOAD_GLOBAL              os
              104  LOAD_ATTR                path
              106  LOAD_ATTR                sep

 L.  63       108  CALL_METHOD_2         2  ''
              110  STORE_FAST               'name'

 L.  65       112  LOAD_GLOBAL              os
              114  LOAD_ATTR                path
              116  LOAD_METHOD              join
              118  LOAD_FAST                'tempdir'
              120  LOAD_FAST                'name'
              122  CALL_METHOD_2         2  ''
              124  STORE_FAST               'dest'

 L.  66       126  LOAD_FAST                'name'
              128  LOAD_METHOD              endswith
              130  LOAD_GLOBAL              os
              132  LOAD_ATTR                path
              134  LOAD_ATTR                sep
              136  CALL_METHOD_1         1  ''
              138  POP_JUMP_IF_FALSE_BACK    80  'to 80'
              140  LOAD_GLOBAL              os
              142  LOAD_ATTR                path
              144  LOAD_METHOD              exists
              146  LOAD_FAST                'dest'
              148  CALL_METHOD_1         1  ''
              150  POP_JUMP_IF_TRUE_BACK    80  'to 80'

 L.  67       152  LOAD_GLOBAL              os
              154  LOAD_METHOD              mkdir
              156  LOAD_FAST                'dest'
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          

 L.  68       162  LOAD_GLOBAL              LOGGER
              164  LOAD_METHOD              debug
              166  LOAD_STR                 'Directory %s created.'
              168  LOAD_FAST                'dest'
              170  BINARY_MODULO    
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          
              176  JUMP_BACK            80  'to 80'
            178_0  COME_FROM            80  '80'

 L.  71       178  LOAD_FAST                'zf'
              180  LOAD_METHOD              namelist
              182  CALL_METHOD_0         0  ''
              184  GET_ITER         
            186_0  COME_FROM           308  '308'
            186_1  COME_FROM           244  '244'
              186  FOR_ITER            310  'to 310'
              188  STORE_FAST               'zip_name'

 L.  75       190  LOAD_FAST                'zip_name'
              192  LOAD_METHOD              replace
              194  LOAD_STR                 '\\'
              196  LOAD_GLOBAL              os
              198  LOAD_ATTR                path
              200  LOAD_ATTR                sep
              202  CALL_METHOD_2         2  ''
              204  LOAD_METHOD              replace

 L.  76       206  LOAD_STR                 '/'

 L.  76       208  LOAD_GLOBAL              os
              210  LOAD_ATTR                path
              212  LOAD_ATTR                sep

 L.  75       214  CALL_METHOD_2         2  ''
              216  STORE_FAST               'name'

 L.  77       218  LOAD_GLOBAL              os
              220  LOAD_ATTR                path
              222  LOAD_METHOD              join
              224  LOAD_FAST                'tempdir'
              226  LOAD_FAST                'name'
              228  CALL_METHOD_2         2  ''
              230  STORE_FAST               'dest'

 L.  78       232  LOAD_FAST                'name'
              234  LOAD_METHOD              endswith
              236  LOAD_GLOBAL              os
              238  LOAD_ATTR                path
              240  LOAD_ATTR                sep
              242  CALL_METHOD_1         1  ''
              244  POP_JUMP_IF_TRUE_BACK   186  'to 186'

 L.  79       246  LOAD_GLOBAL              LOGGER
              248  LOAD_METHOD              debug
              250  LOAD_STR                 'Copying file %s......'
              252  LOAD_FAST                'dest'
              254  BINARY_MODULO    
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          

 L.  80       260  LOAD_GLOBAL              open
              262  LOAD_FAST                'dest'
              264  LOAD_STR                 'wb'
              266  CALL_FUNCTION_2       2  ''
              268  STORE_FAST               'outfile'

 L.  81       270  LOAD_FAST                'outfile'
              272  LOAD_METHOD              write
              274  LOAD_FAST                'zf'
              276  LOAD_METHOD              read
              278  LOAD_FAST                'zip_name'
              280  CALL_METHOD_1         1  ''
              282  CALL_METHOD_1         1  ''
              284  POP_TOP          

 L.  82       286  LOAD_FAST                'outfile'
              288  LOAD_METHOD              close
              290  CALL_METHOD_0         0  ''
              292  POP_TOP          

 L.  83       294  LOAD_GLOBAL              LOGGER
              296  LOAD_METHOD              debug
              298  LOAD_STR                 'File %s copied.'
              300  LOAD_FAST                'dest'
              302  BINARY_MODULO    
              304  CALL_METHOD_1         1  ''
              306  POP_TOP          
              308  JUMP_BACK           186  'to 186'
            310_0  COME_FROM           186  '186'

 L.  85       310  LOAD_GLOBAL              LOGGER
              312  LOAD_METHOD              info
              314  LOAD_STR                 'Unzipped file can be found at %s'
              316  LOAD_FAST                'tempdir'
              318  BINARY_MODULO    
              320  CALL_METHOD_1         1  ''
              322  POP_TOP          

 L.  86       324  LOAD_FAST                'tempdir'
              326  POP_BLOCK        
              328  RETURN_VALUE     
            330_0  COME_FROM_FINALLY    68  '68'

 L.  88       330  DUP_TOP          
              332  LOAD_GLOBAL              IOError
              334  COMPARE_OP               exception-match
          336_338  POP_JUMP_IF_FALSE   384  'to 384'
              340  POP_TOP          
              342  STORE_FAST               'err'
              344  POP_TOP          
              346  SETUP_FINALLY       372  'to 372'

 L.  89       348  LOAD_GLOBAL              LOGGER
              350  LOAD_METHOD              error
              352  LOAD_STR                 'Error in extracting webdriver.xpi: %s'
              354  LOAD_FAST                'err'
              356  BINARY_MODULO    
              358  CALL_METHOD_1         1  ''
              360  POP_TOP          

 L.  90       362  POP_BLOCK        
              364  POP_EXCEPT       
              366  CALL_FINALLY        372  'to 372'
              368  LOAD_CONST               None
              370  RETURN_VALUE     
            372_0  COME_FROM           366  '366'
            372_1  COME_FROM_FINALLY   346  '346'
              372  LOAD_CONST               None
              374  STORE_FAST               'err'
              376  DELETE_FAST              'err'
              378  END_FINALLY      
              380  POP_EXCEPT       
              382  JUMP_FORWARD        386  'to 386'
            384_0  COME_FROM           336  '336'
              384  END_FINALLY      
            386_0  COME_FROM           382  '382'

Parse error at or near `POP_EXCEPT' instruction at offset 364