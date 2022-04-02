# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\ImageFile.py
import io, struct, sys, warnings
from . import Image
from ._util import isPath
MAXBLOCK = 65536
SAFEBLOCK = 1048576
LOAD_TRUNCATED_IMAGES = False
ERRORS = {-1:'image buffer overrun error', 
 -2:'decoding error', 
 -3:'unknown error', 
 -8:'bad configuration', 
 -9:'out of memory error'}

def raise_oserror--- This code section failed: ---

 L.  61         0  SETUP_FINALLY        18  'to 18'

 L.  62         2  LOAD_GLOBAL              Image
                4  LOAD_ATTR                core
                6  LOAD_METHOD              getcodecstatus
                8  LOAD_FAST                'error'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'message'
               14  POP_BLOCK        
               16  JUMP_FORWARD         46  'to 46'
             18_0  COME_FROM_FINALLY     0  '0'

 L.  63        18  DUP_TOP          
               20  LOAD_GLOBAL              AttributeError
               22  <121>                44  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  64        30  LOAD_GLOBAL              ERRORS
               32  LOAD_METHOD              get
               34  LOAD_FAST                'error'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'message'
               40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
               44  <48>             
             46_0  COME_FROM            42  '42'
             46_1  COME_FROM            16  '16'

 L.  65        46  LOAD_FAST                'message'
               48  POP_JUMP_IF_TRUE     60  'to 60'

 L.  66        50  LOAD_STR                 'decoder error '
               52  LOAD_FAST                'error'
               54  FORMAT_VALUE          0  ''
               56  BUILD_STRING_2        2 
               58  STORE_FAST               'message'
             60_0  COME_FROM            48  '48'

 L.  67        60  LOAD_GLOBAL              OSError
               62  LOAD_FAST                'message'
               64  LOAD_STR                 ' when reading image file'
               66  BINARY_ADD       
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<121>' instruction at offset 22


def raise_ioerror(error):
    warnings.warn('raise_ioerror is deprecated and will be removed in Pillow 9 (2022-01-02). Use raise_oserror instead.', DeprecationWarning)
    return raise_oserror(error)


def _tilesort(t):
    return t[2]


class ImageFile(Image.Image):
    __doc__ = 'Base class for image file format handlers.'

    def __init__--- This code section failed: ---

 L.  93         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              __init__
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          

 L.  95        10  LOAD_CONST               0
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _min_frame

 L.  97        16  LOAD_CONST               None
               18  LOAD_FAST                'self'
               20  STORE_ATTR               custom_mimetype

 L.  99        22  LOAD_CONST               None
               24  LOAD_FAST                'self'
               26  STORE_ATTR               tile

 L. 102        28  LOAD_CONST               1
               30  LOAD_FAST                'self'
               32  STORE_ATTR               readonly

 L. 104        34  LOAD_CONST               ()
               36  LOAD_FAST                'self'
               38  STORE_ATTR               decoderconfig

 L. 105        40  LOAD_GLOBAL              MAXBLOCK
               42  LOAD_FAST                'self'
               44  STORE_ATTR               decodermaxblock

 L. 107        46  LOAD_GLOBAL              isPath
               48  LOAD_FAST                'fp'
               50  CALL_FUNCTION_1       1  ''
               52  POP_JUMP_IF_FALSE    80  'to 80'

 L. 109        54  LOAD_GLOBAL              open
               56  LOAD_FAST                'fp'
               58  LOAD_STR                 'rb'
               60  CALL_FUNCTION_2       2  ''
               62  LOAD_FAST                'self'
               64  STORE_ATTR               fp

 L. 110        66  LOAD_FAST                'fp'
               68  LOAD_FAST                'self'
               70  STORE_ATTR               filename

 L. 111        72  LOAD_CONST               True
               74  LOAD_FAST                'self'
               76  STORE_ATTR               _exclusive_fp
               78  JUMP_FORWARD         98  'to 98'
             80_0  COME_FROM            52  '52'

 L. 114        80  LOAD_FAST                'fp'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               fp

 L. 115        86  LOAD_FAST                'filename'
               88  LOAD_FAST                'self'
               90  STORE_ATTR               filename

 L. 117        92  LOAD_CONST               None
               94  LOAD_FAST                'self'
               96  STORE_ATTR               _exclusive_fp
             98_0  COME_FROM            78  '78'

 L. 119        98  SETUP_FINALLY       204  'to 204'

 L. 120       100  SETUP_FINALLY       114  'to 114'

 L. 121       102  LOAD_FAST                'self'
              104  LOAD_METHOD              _open
              106  CALL_METHOD_0         0  ''
              108  POP_TOP          
              110  POP_BLOCK        
              112  JUMP_FORWARD        172  'to 172'
            114_0  COME_FROM_FINALLY   100  '100'

 L. 122       114  DUP_TOP          

 L. 123       116  LOAD_GLOBAL              IndexError

 L. 124       118  LOAD_GLOBAL              TypeError

 L. 125       120  LOAD_GLOBAL              KeyError

 L. 126       122  LOAD_GLOBAL              EOFError

 L. 127       124  LOAD_GLOBAL              struct
              126  LOAD_ATTR                error

 L. 122       128  BUILD_TUPLE_5         5 
              130  <121>               170  ''
              132  POP_TOP          
              134  STORE_FAST               'v'
              136  POP_TOP          
              138  SETUP_FINALLY       162  'to 162'

 L. 129       140  LOAD_GLOBAL              SyntaxError
              142  LOAD_FAST                'v'
              144  CALL_FUNCTION_1       1  ''
              146  LOAD_FAST                'v'
              148  RAISE_VARARGS_2       2  'exception instance with __cause__'
              150  POP_BLOCK        
              152  POP_EXCEPT       
              154  LOAD_CONST               None
              156  STORE_FAST               'v'
              158  DELETE_FAST              'v'
              160  JUMP_FORWARD        172  'to 172'
            162_0  COME_FROM_FINALLY   138  '138'
              162  LOAD_CONST               None
              164  STORE_FAST               'v'
              166  DELETE_FAST              'v'
              168  <48>             
              170  <48>             
            172_0  COME_FROM           160  '160'
            172_1  COME_FROM           112  '112'

 L. 131       172  LOAD_FAST                'self'
              174  LOAD_ATTR                mode
              176  POP_JUMP_IF_FALSE   192  'to 192'
              178  LOAD_FAST                'self'
              180  LOAD_ATTR                size
              182  LOAD_CONST               0
              184  BINARY_SUBSCR    
              186  LOAD_CONST               0
              188  COMPARE_OP               <=
              190  POP_JUMP_IF_FALSE   200  'to 200'
            192_0  COME_FROM           176  '176'

 L. 132       192  LOAD_GLOBAL              SyntaxError
              194  LOAD_STR                 'not identified by this driver'
              196  CALL_FUNCTION_1       1  ''
              198  RAISE_VARARGS_1       1  'exception instance'
            200_0  COME_FROM           190  '190'
              200  POP_BLOCK        
              202  JUMP_FORWARD        240  'to 240'
            204_0  COME_FROM_FINALLY    98  '98'

 L. 133       204  DUP_TOP          
              206  LOAD_GLOBAL              BaseException
              208  <121>               238  ''
              210  POP_TOP          
              212  POP_TOP          
              214  POP_TOP          

 L. 135       216  LOAD_FAST                'self'
              218  LOAD_ATTR                _exclusive_fp
              220  POP_JUMP_IF_FALSE   232  'to 232'

 L. 136       222  LOAD_FAST                'self'
              224  LOAD_ATTR                fp
              226  LOAD_METHOD              close
              228  CALL_METHOD_0         0  ''
              230  POP_TOP          
            232_0  COME_FROM           220  '220'

 L. 137       232  RAISE_VARARGS_0       0  'reraise'
              234  POP_EXCEPT       
              236  JUMP_FORWARD        240  'to 240'
              238  <48>             
            240_0  COME_FROM           236  '236'
            240_1  COME_FROM           202  '202'

Parse error at or near `<121>' instruction at offset 130

    def get_format_mimetype--- This code section failed: ---

 L. 140         0  LOAD_FAST                'self'
                2  LOAD_ATTR                custom_mimetype
                4  POP_JUMP_IF_FALSE    12  'to 12'

 L. 141         6  LOAD_FAST                'self'
                8  LOAD_ATTR                custom_mimetype
               10  RETURN_VALUE     
             12_0  COME_FROM             4  '4'

 L. 142        12  LOAD_FAST                'self'
               14  LOAD_ATTR                format
               16  LOAD_CONST               None
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    40  'to 40'

 L. 143        22  LOAD_GLOBAL              Image
               24  LOAD_ATTR                MIME
               26  LOAD_METHOD              get
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                format
               32  LOAD_METHOD              upper
               34  CALL_METHOD_0         0  ''
               36  CALL_METHOD_1         1  ''
               38  RETURN_VALUE     
             40_0  COME_FROM            20  '20'

Parse error at or near `<117>' instruction at offset 18

    def verify(self):
        """Check file integrity"""
        if self._exclusive_fp:
            self.fp.close
        self.fp = None

    def load--- This code section failed: ---

 L. 157         0  LOAD_FAST                'self'
                2  LOAD_ATTR                tile
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 158        10  LOAD_GLOBAL              OSError
               12  LOAD_STR                 'cannot load this image'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 160        18  LOAD_GLOBAL              Image
               20  LOAD_ATTR                Image
               22  LOAD_METHOD              load
               24  LOAD_FAST                'self'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'pixel'

 L. 161        30  LOAD_FAST                'self'
               32  LOAD_ATTR                tile
               34  POP_JUMP_IF_TRUE     40  'to 40'

 L. 162        36  LOAD_FAST                'pixel'
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L. 164        40  LOAD_CONST               None
               42  LOAD_FAST                'self'
               44  STORE_ATTR               map

 L. 165        46  LOAD_FAST                'self'
               48  LOAD_ATTR                filename
               50  JUMP_IF_FALSE_OR_POP    64  'to 64'
               52  LOAD_GLOBAL              len
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                tile
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_CONST               1
               62  COMPARE_OP               ==
             64_0  COME_FROM            50  '50'
               64  STORE_FAST               'use_mmap'

 L. 167        66  LOAD_FAST                'use_mmap'
               68  JUMP_IF_FALSE_OR_POP    80  'to 80'
               70  LOAD_GLOBAL              hasattr
               72  LOAD_GLOBAL              sys
               74  LOAD_STR                 'pypy_version_info'
               76  CALL_FUNCTION_2       2  ''
               78  UNARY_NOT        
             80_0  COME_FROM            68  '68'
               80  STORE_FAST               'use_mmap'

 L. 169        82  LOAD_CONST               0
               84  STORE_FAST               'readonly'

 L. 172        86  SETUP_FINALLY       102  'to 102'

 L. 173        88  LOAD_FAST                'self'
               90  LOAD_ATTR                load_read
               92  STORE_FAST               'read'

 L. 175        94  LOAD_CONST               False
               96  STORE_FAST               'use_mmap'
               98  POP_BLOCK        
              100  JUMP_FORWARD        128  'to 128'
            102_0  COME_FROM_FINALLY    86  '86'

 L. 176       102  DUP_TOP          
              104  LOAD_GLOBAL              AttributeError
              106  <121>               126  ''
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 177       114  LOAD_FAST                'self'
              116  LOAD_ATTR                fp
              118  LOAD_ATTR                read
              120  STORE_FAST               'read'
              122  POP_EXCEPT       
              124  JUMP_FORWARD        128  'to 128'
              126  <48>             
            128_0  COME_FROM           124  '124'
            128_1  COME_FROM           100  '100'

 L. 179       128  SETUP_FINALLY       144  'to 144'

 L. 180       130  LOAD_FAST                'self'
              132  LOAD_ATTR                load_seek
              134  STORE_FAST               'seek'

 L. 181       136  LOAD_CONST               False
              138  STORE_FAST               'use_mmap'
              140  POP_BLOCK        
              142  JUMP_FORWARD        170  'to 170'
            144_0  COME_FROM_FINALLY   128  '128'

 L. 182       144  DUP_TOP          
              146  LOAD_GLOBAL              AttributeError
              148  <121>               168  ''
              150  POP_TOP          
              152  POP_TOP          
              154  POP_TOP          

 L. 183       156  LOAD_FAST                'self'
              158  LOAD_ATTR                fp
              160  LOAD_ATTR                seek
              162  STORE_FAST               'seek'
              164  POP_EXCEPT       
              166  JUMP_FORWARD        170  'to 170'
              168  <48>             
            170_0  COME_FROM           166  '166'
            170_1  COME_FROM           142  '142'

 L. 185       170  LOAD_FAST                'use_mmap'
          172_174  POP_JUMP_IF_FALSE   486  'to 486'

 L. 187       176  LOAD_FAST                'self'
              178  LOAD_ATTR                tile
              180  LOAD_CONST               0
              182  BINARY_SUBSCR    
              184  UNPACK_SEQUENCE_4     4 
              186  STORE_FAST               'decoder_name'
              188  STORE_FAST               'extents'
              190  STORE_FAST               'offset'
              192  STORE_FAST               'args'

 L. 189       194  LOAD_FAST                'decoder_name'
              196  LOAD_STR                 'raw'
              198  COMPARE_OP               ==

 L. 188   200_202  POP_JUMP_IF_FALSE   486  'to 486'

 L. 190       204  LOAD_GLOBAL              len
              206  LOAD_FAST                'args'
              208  CALL_FUNCTION_1       1  ''
              210  LOAD_CONST               3
              212  COMPARE_OP               >=

 L. 188   214_216  POP_JUMP_IF_FALSE   486  'to 486'

 L. 191       218  LOAD_FAST                'args'
              220  LOAD_CONST               0
              222  BINARY_SUBSCR    
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                mode
              228  COMPARE_OP               ==

 L. 188   230_232  POP_JUMP_IF_FALSE   486  'to 486'

 L. 192       234  LOAD_FAST                'args'
              236  LOAD_CONST               0
              238  BINARY_SUBSCR    
              240  LOAD_GLOBAL              Image
              242  LOAD_ATTR                _MAPMODES
              244  <118>                 0  ''

 L. 188   246_248  POP_JUMP_IF_FALSE   486  'to 486'

 L. 194       250  SETUP_FINALLY       454  'to 454'

 L. 195       252  LOAD_GLOBAL              hasattr
              254  LOAD_GLOBAL              Image
              256  LOAD_ATTR                core
              258  LOAD_STR                 'map'
              260  CALL_FUNCTION_2       2  ''
          262_264  POP_JUMP_IF_FALSE   328  'to 328'

 L. 197       266  LOAD_GLOBAL              Image
              268  LOAD_ATTR                core
              270  LOAD_METHOD              map
              272  LOAD_FAST                'self'
              274  LOAD_ATTR                filename
              276  CALL_METHOD_1         1  ''
              278  LOAD_FAST                'self'
              280  STORE_ATTR               map

 L. 198       282  LOAD_FAST                'self'
              284  LOAD_ATTR                map
              286  LOAD_METHOD              seek
              288  LOAD_FAST                'offset'
              290  CALL_METHOD_1         1  ''
              292  POP_TOP          

 L. 199       294  LOAD_FAST                'self'
              296  LOAD_ATTR                map
              298  LOAD_METHOD              readimage

 L. 200       300  LOAD_FAST                'self'
              302  LOAD_ATTR                mode
              304  LOAD_FAST                'self'
              306  LOAD_ATTR                size
              308  LOAD_FAST                'args'
              310  LOAD_CONST               1
              312  BINARY_SUBSCR    
              314  LOAD_FAST                'args'
              316  LOAD_CONST               2
              318  BINARY_SUBSCR    

 L. 199       320  CALL_METHOD_4         4  ''
              322  LOAD_FAST                'self'
              324  STORE_ATTR               im
              326  JUMP_FORWARD        430  'to 430'
            328_0  COME_FROM           262  '262'

 L. 204       328  LOAD_CONST               0
              330  LOAD_CONST               None
              332  IMPORT_NAME              mmap
              334  STORE_FAST               'mmap'

 L. 206       336  LOAD_GLOBAL              open
              338  LOAD_FAST                'self'
              340  LOAD_ATTR                filename
              342  CALL_FUNCTION_1       1  ''
              344  SETUP_WITH          386  'to 386'
              346  STORE_FAST               'fp'

 L. 207       348  LOAD_FAST                'mmap'
              350  LOAD_ATTR                mmap

 L. 208       352  LOAD_FAST                'fp'
              354  LOAD_METHOD              fileno
              356  CALL_METHOD_0         0  ''
              358  LOAD_CONST               0
              360  LOAD_FAST                'mmap'
              362  LOAD_ATTR                ACCESS_READ

 L. 207       364  LOAD_CONST               ('access',)
              366  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              368  LOAD_FAST                'self'
              370  STORE_ATTR               map
              372  POP_BLOCK        
              374  LOAD_CONST               None
              376  DUP_TOP          
              378  DUP_TOP          
              380  CALL_FUNCTION_3       3  ''
              382  POP_TOP          
              384  JUMP_FORWARD        404  'to 404'
            386_0  COME_FROM_WITH      344  '344'
              386  <49>             
          388_390  POP_JUMP_IF_TRUE    394  'to 394'
              392  <48>             
            394_0  COME_FROM           388  '388'
              394  POP_TOP          
              396  POP_TOP          
              398  POP_TOP          
              400  POP_EXCEPT       
              402  POP_TOP          
            404_0  COME_FROM           384  '384'

 L. 210       404  LOAD_GLOBAL              Image
              406  LOAD_ATTR                core
              408  LOAD_METHOD              map_buffer

 L. 211       410  LOAD_FAST                'self'
              412  LOAD_ATTR                map
              414  LOAD_FAST                'self'
              416  LOAD_ATTR                size
              418  LOAD_FAST                'decoder_name'
              420  LOAD_FAST                'offset'
              422  LOAD_FAST                'args'

 L. 210       424  CALL_METHOD_5         5  ''
              426  LOAD_FAST                'self'
              428  STORE_ATTR               im
            430_0  COME_FROM           326  '326'

 L. 213       430  LOAD_CONST               1
              432  STORE_FAST               'readonly'

 L. 216       434  LOAD_FAST                'self'
              436  LOAD_ATTR                palette
          438_440  POP_JUMP_IF_FALSE   450  'to 450'

 L. 217       442  LOAD_CONST               1
              444  LOAD_FAST                'self'
              446  LOAD_ATTR                palette
              448  STORE_ATTR               dirty
            450_0  COME_FROM           438  '438'
              450  POP_BLOCK        
              452  JUMP_FORWARD        486  'to 486'
            454_0  COME_FROM_FINALLY   250  '250'

 L. 218       454  DUP_TOP          
              456  LOAD_GLOBAL              AttributeError
              458  LOAD_GLOBAL              OSError
              460  LOAD_GLOBAL              ImportError
              462  BUILD_TUPLE_3         3 
          464_466  <121>               484  ''
              468  POP_TOP          
              470  POP_TOP          
              472  POP_TOP          

 L. 219       474  LOAD_CONST               None
              476  LOAD_FAST                'self'
              478  STORE_ATTR               map
              480  POP_EXCEPT       
              482  JUMP_FORWARD        486  'to 486'
              484  <48>             
            486_0  COME_FROM           482  '482'
            486_1  COME_FROM           452  '452'
            486_2  COME_FROM           246  '246'
            486_3  COME_FROM           230  '230'
            486_4  COME_FROM           214  '214'
            486_5  COME_FROM           200  '200'
            486_6  COME_FROM           172  '172'

 L. 221       486  LOAD_FAST                'self'
              488  LOAD_METHOD              load_prepare
              490  CALL_METHOD_0         0  ''
              492  POP_TOP          

 L. 222       494  LOAD_CONST               -3
              496  STORE_FAST               'err_code'

 L. 223       498  LOAD_FAST                'self'
              500  LOAD_ATTR                map
          502_504  POP_JUMP_IF_TRUE    870  'to 870'

 L. 225       506  LOAD_FAST                'self'
              508  LOAD_ATTR                tile
              510  LOAD_ATTR                sort
              512  LOAD_GLOBAL              _tilesort
              514  LOAD_CONST               ('key',)
              516  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              518  POP_TOP          

 L. 227       520  SETUP_FINALLY       532  'to 532'

 L. 229       522  LOAD_FAST                'self'
              524  LOAD_ATTR                tile_prefix
              526  STORE_FAST               'prefix'
              528  POP_BLOCK        
              530  JUMP_FORWARD        556  'to 556'
            532_0  COME_FROM_FINALLY   520  '520'

 L. 230       532  DUP_TOP          
              534  LOAD_GLOBAL              AttributeError
          536_538  <121>               554  ''
              540  POP_TOP          
              542  POP_TOP          
              544  POP_TOP          

 L. 231       546  LOAD_CONST               b''
              548  STORE_FAST               'prefix'
              550  POP_EXCEPT       
              552  JUMP_FORWARD        556  'to 556'
              554  <48>             
            556_0  COME_FROM           552  '552'
            556_1  COME_FROM           530  '530'

 L. 233       556  LOAD_FAST                'self'
              558  LOAD_ATTR                tile
              560  GET_ITER         
            562_0  COME_FROM           866  '866'
            562_1  COME_FROM           854  '854'
          562_564  FOR_ITER            870  'to 870'
              566  UNPACK_SEQUENCE_4     4 
              568  STORE_FAST               'decoder_name'
              570  STORE_FAST               'extents'
              572  STORE_FAST               'offset'
              574  STORE_FAST               'args'

 L. 234       576  LOAD_GLOBAL              Image
              578  LOAD_METHOD              _getdecoder

 L. 235       580  LOAD_FAST                'self'
              582  LOAD_ATTR                mode
              584  LOAD_FAST                'decoder_name'
              586  LOAD_FAST                'args'
              588  LOAD_FAST                'self'
              590  LOAD_ATTR                decoderconfig

 L. 234       592  CALL_METHOD_4         4  ''
              594  STORE_FAST               'decoder'

 L. 237   596_598  SETUP_FINALLY       856  'to 856'

 L. 238       600  LOAD_FAST                'seek'
              602  LOAD_FAST                'offset'
              604  CALL_FUNCTION_1       1  ''
              606  POP_TOP          

 L. 239       608  LOAD_FAST                'decoder'
              610  LOAD_METHOD              setimage
              612  LOAD_FAST                'self'
              614  LOAD_ATTR                im
              616  LOAD_FAST                'extents'
              618  CALL_METHOD_2         2  ''
              620  POP_TOP          

 L. 240       622  LOAD_FAST                'decoder'
              624  LOAD_ATTR                pulls_fd
          626_628  POP_JUMP_IF_FALSE   658  'to 658'

 L. 241       630  LOAD_FAST                'decoder'
              632  LOAD_METHOD              setfd
              634  LOAD_FAST                'self'
              636  LOAD_ATTR                fp
              638  CALL_METHOD_1         1  ''
              640  POP_TOP          

 L. 242       642  LOAD_FAST                'decoder'
              644  LOAD_METHOD              decode
              646  LOAD_CONST               b''
              648  CALL_METHOD_1         1  ''
              650  UNPACK_SEQUENCE_2     2 
              652  STORE_FAST               'status'
              654  STORE_FAST               'err_code'
              656  JUMP_FORWARD        844  'to 844'
            658_0  COME_FROM           626  '626'

 L. 244       658  LOAD_FAST                'prefix'
              660  STORE_FAST               'b'
            662_0  COME_FROM           840  '840'

 L. 246       662  SETUP_FINALLY       678  'to 678'

 L. 247       664  LOAD_FAST                'read'
              666  LOAD_FAST                'self'
              668  LOAD_ATTR                decodermaxblock
              670  CALL_FUNCTION_1       1  ''
              672  STORE_FAST               's'
              674  POP_BLOCK        
              676  JUMP_FORWARD        754  'to 754'
            678_0  COME_FROM_FINALLY   662  '662'

 L. 248       678  DUP_TOP          
              680  LOAD_GLOBAL              IndexError
              682  LOAD_GLOBAL              struct
              684  LOAD_ATTR                error
              686  BUILD_TUPLE_2         2 
          688_690  <121>               752  ''
              692  POP_TOP          
              694  STORE_FAST               'e'
              696  POP_TOP          
              698  SETUP_FINALLY       744  'to 744'

 L. 250       700  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          702_704  POP_JUMP_IF_FALSE   722  'to 722'

 L. 251       706  POP_BLOCK        
              708  POP_EXCEPT       
              710  LOAD_CONST               None
              712  STORE_FAST               'e'
              714  DELETE_FAST              'e'
          716_718  JUMP_FORWARD        844  'to 844'
              720  JUMP_FORWARD        732  'to 732'
            722_0  COME_FROM           702  '702'

 L. 253       722  LOAD_GLOBAL              OSError
              724  LOAD_STR                 'image file is truncated'
              726  CALL_FUNCTION_1       1  ''
              728  LOAD_FAST                'e'
              730  RAISE_VARARGS_2       2  'exception instance with __cause__'
            732_0  COME_FROM           720  '720'
              732  POP_BLOCK        
              734  POP_EXCEPT       
              736  LOAD_CONST               None
              738  STORE_FAST               'e'
              740  DELETE_FAST              'e'
              742  JUMP_FORWARD        754  'to 754'
            744_0  COME_FROM_FINALLY   698  '698'
              744  LOAD_CONST               None
              746  STORE_FAST               'e'
              748  DELETE_FAST              'e'
              750  <48>             
              752  <48>             
            754_0  COME_FROM           742  '742'
            754_1  COME_FROM           676  '676'

 L. 255       754  LOAD_FAST                's'
          756_758  POP_JUMP_IF_TRUE    792  'to 792'

 L. 256       760  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          762_764  POP_JUMP_IF_FALSE   772  'to 772'

 L. 257   766_768  JUMP_FORWARD        844  'to 844'
              770  BREAK_LOOP          792  'to 792'
            772_0  COME_FROM           762  '762'

 L. 259       772  LOAD_GLOBAL              OSError

 L. 260       774  LOAD_STR                 'image file is truncated ('

 L. 261       776  LOAD_GLOBAL              len
              778  LOAD_FAST                'b'
              780  CALL_FUNCTION_1       1  ''

 L. 260       782  FORMAT_VALUE          0  ''
              784  LOAD_STR                 ' bytes not processed)'
              786  BUILD_STRING_3        3 

 L. 259       788  CALL_FUNCTION_1       1  ''
              790  RAISE_VARARGS_1       1  'exception instance'
            792_0  COME_FROM           770  '770'
            792_1  COME_FROM           756  '756'

 L. 264       792  LOAD_FAST                'b'
              794  LOAD_FAST                's'
              796  BINARY_ADD       
              798  STORE_FAST               'b'

 L. 265       800  LOAD_FAST                'decoder'
              802  LOAD_METHOD              decode
              804  LOAD_FAST                'b'
              806  CALL_METHOD_1         1  ''
              808  UNPACK_SEQUENCE_2     2 
              810  STORE_FAST               'n'
              812  STORE_FAST               'err_code'

 L. 266       814  LOAD_FAST                'n'
              816  LOAD_CONST               0
              818  COMPARE_OP               <
          820_822  POP_JUMP_IF_FALSE   828  'to 828'

 L. 267   824_826  JUMP_FORWARD        844  'to 844'
            828_0  COME_FROM           820  '820'

 L. 268       828  LOAD_FAST                'b'
              830  LOAD_FAST                'n'
              832  LOAD_CONST               None
              834  BUILD_SLICE_2         2 
              836  BINARY_SUBSCR    
              838  STORE_FAST               'b'
          840_842  JUMP_BACK           662  'to 662'
            844_0  COME_FROM           824  '824'
            844_1  COME_FROM           766  '766'
            844_2  COME_FROM           716  '716'
            844_3  COME_FROM           656  '656'
              844  POP_BLOCK        

 L. 271       846  LOAD_FAST                'decoder'
              848  LOAD_METHOD              cleanup
              850  CALL_METHOD_0         0  ''
              852  POP_TOP          
              854  JUMP_BACK           562  'to 562'
            856_0  COME_FROM_FINALLY   596  '596'
              856  LOAD_FAST                'decoder'
              858  LOAD_METHOD              cleanup
              860  CALL_METHOD_0         0  ''
              862  POP_TOP          
              864  <48>             
          866_868  JUMP_BACK           562  'to 562'
            870_0  COME_FROM           562  '562'
            870_1  COME_FROM           502  '502'

 L. 273       870  BUILD_LIST_0          0 
              872  LOAD_FAST                'self'
              874  STORE_ATTR               tile

 L. 274       876  LOAD_FAST                'readonly'
              878  LOAD_FAST                'self'
              880  STORE_ATTR               readonly

 L. 276       882  LOAD_FAST                'self'
              884  LOAD_METHOD              load_end
              886  CALL_METHOD_0         0  ''
              888  POP_TOP          

 L. 278       890  LOAD_FAST                'self'
              892  LOAD_ATTR                _exclusive_fp
          894_896  POP_JUMP_IF_FALSE   916  'to 916'
              898  LOAD_FAST                'self'
              900  LOAD_ATTR                _close_exclusive_fp_after_loading
          902_904  POP_JUMP_IF_FALSE   916  'to 916'

 L. 279       906  LOAD_FAST                'self'
              908  LOAD_ATTR                fp
              910  LOAD_METHOD              close
              912  CALL_METHOD_0         0  ''
              914  POP_TOP          
            916_0  COME_FROM           902  '902'
            916_1  COME_FROM           894  '894'

 L. 280       916  LOAD_CONST               None
              918  LOAD_FAST                'self'
              920  STORE_ATTR               fp

 L. 282       922  LOAD_FAST                'self'
              924  LOAD_ATTR                map
          926_928  POP_JUMP_IF_TRUE    954  'to 954'
              930  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          932_934  POP_JUMP_IF_TRUE    954  'to 954'
              936  LOAD_FAST                'err_code'
              938  LOAD_CONST               0
              940  COMPARE_OP               <
          942_944  POP_JUMP_IF_FALSE   954  'to 954'

 L. 284       946  LOAD_GLOBAL              raise_oserror
              948  LOAD_FAST                'err_code'
              950  CALL_FUNCTION_1       1  ''
              952  POP_TOP          
            954_0  COME_FROM           942  '942'
            954_1  COME_FROM           932  '932'
            954_2  COME_FROM           926  '926'

 L. 286       954  LOAD_GLOBAL              Image
              956  LOAD_ATTR                Image
              958  LOAD_METHOD              load
              960  LOAD_FAST                'self'
              962  CALL_METHOD_1         1  ''
              964  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def load_prepare(self):
        if self.im:
            if self.im.mode != self.mode or (self.im.size != self.size):
                self.im = Image.core.new(self.mode, self.size)
            if self.mode == 'P':
                Image.Image.loadself

    def load_end(self):
        pass

    def _seek_check--- This code section failed: ---

 L. 310         0  LOAD_FAST                'frame'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _min_frame
                6  COMPARE_OP               <

 L. 309         8  POP_JUMP_IF_TRUE     46  'to 46'

 L. 314        10  LOAD_GLOBAL              hasattr
               12  LOAD_FAST                'self'
               14  LOAD_STR                 '_n_frames'
               16  CALL_FUNCTION_2       2  ''

 L. 309        18  POP_JUMP_IF_FALSE    30  'to 30'

 L. 314        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _n_frames
               24  LOAD_CONST               None
               26  <117>                 0  ''

 L. 309        28  POP_JUMP_IF_TRUE     54  'to 54'
             30_0  COME_FROM            18  '18'

 L. 315        30  LOAD_FAST                'frame'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                n_frames
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _min_frame
               40  BINARY_ADD       
               42  COMPARE_OP               >=

 L. 309        44  POP_JUMP_IF_FALSE    54  'to 54'
             46_0  COME_FROM             8  '8'

 L. 318        46  LOAD_GLOBAL              EOFError
               48  LOAD_STR                 'attempt to seek outside sequence'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'
             54_1  COME_FROM            28  '28'

 L. 320        54  LOAD_FAST                'self'
               56  LOAD_METHOD              tell
               58  CALL_METHOD_0         0  ''
               60  LOAD_FAST                'frame'
               62  COMPARE_OP               !=
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26


class StubImageFile(ImageFile):
    __doc__ = '\n    Base class for stub image loaders.\n\n    A stub loader is an image loader that can identify files of a\n    certain format, but relies on external code to load the file.\n    '

    def _open(self):
        raise NotImplementedError('StubImageFile subclass must implement _open')

    def load--- This code section failed: ---

 L. 335         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _load
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'loader'

 L. 336         8  LOAD_FAST                'loader'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    34  'to 34'

 L. 337        16  LOAD_GLOBAL              OSError
               18  LOAD_STR                 'cannot find loader for this '
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                format
               24  FORMAT_VALUE          0  ''
               26  LOAD_STR                 ' file'
               28  BUILD_STRING_3        3 
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            14  '14'

 L. 338        34  LOAD_FAST                'loader'
               36  LOAD_METHOD              load
               38  LOAD_FAST                'self'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'image'

 L. 339        44  LOAD_FAST                'image'
               46  LOAD_CONST               None
               48  <117>                 1  ''
               50  POP_JUMP_IF_TRUE     56  'to 56'
               52  <74>             
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            50  '50'

 L. 341        56  LOAD_FAST                'image'
               58  LOAD_ATTR                __class__
               60  LOAD_FAST                'self'
               62  STORE_ATTR               __class__

 L. 342        64  LOAD_FAST                'image'
               66  LOAD_ATTR                __dict__
               68  LOAD_FAST                'self'
               70  STORE_ATTR               __dict__

Parse error at or near `<117>' instruction at offset 12

    def _load(self):
        """(Hook) Find actual image loader."""
        raise NotImplementedError('StubImageFile subclass must implement _load')


class Parser:
    __doc__ = '\n    Incremental image parser.  This class implements the standard\n    feed/close consumer interface.\n    '
    incremental = None
    image = None
    data = None
    decoder = None
    offset = 0
    finished = 0

    def reset--- This code section failed: ---

 L. 368         0  LOAD_FAST                'self'
                2  LOAD_ATTR                data
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'
               10  <74>             
               12  LOAD_STR                 'cannot reuse parsers'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def feed--- This code section failed: ---

 L. 379         0  LOAD_FAST                'self'
                2  LOAD_ATTR                finished
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 380         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 382        10  LOAD_FAST                'self'
               12  LOAD_ATTR                data
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 383        20  LOAD_FAST                'data'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               data
               26  JUMP_FORWARD         40  'to 40'
             28_0  COME_FROM            18  '18'

 L. 385        28  LOAD_FAST                'self'
               30  LOAD_ATTR                data
               32  LOAD_FAST                'data'
               34  BINARY_ADD       
               36  LOAD_FAST                'self'
               38  STORE_ATTR               data
             40_0  COME_FROM            26  '26'

 L. 388        40  LOAD_FAST                'self'
               42  LOAD_ATTR                decoder
               44  POP_JUMP_IF_FALSE   208  'to 208'

 L. 390        46  LOAD_FAST                'self'
               48  LOAD_ATTR                offset
               50  LOAD_CONST               0
               52  COMPARE_OP               >
               54  POP_JUMP_IF_FALSE   122  'to 122'

 L. 392        56  LOAD_GLOBAL              min
               58  LOAD_GLOBAL              len
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                data
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                offset
               70  CALL_FUNCTION_2       2  ''
               72  STORE_FAST               'skip'

 L. 393        74  LOAD_FAST                'self'
               76  LOAD_ATTR                data
               78  LOAD_FAST                'skip'
               80  LOAD_CONST               None
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    
               86  LOAD_FAST                'self'
               88  STORE_ATTR               data

 L. 394        90  LOAD_FAST                'self'
               92  LOAD_ATTR                offset
               94  LOAD_FAST                'skip'
               96  BINARY_SUBTRACT  
               98  LOAD_FAST                'self'
              100  STORE_ATTR               offset

 L. 395       102  LOAD_FAST                'self'
              104  LOAD_ATTR                offset
              106  LOAD_CONST               0
              108  COMPARE_OP               >
              110  POP_JUMP_IF_TRUE    118  'to 118'
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                data
              116  POP_JUMP_IF_TRUE    122  'to 122'
            118_0  COME_FROM           110  '110'

 L. 396       118  LOAD_CONST               None
              120  RETURN_VALUE     
            122_0  COME_FROM           116  '116'
            122_1  COME_FROM            54  '54'

 L. 398       122  LOAD_FAST                'self'
              124  LOAD_ATTR                decoder
              126  LOAD_METHOD              decode
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                data
              132  CALL_METHOD_1         1  ''
              134  UNPACK_SEQUENCE_2     2 
              136  STORE_FAST               'n'
              138  STORE_FAST               'e'

 L. 400       140  LOAD_FAST                'n'
              142  LOAD_CONST               0
              144  COMPARE_OP               <
              146  POP_JUMP_IF_FALSE   188  'to 188'

 L. 402       148  LOAD_CONST               None
              150  LOAD_FAST                'self'
              152  STORE_ATTR               data

 L. 403       154  LOAD_CONST               1
              156  LOAD_FAST                'self'
              158  STORE_ATTR               finished

 L. 404       160  LOAD_FAST                'e'
              162  LOAD_CONST               0
              164  COMPARE_OP               <
              166  POP_JUMP_IF_FALSE   184  'to 184'

 L. 406       168  LOAD_CONST               None
              170  LOAD_FAST                'self'
              172  STORE_ATTR               image

 L. 407       174  LOAD_GLOBAL              raise_oserror
              176  LOAD_FAST                'e'
              178  CALL_FUNCTION_1       1  ''
              180  POP_TOP          
              182  JUMP_FORWARD        188  'to 188'
            184_0  COME_FROM           166  '166'

 L. 410       184  LOAD_CONST               None
              186  RETURN_VALUE     
            188_0  COME_FROM           182  '182'
            188_1  COME_FROM           146  '146'

 L. 411       188  LOAD_FAST                'self'
              190  LOAD_ATTR                data
              192  LOAD_FAST                'n'
              194  LOAD_CONST               None
              196  BUILD_SLICE_2         2 
              198  BINARY_SUBSCR    
              200  LOAD_FAST                'self'
              202  STORE_ATTR               data
          204_206  JUMP_FORWARD        476  'to 476'
            208_0  COME_FROM            44  '44'

 L. 413       208  LOAD_FAST                'self'
              210  LOAD_ATTR                image
              212  POP_JUMP_IF_FALSE   218  'to 218'

 L. 418   214_216  JUMP_FORWARD        476  'to 476'
            218_0  COME_FROM           212  '212'

 L. 423       218  SETUP_FINALLY       280  'to 280'

 L. 424       220  LOAD_GLOBAL              io
              222  LOAD_METHOD              BytesIO
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                data
              228  CALL_METHOD_1         1  ''
              230  SETUP_WITH          258  'to 258'
              232  STORE_FAST               'fp'

 L. 425       234  LOAD_GLOBAL              Image
              236  LOAD_METHOD              open
              238  LOAD_FAST                'fp'
              240  CALL_METHOD_1         1  ''
              242  STORE_FAST               'im'
              244  POP_BLOCK        
              246  LOAD_CONST               None
              248  DUP_TOP          
              250  DUP_TOP          
              252  CALL_FUNCTION_3       3  ''
              254  POP_TOP          
              256  JUMP_FORWARD        276  'to 276'
            258_0  COME_FROM_WITH      230  '230'
              258  <49>             
          260_262  POP_JUMP_IF_TRUE    266  'to 266'
              264  <48>             
            266_0  COME_FROM           260  '260'
              266  POP_TOP          
              268  POP_TOP          
              270  POP_TOP          
              272  POP_EXCEPT       
              274  POP_TOP          
            276_0  COME_FROM           256  '256'
              276  POP_BLOCK        
              278  JUMP_FORWARD        300  'to 300'
            280_0  COME_FROM_FINALLY   218  '218'

 L. 426       280  DUP_TOP          
              282  LOAD_GLOBAL              OSError
          284_286  <121>               298  ''
              288  POP_TOP          
              290  POP_TOP          
              292  POP_TOP          

 L. 428       294  POP_EXCEPT       
              296  JUMP_FORWARD        476  'to 476'
              298  <48>             
            300_0  COME_FROM           278  '278'

 L. 430       300  LOAD_GLOBAL              hasattr
              302  LOAD_FAST                'im'
              304  LOAD_STR                 'load_seek'
              306  CALL_FUNCTION_2       2  ''
          308_310  JUMP_IF_TRUE_OR_POP   320  'to 320'
              312  LOAD_GLOBAL              hasattr
              314  LOAD_FAST                'im'
              316  LOAD_STR                 'load_read'
              318  CALL_FUNCTION_2       2  ''
            320_0  COME_FROM           308  '308'
              320  STORE_FAST               'flag'

 L. 431       322  LOAD_FAST                'flag'
          324_326  POP_JUMP_IF_TRUE    344  'to 344'
              328  LOAD_GLOBAL              len
              330  LOAD_FAST                'im'
              332  LOAD_ATTR                tile
              334  CALL_FUNCTION_1       1  ''
              336  LOAD_CONST               1
              338  COMPARE_OP               !=
          340_342  POP_JUMP_IF_FALSE   352  'to 352'
            344_0  COME_FROM           324  '324'

 L. 433       344  LOAD_CONST               None
              346  LOAD_FAST                'self'
              348  STORE_ATTR               decode
              350  JUMP_FORWARD        470  'to 470'
            352_0  COME_FROM           340  '340'

 L. 436       352  LOAD_FAST                'im'
              354  LOAD_METHOD              load_prepare
              356  CALL_METHOD_0         0  ''
              358  POP_TOP          

 L. 437       360  LOAD_FAST                'im'
              362  LOAD_ATTR                tile
              364  LOAD_CONST               0
              366  BINARY_SUBSCR    
              368  UNPACK_SEQUENCE_4     4 
              370  STORE_FAST               'd'
              372  STORE_FAST               'e'
              374  STORE_FAST               'o'
              376  STORE_FAST               'a'

 L. 438       378  BUILD_LIST_0          0 
              380  LOAD_FAST                'im'
              382  STORE_ATTR               tile

 L. 439       384  LOAD_GLOBAL              Image
              386  LOAD_METHOD              _getdecoder
              388  LOAD_FAST                'im'
              390  LOAD_ATTR                mode
              392  LOAD_FAST                'd'
              394  LOAD_FAST                'a'
              396  LOAD_FAST                'im'
              398  LOAD_ATTR                decoderconfig
              400  CALL_METHOD_4         4  ''
              402  LOAD_FAST                'self'
              404  STORE_ATTR               decoder

 L. 440       406  LOAD_FAST                'self'
              408  LOAD_ATTR                decoder
              410  LOAD_METHOD              setimage
              412  LOAD_FAST                'im'
              414  LOAD_ATTR                im
              416  LOAD_FAST                'e'
              418  CALL_METHOD_2         2  ''
              420  POP_TOP          

 L. 443       422  LOAD_FAST                'o'
              424  LOAD_FAST                'self'
              426  STORE_ATTR               offset

 L. 444       428  LOAD_FAST                'self'
              430  LOAD_ATTR                offset
              432  LOAD_GLOBAL              len
              434  LOAD_FAST                'self'
              436  LOAD_ATTR                data
              438  CALL_FUNCTION_1       1  ''
              440  COMPARE_OP               <=
          442_444  POP_JUMP_IF_FALSE   470  'to 470'

 L. 445       446  LOAD_FAST                'self'
              448  LOAD_ATTR                data
              450  LOAD_FAST                'self'
              452  LOAD_ATTR                offset
              454  LOAD_CONST               None
              456  BUILD_SLICE_2         2 
              458  BINARY_SUBSCR    
              460  LOAD_FAST                'self'
              462  STORE_ATTR               data

 L. 446       464  LOAD_CONST               0
              466  LOAD_FAST                'self'
              468  STORE_ATTR               offset
            470_0  COME_FROM           442  '442'
            470_1  COME_FROM           350  '350'

 L. 448       470  LOAD_FAST                'im'
              472  LOAD_FAST                'self'
              474  STORE_ATTR               image
            476_0  COME_FROM           296  '296'
            476_1  COME_FROM           214  '214'
            476_2  COME_FROM           204  '204'

Parse error at or near `<117>' instruction at offset 16

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close

    def close--- This code section failed: ---

 L. 466         0  LOAD_FAST                'self'
                2  LOAD_ATTR                decoder
                4  POP_JUMP_IF_FALSE    42  'to 42'

 L. 468         6  LOAD_FAST                'self'
                8  LOAD_METHOD              feed
               10  LOAD_CONST               b''
               12  CALL_METHOD_1         1  ''
               14  POP_TOP          

 L. 469        16  LOAD_CONST               None
               18  DUP_TOP          
               20  LOAD_FAST                'self'
               22  STORE_ATTR               data
               24  LOAD_FAST                'self'
               26  STORE_ATTR               decoder

 L. 470        28  LOAD_FAST                'self'
               30  LOAD_ATTR                finished
               32  POP_JUMP_IF_TRUE     42  'to 42'

 L. 471        34  LOAD_GLOBAL              OSError
               36  LOAD_STR                 'image was incomplete'
               38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            32  '32'
             42_1  COME_FROM             4  '4'

 L. 472        42  LOAD_FAST                'self'
               44  LOAD_ATTR                image
               46  POP_JUMP_IF_TRUE     56  'to 56'

 L. 473        48  LOAD_GLOBAL              OSError
               50  LOAD_STR                 'cannot parse this image'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L. 474        56  LOAD_FAST                'self'
               58  LOAD_ATTR                data
               60  POP_JUMP_IF_FALSE   146  'to 146'

 L. 477        62  LOAD_GLOBAL              io
               64  LOAD_METHOD              BytesIO
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                data
               70  CALL_METHOD_1         1  ''
               72  SETUP_WITH          130  'to 130'
               74  STORE_FAST               'fp'

 L. 478        76  SETUP_FINALLY       104  'to 104'

 L. 479        78  LOAD_GLOBAL              Image
               80  LOAD_METHOD              open
               82  LOAD_FAST                'fp'
               84  CALL_METHOD_1         1  ''
               86  LOAD_FAST                'self'
               88  STORE_ATTR               image
               90  POP_BLOCK        

 L. 481        92  LOAD_FAST                'self'
               94  LOAD_ATTR                image
               96  LOAD_METHOD              load
               98  CALL_METHOD_0         0  ''
              100  POP_TOP          
              102  JUMP_FORWARD        116  'to 116'
            104_0  COME_FROM_FINALLY    76  '76'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                image
              108  LOAD_METHOD              load
              110  CALL_METHOD_0         0  ''
              112  POP_TOP          
              114  <48>             
            116_0  COME_FROM           102  '102'
              116  POP_BLOCK        
              118  LOAD_CONST               None
              120  DUP_TOP          
              122  DUP_TOP          
              124  CALL_FUNCTION_3       3  ''
              126  POP_TOP          
              128  JUMP_FORWARD        146  'to 146'
            130_0  COME_FROM_WITH       72  '72'
              130  <49>             
              132  POP_JUMP_IF_TRUE    136  'to 136'
              134  <48>             
            136_0  COME_FROM           132  '132'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          
              142  POP_EXCEPT       
              144  POP_TOP          
            146_0  COME_FROM           128  '128'
            146_1  COME_FROM            60  '60'

 L. 482       146  LOAD_FAST                'self'
              148  LOAD_ATTR                image
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 100


def _save--- This code section failed: ---

 L. 497         0  LOAD_FAST                'im'
                2  LOAD_METHOD              load
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 498         8  LOAD_GLOBAL              hasattr
               10  LOAD_FAST                'im'
               12  LOAD_STR                 'encoderconfig'
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     24  'to 24'

 L. 499        18  LOAD_CONST               ()
               20  LOAD_FAST                'im'
               22  STORE_ATTR               encoderconfig
             24_0  COME_FROM            16  '16'

 L. 500        24  LOAD_FAST                'tile'
               26  LOAD_ATTR                sort
               28  LOAD_GLOBAL              _tilesort
               30  LOAD_CONST               ('key',)
               32  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               34  POP_TOP          

 L. 505        36  LOAD_GLOBAL              max
               38  LOAD_GLOBAL              MAXBLOCK
               40  LOAD_FAST                'bufsize'
               42  LOAD_FAST                'im'
               44  LOAD_ATTR                size
               46  LOAD_CONST               0
               48  BINARY_SUBSCR    
               50  LOAD_CONST               4
               52  BINARY_MULTIPLY  
               54  CALL_FUNCTION_3       3  ''
               56  STORE_FAST               'bufsize'

 L. 506        58  LOAD_FAST                'fp'
               60  LOAD_GLOBAL              sys
               62  LOAD_ATTR                stdout
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    80  'to 80'

 L. 507        68  LOAD_FAST                'fp'
               70  LOAD_METHOD              flush
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          

 L. 508        76  LOAD_CONST               None
               78  RETURN_VALUE     
             80_0  COME_FROM            66  '66'

 L. 509        80  SETUP_FINALLY       102  'to 102'

 L. 510        82  LOAD_FAST                'fp'
               84  LOAD_METHOD              fileno
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'fh'

 L. 511        90  LOAD_FAST                'fp'
               92  LOAD_METHOD              flush
               94  CALL_METHOD_0         0  ''
               96  POP_TOP          
               98  POP_BLOCK        
              100  JUMP_FORWARD        318  'to 318'
            102_0  COME_FROM_FINALLY    80  '80'

 L. 512       102  DUP_TOP          
              104  LOAD_GLOBAL              AttributeError
              106  LOAD_GLOBAL              io
              108  LOAD_ATTR                UnsupportedOperation
              110  BUILD_TUPLE_2         2 
          112_114  <121>               316  ''
              116  POP_TOP          
              118  STORE_FAST               'exc'
              120  POP_TOP          
              122  SETUP_FINALLY       308  'to 308'

 L. 514       124  LOAD_FAST                'tile'
              126  GET_ITER         
            128_0  COME_FROM           294  '294'
              128  FOR_ITER            296  'to 296'
              130  UNPACK_SEQUENCE_4     4 
              132  STORE_FAST               'e'
              134  STORE_FAST               'b'
              136  STORE_FAST               'o'
              138  STORE_FAST               'a'

 L. 515       140  LOAD_GLOBAL              Image
              142  LOAD_METHOD              _getencoder
              144  LOAD_FAST                'im'
              146  LOAD_ATTR                mode
              148  LOAD_FAST                'e'
              150  LOAD_FAST                'a'
              152  LOAD_FAST                'im'
              154  LOAD_ATTR                encoderconfig
              156  CALL_METHOD_4         4  ''
              158  STORE_FAST               'e'

 L. 516       160  LOAD_FAST                'o'
              162  LOAD_CONST               0
              164  COMPARE_OP               >
              166  POP_JUMP_IF_FALSE   178  'to 178'

 L. 517       168  LOAD_FAST                'fp'
              170  LOAD_METHOD              seek
              172  LOAD_FAST                'o'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          
            178_0  COME_FROM           166  '166'

 L. 518       178  LOAD_FAST                'e'
              180  LOAD_METHOD              setimage
              182  LOAD_FAST                'im'
              184  LOAD_ATTR                im
              186  LOAD_FAST                'b'
              188  CALL_METHOD_2         2  ''
              190  POP_TOP          

 L. 519       192  LOAD_FAST                'e'
              194  LOAD_ATTR                pushes_fd
              196  POP_JUMP_IF_FALSE   222  'to 222'

 L. 520       198  LOAD_FAST                'e'
              200  LOAD_METHOD              setfd
              202  LOAD_FAST                'fp'
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          

 L. 521       208  LOAD_FAST                'e'
              210  LOAD_METHOD              encode_to_pyfd
              212  CALL_METHOD_0         0  ''
              214  UNPACK_SEQUENCE_2     2 
              216  STORE_FAST               'l'
              218  STORE_FAST               's'
              220  JUMP_FORWARD        258  'to 258'
            222_0  COME_FROM           256  '256'
            222_1  COME_FROM           250  '250'
            222_2  COME_FROM           196  '196'

 L. 524       222  LOAD_FAST                'e'
              224  LOAD_METHOD              encode
              226  LOAD_FAST                'bufsize'
              228  CALL_METHOD_1         1  ''
              230  UNPACK_SEQUENCE_3     3 
              232  STORE_FAST               'l'
              234  STORE_FAST               's'
              236  STORE_FAST               'd'

 L. 525       238  LOAD_FAST                'fp'
              240  LOAD_METHOD              write
              242  LOAD_FAST                'd'
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L. 526       248  LOAD_FAST                's'
              250  POP_JUMP_IF_FALSE_BACK   222  'to 222'

 L. 527   252_254  JUMP_FORWARD        258  'to 258'
              256  JUMP_BACK           222  'to 222'
            258_0  COME_FROM           252  '252'
            258_1  COME_FROM           220  '220'

 L. 528       258  LOAD_FAST                's'
              260  LOAD_CONST               0
              262  COMPARE_OP               <
          264_266  POP_JUMP_IF_FALSE   286  'to 286'

 L. 529       268  LOAD_GLOBAL              OSError
              270  LOAD_STR                 'encoder error '
              272  LOAD_FAST                's'
              274  FORMAT_VALUE          0  ''
              276  LOAD_STR                 ' when writing image file'
              278  BUILD_STRING_3        3 
              280  CALL_FUNCTION_1       1  ''
              282  LOAD_FAST                'exc'
              284  RAISE_VARARGS_2       2  'exception instance with __cause__'
            286_0  COME_FROM           264  '264'

 L. 530       286  LOAD_FAST                'e'
              288  LOAD_METHOD              cleanup
              290  CALL_METHOD_0         0  ''
              292  POP_TOP          
              294  JUMP_BACK           128  'to 128'
            296_0  COME_FROM           128  '128'
              296  POP_BLOCK        
              298  POP_EXCEPT       
              300  LOAD_CONST               None
              302  STORE_FAST               'exc'
              304  DELETE_FAST              'exc'
              306  JUMP_FORWARD        470  'to 470'
            308_0  COME_FROM_FINALLY   122  '122'
              308  LOAD_CONST               None
              310  STORE_FAST               'exc'
              312  DELETE_FAST              'exc'
              314  <48>             
              316  <48>             
            318_0  COME_FROM           100  '100'

 L. 533       318  LOAD_FAST                'tile'
              320  GET_ITER         
            322_0  COME_FROM           466  '466'
              322  FOR_ITER            470  'to 470'
              324  UNPACK_SEQUENCE_4     4 
              326  STORE_FAST               'e'
              328  STORE_FAST               'b'
              330  STORE_FAST               'o'
              332  STORE_FAST               'a'

 L. 534       334  LOAD_GLOBAL              Image
              336  LOAD_METHOD              _getencoder
              338  LOAD_FAST                'im'
              340  LOAD_ATTR                mode
              342  LOAD_FAST                'e'
              344  LOAD_FAST                'a'
              346  LOAD_FAST                'im'
              348  LOAD_ATTR                encoderconfig
              350  CALL_METHOD_4         4  ''
              352  STORE_FAST               'e'

 L. 535       354  LOAD_FAST                'o'
              356  LOAD_CONST               0
              358  COMPARE_OP               >
          360_362  POP_JUMP_IF_FALSE   374  'to 374'

 L. 536       364  LOAD_FAST                'fp'
              366  LOAD_METHOD              seek
              368  LOAD_FAST                'o'
              370  CALL_METHOD_1         1  ''
              372  POP_TOP          
            374_0  COME_FROM           360  '360'

 L. 537       374  LOAD_FAST                'e'
              376  LOAD_METHOD              setimage
              378  LOAD_FAST                'im'
              380  LOAD_ATTR                im
              382  LOAD_FAST                'b'
              384  CALL_METHOD_2         2  ''
              386  POP_TOP          

 L. 538       388  LOAD_FAST                'e'
              390  LOAD_ATTR                pushes_fd
          392_394  POP_JUMP_IF_FALSE   420  'to 420'

 L. 539       396  LOAD_FAST                'e'
              398  LOAD_METHOD              setfd
              400  LOAD_FAST                'fp'
              402  CALL_METHOD_1         1  ''
              404  POP_TOP          

 L. 540       406  LOAD_FAST                'e'
              408  LOAD_METHOD              encode_to_pyfd
              410  CALL_METHOD_0         0  ''
              412  UNPACK_SEQUENCE_2     2 
              414  STORE_FAST               'l'
              416  STORE_FAST               's'
              418  JUMP_FORWARD        432  'to 432'
            420_0  COME_FROM           392  '392'

 L. 542       420  LOAD_FAST                'e'
              422  LOAD_METHOD              encode_to_file
              424  LOAD_FAST                'fh'
              426  LOAD_FAST                'bufsize'
              428  CALL_METHOD_2         2  ''
              430  STORE_FAST               's'
            432_0  COME_FROM           418  '418'

 L. 543       432  LOAD_FAST                's'
              434  LOAD_CONST               0
              436  COMPARE_OP               <
          438_440  POP_JUMP_IF_FALSE   458  'to 458'

 L. 544       442  LOAD_GLOBAL              OSError
              444  LOAD_STR                 'encoder error '
              446  LOAD_FAST                's'
              448  FORMAT_VALUE          0  ''
              450  LOAD_STR                 ' when writing image file'
              452  BUILD_STRING_3        3 
              454  CALL_FUNCTION_1       1  ''
              456  RAISE_VARARGS_1       1  'exception instance'
            458_0  COME_FROM           438  '438'

 L. 545       458  LOAD_FAST                'e'
              460  LOAD_METHOD              cleanup
              462  CALL_METHOD_0         0  ''
              464  POP_TOP          
          466_468  JUMP_BACK           322  'to 322'
            470_0  COME_FROM           322  '322'
            470_1  COME_FROM           306  '306'

 L. 546       470  LOAD_GLOBAL              hasattr
              472  LOAD_FAST                'fp'
              474  LOAD_STR                 'flush'
              476  CALL_FUNCTION_2       2  ''
          478_480  POP_JUMP_IF_FALSE   490  'to 490'

 L. 547       482  LOAD_FAST                'fp'
              484  LOAD_METHOD              flush
              486  CALL_METHOD_0         0  ''
              488  POP_TOP          
            490_0  COME_FROM           478  '478'

Parse error at or near `<121>' instruction at offset 112_114


def _safe_read(fp, size):
    """
    Reads large blocks in a safe way.  Unlike fp.read(n), this function
    doesn't trust the user.  If the requested size is larger than
    SAFEBLOCK, the file is read block by block.

    :param fp: File handle.  Must implement a <b>read</b> method.
    :param size: Number of bytes to read.
    :returns: A string containing up to <i>size</i> bytes of data.
    """
    if size <= 0:
        return b''
    if size <= SAFEBLOCK:
        return fp.readsize
    data = []
    while True:
        if size > 0:
            block = fp.readmin(size, SAFEBLOCK)
            if not block:
                pass
            else:
                data.appendblock
                size -= len(block)

    return (b'').joindata


class PyCodecState:

    def __init__(self):
        self.xsize = 0
        self.ysize = 0
        self.xoff = 0
        self.yoff = 0

    def extents(self):
        return (
         self.xoff, self.yoff, self.xoff + self.xsize, self.yoff + self.ysize)


class PyDecoder:
    __doc__ = '\n    Python implementation of a format decoder. Override this class and\n    add the decoding logic in the :meth:`decode` method.\n\n    See :ref:`Writing Your Own File Decoder in Python<file-decoders-py>`\n    '
    _pulls_fd = False

    def __init__(self, mode, *args):
        self.im = None
        self.state = PyCodecState
        self.fd = None
        self.mode = mode
        self.initargs

    def init(self, args):
        """
        Override to perform decoder specific initialization

        :param args: Array of args items from the tile entry
        :returns: None
        """
        self.args = args

    @property
    def pulls_fd(self):
        return self._pulls_fd

    def decode(self, buffer):
        """
        Override to perform the decoding process.

        :param buffer: A bytes object with the data to be decoded.
        :returns: A tuple of ``(bytes consumed, errcode)``.
            If finished with decoding return <0 for the bytes consumed.
            Err codes are from :data:`.ImageFile.ERRORS`.
        """
        raise NotImplementedError

    def cleanup(self):
        """
        Override to perform decoder specific cleanup

        :returns: None
        """
        pass

    def setfd(self, fd):
        """
        Called from ImageFile to set the python file-like object

        :param fd: A python file-like object
        :returns: None
        """
        self.fd = fd

    def setimage(self, im, extents=None):
        """
        Called from ImageFile to set the core output image for the decoder

        :param im: A core image object
        :param extents: a 4 tuple of (x0, y0, x1, y1) defining the rectangle
            for this tile
        :returns: None
        """
        self.im = im
        if extents:
            x0, y0, x1, y1 = extents
        else:
            x0, y0, x1, y1 = (0, 0, 0, 0)
        if x0 == 0 and x1 == 0:
            self.state.xsize, self.state.ysize = self.im.size
        else:
            self.state.xoff = x0
            self.state.yoff = y0
            self.state.xsize = x1 - x0
            self.state.ysize = y1 - y0
        if self.state.xsize <= 0 or (self.state.ysize <= 0):
            raise ValueError('Size cannot be negative')
        if self.state.xsize + self.state.xoff > self.im.size[0] or (self.state.ysize + self.state.yoff > self.im.size[1]):
            raise ValueError('Tile cannot extend outside image')

    def set_as_raw(self, data, rawmode=None):
        """
        Convenience method to set the internal image from a stream of raw data

        :param data: Bytes to be set
        :param rawmode: The rawmode to be used for the decoder.
            If not specified, it will default to the mode of the image
        :returns: None
        """
        if not rawmode:
            rawmode = self.mode
        d = Image._getdecoder(self.mode, 'raw', rawmode)
        d.setimage(self.im, self.state.extents)
        s = d.decodedata
        if s[0] >= 0:
            raise ValueError('not enough image data')
        if s[1] != 0:
            raise ValueError('cannot decode image data')