# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\IptcImagePlugin.py
import os, tempfile
from . import Image, ImageFile
from ._binary import i8, i16be as i16, i32be as i32, o8
COMPRESSION = {1:'raw', 
 5:'jpeg'}
PAD = o8(0) * 4

def i(c):
    return i32((PAD + c)[-4:])


def dump(c):
    for i in c:
        print(('%02x' % i8(i)), end=' ')
    else:
        print()


class IptcImageFile(ImageFile.ImageFile):
    format = 'IPTC'
    format_description = 'IPTC/NAA'

    def getint(self, key):
        return i(self.info[key])

    def field(self):
        s = self.fp.read(5)
        if not len(s):
            return (None, 0)
        tag = (i8(s[1]), i8(s[2]))
        if not i8(s[0]) != 28:
            if tag[0] < 1 or (tag[0] > 9):
                raise SyntaxError('invalid IPTC/NAA file')
            size = i8(s[3])
            if size > 132:
                raise OSError('illegal field length in IPTC/NAA file')
            elif size == 128:
                size = 0
            elif size > 128:
                size = i(self.fp.read(size - 128))
            else:
                size = i16(s[3:])
            return (
             tag, size)

    def _open--- This code section failed: ---
              0_0  COME_FROM           134  '134'
              0_1  COME_FROM           122  '122'

 L.  85         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              tell
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'offset'

 L.  86        10  LOAD_FAST                'self'
               12  LOAD_METHOD              field
               14  CALL_METHOD_0         0  ''
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'tag'
               20  STORE_FAST               'size'

 L.  87        22  LOAD_FAST                'tag'
               24  POP_JUMP_IF_FALSE   136  'to 136'
               26  LOAD_FAST                'tag'
               28  LOAD_CONST               (8, 10)
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    36  'to 36'

 L.  88        34  JUMP_FORWARD        136  'to 136'
             36_0  COME_FROM            32  '32'

 L.  89        36  LOAD_FAST                'size'
               38  POP_JUMP_IF_FALSE    54  'to 54'

 L.  90        40  LOAD_FAST                'self'
               42  LOAD_ATTR                fp
               44  LOAD_METHOD              read
               46  LOAD_FAST                'size'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'tagdata'
               52  JUMP_FORWARD         58  'to 58'
             54_0  COME_FROM            38  '38'

 L.  92        54  LOAD_CONST               None
               56  STORE_FAST               'tagdata'
             58_0  COME_FROM            52  '52'

 L.  93        58  LOAD_FAST                'tag'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                info
               64  COMPARE_OP               in
               66  POP_JUMP_IF_FALSE   124  'to 124'

 L.  94        68  LOAD_GLOBAL              isinstance
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                info
               74  LOAD_FAST                'tag'
               76  BINARY_SUBSCR    
               78  LOAD_GLOBAL              list
               80  CALL_FUNCTION_2       2  ''
               82  POP_JUMP_IF_FALSE   102  'to 102'

 L.  95        84  LOAD_FAST                'self'
               86  LOAD_ATTR                info
               88  LOAD_FAST                'tag'
               90  BINARY_SUBSCR    
               92  LOAD_METHOD              append
               94  LOAD_FAST                'tagdata'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
              100  JUMP_FORWARD        134  'to 134'
            102_0  COME_FROM            82  '82'

 L.  97       102  LOAD_FAST                'self'
              104  LOAD_ATTR                info
              106  LOAD_FAST                'tag'
              108  BINARY_SUBSCR    
              110  LOAD_FAST                'tagdata'
              112  BUILD_LIST_2          2 
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                info
              118  LOAD_FAST                'tag'
              120  STORE_SUBSCR     
              122  JUMP_BACK             0  'to 0'
            124_0  COME_FROM            66  '66'

 L.  99       124  LOAD_FAST                'tagdata'
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                info
              130  LOAD_FAST                'tag'
              132  STORE_SUBSCR     
            134_0  COME_FROM           100  '100'
              134  JUMP_BACK             0  'to 0'
            136_0  COME_FROM            34  '34'
            136_1  COME_FROM            24  '24'

 L. 102       136  LOAD_GLOBAL              i8
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                info
              142  LOAD_CONST               (3, 60)
              144  BINARY_SUBSCR    
              146  LOAD_CONST               0
              148  BINARY_SUBSCR    
              150  CALL_FUNCTION_1       1  ''
              152  STORE_FAST               'layers'

 L. 103       154  LOAD_GLOBAL              i8
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                info
              160  LOAD_CONST               (3, 60)
              162  BINARY_SUBSCR    
              164  LOAD_CONST               1
              166  BINARY_SUBSCR    
              168  CALL_FUNCTION_1       1  ''
              170  STORE_FAST               'component'

 L. 104       172  LOAD_CONST               (3, 65)
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                info
              178  COMPARE_OP               in
              180  POP_JUMP_IF_FALSE   206  'to 206'

 L. 105       182  LOAD_GLOBAL              i8
              184  LOAD_FAST                'self'
              186  LOAD_ATTR                info
              188  LOAD_CONST               (3, 65)
              190  BINARY_SUBSCR    
              192  LOAD_CONST               0
              194  BINARY_SUBSCR    
              196  CALL_FUNCTION_1       1  ''
              198  LOAD_CONST               1
              200  BINARY_SUBTRACT  
              202  STORE_FAST               'id'
              204  JUMP_FORWARD        210  'to 210'
            206_0  COME_FROM           180  '180'

 L. 107       206  LOAD_CONST               0
              208  STORE_FAST               'id'
            210_0  COME_FROM           204  '204'

 L. 108       210  LOAD_FAST                'layers'
              212  LOAD_CONST               1
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE   230  'to 230'
              218  LOAD_FAST                'component'
              220  POP_JUMP_IF_TRUE    230  'to 230'

 L. 109       222  LOAD_STR                 'L'
              224  LOAD_FAST                'self'
              226  STORE_ATTR               mode
              228  JUMP_FORWARD        280  'to 280'
            230_0  COME_FROM           220  '220'
            230_1  COME_FROM           216  '216'

 L. 110       230  LOAD_FAST                'layers'
              232  LOAD_CONST               3
              234  COMPARE_OP               ==
              236  POP_JUMP_IF_FALSE   254  'to 254'
              238  LOAD_FAST                'component'
              240  POP_JUMP_IF_FALSE   254  'to 254'

 L. 111       242  LOAD_STR                 'RGB'
              244  LOAD_FAST                'id'
              246  BINARY_SUBSCR    
              248  LOAD_FAST                'self'
              250  STORE_ATTR               mode
              252  JUMP_FORWARD        280  'to 280'
            254_0  COME_FROM           240  '240'
            254_1  COME_FROM           236  '236'

 L. 112       254  LOAD_FAST                'layers'
              256  LOAD_CONST               4
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_FALSE   280  'to 280'
              264  LOAD_FAST                'component'
          266_268  POP_JUMP_IF_FALSE   280  'to 280'

 L. 113       270  LOAD_STR                 'CMYK'
              272  LOAD_FAST                'id'
              274  BINARY_SUBSCR    
              276  LOAD_FAST                'self'
              278  STORE_ATTR               mode
            280_0  COME_FROM           266  '266'
            280_1  COME_FROM           260  '260'
            280_2  COME_FROM           252  '252'
            280_3  COME_FROM           228  '228'

 L. 116       280  LOAD_FAST                'self'
              282  LOAD_METHOD              getint
              284  LOAD_CONST               (3, 20)
              286  CALL_METHOD_1         1  ''
              288  LOAD_FAST                'self'
              290  LOAD_METHOD              getint
              292  LOAD_CONST               (3, 30)
              294  CALL_METHOD_1         1  ''
              296  BUILD_TUPLE_2         2 
              298  LOAD_FAST                'self'
              300  STORE_ATTR               _size

 L. 119       302  SETUP_FINALLY       322  'to 322'

 L. 120       304  LOAD_GLOBAL              COMPRESSION
              306  LOAD_FAST                'self'
              308  LOAD_METHOD              getint
              310  LOAD_CONST               (3, 120)
              312  CALL_METHOD_1         1  ''
              314  BINARY_SUBSCR    
              316  STORE_FAST               'compression'
              318  POP_BLOCK        
              320  JUMP_FORWARD        368  'to 368'
            322_0  COME_FROM_FINALLY   302  '302'

 L. 121       322  DUP_TOP          
              324  LOAD_GLOBAL              KeyError
              326  COMPARE_OP               exception-match
          328_330  POP_JUMP_IF_FALSE   366  'to 366'
              332  POP_TOP          
              334  STORE_FAST               'e'
              336  POP_TOP          
              338  SETUP_FINALLY       354  'to 354'

 L. 122       340  LOAD_GLOBAL              OSError
              342  LOAD_STR                 'Unknown IPTC image compression'
              344  CALL_FUNCTION_1       1  ''
              346  LOAD_FAST                'e'
              348  RAISE_VARARGS_2       2  'exception instance with __cause__'
              350  POP_BLOCK        
              352  BEGIN_FINALLY    
            354_0  COME_FROM_FINALLY   338  '338'
              354  LOAD_CONST               None
              356  STORE_FAST               'e'
              358  DELETE_FAST              'e'
              360  END_FINALLY      
              362  POP_EXCEPT       
              364  JUMP_FORWARD        368  'to 368'
            366_0  COME_FROM           328  '328'
              366  END_FINALLY      
            368_0  COME_FROM           364  '364'
            368_1  COME_FROM           320  '320'

 L. 125       368  LOAD_FAST                'tag'
              370  LOAD_CONST               (8, 10)
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   416  'to 416'

 L. 127       378  LOAD_STR                 'iptc'
              380  LOAD_FAST                'compression'
              382  LOAD_FAST                'offset'
              384  BUILD_TUPLE_2         2 
              386  LOAD_CONST               0
              388  LOAD_CONST               0
              390  LOAD_FAST                'self'
              392  LOAD_ATTR                size
              394  LOAD_CONST               0
              396  BINARY_SUBSCR    
              398  LOAD_FAST                'self'
              400  LOAD_ATTR                size
              402  LOAD_CONST               1
              404  BINARY_SUBSCR    
              406  BUILD_TUPLE_4         4 
              408  BUILD_TUPLE_3         3 

 L. 126       410  BUILD_LIST_1          1 
              412  LOAD_FAST                'self'
              414  STORE_ATTR               tile
            416_0  COME_FROM           374  '374'

Parse error at or near `STORE_ATTR' instruction at offset 414

    def load(self):
        if len(self.tile) != 1 or (self.tile[0][0] != 'iptc'):
            return ImageFile.ImageFile.load(self)
        type, tile, box = self.tile[0]
        encoding, offset = tile
        self.fp.seek(offset)
        o_fd, outfile = tempfile.mkstemp(text=False)
        o = os.fdopen(o_fd)
        if encoding == 'raw':
            o.write('P5\n%d %d\n255\n' % self.size)
            while True:
                type, size = self.field
                if type != (8, 10):
                    pass
                else:
                    while True:
                        if size > 0:
                            s = self.fp.read(minsize8192)
                            if not s:
                                pass
                            else:
                                o.write(s)
                                size -= len(s)

        o.close
        try:
            with Image.open(outfile) as _im:
                _im.load
                self.im = _im.im
        finally:
            try:
                os.unlink(outfile)
            except OSError:
                pass


Image.register_open(IptcImageFile.format, IptcImageFile)
Image.register_extension(IptcImageFile.format, '.iim')

def getiptcinfo(im):
    """
    Get IPTC information from TIFF, JPEG, or IPTC file.

    :param im: An image containing IPTC data.
    :returns: A dictionary containing IPTC information, or None if
        no IPTC information block was found.
    """
    from . import TiffImagePlugin, JpegImagePlugin
    import io
    data = None
    if isinstanceimIptcImageFile:
        return im.info
    if isinstanceimJpegImagePlugin.JpegImageFile:
        photoshop = im.info.get('photoshop')
        if photoshop:
            data = photoshop.get(1028)
    else:
        pass
    if isinstanceimTiffImagePlugin.TiffImageFile:
        try:
            data = im.tag.tagdata[TiffImagePlugin.IPTC_NAA_CHUNK]
        except (AttributeError, KeyError):
            pass
        else:
            if data is None:
                return

    class FakeImage:
        pass

    im = FakeImage()
    im.__class__ = IptcImageFile
    im.info = {}
    im.fp = io.BytesIO(data)
    try:
        im._open
    except (IndexError, KeyError):
        pass
    else:
        return im.info