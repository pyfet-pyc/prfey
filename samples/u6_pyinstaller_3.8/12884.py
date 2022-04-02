# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
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

def raise_oserror(error):
    try:
        message = Image.core.getcodecstatus(error)
    except AttributeError:
        message = ERRORS.get(error)
    else:
        if not message:
            message = f"decoder error {error}"
        raise OSError(message + ' when reading image file')


def raise_ioerror(error):
    warnings.warn('raise_ioerror is deprecated and will be removed in Pillow 9 (2022-01-02). Use raise_oserror instead.', DeprecationWarning)
    return raise_oserror(error)


def _tilesort(t):
    return t[2]


class ImageFile(Image.Image):
    __doc__ = 'Base class for image file format handlers.'

    def __init__(self, fp=None, filename=None):
        super().__init__()
        self._min_frame = 0
        self.custom_mimetype = None
        self.tile = None
        self.readonly = 1
        self.decoderconfig = ()
        self.decodermaxblock = MAXBLOCK
        if isPath(fp):
            self.fp = open(fp, 'rb')
            self.filename = fp
            self._exclusive_fp = True
        else:
            self.fp = fp
            self.filename = filename
            self._exclusive_fp = None
        try:
            try:
                self._open()
            except (IndexError,
             TypeError,
             KeyError,
             EOFError,
             struct.error) as v:
                try:
                    raise SyntaxError(v) from v
                finally:
                    v = None
                    del v

            else:
                if not self.mode or self.size[0] <= 0:
                    raise SyntaxError('not identified by this driver')
        except BaseException:
            if self._exclusive_fp:
                self.fp.close()
            raise

    def get_format_mimetype(self):
        if self.custom_mimetype:
            return self.custom_mimetype
        if self.format is not None:
            return Image.MIME.get(self.format.upper())

    def verify(self):
        """Check file integrity"""
        if self._exclusive_fp:
            self.fp.close()
        self.fp = None

    def load--- This code section failed: ---

 L. 157         0  LOAD_FAST                'self'
                2  LOAD_ATTR                tile
                4  LOAD_CONST               None
                6  COMPARE_OP               is
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
              100  JUMP_FORWARD        130  'to 130'
            102_0  COME_FROM_FINALLY    86  '86'

 L. 176       102  DUP_TOP          
              104  LOAD_GLOBAL              AttributeError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   128  'to 128'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 177       116  LOAD_FAST                'self'
              118  LOAD_ATTR                fp
              120  LOAD_ATTR                read
              122  STORE_FAST               'read'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM           108  '108'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           100  '100'

 L. 179       130  SETUP_FINALLY       146  'to 146'

 L. 180       132  LOAD_FAST                'self'
              134  LOAD_ATTR                load_seek
              136  STORE_FAST               'seek'

 L. 181       138  LOAD_CONST               False
              140  STORE_FAST               'use_mmap'
              142  POP_BLOCK        
              144  JUMP_FORWARD        174  'to 174'
            146_0  COME_FROM_FINALLY   130  '130'

 L. 182       146  DUP_TOP          
              148  LOAD_GLOBAL              AttributeError
              150  COMPARE_OP               exception-match
              152  POP_JUMP_IF_FALSE   172  'to 172'
              154  POP_TOP          
              156  POP_TOP          
              158  POP_TOP          

 L. 183       160  LOAD_FAST                'self'
              162  LOAD_ATTR                fp
              164  LOAD_ATTR                seek
              166  STORE_FAST               'seek'
              168  POP_EXCEPT       
              170  JUMP_FORWARD        174  'to 174'
            172_0  COME_FROM           152  '152'
              172  END_FINALLY      
            174_0  COME_FROM           170  '170'
            174_1  COME_FROM           144  '144'

 L. 185       174  LOAD_FAST                'use_mmap'
          176_178  POP_JUMP_IF_FALSE   470  'to 470'

 L. 187       180  LOAD_FAST                'self'
              182  LOAD_ATTR                tile
              184  LOAD_CONST               0
              186  BINARY_SUBSCR    
              188  UNPACK_SEQUENCE_4     4 
              190  STORE_FAST               'decoder_name'
              192  STORE_FAST               'extents'
              194  STORE_FAST               'offset'
              196  STORE_FAST               'args'

 L. 189       198  LOAD_FAST                'decoder_name'
              200  LOAD_STR                 'raw'
              202  COMPARE_OP               ==

 L. 188   204_206  POP_JUMP_IF_FALSE   470  'to 470'

 L. 190       208  LOAD_GLOBAL              len
              210  LOAD_FAST                'args'
              212  CALL_FUNCTION_1       1  ''
              214  LOAD_CONST               3
              216  COMPARE_OP               >=

 L. 188   218_220  POP_JUMP_IF_FALSE   470  'to 470'

 L. 191       222  LOAD_FAST                'args'
              224  LOAD_CONST               0
              226  BINARY_SUBSCR    
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                mode
              232  COMPARE_OP               ==

 L. 188   234_236  POP_JUMP_IF_FALSE   470  'to 470'

 L. 192       238  LOAD_FAST                'args'
              240  LOAD_CONST               0
              242  BINARY_SUBSCR    
              244  LOAD_GLOBAL              Image
              246  LOAD_ATTR                _MAPMODES
              248  COMPARE_OP               in

 L. 188   250_252  POP_JUMP_IF_FALSE   470  'to 470'

 L. 194       254  SETUP_FINALLY       436  'to 436'

 L. 195       256  LOAD_GLOBAL              hasattr
              258  LOAD_GLOBAL              Image
              260  LOAD_ATTR                core
              262  LOAD_STR                 'map'
              264  CALL_FUNCTION_2       2  ''
          266_268  POP_JUMP_IF_FALSE   332  'to 332'

 L. 197       270  LOAD_GLOBAL              Image
              272  LOAD_ATTR                core
              274  LOAD_METHOD              map
              276  LOAD_FAST                'self'
              278  LOAD_ATTR                filename
              280  CALL_METHOD_1         1  ''
              282  LOAD_FAST                'self'
              284  STORE_ATTR               map

 L. 198       286  LOAD_FAST                'self'
              288  LOAD_ATTR                map
              290  LOAD_METHOD              seek
              292  LOAD_FAST                'offset'
              294  CALL_METHOD_1         1  ''
              296  POP_TOP          

 L. 199       298  LOAD_FAST                'self'
              300  LOAD_ATTR                map
              302  LOAD_METHOD              readimage

 L. 200       304  LOAD_FAST                'self'
              306  LOAD_ATTR                mode

 L. 200       308  LOAD_FAST                'self'
              310  LOAD_ATTR                size

 L. 200       312  LOAD_FAST                'args'
              314  LOAD_CONST               1
              316  BINARY_SUBSCR    

 L. 200       318  LOAD_FAST                'args'
              320  LOAD_CONST               2
              322  BINARY_SUBSCR    

 L. 199       324  CALL_METHOD_4         4  ''
              326  LOAD_FAST                'self'
              328  STORE_ATTR               im
              330  JUMP_FORWARD        412  'to 412'
            332_0  COME_FROM           266  '266'

 L. 204       332  LOAD_CONST               0
              334  LOAD_CONST               None
              336  IMPORT_NAME              mmap
              338  STORE_FAST               'mmap'

 L. 206       340  LOAD_GLOBAL              open
              342  LOAD_FAST                'self'
              344  LOAD_ATTR                filename
              346  CALL_FUNCTION_1       1  ''
              348  SETUP_WITH          380  'to 380'
              350  STORE_FAST               'fp'

 L. 207       352  LOAD_FAST                'mmap'
              354  LOAD_ATTR                mmap

 L. 208       356  LOAD_FAST                'fp'
              358  LOAD_METHOD              fileno
              360  CALL_METHOD_0         0  ''

 L. 208       362  LOAD_CONST               0

 L. 208       364  LOAD_FAST                'mmap'
              366  LOAD_ATTR                ACCESS_READ

 L. 207       368  LOAD_CONST               ('access',)
              370  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              372  LOAD_FAST                'self'
              374  STORE_ATTR               map
              376  POP_BLOCK        
              378  BEGIN_FINALLY    
            380_0  COME_FROM_WITH      348  '348'
              380  WITH_CLEANUP_START
              382  WITH_CLEANUP_FINISH
              384  END_FINALLY      

 L. 210       386  LOAD_GLOBAL              Image
              388  LOAD_ATTR                core
              390  LOAD_METHOD              map_buffer

 L. 211       392  LOAD_FAST                'self'
              394  LOAD_ATTR                map

 L. 211       396  LOAD_FAST                'self'
              398  LOAD_ATTR                size

 L. 211       400  LOAD_FAST                'decoder_name'

 L. 211       402  LOAD_FAST                'offset'

 L. 211       404  LOAD_FAST                'args'

 L. 210       406  CALL_METHOD_5         5  ''
              408  LOAD_FAST                'self'
              410  STORE_ATTR               im
            412_0  COME_FROM           330  '330'

 L. 213       412  LOAD_CONST               1
              414  STORE_FAST               'readonly'

 L. 216       416  LOAD_FAST                'self'
              418  LOAD_ATTR                palette
          420_422  POP_JUMP_IF_FALSE   432  'to 432'

 L. 217       424  LOAD_CONST               1
              426  LOAD_FAST                'self'
              428  LOAD_ATTR                palette
              430  STORE_ATTR               dirty
            432_0  COME_FROM           420  '420'
              432  POP_BLOCK        
              434  JUMP_FORWARD        470  'to 470'
            436_0  COME_FROM_FINALLY   254  '254'

 L. 218       436  DUP_TOP          
              438  LOAD_GLOBAL              AttributeError
              440  LOAD_GLOBAL              OSError
              442  LOAD_GLOBAL              ImportError
              444  BUILD_TUPLE_3         3 
              446  COMPARE_OP               exception-match
          448_450  POP_JUMP_IF_FALSE   468  'to 468'
              452  POP_TOP          
              454  POP_TOP          
              456  POP_TOP          

 L. 219       458  LOAD_CONST               None
              460  LOAD_FAST                'self'
              462  STORE_ATTR               map
              464  POP_EXCEPT       
              466  JUMP_FORWARD        470  'to 470'
            468_0  COME_FROM           448  '448'
              468  END_FINALLY      
            470_0  COME_FROM           466  '466'
            470_1  COME_FROM           434  '434'
            470_2  COME_FROM           250  '250'
            470_3  COME_FROM           234  '234'
            470_4  COME_FROM           218  '218'
            470_5  COME_FROM           204  '204'
            470_6  COME_FROM           176  '176'

 L. 221       470  LOAD_FAST                'self'
              472  LOAD_METHOD              load_prepare
              474  CALL_METHOD_0         0  ''
              476  POP_TOP          

 L. 222       478  LOAD_CONST               -3
              480  STORE_FAST               'err_code'

 L. 223       482  LOAD_FAST                'self'
              484  LOAD_ATTR                map
          486_488  POP_JUMP_IF_TRUE    840  'to 840'

 L. 225       490  LOAD_FAST                'self'
              492  LOAD_ATTR                tile
              494  LOAD_ATTR                sort
              496  LOAD_GLOBAL              _tilesort
              498  LOAD_CONST               ('key',)
              500  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              502  POP_TOP          

 L. 227       504  SETUP_FINALLY       516  'to 516'

 L. 229       506  LOAD_FAST                'self'
              508  LOAD_ATTR                tile_prefix
              510  STORE_FAST               'prefix'
              512  POP_BLOCK        
              514  JUMP_FORWARD        542  'to 542'
            516_0  COME_FROM_FINALLY   504  '504'

 L. 230       516  DUP_TOP          
              518  LOAD_GLOBAL              AttributeError
              520  COMPARE_OP               exception-match
          522_524  POP_JUMP_IF_FALSE   540  'to 540'
              526  POP_TOP          
              528  POP_TOP          
              530  POP_TOP          

 L. 231       532  LOAD_CONST               b''
              534  STORE_FAST               'prefix'
              536  POP_EXCEPT       
              538  JUMP_FORWARD        542  'to 542'
            540_0  COME_FROM           522  '522'
              540  END_FINALLY      
            542_0  COME_FROM           538  '538'
            542_1  COME_FROM           514  '514'

 L. 233       542  LOAD_FAST                'self'
              544  LOAD_ATTR                tile
              546  GET_ITER         
          548_550  FOR_ITER            840  'to 840'
              552  UNPACK_SEQUENCE_4     4 
              554  STORE_FAST               'decoder_name'
              556  STORE_FAST               'extents'
              558  STORE_FAST               'offset'
              560  STORE_FAST               'args'

 L. 234       562  LOAD_GLOBAL              Image
              564  LOAD_METHOD              _getdecoder

 L. 235       566  LOAD_FAST                'self'
              568  LOAD_ATTR                mode

 L. 235       570  LOAD_FAST                'decoder_name'

 L. 235       572  LOAD_FAST                'args'

 L. 235       574  LOAD_FAST                'self'
              576  LOAD_ATTR                decoderconfig

 L. 234       578  CALL_METHOD_4         4  ''
              580  STORE_FAST               'decoder'

 L. 237       582  SETUP_FINALLY       826  'to 826'

 L. 238       584  LOAD_FAST                'seek'
              586  LOAD_FAST                'offset'
              588  CALL_FUNCTION_1       1  ''
              590  POP_TOP          

 L. 239       592  LOAD_FAST                'decoder'
              594  LOAD_METHOD              setimage
              596  LOAD_FAST                'self'
              598  LOAD_ATTR                im
              600  LOAD_FAST                'extents'
              602  CALL_METHOD_2         2  ''
              604  POP_TOP          

 L. 240       606  LOAD_FAST                'decoder'
              608  LOAD_ATTR                pulls_fd
          610_612  POP_JUMP_IF_FALSE   642  'to 642'

 L. 241       614  LOAD_FAST                'decoder'
              616  LOAD_METHOD              setfd
              618  LOAD_FAST                'self'
              620  LOAD_ATTR                fp
              622  CALL_METHOD_1         1  ''
              624  POP_TOP          

 L. 242       626  LOAD_FAST                'decoder'
              628  LOAD_METHOD              decode
              630  LOAD_CONST               b''
              632  CALL_METHOD_1         1  ''
              634  UNPACK_SEQUENCE_2     2 
              636  STORE_FAST               'status'
              638  STORE_FAST               'err_code'
              640  JUMP_FORWARD        822  'to 822'
            642_0  COME_FROM           610  '610'

 L. 244       642  LOAD_FAST                'prefix'
              644  STORE_FAST               'b'

 L. 246       646  SETUP_FINALLY       662  'to 662'

 L. 247       648  LOAD_FAST                'read'
              650  LOAD_FAST                'self'
              652  LOAD_ATTR                decodermaxblock
              654  CALL_FUNCTION_1       1  ''
              656  STORE_FAST               's'
              658  POP_BLOCK        
              660  JUMP_FORWARD        732  'to 732'
            662_0  COME_FROM_FINALLY   646  '646'

 L. 248       662  DUP_TOP          
              664  LOAD_GLOBAL              IndexError
              666  LOAD_GLOBAL              struct
              668  LOAD_ATTR                error
              670  BUILD_TUPLE_2         2 
              672  COMPARE_OP               exception-match
          674_676  POP_JUMP_IF_FALSE   730  'to 730'
              678  POP_TOP          
              680  STORE_FAST               'e'
              682  POP_TOP          
              684  SETUP_FINALLY       718  'to 718'

 L. 250       686  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          688_690  POP_JUMP_IF_FALSE   704  'to 704'

 L. 251       692  POP_BLOCK        
              694  POP_EXCEPT       
              696  CALL_FINALLY        718  'to 718'
          698_700  JUMP_ABSOLUTE       822  'to 822'
              702  JUMP_FORWARD        714  'to 714'
            704_0  COME_FROM           688  '688'

 L. 253       704  LOAD_GLOBAL              OSError
              706  LOAD_STR                 'image file is truncated'
              708  CALL_FUNCTION_1       1  ''
              710  LOAD_FAST                'e'
              712  RAISE_VARARGS_2       2  'exception instance with __cause__'
            714_0  COME_FROM           702  '702'
              714  POP_BLOCK        
              716  BEGIN_FINALLY    
            718_0  COME_FROM           696  '696'
            718_1  COME_FROM_FINALLY   684  '684'
              718  LOAD_CONST               None
              720  STORE_FAST               'e'
              722  DELETE_FAST              'e'
              724  END_FINALLY      
              726  POP_EXCEPT       
              728  JUMP_FORWARD        732  'to 732'
            730_0  COME_FROM           674  '674'
              730  END_FINALLY      
            732_0  COME_FROM           728  '728'
            732_1  COME_FROM           660  '660'

 L. 255       732  LOAD_FAST                's'
          734_736  POP_JUMP_IF_TRUE    770  'to 770'

 L. 256       738  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          740_742  POP_JUMP_IF_FALSE   750  'to 750'

 L. 257   744_746  BREAK_LOOP          822  'to 822'
              748  JUMP_FORWARD        770  'to 770'
            750_0  COME_FROM           740  '740'

 L. 259       750  LOAD_GLOBAL              OSError

 L. 260       752  LOAD_STR                 'image file is truncated ('
              754  LOAD_GLOBAL              len
              756  LOAD_FAST                'b'
              758  CALL_FUNCTION_1       1  ''
              760  FORMAT_VALUE          0  ''
              762  LOAD_STR                 ' bytes not processed)'
              764  BUILD_STRING_3        3 

 L. 259       766  CALL_FUNCTION_1       1  ''
              768  RAISE_VARARGS_1       1  'exception instance'
            770_0  COME_FROM           748  '748'
            770_1  COME_FROM           734  '734'

 L. 264       770  LOAD_FAST                'b'
              772  LOAD_FAST                's'
              774  BINARY_ADD       
              776  STORE_FAST               'b'

 L. 265       778  LOAD_FAST                'decoder'
              780  LOAD_METHOD              decode
              782  LOAD_FAST                'b'
              784  CALL_METHOD_1         1  ''
              786  UNPACK_SEQUENCE_2     2 
              788  STORE_FAST               'n'
              790  STORE_FAST               'err_code'

 L. 266       792  LOAD_FAST                'n'
              794  LOAD_CONST               0
              796  COMPARE_OP               <
          798_800  POP_JUMP_IF_FALSE   806  'to 806'

 L. 267   802_804  BREAK_LOOP          822  'to 822'
            806_0  COME_FROM           798  '798'

 L. 268       806  LOAD_FAST                'b'
              808  LOAD_FAST                'n'
              810  LOAD_CONST               None
              812  BUILD_SLICE_2         2 
              814  BINARY_SUBSCR    
              816  STORE_FAST               'b'
          818_820  JUMP_BACK           646  'to 646'
            822_0  COME_FROM           640  '640'
              822  POP_BLOCK        
              824  BEGIN_FINALLY    
            826_0  COME_FROM_FINALLY   582  '582'

 L. 271       826  LOAD_FAST                'decoder'
              828  LOAD_METHOD              cleanup
              830  CALL_METHOD_0         0  ''
              832  POP_TOP          
              834  END_FINALLY      
          836_838  JUMP_BACK           548  'to 548'
            840_0  COME_FROM           486  '486'

 L. 273       840  BUILD_LIST_0          0 
              842  LOAD_FAST                'self'
              844  STORE_ATTR               tile

 L. 274       846  LOAD_FAST                'readonly'
              848  LOAD_FAST                'self'
              850  STORE_ATTR               readonly

 L. 276       852  LOAD_FAST                'self'
              854  LOAD_METHOD              load_end
              856  CALL_METHOD_0         0  ''
              858  POP_TOP          

 L. 278       860  LOAD_FAST                'self'
              862  LOAD_ATTR                _exclusive_fp
          864_866  POP_JUMP_IF_FALSE   886  'to 886'
              868  LOAD_FAST                'self'
              870  LOAD_ATTR                _close_exclusive_fp_after_loading
          872_874  POP_JUMP_IF_FALSE   886  'to 886'

 L. 279       876  LOAD_FAST                'self'
              878  LOAD_ATTR                fp
              880  LOAD_METHOD              close
              882  CALL_METHOD_0         0  ''
              884  POP_TOP          
            886_0  COME_FROM           872  '872'
            886_1  COME_FROM           864  '864'

 L. 280       886  LOAD_CONST               None
              888  LOAD_FAST                'self'
              890  STORE_ATTR               fp

 L. 282       892  LOAD_FAST                'self'
              894  LOAD_ATTR                map
          896_898  POP_JUMP_IF_TRUE    924  'to 924'
              900  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          902_904  POP_JUMP_IF_TRUE    924  'to 924'
              906  LOAD_FAST                'err_code'
              908  LOAD_CONST               0
              910  COMPARE_OP               <
          912_914  POP_JUMP_IF_FALSE   924  'to 924'

 L. 284       916  LOAD_GLOBAL              raise_oserror
              918  LOAD_FAST                'err_code'
              920  CALL_FUNCTION_1       1  ''
              922  POP_TOP          
            924_0  COME_FROM           912  '912'
            924_1  COME_FROM           902  '902'
            924_2  COME_FROM           896  '896'

 L. 286       924  LOAD_GLOBAL              Image
              926  LOAD_ATTR                Image
              928  LOAD_METHOD              load
              930  LOAD_FAST                'self'
              932  CALL_METHOD_1         1  ''
              934  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 694

    def load_prepare(self):
        if not self.im or self.im.mode != self.mode or self.im.size != self.size:
            self.im = Image.core.new(self.mode, self.size)
        if self.mode == 'P':
            Image.Image.load(self)

    def load_end(self):
        pass

    def _seek_check(self, frame):
        if not ((frame < self._min_frame or hasattr)(self, '_n_frames') and self._n_frames is None):
            if frame >= self.n_frames + self._min_frame:
                raise EOFError('attempt to seek outside sequence')
        return self.tell() != frame


class StubImageFile(ImageFile):
    __doc__ = '\n    Base class for stub image loaders.\n\n    A stub loader is an image loader that can identify files of a\n    certain format, but relies on external code to load the file.\n    '

    def _open(self):
        raise NotImplementedError('StubImageFile subclass must implement _open')

    def load(self):
        loader = self._load()
        if loader is None:
            raise OSError(f"cannot find loader for this {self.format} file")
        image = loader.load(self)
        assert image is not None
        self.__class__ = image.__class__
        self.__dict__ = image.__dict__

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

    def reset(self):
        """
        (Consumer) Reset the parser.  Note that you can only call this
        method immediately after you've created a parser; parser
        instances cannot be reused.
        """
        assert self.data is None, 'cannot reuse parsers'

    def feed(self, data):
        """
        (Consumer) Feed data to the parser.

        :param data: A string buffer.
        :exception OSError: If the parser failed to parse the image file.
        """
        if self.finished:
            return
            if self.data is None:
                self.data = data
            else:
                self.data = self.data + data
            if self.decoder:
                if self.offset > 0:
                    skip = min(len(self.data), self.offset)
                    self.data = self.data[skip:]
                    self.offset = self.offset - skip
                    return self.offset > 0 or self.data or None
                n, e = self.decoder.decode(self.data)
                if n < 0:
                    self.data = None
                    self.finished = 1
                    if e < 0:
                        self.image = None
                        raise_oserror(e)
                    else:
                        return
                self.data = self.data[n:]
            else:
                if self.image:
                    pass
                else:
                    try:
                        with io.BytesIO(self.data) as (fp):
                            im = Image.open(fp)
                    except OSError:
                        pass
                    else:
                        flag = hasattr(im, 'load_seek') or hasattr(im, 'load_read')
                        if flag or len(im.tile) != 1:
                            self.decode = None
        else:
            im.load_prepare()
            d, e, o, a = im.tile[0]
            im.tile = []
            self.decoder = Image._getdecoderim.modedaim.decoderconfig
            self.decoder.setimage(im.im, e)
            self.offset = o
            if self.offset <= len(self.data):
                self.data = self.data[self.offset:]
                self.offset = 0
            self.image = im

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """
        (Consumer) Close the stream.

        :returns: An image object.
        :exception OSError: If the parser failed to parse the image file either
                            because it cannot be identified or cannot be
                            decoded.
        """
        if self.decoder:
            self.feed(b'')
            self.data = self.decoder = None
            if not self.finished:
                raise OSError('image was incomplete')
        if not self.image:
            raise OSError('cannot parse this image')
        if self.data:
            with io.BytesIO(self.data) as (fp):
                try:
                    self.image = Image.open(fp)
                finally:
                    self.image.load()

        return self.image


def _save(im, fp, tile, bufsize=0):
    """Helper to save image based on tile list

    :param im: Image object.
    :param fp: File object.
    :param tile: Tile list.
    :param bufsize: Optional buffer size
    """
    im.load()
    if not hasattr(im, 'encoderconfig'):
        im.encoderconfig = ()
    tile.sort(key=_tilesort)
    bufsize = max(MAXBLOCK, bufsize, im.size[0] * 4)
    if fp == sys.stdout:
        fp.flush()
        return None
    try:
        fh = fp.fileno()
        fp.flush()
    except (AttributeError, io.UnsupportedOperation) as exc:
        try:
            for e, b, o, a in tile:
                e = Image._getencoderim.modeeaim.encoderconfig
                if o > 0:
                    fp.seek(o)
                e.setimage(im.im, b)
                if e.pushes_fd:
                    e.setfd(fp)
                    l, s = e.encode_to_pyfd()
                else:
                    l, s, d = e.encode(bufsize)
                fp.write(d)
                if s:
                    break
                else:
                    if s < 0:
                        raise OSError(f"encoder error {s} when writing image file") from exc
                    e.cleanup()

        finally:
            exc = None
            del exc

    else:
        for e, b, o, a in tile:
            e = Image._getencoderim.modeeaim.encoderconfig
            if o > 0:
                fp.seek(o)
            else:
                e.setimage(im.im, b)
                if e.pushes_fd:
                    e.setfd(fp)
                    l, s = e.encode_to_pyfd()
                else:
                    s = e.encode_to_file(fh, bufsize)
            if s < 0:
                raise OSError(f"encoder error {s} when writing image file")
            e.cleanup()
        else:
            if hasattr(fp, 'flush'):
                fp.flush()


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
    else:
        if size <= SAFEBLOCK:
            return fp.read(size)
        data = []
        while True:
            if size > 0:
                block = fp.read(min(size, SAFEBLOCK))
                if not block:
                    break
                data.append(block)
                size -= len(block)

    return (b'').join(data)


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
        self.state = PyCodecState()
        self.fd = None
        self.mode = mode
        self.init(args)

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
        raise NotImplementedError()

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
        d.setimage(self.im, self.state.extents())
        s = d.decode(data)
        if s[0] >= 0:
            raise ValueError('not enough image data')
        if s[1] != 0:
            raise ValueError('cannot decode image data')