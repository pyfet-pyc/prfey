# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Cipher\_mode_ccm.py
"""
Counter with CBC-MAC (CCM) mode.
"""
__all__ = [
 'CcmMode']
import struct
from binascii import unhexlify
from Crypto.Util.py3compat import byte_string, bord, _copy_bytes
from Crypto.Util._raw_api import is_writeable_buffer
import Crypto.Util.strxor as strxor
from Crypto.Util.number import long_to_bytes
from Crypto.Hash import BLAKE2s
from Crypto.Random import get_random_bytes

def enum(**enums):
    return type('Enum', (), enums)


MacStatus = enum(NOT_STARTED=0, PROCESSING_AUTH_DATA=1, PROCESSING_PLAINTEXT=2)

class CcmMode(object):
    __doc__ = 'Counter with CBC-MAC (CCM).\n\n    This is an Authenticated Encryption with Associated Data (`AEAD`_) mode.\n    It provides both confidentiality and authenticity.\n\n    The header of the message may be left in the clear, if needed, and it will\n    still be subject to authentication. The decryption step tells the receiver\n    if the message comes from a source that really knowns the secret key.\n    Additionally, decryption detects if any part of the message - including the\n    header - has been modified or corrupted.\n\n    This mode requires a nonce. The nonce shall never repeat for two\n    different messages encrypted with the same key, but it does not need\n    to be random.\n    Note that there is a trade-off between the size of the nonce and the\n    maximum size of a single message you can encrypt.\n\n    It is important to use a large nonce if the key is reused across several\n    messages and the nonce is chosen randomly.\n\n    It is acceptable to us a short nonce if the key is only used a few times or\n    if the nonce is taken from a counter.\n\n    The following table shows the trade-off when the nonce is chosen at\n    random. The column on the left shows how many messages it takes\n    for the keystream to repeat **on average**. In practice, you will want to\n    stop using the key way before that.\n\n    +--------------------+---------------+-------------------+\n    | Avg. # of messages |    nonce      |     Max. message  |\n    | before keystream   |    size       |     size          |\n    | repeats            |    (bytes)    |     (bytes)       |\n    +====================+===============+===================+\n    |       2^52         |      13       |        64K        |\n    +--------------------+---------------+-------------------+\n    |       2^48         |      12       |        16M        |\n    +--------------------+---------------+-------------------+\n    |       2^44         |      11       |         4G        |\n    +--------------------+---------------+-------------------+\n    |       2^40         |      10       |         1T        |\n    +--------------------+---------------+-------------------+\n    |       2^36         |       9       |        64P        |\n    +--------------------+---------------+-------------------+\n    |       2^32         |       8       |        16E        |\n    +--------------------+---------------+-------------------+\n\n    This mode is only available for ciphers that operate on 128 bits blocks\n    (e.g. AES but not TDES).\n\n    See `NIST SP800-38C`_ or RFC3610_.\n\n    .. _`NIST SP800-38C`: http://csrc.nist.gov/publications/nistpubs/800-38C/SP800-38C.pdf\n    .. _RFC3610: https://tools.ietf.org/html/rfc3610\n    .. _AEAD: http://blog.cryptographyengineering.com/2012/05/how-to-choose-authenticated-encryption.html\n\n    :undocumented: __init__\n    '

    def __init__--- This code section failed: ---

 L. 119         0  LOAD_FAST                'factory'
                2  LOAD_ATTR                block_size
                4  LOAD_FAST                'self'
                6  STORE_ATTR               block_size

 L. 122         8  LOAD_GLOBAL              _copy_bytes
               10  LOAD_CONST               None
               12  LOAD_CONST               None
               14  LOAD_FAST                'nonce'
               16  CALL_FUNCTION_3       3  ''
               18  LOAD_FAST                'self'
               20  STORE_ATTR               nonce

 L. 125        22  LOAD_FAST                'factory'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _factory

 L. 126        28  LOAD_GLOBAL              _copy_bytes
               30  LOAD_CONST               None
               32  LOAD_CONST               None
               34  LOAD_FAST                'key'
               36  CALL_FUNCTION_3       3  ''
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _key

 L. 127        42  LOAD_FAST                'mac_len'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _mac_len

 L. 128        48  LOAD_FAST                'msg_len'
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _msg_len

 L. 129        54  LOAD_FAST                'assoc_len'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _assoc_len

 L. 130        60  LOAD_FAST                'cipher_params'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _cipher_params

 L. 132        66  LOAD_CONST               None
               68  LOAD_FAST                'self'
               70  STORE_ATTR               _mac_tag

 L. 134        72  LOAD_FAST                'self'
               74  LOAD_ATTR                block_size
               76  LOAD_CONST               16
               78  COMPARE_OP               !=
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 135        82  LOAD_GLOBAL              ValueError
               84  LOAD_STR                 'CCM mode is only available for ciphers that operate on 128 bits blocks'
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'

 L. 139        90  LOAD_FAST                'mac_len'
               92  LOAD_CONST               (4, 6, 8, 10, 12, 14, 16)
               94  <118>                 1  ''
               96  POP_JUMP_IF_FALSE   110  'to 110'

 L. 140        98  LOAD_GLOBAL              ValueError
              100  LOAD_STR                 "Parameter 'mac_len' must be even and in the range 4..16 (not %d)"

 L. 141       102  LOAD_FAST                'mac_len'

 L. 140       104  BINARY_MODULO    
              106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
            110_0  COME_FROM            96  '96'

 L. 144       110  LOAD_FAST                'nonce'
              112  POP_JUMP_IF_FALSE   140  'to 140'
              114  LOAD_CONST               7
              116  LOAD_GLOBAL              len
              118  LOAD_FAST                'nonce'
              120  CALL_FUNCTION_1       1  ''
              122  DUP_TOP          
              124  ROT_THREE        
              126  COMPARE_OP               <=
              128  POP_JUMP_IF_FALSE   138  'to 138'
              130  LOAD_CONST               13
              132  COMPARE_OP               <=
              134  POP_JUMP_IF_TRUE    148  'to 148'
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM           128  '128'
              138  POP_TOP          
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM           112  '112'

 L. 145       140  LOAD_GLOBAL              ValueError
              142  LOAD_STR                 "Length of parameter 'nonce' must be in the range 7..13 bytes"
              144  CALL_FUNCTION_1       1  ''
              146  RAISE_VARARGS_1       1  'exception instance'
            148_0  COME_FROM           134  '134'

 L. 150       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _factory
              152  LOAD_ATTR                new
              154  LOAD_FAST                'key'

 L. 151       156  LOAD_FAST                'factory'
              158  LOAD_ATTR                MODE_CBC

 L. 150       160  BUILD_TUPLE_2         2 
              162  LOAD_STR                 'iv'

 L. 152       164  LOAD_CONST               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

 L. 150       166  BUILD_MAP_1           1 

 L. 153       168  LOAD_FAST                'cipher_params'

 L. 150       170  <164>                 1  ''
              172  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              174  LOAD_FAST                'self'
              176  STORE_ATTR               _mac

 L. 154       178  LOAD_GLOBAL              MacStatus
              180  LOAD_ATTR                NOT_STARTED
              182  LOAD_FAST                'self'
              184  STORE_ATTR               _mac_status

 L. 155       186  LOAD_CONST               None
              188  LOAD_FAST                'self'
              190  STORE_ATTR               _t

 L. 158       192  LOAD_FAST                'self'
              194  LOAD_ATTR                update
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                encrypt
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                decrypt

 L. 159       204  LOAD_FAST                'self'
              206  LOAD_ATTR                digest
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                verify

 L. 158       212  BUILD_LIST_5          5 
              214  LOAD_FAST                'self'
              216  STORE_ATTR               _next

 L. 162       218  LOAD_CONST               0
              220  LOAD_FAST                'self'
              222  STORE_ATTR               _cumul_assoc_len

 L. 163       224  LOAD_CONST               0
              226  LOAD_FAST                'self'
              228  STORE_ATTR               _cumul_msg_len

 L. 168       230  BUILD_LIST_0          0 
              232  LOAD_FAST                'self'
              234  STORE_ATTR               _cache

 L. 171       236  LOAD_CONST               15
              238  LOAD_GLOBAL              len
              240  LOAD_FAST                'nonce'
              242  CALL_FUNCTION_1       1  ''
              244  BINARY_SUBTRACT  
              246  STORE_FAST               'q'

 L. 172       248  LOAD_FAST                'self'
              250  LOAD_ATTR                _factory
              252  LOAD_ATTR                new
              254  LOAD_FAST                'key'

 L. 173       256  LOAD_FAST                'self'
              258  LOAD_ATTR                _factory
              260  LOAD_ATTR                MODE_CTR

 L. 172       262  BUILD_TUPLE_2         2 
              264  LOAD_STR                 'nonce'

 L. 174       266  LOAD_GLOBAL              struct
              268  LOAD_METHOD              pack
              270  LOAD_STR                 'B'
              272  LOAD_FAST                'q'
              274  LOAD_CONST               1
              276  BINARY_SUBTRACT  
              278  CALL_METHOD_2         2  ''
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                nonce
              284  BINARY_ADD       

 L. 172       286  BUILD_MAP_1           1 

 L. 175       288  LOAD_FAST                'cipher_params'

 L. 172       290  <164>                 1  ''
              292  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              294  LOAD_FAST                'self'
              296  STORE_ATTR               _cipher

 L. 178       298  LOAD_FAST                'self'
              300  LOAD_ATTR                _cipher
              302  LOAD_METHOD              encrypt
              304  LOAD_CONST               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
              306  CALL_METHOD_1         1  ''
              308  LOAD_FAST                'self'
              310  STORE_ATTR               _s_0

 L. 181       312  LOAD_CONST               None
              314  LOAD_FAST                'assoc_len'
              316  LOAD_FAST                'msg_len'
              318  BUILD_TUPLE_2         2 
              320  <118>                 1  ''
          322_324  POP_JUMP_IF_FALSE   334  'to 334'

 L. 182       326  LOAD_FAST                'self'
              328  LOAD_METHOD              _start_mac
              330  CALL_METHOD_0         0  ''
              332  POP_TOP          
            334_0  COME_FROM           322  '322'

Parse error at or near `<118>' instruction at offset 94

    def _start_mac--- This code section failed: ---

 L. 186         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _mac_status
                4  LOAD_GLOBAL              MacStatus
                6  LOAD_ATTR                NOT_STARTED
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L. 187        16  LOAD_CONST               None
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _assoc_len
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _msg_len
               26  BUILD_TUPLE_2         2 
               28  <118>                 1  ''
               30  POP_JUMP_IF_TRUE     36  'to 36'
               32  <74>             
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            30  '30'

 L. 188        36  LOAD_GLOBAL              isinstance
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _cache
               42  LOAD_GLOBAL              list
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_TRUE     52  'to 52'
               48  <74>             
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            46  '46'

 L. 191        52  LOAD_CONST               15
               54  LOAD_GLOBAL              len
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                nonce
               60  CALL_FUNCTION_1       1  ''
               62  BINARY_SUBTRACT  
               64  STORE_FAST               'q'

 L. 192        66  LOAD_CONST               64
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _assoc_len
               72  LOAD_CONST               0
               74  COMPARE_OP               >
               76  BINARY_MULTIPLY  
               78  LOAD_CONST               8
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _mac_len
               84  LOAD_CONST               2
               86  BINARY_SUBTRACT  
               88  LOAD_CONST               2
               90  BINARY_FLOOR_DIVIDE
               92  BINARY_MULTIPLY  
               94  BINARY_ADD       

 L. 193        96  LOAD_FAST                'q'
               98  LOAD_CONST               1
              100  BINARY_SUBTRACT  

 L. 192       102  BINARY_ADD       
              104  STORE_FAST               'flags'

 L. 194       106  LOAD_GLOBAL              struct
              108  LOAD_METHOD              pack
              110  LOAD_STR                 'B'
              112  LOAD_FAST                'flags'
              114  CALL_METHOD_2         2  ''
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                nonce
              120  BINARY_ADD       
              122  LOAD_GLOBAL              long_to_bytes
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                _msg_len
              128  LOAD_FAST                'q'
              130  CALL_FUNCTION_2       2  ''
              132  BINARY_ADD       
              134  STORE_FAST               'b_0'

 L. 198       136  LOAD_CONST               b''
              138  STORE_FAST               'assoc_len_encoded'

 L. 199       140  LOAD_FAST                'self'
              142  LOAD_ATTR                _assoc_len
              144  LOAD_CONST               0
              146  COMPARE_OP               >
              148  POP_JUMP_IF_FALSE   210  'to 210'

 L. 200       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _assoc_len
              154  LOAD_CONST               65280
              156  COMPARE_OP               <
              158  POP_JUMP_IF_FALSE   166  'to 166'

 L. 201       160  LOAD_CONST               2
              162  STORE_FAST               'enc_size'
              164  JUMP_FORWARD        194  'to 194'
            166_0  COME_FROM           158  '158'

 L. 202       166  LOAD_FAST                'self'
              168  LOAD_ATTR                _assoc_len
              170  LOAD_CONST               4294967296
              172  COMPARE_OP               <
              174  POP_JUMP_IF_FALSE   186  'to 186'

 L. 203       176  LOAD_CONST               b'\xff\xfe'
              178  STORE_FAST               'assoc_len_encoded'

 L. 204       180  LOAD_CONST               4
              182  STORE_FAST               'enc_size'
              184  JUMP_FORWARD        194  'to 194'
            186_0  COME_FROM           174  '174'

 L. 206       186  LOAD_CONST               b'\xff\xff'
              188  STORE_FAST               'assoc_len_encoded'

 L. 207       190  LOAD_CONST               8
              192  STORE_FAST               'enc_size'
            194_0  COME_FROM           184  '184'
            194_1  COME_FROM           164  '164'

 L. 208       194  LOAD_FAST                'assoc_len_encoded'
              196  LOAD_GLOBAL              long_to_bytes
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                _assoc_len
              202  LOAD_FAST                'enc_size'
              204  CALL_FUNCTION_2       2  ''
              206  INPLACE_ADD      
              208  STORE_FAST               'assoc_len_encoded'
            210_0  COME_FROM           148  '148'

 L. 211       210  LOAD_FAST                'self'
              212  LOAD_ATTR                _cache
              214  LOAD_METHOD              insert
              216  LOAD_CONST               0
              218  LOAD_FAST                'b_0'
              220  CALL_METHOD_2         2  ''
              222  POP_TOP          

 L. 212       224  LOAD_FAST                'self'
              226  LOAD_ATTR                _cache
              228  LOAD_METHOD              insert
              230  LOAD_CONST               1
              232  LOAD_FAST                'assoc_len_encoded'
              234  CALL_METHOD_2         2  ''
              236  POP_TOP          

 L. 215       238  LOAD_CONST               b''
              240  LOAD_METHOD              join
              242  LOAD_FAST                'self'
              244  LOAD_ATTR                _cache
              246  CALL_METHOD_1         1  ''
              248  STORE_FAST               'first_data_to_mac'

 L. 216       250  LOAD_CONST               b''
              252  LOAD_FAST                'self'
              254  STORE_ATTR               _cache

 L. 217       256  LOAD_GLOBAL              MacStatus
              258  LOAD_ATTR                PROCESSING_AUTH_DATA
              260  LOAD_FAST                'self'
              262  STORE_ATTR               _mac_status

 L. 218       264  LOAD_FAST                'self'
              266  LOAD_METHOD              _update
              268  LOAD_FAST                'first_data_to_mac'
              270  CALL_METHOD_1         1  ''
              272  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _pad_cache_and_update--- This code section failed: ---

 L. 222         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _mac_status
                4  LOAD_GLOBAL              MacStatus
                6  LOAD_ATTR                NOT_STARTED
                8  COMPARE_OP               !=
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L. 223        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _cache
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                block_size
               28  COMPARE_OP               <
               30  POP_JUMP_IF_TRUE     36  'to 36'
               32  <74>             
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            30  '30'

 L. 228        36  LOAD_GLOBAL              len
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _cache
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'len_cache'

 L. 229        46  LOAD_FAST                'len_cache'
               48  LOAD_CONST               0
               50  COMPARE_OP               >
               52  POP_JUMP_IF_FALSE    74  'to 74'

 L. 230        54  LOAD_FAST                'self'
               56  LOAD_METHOD              _update
               58  LOAD_CONST               b'\x00'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                block_size
               64  LOAD_FAST                'len_cache'
               66  BINARY_SUBTRACT  
               68  BINARY_MULTIPLY  
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
             74_0  COME_FROM            52  '52'

Parse error at or near `None' instruction at offset -1

    def update--- This code section failed: ---

 L. 255         0  LOAD_FAST                'self'
                2  LOAD_ATTR                update
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 256        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'update() can only be called immediately after initialization'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 259        20  LOAD_FAST                'self'
               22  LOAD_ATTR                update
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                encrypt
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                decrypt

 L. 260        32  LOAD_FAST                'self'
               34  LOAD_ATTR                digest
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                verify

 L. 259        40  BUILD_LIST_5          5 
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _next

 L. 262        46  LOAD_FAST                'self'
               48  DUP_TOP          
               50  LOAD_ATTR                _cumul_assoc_len
               52  LOAD_GLOBAL              len
               54  LOAD_FAST                'assoc_data'
               56  CALL_FUNCTION_1       1  ''
               58  INPLACE_ADD      
               60  ROT_TWO          
               62  STORE_ATTR               _cumul_assoc_len

 L. 263        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _assoc_len
               68  LOAD_CONST               None
               70  <117>                 1  ''
               72  POP_JUMP_IF_FALSE    94  'to 94'

 L. 264        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _cumul_assoc_len
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _assoc_len
               82  COMPARE_OP               >

 L. 263        84  POP_JUMP_IF_FALSE    94  'to 94'

 L. 265        86  LOAD_GLOBAL              ValueError
               88  LOAD_STR                 'Associated data is too long'
               90  CALL_FUNCTION_1       1  ''
               92  RAISE_VARARGS_1       1  'exception instance'
             94_0  COME_FROM            84  '84'
             94_1  COME_FROM            72  '72'

 L. 267        94  LOAD_FAST                'self'
               96  LOAD_METHOD              _update
               98  LOAD_FAST                'assoc_data'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          

 L. 268       104  LOAD_FAST                'self'
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _update--- This code section failed: ---

 L. 276         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _mac_status
                4  LOAD_GLOBAL              MacStatus
                6  LOAD_ATTR                NOT_STARTED
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    48  'to 48'

 L. 277        12  LOAD_GLOBAL              is_writeable_buffer
               14  LOAD_FAST                'assoc_data_pt'
               16  CALL_FUNCTION_1       1  ''
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L. 278        20  LOAD_GLOBAL              _copy_bytes
               22  LOAD_CONST               None
               24  LOAD_CONST               None
               26  LOAD_FAST                'assoc_data_pt'
               28  CALL_FUNCTION_3       3  ''
               30  STORE_FAST               'assoc_data_pt'
             32_0  COME_FROM            18  '18'

 L. 279        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _cache
               36  LOAD_METHOD              append
               38  LOAD_FAST                'assoc_data_pt'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 280        44  LOAD_CONST               None
               46  RETURN_VALUE     
             48_0  COME_FROM            10  '10'

 L. 282        48  LOAD_GLOBAL              len
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                _cache
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                block_size
               60  COMPARE_OP               <
               62  POP_JUMP_IF_TRUE     68  'to 68'
               64  <74>             
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            62  '62'

 L. 284        68  LOAD_GLOBAL              len
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _cache
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_CONST               0
               78  COMPARE_OP               >
               80  POP_JUMP_IF_FALSE   184  'to 184'

 L. 285        82  LOAD_GLOBAL              min
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                block_size
               88  LOAD_GLOBAL              len
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _cache
               94  CALL_FUNCTION_1       1  ''
               96  BINARY_SUBTRACT  

 L. 286        98  LOAD_GLOBAL              len
              100  LOAD_FAST                'assoc_data_pt'
              102  CALL_FUNCTION_1       1  ''

 L. 285       104  CALL_FUNCTION_2       2  ''
              106  STORE_FAST               'filler'

 L. 287       108  LOAD_FAST                'self'
              110  DUP_TOP          
              112  LOAD_ATTR                _cache
              114  LOAD_GLOBAL              _copy_bytes
              116  LOAD_CONST               None
              118  LOAD_FAST                'filler'
              120  LOAD_FAST                'assoc_data_pt'
              122  CALL_FUNCTION_3       3  ''
              124  INPLACE_ADD      
              126  ROT_TWO          
              128  STORE_ATTR               _cache

 L. 288       130  LOAD_GLOBAL              _copy_bytes
              132  LOAD_FAST                'filler'
              134  LOAD_CONST               None
              136  LOAD_FAST                'assoc_data_pt'
              138  CALL_FUNCTION_3       3  ''
              140  STORE_FAST               'assoc_data_pt'

 L. 290       142  LOAD_GLOBAL              len
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                _cache
              148  CALL_FUNCTION_1       1  ''
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                block_size
              154  COMPARE_OP               <
              156  POP_JUMP_IF_FALSE   162  'to 162'

 L. 291       158  LOAD_CONST               None
              160  RETURN_VALUE     
            162_0  COME_FROM           156  '156'

 L. 294       162  LOAD_FAST                'self'
              164  LOAD_ATTR                _mac
              166  LOAD_METHOD              encrypt
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                _cache
              172  CALL_METHOD_1         1  ''
              174  LOAD_FAST                'self'
              176  STORE_ATTR               _t

 L. 295       178  LOAD_CONST               b''
              180  LOAD_FAST                'self'
              182  STORE_ATTR               _cache
            184_0  COME_FROM            80  '80'

 L. 297       184  LOAD_GLOBAL              len
              186  LOAD_FAST                'assoc_data_pt'
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                block_size
              194  BINARY_FLOOR_DIVIDE
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                block_size
              200  BINARY_MULTIPLY  
              202  STORE_FAST               'update_len'

 L. 298       204  LOAD_GLOBAL              _copy_bytes
              206  LOAD_FAST                'update_len'
              208  LOAD_CONST               None
              210  LOAD_FAST                'assoc_data_pt'
              212  CALL_FUNCTION_3       3  ''
              214  LOAD_FAST                'self'
              216  STORE_ATTR               _cache

 L. 299       218  LOAD_FAST                'update_len'
              220  LOAD_CONST               0
              222  COMPARE_OP               >
          224_226  POP_JUMP_IF_FALSE   258  'to 258'

 L. 300       228  LOAD_FAST                'self'
              230  LOAD_ATTR                _mac
              232  LOAD_METHOD              encrypt
              234  LOAD_FAST                'assoc_data_pt'
              236  LOAD_CONST               None
              238  LOAD_FAST                'update_len'
              240  BUILD_SLICE_2         2 
              242  BINARY_SUBSCR    
              244  CALL_METHOD_1         1  ''
              246  LOAD_CONST               -16
              248  LOAD_CONST               None
              250  BUILD_SLICE_2         2 
              252  BINARY_SUBSCR    
              254  LOAD_FAST                'self'
              256  STORE_ATTR               _t
            258_0  COME_FROM           224  '224'

Parse error at or near `<74>' instruction at offset 64

    def encrypt--- This code section failed: ---

 L. 339         0  LOAD_FAST                'self'
                2  LOAD_ATTR                encrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 340        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'encrypt() can only be called after initialization or an update()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 342        20  LOAD_FAST                'self'
               22  LOAD_ATTR                encrypt
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                digest
               28  BUILD_LIST_2          2 
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _next

 L. 345        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _assoc_len
               38  LOAD_CONST               None
               40  <117>                 0  ''
               42  POP_JUMP_IF_FALSE   102  'to 102'

 L. 346        44  LOAD_GLOBAL              isinstance
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _cache
               50  LOAD_GLOBAL              list
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_TRUE     60  'to 60'
               56  <74>             
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            54  '54'

 L. 347        60  LOAD_GLOBAL              sum
               62  LOAD_LISTCOMP            '<code_object <listcomp>>'
               64  LOAD_STR                 'CcmMode.encrypt.<locals>.<listcomp>'
               66  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _cache
               72  GET_ITER         
               74  CALL_FUNCTION_1       1  ''
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_FAST                'self'
               80  STORE_ATTR               _assoc_len

 L. 348        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _msg_len
               86  LOAD_CONST               None
               88  <117>                 1  ''
               90  POP_JUMP_IF_FALSE   122  'to 122'

 L. 349        92  LOAD_FAST                'self'
               94  LOAD_METHOD              _start_mac
               96  CALL_METHOD_0         0  ''
               98  POP_TOP          
              100  JUMP_FORWARD        122  'to 122'
            102_0  COME_FROM            42  '42'

 L. 351       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _cumul_assoc_len
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                _assoc_len
              110  COMPARE_OP               <
              112  POP_JUMP_IF_FALSE   122  'to 122'

 L. 352       114  LOAD_GLOBAL              ValueError
              116  LOAD_STR                 'Associated data is too short'
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           112  '112'
            122_1  COME_FROM           100  '100'
            122_2  COME_FROM            90  '90'

 L. 356       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _msg_len
              126  LOAD_CONST               None
              128  <117>                 0  ''
              130  POP_JUMP_IF_FALSE   160  'to 160'

 L. 357       132  LOAD_GLOBAL              len
              134  LOAD_FAST                'plaintext'
              136  CALL_FUNCTION_1       1  ''
              138  LOAD_FAST                'self'
              140  STORE_ATTR               _msg_len

 L. 358       142  LOAD_FAST                'self'
              144  LOAD_METHOD              _start_mac
              146  CALL_METHOD_0         0  ''
              148  POP_TOP          

 L. 359       150  LOAD_FAST                'self'
              152  LOAD_ATTR                digest
              154  BUILD_LIST_1          1 
              156  LOAD_FAST                'self'
              158  STORE_ATTR               _next
            160_0  COME_FROM           130  '130'

 L. 361       160  LOAD_FAST                'self'
              162  DUP_TOP          
              164  LOAD_ATTR                _cumul_msg_len
              166  LOAD_GLOBAL              len
              168  LOAD_FAST                'plaintext'
              170  CALL_FUNCTION_1       1  ''
              172  INPLACE_ADD      
              174  ROT_TWO          
              176  STORE_ATTR               _cumul_msg_len

 L. 362       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _cumul_msg_len
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                _msg_len
              186  COMPARE_OP               >
              188  POP_JUMP_IF_FALSE   198  'to 198'

 L. 363       190  LOAD_GLOBAL              ValueError
              192  LOAD_STR                 'Message is too long'
              194  CALL_FUNCTION_1       1  ''
              196  RAISE_VARARGS_1       1  'exception instance'
            198_0  COME_FROM           188  '188'

 L. 365       198  LOAD_FAST                'self'
              200  LOAD_ATTR                _mac_status
              202  LOAD_GLOBAL              MacStatus
              204  LOAD_ATTR                PROCESSING_AUTH_DATA
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   226  'to 226'

 L. 369       210  LOAD_FAST                'self'
              212  LOAD_METHOD              _pad_cache_and_update
              214  CALL_METHOD_0         0  ''
              216  POP_TOP          

 L. 370       218  LOAD_GLOBAL              MacStatus
              220  LOAD_ATTR                PROCESSING_PLAINTEXT
              222  LOAD_FAST                'self'
              224  STORE_ATTR               _mac_status
            226_0  COME_FROM           208  '208'

 L. 372       226  LOAD_FAST                'self'
              228  LOAD_METHOD              _update
              230  LOAD_FAST                'plaintext'
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          

 L. 373       236  LOAD_FAST                'self'
              238  LOAD_ATTR                _cipher
              240  LOAD_ATTR                encrypt
              242  LOAD_FAST                'plaintext'
              244  LOAD_FAST                'output'
              246  LOAD_CONST               ('output',)
              248  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              250  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def decrypt--- This code section failed: ---

 L. 412         0  LOAD_FAST                'self'
                2  LOAD_ATTR                decrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 413        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'decrypt() can only be called after initialization or an update()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 415        20  LOAD_FAST                'self'
               22  LOAD_ATTR                decrypt
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                verify
               28  BUILD_LIST_2          2 
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _next

 L. 418        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _assoc_len
               38  LOAD_CONST               None
               40  <117>                 0  ''
               42  POP_JUMP_IF_FALSE   102  'to 102'

 L. 419        44  LOAD_GLOBAL              isinstance
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _cache
               50  LOAD_GLOBAL              list
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_TRUE     60  'to 60'
               56  <74>             
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            54  '54'

 L. 420        60  LOAD_GLOBAL              sum
               62  LOAD_LISTCOMP            '<code_object <listcomp>>'
               64  LOAD_STR                 'CcmMode.decrypt.<locals>.<listcomp>'
               66  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _cache
               72  GET_ITER         
               74  CALL_FUNCTION_1       1  ''
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_FAST                'self'
               80  STORE_ATTR               _assoc_len

 L. 421        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _msg_len
               86  LOAD_CONST               None
               88  <117>                 1  ''
               90  POP_JUMP_IF_FALSE   122  'to 122'

 L. 422        92  LOAD_FAST                'self'
               94  LOAD_METHOD              _start_mac
               96  CALL_METHOD_0         0  ''
               98  POP_TOP          
              100  JUMP_FORWARD        122  'to 122'
            102_0  COME_FROM            42  '42'

 L. 424       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _cumul_assoc_len
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                _assoc_len
              110  COMPARE_OP               <
              112  POP_JUMP_IF_FALSE   122  'to 122'

 L. 425       114  LOAD_GLOBAL              ValueError
              116  LOAD_STR                 'Associated data is too short'
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           112  '112'
            122_1  COME_FROM           100  '100'
            122_2  COME_FROM            90  '90'

 L. 429       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _msg_len
              126  LOAD_CONST               None
              128  <117>                 0  ''
              130  POP_JUMP_IF_FALSE   160  'to 160'

 L. 430       132  LOAD_GLOBAL              len
              134  LOAD_FAST                'ciphertext'
              136  CALL_FUNCTION_1       1  ''
              138  LOAD_FAST                'self'
              140  STORE_ATTR               _msg_len

 L. 431       142  LOAD_FAST                'self'
              144  LOAD_METHOD              _start_mac
              146  CALL_METHOD_0         0  ''
              148  POP_TOP          

 L. 432       150  LOAD_FAST                'self'
              152  LOAD_ATTR                verify
              154  BUILD_LIST_1          1 
              156  LOAD_FAST                'self'
              158  STORE_ATTR               _next
            160_0  COME_FROM           130  '130'

 L. 434       160  LOAD_FAST                'self'
              162  DUP_TOP          
              164  LOAD_ATTR                _cumul_msg_len
              166  LOAD_GLOBAL              len
              168  LOAD_FAST                'ciphertext'
              170  CALL_FUNCTION_1       1  ''
              172  INPLACE_ADD      
              174  ROT_TWO          
              176  STORE_ATTR               _cumul_msg_len

 L. 435       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _cumul_msg_len
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                _msg_len
              186  COMPARE_OP               >
              188  POP_JUMP_IF_FALSE   198  'to 198'

 L. 436       190  LOAD_GLOBAL              ValueError
              192  LOAD_STR                 'Message is too long'
              194  CALL_FUNCTION_1       1  ''
              196  RAISE_VARARGS_1       1  'exception instance'
            198_0  COME_FROM           188  '188'

 L. 438       198  LOAD_FAST                'self'
              200  LOAD_ATTR                _mac_status
              202  LOAD_GLOBAL              MacStatus
              204  LOAD_ATTR                PROCESSING_AUTH_DATA
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   226  'to 226'

 L. 442       210  LOAD_FAST                'self'
              212  LOAD_METHOD              _pad_cache_and_update
              214  CALL_METHOD_0         0  ''
              216  POP_TOP          

 L. 443       218  LOAD_GLOBAL              MacStatus
              220  LOAD_ATTR                PROCESSING_PLAINTEXT
              222  LOAD_FAST                'self'
              224  STORE_ATTR               _mac_status
            226_0  COME_FROM           208  '208'

 L. 446       226  LOAD_FAST                'self'
              228  LOAD_ATTR                _cipher
              230  LOAD_ATTR                encrypt
              232  LOAD_FAST                'ciphertext'
              234  LOAD_FAST                'output'
              236  LOAD_CONST               ('output',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  STORE_FAST               'plaintext'

 L. 447       242  LOAD_FAST                'output'
              244  LOAD_CONST               None
              246  <117>                 0  ''
          248_250  POP_JUMP_IF_FALSE   264  'to 264'

 L. 448       252  LOAD_FAST                'self'
              254  LOAD_METHOD              _update
              256  LOAD_FAST                'plaintext'
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          
              262  JUMP_FORWARD        274  'to 274'
            264_0  COME_FROM           248  '248'

 L. 450       264  LOAD_FAST                'self'
              266  LOAD_METHOD              _update
              268  LOAD_FAST                'output'
              270  CALL_METHOD_1         1  ''
              272  POP_TOP          
            274_0  COME_FROM           262  '262'

 L. 451       274  LOAD_FAST                'plaintext'
              276  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def digest--- This code section failed: ---

 L. 464         0  LOAD_FAST                'self'
                2  LOAD_ATTR                digest
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 465        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'digest() cannot be called when decrypting or validating a message'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 467        20  LOAD_FAST                'self'
               22  LOAD_ATTR                digest
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 468        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _digest
               34  CALL_METHOD_0         0  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _digest--- This code section failed: ---

 L. 471         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _mac_tag
                4  POP_JUMP_IF_FALSE    12  'to 12'

 L. 472         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _mac_tag
               10  RETURN_VALUE     
             12_0  COME_FROM             4  '4'

 L. 474        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _assoc_len
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    80  'to 80'

 L. 475        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _cache
               28  LOAD_GLOBAL              list
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_TRUE     38  'to 38'
               34  <74>             
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            32  '32'

 L. 476        38  LOAD_GLOBAL              sum
               40  LOAD_LISTCOMP            '<code_object <listcomp>>'
               42  LOAD_STR                 'CcmMode._digest.<locals>.<listcomp>'
               44  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _cache
               50  GET_ITER         
               52  CALL_FUNCTION_1       1  ''
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _assoc_len

 L. 477        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _msg_len
               64  LOAD_CONST               None
               66  <117>                 1  ''
               68  POP_JUMP_IF_FALSE   100  'to 100'

 L. 478        70  LOAD_FAST                'self'
               72  LOAD_METHOD              _start_mac
               74  CALL_METHOD_0         0  ''
               76  POP_TOP          
               78  JUMP_FORWARD        100  'to 100'
             80_0  COME_FROM            20  '20'

 L. 480        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _cumul_assoc_len
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _assoc_len
               88  COMPARE_OP               <
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L. 481        92  LOAD_GLOBAL              ValueError
               94  LOAD_STR                 'Associated data is too short'
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            90  '90'
            100_1  COME_FROM            78  '78'
            100_2  COME_FROM            68  '68'

 L. 483       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _msg_len
              104  LOAD_CONST               None
              106  <117>                 0  ''
              108  POP_JUMP_IF_FALSE   124  'to 124'

 L. 484       110  LOAD_CONST               0
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _msg_len

 L. 485       116  LOAD_FAST                'self'
              118  LOAD_METHOD              _start_mac
              120  CALL_METHOD_0         0  ''
              122  POP_TOP          
            124_0  COME_FROM           108  '108'

 L. 487       124  LOAD_FAST                'self'
              126  LOAD_ATTR                _cumul_msg_len
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                _msg_len
              132  COMPARE_OP               !=
              134  POP_JUMP_IF_FALSE   144  'to 144'

 L. 488       136  LOAD_GLOBAL              ValueError
              138  LOAD_STR                 'Message is too short'
              140  CALL_FUNCTION_1       1  ''
              142  RAISE_VARARGS_1       1  'exception instance'
            144_0  COME_FROM           134  '134'

 L. 493       144  LOAD_FAST                'self'
              146  LOAD_METHOD              _pad_cache_and_update
              148  CALL_METHOD_0         0  ''
              150  POP_TOP          

 L. 496       152  LOAD_GLOBAL              strxor
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                _t
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                _s_0
              162  CALL_FUNCTION_2       2  ''
              164  LOAD_CONST               None
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                _mac_len
              170  BUILD_SLICE_2         2 
              172  BINARY_SUBSCR    
              174  LOAD_FAST                'self'
              176  STORE_ATTR               _mac_tag

 L. 498       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _mac_tag
              182  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18

    def hexdigest(self):
        """Compute the *printable* MAC tag.

        This method is like `digest`.

        :Return: the MAC, as a hexadecimal string.
        """
        return ''.join['%02x' % bord(x) for x in self.digest]

    def verify--- This code section failed: ---

 L. 526         0  LOAD_FAST                'self'
                2  LOAD_ATTR                verify
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 527        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'verify() cannot be called when encrypting a message'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 529        20  LOAD_FAST                'self'
               22  LOAD_ATTR                verify
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 531        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _digest
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          

 L. 532        38  LOAD_GLOBAL              get_random_bytes
               40  LOAD_CONST               16
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'secret'

 L. 534        46  LOAD_GLOBAL              BLAKE2s
               48  LOAD_ATTR                new
               50  LOAD_CONST               160
               52  LOAD_FAST                'secret'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _mac_tag
               58  LOAD_CONST               ('digest_bits', 'key', 'data')
               60  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               62  STORE_FAST               'mac1'

 L. 535        64  LOAD_GLOBAL              BLAKE2s
               66  LOAD_ATTR                new
               68  LOAD_CONST               160
               70  LOAD_FAST                'secret'
               72  LOAD_FAST                'received_mac_tag'
               74  LOAD_CONST               ('digest_bits', 'key', 'data')
               76  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               78  STORE_FAST               'mac2'

 L. 537        80  LOAD_FAST                'mac1'
               82  LOAD_METHOD              digest
               84  CALL_METHOD_0         0  ''
               86  LOAD_FAST                'mac2'
               88  LOAD_METHOD              digest
               90  CALL_METHOD_0         0  ''
               92  COMPARE_OP               !=
               94  POP_JUMP_IF_FALSE   104  'to 104'

 L. 538        96  LOAD_GLOBAL              ValueError
               98  LOAD_STR                 'MAC check failed'
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            94  '94'

Parse error at or near `None' instruction at offset -1

    def hexverify(self, hex_mac_tag):
        """Validate the *printable* MAC tag.

        This method is like `verify`.

        :Parameters:
          hex_mac_tag : string
            This is the *printable* MAC, as received from the sender.
        :Raises ValueError:
            if the MAC does not match. The message has been tampered with
            or the key is incorrect.
        """
        self.verifyunhexlify(hex_mac_tag)

    def encrypt_and_digest(self, plaintext, output=None):
        """Perform encrypt() and digest() in one step.

        :Parameters:
          plaintext : bytes/bytearray/memoryview
            The piece of data to encrypt.
        :Keywords:
          output : bytearray/memoryview
            The location where the ciphertext must be written to.
            If ``None``, the ciphertext is returned.
        :Return:
            a tuple with two items:

            - the ciphertext, as ``bytes``
            - the MAC tag, as ``bytes``

            The first item becomes ``None`` when the ``output`` parameter
            specified a location for the result.
        """
        return (
         self.encrypt(plaintext, output=output), self.digest)

    def decrypt_and_verify(self, ciphertext, received_mac_tag, output=None):
        """Perform decrypt() and verify() in one step.

        :Parameters:
          ciphertext : bytes/bytearray/memoryview
            The piece of data to decrypt.
          received_mac_tag : bytes/bytearray/memoryview
            This is the *binary* MAC, as received from the sender.
        :Keywords:
          output : bytearray/memoryview
            The location where the plaintext must be written to.
            If ``None``, the plaintext is returned.
        :Return: the plaintext as ``bytes`` or ``None`` when the ``output``
            parameter specified a location for the result.
        :Raises ValueError:
            if the MAC does not match. The message has been tampered with
            or the key is incorrect.
        """
        plaintext = self.decrypt(ciphertext, output=output)
        self.verifyreceived_mac_tag
        return plaintext


def _create_ccm_cipher--- This code section failed: ---

 L. 636         0  SETUP_FINALLY        20  'to 20'

 L. 637         2  LOAD_FAST                'kwargs'
                4  LOAD_METHOD              pop
                6  LOAD_STR                 'key'
                8  CALL_METHOD_1         1  ''
               10  DUP_TOP          
               12  STORE_FAST               'key'
               14  STORE_FAST               'key'
               16  POP_BLOCK        
               18  JUMP_FORWARD         72  'to 72'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 638        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  <121>                70  ''
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        62  'to 62'

 L. 639        34  LOAD_GLOBAL              TypeError
               36  LOAD_STR                 'Missing parameter: '
               38  LOAD_GLOBAL              str
               40  LOAD_FAST                'e'
               42  CALL_FUNCTION_1       1  ''
               44  BINARY_ADD       
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
               50  POP_BLOCK        
               52  POP_EXCEPT       
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  JUMP_FORWARD         72  'to 72'
             62_0  COME_FROM_FINALLY    32  '32'
               62  LOAD_CONST               None
               64  STORE_FAST               'e'
               66  DELETE_FAST              'e'
               68  <48>             
               70  <48>             
             72_0  COME_FROM            60  '60'
             72_1  COME_FROM            18  '18'

 L. 641        72  LOAD_FAST                'kwargs'
               74  LOAD_METHOD              pop
               76  LOAD_STR                 'nonce'
               78  LOAD_CONST               None
               80  CALL_METHOD_2         2  ''
               82  STORE_FAST               'nonce'

 L. 642        84  LOAD_FAST                'nonce'
               86  LOAD_CONST               None
               88  <117>                 0  ''
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L. 643        92  LOAD_GLOBAL              get_random_bytes
               94  LOAD_CONST               11
               96  CALL_FUNCTION_1       1  ''
               98  STORE_FAST               'nonce'
            100_0  COME_FROM            90  '90'

 L. 644       100  LOAD_FAST                'kwargs'
              102  LOAD_METHOD              pop
              104  LOAD_STR                 'mac_len'
              106  LOAD_FAST                'factory'
              108  LOAD_ATTR                block_size
              110  CALL_METHOD_2         2  ''
              112  STORE_FAST               'mac_len'

 L. 645       114  LOAD_FAST                'kwargs'
              116  LOAD_METHOD              pop
              118  LOAD_STR                 'msg_len'
              120  LOAD_CONST               None
              122  CALL_METHOD_2         2  ''
              124  STORE_FAST               'msg_len'

 L. 646       126  LOAD_FAST                'kwargs'
              128  LOAD_METHOD              pop
              130  LOAD_STR                 'assoc_len'
              132  LOAD_CONST               None
              134  CALL_METHOD_2         2  ''
              136  STORE_FAST               'assoc_len'

 L. 647       138  LOAD_GLOBAL              dict
              140  LOAD_FAST                'kwargs'
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'cipher_params'

 L. 649       146  LOAD_GLOBAL              CcmMode
              148  LOAD_FAST                'factory'
              150  LOAD_FAST                'key'
              152  LOAD_FAST                'nonce'
              154  LOAD_FAST                'mac_len'
              156  LOAD_FAST                'msg_len'

 L. 650       158  LOAD_FAST                'assoc_len'
              160  LOAD_FAST                'cipher_params'

 L. 649       162  CALL_FUNCTION_7       7  ''
              164  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 24