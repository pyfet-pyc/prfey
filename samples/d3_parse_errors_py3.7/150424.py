# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\TiffImagePlugin.py
import io, itertools, logging, os, struct, warnings
from collections.abc import MutableMapping
from fractions import Fraction
from numbers import Number, Rational
from . import Image, ImageFile, ImagePalette, TiffTags
from ._binary import o8
from .TiffTags import TYPES
logger = logging.getLogger(__name__)
READ_LIBTIFF = False
WRITE_LIBTIFF = False
IFD_LEGACY_API = True
II = 'II'
MM = 'MM'
IMAGEWIDTH = 256
IMAGELENGTH = 257
BITSPERSAMPLE = 258
COMPRESSION = 259
PHOTOMETRIC_INTERPRETATION = 262
FILLORDER = 266
IMAGEDESCRIPTION = 270
STRIPOFFSETS = 273
SAMPLESPERPIXEL = 277
ROWSPERSTRIP = 278
STRIPBYTECOUNTS = 279
X_RESOLUTION = 282
Y_RESOLUTION = 283
PLANAR_CONFIGURATION = 284
RESOLUTION_UNIT = 296
TRANSFERFUNCTION = 301
SOFTWARE = 305
DATE_TIME = 306
ARTIST = 315
PREDICTOR = 317
COLORMAP = 320
TILEOFFSETS = 324
SUBIFD = 330
EXTRASAMPLES = 338
SAMPLEFORMAT = 339
JPEGTABLES = 347
REFERENCEBLACKWHITE = 532
COPYRIGHT = 33432
IPTC_NAA_CHUNK = 33723
PHOTOSHOP_CHUNK = 34377
ICCPROFILE = 34675
EXIFIFD = 34665
XMP = 700
JPEGQUALITY = 65537
IMAGEJ_META_DATA_BYTE_COUNTS = 50838
IMAGEJ_META_DATA = 50839
COMPRESSION_INFO = {1:'raw', 
 2:'tiff_ccitt', 
 3:'group3', 
 4:'group4', 
 5:'tiff_lzw', 
 6:'tiff_jpeg', 
 7:'jpeg', 
 8:'tiff_adobe_deflate', 
 32771:'tiff_raw_16', 
 32773:'packbits', 
 32809:'tiff_thunderscan', 
 32946:'tiff_deflate', 
 34676:'tiff_sgilog', 
 34677:'tiff_sgilog24', 
 34925:'lzma', 
 50000:'zstd', 
 50001:'webp'}
COMPRESSION_INFO_REV = {v:k for k, v in COMPRESSION_INFO.items()}
OPEN_INFO = {(
 II, 0, (1, ), 1, (1, ), ()): ('1', '1;I'), 
 (
 MM, 0, (1, ), 1, (1, ), ()): ('1', '1;I'), 
 (
 II, 0, (1, ), 2, (1, ), ()): ('1', '1;IR'), 
 (
 MM, 0, (1, ), 2, (1, ), ()): ('1', '1;IR'), 
 (
 II, 1, (1, ), 1, (1, ), ()): ('1', '1'), 
 (
 MM, 1, (1, ), 1, (1, ), ()): ('1', '1'), 
 (
 II, 1, (1, ), 2, (1, ), ()): ('1', '1;R'), 
 (
 MM, 1, (1, ), 2, (1, ), ()): ('1', '1;R'), 
 (
 II, 0, (1, ), 1, (2, ), ()): ('L', 'L;2I'), 
 (
 MM, 0, (1, ), 1, (2, ), ()): ('L', 'L;2I'), 
 (
 II, 0, (1, ), 2, (2, ), ()): ('L', 'L;2IR'), 
 (
 MM, 0, (1, ), 2, (2, ), ()): ('L', 'L;2IR'), 
 (
 II, 1, (1, ), 1, (2, ), ()): ('L', 'L;2'), 
 (
 MM, 1, (1, ), 1, (2, ), ()): ('L', 'L;2'), 
 (
 II, 1, (1, ), 2, (2, ), ()): ('L', 'L;2R'), 
 (
 MM, 1, (1, ), 2, (2, ), ()): ('L', 'L;2R'), 
 (
 II, 0, (1, ), 1, (4, ), ()): ('L', 'L;4I'), 
 (
 MM, 0, (1, ), 1, (4, ), ()): ('L', 'L;4I'), 
 (
 II, 0, (1, ), 2, (4, ), ()): ('L', 'L;4IR'), 
 (
 MM, 0, (1, ), 2, (4, ), ()): ('L', 'L;4IR'), 
 (
 II, 1, (1, ), 1, (4, ), ()): ('L', 'L;4'), 
 (
 MM, 1, (1, ), 1, (4, ), ()): ('L', 'L;4'), 
 (
 II, 1, (1, ), 2, (4, ), ()): ('L', 'L;4R'), 
 (
 MM, 1, (1, ), 2, (4, ), ()): ('L', 'L;4R'), 
 (
 II, 0, (1, ), 1, (8, ), ()): ('L', 'L;I'), 
 (
 MM, 0, (1, ), 1, (8, ), ()): ('L', 'L;I'), 
 (
 II, 0, (1, ), 2, (8, ), ()): ('L', 'L;IR'), 
 (
 MM, 0, (1, ), 2, (8, ), ()): ('L', 'L;IR'), 
 (
 II, 1, (1, ), 1, (8, ), ()): ('L', 'L'), 
 (
 MM, 1, (1, ), 1, (8, ), ()): ('L', 'L'), 
 (
 II, 1, (1, ), 2, (8, ), ()): ('L', 'L;R'), 
 (
 MM, 1, (1, ), 2, (8, ), ()): ('L', 'L;R'), 
 (
 II, 1, (1, ), 1, (12, ), ()): ('I;16', 'I;12'), 
 (
 II, 1, (1, ), 1, (16, ), ()): ('I;16', 'I;16'), 
 (
 MM, 1, (1, ), 1, (16, ), ()): ('I;16B', 'I;16B'), 
 (
 II, 1, (2, ), 1, (16, ), ()): ('I', 'I;16S'), 
 (
 MM, 1, (2, ), 1, (16, ), ()): ('I', 'I;16BS'), 
 (
 II, 0, (3, ), 1, (32, ), ()): ('F', 'F;32F'), 
 (
 MM, 0, (3, ), 1, (32, ), ()): ('F', 'F;32BF'), 
 (
 II, 1, (1, ), 1, (32, ), ()): ('I', 'I;32N'), 
 (
 II, 1, (2, ), 1, (32, ), ()): ('I', 'I;32S'), 
 (
 MM, 1, (2, ), 1, (32, ), ()): ('I', 'I;32BS'), 
 (
 II, 1, (3, ), 1, (32, ), ()): ('F', 'F;32F'), 
 (
 MM, 1, (3, ), 1, (32, ), ()): ('F', 'F;32BF'), 
 (
 II, 1, (1, ), 1, (8, 8), (2, )): ('LA', 'LA'), 
 (
 MM, 1, (1, ), 1, (8, 8), (2, )): ('LA', 'LA'), 
 (
 II, 2, (1, ), 1, (8, 8, 8), ()): ('RGB', 'RGB'), 
 (
 MM, 2, (1, ), 1, (8, 8, 8), ()): ('RGB', 'RGB'), 
 (
 II, 2, (1, ), 2, (8, 8, 8), ()): ('RGB', 'RGB;R'), 
 (
 MM, 2, (1, ), 2, (8, 8, 8), ()): ('RGB', 'RGB;R'), 
 (
 II, 2, (1, ), 1, (8, 8, 8, 8), ()): ('RGBA', 'RGBA'), 
 (
 MM, 2, (1, ), 1, (8, 8, 8, 8), ()): ('RGBA', 'RGBA'), 
 (
 II, 2, (1, ), 1, (8, 8, 8, 8), (0, )): ('RGBX', 'RGBX'), 
 (
 MM, 2, (1, ), 1, (8, 8, 8, 8), (0, )): ('RGBX', 'RGBX'), 
 (
 II, 2, (1, ), 1, (8, 8, 8, 8, 8), (0, 0)): ('RGBX', 'RGBXX'), 
 (
 MM, 2, (1, ), 1, (8, 8, 8, 8, 8), (0, 0)): ('RGBX', 'RGBXX'), 
 (
 II, 2, (1, ), 1, (8, 8, 8, 8, 8, 8), (0, 0, 0)): ('RGBX', 'RGBXXX'), 
 (
 MM, 2, (1, ), 1, (8, 8, 8, 8, 8, 8), (0, 0, 0)): ('RGBX', 'RGBXXX'), 
 (
 II, 2, (1, ), 1, (8, 8, 8, 8), (1, )): ('RGBA', 'RGBa'), 
 (
 MM, 2, (1, ), 1, (8, 8, 8, 8), (1, )): ('RGBA', 'RGBa'), 
 (
 II, 2, (1, ), 1, (8, 8, 8, 8, 8), (1, 0)): ('RGBA', 'RGBaX'), 
 (
 MM, 2, (1, ), 1, (8, 8, 8, 8, 8), (1, 0)): ('RGBA', 'RGBaX'), 
 (
 II, 2, (1, ), 1, (8, 8, 8, 8, 8, 8), (1, 0, 0)): ('RGBA', 'RGBaXX'), 
 (
 MM, 2, (1, ), 1, (8, 8, 8, 8, 8, 8), (1, 0, 0)): ('RGBA', 'RGBaXX'), 
 (
 II, 2, (1, ), 1, (8, 8, 8, 8), (2, )): ('RGBA', 'RGBA'), 
 (
 MM, 2, (1, ), 1, (8, 8, 8, 8), (2, )): ('RGBA', 'RGBA'), 
 (
 II, 2, (1, ), 1, (8, 8, 8, 8, 8), (2, 0)): ('RGBA', 'RGBAX'), 
 (
 MM, 2, (1, ), 1, (8, 8, 8, 8, 8), (2, 0)): ('RGBA', 'RGBAX'), 
 (
 II, 2, (1, ), 1, (8, 8, 8, 8, 8, 8), (2, 0, 0)): ('RGBA', 'RGBAXX'), 
 (
 MM, 2, (1, ), 1, (8, 8, 8, 8, 8, 8), (2, 0, 0)): ('RGBA', 'RGBAXX'), 
 (
 II, 2, (1, ), 1, (8, 8, 8, 8), (999, )): ('RGBA', 'RGBA'), 
 (
 MM, 2, (1, ), 1, (8, 8, 8, 8), (999, )): ('RGBA', 'RGBA'), 
 (
 II, 2, (1, ), 1, (16, 16, 16), ()): ('RGB', 'RGB;16L'), 
 (
 MM, 2, (1, ), 1, (16, 16, 16), ()): ('RGB', 'RGB;16B'), 
 (
 II, 2, (1, ), 1, (16, 16, 16, 16), ()): ('RGBA', 'RGBA;16L'), 
 (
 MM, 2, (1, ), 1, (16, 16, 16, 16), ()): ('RGBA', 'RGBA;16B'), 
 (
 II, 2, (1, ), 1, (16, 16, 16, 16), (0, )): ('RGBX', 'RGBX;16L'), 
 (
 MM, 2, (1, ), 1, (16, 16, 16, 16), (0, )): ('RGBX', 'RGBX;16B'), 
 (
 II, 2, (1, ), 1, (16, 16, 16, 16), (1, )): ('RGBA', 'RGBa;16L'), 
 (
 MM, 2, (1, ), 1, (16, 16, 16, 16), (1, )): ('RGBA', 'RGBa;16B'), 
 (
 II, 2, (1, ), 1, (16, 16, 16, 16), (2, )): ('RGBA', 'RGBA;16L'), 
 (
 MM, 2, (1, ), 1, (16, 16, 16, 16), (2, )): ('RGBA', 'RGBA;16B'), 
 (
 II, 3, (1, ), 1, (1, ), ()): ('P', 'P;1'), 
 (
 MM, 3, (1, ), 1, (1, ), ()): ('P', 'P;1'), 
 (
 II, 3, (1, ), 2, (1, ), ()): ('P', 'P;1R'), 
 (
 MM, 3, (1, ), 2, (1, ), ()): ('P', 'P;1R'), 
 (
 II, 3, (1, ), 1, (2, ), ()): ('P', 'P;2'), 
 (
 MM, 3, (1, ), 1, (2, ), ()): ('P', 'P;2'), 
 (
 II, 3, (1, ), 2, (2, ), ()): ('P', 'P;2R'), 
 (
 MM, 3, (1, ), 2, (2, ), ()): ('P', 'P;2R'), 
 (
 II, 3, (1, ), 1, (4, ), ()): ('P', 'P;4'), 
 (
 MM, 3, (1, ), 1, (4, ), ()): ('P', 'P;4'), 
 (
 II, 3, (1, ), 2, (4, ), ()): ('P', 'P;4R'), 
 (
 MM, 3, (1, ), 2, (4, ), ()): ('P', 'P;4R'), 
 (
 II, 3, (1, ), 1, (8, ), ()): ('P', 'P'), 
 (
 MM, 3, (1, ), 1, (8, ), ()): ('P', 'P'), 
 (
 II, 3, (1, ), 1, (8, 8), (2, )): ('PA', 'PA'), 
 (
 MM, 3, (1, ), 1, (8, 8), (2, )): ('PA', 'PA'), 
 (
 II, 3, (1, ), 2, (8, ), ()): ('P', 'P;R'), 
 (
 MM, 3, (1, ), 2, (8, ), ()): ('P', 'P;R'), 
 (
 II, 5, (1, ), 1, (8, 8, 8, 8), ()): ('CMYK', 'CMYK'), 
 (
 MM, 5, (1, ), 1, (8, 8, 8, 8), ()): ('CMYK', 'CMYK'), 
 (
 II, 5, (1, ), 1, (8, 8, 8, 8, 8), (0, )): ('CMYK', 'CMYKX'), 
 (
 MM, 5, (1, ), 1, (8, 8, 8, 8, 8), (0, )): ('CMYK', 'CMYKX'), 
 (
 II, 5, (1, ), 1, (8, 8, 8, 8, 8, 8), (0, 0)): ('CMYK', 'CMYKXX'), 
 (
 MM, 5, (1, ), 1, (8, 8, 8, 8, 8, 8), (0, 0)): ('CMYK', 'CMYKXX'), 
 (
 II, 5, (1, ), 1, (16, 16, 16, 16), ()): ('CMYK', 'CMYK;16L'), 
 (
 II, 6, (1, ), 1, (8, 8, 8), ()): ('RGB', 'RGBX'), 
 (
 MM, 6, (1, ), 1, (8, 8, 8), ()): ('RGB', 'RGBX'), 
 (
 II, 8, (1, ), 1, (8, 8, 8), ()): ('LAB', 'LAB'), 
 (
 MM, 8, (1, ), 1, (8, 8, 8), ()): ('LAB', 'LAB')}
PREFIXES = [
 'MM\x00*',
 'II*\x00',
 'MM*\x00',
 'II\x00*']

def _accept(prefix):
    return prefix[:4] in PREFIXES


def _limit_rational(val, max_val):
    inv = abs(val) > 1
    n_d = IFDRational(1 / val if inv else val).limit_rational(max_val)
    if inv:
        return n_d[::-1]
    return n_d


def _limit_signed_rational(val, max_val, min_val):
    frac = Fraction(val)
    n_d = (frac.numerator, frac.denominator)
    if min(n_d) < min_val:
        n_d = _limit_rational(val, abs(min_val))
    if max(n_d) > max_val:
        val = Fraction(*n_d)
        n_d = _limit_rational(val, max_val)
    return n_d


_load_dispatch = {}
_write_dispatch = {}

class IFDRational(Rational):
    __doc__ = 'Implements a rational class where 0/0 is a legal value to match\n    the in the wild use of exif rationals.\n\n    e.g., DigitalZoomRatio - 0.00/0.00  indicates that no digital zoom was used\n    '
    __slots__ = ('_numerator', '_denominator', '_val')

    def __init__(self, value, denominator=1):
        """
        :param value: either an integer numerator, a
        float/rational/other number, or an IFDRational
        :param denominator: Optional integer denominator
        """
        if isinstance(value, IFDRational):
            self._numerator = value.numerator
            self._denominator = value.denominator
            self._val = value._val
            return
        if isinstance(value, Fraction):
            self._numerator = value.numerator
            self._denominator = value.denominator
        else:
            self._numerator = value
            self._denominator = denominator
        if denominator == 0:
            self._val = float('nan')
        elif denominator == 1:
            self._val = Fraction(value)
        else:
            self._val = Fraction(value, denominator)

    @property
    def numerator(a):
        return a._numerator

    @property
    def denominator(a):
        return a._denominator

    def limit_rational(self, max_denominator):
        """

        :param max_denominator: Integer, the maximum denominator value
        :returns: Tuple of (numerator, denominator)
        """
        if self.denominator == 0:
            return (self.numerator, self.denominator)
        f = self._val.limit_denominator(max_denominator)
        return (
         f.numerator, f.denominator)

    def __repr__(self):
        return str(float(self._val))

    def __hash__(self):
        return self._val.__hash__()

    def __eq__(self, other):
        if isinstance(other, IFDRational):
            other = other._val
        return self._val == other

    def _delegate(op):

        def delegate(self, *args):
            return (getattr(self._val, op))(*args)

        return delegate

    __add__ = _delegate('__add__')
    __radd__ = _delegate('__radd__')
    __sub__ = _delegate('__sub__')
    __rsub__ = _delegate('__rsub__')
    __mul__ = _delegate('__mul__')
    __rmul__ = _delegate('__rmul__')
    __truediv__ = _delegate('__truediv__')
    __rtruediv__ = _delegate('__rtruediv__')
    __floordiv__ = _delegate('__floordiv__')
    __rfloordiv__ = _delegate('__rfloordiv__')
    __mod__ = _delegate('__mod__')
    __rmod__ = _delegate('__rmod__')
    __pow__ = _delegate('__pow__')
    __rpow__ = _delegate('__rpow__')
    __pos__ = _delegate('__pos__')
    __neg__ = _delegate('__neg__')
    __abs__ = _delegate('__abs__')
    __trunc__ = _delegate('__trunc__')
    __lt__ = _delegate('__lt__')
    __gt__ = _delegate('__gt__')
    __le__ = _delegate('__le__')
    __ge__ = _delegate('__ge__')
    __bool__ = _delegate('__bool__')
    __ceil__ = _delegate('__ceil__')
    __floor__ = _delegate('__floor__')
    __round__ = _delegate('__round__')


class ImageFileDirectory_v2(MutableMapping):
    __doc__ = "This class represents a TIFF tag directory.  To speed things up, we\n    don't decode tags unless they're asked for.\n\n    Exposes a dictionary interface of the tags in the directory::\n\n        ifd = ImageFileDirectory_v2()\n        ifd[key] = 'Some Data'\n        ifd.tagtype[key] = TiffTags.ASCII\n        print(ifd[key])\n        'Some Data'\n\n    Individual values are returned as the strings or numbers, sequences are\n    returned as tuples of the values.\n\n    The tiff metadata type of each item is stored in a dictionary of\n    tag types in\n    :attr:`~PIL.TiffImagePlugin.ImageFileDirectory_v2.tagtype`. The types\n    are read from a tiff file, guessed from the type added, or added\n    manually.\n\n    Data Structures:\n\n        * self.tagtype = {}\n\n          * Key: numerical tiff tag number\n          * Value: integer corresponding to the data type from\n                   ~PIL.TiffTags.TYPES`\n\n    .. versionadded:: 3.0.0\n    "

    def __init__(self, ifh='II*\x00\x00\x00\x00\x00', prefix=None):
        """Initialize an ImageFileDirectory.

        To construct an ImageFileDirectory from a real file, pass the 8-byte
        magic header to the constructor.  To only set the endianness, pass it
        as the 'prefix' keyword argument.

        :param ifh: One of the accepted magic headers (cf. PREFIXES); also sets
              endianness.
        :param prefix: Override the endianness of the file.
        """
        if ifh[:4] not in PREFIXES:
            raise SyntaxError(f"not a TIFF file (header {repr(ifh)} not valid)")
        self._prefix = prefix if prefix is not None else ifh[:2]
        if self._prefix == MM:
            self._endian = '>'
        elif self._prefix == II:
            self._endian = '<'
        else:
            raise SyntaxError('not a TIFF IFD')
        self.tagtype = {}
        self.reset()
        self.next, = self._unpack('L', ifh[4:])
        self._legacy_api = False

    prefix = property(lambda self: self._prefix)
    offset = property(lambda self: self._offset)
    legacy_api = property(lambda self: self._legacy_api)

    @legacy_api.setter
    def legacy_api(self, value):
        raise Exception('Not allowing setting of legacy api')

    def reset(self):
        self._tags_v1 = {}
        self._tags_v2 = {}
        self._tagdata = {}
        self.tagtype = {}
        self._next = None
        self._offset = None

    def __str__(self):
        return str(dict(self))

    def named(self):
        """
        :returns: dict of name|key: value

        Returns the complete tag dictionary, with named tags where possible.
        """
        return {TiffTags.lookup(code).name:value for code, value in self.items()}

    def __len__(self):
        return len(set(self._tagdata) | set(self._tags_v2))

    def __getitem__(self, tag):
        if tag not in self._tags_v2:
            data = self._tagdata[tag]
            typ = self.tagtype[tag]
            size, handler = self._load_dispatch[typ]
            self[tag] = handler(self, data, self.legacy_api)
        val = self._tags_v2[tag]
        if self.legacy_api:
            if not isinstance(val, (tuple, bytes)):
                val = (
                 val,)
            return val

    def __contains__(self, tag):
        return tag in self._tags_v2 or tag in self._tagdata

    def __setitem__(self, tag, value):
        self._setitem(tag, value, self.legacy_api)

    def _setitem(self, tag, value, legacy_api):
        basetypes = (
         Number, bytes, str)
        info = TiffTags.lookup(tag)
        values = [value] if isinstance(value, basetypes) else value
        if tag not in self.tagtype:
            if info.type:
                self.tagtype[tag] = info.type
            else:
                self.tagtype[tag] = TiffTags.UNDEFINED
                if all((isinstance(v, IFDRational) for v in values)):
                    self.tagtype[tag] = TiffTags.RATIONAL if all((v >= 0 for v in values)) else TiffTags.SIGNED_RATIONAL
                elif all((isinstance(v, int) for v in values)):
                    if all((0 <= v < 65536 for v in values)):
                        self.tagtype[tag] = TiffTags.SHORT
                    elif all((-32768 < v < 32768 for v in values)):
                        self.tagtype[tag] = TiffTags.SIGNED_SHORT
                    else:
                        self.tagtype[tag] = TiffTags.LONG if all((v >= 0 for v in values)) else TiffTags.SIGNED_LONG
                elif all((isinstance(v, float) for v in values)):
                    self.tagtype[tag] = TiffTags.DOUBLE
                elif all((isinstance(v, str) for v in values)):
                    self.tagtype[tag] = TiffTags.ASCII
                elif all((isinstance(v, bytes) for v in values)):
                    self.tagtype[tag] = TiffTags.BYTE
        if self.tagtype[tag] == TiffTags.UNDEFINED:
            values = [value.encode('ascii', 'replace') if isinstance(value, str) else value]
        elif self.tagtype[tag] == TiffTags.RATIONAL:
            values = [float(v) if isinstance(v, int) else v for v in values]
        is_ifd = self.tagtype[tag] == TiffTags.LONG and isinstance(values, dict)
        if not is_ifd:
            values = tuple((info.cvt_enum(value) for value in values))
        dest = self._tags_v1 if legacy_api else self._tags_v2
        if not ((is_ifd or info.length == 1 or self.tagtype[tag] == TiffTags.BYTE or info.length) is None and len(values) == 1 and legacy_api):
            if legacy_api:
                if self.tagtype[tag] in [
                 TiffTags.RATIONAL,
                 TiffTags.SIGNED_RATIONAL]:
                    values = (values,)
            try:
                dest[tag], = values
            except ValueError:
                warnings.warn(f"Metadata Warning, tag {tag} had too many entries: {len(values)}, expected 1")
                dest[tag] = values[0]

        else:
            dest[tag] = values

    def __delitem__(self, tag):
        self._tags_v2.pop(tag, None)
        self._tags_v1.pop(tag, None)
        self._tagdata.pop(tag, None)

    def __iter__(self):
        return iter(set(self._tagdata) | set(self._tags_v2))

    def _unpack(self, fmt, data):
        return struct.unpack(self._endian + fmt, data)

    def _pack(self, fmt, *values):
        return (struct.pack)(self._endian + fmt, *values)

    def _register_loader(idx, size):

        def decorator(func):
            from .TiffTags import TYPES
            if func.__name__.startswith('load_'):
                TYPES[idx] = func.__name__[5:].replace('_', ' ')
            _load_dispatch[idx] = (
             size, func)
            return func

        return decorator

    def _register_writer(idx):

        def decorator(func):
            _write_dispatch[idx] = func
            return func

        return decorator

    def _register_basic--- This code section failed: ---

 L. 643         0  LOAD_CONST               1
                2  LOAD_CONST               ('TYPES',)
                4  IMPORT_NAME              TiffTags
                6  IMPORT_FROM              TYPES
                8  STORE_FAST               'TYPES'
               10  POP_TOP          

 L. 645        12  LOAD_FAST                'idx_fmt_name'
               14  UNPACK_SEQUENCE_3     3 
               16  STORE_FAST               'idx'
               18  STORE_DEREF              'fmt'
               20  STORE_FAST               'name'

 L. 646        22  LOAD_FAST                'name'
               24  LOAD_FAST                'TYPES'
               26  LOAD_FAST                'idx'
               28  STORE_SUBSCR     

 L. 647        30  LOAD_GLOBAL              struct
               32  LOAD_METHOD              calcsize
               34  LOAD_STR                 '='
               36  LOAD_DEREF               'fmt'
               38  BINARY_ADD       
               40  CALL_METHOD_1         1  '1 positional argument'
               42  STORE_DEREF              'size'

 L. 649        44  LOAD_DEREF               'size'

 L. 650        46  LOAD_CONST               (True,)
               48  LOAD_CLOSURE             'fmt'
               50  LOAD_CLOSURE             'size'
               52  BUILD_TUPLE_2         2 
               54  LOAD_LAMBDA              '<code_object <lambda>>'
               56  LOAD_STR                 'ImageFileDirectory_v2._register_basic.<locals>.<lambda>'
               58  MAKE_FUNCTION_9          'default, closure'
               60  BUILD_TUPLE_2         2 
               62  LOAD_GLOBAL              _load_dispatch
               64  LOAD_FAST                'idx'
               66  STORE_SUBSCR     

 L. 654        68  LOAD_CLOSURE             'fmt'
               70  BUILD_TUPLE_1         1 
               72  LOAD_LAMBDA              '<code_object <lambda>>'
               74  LOAD_STR                 'ImageFileDirectory_v2._register_basic.<locals>.<lambda>'
               76  MAKE_FUNCTION_8          'closure'
               78  LOAD_GLOBAL              _write_dispatch
               80  LOAD_FAST                'idx'
               82  STORE_SUBSCR     

Parse error at or near `MAKE_FUNCTION_9' instruction at offset 58

    list(map(_register_basic, [
     (
      TiffTags.SHORT, 'H', 'short'),
     (
      TiffTags.LONG, 'L', 'long'),
     (
      TiffTags.SIGNED_BYTE, 'b', 'signed byte'),
     (
      TiffTags.SIGNED_SHORT, 'h', 'signed short'),
     (
      TiffTags.SIGNED_LONG, 'l', 'signed long'),
     (
      TiffTags.FLOAT, 'f', 'float'),
     (
      TiffTags.DOUBLE, 'd', 'double'),
     (
      TiffTags.IFD, 'L', 'long')]))

    @_register_loader(1, 1)
    def load_byte(self, data, legacy_api=True):
        return data

    @_register_writer(1)
    def write_byte(self, data):
        return data

    @_register_loader(2, 1)
    def load_string(self, data, legacy_api=True):
        if data.endswith('\x00'):
            data = data[:-1]
        return data.decode('latin-1', 'replace')

    @_register_writer(2)
    def write_string(self, value):
        return '' + value.encode('ascii', 'replace') + '\x00'

    @_register_loader(5, 8)
    def load_rational(self, data, legacy_api=True):
        vals = self._unpack('{}L'.format(len(data) // 4), data)

        def combine(a, b):
            if legacy_api:
                return (a, b)
            return IFDRational(a, b)

        return tuple((combine(num, denom) for num, denom in zip(vals[::2], vals[1::2])))

    @_register_writer(5)
    def write_rational(self, *values):
        return ''.join(((self._pack)(*('2L', ), *_limit_rational(frac, 4294967295)) for frac in values))

    @_register_loader(7, 1)
    def load_undefined(self, data, legacy_api=True):
        return data

    @_register_writer(7)
    def write_undefined(self, value):
        return value

    @_register_loader(10, 8)
    def load_signed_rational(self, data, legacy_api=True):
        vals = self._unpack('{}l'.format(len(data) // 4), data)

        def combine(a, b):
            if legacy_api:
                return (a, b)
            return IFDRational(a, b)

        return tuple((combine(num, denom) for num, denom in zip(vals[::2], vals[1::2])))

    @_register_writer(10)
    def write_signed_rational(self, *values):
        return ''.join(((self._pack)(*('2l', ), *_limit_signed_rational(frac, 2147483647, -2147483648)) for frac in values))

    def _ensure_read(self, fp, size):
        ret = fp.read(size)
        if len(ret) != size:
            raise OSError(f"Corrupt EXIF data.  Expecting to read {size} bytes but only got {len(ret)}. ")
        return ret

    def load(self, fp):
        self.reset()
        self._offset = fp.tell()
        try:
            for i in range(self._unpack('H', self._ensure_read(fp, 2))[0]):
                tag, typ, count, data = self._unpack('HHL4s', self._ensure_read(fp, 12))
                tagname = TiffTags.lookup(tag).name
                typname = TYPES.get(typ, 'unknown')
                msg = f"tag: {tagname} ({tag}) - type: {typname} ({typ})"
                try:
                    unit_size, handler = self._load_dispatch[typ]
                except KeyError:
                    logger.debug(msg + f" - unsupported type {typ}")
                    continue

                size = count * unit_size
                if size > 4:
                    here = fp.tell()
                    offset, = self._unpack('L', data)
                    msg += f" Tag Location: {here} - Data Location: {offset}"
                    fp.seek(offset)
                    data = ImageFile._safe_read(fp, size)
                    fp.seek(here)
                else:
                    data = data[:size]
                if len(data) != size:
                    warnings.warn(f"Possibly corrupt EXIF data.  Expecting to read {size} bytes but only got {len(data)}. Skipping tag {tag}")
                    logger.debug(msg)
                    continue
                if not data:
                    logger.debug(msg)
                    continue
                else:
                    self._tagdata[tag] = data
                    self.tagtype[tag] = typ
                    msg += ' - value: ' + ('<table: %d bytes>' % size if size > 32 else repr(data))
                    logger.debug(msg)

            self.next, = self._unpack('L', self._ensure_read(fp, 4))
        except OSError as msg:
            try:
                warnings.warn(str(msg))
                return
            finally:
                msg = None
                del msg

    def tobytes(self, offset=0):
        result = self._pack('H', len(self._tags_v2))
        entries = []
        offset = offset + len(result) + len(self._tags_v2) * 12 + 4
        stripoffsets = None
        for tag, value in sorted(self._tags_v2.items()):
            if tag == STRIPOFFSETS:
                stripoffsets = len(entries)
            typ = self.tagtype.get(tag)
            logger.debug(f"Tag {tag}, Type: {typ}, Value: {repr(value)}")
            is_ifd = typ == TiffTags.LONG and isinstance(value, dict)
            if is_ifd:
                if self._endian == '<':
                    ifh = 'II*\x00\x08\x00\x00\x00'
                else:
                    ifh = 'MM\x00*\x00\x00\x00\x08'
                ifd = ImageFileDirectory_v2(ifh)
                for ifd_tag, ifd_value in self._tags_v2[tag].items():
                    ifd[ifd_tag] = ifd_value

                data = ifd.tobytes(offset)
            else:
                values = value if isinstance(value, tuple) else (value,)
                data = (self._write_dispatch[typ])(self, *values)
            tagname = TiffTags.lookup(tag).name
            typname = 'ifd' if is_ifd else TYPES.get(typ, 'unknown')
            msg = f"save: {tagname} ({tag}) - type: {typname} ({typ})"
            msg += ' - value: ' + ('<table: %d bytes>' % len(data) if len(data) >= 16 else str(values))
            logger.debug(msg)
            if is_ifd:
                count = 1
            elif typ in [TiffTags.BYTE, TiffTags.ASCII, TiffTags.UNDEFINED]:
                count = len(data)
            else:
                count = len(values)
            if len(data) <= 4:
                entries.append((tag, typ, count, data.ljust(4, '\x00'), ''))
            else:
                entries.append((tag, typ, count, self._pack('L', offset), data))
                offset += (len(data) + 1) // 2 * 2

        if stripoffsets is not None:
            tag, typ, count, value, data = entries[stripoffsets]
            if data:
                raise NotImplementedError('multistrip support not yet implemented')
            value = self._pack('L', self._unpack('L', value)[0] + offset)
            entries[stripoffsets] = (tag, typ, count, value, data)
        for tag, typ, count, value, data in entries:
            logger.debug(f"{tag} {typ} {count} {repr(value)} {repr(data)}")
            result += self._pack('HHL4s', tag, typ, count, value)

        result += '\x00\x00\x00\x00'
        for tag, typ, count, value, data in entries:
            result += data
            if len(data) & 1:
                result += '\x00'

        return result

    def save(self, fp):
        if fp.tell() == 0:
            fp.write(self._prefix + self._pack('HL', 42, 8))
        offset = fp.tell()
        result = self.tobytes(offset)
        fp.write(result)
        return offset + len(result)


ImageFileDirectory_v2._load_dispatch = _load_dispatch
ImageFileDirectory_v2._write_dispatch = _write_dispatch
for idx, name in TYPES.items():
    name = name.replace(' ', '_')
    setattr(ImageFileDirectory_v2, 'load_' + name, _load_dispatch[idx][1])
    setattr(ImageFileDirectory_v2, 'write_' + name, _write_dispatch[idx])

del _load_dispatch
del _write_dispatch
del idx
del name

class ImageFileDirectory_v1(ImageFileDirectory_v2):
    __doc__ = "This class represents the **legacy** interface to a TIFF tag directory.\n\n    Exposes a dictionary interface of the tags in the directory::\n\n        ifd = ImageFileDirectory_v1()\n        ifd[key] = 'Some Data'\n        ifd.tagtype[key] = TiffTags.ASCII\n        print(ifd[key])\n        ('Some Data',)\n\n    Also contains a dictionary of tag types as read from the tiff image file,\n    :attr:`~PIL.TiffImagePlugin.ImageFileDirectory_v1.tagtype`.\n\n    Values are returned as a tuple.\n\n    ..  deprecated:: 3.0.0\n    "

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._legacy_api = True

    tags = property(lambda self: self._tags_v1)
    tagdata = property(lambda self: self._tagdata)
    tagtype: dict

    @classmethod
    def from_v2(cls, original):
        """Returns an
        :py:class:`~PIL.TiffImagePlugin.ImageFileDirectory_v1`
        instance with the same data as is contained in the original
        :py:class:`~PIL.TiffImagePlugin.ImageFileDirectory_v2`
        instance.

        :returns: :py:class:`~PIL.TiffImagePlugin.ImageFileDirectory_v1`

        """
        ifd = cls(prefix=(original.prefix))
        ifd._tagdata = original._tagdata
        ifd.tagtype = original.tagtype
        ifd.next = original.next
        return ifd

    def to_v2(self):
        """Returns an
        :py:class:`~PIL.TiffImagePlugin.ImageFileDirectory_v2`
        instance with the same data as is contained in the original
        :py:class:`~PIL.TiffImagePlugin.ImageFileDirectory_v1`
        instance.

        :returns: :py:class:`~PIL.TiffImagePlugin.ImageFileDirectory_v2`

        """
        ifd = ImageFileDirectory_v2(prefix=(self.prefix))
        ifd._tagdata = dict(self._tagdata)
        ifd.tagtype = dict(self.tagtype)
        ifd._tags_v2 = dict(self._tags_v2)
        return ifd

    def __contains__(self, tag):
        return tag in self._tags_v1 or tag in self._tagdata

    def __len__(self):
        return len(set(self._tagdata) | set(self._tags_v1))

    def __iter__(self):
        return iter(set(self._tagdata) | set(self._tags_v1))

    def __setitem__(self, tag, value):
        for legacy_api in (False, True):
            self._setitem(tag, value, legacy_api)

    def __getitem__(self, tag):
        if tag not in self._tags_v1:
            data = self._tagdata[tag]
            typ = self.tagtype[tag]
            size, handler = self._load_dispatch[typ]
            for legacy in (False, True):
                self._setitem(tag, handler(self, data, legacy), legacy)

        val = self._tags_v1[tag]
        if not isinstance(val, (tuple, bytes)):
            val = (
             val,)
        return val


ImageFileDirectory = ImageFileDirectory_v1

class TiffImageFile(ImageFile.ImageFile):
    format = 'TIFF'
    format_description = 'Adobe TIFF'
    _close_exclusive_fp_after_loading = False

    def __init__(self, fp=None, filename=None):
        self.tag_v2 = None
        self.tag = None
        super().__init__(fp, filename)

    def _open(self):
        """Open the first image in a TIFF file"""
        ifh = self.fp.read(8)
        self.tag_v2 = ImageFileDirectory_v2(ifh)
        self.ifd = None
        self._TiffImageFile__first = self._TiffImageFile__next = self.tag_v2.next
        self._TiffImageFile__frame = -1
        self._TiffImageFile__fp = self.fp
        self._frame_pos = []
        self._n_frames = None
        logger.debug('*** TiffImageFile._open ***')
        logger.debug(f"- __first: {self._TiffImageFile__first}")
        logger.debug(f"- ifh: {repr(ifh)}")
        self._seek(0)

    @property
    def n_frames(self):
        if self._n_frames is None:
            current = self.tell()
            self._seek(len(self._frame_pos))
            while self._n_frames is None:
                self._seek(self.tell() + 1)

            self.seek(current)
        return self._n_frames

    def seek(self, frame):
        """Select a given frame as current image"""
        if not self._seek_check(frame):
            return
        self._seek(frame)
        Image._decompression_bomb_check(self.size)
        self.im = Image.core.new(self.mode, self.size)

    def _seek(self, frame):
        self.fp = self._TiffImageFile__fp
        while len(self._frame_pos) <= frame:
            if not self._TiffImageFile__next:
                raise EOFError('no more images in TIFF file')
            else:
                logger.debug(f"Seeking to frame {frame}, on frame {self._TiffImageFile__frame}, __next {self._TiffImageFile__next}, location: {self.fp.tell()}")
                self.fp.tell()
                self.fp.seek(self._TiffImageFile__next)
                self._frame_pos.append(self._TiffImageFile__next)
                logger.debug('Loading tags, location: %s' % self.fp.tell())
                self.tag_v2.load(self.fp)
                self._TiffImageFile__next = self.tag_v2.next
                if self._TiffImageFile__next == 0:
                    self._n_frames = frame + 1
                if len(self._frame_pos) == 1:
                    self.is_animated = self._TiffImageFile__next != 0
                self._TiffImageFile__frame += 1

        self.fp.seek(self._frame_pos[frame])
        self.tag_v2.load(self.fp)
        self.tag = self.ifd = ImageFileDirectory_v1.from_v2(self.tag_v2)
        self._TiffImageFile__frame = frame
        self._setup()

    def tell(self):
        """Return the current frame number"""
        return self._TiffImageFile__frame

    def load(self):
        if self.tile:
            if self.use_load_libtiff:
                return self._load_libtiff()
        return super().load()

    def load_end(self):
        if self._tile_orientation:
            method = {2:Image.FLIP_LEFT_RIGHT,  3:Image.ROTATE_180, 
             4:Image.FLIP_TOP_BOTTOM, 
             5:Image.TRANSPOSE, 
             6:Image.ROTATE_270, 
             7:Image.TRANSVERSE, 
             8:Image.ROTATE_90}.get(self._tile_orientation)
            if method is not None:
                self.im = self.im.transpose(method)
                self._size = self.im.size
        if not self.is_animated:
            self._close_exclusive_fp_after_loading = True

    def _load_libtiff(self):
        """Overload method triggered when we detect a compressed tiff
        Calls out to libtiff"""
        Image.Image.load(self)
        self.load_prepare()
        if not len(self.tile) == 1:
            raise OSError('Not exactly one tile')
        extents = self.tile[0][1]
        args = list(self.tile[0][3])
        try:
            fp = hasattr(self.fp, 'fileno') and os.dup(self.fp.fileno())
            if hasattr(self.fp, 'flush'):
                self.fp.flush()
        except OSError:
            fp = False

        if fp:
            args[2] = fp
        decoder = Image._getdecoder(self.mode, 'libtiff', tuple(args), self.decoderconfig)
        try:
            decoder.setimage(self.im, extents)
        except ValueError as e:
            try:
                raise OSError("Couldn't set the image") from e
            finally:
                e = None
                del e

        close_self_fp = self._exclusive_fp and not self.is_animated
        if hasattr(self.fp, 'getvalue'):
            logger.debug('have getvalue. just sending in a string from getvalue')
            n, err = decoder.decode(self.fp.getvalue())
        elif fp:
            logger.debug('have fileno, calling fileno version of the decoder.')
            if not close_self_fp:
                self.fp.seek(0)
            n, err = decoder.decode('fpfp')
        else:
            logger.debug("don't have fileno or getvalue. just reading")
            self.fp.seek(0)
            n, err = decoder.decode(self.fp.read())
        self.tile = []
        self.readonly = 0
        self.load_end()
        if close_self_fp:
            self.fp.close()
            self.fp = None
        if err < 0:
            raise OSError(err)
        return Image.Image.load(self)

    def _setup(self):
        """Setup this image object based on current tags"""
        if 48129 in self.tag_v2:
            raise OSError('Windows Media Photo files not yet supported')
        self._compression = COMPRESSION_INFO[self.tag_v2.get(COMPRESSION, 1)]
        self._planar_configuration = self.tag_v2.get(PLANAR_CONFIGURATION, 1)
        photo = self.tag_v2.get(PHOTOMETRIC_INTERPRETATION, 0)
        if self._compression == 'tiff_jpeg':
            photo = 6
        fillorder = self.tag_v2.get(FILLORDER, 1)
        logger.debug('*** Summary ***')
        logger.debug(f"- compression: {self._compression}")
        logger.debug(f"- photometric_interpretation: {photo}")
        logger.debug(f"- planar_configuration: {self._planar_configuration}")
        logger.debug(f"- fill_order: {fillorder}")
        logger.debug(f"- YCbCr subsampling: {self.tag.get(530)}")
        xsize = int(self.tag_v2.get(IMAGEWIDTH))
        ysize = int(self.tag_v2.get(IMAGELENGTH))
        self._size = (xsize, ysize)
        logger.debug(f"- size: {self.size}")
        sampleFormat = self.tag_v2.get(SAMPLEFORMAT, (1, ))
        if len(sampleFormat) > 1:
            if max(sampleFormat) == min(sampleFormat) == 1:
                sampleFormat = (1, )
        bps_tuple = self.tag_v2.get(BITSPERSAMPLE, (1, ))
        extra_tuple = self.tag_v2.get(EXTRASAMPLES, ())
        if photo in (2, 6, 8):
            bps_count = 3
        elif photo == 5:
            bps_count = 4
        else:
            bps_count = 1
        bps_count += len(extra_tuple)
        if bps_count > len(bps_tuple):
            if len(bps_tuple) == 1:
                bps_tuple = bps_tuple * bps_count
        key = (
         self.tag_v2.prefix,
         photo,
         sampleFormat,
         fillorder,
         bps_tuple,
         extra_tuple)
        logger.debug(f"format key: {key}")
        try:
            self.mode, rawmode = OPEN_INFO[key]
        except KeyError as e:
            try:
                logger.debug('- unsupported format')
                raise SyntaxError('unknown pixel mode') from e
            finally:
                e = None
                del e

        logger.debug(f"- raw mode: {rawmode}")
        logger.debug(f"- pil mode: {self.mode}")
        self.info['compression'] = self._compression
        xres = self.tag_v2.get(X_RESOLUTION, 1)
        yres = self.tag_v2.get(Y_RESOLUTION, 1)
        if xres:
            if yres:
                resunit = self.tag_v2.get(RESOLUTION_UNIT)
                if resunit == 2:
                    self.info['dpi'] = (
                     int(xres + 0.5), int(yres + 0.5))
                elif resunit == 3:
                    self.info['dpi'] = (
                     int(xres * 2.54 + 0.5), int(yres * 2.54 + 0.5))
                elif resunit is None:
                    self.info['dpi'] = (
                     int(xres + 0.5), int(yres + 0.5))
                    self.info['resolution'] = (
                     xres, yres)
                else:
                    self.info['resolution'] = (
                     xres, yres)
        x = y = layer = 0
        self.tile = []
        self.use_load_libtiff = READ_LIBTIFF or self._compression != 'raw'
        if self.use_load_libtiff:
            if fillorder == 2:
                key = key[:3] + (1, ) + key[4:]
                logger.debug(f"format key: {key}")
                self.mode, rawmode = OPEN_INFO[key]
            if rawmode == 'I;16':
                rawmode = 'I;16N'
            if ';16B' in rawmode:
                rawmode = rawmode.replace(';16B', ';16N')
            if ';16L' in rawmode:
                rawmode = rawmode.replace(';16L', ';16N')
            a = (
             rawmode, self._compression, False, self.tag_v2.offset)
            self.tile.append(('libtiff', (0, 0, xsize, ysize), 0, a))
        elif STRIPOFFSETS in self.tag_v2 or TILEOFFSETS in self.tag_v2:
            if STRIPOFFSETS in self.tag_v2:
                offsets = self.tag_v2[STRIPOFFSETS]
                h = self.tag_v2.get(ROWSPERSTRIP, ysize)
                w = self.size[0]
            else:
                offsets = self.tag_v2[TILEOFFSETS]
                w = self.tag_v2.get(322)
                h = self.tag_v2.get(323)
            for offset in offsets:
                if x + w > xsize:
                    stride = w * sum(bps_tuple) / 8
                else:
                    stride = 0
                tile_rawmode = rawmode
                if self._planar_configuration == 2:
                    tile_rawmode = rawmode[layer]
                    stride /= bps_count
                a = (tile_rawmode, int(stride), 1)
                self.tile.append((
                 self._compression,
                 (
                  x, y, min(x + w, xsize), min(y + h, ysize)),
                 offset,
                 a))
                x = x + w
                if x >= self.size[0]:
                    x, y = 0, y + h
                    if y >= self.size[1]:
                        x = y = 0
                        layer += 1

        else:
            logger.debug('- unsupported data organization')
            raise SyntaxError('unknown data organization')
        if ICCPROFILE in self.tag_v2:
            self.info['icc_profile'] = self.tag_v2[ICCPROFILE]
        if self.mode in ('P', 'PA'):
            palette = [o8(b // 256) for b in self.tag_v2[COLORMAP]]
            self.palette = ImagePalette.raw('RGB;L', ''.join(palette))
        self._tile_orientation = self.tag_v2.get(274)

    def _close__fp(self):
        try:
            try:
                if self._TiffImageFile__fp != self.fp:
                    self._TiffImageFile__fp.close()
            except AttributeError:
                pass

        finally:
            self._TiffImageFile__fp = None


SAVE_INFO = {'1':(
  '1', II, 1, 1, (1, ), None), 
 'L':(
  'L', II, 1, 1, (8, ), None), 
 'LA':(
  'LA', II, 1, 1, (8, 8), 2), 
 'P':(
  'P', II, 3, 1, (8, ), None), 
 'PA':(
  'PA', II, 3, 1, (8, 8), 2), 
 'I':(
  'I;32S', II, 1, 2, (32, ), None), 
 'I;16':(
  'I;16', II, 1, 1, (16, ), None), 
 'I;16S':(
  'I;16S', II, 1, 2, (16, ), None), 
 'F':(
  'F;32F', II, 1, 3, (32, ), None), 
 'RGB':(
  'RGB', II, 2, 1, (8, 8, 8), None), 
 'RGBX':(
  'RGBX', II, 2, 1, (8, 8, 8, 8), 0), 
 'RGBA':(
  'RGBA', II, 2, 1, (8, 8, 8, 8), 2), 
 'CMYK':(
  'CMYK', II, 5, 1, (8, 8, 8, 8), None), 
 'YCbCr':(
  'YCbCr', II, 6, 1, (8, 8, 8), None), 
 'LAB':(
  'LAB', II, 8, 1, (8, 8, 8), None), 
 'I;32BS':(
  'I;32BS', MM, 1, 2, (32, ), None), 
 'I;16B':(
  'I;16B', MM, 1, 1, (16, ), None), 
 'I;16BS':(
  'I;16BS', MM, 1, 2, (16, ), None), 
 'F;32BF':(
  'F;32BF', MM, 1, 3, (32, ), None)}

def _save(im, fp, filename):
    try:
        rawmode, prefix, photo, format, bits, extra = SAVE_INFO[im.mode]
    except KeyError as e:
        try:
            raise OSError(f"cannot write mode {im.mode} as TIFF") from e
        finally:
            e = None
            del e

    ifd = ImageFileDirectory_v2(prefix=prefix)
    compression = im.encoderinfo.get('compression', im.info.get('compression'))
    if compression is None:
        compression = 'raw'
    elif compression == 'tiff_jpeg':
        compression = 'jpeg'
    libtiff = WRITE_LIBTIFF or compression != 'raw'
    ifd[PLANAR_CONFIGURATION] = getattr(im, '_planar_configuration', 1)
    ifd[IMAGEWIDTH] = im.size[0]
    ifd[IMAGELENGTH] = im.size[1]
    info = im.encoderinfo.get('tiffinfo', {})
    logger.debug('Tiffinfo Keys: %s' % list(info))
    if isinstance(info, ImageFileDirectory_v1):
        info = info.to_v2()
    for key in info:
        ifd[key] = info.get(key)
        try:
            ifd.tagtype[key] = info.tagtype[key]
        except Exception:
            pass

    if hasattr(im, 'tag_v2'):
        for key in (
         RESOLUTION_UNIT,
         X_RESOLUTION,
         Y_RESOLUTION,
         IPTC_NAA_CHUNK,
         PHOTOSHOP_CHUNK,
         XMP):
            if key in im.tag_v2:
                ifd[key] = im.tag_v2[key]
                ifd.tagtype[key] = im.tag_v2.tagtype[key]

    if 'icc_profile' in im.info:
        ifd[ICCPROFILE] = im.info['icc_profile']
    for key, name in [
     (
      IMAGEDESCRIPTION, 'description'),
     (
      X_RESOLUTION, 'resolution'),
     (
      Y_RESOLUTION, 'resolution'),
     (
      X_RESOLUTION, 'x_resolution'),
     (
      Y_RESOLUTION, 'y_resolution'),
     (
      RESOLUTION_UNIT, 'resolution_unit'),
     (
      SOFTWARE, 'software'),
     (
      DATE_TIME, 'date_time'),
     (
      ARTIST, 'artist'),
     (
      COPYRIGHT, 'copyright')]:
        if name in im.encoderinfo:
            ifd[key] = im.encoderinfo[name]

    dpi = im.encoderinfo.get('dpi')
    if dpi:
        ifd[RESOLUTION_UNIT] = 2
        ifd[X_RESOLUTION] = int(dpi[0] + 0.5)
        ifd[Y_RESOLUTION] = int(dpi[1] + 0.5)
    if bits != (1, ):
        ifd[BITSPERSAMPLE] = bits
        if len(bits) != 1:
            ifd[SAMPLESPERPIXEL] = len(bits)
    if extra is not None:
        ifd[EXTRASAMPLES] = extra
    if format != 1:
        ifd[SAMPLEFORMAT] = format
    ifd[PHOTOMETRIC_INTERPRETATION] = photo
    if im.mode in ('P', 'PA'):
        lut = im.im.getpalette('RGB', 'RGB;L')
        ifd[COLORMAP] = tuple((v * 256 for v in lut))
    stride = len(bits) * ((im.size[0] * bits[0] + 7) // 8)
    ifd[ROWSPERSTRIP] = im.size[1]
    strip_byte_counts = stride * im.size[1]
    if strip_byte_counts >= 65536:
        ifd.tagtype[STRIPBYTECOUNTS] = TiffTags.LONG
    ifd[STRIPBYTECOUNTS] = strip_byte_counts
    ifd[STRIPOFFSETS] = 0
    ifd[COMPRESSION] = COMPRESSION_INFO_REV.get(compression, 1)
    if libtiff:
        if 'quality' in im.encoderinfo:
            quality = im.encoderinfo['quality']
            if isinstance(quality, int):
                if quality < 0 or (quality > 100):
                    raise ValueError('Invalid quality setting')
                if compression != 'jpeg':
                    raise ValueError("quality setting only supported for 'jpeg' compression")
            ifd[JPEGQUALITY] = quality
        logger.debug('Saving using libtiff encoder')
        logger.debug('Items: %s' % sorted(ifd.items()))
        _fp = 0
        if hasattr(fp, 'fileno'):
            try:
                fp.seek(0)
                _fp = os.dup(fp.fileno())
            except io.UnsupportedOperation:
                pass

            types = {}
            blocklist = [
             REFERENCEBLACKWHITE,
             SAMPLEFORMAT,
             STRIPBYTECOUNTS,
             STRIPOFFSETS,
             TRANSFERFUNCTION,
             SUBIFD]
            atts = {}
            atts[BITSPERSAMPLE] = bits[0]
            legacy_ifd = {}
            if hasattr(im, 'tag'):
                legacy_ifd = im.tag.to_v2()
            for tag, value in itertools.chain(ifd.items(), getattr(im, 'tag_v2', {}).items(), legacy_ifd.items()):
                if tag not in TiffTags.LIBTIFF_CORE:
                    if not Image.core.libtiff_support_custom_tags:
                        continue
                    if tag in ifd.tagtype:
                        types[tag] = ifd.tagtype[tag]
                    else:
                        if not isinstance(value, (int, float, str, bytes)):
                            continue
                        else:
                            type = TiffTags.lookup(tag).type
                            if type:
                                types[tag] = type
                if tag not in atts:
                    if tag not in blocklist:
                        if isinstance(value, str):
                            atts[tag] = value.encode('ascii', 'replace') + '\x00'
                        else:
                            if isinstance(value, IFDRational):
                                atts[tag] = float(value)
                            else:
                                atts[tag] = value

            logger.debug('Converted items: %s' % sorted(atts.items()))
            if im.mode in ('I;16B', 'I;16'):
                rawmode = 'I;16N'
            tags = list(atts.items())
            tags.sort()
            a = (rawmode, compression, _fp, filename, tags, types)
            e = Image._getencoder(im.mode, 'libtiff', a, im.encoderconfig)
            e.setimage(im.im, (0, 0) + im.size)
            while True:
                l, s, d = e.encode(16384)
                if not _fp:
                    fp.write(d)
                if s:
                    break

        if s < 0:
            raise OSError(f"encoder error {s} when writing image file")
    else:
        offset = ifd.save(fp)
        ImageFile._save(im, fp, [('raw', (0, 0) + im.size, offset, (rawmode, stride, 1))])
    if '_debug_multipage' in im.encoderinfo:
        im._debug_multipage = ifd


class AppendingTiffWriter:
    fieldSizes = [
     0,
     1,
     1,
     2,
     4,
     8,
     1,
     1,
     2,
     4,
     8,
     4,
     8]
    Tags = {
     273, 288, 324, 519, 520, 521}

    def __init__(self, fn, new=False):
        if hasattr(fn, 'read'):
            self.f = fn
            self.close_fp = False
        else:
            self.name = fn
            self.close_fp = True
            try:
                self.f = open(fn, 'w+b' if new else 'r+b')
            except OSError:
                self.f = open(fn, 'w+b')

        self.beginning = self.f.tell()
        self.setup()

    def setup(self):
        self.f.seek(self.beginning, os.SEEK_SET)
        self.whereToWriteNewIFDOffset = None
        self.offsetOfNewPage = 0
        self.IIMM = IIMM = self.f.read(4)
        if not IIMM:
            self.isFirst = True
            return
        self.isFirst = False
        if IIMM == 'II*\x00':
            self.setEndian('<')
        elif IIMM == 'MM\x00*':
            self.setEndian('>')
        else:
            raise RuntimeError('Invalid TIFF file header')
        self.skipIFDs()
        self.goToEnd()

    def finalize(self):
        if self.isFirst:
            return
        self.f.seek(self.offsetOfNewPage)
        IIMM = self.f.read(4)
        if not IIMM:
            return
        if IIMM != self.IIMM:
            raise RuntimeError("IIMM of new page doesn't match IIMM of first page")
        IFDoffset = self.readLong()
        IFDoffset += self.offsetOfNewPage
        self.f.seek(self.whereToWriteNewIFDOffset)
        self.writeLong(IFDoffset)
        self.f.seek(IFDoffset)
        self.fixIFD()

    def newFrame(self):
        self.finalize()
        self.setup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.close_fp:
            self.close()
        return False

    def tell(self):
        return self.f.tell() - self.offsetOfNewPage

    def seek(self, offset, whence=io.SEEK_SET):
        if whence == os.SEEK_SET:
            offset += self.offsetOfNewPage
        self.f.seek(offset, whence)
        return self.tell()

    def goToEnd(self):
        self.f.seek(0, os.SEEK_END)
        pos = self.f.tell()
        padBytes = 16 - pos % 16
        if 0 < padBytes < 16:
            self.f.write(bytes(padBytes))
        self.offsetOfNewPage = self.f.tell()

    def setEndian(self, endian):
        self.endian = endian
        self.longFmt = self.endian + 'L'
        self.shortFmt = self.endian + 'H'
        self.tagFormat = self.endian + 'HHL'

    def skipIFDs(self):
        while True:
            IFDoffset = self.readLong()
            if IFDoffset == 0:
                self.whereToWriteNewIFDOffset = self.f.tell() - 4
                break
            else:
                self.f.seek(IFDoffset)
                numTags = self.readShort()
                self.f.seek(numTags * 12, os.SEEK_CUR)

    def write(self, data):
        return self.f.write(data)

    def readShort(self):
        value, = struct.unpack(self.shortFmt, self.f.read(2))
        return value

    def readLong(self):
        value, = struct.unpack(self.longFmt, self.f.read(4))
        return value

    def rewriteLastShortToLong(self, value):
        self.f.seek(-2, os.SEEK_CUR)
        bytesWritten = self.f.write(struct.pack(self.longFmt, value))
        if bytesWritten is not None:
            if bytesWritten != 4:
                raise RuntimeError(f"wrote only {bytesWritten} bytes but wanted 4")

    def rewriteLastShort(self, value):
        self.f.seek(-2, os.SEEK_CUR)
        bytesWritten = self.f.write(struct.pack(self.shortFmt, value))
        if bytesWritten is not None:
            if bytesWritten != 2:
                raise RuntimeError(f"wrote only {bytesWritten} bytes but wanted 2")

    def rewriteLastLong(self, value):
        self.f.seek(-4, os.SEEK_CUR)
        bytesWritten = self.f.write(struct.pack(self.longFmt, value))
        if bytesWritten is not None:
            if bytesWritten != 4:
                raise RuntimeError(f"wrote only {bytesWritten} bytes but wanted 4")

    def writeShort(self, value):
        bytesWritten = self.f.write(struct.pack(self.shortFmt, value))
        if bytesWritten is not None:
            if bytesWritten != 2:
                raise RuntimeError(f"wrote only {bytesWritten} bytes but wanted 2")

    def writeLong(self, value):
        bytesWritten = self.f.write(struct.pack(self.longFmt, value))
        if bytesWritten is not None:
            if bytesWritten != 4:
                raise RuntimeError(f"wrote only {bytesWritten} bytes but wanted 4")

    def close(self):
        self.finalize()
        self.f.close()

    def fixIFD(self):
        numTags = self.readShort()
        for i in range(numTags):
            tag, fieldType, count = struct.unpack(self.tagFormat, self.f.read(8))
            fieldSize = self.fieldSizes[fieldType]
            totalSize = fieldSize * count
            isLocal = totalSize <= 4
            if not isLocal:
                offset = self.readLong()
                offset += self.offsetOfNewPage
                self.rewriteLastLong(offset)
            if tag in self.Tags:
                curPos = self.f.tell()
                if isLocal:
                    self.fixOffsets(count,
                      isShort=(fieldSize == 2), isLong=(fieldSize == 4))
                    self.f.seek(curPos + 4)
                else:
                    self.f.seek(offset)
                    self.fixOffsets(count,
                      isShort=(fieldSize == 2), isLong=(fieldSize == 4))
                    self.f.seek(curPos)
                offset = curPos = None
            if isLocal:
                self.f.seek(4, os.SEEK_CUR)

    def fixOffsets(self, count, isShort=False, isLong=False):
        if not isShort:
            if not isLong:
                raise RuntimeError('offset is neither short nor long')
        for i in range(count):
            offset = self.readShort() if isShort else self.readLong()
            offset += self.offsetOfNewPage
            if isShort and offset >= 65536:
                if count != 1:
                    raise RuntimeError('not implemented')
                else:
                    self.rewriteLastShortToLong(offset)
                    self.f.seek(-10, os.SEEK_CUR)
                    self.writeShort(TiffTags.LONG)
                    self.f.seek(8, os.SEEK_CUR)
            else:
                if isShort:
                    self.rewriteLastShort(offset)
                else:
                    self.rewriteLastLong(offset)


def _save_all(im, fp, filename):
    encoderinfo = im.encoderinfo.copy()
    encoderconfig = im.encoderconfig
    append_images = list(encoderinfo.get('append_images', []))
    if not hasattr(im, 'n_frames'):
        if not append_images:
            return _save(im, fp, filename)
    cur_idx = im.tell()
    try:
        with AppendingTiffWriter(fp) as tf:
            for ims in [im] + append_images:
                ims.encoderinfo = encoderinfo
                ims.encoderconfig = encoderconfig
                if not hasattr(ims, 'n_frames'):
                    nfr = 1
                else:
                    nfr = ims.n_frames
                for idx in range(nfr):
                    ims.seek(idx)
                    ims.load()
                    _save(ims, tf, filename)
                    tf.newFrame()

    finally:
        im.seek(cur_idx)


Image.register_open(TiffImageFile.format, TiffImageFile, _accept)
Image.register_save(TiffImageFile.format, _save)
Image.register_save_all(TiffImageFile.format, _save_all)
Image.register_extensions(TiffImageFile.format, ['.tif', '.tiff'])
Image.register_mime(TiffImageFile.format, 'image/tiff')