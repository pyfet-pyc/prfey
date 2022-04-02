# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\ImageFile.py
import io, struct, sys
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

def raise_ioerror(error):
    try:
        message = Image.core.getcodecstatus(error)
    except AttributeError:
        message = ERRORS.get(error)
    else:
        if not message:
            message = 'decoder error %d' % error
        raise OSError(message + ' when reading image file')


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
                    raise SyntaxError(v)
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

 L. 143         0  LOAD_GLOBAL              Image
                2  LOAD_ATTR                Image
                4  LOAD_METHOD              load
                6  LOAD_FAST                'self'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'pixel'

 L. 145        12  LOAD_FAST                'self'
               14  LOAD_ATTR                tile
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 146        22  LOAD_GLOBAL              OSError
               24  LOAD_STR                 'cannot load this image'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L. 147        30  LOAD_FAST                'self'
               32  LOAD_ATTR                tile
               34  POP_JUMP_IF_TRUE     40  'to 40'

 L. 148        36  LOAD_FAST                'pixel'
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L. 150        40  LOAD_CONST               None
               42  LOAD_FAST                'self'
               44  STORE_ATTR               map

 L. 151        46  LOAD_FAST                'self'
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

 L. 153        66  LOAD_FAST                'use_mmap'
               68  JUMP_IF_FALSE_OR_POP    80  'to 80'
               70  LOAD_GLOBAL              hasattr
               72  LOAD_GLOBAL              sys
               74  LOAD_STR                 'pypy_version_info'
               76  CALL_FUNCTION_2       2  ''
               78  UNARY_NOT        
             80_0  COME_FROM            68  '68'
               80  STORE_FAST               'use_mmap'

 L. 155        82  LOAD_CONST               0
               84  STORE_FAST               'readonly'

 L. 158        86  SETUP_FINALLY       102  'to 102'

 L. 159        88  LOAD_FAST                'self'
               90  LOAD_ATTR                load_read
               92  STORE_FAST               'read'

 L. 161        94  LOAD_CONST               False
               96  STORE_FAST               'use_mmap'
               98  POP_BLOCK        
              100  JUMP_FORWARD        130  'to 130'
            102_0  COME_FROM_FINALLY    86  '86'

 L. 162       102  DUP_TOP          
              104  LOAD_GLOBAL              AttributeError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   128  'to 128'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 163       116  LOAD_FAST                'self'
              118  LOAD_ATTR                fp
              120  LOAD_ATTR                read
              122  STORE_FAST               'read'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM           108  '108'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           100  '100'

 L. 165       130  SETUP_FINALLY       146  'to 146'

 L. 166       132  LOAD_FAST                'self'
              134  LOAD_ATTR                load_seek
              136  STORE_FAST               'seek'

 L. 167       138  LOAD_CONST               False
              140  STORE_FAST               'use_mmap'
              142  POP_BLOCK        
              144  JUMP_FORWARD        174  'to 174'
            146_0  COME_FROM_FINALLY   130  '130'

 L. 168       146  DUP_TOP          
              148  LOAD_GLOBAL              AttributeError
              150  COMPARE_OP               exception-match
              152  POP_JUMP_IF_FALSE   172  'to 172'
              154  POP_TOP          
              156  POP_TOP          
              158  POP_TOP          

 L. 169       160  LOAD_FAST                'self'
              162  LOAD_ATTR                fp
              164  LOAD_ATTR                seek
              166  STORE_FAST               'seek'
              168  POP_EXCEPT       
              170  JUMP_FORWARD        174  'to 174'
            172_0  COME_FROM           152  '152'
              172  END_FINALLY      
            174_0  COME_FROM           170  '170'
            174_1  COME_FROM           144  '144'

 L. 171       174  LOAD_FAST                'use_mmap'
          176_178  POP_JUMP_IF_FALSE   474  'to 474'

 L. 173       180  LOAD_FAST                'self'
              182  LOAD_ATTR                tile
              184  LOAD_CONST               0
              186  BINARY_SUBSCR    
              188  UNPACK_SEQUENCE_4     4 
              190  STORE_FAST               'decoder_name'
              192  STORE_FAST               'extents'
              194  STORE_FAST               'offset'
              196  STORE_FAST               'args'

 L. 175       198  LOAD_FAST                'decoder_name'
              200  LOAD_STR                 'raw'
              202  COMPARE_OP               ==

 L. 174   204_206  POP_JUMP_IF_FALSE   474  'to 474'

 L. 176       208  LOAD_GLOBAL              len
              210  LOAD_FAST                'args'
              212  CALL_FUNCTION_1       1  ''
              214  LOAD_CONST               3
              216  COMPARE_OP               >=

 L. 174   218_220  POP_JUMP_IF_FALSE   474  'to 474'

 L. 177       222  LOAD_FAST                'args'
              224  LOAD_CONST               0
              226  BINARY_SUBSCR    
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                mode
              232  COMPARE_OP               ==

 L. 174   234_236  POP_JUMP_IF_FALSE   474  'to 474'

 L. 178       238  LOAD_FAST                'args'
              240  LOAD_CONST               0
              242  BINARY_SUBSCR    
              244  LOAD_GLOBAL              Image
              246  LOAD_ATTR                _MAPMODES
              248  COMPARE_OP               in

 L. 174   250_252  POP_JUMP_IF_FALSE   474  'to 474'

 L. 180       254  SETUP_FINALLY       440  'to 440'

 L. 181       256  LOAD_GLOBAL              hasattr
              258  LOAD_GLOBAL              Image
              260  LOAD_ATTR                core
              262  LOAD_STR                 'map'
              264  CALL_FUNCTION_2       2  ''
          266_268  POP_JUMP_IF_FALSE   332  'to 332'

 L. 183       270  LOAD_GLOBAL              Image
              272  LOAD_ATTR                core
              274  LOAD_METHOD              map
              276  LOAD_FAST                'self'
              278  LOAD_ATTR                filename
              280  CALL_METHOD_1         1  ''
              282  LOAD_FAST                'self'
              284  STORE_ATTR               map

 L. 184       286  LOAD_FAST                'self'
              288  LOAD_ATTR                map
              290  LOAD_METHOD              seek
              292  LOAD_FAST                'offset'
              294  CALL_METHOD_1         1  ''
              296  POP_TOP          

 L. 185       298  LOAD_FAST                'self'
              300  LOAD_ATTR                map
              302  LOAD_METHOD              readimage

 L. 186       304  LOAD_FAST                'self'
              306  LOAD_ATTR                mode

 L. 186       308  LOAD_FAST                'self'
              310  LOAD_ATTR                size

 L. 186       312  LOAD_FAST                'args'
              314  LOAD_CONST               1
              316  BINARY_SUBSCR    

 L. 186       318  LOAD_FAST                'args'
              320  LOAD_CONST               2
              322  BINARY_SUBSCR    

 L. 185       324  CALL_METHOD_4         4  ''
              326  LOAD_FAST                'self'
              328  STORE_ATTR               im
              330  JUMP_FORWARD        416  'to 416'
            332_0  COME_FROM           266  '266'

 L. 190       332  LOAD_CONST               0
              334  LOAD_CONST               None
              336  IMPORT_NAME              mmap
              338  STORE_FAST               'mmap'

 L. 192       340  LOAD_GLOBAL              open
              342  LOAD_FAST                'self'
              344  LOAD_ATTR                filename
              346  LOAD_STR                 'r'
              348  CALL_FUNCTION_2       2  ''
              350  SETUP_WITH          382  'to 382'
              352  STORE_FAST               'fp'

 L. 193       354  LOAD_FAST                'mmap'
              356  LOAD_ATTR                mmap

 L. 194       358  LOAD_FAST                'fp'
              360  LOAD_METHOD              fileno
              362  CALL_METHOD_0         0  ''

 L. 194       364  LOAD_CONST               0

 L. 194       366  LOAD_FAST                'mmap'
              368  LOAD_ATTR                ACCESS_READ

 L. 193       370  LOAD_CONST               ('access',)
              372  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              374  LOAD_FAST                'self'
              376  STORE_ATTR               map
              378  POP_BLOCK        
              380  BEGIN_FINALLY    
            382_0  COME_FROM_WITH      350  '350'
              382  WITH_CLEANUP_START
              384  WITH_CLEANUP_FINISH
              386  END_FINALLY      

 L. 196       388  LOAD_GLOBAL              Image
              390  LOAD_ATTR                core
              392  LOAD_METHOD              map_buffer

 L. 197       394  LOAD_FAST                'self'
              396  LOAD_ATTR                map

 L. 197       398  LOAD_FAST                'self'
              400  LOAD_ATTR                size

 L. 197       402  LOAD_FAST                'decoder_name'

 L. 197       404  LOAD_FAST                'extents'

 L. 197       406  LOAD_FAST                'offset'

 L. 197       408  LOAD_FAST                'args'

 L. 196       410  CALL_METHOD_6         6  ''
              412  LOAD_FAST                'self'
              414  STORE_ATTR               im
            416_0  COME_FROM           330  '330'

 L. 199       416  LOAD_CONST               1
              418  STORE_FAST               'readonly'

 L. 202       420  LOAD_FAST                'self'
              422  LOAD_ATTR                palette
          424_426  POP_JUMP_IF_FALSE   436  'to 436'

 L. 203       428  LOAD_CONST               1
              430  LOAD_FAST                'self'
              432  LOAD_ATTR                palette
              434  STORE_ATTR               dirty
            436_0  COME_FROM           424  '424'
              436  POP_BLOCK        
              438  JUMP_FORWARD        474  'to 474'
            440_0  COME_FROM_FINALLY   254  '254'

 L. 204       440  DUP_TOP          
              442  LOAD_GLOBAL              AttributeError
              444  LOAD_GLOBAL              OSError
              446  LOAD_GLOBAL              ImportError
              448  BUILD_TUPLE_3         3 
              450  COMPARE_OP               exception-match
          452_454  POP_JUMP_IF_FALSE   472  'to 472'
              456  POP_TOP          
              458  POP_TOP          
              460  POP_TOP          

 L. 205       462  LOAD_CONST               None
              464  LOAD_FAST                'self'
              466  STORE_ATTR               map
              468  POP_EXCEPT       
              470  JUMP_FORWARD        474  'to 474'
            472_0  COME_FROM           452  '452'
              472  END_FINALLY      
            474_0  COME_FROM           470  '470'
            474_1  COME_FROM           438  '438'
            474_2  COME_FROM           250  '250'
            474_3  COME_FROM           234  '234'
            474_4  COME_FROM           218  '218'
            474_5  COME_FROM           204  '204'
            474_6  COME_FROM           176  '176'

 L. 207       474  LOAD_FAST                'self'
              476  LOAD_METHOD              load_prepare
              478  CALL_METHOD_0         0  ''
              480  POP_TOP          

 L. 208       482  LOAD_CONST               -3
              484  STORE_FAST               'err_code'

 L. 209       486  LOAD_FAST                'self'
              488  LOAD_ATTR                map
          490_492  POP_JUMP_IF_TRUE    820  'to 820'

 L. 211       494  LOAD_FAST                'self'
              496  LOAD_ATTR                tile
              498  LOAD_ATTR                sort
              500  LOAD_GLOBAL              _tilesort
              502  LOAD_CONST               ('key',)
              504  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              506  POP_TOP          

 L. 213       508  SETUP_FINALLY       520  'to 520'

 L. 215       510  LOAD_FAST                'self'
              512  LOAD_ATTR                tile_prefix
              514  STORE_FAST               'prefix'
              516  POP_BLOCK        
              518  JUMP_FORWARD        546  'to 546'
            520_0  COME_FROM_FINALLY   508  '508'

 L. 216       520  DUP_TOP          
              522  LOAD_GLOBAL              AttributeError
              524  COMPARE_OP               exception-match
          526_528  POP_JUMP_IF_FALSE   544  'to 544'
              530  POP_TOP          
              532  POP_TOP          
              534  POP_TOP          

 L. 217       536  LOAD_CONST               b''
              538  STORE_FAST               'prefix'
              540  POP_EXCEPT       
              542  JUMP_FORWARD        546  'to 546'
            544_0  COME_FROM           526  '526'
              544  END_FINALLY      
            546_0  COME_FROM           542  '542'
            546_1  COME_FROM           518  '518'

 L. 219       546  LOAD_FAST                'self'
              548  LOAD_ATTR                tile
              550  GET_ITER         
          552_554  FOR_ITER            820  'to 820'
              556  UNPACK_SEQUENCE_4     4 
              558  STORE_FAST               'decoder_name'
              560  STORE_FAST               'extents'
              562  STORE_FAST               'offset'
              564  STORE_FAST               'args'

 L. 220       566  LOAD_GLOBAL              Image
              568  LOAD_METHOD              _getdecoder

 L. 221       570  LOAD_FAST                'self'
              572  LOAD_ATTR                mode

 L. 221       574  LOAD_FAST                'decoder_name'

 L. 221       576  LOAD_FAST                'args'

 L. 221       578  LOAD_FAST                'self'
              580  LOAD_ATTR                decoderconfig

 L. 220       582  CALL_METHOD_4         4  ''
              584  STORE_FAST               'decoder'

 L. 223       586  SETUP_FINALLY       806  'to 806'

 L. 224       588  LOAD_FAST                'seek'
              590  LOAD_FAST                'offset'
              592  CALL_FUNCTION_1       1  ''
              594  POP_TOP          

 L. 225       596  LOAD_FAST                'decoder'
              598  LOAD_METHOD              setimage
              600  LOAD_FAST                'self'
              602  LOAD_ATTR                im
              604  LOAD_FAST                'extents'
              606  CALL_METHOD_2         2  ''
              608  POP_TOP          

 L. 226       610  LOAD_FAST                'decoder'
              612  LOAD_ATTR                pulls_fd
          614_616  POP_JUMP_IF_FALSE   646  'to 646'

 L. 227       618  LOAD_FAST                'decoder'
              620  LOAD_METHOD              setfd
              622  LOAD_FAST                'self'
              624  LOAD_ATTR                fp
              626  CALL_METHOD_1         1  ''
              628  POP_TOP          

 L. 228       630  LOAD_FAST                'decoder'
              632  LOAD_METHOD              decode
              634  LOAD_CONST               b''
              636  CALL_METHOD_1         1  ''
              638  UNPACK_SEQUENCE_2     2 
              640  STORE_FAST               'status'
              642  STORE_FAST               'err_code'
              644  JUMP_FORWARD        802  'to 802'
            646_0  COME_FROM           614  '614'

 L. 230       646  LOAD_FAST                'prefix'
              648  STORE_FAST               'b'

 L. 232       650  SETUP_FINALLY       666  'to 666'

 L. 233       652  LOAD_FAST                'read'
              654  LOAD_FAST                'self'
              656  LOAD_ATTR                decodermaxblock
              658  CALL_FUNCTION_1       1  ''
              660  STORE_FAST               's'
              662  POP_BLOCK        
              664  JUMP_FORWARD        716  'to 716'
            666_0  COME_FROM_FINALLY   650  '650'

 L. 234       666  DUP_TOP          
              668  LOAD_GLOBAL              IndexError
              670  LOAD_GLOBAL              struct
              672  LOAD_ATTR                error
              674  BUILD_TUPLE_2         2 
              676  COMPARE_OP               exception-match
          678_680  POP_JUMP_IF_FALSE   714  'to 714'
              682  POP_TOP          
              684  POP_TOP          
              686  POP_TOP          

 L. 236       688  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          690_692  POP_JUMP_IF_FALSE   702  'to 702'

 L. 237       694  POP_EXCEPT       
          696_698  JUMP_ABSOLUTE       802  'to 802'
              700  JUMP_FORWARD        710  'to 710'
            702_0  COME_FROM           690  '690'

 L. 239       702  LOAD_GLOBAL              OSError
              704  LOAD_STR                 'image file is truncated'
              706  CALL_FUNCTION_1       1  ''
              708  RAISE_VARARGS_1       1  'exception instance'
            710_0  COME_FROM           700  '700'
              710  POP_EXCEPT       
              712  JUMP_FORWARD        716  'to 716'
            714_0  COME_FROM           678  '678'
              714  END_FINALLY      
            716_0  COME_FROM           712  '712'
            716_1  COME_FROM           664  '664'

 L. 241       716  LOAD_FAST                's'
          718_720  POP_JUMP_IF_TRUE    750  'to 750'

 L. 242       722  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          724_726  POP_JUMP_IF_FALSE   734  'to 734'

 L. 243   728_730  BREAK_LOOP          802  'to 802'
              732  JUMP_FORWARD        750  'to 750'
            734_0  COME_FROM           724  '724'

 L. 245       734  LOAD_GLOBAL              OSError

 L. 246       736  LOAD_STR                 'image file is truncated (%d bytes not processed)'

 L. 247       738  LOAD_GLOBAL              len
              740  LOAD_FAST                'b'
              742  CALL_FUNCTION_1       1  ''

 L. 246       744  BINARY_MODULO    

 L. 245       746  CALL_FUNCTION_1       1  ''
              748  RAISE_VARARGS_1       1  'exception instance'
            750_0  COME_FROM           732  '732'
            750_1  COME_FROM           718  '718'

 L. 250       750  LOAD_FAST                'b'
              752  LOAD_FAST                's'
              754  BINARY_ADD       
              756  STORE_FAST               'b'

 L. 251       758  LOAD_FAST                'decoder'
              760  LOAD_METHOD              decode
              762  LOAD_FAST                'b'
              764  CALL_METHOD_1         1  ''
              766  UNPACK_SEQUENCE_2     2 
              768  STORE_FAST               'n'
              770  STORE_FAST               'err_code'

 L. 252       772  LOAD_FAST                'n'
              774  LOAD_CONST               0
              776  COMPARE_OP               <
          778_780  POP_JUMP_IF_FALSE   786  'to 786'

 L. 253   782_784  BREAK_LOOP          802  'to 802'
            786_0  COME_FROM           778  '778'

 L. 254       786  LOAD_FAST                'b'
              788  LOAD_FAST                'n'
              790  LOAD_CONST               None
              792  BUILD_SLICE_2         2 
              794  BINARY_SUBSCR    
              796  STORE_FAST               'b'
          798_800  JUMP_BACK           650  'to 650'
            802_0  COME_FROM           644  '644'
              802  POP_BLOCK        
              804  BEGIN_FINALLY    
            806_0  COME_FROM_FINALLY   586  '586'

 L. 257       806  LOAD_FAST                'decoder'
              808  LOAD_METHOD              cleanup
              810  CALL_METHOD_0         0  ''
              812  POP_TOP          
              814  END_FINALLY      
          816_818  JUMP_BACK           552  'to 552'
            820_0  COME_FROM           490  '490'

 L. 259       820  BUILD_LIST_0          0 
              822  LOAD_FAST                'self'
              824  STORE_ATTR               tile

 L. 260       826  LOAD_FAST                'readonly'
              828  LOAD_FAST                'self'
              830  STORE_ATTR               readonly

 L. 262       832  LOAD_FAST                'self'
              834  LOAD_METHOD              load_end
              836  CALL_METHOD_0         0  ''
              838  POP_TOP          

 L. 264       840  LOAD_FAST                'self'
              842  LOAD_ATTR                _exclusive_fp
          844_846  POP_JUMP_IF_FALSE   866  'to 866'
              848  LOAD_FAST                'self'
              850  LOAD_ATTR                _close_exclusive_fp_after_loading
          852_854  POP_JUMP_IF_FALSE   866  'to 866'

 L. 265       856  LOAD_FAST                'self'
              858  LOAD_ATTR                fp
              860  LOAD_METHOD              close
              862  CALL_METHOD_0         0  ''
              864  POP_TOP          
            866_0  COME_FROM           852  '852'
            866_1  COME_FROM           844  '844'

 L. 266       866  LOAD_CONST               None
              868  LOAD_FAST                'self'
              870  STORE_ATTR               fp

 L. 268       872  LOAD_FAST                'self'
              874  LOAD_ATTR                map
          876_878  POP_JUMP_IF_TRUE    904  'to 904'
              880  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          882_884  POP_JUMP_IF_TRUE    904  'to 904'
              886  LOAD_FAST                'err_code'
              888  LOAD_CONST               0
              890  COMPARE_OP               <
          892_894  POP_JUMP_IF_FALSE   904  'to 904'

 L. 270       896  LOAD_GLOBAL              raise_ioerror
              898  LOAD_FAST                'err_code'
              900  CALL_FUNCTION_1       1  ''
              902  POP_TOP          
            904_0  COME_FROM           892  '892'
            904_1  COME_FROM           882  '882'
            904_2  COME_FROM           876  '876'

 L. 272       904  LOAD_GLOBAL              Image
              906  LOAD_ATTR                Image
              908  LOAD_METHOD              load
              910  LOAD_FAST                'self'
              912  CALL_METHOD_1         1  ''
              914  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 696_698

    def load_prepare(self):
        if not self.im or self.im.mode != self.mode or self.im.size != self.size:
            self.im = Image.core.newself.modeself.size
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
            raise OSError('cannot find loader for this %s file' % self.format)
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
        :exception IOError: If the parser failed to parse the image file.
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
                        raise_ioerror(e)
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
            self.decoder.setimageim.ime
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
        :exception IOError: If the parser failed to parse the image file either
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
    except (AttributeError, io.UnsupportedOperation):
        for e, b, o, a in tile:
            e = Image._getencoderim.modeeaim.encoderconfig
            if o > 0:
                fp.seek(o)
            e.setimageim.imb
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
                    raise OSError('encoder error %d when writing image file' % s)
                e.cleanup()

    else:
        for e, b, o, a in tile:
            e = Image._getencoderim.modeeaim.encoderconfig
            if o > 0:
                fp.seek(o)
            else:
                e.setimageim.imb
                if e.pushes_fd:
                    e.setfd(fp)
                    l, s = e.encode_to_pyfd()
                else:
                    s = e.encode_to_filefhbufsize
            if s < 0:
                raise OSError('encoder error %d when writing image file' % s)
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
    __doc__ = '\n    Python implementation of a format decoder. Override this class and\n    add the decoding logic in the `decode` method.\n\n    See :ref:`Writing Your Own File Decoder in Python<file-decoders-py>`\n    '
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
        :returns: A tuple of (bytes consumed, errcode).
            If finished with decoding return <0 for the bytes consumed.
            Err codes are from `ERRORS`
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
        d.setimageself.imself.state.extents()
        s = d.decode(data)
        if s[0] >= 0:
            raise ValueError('not enough image data')
        if s[1] != 0:
            raise ValueError('cannot decode image data')