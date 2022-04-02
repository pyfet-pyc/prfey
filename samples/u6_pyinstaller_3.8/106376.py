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
          176_178  POP_JUMP_IF_FALSE   472  'to 472'

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

 L. 174   204_206  POP_JUMP_IF_FALSE   472  'to 472'

 L. 176       208  LOAD_GLOBAL              len
              210  LOAD_FAST                'args'
              212  CALL_FUNCTION_1       1  ''
              214  LOAD_CONST               3
              216  COMPARE_OP               >=

 L. 174   218_220  POP_JUMP_IF_FALSE   472  'to 472'

 L. 177       222  LOAD_FAST                'args'
              224  LOAD_CONST               0
              226  BINARY_SUBSCR    
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                mode
              232  COMPARE_OP               ==

 L. 174   234_236  POP_JUMP_IF_FALSE   472  'to 472'

 L. 178       238  LOAD_FAST                'args'
              240  LOAD_CONST               0
              242  BINARY_SUBSCR    
              244  LOAD_GLOBAL              Image
              246  LOAD_ATTR                _MAPMODES
              248  COMPARE_OP               in

 L. 174   250_252  POP_JUMP_IF_FALSE   472  'to 472'

 L. 180       254  SETUP_FINALLY       438  'to 438'

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
              330  JUMP_FORWARD        414  'to 414'
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

 L. 197       404  LOAD_FAST                'offset'

 L. 197       406  LOAD_FAST                'args'

 L. 196       408  CALL_METHOD_5         5  ''
              410  LOAD_FAST                'self'
              412  STORE_ATTR               im
            414_0  COME_FROM           330  '330'

 L. 199       414  LOAD_CONST               1
              416  STORE_FAST               'readonly'

 L. 202       418  LOAD_FAST                'self'
              420  LOAD_ATTR                palette
          422_424  POP_JUMP_IF_FALSE   434  'to 434'

 L. 203       426  LOAD_CONST               1
              428  LOAD_FAST                'self'
              430  LOAD_ATTR                palette
              432  STORE_ATTR               dirty
            434_0  COME_FROM           422  '422'
              434  POP_BLOCK        
              436  JUMP_FORWARD        472  'to 472'
            438_0  COME_FROM_FINALLY   254  '254'

 L. 204       438  DUP_TOP          
              440  LOAD_GLOBAL              AttributeError
              442  LOAD_GLOBAL              OSError
              444  LOAD_GLOBAL              ImportError
              446  BUILD_TUPLE_3         3 
              448  COMPARE_OP               exception-match
          450_452  POP_JUMP_IF_FALSE   470  'to 470'
              454  POP_TOP          
              456  POP_TOP          
              458  POP_TOP          

 L. 205       460  LOAD_CONST               None
              462  LOAD_FAST                'self'
              464  STORE_ATTR               map
              466  POP_EXCEPT       
              468  JUMP_FORWARD        472  'to 472'
            470_0  COME_FROM           450  '450'
              470  END_FINALLY      
            472_0  COME_FROM           468  '468'
            472_1  COME_FROM           436  '436'
            472_2  COME_FROM           250  '250'
            472_3  COME_FROM           234  '234'
            472_4  COME_FROM           218  '218'
            472_5  COME_FROM           204  '204'
            472_6  COME_FROM           176  '176'

 L. 207       472  LOAD_FAST                'self'
              474  LOAD_METHOD              load_prepare
              476  CALL_METHOD_0         0  ''
              478  POP_TOP          

 L. 208       480  LOAD_CONST               -3
              482  STORE_FAST               'err_code'

 L. 209       484  LOAD_FAST                'self'
              486  LOAD_ATTR                map
          488_490  POP_JUMP_IF_TRUE    818  'to 818'

 L. 211       492  LOAD_FAST                'self'
              494  LOAD_ATTR                tile
              496  LOAD_ATTR                sort
              498  LOAD_GLOBAL              _tilesort
              500  LOAD_CONST               ('key',)
              502  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              504  POP_TOP          

 L. 213       506  SETUP_FINALLY       518  'to 518'

 L. 215       508  LOAD_FAST                'self'
              510  LOAD_ATTR                tile_prefix
              512  STORE_FAST               'prefix'
              514  POP_BLOCK        
              516  JUMP_FORWARD        544  'to 544'
            518_0  COME_FROM_FINALLY   506  '506'

 L. 216       518  DUP_TOP          
              520  LOAD_GLOBAL              AttributeError
              522  COMPARE_OP               exception-match
          524_526  POP_JUMP_IF_FALSE   542  'to 542'
              528  POP_TOP          
              530  POP_TOP          
              532  POP_TOP          

 L. 217       534  LOAD_CONST               b''
              536  STORE_FAST               'prefix'
              538  POP_EXCEPT       
              540  JUMP_FORWARD        544  'to 544'
            542_0  COME_FROM           524  '524'
              542  END_FINALLY      
            544_0  COME_FROM           540  '540'
            544_1  COME_FROM           516  '516'

 L. 219       544  LOAD_FAST                'self'
              546  LOAD_ATTR                tile
              548  GET_ITER         
          550_552  FOR_ITER            818  'to 818'
              554  UNPACK_SEQUENCE_4     4 
              556  STORE_FAST               'decoder_name'
              558  STORE_FAST               'extents'
              560  STORE_FAST               'offset'
              562  STORE_FAST               'args'

 L. 220       564  LOAD_GLOBAL              Image
              566  LOAD_METHOD              _getdecoder

 L. 221       568  LOAD_FAST                'self'
              570  LOAD_ATTR                mode

 L. 221       572  LOAD_FAST                'decoder_name'

 L. 221       574  LOAD_FAST                'args'

 L. 221       576  LOAD_FAST                'self'
              578  LOAD_ATTR                decoderconfig

 L. 220       580  CALL_METHOD_4         4  ''
              582  STORE_FAST               'decoder'

 L. 223       584  SETUP_FINALLY       804  'to 804'

 L. 224       586  LOAD_FAST                'seek'
              588  LOAD_FAST                'offset'
              590  CALL_FUNCTION_1       1  ''
              592  POP_TOP          

 L. 225       594  LOAD_FAST                'decoder'
              596  LOAD_METHOD              setimage
              598  LOAD_FAST                'self'
              600  LOAD_ATTR                im
              602  LOAD_FAST                'extents'
              604  CALL_METHOD_2         2  ''
              606  POP_TOP          

 L. 226       608  LOAD_FAST                'decoder'
              610  LOAD_ATTR                pulls_fd
          612_614  POP_JUMP_IF_FALSE   644  'to 644'

 L. 227       616  LOAD_FAST                'decoder'
              618  LOAD_METHOD              setfd
              620  LOAD_FAST                'self'
              622  LOAD_ATTR                fp
              624  CALL_METHOD_1         1  ''
              626  POP_TOP          

 L. 228       628  LOAD_FAST                'decoder'
              630  LOAD_METHOD              decode
              632  LOAD_CONST               b''
              634  CALL_METHOD_1         1  ''
              636  UNPACK_SEQUENCE_2     2 
              638  STORE_FAST               'status'
              640  STORE_FAST               'err_code'
              642  JUMP_FORWARD        800  'to 800'
            644_0  COME_FROM           612  '612'

 L. 230       644  LOAD_FAST                'prefix'
              646  STORE_FAST               'b'

 L. 232       648  SETUP_FINALLY       664  'to 664'

 L. 233       650  LOAD_FAST                'read'
              652  LOAD_FAST                'self'
              654  LOAD_ATTR                decodermaxblock
              656  CALL_FUNCTION_1       1  ''
              658  STORE_FAST               's'
              660  POP_BLOCK        
              662  JUMP_FORWARD        714  'to 714'
            664_0  COME_FROM_FINALLY   648  '648'

 L. 234       664  DUP_TOP          
              666  LOAD_GLOBAL              IndexError
              668  LOAD_GLOBAL              struct
              670  LOAD_ATTR                error
              672  BUILD_TUPLE_2         2 
              674  COMPARE_OP               exception-match
          676_678  POP_JUMP_IF_FALSE   712  'to 712'
              680  POP_TOP          
              682  POP_TOP          
              684  POP_TOP          

 L. 236       686  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          688_690  POP_JUMP_IF_FALSE   700  'to 700'

 L. 237       692  POP_EXCEPT       
          694_696  JUMP_ABSOLUTE       800  'to 800'
              698  JUMP_FORWARD        708  'to 708'
            700_0  COME_FROM           688  '688'

 L. 239       700  LOAD_GLOBAL              OSError
              702  LOAD_STR                 'image file is truncated'
              704  CALL_FUNCTION_1       1  ''
              706  RAISE_VARARGS_1       1  'exception instance'
            708_0  COME_FROM           698  '698'
              708  POP_EXCEPT       
              710  JUMP_FORWARD        714  'to 714'
            712_0  COME_FROM           676  '676'
              712  END_FINALLY      
            714_0  COME_FROM           710  '710'
            714_1  COME_FROM           662  '662'

 L. 241       714  LOAD_FAST                's'
          716_718  POP_JUMP_IF_TRUE    748  'to 748'

 L. 242       720  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          722_724  POP_JUMP_IF_FALSE   732  'to 732'

 L. 243   726_728  BREAK_LOOP          800  'to 800'
              730  JUMP_FORWARD        748  'to 748'
            732_0  COME_FROM           722  '722'

 L. 245       732  LOAD_GLOBAL              OSError

 L. 246       734  LOAD_STR                 'image file is truncated (%d bytes not processed)'

 L. 247       736  LOAD_GLOBAL              len
              738  LOAD_FAST                'b'
              740  CALL_FUNCTION_1       1  ''

 L. 246       742  BINARY_MODULO    

 L. 245       744  CALL_FUNCTION_1       1  ''
              746  RAISE_VARARGS_1       1  'exception instance'
            748_0  COME_FROM           730  '730'
            748_1  COME_FROM           716  '716'

 L. 250       748  LOAD_FAST                'b'
              750  LOAD_FAST                's'
              752  BINARY_ADD       
              754  STORE_FAST               'b'

 L. 251       756  LOAD_FAST                'decoder'
              758  LOAD_METHOD              decode
              760  LOAD_FAST                'b'
              762  CALL_METHOD_1         1  ''
              764  UNPACK_SEQUENCE_2     2 
              766  STORE_FAST               'n'
              768  STORE_FAST               'err_code'

 L. 252       770  LOAD_FAST                'n'
              772  LOAD_CONST               0
              774  COMPARE_OP               <
          776_778  POP_JUMP_IF_FALSE   784  'to 784'

 L. 253   780_782  BREAK_LOOP          800  'to 800'
            784_0  COME_FROM           776  '776'

 L. 254       784  LOAD_FAST                'b'
              786  LOAD_FAST                'n'
              788  LOAD_CONST               None
              790  BUILD_SLICE_2         2 
              792  BINARY_SUBSCR    
              794  STORE_FAST               'b'
          796_798  JUMP_BACK           648  'to 648'
            800_0  COME_FROM           642  '642'
              800  POP_BLOCK        
              802  BEGIN_FINALLY    
            804_0  COME_FROM_FINALLY   584  '584'

 L. 257       804  LOAD_FAST                'decoder'
              806  LOAD_METHOD              cleanup
              808  CALL_METHOD_0         0  ''
              810  POP_TOP          
              812  END_FINALLY      
          814_816  JUMP_BACK           550  'to 550'
            818_0  COME_FROM           488  '488'

 L. 259       818  BUILD_LIST_0          0 
              820  LOAD_FAST                'self'
              822  STORE_ATTR               tile

 L. 260       824  LOAD_FAST                'readonly'
              826  LOAD_FAST                'self'
              828  STORE_ATTR               readonly

 L. 262       830  LOAD_FAST                'self'
              832  LOAD_METHOD              load_end
              834  CALL_METHOD_0         0  ''
              836  POP_TOP          

 L. 264       838  LOAD_FAST                'self'
              840  LOAD_ATTR                _exclusive_fp
          842_844  POP_JUMP_IF_FALSE   864  'to 864'
              846  LOAD_FAST                'self'
              848  LOAD_ATTR                _close_exclusive_fp_after_loading
          850_852  POP_JUMP_IF_FALSE   864  'to 864'

 L. 265       854  LOAD_FAST                'self'
              856  LOAD_ATTR                fp
              858  LOAD_METHOD              close
              860  CALL_METHOD_0         0  ''
              862  POP_TOP          
            864_0  COME_FROM           850  '850'
            864_1  COME_FROM           842  '842'

 L. 266       864  LOAD_CONST               None
              866  LOAD_FAST                'self'
              868  STORE_ATTR               fp

 L. 268       870  LOAD_FAST                'self'
              872  LOAD_ATTR                map
          874_876  POP_JUMP_IF_TRUE    902  'to 902'
              878  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          880_882  POP_JUMP_IF_TRUE    902  'to 902'
              884  LOAD_FAST                'err_code'
              886  LOAD_CONST               0
              888  COMPARE_OP               <
          890_892  POP_JUMP_IF_FALSE   902  'to 902'

 L. 270       894  LOAD_GLOBAL              raise_ioerror
              896  LOAD_FAST                'err_code'
              898  CALL_FUNCTION_1       1  ''
              900  POP_TOP          
            902_0  COME_FROM           890  '890'
            902_1  COME_FROM           880  '880'
            902_2  COME_FROM           874  '874'

 L. 272       902  LOAD_GLOBAL              Image
              904  LOAD_ATTR                Image
              906  LOAD_METHOD              load
              908  LOAD_FAST                'self'
              910  CALL_METHOD_1         1  ''
              912  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 694_696

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