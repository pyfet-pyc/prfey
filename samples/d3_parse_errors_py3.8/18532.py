# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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

    def load(self):
        """Load image data based on tile list"""
        pixel = Image.Image.load(self)
        if self.tile is None:
            raise OSError('cannot load this image')
        if not self.tile:
            return pixel
        self.map = None
        use_mmap = self.filename and len(self.tile) == 1
        use_mmap = use_mmap and not hasattr(sys, 'pypy_version_info')
        readonly = 0
        try:
            read = self.load_read
            use_mmap = False
        except AttributeError:
            read = self.fp.read

        try:
            seek = self.load_seek
            use_mmap = False
        except AttributeError:
            seek = self.fp.seek
        else:
            if use_mmap:
                decoder_name, extents, offset, args = self.tile[0]
                if not decoder_name == 'raw'and len(args) >= 3 and len(args) >= 3 or args[0] in Image._MAPMODES:
                    try:
                        if hasattr(Image.core, 'map'):
                            self.map = Image.core.map(self.filename)
                            self.map.seek(offset)
                            self.im = self.map.readimage(self.mode, self.size, args[1], args[2])
                        else:
                            import mmap
                            with open(self.filename, 'r') as fp:
                                self.map = mmap.mmap((fp.fileno()),
                                  0, access=(mmap.ACCESS_READ))
                            self.im = Image.core.map_buffer(self.map, self.size, decoder_name, extents, offset, args)
                        readonly = 1
                        if self.palette:
                            self.palette.dirty = 1
                    except (AttributeError, OSError, ImportError):
                        self.map = None
                    else:
                        self.load_prepare()
                err_code = -3
                self.map or self.tile.sort(key=_tilesort)
                try:
                    prefix = self.tile_prefix
                except AttributeError:
                    prefix = b''

                for decoder_name, extents, offset, args in self.tile:
                    decoder = Image._getdecoder(self.mode, decoder_name, args, self.decoderconfig)
                    try:
                        seek(offset)
                        decoder.setimage(self.im, extents)
                        if decoder.pulls_fd:
                            decoder.setfd(self.fp)
                            status, err_code = decoder.decode(b'')
                        else:
                            b = prefix
                            while True:
                                try:
                                    s = read(self.decodermaxblock)
                                except (IndexError, struct.error):
                                    if LOAD_TRUNCATED_IMAGES:
                                        break
                                    else:
                                        raise OSError('image file is truncated')
                                else:
                                    if not s:
                                        if LOAD_TRUNCATED_IMAGES:
                                            pass
                                        else:
                                            break
                                        raise OSError('image file is truncated (%d bytes not processed)' % len(b))
                                    b = b + s
                                    n, err_code = decoder.decode(b)
                                    if n < 0:
                                        pass
                                    else:
                                        b = b[n:]

                    finally:
                        decoder.cleanup()

                else:
                    self.tile = []
                    self.readonly = readonly
                    self.load_end()
                    if self._exclusive_fp:
                        if self._close_exclusive_fp_after_loading:
                            self.fp.close()
                    self.fp = None
                    if not self.map:
                        if not LOAD_TRUNCATED_IMAGES:
                            if err_code < 0:
                                raise_ioerror(err_code)
                        return Image.Image.load(self)

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
                if not (self.offset > 0 or self.data):
                    return
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
                    self.decoder = Image._getdecoder(im.mode, d, a, im.decoderconfig)
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
                with io.BytesIO(self.data) as fp:
                    try:
                        self.image = Image.open(fp)
                    finally:
                        self.image.load()

            return self.image


def _save--- This code section failed: ---

 L. 483         0  LOAD_FAST                'im'
                2  LOAD_METHOD              load
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 484         8  LOAD_GLOBAL              hasattr
               10  LOAD_FAST                'im'
               12  LOAD_STR                 'encoderconfig'
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     24  'to 24'

 L. 485        18  LOAD_CONST               ()
               20  LOAD_FAST                'im'
               22  STORE_ATTR               encoderconfig
             24_0  COME_FROM            16  '16'

 L. 486        24  LOAD_FAST                'tile'
               26  LOAD_ATTR                sort
               28  LOAD_GLOBAL              _tilesort
               30  LOAD_CONST               ('key',)
               32  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               34  POP_TOP          

 L. 491        36  LOAD_GLOBAL              max
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

 L. 492        58  LOAD_FAST                'fp'
               60  LOAD_GLOBAL              sys
               62  LOAD_ATTR                stdout
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    80  'to 80'

 L. 493        68  LOAD_FAST                'fp'
               70  LOAD_METHOD              flush
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          

 L. 494        76  LOAD_CONST               None
               78  RETURN_VALUE     
             80_0  COME_FROM            66  '66'

 L. 495        80  SETUP_FINALLY       102  'to 102'

 L. 496        82  LOAD_FAST                'fp'
               84  LOAD_METHOD              fileno
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'fh'

 L. 497        90  LOAD_FAST                'fp'
               92  LOAD_METHOD              flush
               94  CALL_METHOD_0         0  ''
               96  POP_TOP          
               98  POP_BLOCK        
              100  JUMP_FORWARD        296  'to 296'
            102_0  COME_FROM_FINALLY    80  '80'

 L. 498       102  DUP_TOP          
              104  LOAD_GLOBAL              AttributeError
              106  LOAD_GLOBAL              io
              108  LOAD_ATTR                UnsupportedOperation
              110  BUILD_TUPLE_2         2 
              112  COMPARE_OP               exception-match
          114_116  POP_JUMP_IF_FALSE   294  'to 294'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 500       124  LOAD_FAST                'tile'
              126  GET_ITER         
            128_0  COME_FROM           288  '288'
              128  FOR_ITER            290  'to 290'
              130  UNPACK_SEQUENCE_4     4 
              132  STORE_FAST               'e'
              134  STORE_FAST               'b'
              136  STORE_FAST               'o'
              138  STORE_FAST               'a'

 L. 501       140  LOAD_GLOBAL              Image
              142  LOAD_METHOD              _getencoder
              144  LOAD_FAST                'im'
              146  LOAD_ATTR                mode
              148  LOAD_FAST                'e'
              150  LOAD_FAST                'a'
              152  LOAD_FAST                'im'
              154  LOAD_ATTR                encoderconfig
              156  CALL_METHOD_4         4  ''
              158  STORE_FAST               'e'

 L. 502       160  LOAD_FAST                'o'
              162  LOAD_CONST               0
              164  COMPARE_OP               >
              166  POP_JUMP_IF_FALSE   178  'to 178'

 L. 503       168  LOAD_FAST                'fp'
              170  LOAD_METHOD              seek
              172  LOAD_FAST                'o'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          
            178_0  COME_FROM           166  '166'

 L. 504       178  LOAD_FAST                'e'
              180  LOAD_METHOD              setimage
              182  LOAD_FAST                'im'
              184  LOAD_ATTR                im
              186  LOAD_FAST                'b'
              188  CALL_METHOD_2         2  ''
              190  POP_TOP          

 L. 505       192  LOAD_FAST                'e'
              194  LOAD_ATTR                pushes_fd
              196  POP_JUMP_IF_FALSE   222  'to 222'

 L. 506       198  LOAD_FAST                'e'
              200  LOAD_METHOD              setfd
              202  LOAD_FAST                'fp'
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          

 L. 507       208  LOAD_FAST                'e'
              210  LOAD_METHOD              encode_to_pyfd
              212  CALL_METHOD_0         0  ''
              214  UNPACK_SEQUENCE_2     2 
              216  STORE_FAST               'l'
              218  STORE_FAST               's'
              220  JUMP_FORWARD        258  'to 258'
            222_0  COME_FROM           256  '256'
            222_1  COME_FROM           250  '250'
            222_2  COME_FROM           196  '196'

 L. 510       222  LOAD_FAST                'e'
              224  LOAD_METHOD              encode
              226  LOAD_FAST                'bufsize'
              228  CALL_METHOD_1         1  ''
              230  UNPACK_SEQUENCE_3     3 
              232  STORE_FAST               'l'
              234  STORE_FAST               's'
              236  STORE_FAST               'd'

 L. 511       238  LOAD_FAST                'fp'
              240  LOAD_METHOD              write
              242  LOAD_FAST                'd'
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L. 512       248  LOAD_FAST                's'
              250  POP_JUMP_IF_FALSE_BACK   222  'to 222'

 L. 513   252_254  JUMP_FORWARD        258  'to 258'
              256  JUMP_BACK           222  'to 222'
            258_0  COME_FROM           252  '252'
            258_1  COME_FROM           220  '220'

 L. 514       258  LOAD_FAST                's'
              260  LOAD_CONST               0
              262  COMPARE_OP               <
          264_266  POP_JUMP_IF_FALSE   280  'to 280'

 L. 515       268  LOAD_GLOBAL              OSError
              270  LOAD_STR                 'encoder error %d when writing image file'
              272  LOAD_FAST                's'
              274  BINARY_MODULO    
              276  CALL_FUNCTION_1       1  ''
              278  RAISE_VARARGS_1       1  'exception instance'
            280_0  COME_FROM           264  '264'

 L. 516       280  LOAD_FAST                'e'
              282  LOAD_METHOD              cleanup
              284  CALL_METHOD_0         0  ''
              286  POP_TOP          
              288  JUMP_BACK           128  'to 128'
            290_0  COME_FROM           128  '128'
              290  POP_EXCEPT       
              292  JUMP_FORWARD        444  'to 444'
            294_0  COME_FROM           114  '114'
              294  END_FINALLY      
            296_0  COME_FROM           100  '100'

 L. 519       296  LOAD_FAST                'tile'
              298  GET_ITER         
            300_0  COME_FROM           440  '440'
              300  FOR_ITER            444  'to 444'
              302  UNPACK_SEQUENCE_4     4 
              304  STORE_FAST               'e'
              306  STORE_FAST               'b'
              308  STORE_FAST               'o'
              310  STORE_FAST               'a'

 L. 520       312  LOAD_GLOBAL              Image
              314  LOAD_METHOD              _getencoder
              316  LOAD_FAST                'im'
              318  LOAD_ATTR                mode
              320  LOAD_FAST                'e'
              322  LOAD_FAST                'a'
              324  LOAD_FAST                'im'
              326  LOAD_ATTR                encoderconfig
              328  CALL_METHOD_4         4  ''
              330  STORE_FAST               'e'

 L. 521       332  LOAD_FAST                'o'
              334  LOAD_CONST               0
              336  COMPARE_OP               >
          338_340  POP_JUMP_IF_FALSE   352  'to 352'

 L. 522       342  LOAD_FAST                'fp'
              344  LOAD_METHOD              seek
              346  LOAD_FAST                'o'
              348  CALL_METHOD_1         1  ''
              350  POP_TOP          
            352_0  COME_FROM           338  '338'

 L. 523       352  LOAD_FAST                'e'
              354  LOAD_METHOD              setimage
              356  LOAD_FAST                'im'
              358  LOAD_ATTR                im
              360  LOAD_FAST                'b'
              362  CALL_METHOD_2         2  ''
              364  POP_TOP          

 L. 524       366  LOAD_FAST                'e'
              368  LOAD_ATTR                pushes_fd
          370_372  POP_JUMP_IF_FALSE   398  'to 398'

 L. 525       374  LOAD_FAST                'e'
              376  LOAD_METHOD              setfd
              378  LOAD_FAST                'fp'
              380  CALL_METHOD_1         1  ''
              382  POP_TOP          

 L. 526       384  LOAD_FAST                'e'
              386  LOAD_METHOD              encode_to_pyfd
              388  CALL_METHOD_0         0  ''
              390  UNPACK_SEQUENCE_2     2 
              392  STORE_FAST               'l'
              394  STORE_FAST               's'
              396  JUMP_FORWARD        410  'to 410'
            398_0  COME_FROM           370  '370'

 L. 528       398  LOAD_FAST                'e'
              400  LOAD_METHOD              encode_to_file
              402  LOAD_FAST                'fh'
              404  LOAD_FAST                'bufsize'
              406  CALL_METHOD_2         2  ''
              408  STORE_FAST               's'
            410_0  COME_FROM           396  '396'

 L. 529       410  LOAD_FAST                's'
              412  LOAD_CONST               0
              414  COMPARE_OP               <
          416_418  POP_JUMP_IF_FALSE   432  'to 432'

 L. 530       420  LOAD_GLOBAL              OSError
              422  LOAD_STR                 'encoder error %d when writing image file'
              424  LOAD_FAST                's'
              426  BINARY_MODULO    
              428  CALL_FUNCTION_1       1  ''
              430  RAISE_VARARGS_1       1  'exception instance'
            432_0  COME_FROM           416  '416'

 L. 531       432  LOAD_FAST                'e'
              434  LOAD_METHOD              cleanup
              436  CALL_METHOD_0         0  ''
              438  POP_TOP          
          440_442  JUMP_BACK           300  'to 300'
            444_0  COME_FROM           300  '300'
            444_1  COME_FROM           292  '292'

 L. 532       444  LOAD_GLOBAL              hasattr
              446  LOAD_FAST                'fp'
              448  LOAD_STR                 'flush'
              450  CALL_FUNCTION_2       2  ''
          452_454  POP_JUMP_IF_FALSE   464  'to 464'

 L. 533       456  LOAD_FAST                'fp'
              458  LOAD_METHOD              flush
              460  CALL_METHOD_0         0  ''
              462  POP_TOP          
            464_0  COME_FROM           452  '452'

Parse error at or near `JUMP_BACK' instruction at offset 256


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
    if size <= SAFEBLOCK:
        return fp.read(size)
    data = []
    while True:
        if size > 0:
            block = fp.read(min(size, SAFEBLOCK))
            if not block:
                pass
            else:
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