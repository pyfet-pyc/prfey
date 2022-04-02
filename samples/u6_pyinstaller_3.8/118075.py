# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\dns\rdtypes\ANY\LOC.py
from __future__ import division
import struct, dns.exception, dns.rdata
from dns._compat import long, xrange, round_py2_compat
_pows = tuple((long(10 ** i) for i in range(0, 11)))
_default_size = 100.0
_default_hprec = 1000000.0
_default_vprec = 1000.0

def _exponent_of(what, desc):
    if what == 0:
        return 0
    exp = None
    for i in xrange(len(_pows)):
        if what // _pows[i] == long(0):
            exp = i - 1
            break
        if exp is None or exp < 0:
            raise dns.exception.SyntaxError('%s value out of bounds' % desc)
        return exp


def _float_to_tuple(what):
    if what < 0:
        sign = -1
        what *= -1
    else:
        sign = 1
    what = round_py2_compat(what * 3600000)
    degrees = int(what // 3600000)
    what -= degrees * 3600000
    minutes = int(what // 60000)
    what -= minutes * 60000
    seconds = int(what // 1000)
    what -= int(seconds * 1000)
    what = int(what)
    return (degrees, minutes, seconds, what, sign)


def _tuple_to_float(what):
    value = float(what[0])
    value += float(what[1]) / 60.0
    value += float(what[2]) / 3600.0
    value += float(what[3]) / 3600000.0
    return float(what[4]) * value


def _encode_size(what, desc):
    what = long(what)
    exponent = _exponent_of(what, desc) & 15
    base = what // pow(10, exponent) & 15
    return base * 16 + exponent


def _decode_size(what, desc):
    exponent = what & 15
    if exponent > 9:
        raise dns.exception.SyntaxError('bad %s exponent' % desc)
    base = (what & 240) >> 4
    if base > 9:
        raise dns.exception.SyntaxError('bad %s base' % desc)
    return long(base) * pow(10, exponent)


class LOC(dns.rdata.Rdata):
    __doc__ = 'LOC record\n\n    @ivar latitude: latitude\n    @type latitude: (int, int, int, int, sign) tuple specifying the degrees, minutes,\n    seconds, milliseconds, and sign of the coordinate.\n    @ivar longitude: longitude\n    @type longitude: (int, int, int, int, sign) tuple specifying the degrees,\n    minutes, seconds, milliseconds, and sign of the coordinate.\n    @ivar altitude: altitude\n    @type altitude: float\n    @ivar size: size of the sphere\n    @type size: float\n    @ivar horizontal_precision: horizontal precision\n    @type horizontal_precision: float\n    @ivar vertical_precision: vertical precision\n    @type vertical_precision: float\n    @see: RFC 1876'
    __slots__ = [
     'latitude', 'longitude', 'altitude', 'size',
     'horizontal_precision', 'vertical_precision']

    def __init__(self, rdclass, rdtype, latitude, longitude, altitude, size=_default_size, hprec=_default_hprec, vprec=_default_vprec):
        """Initialize a LOC record instance.

        The parameters I{latitude} and I{longitude} may be either a 4-tuple
        of integers specifying (degrees, minutes, seconds, milliseconds),
        or they may be floating point values specifying the number of
        degrees. The other parameters are floats. Size, horizontal precision,
        and vertical precision are specified in centimeters."""
        super(LOC, self).__init__(rdclass, rdtype)
        if isinstance(latitude, int) or isinstance(latitude, long):
            latitude = float(latitude)
        if isinstance(latitude, float):
            latitude = _float_to_tuple(latitude)
        self.latitude = latitude
        if isinstance(longitude, int) or isinstance(longitude, long):
            longitude = float(longitude)
        if isinstance(longitude, float):
            longitude = _float_to_tuple(longitude)
        self.longitude = longitude
        self.altitude = float(altitude)
        self.size = float(size)
        self.horizontal_precision = float(hprec)
        self.vertical_precision = float(vprec)

    def to_text(self, origin=None, relativize=True, **kw):
        if self.latitude[4] > 0:
            lat_hemisphere = 'N'
        else:
            lat_hemisphere = 'S'
        if self.longitude[4] > 0:
            long_hemisphere = 'E'
        else:
            long_hemisphere = 'W'
        text = '%d %d %d.%03d %s %d %d %d.%03d %s %0.2fm' % (
         self.latitude[0], self.latitude[1],
         self.latitude[2], self.latitude[3], lat_hemisphere,
         self.longitude[0], self.longitude[1], self.longitude[2],
         self.longitude[3], long_hemisphere,
         self.altitude / 100.0)
        if self.size != _default_size or self.horizontal_precision != _default_hprec or self.vertical_precision != _default_vprec:
            text += ' {:0.2f}m {:0.2f}m {:0.2f}m'.format(self.size / 100.0, self.horizontal_precision / 100.0, self.vertical_precision / 100.0)
        return text

    @classmethod
    def from_text--- This code section failed: ---

 L. 169         0  LOAD_CONST               0
                2  LOAD_CONST               0
                4  LOAD_CONST               0
                6  LOAD_CONST               0
                8  LOAD_CONST               1
               10  BUILD_LIST_5          5 
               12  STORE_FAST               'latitude'

 L. 170        14  LOAD_CONST               0
               16  LOAD_CONST               0
               18  LOAD_CONST               0
               20  LOAD_CONST               0
               22  LOAD_CONST               1
               24  BUILD_LIST_5          5 
               26  STORE_FAST               'longitude'

 L. 171        28  LOAD_GLOBAL              _default_size
               30  STORE_FAST               'size'

 L. 172        32  LOAD_GLOBAL              _default_hprec
               34  STORE_FAST               'hprec'

 L. 173        36  LOAD_GLOBAL              _default_vprec
               38  STORE_FAST               'vprec'

 L. 175        40  LOAD_FAST                'tok'
               42  LOAD_METHOD              get_int
               44  CALL_METHOD_0         0  ''
               46  LOAD_FAST                'latitude'
               48  LOAD_CONST               0
               50  STORE_SUBSCR     

 L. 176        52  LOAD_FAST                'tok'
               54  LOAD_METHOD              get_string
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               't'

 L. 177        60  LOAD_FAST                't'
               62  LOAD_METHOD              isdigit
               64  CALL_METHOD_0         0  ''
            66_68  POP_JUMP_IF_FALSE   302  'to 302'

 L. 178        70  LOAD_GLOBAL              int
               72  LOAD_FAST                't'
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_FAST                'latitude'
               78  LOAD_CONST               1
               80  STORE_SUBSCR     

 L. 179        82  LOAD_FAST                'tok'
               84  LOAD_METHOD              get_string
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               't'

 L. 180        90  LOAD_STR                 '.'
               92  LOAD_FAST                't'
               94  COMPARE_OP               in
            96_98  POP_JUMP_IF_FALSE   272  'to 272'

 L. 181       100  LOAD_FAST                't'
              102  LOAD_METHOD              split
              104  LOAD_STR                 '.'
              106  CALL_METHOD_1         1  ''
              108  UNPACK_SEQUENCE_2     2 
              110  STORE_FAST               'seconds'
              112  STORE_FAST               'milliseconds'

 L. 182       114  LOAD_FAST                'seconds'
              116  LOAD_METHOD              isdigit
              118  CALL_METHOD_0         0  ''
              120  POP_JUMP_IF_TRUE    134  'to 134'

 L. 183       122  LOAD_GLOBAL              dns
              124  LOAD_ATTR                exception
              126  LOAD_METHOD              SyntaxError

 L. 184       128  LOAD_STR                 'bad latitude seconds value'

 L. 183       130  CALL_METHOD_1         1  ''
              132  RAISE_VARARGS_1       1  'exception instance'
            134_0  COME_FROM           120  '120'

 L. 185       134  LOAD_GLOBAL              int
              136  LOAD_FAST                'seconds'
              138  CALL_FUNCTION_1       1  ''
              140  LOAD_FAST                'latitude'
              142  LOAD_CONST               2
              144  STORE_SUBSCR     

 L. 186       146  LOAD_FAST                'latitude'
              148  LOAD_CONST               2
              150  BINARY_SUBSCR    
              152  LOAD_CONST               60
              154  COMPARE_OP               >=
              156  POP_JUMP_IF_FALSE   170  'to 170'

 L. 187       158  LOAD_GLOBAL              dns
              160  LOAD_ATTR                exception
              162  LOAD_METHOD              SyntaxError
              164  LOAD_STR                 'latitude seconds >= 60'
              166  CALL_METHOD_1         1  ''
              168  RAISE_VARARGS_1       1  'exception instance'
            170_0  COME_FROM           156  '156'

 L. 188       170  LOAD_GLOBAL              len
              172  LOAD_FAST                'milliseconds'
              174  CALL_FUNCTION_1       1  ''
              176  STORE_FAST               'l'

 L. 189       178  LOAD_FAST                'l'
              180  LOAD_CONST               0
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_TRUE    202  'to 202'
              186  LOAD_FAST                'l'
              188  LOAD_CONST               3
              190  COMPARE_OP               >
              192  POP_JUMP_IF_TRUE    202  'to 202'
              194  LOAD_FAST                'milliseconds'
              196  LOAD_METHOD              isdigit
              198  CALL_METHOD_0         0  ''
              200  POP_JUMP_IF_TRUE    214  'to 214'
            202_0  COME_FROM           192  '192'
            202_1  COME_FROM           184  '184'

 L. 190       202  LOAD_GLOBAL              dns
              204  LOAD_ATTR                exception
              206  LOAD_METHOD              SyntaxError

 L. 191       208  LOAD_STR                 'bad latitude milliseconds value'

 L. 190       210  CALL_METHOD_1         1  ''
              212  RAISE_VARARGS_1       1  'exception instance'
            214_0  COME_FROM           200  '200'

 L. 192       214  LOAD_FAST                'l'
              216  LOAD_CONST               1
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_FALSE   228  'to 228'

 L. 193       222  LOAD_CONST               100
              224  STORE_FAST               'm'
              226  JUMP_FORWARD        246  'to 246'
            228_0  COME_FROM           220  '220'

 L. 194       228  LOAD_FAST                'l'
              230  LOAD_CONST               2
              232  COMPARE_OP               ==
              234  POP_JUMP_IF_FALSE   242  'to 242'

 L. 195       236  LOAD_CONST               10
              238  STORE_FAST               'm'
              240  JUMP_FORWARD        246  'to 246'
            242_0  COME_FROM           234  '234'

 L. 197       242  LOAD_CONST               1
              244  STORE_FAST               'm'
            246_0  COME_FROM           240  '240'
            246_1  COME_FROM           226  '226'

 L. 198       246  LOAD_FAST                'm'
              248  LOAD_GLOBAL              int
              250  LOAD_FAST                'milliseconds'
              252  CALL_FUNCTION_1       1  ''
              254  BINARY_MULTIPLY  
              256  LOAD_FAST                'latitude'
              258  LOAD_CONST               3
              260  STORE_SUBSCR     

 L. 199       262  LOAD_FAST                'tok'
              264  LOAD_METHOD              get_string
              266  CALL_METHOD_0         0  ''
              268  STORE_FAST               't'
              270  JUMP_FORWARD        302  'to 302'
            272_0  COME_FROM            96  '96'

 L. 200       272  LOAD_FAST                't'
              274  LOAD_METHOD              isdigit
              276  CALL_METHOD_0         0  ''
          278_280  POP_JUMP_IF_FALSE   302  'to 302'

 L. 201       282  LOAD_GLOBAL              int
              284  LOAD_FAST                't'
              286  CALL_FUNCTION_1       1  ''
              288  LOAD_FAST                'latitude'
              290  LOAD_CONST               2
              292  STORE_SUBSCR     

 L. 202       294  LOAD_FAST                'tok'
              296  LOAD_METHOD              get_string
              298  CALL_METHOD_0         0  ''
              300  STORE_FAST               't'
            302_0  COME_FROM           278  '278'
            302_1  COME_FROM           270  '270'
            302_2  COME_FROM            66  '66'

 L. 203       302  LOAD_FAST                't'
              304  LOAD_STR                 'S'
              306  COMPARE_OP               ==
          308_310  POP_JUMP_IF_FALSE   322  'to 322'

 L. 204       312  LOAD_CONST               -1
              314  LOAD_FAST                'latitude'
              316  LOAD_CONST               4
              318  STORE_SUBSCR     
              320  JUMP_FORWARD        344  'to 344'
            322_0  COME_FROM           308  '308'

 L. 205       322  LOAD_FAST                't'
              324  LOAD_STR                 'N'
              326  COMPARE_OP               !=
          328_330  POP_JUMP_IF_FALSE   344  'to 344'

 L. 206       332  LOAD_GLOBAL              dns
              334  LOAD_ATTR                exception
              336  LOAD_METHOD              SyntaxError
              338  LOAD_STR                 'bad latitude hemisphere value'
              340  CALL_METHOD_1         1  ''
              342  RAISE_VARARGS_1       1  'exception instance'
            344_0  COME_FROM           328  '328'
            344_1  COME_FROM           320  '320'

 L. 208       344  LOAD_FAST                'tok'
              346  LOAD_METHOD              get_int
              348  CALL_METHOD_0         0  ''
              350  LOAD_FAST                'longitude'
              352  LOAD_CONST               0
              354  STORE_SUBSCR     

 L. 209       356  LOAD_FAST                'tok'
              358  LOAD_METHOD              get_string
              360  CALL_METHOD_0         0  ''
              362  STORE_FAST               't'

 L. 210       364  LOAD_FAST                't'
              366  LOAD_METHOD              isdigit
              368  CALL_METHOD_0         0  ''
          370_372  POP_JUMP_IF_FALSE   620  'to 620'

 L. 211       374  LOAD_GLOBAL              int
              376  LOAD_FAST                't'
              378  CALL_FUNCTION_1       1  ''
              380  LOAD_FAST                'longitude'
              382  LOAD_CONST               1
              384  STORE_SUBSCR     

 L. 212       386  LOAD_FAST                'tok'
              388  LOAD_METHOD              get_string
              390  CALL_METHOD_0         0  ''
              392  STORE_FAST               't'

 L. 213       394  LOAD_STR                 '.'
              396  LOAD_FAST                't'
              398  COMPARE_OP               in
          400_402  POP_JUMP_IF_FALSE   590  'to 590'

 L. 214       404  LOAD_FAST                't'
              406  LOAD_METHOD              split
              408  LOAD_STR                 '.'
              410  CALL_METHOD_1         1  ''
              412  UNPACK_SEQUENCE_2     2 
              414  STORE_FAST               'seconds'
              416  STORE_FAST               'milliseconds'

 L. 215       418  LOAD_FAST                'seconds'
              420  LOAD_METHOD              isdigit
              422  CALL_METHOD_0         0  ''
          424_426  POP_JUMP_IF_TRUE    440  'to 440'

 L. 216       428  LOAD_GLOBAL              dns
              430  LOAD_ATTR                exception
              432  LOAD_METHOD              SyntaxError

 L. 217       434  LOAD_STR                 'bad longitude seconds value'

 L. 216       436  CALL_METHOD_1         1  ''
              438  RAISE_VARARGS_1       1  'exception instance'
            440_0  COME_FROM           424  '424'

 L. 218       440  LOAD_GLOBAL              int
              442  LOAD_FAST                'seconds'
              444  CALL_FUNCTION_1       1  ''
              446  LOAD_FAST                'longitude'
              448  LOAD_CONST               2
              450  STORE_SUBSCR     

 L. 219       452  LOAD_FAST                'longitude'
              454  LOAD_CONST               2
              456  BINARY_SUBSCR    
              458  LOAD_CONST               60
              460  COMPARE_OP               >=
          462_464  POP_JUMP_IF_FALSE   478  'to 478'

 L. 220       466  LOAD_GLOBAL              dns
              468  LOAD_ATTR                exception
              470  LOAD_METHOD              SyntaxError
              472  LOAD_STR                 'longitude seconds >= 60'
              474  CALL_METHOD_1         1  ''
              476  RAISE_VARARGS_1       1  'exception instance'
            478_0  COME_FROM           462  '462'

 L. 221       478  LOAD_GLOBAL              len
              480  LOAD_FAST                'milliseconds'
              482  CALL_FUNCTION_1       1  ''
              484  STORE_FAST               'l'

 L. 222       486  LOAD_FAST                'l'
              488  LOAD_CONST               0
              490  COMPARE_OP               ==
          492_494  POP_JUMP_IF_TRUE    516  'to 516'
              496  LOAD_FAST                'l'
              498  LOAD_CONST               3
              500  COMPARE_OP               >
          502_504  POP_JUMP_IF_TRUE    516  'to 516'
              506  LOAD_FAST                'milliseconds'
              508  LOAD_METHOD              isdigit
              510  CALL_METHOD_0         0  ''
          512_514  POP_JUMP_IF_TRUE    528  'to 528'
            516_0  COME_FROM           502  '502'
            516_1  COME_FROM           492  '492'

 L. 223       516  LOAD_GLOBAL              dns
              518  LOAD_ATTR                exception
              520  LOAD_METHOD              SyntaxError

 L. 224       522  LOAD_STR                 'bad longitude milliseconds value'

 L. 223       524  CALL_METHOD_1         1  ''
              526  RAISE_VARARGS_1       1  'exception instance'
            528_0  COME_FROM           512  '512'

 L. 225       528  LOAD_FAST                'l'
              530  LOAD_CONST               1
              532  COMPARE_OP               ==
          534_536  POP_JUMP_IF_FALSE   544  'to 544'

 L. 226       538  LOAD_CONST               100
              540  STORE_FAST               'm'
              542  JUMP_FORWARD        564  'to 564'
            544_0  COME_FROM           534  '534'

 L. 227       544  LOAD_FAST                'l'
              546  LOAD_CONST               2
              548  COMPARE_OP               ==
          550_552  POP_JUMP_IF_FALSE   560  'to 560'

 L. 228       554  LOAD_CONST               10
              556  STORE_FAST               'm'
              558  JUMP_FORWARD        564  'to 564'
            560_0  COME_FROM           550  '550'

 L. 230       560  LOAD_CONST               1
              562  STORE_FAST               'm'
            564_0  COME_FROM           558  '558'
            564_1  COME_FROM           542  '542'

 L. 231       564  LOAD_FAST                'm'
              566  LOAD_GLOBAL              int
              568  LOAD_FAST                'milliseconds'
              570  CALL_FUNCTION_1       1  ''
              572  BINARY_MULTIPLY  
              574  LOAD_FAST                'longitude'
              576  LOAD_CONST               3
              578  STORE_SUBSCR     

 L. 232       580  LOAD_FAST                'tok'
              582  LOAD_METHOD              get_string
              584  CALL_METHOD_0         0  ''
              586  STORE_FAST               't'
              588  JUMP_FORWARD        620  'to 620'
            590_0  COME_FROM           400  '400'

 L. 233       590  LOAD_FAST                't'
              592  LOAD_METHOD              isdigit
              594  CALL_METHOD_0         0  ''
          596_598  POP_JUMP_IF_FALSE   620  'to 620'

 L. 234       600  LOAD_GLOBAL              int
              602  LOAD_FAST                't'
              604  CALL_FUNCTION_1       1  ''
              606  LOAD_FAST                'longitude'
              608  LOAD_CONST               2
              610  STORE_SUBSCR     

 L. 235       612  LOAD_FAST                'tok'
              614  LOAD_METHOD              get_string
              616  CALL_METHOD_0         0  ''
              618  STORE_FAST               't'
            620_0  COME_FROM           596  '596'
            620_1  COME_FROM           588  '588'
            620_2  COME_FROM           370  '370'

 L. 236       620  LOAD_FAST                't'
              622  LOAD_STR                 'W'
              624  COMPARE_OP               ==
          626_628  POP_JUMP_IF_FALSE   640  'to 640'

 L. 237       630  LOAD_CONST               -1
              632  LOAD_FAST                'longitude'
              634  LOAD_CONST               4
              636  STORE_SUBSCR     
              638  JUMP_FORWARD        662  'to 662'
            640_0  COME_FROM           626  '626'

 L. 238       640  LOAD_FAST                't'
              642  LOAD_STR                 'E'
              644  COMPARE_OP               !=
          646_648  POP_JUMP_IF_FALSE   662  'to 662'

 L. 239       650  LOAD_GLOBAL              dns
              652  LOAD_ATTR                exception
              654  LOAD_METHOD              SyntaxError
              656  LOAD_STR                 'bad longitude hemisphere value'
              658  CALL_METHOD_1         1  ''
              660  RAISE_VARARGS_1       1  'exception instance'
            662_0  COME_FROM           646  '646'
            662_1  COME_FROM           638  '638'

 L. 241       662  LOAD_FAST                'tok'
              664  LOAD_METHOD              get_string
              666  CALL_METHOD_0         0  ''
              668  STORE_FAST               't'

 L. 242       670  LOAD_FAST                't'
              672  LOAD_CONST               -1
              674  BINARY_SUBSCR    
              676  LOAD_STR                 'm'
              678  COMPARE_OP               ==
          680_682  POP_JUMP_IF_FALSE   696  'to 696'

 L. 243       684  LOAD_FAST                't'
              686  LOAD_CONST               0
              688  LOAD_CONST               -1
              690  BUILD_SLICE_2         2 
              692  BINARY_SUBSCR    
              694  STORE_FAST               't'
            696_0  COME_FROM           680  '680'

 L. 244       696  LOAD_GLOBAL              float
              698  LOAD_FAST                't'
              700  CALL_FUNCTION_1       1  ''
              702  LOAD_CONST               100.0
              704  BINARY_MULTIPLY  
              706  STORE_FAST               'altitude'

 L. 246       708  LOAD_FAST                'tok'
              710  LOAD_METHOD              get
              712  CALL_METHOD_0         0  ''
              714  LOAD_METHOD              unescape
              716  CALL_METHOD_0         0  ''
              718  STORE_FAST               'token'

 L. 247       720  LOAD_FAST                'token'
              722  LOAD_METHOD              is_eol_or_eof
              724  CALL_METHOD_0         0  ''
          726_728  POP_JUMP_IF_TRUE    914  'to 914'

 L. 248       730  LOAD_FAST                'token'
              732  LOAD_ATTR                value
              734  STORE_FAST               'value'

 L. 249       736  LOAD_FAST                'value'
              738  LOAD_CONST               -1
              740  BINARY_SUBSCR    
              742  LOAD_STR                 'm'
              744  COMPARE_OP               ==
          746_748  POP_JUMP_IF_FALSE   762  'to 762'

 L. 250       750  LOAD_FAST                'value'
              752  LOAD_CONST               0
              754  LOAD_CONST               -1
              756  BUILD_SLICE_2         2 
              758  BINARY_SUBSCR    
              760  STORE_FAST               'value'
            762_0  COME_FROM           746  '746'

 L. 251       762  LOAD_GLOBAL              float
              764  LOAD_FAST                'value'
              766  CALL_FUNCTION_1       1  ''
              768  LOAD_CONST               100.0
              770  BINARY_MULTIPLY  
              772  STORE_FAST               'size'

 L. 252       774  LOAD_FAST                'tok'
              776  LOAD_METHOD              get
              778  CALL_METHOD_0         0  ''
              780  LOAD_METHOD              unescape
              782  CALL_METHOD_0         0  ''
              784  STORE_FAST               'token'

 L. 253       786  LOAD_FAST                'token'
              788  LOAD_METHOD              is_eol_or_eof
              790  CALL_METHOD_0         0  ''
          792_794  POP_JUMP_IF_TRUE    914  'to 914'

 L. 254       796  LOAD_FAST                'token'
              798  LOAD_ATTR                value
              800  STORE_FAST               'value'

 L. 255       802  LOAD_FAST                'value'
              804  LOAD_CONST               -1
              806  BINARY_SUBSCR    
              808  LOAD_STR                 'm'
              810  COMPARE_OP               ==
          812_814  POP_JUMP_IF_FALSE   828  'to 828'

 L. 256       816  LOAD_FAST                'value'
              818  LOAD_CONST               0
              820  LOAD_CONST               -1
              822  BUILD_SLICE_2         2 
              824  BINARY_SUBSCR    
              826  STORE_FAST               'value'
            828_0  COME_FROM           812  '812'

 L. 257       828  LOAD_GLOBAL              float
              830  LOAD_FAST                'value'
              832  CALL_FUNCTION_1       1  ''
              834  LOAD_CONST               100.0
              836  BINARY_MULTIPLY  
              838  STORE_FAST               'hprec'

 L. 258       840  LOAD_FAST                'tok'
              842  LOAD_METHOD              get
              844  CALL_METHOD_0         0  ''
              846  LOAD_METHOD              unescape
              848  CALL_METHOD_0         0  ''
              850  STORE_FAST               'token'

 L. 259       852  LOAD_FAST                'token'
              854  LOAD_METHOD              is_eol_or_eof
              856  CALL_METHOD_0         0  ''
          858_860  POP_JUMP_IF_TRUE    914  'to 914'

 L. 260       862  LOAD_FAST                'token'
              864  LOAD_ATTR                value
              866  STORE_FAST               'value'

 L. 261       868  LOAD_FAST                'value'
              870  LOAD_CONST               -1
              872  BINARY_SUBSCR    
              874  LOAD_STR                 'm'
              876  COMPARE_OP               ==
          878_880  POP_JUMP_IF_FALSE   894  'to 894'

 L. 262       882  LOAD_FAST                'value'
              884  LOAD_CONST               0
              886  LOAD_CONST               -1
              888  BUILD_SLICE_2         2 
              890  BINARY_SUBSCR    
              892  STORE_FAST               'value'
            894_0  COME_FROM           878  '878'

 L. 263       894  LOAD_GLOBAL              float
              896  LOAD_FAST                'value'
              898  CALL_FUNCTION_1       1  ''
              900  LOAD_CONST               100.0
              902  BINARY_MULTIPLY  
              904  STORE_FAST               'vprec'

 L. 264       906  LOAD_FAST                'tok'
              908  LOAD_METHOD              get_eol
              910  CALL_METHOD_0         0  ''
              912  POP_TOP          
            914_0  COME_FROM           858  '858'
            914_1  COME_FROM           792  '792'
            914_2  COME_FROM           726  '726'

 L. 266       914  LOAD_FAST                'cls'
              916  LOAD_FAST                'rdclass'
              918  LOAD_FAST                'rdtype'
              920  LOAD_FAST                'latitude'
              922  LOAD_FAST                'longitude'
              924  LOAD_FAST                'altitude'

 L. 267       926  LOAD_FAST                'size'

 L. 267       928  LOAD_FAST                'hprec'

 L. 267       930  LOAD_FAST                'vprec'

 L. 266       932  CALL_FUNCTION_8       8  ''
              934  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 270

    def to_wire(self, file, compress=None, origin=None):
        milliseconds = (self.latitude[0] * 3600000 + self.latitude[1] * 60000 + self.latitude[2] * 1000 + self.latitude[3]) * self.latitude[4]
        latitude = long(2147483648) + milliseconds
        milliseconds = (self.longitude[0] * 3600000 + self.longitude[1] * 60000 + self.longitude[2] * 1000 + self.longitude[3]) * self.longitude[4]
        longitude = long(2147483648) + milliseconds
        altitude = long(self.altitude) + long(10000000)
        size = _encode_size(self.size, 'size')
        hprec = _encode_size(self.horizontal_precision, 'horizontal precision')
        vprec = _encode_size(self.vertical_precision, 'vertical precision')
        wire = struct.pack('!BBBBIII', 0, size, hprec, vprec, latitude, longitude, altitude)
        file.write(wire)

    @classmethod
    def from_wire(cls, rdclass, rdtype, wire, current, rdlen, origin=None):
        version, size, hprec, vprec, latitude, longitude, altitude = struct.unpack('!BBBBIII', wire[current:current + rdlen])
        if latitude > long(2147483648):
            latitude = float(latitude - long(2147483648)) / 3600000
        else:
            latitude = -1 * float(long(2147483648) - latitude) / 3600000
        if latitude < -90.0 or latitude > 90.0:
            raise dns.exception.FormError('bad latitude')
        elif longitude > long(2147483648):
            longitude = float(longitude - long(2147483648)) / 3600000
        else:
            longitude = -1 * float(long(2147483648) - longitude) / 3600000
        if longitude < -180.0 or longitude > 180.0:
            raise dns.exception.FormError('bad longitude')
        altitude = float(altitude) - 10000000.0
        size = _decode_size(size, 'size')
        hprec = _decode_size(hprec, 'horizontal precision')
        vprec = _decode_size(vprec, 'vertical precision')
        return clsrdclassrdtypelatitudelongitudealtitudesizehprecvprec

    def _get_float_latitude(self):
        return _tuple_to_float(self.latitude)

    def _set_float_latitude(self, value):
        self.latitude = _float_to_tuple(value)

    float_latitude = property(_get_float_latitude, _set_float_latitude, doc='latitude as a floating point value')

    def _get_float_longitude(self):
        return _tuple_to_float(self.longitude)

    def _set_float_longitude(self, value):
        self.longitude = _float_to_tuple(value)

    float_longitude = property(_get_float_longitude, _set_float_longitude, doc='longitude as a floating point value')