# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\core\getlimits.py
"""Machine limits for Float32 and Float64 and (long double) if available...

"""
__all__ = [
 'finfo', 'iinfo']
import warnings
from .machar import MachAr
from .overrides import set_module
from . import numeric
from . import numerictypes as ntypes
from .numeric import array, inf
from .umath import log10, exp2
from . import umath

def _fr0(a):
    """fix rank-0 --> rank-1"""
    if a.ndim == 0:
        a = a.copy()
        a.shape = (1, )
    return a


def _fr1(a):
    """fix rank > 0 --> rank-0"""
    if a.size == 1:
        a = a.copy()
        a.shape = ()
    return a


class MachArLike:
    __doc__ = ' Object to simulate MachAr instance '

    def __init__(self, ftype, *, eps, epsneg, huge, tiny, ibeta, **kwargs):
        params = _MACHAR_PARAMS[ftype]
        float_conv = lambda v: array([v], ftype)
        float_to_float = lambda v: _fr1(float_conv(v))
        float_to_str = lambda v: params['fmt'] % array(_fr0(v)[0], ftype)
        self.title = params['title']
        self.epsilon = self.eps = float_to_float(eps)
        self.epsneg = float_to_float(epsneg)
        self.xmax = self.huge = float_to_float(huge)
        self.xmin = self.tiny = float_to_float(tiny)
        self.ibeta = params['itype'](ibeta)
        self.__dict__.update(kwargs)
        self.precision = int(-log10(self.eps))
        self.resolution = float_to_float(float_conv(10) ** (-self.precision))
        self._str_eps = float_to_str(self.eps)
        self._str_epsneg = float_to_str(self.epsneg)
        self._str_xmin = float_to_str(self.xmin)
        self._str_xmax = float_to_str(self.xmax)
        self._str_resolution = float_to_str(self.resolution)


_convert_to_float = {ntypes.csingle: ntypes.single, 
 ntypes.complex_: ntypes.float_, 
 ntypes.clongfloat: ntypes.longfloat}
_title_fmt = 'numpy {} precision floating point number'
_MACHAR_PARAMS = {ntypes.double: dict(itype=(ntypes.int64),
                  fmt='%24.16e',
                  title=(_title_fmt.format('double'))), 
 
 ntypes.single: dict(itype=(ntypes.int32),
                  fmt='%15.7e',
                  title=(_title_fmt.format('single'))), 
 
 ntypes.longdouble: dict(itype=(ntypes.longlong),
                      fmt='%s',
                      title=(_title_fmt.format('long double'))), 
 
 ntypes.half: dict(itype=(ntypes.int16),
                fmt='%12.5e',
                title=(_title_fmt.format('half')))}
_KNOWN_TYPES = {}

def _register_type(machar, bytepat):
    _KNOWN_TYPES[bytepat] = machar


_float_ma = {}

def _register_known_types--- This code section failed: ---

 L.  97         0  LOAD_GLOBAL              ntypes
                2  LOAD_ATTR                float16
                4  STORE_FAST               'f16'

 L.  98         6  LOAD_GLOBAL              MachArLike
                8  LOAD_FAST                'f16'

 L.  99        10  LOAD_CONST               -10

 L. 100        12  LOAD_CONST               -11

 L. 101        14  LOAD_CONST               -14

 L. 102        16  LOAD_CONST               16

 L. 103        18  LOAD_CONST               10

 L. 104        20  LOAD_CONST               5

 L. 105        22  LOAD_CONST               2

 L. 106        24  LOAD_CONST               5

 L. 107        26  LOAD_CONST               0

 L. 108        28  LOAD_GLOBAL              exp2
               30  LOAD_FAST                'f16'
               32  LOAD_CONST               -10
               34  CALL_FUNCTION_1       1  ''
               36  CALL_FUNCTION_1       1  ''

 L. 109        38  LOAD_GLOBAL              exp2
               40  LOAD_FAST                'f16'
               42  LOAD_CONST               -11
               44  CALL_FUNCTION_1       1  ''
               46  CALL_FUNCTION_1       1  ''

 L. 110        48  LOAD_FAST                'f16'
               50  LOAD_CONST               65504
               52  CALL_FUNCTION_1       1  ''

 L. 111        54  LOAD_FAST                'f16'
               56  LOAD_CONST               6.103515625e-05
               58  CALL_FUNCTION_1       1  ''

 L.  98        60  LOAD_CONST               ('machep', 'negep', 'minexp', 'maxexp', 'it', 'iexp', 'ibeta', 'irnd', 'ngrd', 'eps', 'epsneg', 'huge', 'tiny')
               62  CALL_FUNCTION_KW_14    14  '14 total positional and keyword args'
               64  STORE_FAST               'float16_ma'

 L. 112        66  LOAD_GLOBAL              _register_type
               68  LOAD_FAST                'float16_ma'
               70  LOAD_CONST               b'f\xae'
               72  CALL_FUNCTION_2       2  ''
               74  POP_TOP          

 L. 113        76  LOAD_FAST                'float16_ma'
               78  LOAD_GLOBAL              _float_ma
               80  LOAD_CONST               16
               82  STORE_SUBSCR     

 L. 116        84  LOAD_GLOBAL              ntypes
               86  LOAD_ATTR                float32
               88  STORE_FAST               'f32'

 L. 117        90  LOAD_GLOBAL              MachArLike
               92  LOAD_FAST                'f32'

 L. 118        94  LOAD_CONST               -23

 L. 119        96  LOAD_CONST               -24

 L. 120        98  LOAD_CONST               -126

 L. 121       100  LOAD_CONST               128

 L. 122       102  LOAD_CONST               23

 L. 123       104  LOAD_CONST               8

 L. 124       106  LOAD_CONST               2

 L. 125       108  LOAD_CONST               5

 L. 126       110  LOAD_CONST               0

 L. 127       112  LOAD_GLOBAL              exp2
              114  LOAD_FAST                'f32'
              116  LOAD_CONST               -23
              118  CALL_FUNCTION_1       1  ''
              120  CALL_FUNCTION_1       1  ''

 L. 128       122  LOAD_GLOBAL              exp2
              124  LOAD_FAST                'f32'
              126  LOAD_CONST               -24
              128  CALL_FUNCTION_1       1  ''
              130  CALL_FUNCTION_1       1  ''

 L. 129       132  LOAD_FAST                'f32'
              134  LOAD_CONST               0.9999999403953552
              136  LOAD_CONST               2
              138  LOAD_CONST               128
              140  BINARY_POWER     
              142  BINARY_MULTIPLY  
              144  CALL_FUNCTION_1       1  ''

 L. 130       146  LOAD_GLOBAL              exp2
              148  LOAD_FAST                'f32'
              150  LOAD_CONST               -126
              152  CALL_FUNCTION_1       1  ''
              154  CALL_FUNCTION_1       1  ''

 L. 117       156  LOAD_CONST               ('machep', 'negep', 'minexp', 'maxexp', 'it', 'iexp', 'ibeta', 'irnd', 'ngrd', 'eps', 'epsneg', 'huge', 'tiny')
              158  CALL_FUNCTION_KW_14    14  '14 total positional and keyword args'
              160  STORE_FAST               'float32_ma'

 L. 131       162  LOAD_GLOBAL              _register_type
              164  LOAD_FAST                'float32_ma'
              166  LOAD_CONST               b'\xcd\xcc\xcc\xbd'
              168  CALL_FUNCTION_2       2  ''
              170  POP_TOP          

 L. 132       172  LOAD_FAST                'float32_ma'
              174  LOAD_GLOBAL              _float_ma
              176  LOAD_CONST               32
              178  STORE_SUBSCR     

 L. 135       180  LOAD_GLOBAL              ntypes
              182  LOAD_ATTR                float64
              184  STORE_FAST               'f64'

 L. 136       186  LOAD_CONST               1.1102230246251565e-16
              188  STORE_FAST               'epsneg_f64'

 L. 137       190  LOAD_CONST               2.2250738585072014e-308
              192  STORE_FAST               'tiny_f64'

 L. 138       194  LOAD_GLOBAL              MachArLike
              196  LOAD_FAST                'f64'

 L. 139       198  LOAD_CONST               -52

 L. 140       200  LOAD_CONST               -53

 L. 141       202  LOAD_CONST               -1022

 L. 142       204  LOAD_CONST               1024

 L. 143       206  LOAD_CONST               52

 L. 144       208  LOAD_CONST               11

 L. 145       210  LOAD_CONST               2

 L. 146       212  LOAD_CONST               5

 L. 147       214  LOAD_CONST               0

 L. 148       216  LOAD_CONST               2.220446049250313e-16

 L. 149       218  LOAD_FAST                'epsneg_f64'

 L. 150       220  LOAD_CONST               1.0
              222  LOAD_FAST                'epsneg_f64'
              224  BINARY_SUBTRACT  
              226  LOAD_FAST                'tiny_f64'
              228  BINARY_TRUE_DIVIDE
              230  LOAD_FAST                'f64'
              232  LOAD_CONST               4
              234  CALL_FUNCTION_1       1  ''
              236  BINARY_MULTIPLY  

 L. 151       238  LOAD_FAST                'tiny_f64'

 L. 138       240  LOAD_CONST               ('machep', 'negep', 'minexp', 'maxexp', 'it', 'iexp', 'ibeta', 'irnd', 'ngrd', 'eps', 'epsneg', 'huge', 'tiny')
              242  CALL_FUNCTION_KW_14    14  '14 total positional and keyword args'
              244  STORE_FAST               'float64_ma'

 L. 152       246  LOAD_GLOBAL              _register_type
              248  LOAD_FAST                'float64_ma'
              250  LOAD_CONST               b'\x9a\x99\x99\x99\x99\x99\xb9\xbf'
              252  CALL_FUNCTION_2       2  ''
              254  POP_TOP          

 L. 153       256  LOAD_FAST                'float64_ma'
              258  LOAD_GLOBAL              _float_ma
              260  LOAD_CONST               64
              262  STORE_SUBSCR     

 L. 156       264  LOAD_GLOBAL              ntypes
              266  LOAD_ATTR                longdouble
              268  STORE_FAST               'ld'

 L. 157       270  LOAD_GLOBAL              exp2
              272  LOAD_FAST                'ld'
              274  LOAD_CONST               -113
              276  CALL_FUNCTION_1       1  ''
              278  CALL_FUNCTION_1       1  ''
              280  STORE_FAST               'epsneg_f128'

 L. 158       282  LOAD_GLOBAL              exp2
              284  LOAD_FAST                'ld'
              286  LOAD_CONST               -16382
              288  CALL_FUNCTION_1       1  ''
              290  CALL_FUNCTION_1       1  ''
              292  STORE_FAST               'tiny_f128'

 L. 160       294  LOAD_GLOBAL              numeric
              296  LOAD_ATTR                errstate
              298  LOAD_STR                 'ignore'
              300  LOAD_CONST               ('all',)
              302  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              304  SETUP_WITH          346  'to 346'
              306  POP_TOP          

 L. 161       308  LOAD_FAST                'ld'
              310  LOAD_CONST               1
              312  CALL_FUNCTION_1       1  ''
              314  LOAD_FAST                'epsneg_f128'
              316  BINARY_SUBTRACT  
              318  LOAD_FAST                'tiny_f128'
              320  BINARY_TRUE_DIVIDE
              322  LOAD_FAST                'ld'
              324  LOAD_CONST               4
              326  CALL_FUNCTION_1       1  ''
              328  BINARY_MULTIPLY  
              330  STORE_FAST               'huge_f128'
              332  POP_BLOCK        
              334  LOAD_CONST               None
              336  DUP_TOP          
              338  DUP_TOP          
              340  CALL_FUNCTION_3       3  ''
              342  POP_TOP          
              344  JUMP_FORWARD        364  'to 364'
            346_0  COME_FROM_WITH      304  '304'
              346  <49>             
          348_350  POP_JUMP_IF_TRUE    354  'to 354'
              352  <48>             
            354_0  COME_FROM           348  '348'
              354  POP_TOP          
              356  POP_TOP          
              358  POP_TOP          
              360  POP_EXCEPT       
              362  POP_TOP          
            364_0  COME_FROM           344  '344'

 L. 162       364  LOAD_GLOBAL              MachArLike
              366  LOAD_FAST                'ld'

 L. 163       368  LOAD_CONST               -112

 L. 164       370  LOAD_CONST               -113

 L. 165       372  LOAD_CONST               -16382

 L. 166       374  LOAD_CONST               16384

 L. 167       376  LOAD_CONST               112

 L. 168       378  LOAD_CONST               15

 L. 169       380  LOAD_CONST               2

 L. 170       382  LOAD_CONST               5

 L. 171       384  LOAD_CONST               0

 L. 172       386  LOAD_GLOBAL              exp2
              388  LOAD_FAST                'ld'
              390  LOAD_CONST               -112
              392  CALL_FUNCTION_1       1  ''
              394  CALL_FUNCTION_1       1  ''

 L. 173       396  LOAD_FAST                'epsneg_f128'

 L. 174       398  LOAD_FAST                'huge_f128'

 L. 175       400  LOAD_FAST                'tiny_f128'

 L. 162       402  LOAD_CONST               ('machep', 'negep', 'minexp', 'maxexp', 'it', 'iexp', 'ibeta', 'irnd', 'ngrd', 'eps', 'epsneg', 'huge', 'tiny')
              404  CALL_FUNCTION_KW_14    14  '14 total positional and keyword args'
              406  STORE_FAST               'float128_ma'

 L. 177       408  LOAD_GLOBAL              _register_type
              410  LOAD_FAST                'float128_ma'

 L. 178       412  LOAD_CONST               b'\x9a\x99\x99\x99\x99\x99\x99\x99\x99\x99\x99\x99\x99\x99\xfb\xbf'

 L. 177       414  CALL_FUNCTION_2       2  ''
              416  POP_TOP          

 L. 179       418  LOAD_GLOBAL              _register_type
              420  LOAD_FAST                'float128_ma'

 L. 180       422  LOAD_CONST               b'\x9a\x99\x99\x99\x99\x99\x99\x99\x99\x99\x99\x99\x99\x99\xfb\xbf'

 L. 179       424  CALL_FUNCTION_2       2  ''
              426  POP_TOP          

 L. 181       428  LOAD_FAST                'float128_ma'
              430  LOAD_GLOBAL              _float_ma
              432  LOAD_CONST               128
              434  STORE_SUBSCR     

 L. 184       436  LOAD_GLOBAL              exp2
              438  LOAD_FAST                'ld'
              440  LOAD_CONST               -64
              442  CALL_FUNCTION_1       1  ''
              444  CALL_FUNCTION_1       1  ''
              446  STORE_FAST               'epsneg_f80'

 L. 185       448  LOAD_GLOBAL              exp2
              450  LOAD_FAST                'ld'
              452  LOAD_CONST               -16382
              454  CALL_FUNCTION_1       1  ''
              456  CALL_FUNCTION_1       1  ''
              458  STORE_FAST               'tiny_f80'

 L. 187       460  LOAD_GLOBAL              numeric
              462  LOAD_ATTR                errstate
              464  LOAD_STR                 'ignore'
              466  LOAD_CONST               ('all',)
              468  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              470  SETUP_WITH          512  'to 512'
              472  POP_TOP          

 L. 188       474  LOAD_FAST                'ld'
              476  LOAD_CONST               1
              478  CALL_FUNCTION_1       1  ''
              480  LOAD_FAST                'epsneg_f80'
              482  BINARY_SUBTRACT  
              484  LOAD_FAST                'tiny_f80'
              486  BINARY_TRUE_DIVIDE
              488  LOAD_FAST                'ld'
              490  LOAD_CONST               4
              492  CALL_FUNCTION_1       1  ''
              494  BINARY_MULTIPLY  
              496  STORE_FAST               'huge_f80'
              498  POP_BLOCK        
              500  LOAD_CONST               None
              502  DUP_TOP          
              504  DUP_TOP          
              506  CALL_FUNCTION_3       3  ''
              508  POP_TOP          
              510  JUMP_FORWARD        530  'to 530'
            512_0  COME_FROM_WITH      470  '470'
              512  <49>             
          514_516  POP_JUMP_IF_TRUE    520  'to 520'
              518  <48>             
            520_0  COME_FROM           514  '514'
              520  POP_TOP          
              522  POP_TOP          
              524  POP_TOP          
              526  POP_EXCEPT       
              528  POP_TOP          
            530_0  COME_FROM           510  '510'

 L. 189       530  LOAD_GLOBAL              MachArLike
              532  LOAD_FAST                'ld'

 L. 190       534  LOAD_CONST               -63

 L. 191       536  LOAD_CONST               -64

 L. 192       538  LOAD_CONST               -16382

 L. 193       540  LOAD_CONST               16384

 L. 194       542  LOAD_CONST               63

 L. 195       544  LOAD_CONST               15

 L. 196       546  LOAD_CONST               2

 L. 197       548  LOAD_CONST               5

 L. 198       550  LOAD_CONST               0

 L. 199       552  LOAD_GLOBAL              exp2
              554  LOAD_FAST                'ld'
              556  LOAD_CONST               -63
              558  CALL_FUNCTION_1       1  ''
              560  CALL_FUNCTION_1       1  ''

 L. 200       562  LOAD_FAST                'epsneg_f80'

 L. 201       564  LOAD_FAST                'huge_f80'

 L. 202       566  LOAD_FAST                'tiny_f80'

 L. 189       568  LOAD_CONST               ('machep', 'negep', 'minexp', 'maxexp', 'it', 'iexp', 'ibeta', 'irnd', 'ngrd', 'eps', 'epsneg', 'huge', 'tiny')
              570  CALL_FUNCTION_KW_14    14  '14 total positional and keyword args'
              572  STORE_FAST               'float80_ma'

 L. 204       574  LOAD_GLOBAL              _register_type
              576  LOAD_FAST                'float80_ma'
              578  LOAD_CONST               b'\xcd\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xfb\xbf'
              580  CALL_FUNCTION_2       2  ''
              582  POP_TOP          

 L. 205       584  LOAD_FAST                'float80_ma'
              586  LOAD_GLOBAL              _float_ma
              588  LOAD_CONST               80
              590  STORE_SUBSCR     

 L. 212       592  LOAD_GLOBAL              hasattr
              594  LOAD_GLOBAL              umath
              596  LOAD_STR                 'nextafter'
              598  CALL_FUNCTION_2       2  ''

 L. 211   600_602  POP_JUMP_IF_FALSE   624  'to 624'
              604  LOAD_GLOBAL              umath
              606  LOAD_METHOD              nextafter
              608  LOAD_FAST                'ld'
              610  LOAD_GLOBAL              inf
              612  CALL_FUNCTION_1       1  ''
              614  LOAD_FAST                'ld'
              616  LOAD_CONST               0
              618  CALL_FUNCTION_1       1  ''
              620  CALL_METHOD_2         2  ''
              622  JUMP_FORWARD        628  'to 628'
            624_0  COME_FROM           600  '600'

 L. 213       624  LOAD_FAST                'float64_ma'
              626  LOAD_ATTR                huge
            628_0  COME_FROM           622  '622'

 L. 211       628  STORE_FAST               'huge_dd'

 L. 214       630  LOAD_GLOBAL              MachArLike
              632  LOAD_FAST                'ld'

 L. 215       634  LOAD_CONST               -105

 L. 216       636  LOAD_CONST               -106

 L. 217       638  LOAD_CONST               -1022

 L. 218       640  LOAD_CONST               1024

 L. 219       642  LOAD_CONST               105

 L. 220       644  LOAD_CONST               11

 L. 221       646  LOAD_CONST               2

 L. 222       648  LOAD_CONST               5

 L. 223       650  LOAD_CONST               0

 L. 224       652  LOAD_GLOBAL              exp2
              654  LOAD_FAST                'ld'
              656  LOAD_CONST               -105
              658  CALL_FUNCTION_1       1  ''
              660  CALL_FUNCTION_1       1  ''

 L. 225       662  LOAD_GLOBAL              exp2
              664  LOAD_FAST                'ld'
              666  LOAD_CONST               -106
              668  CALL_FUNCTION_1       1  ''
              670  CALL_FUNCTION_1       1  ''

 L. 226       672  LOAD_FAST                'huge_dd'

 L. 227       674  LOAD_GLOBAL              exp2
              676  LOAD_FAST                'ld'
              678  LOAD_CONST               -1022
              680  CALL_FUNCTION_1       1  ''
              682  CALL_FUNCTION_1       1  ''

 L. 214       684  LOAD_CONST               ('machep', 'negep', 'minexp', 'maxexp', 'it', 'iexp', 'ibeta', 'irnd', 'ngrd', 'eps', 'epsneg', 'huge', 'tiny')
              686  CALL_FUNCTION_KW_14    14  '14 total positional and keyword args'
              688  STORE_FAST               'float_dd_ma'

 L. 229       690  LOAD_GLOBAL              _register_type
              692  LOAD_FAST                'float_dd_ma'

 L. 230       694  LOAD_CONST               b'\x9a\x99\x99\x99\x99\x99Y<\x9a\x99\x99\x99\x99\x99\xb9\xbf'

 L. 229       696  CALL_FUNCTION_2       2  ''
              698  POP_TOP          

 L. 232       700  LOAD_GLOBAL              _register_type
              702  LOAD_FAST                'float_dd_ma'

 L. 233       704  LOAD_CONST               b'\x9a\x99\x99\x99\x99\x99\xb9\xbf\x9a\x99\x99\x99\x99\x99Y<'

 L. 232       706  CALL_FUNCTION_2       2  ''
              708  POP_TOP          

 L. 234       710  LOAD_FAST                'float_dd_ma'
              712  LOAD_GLOBAL              _float_ma
              714  LOAD_STR                 'dd'
              716  STORE_SUBSCR     

Parse error at or near `DUP_TOP' instruction at offset 336


def _get_machar--- This code section failed: ---

 L. 260         0  LOAD_GLOBAL              _MACHAR_PARAMS
                2  LOAD_METHOD              get
                4  LOAD_FAST                'ftype'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'params'

 L. 261        10  LOAD_FAST                'params'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    30  'to 30'

 L. 262        18  LOAD_GLOBAL              ValueError
               20  LOAD_GLOBAL              repr
               22  LOAD_FAST                'ftype'
               24  CALL_FUNCTION_1       1  ''
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            16  '16'

 L. 264        30  LOAD_FAST                'ftype'
               32  LOAD_STR                 '-0.1'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_METHOD              newbyteorder
               38  LOAD_STR                 '<'
               40  CALL_METHOD_1         1  ''
               42  LOAD_METHOD              tobytes
               44  CALL_METHOD_0         0  ''
               46  STORE_FAST               'key'

 L. 265        48  LOAD_GLOBAL              _KNOWN_TYPES
               50  LOAD_METHOD              get
               52  LOAD_FAST                'key'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'ma_like'

 L. 268        58  LOAD_FAST                'ma_like'
               60  LOAD_CONST               None
               62  <117>                 0  ''
               64  POP_JUMP_IF_FALSE    94  'to 94'
               66  LOAD_FAST                'ftype'
               68  LOAD_GLOBAL              ntypes
               70  LOAD_ATTR                longdouble
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE    94  'to 94'

 L. 269        76  LOAD_GLOBAL              _KNOWN_TYPES
               78  LOAD_METHOD              get
               80  LOAD_FAST                'key'
               82  LOAD_CONST               None
               84  LOAD_CONST               10
               86  BUILD_SLICE_2         2 
               88  BINARY_SUBSCR    
               90  CALL_METHOD_1         1  ''
               92  STORE_FAST               'ma_like'
             94_0  COME_FROM            74  '74'
             94_1  COME_FROM            64  '64'

 L. 270        94  LOAD_FAST                'ma_like'
               96  LOAD_CONST               None
               98  <117>                 1  ''
              100  POP_JUMP_IF_FALSE   106  'to 106'

 L. 271       102  LOAD_FAST                'ma_like'
              104  RETURN_VALUE     
            106_0  COME_FROM           100  '100'

 L. 273       106  LOAD_GLOBAL              warnings
              108  LOAD_ATTR                warn

 L. 274       110  LOAD_STR                 'Signature {} for {} does not match any known type: falling back to type probe function'
              112  LOAD_METHOD              format

 L. 275       114  LOAD_FAST                'key'
              116  LOAD_FAST                'ftype'

 L. 274       118  CALL_METHOD_2         2  ''

 L. 276       120  LOAD_GLOBAL              UserWarning
              122  LOAD_CONST               2

 L. 273       124  LOAD_CONST               ('stacklevel',)
              126  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              128  POP_TOP          

 L. 277       130  LOAD_GLOBAL              _discovered_machar
              132  LOAD_FAST                'ftype'
              134  CALL_FUNCTION_1       1  ''
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14


def _discovered_machar(ftype):
    """ Create MachAr instance with found information on float types
    """
    params = _MACHAR_PARAMS[ftype]
    return MachAr(lambda v: array([v], ftype), lambda v: _fr0(v.astype(params['itype']))[0], lambda v: array(_fr0(v)[0], ftype), lambda v: params['fmt'] % array(_fr0(v)[0], ftype), params['title'])


@set_module('numpy')
class finfo:
    __doc__ = "\n    finfo(dtype)\n\n    Machine limits for floating point types.\n\n    Attributes\n    ----------\n    bits : int\n        The number of bits occupied by the type.\n    eps : float\n        The difference between 1.0 and the next smallest representable float\n        larger than 1.0. For example, for 64-bit binary floats in the IEEE-754\n        standard, ``eps = 2**-52``, approximately 2.22e-16.\n    epsneg : float\n        The difference between 1.0 and the next smallest representable float\n        less than 1.0. For example, for 64-bit binary floats in the IEEE-754\n        standard, ``epsneg = 2**-53``, approximately 1.11e-16.\n    iexp : int\n        The number of bits in the exponent portion of the floating point\n        representation.\n    machar : MachAr\n        The object which calculated these parameters and holds more\n        detailed information.\n    machep : int\n        The exponent that yields `eps`.\n    max : floating point number of the appropriate type\n        The largest representable number.\n    maxexp : int\n        The smallest positive power of the base (2) that causes overflow.\n    min : floating point number of the appropriate type\n        The smallest representable number, typically ``-max``.\n    minexp : int\n        The most negative power of the base (2) consistent with there\n        being no leading 0's in the mantissa.\n    negep : int\n        The exponent that yields `epsneg`.\n    nexp : int\n        The number of bits in the exponent including its sign and bias.\n    nmant : int\n        The number of bits in the mantissa.\n    precision : int\n        The approximate number of decimal digits to which this kind of\n        float is precise.\n    resolution : floating point number of the appropriate type\n        The approximate decimal resolution of this type, i.e.,\n        ``10**-precision``.\n    tiny : float\n        The smallest positive usable number.  Type of `tiny` is an\n        appropriate floating point type.\n\n    Parameters\n    ----------\n    dtype : float, dtype, or instance\n        Kind of floating point data-type about which to get information.\n\n    See Also\n    --------\n    MachAr : The implementation of the tests that produce this information.\n    iinfo : The equivalent for integer data types.\n    spacing : The distance between a value and the nearest adjacent number\n    nextafter : The next floating point value after x1 towards x2\n\n    Notes\n    -----\n    For developers of NumPy: do not instantiate this at the module level.\n    The initial calculation of these parameters is expensive and negatively\n    impacts import times.  These objects are cached, so calling ``finfo()``\n    repeatedly inside your functions is not a problem.\n\n    "
    _finfo_cache = {}

    def __new__--- This code section failed: ---

 L. 367         0  SETUP_FINALLY        16  'to 16'

 L. 368         2  LOAD_GLOBAL              numeric
                4  LOAD_METHOD              dtype
                6  LOAD_FAST                'dtype'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'dtype'
               12  POP_BLOCK        
               14  JUMP_FORWARD         48  'to 48'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 369        16  DUP_TOP          
               18  LOAD_GLOBAL              TypeError
               20  <121>                46  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 371        28  LOAD_GLOBAL              numeric
               30  LOAD_METHOD              dtype
               32  LOAD_GLOBAL              type
               34  LOAD_FAST                'dtype'
               36  CALL_FUNCTION_1       1  ''
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'dtype'
               42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            14  '14'

 L. 373        48  LOAD_FAST                'cls'
               50  LOAD_ATTR                _finfo_cache
               52  LOAD_METHOD              get
               54  LOAD_FAST                'dtype'
               56  LOAD_CONST               None
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'obj'

 L. 374        62  LOAD_FAST                'obj'
               64  LOAD_CONST               None
               66  <117>                 1  ''
               68  POP_JUMP_IF_FALSE    74  'to 74'

 L. 375        70  LOAD_FAST                'obj'
               72  RETURN_VALUE     
             74_0  COME_FROM            68  '68'

 L. 376        74  LOAD_FAST                'dtype'
               76  BUILD_LIST_1          1 
               78  STORE_FAST               'dtypes'

 L. 377        80  LOAD_GLOBAL              numeric
               82  LOAD_METHOD              obj2sctype
               84  LOAD_FAST                'dtype'
               86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'newdtype'

 L. 378        90  LOAD_FAST                'newdtype'
               92  LOAD_FAST                'dtype'
               94  <117>                 1  ''
               96  POP_JUMP_IF_FALSE   112  'to 112'

 L. 379        98  LOAD_FAST                'dtypes'
              100  LOAD_METHOD              append
              102  LOAD_FAST                'newdtype'
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          

 L. 380       108  LOAD_FAST                'newdtype'
              110  STORE_FAST               'dtype'
            112_0  COME_FROM            96  '96'

 L. 381       112  LOAD_GLOBAL              issubclass
              114  LOAD_FAST                'dtype'
              116  LOAD_GLOBAL              numeric
              118  LOAD_ATTR                inexact
              120  CALL_FUNCTION_2       2  ''
              122  POP_JUMP_IF_TRUE    136  'to 136'

 L. 382       124  LOAD_GLOBAL              ValueError
              126  LOAD_STR                 'data type %r not inexact'
              128  LOAD_FAST                'dtype'
              130  BINARY_MODULO    
              132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           122  '122'

 L. 383       136  LOAD_FAST                'cls'
              138  LOAD_ATTR                _finfo_cache
              140  LOAD_METHOD              get
              142  LOAD_FAST                'dtype'
              144  LOAD_CONST               None
              146  CALL_METHOD_2         2  ''
              148  STORE_FAST               'obj'

 L. 384       150  LOAD_FAST                'obj'
              152  LOAD_CONST               None
              154  <117>                 1  ''
              156  POP_JUMP_IF_FALSE   162  'to 162'

 L. 385       158  LOAD_FAST                'obj'
              160  RETURN_VALUE     
            162_0  COME_FROM           156  '156'

 L. 386       162  LOAD_GLOBAL              issubclass
              164  LOAD_FAST                'dtype'
              166  LOAD_GLOBAL              numeric
              168  LOAD_ATTR                floating
              170  CALL_FUNCTION_2       2  ''
              172  POP_JUMP_IF_TRUE    204  'to 204'

 L. 387       174  LOAD_GLOBAL              _convert_to_float
              176  LOAD_FAST                'dtype'
              178  BINARY_SUBSCR    
              180  STORE_FAST               'newdtype'

 L. 388       182  LOAD_FAST                'newdtype'
              184  LOAD_FAST                'dtype'
              186  <117>                 1  ''
              188  POP_JUMP_IF_FALSE   204  'to 204'

 L. 389       190  LOAD_FAST                'dtypes'
              192  LOAD_METHOD              append
              194  LOAD_FAST                'newdtype'
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          

 L. 390       200  LOAD_FAST                'newdtype'
              202  STORE_FAST               'dtype'
            204_0  COME_FROM           188  '188'
            204_1  COME_FROM           172  '172'

 L. 391       204  LOAD_FAST                'cls'
              206  LOAD_ATTR                _finfo_cache
              208  LOAD_METHOD              get
              210  LOAD_FAST                'dtype'
              212  LOAD_CONST               None
              214  CALL_METHOD_2         2  ''
              216  STORE_FAST               'obj'

 L. 392       218  LOAD_FAST                'obj'
              220  LOAD_CONST               None
              222  <117>                 1  ''
              224  POP_JUMP_IF_FALSE   230  'to 230'

 L. 393       226  LOAD_FAST                'obj'
              228  RETURN_VALUE     
            230_0  COME_FROM           224  '224'

 L. 394       230  LOAD_GLOBAL              object
              232  LOAD_METHOD              __new__
              234  LOAD_FAST                'cls'
              236  CALL_METHOD_1         1  ''
              238  LOAD_METHOD              _init
              240  LOAD_FAST                'dtype'
              242  CALL_METHOD_1         1  ''
              244  STORE_FAST               'obj'

 L. 395       246  LOAD_FAST                'dtypes'
              248  GET_ITER         
            250_0  COME_FROM           264  '264'
              250  FOR_ITER            266  'to 266'
              252  STORE_FAST               'dt'

 L. 396       254  LOAD_FAST                'obj'
              256  LOAD_FAST                'cls'
              258  LOAD_ATTR                _finfo_cache
              260  LOAD_FAST                'dt'
              262  STORE_SUBSCR     
              264  JUMP_BACK           250  'to 250'
            266_0  COME_FROM           250  '250'

 L. 397       266  LOAD_FAST                'obj'
              268  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 20

    def _init(self, dtype):
        self.dtype = numeric.dtype(dtype)
        machar = _get_machar(dtype)
        for word in ('precision', 'iexp', 'maxexp', 'minexp', 'negep', 'machep'):
            setattrselfwordgetattr(machar, word)
        else:
            for word in ('tiny', 'resolution', 'epsneg'):
                setattrselfwordgetattr(machar, word).flat[0]
            else:
                self.bits = self.dtype.itemsize * 8
                self.max = machar.huge.flat[0]
                self.min = -self.max
                self.eps = machar.eps.flat[0]
                self.nexp = machar.iexp
                self.nmant = machar.it
                self.machar = machar
                self._str_tiny = machar._str_xmin.strip()
                self._str_max = machar._str_xmax.strip()
                self._str_epsneg = machar._str_epsneg.strip()
                self._str_eps = machar._str_eps.strip()
                self._str_resolution = machar._str_resolution.strip()
                return self

    def __str__(self):
        fmt = 'Machine parameters for %(dtype)s\n---------------------------------------------------------------\nprecision = %(precision)3s   resolution = %(_str_resolution)s\nmachep = %(machep)6s   eps =        %(_str_eps)s\nnegep =  %(negep)6s   epsneg =     %(_str_epsneg)s\nminexp = %(minexp)6s   tiny =       %(_str_tiny)s\nmaxexp = %(maxexp)6s   max =        %(_str_max)s\nnexp =   %(nexp)6s   min =        -max\n---------------------------------------------------------------\n'
        return fmt % self.__dict__

    def __repr__(self):
        c = self.__class__.__name__
        d = self.__dict__.copy()
        d['klass'] = c
        return '%(klass)s(resolution=%(resolution)s, min=-%(_str_max)s, max=%(_str_max)s, dtype=%(dtype)s)' % d


@set_module('numpy')
class iinfo:
    __doc__ = '\n    iinfo(type)\n\n    Machine limits for integer types.\n\n    Attributes\n    ----------\n    bits : int\n        The number of bits occupied by the type.\n    min : int\n        The smallest integer expressible by the type.\n    max : int\n        The largest integer expressible by the type.\n\n    Parameters\n    ----------\n    int_type : integer type, dtype, or instance\n        The kind of integer data type to get information about.\n\n    See Also\n    --------\n    finfo : The equivalent for floating point data types.\n\n    Examples\n    --------\n    With types:\n\n    >>> ii16 = np.iinfo(np.int16)\n    >>> ii16.min\n    -32768\n    >>> ii16.max\n    32767\n    >>> ii32 = np.iinfo(np.int32)\n    >>> ii32.min\n    -2147483648\n    >>> ii32.max\n    2147483647\n\n    With instances:\n\n    >>> ii32 = np.iinfo(np.int32(10))\n    >>> ii32.min\n    -2147483648\n    >>> ii32.max\n    2147483647\n\n    '
    _min_vals = {}
    _max_vals = {}

    def __init__--- This code section failed: ---

 L. 499         0  SETUP_FINALLY        18  'to 18'

 L. 500         2  LOAD_GLOBAL              numeric
                4  LOAD_METHOD              dtype
                6  LOAD_FAST                'int_type'
                8  CALL_METHOD_1         1  ''
               10  LOAD_FAST                'self'
               12  STORE_ATTR               dtype
               14  POP_BLOCK        
               16  JUMP_FORWARD         52  'to 52'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 501        18  DUP_TOP          
               20  LOAD_GLOBAL              TypeError
               22  <121>                50  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 502        30  LOAD_GLOBAL              numeric
               32  LOAD_METHOD              dtype
               34  LOAD_GLOBAL              type
               36  LOAD_FAST                'int_type'
               38  CALL_FUNCTION_1       1  ''
               40  CALL_METHOD_1         1  ''
               42  LOAD_FAST                'self'
               44  STORE_ATTR               dtype
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
               50  <48>             
             52_0  COME_FROM            48  '48'
             52_1  COME_FROM            16  '16'

 L. 503        52  LOAD_FAST                'self'
               54  LOAD_ATTR                dtype
               56  LOAD_ATTR                kind
               58  LOAD_FAST                'self'
               60  STORE_ATTR               kind

 L. 504        62  LOAD_FAST                'self'
               64  LOAD_ATTR                dtype
               66  LOAD_ATTR                itemsize
               68  LOAD_CONST               8
               70  BINARY_MULTIPLY  
               72  LOAD_FAST                'self'
               74  STORE_ATTR               bits

 L. 505        76  LOAD_STR                 '%s%d'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                kind
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                bits
               86  BUILD_TUPLE_2         2 
               88  BINARY_MODULO    
               90  LOAD_FAST                'self'
               92  STORE_ATTR               key

 L. 506        94  LOAD_FAST                'self'
               96  LOAD_ATTR                kind
               98  LOAD_STR                 'iu'
              100  <118>                 1  ''
              102  POP_JUMP_IF_FALSE   120  'to 120'

 L. 507       104  LOAD_GLOBAL              ValueError
              106  LOAD_STR                 'Invalid integer data type %r.'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                kind
              112  BUILD_TUPLE_1         1 
              114  BINARY_MODULO    
              116  CALL_FUNCTION_1       1  ''
              118  RAISE_VARARGS_1       1  'exception instance'
            120_0  COME_FROM           102  '102'

Parse error at or near `<121>' instruction at offset 22

    @property
    def min--- This code section failed: ---

 L. 512         0  LOAD_FAST                'self'
                2  LOAD_ATTR                kind
                4  LOAD_STR                 'u'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 513        10  LOAD_CONST               0
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 515        14  SETUP_FINALLY        32  'to 32'

 L. 516        16  LOAD_GLOBAL              iinfo
               18  LOAD_ATTR                _min_vals
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                key
               24  BINARY_SUBSCR    
               26  STORE_FAST               'val'
               28  POP_BLOCK        
               30  JUMP_FORWARD         82  'to 82'
             32_0  COME_FROM_FINALLY    14  '14'

 L. 517        32  DUP_TOP          
               34  LOAD_GLOBAL              KeyError
               36  <121>                80  ''
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 518        44  LOAD_GLOBAL              int
               46  LOAD_CONST               1
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                bits
               52  LOAD_CONST               1
               54  BINARY_SUBTRACT  
               56  BINARY_LSHIFT    
               58  UNARY_NEGATIVE   
               60  CALL_FUNCTION_1       1  ''
               62  STORE_FAST               'val'

 L. 519        64  LOAD_FAST                'val'
               66  LOAD_GLOBAL              iinfo
               68  LOAD_ATTR                _min_vals
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                key
               74  STORE_SUBSCR     
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
               80  <48>             
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            30  '30'

 L. 520        82  LOAD_FAST                'val'
               84  RETURN_VALUE     

Parse error at or near `<121>' instruction at offset 36

    @property
    def max--- This code section failed: ---

 L. 525         0  SETUP_FINALLY        18  'to 18'

 L. 526         2  LOAD_GLOBAL              iinfo
                4  LOAD_ATTR                _max_vals
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                key
               10  BINARY_SUBSCR    
               12  STORE_FAST               'val'
               14  POP_BLOCK        
               16  JUMP_FORWARD        100  'to 100'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 527        18  DUP_TOP          
               20  LOAD_GLOBAL              KeyError
               22  <121>                98  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 528        30  LOAD_FAST                'self'
               32  LOAD_ATTR                kind
               34  LOAD_STR                 'u'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    60  'to 60'

 L. 529        40  LOAD_GLOBAL              int
               42  LOAD_CONST               1
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                bits
               48  BINARY_LSHIFT    
               50  LOAD_CONST               1
               52  BINARY_SUBTRACT  
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'val'
               58  JUMP_FORWARD         82  'to 82'
             60_0  COME_FROM            38  '38'

 L. 531        60  LOAD_GLOBAL              int
               62  LOAD_CONST               1
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                bits
               68  LOAD_CONST               1
               70  BINARY_SUBTRACT  
               72  BINARY_LSHIFT    
               74  LOAD_CONST               1
               76  BINARY_SUBTRACT  
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'val'
             82_0  COME_FROM            58  '58'

 L. 532        82  LOAD_FAST                'val'
               84  LOAD_GLOBAL              iinfo
               86  LOAD_ATTR                _max_vals
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                key
               92  STORE_SUBSCR     
               94  POP_EXCEPT       
               96  JUMP_FORWARD        100  'to 100'
               98  <48>             
            100_0  COME_FROM            96  '96'
            100_1  COME_FROM            16  '16'

 L. 533       100  LOAD_FAST                'val'
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 22

    def __str__(self):
        """String representation."""
        fmt = 'Machine parameters for %(dtype)s\n---------------------------------------------------------------\nmin = %(min)s\nmax = %(max)s\n---------------------------------------------------------------\n'
        return fmt % {'dtype':self.dtype,  'min':self.min,  'max':self.max}

    def __repr__(self):
        return '%s(min=%s, max=%s, dtype=%s)' % (self.__class__.__name__,
         self.min, self.max, self.dtype)