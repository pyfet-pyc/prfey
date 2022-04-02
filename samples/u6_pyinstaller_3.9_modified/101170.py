# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Cipher\_mode_siv.py
"""
Synthetic Initialization Vector (SIV) mode.
"""
__all__ = [
 'SivMode']
from binascii import hexlify, unhexlify
from Crypto.Util.py3compat import bord, _copy_bytes
from Crypto.Util._raw_api import is_buffer
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Protocol.KDF import _S2V
from Crypto.Hash import BLAKE2s
from Crypto.Random import get_random_bytes

class SivMode(object):
    __doc__ = 'Synthetic Initialization Vector (SIV).\n\n    This is an Authenticated Encryption with Associated Data (`AEAD`_) mode.\n    It provides both confidentiality and authenticity.\n\n    The header of the message may be left in the clear, if needed, and it will\n    still be subject to authentication. The decryption step tells the receiver\n    if the message comes from a source that really knowns the secret key.\n    Additionally, decryption detects if any part of the message - including the\n    header - has been modified or corrupted.\n\n    Unlike other AEAD modes such as CCM, EAX or GCM, accidental reuse of a\n    nonce is not catastrophic for the confidentiality of the message. The only\n    effect is that an attacker can tell when the same plaintext (and same\n    associated data) is protected with the same key.\n\n    The length of the MAC is fixed to the block size of the underlying cipher.\n    The key size is twice the length of the key of the underlying cipher.\n\n    This mode is only available for AES ciphers.\n\n    +--------------------+---------------+-------------------+\n    |      Cipher        | SIV MAC size  |   SIV key length  |\n    |                    |    (bytes)    |     (bytes)       |\n    +====================+===============+===================+\n    |    AES-128         |      16       |        32         |\n    +--------------------+---------------+-------------------+\n    |    AES-192         |      16       |        48         |\n    +--------------------+---------------+-------------------+\n    |    AES-256         |      16       |        64         |\n    +--------------------+---------------+-------------------+\n\n    See `RFC5297`_ and the `original paper`__.\n\n    .. _RFC5297: https://tools.ietf.org/html/rfc5297\n    .. _AEAD: http://blog.cryptographyengineering.com/2012/05/how-to-choose-authenticated-encryption.html\n    .. __: http://www.cs.ucdavis.edu/~rogaway/papers/keywrap.pdf\n\n    :undocumented: __init__\n    '

    def __init__--- This code section failed: ---

 L.  93         0  LOAD_FAST                'factory'
                2  LOAD_ATTR                block_size
                4  LOAD_FAST                'self'
                6  STORE_ATTR               block_size

 L.  96         8  LOAD_FAST                'factory'
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _factory

 L.  98        14  LOAD_FAST                'kwargs'
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _cipher_params

 L. 100        20  LOAD_GLOBAL              len
               22  LOAD_FAST                'key'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_CONST               (32, 48, 64)
               28  <118>                 1  ''
               30  POP_JUMP_IF_FALSE    48  'to 48'

 L. 101        32  LOAD_GLOBAL              ValueError
               34  LOAD_STR                 'Incorrect key length (%d bytes)'
               36  LOAD_GLOBAL              len
               38  LOAD_FAST                'key'
               40  CALL_FUNCTION_1       1  ''
               42  BINARY_MODULO    
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            30  '30'

 L. 103        48  LOAD_FAST                'nonce'
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_FALSE   106  'to 106'

 L. 104        56  LOAD_GLOBAL              is_buffer
               58  LOAD_FAST                'nonce'
               60  CALL_FUNCTION_1       1  ''
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L. 105        64  LOAD_GLOBAL              TypeError
               66  LOAD_STR                 'When provided, the nonce must be bytes, bytearray or memoryview'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L. 107        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'nonce'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_CONST               0
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE    92  'to 92'

 L. 108        84  LOAD_GLOBAL              ValueError
               86  LOAD_STR                 'When provided, the nonce must be non-empty'
               88  CALL_FUNCTION_1       1  ''
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            82  '82'

 L. 110        92  LOAD_GLOBAL              _copy_bytes
               94  LOAD_CONST               None
               96  LOAD_CONST               None
               98  LOAD_FAST                'nonce'
              100  CALL_FUNCTION_3       3  ''
              102  LOAD_FAST                'self'
              104  STORE_ATTR               nonce
            106_0  COME_FROM            54  '54'

 L. 114       106  LOAD_GLOBAL              len
              108  LOAD_FAST                'key'
              110  CALL_FUNCTION_1       1  ''
              112  LOAD_CONST               2
              114  BINARY_FLOOR_DIVIDE
              116  STORE_FAST               'subkey_size'

 L. 116       118  LOAD_CONST               None
              120  LOAD_FAST                'self'
              122  STORE_ATTR               _mac_tag

 L. 117       124  LOAD_GLOBAL              _S2V
              126  LOAD_FAST                'key'
              128  LOAD_CONST               None
              130  LOAD_FAST                'subkey_size'
              132  BUILD_SLICE_2         2 
              134  BINARY_SUBSCR    

 L. 118       136  LOAD_FAST                'factory'

 L. 119       138  LOAD_FAST                'self'
              140  LOAD_ATTR                _cipher_params

 L. 117       142  LOAD_CONST               ('ciphermod', 'cipher_params')
              144  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              146  LOAD_FAST                'self'
              148  STORE_ATTR               _kdf

 L. 120       150  LOAD_FAST                'key'
              152  LOAD_FAST                'subkey_size'
              154  LOAD_CONST               None
              156  BUILD_SLICE_2         2 
              158  BINARY_SUBSCR    
              160  LOAD_FAST                'self'
              162  STORE_ATTR               _subkey_cipher

 L. 123       164  LOAD_FAST                'factory'
              166  LOAD_ATTR                new
              168  LOAD_FAST                'key'
              170  LOAD_CONST               None
              172  LOAD_FAST                'subkey_size'
              174  BUILD_SLICE_2         2 
              176  BINARY_SUBSCR    
              178  LOAD_FAST                'factory'
              180  LOAD_ATTR                MODE_ECB
              182  BUILD_TUPLE_2         2 
              184  BUILD_MAP_0           0 
              186  LOAD_FAST                'kwargs'
              188  <164>                 1  ''
              190  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              192  POP_TOP          

 L. 126       194  LOAD_FAST                'self'
              196  LOAD_ATTR                update
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                encrypt
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                decrypt

 L. 127       206  LOAD_FAST                'self'
              208  LOAD_ATTR                digest
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                verify

 L. 126       214  BUILD_LIST_5          5 
              216  LOAD_FAST                'self'
              218  STORE_ATTR               _next

Parse error at or near `<118>' instruction at offset 28

    def _create_ctr_cipher--- This code section failed: ---

 L. 132         0  LOAD_GLOBAL              bytes_to_long
                2  LOAD_FAST                'v'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'v_int'

 L. 133         8  LOAD_FAST                'v_int'
               10  LOAD_CONST               340282366920938463454151235392765951999
               12  BINARY_AND       
               14  STORE_FAST               'q'

 L. 134        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _factory
               20  LOAD_ATTR                new

 L. 135        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _subkey_cipher

 L. 136        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _factory
               30  LOAD_ATTR                MODE_CTR

 L. 134        32  BUILD_TUPLE_2         2 

 L. 137        34  LOAD_FAST                'q'

 L. 138        36  LOAD_CONST               b''

 L. 134        38  LOAD_CONST               ('initial_value', 'nonce')
               40  BUILD_CONST_KEY_MAP_2     2 

 L. 139        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _cipher_params

 L. 134        46  <164>                 1  ''
               48  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 46

    def update--- This code section failed: ---

 L. 167         0  LOAD_FAST                'self'
                2  LOAD_ATTR                update
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 168        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'update() can only be called immediately after initialization'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 171        20  LOAD_FAST                'self'
               22  LOAD_ATTR                update
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                encrypt
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                decrypt

 L. 172        32  LOAD_FAST                'self'
               34  LOAD_ATTR                digest
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                verify

 L. 171        40  BUILD_LIST_5          5 
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _next

 L. 174        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _kdf
               50  LOAD_METHOD              update
               52  LOAD_FAST                'component'
               54  CALL_METHOD_1         1  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def encrypt(self, plaintext):
        """
        For SIV, encryption and MAC authentication must take place at the same
        point. This method shall not be used.

        Use `encrypt_and_digest` instead.
        """
        raise TypeError('encrypt() not allowed for SIV mode. Use encrypt_and_digest() instead.')

    def decrypt(self, ciphertext):
        """
        For SIV, decryption and verification must take place at the same
        point. This method shall not be used.

        Use `decrypt_and_verify` instead.
        """
        raise TypeError('decrypt() not allowed for SIV mode. Use decrypt_and_verify() instead.')

    def digest--- This code section failed: ---

 L. 209         0  LOAD_FAST                'self'
                2  LOAD_ATTR                digest
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 210        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'digest() cannot be called when decrypting or validating a message'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 212        20  LOAD_FAST                'self'
               22  LOAD_ATTR                digest
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 213        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _mac_tag
               34  LOAD_CONST               None
               36  <117>                 0  ''
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L. 214        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _kdf
               44  LOAD_METHOD              derive
               46  CALL_METHOD_0         0  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _mac_tag
             52_0  COME_FROM            38  '38'

 L. 215        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _mac_tag
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def hexdigest(self):
        """Compute the *printable* MAC tag.

        This method is like `digest`.

        :Return: the MAC, as a hexadecimal string.
        """
        return ''.join['%02x' % bord(x) for x in self.digest]

    def verify--- This code section failed: ---

 L. 243         0  LOAD_FAST                'self'
                2  LOAD_ATTR                verify
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 244        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'verify() cannot be called when encrypting a message'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 246        20  LOAD_FAST                'self'
               22  LOAD_ATTR                verify
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 248        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _mac_tag
               34  LOAD_CONST               None
               36  <117>                 0  ''
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L. 249        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _kdf
               44  LOAD_METHOD              derive
               46  CALL_METHOD_0         0  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _mac_tag
             52_0  COME_FROM            38  '38'

 L. 251        52  LOAD_GLOBAL              get_random_bytes
               54  LOAD_CONST               16
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'secret'

 L. 253        60  LOAD_GLOBAL              BLAKE2s
               62  LOAD_ATTR                new
               64  LOAD_CONST               160
               66  LOAD_FAST                'secret'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _mac_tag
               72  LOAD_CONST               ('digest_bits', 'key', 'data')
               74  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               76  STORE_FAST               'mac1'

 L. 254        78  LOAD_GLOBAL              BLAKE2s
               80  LOAD_ATTR                new
               82  LOAD_CONST               160
               84  LOAD_FAST                'secret'
               86  LOAD_FAST                'received_mac_tag'
               88  LOAD_CONST               ('digest_bits', 'key', 'data')
               90  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               92  STORE_FAST               'mac2'

 L. 256        94  LOAD_FAST                'mac1'
               96  LOAD_METHOD              digest
               98  CALL_METHOD_0         0  ''
              100  LOAD_FAST                'mac2'
              102  LOAD_METHOD              digest
              104  CALL_METHOD_0         0  ''
              106  COMPARE_OP               !=
              108  POP_JUMP_IF_FALSE   118  'to 118'

 L. 257       110  LOAD_GLOBAL              ValueError
              112  LOAD_STR                 'MAC check failed'
              114  CALL_FUNCTION_1       1  ''
              116  RAISE_VARARGS_1       1  'exception instance'
            118_0  COME_FROM           108  '108'

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

    def encrypt_and_digest--- This code section failed: ---

 L. 294         0  LOAD_FAST                'self'
                2  LOAD_ATTR                encrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 295        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'encrypt() can only be called after initialization or an update()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 298        20  LOAD_FAST                'self'
               22  LOAD_ATTR                digest
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 301        30  LOAD_GLOBAL              hasattr
               32  LOAD_FAST                'self'
               34  LOAD_STR                 'nonce'
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_FALSE    54  'to 54'

 L. 302        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _kdf
               44  LOAD_METHOD              update
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                nonce
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          
             54_0  COME_FROM            38  '38'

 L. 303        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _kdf
               58  LOAD_METHOD              update
               60  LOAD_FAST                'plaintext'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 304        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _kdf
               70  LOAD_METHOD              derive
               72  CALL_METHOD_0         0  ''
               74  LOAD_FAST                'self'
               76  STORE_ATTR               _mac_tag

 L. 306        78  LOAD_FAST                'self'
               80  LOAD_METHOD              _create_ctr_cipher
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                _mac_tag
               86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'cipher'

 L. 308        90  LOAD_FAST                'cipher'
               92  LOAD_ATTR                encrypt
               94  LOAD_FAST                'plaintext'
               96  LOAD_FAST                'output'
               98  LOAD_CONST               ('output',)
              100  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                _mac_tag
              106  BUILD_TUPLE_2         2 
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def decrypt_and_verify--- This code section failed: ---

 L. 339         0  LOAD_FAST                'self'
                2  LOAD_ATTR                decrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 340        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'decrypt() can only be called after initialization or an update()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 342        20  LOAD_FAST                'self'
               22  LOAD_ATTR                verify
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 345        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _create_ctr_cipher
               34  LOAD_FAST                'mac_tag'
               36  CALL_METHOD_1         1  ''
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _cipher

 L. 347        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _cipher
               46  LOAD_ATTR                decrypt
               48  LOAD_FAST                'ciphertext'
               50  LOAD_FAST                'output'
               52  LOAD_CONST               ('output',)
               54  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               56  STORE_FAST               'plaintext'

 L. 349        58  LOAD_GLOBAL              hasattr
               60  LOAD_FAST                'self'
               62  LOAD_STR                 'nonce'
               64  CALL_FUNCTION_2       2  ''
               66  POP_JUMP_IF_FALSE    82  'to 82'

 L. 350        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _kdf
               72  LOAD_METHOD              update
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                nonce
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
             82_0  COME_FROM            66  '66'

 L. 351        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _kdf
               86  LOAD_METHOD              update
               88  LOAD_FAST                'output'
               90  LOAD_CONST               None
               92  <117>                 0  ''
               94  POP_JUMP_IF_FALSE   100  'to 100'
               96  LOAD_FAST                'plaintext'
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            94  '94'
              100  LOAD_FAST                'output'
            102_0  COME_FROM            98  '98'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L. 352       106  LOAD_FAST                'self'
              108  LOAD_METHOD              verify
              110  LOAD_FAST                'mac_tag'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

 L. 354       116  LOAD_FAST                'plaintext'
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _create_siv_cipher--- This code section failed: ---

 L. 385         0  SETUP_FINALLY        16  'to 16'

 L. 386         2  LOAD_FAST                'kwargs'
                4  LOAD_METHOD              pop
                6  LOAD_STR                 'key'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'key'
               12  POP_BLOCK        
               14  JUMP_FORWARD         68  'to 68'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 387        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  <121>                66  ''
               22  POP_TOP          
               24  STORE_FAST               'e'
               26  POP_TOP          
               28  SETUP_FINALLY        58  'to 58'

 L. 388        30  LOAD_GLOBAL              TypeError
               32  LOAD_STR                 'Missing parameter: '
               34  LOAD_GLOBAL              str
               36  LOAD_FAST                'e'
               38  CALL_FUNCTION_1       1  ''
               40  BINARY_ADD       
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_BLOCK        
               48  POP_EXCEPT       
               50  LOAD_CONST               None
               52  STORE_FAST               'e'
               54  DELETE_FAST              'e'
               56  JUMP_FORWARD         68  'to 68'
             58_0  COME_FROM_FINALLY    28  '28'
               58  LOAD_CONST               None
               60  STORE_FAST               'e'
               62  DELETE_FAST              'e'
               64  <48>             
               66  <48>             
             68_0  COME_FROM            56  '56'
             68_1  COME_FROM            14  '14'

 L. 390        68  LOAD_FAST                'kwargs'
               70  LOAD_METHOD              pop
               72  LOAD_STR                 'nonce'
               74  LOAD_CONST               None
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'nonce'

 L. 392        80  LOAD_GLOBAL              SivMode
               82  LOAD_FAST                'factory'
               84  LOAD_FAST                'key'
               86  LOAD_FAST                'nonce'
               88  LOAD_FAST                'kwargs'
               90  CALL_FUNCTION_4       4  ''
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 20