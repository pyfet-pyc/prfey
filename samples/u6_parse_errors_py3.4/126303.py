# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\GifImagePlugin.py
from . import Image, ImageFile, ImagePalette, ImageChops, ImageSequence
from ._binary import i8, i16le as i16, o8, o16le as o16
import itertools
__version__ = '0.9'

def _accept(prefix):
    return prefix[:6] in (b'GIF87a', b'GIF89a')


class GifImageFile(ImageFile.ImageFile):
    format = 'GIF'
    format_description = 'Compuserve GIF'
    _close_exclusive_fp_after_loading = False
    global_palette = None

    def data(self):
        s = self.fp.read(1)
        if s and i8(s):
            return self.fp.read(i8(s))

    def _open(self):
        s = self.fp.read(13)
        if s[:6] not in (b'GIF87a', b'GIF89a'):
            raise SyntaxError('not a GIF file')
        self.info['version'] = s[:6]
        self._size = (i16(s[6:]), i16(s[8:]))
        self.tile = []
        flags = i8(s[10])
        bits = (flags & 7) + 1
        if flags & 128:
            self.info['background'] = i8(s[11])
            p = self.fp.read(3 << bits)
            for i in range(0, len(p), 3):
                if not i // 3 == i8(p[i]) == i8(p[(i + 1)]) == i8(p[(i + 2)]):
                    p = ImagePalette.raw('RGB', p)
                    self.global_palette = self.palette = p
                    break

        self._GifImageFile__fp = self.fp
        self._GifImageFile__rewind = self.fp.tell()
        self._n_frames = None
        self._is_animated = None
        self._seek(0)

    @property
    def n_frames(self):
        if self._n_frames is None:
            current = self.tell()
            try:
                while True:
                    self.seek(self.tell() + 1)

            except EOFError:
                self._n_frames = self.tell() + 1

            self.seek(current)
        return self._n_frames

    @property
    def is_animated(self):
        if self._is_animated is None:
            if self._n_frames is not None:
                self._is_animated = self._n_frames != 1
            else:
                current = self.tell()
                try:
                    self.seek(1)
                    self._is_animated = True
                except EOFError:
                    self._is_animated = False

                self.seek(current)
        return self._is_animated

    def seek(self, frame):
        if not self._seek_check(frame):
            return
        if frame < self._GifImageFile__frame:
            self._seek(0)
        last_frame = self._GifImageFile__frame
        for f in range(self._GifImageFile__frame + 1, frame + 1):
            try:
                self._seek(f)
            except EOFError:
                self.seek(last_frame)
                raise EOFError('no more images in GIF file')

    def _seek(self, frame):
        if frame == 0:
            self._GifImageFile__offset = 0
            self.dispose = None
            self.dispose_extent = [0, 0, 0, 0]
            self._GifImageFile__frame = -1
            self._GifImageFile__fp.seek(self._GifImageFile__rewind)
            self._prev_im = None
            self.disposal_method = 0
        elif not self.im:
            self.load()
        if frame != self._GifImageFile__frame + 1:
            raise ValueError('cannot seek to frame %d' % frame)
        self._GifImageFile__frame = frame
        self.tile = []
        self.fp = self._GifImageFile__fp
        if self._GifImageFile__offset:
            self.fp.seek(self._GifImageFile__offset)
            while self.data():
                pass

            self._GifImageFile__offset = 0
        if self.dispose:
            self.im.paste(self.dispose, self.dispose_extent)
        from copy import copy
        self.palette = copy(self.global_palette)
        info = {}
        while 1:
            s = self.fp.read(1)
            if not s or s == b';':
                break
            elif s == b'!':
                s = self.fp.read(1)
                block = self.data()
                if i8(s) == 249:
                    flags = i8(block[0])
                    if flags & 1:
                        info['transparency'] = i8(block[3])
                    info['duration'] = i16(block[1:3]) * 10
                    dispose_bits = 28 & flags
                    dispose_bits = dispose_bits >> 2
                    if dispose_bits:
                        self.disposal_method = dispose_bits
                else:
                    if i8(s) == 254:
                        while block:
                            if 'comment' in info:
                                info['comment'] += block
                            else:
                                info['comment'] = block
                            block = self.data()

                        continue
                    elif i8(s) == 255:
                        info['extension'] = (
                         block, self.fp.tell())
                        if block[:11] == b'NETSCAPE2.0':
                            block = self.data()
                            if len(block) >= 3:
                                if i8(block[0]) == 1:
                                    info['loop'] = i16(block[1:3])
                while self.data():
                    pass

            elif s == b',':
                s = self.fp.read(9)
                x0, y0 = i16(s[0:]), i16(s[2:])
                x1, y1 = x0 + i16(s[4:]), y0 + i16(s[6:])
                self.dispose_extent = (x0, y0, x1, y1)
                flags = i8(s[8])
                interlace = flags & 64 != 0
                if flags & 128:
                    bits = (flags & 7) + 1
                    self.palette = ImagePalette.raw('RGB', self.fp.read(3 << bits))
                bits = i8(self.fp.read(1))
                self._GifImageFile__offset = self.fp.tell()
                self.tile = [
                 ('gif',
                  (
                   x0, y0, x1, y1),
                  self._GifImageFile__offset,
                  (
                   bits, interlace))]
                break

        try:
            if self.disposal_method < 2:
                self.dispose = None
            else:
                if self.disposal_method == 2:
                    self.dispose = Image.core.fill('P', self.size, self.info['background'])
                elif self.im:
                    self.dispose = self.im.copy()
            if self.dispose:
                self.dispose = self._crop(self.dispose, self.dispose_extent)
        except (AttributeError, KeyError):
            pass

        if not self.tile:
            raise EOFError
        for k in ['transparency', 'duration', 'comment', 'extension', 'loop']:
            if k in info:
                self.info[k] = info[k]
            elif k in self.info:
                del self.info[k]
                continue

        self.mode = 'L'
        if self.palette:
            self.mode = 'P'

    def tell(self):
        return self._GifImageFile__frame

    def load_end(self):
        ImageFile.ImageFile.load_end(self)
        if self._prev_im:
            if self.disposal_method == 1:
                updated = self._crop(self.im, self.dispose_extent)
                self._prev_im.paste(updated, self.dispose_extent, updated.convert('RGBA'))
                self.im = self._prev_im
        self._prev_im = self.im.copy()

    def _close__fp(self):
        try:
            try:
                if self._GifImageFile__fp != self.fp:
                    self._GifImageFile__fp.close()
            except AttributeError:
                pass

        finally:
            self._GifImageFile__fp = None


RAWMODE = {'1': 'L', 
 'L': 'L', 
 'P': 'P'}

def _normalize_mode(im, initial_call=False):
    """
    Takes an image (or frame), returns an image in a mode that is appropriate
    for saving in a Gif.

    It may return the original image, or it may return an image converted to
    palette or 'L' mode.

    UNDONE: What is the point of mucking with the initial call palette, for
    an image that shouldn't have a palette, or it would be a mode 'P' and
    get returned in the RAWMODE clause.

    :param im: Image object
    :param initial_call: Default false, set to true for a single frame.
    :returns: Image object
    """
    if im.mode in RAWMODE:
        im.load()
        return im
    if Image.getmodebase(im.mode) == 'RGB':
        if initial_call:
            palette_size = 256
            if im.palette:
                palette_size = len(im.palette.getdata()[1]) // 3
            return im.convert('P', palette=Image.ADAPTIVE, colors=palette_size)
        else:
            return im.convert('P')
    return im.convert('L')


def _normalize_palette(im, palette, info):
    """
    Normalizes the palette for image.
      - Sets the palette to the incoming palette, if provided.
      - Ensures that there's a palette for L mode images
      - Optimizes the palette if necessary/desired.

    :param im: Image object
    :param palette: bytes object containing the source palette, or ....
    :param info: encoderinfo
    :returns: Image object
    """
    source_palette = None
    if palette:
        if isinstance(palette, (bytes, bytearray, list)):
            source_palette = bytearray(palette[:768])
        if isinstance(palette, ImagePalette.ImagePalette):
            source_palette = bytearray(itertools.chain.from_iterable(zip(palette.palette[:256], palette.palette[256:512], palette.palette[512:768])))
        if im.mode == 'P':
            if not source_palette:
                source_palette = im.im.getpalette('RGB')[:768]
    else:
        if not source_palette:
            source_palette = bytearray(i // 3 for i in range(768))
        im.palette = ImagePalette.ImagePalette('RGB', palette=source_palette)
    used_palette_colors = _get_optimize(im, info)
    if used_palette_colors is not None:
        return im.remap_palette(used_palette_colors, source_palette)
    im.palette.palette = source_palette
    return im


def _write_single_frame(im, fp, palette):
    im_out = _normalize_mode(im, True)
    for k, v in im_out.info.items():
        im.encoderinfo.setdefault(k, v)

    im_out = _normalize_palette(im_out, palette, im.encoderinfo)
    for s in _get_global_header(im_out, im.encoderinfo):
        fp.write(s)

    flags = 0
    if get_interlace(im):
        flags = flags | 64
    _write_local_header(fp, im, (0, 0), flags)
    im_out.encoderconfig = (
     8, get_interlace(im))
    ImageFile._save(im_out, fp, [
     ('gif', (0, 0) + im.size, 0,
      RAWMODE[im_out.mode])])
    fp.write(b'\x00')


def _write_multiple_frames--- This code section failed: ---

 L. 419         0  LOAD_FAST                'im'
                3  LOAD_ATTR                encoderinfo
                6  LOAD_ATTR                get
                9  LOAD_STR                 'duration'
               12  LOAD_FAST                'im'
               15  LOAD_ATTR                info
               18  LOAD_ATTR                get
               21  LOAD_STR                 'duration'
               24  CALL_FUNCTION_1       1  '1 positional, 0 named'
               27  CALL_FUNCTION_2       2  '2 positional, 0 named'
               30  STORE_FAST               'duration'

 L. 420        33  LOAD_FAST                'im'
               36  LOAD_ATTR                encoderinfo
               39  LOAD_ATTR                get
               42  LOAD_STR                 'disposal'
               45  LOAD_FAST                'im'
               48  LOAD_ATTR                info
               51  LOAD_ATTR                get
               54  LOAD_STR                 'disposal'
               57  CALL_FUNCTION_1       1  '1 positional, 0 named'
               60  CALL_FUNCTION_2       2  '2 positional, 0 named'
               63  STORE_FAST               'disposal'

 L. 422        66  BUILD_LIST_0          0 
               69  STORE_FAST               'im_frames'

 L. 423        72  LOAD_CONST               0
               75  STORE_FAST               'frame_count'

 L. 424        78  SETUP_LOOP          564  'to 564'
               81  LOAD_GLOBAL              itertools
               84  LOAD_ATTR                chain
               87  LOAD_FAST                'im'
               90  BUILD_LIST_1          1 

 L. 425        93  LOAD_FAST                'im'
               96  LOAD_ATTR                encoderinfo
               99  LOAD_ATTR                get
              102  LOAD_STR                 'append_images'
              105  BUILD_LIST_0          0 
              108  CALL_FUNCTION_2       2  '2 positional, 0 named'
              111  CALL_FUNCTION_2       2  '2 positional, 0 named'
              114  GET_ITER         
              115  FOR_ITER            563  'to 563'
              118  STORE_FAST               'imSequence'

 L. 426       121  SETUP_LOOP          560  'to 560'
              124  LOAD_GLOBAL              ImageSequence
              127  LOAD_ATTR                Iterator
              130  LOAD_FAST                'imSequence'
              133  CALL_FUNCTION_1       1  '1 positional, 0 named'
              136  GET_ITER         
              137  FOR_ITER            559  'to 559'
              140  STORE_FAST               'im_frame'

 L. 428       143  LOAD_GLOBAL              _normalize_mode
              146  LOAD_FAST                'im_frame'
              149  LOAD_ATTR                copy
              152  CALL_FUNCTION_0       0  '0 positional, 0 named'
              155  CALL_FUNCTION_1       1  '1 positional, 0 named'
              158  STORE_FAST               'im_frame'

 L. 429       161  LOAD_FAST                'frame_count'
              164  LOAD_CONST               0
              167  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   227  'to 227'

 L. 430       173  SETUP_LOOP          227  'to 227'
              176  LOAD_FAST                'im_frame'
              179  LOAD_ATTR                info
              182  LOAD_ATTR                items
              185  CALL_FUNCTION_0       0  '0 positional, 0 named'
              188  GET_ITER         
              189  FOR_ITER            223  'to 223'
              192  UNPACK_SEQUENCE_2     2 
              195  STORE_FAST               'k'
              198  STORE_FAST               'v'

 L. 431       201  LOAD_FAST                'im'
              204  LOAD_ATTR                encoderinfo
              207  LOAD_ATTR                setdefault
              210  LOAD_FAST                'k'
              213  LOAD_FAST                'v'
              216  CALL_FUNCTION_2       2  '2 positional, 0 named'
              219  POP_TOP          
              220  JUMP_BACK           189  'to 189'
              223  POP_BLOCK        
            224_0  COME_FROM_LOOP      173  '173'
              224  JUMP_FORWARD        227  'to 227'
            227_0  COME_FROM           224  '224'

 L. 432       227  LOAD_GLOBAL              _normalize_palette
              230  LOAD_FAST                'im_frame'
              233  LOAD_FAST                'palette'
              236  LOAD_FAST                'im'
              239  LOAD_ATTR                encoderinfo
              242  CALL_FUNCTION_3       3  '3 positional, 0 named'
              245  STORE_FAST               'im_frame'

 L. 434       248  LOAD_FAST                'im'
              251  LOAD_ATTR                encoderinfo
              254  LOAD_ATTR                copy
              257  CALL_FUNCTION_0       0  '0 positional, 0 named'
              260  STORE_FAST               'encoderinfo'

 L. 435       263  LOAD_GLOBAL              isinstance
              266  LOAD_FAST                'duration'
              269  LOAD_GLOBAL              list
              272  LOAD_GLOBAL              tuple
              275  BUILD_TUPLE_2         2 
              278  CALL_FUNCTION_2       2  '2 positional, 0 named'
              281  POP_JUMP_IF_FALSE   301  'to 301'

 L. 436       284  LOAD_FAST                'duration'
              287  LOAD_FAST                'frame_count'
              290  BINARY_SUBSCR    
              291  LOAD_FAST                'encoderinfo'
              294  LOAD_STR                 'duration'
              297  STORE_SUBSCR     
              298  JUMP_FORWARD        301  'to 301'
            301_0  COME_FROM           298  '298'

 L. 437       301  LOAD_GLOBAL              isinstance
              304  LOAD_FAST                'disposal'
              307  LOAD_GLOBAL              list
              310  LOAD_GLOBAL              tuple
              313  BUILD_TUPLE_2         2 
              316  CALL_FUNCTION_2       2  '2 positional, 0 named'
              319  POP_JUMP_IF_FALSE   339  'to 339'

 L. 438       322  LOAD_FAST                'disposal'
              325  LOAD_FAST                'frame_count'
              328  BINARY_SUBSCR    
              329  LOAD_FAST                'encoderinfo'
              332  LOAD_STR                 'disposal'
              335  STORE_SUBSCR     
              336  JUMP_FORWARD        339  'to 339'
            339_0  COME_FROM           336  '336'

 L. 439       339  LOAD_FAST                'frame_count'
              342  LOAD_CONST               1
              345  INPLACE_ADD      
              346  STORE_FAST               'frame_count'

 L. 441       349  LOAD_FAST                'im_frames'
              352  POP_JUMP_IF_FALSE   516  'to 516'

 L. 443       355  LOAD_FAST                'im_frames'
              358  LOAD_CONST               -1
              361  BINARY_SUBSCR    
              362  STORE_FAST               'previous'

 L. 444       365  LOAD_GLOBAL              _get_palette_bytes
              368  LOAD_FAST                'im_frame'
              371  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L. 445       374  LOAD_GLOBAL              _get_palette_bytes
              377  LOAD_FAST                'previous'
              380  LOAD_STR                 'im'
              383  BINARY_SUBSCR    
              384  CALL_FUNCTION_1       1  '1 positional, 0 named'
              387  COMPARE_OP               ==
              390  POP_JUMP_IF_FALSE   418  'to 418'

 L. 446       393  LOAD_GLOBAL              ImageChops
              396  LOAD_ATTR                subtract_modulo
              399  LOAD_FAST                'im_frame'

 L. 447       402  LOAD_FAST                'previous'
              405  LOAD_STR                 'im'
              408  BINARY_SUBSCR    
              409  CALL_FUNCTION_2       2  '2 positional, 0 named'
              412  STORE_FAST               'delta'
              415  JUMP_FORWARD        458  'to 458'
              418  ELSE                     '458'

 L. 449       418  LOAD_GLOBAL              ImageChops
              421  LOAD_ATTR                subtract_modulo

 L. 450       424  LOAD_FAST                'im_frame'
              427  LOAD_ATTR                convert
              430  LOAD_STR                 'RGB'
              433  CALL_FUNCTION_1       1  '1 positional, 0 named'
              436  LOAD_FAST                'previous'
              439  LOAD_STR                 'im'
              442  BINARY_SUBSCR    
              443  LOAD_ATTR                convert
              446  LOAD_STR                 'RGB'
              449  CALL_FUNCTION_1       1  '1 positional, 0 named'
              452  CALL_FUNCTION_2       2  '2 positional, 0 named'
              455  STORE_FAST               'delta'
            458_0  COME_FROM           415  '415'

 L. 451       458  LOAD_FAST                'delta'
              461  LOAD_ATTR                getbbox
              464  CALL_FUNCTION_0       0  '0 positional, 0 named'
              467  STORE_FAST               'bbox'

 L. 452       470  LOAD_FAST                'bbox'
              473  POP_JUMP_IF_TRUE    522  'to 522'

 L. 454       476  LOAD_FAST                'duration'
              479  POP_JUMP_IF_FALSE   137  'to 137'

 L. 455       482  LOAD_FAST                'previous'
              485  LOAD_STR                 'encoderinfo'
              488  BINARY_SUBSCR    
              489  LOAD_STR                 'duration'
              492  DUP_TOP_TWO      
              493  BINARY_SUBSCR    

 L. 456       494  LOAD_FAST                'encoderinfo'
              497  LOAD_STR                 'duration'
              500  BINARY_SUBSCR    
              501  INPLACE_ADD      
              502  ROT_THREE        
              503  STORE_SUBSCR     
              504  JUMP_BACK           137  'to 137'

 L. 457       507  CONTINUE            137  'to 137'
              510  JUMP_ABSOLUTE       522  'to 522'
              513  JUMP_FORWARD        522  'to 522'
              516  ELSE                     '522'

 L. 459       516  LOAD_CONST               None
              519  STORE_FAST               'bbox'
            522_0  COME_FROM           513  '513'

 L. 460       522  LOAD_FAST                'im_frames'
              525  LOAD_ATTR                append
              528  BUILD_MAP_3           3  ''

 L. 461       531  LOAD_FAST                'im_frame'
              534  LOAD_STR                 'im'
              537  STORE_MAP        

 L. 462       538  LOAD_FAST                'bbox'
              541  LOAD_STR                 'bbox'
              544  STORE_MAP        

 L. 463       545  LOAD_FAST                'encoderinfo'
              548  LOAD_STR                 'encoderinfo'
              551  STORE_MAP        
              552  CALL_FUNCTION_1       1  '1 positional, 0 named'
              555  POP_TOP          
              556  JUMP_BACK           137  'to 137'
              559  POP_BLOCK        
            560_0  COME_FROM_LOOP      121  '121'
              560  JUMP_BACK           115  'to 115'
              563  POP_BLOCK        
            564_0  COME_FROM_LOOP       78  '78'

 L. 466       564  LOAD_GLOBAL              len
              567  LOAD_FAST                'im_frames'
              570  CALL_FUNCTION_1       1  '1 positional, 0 named'
              573  LOAD_CONST               1
              576  COMPARE_OP               >
              579  POP_JUMP_IF_FALSE   751  'to 751'

 L. 467       582  SETUP_LOOP          747  'to 747'
              585  LOAD_FAST                'im_frames'
              588  GET_ITER         
              589  FOR_ITER            746  'to 746'
              592  STORE_FAST               'frame_data'

 L. 468       595  LOAD_FAST                'frame_data'
              598  LOAD_STR                 'im'
              601  BINARY_SUBSCR    
              602  STORE_FAST               'im_frame'

 L. 469       605  LOAD_FAST                'frame_data'
              608  LOAD_STR                 'bbox'
              611  BINARY_SUBSCR    
              612  POP_JUMP_IF_TRUE    667  'to 667'

 L. 471       615  SETUP_LOOP          658  'to 658'
              618  LOAD_GLOBAL              _get_global_header
              621  LOAD_FAST                'im_frame'

 L. 472       624  LOAD_FAST                'frame_data'
              627  LOAD_STR                 'encoderinfo'
              630  BINARY_SUBSCR    
              631  CALL_FUNCTION_2       2  '2 positional, 0 named'
              634  GET_ITER         
              635  FOR_ITER            657  'to 657'
              638  STORE_FAST               's'

 L. 473       641  LOAD_FAST                'fp'
              644  LOAD_ATTR                write
              647  LOAD_FAST                's'
              650  CALL_FUNCTION_1       1  '1 positional, 0 named'
              653  POP_TOP          
              654  JUMP_BACK           635  'to 635'
              657  POP_BLOCK        
            658_0  COME_FROM_LOOP      615  '615'

 L. 474       658  LOAD_CONST               (0, 0)
              661  STORE_FAST               'offset'
              664  JUMP_FORWARD        720  'to 720'
              667  ELSE                     '720'

 L. 477       667  LOAD_CONST               True
              670  LOAD_FAST                'frame_data'
              673  LOAD_STR                 'encoderinfo'
              676  BINARY_SUBSCR    
              677  LOAD_STR                 'include_color_table'
              680  STORE_SUBSCR     

 L. 479       681  LOAD_FAST                'im_frame'
              684  LOAD_ATTR                crop
              687  LOAD_FAST                'frame_data'
              690  LOAD_STR                 'bbox'
              693  BINARY_SUBSCR    
              694  CALL_FUNCTION_1       1  '1 positional, 0 named'
              697  STORE_FAST               'im_frame'

 L. 480       700  LOAD_FAST                'frame_data'
              703  LOAD_STR                 'bbox'
              706  BINARY_SUBSCR    
              707  LOAD_CONST               None
              710  LOAD_CONST               2
              713  BUILD_SLICE_2         2 
              716  BINARY_SUBSCR    
              717  STORE_FAST               'offset'
            720_0  COME_FROM           664  '664'

 L. 481       720  LOAD_GLOBAL              _write_frame_data
              723  LOAD_FAST                'fp'
              726  LOAD_FAST                'im_frame'
              729  LOAD_FAST                'offset'
              732  LOAD_FAST                'frame_data'
              735  LOAD_STR                 'encoderinfo'
              738  BINARY_SUBSCR    
              739  CALL_FUNCTION_4       4  '4 positional, 0 named'
              742  POP_TOP          
              743  JUMP_BACK           589  'to 589'
              746  POP_BLOCK        
            747_0  COME_FROM_LOOP      582  '582'

 L. 482       747  LOAD_CONST               True
              750  RETURN_END_IF    
            751_0  COME_FROM           579  '579'

Parse error at or near `ELSE' instruction at offset 516


def _save_all(im, fp, filename):
    _save(im, fp, filename, save_all=True)


def _save(im, fp, filename, save_all=False):
    if 'palette' in im.encoderinfo or 'palette' in im.info:
        palette = im.encoderinfo.get('palette', im.info.get('palette'))
    else:
        palette = None
        im.encoderinfo['optimize'] = im.encoderinfo.get('optimize', True)
    if not save_all or not _write_multiple_frames(im, fp, palette):
        _write_single_frame(im, fp, palette)
    fp.write(b';')
    if hasattr(fp, 'flush'):
        fp.flush()


def get_interlace(im):
    interlace = im.encoderinfo.get('interlace', 1)
    if min(im.size) < 16:
        interlace = 0
    return interlace


def _write_local_header(fp, im, offset, flags):
    transparent_color_exists = False
    try:
        transparency = im.encoderinfo['transparency']
    except KeyError:
        pass
    else:
        transparency = int(transparency)
        transparent_color_exists = True
        used_palette_colors = _get_optimize(im, im.encoderinfo)
        if used_palette_colors is not None:
            try:
                transparency = used_palette_colors.index(transparency)
            except ValueError:
                transparent_color_exists = False

        if 'duration' in im.encoderinfo:
            duration = int(im.encoderinfo['duration'] / 10)
        else:
            duration = 0
        disposal = int(im.encoderinfo.get('disposal', 0))
        if transparent_color_exists or duration != 0 or disposal:
            packed_flag = 1 if transparent_color_exists else 0
            packed_flag |= disposal << 2
            if not transparent_color_exists:
                transparency = 0
            fp.write(b'!' + o8(249) + o8(4) + o8(packed_flag) + o16(duration) + o8(transparency) + o8(0))
        if 'comment' in im.encoderinfo:
            if 1 <= len(im.encoderinfo['comment']):
                fp.write(b'!' + o8(254))
                for i in range(0, len(im.encoderinfo['comment']), 255):
                    subblock = im.encoderinfo['comment'][i:i + 255]
                    fp.write(o8(len(subblock)) + subblock)

                fp.write(o8(0))
        if 'loop' in im.encoderinfo:
            number_of_loops = im.encoderinfo['loop']
            fp.write(b'!' + o8(255) + o8(11) + b'NETSCAPE2.0' + o8(3) + o8(1) + o16(number_of_loops) + o8(0))
        include_color_table = im.encoderinfo.get('include_color_table')
        if include_color_table:
            palette_bytes = _get_palette_bytes(im)
            color_table_size = _get_color_table_size(palette_bytes)
            if color_table_size:
                flags = flags | 128
                flags = flags | color_table_size
            fp.write(b',' + o16(offset[0]) + o16(offset[1]) + o16(im.size[0]) + o16(im.size[1]) + o8(flags))
            if include_color_table:
                if color_table_size:
                    fp.write(_get_header_palette(palette_bytes))
            fp.write(o8(8))


def _save_netpbm(im, fp, filename):
    import os
    from subprocess import Popen, check_call, PIPE, CalledProcessError
    file = im._dump()
    with open(filename, 'wb') as (f):
        if im.mode != 'RGB':
            with open(os.devnull, 'wb') as (devnull):
                check_call(['ppmtogif', file], stdout=f, stderr=devnull)
        else:
            quant_cmd = [
             'ppmquant', '256', file]
            togif_cmd = ['ppmtogif']
            with open(os.devnull, 'wb') as (devnull):
                quant_proc = Popen(quant_cmd, stdout=PIPE, stderr=devnull)
                togif_proc = Popen(togif_cmd, stdin=quant_proc.stdout, stdout=f, stderr=devnull)
            quant_proc.stdout.close()
            retcode = quant_proc.wait()
            if retcode:
                raise CalledProcessError(retcode, quant_cmd)
            retcode = togif_proc.wait()
        if retcode:
            raise CalledProcessError(retcode, togif_cmd)
    try:
        os.unlink(file)
    except OSError:
        pass


_FORCE_OPTIMIZE = False

def _get_optimize(im, info):
    """
    Palette optimization is a potentially expensive operation.

    This function determines if the palette should be optimized using
    some heuristics, then returns the list of palette entries in use.

    :param im: Image object
    :param info: encoderinfo
    :returns: list of indexes of palette entries in use, or None
    """
    if im.mode in ('P', 'L'):
        if info:
            if info.get('optimize', 0):
                optimise = _FORCE_OPTIMIZE or im.mode == 'L'
                if optimise or im.width * im.height < 262144:
                    used_palette_colors = []
                    for i, count in enumerate(im.histogram()):
                        if count:
                            used_palette_colors.append(i)
                            continue

                    if optimise or len(used_palette_colors) <= 128 and max(used_palette_colors) > len(used_palette_colors):
                        pass
                    return used_palette_colors


def _get_color_table_size(palette_bytes):
    import math
    color_table_size = int(math.ceil(math.log(len(palette_bytes) // 3, 2))) - 1
    if color_table_size < 0:
        color_table_size = 0
    return color_table_size


def _get_header_palette(palette_bytes):
    """
    Returns the palette, null padded to the next power of 2 (*3) bytes
    suitable for direct inclusion in the GIF header

    :param palette_bytes: Unpadded palette bytes, in RGBRGB form
    :returns: Null padded palette
    """
    color_table_size = _get_color_table_size(palette_bytes)
    actual_target_size_diff = (2 << color_table_size) - len(palette_bytes) // 3
    if actual_target_size_diff > 0:
        palette_bytes += o8(0) * 3 * actual_target_size_diff
    return palette_bytes


def _get_palette_bytes(im):
    """
    Gets the palette for inclusion in the gif header

    :param im: Image object
    :returns: Bytes, len<=768 suitable for inclusion in gif header
    """
    return im.palette.palette


def _get_global_header(im, info):
    """Return a list of strings representing a GIF header"""
    version = b'87a'
    for extensionKey in ['transparency', 'duration', 'loop', 'comment']:
        if info and extensionKey in info:
            if not (extensionKey == 'duration' and info[extensionKey] == 0):
                if extensionKey == 'comment':
                    if not 1 <= len(info[extensionKey]) <= 255:
                        continue
                    version = b'89a'
                    break
                continue
    else:
        if im.info.get('version') == b'89a':
            version = b'89a'

    background = 0
    if 'background' in info:
        background = info['background']
        if isinstance(background, tuple):
            background = im.palette.getcolor(background)
    palette_bytes = _get_palette_bytes(im)
    color_table_size = _get_color_table_size(palette_bytes)
    return [
     b'GIF' + version + o16(im.size[0]) + o16(im.size[1]),
     o8(color_table_size + 128),
     o8(background) + o8(0),
     _get_header_palette(palette_bytes)]


def _write_frame_data(fp, im_frame, offset, params):
    try:
        im_frame.encoderinfo = params
        _write_local_header(fp, im_frame, offset, 0)
        ImageFile._save(im_frame, fp, [
         ('gif', (0, 0) + im_frame.size, 0,
          RAWMODE[im_frame.mode])])
        fp.write(b'\x00')
    finally:
        del im_frame.encoderinfo


def getheader(im, palette=None, info=None):
    """
    Legacy Method to get Gif data from image.

    Warning:: May modify image data.

    :param im: Image object
    :param palette: bytes object containing the source palette, or ....
    :param info: encoderinfo
    :returns: tuple of(list of header items, optimized palette)

    """
    used_palette_colors = _get_optimize(im, info)
    if info is None:
        info = {}
    if 'background' not in info:
        if 'background' in im.info:
            info['background'] = im.info['background']
    im_mod = _normalize_palette(im, palette, info)
    im.palette = im_mod.palette
    im.im = im_mod.im
    header = _get_global_header(im, info)
    return (
     header, used_palette_colors)


def getdata(im, offset=(
 0, 0), **params):
    r"""
    Legacy Method

    Return a list of strings representing this image.
    The first string is a local image header, the rest contains
    encoded image data.

    :param im: Image object
    :param offset: Tuple of (x, y) pixels. Defaults to (0,0)
    :param \**params: E.g. duration or other encoder info parameters
    :returns: List of Bytes containing gif encoded frame data

    """

    class Collector(object):
        data = []

        def write(self, data):
            self.data.append(data)

    im.load()
    fp = Collector()
    _write_frame_data(fp, im, offset, params)
    return fp.data


Image.register_open(GifImageFile.format, GifImageFile, _accept)
Image.register_save(GifImageFile.format, _save)
Image.register_save_all(GifImageFile.format, _save_all)
Image.register_extension(GifImageFile.format, '.gif')
Image.register_mime(GifImageFile.format, 'image/gif')