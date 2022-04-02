# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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
            else:
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
          176_178  POP_JUMP_IF_FALSE   394  'to 394'

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

 L. 188   204_206  POP_JUMP_IF_FALSE   394  'to 394'

 L. 190       208  LOAD_GLOBAL              len
              210  LOAD_FAST                'args'
              212  CALL_FUNCTION_1       1  ''
              214  LOAD_CONST               3
              216  COMPARE_OP               >=

 L. 188   218_220  POP_JUMP_IF_FALSE   394  'to 394'

 L. 191       222  LOAD_FAST                'args'
              224  LOAD_CONST               0
              226  BINARY_SUBSCR    
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                mode
              232  COMPARE_OP               ==

 L. 188   234_236  POP_JUMP_IF_FALSE   394  'to 394'

 L. 192       238  LOAD_FAST                'args'
              240  LOAD_CONST               0
              242  BINARY_SUBSCR    
              244  LOAD_GLOBAL              Image
              246  LOAD_ATTR                _MAPMODES
              248  COMPARE_OP               in

 L. 188   250_252  POP_JUMP_IF_FALSE   394  'to 394'

 L. 194       254  SETUP_FINALLY       360  'to 360'

 L. 196       256  LOAD_CONST               0
              258  LOAD_CONST               None
              260  IMPORT_NAME              mmap
              262  STORE_FAST               'mmap'

 L. 198       264  LOAD_GLOBAL              open
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                filename
              270  CALL_FUNCTION_1       1  ''
              272  SETUP_WITH          304  'to 304'
              274  STORE_FAST               'fp'

 L. 199       276  LOAD_FAST                'mmap'
              278  LOAD_ATTR                mmap
              280  LOAD_FAST                'fp'
              282  LOAD_METHOD              fileno
              284  CALL_METHOD_0         0  ''
              286  LOAD_CONST               0
              288  LOAD_FAST                'mmap'
              290  LOAD_ATTR                ACCESS_READ
              292  LOAD_CONST               ('access',)
              294  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              296  LOAD_FAST                'self'
              298  STORE_ATTR               map
              300  POP_BLOCK        
              302  BEGIN_FINALLY    
            304_0  COME_FROM_WITH      272  '272'
              304  WITH_CLEANUP_START
              306  WITH_CLEANUP_FINISH
              308  END_FINALLY      

 L. 200       310  LOAD_GLOBAL              Image
              312  LOAD_ATTR                core
              314  LOAD_METHOD              map_buffer

 L. 201       316  LOAD_FAST                'self'
              318  LOAD_ATTR                map

 L. 201       320  LOAD_FAST                'self'
              322  LOAD_ATTR                size

 L. 201       324  LOAD_FAST                'decoder_name'

 L. 201       326  LOAD_FAST                'offset'

 L. 201       328  LOAD_FAST                'args'

 L. 200       330  CALL_METHOD_5         5  ''
              332  LOAD_FAST                'self'
              334  STORE_ATTR               im

 L. 203       336  LOAD_CONST               1
              338  STORE_FAST               'readonly'

 L. 206       340  LOAD_FAST                'self'
              342  LOAD_ATTR                palette
          344_346  POP_JUMP_IF_FALSE   356  'to 356'

 L. 207       348  LOAD_CONST               1
              350  LOAD_FAST                'self'
              352  LOAD_ATTR                palette
              354  STORE_ATTR               dirty
            356_0  COME_FROM           344  '344'
              356  POP_BLOCK        
              358  JUMP_FORWARD        394  'to 394'
            360_0  COME_FROM_FINALLY   254  '254'

 L. 208       360  DUP_TOP          
              362  LOAD_GLOBAL              AttributeError
              364  LOAD_GLOBAL              OSError
              366  LOAD_GLOBAL              ImportError
              368  BUILD_TUPLE_3         3 
              370  COMPARE_OP               exception-match
          372_374  POP_JUMP_IF_FALSE   392  'to 392'
              376  POP_TOP          
              378  POP_TOP          
              380  POP_TOP          

 L. 209       382  LOAD_CONST               None
              384  LOAD_FAST                'self'
              386  STORE_ATTR               map
              388  POP_EXCEPT       
              390  JUMP_FORWARD        394  'to 394'
            392_0  COME_FROM           372  '372'
              392  END_FINALLY      
            394_0  COME_FROM           390  '390'
            394_1  COME_FROM           358  '358'
            394_2  COME_FROM           250  '250'
            394_3  COME_FROM           234  '234'
            394_4  COME_FROM           218  '218'
            394_5  COME_FROM           204  '204'
            394_6  COME_FROM           176  '176'

 L. 211       394  LOAD_FAST                'self'
              396  LOAD_METHOD              load_prepare
              398  CALL_METHOD_0         0  ''
              400  POP_TOP          

 L. 212       402  LOAD_CONST               -3
              404  STORE_FAST               'err_code'

 L. 213       406  LOAD_FAST                'self'
              408  LOAD_ATTR                map
          410_412  POP_JUMP_IF_TRUE    764  'to 764'

 L. 215       414  LOAD_FAST                'self'
              416  LOAD_ATTR                tile
              418  LOAD_ATTR                sort
              420  LOAD_GLOBAL              _tilesort
              422  LOAD_CONST               ('key',)
              424  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              426  POP_TOP          

 L. 217       428  SETUP_FINALLY       440  'to 440'

 L. 219       430  LOAD_FAST                'self'
              432  LOAD_ATTR                tile_prefix
              434  STORE_FAST               'prefix'
              436  POP_BLOCK        
              438  JUMP_FORWARD        466  'to 466'
            440_0  COME_FROM_FINALLY   428  '428'

 L. 220       440  DUP_TOP          
              442  LOAD_GLOBAL              AttributeError
              444  COMPARE_OP               exception-match
          446_448  POP_JUMP_IF_FALSE   464  'to 464'
              450  POP_TOP          
              452  POP_TOP          
              454  POP_TOP          

 L. 221       456  LOAD_CONST               b''
              458  STORE_FAST               'prefix'
              460  POP_EXCEPT       
              462  JUMP_FORWARD        466  'to 466'
            464_0  COME_FROM           446  '446'
              464  END_FINALLY      
            466_0  COME_FROM           462  '462'
            466_1  COME_FROM           438  '438'

 L. 223       466  LOAD_FAST                'self'
              468  LOAD_ATTR                tile
              470  GET_ITER         
            472_0  COME_FROM           760  '760'
          472_474  FOR_ITER            764  'to 764'
              476  UNPACK_SEQUENCE_4     4 
              478  STORE_FAST               'decoder_name'
              480  STORE_FAST               'extents'
              482  STORE_FAST               'offset'
              484  STORE_FAST               'args'

 L. 224       486  LOAD_GLOBAL              Image
              488  LOAD_METHOD              _getdecoder

 L. 225       490  LOAD_FAST                'self'
              492  LOAD_ATTR                mode

 L. 225       494  LOAD_FAST                'decoder_name'

 L. 225       496  LOAD_FAST                'args'

 L. 225       498  LOAD_FAST                'self'
              500  LOAD_ATTR                decoderconfig

 L. 224       502  CALL_METHOD_4         4  ''
              504  STORE_FAST               'decoder'

 L. 227       506  SETUP_FINALLY       750  'to 750'

 L. 228       508  LOAD_FAST                'seek'
              510  LOAD_FAST                'offset'
              512  CALL_FUNCTION_1       1  ''
              514  POP_TOP          

 L. 229       516  LOAD_FAST                'decoder'
              518  LOAD_METHOD              setimage
              520  LOAD_FAST                'self'
              522  LOAD_ATTR                im
              524  LOAD_FAST                'extents'
              526  CALL_METHOD_2         2  ''
              528  POP_TOP          

 L. 230       530  LOAD_FAST                'decoder'
              532  LOAD_ATTR                pulls_fd
          534_536  POP_JUMP_IF_FALSE   566  'to 566'

 L. 231       538  LOAD_FAST                'decoder'
              540  LOAD_METHOD              setfd
              542  LOAD_FAST                'self'
              544  LOAD_ATTR                fp
              546  CALL_METHOD_1         1  ''
              548  POP_TOP          

 L. 232       550  LOAD_FAST                'decoder'
              552  LOAD_METHOD              decode
              554  LOAD_CONST               b''
              556  CALL_METHOD_1         1  ''
              558  UNPACK_SEQUENCE_2     2 
              560  STORE_FAST               'status'
              562  STORE_FAST               'err_code'
              564  JUMP_FORWARD        746  'to 746'
            566_0  COME_FROM           534  '534'

 L. 234       566  LOAD_FAST                'prefix'
              568  STORE_FAST               'b'
            570_0  COME_FROM           742  '742'

 L. 236       570  SETUP_FINALLY       586  'to 586'

 L. 237       572  LOAD_FAST                'read'
              574  LOAD_FAST                'self'
              576  LOAD_ATTR                decodermaxblock
              578  CALL_FUNCTION_1       1  ''
              580  STORE_FAST               's'
              582  POP_BLOCK        
              584  JUMP_FORWARD        656  'to 656'
            586_0  COME_FROM_FINALLY   570  '570'

 L. 238       586  DUP_TOP          
              588  LOAD_GLOBAL              IndexError
              590  LOAD_GLOBAL              struct
              592  LOAD_ATTR                error
              594  BUILD_TUPLE_2         2 
              596  COMPARE_OP               exception-match
          598_600  POP_JUMP_IF_FALSE   654  'to 654'
              602  POP_TOP          
              604  STORE_FAST               'e'
              606  POP_TOP          
              608  SETUP_FINALLY       642  'to 642'

 L. 240       610  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          612_614  POP_JUMP_IF_FALSE   628  'to 628'

 L. 241       616  POP_BLOCK        
              618  POP_EXCEPT       
              620  CALL_FINALLY        642  'to 642'
          622_624  JUMP_FORWARD        746  'to 746'
              626  JUMP_FORWARD        638  'to 638'
            628_0  COME_FROM           612  '612'

 L. 243       628  LOAD_GLOBAL              OSError
              630  LOAD_STR                 'image file is truncated'
              632  CALL_FUNCTION_1       1  ''
              634  LOAD_FAST                'e'
              636  RAISE_VARARGS_2       2  'exception instance with __cause__'
            638_0  COME_FROM           626  '626'
              638  POP_BLOCK        
              640  BEGIN_FINALLY    
            642_0  COME_FROM           620  '620'
            642_1  COME_FROM_FINALLY   608  '608'
              642  LOAD_CONST               None
              644  STORE_FAST               'e'
              646  DELETE_FAST              'e'
              648  END_FINALLY      
              650  POP_EXCEPT       
              652  JUMP_FORWARD        656  'to 656'
            654_0  COME_FROM           598  '598'
              654  END_FINALLY      
            656_0  COME_FROM           652  '652'
            656_1  COME_FROM           584  '584'

 L. 245       656  LOAD_FAST                's'
          658_660  POP_JUMP_IF_TRUE    694  'to 694'

 L. 246       662  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          664_666  POP_JUMP_IF_FALSE   674  'to 674'

 L. 247   668_670  JUMP_FORWARD        746  'to 746'
              672  BREAK_LOOP          694  'to 694'
            674_0  COME_FROM           664  '664'

 L. 249       674  LOAD_GLOBAL              OSError

 L. 250       676  LOAD_STR                 'image file is truncated ('
              678  LOAD_GLOBAL              len
              680  LOAD_FAST                'b'
              682  CALL_FUNCTION_1       1  ''
              684  FORMAT_VALUE          0  ''
              686  LOAD_STR                 ' bytes not processed)'
              688  BUILD_STRING_3        3 

 L. 249       690  CALL_FUNCTION_1       1  ''
              692  RAISE_VARARGS_1       1  'exception instance'
            694_0  COME_FROM           672  '672'
            694_1  COME_FROM           658  '658'

 L. 254       694  LOAD_FAST                'b'
              696  LOAD_FAST                's'
              698  BINARY_ADD       
              700  STORE_FAST               'b'

 L. 255       702  LOAD_FAST                'decoder'
              704  LOAD_METHOD              decode
              706  LOAD_FAST                'b'
              708  CALL_METHOD_1         1  ''
              710  UNPACK_SEQUENCE_2     2 
              712  STORE_FAST               'n'
              714  STORE_FAST               'err_code'

 L. 256       716  LOAD_FAST                'n'
              718  LOAD_CONST               0
              720  COMPARE_OP               <
          722_724  POP_JUMP_IF_FALSE   730  'to 730'

 L. 257   726_728  JUMP_FORWARD        746  'to 746'
            730_0  COME_FROM           722  '722'

 L. 258       730  LOAD_FAST                'b'
              732  LOAD_FAST                'n'
              734  LOAD_CONST               None
              736  BUILD_SLICE_2         2 
              738  BINARY_SUBSCR    
              740  STORE_FAST               'b'
          742_744  JUMP_BACK           570  'to 570'
            746_0  COME_FROM           726  '726'
            746_1  COME_FROM           668  '668'
            746_2  COME_FROM           622  '622'
            746_3  COME_FROM           564  '564'
              746  POP_BLOCK        
              748  BEGIN_FINALLY    
            750_0  COME_FROM_FINALLY   506  '506'

 L. 261       750  LOAD_FAST                'decoder'
              752  LOAD_METHOD              cleanup
              754  CALL_METHOD_0         0  ''
              756  POP_TOP          
              758  END_FINALLY      
          760_762  JUMP_BACK           472  'to 472'
            764_0  COME_FROM           472  '472'
            764_1  COME_FROM           410  '410'

 L. 263       764  BUILD_LIST_0          0 
              766  LOAD_FAST                'self'
              768  STORE_ATTR               tile

 L. 264       770  LOAD_FAST                'readonly'
              772  LOAD_FAST                'self'
              774  STORE_ATTR               readonly

 L. 266       776  LOAD_FAST                'self'
              778  LOAD_METHOD              load_end
              780  CALL_METHOD_0         0  ''
              782  POP_TOP          

 L. 268       784  LOAD_FAST                'self'
              786  LOAD_ATTR                _exclusive_fp
          788_790  POP_JUMP_IF_FALSE   810  'to 810'
              792  LOAD_FAST                'self'
              794  LOAD_ATTR                _close_exclusive_fp_after_loading
          796_798  POP_JUMP_IF_FALSE   810  'to 810'

 L. 269       800  LOAD_FAST                'self'
              802  LOAD_ATTR                fp
              804  LOAD_METHOD              close
              806  CALL_METHOD_0         0  ''
              808  POP_TOP          
            810_0  COME_FROM           796  '796'
            810_1  COME_FROM           788  '788'

 L. 270       810  LOAD_CONST               None
              812  LOAD_FAST                'self'
              814  STORE_ATTR               fp

 L. 272       816  LOAD_FAST                'self'
              818  LOAD_ATTR                map
          820_822  POP_JUMP_IF_TRUE    848  'to 848'
              824  LOAD_GLOBAL              LOAD_TRUNCATED_IMAGES
          826_828  POP_JUMP_IF_TRUE    848  'to 848'
              830  LOAD_FAST                'err_code'
              832  LOAD_CONST               0
              834  COMPARE_OP               <
          836_838  POP_JUMP_IF_FALSE   848  'to 848'

 L. 274       840  LOAD_GLOBAL              raise_oserror
              842  LOAD_FAST                'err_code'
              844  CALL_FUNCTION_1       1  ''
              846  POP_TOP          
            848_0  COME_FROM           836  '836'
            848_1  COME_FROM           826  '826'
            848_2  COME_FROM           820  '820'

 L. 276       848  LOAD_GLOBAL              Image
              850  LOAD_ATTR                Image
              852  LOAD_METHOD              load
              854  LOAD_FAST                'self'
              856  CALL_METHOD_1         1  ''
              858  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 618

    def load_prepare(self):
        if self.im:
            if self.im.mode != self.mode or (self.im.size != self.size):
                self.im = Image.core.new(self.mode, self.size)
            if self.mode == 'P':
                Image.Image.load(self)

    def load_end(self):
        pass

    def _seek_check(self, frame):
        if not frame < self._min_frame:
            if hasattr(self, '_n_frames') and self._n_frames is None or frame >= self.n_frames + self._min_frame:
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
                if not (self.offset > 0 or self.data):
                    return
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
            pass
        if self.image:
            pass
        else:
            try:
                with io.BytesIO(self.data) as fp:
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
                with io.BytesIO(self.data) as fp:
                    try:
                        self.image = Image.open(fp)
                    finally:
                        self.image.load()

            return self.image


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
              100  JUMP_FORWARD        316  'to 316'
            102_0  COME_FROM_FINALLY    80  '80'

 L. 502       102  DUP_TOP          
              104  LOAD_GLOBAL              AttributeError
              106  LOAD_GLOBAL              io
              108  LOAD_ATTR                UnsupportedOperation
              110  BUILD_TUPLE_2         2 
              112  COMPARE_OP               exception-match
          114_116  POP_JUMP_IF_FALSE   314  'to 314'
              118  POP_TOP          
              120  STORE_FAST               'exc'
              122  POP_TOP          
              124  SETUP_FINALLY       302  'to 302'

 L. 504       126  LOAD_FAST                'tile'
              128  GET_ITER         
            130_0  COME_FROM           296  '296'
              130  FOR_ITER            298  'to 298'
              132  UNPACK_SEQUENCE_4     4 
              134  STORE_FAST               'e'
              136  STORE_FAST               'b'
              138  STORE_FAST               'o'
              140  STORE_FAST               'a'

 L. 505       142  LOAD_GLOBAL              Image
              144  LOAD_METHOD              _getencoder
              146  LOAD_FAST                'im'
              148  LOAD_ATTR                mode
              150  LOAD_FAST                'e'
              152  LOAD_FAST                'a'
              154  LOAD_FAST                'im'
              156  LOAD_ATTR                encoderconfig
              158  CALL_METHOD_4         4  ''
              160  STORE_FAST               'e'

 L. 506       162  LOAD_FAST                'o'
              164  LOAD_CONST               0
              166  COMPARE_OP               >
              168  POP_JUMP_IF_FALSE   180  'to 180'

 L. 507       170  LOAD_FAST                'fp'
              172  LOAD_METHOD              seek
              174  LOAD_FAST                'o'
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          
            180_0  COME_FROM           168  '168'

 L. 508       180  LOAD_FAST                'e'
              182  LOAD_METHOD              setimage
              184  LOAD_FAST                'im'
              186  LOAD_ATTR                im
              188  LOAD_FAST                'b'
              190  CALL_METHOD_2         2  ''
              192  POP_TOP          

 L. 509       194  LOAD_FAST                'e'
              196  LOAD_ATTR                pushes_fd
              198  POP_JUMP_IF_FALSE   224  'to 224'

 L. 510       200  LOAD_FAST                'e'
              202  LOAD_METHOD              setfd
              204  LOAD_FAST                'fp'
              206  CALL_METHOD_1         1  ''
              208  POP_TOP          

 L. 511       210  LOAD_FAST                'e'
              212  LOAD_METHOD              encode_to_pyfd
              214  CALL_METHOD_0         0  ''
              216  UNPACK_SEQUENCE_2     2 
              218  STORE_FAST               'l'
              220  STORE_FAST               's'
              222  JUMP_FORWARD        260  'to 260'
            224_0  COME_FROM           258  '258'
            224_1  COME_FROM           252  '252'
            224_2  COME_FROM           198  '198'

 L. 514       224  LOAD_FAST                'e'
              226  LOAD_METHOD              encode
              228  LOAD_FAST                'bufsize'
              230  CALL_METHOD_1         1  ''
              232  UNPACK_SEQUENCE_3     3 
              234  STORE_FAST               'l'
              236  STORE_FAST               's'
              238  STORE_FAST               'd'

 L. 515       240  LOAD_FAST                'fp'
              242  LOAD_METHOD              write
              244  LOAD_FAST                'd'
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          

 L. 516       250  LOAD_FAST                's'
              252  POP_JUMP_IF_FALSE_BACK   224  'to 224'

 L. 517   254_256  JUMP_FORWARD        260  'to 260'
              258  JUMP_BACK           224  'to 224'
            260_0  COME_FROM           254  '254'
            260_1  COME_FROM           222  '222'

 L. 518       260  LOAD_FAST                's'
              262  LOAD_CONST               0
              264  COMPARE_OP               <
          266_268  POP_JUMP_IF_FALSE   288  'to 288'

 L. 519       270  LOAD_GLOBAL              OSError
              272  LOAD_STR                 'encoder error '
              274  LOAD_FAST                's'
              276  FORMAT_VALUE          0  ''
              278  LOAD_STR                 ' when writing image file'
              280  BUILD_STRING_3        3 
              282  CALL_FUNCTION_1       1  ''
              284  LOAD_FAST                'exc'
              286  RAISE_VARARGS_2       2  'exception instance with __cause__'
            288_0  COME_FROM           266  '266'

 L. 520       288  LOAD_FAST                'e'
              290  LOAD_METHOD              cleanup
              292  CALL_METHOD_0         0  ''
              294  POP_TOP          
              296  JUMP_BACK           130  'to 130'
            298_0  COME_FROM           130  '130'
              298  POP_BLOCK        
              300  BEGIN_FINALLY    
            302_0  COME_FROM_FINALLY   124  '124'
              302  LOAD_CONST               None
              304  STORE_FAST               'exc'
              306  DELETE_FAST              'exc'
              308  END_FINALLY      
              310  POP_EXCEPT       
              312  JUMP_FORWARD        468  'to 468'
            314_0  COME_FROM           114  '114'
              314  END_FINALLY      
            316_0  COME_FROM           100  '100'

 L. 523       316  LOAD_FAST                'tile'
              318  GET_ITER         
            320_0  COME_FROM           464  '464'
              320  FOR_ITER            468  'to 468'
              322  UNPACK_SEQUENCE_4     4 
              324  STORE_FAST               'e'
              326  STORE_FAST               'b'
              328  STORE_FAST               'o'
              330  STORE_FAST               'a'

 L. 524       332  LOAD_GLOBAL              Image
              334  LOAD_METHOD              _getencoder
              336  LOAD_FAST                'im'
              338  LOAD_ATTR                mode
              340  LOAD_FAST                'e'
              342  LOAD_FAST                'a'
              344  LOAD_FAST                'im'
              346  LOAD_ATTR                encoderconfig
              348  CALL_METHOD_4         4  ''
              350  STORE_FAST               'e'

 L. 525       352  LOAD_FAST                'o'
              354  LOAD_CONST               0
              356  COMPARE_OP               >
          358_360  POP_JUMP_IF_FALSE   372  'to 372'

 L. 526       362  LOAD_FAST                'fp'
              364  LOAD_METHOD              seek
              366  LOAD_FAST                'o'
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          
            372_0  COME_FROM           358  '358'

 L. 527       372  LOAD_FAST                'e'
              374  LOAD_METHOD              setimage
              376  LOAD_FAST                'im'
              378  LOAD_ATTR                im
              380  LOAD_FAST                'b'
              382  CALL_METHOD_2         2  ''
              384  POP_TOP          

 L. 528       386  LOAD_FAST                'e'
              388  LOAD_ATTR                pushes_fd
          390_392  POP_JUMP_IF_FALSE   418  'to 418'

 L. 529       394  LOAD_FAST                'e'
              396  LOAD_METHOD              setfd
              398  LOAD_FAST                'fp'
              400  CALL_METHOD_1         1  ''
              402  POP_TOP          

 L. 530       404  LOAD_FAST                'e'
              406  LOAD_METHOD              encode_to_pyfd
              408  CALL_METHOD_0         0  ''
              410  UNPACK_SEQUENCE_2     2 
              412  STORE_FAST               'l'
              414  STORE_FAST               's'
              416  JUMP_FORWARD        430  'to 430'
            418_0  COME_FROM           390  '390'

 L. 532       418  LOAD_FAST                'e'
              420  LOAD_METHOD              encode_to_file
              422  LOAD_FAST                'fh'
              424  LOAD_FAST                'bufsize'
              426  CALL_METHOD_2         2  ''
              428  STORE_FAST               's'
            430_0  COME_FROM           416  '416'

 L. 533       430  LOAD_FAST                's'
              432  LOAD_CONST               0
              434  COMPARE_OP               <
          436_438  POP_JUMP_IF_FALSE   456  'to 456'

 L. 534       440  LOAD_GLOBAL              OSError
              442  LOAD_STR                 'encoder error '
              444  LOAD_FAST                's'
              446  FORMAT_VALUE          0  ''
              448  LOAD_STR                 ' when writing image file'
              450  BUILD_STRING_3        3 
              452  CALL_FUNCTION_1       1  ''
              454  RAISE_VARARGS_1       1  'exception instance'
            456_0  COME_FROM           436  '436'

 L. 535       456  LOAD_FAST                'e'
              458  LOAD_METHOD              cleanup
              460  CALL_METHOD_0         0  ''
              462  POP_TOP          
          464_466  JUMP_BACK           320  'to 320'
            468_0  COME_FROM           320  '320'
            468_1  COME_FROM           312  '312'

 L. 536       468  LOAD_GLOBAL              hasattr
              470  LOAD_FAST                'fp'
              472  LOAD_STR                 'flush'
              474  CALL_FUNCTION_2       2  ''
          476_478  POP_JUMP_IF_FALSE   488  'to 488'

 L. 537       480  LOAD_FAST                'fp'
              482  LOAD_METHOD              flush
              484  CALL_METHOD_0         0  ''
              486  POP_TOP          
            488_0  COME_FROM           476  '476'

Parse error at or near `JUMP_BACK' instruction at offset 258


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
    if size <= SAFEBLOCK:
        data = fp.read(size)
        if len(data) < size:
            raise OSError('Truncated File Read')
        return data
    data = []
    while True:
        if size > 0:
            block = fp.read(min(size, SAFEBLOCK))
            if not block:
                pass
            else:
                data.append(block)
                size -= len(block)

    if sum((len(d) for d in data)) < size:
        raise OSError('Truncated File Read')
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
        d.setimage(self.im, self.state.extents())
        s = d.decode(data)
        if s[0] >= 0:
            raise ValueError('not enough image data')
        if s[1] != 0:
            raise ValueError('cannot decode image data')