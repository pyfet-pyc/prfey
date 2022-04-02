# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\IcnsImagePlugin.py
import io, os, shutil, struct, subprocess, sys, tempfile
from PIL import Image, ImageFile, PngImagePlugin, features
from PIL._binary import i8
enable_jpeg2k = features.check_codec('jpg_2000')
if enable_jpeg2k:
    from PIL import Jpeg2KImagePlugin
HEADERSIZE = 8

def nextheader(fobj):
    return struct.unpack('>4sI', fobj.read(HEADERSIZE))


def read_32t(fobj, start_length, size):
    start, length = start_length
    fobj.seek(start)
    sig = fobj.read(4)
    if sig != b'\x00\x00\x00\x00':
        raise SyntaxError('Unknown signature, expecting 0x00000000')
    return read_32(fobj, (start + 4, length - 4), size)


def read_32--- This code section failed: ---

 L.  55         0  LOAD_FAST                'start_length'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'start'
                6  STORE_FAST               'length'

 L.  56         8  LOAD_FAST                'fobj'
               10  LOAD_METHOD              seek
               12  LOAD_FAST                'start'
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          

 L.  57        18  LOAD_FAST                'size'
               20  LOAD_CONST               0
               22  BINARY_SUBSCR    
               24  LOAD_FAST                'size'
               26  LOAD_CONST               2
               28  BINARY_SUBSCR    
               30  BINARY_MULTIPLY  
               32  LOAD_FAST                'size'
               34  LOAD_CONST               1
               36  BINARY_SUBSCR    
               38  LOAD_FAST                'size'
               40  LOAD_CONST               2
               42  BINARY_SUBSCR    
               44  BINARY_MULTIPLY  
               46  BUILD_TUPLE_2         2 
               48  STORE_FAST               'pixel_size'

 L.  58        50  LOAD_FAST                'pixel_size'
               52  LOAD_CONST               0
               54  BINARY_SUBSCR    
               56  LOAD_FAST                'pixel_size'
               58  LOAD_CONST               1
               60  BINARY_SUBSCR    
               62  BINARY_MULTIPLY  
               64  STORE_FAST               'sizesq'

 L.  59        66  LOAD_FAST                'length'
               68  LOAD_FAST                'sizesq'
               70  LOAD_CONST               3
               72  BINARY_MULTIPLY  
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE   112  'to 112'

 L.  61        78  LOAD_FAST                'fobj'
               80  LOAD_METHOD              read
               82  LOAD_FAST                'length'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'indata'

 L.  62        88  LOAD_GLOBAL              Image
               90  LOAD_METHOD              frombuffer
               92  LOAD_STR                 'RGB'
               94  LOAD_FAST                'pixel_size'
               96  LOAD_FAST                'indata'
               98  LOAD_STR                 'raw'
              100  LOAD_STR                 'RGB'
              102  LOAD_CONST               0
              104  LOAD_CONST               1
              106  CALL_METHOD_7         7  ''
              108  STORE_FAST               'im'
              110  JUMP_FORWARD        348  'to 348'
            112_0  COME_FROM            76  '76'

 L.  65       112  LOAD_GLOBAL              Image
              114  LOAD_METHOD              new
              116  LOAD_STR                 'RGB'
              118  LOAD_FAST                'pixel_size'
              120  LOAD_CONST               None
              122  CALL_METHOD_3         3  ''
              124  STORE_FAST               'im'

 L.  66       126  LOAD_GLOBAL              range
              128  LOAD_CONST               3
              130  CALL_FUNCTION_1       1  ''
              132  GET_ITER         
            134_0  COME_FROM           346  '346'
              134  FOR_ITER            348  'to 348'
              136  STORE_FAST               'band_ix'

 L.  67       138  BUILD_LIST_0          0 
              140  STORE_FAST               'data'

 L.  68       142  LOAD_FAST                'sizesq'
              144  STORE_FAST               'bytesleft'
            146_0  COME_FROM           278  '278'
            146_1  COME_FROM           272  '272'

 L.  69       146  LOAD_FAST                'bytesleft'
              148  LOAD_CONST               0
              150  COMPARE_OP               >
          152_154  POP_JUMP_IF_FALSE   280  'to 280'

 L.  70       156  LOAD_FAST                'fobj'
              158  LOAD_METHOD              read
              160  LOAD_CONST               1
              162  CALL_METHOD_1         1  ''
              164  STORE_FAST               'byte'

 L.  71       166  LOAD_FAST                'byte'
              168  POP_JUMP_IF_TRUE    174  'to 174'

 L.  72   170_172  JUMP_FORWARD        280  'to 280'
            174_0  COME_FROM           168  '168'

 L.  73       174  LOAD_GLOBAL              i8
              176  LOAD_FAST                'byte'
              178  CALL_FUNCTION_1       1  ''
              180  STORE_FAST               'byte'

 L.  74       182  LOAD_FAST                'byte'
              184  LOAD_CONST               128
              186  BINARY_AND       
              188  POP_JUMP_IF_FALSE   234  'to 234'

 L.  75       190  LOAD_FAST                'byte'
              192  LOAD_CONST               125
              194  BINARY_SUBTRACT  
              196  STORE_FAST               'blocksize'

 L.  76       198  LOAD_FAST                'fobj'
              200  LOAD_METHOD              read
              202  LOAD_CONST               1
              204  CALL_METHOD_1         1  ''
              206  STORE_FAST               'byte'

 L.  77       208  LOAD_GLOBAL              range
              210  LOAD_FAST                'blocksize'
              212  CALL_FUNCTION_1       1  ''
              214  GET_ITER         
            216_0  COME_FROM           230  '230'
              216  FOR_ITER            232  'to 232'
              218  STORE_FAST               'i'

 L.  78       220  LOAD_FAST                'data'
              222  LOAD_METHOD              append
              224  LOAD_FAST                'byte'
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          
              230  JUMP_BACK           216  'to 216'
            232_0  COME_FROM           216  '216'
              232  JUMP_FORWARD        258  'to 258'
            234_0  COME_FROM           188  '188'

 L.  80       234  LOAD_FAST                'byte'
              236  LOAD_CONST               1
              238  BINARY_ADD       
              240  STORE_FAST               'blocksize'

 L.  81       242  LOAD_FAST                'data'
              244  LOAD_METHOD              append
              246  LOAD_FAST                'fobj'
              248  LOAD_METHOD              read
              250  LOAD_FAST                'blocksize'
              252  CALL_METHOD_1         1  ''
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          
            258_0  COME_FROM           232  '232'

 L.  82       258  LOAD_FAST                'bytesleft'
              260  LOAD_FAST                'blocksize'
              262  INPLACE_SUBTRACT 
              264  STORE_FAST               'bytesleft'

 L.  83       266  LOAD_FAST                'bytesleft'
              268  LOAD_CONST               0
              270  COMPARE_OP               <=
              272  POP_JUMP_IF_FALSE_BACK   146  'to 146'

 L.  84   274_276  JUMP_FORWARD        280  'to 280'
              278  JUMP_BACK           146  'to 146'
            280_0  COME_FROM           274  '274'
            280_1  COME_FROM           170  '170'
            280_2  COME_FROM           152  '152'

 L.  85       280  LOAD_FAST                'bytesleft'
              282  LOAD_CONST               0
              284  COMPARE_OP               !=
          286_288  POP_JUMP_IF_FALSE   302  'to 302'

 L.  86       290  LOAD_GLOBAL              SyntaxError
              292  LOAD_STR                 'Error reading channel [%r left]'
              294  LOAD_FAST                'bytesleft'
              296  BINARY_MODULO    
              298  CALL_FUNCTION_1       1  ''
              300  RAISE_VARARGS_1       1  'exception instance'
            302_0  COME_FROM           286  '286'

 L.  87       302  LOAD_GLOBAL              Image
              304  LOAD_METHOD              frombuffer
              306  LOAD_STR                 'L'
              308  LOAD_FAST                'pixel_size'
              310  LOAD_CONST               b''
              312  LOAD_METHOD              join
              314  LOAD_FAST                'data'
              316  CALL_METHOD_1         1  ''
              318  LOAD_STR                 'raw'
              320  LOAD_STR                 'L'
              322  LOAD_CONST               0
              324  LOAD_CONST               1
              326  CALL_METHOD_7         7  ''
              328  STORE_FAST               'band'

 L.  88       330  LOAD_FAST                'im'
              332  LOAD_ATTR                im
              334  LOAD_METHOD              putband
              336  LOAD_FAST                'band'
              338  LOAD_ATTR                im
              340  LOAD_FAST                'band_ix'
              342  CALL_METHOD_2         2  ''
              344  POP_TOP          
              346  JUMP_BACK           134  'to 134'
            348_0  COME_FROM           134  '134'
            348_1  COME_FROM           110  '110'

 L.  89       348  LOAD_STR                 'RGB'
              350  LOAD_FAST                'im'
              352  BUILD_MAP_1           1 
              354  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 278


def read_mk(fobj, start_length, size):
    start = start_length[0]
    fobj.seek(start)
    pixel_size = (size[0] * size[2], size[1] * size[2])
    sizesq = pixel_size[0] * pixel_size[1]
    band = Image.frombuffer'L'pixel_sizefobj.read(sizesq)'raw''L'01
    return {'A': band}


def read_png_or_jpeg2000(fobj, start_length, size):
    start, length = start_length
    fobj.seek(start)
    sig = fobj.read(12)
    if sig[:8] == b'\x89PNG\r\n\x1a\n':
        fobj.seek(start)
        im = PngImagePlugin.PngImageFile(fobj)
        return {'RGBA': im}
    if sig[:4] == b'\xffO\xffQ' or (sig[:4] == b'\r\n\x87\n' or sig == b'\x00\x00\x00\x0cjP  \r\n\x87\n'):
        if not enable_jpeg2k:
            raise ValueError('Unsupported icon subimage format (rebuild PIL with JPEG 2000 support to fix this)')
        fobj.seek(start)
        jp2kstream = fobj.read(length)
        f = io.BytesIO(jp2kstream)
        im = Jpeg2KImagePlugin.Jpeg2KImageFile(f)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        return {'RGBA': im}
    raise ValueError('Unsupported icon subimage format')


class IcnsFile:
    SIZES = {(512, 512, 2):[
      (
       b'ic10', read_png_or_jpeg2000)], 
     (512, 512, 1):[
      (
       b'ic09', read_png_or_jpeg2000)], 
     (256, 256, 2):[
      (
       b'ic14', read_png_or_jpeg2000)], 
     (256, 256, 1):[
      (
       b'ic08', read_png_or_jpeg2000)], 
     (128, 128, 2):[
      (
       b'ic13', read_png_or_jpeg2000)], 
     (128, 128, 1):[
      (
       b'ic07', read_png_or_jpeg2000),
      (
       b'it32', read_32t),
      (
       b't8mk', read_mk)], 
     (64, 64, 1):[
      (
       b'icp6', read_png_or_jpeg2000)], 
     (32, 32, 2):[
      (
       b'ic12', read_png_or_jpeg2000)], 
     (48, 48, 1):[
      (
       b'ih32', read_32), (b'h8mk', read_mk)], 
     (32, 32, 1):[
      (
       b'icp5', read_png_or_jpeg2000),
      (
       b'il32', read_32),
      (
       b'l8mk', read_mk)], 
     (16, 16, 2):[
      (
       b'ic11', read_png_or_jpeg2000)], 
     (16, 16, 1):[
      (
       b'icp4', read_png_or_jpeg2000),
      (
       b'is32', read_32),
      (
       b's8mk', read_mk)]}

    def __init__(self, fobj):
        """
        fobj is a file-like object as an icns resource
        """
        self.dct = dct = {}
        self.fobj = fobj
        sig, filesize = nextheader(fobj)
        if sig != b'icns':
            raise SyntaxError('not an icns file')
        i = HEADERSIZE
        while True:
            if i < filesize:
                sig, blocksize = nextheader(fobj)
                if blocksize <= 0:
                    raise SyntaxError('invalid block header')
                i += HEADERSIZE
                blocksize -= HEADERSIZE
                dct[sig] = (i, blocksize)
                fobj.seek(blocksize, io.SEEK_CUR)
                i += blocksize

    def itersizes(self):
        sizes = []
        for size, fmts in self.SIZES.items():
            for fmt, reader in fmts:
                if fmt in self.dct:
                    sizes.append(size)
                    break
            else:
                return sizes

    def bestsize(self):
        sizes = self.itersizes()
        if not sizes:
            raise SyntaxError('No 32bit icon resources found')
        return max(sizes)

    def dataforsize(self, size):
        """
        Get an icon resource as {channel: array}.  Note that
        the arrays are bottom-up like windows bitmaps and will likely
        need to be flipped or transposed in some way.
        """
        dct = {}
        for code, reader in self.SIZES[size]:
            desc = self.dct.get(code)
            if desc is not None:
                dct.update(reader(self.fobj, desc, size))
        else:
            return dct

    def getimage(self, size=None):
        if size is None:
            size = self.bestsize()
        if len(size) == 2:
            size = (
             size[0], size[1], 1)
        channels = self.dataforsize(size)
        im = channels.get('RGBA', None)
        if im:
            return im
        im = channels.get('RGB').copy()
        try:
            im.putalpha(channels['A'])
        except KeyError:
            pass
        else:
            return im


class IcnsImageFile(ImageFile.ImageFile):
    __doc__ = "\n    PIL image support for Mac OS .icns files.\n    Chooses the best resolution, but will possibly load\n    a different size image if you mutate the size attribute\n    before calling 'load'.\n\n    The info dictionary has a key 'sizes' that is a list\n    of sizes that the icns file has.\n    "
    format = 'ICNS'
    format_description = 'Mac OS icns resource'

    def _open(self):
        self.icns = IcnsFile(self.fp)
        self.mode = 'RGBA'
        self.info['sizes'] = self.icns.itersizes()
        self.best_size = self.icns.bestsize()
        self.size = (
         self.best_size[0] * self.best_size[2],
         self.best_size[1] * self.best_size[2])

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        info_size = value
        if info_size not in self.info['sizes']:
            if len(info_size) == 2:
                info_size = (
                 info_size[0], info_size[1], 1)
        if info_size not in self.info['sizes']:
            if len(info_size) == 3:
                if info_size[2] == 1:
                    simple_sizes = [(
                     size[0] * size[2], size[1] * size[2]) for size in self.info['sizes']]
                    if value in simple_sizes:
                        info_size = self.info['sizes'][simple_sizes.index(value)]
        if info_size not in self.info['sizes']:
            raise ValueError('This is not one of the allowed sizes of this image')
        self._size = value

    def load(self):
        if len(self.size) == 3:
            self.best_size = self.size
            self.size = (
             self.best_size[0] * self.best_size[2],
             self.best_size[1] * self.best_size[2])
        Image.Image.load(self)
        if self.im:
            if self.im.size == self.size:
                return
        self.load_prepare()
        im = self.icns.getimage(self.best_size)
        im.load()
        self.im = im.im
        self.mode = im.mode
        self.size = im.size
        self.load_end()


def _save(im, fp, filename):
    """
    Saves the image as a series of PNG files,
    that are then converted to a .icns file
    using the macOS command line utility 'iconutil'.

    macOS only.
    """
    if hasattr(fp, 'flush'):
        fp.flush()
    with tempfile.TemporaryDirectory('.iconset') as iconset:
        provided_images = {im:im.width for im in im.encoderinfo.get('append_images', [])}
        last_w = None
        second_path = None
        for w in (16, 32, 128, 256, 512):
            prefix = 'icon_{}x{}'.format(w, w)
            first_path = os.path.join(iconset, prefix + '.png')
            if last_w == w:
                shutil.copyfile(second_path, first_path)
            else:
                im_w = provided_images.get(w, im.resize((w, w), Image.LANCZOS))
                im_w.save(first_path)
            second_path = os.path.join(iconset, prefix + '@2x.png')
            im_w2 = provided_images.get(w * 2, im.resize((w * 2, w * 2), Image.LANCZOS))
            im_w2.save(second_path)
            last_w = w * 2
        else:
            fp_only = not filename
            if fp_only:
                f, filename = tempfile.mkstemp('.icns')
                os.close(f)
            convert_cmd = [
             'iconutil', '-c', 'icns', '-o', filename, iconset]
            convert_proc = subprocess.Popen(convert_cmd,
              stdout=(subprocess.PIPE), stderr=(subprocess.DEVNULL))
            convert_proc.stdout.close()
            retcode = convert_proc.wait()
            if retcode:
                raise subprocess.CalledProcessError(retcode, convert_cmd)
            if fp_only:
                with open(filename, 'rb') as f:
                    fp.write(f.read())


Image.register_open(IcnsImageFile.format, IcnsImageFile, lambda x: x[:4] == b'icns')
Image.register_extension(IcnsImageFile.format, '.icns')
if sys.platform == 'darwin':
    Image.register_save(IcnsImageFile.format, _save)
    Image.register_mime(IcnsImageFile.format, 'image/icns')
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Syntax: python IcnsImagePlugin.py [file]')
        sys.exit()
    with open(sys.argv[1], 'rb') as fp:
        imf = IcnsImageFile(fp)
        for size in imf.info['sizes']:
            imf.size = size
            imf.save('out-%s-%s-%s.png' % size)
        else:
            with Image.open(sys.argv[1]) as im:
                im.save('out.png')
            if sys.platform == 'windows':
                os.startfile('out.png')