# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\EpsImagePlugin.py
import io, os, re, subprocess, sys, tempfile
from . import Image, ImageFile
from ._binary import i32le as i32
split = re.compile('^%%([^:]*):[ \\t]*(.*)[ \\t]*$')
field = re.compile('^%[%!\\w]([^:]*)[ \\t]*$')
gs_windows_binary = None
if sys.platform.startswith('win'):
    import shutil
    for binary in ('gswin32c', 'gswin64c', 'gs'):
        if shutil.which(binary) is not None:
            gs_windows_binary = binary
            break
    else:
        gs_windows_binary = False

def has_ghostscript--- This code section failed: ---

 L.  52         0  LOAD_GLOBAL              gs_windows_binary
                2  POP_JUMP_IF_FALSE     8  'to 8'

 L.  53         4  LOAD_CONST               True
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L.  54         8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                platform
               12  LOAD_METHOD              startswith
               14  LOAD_STR                 'win'
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_TRUE     68  'to 68'

 L.  55        20  SETUP_FINALLY        48  'to 48'

 L.  56        22  LOAD_GLOBAL              subprocess
               24  LOAD_ATTR                check_call
               26  LOAD_STR                 'gs'
               28  LOAD_STR                 '--version'
               30  BUILD_LIST_2          2 
               32  LOAD_GLOBAL              subprocess
               34  LOAD_ATTR                DEVNULL
               36  LOAD_CONST               ('stdout',)
               38  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               40  POP_TOP          

 L.  57        42  POP_BLOCK        
               44  LOAD_CONST               True
               46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY    20  '20'

 L.  58        48  DUP_TOP          
               50  LOAD_GLOBAL              OSError
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    66  'to 66'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.  60        62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
             66_0  COME_FROM            54  '54'
               66  END_FINALLY      
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM            18  '18'

 L.  61        68  LOAD_CONST               False
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 48


def Ghostscript--- This code section failed: ---

 L.  68         0  LOAD_FAST                'tile'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  UNPACK_SEQUENCE_4     4 
                8  STORE_FAST               'decoder'
               10  STORE_FAST               'tile'
               12  STORE_FAST               'offset'
               14  STORE_FAST               'data'

 L.  69        16  LOAD_FAST                'data'
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'length'
               22  STORE_FAST               'bbox'

 L.  72        24  LOAD_GLOBAL              int
               26  LOAD_FAST                'scale'
               28  CALL_FUNCTION_1       1  ''
               30  JUMP_IF_TRUE_OR_POP    34  'to 34'
               32  LOAD_CONST               1
             34_0  COME_FROM            30  '30'
               34  STORE_FAST               'scale'

 L.  75        36  LOAD_FAST                'size'
               38  LOAD_CONST               0
               40  BINARY_SUBSCR    
               42  LOAD_FAST                'scale'
               44  BINARY_MULTIPLY  
               46  LOAD_FAST                'size'
               48  LOAD_CONST               1
               50  BINARY_SUBSCR    
               52  LOAD_FAST                'scale'
               54  BINARY_MULTIPLY  
               56  BUILD_TUPLE_2         2 
               58  STORE_FAST               'size'

 L.  78        60  LOAD_GLOBAL              float
               62  LOAD_CONST               72.0
               64  LOAD_FAST                'size'
               66  LOAD_CONST               0
               68  BINARY_SUBSCR    
               70  BINARY_MULTIPLY  
               72  LOAD_FAST                'bbox'
               74  LOAD_CONST               2
               76  BINARY_SUBSCR    
               78  LOAD_FAST                'bbox'
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  BINARY_SUBTRACT  
               86  BINARY_TRUE_DIVIDE
               88  CALL_FUNCTION_1       1  ''

 L.  79        90  LOAD_GLOBAL              float
               92  LOAD_CONST               72.0
               94  LOAD_FAST                'size'
               96  LOAD_CONST               1
               98  BINARY_SUBSCR    
              100  BINARY_MULTIPLY  
              102  LOAD_FAST                'bbox'
              104  LOAD_CONST               3
              106  BINARY_SUBSCR    
              108  LOAD_FAST                'bbox'
              110  LOAD_CONST               1
              112  BINARY_SUBSCR    
              114  BINARY_SUBTRACT  
              116  BINARY_TRUE_DIVIDE
              118  CALL_FUNCTION_1       1  ''

 L.  77       120  BUILD_TUPLE_2         2 
              122  STORE_FAST               'res'

 L.  82       124  LOAD_GLOBAL              tempfile
              126  LOAD_METHOD              mkstemp
              128  CALL_METHOD_0         0  ''
              130  UNPACK_SEQUENCE_2     2 
              132  STORE_FAST               'out_fd'
              134  STORE_FAST               'outfile'

 L.  83       136  LOAD_GLOBAL              os
              138  LOAD_METHOD              close
              140  LOAD_FAST                'out_fd'
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          

 L.  85       146  LOAD_CONST               None
              148  STORE_FAST               'infile_temp'

 L.  86       150  LOAD_GLOBAL              hasattr
              152  LOAD_FAST                'fp'
              154  LOAD_STR                 'name'
              156  CALL_FUNCTION_2       2  ''
              158  POP_JUMP_IF_FALSE   182  'to 182'
              160  LOAD_GLOBAL              os
              162  LOAD_ATTR                path
              164  LOAD_METHOD              exists
              166  LOAD_FAST                'fp'
              168  LOAD_ATTR                name
              170  CALL_METHOD_1         1  ''
              172  POP_JUMP_IF_FALSE   182  'to 182'

 L.  87       174  LOAD_FAST                'fp'
              176  LOAD_ATTR                name
              178  STORE_FAST               'infile'
              180  JUMP_FORWARD        328  'to 328'
            182_0  COME_FROM           172  '172'
            182_1  COME_FROM           158  '158'

 L.  89       182  LOAD_GLOBAL              tempfile
              184  LOAD_METHOD              mkstemp
              186  CALL_METHOD_0         0  ''
              188  UNPACK_SEQUENCE_2     2 
              190  STORE_FAST               'in_fd'
              192  STORE_FAST               'infile_temp'

 L.  90       194  LOAD_GLOBAL              os
              196  LOAD_METHOD              close
              198  LOAD_FAST                'in_fd'
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          

 L.  91       204  LOAD_FAST                'infile_temp'
              206  STORE_FAST               'infile'

 L.  96       208  LOAD_GLOBAL              open
              210  LOAD_FAST                'infile_temp'
              212  LOAD_STR                 'wb'
              214  CALL_FUNCTION_2       2  ''
              216  SETUP_WITH          322  'to 322'
              218  STORE_FAST               'f'

 L.  98       220  LOAD_FAST                'fp'
              222  LOAD_METHOD              seek
              224  LOAD_CONST               0
              226  LOAD_GLOBAL              io
              228  LOAD_ATTR                SEEK_END
              230  CALL_METHOD_2         2  ''
              232  POP_TOP          

 L.  99       234  LOAD_FAST                'fp'
              236  LOAD_METHOD              tell
              238  CALL_METHOD_0         0  ''
              240  STORE_FAST               'fsize'

 L. 102       242  LOAD_FAST                'fp'
              244  LOAD_METHOD              seek
              246  LOAD_CONST               0
              248  CALL_METHOD_1         1  ''
              250  POP_TOP          

 L. 103       252  LOAD_FAST                'fsize'
              254  STORE_FAST               'lengthfile'
            256_0  COME_FROM           314  '314'

 L. 104       256  LOAD_FAST                'lengthfile'
              258  LOAD_CONST               0
              260  COMPARE_OP               >
          262_264  POP_JUMP_IF_FALSE   318  'to 318'

 L. 105       266  LOAD_FAST                'fp'
              268  LOAD_METHOD              read
              270  LOAD_GLOBAL              min
              272  LOAD_FAST                'lengthfile'
              274  LOAD_CONST               102400
              276  CALL_FUNCTION_2       2  ''
              278  CALL_METHOD_1         1  ''
              280  STORE_FAST               's'

 L. 106       282  LOAD_FAST                's'
          284_286  POP_JUMP_IF_TRUE    292  'to 292'

 L. 107   288_290  JUMP_FORWARD        318  'to 318'
            292_0  COME_FROM           284  '284'

 L. 108       292  LOAD_FAST                'lengthfile'
              294  LOAD_GLOBAL              len
              296  LOAD_FAST                's'
              298  CALL_FUNCTION_1       1  ''
              300  INPLACE_SUBTRACT 
              302  STORE_FAST               'lengthfile'

 L. 109       304  LOAD_FAST                'f'
              306  LOAD_METHOD              write
              308  LOAD_FAST                's'
              310  CALL_METHOD_1         1  ''
              312  POP_TOP          
          314_316  JUMP_BACK           256  'to 256'
            318_0  COME_FROM           288  '288'
            318_1  COME_FROM           262  '262'
              318  POP_BLOCK        
              320  BEGIN_FINALLY    
            322_0  COME_FROM_WITH      216  '216'
              322  WITH_CLEANUP_START
              324  WITH_CLEANUP_FINISH
              326  END_FINALLY      
            328_0  COME_FROM           180  '180'

 L. 113       328  LOAD_STR                 'gs'

 L. 114       330  LOAD_STR                 '-q'

 L. 115       332  LOAD_STR                 '-g%dx%d'
              334  LOAD_FAST                'size'
              336  BINARY_MODULO    

 L. 116       338  LOAD_STR                 '-r%fx%f'
              340  LOAD_FAST                'res'
              342  BINARY_MODULO    

 L. 117       344  LOAD_STR                 '-dBATCH'

 L. 118       346  LOAD_STR                 '-dNOPAUSE'

 L. 119       348  LOAD_STR                 '-dSAFER'

 L. 120       350  LOAD_STR                 '-sDEVICE=ppmraw'

 L. 121       352  LOAD_STR                 '-sOutputFile=%s'
              354  LOAD_FAST                'outfile'
              356  BINARY_MODULO    

 L. 123       358  LOAD_STR                 '-c'

 L. 124       360  LOAD_STR                 '%d %d translate'
              362  LOAD_FAST                'bbox'
              364  LOAD_CONST               0
              366  BINARY_SUBSCR    
              368  UNARY_NEGATIVE   
              370  LOAD_FAST                'bbox'
              372  LOAD_CONST               1
              374  BINARY_SUBSCR    
              376  UNARY_NEGATIVE   
              378  BUILD_TUPLE_2         2 
              380  BINARY_MODULO    

 L. 125       382  LOAD_STR                 '-f'

 L. 126       384  LOAD_FAST                'infile'

 L. 128       386  LOAD_STR                 '-c'

 L. 129       388  LOAD_STR                 'showpage'

 L. 112       390  BUILD_LIST_15        15 
              392  STORE_FAST               'command'

 L. 132       394  LOAD_GLOBAL              gs_windows_binary
              396  LOAD_CONST               None
              398  COMPARE_OP               is-not
          400_402  POP_JUMP_IF_FALSE   426  'to 426'

 L. 133       404  LOAD_GLOBAL              gs_windows_binary
          406_408  POP_JUMP_IF_TRUE    418  'to 418'

 L. 134       410  LOAD_GLOBAL              OSError
              412  LOAD_STR                 'Unable to locate Ghostscript on paths'
              414  CALL_FUNCTION_1       1  ''
              416  RAISE_VARARGS_1       1  'exception instance'
            418_0  COME_FROM           406  '406'

 L. 135       418  LOAD_GLOBAL              gs_windows_binary
              420  LOAD_FAST                'command'
              422  LOAD_CONST               0
              424  STORE_SUBSCR     
            426_0  COME_FROM           400  '400'

 L. 138       426  SETUP_FINALLY       506  'to 506'

 L. 139       428  LOAD_CONST               None
              430  STORE_FAST               'startupinfo'

 L. 140       432  LOAD_GLOBAL              sys
              434  LOAD_ATTR                platform
              436  LOAD_METHOD              startswith
              438  LOAD_STR                 'win'
              440  CALL_METHOD_1         1  ''
          442_444  POP_JUMP_IF_FALSE   470  'to 470'

 L. 141       446  LOAD_GLOBAL              subprocess
              448  LOAD_METHOD              STARTUPINFO
              450  CALL_METHOD_0         0  ''
              452  STORE_FAST               'startupinfo'

 L. 142       454  LOAD_FAST                'startupinfo'
              456  DUP_TOP          
              458  LOAD_ATTR                dwFlags
              460  LOAD_GLOBAL              subprocess
              462  LOAD_ATTR                STARTF_USESHOWWINDOW
              464  INPLACE_OR       
              466  ROT_TWO          
              468  STORE_ATTR               dwFlags
            470_0  COME_FROM           442  '442'

 L. 143       470  LOAD_GLOBAL              subprocess
              472  LOAD_ATTR                check_call
              474  LOAD_FAST                'command'
              476  LOAD_FAST                'startupinfo'
              478  LOAD_CONST               ('startupinfo',)
              480  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              482  POP_TOP          

 L. 144       484  LOAD_GLOBAL              Image
              486  LOAD_METHOD              open
              488  LOAD_FAST                'outfile'
              490  CALL_METHOD_1         1  ''
              492  STORE_FAST               'im'

 L. 145       494  LOAD_FAST                'im'
              496  LOAD_METHOD              load
              498  CALL_METHOD_0         0  ''
              500  POP_TOP          
              502  POP_BLOCK        
              504  BEGIN_FINALLY    
            506_0  COME_FROM_FINALLY   426  '426'

 L. 147       506  SETUP_FINALLY       538  'to 538'

 L. 148       508  LOAD_GLOBAL              os
              510  LOAD_METHOD              unlink
              512  LOAD_FAST                'outfile'
              514  CALL_METHOD_1         1  ''
              516  POP_TOP          

 L. 149       518  LOAD_FAST                'infile_temp'
          520_522  POP_JUMP_IF_FALSE   534  'to 534'

 L. 150       524  LOAD_GLOBAL              os
              526  LOAD_METHOD              unlink
              528  LOAD_FAST                'infile_temp'
              530  CALL_METHOD_1         1  ''
              532  POP_TOP          
            534_0  COME_FROM           520  '520'
              534  POP_BLOCK        
              536  JUMP_FORWARD        560  'to 560'
            538_0  COME_FROM_FINALLY   506  '506'

 L. 151       538  DUP_TOP          
              540  LOAD_GLOBAL              OSError
              542  COMPARE_OP               exception-match
          544_546  POP_JUMP_IF_FALSE   558  'to 558'
              548  POP_TOP          
              550  POP_TOP          
              552  POP_TOP          

 L. 152       554  POP_EXCEPT       
              556  BREAK_LOOP          560  'to 560'
            558_0  COME_FROM           544  '544'
              558  END_FINALLY      
            560_0  COME_FROM           556  '556'
            560_1  COME_FROM           536  '536'
              560  END_FINALLY      

 L. 154       562  LOAD_FAST                'im'
              564  LOAD_ATTR                im
              566  LOAD_METHOD              copy
              568  CALL_METHOD_0         0  ''
              570  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 558


class PSFile:
    __doc__ = '\n    Wrapper for bytesio object that treats either CR or LF as end of line.\n    '

    def __init__(self, fp):
        self.fp = fp
        self.char = None

    def seek(self, offset, whence=io.SEEK_SET):
        self.char = None
        self.fp.seek(offset, whence)

    def readline(self):
        s = self.char or b''
        self.char = None
        c = self.fp.read(1)
        while True:
            if c not in b'\r\n':
                s = s + c
                c = self.fp.read(1)

        self.char = self.fp.read(1)
        if self.char in b'\r\n':
            self.char = None
        return s.decode('latin-1')


def _accept(prefix):
    return (prefix[:4] == b'%!PS') or ((len(prefix) >= 4) and (i32(prefix) == 3335770309))


class EpsImageFile(ImageFile.ImageFile):
    __doc__ = 'EPS File Parser for the Python Imaging Library'
    format = 'EPS'
    format_description = 'Encapsulated Postscript'
    mode_map = {1:'L', 
     2:'LAB',  3:'RGB',  4:'CMYK'}

    def _open--- This code section failed: ---

 L. 205         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _find_offset
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fp
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'length'
               14  STORE_FAST               'offset'

 L. 209        16  LOAD_GLOBAL              PSFile
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                fp
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'fp'

 L. 212        26  LOAD_FAST                'fp'
               28  LOAD_METHOD              seek
               30  LOAD_FAST                'offset'
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 214        36  LOAD_CONST               None
               38  STORE_FAST               'box'

 L. 216        40  LOAD_STR                 'RGB'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               mode

 L. 217        46  LOAD_CONST               (1, 1)
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _size

 L. 222        52  LOAD_FAST                'fp'
               54  LOAD_METHOD              readline
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               's_raw'

 L. 223        60  LOAD_FAST                's_raw'
               62  LOAD_METHOD              strip
               64  LOAD_STR                 '\r\n'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               's'
             70_0  COME_FROM           462  '462'
             70_1  COME_FROM           456  '456'
             70_2  COME_FROM           440  '440'

 L. 225        70  LOAD_FAST                's_raw'
            72_74  POP_JUMP_IF_FALSE   464  'to 464'

 L. 226        76  LOAD_FAST                's'
            78_80  POP_JUMP_IF_FALSE   420  'to 420'

 L. 227        82  LOAD_GLOBAL              len
               84  LOAD_FAST                's'
               86  CALL_FUNCTION_1       1  ''
               88  LOAD_CONST               255
               90  COMPARE_OP               >
               92  POP_JUMP_IF_FALSE   102  'to 102'

 L. 228        94  LOAD_GLOBAL              SyntaxError
               96  LOAD_STR                 'not an EPS file'
               98  CALL_FUNCTION_1       1  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            92  '92'

 L. 230       102  SETUP_FINALLY       118  'to 118'

 L. 231       104  LOAD_GLOBAL              split
              106  LOAD_METHOD              match
              108  LOAD_FAST                's'
              110  CALL_METHOD_1         1  ''
              112  STORE_FAST               'm'
              114  POP_BLOCK        
              116  JUMP_FORWARD        148  'to 148'
            118_0  COME_FROM_FINALLY   102  '102'

 L. 232       118  DUP_TOP          
              120  LOAD_GLOBAL              re
              122  LOAD_ATTR                error
              124  COMPARE_OP               exception-match
              126  POP_JUMP_IF_FALSE   146  'to 146'
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L. 233       134  LOAD_GLOBAL              SyntaxError
              136  LOAD_STR                 'not an EPS file'
              138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           126  '126'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM           116  '116'

 L. 235       148  LOAD_FAST                'm'
          150_152  POP_JUMP_IF_FALSE   298  'to 298'

 L. 236       154  LOAD_FAST                'm'
              156  LOAD_METHOD              group
              158  LOAD_CONST               1
              160  LOAD_CONST               2
              162  CALL_METHOD_2         2  ''
              164  UNPACK_SEQUENCE_2     2 
              166  STORE_FAST               'k'
              168  STORE_FAST               'v'

 L. 237       170  LOAD_FAST                'v'
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                info
              176  LOAD_FAST                'k'
              178  STORE_SUBSCR     

 L. 238       180  LOAD_FAST                'k'
              182  LOAD_STR                 'BoundingBox'
              184  COMPARE_OP               ==
          186_188  POP_JUMP_IF_FALSE   420  'to 420'

 L. 239       190  SETUP_FINALLY       274  'to 274'

 L. 243       192  LOAD_LISTCOMP            '<code_object <listcomp>>'
              194  LOAD_STR                 'EpsImageFile._open.<locals>.<listcomp>'
              196  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              198  LOAD_FAST                'v'
              200  LOAD_METHOD              split
              202  CALL_METHOD_0         0  ''
              204  GET_ITER         
              206  CALL_FUNCTION_1       1  ''
              208  STORE_FAST               'box'

 L. 244       210  LOAD_FAST                'box'
              212  LOAD_CONST               2
              214  BINARY_SUBSCR    
              216  LOAD_FAST                'box'
              218  LOAD_CONST               0
              220  BINARY_SUBSCR    
              222  BINARY_SUBTRACT  
              224  LOAD_FAST                'box'
              226  LOAD_CONST               3
              228  BINARY_SUBSCR    
              230  LOAD_FAST                'box'
              232  LOAD_CONST               1
              234  BINARY_SUBSCR    
              236  BINARY_SUBTRACT  
              238  BUILD_TUPLE_2         2 
              240  LOAD_FAST                'self'
              242  STORE_ATTR               _size

 L. 246       244  LOAD_STR                 'eps'
              246  LOAD_CONST               (0, 0)
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                size
              252  BINARY_ADD       
              254  LOAD_FAST                'offset'
              256  LOAD_FAST                'length'
              258  LOAD_FAST                'box'
              260  BUILD_TUPLE_2         2 
              262  BUILD_TUPLE_4         4 

 L. 245       264  BUILD_LIST_1          1 
              266  LOAD_FAST                'self'
              268  STORE_ATTR               tile
              270  POP_BLOCK        
              272  JUMP_FORWARD        296  'to 296'
            274_0  COME_FROM_FINALLY   190  '190'

 L. 248       274  DUP_TOP          
              276  LOAD_GLOBAL              Exception
              278  COMPARE_OP               exception-match
          280_282  POP_JUMP_IF_FALSE   294  'to 294'
              284  POP_TOP          
              286  POP_TOP          
              288  POP_TOP          

 L. 249       290  POP_EXCEPT       
              292  BREAK_LOOP          296  'to 296'
            294_0  COME_FROM           280  '280'
              294  END_FINALLY      
            296_0  COME_FROM           292  '292'
            296_1  COME_FROM           272  '272'
              296  JUMP_FORWARD        420  'to 420'
            298_0  COME_FROM           150  '150'

 L. 252       298  LOAD_GLOBAL              field
              300  LOAD_METHOD              match
              302  LOAD_FAST                's'
              304  CALL_METHOD_1         1  ''
              306  STORE_FAST               'm'

 L. 253       308  LOAD_FAST                'm'
          310_312  POP_JUMP_IF_FALSE   396  'to 396'

 L. 254       314  LOAD_FAST                'm'
              316  LOAD_METHOD              group
              318  LOAD_CONST               1
              320  CALL_METHOD_1         1  ''
              322  STORE_FAST               'k'

 L. 256       324  LOAD_FAST                'k'
              326  LOAD_STR                 'EndComments'
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_FALSE   338  'to 338'

 L. 257   334_336  JUMP_FORWARD        464  'to 464'
            338_0  COME_FROM           330  '330'

 L. 258       338  LOAD_FAST                'k'
              340  LOAD_CONST               None
              342  LOAD_CONST               8
              344  BUILD_SLICE_2         2 
              346  BINARY_SUBSCR    
              348  LOAD_STR                 'PS-Adobe'
              350  COMPARE_OP               ==
          352_354  POP_JUMP_IF_FALSE   384  'to 384'

 L. 259       356  LOAD_FAST                'k'
              358  LOAD_CONST               9
              360  LOAD_CONST               None
              362  BUILD_SLICE_2         2 
              364  BINARY_SUBSCR    
              366  LOAD_FAST                'self'
              368  LOAD_ATTR                info
              370  LOAD_FAST                'k'
              372  LOAD_CONST               None
              374  LOAD_CONST               8
              376  BUILD_SLICE_2         2 
              378  BINARY_SUBSCR    
              380  STORE_SUBSCR     
              382  JUMP_FORWARD        394  'to 394'
            384_0  COME_FROM           352  '352'

 L. 261       384  LOAD_STR                 ''
              386  LOAD_FAST                'self'
              388  LOAD_ATTR                info
              390  LOAD_FAST                'k'
              392  STORE_SUBSCR     
            394_0  COME_FROM           382  '382'
              394  JUMP_FORWARD        420  'to 420'
            396_0  COME_FROM           310  '310'

 L. 262       396  LOAD_FAST                's'
              398  LOAD_CONST               0
              400  BINARY_SUBSCR    
              402  LOAD_STR                 '%'
              404  COMPARE_OP               ==
          406_408  POP_JUMP_IF_FALSE   412  'to 412'

 L. 265       410  JUMP_FORWARD        420  'to 420'
            412_0  COME_FROM           406  '406'

 L. 267       412  LOAD_GLOBAL              OSError
              414  LOAD_STR                 'bad EPS header'
              416  CALL_FUNCTION_1       1  ''
              418  RAISE_VARARGS_1       1  'exception instance'
            420_0  COME_FROM           410  '410'
            420_1  COME_FROM           394  '394'
            420_2  COME_FROM           296  '296'
            420_3  COME_FROM           186  '186'
            420_4  COME_FROM            78  '78'

 L. 269       420  LOAD_FAST                'fp'
              422  LOAD_METHOD              readline
              424  CALL_METHOD_0         0  ''
              426  STORE_FAST               's_raw'

 L. 270       428  LOAD_FAST                's_raw'
              430  LOAD_METHOD              strip
              432  LOAD_STR                 '\r\n'
              434  CALL_METHOD_1         1  ''
              436  STORE_FAST               's'

 L. 272       438  LOAD_FAST                's'
              440  POP_JUMP_IF_FALSE_BACK    70  'to 70'
              442  LOAD_FAST                's'
              444  LOAD_CONST               None
              446  LOAD_CONST               1
              448  BUILD_SLICE_2         2 
              450  BINARY_SUBSCR    
              452  LOAD_STR                 '%'
              454  COMPARE_OP               !=
              456  POP_JUMP_IF_FALSE_BACK    70  'to 70'

 L. 273   458_460  JUMP_FORWARD        464  'to 464'
              462  JUMP_BACK            70  'to 70'
            464_0  COME_FROM           672  '672'
            464_1  COME_FROM           664  '664'
            464_2  COME_FROM           458  '458'
            464_3  COME_FROM           334  '334'
            464_4  COME_FROM            72  '72'

 L. 278       464  LOAD_FAST                's'
              466  LOAD_CONST               None
              468  LOAD_CONST               1
              470  BUILD_SLICE_2         2 
              472  BINARY_SUBSCR    
              474  LOAD_STR                 '%'
              476  COMPARE_OP               ==
          478_480  POP_JUMP_IF_FALSE   676  'to 676'

 L. 280       482  LOAD_GLOBAL              len
              484  LOAD_FAST                's'
              486  CALL_FUNCTION_1       1  ''
              488  LOAD_CONST               255
              490  COMPARE_OP               >
          492_494  POP_JUMP_IF_FALSE   504  'to 504'

 L. 281       496  LOAD_GLOBAL              SyntaxError
              498  LOAD_STR                 'not an EPS file'
              500  CALL_FUNCTION_1       1  ''
              502  RAISE_VARARGS_1       1  'exception instance'
            504_0  COME_FROM           492  '492'

 L. 283       504  LOAD_FAST                's'
              506  LOAD_CONST               None
              508  LOAD_CONST               11
              510  BUILD_SLICE_2         2 
              512  BINARY_SUBSCR    
              514  LOAD_STR                 '%ImageData:'
              516  COMPARE_OP               ==
          518_520  POP_JUMP_IF_FALSE   648  'to 648'

 L. 285       522  LOAD_FAST                's'
              524  LOAD_CONST               11
              526  LOAD_CONST               None
              528  BUILD_SLICE_2         2 
              530  BINARY_SUBSCR    
              532  LOAD_METHOD              split
              534  LOAD_CONST               None
              536  LOAD_CONST               7
              538  CALL_METHOD_2         2  ''
              540  LOAD_CONST               None
              542  LOAD_CONST               4
              544  BUILD_SLICE_2         2 
              546  BINARY_SUBSCR    
              548  UNPACK_SEQUENCE_4     4 
              550  STORE_FAST               'x'
              552  STORE_FAST               'y'
              554  STORE_FAST               'bi'
              556  STORE_FAST               'mo'

 L. 287       558  LOAD_GLOBAL              int
              560  LOAD_FAST                'bi'
              562  CALL_FUNCTION_1       1  ''
              564  LOAD_CONST               8
              566  COMPARE_OP               !=
          568_570  POP_JUMP_IF_FALSE   576  'to 576'

 L. 288   572_574  JUMP_FORWARD        676  'to 676'
            576_0  COME_FROM           568  '568'

 L. 289       576  SETUP_FINALLY       598  'to 598'

 L. 290       578  LOAD_FAST                'self'
              580  LOAD_ATTR                mode_map
              582  LOAD_GLOBAL              int
              584  LOAD_FAST                'mo'
              586  CALL_FUNCTION_1       1  ''
              588  BINARY_SUBSCR    
              590  LOAD_FAST                'self'
              592  STORE_ATTR               mode
              594  POP_BLOCK        
              596  JUMP_FORWARD        626  'to 626'
            598_0  COME_FROM_FINALLY   576  '576'

 L. 291       598  DUP_TOP          
              600  LOAD_GLOBAL              ValueError
              602  COMPARE_OP               exception-match
          604_606  POP_JUMP_IF_FALSE   624  'to 624'
              608  POP_TOP          
              610  POP_TOP          
              612  POP_TOP          

 L. 292       614  POP_EXCEPT       
          616_618  BREAK_LOOP          676  'to 676'
              620  POP_EXCEPT       
              622  JUMP_FORWARD        626  'to 626'
            624_0  COME_FROM           604  '604'
              624  END_FINALLY      
            626_0  COME_FROM           622  '622'
            626_1  COME_FROM           596  '596'

 L. 294       626  LOAD_GLOBAL              int
              628  LOAD_FAST                'x'
              630  CALL_FUNCTION_1       1  ''
              632  LOAD_GLOBAL              int
              634  LOAD_FAST                'y'
              636  CALL_FUNCTION_1       1  ''
              638  BUILD_TUPLE_2         2 
              640  LOAD_FAST                'self'
              642  STORE_ATTR               _size

 L. 295       644  LOAD_CONST               None
              646  RETURN_VALUE     
            648_0  COME_FROM           518  '518'

 L. 297       648  LOAD_FAST                'fp'
              650  LOAD_METHOD              readline
              652  CALL_METHOD_0         0  ''
              654  LOAD_METHOD              strip
              656  LOAD_STR                 '\r\n'
              658  CALL_METHOD_1         1  ''
              660  STORE_FAST               's'

 L. 298       662  LOAD_FAST                's'
          664_666  POP_JUMP_IF_TRUE_BACK   464  'to 464'

 L. 299   668_670  JUMP_FORWARD        676  'to 676'
          672_674  JUMP_BACK           464  'to 464'
            676_0  COME_FROM           668  '668'
            676_1  COME_FROM           616  '616'
            676_2  COME_FROM           572  '572'
            676_3  COME_FROM           478  '478'

 L. 301       676  LOAD_FAST                'box'
          678_680  POP_JUMP_IF_TRUE    690  'to 690'

 L. 302       682  LOAD_GLOBAL              OSError
              684  LOAD_STR                 'cannot determine EPS bounding box'
              686  CALL_FUNCTION_1       1  ''
              688  RAISE_VARARGS_1       1  'exception instance'
            690_0  COME_FROM           678  '678'

Parse error at or near `END_FINALLY' instruction at offset 294

    def _find_offset(self, fp):
        s = fp.read(160)
        if s[:4] == b'%!PS':
            fp.seek(0, io.SEEK_END)
            length = fp.tell
            offset = 0
        elif i32(s[0:4]) == 3335770309:
            offset = i32(s[4:8])
            length = i32(s[8:12])
        else:
            raise SyntaxError('not an EPS file')
        return (
         length, offset)

    def load(self, scale=1):
        if not self.tile:
            return
        self.im = Ghostscript(self.tile, self.size, self.fp, scale)
        self.mode = self.im.mode
        self._size = self.im.size
        self.tile = []

    def load_seek(self, *args, **kwargs):
        pass


def _save(im, fp, filename, eps=1):
    """EPS Writer for the Python Imaging Library."""
    im.load
    if im.mode == 'L':
        operator = (8, 1, 'image')
    elif im.mode == 'RGB':
        operator = (8, 3, 'false 3 colorimage')
    elif im.mode == 'CMYK':
        operator = (8, 4, 'false 4 colorimage')
    else:
        raise ValueError('image mode is not supported')
    base_fp = fp
    wrapped_fp = False
    if fp != sys.stdout:
        fp = io.TextIOWrapper(fp, encoding='latin-1')
        wrapped_fp = True
    try:
        if eps:
            fp.write('%!PS-Adobe-3.0 EPSF-3.0\n')
            fp.write('%%Creator: PIL 0.1 EpsEncode\n')
            fp.write('%%%%BoundingBox: 0 0 %d %d\n' % im.size)
            fp.write('%%Pages: 1\n')
            fp.write('%%EndComments\n')
            fp.write('%%Page: 1 1\n')
            fp.write('%%ImageData: %d %d ' % im.size)
            fp.write('%d %d 0 1 1 "%s"\n' % operator)
        fp.write('gsave\n')
        fp.write('10 dict begin\n')
        fp.write('/buf %d string def\n' % (im.size[0] * operator[1]))
        fp.write('%d %d scale\n' % im.size)
        fp.write('%d %d 8\n' % im.size)
        fp.write('[%d 0 0 -%d 0 %d]\n' % (im.size[0], im.size[1], im.size[1]))
        fp.write('{ currentfile buf readhexstring pop } bind\n')
        fp.write(operator[2] + '\n')
        if hasattr(fp, 'flush'):
            fp.flush
        ImageFile._save(im, base_fp, [('eps', (0, 0) + im.size, 0, None)])
        fp.write('\n%%%%EndBinary\n')
        fp.write('grestore end\n')
        if hasattr(fp, 'flush'):
            fp.flush
    finally:
        if wrapped_fp:
            fp.detach


Image.register_open(EpsImageFile.format, EpsImageFile, _accept)
Image.register_save(EpsImageFile.format, _save)
Image.register_extensions(EpsImageFile.format, ['.ps', '.eps'])
Image.register_mime(EpsImageFile.format, 'application/postscript')