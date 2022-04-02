# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\Crypto\PublicKey\_RSA.py
__revision__ = '$Id$'
from Crypto.PublicKey import pubkey
from Crypto.Util import number

def generate_py--- This code section failed: ---

 L.  39         0  LOAD_GLOBAL           0  'RSAobj'
                3  CALL_FUNCTION_0       0  None
                6  STORE_FAST            4  'obj'

 L.  40         9  LOAD_GLOBAL           1  'long'
               12  LOAD_FAST             3  'e'
               15  CALL_FUNCTION_1       1  None
               18  LOAD_FAST             4  'obj'
               21  STORE_ATTR            2  'e'

 L.  43        24  LOAD_FAST             2  'progress_func'
               27  POP_JUMP_IF_FALSE    43  'to 43'

 L.  44        30  LOAD_FAST             2  'progress_func'
               33  LOAD_CONST               'p,q\n'
               36  CALL_FUNCTION_1       1  None
               39  POP_TOP          
               40  JUMP_FORWARD          0  'to 43'
             43_0  COME_FROM            40  '40'

 L.  45        43  LOAD_CONST               1
               46  DUP_TOP          
               47  STORE_FAST            5  'p'
               50  STORE_FAST            6  'q'

 L.  46        53  SETUP_LOOP           95  'to 151'
               56  LOAD_GLOBAL           3  'number'
               59  LOAD_ATTR             4  'size'
               62  LOAD_FAST             5  'p'
               65  LOAD_FAST             6  'q'
               68  BINARY_MULTIPLY  
               69  CALL_FUNCTION_1       1  None
               72  LOAD_FAST             0  'bits'
               75  COMPARE_OP            0  <
               78  POP_JUMP_IF_FALSE   150  'to 150'

 L.  50        81  LOAD_GLOBAL           5  'pubkey'
               84  LOAD_ATTR             6  'getStrongPrime'
               87  LOAD_FAST             0  'bits'
               90  LOAD_CONST               1
               93  BINARY_RSHIFT    
               94  LOAD_FAST             4  'obj'
               97  LOAD_ATTR             2  'e'
              100  LOAD_CONST               1e-12
              103  LOAD_FAST             1  'randfunc'
              106  CALL_FUNCTION_4       4  None
              109  STORE_FAST            5  'p'

 L.  51       112  LOAD_GLOBAL           5  'pubkey'
              115  LOAD_ATTR             6  'getStrongPrime'
              118  LOAD_FAST             0  'bits'
              121  LOAD_FAST             0  'bits'
              124  LOAD_CONST               1
              127  BINARY_RSHIFT    
              128  BINARY_SUBTRACT  
              129  LOAD_FAST             4  'obj'
              132  LOAD_ATTR             2  'e'
              135  LOAD_CONST               1e-12
              138  LOAD_FAST             1  'randfunc'
              141  CALL_FUNCTION_4       4  None
              144  STORE_FAST            6  'q'
              147  JUMP_BACK            56  'to 56'
              150  POP_BLOCK        
            151_0  COME_FROM            53  '53'

 L.  56       151  LOAD_FAST             5  'p'
              154  LOAD_FAST             6  'q'
              157  COMPARE_OP            4  >
              160  POP_JUMP_IF_FALSE   179  'to 179'

 L.  57       163  LOAD_FAST             6  'q'
              166  LOAD_FAST             5  'p'
              169  ROT_TWO          
              170  STORE_FAST            5  'p'
              173  STORE_FAST            6  'q'
              176  JUMP_FORWARD          0  'to 179'
            179_0  COME_FROM           176  '176'

 L.  58       179  LOAD_FAST             5  'p'
              182  LOAD_FAST             4  'obj'
              185  STORE_ATTR            7  'p'

 L.  59       188  LOAD_FAST             6  'q'
              191  LOAD_FAST             4  'obj'
              194  STORE_ATTR            8  'q'

 L.  61       197  LOAD_FAST             2  'progress_func'
              200  POP_JUMP_IF_FALSE   216  'to 216'

 L.  62       203  LOAD_FAST             2  'progress_func'
              206  LOAD_CONST               'u\n'
              209  CALL_FUNCTION_1       1  None
              212  POP_TOP          
              213  JUMP_FORWARD          0  'to 216'
            216_0  COME_FROM           213  '213'

 L.  63       216  LOAD_GLOBAL           5  'pubkey'
              219  LOAD_ATTR             9  'inverse'
              222  LOAD_FAST             4  'obj'
              225  LOAD_ATTR             7  'p'
              228  LOAD_FAST             4  'obj'
              231  LOAD_ATTR             8  'q'
              234  CALL_FUNCTION_2       2  None
              237  LOAD_FAST             4  'obj'
              240  STORE_ATTR           10  'u'

 L.  64       243  LOAD_FAST             4  'obj'
              246  LOAD_ATTR             7  'p'
              249  LOAD_FAST             4  'obj'
              252  LOAD_ATTR             8  'q'
              255  BINARY_MULTIPLY  
              256  LOAD_FAST             4  'obj'
              259  STORE_ATTR           11  'n'

 L.  66       262  LOAD_FAST             2  'progress_func'
              265  POP_JUMP_IF_FALSE   281  'to 281'

 L.  67       268  LOAD_FAST             2  'progress_func'
              271  LOAD_CONST               'd\n'
              274  CALL_FUNCTION_1       1  None
              277  POP_TOP          
              278  JUMP_FORWARD          0  'to 281'
            281_0  COME_FROM           278  '278'

 L.  68       281  LOAD_GLOBAL           5  'pubkey'
              284  LOAD_ATTR             9  'inverse'
              287  LOAD_FAST             4  'obj'
              290  LOAD_ATTR             2  'e'
              293  LOAD_FAST             4  'obj'
              296  LOAD_ATTR             7  'p'
              299  LOAD_CONST               1
              302  BINARY_SUBTRACT  
              303  LOAD_FAST             4  'obj'
              306  LOAD_ATTR             8  'q'
              309  LOAD_CONST               1
              312  BINARY_SUBTRACT  
              313  BINARY_MULTIPLY  
              314  CALL_FUNCTION_2       2  None
              317  LOAD_FAST             4  'obj'
              320  STORE_ATTR           12  'd'

 L.  70       323  LOAD_FAST             0  'bits'
              326  LOAD_CONST               1
              329  LOAD_FAST             4  'obj'
              332  LOAD_ATTR             4  'size'
              335  CALL_FUNCTION_0       0  None
              338  BINARY_ADD       
              339  COMPARE_OP            1  <=
              342  POP_JUMP_IF_TRUE    354  'to 354'
              345  LOAD_ASSERT              AssertionError
              348  LOAD_CONST               'Generated key is too small'
              351  RAISE_VARARGS_2       2  None

 L.  72       354  LOAD_FAST             4  'obj'
              357  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 357


class RSAobj(pubkey.pubkey):

    def size(self):
        """size() : int
        Return the maximum number of bits that can be handled by this key.
        """
        return number.size(self.n) - 1