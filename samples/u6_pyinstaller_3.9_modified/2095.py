# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\PngImagePlugin.py
import itertools, logging, re, struct, warnings, zlib
from . import Image, ImageChops, ImageFile, ImagePalette, ImageSequence
from ._binary import i16be as i16
from ._binary import i32be as i32
from ._binary import o8
from ._binary import o16be as o16
from ._binary import o32be as o32
logger = logging.getLogger(__name__)
is_cid = re.compile(b'\\w\\w\\w\\w').match
_MAGIC = b'\x89PNG\r\n\x1a\n'
_MODES = {(1, 0):('1', '1'), 
 (2, 0):('L', 'L;2'), 
 (4, 0):('L', 'L;4'), 
 (8, 0):('L', 'L'), 
 (16, 0):('I', 'I;16B'), 
 (8, 2):('RGB', 'RGB'), 
 (16, 2):('RGB', 'RGB;16B'), 
 (1, 3):('P', 'P;1'), 
 (2, 3):('P', 'P;2'), 
 (4, 3):('P', 'P;4'), 
 (8, 3):('P', 'P'), 
 (8, 4):('LA', 'LA'), 
 (16, 4):('RGBA', 'LA;16B'), 
 (8, 6):('RGBA', 'RGBA'), 
 (16, 6):('RGBA', 'RGBA;16B')}
_simple_palette = re.compile(b'^\xff*\x00\xff*$')
MAX_TEXT_CHUNK = ImageFile.SAFEBLOCK
MAX_TEXT_MEMORY = 64 * MAX_TEXT_CHUNK
APNG_DISPOSE_OP_NONE = 0
APNG_DISPOSE_OP_BACKGROUND = 1
APNG_DISPOSE_OP_PREVIOUS = 2
APNG_BLEND_OP_SOURCE = 0
APNG_BLEND_OP_OVER = 1

def _safe_zlib_decompress(s):
    dobj = zlib.decompressobj()
    plaintext = dobj.decompress(s, MAX_TEXT_CHUNK)
    if dobj.unconsumed_tail:
        raise ValueError('Decompressed Data Too Large')
    return plaintext


def _crc32(data, seed=0):
    return zlib.crc32(data, seed) & 4294967295


class ChunkStream:

    def __init__(self, fp):
        self.fp = fp
        self.queue = []

    def read(self):
        """Fetch a new chunk. Returns header information."""
        cid = None
        if self.queue:
            cid, pos, length = self.queue.pop()
            self.fp.seek(pos)
        else:
            s = self.fp.read(8)
            cid = s[4:]
            pos = self.fp.tell()
            length = i32(s)
        if not is_cid(cid):
            if not ImageFile.LOAD_TRUNCATED_IMAGES:
                raise SyntaxError(f"broken PNG file (chunk {repr(cid)})")
        return (
         cid, pos, length)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self.queue = self.crc = self.fp = None

    def push(self, cid, pos, length):
        self.queue.append((cid, pos, length))

    def call(self, cid, pos, length):
        """Call the appropriate chunk handler"""
        logger.debug('STREAM %r %s %s', cid, pos, length)
        return getattr(self, 'chunk_' + cid.decode('ascii'))(pos, length)

    def crc--- This code section failed: ---

 L. 195         0  LOAD_GLOBAL              ImageFile
                2  LOAD_ATTR                LOAD_TRUNCATED_IMAGES
                4  POP_JUMP_IF_FALSE    38  'to 38'
                6  LOAD_FAST                'cid'
                8  LOAD_CONST               0
               10  BINARY_SUBSCR    
               12  LOAD_CONST               5
               14  BINARY_RSHIFT    
               16  LOAD_CONST               1
               18  BINARY_AND       
               20  POP_JUMP_IF_FALSE    38  'to 38'

 L. 196        22  LOAD_FAST                'self'
               24  LOAD_METHOD              crc_skip
               26  LOAD_FAST                'cid'
               28  LOAD_FAST                'data'
               30  CALL_METHOD_2         2  ''
               32  POP_TOP          

 L. 197        34  LOAD_CONST               None
               36  RETURN_VALUE     
             38_0  COME_FROM            20  '20'
             38_1  COME_FROM             4  '4'

 L. 199        38  SETUP_FINALLY       102  'to 102'

 L. 200        40  LOAD_GLOBAL              _crc32
               42  LOAD_FAST                'data'
               44  LOAD_GLOBAL              _crc32
               46  LOAD_FAST                'cid'
               48  CALL_FUNCTION_1       1  ''
               50  CALL_FUNCTION_2       2  ''
               52  STORE_FAST               'crc1'

 L. 201        54  LOAD_GLOBAL              i32
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                fp
               60  LOAD_METHOD              read
               62  LOAD_CONST               4
               64  CALL_METHOD_1         1  ''
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'crc2'

 L. 202        70  LOAD_FAST                'crc1'
               72  LOAD_FAST                'crc2'
               74  COMPARE_OP               !=
               76  POP_JUMP_IF_FALSE    98  'to 98'

 L. 203        78  LOAD_GLOBAL              SyntaxError

 L. 204        80  LOAD_STR                 'broken PNG file (bad header checksum in '
               82  LOAD_GLOBAL              repr
               84  LOAD_FAST                'cid'
               86  CALL_FUNCTION_1       1  ''
               88  FORMAT_VALUE          0  ''
               90  LOAD_STR                 ')'
               92  BUILD_STRING_3        3 

 L. 203        94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            76  '76'
               98  POP_BLOCK        
              100  JUMP_FORWARD        162  'to 162'
            102_0  COME_FROM_FINALLY    38  '38'

 L. 206       102  DUP_TOP          
              104  LOAD_GLOBAL              struct
              106  LOAD_ATTR                error
              108  <121>               160  ''
              110  POP_TOP          
              112  STORE_FAST               'e'
              114  POP_TOP          
              116  SETUP_FINALLY       152  'to 152'

 L. 207       118  LOAD_GLOBAL              SyntaxError

 L. 208       120  LOAD_STR                 'broken PNG file (incomplete checksum in '
              122  LOAD_GLOBAL              repr
              124  LOAD_FAST                'cid'
              126  CALL_FUNCTION_1       1  ''
              128  FORMAT_VALUE          0  ''
              130  LOAD_STR                 ')'
              132  BUILD_STRING_3        3 

 L. 207       134  CALL_FUNCTION_1       1  ''

 L. 209       136  LOAD_FAST                'e'

 L. 207       138  RAISE_VARARGS_2       2  'exception instance with __cause__'
              140  POP_BLOCK        
              142  POP_EXCEPT       
              144  LOAD_CONST               None
              146  STORE_FAST               'e'
              148  DELETE_FAST              'e'
              150  JUMP_FORWARD        162  'to 162'
            152_0  COME_FROM_FINALLY   116  '116'
              152  LOAD_CONST               None
              154  STORE_FAST               'e'
              156  DELETE_FAST              'e'
              158  <48>             
              160  <48>             
            162_0  COME_FROM           150  '150'
            162_1  COME_FROM           100  '100'

Parse error at or near `<121>' instruction at offset 108

    def crc_skip(self, cid, data):
        """Read checksum.  Used if the C module is not present"""
        self.fp.read(4)

    def verify--- This code section failed: ---

 L. 221         0  BUILD_LIST_0          0 
                2  STORE_FAST               'cids'

 L. 224         4  SETUP_FINALLY        24  'to 24'

 L. 225         6  LOAD_FAST                'self'
                8  LOAD_METHOD              read
               10  CALL_METHOD_0         0  ''
               12  UNPACK_SEQUENCE_3     3 
               14  STORE_FAST               'cid'
               16  STORE_FAST               'pos'
               18  STORE_FAST               'length'
               20  POP_BLOCK        
               22  JUMP_FORWARD         72  'to 72'
             24_0  COME_FROM_FINALLY     4  '4'

 L. 226        24  DUP_TOP          
               26  LOAD_GLOBAL              struct
               28  LOAD_ATTR                error
               30  <121>                70  ''
               32  POP_TOP          
               34  STORE_FAST               'e'
               36  POP_TOP          
               38  SETUP_FINALLY        62  'to 62'

 L. 227        40  LOAD_GLOBAL              OSError
               42  LOAD_STR                 'truncated PNG file'
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_FAST                'e'
               48  RAISE_VARARGS_2       2  'exception instance with __cause__'
               50  POP_BLOCK        
               52  POP_EXCEPT       
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  JUMP_FORWARD         72  'to 72'
             62_0  COME_FROM_FINALLY    38  '38'
               62  LOAD_CONST               None
               64  STORE_FAST               'e'
               66  DELETE_FAST              'e'
               68  <48>             
               70  <48>             
             72_0  COME_FROM            60  '60'
             72_1  COME_FROM            22  '22'

 L. 229        72  LOAD_FAST                'cid'
               74  LOAD_FAST                'endchunk'
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE    82  'to 82'

 L. 230        80  BREAK_LOOP          116  'to 116'
             82_0  COME_FROM            78  '78'

 L. 231        82  LOAD_FAST                'self'
               84  LOAD_METHOD              crc
               86  LOAD_FAST                'cid'
               88  LOAD_GLOBAL              ImageFile
               90  LOAD_METHOD              _safe_read
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                fp
               96  LOAD_FAST                'length'
               98  CALL_METHOD_2         2  ''
              100  CALL_METHOD_2         2  ''
              102  POP_TOP          

 L. 232       104  LOAD_FAST                'cids'
              106  LOAD_METHOD              append
              108  LOAD_FAST                'cid'
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          
              114  JUMP_BACK             4  'to 4'

 L. 234       116  LOAD_FAST                'cids'
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 30


class iTXt(str):
    __doc__ = '\n    Subclass of string to allow iTXt chunks to look like strings while\n    keeping their extra information\n\n    '

    @staticmethod
    def __new__(cls, text, lang=None, tkey=None):
        """
        :param cls: the class to use when creating the instance
        :param text: value for this key
        :param lang: language code
        :param tkey: UTF-8 version of the key name
        """
        self = str.__new__(cls, text)
        self.lang = lang
        self.tkey = tkey
        return self


class PngInfo:
    __doc__ = '\n    PNG chunk container (for use with save(pnginfo=))\n\n    '

    def __init__(self):
        self.chunks = []

    def add(self, cid, data, after_idat=False):
        """Appends an arbitrary chunk. Use with caution.

        :param cid: a byte string, 4 bytes long.
        :param data: a byte string of the encoded data
        :param after_idat: for use with private chunks. Whether the chunk
                           should be written after IDAT

        """
        chunk = [
         cid, data]
        if after_idat:
            chunk.append(True)
        self.chunks.append(tuple(chunk))

    def add_itxt(self, key, value, lang='', tkey='', zip=False):
        """Appends an iTXt chunk.

        :param key: latin-1 encodable text key name
        :param value: value for this key
        :param lang: language code
        :param tkey: UTF-8 version of the key name
        :param zip: compression flag

        """
        if not isinstance(key, bytes):
            key = key.encode('latin-1', 'strict')
        else:
            if not isinstance(value, bytes):
                value = value.encode('utf-8', 'strict')
            else:
                if not isinstance(lang, bytes):
                    lang = lang.encode('utf-8', 'strict')
                tkey = isinstance(tkey, bytes) or tkey.encode('utf-8', 'strict')
            if zip:
                self.add(b'iTXt', key + b'\x00\x01\x00' + lang + b'\x00' + tkey + b'\x00' + zlib.compress(value))
            else:
                self.add(b'iTXt', key + b'\x00\x00\x00' + lang + b'\x00' + tkey + b'\x00' + value)

    def add_text--- This code section failed: ---

 L. 320         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              iTXt
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    34  'to 34'

 L. 321        10  LOAD_FAST                'self'
               12  LOAD_ATTR                add_itxt
               14  LOAD_FAST                'key'
               16  LOAD_FAST                'value'
               18  LOAD_FAST                'value'
               20  LOAD_ATTR                lang
               22  LOAD_FAST                'value'
               24  LOAD_ATTR                tkey
               26  LOAD_FAST                'zip'
               28  LOAD_CONST               ('zip',)
               30  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               32  RETURN_VALUE     
             34_0  COME_FROM             8  '8'

 L. 324        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'value'
               38  LOAD_GLOBAL              bytes
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_TRUE     96  'to 96'

 L. 325        44  SETUP_FINALLY        62  'to 62'

 L. 326        46  LOAD_FAST                'value'
               48  LOAD_METHOD              encode
               50  LOAD_STR                 'latin-1'
               52  LOAD_STR                 'strict'
               54  CALL_METHOD_2         2  ''
               56  STORE_FAST               'value'
               58  POP_BLOCK        
               60  JUMP_FORWARD         96  'to 96'
             62_0  COME_FROM_FINALLY    44  '44'

 L. 327        62  DUP_TOP          
               64  LOAD_GLOBAL              UnicodeError
               66  <121>                94  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 328        74  LOAD_FAST                'self'
               76  LOAD_ATTR                add_itxt
               78  LOAD_FAST                'key'
               80  LOAD_FAST                'value'
               82  LOAD_FAST                'zip'
               84  LOAD_CONST               ('zip',)
               86  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               88  ROT_FOUR         
               90  POP_EXCEPT       
               92  RETURN_VALUE     
               94  <48>             
             96_0  COME_FROM            60  '60'
             96_1  COME_FROM            42  '42'

 L. 330        96  LOAD_GLOBAL              isinstance
               98  LOAD_FAST                'key'
              100  LOAD_GLOBAL              bytes
              102  CALL_FUNCTION_2       2  ''
              104  POP_JUMP_IF_TRUE    118  'to 118'

 L. 331       106  LOAD_FAST                'key'
              108  LOAD_METHOD              encode
              110  LOAD_STR                 'latin-1'
              112  LOAD_STR                 'strict'
              114  CALL_METHOD_2         2  ''
              116  STORE_FAST               'key'
            118_0  COME_FROM           104  '104'

 L. 333       118  LOAD_FAST                'zip'
              120  POP_JUMP_IF_FALSE   150  'to 150'

 L. 334       122  LOAD_FAST                'self'
              124  LOAD_METHOD              add
              126  LOAD_CONST               b'zTXt'
              128  LOAD_FAST                'key'
              130  LOAD_CONST               b'\x00\x00'
              132  BINARY_ADD       
              134  LOAD_GLOBAL              zlib
              136  LOAD_METHOD              compress
              138  LOAD_FAST                'value'
              140  CALL_METHOD_1         1  ''
              142  BINARY_ADD       
              144  CALL_METHOD_2         2  ''
              146  POP_TOP          
              148  JUMP_FORWARD        170  'to 170'
            150_0  COME_FROM           120  '120'

 L. 336       150  LOAD_FAST                'self'
              152  LOAD_METHOD              add
              154  LOAD_CONST               b'tEXt'
              156  LOAD_FAST                'key'
              158  LOAD_CONST               b'\x00'
              160  BINARY_ADD       
              162  LOAD_FAST                'value'
              164  BINARY_ADD       
              166  CALL_METHOD_2         2  ''
              168  POP_TOP          
            170_0  COME_FROM           148  '148'

Parse error at or near `<121>' instruction at offset 66


class PngStream(ChunkStream):

    def __init__(self, fp):
        super().__init__(fp)
        self.im_info = {}
        self.im_text = {}
        self.im_size = (0, 0)
        self.im_mode = None
        self.im_tile = None
        self.im_palette = None
        self.im_custom_mimetype = None
        self.im_n_frames = None
        self._seq_num = None
        self.rewind_state = None
        self.text_memory = 0

    def check_text_memory(self, chunklen):
        self.text_memory += chunklen
        if self.text_memory > MAX_TEXT_MEMORY:
            raise ValueError(f"Too much memory used in text chunks: {self.text_memory}>MAX_TEXT_MEMORY")

    def save_rewind(self):
        self.rewind_state = {'info':self.im_info.copy(), 
         'tile':self.im_tile, 
         'seq_num':self._seq_num}

    def rewind(self):
        self.im_info = self.rewind_state['info']
        self.im_tile = self.rewind_state['tile']
        self._seq_num = self.rewind_state['seq_num']

    def chunk_iCCP--- This code section failed: ---

 L. 384         0  LOAD_GLOBAL              ImageFile
                2  LOAD_METHOD              _safe_read
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fp
                8  LOAD_FAST                'length'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               's'

 L. 390        14  LOAD_FAST                's'
               16  LOAD_METHOD              find
               18  LOAD_CONST               b'\x00'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'i'

 L. 391        24  LOAD_GLOBAL              logger
               26  LOAD_METHOD              debug
               28  LOAD_STR                 'iCCP profile name %r'
               30  LOAD_FAST                's'
               32  LOAD_CONST               None
               34  LOAD_FAST                'i'
               36  BUILD_SLICE_2         2 
               38  BINARY_SUBSCR    
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          

 L. 392        44  LOAD_GLOBAL              logger
               46  LOAD_METHOD              debug
               48  LOAD_STR                 'Compression method %s'
               50  LOAD_FAST                's'
               52  LOAD_FAST                'i'
               54  BINARY_SUBSCR    
               56  CALL_METHOD_2         2  ''
               58  POP_TOP          

 L. 393        60  LOAD_FAST                's'
               62  LOAD_FAST                'i'
               64  BINARY_SUBSCR    
               66  STORE_FAST               'comp_method'

 L. 394        68  LOAD_FAST                'comp_method'
               70  LOAD_CONST               0
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_FALSE    92  'to 92'

 L. 395        76  LOAD_GLOBAL              SyntaxError
               78  LOAD_STR                 'Unknown compression method '
               80  LOAD_FAST                'comp_method'
               82  FORMAT_VALUE          0  ''
               84  LOAD_STR                 ' in iCCP chunk'
               86  BUILD_STRING_3        3 
               88  CALL_FUNCTION_1       1  ''
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            74  '74'

 L. 396        92  SETUP_FINALLY       118  'to 118'

 L. 397        94  LOAD_GLOBAL              _safe_zlib_decompress
               96  LOAD_FAST                's'
               98  LOAD_FAST                'i'
              100  LOAD_CONST               2
              102  BINARY_ADD       
              104  LOAD_CONST               None
              106  BUILD_SLICE_2         2 
              108  BINARY_SUBSCR    
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'icc_profile'
              114  POP_BLOCK        
              116  JUMP_FORWARD        172  'to 172'
            118_0  COME_FROM_FINALLY    92  '92'

 L. 398       118  DUP_TOP          
              120  LOAD_GLOBAL              ValueError
              122  <121>               148  ''
              124  POP_TOP          
              126  POP_TOP          
              128  POP_TOP          

 L. 399       130  LOAD_GLOBAL              ImageFile
              132  LOAD_ATTR                LOAD_TRUNCATED_IMAGES
              134  POP_JUMP_IF_FALSE   142  'to 142'

 L. 400       136  LOAD_CONST               None
              138  STORE_FAST               'icc_profile'
              140  JUMP_FORWARD        144  'to 144'
            142_0  COME_FROM           134  '134'

 L. 402       142  RAISE_VARARGS_0       0  'reraise'
            144_0  COME_FROM           140  '140'
              144  POP_EXCEPT       
              146  JUMP_FORWARD        172  'to 172'

 L. 403       148  DUP_TOP          
              150  LOAD_GLOBAL              zlib
              152  LOAD_ATTR                error
              154  <121>               170  ''
              156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          

 L. 404       162  LOAD_CONST               None
              164  STORE_FAST               'icc_profile'
              166  POP_EXCEPT       
              168  JUMP_FORWARD        172  'to 172'
              170  <48>             
            172_0  COME_FROM           168  '168'
            172_1  COME_FROM           146  '146'
            172_2  COME_FROM           116  '116'

 L. 405       172  LOAD_FAST                'icc_profile'
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                im_info
              178  LOAD_STR                 'icc_profile'
              180  STORE_SUBSCR     

 L. 406       182  LOAD_FAST                's'
              184  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 122

    def chunk_IHDR--- This code section failed: ---

 L. 411         0  LOAD_GLOBAL              ImageFile
                2  LOAD_METHOD              _safe_read
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fp
                8  LOAD_FAST                'length'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               's'

 L. 412        14  LOAD_GLOBAL              i32
               16  LOAD_FAST                's'
               18  LOAD_CONST               0
               20  CALL_FUNCTION_2       2  ''
               22  LOAD_GLOBAL              i32
               24  LOAD_FAST                's'
               26  LOAD_CONST               4
               28  CALL_FUNCTION_2       2  ''
               30  BUILD_TUPLE_2         2 
               32  LOAD_FAST                'self'
               34  STORE_ATTR               im_size

 L. 413        36  SETUP_FINALLY        70  'to 70'

 L. 414        38  LOAD_GLOBAL              _MODES
               40  LOAD_FAST                's'
               42  LOAD_CONST               8
               44  BINARY_SUBSCR    
               46  LOAD_FAST                's'
               48  LOAD_CONST               9
               50  BINARY_SUBSCR    
               52  BUILD_TUPLE_2         2 
               54  BINARY_SUBSCR    
               56  UNPACK_SEQUENCE_2     2 
               58  LOAD_FAST                'self'
               60  STORE_ATTR               im_mode
               62  LOAD_FAST                'self'
               64  STORE_ATTR               im_rawmode
               66  POP_BLOCK        
               68  JUMP_FORWARD         88  'to 88'
             70_0  COME_FROM_FINALLY    36  '36'

 L. 415        70  DUP_TOP          
               72  LOAD_GLOBAL              Exception
               74  <121>                86  ''
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 416        82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
               86  <48>             
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            68  '68'

 L. 417        88  LOAD_FAST                's'
               90  LOAD_CONST               12
               92  BINARY_SUBSCR    
               94  POP_JUMP_IF_FALSE   106  'to 106'

 L. 418        96  LOAD_CONST               1
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                im_info
              102  LOAD_STR                 'interlace'
              104  STORE_SUBSCR     
            106_0  COME_FROM            94  '94'

 L. 419       106  LOAD_FAST                's'
              108  LOAD_CONST               11
              110  BINARY_SUBSCR    
              112  POP_JUMP_IF_FALSE   122  'to 122'

 L. 420       114  LOAD_GLOBAL              SyntaxError
              116  LOAD_STR                 'unknown filter category'
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           112  '112'

 L. 421       122  LOAD_FAST                's'
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 74

    def chunk_IDAT--- This code section failed: ---

 L. 426         0  LOAD_STR                 'bbox'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                im_info
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    34  'to 34'

 L. 427        10  LOAD_STR                 'zip'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                im_info
               16  LOAD_STR                 'bbox'
               18  BINARY_SUBSCR    
               20  LOAD_FAST                'pos'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                im_rawmode
               26  BUILD_TUPLE_4         4 
               28  BUILD_LIST_1          1 
               30  STORE_FAST               'tile'
               32  JUMP_FORWARD         76  'to 76'
             34_0  COME_FROM             8  '8'

 L. 429        34  LOAD_FAST                'self'
               36  LOAD_ATTR                im_n_frames
               38  LOAD_CONST               None
               40  <117>                 1  ''
               42  POP_JUMP_IF_FALSE    54  'to 54'

 L. 430        44  LOAD_CONST               True
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                im_info
               50  LOAD_STR                 'default_image'
               52  STORE_SUBSCR     
             54_0  COME_FROM            42  '42'

 L. 431        54  LOAD_STR                 'zip'
               56  LOAD_CONST               (0, 0)
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                im_size
               62  BINARY_ADD       
               64  LOAD_FAST                'pos'
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                im_rawmode
               70  BUILD_TUPLE_4         4 
               72  BUILD_LIST_1          1 
               74  STORE_FAST               'tile'
             76_0  COME_FROM            32  '32'

 L. 432        76  LOAD_FAST                'tile'
               78  LOAD_FAST                'self'
               80  STORE_ATTR               im_tile

 L. 433        82  LOAD_FAST                'length'
               84  LOAD_FAST                'self'
               86  STORE_ATTR               im_idat

 L. 434        88  LOAD_GLOBAL              EOFError
               90  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `None' instruction at offset -1

    def chunk_IEND(self, pos, length):
        raise EOFError

    def chunk_PLTE(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        if self.im_mode == 'P':
            self.im_palette = (
             'RGB', s)
        return s

    def chunk_tRNS--- This code section failed: ---

 L. 452         0  LOAD_GLOBAL              ImageFile
                2  LOAD_METHOD              _safe_read
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fp
                8  LOAD_FAST                'length'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               's'

 L. 453        14  LOAD_FAST                'self'
               16  LOAD_ATTR                im_mode
               18  LOAD_STR                 'P'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    76  'to 76'

 L. 454        24  LOAD_GLOBAL              _simple_palette
               26  LOAD_METHOD              match
               28  LOAD_FAST                's'
               30  CALL_METHOD_1         1  ''
               32  POP_JUMP_IF_FALSE    64  'to 64'

 L. 457        34  LOAD_FAST                's'
               36  LOAD_METHOD              find
               38  LOAD_CONST               b'\x00'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'i'

 L. 458        44  LOAD_FAST                'i'
               46  LOAD_CONST               0
               48  COMPARE_OP               >=
               50  POP_JUMP_IF_FALSE    74  'to 74'

 L. 459        52  LOAD_FAST                'i'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                im_info
               58  LOAD_STR                 'transparency'
               60  STORE_SUBSCR     
               62  JUMP_ABSOLUTE       144  'to 144'
             64_0  COME_FROM            32  '32'

 L. 463        64  LOAD_FAST                's'
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                im_info
               70  LOAD_STR                 'transparency'
               72  STORE_SUBSCR     
             74_0  COME_FROM            50  '50'
               74  JUMP_FORWARD        144  'to 144'
             76_0  COME_FROM            22  '22'

 L. 464        76  LOAD_FAST                'self'
               78  LOAD_ATTR                im_mode
               80  LOAD_CONST               ('1', 'L', 'I')
               82  <118>                 0  ''
               84  POP_JUMP_IF_FALSE   102  'to 102'

 L. 465        86  LOAD_GLOBAL              i16
               88  LOAD_FAST                's'
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                im_info
               96  LOAD_STR                 'transparency'
               98  STORE_SUBSCR     
              100  JUMP_FORWARD        144  'to 144'
            102_0  COME_FROM            84  '84'

 L. 466       102  LOAD_FAST                'self'
              104  LOAD_ATTR                im_mode
              106  LOAD_STR                 'RGB'
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   144  'to 144'

 L. 467       112  LOAD_GLOBAL              i16
              114  LOAD_FAST                's'
              116  CALL_FUNCTION_1       1  ''
              118  LOAD_GLOBAL              i16
              120  LOAD_FAST                's'
              122  LOAD_CONST               2
              124  CALL_FUNCTION_2       2  ''
              126  LOAD_GLOBAL              i16
              128  LOAD_FAST                's'
              130  LOAD_CONST               4
              132  CALL_FUNCTION_2       2  ''
              134  BUILD_TUPLE_3         3 
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                im_info
              140  LOAD_STR                 'transparency'
              142  STORE_SUBSCR     
            144_0  COME_FROM           110  '110'
            144_1  COME_FROM           100  '100'
            144_2  COME_FROM            74  '74'

 L. 468       144  LOAD_FAST                's'
              146  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 82

    def chunk_gAMA(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        self.im_info['gamma'] = i32(s) / 100000.0
        return s

    def chunk_cHRM(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        raw_vals = struct.unpack('>%dI' % (len(s) // 4), s)
        self.im_info['chromaticity'] = tuple((elt / 100000.0 for elt in raw_vals))
        return s

    def chunk_sRGB(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        self.im_info['srgb'] = s[0]
        return s

    def chunk_pHYs(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        px, py = i32(s, 0), i32(s, 4)
        unit = s[8]
        if unit == 1:
            dpi = (
             px * 0.0254, py * 0.0254)
            self.im_info['dpi'] = dpi
        else:
            if unit == 0:
                self.im_info['aspect'] = (
                 px, py)
        return s

    def chunk_tEXt--- This code section failed: ---

 L. 512         0  LOAD_GLOBAL              ImageFile
                2  LOAD_METHOD              _safe_read
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fp
                8  LOAD_FAST                'length'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               's'

 L. 513        14  SETUP_FINALLY        36  'to 36'

 L. 514        16  LOAD_FAST                's'
               18  LOAD_METHOD              split
               20  LOAD_CONST               b'\x00'
               22  LOAD_CONST               1
               24  CALL_METHOD_2         2  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'k'
               30  STORE_FAST               'v'
               32  POP_BLOCK        
               34  JUMP_FORWARD         62  'to 62'
             36_0  COME_FROM_FINALLY    14  '14'

 L. 515        36  DUP_TOP          
               38  LOAD_GLOBAL              ValueError
               40  <121>                60  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 517        48  LOAD_FAST                's'
               50  STORE_FAST               'k'

 L. 518        52  LOAD_CONST               b''
               54  STORE_FAST               'v'
               56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
               60  <48>             
             62_0  COME_FROM            58  '58'
             62_1  COME_FROM            34  '34'

 L. 519        62  LOAD_FAST                'k'
               64  POP_JUMP_IF_FALSE   136  'to 136'

 L. 520        66  LOAD_FAST                'k'
               68  LOAD_METHOD              decode
               70  LOAD_STR                 'latin-1'
               72  LOAD_STR                 'strict'
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'k'

 L. 521        78  LOAD_FAST                'v'
               80  LOAD_METHOD              decode
               82  LOAD_STR                 'latin-1'
               84  LOAD_STR                 'replace'
               86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'v_str'

 L. 523        90  LOAD_FAST                'k'
               92  LOAD_STR                 'exif'
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   102  'to 102'
               98  LOAD_FAST                'v'
              100  JUMP_FORWARD        104  'to 104'
            102_0  COME_FROM            96  '96'
              102  LOAD_FAST                'v_str'
            104_0  COME_FROM           100  '100'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                im_info
              108  LOAD_FAST                'k'
              110  STORE_SUBSCR     

 L. 524       112  LOAD_FAST                'v_str'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                im_text
              118  LOAD_FAST                'k'
              120  STORE_SUBSCR     

 L. 525       122  LOAD_FAST                'self'
              124  LOAD_METHOD              check_text_memory
              126  LOAD_GLOBAL              len
              128  LOAD_FAST                'v_str'
              130  CALL_FUNCTION_1       1  ''
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
            136_0  COME_FROM            64  '64'

 L. 527       136  LOAD_FAST                's'
              138  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 40

    def chunk_zTXt--- This code section failed: ---

 L. 532         0  LOAD_GLOBAL              ImageFile
                2  LOAD_METHOD              _safe_read
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fp
                8  LOAD_FAST                'length'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               's'

 L. 533        14  SETUP_FINALLY        36  'to 36'

 L. 534        16  LOAD_FAST                's'
               18  LOAD_METHOD              split
               20  LOAD_CONST               b'\x00'
               22  LOAD_CONST               1
               24  CALL_METHOD_2         2  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'k'
               30  STORE_FAST               'v'
               32  POP_BLOCK        
               34  JUMP_FORWARD         62  'to 62'
             36_0  COME_FROM_FINALLY    14  '14'

 L. 535        36  DUP_TOP          
               38  LOAD_GLOBAL              ValueError
               40  <121>                60  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 536        48  LOAD_FAST                's'
               50  STORE_FAST               'k'

 L. 537        52  LOAD_CONST               b''
               54  STORE_FAST               'v'
               56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
               60  <48>             
             62_0  COME_FROM            58  '58'
             62_1  COME_FROM            34  '34'

 L. 538        62  LOAD_FAST                'v'
               64  POP_JUMP_IF_FALSE    76  'to 76'

 L. 539        66  LOAD_FAST                'v'
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  STORE_FAST               'comp_method'
               74  JUMP_FORWARD         80  'to 80'
             76_0  COME_FROM            64  '64'

 L. 541        76  LOAD_CONST               0
               78  STORE_FAST               'comp_method'
             80_0  COME_FROM            74  '74'

 L. 542        80  LOAD_FAST                'comp_method'
               82  LOAD_CONST               0
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L. 543        88  LOAD_GLOBAL              SyntaxError
               90  LOAD_STR                 'Unknown compression method '
               92  LOAD_FAST                'comp_method'
               94  FORMAT_VALUE          0  ''
               96  LOAD_STR                 ' in zTXt chunk'
               98  BUILD_STRING_3        3 
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            86  '86'

 L. 544       104  SETUP_FINALLY       126  'to 126'

 L. 545       106  LOAD_GLOBAL              _safe_zlib_decompress
              108  LOAD_FAST                'v'
              110  LOAD_CONST               1
              112  LOAD_CONST               None
              114  BUILD_SLICE_2         2 
              116  BINARY_SUBSCR    
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'v'
              122  POP_BLOCK        
              124  JUMP_FORWARD        180  'to 180'
            126_0  COME_FROM_FINALLY   104  '104'

 L. 546       126  DUP_TOP          
              128  LOAD_GLOBAL              ValueError
              130  <121>               156  ''
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L. 547       138  LOAD_GLOBAL              ImageFile
              140  LOAD_ATTR                LOAD_TRUNCATED_IMAGES
              142  POP_JUMP_IF_FALSE   150  'to 150'

 L. 548       144  LOAD_CONST               b''
              146  STORE_FAST               'v'
              148  JUMP_FORWARD        152  'to 152'
            150_0  COME_FROM           142  '142'

 L. 550       150  RAISE_VARARGS_0       0  'reraise'
            152_0  COME_FROM           148  '148'
              152  POP_EXCEPT       
              154  JUMP_FORWARD        180  'to 180'

 L. 551       156  DUP_TOP          
              158  LOAD_GLOBAL              zlib
              160  LOAD_ATTR                error
              162  <121>               178  ''
              164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          

 L. 552       170  LOAD_CONST               b''
              172  STORE_FAST               'v'
              174  POP_EXCEPT       
              176  JUMP_FORWARD        180  'to 180'
              178  <48>             
            180_0  COME_FROM           176  '176'
            180_1  COME_FROM           154  '154'
            180_2  COME_FROM           124  '124'

 L. 554       180  LOAD_FAST                'k'
              182  POP_JUMP_IF_FALSE   242  'to 242'

 L. 555       184  LOAD_FAST                'k'
              186  LOAD_METHOD              decode
              188  LOAD_STR                 'latin-1'
              190  LOAD_STR                 'strict'
              192  CALL_METHOD_2         2  ''
              194  STORE_FAST               'k'

 L. 556       196  LOAD_FAST                'v'
              198  LOAD_METHOD              decode
              200  LOAD_STR                 'latin-1'
              202  LOAD_STR                 'replace'
              204  CALL_METHOD_2         2  ''
              206  STORE_FAST               'v'

 L. 558       208  LOAD_FAST                'v'
              210  DUP_TOP          
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                im_info
              216  LOAD_FAST                'k'
              218  STORE_SUBSCR     
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                im_text
              224  LOAD_FAST                'k'
              226  STORE_SUBSCR     

 L. 559       228  LOAD_FAST                'self'
              230  LOAD_METHOD              check_text_memory
              232  LOAD_GLOBAL              len
              234  LOAD_FAST                'v'
              236  CALL_FUNCTION_1       1  ''
              238  CALL_METHOD_1         1  ''
              240  POP_TOP          
            242_0  COME_FROM           182  '182'

 L. 561       242  LOAD_FAST                's'
              244  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 40

    def chunk_iTXt--- This code section failed: ---

 L. 566         0  LOAD_GLOBAL              ImageFile
                2  LOAD_METHOD              _safe_read
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fp
                8  LOAD_FAST                'length'
               10  CALL_METHOD_2         2  ''
               12  DUP_TOP          
               14  STORE_FAST               'r'
               16  STORE_FAST               's'

 L. 567        18  SETUP_FINALLY        40  'to 40'

 L. 568        20  LOAD_FAST                'r'
               22  LOAD_METHOD              split
               24  LOAD_CONST               b'\x00'
               26  LOAD_CONST               1
               28  CALL_METHOD_2         2  ''
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'k'
               34  STORE_FAST               'r'
               36  POP_BLOCK        
               38  JUMP_FORWARD         62  'to 62'
             40_0  COME_FROM_FINALLY    18  '18'

 L. 569        40  DUP_TOP          
               42  LOAD_GLOBAL              ValueError
               44  <121>                60  ''
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 570        52  LOAD_FAST                's'
               54  ROT_FOUR         
               56  POP_EXCEPT       
               58  RETURN_VALUE     
               60  <48>             
             62_0  COME_FROM            38  '38'

 L. 571        62  LOAD_GLOBAL              len
               64  LOAD_FAST                'r'
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_CONST               2
               70  COMPARE_OP               <
               72  POP_JUMP_IF_FALSE    78  'to 78'

 L. 572        74  LOAD_FAST                's'
               76  RETURN_VALUE     
             78_0  COME_FROM            72  '72'

 L. 573        78  LOAD_FAST                'r'
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'r'
               86  LOAD_CONST               1
               88  BINARY_SUBSCR    
               90  LOAD_FAST                'r'
               92  LOAD_CONST               2
               94  LOAD_CONST               None
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  ROT_THREE        
              102  ROT_TWO          
              104  STORE_FAST               'cf'
              106  STORE_FAST               'cm'
              108  STORE_FAST               'r'

 L. 574       110  SETUP_FINALLY       134  'to 134'

 L. 575       112  LOAD_FAST                'r'
              114  LOAD_METHOD              split
              116  LOAD_CONST               b'\x00'
              118  LOAD_CONST               2
              120  CALL_METHOD_2         2  ''
              122  UNPACK_SEQUENCE_3     3 
              124  STORE_FAST               'lang'
              126  STORE_FAST               'tk'
              128  STORE_FAST               'v'
              130  POP_BLOCK        
              132  JUMP_FORWARD        156  'to 156'
            134_0  COME_FROM_FINALLY   110  '110'

 L. 576       134  DUP_TOP          
              136  LOAD_GLOBAL              ValueError
              138  <121>               154  ''
              140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L. 577       146  LOAD_FAST                's'
              148  ROT_FOUR         
              150  POP_EXCEPT       
              152  RETURN_VALUE     
              154  <48>             
            156_0  COME_FROM           132  '132'

 L. 578       156  LOAD_FAST                'cf'
              158  LOAD_CONST               0
              160  COMPARE_OP               !=
          162_164  POP_JUMP_IF_FALSE   254  'to 254'

 L. 579       166  LOAD_FAST                'cm'
              168  LOAD_CONST               0
              170  COMPARE_OP               ==
          172_174  POP_JUMP_IF_FALSE   250  'to 250'

 L. 580       176  SETUP_FINALLY       190  'to 190'

 L. 581       178  LOAD_GLOBAL              _safe_zlib_decompress
              180  LOAD_FAST                'v'
              182  CALL_FUNCTION_1       1  ''
              184  STORE_FAST               'v'
              186  POP_BLOCK        
              188  JUMP_FORWARD        248  'to 248'
            190_0  COME_FROM_FINALLY   176  '176'

 L. 582       190  DUP_TOP          
              192  LOAD_GLOBAL              ValueError
              194  <121>               222  ''
              196  POP_TOP          
              198  POP_TOP          
              200  POP_TOP          

 L. 583       202  LOAD_GLOBAL              ImageFile
              204  LOAD_ATTR                LOAD_TRUNCATED_IMAGES
              206  POP_JUMP_IF_FALSE   216  'to 216'

 L. 584       208  LOAD_FAST                's'
              210  ROT_FOUR         
              212  POP_EXCEPT       
              214  RETURN_VALUE     
            216_0  COME_FROM           206  '206'

 L. 586       216  RAISE_VARARGS_0       0  'reraise'
              218  POP_EXCEPT       
              220  JUMP_FORWARD        248  'to 248'

 L. 587       222  DUP_TOP          
              224  LOAD_GLOBAL              zlib
              226  LOAD_ATTR                error
          228_230  <121>               246  ''
              232  POP_TOP          
              234  POP_TOP          
              236  POP_TOP          

 L. 588       238  LOAD_FAST                's'
              240  ROT_FOUR         
              242  POP_EXCEPT       
              244  RETURN_VALUE     
              246  <48>             
            248_0  COME_FROM           220  '220'
            248_1  COME_FROM           188  '188'
              248  JUMP_FORWARD        254  'to 254'
            250_0  COME_FROM           172  '172'

 L. 590       250  LOAD_FAST                's'
              252  RETURN_VALUE     
            254_0  COME_FROM           248  '248'
            254_1  COME_FROM           162  '162'

 L. 591       254  SETUP_FINALLY       308  'to 308'

 L. 592       256  LOAD_FAST                'k'
              258  LOAD_METHOD              decode
              260  LOAD_STR                 'latin-1'
              262  LOAD_STR                 'strict'
              264  CALL_METHOD_2         2  ''
              266  STORE_FAST               'k'

 L. 593       268  LOAD_FAST                'lang'
              270  LOAD_METHOD              decode
              272  LOAD_STR                 'utf-8'
              274  LOAD_STR                 'strict'
              276  CALL_METHOD_2         2  ''
              278  STORE_FAST               'lang'

 L. 594       280  LOAD_FAST                'tk'
              282  LOAD_METHOD              decode
              284  LOAD_STR                 'utf-8'
              286  LOAD_STR                 'strict'
              288  CALL_METHOD_2         2  ''
              290  STORE_FAST               'tk'

 L. 595       292  LOAD_FAST                'v'
              294  LOAD_METHOD              decode
              296  LOAD_STR                 'utf-8'
              298  LOAD_STR                 'strict'
              300  CALL_METHOD_2         2  ''
              302  STORE_FAST               'v'
              304  POP_BLOCK        
              306  JUMP_FORWARD        332  'to 332'
            308_0  COME_FROM_FINALLY   254  '254'

 L. 596       308  DUP_TOP          
              310  LOAD_GLOBAL              UnicodeError
          312_314  <121>               330  ''
              316  POP_TOP          
              318  POP_TOP          
              320  POP_TOP          

 L. 597       322  LOAD_FAST                's'
              324  ROT_FOUR         
              326  POP_EXCEPT       
              328  RETURN_VALUE     
              330  <48>             
            332_0  COME_FROM           306  '306'

 L. 599       332  LOAD_GLOBAL              iTXt
              334  LOAD_FAST                'v'
              336  LOAD_FAST                'lang'
              338  LOAD_FAST                'tk'
              340  CALL_FUNCTION_3       3  ''
              342  DUP_TOP          
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                im_info
              348  LOAD_FAST                'k'
              350  STORE_SUBSCR     
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                im_text
              356  LOAD_FAST                'k'
              358  STORE_SUBSCR     

 L. 600       360  LOAD_FAST                'self'
              362  LOAD_METHOD              check_text_memory
              364  LOAD_GLOBAL              len
              366  LOAD_FAST                'v'
              368  CALL_FUNCTION_1       1  ''
              370  CALL_METHOD_1         1  ''
              372  POP_TOP          

 L. 602       374  LOAD_FAST                's'
              376  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 44

    def chunk_eXIf(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        self.im_info['exif'] = b'Exif\x00\x00' + s
        return s

    def chunk_acTL--- This code section failed: ---

 L. 611         0  LOAD_GLOBAL              ImageFile
                2  LOAD_METHOD              _safe_read
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fp
                8  LOAD_FAST                'length'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               's'

 L. 612        14  LOAD_FAST                'self'
               16  LOAD_ATTR                im_n_frames
               18  LOAD_CONST               None
               20  <117>                 1  ''
               22  POP_JUMP_IF_FALSE    44  'to 44'

 L. 613        24  LOAD_CONST               None
               26  LOAD_FAST                'self'
               28  STORE_ATTR               im_n_frames

 L. 614        30  LOAD_GLOBAL              warnings
               32  LOAD_METHOD              warn
               34  LOAD_STR                 'Invalid APNG, will use default PNG image if possible'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 615        40  LOAD_FAST                's'
               42  RETURN_VALUE     
             44_0  COME_FROM            22  '22'

 L. 616        44  LOAD_GLOBAL              i32
               46  LOAD_FAST                's'
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'n_frames'

 L. 617        52  LOAD_FAST                'n_frames'
               54  LOAD_CONST               0
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_TRUE     68  'to 68'
               60  LOAD_FAST                'n_frames'
               62  LOAD_CONST               2147483648
               64  COMPARE_OP               >
               66  POP_JUMP_IF_FALSE    82  'to 82'
             68_0  COME_FROM            58  '58'

 L. 618        68  LOAD_GLOBAL              warnings
               70  LOAD_METHOD              warn
               72  LOAD_STR                 'Invalid APNG, will use default PNG image if possible'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L. 619        78  LOAD_FAST                's'
               80  RETURN_VALUE     
             82_0  COME_FROM            66  '66'

 L. 620        82  LOAD_FAST                'n_frames'
               84  LOAD_FAST                'self'
               86  STORE_ATTR               im_n_frames

 L. 621        88  LOAD_GLOBAL              i32
               90  LOAD_FAST                's'
               92  LOAD_CONST               4
               94  CALL_FUNCTION_2       2  ''
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                im_info
              100  LOAD_STR                 'loop'
              102  STORE_SUBSCR     

 L. 622       104  LOAD_STR                 'image/apng'
              106  LOAD_FAST                'self'
              108  STORE_ATTR               im_custom_mimetype

 L. 623       110  LOAD_FAST                's'
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 20

    def chunk_fcTL--- This code section failed: ---

 L. 626         0  LOAD_GLOBAL              ImageFile
                2  LOAD_METHOD              _safe_read
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fp
                8  LOAD_FAST                'length'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               's'

 L. 627        14  LOAD_GLOBAL              i32
               16  LOAD_FAST                's'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'seq'

 L. 628        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _seq_num
               26  LOAD_CONST               None
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    40  'to 40'
               32  LOAD_FAST                'seq'
               34  LOAD_CONST               0
               36  COMPARE_OP               !=
               38  POP_JUMP_IF_TRUE     64  'to 64'
             40_0  COME_FROM            30  '30'

 L. 629        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _seq_num
               44  LOAD_CONST               None
               46  <117>                 1  ''

 L. 628        48  POP_JUMP_IF_FALSE    72  'to 72'

 L. 629        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _seq_num
               54  LOAD_FAST                'seq'
               56  LOAD_CONST               1
               58  BINARY_SUBTRACT  
               60  COMPARE_OP               !=

 L. 628        62  POP_JUMP_IF_FALSE    72  'to 72'
             64_0  COME_FROM            38  '38'

 L. 631        64  LOAD_GLOBAL              SyntaxError
               66  LOAD_STR                 'APNG contains frame sequence errors'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'
             72_1  COME_FROM            48  '48'

 L. 632        72  LOAD_FAST                'seq'
               74  LOAD_FAST                'self'
               76  STORE_ATTR               _seq_num

 L. 633        78  LOAD_GLOBAL              i32
               80  LOAD_FAST                's'
               82  LOAD_CONST               4
               84  CALL_FUNCTION_2       2  ''
               86  LOAD_GLOBAL              i32
               88  LOAD_FAST                's'
               90  LOAD_CONST               8
               92  CALL_FUNCTION_2       2  ''
               94  ROT_TWO          
               96  STORE_FAST               'width'
               98  STORE_FAST               'height'

 L. 634       100  LOAD_GLOBAL              i32
              102  LOAD_FAST                's'
              104  LOAD_CONST               12
              106  CALL_FUNCTION_2       2  ''
              108  LOAD_GLOBAL              i32
              110  LOAD_FAST                's'
              112  LOAD_CONST               16
              114  CALL_FUNCTION_2       2  ''
              116  ROT_TWO          
              118  STORE_FAST               'px'
              120  STORE_FAST               'py'

 L. 635       122  LOAD_FAST                'self'
              124  LOAD_ATTR                im_size
              126  UNPACK_SEQUENCE_2     2 
              128  STORE_FAST               'im_w'
              130  STORE_FAST               'im_h'

 L. 636       132  LOAD_FAST                'px'
              134  LOAD_FAST                'width'
              136  BINARY_ADD       
              138  LOAD_FAST                'im_w'
              140  COMPARE_OP               >
              142  POP_JUMP_IF_TRUE    156  'to 156'
              144  LOAD_FAST                'py'
              146  LOAD_FAST                'height'
              148  BINARY_ADD       
              150  LOAD_FAST                'im_h'
              152  COMPARE_OP               >
              154  POP_JUMP_IF_FALSE   164  'to 164'
            156_0  COME_FROM           142  '142'

 L. 637       156  LOAD_GLOBAL              SyntaxError
              158  LOAD_STR                 'APNG contains invalid frames'
              160  CALL_FUNCTION_1       1  ''
              162  RAISE_VARARGS_1       1  'exception instance'
            164_0  COME_FROM           154  '154'

 L. 638       164  LOAD_FAST                'px'
              166  LOAD_FAST                'py'
              168  LOAD_FAST                'px'
              170  LOAD_FAST                'width'
              172  BINARY_ADD       
              174  LOAD_FAST                'py'
              176  LOAD_FAST                'height'
              178  BINARY_ADD       
              180  BUILD_TUPLE_4         4 
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                im_info
              186  LOAD_STR                 'bbox'
              188  STORE_SUBSCR     

 L. 639       190  LOAD_GLOBAL              i16
              192  LOAD_FAST                's'
              194  LOAD_CONST               20
              196  CALL_FUNCTION_2       2  ''
              198  LOAD_GLOBAL              i16
              200  LOAD_FAST                's'
              202  LOAD_CONST               22
              204  CALL_FUNCTION_2       2  ''
              206  ROT_TWO          
              208  STORE_FAST               'delay_num'
              210  STORE_FAST               'delay_den'

 L. 640       212  LOAD_FAST                'delay_den'
              214  LOAD_CONST               0
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_FALSE   224  'to 224'

 L. 641       220  LOAD_CONST               100
              222  STORE_FAST               'delay_den'
            224_0  COME_FROM           218  '218'

 L. 642       224  LOAD_GLOBAL              float
              226  LOAD_FAST                'delay_num'
              228  CALL_FUNCTION_1       1  ''
              230  LOAD_GLOBAL              float
              232  LOAD_FAST                'delay_den'
              234  CALL_FUNCTION_1       1  ''
              236  BINARY_TRUE_DIVIDE
              238  LOAD_CONST               1000
              240  BINARY_MULTIPLY  
              242  LOAD_FAST                'self'
              244  LOAD_ATTR                im_info
              246  LOAD_STR                 'duration'
              248  STORE_SUBSCR     

 L. 643       250  LOAD_FAST                's'
              252  LOAD_CONST               24
              254  BINARY_SUBSCR    
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                im_info
              260  LOAD_STR                 'disposal'
              262  STORE_SUBSCR     

 L. 644       264  LOAD_FAST                's'
              266  LOAD_CONST               25
              268  BINARY_SUBSCR    
              270  LOAD_FAST                'self'
              272  LOAD_ATTR                im_info
              274  LOAD_STR                 'blend'
              276  STORE_SUBSCR     

 L. 645       278  LOAD_FAST                's'
              280  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 28

    def chunk_fdAT(self, pos, length):
        s = ImageFile._safe_read(self.fp, 4)
        seq = i32(s)
        if self._seq_num != seq - 1:
            raise SyntaxError('APNG contains frame sequence errors')
        self._seq_num = seq
        return self.chunk_IDAT(pos + 4, length - 4)


def _accept(prefix):
    return prefix[:8] == _MAGIC


class PngImageFile(ImageFile.ImageFile):
    format = 'PNG'
    format_description = 'Portable network graphics'

    def _open--- This code section failed: ---

 L. 675         0  LOAD_GLOBAL              _accept
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                fp
                6  LOAD_METHOD              read
                8  LOAD_CONST               8
               10  CALL_METHOD_1         1  ''
               12  CALL_FUNCTION_1       1  ''
               14  POP_JUMP_IF_TRUE     24  'to 24'

 L. 676        16  LOAD_GLOBAL              SyntaxError
               18  LOAD_STR                 'not a PNG file'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L. 677        24  LOAD_FAST                'self'
               26  LOAD_ATTR                fp
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _PngImageFile__fp

 L. 678        32  LOAD_CONST               0
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _PngImageFile__frame

 L. 683        38  BUILD_LIST_0          0 
               40  LOAD_FAST                'self'
               42  STORE_ATTR               private_chunks

 L. 684        44  LOAD_GLOBAL              PngStream
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                fp
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_FAST                'self'
               54  STORE_ATTR               png

 L. 691        56  LOAD_FAST                'self'
               58  LOAD_ATTR                png
               60  LOAD_METHOD              read
               62  CALL_METHOD_0         0  ''
               64  UNPACK_SEQUENCE_3     3 
               66  STORE_FAST               'cid'
               68  STORE_FAST               'pos'
               70  STORE_FAST               'length'

 L. 693        72  SETUP_FINALLY        94  'to 94'

 L. 694        74  LOAD_FAST                'self'
               76  LOAD_ATTR                png
               78  LOAD_METHOD              call
               80  LOAD_FAST                'cid'
               82  LOAD_FAST                'pos'
               84  LOAD_FAST                'length'
               86  CALL_METHOD_3         3  ''
               88  STORE_FAST               's'
               90  POP_BLOCK        
               92  JUMP_FORWARD        194  'to 194'
             94_0  COME_FROM_FINALLY    72  '72'

 L. 695        94  DUP_TOP          
               96  LOAD_GLOBAL              EOFError
               98  <121>               114  ''
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 696       106  POP_EXCEPT       
              108  BREAK_LOOP          210  'to 210'
              110  POP_EXCEPT       
              112  JUMP_FORWARD        194  'to 194'

 L. 697       114  DUP_TOP          
              116  LOAD_GLOBAL              AttributeError
              118  <121>               192  ''
              120  POP_TOP          
              122  POP_TOP          
              124  POP_TOP          

 L. 698       126  LOAD_GLOBAL              logger
              128  LOAD_METHOD              debug
              130  LOAD_STR                 '%r %s %s (unknown)'
              132  LOAD_FAST                'cid'
              134  LOAD_FAST                'pos'
              136  LOAD_FAST                'length'
              138  CALL_METHOD_4         4  ''
              140  POP_TOP          

 L. 699       142  LOAD_GLOBAL              ImageFile
              144  LOAD_METHOD              _safe_read
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                fp
              150  LOAD_FAST                'length'
              152  CALL_METHOD_2         2  ''
              154  STORE_FAST               's'

 L. 700       156  LOAD_FAST                'cid'
              158  LOAD_CONST               1
              160  LOAD_CONST               2
              162  BUILD_SLICE_2         2 
              164  BINARY_SUBSCR    
              166  LOAD_METHOD              islower
              168  CALL_METHOD_0         0  ''
              170  POP_JUMP_IF_FALSE   188  'to 188'

 L. 701       172  LOAD_FAST                'self'
              174  LOAD_ATTR                private_chunks
              176  LOAD_METHOD              append
              178  LOAD_FAST                'cid'
              180  LOAD_FAST                's'
              182  BUILD_TUPLE_2         2 
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
            188_0  COME_FROM           170  '170'
              188  POP_EXCEPT       
              190  JUMP_FORWARD        194  'to 194'
              192  <48>             
            194_0  COME_FROM           190  '190'
            194_1  COME_FROM           112  '112'
            194_2  COME_FROM            92  '92'

 L. 703       194  LOAD_FAST                'self'
              196  LOAD_ATTR                png
              198  LOAD_METHOD              crc
              200  LOAD_FAST                'cid'
              202  LOAD_FAST                's'
              204  CALL_METHOD_2         2  ''
              206  POP_TOP          
              208  JUMP_BACK            56  'to 56'
            210_0  COME_FROM_EXCEPT_CLAUSE   108  '108'

 L. 712       210  LOAD_FAST                'self'
              212  LOAD_ATTR                png
              214  LOAD_ATTR                im_mode
              216  LOAD_FAST                'self'
              218  STORE_ATTR               mode

 L. 713       220  LOAD_FAST                'self'
              222  LOAD_ATTR                png
              224  LOAD_ATTR                im_size
              226  LOAD_FAST                'self'
              228  STORE_ATTR               _size

 L. 714       230  LOAD_FAST                'self'
              232  LOAD_ATTR                png
              234  LOAD_ATTR                im_info
              236  LOAD_FAST                'self'
              238  STORE_ATTR               info

 L. 715       240  LOAD_CONST               None
              242  LOAD_FAST                'self'
              244  STORE_ATTR               _text

 L. 716       246  LOAD_FAST                'self'
              248  LOAD_ATTR                png
              250  LOAD_ATTR                im_tile
              252  LOAD_FAST                'self'
              254  STORE_ATTR               tile

 L. 717       256  LOAD_FAST                'self'
              258  LOAD_ATTR                png
              260  LOAD_ATTR                im_custom_mimetype
              262  LOAD_FAST                'self'
              264  STORE_ATTR               custom_mimetype

 L. 718       266  LOAD_FAST                'self'
              268  LOAD_ATTR                png
              270  LOAD_ATTR                im_n_frames
          272_274  JUMP_IF_TRUE_OR_POP   278  'to 278'
              276  LOAD_CONST               1
            278_0  COME_FROM           272  '272'
              278  LOAD_FAST                'self'
              280  STORE_ATTR               n_frames

 L. 719       282  LOAD_FAST                'self'
              284  LOAD_ATTR                info
              286  LOAD_METHOD              get
              288  LOAD_STR                 'default_image'
              290  LOAD_CONST               False
              292  CALL_METHOD_2         2  ''
              294  LOAD_FAST                'self'
              296  STORE_ATTR               default_image

 L. 721       298  LOAD_FAST                'self'
              300  LOAD_ATTR                png
              302  LOAD_ATTR                im_palette
          304_306  POP_JUMP_IF_FALSE   334  'to 334'

 L. 722       308  LOAD_FAST                'self'
              310  LOAD_ATTR                png
              312  LOAD_ATTR                im_palette
              314  UNPACK_SEQUENCE_2     2 
              316  STORE_FAST               'rawmode'
              318  STORE_FAST               'data'

 L. 723       320  LOAD_GLOBAL              ImagePalette
              322  LOAD_METHOD              raw
              324  LOAD_FAST                'rawmode'
              326  LOAD_FAST                'data'
              328  CALL_METHOD_2         2  ''
              330  LOAD_FAST                'self'
              332  STORE_ATTR               palette
            334_0  COME_FROM           304  '304'

 L. 725       334  LOAD_FAST                'cid'
              336  LOAD_CONST               b'fdAT'
              338  COMPARE_OP               ==
          340_342  POP_JUMP_IF_FALSE   356  'to 356'

 L. 726       344  LOAD_FAST                'length'
              346  LOAD_CONST               4
              348  BINARY_SUBTRACT  
              350  LOAD_FAST                'self'
              352  STORE_ATTR               _PngImageFile__prepare_idat
              354  JUMP_FORWARD        362  'to 362'
            356_0  COME_FROM           340  '340'

 L. 728       356  LOAD_FAST                'length'
              358  LOAD_FAST                'self'
              360  STORE_ATTR               _PngImageFile__prepare_idat
            362_0  COME_FROM           354  '354'

 L. 730       362  LOAD_FAST                'self'
              364  LOAD_ATTR                png
              366  LOAD_ATTR                im_n_frames
              368  LOAD_CONST               None
              370  <117>                 1  ''
          372_374  POP_JUMP_IF_FALSE   444  'to 444'

 L. 731       376  LOAD_CONST               False
              378  LOAD_FAST                'self'
              380  STORE_ATTR               _close_exclusive_fp_after_loading

 L. 732       382  LOAD_FAST                'self'
              384  LOAD_ATTR                png
              386  LOAD_METHOD              save_rewind
              388  CALL_METHOD_0         0  ''
              390  POP_TOP          

 L. 733       392  LOAD_FAST                'self'
              394  LOAD_ATTR                _PngImageFile__prepare_idat
              396  LOAD_FAST                'self'
              398  STORE_ATTR               _PngImageFile__rewind_idat

 L. 734       400  LOAD_FAST                'self'
              402  LOAD_ATTR                _PngImageFile__fp
              404  LOAD_METHOD              tell
              406  CALL_METHOD_0         0  ''
              408  LOAD_FAST                'self'
              410  STORE_ATTR               _PngImageFile__rewind

 L. 735       412  LOAD_FAST                'self'
              414  LOAD_ATTR                default_image
          416_418  POP_JUMP_IF_FALSE   434  'to 434'

 L. 737       420  LOAD_FAST                'self'
              422  DUP_TOP          
              424  LOAD_ATTR                n_frames
              426  LOAD_CONST               1
              428  INPLACE_ADD      
              430  ROT_TWO          
              432  STORE_ATTR               n_frames
            434_0  COME_FROM           416  '416'

 L. 738       434  LOAD_FAST                'self'
              436  LOAD_METHOD              _seek
              438  LOAD_CONST               0
              440  CALL_METHOD_1         1  ''
              442  POP_TOP          
            444_0  COME_FROM           372  '372'

 L. 739       444  LOAD_FAST                'self'
              446  LOAD_ATTR                n_frames
              448  LOAD_CONST               1
              450  COMPARE_OP               >
              452  LOAD_FAST                'self'
              454  STORE_ATTR               is_animated

Parse error at or near `<121>' instruction at offset 98

    @property
    def text--- This code section failed: ---

 L. 744         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _text
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    62  'to 62'

 L. 747        10  LOAD_FAST                'self'
               12  LOAD_ATTR                is_animated
               14  POP_JUMP_IF_FALSE    38  'to 38'

 L. 748        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _PngImageFile__frame
               20  STORE_FAST               'frame'

 L. 750        22  LOAD_FAST                'self'
               24  LOAD_METHOD              seek
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                n_frames
               30  LOAD_CONST               1
               32  BINARY_SUBTRACT  
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          
             38_0  COME_FROM            14  '14'

 L. 751        38  LOAD_FAST                'self'
               40  LOAD_METHOD              load
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          

 L. 752        46  LOAD_FAST                'self'
               48  LOAD_ATTR                is_animated
               50  POP_JUMP_IF_FALSE    62  'to 62'

 L. 753        52  LOAD_FAST                'self'
               54  LOAD_METHOD              seek
               56  LOAD_FAST                'frame'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
             62_0  COME_FROM            50  '50'
             62_1  COME_FROM             8  '8'

 L. 754        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _text
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def verify--- This code section failed: ---

 L. 759         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 760        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'verify must be called directly after open'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 763        18  LOAD_FAST                'self'
               20  LOAD_ATTR                fp
               22  LOAD_METHOD              seek
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                tile
               28  LOAD_CONST               0
               30  BINARY_SUBSCR    
               32  LOAD_CONST               2
               34  BINARY_SUBSCR    
               36  LOAD_CONST               8
               38  BINARY_SUBTRACT  
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 765        44  LOAD_FAST                'self'
               46  LOAD_ATTR                png
               48  LOAD_METHOD              verify
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          

 L. 766        54  LOAD_FAST                'self'
               56  LOAD_ATTR                png
               58  LOAD_METHOD              close
               60  CALL_METHOD_0         0  ''
               62  POP_TOP          

 L. 768        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _exclusive_fp
               68  POP_JUMP_IF_FALSE    80  'to 80'

 L. 769        70  LOAD_FAST                'self'
               72  LOAD_ATTR                fp
               74  LOAD_METHOD              close
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          
             80_0  COME_FROM            68  '68'

 L. 770        80  LOAD_CONST               None
               82  LOAD_FAST                'self'
               84  STORE_ATTR               fp

Parse error at or near `None' instruction at offset -1

    def seek--- This code section failed: ---

 L. 773         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _seek_check
                4  LOAD_FAST                'frame'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L. 774        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 775        14  LOAD_FAST                'frame'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _PngImageFile__frame
               20  COMPARE_OP               <
               22  POP_JUMP_IF_FALSE    36  'to 36'

 L. 776        24  LOAD_FAST                'self'
               26  LOAD_METHOD              _seek
               28  LOAD_CONST               0
               30  LOAD_CONST               True
               32  CALL_METHOD_2         2  ''
               34  POP_TOP          
             36_0  COME_FROM            22  '22'

 L. 778        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _PngImageFile__frame
               40  STORE_FAST               'last_frame'

 L. 779        42  LOAD_GLOBAL              range
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _PngImageFile__frame
               48  LOAD_CONST               1
               50  BINARY_ADD       
               52  LOAD_FAST                'frame'
               54  LOAD_CONST               1
               56  BINARY_ADD       
               58  CALL_FUNCTION_2       2  ''
               60  GET_ITER         
               62  FOR_ITER            140  'to 140'
               64  STORE_FAST               'f'

 L. 780        66  SETUP_FINALLY        82  'to 82'

 L. 781        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _seek
               72  LOAD_FAST                'f'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          
               78  POP_BLOCK        
               80  JUMP_BACK            62  'to 62'
             82_0  COME_FROM_FINALLY    66  '66'

 L. 782        82  DUP_TOP          
               84  LOAD_GLOBAL              EOFError
               86  <121>               136  ''
               88  POP_TOP          
               90  STORE_FAST               'e'
               92  POP_TOP          
               94  SETUP_FINALLY       128  'to 128'

 L. 783        96  LOAD_FAST                'self'
               98  LOAD_METHOD              seek
              100  LOAD_FAST                'last_frame'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L. 784       106  LOAD_GLOBAL              EOFError
              108  LOAD_STR                 'no more images in APNG file'
              110  CALL_FUNCTION_1       1  ''
              112  LOAD_FAST                'e'
              114  RAISE_VARARGS_2       2  'exception instance with __cause__'
              116  POP_BLOCK        
              118  POP_EXCEPT       
              120  LOAD_CONST               None
              122  STORE_FAST               'e'
              124  DELETE_FAST              'e'
              126  JUMP_BACK            62  'to 62'
            128_0  COME_FROM_FINALLY    94  '94'
              128  LOAD_CONST               None
              130  STORE_FAST               'e'
              132  DELETE_FAST              'e'
              134  <48>             
              136  <48>             
              138  JUMP_BACK            62  'to 62'

Parse error at or near `<121>' instruction at offset 86

    def _seek--- This code section failed: ---

 L. 787         0  LOAD_FAST                'frame'
                2  LOAD_CONST               0
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE   170  'to 170'

 L. 788         8  LOAD_FAST                'rewind'
               10  POP_JUMP_IF_FALSE    90  'to 90'

 L. 789        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _PngImageFile__fp
               16  LOAD_METHOD              seek
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _PngImageFile__rewind
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          

 L. 790        26  LOAD_FAST                'self'
               28  LOAD_ATTR                png
               30  LOAD_METHOD              rewind
               32  CALL_METHOD_0         0  ''
               34  POP_TOP          

 L. 791        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _PngImageFile__rewind_idat
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _PngImageFile__prepare_idat

 L. 792        44  LOAD_CONST               None
               46  LOAD_FAST                'self'
               48  STORE_ATTR               im

 L. 793        50  LOAD_FAST                'self'
               52  LOAD_ATTR                pyaccess
               54  POP_JUMP_IF_FALSE    62  'to 62'

 L. 794        56  LOAD_CONST               None
               58  LOAD_FAST                'self'
               60  STORE_ATTR               pyaccess
             62_0  COME_FROM            54  '54'

 L. 795        62  LOAD_FAST                'self'
               64  LOAD_ATTR                png
               66  LOAD_ATTR                im_info
               68  LOAD_FAST                'self'
               70  STORE_ATTR               info

 L. 796        72  LOAD_FAST                'self'
               74  LOAD_ATTR                png
               76  LOAD_ATTR                im_tile
               78  LOAD_FAST                'self'
               80  STORE_ATTR               tile

 L. 797        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _PngImageFile__fp
               86  LOAD_FAST                'self'
               88  STORE_ATTR               fp
             90_0  COME_FROM            10  '10'

 L. 798        90  LOAD_CONST               None
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _prev_im

 L. 799        96  LOAD_CONST               None
               98  LOAD_FAST                'self'
              100  STORE_ATTR               dispose

 L. 800       102  LOAD_FAST                'self'
              104  LOAD_ATTR                info
              106  LOAD_METHOD              get
              108  LOAD_STR                 'default_image'
              110  LOAD_CONST               False
              112  CALL_METHOD_2         2  ''
              114  LOAD_FAST                'self'
              116  STORE_ATTR               default_image

 L. 801       118  LOAD_FAST                'self'
              120  LOAD_ATTR                info
              122  LOAD_METHOD              get
              124  LOAD_STR                 'disposal'
              126  CALL_METHOD_1         1  ''
              128  LOAD_FAST                'self'
              130  STORE_ATTR               dispose_op

 L. 802       132  LOAD_FAST                'self'
              134  LOAD_ATTR                info
              136  LOAD_METHOD              get
              138  LOAD_STR                 'blend'
              140  CALL_METHOD_1         1  ''
              142  LOAD_FAST                'self'
              144  STORE_ATTR               blend_op

 L. 803       146  LOAD_FAST                'self'
              148  LOAD_ATTR                info
              150  LOAD_METHOD              get
              152  LOAD_STR                 'bbox'
              154  CALL_METHOD_1         1  ''
              156  LOAD_FAST                'self'
              158  STORE_ATTR               dispose_extent

 L. 804       160  LOAD_CONST               0
              162  LOAD_FAST                'self'
              164  STORE_ATTR               _PngImageFile__frame
          166_168  JUMP_FORWARD        634  'to 634'
            170_0  COME_FROM             6  '6'

 L. 806       170  LOAD_FAST                'frame'
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                _PngImageFile__frame
              176  LOAD_CONST               1
              178  BINARY_ADD       
              180  COMPARE_OP               !=
              182  POP_JUMP_IF_FALSE   198  'to 198'

 L. 807       184  LOAD_GLOBAL              ValueError
              186  LOAD_STR                 'cannot seek to frame '
              188  LOAD_FAST                'frame'
              190  FORMAT_VALUE          0  ''
              192  BUILD_STRING_2        2 
              194  CALL_FUNCTION_1       1  ''
              196  RAISE_VARARGS_1       1  'exception instance'
            198_0  COME_FROM           182  '182'

 L. 810       198  LOAD_FAST                'self'
              200  LOAD_METHOD              load
              202  CALL_METHOD_0         0  ''
              204  POP_TOP          

 L. 812       206  LOAD_FAST                'self'
              208  LOAD_ATTR                dispose
              210  POP_JUMP_IF_FALSE   230  'to 230'

 L. 813       212  LOAD_FAST                'self'
              214  LOAD_ATTR                im
              216  LOAD_METHOD              paste
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                dispose
              222  LOAD_FAST                'self'
              224  LOAD_ATTR                dispose_extent
              226  CALL_METHOD_2         2  ''
              228  POP_TOP          
            230_0  COME_FROM           210  '210'

 L. 814       230  LOAD_FAST                'self'
              232  LOAD_ATTR                im
              234  LOAD_METHOD              copy
              236  CALL_METHOD_0         0  ''
              238  LOAD_FAST                'self'
              240  STORE_ATTR               _prev_im

 L. 816       242  LOAD_FAST                'self'
              244  LOAD_ATTR                _PngImageFile__fp
              246  LOAD_FAST                'self'
              248  STORE_ATTR               fp

 L. 819       250  LOAD_FAST                'self'
              252  LOAD_ATTR                _PngImageFile__prepare_idat
          254_256  POP_JUMP_IF_FALSE   280  'to 280'

 L. 820       258  LOAD_GLOBAL              ImageFile
              260  LOAD_METHOD              _safe_read
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                fp
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                _PngImageFile__prepare_idat
              270  CALL_METHOD_2         2  ''
              272  POP_TOP          

 L. 821       274  LOAD_CONST               0
              276  LOAD_FAST                'self'
              278  STORE_ATTR               _PngImageFile__prepare_idat
            280_0  COME_FROM           254  '254'

 L. 822       280  LOAD_CONST               False
              282  STORE_FAST               'frame_start'

 L. 824       284  LOAD_FAST                'self'
              286  LOAD_ATTR                fp
              288  LOAD_METHOD              read
              290  LOAD_CONST               4
              292  CALL_METHOD_1         1  ''
              294  POP_TOP          

 L. 826       296  SETUP_FINALLY       318  'to 318'

 L. 827       298  LOAD_FAST                'self'
              300  LOAD_ATTR                png
              302  LOAD_METHOD              read
              304  CALL_METHOD_0         0  ''
              306  UNPACK_SEQUENCE_3     3 
              308  STORE_FAST               'cid'
              310  STORE_FAST               'pos'
              312  STORE_FAST               'length'
              314  POP_BLOCK        
              316  JUMP_FORWARD        350  'to 350'
            318_0  COME_FROM_FINALLY   296  '296'

 L. 828       318  DUP_TOP          
              320  LOAD_GLOBAL              struct
              322  LOAD_ATTR                error
              324  LOAD_GLOBAL              SyntaxError
              326  BUILD_TUPLE_2         2 
          328_330  <121>               348  ''
              332  POP_TOP          
              334  POP_TOP          
              336  POP_TOP          

 L. 829       338  POP_EXCEPT       
          340_342  BREAK_LOOP          564  'to 564'
              344  POP_EXCEPT       
              346  JUMP_FORWARD        350  'to 350'
              348  <48>             
            350_0  COME_FROM           346  '346'
            350_1  COME_FROM           316  '316'

 L. 831       350  LOAD_FAST                'cid'
              352  LOAD_CONST               b'IEND'
              354  COMPARE_OP               ==
          356_358  POP_JUMP_IF_FALSE   368  'to 368'

 L. 832       360  LOAD_GLOBAL              EOFError
              362  LOAD_STR                 'No more images in APNG file'
              364  CALL_FUNCTION_1       1  ''
              366  RAISE_VARARGS_1       1  'exception instance'
            368_0  COME_FROM           356  '356'

 L. 833       368  LOAD_FAST                'cid'
              370  LOAD_CONST               b'fcTL'
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   396  'to 396'

 L. 834       378  LOAD_FAST                'frame_start'
          380_382  POP_JUMP_IF_FALSE   392  'to 392'

 L. 836       384  LOAD_GLOBAL              SyntaxError
              386  LOAD_STR                 'APNG missing frame data'
              388  CALL_FUNCTION_1       1  ''
              390  RAISE_VARARGS_1       1  'exception instance'
            392_0  COME_FROM           380  '380'

 L. 837       392  LOAD_CONST               True
              394  STORE_FAST               'frame_start'
            396_0  COME_FROM           374  '374'

 L. 839       396  SETUP_FINALLY       418  'to 418'

 L. 840       398  LOAD_FAST                'self'
              400  LOAD_ATTR                png
              402  LOAD_METHOD              call
              404  LOAD_FAST                'cid'
              406  LOAD_FAST                'pos'
              408  LOAD_FAST                'length'
              410  CALL_METHOD_3         3  ''
              412  POP_TOP          
              414  POP_BLOCK        
              416  JUMP_BACK           284  'to 284'
            418_0  COME_FROM_FINALLY   396  '396'

 L. 841       418  DUP_TOP          
              420  LOAD_GLOBAL              UnicodeDecodeError
          422_424  <121>               442  ''
              426  POP_TOP          
              428  POP_TOP          
              430  POP_TOP          

 L. 842       432  POP_EXCEPT       
          434_436  BREAK_LOOP          564  'to 564'
              438  POP_EXCEPT       
              440  JUMP_BACK           284  'to 284'

 L. 843       442  DUP_TOP          
              444  LOAD_GLOBAL              EOFError
          446_448  <121>               510  ''
              450  POP_TOP          
              452  POP_TOP          
              454  POP_TOP          

 L. 844       456  LOAD_FAST                'cid'
              458  LOAD_CONST               b'fdAT'
              460  COMPARE_OP               ==
          462_464  POP_JUMP_IF_FALSE   492  'to 492'

 L. 845       466  LOAD_FAST                'length'
              468  LOAD_CONST               4
              470  INPLACE_SUBTRACT 
              472  STORE_FAST               'length'

 L. 846       474  LOAD_FAST                'frame_start'
          476_478  POP_JUMP_IF_FALSE   492  'to 492'

 L. 847       480  LOAD_FAST                'length'
              482  LOAD_FAST                'self'
              484  STORE_ATTR               _PngImageFile__prepare_idat

 L. 848       486  POP_EXCEPT       
          488_490  BREAK_LOOP          564  'to 564'
            492_0  COME_FROM           476  '476'
            492_1  COME_FROM           462  '462'

 L. 849       492  LOAD_GLOBAL              ImageFile
              494  LOAD_METHOD              _safe_read
              496  LOAD_FAST                'self'
              498  LOAD_ATTR                fp
              500  LOAD_FAST                'length'
              502  CALL_METHOD_2         2  ''
              504  POP_TOP          
              506  POP_EXCEPT       
              508  JUMP_BACK           284  'to 284'

 L. 850       510  DUP_TOP          
              512  LOAD_GLOBAL              AttributeError
          514_516  <121>               558  ''
              518  POP_TOP          
              520  POP_TOP          
              522  POP_TOP          

 L. 851       524  LOAD_GLOBAL              logger
              526  LOAD_METHOD              debug
              528  LOAD_STR                 '%r %s %s (unknown)'
              530  LOAD_FAST                'cid'
              532  LOAD_FAST                'pos'
              534  LOAD_FAST                'length'
              536  CALL_METHOD_4         4  ''
              538  POP_TOP          

 L. 852       540  LOAD_GLOBAL              ImageFile
              542  LOAD_METHOD              _safe_read
              544  LOAD_FAST                'self'
              546  LOAD_ATTR                fp
              548  LOAD_FAST                'length'
              550  CALL_METHOD_2         2  ''
              552  POP_TOP          
              554  POP_EXCEPT       
              556  JUMP_BACK           284  'to 284'
              558  <48>             
          560_562  JUMP_BACK           284  'to 284'

 L. 854       564  LOAD_FAST                'frame'
              566  LOAD_FAST                'self'
              568  STORE_ATTR               _PngImageFile__frame

 L. 855       570  LOAD_FAST                'self'
              572  LOAD_ATTR                png
              574  LOAD_ATTR                im_tile
              576  LOAD_FAST                'self'
              578  STORE_ATTR               tile

 L. 856       580  LOAD_FAST                'self'
              582  LOAD_ATTR                info
              584  LOAD_METHOD              get
              586  LOAD_STR                 'disposal'
              588  CALL_METHOD_1         1  ''
              590  LOAD_FAST                'self'
              592  STORE_ATTR               dispose_op

 L. 857       594  LOAD_FAST                'self'
              596  LOAD_ATTR                info
              598  LOAD_METHOD              get
              600  LOAD_STR                 'blend'
              602  CALL_METHOD_1         1  ''
              604  LOAD_FAST                'self'
              606  STORE_ATTR               blend_op

 L. 858       608  LOAD_FAST                'self'
              610  LOAD_ATTR                info
              612  LOAD_METHOD              get
              614  LOAD_STR                 'bbox'
              616  CALL_METHOD_1         1  ''
              618  LOAD_FAST                'self'
              620  STORE_ATTR               dispose_extent

 L. 860       622  LOAD_FAST                'self'
              624  LOAD_ATTR                tile
          626_628  POP_JUMP_IF_TRUE    634  'to 634'

 L. 861       630  LOAD_GLOBAL              EOFError
              632  RAISE_VARARGS_1       1  'exception instance'
            634_0  COME_FROM           626  '626'
            634_1  COME_FROM           166  '166'

 L. 864       634  LOAD_FAST                'self'
              636  LOAD_ATTR                _prev_im
              638  LOAD_CONST               None
              640  <117>                 0  ''
          642_644  POP_JUMP_IF_FALSE   664  'to 664'
              646  LOAD_FAST                'self'
              648  LOAD_ATTR                dispose_op
              650  LOAD_GLOBAL              APNG_DISPOSE_OP_PREVIOUS
              652  COMPARE_OP               ==
          654_656  POP_JUMP_IF_FALSE   664  'to 664'

 L. 865       658  LOAD_GLOBAL              APNG_DISPOSE_OP_BACKGROUND
              660  LOAD_FAST                'self'
              662  STORE_ATTR               dispose_op
            664_0  COME_FROM           654  '654'
            664_1  COME_FROM           642  '642'

 L. 867       664  LOAD_FAST                'self'
              666  LOAD_ATTR                dispose_op
              668  LOAD_GLOBAL              APNG_DISPOSE_OP_PREVIOUS
              670  COMPARE_OP               ==
          672_674  POP_JUMP_IF_FALSE   708  'to 708'

 L. 868       676  LOAD_FAST                'self'
              678  LOAD_ATTR                _prev_im
              680  LOAD_METHOD              copy
              682  CALL_METHOD_0         0  ''
              684  LOAD_FAST                'self'
              686  STORE_ATTR               dispose

 L. 869       688  LOAD_FAST                'self'
              690  LOAD_METHOD              _crop
              692  LOAD_FAST                'self'
              694  LOAD_ATTR                dispose
              696  LOAD_FAST                'self'
              698  LOAD_ATTR                dispose_extent
              700  CALL_METHOD_2         2  ''
              702  LOAD_FAST                'self'
              704  STORE_ATTR               dispose
              706  JUMP_FORWARD        766  'to 766'
            708_0  COME_FROM           672  '672'

 L. 870       708  LOAD_FAST                'self'
              710  LOAD_ATTR                dispose_op
              712  LOAD_GLOBAL              APNG_DISPOSE_OP_BACKGROUND
              714  COMPARE_OP               ==
          716_718  POP_JUMP_IF_FALSE   760  'to 760'

 L. 871       720  LOAD_GLOBAL              Image
              722  LOAD_ATTR                core
              724  LOAD_METHOD              fill
              726  LOAD_FAST                'self'
              728  LOAD_ATTR                mode
              730  LOAD_FAST                'self'
              732  LOAD_ATTR                size
              734  CALL_METHOD_2         2  ''
              736  LOAD_FAST                'self'
              738  STORE_ATTR               dispose

 L. 872       740  LOAD_FAST                'self'
              742  LOAD_METHOD              _crop
              744  LOAD_FAST                'self'
              746  LOAD_ATTR                dispose
              748  LOAD_FAST                'self'
              750  LOAD_ATTR                dispose_extent
              752  CALL_METHOD_2         2  ''
              754  LOAD_FAST                'self'
              756  STORE_ATTR               dispose
              758  JUMP_FORWARD        766  'to 766'
            760_0  COME_FROM           716  '716'

 L. 874       760  LOAD_CONST               None
              762  LOAD_FAST                'self'
              764  STORE_ATTR               dispose
            766_0  COME_FROM           758  '758'
            766_1  COME_FROM           706  '706'

Parse error at or near `<121>' instruction at offset 328_330

    def tell(self):
        return self._PngImageFile__frame

    def load_prepare(self):
        """internal: prepare to read PNG file"""
        if self.info.get('interlace'):
            self.decoderconfig = self.decoderconfig + (1, )
        self._PngImageFile__idat = self._PngImageFile__prepare_idat
        ImageFile.ImageFile.load_prepare(self)

    def load_read--- This code section failed: ---

 L. 891         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _PngImageFile__idat
                4  LOAD_CONST               0
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE   134  'to 134'

 L. 894        10  LOAD_FAST                'self'
               12  LOAD_ATTR                fp
               14  LOAD_METHOD              read
               16  LOAD_CONST               4
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 896        22  LOAD_FAST                'self'
               24  LOAD_ATTR                png
               26  LOAD_METHOD              read
               28  CALL_METHOD_0         0  ''
               30  UNPACK_SEQUENCE_3     3 
               32  STORE_FAST               'cid'
               34  STORE_FAST               'pos'
               36  STORE_FAST               'length'

 L. 898        38  LOAD_FAST                'cid'
               40  LOAD_CONST               (b'IDAT', b'DDAT', b'fdAT')
               42  <118>                 1  ''
               44  POP_JUMP_IF_FALSE    66  'to 66'

 L. 899        46  LOAD_FAST                'self'
               48  LOAD_ATTR                png
               50  LOAD_METHOD              push
               52  LOAD_FAST                'cid'
               54  LOAD_FAST                'pos'
               56  LOAD_FAST                'length'
               58  CALL_METHOD_3         3  ''
               60  POP_TOP          

 L. 900        62  LOAD_CONST               b''
               64  RETURN_VALUE     
             66_0  COME_FROM            44  '44'

 L. 902        66  LOAD_FAST                'cid'
               68  LOAD_CONST               b'fdAT'
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE   126  'to 126'

 L. 903        74  SETUP_FINALLY        96  'to 96'

 L. 904        76  LOAD_FAST                'self'
               78  LOAD_ATTR                png
               80  LOAD_METHOD              call
               82  LOAD_FAST                'cid'
               84  LOAD_FAST                'pos'
               86  LOAD_FAST                'length'
               88  CALL_METHOD_3         3  ''
               90  POP_TOP          
               92  POP_BLOCK        
               94  JUMP_FORWARD        114  'to 114'
             96_0  COME_FROM_FINALLY    74  '74'

 L. 905        96  DUP_TOP          
               98  LOAD_GLOBAL              EOFError
              100  <121>               112  ''
              102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          

 L. 906       108  POP_EXCEPT       
              110  JUMP_FORWARD        114  'to 114'
              112  <48>             
            114_0  COME_FROM           110  '110'
            114_1  COME_FROM            94  '94'

 L. 907       114  LOAD_FAST                'length'
              116  LOAD_CONST               4
              118  BINARY_SUBTRACT  
              120  LOAD_FAST                'self'
              122  STORE_ATTR               _PngImageFile__idat
              124  JUMP_BACK             0  'to 0'
            126_0  COME_FROM            72  '72'

 L. 909       126  LOAD_FAST                'length'
              128  LOAD_FAST                'self'
              130  STORE_ATTR               _PngImageFile__idat
              132  JUMP_BACK             0  'to 0'
            134_0  COME_FROM             8  '8'

 L. 912       134  LOAD_FAST                'read_bytes'
              136  LOAD_CONST               0
              138  COMPARE_OP               <=
              140  POP_JUMP_IF_FALSE   150  'to 150'

 L. 913       142  LOAD_FAST                'self'
              144  LOAD_ATTR                _PngImageFile__idat
              146  STORE_FAST               'read_bytes'
              148  JUMP_FORWARD        162  'to 162'
            150_0  COME_FROM           140  '140'

 L. 915       150  LOAD_GLOBAL              min
              152  LOAD_FAST                'read_bytes'
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                _PngImageFile__idat
              158  CALL_FUNCTION_2       2  ''
              160  STORE_FAST               'read_bytes'
            162_0  COME_FROM           148  '148'

 L. 917       162  LOAD_FAST                'self'
              164  LOAD_ATTR                _PngImageFile__idat
              166  LOAD_FAST                'read_bytes'
              168  BINARY_SUBTRACT  
              170  LOAD_FAST                'self'
              172  STORE_ATTR               _PngImageFile__idat

 L. 919       174  LOAD_FAST                'self'
              176  LOAD_ATTR                fp
              178  LOAD_METHOD              read
              180  LOAD_FAST                'read_bytes'
              182  CALL_METHOD_1         1  ''
              184  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 42

    def load_end--- This code section failed: ---

 L. 923         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _PngImageFile__idat
                4  LOAD_CONST               0
                6  COMPARE_OP               !=
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 924        10  LOAD_FAST                'self'
               12  LOAD_ATTR                fp
               14  LOAD_METHOD              read
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _PngImageFile__idat
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          
             24_0  COME_FROM             8  '8'

 L. 926        24  LOAD_FAST                'self'
               26  LOAD_ATTR                fp
               28  LOAD_METHOD              read
               30  LOAD_CONST               4
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 928        36  SETUP_FINALLY        58  'to 58'

 L. 929        38  LOAD_FAST                'self'
               40  LOAD_ATTR                png
               42  LOAD_METHOD              read
               44  CALL_METHOD_0         0  ''
               46  UNPACK_SEQUENCE_3     3 
               48  STORE_FAST               'cid'
               50  STORE_FAST               'pos'
               52  STORE_FAST               'length'
               54  POP_BLOCK        
               56  JUMP_FORWARD         88  'to 88'
             58_0  COME_FROM_FINALLY    36  '36'

 L. 930        58  DUP_TOP          
               60  LOAD_GLOBAL              struct
               62  LOAD_ATTR                error
               64  LOAD_GLOBAL              SyntaxError
               66  BUILD_TUPLE_2         2 
               68  <121>                86  ''
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 931        76  POP_EXCEPT       
            78_80  BREAK_LOOP          320  'to 320'
               82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
               86  <48>             
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            56  '56'

 L. 933        88  LOAD_FAST                'cid'
               90  LOAD_CONST               b'IEND'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   102  'to 102'

 L. 934     96_98  BREAK_LOOP          320  'to 320'
              100  JUMP_FORWARD        142  'to 142'
            102_0  COME_FROM            94  '94'

 L. 935       102  LOAD_FAST                'cid'
              104  LOAD_CONST               b'fcTL'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   142  'to 142'
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                is_animated
              114  POP_JUMP_IF_FALSE   142  'to 142'

 L. 937       116  LOAD_CONST               0
              118  LOAD_FAST                'self'
              120  STORE_ATTR               _PngImageFile__prepare_idat

 L. 938       122  LOAD_FAST                'self'
              124  LOAD_ATTR                png
              126  LOAD_METHOD              push
              128  LOAD_FAST                'cid'
              130  LOAD_FAST                'pos'
              132  LOAD_FAST                'length'
              134  CALL_METHOD_3         3  ''
              136  POP_TOP          

 L. 939   138_140  BREAK_LOOP          320  'to 320'
            142_0  COME_FROM           114  '114'
            142_1  COME_FROM           108  '108'
            142_2  COME_FROM           100  '100'

 L. 941       142  SETUP_FINALLY       164  'to 164'

 L. 942       144  LOAD_FAST                'self'
              146  LOAD_ATTR                png
              148  LOAD_METHOD              call
              150  LOAD_FAST                'cid'
              152  LOAD_FAST                'pos'
              154  LOAD_FAST                'length'
              156  CALL_METHOD_3         3  ''
              158  POP_TOP          
              160  POP_BLOCK        
              162  JUMP_BACK            24  'to 24'
            164_0  COME_FROM_FINALLY   142  '142'

 L. 943       164  DUP_TOP          
              166  LOAD_GLOBAL              UnicodeDecodeError
              168  <121>               186  ''
              170  POP_TOP          
              172  POP_TOP          
              174  POP_TOP          

 L. 944       176  POP_EXCEPT       
          178_180  BREAK_LOOP          320  'to 320'
              182  POP_EXCEPT       
              184  JUMP_BACK            24  'to 24'

 L. 945       186  DUP_TOP          
              188  LOAD_GLOBAL              EOFError
              190  <121>               232  ''
              192  POP_TOP          
              194  POP_TOP          
              196  POP_TOP          

 L. 946       198  LOAD_FAST                'cid'
              200  LOAD_CONST               b'fdAT'
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   214  'to 214'

 L. 947       206  LOAD_FAST                'length'
              208  LOAD_CONST               4
              210  INPLACE_SUBTRACT 
              212  STORE_FAST               'length'
            214_0  COME_FROM           204  '204'

 L. 948       214  LOAD_GLOBAL              ImageFile
              216  LOAD_METHOD              _safe_read
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                fp
              222  LOAD_FAST                'length'
              224  CALL_METHOD_2         2  ''
              226  POP_TOP          
              228  POP_EXCEPT       
              230  JUMP_BACK            24  'to 24'

 L. 949       232  DUP_TOP          
              234  LOAD_GLOBAL              AttributeError
          236_238  <121>               316  ''
              240  POP_TOP          
              242  POP_TOP          
              244  POP_TOP          

 L. 950       246  LOAD_GLOBAL              logger
              248  LOAD_METHOD              debug
              250  LOAD_STR                 '%r %s %s (unknown)'
              252  LOAD_FAST                'cid'
              254  LOAD_FAST                'pos'
              256  LOAD_FAST                'length'
              258  CALL_METHOD_4         4  ''
              260  POP_TOP          

 L. 951       262  LOAD_GLOBAL              ImageFile
              264  LOAD_METHOD              _safe_read
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                fp
              270  LOAD_FAST                'length'
              272  CALL_METHOD_2         2  ''
              274  STORE_FAST               's'

 L. 952       276  LOAD_FAST                'cid'
              278  LOAD_CONST               1
              280  LOAD_CONST               2
              282  BUILD_SLICE_2         2 
              284  BINARY_SUBSCR    
              286  LOAD_METHOD              islower
              288  CALL_METHOD_0         0  ''
          290_292  POP_JUMP_IF_FALSE   312  'to 312'

 L. 953       294  LOAD_FAST                'self'
              296  LOAD_ATTR                private_chunks
              298  LOAD_METHOD              append
              300  LOAD_FAST                'cid'
              302  LOAD_FAST                's'
              304  LOAD_CONST               True
              306  BUILD_TUPLE_3         3 
              308  CALL_METHOD_1         1  ''
              310  POP_TOP          
            312_0  COME_FROM           290  '290'
              312  POP_EXCEPT       
              314  JUMP_BACK            24  'to 24'
              316  <48>             
              318  JUMP_BACK            24  'to 24'

 L. 954       320  LOAD_FAST                'self'
              322  LOAD_ATTR                png
              324  LOAD_ATTR                im_text
              326  LOAD_FAST                'self'
              328  STORE_ATTR               _text

 L. 955       330  LOAD_FAST                'self'
              332  LOAD_ATTR                is_animated
          334_336  POP_JUMP_IF_TRUE    356  'to 356'

 L. 956       338  LOAD_FAST                'self'
              340  LOAD_ATTR                png
              342  LOAD_METHOD              close
              344  CALL_METHOD_0         0  ''
              346  POP_TOP          

 L. 957       348  LOAD_CONST               None
              350  LOAD_FAST                'self'
              352  STORE_ATTR               png
              354  JUMP_FORWARD        438  'to 438'
            356_0  COME_FROM           334  '334'

 L. 959       356  LOAD_FAST                'self'
              358  LOAD_ATTR                _prev_im
          360_362  POP_JUMP_IF_FALSE   438  'to 438'
              364  LOAD_FAST                'self'
              366  LOAD_ATTR                blend_op
              368  LOAD_GLOBAL              APNG_BLEND_OP_OVER
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   438  'to 438'

 L. 960       376  LOAD_FAST                'self'
              378  LOAD_METHOD              _crop
              380  LOAD_FAST                'self'
              382  LOAD_ATTR                im
              384  LOAD_FAST                'self'
              386  LOAD_ATTR                dispose_extent
              388  CALL_METHOD_2         2  ''
              390  STORE_FAST               'updated'

 L. 961       392  LOAD_FAST                'self'
              394  LOAD_ATTR                _prev_im
              396  LOAD_METHOD              paste

 L. 962       398  LOAD_FAST                'updated'
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                dispose_extent
              404  LOAD_FAST                'updated'
              406  LOAD_METHOD              convert
              408  LOAD_STR                 'RGBA'
              410  CALL_METHOD_1         1  ''

 L. 961       412  CALL_METHOD_3         3  ''
              414  POP_TOP          

 L. 964       416  LOAD_FAST                'self'
              418  LOAD_ATTR                _prev_im
              420  LOAD_FAST                'self'
              422  STORE_ATTR               im

 L. 965       424  LOAD_FAST                'self'
              426  LOAD_ATTR                pyaccess
          428_430  POP_JUMP_IF_FALSE   438  'to 438'

 L. 966       432  LOAD_CONST               None
              434  LOAD_FAST                'self'
              436  STORE_ATTR               pyaccess
            438_0  COME_FROM           428  '428'
            438_1  COME_FROM           372  '372'
            438_2  COME_FROM           360  '360'
            438_3  COME_FROM           354  '354'

Parse error at or near `<121>' instruction at offset 68

    def _getexif--- This code section failed: ---

 L. 969         0  LOAD_STR                 'exif'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                info
                6  <118>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 970        10  LOAD_FAST                'self'
               12  LOAD_METHOD              load
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 971        18  LOAD_STR                 'exif'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                info
               24  <118>                 1  ''
               26  POP_JUMP_IF_FALSE    42  'to 42'
               28  LOAD_STR                 'Raw profile type exif'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                info
               34  <118>                 1  ''
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L. 972        38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            36  '36'
             42_1  COME_FROM            26  '26'

 L. 973        42  LOAD_FAST                'self'
               44  LOAD_METHOD              getexif
               46  CALL_METHOD_0         0  ''
               48  LOAD_METHOD              _get_merged_dict
               50  CALL_METHOD_0         0  ''
               52  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def getexif--- This code section failed: ---

 L. 976         0  LOAD_STR                 'exif'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                info
                6  <118>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 977        10  LOAD_FAST                'self'
               12  LOAD_METHOD              load
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 979        18  LOAD_GLOBAL              super
               20  CALL_FUNCTION_0       0  ''
               22  LOAD_METHOD              getexif
               24  CALL_METHOD_0         0  ''
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def getxmp--- This code section failed: ---

 L. 989         0  LOAD_STR                 'XML:com.adobe.xmp'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                info
                6  <118>                 0  ''

 L. 988         8  POP_JUMP_IF_FALSE    26  'to 26'
               10  LOAD_FAST                'self'
               12  LOAD_METHOD              _getxmp
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                info
               18  LOAD_STR                 'XML:com.adobe.xmp'
               20  BINARY_SUBSCR    
               22  CALL_METHOD_1         1  ''
               24  RETURN_VALUE     
             26_0  COME_FROM             8  '8'

 L. 990        26  BUILD_MAP_0           0 

 L. 987        28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _close__fp--- This code section failed: ---

 L. 994         0  SETUP_FINALLY        58  'to 58'
                2  SETUP_FINALLY        30  'to 30'

 L. 995         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _PngImageFile__fp
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                fp
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 996        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _PngImageFile__fp
               20  LOAD_METHOD              close
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'
               26  POP_BLOCK        
               28  JUMP_FORWARD         48  'to 48'
             30_0  COME_FROM_FINALLY     2  '2'

 L. 997        30  DUP_TOP          
               32  LOAD_GLOBAL              AttributeError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 998        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            28  '28'
               48  POP_BLOCK        

 L.1000        50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _PngImageFile__fp
               56  JUMP_FORWARD         66  'to 66'
             58_0  COME_FROM_FINALLY     0  '0'
               58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _PngImageFile__fp
               64  <48>             
             66_0  COME_FROM            56  '56'

Parse error at or near `<121>' instruction at offset 34


_OUTMODES = {'1':('1', b'\x01\x00'), 
 'L;1':('L;1', b'\x01\x00'), 
 'L;2':('L;2', b'\x02\x00'), 
 'L;4':('L;4', b'\x04\x00'), 
 'L':('L', b'\x08\x00'), 
 'LA':('LA', b'\x08\x04'), 
 'I':('I;16B', b'\x10\x00'), 
 'I;16':('I;16B', b'\x10\x00'), 
 'P;1':('P;1', b'\x01\x03'), 
 'P;2':('P;2', b'\x02\x03'), 
 'P;4':('P;4', b'\x04\x03'), 
 'P':('P', b'\x08\x03'), 
 'RGB':('RGB', b'\x08\x02'), 
 'RGBA':('RGBA', b'\x08\x06')}

def putchunk(fp, cid, *data):
    """Write a PNG chunk (including CRC field)"""
    data = (b'').join(data)
    fp.write(o32(len(data)) + cid)
    fp.write(data)
    crc = _crc32(data, _crc32(cid))
    fp.write(o32(crc))


class _idat:

    def __init__(self, fp, chunk):
        self.fp = fp
        self.chunk = chunk

    def write(self, data):
        self.chunk(self.fp, b'IDAT', data)


class _fdat:

    def __init__(self, fp, chunk, seq_num):
        self.fp = fp
        self.chunk = chunk
        self.seq_num = seq_num

    def write(self, data):
        self.chunk(self.fp, b'fdAT', o32(self.seq_num), data)
        self.seq_num += 1


def _write_multiple_frames--- This code section failed: ---

 L.1061         0  LOAD_FAST                'im'
                2  LOAD_ATTR                encoderinfo
                4  LOAD_METHOD              get
                6  LOAD_STR                 'default_image'
                8  LOAD_FAST                'im'
               10  LOAD_ATTR                info
               12  LOAD_METHOD              get
               14  LOAD_STR                 'default_image'
               16  CALL_METHOD_1         1  ''
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'default_image'

 L.1062        22  LOAD_FAST                'im'
               24  LOAD_ATTR                encoderinfo
               26  LOAD_METHOD              get
               28  LOAD_STR                 'duration'
               30  LOAD_FAST                'im'
               32  LOAD_ATTR                info
               34  LOAD_METHOD              get
               36  LOAD_STR                 'duration'
               38  LOAD_CONST               0
               40  CALL_METHOD_2         2  ''
               42  CALL_METHOD_2         2  ''
               44  STORE_FAST               'duration'

 L.1063        46  LOAD_FAST                'im'
               48  LOAD_ATTR                encoderinfo
               50  LOAD_METHOD              get
               52  LOAD_STR                 'loop'
               54  LOAD_FAST                'im'
               56  LOAD_ATTR                info
               58  LOAD_METHOD              get
               60  LOAD_STR                 'loop'
               62  LOAD_CONST               0
               64  CALL_METHOD_2         2  ''
               66  CALL_METHOD_2         2  ''
               68  STORE_FAST               'loop'

 L.1064        70  LOAD_FAST                'im'
               72  LOAD_ATTR                encoderinfo
               74  LOAD_METHOD              get
               76  LOAD_STR                 'disposal'
               78  LOAD_FAST                'im'
               80  LOAD_ATTR                info
               82  LOAD_METHOD              get
               84  LOAD_STR                 'disposal'
               86  CALL_METHOD_1         1  ''
               88  CALL_METHOD_2         2  ''
               90  STORE_FAST               'disposal'

 L.1065        92  LOAD_FAST                'im'
               94  LOAD_ATTR                encoderinfo
               96  LOAD_METHOD              get
               98  LOAD_STR                 'blend'
              100  LOAD_FAST                'im'
              102  LOAD_ATTR                info
              104  LOAD_METHOD              get
              106  LOAD_STR                 'blend'
              108  CALL_METHOD_1         1  ''
              110  CALL_METHOD_2         2  ''
              112  STORE_FAST               'blend'

 L.1067       114  LOAD_FAST                'default_image'
              116  POP_JUMP_IF_FALSE   140  'to 140'

 L.1068       118  LOAD_GLOBAL              itertools
              120  LOAD_METHOD              chain
              122  LOAD_FAST                'im'
              124  LOAD_ATTR                encoderinfo
              126  LOAD_METHOD              get
              128  LOAD_STR                 'append_images'
              130  BUILD_LIST_0          0 
              132  CALL_METHOD_2         2  ''
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'chain'
              138  JUMP_FORWARD        164  'to 164'
            140_0  COME_FROM           116  '116'

 L.1070       140  LOAD_GLOBAL              itertools
              142  LOAD_METHOD              chain
              144  LOAD_FAST                'im'
              146  BUILD_LIST_1          1 
              148  LOAD_FAST                'im'
              150  LOAD_ATTR                encoderinfo
              152  LOAD_METHOD              get
              154  LOAD_STR                 'append_images'
              156  BUILD_LIST_0          0 
              158  CALL_METHOD_2         2  ''
              160  CALL_METHOD_2         2  ''
              162  STORE_FAST               'chain'
            164_0  COME_FROM           138  '138'

 L.1072       164  BUILD_LIST_0          0 
              166  STORE_FAST               'im_frames'

 L.1073       168  LOAD_CONST               0
              170  STORE_FAST               'frame_count'

 L.1074       172  LOAD_FAST                'chain'
              174  GET_ITER         
          176_178  FOR_ITER            716  'to 716'
              180  STORE_FAST               'im_seq'

 L.1075       182  LOAD_GLOBAL              ImageSequence
              184  LOAD_METHOD              Iterator
              186  LOAD_FAST                'im_seq'
              188  CALL_METHOD_1         1  ''
              190  GET_ITER         
            192_0  COME_FROM           636  '636'
          192_194  FOR_ITER            714  'to 714'
              196  STORE_FAST               'im_frame'

 L.1076       198  LOAD_FAST                'im_frame'
              200  LOAD_METHOD              copy
              202  CALL_METHOD_0         0  ''
              204  STORE_FAST               'im_frame'

 L.1077       206  LOAD_FAST                'im_frame'
              208  LOAD_ATTR                mode
              210  LOAD_FAST                'im'
              212  LOAD_ATTR                mode
              214  COMPARE_OP               !=
          216_218  POP_JUMP_IF_FALSE   262  'to 262'

 L.1078       220  LOAD_FAST                'im'
              222  LOAD_ATTR                mode
              224  LOAD_STR                 'P'
              226  COMPARE_OP               ==
              228  POP_JUMP_IF_FALSE   250  'to 250'

 L.1079       230  LOAD_FAST                'im_frame'
              232  LOAD_ATTR                convert
              234  LOAD_FAST                'im'
              236  LOAD_ATTR                mode
              238  LOAD_FAST                'im'
              240  LOAD_ATTR                palette
              242  LOAD_CONST               ('palette',)
              244  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              246  STORE_FAST               'im_frame'
              248  JUMP_FORWARD        262  'to 262'
            250_0  COME_FROM           228  '228'

 L.1081       250  LOAD_FAST                'im_frame'
              252  LOAD_METHOD              convert
              254  LOAD_FAST                'im'
              256  LOAD_ATTR                mode
              258  CALL_METHOD_1         1  ''
              260  STORE_FAST               'im_frame'
            262_0  COME_FROM           248  '248'
            262_1  COME_FROM           216  '216'

 L.1082       262  LOAD_FAST                'im'
              264  LOAD_ATTR                encoderinfo
              266  LOAD_METHOD              copy
              268  CALL_METHOD_0         0  ''
              270  STORE_FAST               'encoderinfo'

 L.1083       272  LOAD_GLOBAL              isinstance
              274  LOAD_FAST                'duration'
              276  LOAD_GLOBAL              list
              278  LOAD_GLOBAL              tuple
              280  BUILD_TUPLE_2         2 
              282  CALL_FUNCTION_2       2  ''
          284_286  POP_JUMP_IF_FALSE   300  'to 300'

 L.1084       288  LOAD_FAST                'duration'
              290  LOAD_FAST                'frame_count'
              292  BINARY_SUBSCR    
              294  LOAD_FAST                'encoderinfo'
              296  LOAD_STR                 'duration'
              298  STORE_SUBSCR     
            300_0  COME_FROM           284  '284'

 L.1085       300  LOAD_GLOBAL              isinstance
              302  LOAD_FAST                'disposal'
              304  LOAD_GLOBAL              list
              306  LOAD_GLOBAL              tuple
              308  BUILD_TUPLE_2         2 
              310  CALL_FUNCTION_2       2  ''
          312_314  POP_JUMP_IF_FALSE   328  'to 328'

 L.1086       316  LOAD_FAST                'disposal'
              318  LOAD_FAST                'frame_count'
              320  BINARY_SUBSCR    
              322  LOAD_FAST                'encoderinfo'
              324  LOAD_STR                 'disposal'
              326  STORE_SUBSCR     
            328_0  COME_FROM           312  '312'

 L.1087       328  LOAD_GLOBAL              isinstance
              330  LOAD_FAST                'blend'
              332  LOAD_GLOBAL              list
              334  LOAD_GLOBAL              tuple
              336  BUILD_TUPLE_2         2 
              338  CALL_FUNCTION_2       2  ''
          340_342  POP_JUMP_IF_FALSE   356  'to 356'

 L.1088       344  LOAD_FAST                'blend'
              346  LOAD_FAST                'frame_count'
              348  BINARY_SUBSCR    
              350  LOAD_FAST                'encoderinfo'
              352  LOAD_STR                 'blend'
              354  STORE_SUBSCR     
            356_0  COME_FROM           340  '340'

 L.1089       356  LOAD_FAST                'frame_count'
              358  LOAD_CONST               1
              360  INPLACE_ADD      
              362  STORE_FAST               'frame_count'

 L.1091       364  LOAD_FAST                'im_frames'
          366_368  POP_JUMP_IF_FALSE   690  'to 690'

 L.1092       370  LOAD_FAST                'im_frames'
              372  LOAD_CONST               -1
              374  BINARY_SUBSCR    
              376  STORE_FAST               'previous'

 L.1093       378  LOAD_FAST                'previous'
              380  LOAD_STR                 'encoderinfo'
              382  BINARY_SUBSCR    
              384  LOAD_METHOD              get
              386  LOAD_STR                 'disposal'
              388  CALL_METHOD_1         1  ''
              390  STORE_FAST               'prev_disposal'

 L.1094       392  LOAD_FAST                'previous'
              394  LOAD_STR                 'encoderinfo'
              396  BINARY_SUBSCR    
              398  LOAD_METHOD              get
              400  LOAD_STR                 'blend'
              402  CALL_METHOD_1         1  ''
              404  STORE_FAST               'prev_blend'

 L.1095       406  LOAD_FAST                'prev_disposal'
              408  LOAD_GLOBAL              APNG_DISPOSE_OP_PREVIOUS
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_FALSE   434  'to 434'
              416  LOAD_GLOBAL              len
              418  LOAD_FAST                'im_frames'
              420  CALL_FUNCTION_1       1  ''
              422  LOAD_CONST               2
              424  COMPARE_OP               <
          426_428  POP_JUMP_IF_FALSE   434  'to 434'

 L.1096       430  LOAD_GLOBAL              APNG_DISPOSE_OP_BACKGROUND
              432  STORE_FAST               'prev_disposal'
            434_0  COME_FROM           426  '426'
            434_1  COME_FROM           412  '412'

 L.1098       434  LOAD_FAST                'prev_disposal'
              436  LOAD_GLOBAL              APNG_DISPOSE_OP_BACKGROUND
              438  COMPARE_OP               ==
          440_442  POP_JUMP_IF_FALSE   520  'to 520'

 L.1099       444  LOAD_FAST                'previous'
              446  LOAD_STR                 'im'
              448  BINARY_SUBSCR    
              450  STORE_FAST               'base_im'

 L.1100       452  LOAD_GLOBAL              Image
              454  LOAD_ATTR                core
              456  LOAD_METHOD              fill
              458  LOAD_STR                 'RGBA'
              460  LOAD_FAST                'im'
              462  LOAD_ATTR                size
              464  LOAD_CONST               (0, 0, 0, 0)
              466  CALL_METHOD_3         3  ''
              468  STORE_FAST               'dispose'

 L.1101       470  LOAD_FAST                'previous'
              472  LOAD_STR                 'bbox'
              474  BINARY_SUBSCR    
              476  STORE_FAST               'bbox'

 L.1102       478  LOAD_FAST                'bbox'
          480_482  POP_JUMP_IF_FALSE   496  'to 496'

 L.1103       484  LOAD_FAST                'dispose'
              486  LOAD_METHOD              crop
              488  LOAD_FAST                'bbox'
              490  CALL_METHOD_1         1  ''
              492  STORE_FAST               'dispose'
              494  JUMP_FORWARD        506  'to 506'
            496_0  COME_FROM           480  '480'

 L.1105       496  LOAD_CONST               (0, 0)
              498  LOAD_FAST                'im'
              500  LOAD_ATTR                size
              502  BINARY_ADD       
              504  STORE_FAST               'bbox'
            506_0  COME_FROM           494  '494'

 L.1106       506  LOAD_FAST                'base_im'
              508  LOAD_METHOD              paste
              510  LOAD_FAST                'dispose'
              512  LOAD_FAST                'bbox'
              514  CALL_METHOD_2         2  ''
              516  POP_TOP          
              518  JUMP_FORWARD        552  'to 552'
            520_0  COME_FROM           440  '440'

 L.1107       520  LOAD_FAST                'prev_disposal'
              522  LOAD_GLOBAL              APNG_DISPOSE_OP_PREVIOUS
              524  COMPARE_OP               ==
          526_528  POP_JUMP_IF_FALSE   544  'to 544'

 L.1108       530  LOAD_FAST                'im_frames'
              532  LOAD_CONST               -2
              534  BINARY_SUBSCR    
              536  LOAD_STR                 'im'
              538  BINARY_SUBSCR    
              540  STORE_FAST               'base_im'
              542  JUMP_FORWARD        552  'to 552'
            544_0  COME_FROM           526  '526'

 L.1110       544  LOAD_FAST                'previous'
              546  LOAD_STR                 'im'
              548  BINARY_SUBSCR    
              550  STORE_FAST               'base_im'
            552_0  COME_FROM           542  '542'
            552_1  COME_FROM           518  '518'

 L.1111       552  LOAD_GLOBAL              ImageChops
              554  LOAD_METHOD              subtract_modulo

 L.1112       556  LOAD_FAST                'im_frame'
              558  LOAD_METHOD              convert
              560  LOAD_STR                 'RGB'
              562  CALL_METHOD_1         1  ''
              564  LOAD_FAST                'base_im'
              566  LOAD_METHOD              convert
              568  LOAD_STR                 'RGB'
              570  CALL_METHOD_1         1  ''

 L.1111       572  CALL_METHOD_2         2  ''
              574  STORE_FAST               'delta'

 L.1114       576  LOAD_FAST                'delta'
              578  LOAD_METHOD              getbbox
              580  CALL_METHOD_0         0  ''
              582  STORE_FAST               'bbox'

 L.1116       584  LOAD_FAST                'bbox'

 L.1115   586_588  POP_JUMP_IF_TRUE    694  'to 694'

 L.1117       590  LOAD_FAST                'prev_disposal'
              592  LOAD_FAST                'encoderinfo'
              594  LOAD_METHOD              get
              596  LOAD_STR                 'disposal'
              598  CALL_METHOD_1         1  ''
              600  COMPARE_OP               ==

 L.1115   602_604  POP_JUMP_IF_FALSE   694  'to 694'

 L.1118       606  LOAD_FAST                'prev_blend'
              608  LOAD_FAST                'encoderinfo'
              610  LOAD_METHOD              get
              612  LOAD_STR                 'blend'
              614  CALL_METHOD_1         1  ''
              616  COMPARE_OP               ==

 L.1115   618_620  POP_JUMP_IF_FALSE   694  'to 694'

 L.1120       622  LOAD_FAST                'encoderinfo'
              624  LOAD_METHOD              get
              626  LOAD_STR                 'duration'
              628  LOAD_CONST               0
              630  CALL_METHOD_2         2  ''
              632  STORE_FAST               'duration'

 L.1121       634  LOAD_FAST                'duration'
              636  POP_JUMP_IF_FALSE   192  'to 192'

 L.1122       638  LOAD_STR                 'duration'
              640  LOAD_FAST                'previous'
              642  LOAD_STR                 'encoderinfo'
              644  BINARY_SUBSCR    
              646  <118>                 0  ''
          648_650  POP_JUMP_IF_FALSE   674  'to 674'

 L.1123       652  LOAD_FAST                'previous'
              654  LOAD_STR                 'encoderinfo'
              656  BINARY_SUBSCR    
              658  LOAD_STR                 'duration'
              660  DUP_TOP_TWO      
              662  BINARY_SUBSCR    
              664  LOAD_FAST                'duration'
              666  INPLACE_ADD      
              668  ROT_THREE        
              670  STORE_SUBSCR     
              672  JUMP_BACK           192  'to 192'
            674_0  COME_FROM           648  '648'

 L.1125       674  LOAD_FAST                'duration'
              676  LOAD_FAST                'previous'
              678  LOAD_STR                 'encoderinfo'
              680  BINARY_SUBSCR    
              682  LOAD_STR                 'duration'
              684  STORE_SUBSCR     

 L.1126       686  JUMP_BACK           192  'to 192'
              688  JUMP_FORWARD        694  'to 694'
            690_0  COME_FROM           366  '366'

 L.1128       690  LOAD_CONST               None
              692  STORE_FAST               'bbox'
            694_0  COME_FROM           688  '688'
            694_1  COME_FROM           618  '618'
            694_2  COME_FROM           602  '602'
            694_3  COME_FROM           586  '586'

 L.1129       694  LOAD_FAST                'im_frames'
              696  LOAD_METHOD              append
              698  LOAD_FAST                'im_frame'
              700  LOAD_FAST                'bbox'
              702  LOAD_FAST                'encoderinfo'
              704  LOAD_CONST               ('im', 'bbox', 'encoderinfo')
              706  BUILD_CONST_KEY_MAP_3     3 
              708  CALL_METHOD_1         1  ''
              710  POP_TOP          
              712  JUMP_BACK           192  'to 192'
              714  JUMP_BACK           176  'to 176'

 L.1132       716  LOAD_FAST                'chunk'

 L.1133       718  LOAD_FAST                'fp'

 L.1134       720  LOAD_CONST               b'acTL'

 L.1135       722  LOAD_GLOBAL              o32
              724  LOAD_GLOBAL              len
              726  LOAD_FAST                'im_frames'
              728  CALL_FUNCTION_1       1  ''
              730  CALL_FUNCTION_1       1  ''

 L.1136       732  LOAD_GLOBAL              o32
              734  LOAD_FAST                'loop'
              736  CALL_FUNCTION_1       1  ''

 L.1132       738  CALL_FUNCTION_4       4  ''
              740  POP_TOP          

 L.1140       742  LOAD_FAST                'default_image'
          744_746  POP_JUMP_IF_FALSE   784  'to 784'

 L.1141       748  LOAD_GLOBAL              ImageFile
              750  LOAD_METHOD              _save
              752  LOAD_FAST                'im'
              754  LOAD_GLOBAL              _idat
              756  LOAD_FAST                'fp'
              758  LOAD_FAST                'chunk'
              760  CALL_FUNCTION_2       2  ''
              762  LOAD_STR                 'zip'
              764  LOAD_CONST               (0, 0)
              766  LOAD_FAST                'im'
              768  LOAD_ATTR                size
              770  BINARY_ADD       
              772  LOAD_CONST               0
              774  LOAD_FAST                'rawmode'
              776  BUILD_TUPLE_4         4 
              778  BUILD_LIST_1          1 
              780  CALL_METHOD_3         3  ''
              782  POP_TOP          
            784_0  COME_FROM           744  '744'

 L.1143       784  LOAD_CONST               0
              786  STORE_FAST               'seq_num'

 L.1144       788  LOAD_GLOBAL              enumerate
              790  LOAD_FAST                'im_frames'
              792  CALL_FUNCTION_1       1  ''
              794  GET_ITER         
          796_798  FOR_ITER           1110  'to 1110'
              800  UNPACK_SEQUENCE_2     2 
              802  STORE_FAST               'frame'
              804  STORE_FAST               'frame_data'

 L.1145       806  LOAD_FAST                'frame_data'
              808  LOAD_STR                 'im'
              810  BINARY_SUBSCR    
              812  STORE_FAST               'im_frame'

 L.1146       814  LOAD_FAST                'frame_data'
              816  LOAD_STR                 'bbox'
              818  BINARY_SUBSCR    
          820_822  POP_JUMP_IF_TRUE    836  'to 836'

 L.1147       824  LOAD_CONST               (0, 0)
              826  LOAD_FAST                'im_frame'
              828  LOAD_ATTR                size
              830  BINARY_ADD       
              832  STORE_FAST               'bbox'
              834  JUMP_FORWARD        854  'to 854'
            836_0  COME_FROM           820  '820'

 L.1149       836  LOAD_FAST                'frame_data'
              838  LOAD_STR                 'bbox'
              840  BINARY_SUBSCR    
              842  STORE_FAST               'bbox'

 L.1150       844  LOAD_FAST                'im_frame'
              846  LOAD_METHOD              crop
              848  LOAD_FAST                'bbox'
              850  CALL_METHOD_1         1  ''
              852  STORE_FAST               'im_frame'
            854_0  COME_FROM           834  '834'

 L.1151       854  LOAD_FAST                'im_frame'
              856  LOAD_ATTR                size
              858  STORE_FAST               'size'

 L.1152       860  LOAD_GLOBAL              int
              862  LOAD_GLOBAL              round
              864  LOAD_FAST                'frame_data'
              866  LOAD_STR                 'encoderinfo'
              868  BINARY_SUBSCR    
              870  LOAD_METHOD              get
              872  LOAD_STR                 'duration'
              874  LOAD_CONST               0
              876  CALL_METHOD_2         2  ''
              878  CALL_FUNCTION_1       1  ''
              880  CALL_FUNCTION_1       1  ''
              882  STORE_FAST               'duration'

 L.1153       884  LOAD_FAST                'frame_data'
              886  LOAD_STR                 'encoderinfo'
              888  BINARY_SUBSCR    
              890  LOAD_METHOD              get
              892  LOAD_STR                 'disposal'
              894  LOAD_GLOBAL              APNG_DISPOSE_OP_NONE
              896  CALL_METHOD_2         2  ''
              898  STORE_FAST               'disposal'

 L.1154       900  LOAD_FAST                'frame_data'
              902  LOAD_STR                 'encoderinfo'
              904  BINARY_SUBSCR    
              906  LOAD_METHOD              get
              908  LOAD_STR                 'blend'
              910  LOAD_GLOBAL              APNG_BLEND_OP_SOURCE
              912  CALL_METHOD_2         2  ''
              914  STORE_FAST               'blend'

 L.1156       916  LOAD_FAST                'chunk'

 L.1157       918  LOAD_FAST                'fp'

 L.1158       920  LOAD_CONST               b'fcTL'

 L.1159       922  LOAD_GLOBAL              o32
              924  LOAD_FAST                'seq_num'
              926  CALL_FUNCTION_1       1  ''

 L.1160       928  LOAD_GLOBAL              o32
              930  LOAD_FAST                'size'
              932  LOAD_CONST               0
              934  BINARY_SUBSCR    
              936  CALL_FUNCTION_1       1  ''

 L.1161       938  LOAD_GLOBAL              o32
              940  LOAD_FAST                'size'
              942  LOAD_CONST               1
              944  BINARY_SUBSCR    
              946  CALL_FUNCTION_1       1  ''

 L.1162       948  LOAD_GLOBAL              o32
              950  LOAD_FAST                'bbox'
              952  LOAD_CONST               0
              954  BINARY_SUBSCR    
              956  CALL_FUNCTION_1       1  ''

 L.1163       958  LOAD_GLOBAL              o32
              960  LOAD_FAST                'bbox'
              962  LOAD_CONST               1
              964  BINARY_SUBSCR    
              966  CALL_FUNCTION_1       1  ''

 L.1164       968  LOAD_GLOBAL              o16
              970  LOAD_FAST                'duration'
              972  CALL_FUNCTION_1       1  ''

 L.1165       974  LOAD_GLOBAL              o16
              976  LOAD_CONST               1000
              978  CALL_FUNCTION_1       1  ''

 L.1166       980  LOAD_GLOBAL              o8
              982  LOAD_FAST                'disposal'
              984  CALL_FUNCTION_1       1  ''

 L.1167       986  LOAD_GLOBAL              o8
              988  LOAD_FAST                'blend'
              990  CALL_FUNCTION_1       1  ''

 L.1156       992  CALL_FUNCTION_11     11  ''
              994  POP_TOP          

 L.1169       996  LOAD_FAST                'seq_num'
              998  LOAD_CONST               1
             1000  INPLACE_ADD      
             1002  STORE_FAST               'seq_num'

 L.1171      1004  LOAD_FAST                'frame'
             1006  LOAD_CONST               0
             1008  COMPARE_OP               ==
         1010_1012  POP_JUMP_IF_FALSE  1058  'to 1058'
             1014  LOAD_FAST                'default_image'
         1016_1018  POP_JUMP_IF_TRUE   1058  'to 1058'

 L.1173      1020  LOAD_GLOBAL              ImageFile
             1022  LOAD_METHOD              _save

 L.1174      1024  LOAD_FAST                'im_frame'

 L.1175      1026  LOAD_GLOBAL              _idat
             1028  LOAD_FAST                'fp'
             1030  LOAD_FAST                'chunk'
             1032  CALL_FUNCTION_2       2  ''

 L.1176      1034  LOAD_STR                 'zip'
             1036  LOAD_CONST               (0, 0)
             1038  LOAD_FAST                'im_frame'
             1040  LOAD_ATTR                size
             1042  BINARY_ADD       
             1044  LOAD_CONST               0
             1046  LOAD_FAST                'rawmode'
             1048  BUILD_TUPLE_4         4 
             1050  BUILD_LIST_1          1 

 L.1173      1052  CALL_METHOD_3         3  ''
             1054  POP_TOP          
             1056  JUMP_BACK           796  'to 796'
           1058_0  COME_FROM          1016  '1016'
           1058_1  COME_FROM          1010  '1010'

 L.1179      1058  LOAD_GLOBAL              _fdat
             1060  LOAD_FAST                'fp'
             1062  LOAD_FAST                'chunk'
             1064  LOAD_FAST                'seq_num'
             1066  CALL_FUNCTION_3       3  ''
             1068  STORE_FAST               'fdat_chunks'

 L.1180      1070  LOAD_GLOBAL              ImageFile
             1072  LOAD_METHOD              _save

 L.1181      1074  LOAD_FAST                'im_frame'

 L.1182      1076  LOAD_FAST                'fdat_chunks'

 L.1183      1078  LOAD_STR                 'zip'
             1080  LOAD_CONST               (0, 0)
             1082  LOAD_FAST                'im_frame'
             1084  LOAD_ATTR                size
             1086  BINARY_ADD       
             1088  LOAD_CONST               0
             1090  LOAD_FAST                'rawmode'
             1092  BUILD_TUPLE_4         4 
             1094  BUILD_LIST_1          1 

 L.1180      1096  CALL_METHOD_3         3  ''
             1098  POP_TOP          

 L.1185      1100  LOAD_FAST                'fdat_chunks'
             1102  LOAD_ATTR                seq_num
             1104  STORE_FAST               'seq_num'
         1106_1108  JUMP_BACK           796  'to 796'

Parse error at or near `<118>' instruction at offset 646


def _save_all(im, fp, filename):
    _save(im, fp, filename, save_all=True)


def _save--- This code section failed: ---

 L.1195         0  LOAD_FAST                'im'
                2  LOAD_ATTR                mode
                4  STORE_FAST               'mode'

 L.1197         6  LOAD_FAST                'mode'
                8  LOAD_STR                 'P'
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE   146  'to 146'

 L.1201        14  LOAD_STR                 'bits'
               16  LOAD_FAST                'im'
               18  LOAD_ATTR                encoderinfo
               20  <118>                 0  ''
               22  POP_JUMP_IF_FALSE    46  'to 46'

 L.1203        24  LOAD_GLOBAL              min
               26  LOAD_CONST               1
               28  LOAD_FAST                'im'
               30  LOAD_ATTR                encoderinfo
               32  LOAD_STR                 'bits'
               34  BINARY_SUBSCR    
               36  BINARY_LSHIFT    
               38  LOAD_CONST               256
               40  CALL_FUNCTION_2       2  ''
               42  STORE_FAST               'colors'
               44  JUMP_FORWARD         92  'to 92'
             46_0  COME_FROM            22  '22'

 L.1206        46  LOAD_FAST                'im'
               48  LOAD_ATTR                palette
               50  POP_JUMP_IF_FALSE    88  'to 88'

 L.1207        52  LOAD_GLOBAL              max
               54  LOAD_GLOBAL              min
               56  LOAD_GLOBAL              len
               58  LOAD_FAST                'im'
               60  LOAD_ATTR                palette
               62  LOAD_METHOD              getdata
               64  CALL_METHOD_0         0  ''
               66  LOAD_CONST               1
               68  BINARY_SUBSCR    
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_CONST               3
               74  BINARY_FLOOR_DIVIDE
               76  LOAD_CONST               256
               78  CALL_FUNCTION_2       2  ''
               80  LOAD_CONST               1
               82  CALL_FUNCTION_2       2  ''
               84  STORE_FAST               'colors'
               86  JUMP_FORWARD         92  'to 92'
             88_0  COME_FROM            50  '50'

 L.1209        88  LOAD_CONST               256
               90  STORE_FAST               'colors'
             92_0  COME_FROM            86  '86'
             92_1  COME_FROM            44  '44'

 L.1211        92  LOAD_FAST                'colors'
               94  LOAD_CONST               16
               96  COMPARE_OP               <=
               98  POP_JUMP_IF_FALSE   146  'to 146'

 L.1212       100  LOAD_FAST                'colors'
              102  LOAD_CONST               2
              104  COMPARE_OP               <=
              106  POP_JUMP_IF_FALSE   114  'to 114'

 L.1213       108  LOAD_CONST               1
              110  STORE_FAST               'bits'
              112  JUMP_FORWARD        132  'to 132'
            114_0  COME_FROM           106  '106'

 L.1214       114  LOAD_FAST                'colors'
              116  LOAD_CONST               4
              118  COMPARE_OP               <=
              120  POP_JUMP_IF_FALSE   128  'to 128'

 L.1215       122  LOAD_CONST               2
              124  STORE_FAST               'bits'
              126  JUMP_FORWARD        132  'to 132'
            128_0  COME_FROM           120  '120'

 L.1217       128  LOAD_CONST               4
              130  STORE_FAST               'bits'
            132_0  COME_FROM           126  '126'
            132_1  COME_FROM           112  '112'

 L.1218       132  LOAD_FAST                'mode'
              134  FORMAT_VALUE          0  ''
              136  LOAD_STR                 ';'
              138  LOAD_FAST                'bits'
              140  FORMAT_VALUE          0  ''
              142  BUILD_STRING_3        3 
              144  STORE_FAST               'mode'
            146_0  COME_FROM            98  '98'
            146_1  COME_FROM            12  '12'

 L.1222       146  LOAD_FAST                'im'
              148  LOAD_ATTR                encoderinfo
              150  LOAD_METHOD              get
              152  LOAD_STR                 'optimize'
              154  LOAD_CONST               False
              156  CALL_METHOD_2         2  ''

 L.1223       158  LOAD_FAST                'im'
              160  LOAD_ATTR                encoderinfo
              162  LOAD_METHOD              get
              164  LOAD_STR                 'compress_level'
              166  LOAD_CONST               -1
              168  CALL_METHOD_2         2  ''

 L.1224       170  LOAD_FAST                'im'
              172  LOAD_ATTR                encoderinfo
              174  LOAD_METHOD              get
              176  LOAD_STR                 'compress_type'
              178  LOAD_CONST               -1
              180  CALL_METHOD_2         2  ''

 L.1225       182  LOAD_FAST                'im'
              184  LOAD_ATTR                encoderinfo
              186  LOAD_METHOD              get
              188  LOAD_STR                 'dictionary'
              190  LOAD_CONST               b''
              192  CALL_METHOD_2         2  ''

 L.1221       194  BUILD_TUPLE_4         4 
              196  LOAD_FAST                'im'
              198  STORE_ATTR               encoderconfig

 L.1229       200  SETUP_FINALLY       218  'to 218'

 L.1230       202  LOAD_GLOBAL              _OUTMODES
              204  LOAD_FAST                'mode'
              206  BINARY_SUBSCR    
              208  UNPACK_SEQUENCE_2     2 
              210  STORE_FAST               'rawmode'
              212  STORE_FAST               'mode'
              214  POP_BLOCK        
              216  JUMP_FORWARD        274  'to 274'
            218_0  COME_FROM_FINALLY   200  '200'

 L.1231       218  DUP_TOP          
              220  LOAD_GLOBAL              KeyError
          222_224  <121>               272  ''
              226  POP_TOP          
              228  STORE_FAST               'e'
              230  POP_TOP          
              232  SETUP_FINALLY       264  'to 264'

 L.1232       234  LOAD_GLOBAL              OSError
              236  LOAD_STR                 'cannot write mode '
              238  LOAD_FAST                'mode'
              240  FORMAT_VALUE          0  ''
              242  LOAD_STR                 ' as PNG'
              244  BUILD_STRING_3        3 
              246  CALL_FUNCTION_1       1  ''
              248  LOAD_FAST                'e'
              250  RAISE_VARARGS_2       2  'exception instance with __cause__'
              252  POP_BLOCK        
              254  POP_EXCEPT       
              256  LOAD_CONST               None
              258  STORE_FAST               'e'
              260  DELETE_FAST              'e'
              262  JUMP_FORWARD        274  'to 274'
            264_0  COME_FROM_FINALLY   232  '232'
              264  LOAD_CONST               None
              266  STORE_FAST               'e'
              268  DELETE_FAST              'e'
              270  <48>             
              272  <48>             
            274_0  COME_FROM           262  '262'
            274_1  COME_FROM           216  '216'

 L.1237       274  LOAD_FAST                'fp'
              276  LOAD_METHOD              write
              278  LOAD_GLOBAL              _MAGIC
              280  CALL_METHOD_1         1  ''
              282  POP_TOP          

 L.1239       284  LOAD_FAST                'chunk'

 L.1240       286  LOAD_FAST                'fp'

 L.1241       288  LOAD_CONST               b'IHDR'

 L.1242       290  LOAD_GLOBAL              o32
              292  LOAD_FAST                'im'
              294  LOAD_ATTR                size
              296  LOAD_CONST               0
              298  BINARY_SUBSCR    
              300  CALL_FUNCTION_1       1  ''

 L.1243       302  LOAD_GLOBAL              o32
              304  LOAD_FAST                'im'
              306  LOAD_ATTR                size
              308  LOAD_CONST               1
              310  BINARY_SUBSCR    
              312  CALL_FUNCTION_1       1  ''

 L.1244       314  LOAD_FAST                'mode'

 L.1245       316  LOAD_CONST               b'\x00'

 L.1246       318  LOAD_CONST               b'\x00'

 L.1247       320  LOAD_CONST               b'\x00'

 L.1239       322  CALL_FUNCTION_8       8  ''
              324  POP_TOP          

 L.1250       326  BUILD_LIST_0          0 
              328  LOAD_CONST               (b'cHRM', b'gAMA', b'sBIT', b'sRGB', b'tIME')
              330  CALL_FINALLY        333  'to 333'
              332  STORE_FAST               'chunks'

 L.1252       334  LOAD_FAST                'im'
              336  LOAD_ATTR                encoderinfo
              338  LOAD_METHOD              get
              340  LOAD_STR                 'icc_profile'
              342  LOAD_FAST                'im'
              344  LOAD_ATTR                info
              346  LOAD_METHOD              get
              348  LOAD_STR                 'icc_profile'
              350  CALL_METHOD_1         1  ''
              352  CALL_METHOD_2         2  ''
              354  STORE_FAST               'icc'

 L.1253       356  LOAD_FAST                'icc'
          358_360  POP_JUMP_IF_FALSE   406  'to 406'

 L.1260       362  LOAD_CONST               b'ICC Profile'
              364  STORE_FAST               'name'

 L.1261       366  LOAD_FAST                'name'
              368  LOAD_CONST               b'\x00\x00'
              370  BINARY_ADD       
              372  LOAD_GLOBAL              zlib
              374  LOAD_METHOD              compress
              376  LOAD_FAST                'icc'
              378  CALL_METHOD_1         1  ''
              380  BINARY_ADD       
              382  STORE_FAST               'data'

 L.1262       384  LOAD_FAST                'chunk'
              386  LOAD_FAST                'fp'
              388  LOAD_CONST               b'iCCP'
              390  LOAD_FAST                'data'
              392  CALL_FUNCTION_3       3  ''
              394  POP_TOP          

 L.1266       396  LOAD_FAST                'chunks'
              398  LOAD_METHOD              remove
              400  LOAD_CONST               b'sRGB'
              402  CALL_METHOD_1         1  ''
              404  POP_TOP          
            406_0  COME_FROM           358  '358'

 L.1268       406  LOAD_FAST                'im'
              408  LOAD_ATTR                encoderinfo
              410  LOAD_METHOD              get
              412  LOAD_STR                 'pnginfo'
              414  CALL_METHOD_1         1  ''
              416  STORE_FAST               'info'

 L.1269       418  LOAD_FAST                'info'
          420_422  POP_JUMP_IF_FALSE   568  'to 568'

 L.1270       424  BUILD_LIST_0          0 
              426  LOAD_CONST               (b'sPLT', b'iTXt', b'tEXt', b'zTXt')
              428  CALL_FINALLY        431  'to 431'
              430  STORE_FAST               'chunks_multiple_allowed'

 L.1271       432  LOAD_FAST                'info'
              434  LOAD_ATTR                chunks
              436  GET_ITER         
            438_0  COME_FROM           548  '548'
            438_1  COME_FROM           530  '530'
              438  FOR_ITER            568  'to 568'
              440  STORE_FAST               'info_chunk'

 L.1272       442  LOAD_FAST                'info_chunk'
              444  LOAD_CONST               None
              446  LOAD_CONST               2
              448  BUILD_SLICE_2         2 
              450  BINARY_SUBSCR    
              452  UNPACK_SEQUENCE_2     2 
              454  STORE_FAST               'cid'
              456  STORE_FAST               'data'

 L.1273       458  LOAD_FAST                'cid'
              460  LOAD_FAST                'chunks'
              462  <118>                 0  ''
          464_466  POP_JUMP_IF_FALSE   492  'to 492'

 L.1274       468  LOAD_FAST                'chunks'
              470  LOAD_METHOD              remove
              472  LOAD_FAST                'cid'
              474  CALL_METHOD_1         1  ''
              476  POP_TOP          

 L.1275       478  LOAD_FAST                'chunk'
              480  LOAD_FAST                'fp'
              482  LOAD_FAST                'cid'
              484  LOAD_FAST                'data'
              486  CALL_FUNCTION_3       3  ''
              488  POP_TOP          
              490  JUMP_BACK           438  'to 438'
            492_0  COME_FROM           464  '464'

 L.1276       492  LOAD_FAST                'cid'
              494  LOAD_FAST                'chunks_multiple_allowed'
              496  <118>                 0  ''
          498_500  POP_JUMP_IF_FALSE   516  'to 516'

 L.1277       502  LOAD_FAST                'chunk'
              504  LOAD_FAST                'fp'
              506  LOAD_FAST                'cid'
              508  LOAD_FAST                'data'
              510  CALL_FUNCTION_3       3  ''
              512  POP_TOP          
              514  JUMP_BACK           438  'to 438'
            516_0  COME_FROM           498  '498'

 L.1278       516  LOAD_FAST                'cid'
              518  LOAD_CONST               1
              520  LOAD_CONST               2
              522  BUILD_SLICE_2         2 
              524  BINARY_SUBSCR    
              526  LOAD_METHOD              islower
              528  CALL_METHOD_0         0  ''
          530_532  POP_JUMP_IF_FALSE   438  'to 438'

 L.1280       534  LOAD_FAST                'info_chunk'
              536  LOAD_CONST               2
              538  LOAD_CONST               3
              540  BUILD_SLICE_2         2 
              542  BINARY_SUBSCR    
              544  STORE_FAST               'after_idat'

 L.1281       546  LOAD_FAST                'after_idat'
          548_550  POP_JUMP_IF_TRUE    438  'to 438'

 L.1282       552  LOAD_FAST                'chunk'
              554  LOAD_FAST                'fp'
              556  LOAD_FAST                'cid'
              558  LOAD_FAST                'data'
              560  CALL_FUNCTION_3       3  ''
              562  POP_TOP          
          564_566  JUMP_BACK           438  'to 438'
            568_0  COME_FROM           420  '420'

 L.1284       568  LOAD_FAST                'im'
              570  LOAD_ATTR                mode
              572  LOAD_STR                 'P'
              574  COMPARE_OP               ==
          576_578  POP_JUMP_IF_FALSE   646  'to 646'

 L.1285       580  LOAD_FAST                'colors'
              582  LOAD_CONST               3
              584  BINARY_MULTIPLY  
              586  STORE_FAST               'palette_byte_number'

 L.1286       588  LOAD_FAST                'im'
              590  LOAD_ATTR                im
              592  LOAD_METHOD              getpalette
              594  LOAD_STR                 'RGB'
              596  CALL_METHOD_1         1  ''
              598  LOAD_CONST               None
              600  LOAD_FAST                'palette_byte_number'
              602  BUILD_SLICE_2         2 
              604  BINARY_SUBSCR    
              606  STORE_FAST               'palette_bytes'

 L.1287       608  LOAD_GLOBAL              len
              610  LOAD_FAST                'palette_bytes'
              612  CALL_FUNCTION_1       1  ''
              614  LOAD_FAST                'palette_byte_number'
              616  COMPARE_OP               <
          618_620  POP_JUMP_IF_FALSE   634  'to 634'

 L.1288       622  LOAD_FAST                'palette_bytes'
              624  LOAD_CONST               b'\x00'
              626  INPLACE_ADD      
              628  STORE_FAST               'palette_bytes'
          630_632  JUMP_BACK           608  'to 608'
            634_0  COME_FROM           618  '618'

 L.1289       634  LOAD_FAST                'chunk'
              636  LOAD_FAST                'fp'
              638  LOAD_CONST               b'PLTE'
              640  LOAD_FAST                'palette_bytes'
              642  CALL_FUNCTION_3       3  ''
              644  POP_TOP          
            646_0  COME_FROM           576  '576'

 L.1291       646  LOAD_FAST                'im'
              648  LOAD_ATTR                encoderinfo
              650  LOAD_METHOD              get
              652  LOAD_STR                 'transparency'
              654  LOAD_FAST                'im'
              656  LOAD_ATTR                info
              658  LOAD_METHOD              get
              660  LOAD_STR                 'transparency'
              662  LOAD_CONST               None
              664  CALL_METHOD_2         2  ''
              666  CALL_METHOD_2         2  ''
              668  STORE_FAST               'transparency'

 L.1293       670  LOAD_FAST                'transparency'
          672_674  POP_JUMP_IF_TRUE    686  'to 686'
              676  LOAD_FAST                'transparency'
              678  LOAD_CONST               0
              680  COMPARE_OP               ==
          682_684  POP_JUMP_IF_FALSE   910  'to 910'
            686_0  COME_FROM           672  '672'

 L.1294       686  LOAD_FAST                'im'
              688  LOAD_ATTR                mode
              690  LOAD_STR                 'P'
              692  COMPARE_OP               ==
          694_696  POP_JUMP_IF_FALSE   786  'to 786'

 L.1296       698  LOAD_FAST                'colors'
              700  STORE_FAST               'alpha_bytes'

 L.1297       702  LOAD_GLOBAL              isinstance
              704  LOAD_FAST                'transparency'
              706  LOAD_GLOBAL              bytes
              708  CALL_FUNCTION_2       2  ''
          710_712  POP_JUMP_IF_FALSE   736  'to 736'

 L.1298       714  LOAD_FAST                'chunk'
              716  LOAD_FAST                'fp'
              718  LOAD_CONST               b'tRNS'
              720  LOAD_FAST                'transparency'
              722  LOAD_CONST               None
              724  LOAD_FAST                'alpha_bytes'
              726  BUILD_SLICE_2         2 
              728  BINARY_SUBSCR    
              730  CALL_FUNCTION_3       3  ''
              732  POP_TOP          
              734  JUMP_FORWARD        784  'to 784'
            736_0  COME_FROM           710  '710'

 L.1300       736  LOAD_GLOBAL              max
              738  LOAD_CONST               0
              740  LOAD_GLOBAL              min
              742  LOAD_CONST               255
              744  LOAD_FAST                'transparency'
              746  CALL_FUNCTION_2       2  ''
              748  CALL_FUNCTION_2       2  ''
              750  STORE_FAST               'transparency'

 L.1301       752  LOAD_CONST               b'\xff'
              754  LOAD_FAST                'transparency'
              756  BINARY_MULTIPLY  
              758  LOAD_CONST               b'\x00'
              760  BINARY_ADD       
              762  STORE_FAST               'alpha'

 L.1302       764  LOAD_FAST                'chunk'
              766  LOAD_FAST                'fp'
              768  LOAD_CONST               b'tRNS'
              770  LOAD_FAST                'alpha'
              772  LOAD_CONST               None
              774  LOAD_FAST                'alpha_bytes'
              776  BUILD_SLICE_2         2 
              778  BINARY_SUBSCR    
              780  CALL_FUNCTION_3       3  ''
              782  POP_TOP          
            784_0  COME_FROM           734  '734'
              784  JUMP_FORWARD        908  'to 908'
            786_0  COME_FROM           694  '694'

 L.1303       786  LOAD_FAST                'im'
              788  LOAD_ATTR                mode
              790  LOAD_CONST               ('1', 'L', 'I')
              792  <118>                 0  ''
          794_796  POP_JUMP_IF_FALSE   832  'to 832'

 L.1304       798  LOAD_GLOBAL              max
              800  LOAD_CONST               0
              802  LOAD_GLOBAL              min
              804  LOAD_CONST               65535
              806  LOAD_FAST                'transparency'
              808  CALL_FUNCTION_2       2  ''
              810  CALL_FUNCTION_2       2  ''
              812  STORE_FAST               'transparency'

 L.1305       814  LOAD_FAST                'chunk'
              816  LOAD_FAST                'fp'
              818  LOAD_CONST               b'tRNS'
              820  LOAD_GLOBAL              o16
              822  LOAD_FAST                'transparency'
              824  CALL_FUNCTION_1       1  ''
              826  CALL_FUNCTION_3       3  ''
              828  POP_TOP          
              830  JUMP_FORWARD        908  'to 908'
            832_0  COME_FROM           794  '794'

 L.1306       832  LOAD_FAST                'im'
              834  LOAD_ATTR                mode
              836  LOAD_STR                 'RGB'
              838  COMPARE_OP               ==
          840_842  POP_JUMP_IF_FALSE   888  'to 888'

 L.1307       844  LOAD_FAST                'transparency'
              846  UNPACK_SEQUENCE_3     3 
              848  STORE_FAST               'red'
              850  STORE_FAST               'green'
              852  STORE_FAST               'blue'

 L.1308       854  LOAD_FAST                'chunk'
              856  LOAD_FAST                'fp'
              858  LOAD_CONST               b'tRNS'
              860  LOAD_GLOBAL              o16
              862  LOAD_FAST                'red'
              864  CALL_FUNCTION_1       1  ''
              866  LOAD_GLOBAL              o16
              868  LOAD_FAST                'green'
              870  CALL_FUNCTION_1       1  ''
              872  BINARY_ADD       
              874  LOAD_GLOBAL              o16
              876  LOAD_FAST                'blue'
              878  CALL_FUNCTION_1       1  ''
              880  BINARY_ADD       
              882  CALL_FUNCTION_3       3  ''
              884  POP_TOP          
              886  JUMP_FORWARD        908  'to 908'
            888_0  COME_FROM           840  '840'

 L.1310       888  LOAD_STR                 'transparency'
              890  LOAD_FAST                'im'
              892  LOAD_ATTR                encoderinfo
              894  <118>                 0  ''
          896_898  POP_JUMP_IF_FALSE   976  'to 976'

 L.1313       900  LOAD_GLOBAL              OSError
              902  LOAD_STR                 'cannot use transparency for this mode'
              904  CALL_FUNCTION_1       1  ''
              906  RAISE_VARARGS_1       1  'exception instance'
            908_0  COME_FROM           886  '886'
            908_1  COME_FROM           830  '830'
            908_2  COME_FROM           784  '784'
              908  JUMP_FORWARD        976  'to 976'
            910_0  COME_FROM           682  '682'

 L.1315       910  LOAD_FAST                'im'
              912  LOAD_ATTR                mode
              914  LOAD_STR                 'P'
              916  COMPARE_OP               ==
          918_920  POP_JUMP_IF_FALSE   976  'to 976'
              922  LOAD_FAST                'im'
              924  LOAD_ATTR                im
              926  LOAD_METHOD              getpalettemode
              928  CALL_METHOD_0         0  ''
              930  LOAD_STR                 'RGBA'
              932  COMPARE_OP               ==
          934_936  POP_JUMP_IF_FALSE   976  'to 976'

 L.1316       938  LOAD_FAST                'im'
              940  LOAD_ATTR                im
              942  LOAD_METHOD              getpalette
              944  LOAD_STR                 'RGBA'
              946  LOAD_STR                 'A'
              948  CALL_METHOD_2         2  ''
              950  STORE_FAST               'alpha'

 L.1317       952  LOAD_FAST                'colors'
              954  STORE_FAST               'alpha_bytes'

 L.1318       956  LOAD_FAST                'chunk'
              958  LOAD_FAST                'fp'
              960  LOAD_CONST               b'tRNS'
              962  LOAD_FAST                'alpha'
              964  LOAD_CONST               None
              966  LOAD_FAST                'alpha_bytes'
              968  BUILD_SLICE_2         2 
              970  BINARY_SUBSCR    
              972  CALL_FUNCTION_3       3  ''
              974  POP_TOP          
            976_0  COME_FROM           934  '934'
            976_1  COME_FROM           918  '918'
            976_2  COME_FROM           908  '908'
            976_3  COME_FROM           896  '896'

 L.1320       976  LOAD_FAST                'im'
              978  LOAD_ATTR                encoderinfo
              980  LOAD_METHOD              get
              982  LOAD_STR                 'dpi'
              984  CALL_METHOD_1         1  ''
              986  STORE_FAST               'dpi'

 L.1321       988  LOAD_FAST                'dpi'
          990_992  POP_JUMP_IF_FALSE  1050  'to 1050'

 L.1322       994  LOAD_FAST                'chunk'

 L.1323       996  LOAD_FAST                'fp'

 L.1324       998  LOAD_CONST               b'pHYs'

 L.1325      1000  LOAD_GLOBAL              o32
             1002  LOAD_GLOBAL              int
             1004  LOAD_FAST                'dpi'
             1006  LOAD_CONST               0
             1008  BINARY_SUBSCR    
             1010  LOAD_CONST               0.0254
             1012  BINARY_TRUE_DIVIDE
             1014  LOAD_CONST               0.5
             1016  BINARY_ADD       
             1018  CALL_FUNCTION_1       1  ''
             1020  CALL_FUNCTION_1       1  ''

 L.1326      1022  LOAD_GLOBAL              o32
             1024  LOAD_GLOBAL              int
             1026  LOAD_FAST                'dpi'
             1028  LOAD_CONST               1
             1030  BINARY_SUBSCR    
             1032  LOAD_CONST               0.0254
             1034  BINARY_TRUE_DIVIDE
             1036  LOAD_CONST               0.5
             1038  BINARY_ADD       
             1040  CALL_FUNCTION_1       1  ''
             1042  CALL_FUNCTION_1       1  ''

 L.1327      1044  LOAD_CONST               b'\x01'

 L.1322      1046  CALL_FUNCTION_5       5  ''
             1048  POP_TOP          
           1050_0  COME_FROM           990  '990'

 L.1330      1050  LOAD_FAST                'info'
         1052_1054  POP_JUMP_IF_FALSE  1126  'to 1126'

 L.1331      1056  LOAD_CONST               b'bKGD'
             1058  LOAD_CONST               b'hIST'
             1060  BUILD_LIST_2          2 
             1062  STORE_FAST               'chunks'

 L.1332      1064  LOAD_FAST                'info'
             1066  LOAD_ATTR                chunks
             1068  GET_ITER         
           1070_0  COME_FROM          1096  '1096'
             1070  FOR_ITER           1126  'to 1126'
             1072  STORE_FAST               'info_chunk'

 L.1333      1074  LOAD_FAST                'info_chunk'
             1076  LOAD_CONST               None
             1078  LOAD_CONST               2
             1080  BUILD_SLICE_2         2 
             1082  BINARY_SUBSCR    
             1084  UNPACK_SEQUENCE_2     2 
             1086  STORE_FAST               'cid'
             1088  STORE_FAST               'data'

 L.1334      1090  LOAD_FAST                'cid'
             1092  LOAD_FAST                'chunks'
             1094  <118>                 0  ''
         1096_1098  POP_JUMP_IF_FALSE  1070  'to 1070'

 L.1335      1100  LOAD_FAST                'chunks'
             1102  LOAD_METHOD              remove
             1104  LOAD_FAST                'cid'
             1106  CALL_METHOD_1         1  ''
             1108  POP_TOP          

 L.1336      1110  LOAD_FAST                'chunk'
             1112  LOAD_FAST                'fp'
             1114  LOAD_FAST                'cid'
             1116  LOAD_FAST                'data'
             1118  CALL_FUNCTION_3       3  ''
             1120  POP_TOP          
         1122_1124  JUMP_BACK          1070  'to 1070'
           1126_0  COME_FROM          1052  '1052'

 L.1338      1126  LOAD_FAST                'im'
             1128  LOAD_ATTR                encoderinfo
             1130  LOAD_METHOD              get
             1132  LOAD_STR                 'exif'
             1134  LOAD_FAST                'im'
             1136  LOAD_ATTR                info
             1138  LOAD_METHOD              get
             1140  LOAD_STR                 'exif'
             1142  CALL_METHOD_1         1  ''
             1144  CALL_METHOD_2         2  ''
             1146  STORE_FAST               'exif'

 L.1339      1148  LOAD_FAST                'exif'
         1150_1152  POP_JUMP_IF_FALSE  1214  'to 1214'

 L.1340      1154  LOAD_GLOBAL              isinstance
             1156  LOAD_FAST                'exif'
             1158  LOAD_GLOBAL              Image
             1160  LOAD_ATTR                Exif
             1162  CALL_FUNCTION_2       2  ''
         1164_1166  POP_JUMP_IF_FALSE  1178  'to 1178'

 L.1341      1168  LOAD_FAST                'exif'
             1170  LOAD_METHOD              tobytes
             1172  LOAD_CONST               8
             1174  CALL_METHOD_1         1  ''
             1176  STORE_FAST               'exif'
           1178_0  COME_FROM          1164  '1164'

 L.1342      1178  LOAD_FAST                'exif'
             1180  LOAD_METHOD              startswith
             1182  LOAD_CONST               b'Exif\x00\x00'
             1184  CALL_METHOD_1         1  ''
         1186_1188  POP_JUMP_IF_FALSE  1202  'to 1202'

 L.1343      1190  LOAD_FAST                'exif'
             1192  LOAD_CONST               6
             1194  LOAD_CONST               None
             1196  BUILD_SLICE_2         2 
             1198  BINARY_SUBSCR    
             1200  STORE_FAST               'exif'
           1202_0  COME_FROM          1186  '1186'

 L.1344      1202  LOAD_FAST                'chunk'
             1204  LOAD_FAST                'fp'
             1206  LOAD_CONST               b'eXIf'
             1208  LOAD_FAST                'exif'
             1210  CALL_FUNCTION_3       3  ''
             1212  POP_TOP          
           1214_0  COME_FROM          1150  '1150'

 L.1346      1214  LOAD_FAST                'save_all'
         1216_1218  POP_JUMP_IF_FALSE  1236  'to 1236'

 L.1347      1220  LOAD_GLOBAL              _write_multiple_frames
             1222  LOAD_FAST                'im'
             1224  LOAD_FAST                'fp'
             1226  LOAD_FAST                'chunk'
             1228  LOAD_FAST                'rawmode'
             1230  CALL_FUNCTION_4       4  ''
             1232  POP_TOP          
             1234  JUMP_FORWARD       1272  'to 1272'
           1236_0  COME_FROM          1216  '1216'

 L.1349      1236  LOAD_GLOBAL              ImageFile
             1238  LOAD_METHOD              _save
             1240  LOAD_FAST                'im'
             1242  LOAD_GLOBAL              _idat
             1244  LOAD_FAST                'fp'
             1246  LOAD_FAST                'chunk'
             1248  CALL_FUNCTION_2       2  ''
             1250  LOAD_STR                 'zip'
             1252  LOAD_CONST               (0, 0)
             1254  LOAD_FAST                'im'
             1256  LOAD_ATTR                size
             1258  BINARY_ADD       
             1260  LOAD_CONST               0
             1262  LOAD_FAST                'rawmode'
             1264  BUILD_TUPLE_4         4 
             1266  BUILD_LIST_1          1 
             1268  CALL_METHOD_3         3  ''
             1270  POP_TOP          
           1272_0  COME_FROM          1234  '1234'

 L.1351      1272  LOAD_FAST                'info'
         1274_1276  POP_JUMP_IF_FALSE  1356  'to 1356'

 L.1352      1278  LOAD_FAST                'info'
             1280  LOAD_ATTR                chunks
             1282  GET_ITER         
           1284_0  COME_FROM          1336  '1336'
           1284_1  COME_FROM          1318  '1318'
             1284  FOR_ITER           1356  'to 1356'
             1286  STORE_FAST               'info_chunk'

 L.1353      1288  LOAD_FAST                'info_chunk'
             1290  LOAD_CONST               None
             1292  LOAD_CONST               2
             1294  BUILD_SLICE_2         2 
             1296  BINARY_SUBSCR    
             1298  UNPACK_SEQUENCE_2     2 
             1300  STORE_FAST               'cid'
             1302  STORE_FAST               'data'

 L.1354      1304  LOAD_FAST                'cid'
             1306  LOAD_CONST               1
             1308  LOAD_CONST               2
             1310  BUILD_SLICE_2         2 
             1312  BINARY_SUBSCR    
             1314  LOAD_METHOD              islower
             1316  CALL_METHOD_0         0  ''
         1318_1320  POP_JUMP_IF_FALSE  1284  'to 1284'

 L.1356      1322  LOAD_FAST                'info_chunk'
             1324  LOAD_CONST               2
             1326  LOAD_CONST               3
             1328  BUILD_SLICE_2         2 
             1330  BINARY_SUBSCR    
             1332  STORE_FAST               'after_idat'

 L.1357      1334  LOAD_FAST                'after_idat'
         1336_1338  POP_JUMP_IF_FALSE  1284  'to 1284'

 L.1358      1340  LOAD_FAST                'chunk'
             1342  LOAD_FAST                'fp'
             1344  LOAD_FAST                'cid'
             1346  LOAD_FAST                'data'
             1348  CALL_FUNCTION_3       3  ''
             1350  POP_TOP          
         1352_1354  JUMP_BACK          1284  'to 1284'
           1356_0  COME_FROM          1274  '1274'

 L.1360      1356  LOAD_FAST                'chunk'
             1358  LOAD_FAST                'fp'
             1360  LOAD_CONST               b'IEND'
             1362  LOAD_CONST               b''
             1364  CALL_FUNCTION_3       3  ''
             1366  POP_TOP          

 L.1362      1368  LOAD_GLOBAL              hasattr
             1370  LOAD_FAST                'fp'
             1372  LOAD_STR                 'flush'
             1374  CALL_FUNCTION_2       2  ''
         1376_1378  POP_JUMP_IF_FALSE  1388  'to 1388'

 L.1363      1380  LOAD_FAST                'fp'
             1382  LOAD_METHOD              flush
             1384  CALL_METHOD_0         0  ''
             1386  POP_TOP          
           1388_0  COME_FROM          1376  '1376'

Parse error at or near `<118>' instruction at offset 20


def getchunks--- This code section failed: ---

 L.1373         0  LOAD_BUILD_CLASS 
                2  LOAD_CODE                <code_object collector>
                4  LOAD_STR                 'collector'
                6  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                8  LOAD_STR                 'collector'
               10  CALL_FUNCTION_2       2  ''
               12  STORE_FAST               'collector'

 L.1382        14  LOAD_CODE                <code_object append>
               16  LOAD_STR                 'getchunks.<locals>.append'
               18  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               20  STORE_FAST               'append'

 L.1387        22  LOAD_FAST                'collector'
               24  CALL_FUNCTION_0       0  ''
               26  STORE_FAST               'fp'

 L.1389        28  SETUP_FINALLY        58  'to 58'

 L.1390        30  LOAD_FAST                'params'
               32  LOAD_FAST                'im'
               34  STORE_ATTR               encoderinfo

 L.1391        36  LOAD_GLOBAL              _save
               38  LOAD_FAST                'im'
               40  LOAD_FAST                'fp'
               42  LOAD_CONST               None
               44  LOAD_FAST                'append'
               46  CALL_FUNCTION_4       4  ''
               48  POP_TOP          
               50  POP_BLOCK        

 L.1393        52  LOAD_FAST                'im'
               54  DELETE_ATTR              encoderinfo
               56  JUMP_FORWARD         64  'to 64'
             58_0  COME_FROM_FINALLY    28  '28'
               58  LOAD_FAST                'im'
               60  DELETE_ATTR              encoderinfo
               62  <48>             
             64_0  COME_FROM            56  '56'

 L.1395        64  LOAD_FAST                'fp'
               66  LOAD_ATTR                data
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 52


Image.register_open(PngImageFile.format, PngImageFile, _accept)
Image.register_save(PngImageFile.format, _save)
Image.register_save_all(PngImageFile.format, _save_all)
Image.register_extensions(PngImageFile.format, ['.png', '.apng'])
Image.register_mime(PngImageFile.format, 'image/png')