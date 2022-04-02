# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Hash\CMAC.py
from binascii import unhexlify
from Crypto.Hash import BLAKE2s
import Crypto.Util.strxor as strxor
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.py3compat import bord, tobytes, _copy_bytes
from Crypto.Random import get_random_bytes
digest_size = None

def _shift_bytes(bs, xor_lsb=0):
    num = bytes_to_long(bs) << 1 ^ xor_lsb
    return long_to_bytes(num, len(bs))[-len(bs):]


class CMAC(object):
    __doc__ = 'A CMAC hash object.\n    Do not instantiate directly. Use the :func:`new` function.\n\n    :ivar digest_size: the size in bytes of the resulting MAC tag\n    :vartype digest_size: integer\n    '
    digest_size = None

    def __init__--- This code section failed: ---

 L.  54         0  LOAD_FAST                'mac_len'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               digest_size

 L.  56         6  LOAD_GLOBAL              _copy_bytes
                8  LOAD_CONST               None
               10  LOAD_CONST               None
               12  LOAD_FAST                'key'
               14  CALL_FUNCTION_3       3  ''
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _key

 L.  57        20  LOAD_FAST                'ciphermod'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _factory

 L.  58        26  LOAD_FAST                'cipher_params'
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _cipher_params

 L.  59        32  LOAD_FAST                'ciphermod'
               34  LOAD_ATTR                block_size
               36  DUP_TOP          
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _block_size
               42  STORE_FAST               'bs'

 L.  60        44  LOAD_CONST               None
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _mac_tag

 L.  61        50  LOAD_FAST                'update_after_digest'
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _update_after_digest

 L.  64        56  LOAD_FAST                'bs'
               58  LOAD_CONST               8
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE    76  'to 76'

 L.  65        64  LOAD_CONST               27
               66  STORE_FAST               'const_Rb'

 L.  66        68  LOAD_CONST               16777216
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _max_size
               74  JUMP_FORWARD        108  'to 108'
             76_0  COME_FROM            62  '62'

 L.  67        76  LOAD_FAST                'bs'
               78  LOAD_CONST               16
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE    96  'to 96'

 L.  68        84  LOAD_CONST               135
               86  STORE_FAST               'const_Rb'

 L.  69        88  LOAD_CONST               4503599627370496
               90  LOAD_FAST                'self'
               92  STORE_ATTR               _max_size
               94  JUMP_FORWARD        108  'to 108'
             96_0  COME_FROM            82  '82'

 L.  71        96  LOAD_GLOBAL              TypeError
               98  LOAD_STR                 'CMAC requires a cipher with a block size of 8 or 16 bytes, not %d'

 L.  72       100  LOAD_FAST                'bs'

 L.  71       102  BINARY_MODULO    
              104  CALL_FUNCTION_1       1  ''
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            94  '94'
            108_1  COME_FROM            74  '74'

 L.  75       108  LOAD_CONST               b'\x00'
              110  LOAD_FAST                'bs'
              112  BINARY_MULTIPLY  
              114  STORE_FAST               'zero_block'

 L.  76       116  LOAD_FAST                'ciphermod'
              118  LOAD_ATTR                new
              120  LOAD_FAST                'key'

 L.  77       122  LOAD_FAST                'ciphermod'
              124  LOAD_ATTR                MODE_ECB

 L.  76       126  BUILD_TUPLE_2         2 
              128  BUILD_MAP_0           0 

 L.  78       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _cipher_params

 L.  76       134  <164>                 1  ''
              136  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              138  LOAD_FAST                'self'
              140  STORE_ATTR               _ecb

 L.  79       142  LOAD_FAST                'self'
              144  LOAD_ATTR                _ecb
              146  LOAD_METHOD              encrypt
              148  LOAD_FAST                'zero_block'
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'L'

 L.  80       154  LOAD_GLOBAL              bord
              156  LOAD_FAST                'L'
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  CALL_FUNCTION_1       1  ''
              164  LOAD_CONST               128
              166  BINARY_AND       
              168  POP_JUMP_IF_FALSE   184  'to 184'

 L.  81       170  LOAD_GLOBAL              _shift_bytes
              172  LOAD_FAST                'L'
              174  LOAD_FAST                'const_Rb'
              176  CALL_FUNCTION_2       2  ''
              178  LOAD_FAST                'self'
              180  STORE_ATTR               _k1
              182  JUMP_FORWARD        194  'to 194'
            184_0  COME_FROM           168  '168'

 L.  83       184  LOAD_GLOBAL              _shift_bytes
              186  LOAD_FAST                'L'
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_FAST                'self'
              192  STORE_ATTR               _k1
            194_0  COME_FROM           182  '182'

 L.  84       194  LOAD_GLOBAL              bord
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                _k1
              200  LOAD_CONST               0
              202  BINARY_SUBSCR    
              204  CALL_FUNCTION_1       1  ''
              206  LOAD_CONST               128
              208  BINARY_AND       
              210  POP_JUMP_IF_FALSE   228  'to 228'

 L.  85       212  LOAD_GLOBAL              _shift_bytes
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                _k1
              218  LOAD_FAST                'const_Rb'
              220  CALL_FUNCTION_2       2  ''
              222  LOAD_FAST                'self'
              224  STORE_ATTR               _k2
              226  JUMP_FORWARD        240  'to 240'
            228_0  COME_FROM           210  '210'

 L.  87       228  LOAD_GLOBAL              _shift_bytes
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                _k1
              234  CALL_FUNCTION_1       1  ''
              236  LOAD_FAST                'self'
              238  STORE_ATTR               _k2
            240_0  COME_FROM           226  '226'

 L.  90       240  LOAD_FAST                'ciphermod'
              242  LOAD_ATTR                new
              244  LOAD_FAST                'key'

 L.  91       246  LOAD_FAST                'ciphermod'
              248  LOAD_ATTR                MODE_CBC

 L.  92       250  LOAD_FAST                'zero_block'

 L.  90       252  BUILD_TUPLE_3         3 
              254  BUILD_MAP_0           0 

 L.  93       256  LOAD_FAST                'self'
              258  LOAD_ATTR                _cipher_params

 L.  90       260  <164>                 1  ''
              262  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              264  LOAD_FAST                'self'
              266  STORE_ATTR               _cbc

 L.  96       268  LOAD_GLOBAL              bytearray
              270  LOAD_FAST                'bs'
              272  CALL_FUNCTION_1       1  ''
              274  LOAD_FAST                'self'
              276  STORE_ATTR               _cache

 L.  97       278  LOAD_CONST               0
              280  LOAD_FAST                'self'
              282  STORE_ATTR               _cache_n

 L. 100       284  LOAD_FAST                'zero_block'
              286  LOAD_FAST                'self'
              288  STORE_ATTR               _last_ct

 L. 103       290  LOAD_CONST               None
              292  LOAD_FAST                'self'
              294  STORE_ATTR               _last_pt

 L. 106       296  LOAD_CONST               0
              298  LOAD_FAST                'self'
              300  STORE_ATTR               _data_size

 L. 108       302  LOAD_FAST                'msg'
          304_306  POP_JUMP_IF_FALSE   318  'to 318'

 L. 109       308  LOAD_FAST                'self'
              310  LOAD_METHOD              update
              312  LOAD_FAST                'msg'
              314  CALL_METHOD_1         1  ''
              316  POP_TOP          
            318_0  COME_FROM           304  '304'

Parse error at or near `<164>' instruction at offset 134

    def update--- This code section failed: ---

 L. 118         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _mac_tag
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _update_after_digest
               14  POP_JUMP_IF_TRUE     24  'to 24'

 L. 119        16  LOAD_GLOBAL              TypeError
               18  LOAD_STR                 'update() cannot be called after digest() or verify()'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'
             24_1  COME_FROM             8  '8'

 L. 121        24  LOAD_FAST                'self'
               26  DUP_TOP          
               28  LOAD_ATTR                _data_size
               30  LOAD_GLOBAL              len
               32  LOAD_FAST                'msg'
               34  CALL_FUNCTION_1       1  ''
               36  INPLACE_ADD      
               38  ROT_TWO          
               40  STORE_ATTR               _data_size

 L. 122        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _block_size
               46  STORE_FAST               'bs'

 L. 124        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _cache_n
               52  LOAD_CONST               0
               54  COMPARE_OP               >
               56  POP_JUMP_IF_FALSE   170  'to 170'

 L. 125        58  LOAD_GLOBAL              min
               60  LOAD_FAST                'bs'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _cache_n
               66  BINARY_SUBTRACT  
               68  LOAD_GLOBAL              len
               70  LOAD_FAST                'msg'
               72  CALL_FUNCTION_1       1  ''
               74  CALL_FUNCTION_2       2  ''
               76  STORE_FAST               'filler'

 L. 126        78  LOAD_FAST                'msg'
               80  LOAD_CONST               None
               82  LOAD_FAST                'filler'
               84  BUILD_SLICE_2         2 
               86  BINARY_SUBSCR    
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                _cache
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                _cache_n
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                _cache_n
              100  LOAD_FAST                'filler'
              102  BINARY_ADD       
              104  BUILD_SLICE_2         2 
              106  STORE_SUBSCR     

 L. 127       108  LOAD_FAST                'self'
              110  DUP_TOP          
              112  LOAD_ATTR                _cache_n
              114  LOAD_FAST                'filler'
              116  INPLACE_ADD      
              118  ROT_TWO          
              120  STORE_ATTR               _cache_n

 L. 129       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _cache_n
              126  LOAD_FAST                'bs'
              128  COMPARE_OP               <
              130  POP_JUMP_IF_FALSE   136  'to 136'

 L. 130       132  LOAD_FAST                'self'
              134  RETURN_VALUE     
            136_0  COME_FROM           130  '130'

 L. 132       136  LOAD_GLOBAL              memoryview
              138  LOAD_FAST                'msg'
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_FAST                'filler'
              144  LOAD_CONST               None
              146  BUILD_SLICE_2         2 
              148  BINARY_SUBSCR    
              150  STORE_FAST               'msg'

 L. 133       152  LOAD_FAST                'self'
              154  LOAD_METHOD              _update
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _cache
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          

 L. 134       164  LOAD_CONST               0
              166  LOAD_FAST                'self'
              168  STORE_ATTR               _cache_n
            170_0  COME_FROM            56  '56'

 L. 136       170  LOAD_GLOBAL              len
              172  LOAD_FAST                'msg'
              174  CALL_FUNCTION_1       1  ''
              176  LOAD_FAST                'bs'
              178  BINARY_MODULO    
              180  STORE_FAST               'remain'

 L. 137       182  LOAD_FAST                'remain'
              184  LOAD_CONST               0
              186  COMPARE_OP               >
              188  POP_JUMP_IF_FALSE   236  'to 236'

 L. 138       190  LOAD_FAST                'self'
              192  LOAD_METHOD              _update
              194  LOAD_FAST                'msg'
              196  LOAD_CONST               None
              198  LOAD_FAST                'remain'
              200  UNARY_NEGATIVE   
              202  BUILD_SLICE_2         2 
              204  BINARY_SUBSCR    
              206  CALL_METHOD_1         1  ''
              208  POP_TOP          

 L. 139       210  LOAD_FAST                'msg'
              212  LOAD_FAST                'remain'
              214  UNARY_NEGATIVE   
              216  LOAD_CONST               None
              218  BUILD_SLICE_2         2 
              220  BINARY_SUBSCR    
              222  LOAD_FAST                'self'
              224  LOAD_ATTR                _cache
              226  LOAD_CONST               None
              228  LOAD_FAST                'remain'
              230  BUILD_SLICE_2         2 
              232  STORE_SUBSCR     
              234  JUMP_FORWARD        246  'to 246'
            236_0  COME_FROM           188  '188'

 L. 141       236  LOAD_FAST                'self'
              238  LOAD_METHOD              _update
              240  LOAD_FAST                'msg'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          
            246_0  COME_FROM           234  '234'

 L. 142       246  LOAD_FAST                'remain'
              248  LOAD_FAST                'self'
              250  STORE_ATTR               _cache_n

 L. 143       252  LOAD_FAST                'self'
              254  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _update--- This code section failed: ---

 L. 148         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _block_size
                4  STORE_FAST               'bs'

 L. 149         6  LOAD_GLOBAL              len
                8  LOAD_FAST                'data_block'
               10  CALL_FUNCTION_1       1  ''
               12  LOAD_FAST                'bs'
               14  BINARY_MODULO    
               16  LOAD_CONST               0
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_TRUE     26  'to 26'
               22  <74>             
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            20  '20'

 L. 151        26  LOAD_GLOBAL              len
               28  LOAD_FAST                'data_block'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_CONST               0
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L. 152        38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            36  '36'

 L. 154        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _cbc
               46  LOAD_METHOD              encrypt
               48  LOAD_FAST                'data_block'
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'ct'

 L. 155        54  LOAD_GLOBAL              len
               56  LOAD_FAST                'data_block'
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_FAST                'bs'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L. 156        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _last_ct
               70  STORE_FAST               'second_last'
               72  JUMP_FORWARD         94  'to 94'
             74_0  COME_FROM            64  '64'

 L. 158        74  LOAD_FAST                'ct'
               76  LOAD_FAST                'bs'
               78  UNARY_NEGATIVE   
               80  LOAD_CONST               2
               82  BINARY_MULTIPLY  
               84  LOAD_FAST                'bs'
               86  UNARY_NEGATIVE   
               88  BUILD_SLICE_2         2 
               90  BINARY_SUBSCR    
               92  STORE_FAST               'second_last'
             94_0  COME_FROM            72  '72'

 L. 159        94  LOAD_FAST                'ct'
               96  LOAD_FAST                'bs'
               98  UNARY_NEGATIVE   
              100  LOAD_CONST               None
              102  BUILD_SLICE_2         2 
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'self'
              108  STORE_ATTR               _last_ct

 L. 160       110  LOAD_GLOBAL              strxor
              112  LOAD_FAST                'second_last'
              114  LOAD_FAST                'data_block'
              116  LOAD_FAST                'bs'
              118  UNARY_NEGATIVE   
              120  LOAD_CONST               None
              122  BUILD_SLICE_2         2 
              124  BINARY_SUBSCR    
              126  CALL_FUNCTION_2       2  ''
              128  LOAD_FAST                'self'
              130  STORE_ATTR               _last_pt

Parse error at or near `<74>' instruction at offset 22

    def copy--- This code section failed: ---

 L. 173         0  LOAD_FAST                'self'
                2  LOAD_METHOD              __new__
                4  LOAD_GLOBAL              CMAC
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'obj'

 L. 174        10  LOAD_FAST                'self'
               12  LOAD_ATTR                __dict__
               14  LOAD_METHOD              copy
               16  CALL_METHOD_0         0  ''
               18  LOAD_FAST                'obj'
               20  STORE_ATTR               __dict__

 L. 175        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _factory
               26  LOAD_ATTR                new
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _key

 L. 176        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _factory
               36  LOAD_ATTR                MODE_CBC

 L. 177        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _last_ct

 L. 175        42  BUILD_TUPLE_3         3 
               44  BUILD_MAP_0           0 

 L. 178        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _cipher_params

 L. 175        50  <164>                 1  ''
               52  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               54  LOAD_FAST                'obj'
               56  STORE_ATTR               _cbc

 L. 179        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _cache
               62  LOAD_CONST               None
               64  LOAD_CONST               None
               66  BUILD_SLICE_2         2 
               68  BINARY_SUBSCR    
               70  LOAD_FAST                'obj'
               72  STORE_ATTR               _cache

 L. 180        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _last_ct
               78  LOAD_CONST               None
               80  LOAD_CONST               None
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    
               86  LOAD_FAST                'obj'
               88  STORE_ATTR               _last_ct

 L. 181        90  LOAD_FAST                'obj'
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 50

    def digest--- This code section failed: ---

 L. 192         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _block_size
                4  STORE_FAST               'bs'

 L. 194         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _mac_tag
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    28  'to 28'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _update_after_digest
               20  POP_JUMP_IF_TRUE     28  'to 28'

 L. 195        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _mac_tag
               26  RETURN_VALUE     
             28_0  COME_FROM            20  '20'
             28_1  COME_FROM            14  '14'

 L. 197        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _data_size
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _max_size
               36  COMPARE_OP               >
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 198        40  LOAD_GLOBAL              ValueError
               42  LOAD_STR                 'MAC is unsafe for this message'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L. 200        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _cache_n
               52  LOAD_CONST               0
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE    84  'to 84'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _data_size
               62  LOAD_CONST               0
               64  COMPARE_OP               >
               66  POP_JUMP_IF_FALSE    84  'to 84'

 L. 202        68  LOAD_GLOBAL              strxor
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _last_pt
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _k1
               78  CALL_FUNCTION_2       2  ''
               80  STORE_FAST               'pt'
               82  JUMP_FORWARD        150  'to 150'
             84_0  COME_FROM            66  '66'
             84_1  COME_FROM            56  '56'

 L. 205        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _cache
               88  LOAD_CONST               None
               90  LOAD_CONST               None
               92  BUILD_SLICE_2         2 
               94  BINARY_SUBSCR    
               96  STORE_FAST               'partial'

 L. 206        98  LOAD_CONST               b'\x80'
              100  LOAD_CONST               b'\x00'
              102  LOAD_FAST                'bs'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                _cache_n
              108  BINARY_SUBTRACT  
              110  LOAD_CONST               1
              112  BINARY_SUBTRACT  
              114  BINARY_MULTIPLY  
              116  BINARY_ADD       
              118  LOAD_FAST                'partial'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                _cache_n
              124  LOAD_CONST               None
              126  BUILD_SLICE_2         2 
              128  STORE_SUBSCR     

 L. 207       130  LOAD_GLOBAL              strxor
              132  LOAD_GLOBAL              strxor
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                _last_ct
              138  LOAD_FAST                'partial'
              140  CALL_FUNCTION_2       2  ''
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                _k2
              146  CALL_FUNCTION_2       2  ''
              148  STORE_FAST               'pt'
            150_0  COME_FROM            82  '82'

 L. 209       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _ecb
              154  LOAD_METHOD              encrypt
              156  LOAD_FAST                'pt'
              158  CALL_METHOD_1         1  ''
              160  LOAD_CONST               None
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                digest_size
              166  BUILD_SLICE_2         2 
              168  BINARY_SUBSCR    
              170  LOAD_FAST                'self'
              172  STORE_ATTR               _mac_tag

 L. 211       174  LOAD_FAST                'self'
              176  LOAD_ATTR                _mac_tag
              178  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 12

    def hexdigest(self):
        """Return the **printable** MAC tag of the message authenticated so far.

        :return: The MAC tag, computed over the data processed so far.
                 Hexadecimal encoded.
        :rtype: string
        """
        return ''.join['%02x' % bord(x) for x in tuple(self.digest)]

    def verify(self, mac_tag):
        """Verify that a given **binary** MAC (computed by another party)
        is valid.

        Args:
          mac_tag (byte string/byte array/memoryview): the expected MAC of the message.

        Raises:
            ValueError: if the MAC does not match. It means that the message
                has been tampered with or that the MAC key is incorrect.
        """
        secret = get_random_bytes(16)
        mac1 = BLAKE2s.new(digest_bits=160, key=secret, data=mac_tag)
        mac2 = BLAKE2s.new(digest_bits=160, key=secret, data=(self.digest))
        if mac1.digest != mac2.digest:
            raise ValueError('MAC check failed')

    def hexverify(self, hex_mac_tag):
        """Return the **printable** MAC tag of the message authenticated so far.

        :return: The MAC tag, computed over the data processed so far.
                 Hexadecimal encoded.
        :rtype: string
        """
        self.verifyunhexlify(tobytes(hex_mac_tag))


def new--- This code section failed: ---

 L. 287         0  LOAD_FAST                'ciphermod'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 288         8  LOAD_GLOBAL              TypeError
               10  LOAD_STR                 'ciphermod must be specified (try AES)'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 290        16  LOAD_FAST                'cipher_params'
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    28  'to 28'
               24  BUILD_MAP_0           0 
               26  JUMP_FORWARD         34  'to 34'
             28_0  COME_FROM            22  '22'
               28  LOAD_GLOBAL              dict
               30  LOAD_FAST                'cipher_params'
               32  CALL_FUNCTION_1       1  ''
             34_0  COME_FROM            26  '26'
               34  STORE_FAST               'cipher_params'

 L. 292        36  LOAD_FAST                'mac_len'
               38  LOAD_CONST               None
               40  <117>                 0  ''
               42  POP_JUMP_IF_FALSE    50  'to 50'

 L. 293        44  LOAD_FAST                'ciphermod'
               46  LOAD_ATTR                block_size
               48  STORE_FAST               'mac_len'
             50_0  COME_FROM            42  '42'

 L. 295        50  LOAD_FAST                'mac_len'
               52  LOAD_CONST               4
               54  COMPARE_OP               <
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 296        58  LOAD_GLOBAL              ValueError
               60  LOAD_STR                 'MAC tag length must be at least 4 bytes long'
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            56  '56'

 L. 298        66  LOAD_FAST                'mac_len'
               68  LOAD_FAST                'ciphermod'
               70  LOAD_ATTR                block_size
               72  COMPARE_OP               >
               74  POP_JUMP_IF_FALSE    90  'to 90'

 L. 299        76  LOAD_GLOBAL              ValueError
               78  LOAD_STR                 'MAC tag length cannot be larger than a cipher block (%d) bytes'
               80  LOAD_FAST                'ciphermod'
               82  LOAD_ATTR                block_size
               84  BINARY_MODULO    
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            74  '74'

 L. 301        90  LOAD_GLOBAL              CMAC
               92  LOAD_FAST                'key'
               94  LOAD_FAST                'msg'
               96  LOAD_FAST                'ciphermod'
               98  LOAD_FAST                'cipher_params'
              100  LOAD_FAST                'mac_len'

 L. 302       102  LOAD_FAST                'update_after_digest'

 L. 301       104  CALL_FUNCTION_6       6  ''
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1