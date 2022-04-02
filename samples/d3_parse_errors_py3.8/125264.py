# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\core\machar.py
"""
Machine arithmetics - determine the parameters of the
floating-point arithmetic system

Author: Pearu Peterson, September 2003

"""
__all__ = [
 'MachAr']
from numpy.core.fromnumeric import any
from numpy.core._ufunc_config import errstate
from numpy.core.overrides import set_module

@set_module('numpy')
class MachAr:
    __doc__ = '\n    Diagnosing machine parameters.\n\n    Attributes\n    ----------\n    ibeta : int\n        Radix in which numbers are represented.\n    it : int\n        Number of base-`ibeta` digits in the floating point mantissa M.\n    machep : int\n        Exponent of the smallest (most negative) power of `ibeta` that,\n        added to 1.0, gives something different from 1.0\n    eps : float\n        Floating-point number ``beta**machep`` (floating point precision)\n    negep : int\n        Exponent of the smallest power of `ibeta` that, subtracted\n        from 1.0, gives something different from 1.0.\n    epsneg : float\n        Floating-point number ``beta**negep``.\n    iexp : int\n        Number of bits in the exponent (including its sign and bias).\n    minexp : int\n        Smallest (most negative) power of `ibeta` consistent with there\n        being no leading zeros in the mantissa.\n    xmin : float\n        Floating point number ``beta**minexp`` (the smallest [in\n        magnitude] usable floating value).\n    maxexp : int\n        Smallest (positive) power of `ibeta` that causes overflow.\n    xmax : float\n        ``(1-epsneg) * beta**maxexp`` (the largest [in magnitude]\n        usable floating value).\n    irnd : int\n        In ``range(6)``, information on what kind of rounding is done\n        in addition, and on how underflow is handled.\n    ngrd : int\n        Number of \'guard digits\' used when truncating the product\n        of two mantissas to fit the representation.\n    epsilon : float\n        Same as `eps`.\n    tiny : float\n        Same as `xmin`.\n    huge : float\n        Same as `xmax`.\n    precision : float\n        ``- int(-log10(eps))``\n    resolution : float\n        ``- 10**(-precision)``\n\n    Parameters\n    ----------\n    float_conv : function, optional\n        Function that converts an integer or integer array to a float\n        or float array. Default is `float`.\n    int_conv : function, optional\n        Function that converts a float or float array to an integer or\n        integer array. Default is `int`.\n    float_to_float : function, optional\n        Function that converts a float array to float. Default is `float`.\n        Note that this does not seem to do anything useful in the current\n        implementation.\n    float_to_str : function, optional\n        Function that converts a single float to a string. Default is\n        ``lambda v:\'%24.16e\' %v``.\n    title : str, optional\n        Title that is printed in the string representation of `MachAr`.\n\n    See Also\n    --------\n    finfo : Machine limits for floating point types.\n    iinfo : Machine limits for integer types.\n\n    References\n    ----------\n    .. [1] Press, Teukolsky, Vetterling and Flannery,\n           "Numerical Recipes in C++," 2nd ed,\n           Cambridge University Press, 2002, p. 31.\n\n    '

    def __init__(self, float_conv=float, int_conv=int, float_to_float=float, float_to_str=lambda v: '%24.16e' % v, title='Python floating point number'):
        """

        float_conv - convert integer to float (array)
        int_conv   - convert float (array) to integer
        float_to_float - convert float array to float
        float_to_str - convert array float to str
        title        - description of used floating point numbers

        """
        with errstate(under='ignore'):
            self._do_init(float_conv, int_conv, float_to_float, float_to_str, title)

    def _do_init--- This code section failed: ---

 L. 117         0  LOAD_CONST               10000
                2  STORE_FAST               'max_iterN'

 L. 118         4  LOAD_STR                 'Did not converge after %d tries with %s'
                6  STORE_FAST               'msg'

 L. 119         8  LOAD_FAST                'float_conv'
               10  LOAD_CONST               1
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'one'

 L. 120        16  LOAD_FAST                'one'
               18  LOAD_FAST                'one'
               20  BINARY_ADD       
               22  STORE_FAST               'two'

 L. 121        24  LOAD_FAST                'one'
               26  LOAD_FAST                'one'
               28  BINARY_SUBTRACT  
               30  STORE_FAST               'zero'

 L. 125        32  LOAD_FAST                'one'
               34  STORE_FAST               'a'

 L. 126        36  LOAD_GLOBAL              range
               38  LOAD_FAST                'max_iterN'
               40  CALL_FUNCTION_1       1  ''
               42  GET_ITER         
             44_0  COME_FROM            92  '92'
             44_1  COME_FROM            86  '86'
               44  FOR_ITER             94  'to 94'
               46  STORE_FAST               '_'

 L. 127        48  LOAD_FAST                'a'
               50  LOAD_FAST                'a'
               52  BINARY_ADD       
               54  STORE_FAST               'a'

 L. 128        56  LOAD_FAST                'a'
               58  LOAD_FAST                'one'
               60  BINARY_ADD       
               62  STORE_FAST               'temp'

 L. 129        64  LOAD_FAST                'temp'
               66  LOAD_FAST                'a'
               68  BINARY_SUBTRACT  
               70  STORE_FAST               'temp1'

 L. 130        72  LOAD_GLOBAL              any
               74  LOAD_FAST                'temp1'
               76  LOAD_FAST                'one'
               78  BINARY_SUBTRACT  
               80  LOAD_FAST                'zero'
               82  COMPARE_OP               !=
               84  CALL_FUNCTION_1       1  ''
               86  POP_JUMP_IF_FALSE_BACK    44  'to 44'

 L. 131        88  POP_TOP          
               90  BREAK_LOOP          112  'to 112'
               92  JUMP_BACK            44  'to 44'
             94_0  COME_FROM            44  '44'

 L. 133        94  LOAD_GLOBAL              RuntimeError
               96  LOAD_FAST                'msg'
               98  LOAD_FAST                '_'
              100  LOAD_FAST                'one'
              102  LOAD_ATTR                dtype
              104  BUILD_TUPLE_2         2 
              106  BINARY_MODULO    
              108  CALL_FUNCTION_1       1  ''
              110  RAISE_VARARGS_1       1  'exception instance'
            112_0  COME_FROM            90  '90'

 L. 134       112  LOAD_FAST                'one'
              114  STORE_FAST               'b'

 L. 135       116  LOAD_GLOBAL              range
              118  LOAD_FAST                'max_iterN'
              120  CALL_FUNCTION_1       1  ''
              122  GET_ITER         
            124_0  COME_FROM           172  '172'
            124_1  COME_FROM           166  '166'
              124  FOR_ITER            174  'to 174'
              126  STORE_FAST               '_'

 L. 136       128  LOAD_FAST                'b'
              130  LOAD_FAST                'b'
              132  BINARY_ADD       
              134  STORE_FAST               'b'

 L. 137       136  LOAD_FAST                'a'
              138  LOAD_FAST                'b'
              140  BINARY_ADD       
              142  STORE_FAST               'temp'

 L. 138       144  LOAD_FAST                'int_conv'
              146  LOAD_FAST                'temp'
              148  LOAD_FAST                'a'
              150  BINARY_SUBTRACT  
              152  CALL_FUNCTION_1       1  ''
              154  STORE_FAST               'itemp'

 L. 139       156  LOAD_GLOBAL              any
              158  LOAD_FAST                'itemp'
              160  LOAD_CONST               0
              162  COMPARE_OP               !=
              164  CALL_FUNCTION_1       1  ''
              166  POP_JUMP_IF_FALSE_BACK   124  'to 124'

 L. 140       168  POP_TOP          
              170  BREAK_LOOP          192  'to 192'
              172  JUMP_BACK           124  'to 124'
            174_0  COME_FROM           124  '124'

 L. 142       174  LOAD_GLOBAL              RuntimeError
              176  LOAD_FAST                'msg'
              178  LOAD_FAST                '_'
              180  LOAD_FAST                'one'
              182  LOAD_ATTR                dtype
              184  BUILD_TUPLE_2         2 
              186  BINARY_MODULO    
              188  CALL_FUNCTION_1       1  ''
              190  RAISE_VARARGS_1       1  'exception instance'
            192_0  COME_FROM           170  '170'

 L. 143       192  LOAD_FAST                'itemp'
              194  STORE_FAST               'ibeta'

 L. 144       196  LOAD_FAST                'float_conv'
              198  LOAD_FAST                'ibeta'
              200  CALL_FUNCTION_1       1  ''
              202  STORE_FAST               'beta'

 L. 147       204  LOAD_CONST               -1
              206  STORE_FAST               'it'

 L. 148       208  LOAD_FAST                'one'
              210  STORE_FAST               'b'

 L. 149       212  LOAD_GLOBAL              range
              214  LOAD_FAST                'max_iterN'
              216  CALL_FUNCTION_1       1  ''
              218  GET_ITER         
            220_0  COME_FROM           278  '278'
            220_1  COME_FROM           270  '270'
              220  FOR_ITER            280  'to 280'
              222  STORE_FAST               '_'

 L. 150       224  LOAD_FAST                'it'
              226  LOAD_CONST               1
              228  BINARY_ADD       
              230  STORE_FAST               'it'

 L. 151       232  LOAD_FAST                'b'
              234  LOAD_FAST                'beta'
              236  BINARY_MULTIPLY  
              238  STORE_FAST               'b'

 L. 152       240  LOAD_FAST                'b'
              242  LOAD_FAST                'one'
              244  BINARY_ADD       
              246  STORE_FAST               'temp'

 L. 153       248  LOAD_FAST                'temp'
              250  LOAD_FAST                'b'
              252  BINARY_SUBTRACT  
              254  STORE_FAST               'temp1'

 L. 154       256  LOAD_GLOBAL              any
              258  LOAD_FAST                'temp1'
              260  LOAD_FAST                'one'
              262  BINARY_SUBTRACT  
              264  LOAD_FAST                'zero'
              266  COMPARE_OP               !=
              268  CALL_FUNCTION_1       1  ''
              270  POP_JUMP_IF_FALSE_BACK   220  'to 220'

 L. 155       272  POP_TOP          
          274_276  BREAK_LOOP          298  'to 298'
              278  JUMP_BACK           220  'to 220'
            280_0  COME_FROM           220  '220'

 L. 157       280  LOAD_GLOBAL              RuntimeError
              282  LOAD_FAST                'msg'
              284  LOAD_FAST                '_'
              286  LOAD_FAST                'one'
              288  LOAD_ATTR                dtype
              290  BUILD_TUPLE_2         2 
              292  BINARY_MODULO    
              294  CALL_FUNCTION_1       1  ''
              296  RAISE_VARARGS_1       1  'exception instance'
            298_0  COME_FROM           274  '274'

 L. 159       298  LOAD_FAST                'beta'
              300  LOAD_FAST                'two'
              302  BINARY_TRUE_DIVIDE
              304  STORE_FAST               'betah'

 L. 160       306  LOAD_FAST                'one'
              308  STORE_FAST               'a'

 L. 161       310  LOAD_GLOBAL              range
              312  LOAD_FAST                'max_iterN'
              314  CALL_FUNCTION_1       1  ''
              316  GET_ITER         
            318_0  COME_FROM           370  '370'
            318_1  COME_FROM           360  '360'
              318  FOR_ITER            374  'to 374'
              320  STORE_FAST               '_'

 L. 162       322  LOAD_FAST                'a'
              324  LOAD_FAST                'a'
              326  BINARY_ADD       
              328  STORE_FAST               'a'

 L. 163       330  LOAD_FAST                'a'
              332  LOAD_FAST                'one'
              334  BINARY_ADD       
              336  STORE_FAST               'temp'

 L. 164       338  LOAD_FAST                'temp'
              340  LOAD_FAST                'a'
              342  BINARY_SUBTRACT  
              344  STORE_FAST               'temp1'

 L. 165       346  LOAD_GLOBAL              any
              348  LOAD_FAST                'temp1'
              350  LOAD_FAST                'one'
              352  BINARY_SUBTRACT  
              354  LOAD_FAST                'zero'
              356  COMPARE_OP               !=
              358  CALL_FUNCTION_1       1  ''
          360_362  POP_JUMP_IF_FALSE_BACK   318  'to 318'

 L. 166       364  POP_TOP          
          366_368  BREAK_LOOP          392  'to 392'
          370_372  JUMP_BACK           318  'to 318'
            374_0  COME_FROM           318  '318'

 L. 168       374  LOAD_GLOBAL              RuntimeError
              376  LOAD_FAST                'msg'
              378  LOAD_FAST                '_'
              380  LOAD_FAST                'one'
              382  LOAD_ATTR                dtype
              384  BUILD_TUPLE_2         2 
              386  BINARY_MODULO    
              388  CALL_FUNCTION_1       1  ''
              390  RAISE_VARARGS_1       1  'exception instance'
            392_0  COME_FROM           366  '366'

 L. 169       392  LOAD_FAST                'a'
              394  LOAD_FAST                'betah'
              396  BINARY_ADD       
              398  STORE_FAST               'temp'

 L. 170       400  LOAD_CONST               0
              402  STORE_FAST               'irnd'

 L. 171       404  LOAD_GLOBAL              any
              406  LOAD_FAST                'temp'
              408  LOAD_FAST                'a'
              410  BINARY_SUBTRACT  
              412  LOAD_FAST                'zero'
              414  COMPARE_OP               !=
              416  CALL_FUNCTION_1       1  ''
          418_420  POP_JUMP_IF_FALSE   426  'to 426'

 L. 172       422  LOAD_CONST               1
              424  STORE_FAST               'irnd'
            426_0  COME_FROM           418  '418'

 L. 173       426  LOAD_FAST                'a'
              428  LOAD_FAST                'beta'
              430  BINARY_ADD       
              432  STORE_FAST               'tempa'

 L. 174       434  LOAD_FAST                'tempa'
              436  LOAD_FAST                'betah'
              438  BINARY_ADD       
              440  STORE_FAST               'temp'

 L. 175       442  LOAD_FAST                'irnd'
              444  LOAD_CONST               0
              446  COMPARE_OP               ==
          448_450  POP_JUMP_IF_FALSE   474  'to 474'
              452  LOAD_GLOBAL              any
              454  LOAD_FAST                'temp'
              456  LOAD_FAST                'tempa'
              458  BINARY_SUBTRACT  
              460  LOAD_FAST                'zero'
              462  COMPARE_OP               !=
              464  CALL_FUNCTION_1       1  ''
          466_468  POP_JUMP_IF_FALSE   474  'to 474'

 L. 176       470  LOAD_CONST               2
              472  STORE_FAST               'irnd'
            474_0  COME_FROM           466  '466'
            474_1  COME_FROM           448  '448'

 L. 179       474  LOAD_FAST                'it'
              476  LOAD_CONST               3
              478  BINARY_ADD       
              480  STORE_FAST               'negep'

 L. 180       482  LOAD_FAST                'one'
              484  LOAD_FAST                'beta'
              486  BINARY_TRUE_DIVIDE
              488  STORE_FAST               'betain'

 L. 181       490  LOAD_FAST                'one'
              492  STORE_FAST               'a'

 L. 182       494  LOAD_GLOBAL              range
              496  LOAD_FAST                'negep'
              498  CALL_FUNCTION_1       1  ''
              500  GET_ITER         
            502_0  COME_FROM           514  '514'
              502  FOR_ITER            518  'to 518'
              504  STORE_FAST               'i'

 L. 183       506  LOAD_FAST                'a'
              508  LOAD_FAST                'betain'
              510  BINARY_MULTIPLY  
              512  STORE_FAST               'a'
          514_516  JUMP_BACK           502  'to 502'
            518_0  COME_FROM           502  '502'

 L. 184       518  LOAD_FAST                'a'
              520  STORE_FAST               'b'

 L. 185       522  LOAD_GLOBAL              range
              524  LOAD_FAST                'max_iterN'
              526  CALL_FUNCTION_1       1  ''
              528  GET_ITER         
            530_0  COME_FROM           606  '606'
            530_1  COME_FROM           588  '588'
              530  FOR_ITER            610  'to 610'
              532  STORE_FAST               '_'

 L. 186       534  LOAD_FAST                'one'
              536  LOAD_FAST                'a'
              538  BINARY_SUBTRACT  
              540  STORE_FAST               'temp'

 L. 187       542  LOAD_GLOBAL              any
              544  LOAD_FAST                'temp'
              546  LOAD_FAST                'one'
              548  BINARY_SUBTRACT  
              550  LOAD_FAST                'zero'
              552  COMPARE_OP               !=
              554  CALL_FUNCTION_1       1  ''
          556_558  POP_JUMP_IF_FALSE   566  'to 566'

 L. 188       560  POP_TOP          
          562_564  BREAK_LOOP          628  'to 628'
            566_0  COME_FROM           556  '556'

 L. 189       566  LOAD_FAST                'a'
              568  LOAD_FAST                'beta'
              570  BINARY_MULTIPLY  
              572  STORE_FAST               'a'

 L. 190       574  LOAD_FAST                'negep'
              576  LOAD_CONST               1
              578  BINARY_SUBTRACT  
              580  STORE_FAST               'negep'

 L. 192       582  LOAD_FAST                'negep'
              584  LOAD_CONST               0
              586  COMPARE_OP               <
          588_590  POP_JUMP_IF_FALSE_BACK   530  'to 530'

 L. 193       592  LOAD_GLOBAL              RuntimeError
              594  LOAD_STR                 "could not determine machine tolerance for 'negep', locals() -> %s"

 L. 194       596  LOAD_GLOBAL              locals
              598  CALL_FUNCTION_0       0  ''

 L. 193       600  BINARY_MODULO    
              602  CALL_FUNCTION_1       1  ''
              604  RAISE_VARARGS_1       1  'exception instance'
          606_608  JUMP_BACK           530  'to 530'
            610_0  COME_FROM           530  '530'

 L. 196       610  LOAD_GLOBAL              RuntimeError
              612  LOAD_FAST                'msg'
              614  LOAD_FAST                '_'
              616  LOAD_FAST                'one'
              618  LOAD_ATTR                dtype
              620  BUILD_TUPLE_2         2 
              622  BINARY_MODULO    
              624  CALL_FUNCTION_1       1  ''
              626  RAISE_VARARGS_1       1  'exception instance'
            628_0  COME_FROM           562  '562'

 L. 197       628  LOAD_FAST                'negep'
              630  UNARY_NEGATIVE   
              632  STORE_FAST               'negep'

 L. 198       634  LOAD_FAST                'a'
              636  STORE_FAST               'epsneg'

 L. 201       638  LOAD_FAST                'it'
              640  UNARY_NEGATIVE   
              642  LOAD_CONST               3
              644  BINARY_SUBTRACT  
              646  STORE_FAST               'machep'

 L. 202       648  LOAD_FAST                'b'
              650  STORE_FAST               'a'

 L. 204       652  LOAD_GLOBAL              range
              654  LOAD_FAST                'max_iterN'
              656  CALL_FUNCTION_1       1  ''
              658  GET_ITER         
            660_0  COME_FROM           712  '712'
              660  FOR_ITER            716  'to 716'
              662  STORE_FAST               '_'

 L. 205       664  LOAD_FAST                'one'
              666  LOAD_FAST                'a'
              668  BINARY_ADD       
              670  STORE_FAST               'temp'

 L. 206       672  LOAD_GLOBAL              any
              674  LOAD_FAST                'temp'
              676  LOAD_FAST                'one'
              678  BINARY_SUBTRACT  
              680  LOAD_FAST                'zero'
              682  COMPARE_OP               !=
              684  CALL_FUNCTION_1       1  ''
          686_688  POP_JUMP_IF_FALSE   696  'to 696'

 L. 207       690  POP_TOP          
          692_694  BREAK_LOOP          734  'to 734'
            696_0  COME_FROM           686  '686'

 L. 208       696  LOAD_FAST                'a'
              698  LOAD_FAST                'beta'
              700  BINARY_MULTIPLY  
              702  STORE_FAST               'a'

 L. 209       704  LOAD_FAST                'machep'
              706  LOAD_CONST               1
              708  BINARY_ADD       
              710  STORE_FAST               'machep'
          712_714  JUMP_BACK           660  'to 660'
            716_0  COME_FROM           660  '660'

 L. 211       716  LOAD_GLOBAL              RuntimeError
              718  LOAD_FAST                'msg'
              720  LOAD_FAST                '_'
              722  LOAD_FAST                'one'
              724  LOAD_ATTR                dtype
              726  BUILD_TUPLE_2         2 
              728  BINARY_MODULO    
              730  CALL_FUNCTION_1       1  ''
              732  RAISE_VARARGS_1       1  'exception instance'
            734_0  COME_FROM           692  '692'

 L. 212       734  LOAD_FAST                'a'
              736  STORE_FAST               'eps'

 L. 215       738  LOAD_CONST               0
              740  STORE_FAST               'ngrd'

 L. 216       742  LOAD_FAST                'one'
              744  LOAD_FAST                'eps'
              746  BINARY_ADD       
              748  STORE_FAST               'temp'

 L. 217       750  LOAD_FAST                'irnd'
              752  LOAD_CONST               0
              754  COMPARE_OP               ==
          756_758  POP_JUMP_IF_FALSE   786  'to 786'
              760  LOAD_GLOBAL              any
              762  LOAD_FAST                'temp'
              764  LOAD_FAST                'one'
              766  BINARY_MULTIPLY  
              768  LOAD_FAST                'one'
              770  BINARY_SUBTRACT  
              772  LOAD_FAST                'zero'
              774  COMPARE_OP               !=
              776  CALL_FUNCTION_1       1  ''
          778_780  POP_JUMP_IF_FALSE   786  'to 786'

 L. 218       782  LOAD_CONST               1
              784  STORE_FAST               'ngrd'
            786_0  COME_FROM           778  '778'
            786_1  COME_FROM           756  '756'

 L. 221       786  LOAD_CONST               0
              788  STORE_FAST               'i'

 L. 222       790  LOAD_CONST               1
              792  STORE_FAST               'k'

 L. 223       794  LOAD_FAST                'betain'
              796  STORE_FAST               'z'

 L. 224       798  LOAD_FAST                'one'
              800  LOAD_FAST                'eps'
              802  BINARY_ADD       
              804  STORE_FAST               't'

 L. 225       806  LOAD_CONST               0
              808  STORE_FAST               'nxres'

 L. 226       810  LOAD_GLOBAL              range
              812  LOAD_FAST                'max_iterN'
              814  CALL_FUNCTION_1       1  ''
              816  GET_ITER         
            818_0  COME_FROM           940  '940'
              818  FOR_ITER            944  'to 944'
              820  STORE_FAST               '_'

 L. 227       822  LOAD_FAST                'z'
              824  STORE_FAST               'y'

 L. 228       826  LOAD_FAST                'y'
              828  LOAD_FAST                'y'
              830  BINARY_MULTIPLY  
              832  STORE_FAST               'z'

 L. 229       834  LOAD_FAST                'z'
              836  LOAD_FAST                'one'
              838  BINARY_MULTIPLY  
              840  STORE_FAST               'a'

 L. 230       842  LOAD_FAST                'z'
              844  LOAD_FAST                't'
              846  BINARY_MULTIPLY  
              848  STORE_FAST               'temp'

 L. 231       850  LOAD_GLOBAL              any
              852  LOAD_FAST                'a'
              854  LOAD_FAST                'a'
              856  BINARY_ADD       
              858  LOAD_FAST                'zero'
              860  COMPARE_OP               ==
              862  CALL_FUNCTION_1       1  ''
          864_866  POP_JUMP_IF_TRUE    886  'to 886'
              868  LOAD_GLOBAL              any
              870  LOAD_GLOBAL              abs
              872  LOAD_FAST                'z'
              874  CALL_FUNCTION_1       1  ''
              876  LOAD_FAST                'y'
              878  COMPARE_OP               >=
              880  CALL_FUNCTION_1       1  ''
          882_884  POP_JUMP_IF_FALSE   892  'to 892'
            886_0  COME_FROM           864  '864'

 L. 232       886  POP_TOP          
          888_890  BREAK_LOOP          962  'to 962'
            892_0  COME_FROM           882  '882'

 L. 233       892  LOAD_FAST                'temp'
              894  LOAD_FAST                'betain'
              896  BINARY_MULTIPLY  
              898  STORE_FAST               'temp1'

 L. 234       900  LOAD_GLOBAL              any
              902  LOAD_FAST                'temp1'
              904  LOAD_FAST                'beta'
              906  BINARY_MULTIPLY  
              908  LOAD_FAST                'z'
              910  COMPARE_OP               ==
              912  CALL_FUNCTION_1       1  ''
          914_916  POP_JUMP_IF_FALSE   924  'to 924'

 L. 235       918  POP_TOP          
          920_922  BREAK_LOOP          962  'to 962'
            924_0  COME_FROM           914  '914'

 L. 236       924  LOAD_FAST                'i'
              926  LOAD_CONST               1
              928  BINARY_ADD       
              930  STORE_FAST               'i'

 L. 237       932  LOAD_FAST                'k'
              934  LOAD_FAST                'k'
              936  BINARY_ADD       
              938  STORE_FAST               'k'
          940_942  JUMP_BACK           818  'to 818'
            944_0  COME_FROM           818  '818'

 L. 239       944  LOAD_GLOBAL              RuntimeError
              946  LOAD_FAST                'msg'
              948  LOAD_FAST                '_'
              950  LOAD_FAST                'one'
              952  LOAD_ATTR                dtype
              954  BUILD_TUPLE_2         2 
              956  BINARY_MODULO    
              958  CALL_FUNCTION_1       1  ''
              960  RAISE_VARARGS_1       1  'exception instance'
            962_0  COME_FROM           920  '920'
            962_1  COME_FROM           888  '888'

 L. 240       962  LOAD_FAST                'ibeta'
              964  LOAD_CONST               10
              966  COMPARE_OP               !=
          968_970  POP_JUMP_IF_FALSE   990  'to 990'

 L. 241       972  LOAD_FAST                'i'
              974  LOAD_CONST               1
              976  BINARY_ADD       
              978  STORE_FAST               'iexp'

 L. 242       980  LOAD_FAST                'k'
              982  LOAD_FAST                'k'
              984  BINARY_ADD       
              986  STORE_FAST               'mx'
              988  JUMP_FORWARD       1040  'to 1040'
            990_0  COME_FROM           968  '968'

 L. 244       990  LOAD_CONST               2
              992  STORE_FAST               'iexp'

 L. 245       994  LOAD_FAST                'ibeta'
              996  STORE_FAST               'iz'
            998_0  COME_FROM          1024  '1024'

 L. 246       998  LOAD_FAST                'k'
             1000  LOAD_FAST                'iz'
             1002  COMPARE_OP               >=
         1004_1006  POP_JUMP_IF_FALSE  1028  'to 1028'

 L. 247      1008  LOAD_FAST                'iz'
             1010  LOAD_FAST                'ibeta'
             1012  BINARY_MULTIPLY  
             1014  STORE_FAST               'iz'

 L. 248      1016  LOAD_FAST                'iexp'
             1018  LOAD_CONST               1
             1020  BINARY_ADD       
             1022  STORE_FAST               'iexp'
         1024_1026  JUMP_BACK           998  'to 998'
           1028_0  COME_FROM          1004  '1004'

 L. 249      1028  LOAD_FAST                'iz'
             1030  LOAD_FAST                'iz'
             1032  BINARY_ADD       
             1034  LOAD_CONST               1
             1036  BINARY_SUBTRACT  
             1038  STORE_FAST               'mx'
           1040_0  COME_FROM           988  '988'

 L. 252      1040  LOAD_GLOBAL              range
             1042  LOAD_FAST                'max_iterN'
             1044  CALL_FUNCTION_1       1  ''
             1046  GET_ITER         
           1048_0  COME_FROM          1186  '1186'
           1048_1  COME_FROM          1178  '1178'
             1048  FOR_ITER           1190  'to 1190'
             1050  STORE_FAST               '_'

 L. 253      1052  LOAD_FAST                'y'
             1054  STORE_FAST               'xmin'

 L. 254      1056  LOAD_FAST                'y'
             1058  LOAD_FAST                'betain'
             1060  BINARY_MULTIPLY  
             1062  STORE_FAST               'y'

 L. 255      1064  LOAD_FAST                'y'
             1066  LOAD_FAST                'one'
             1068  BINARY_MULTIPLY  
             1070  STORE_FAST               'a'

 L. 256      1072  LOAD_FAST                'y'
             1074  LOAD_FAST                't'
             1076  BINARY_MULTIPLY  
             1078  STORE_FAST               'temp'

 L. 257      1080  LOAD_GLOBAL              any
             1082  LOAD_FAST                'a'
             1084  LOAD_FAST                'a'
             1086  BINARY_ADD       
             1088  LOAD_FAST                'zero'
             1090  COMPARE_OP               !=
             1092  CALL_FUNCTION_1       1  ''
         1094_1096  POP_JUMP_IF_FALSE  1180  'to 1180'
             1098  LOAD_GLOBAL              any
             1100  LOAD_GLOBAL              abs
             1102  LOAD_FAST                'y'
             1104  CALL_FUNCTION_1       1  ''
             1106  LOAD_FAST                'xmin'
             1108  COMPARE_OP               <
             1110  CALL_FUNCTION_1       1  ''
         1112_1114  POP_JUMP_IF_FALSE  1180  'to 1180'

 L. 258      1116  LOAD_FAST                'k'
             1118  LOAD_CONST               1
             1120  BINARY_ADD       
             1122  STORE_FAST               'k'

 L. 259      1124  LOAD_FAST                'temp'
             1126  LOAD_FAST                'betain'
             1128  BINARY_MULTIPLY  
             1130  STORE_FAST               'temp1'

 L. 260      1132  LOAD_GLOBAL              any
             1134  LOAD_FAST                'temp1'
             1136  LOAD_FAST                'beta'
             1138  BINARY_MULTIPLY  
             1140  LOAD_FAST                'y'
             1142  COMPARE_OP               ==
             1144  CALL_FUNCTION_1       1  ''
         1146_1148  POP_JUMP_IF_FALSE  1186  'to 1186'
             1150  LOAD_GLOBAL              any
             1152  LOAD_FAST                'temp'
             1154  LOAD_FAST                'y'
             1156  COMPARE_OP               !=
             1158  CALL_FUNCTION_1       1  ''
         1160_1162  POP_JUMP_IF_FALSE  1186  'to 1186'

 L. 261      1164  LOAD_CONST               3
             1166  STORE_FAST               'nxres'

 L. 262      1168  LOAD_FAST                'y'
             1170  STORE_FAST               'xmin'

 L. 263      1172  POP_TOP          
         1174_1176  BREAK_LOOP         1208  'to 1208'
             1178  JUMP_BACK          1048  'to 1048'
           1180_0  COME_FROM          1112  '1112'
           1180_1  COME_FROM          1094  '1094'

 L. 265      1180  POP_TOP          
         1182_1184  BREAK_LOOP         1208  'to 1208'
           1186_0  COME_FROM          1160  '1160'
           1186_1  COME_FROM          1146  '1146'
         1186_1188  JUMP_BACK          1048  'to 1048'
           1190_0  COME_FROM          1048  '1048'

 L. 267      1190  LOAD_GLOBAL              RuntimeError
             1192  LOAD_FAST                'msg'
             1194  LOAD_FAST                '_'
             1196  LOAD_FAST                'one'
             1198  LOAD_ATTR                dtype
             1200  BUILD_TUPLE_2         2 
             1202  BINARY_MODULO    
             1204  CALL_FUNCTION_1       1  ''
             1206  RAISE_VARARGS_1       1  'exception instance'
           1208_0  COME_FROM          1182  '1182'
           1208_1  COME_FROM          1174  '1174'

 L. 268      1208  LOAD_FAST                'k'
             1210  UNARY_NEGATIVE   
             1212  STORE_FAST               'minexp'

 L. 271      1214  LOAD_FAST                'mx'
             1216  LOAD_FAST                'k'
             1218  LOAD_FAST                'k'
             1220  BINARY_ADD       
             1222  LOAD_CONST               3
             1224  BINARY_SUBTRACT  
             1226  COMPARE_OP               <=
         1228_1230  POP_JUMP_IF_FALSE  1258  'to 1258'
             1232  LOAD_FAST                'ibeta'
             1234  LOAD_CONST               10
             1236  COMPARE_OP               !=
         1238_1240  POP_JUMP_IF_FALSE  1258  'to 1258'

 L. 272      1242  LOAD_FAST                'mx'
             1244  LOAD_FAST                'mx'
             1246  BINARY_ADD       
             1248  STORE_FAST               'mx'

 L. 273      1250  LOAD_FAST                'iexp'
             1252  LOAD_CONST               1
             1254  BINARY_ADD       
             1256  STORE_FAST               'iexp'
           1258_0  COME_FROM          1238  '1238'
           1258_1  COME_FROM          1228  '1228'

 L. 274      1258  LOAD_FAST                'mx'
             1260  LOAD_FAST                'minexp'
             1262  BINARY_ADD       
             1264  STORE_FAST               'maxexp'

 L. 275      1266  LOAD_FAST                'irnd'
             1268  LOAD_FAST                'nxres'
             1270  BINARY_ADD       
             1272  STORE_FAST               'irnd'

 L. 276      1274  LOAD_FAST                'irnd'
             1276  LOAD_CONST               2
             1278  COMPARE_OP               >=
         1280_1282  POP_JUMP_IF_FALSE  1292  'to 1292'

 L. 277      1284  LOAD_FAST                'maxexp'
             1286  LOAD_CONST               2
             1288  BINARY_SUBTRACT  
             1290  STORE_FAST               'maxexp'
           1292_0  COME_FROM          1280  '1280'

 L. 278      1292  LOAD_FAST                'maxexp'
             1294  LOAD_FAST                'minexp'
             1296  BINARY_ADD       
             1298  STORE_FAST               'i'

 L. 279      1300  LOAD_FAST                'ibeta'
             1302  LOAD_CONST               2
             1304  COMPARE_OP               ==
         1306_1308  POP_JUMP_IF_FALSE  1324  'to 1324'
             1310  LOAD_FAST                'i'
         1312_1314  POP_JUMP_IF_TRUE   1324  'to 1324'

 L. 280      1316  LOAD_FAST                'maxexp'
             1318  LOAD_CONST               1
             1320  BINARY_SUBTRACT  
             1322  STORE_FAST               'maxexp'
           1324_0  COME_FROM          1312  '1312'
           1324_1  COME_FROM          1306  '1306'

 L. 281      1324  LOAD_FAST                'i'
             1326  LOAD_CONST               20
             1328  COMPARE_OP               >
         1330_1332  POP_JUMP_IF_FALSE  1342  'to 1342'

 L. 282      1334  LOAD_FAST                'maxexp'
             1336  LOAD_CONST               1
             1338  BINARY_SUBTRACT  
             1340  STORE_FAST               'maxexp'
           1342_0  COME_FROM          1330  '1330'

 L. 283      1342  LOAD_GLOBAL              any
             1344  LOAD_FAST                'a'
             1346  LOAD_FAST                'y'
             1348  COMPARE_OP               !=
             1350  CALL_FUNCTION_1       1  ''
         1352_1354  POP_JUMP_IF_FALSE  1364  'to 1364'

 L. 284      1356  LOAD_FAST                'maxexp'
             1358  LOAD_CONST               2
             1360  BINARY_SUBTRACT  
             1362  STORE_FAST               'maxexp'
           1364_0  COME_FROM          1352  '1352'

 L. 285      1364  LOAD_FAST                'one'
             1366  LOAD_FAST                'epsneg'
             1368  BINARY_SUBTRACT  
             1370  STORE_FAST               'xmax'

 L. 286      1372  LOAD_GLOBAL              any
             1374  LOAD_FAST                'xmax'
             1376  LOAD_FAST                'one'
             1378  BINARY_MULTIPLY  
             1380  LOAD_FAST                'xmax'
             1382  COMPARE_OP               !=
             1384  CALL_FUNCTION_1       1  ''
         1386_1388  POP_JUMP_IF_FALSE  1402  'to 1402'

 L. 287      1390  LOAD_FAST                'one'
             1392  LOAD_FAST                'beta'
             1394  LOAD_FAST                'epsneg'
             1396  BINARY_MULTIPLY  
             1398  BINARY_SUBTRACT  
             1400  STORE_FAST               'xmax'
           1402_0  COME_FROM          1386  '1386'

 L. 288      1402  LOAD_FAST                'xmax'
             1404  LOAD_FAST                'xmin'
             1406  LOAD_FAST                'beta'
             1408  BINARY_MULTIPLY  
             1410  LOAD_FAST                'beta'
             1412  BINARY_MULTIPLY  
             1414  LOAD_FAST                'beta'
             1416  BINARY_MULTIPLY  
             1418  BINARY_TRUE_DIVIDE
             1420  STORE_FAST               'xmax'

 L. 289      1422  LOAD_FAST                'maxexp'
             1424  LOAD_FAST                'minexp'
             1426  BINARY_ADD       
             1428  LOAD_CONST               3
             1430  BINARY_ADD       
             1432  STORE_FAST               'i'

 L. 290      1434  LOAD_GLOBAL              range
             1436  LOAD_FAST                'i'
             1438  CALL_FUNCTION_1       1  ''
             1440  GET_ITER         
           1442_0  COME_FROM          1474  '1474'
           1442_1  COME_FROM          1464  '1464'
             1442  FOR_ITER           1478  'to 1478'
             1444  STORE_FAST               'j'

 L. 291      1446  LOAD_FAST                'ibeta'
             1448  LOAD_CONST               2
             1450  COMPARE_OP               ==
         1452_1454  POP_JUMP_IF_FALSE  1466  'to 1466'

 L. 292      1456  LOAD_FAST                'xmax'
             1458  LOAD_FAST                'xmax'
             1460  BINARY_ADD       
             1462  STORE_FAST               'xmax'
             1464  JUMP_BACK          1442  'to 1442'
           1466_0  COME_FROM          1452  '1452'

 L. 294      1466  LOAD_FAST                'xmax'
             1468  LOAD_FAST                'beta'
             1470  BINARY_MULTIPLY  
             1472  STORE_FAST               'xmax'
         1474_1476  JUMP_BACK          1442  'to 1442'
           1478_0  COME_FROM          1442  '1442'

 L. 296      1478  LOAD_FAST                'ibeta'
             1480  LOAD_FAST                'self'
             1482  STORE_ATTR               ibeta

 L. 297      1484  LOAD_FAST                'it'
             1486  LOAD_FAST                'self'
             1488  STORE_ATTR               it

 L. 298      1490  LOAD_FAST                'negep'
             1492  LOAD_FAST                'self'
             1494  STORE_ATTR               negep

 L. 299      1496  LOAD_FAST                'float_to_float'
             1498  LOAD_FAST                'epsneg'
             1500  CALL_FUNCTION_1       1  ''
             1502  LOAD_FAST                'self'
             1504  STORE_ATTR               epsneg

 L. 300      1506  LOAD_FAST                'float_to_str'
             1508  LOAD_FAST                'epsneg'
             1510  CALL_FUNCTION_1       1  ''
             1512  LOAD_FAST                'self'
             1514  STORE_ATTR               _str_epsneg

 L. 301      1516  LOAD_FAST                'machep'
             1518  LOAD_FAST                'self'
             1520  STORE_ATTR               machep

 L. 302      1522  LOAD_FAST                'float_to_float'
             1524  LOAD_FAST                'eps'
             1526  CALL_FUNCTION_1       1  ''
             1528  LOAD_FAST                'self'
             1530  STORE_ATTR               eps

 L. 303      1532  LOAD_FAST                'float_to_str'
             1534  LOAD_FAST                'eps'
             1536  CALL_FUNCTION_1       1  ''
             1538  LOAD_FAST                'self'
             1540  STORE_ATTR               _str_eps

 L. 304      1542  LOAD_FAST                'ngrd'
             1544  LOAD_FAST                'self'
             1546  STORE_ATTR               ngrd

 L. 305      1548  LOAD_FAST                'iexp'
             1550  LOAD_FAST                'self'
             1552  STORE_ATTR               iexp

 L. 306      1554  LOAD_FAST                'minexp'
             1556  LOAD_FAST                'self'
             1558  STORE_ATTR               minexp

 L. 307      1560  LOAD_FAST                'float_to_float'
             1562  LOAD_FAST                'xmin'
             1564  CALL_FUNCTION_1       1  ''
             1566  LOAD_FAST                'self'
             1568  STORE_ATTR               xmin

 L. 308      1570  LOAD_FAST                'float_to_str'
             1572  LOAD_FAST                'xmin'
             1574  CALL_FUNCTION_1       1  ''
             1576  LOAD_FAST                'self'
             1578  STORE_ATTR               _str_xmin

 L. 309      1580  LOAD_FAST                'maxexp'
             1582  LOAD_FAST                'self'
             1584  STORE_ATTR               maxexp

 L. 310      1586  LOAD_FAST                'float_to_float'
             1588  LOAD_FAST                'xmax'
             1590  CALL_FUNCTION_1       1  ''
             1592  LOAD_FAST                'self'
             1594  STORE_ATTR               xmax

 L. 311      1596  LOAD_FAST                'float_to_str'
             1598  LOAD_FAST                'xmax'
             1600  CALL_FUNCTION_1       1  ''
             1602  LOAD_FAST                'self'
             1604  STORE_ATTR               _str_xmax

 L. 312      1606  LOAD_FAST                'irnd'
             1608  LOAD_FAST                'self'
             1610  STORE_ATTR               irnd

 L. 314      1612  LOAD_FAST                'title'
             1614  LOAD_FAST                'self'
             1616  STORE_ATTR               title

 L. 316      1618  LOAD_FAST                'self'
             1620  LOAD_ATTR                eps
             1622  LOAD_FAST                'self'
             1624  STORE_ATTR               epsilon

 L. 317      1626  LOAD_FAST                'self'
             1628  LOAD_ATTR                xmin
             1630  LOAD_FAST                'self'
             1632  STORE_ATTR               tiny

 L. 318      1634  LOAD_FAST                'self'
             1636  LOAD_ATTR                xmax
             1638  LOAD_FAST                'self'
             1640  STORE_ATTR               huge

 L. 320      1642  LOAD_CONST               0
             1644  LOAD_CONST               None
             1646  IMPORT_NAME              math
             1648  STORE_FAST               'math'

 L. 321      1650  LOAD_GLOBAL              int
             1652  LOAD_FAST                'math'
             1654  LOAD_METHOD              log10
             1656  LOAD_FAST                'float_to_float'
             1658  LOAD_FAST                'self'
             1660  LOAD_ATTR                eps
             1662  CALL_FUNCTION_1       1  ''
             1664  CALL_METHOD_1         1  ''
             1666  UNARY_NEGATIVE   
             1668  CALL_FUNCTION_1       1  ''
             1670  LOAD_FAST                'self'
             1672  STORE_ATTR               precision

 L. 322      1674  LOAD_FAST                'two'
             1676  LOAD_FAST                'two'
             1678  BINARY_ADD       
             1680  LOAD_FAST                'two'
             1682  BINARY_ADD       
             1684  LOAD_FAST                'two'
             1686  BINARY_ADD       
             1688  LOAD_FAST                'two'
             1690  BINARY_ADD       
             1692  STORE_FAST               'ten'

 L. 323      1694  LOAD_FAST                'ten'
             1696  LOAD_FAST                'self'
             1698  LOAD_ATTR                precision
             1700  UNARY_NEGATIVE   
             1702  BINARY_POWER     
             1704  STORE_FAST               'resolution'

 L. 324      1706  LOAD_FAST                'float_to_float'
             1708  LOAD_FAST                'resolution'
             1710  CALL_FUNCTION_1       1  ''
             1712  LOAD_FAST                'self'
             1714  STORE_ATTR               resolution

 L. 325      1716  LOAD_FAST                'float_to_str'
             1718  LOAD_FAST                'resolution'
             1720  CALL_FUNCTION_1       1  ''
             1722  LOAD_FAST                'self'
             1724  STORE_ATTR               _str_resolution

Parse error at or near `LOAD_FAST' instruction at offset 1722

    def __str__(self):
        fmt = 'Machine parameters for %(title)s\n---------------------------------------------------------------------\nibeta=%(ibeta)s it=%(it)s iexp=%(iexp)s ngrd=%(ngrd)s irnd=%(irnd)s\nmachep=%(machep)s     eps=%(_str_eps)s (beta**machep == epsilon)\nnegep =%(negep)s  epsneg=%(_str_epsneg)s (beta**epsneg)\nminexp=%(minexp)s   xmin=%(_str_xmin)s (beta**minexp == tiny)\nmaxexp=%(maxexp)s    xmax=%(_str_xmax)s ((1-epsneg)*beta**maxexp == huge)\n---------------------------------------------------------------------\n'
        return fmt % self.__dict__


if __name__ == '__main__':
    print(MachAr())