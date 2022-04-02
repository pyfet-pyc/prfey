# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\SpiderImagePlugin.py
import os, struct, sys
from PIL import Image, ImageFile

def isInt--- This code section failed: ---

 L.  43         0  SETUP_FINALLY        38  'to 38'

 L.  44         2  LOAD_GLOBAL              int
                4  LOAD_FAST                'f'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'i'

 L.  45        10  LOAD_FAST                'f'
               12  LOAD_FAST                'i'
               14  BINARY_SUBTRACT  
               16  LOAD_CONST               0
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L.  46        22  POP_BLOCK        
               24  LOAD_CONST               1
               26  RETURN_VALUE     
             28_0  COME_FROM            20  '20'

 L.  48        28  POP_BLOCK        
               30  LOAD_CONST               0
               32  RETURN_VALUE     
               34  POP_BLOCK        
               36  JUMP_FORWARD         64  'to 64'
             38_0  COME_FROM_FINALLY     0  '0'

 L.  49        38  DUP_TOP          
               40  LOAD_GLOBAL              ValueError
               42  LOAD_GLOBAL              OverflowError
               44  BUILD_TUPLE_2         2 
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    62  'to 62'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L.  50        56  POP_EXCEPT       
               58  LOAD_CONST               0
               60  RETURN_VALUE     
             62_0  COME_FROM            48  '48'
               62  END_FINALLY      
             64_0  COME_FROM            36  '36'

Parse error at or near `LOAD_CONST' instruction at offset 24


iforms = [
 1, 3, -11, -12, -21, -22]

def isSpiderHeader(t):
    h = (99, ) + t
    for i in (1, 2, 5, 12, 13, 22, 23):
        if not isInt(h[i]):
            return 0
        iform = int(h[5])
        if iform not in iforms:
            return 0
        labrec = int(h[13])
        labbyt = int(h[22])
        lenbyt = int(h[23])
        if labbyt != labrec * lenbyt:
            return 0
        return labbyt


def isSpiderImage(filename):
    with open(filename, 'rb') as (fp):
        f = fp.read(92)
    t = struct.unpack('>23f', f)
    hdrlen = isSpiderHeader(t)
    if hdrlen == 0:
        t = struct.unpack('<23f', f)
        hdrlen = isSpiderHeader(t)
    return hdrlen


class SpiderImageFile(ImageFile.ImageFile):
    format = 'SPIDER'
    format_description = 'Spider 2D image'
    _close_exclusive_fp_after_loading = False

    def _open(self):
        n = 108
        f = self.fp.read(n)
        try:
            self.bigendian = 1
            t = struct.unpack('>27f', f)
            hdrlen = isSpiderHeader(t)
            if hdrlen == 0:
                self.bigendian = 0
                t = struct.unpack('<27f', f)
                hdrlen = isSpiderHeader(t)
            if hdrlen == 0:
                raise SyntaxError('not a valid Spider file')
        except struct.error as e:
            try:
                raise SyntaxError('not a valid Spider file') from e
            finally:
                e = None
                del e

        else:
            h = (99, ) + t
            iform = int(h[5])
            if iform != 1:
                raise SyntaxError('not a Spider 2D image')
            self._size = (int(h[12]), int(h[2]))
            self.istack = int(h[24])
            self.imgnumber = int(h[27])
        if self.istack == 0 and self.imgnumber == 0:
            offset = hdrlen
            self._nimages = 1
        else:
            if self.istack > 0 and self.imgnumber == 0:
                self.imgbytes = int(h[12]) * int(h[2]) * 4
                self.hdrlen = hdrlen
                self._nimages = int(h[26])
                offset = hdrlen * 2
                self.imgnumber = 1
            else:
                if self.istack == 0:
                    if self.imgnumber > 0:
                        offset = hdrlen + self.stkoffset
                        self.istack = 2
                    else:
                        raise SyntaxError('inconsistent stack header values')
                elif self.bigendian:
                    self.rawmode = 'F;32BF'
                else:
                    self.rawmode = 'F;32F'
                self.mode = 'F'
                self.tile = [
                 (
                  'raw', (0, 0) + self.size, offset, (self.rawmode, 0, 1))]
                self._SpiderImageFile__fp = self.fp

    @property
    def n_frames(self):
        return self._nimages

    @property
    def is_animated(self):
        return self._nimages > 1

    def tell(self):
        if self.imgnumber < 1:
            return 0
        return self.imgnumber - 1

    def seek(self, frame):
        if self.istack == 0:
            raise EOFError('attempt to seek in a non-stack file')
        else:
            return self._seek_check(frame) or None
        self.stkoffset = self.hdrlen + frame * (self.hdrlen + self.imgbytes)
        self.fp = self._SpiderImageFile__fp
        self.fp.seek(self.stkoffset)
        self._open()

    def convert2byte(self, depth=255):
        minimum, maximum = self.getextrema()
        m = 1
        if maximum != minimum:
            m = depth / (maximum - minimum)
        b = -m * minimum
        return self.point(lambda i, m=m, b=b: i * m + b).convert('L')

    def tkPhotoImage(self):
        from PIL import ImageTk
        return ImageTk.PhotoImage((self.convert2byte()), palette=256)

    def _close__fp(self):
        try:
            try:
                if self._SpiderImageFile__fp != self.fp:
                    self._SpiderImageFile__fp.close()
            except AttributeError:
                pass

        finally:
            self._SpiderImageFile__fp = None


def loadImageSeries--- This code section failed: ---

 L. 210         0  LOAD_FAST                'filelist'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_TRUE     20  'to 20'
                8  LOAD_GLOBAL              len
               10  LOAD_FAST                'filelist'
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_CONST               1
               16  COMPARE_OP               <
               18  POP_JUMP_IF_FALSE    24  'to 24'
             20_0  COME_FROM             6  '6'

 L. 211        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 213        24  BUILD_LIST_0          0 
               26  STORE_FAST               'imglist'

 L. 214        28  LOAD_FAST                'filelist'
               30  GET_ITER         
               32  FOR_ITER            166  'to 166'
               34  STORE_FAST               'img'

 L. 215        36  LOAD_GLOBAL              os
               38  LOAD_ATTR                path
               40  LOAD_METHOD              exists
               42  LOAD_FAST                'img'
               44  CALL_METHOD_1         1  ''
               46  POP_JUMP_IF_TRUE     64  'to 64'

 L. 216        48  LOAD_GLOBAL              print
               50  LOAD_STR                 'unable to find '
               52  LOAD_FAST                'img'
               54  FORMAT_VALUE          0  ''
               56  BUILD_STRING_2        2 
               58  CALL_FUNCTION_1       1  ''
               60  POP_TOP          

 L. 217        62  JUMP_BACK            32  'to 32'
             64_0  COME_FROM            46  '46'

 L. 218        64  SETUP_FINALLY       100  'to 100'

 L. 219        66  LOAD_GLOBAL              Image
               68  LOAD_METHOD              open
               70  LOAD_FAST                'img'
               72  CALL_METHOD_1         1  ''
               74  SETUP_WITH           90  'to 90'
               76  STORE_FAST               'im'

 L. 220        78  LOAD_FAST                'im'
               80  LOAD_METHOD              convert2byte
               82  CALL_METHOD_0         0  ''
               84  STORE_FAST               'im'
               86  POP_BLOCK        
               88  BEGIN_FINALLY    
             90_0  COME_FROM_WITH       74  '74'
               90  WITH_CLEANUP_START
               92  WITH_CLEANUP_FINISH
               94  END_FINALLY      
               96  POP_BLOCK        
               98  JUMP_FORWARD        144  'to 144'
            100_0  COME_FROM_FINALLY    64  '64'

 L. 221       100  DUP_TOP          
              102  LOAD_GLOBAL              Exception
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   142  'to 142'
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 222       114  LOAD_GLOBAL              isSpiderImage
              116  LOAD_FAST                'img'
              118  CALL_FUNCTION_1       1  ''
              120  POP_JUMP_IF_TRUE    134  'to 134'

 L. 223       122  LOAD_GLOBAL              print
              124  LOAD_FAST                'img'
              126  LOAD_STR                 ' is not a Spider image file'
              128  BINARY_ADD       
              130  CALL_FUNCTION_1       1  ''
              132  POP_TOP          
            134_0  COME_FROM           120  '120'

 L. 224       134  POP_EXCEPT       
              136  JUMP_BACK            32  'to 32'
              138  POP_EXCEPT       
              140  JUMP_FORWARD        144  'to 144'
            142_0  COME_FROM           106  '106'
              142  END_FINALLY      
            144_0  COME_FROM           140  '140'
            144_1  COME_FROM            98  '98'

 L. 225       144  LOAD_FAST                'img'
              146  LOAD_FAST                'im'
              148  LOAD_ATTR                info
              150  LOAD_STR                 'filename'
              152  STORE_SUBSCR     

 L. 226       154  LOAD_FAST                'imglist'
              156  LOAD_METHOD              append
              158  LOAD_FAST                'im'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
              164  JUMP_BACK            32  'to 32'

 L. 227       166  LOAD_FAST                'imglist'
              168  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 138


def makeSpiderHeader(im):
    nsam, nrow = im.size
    lenbyt = nsam * 4
    labrec = int(1024 / lenbyt)
    if 1024 % lenbyt != 0:
        labrec += 1
    labbyt = labrec * lenbyt
    hdr = []
    nvalues = int(labbyt / 4)
    for i in range(nvalues):
        hdr.append(0.0)
    else:
        if len(hdr) < 23:
            return []
        hdr[1] = 1.0
        hdr[2] = float(nrow)
        hdr[5] = 1.0
        hdr[12] = float(nsam)
        hdr[13] = float(labrec)
        hdr[22] = float(labbyt)
        hdr[23] = float(lenbyt)
        hdr = hdr[1:]
        hdr.append(0.0)
        hdrstr = []
        for v in hdr:
            hdrstr.append(struct.pack('f', v))
        else:
            return hdrstr


def _save(im, fp, filename):
    if im.mode[0] != 'F':
        im = im.convert('F')
    hdr = makeSpiderHeader(im)
    if len(hdr) < 256:
        raise OSError('Error creating Spider header')
    fp.writelines(hdr)
    rawmode = 'F;32NF'
    ImageFile._save(im, fp, [('raw', (0, 0) + im.size, 0, (rawmode, 0, 1))])


def _save_spider(im, fp, filename):
    ext = os.path.splitext(filename)[1]
    Image.register_extension(SpiderImageFile.format, ext)
    _save(im, fp, filename)


Image.register_open(SpiderImageFile.format, SpiderImageFile)
Image.register_save(SpiderImageFile.format, _save_spider)
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Syntax: python SpiderImagePlugin.py [infile] [outfile]')
        sys.exit()
    filename = sys.argv[1]
    if not isSpiderImage(filename):
        print('input image must be in Spider format')
        sys.exit()
    with Image.open(filename) as (im):
        print('image: ' + str(im))
        print('format: ' + str(im.format))
        print('size: ' + str(im.size))
        print('mode: ' + str(im.mode))
        print('max, min: ', end=' ')
        print(im.getextrema())
        if len(sys.argv) > 2:
            outfile = sys.argv[2]
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
            print(f"saving a flipped version of {os.path.basename(filename)} as {outfile} ")
            im.save(outfile, SpiderImageFile.format)