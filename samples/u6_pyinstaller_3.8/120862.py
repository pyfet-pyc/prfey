# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\IcnsImagePlugin.py
import io, os, shutil, struct, subprocess, sys, tempfile
from PIL import Image, ImageFile, PngImagePlugin, features
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


def read_32(fobj, start_length, size):
    """
    Read a 32bit RGB icon resource.  Seems to be either uncompressed or
    an RLE packbits-like scheme.
    """
    start, length = start_length
    fobj.seek(start)
    pixel_size = (size[0] * size[2], size[1] * size[2])
    sizesq = pixel_size[0] * pixel_size[1]
    if length == sizesq * 3:
        indata = fobj.read(length)
        im = Image.frombuffer('RGB', pixel_size, indata, 'raw', 'RGB', 0, 1)
    else:
        im = Image.new('RGB', pixel_size, None)
        for band_ix in range(3):
            data = []
            bytesleft = sizesq
            while bytesleft > 0:
                byte = fobj.read(1)
                if not byte:
                    break
                else:
                    byte = byte[0]
                    if byte & 128:
                        blocksize = byte - 125
                        byte = fobj.read(1)
                        for i in range(blocksize):
                            data.append(byte)

                    else:
                        blocksize = byte + 1
                    data.append(fobj.read(blocksize))
                bytesleft -= blocksize
                if bytesleft <= 0:
                    break

            if bytesleft != 0:
                raise SyntaxError(f"Error reading channel [{repr(bytesleft)} left]")
            band = Image.frombuffer('L', pixel_size, (b'').join(data), 'raw', 'L', 0, 1)
            im.im.putband(band.im, band_ix)
        else:
            return {'RGB': im}


def read_mk(fobj, start_length, size):
    start = start_length[0]
    fobj.seek(start)
    pixel_size = (size[0] * size[2], size[1] * size[2])
    sizesq = pixel_size[0] * pixel_size[1]
    band = Image.frombuffer('L', pixel_size, fobj.read(sizesq), 'raw', 'L', 0, 1)
    return {'A': band}


def read_png_or_jpeg2000(fobj, start_length, size):
    start, length = start_length
    fobj.seek(start)
    sig = fobj.read(12)
    if sig[:8] == b'\x89PNG\r\n\x1a\n':
        fobj.seek(start)
        im = PngImagePlugin.PngImageFile(fobj)
        Image._decompression_bomb_check(im.size)
        return {'RGBA': im}
    if sig[:4] == b'\xffO\xffQ' or sig[:4] == b'\r\n\x87\n' or sig == b'\x00\x00\x00\x0cjP  \r\n\x87\n':
        if not enable_jpeg2k:
            raise ValueError('Unsupported icon subimage format (rebuild PIL with JPEG 2000 support to fix this)')
        fobj.seek(start)
        jp2kstream = fobj.read(length)
        f = io.BytesIO(jp2kstream)
        im = Jpeg2KImagePlugin.Jpeg2KImageFile(f)
        Image._decompression_bomb_check(im.size)
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
        else:
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

    def itersizes--- This code section failed: ---

 L. 184         0  BUILD_LIST_0          0 
                2  STORE_FAST               'sizes'

 L. 185         4  LOAD_FAST                'self'
                6  LOAD_ATTR                SIZES
                8  LOAD_METHOD              items
               10  CALL_METHOD_0         0  ''
               12  GET_ITER         
               14  FOR_ITER             62  'to 62'
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'size'
               20  STORE_FAST               'fmts'

 L. 186        22  LOAD_FAST                'fmts'
               24  GET_ITER         
             26_0  COME_FROM            42  '42'
               26  FOR_ITER             60  'to 60'
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'fmt'
               32  STORE_FAST               'reader'

 L. 187        34  LOAD_FAST                'fmt'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                dct
               40  COMPARE_OP               in
               42  POP_JUMP_IF_FALSE    26  'to 26'

 L. 188        44  LOAD_FAST                'sizes'
               46  LOAD_METHOD              append
               48  LOAD_FAST                'size'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 189        54  POP_TOP          
               56  CONTINUE             14  'to 14'
               58  JUMP_BACK            26  'to 26'
               60  JUMP_BACK            14  'to 14'

 L. 190        62  LOAD_FAST                'sizes'
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 56

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
    with tempfile.TemporaryDirectory('.iconset') as (iconset):
        provided_images = {im:im.width for im in im.encoderinfo.get('append_images', [])}
        last_w = None
        second_path = None
        for w in (16, 32, 128, 256, 512):
            prefix = f"icon_{w}x{w}"
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
                with open(filename, 'rb') as (f):
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
    with open(sys.argv[1], 'rb') as (fp):
        imf = IcnsImageFile(fp)
        for size in imf.info['sizes']:
            imf.size = size
            imf.save('out-%s-%s-%s.png' % size)
        else:
            with Image.open(sys.argv[1]) as (im):
                im.save('out.png')
            if sys.platform == 'windows':
                os.startfile('out.png')