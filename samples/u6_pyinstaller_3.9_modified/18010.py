# uncompyle6 version 3.7.4
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
          172_174  POP_JUMP_IF_FALSE   410  'to 410'

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

 L. 188   200_202  POP_JUMP_IF_FALSE   410  'to 410'

 L. 190       204  LOAD_GLOBAL              len
              206  LOAD_FAST                'args'
              208  CALL_FUNCTION_1       1  ''
              210  LOAD_CONST               3
              212  COMPARE_OP               >=

 L. 188   214_216  POP_JUMP_IF_FALSE   410  'to 410'

 L. 191       218  LOAD_FAST                'args'
              220  LOAD_CONST               0
              222  BINARY_SUBSCR    
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                mode
              228  COMPARE_OP               ==

 L. 188   230_232  POP_JUMP_IF_FALSE   410  'to 410'

 L. 192       234  LOAD_FAST                'args'
              236  LOAD_CONST               0
              238  BINARY_SUBSCR    
              240  LOAD_GLOBAL              Image
              242  LOAD_ATTR                _MAPMODES
              244  <118>                 0  ''

 L. 188   246_248  POP_JUMP_IF_FALSE   410  'to 410'

 L. 194       250  SETUP_FINALLY       378  'to 378'

 L. 196       252  LOAD_CONST               0
              254  LOAD_CONST               None
              256  IMPORT_NAME              mmap
              258  STORE_FAST               'mmap'

 L. 198       260  LOAD_GLOBAL              open
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                filename
              266  CALL_FUNCTION_1       1  ''
              268  SETUP_WITH          310  'to 310'
              270  STORE_FAST               'fp'

 L. 199       272  LOAD_FAST                'mmap'
              274  LOAD_ATTR                mmap
              276  LOAD_FAST                'fp'
              278  LOAD_METHOD              fileno
              280  CALL_METHOD_0         0  ''
              282  LOAD_CONST               0
              284  LOAD_FAST                'mmap'
              286  LOAD_ATTR                ACCESS_READ
              288  LOAD_CONST               ('access',)
              290  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              292  LOAD_FAST                'self'
              294  STORE_ATTR               map
              296  POP_BLOCK        
              298  LOAD_CONST               None
              300  DUP_TOP          
              302  DUP_TOP          
              304  CALL_FUNCTION_3       3  ''
              306  POP_TOP          
              308  JUMP_FORWARD        328  'to 328'
            310_0  COME_FROM_WITH      268  '268'
              310  <49>             
          312_314  POP_JUMP_IF_TRUE    318  'to 318'
              316  <48>             
            318_0  COME_FROM           312  '312'
              318  POP_TOP          
              320  POP_TOP          
              322  POP_TOP          
              324  POP_EXCEPT       
              326  POP_TOP          
            328_0  COME_FROM           308  '308'

 L. 200       328  LOAD_GLOBAL              Image
              330  LOAD_ATTR                core
              332  LOAD_METHOD              map_buffer

 L. 201       334  LOAD_FAST                'self'
              336  LOAD_ATTR                map
              338  LOAD_FAST                'self'
              340  LOAD_ATTR                size
              342  LOAD_FAST                'decoder_name'
              344  LOAD_FAST                'offset'
              346  LOAD_FAST                'args'

 L. 200       348  CALL_METHOD_5         5  ''
              350  LOAD_FAST                'self'
              352  STORE_ATTR               im

 L. 203       354  LOAD_CONST               1
              356  STORE_FAST               'readonly'

 L. 206       358  LOAD_FAST                'self'
              360  LOAD_ATTR                palette
          362_364  POP_JUMP_IF_FALSE   374  'to 374'

 L. 207       366  LOAD_CONST               1
              368  LOAD_FAST                'self'
              370  LOAD_ATTR                palette
              372  STORE_ATTR               dirty
            374_0  COME_FROM           362  '362'
              374  POP_BLOCK        
              376  JUMP_FORWARD        410  'to 410'
            378_0  COME_FROM_FINALLY   250  '250'

 L. 208       378  DUP_TOP          
              380  LOAD_GLOBAL              AttributeError
              382  LOAD_GLOBAL              OSError
              384  LOAD_GLOBAL              ImportError
              386  BUILD_TUPLE_3         3 
          388_390  <121>               408  ''
              392  POP_TOP          
              394  POP_TOP          
              396  POP_TOP          

 L. 209       398  LOAD_CONST               None
              400  LOAD_FAST                'self'
              402  STORE_ATTR               map
              404  POP_EXCEPT       
              406  JUMP_FORWARD        410  'to 410'
              408  <48>             
            410_0  COME_FROM           406  '406'
            410_1  COME_FROM           376  '376'
            410_2  COME_FROM           246  '246'
            410_3  COME_FROM           230  '230'
            410_4  COME_FROM           214  '214'
            410_5  COME_FROM           200  '200'
            410_6  COME_FROM           172  '172'

 L. 211       410  LOAD_FAST                'self'
              412  LOAD_METHOD              load_prepare
              414  CALL_METHOD_0         0  ''
              416  POP_TOP          

 L. 212       418  LOAD_CONST               -3
              420  STORE_FAST               'err_code'

 L. 213       422  LOAD_FAST                'self'
              424  LOAD_ATTR                map
          426_428  POP_JUMP_IF_TRUE    794  'to 794'

 L. 215       430  LOAD_FAST                'self'
              432  LOAD_ATTR                tile
              434  LOAD_ATTR                sort
              436  LOAD_GLOBAL              _tilesort
              438  LOAD_CONST               ('key',)
              440  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              442  POP_TOP          

 L. 217       444  SETUP_FINALLY       456  'to 456'

 L. 219       446  LOAD_FAST                'self'
              448  LOAD_ATTR                tile_prefix
              450  STORE_FAST               'prefix'
              452  POP_BLOCK        
              454  JUMP_FORWARD        480  'to 480'
            456_0  COME_FROM_FINALLY   444  '444'

 L. 220       456  DUP_TOP          
              458  LOAD_GLOBAL              AttributeError
          460_462  <121>               478  ''
              464  POP_TOP          
              466  POP_TOP          
              468  POP_TOP          

 L. 221       470  LOAD_CONST               b''
              472  STORE_FAST               'prefix'
              474  POP_EXCEPT       
              476  JUMP_FORWARD        480  'to 480'
              478  <48>             
            480_0  COME_FROM           476  '476'
            480_1  COME_FROM           454  '454'

 L. 223       480  LOAD_FAST                'self'
              482  LOAD_ATTR                tile
              484  GET_ITER         
          486_488  FOR_ITER            794  'to 794'
              490  UNPACK_SEQUENCE_4     4 
              492  STORE_FAST               'decoder_name'
              494  STORE_FAST               'extents'
              496  STORE_FAST               'offset'
              498  STORE_FAST               'args'

 L. 224       500  LOAD_GLOBAL              Image
              502  LOAD_METHOD              _getdecoder

 L. 225       504  LOAD_FAST                'self'
              506  LOAD_ATTR                mode
              508  LOAD_FAST                'decoder_name'
              510  LOAD_FAST                'args'
              512  LOAD_FAST                'self'
              514  LOAD_ATTR                decoderconfig

 L. 224       516  CALL_METHOD_4         4  ''
              518  STORE_FAST               'decoder'

 L. 227   520_522  SETUP_FINALLY       780  'to 780'

 L. 228       524  LOAD_FAST                'seek'
              526  LOAD_FAST                'offset'
              528  CALL_FUNCTION_1       1  ''
              530  POP_TOP          

 L. 229       532  LOAD_FAST                'decoder'
              534  LOAD_METHOD              setimage
              536  LOAD_FAST                'self'
              538  LOAD_ATTR                im
              540  LOAD_FAST                'extents'
              542  CALL_METHOD_2         2  ''
              544  POP_TOP          

 L. 230       546  LOAD_FAST                'decoder'
              548  LOAD_ATTR                pulls_fd
          550_552  POP_JUMP_IF_FALSE   582  'to 582'

 L. 231       554  LOAD_FAST                'decoder'
              556  LOAD_METHOD              setfd
              558  LOAD_FAST                'self'
              560  LOAD_ATTR                fp
              562  CALL_METHOD_1         1  ''
              564  POP_TOP          

 L. 232       566  LOAD_FAST                'decoder'
              568  LOAD_METHOD              decode
              570  LOAD_CONST               b''
              572  CALL_METHOD_1         1  ''
              574  UNPACK_SEQUENCE_2     2 
              576  STORE_FAST               'status'
              578  STORE_FAST               'err_code'
              580  JUMP_FORWARD        768  'to 768'
            582_0  COME_FROM           550  '550'

 L. 234       582  LOAD_FAST                'prefix'
              584  STORE_FAST               'b'

 L. 236       586  SETUP_FINALLY       602  'to 602'

 L. 237       588  LOAD_FAST                'read'
              590  LOAD_FAST                'self'
              592  LOAD_ATTR                decodermaxblock
              594  CALL_FUNCTION_1       1  ''
              596  STORE_FAST               's'
              598  POP_BLOCK        
              600  JUMP_FORWARD        678  'to 678'
            602_0  COME_FROM_FINALLY   586  '586'

 L. 238       602  DUP_TOP          
              604  LOAD_GLOBAL              IndexError
              606  LOAD_GLOBAL              struct
              608  LOAD_ATTR                error
              610  BUILD_TUPLE_2         2 
          612_614  <121>               676  ''
              616  POP_TOP          
              618  STORE_FAST               'e'
              620  POP_TOP          
              622  SETUP_FINALLY       668  'to 668'

 L. 240       624  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          626_628  POP_JUMP_IF_FALSE   646  'to 646'

 L. 241       630  POP_BLOCK        
              632  POP_EXCEPT       
              634  LOAD_CONST               None
              636  STORE_FAST               'e'
              638  DELETE_FAST              'e'
          640_642  JUMP_ABSOLUTE       768  'to 768'
              644  JUMP_FORWARD        656  'to 656'
            646_0  COME_FROM           626  '626'

 L. 243       646  LOAD_GLOBAL              OSError
              648  LOAD_STR                 'image file is truncated'
              650  CALL_FUNCTION_1       1  ''
              652  LOAD_FAST                'e'
              654  RAISE_VARARGS_2       2  'exception instance with __cause__'
            656_0  COME_FROM           644  '644'
              656  POP_BLOCK        
              658  POP_EXCEPT       
              660  LOAD_CONST               None
              662  STORE_FAST               'e'
              664  DELETE_FAST              'e'
              666  JUMP_FORWARD        678  'to 678'
            668_0  COME_FROM_FINALLY   622  '622'
              668  LOAD_CONST               None
              670  STORE_FAST               'e'
              672  DELETE_FAST              'e'
              674  <48>             
              676  <48>             
            678_0  COME_FROM           666  '666'
            678_1  COME_FROM           600  '600'

 L. 245       678  LOAD_FAST                's'
          680_682  POP_JUMP_IF_TRUE    716  'to 716'

 L. 246       684  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          686_688  POP_JUMP_IF_FALSE   696  'to 696'

 L. 247   690_692  BREAK_LOOP          768  'to 768'
              694  JUMP_FORWARD        716  'to 716'
            696_0  COME_FROM           686  '686'

 L. 249       696  LOAD_GLOBAL              OSError

 L. 250       698  LOAD_STR                 'image file is truncated ('

 L. 251       700  LOAD_GLOBAL              len
              702  LOAD_FAST                'b'
              704  CALL_FUNCTION_1       1  ''

 L. 250       706  FORMAT_VALUE          0  ''
              708  LOAD_STR                 ' bytes not processed)'
              710  BUILD_STRING_3        3 

 L. 249       712  CALL_FUNCTION_1       1  ''
              714  RAISE_VARARGS_1       1  'exception instance'
            716_0  COME_FROM           694  '694'
            716_1  COME_FROM           680  '680'

 L. 254       716  LOAD_FAST                'b'
              718  LOAD_FAST                's'
              720  BINARY_ADD       
              722  STORE_FAST               'b'

 L. 255       724  LOAD_FAST                'decoder'
              726  LOAD_METHOD              decode
              728  LOAD_FAST                'b'
              730  CALL_METHOD_1         1  ''
              732  UNPACK_SEQUENCE_2     2 
              734  STORE_FAST               'n'
              736  STORE_FAST               'err_code'

 L. 256       738  LOAD_FAST                'n'
              740  LOAD_CONST               0
              742  COMPARE_OP               <
          744_746  POP_JUMP_IF_FALSE   752  'to 752'

 L. 257   748_750  BREAK_LOOP          768  'to 768'
            752_0  COME_FROM           744  '744'

 L. 258       752  LOAD_FAST                'b'
              754  LOAD_FAST                'n'
              756  LOAD_CONST               None
              758  BUILD_SLICE_2         2 
              760  BINARY_SUBSCR    
              762  STORE_FAST               'b'
          764_766  JUMP_BACK           586  'to 586'
            768_0  COME_FROM           580  '580'
              768  POP_BLOCK        

 L. 261       770  LOAD_FAST                'decoder'
              772  LOAD_METHOD              cleanup
              774  CALL_METHOD_0         0  ''
              776  POP_TOP          
              778  JUMP_BACK           486  'to 486'
            780_0  COME_FROM_FINALLY   520  '520'
              780  LOAD_FAST                'decoder'
              782  LOAD_METHOD              cleanup
              784  CALL_METHOD_0         0  ''
              786  POP_TOP          
              788  <48>             
          790_792  JUMP_BACK           486  'to 486'
            794_0  COME_FROM           426  '426'

 L. 263       794  BUILD_LIST_0          0 
              796  LOAD_FAST                'self'
              798  STORE_ATTR               tile

 L. 264       800  LOAD_FAST                'readonly'
              802  LOAD_FAST                'self'
              804  STORE_ATTR               readonly

 L. 266       806  LOAD_FAST                'self'
              808  LOAD_METHOD              load_end
              810  CALL_METHOD_0         0  ''
              812  POP_TOP          

 L. 268       814  LOAD_FAST                'self'
              816  LOAD_ATTR                _exclusive_fp
          818_820  POP_JUMP_IF_FALSE   840  'to 840'
              822  LOAD_FAST                'self'
              824  LOAD_ATTR                _close_exclusive_fp_after_loading
          826_828  POP_JUMP_IF_FALSE   840  'to 840'

 L. 269       830  LOAD_FAST                'self'
              832  LOAD_ATTR                fp
              834  LOAD_METHOD              close
              836  CALL_METHOD_0         0  ''
              838  POP_TOP          
            840_0  COME_FROM           826  '826'
            840_1  COME_FROM           818  '818'

 L. 270       840  LOAD_CONST               None
              842  LOAD_FAST                'self'
              844  STORE_ATTR               fp

 L. 272       846  LOAD_FAST                'self'
              848  LOAD_ATTR                map
          850_852  POP_JUMP_IF_TRUE    878  'to 878'
              854  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          856_858  POP_JUMP_IF_TRUE    878  'to 878'
              860  LOAD_FAST                'err_code'
              862  LOAD_CONST               0
              864  COMPARE_OP               <
          866_868  POP_JUMP_IF_FALSE   878  'to 878'

 L. 274       870  LOAD_GLOBAL              raise_oserror
              872  LOAD_FAST                'err_code'
              874  CALL_FUNCTION_1       1  ''
              876  POP_TOP          
            878_0  COME_FROM           866  '866'
            878_1  COME_FROM           856  '856'
            878_2  COME_FROM           850  '850'

 L. 276       878  LOAD_GLOBAL              Image
              880  LOAD_ATTR                Image
              882  LOAD_METHOD              load
              884  LOAD_FAST                'self'
              886  CALL_METHOD_1         1  ''
              888  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def load_prepare(self):
        if not self.im or self.im.mode != self.mode or self.im.size != self.size:
            self.im = Image.core.new(self.mode, self.size)
        if self.mode == 'P':
            Image.Image.loadself

    def load_end(self):
        pass

    def _seek_check--- This code section failed: ---

 L. 300         0  LOAD_FAST                'frame'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _min_frame
                6  COMPARE_OP               <

 L. 299         8  POP_JUMP_IF_TRUE     46  'to 46'

 L. 304        10  LOAD_GLOBAL              hasattr
               12  LOAD_FAST                'self'
               14  LOAD_STR                 '_n_frames'
               16  CALL_FUNCTION_2       2  ''

 L. 299        18  POP_JUMP_IF_FALSE    30  'to 30'

 L. 304        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _n_frames
               24  LOAD_CONST               None
               26  <117>                 0  ''

 L. 299        28  POP_JUMP_IF_TRUE     54  'to 54'
             30_0  COME_FROM            18  '18'

 L. 305        30  LOAD_FAST                'frame'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                n_frames
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _min_frame
               40  BINARY_ADD       
               42  COMPARE_OP               >=

 L. 299        44  POP_JUMP_IF_FALSE    54  'to 54'
             46_0  COME_FROM             8  '8'

 L. 308        46  LOAD_GLOBAL              EOFError
               48  LOAD_STR                 'attempt to seek outside sequence'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'
             54_1  COME_FROM            28  '28'

 L. 310        54  LOAD_FAST                'self'
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

 L. 325         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _load
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'loader'

 L. 326         8  LOAD_FAST                'loader'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    34  'to 34'

 L. 327        16  LOAD_GLOBAL              OSError
               18  LOAD_STR                 'cannot find loader for this '
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                format
               24  FORMAT_VALUE          0  ''
               26  LOAD_STR                 ' file'
               28  BUILD_STRING_3        3 
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            14  '14'

 L. 328        34  LOAD_FAST                'loader'
               36  LOAD_METHOD              load
               38  LOAD_FAST                'self'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'image'

 L. 329        44  LOAD_FAST                'image'
               46  LOAD_CONST               None
               48  <117>                 1  ''
               50  POP_JUMP_IF_TRUE     56  'to 56'
               52  <74>             
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            50  '50'

 L. 331        56  LOAD_FAST                'image'
               58  LOAD_ATTR                __class__
               60  LOAD_FAST                'self'
               62  STORE_ATTR               __class__

 L. 332        64  LOAD_FAST                'image'
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

 L. 358         0  LOAD_FAST                'self'
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

 L. 369         0  LOAD_FAST                'self'
                2  LOAD_ATTR                finished
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 370         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 372        10  LOAD_FAST                'self'
               12  LOAD_ATTR                data
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 373        20  LOAD_FAST                'data'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               data
               26  JUMP_FORWARD         40  'to 40'
             28_0  COME_FROM            18  '18'

 L. 375        28  LOAD_FAST                'self'
               30  LOAD_ATTR                data
               32  LOAD_FAST                'data'
               34  BINARY_ADD       
               36  LOAD_FAST                'self'
               38  STORE_ATTR               data
             40_0  COME_FROM            26  '26'

 L. 378        40  LOAD_FAST                'self'
               42  LOAD_ATTR                decoder
               44  POP_JUMP_IF_FALSE   208  'to 208'

 L. 380        46  LOAD_FAST                'self'
               48  LOAD_ATTR                offset
               50  LOAD_CONST               0
               52  COMPARE_OP               >
               54  POP_JUMP_IF_FALSE   122  'to 122'

 L. 382        56  LOAD_GLOBAL              min
               58  LOAD_GLOBAL              len
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                data
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                offset
               70  CALL_FUNCTION_2       2  ''
               72  STORE_FAST               'skip'

 L. 383        74  LOAD_FAST                'self'
               76  LOAD_ATTR                data
               78  LOAD_FAST                'skip'
               80  LOAD_CONST               None
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    
               86  LOAD_FAST                'self'
               88  STORE_ATTR               data

 L. 384        90  LOAD_FAST                'self'
               92  LOAD_ATTR                offset
               94  LOAD_FAST                'skip'
               96  BINARY_SUBTRACT  
               98  LOAD_FAST                'self'
              100  STORE_ATTR               offset

 L. 385       102  LOAD_FAST                'self'
              104  LOAD_ATTR                offset
              106  LOAD_CONST               0
              108  COMPARE_OP               >
              110  POP_JUMP_IF_TRUE    118  'to 118'
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                data
              116  POP_JUMP_IF_TRUE    122  'to 122'
            118_0  COME_FROM           110  '110'

 L. 386       118  LOAD_CONST               None
              120  RETURN_VALUE     
            122_0  COME_FROM           116  '116'
            122_1  COME_FROM            54  '54'

 L. 388       122  LOAD_FAST                'self'
              124  LOAD_ATTR                decoder
              126  LOAD_METHOD              decode
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                data
              132  CALL_METHOD_1         1  ''
              134  UNPACK_SEQUENCE_2     2 
              136  STORE_FAST               'n'
              138  STORE_FAST               'e'

 L. 390       140  LOAD_FAST                'n'
              142  LOAD_CONST               0
              144  COMPARE_OP               <
              146  POP_JUMP_IF_FALSE   188  'to 188'

 L. 392       148  LOAD_CONST               None
              150  LOAD_FAST                'self'
              152  STORE_ATTR               data

 L. 393       154  LOAD_CONST               1
              156  LOAD_FAST                'self'
              158  STORE_ATTR               finished

 L. 394       160  LOAD_FAST                'e'
              162  LOAD_CONST               0
              164  COMPARE_OP               <
              166  POP_JUMP_IF_FALSE   184  'to 184'

 L. 396       168  LOAD_CONST               None
              170  LOAD_FAST                'self'
              172  STORE_ATTR               image

 L. 397       174  LOAD_GLOBAL              raise_oserror
              176  LOAD_FAST                'e'
              178  CALL_FUNCTION_1       1  ''
              180  POP_TOP          
              182  JUMP_FORWARD        188  'to 188'
            184_0  COME_FROM           166  '166'

 L. 400       184  LOAD_CONST               None
              186  RETURN_VALUE     
            188_0  COME_FROM           182  '182'
            188_1  COME_FROM           146  '146'

 L. 401       188  LOAD_FAST                'self'
              190  LOAD_ATTR                data
              192  LOAD_FAST                'n'
              194  LOAD_CONST               None
              196  BUILD_SLICE_2         2 
              198  BINARY_SUBSCR    
              200  LOAD_FAST                'self'
              202  STORE_ATTR               data
          204_206  JUMP_FORWARD        476  'to 476'
            208_0  COME_FROM            44  '44'

 L. 403       208  LOAD_FAST                'self'
              210  LOAD_ATTR                image
              212  POP_JUMP_IF_FALSE   218  'to 218'

 L. 408   214_216  JUMP_FORWARD        476  'to 476'
            218_0  COME_FROM           212  '212'

 L. 413       218  SETUP_FINALLY       280  'to 280'

 L. 414       220  LOAD_GLOBAL              io
              222  LOAD_METHOD              BytesIO
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                data
              228  CALL_METHOD_1         1  ''
              230  SETUP_WITH          258  'to 258'
              232  STORE_FAST               'fp'

 L. 415       234  LOAD_GLOBAL              Image
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

 L. 416       280  DUP_TOP          
              282  LOAD_GLOBAL              OSError
          284_286  <121>               298  ''
              288  POP_TOP          
              290  POP_TOP          
              292  POP_TOP          

 L. 418       294  POP_EXCEPT       
              296  JUMP_FORWARD        476  'to 476'
              298  <48>             
            300_0  COME_FROM           278  '278'

 L. 420       300  LOAD_GLOBAL              hasattr
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

 L. 421       322  LOAD_FAST                'flag'
          324_326  POP_JUMP_IF_TRUE    344  'to 344'
              328  LOAD_GLOBAL              len
              330  LOAD_FAST                'im'
              332  LOAD_ATTR                tile
              334  CALL_FUNCTION_1       1  ''
              336  LOAD_CONST               1
              338  COMPARE_OP               !=
          340_342  POP_JUMP_IF_FALSE   352  'to 352'
            344_0  COME_FROM           324  '324'

 L. 423       344  LOAD_CONST               None
              346  LOAD_FAST                'self'
              348  STORE_ATTR               decode
              350  JUMP_FORWARD        470  'to 470'
            352_0  COME_FROM           340  '340'

 L. 426       352  LOAD_FAST                'im'
              354  LOAD_METHOD              load_prepare
              356  CALL_METHOD_0         0  ''
              358  POP_TOP          

 L. 427       360  LOAD_FAST                'im'
              362  LOAD_ATTR                tile
              364  LOAD_CONST               0
              366  BINARY_SUBSCR    
              368  UNPACK_SEQUENCE_4     4 
              370  STORE_FAST               'd'
              372  STORE_FAST               'e'
              374  STORE_FAST               'o'
              376  STORE_FAST               'a'

 L. 428       378  BUILD_LIST_0          0 
              380  LOAD_FAST                'im'
              382  STORE_ATTR               tile

 L. 429       384  LOAD_GLOBAL              Image
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

 L. 430       406  LOAD_FAST                'self'
              408  LOAD_ATTR                decoder
              410  LOAD_METHOD              setimage
              412  LOAD_FAST                'im'
              414  LOAD_ATTR                im
              416  LOAD_FAST                'e'
              418  CALL_METHOD_2         2  ''
              420  POP_TOP          

 L. 433       422  LOAD_FAST                'o'
              424  LOAD_FAST                'self'
              426  STORE_ATTR               offset

 L. 434       428  LOAD_FAST                'self'
              430  LOAD_ATTR                offset
              432  LOAD_GLOBAL              len
              434  LOAD_FAST                'self'
              436  LOAD_ATTR                data
              438  CALL_FUNCTION_1       1  ''
              440  COMPARE_OP               <=
          442_444  POP_JUMP_IF_FALSE   470  'to 470'

 L. 435       446  LOAD_FAST                'self'
              448  LOAD_ATTR                data
              450  LOAD_FAST                'self'
              452  LOAD_ATTR                offset
              454  LOAD_CONST               None
              456  BUILD_SLICE_2         2 
              458  BINARY_SUBSCR    
              460  LOAD_FAST                'self'
              462  STORE_ATTR               data

 L. 436       464  LOAD_CONST               0
              466  LOAD_FAST                'self'
              468  STORE_ATTR               offset
            470_0  COME_FROM           442  '442'
            470_1  COME_FROM           350  '350'

 L. 438       470  LOAD_FAST                'im'
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

 L. 456         0  LOAD_FAST                'self'
                2  LOAD_ATTR                decoder
                4  POP_JUMP_IF_FALSE    42  'to 42'

 L. 458         6  LOAD_FAST                'self'
                8  LOAD_METHOD              feed
               10  LOAD_CONST               b''
               12  CALL_METHOD_1         1  ''
               14  POP_TOP          

 L. 459        16  LOAD_CONST               None
               18  DUP_TOP          
               20  LOAD_FAST                'self'
               22  STORE_ATTR               data
               24  LOAD_FAST                'self'
               26  STORE_ATTR               decoder

 L. 460        28  LOAD_FAST                'self'
               30  LOAD_ATTR                finished
               32  POP_JUMP_IF_TRUE     42  'to 42'

 L. 461        34  LOAD_GLOBAL              OSError
               36  LOAD_STR                 'image was incomplete'
               38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            32  '32'
             42_1  COME_FROM             4  '4'

 L. 462        42  LOAD_FAST                'self'
               44  LOAD_ATTR                image
               46  POP_JUMP_IF_TRUE     56  'to 56'

 L. 463        48  LOAD_GLOBAL              OSError
               50  LOAD_STR                 'cannot parse this image'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L. 464        56  LOAD_FAST                'self'
               58  LOAD_ATTR                data
               60  POP_JUMP_IF_FALSE   146  'to 146'

 L. 467        62  LOAD_GLOBAL              io
               64  LOAD_METHOD              BytesIO
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                data
               70  CALL_METHOD_1         1  ''
               72  SETUP_WITH          130  'to 130'
               74  STORE_FAST               'fp'

 L. 468        76  SETUP_FINALLY       104  'to 104'

 L. 469        78  LOAD_GLOBAL              Image
               80  LOAD_METHOD              open
               82  LOAD_FAST                'fp'
               84  CALL_METHOD_1         1  ''
               86  LOAD_FAST                'self'
               88  STORE_ATTR               image
               90  POP_BLOCK        

 L. 471        92  LOAD_FAST                'self'
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

 L. 472       146  LOAD_FAST                'self'
              148  LOAD_ATTR                image
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 92


def _save--- This code section failed: ---

 L. 487         0  LOAD_FAST                'im'
                2  LOAD_METHOD              load
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 488         8  LOAD_GLOBAL              hasattr
               10  LOAD_FAST                'im'
               12  LOAD_STR                 'encoderconfig'
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     24  'to 24'

 L. 489        18  LOAD_CONST               ()
               20  LOAD_FAST                'im'
               22  STORE_ATTR               encoderconfig
             24_0  COME_FROM            16  '16'

 L. 490        24  LOAD_FAST                'tile'
               26  LOAD_ATTR                sort
               28  LOAD_GLOBAL              _tilesort
               30  LOAD_CONST               ('key',)
               32  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               34  POP_TOP          

 L. 495        36  LOAD_GLOBAL              max
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

 L. 496        58  LOAD_FAST                'fp'
               60  LOAD_GLOBAL              sys
               62  LOAD_ATTR                stdout
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    80  'to 80'

 L. 497        68  LOAD_FAST                'fp'
               70  LOAD_METHOD              flush
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          

 L. 498        76  LOAD_CONST               None
               78  RETURN_VALUE     
             80_0  COME_FROM            66  '66'

 L. 499        80  SETUP_FINALLY       102  'to 102'

 L. 500        82  LOAD_FAST                'fp'
               84  LOAD_METHOD              fileno
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'fh'

 L. 501        90  LOAD_FAST                'fp'
               92  LOAD_METHOD              flush
               94  CALL_METHOD_0         0  ''
               96  POP_TOP          
               98  POP_BLOCK        
              100  JUMP_FORWARD        318  'to 318'
            102_0  COME_FROM_FINALLY    80  '80'

 L. 502       102  DUP_TOP          
              104  LOAD_GLOBAL              AttributeError
              106  LOAD_GLOBAL              io
              108  LOAD_ATTR                UnsupportedOperation
              110  BUILD_TUPLE_2         2 
          112_114  <121>               316  ''
              116  POP_TOP          
              118  STORE_FAST               'exc'
              120  POP_TOP          
              122  SETUP_FINALLY       308  'to 308'

 L. 504       124  LOAD_FAST                'tile'
              126  GET_ITER         
              128  FOR_ITER            296  'to 296'
              130  UNPACK_SEQUENCE_4     4 
              132  STORE_FAST               'e'
              134  STORE_FAST               'b'
              136  STORE_FAST               'o'
              138  STORE_FAST               'a'

 L. 505       140  LOAD_GLOBAL              Image
              142  LOAD_METHOD              _getencoder
              144  LOAD_FAST                'im'
              146  LOAD_ATTR                mode
              148  LOAD_FAST                'e'
              150  LOAD_FAST                'a'
              152  LOAD_FAST                'im'
              154  LOAD_ATTR                encoderconfig
              156  CALL_METHOD_4         4  ''
              158  STORE_FAST               'e'

 L. 506       160  LOAD_FAST                'o'
              162  LOAD_CONST               0
              164  COMPARE_OP               >
              166  POP_JUMP_IF_FALSE   178  'to 178'

 L. 507       168  LOAD_FAST                'fp'
              170  LOAD_METHOD              seek
              172  LOAD_FAST                'o'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          
            178_0  COME_FROM           166  '166'

 L. 508       178  LOAD_FAST                'e'
              180  LOAD_METHOD              setimage
              182  LOAD_FAST                'im'
              184  LOAD_ATTR                im
              186  LOAD_FAST                'b'
              188  CALL_METHOD_2         2  ''
              190  POP_TOP          

 L. 509       192  LOAD_FAST                'e'
              194  LOAD_ATTR                pushes_fd
              196  POP_JUMP_IF_FALSE   222  'to 222'

 L. 510       198  LOAD_FAST                'e'
              200  LOAD_METHOD              setfd
              202  LOAD_FAST                'fp'
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          

 L. 511       208  LOAD_FAST                'e'
              210  LOAD_METHOD              encode_to_pyfd
              212  CALL_METHOD_0         0  ''
              214  UNPACK_SEQUENCE_2     2 
              216  STORE_FAST               'l'
              218  STORE_FAST               's'
              220  JUMP_FORWARD        258  'to 258'
            222_0  COME_FROM           250  '250'
            222_1  COME_FROM           196  '196'

 L. 514       222  LOAD_FAST                'e'
              224  LOAD_METHOD              encode
              226  LOAD_FAST                'bufsize'
              228  CALL_METHOD_1         1  ''
              230  UNPACK_SEQUENCE_3     3 
              232  STORE_FAST               'l'
              234  STORE_FAST               's'
              236  STORE_FAST               'd'

 L. 515       238  LOAD_FAST                'fp'
              240  LOAD_METHOD              write
              242  LOAD_FAST                'd'
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L. 516       248  LOAD_FAST                's'
              250  POP_JUMP_IF_FALSE   222  'to 222'

 L. 517   252_254  BREAK_LOOP          258  'to 258'
              256  JUMP_BACK           222  'to 222'
            258_0  COME_FROM           220  '220'

 L. 518       258  LOAD_FAST                's'
              260  LOAD_CONST               0
              262  COMPARE_OP               <
          264_266  POP_JUMP_IF_FALSE   286  'to 286'

 L. 519       268  LOAD_GLOBAL              OSError
              270  LOAD_STR                 'encoder error '
              272  LOAD_FAST                's'
              274  FORMAT_VALUE          0  ''
              276  LOAD_STR                 ' when writing image file'
              278  BUILD_STRING_3        3 
              280  CALL_FUNCTION_1       1  ''
              282  LOAD_FAST                'exc'
              284  RAISE_VARARGS_2       2  'exception instance with __cause__'
            286_0  COME_FROM           264  '264'

 L. 520       286  LOAD_FAST                'e'
              288  LOAD_METHOD              cleanup
              290  CALL_METHOD_0         0  ''
              292  POP_TOP          
              294  JUMP_BACK           128  'to 128'
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

 L. 523       318  LOAD_FAST                'tile'
              320  GET_ITER         
              322  FOR_ITER            470  'to 470'
              324  UNPACK_SEQUENCE_4     4 
              326  STORE_FAST               'e'
              328  STORE_FAST               'b'
              330  STORE_FAST               'o'
              332  STORE_FAST               'a'

 L. 524       334  LOAD_GLOBAL              Image
              336  LOAD_METHOD              _getencoder
              338  LOAD_FAST                'im'
              340  LOAD_ATTR                mode
              342  LOAD_FAST                'e'
              344  LOAD_FAST                'a'
              346  LOAD_FAST                'im'
              348  LOAD_ATTR                encoderconfig
              350  CALL_METHOD_4         4  ''
              352  STORE_FAST               'e'

 L. 525       354  LOAD_FAST                'o'
              356  LOAD_CONST               0
              358  COMPARE_OP               >
          360_362  POP_JUMP_IF_FALSE   374  'to 374'

 L. 526       364  LOAD_FAST                'fp'
              366  LOAD_METHOD              seek
              368  LOAD_FAST                'o'
              370  CALL_METHOD_1         1  ''
              372  POP_TOP          
            374_0  COME_FROM           360  '360'

 L. 527       374  LOAD_FAST                'e'
              376  LOAD_METHOD              setimage
              378  LOAD_FAST                'im'
              380  LOAD_ATTR                im
              382  LOAD_FAST                'b'
              384  CALL_METHOD_2         2  ''
              386  POP_TOP          

 L. 528       388  LOAD_FAST                'e'
              390  LOAD_ATTR                pushes_fd
          392_394  POP_JUMP_IF_FALSE   420  'to 420'

 L. 529       396  LOAD_FAST                'e'
              398  LOAD_METHOD              setfd
              400  LOAD_FAST                'fp'
              402  CALL_METHOD_1         1  ''
              404  POP_TOP          

 L. 530       406  LOAD_FAST                'e'
              408  LOAD_METHOD              encode_to_pyfd
              410  CALL_METHOD_0         0  ''
              412  UNPACK_SEQUENCE_2     2 
              414  STORE_FAST               'l'
              416  STORE_FAST               's'
              418  JUMP_FORWARD        432  'to 432'
            420_0  COME_FROM           392  '392'

 L. 532       420  LOAD_FAST                'e'
              422  LOAD_METHOD              encode_to_file
              424  LOAD_FAST                'fh'
              426  LOAD_FAST                'bufsize'
              428  CALL_METHOD_2         2  ''
              430  STORE_FAST               's'
            432_0  COME_FROM           418  '418'

 L. 533       432  LOAD_FAST                's'
              434  LOAD_CONST               0
              436  COMPARE_OP               <
          438_440  POP_JUMP_IF_FALSE   458  'to 458'

 L. 534       442  LOAD_GLOBAL              OSError
              444  LOAD_STR                 'encoder error '
              446  LOAD_FAST                's'
              448  FORMAT_VALUE          0  ''
              450  LOAD_STR                 ' when writing image file'
              452  BUILD_STRING_3        3 
              454  CALL_FUNCTION_1       1  ''
              456  RAISE_VARARGS_1       1  'exception instance'
            458_0  COME_FROM           438  '438'

 L. 535       458  LOAD_FAST                'e'
              460  LOAD_METHOD              cleanup
              462  CALL_METHOD_0         0  ''
              464  POP_TOP          
          466_468  JUMP_BACK           322  'to 322'
            470_0  COME_FROM           306  '306'

 L. 536       470  LOAD_GLOBAL              hasattr
              472  LOAD_FAST                'fp'
              474  LOAD_STR                 'flush'
              476  CALL_FUNCTION_2       2  ''
          478_480  POP_JUMP_IF_FALSE   490  'to 490'

 L. 537       482  LOAD_FAST                'fp'
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
    :returns: A string containing <i>size</i> bytes of data.

    Raises an OSError if the file is truncated and the read cannot be completed

    """
    if size <= 0:
        return b''
    else:
        if size <= SAFEBLOCK:
            data = fp.readsize
            if len(data) < size:
                raise OSError('Truncated File Read')
            return data
        data = []
        while True:
            if size > 0:
                block = fp.readmin(size, SAFEBLOCK)
                if not block:
                    break
                data.appendblock
                size -= len(block)

    if sum((len(d) for d in data)) < size:
        raise OSError('Truncated File Read')
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
        if self.state.xsize <= 0 or self.state.ysize <= 0:
            raise ValueError('Size cannot be negative')
        if self.state.xsize + self.state.xoff > self.im.size[0] or self.state.ysize + self.state.yoff > self.im.size[1]:
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