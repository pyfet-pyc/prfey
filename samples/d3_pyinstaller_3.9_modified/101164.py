# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Cipher\_mode_eax.py
"""
EAX mode.
"""
__all__ = [
 'EaxMode']
import struct
from binascii import unhexlify
from Crypto.Util.py3compat import byte_string, bord, _copy_bytes
from Crypto.Util._raw_api import is_buffer
import Crypto.Util.strxor as strxor
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Hash import CMAC, BLAKE2s
from Crypto.Random import get_random_bytes

class EaxMode(object):
    __doc__ = '*EAX* mode.\n\n    This is an Authenticated Encryption with Associated Data\n    (`AEAD`_) mode. It provides both confidentiality and authenticity.\n\n    The header of the message may be left in the clear, if needed,\n    and it will still be subject to authentication.\n\n    The decryption step tells the receiver if the message comes\n    from a source that really knowns the secret key.\n    Additionally, decryption detects if any part of the message -\n    including the header - has been modified or corrupted.\n\n    This mode requires a *nonce*.\n\n    This mode is only available for ciphers that operate on 64 or\n    128 bits blocks.\n\n    There are no official standards defining EAX.\n    The implementation is based on `a proposal`__ that\n    was presented to NIST.\n\n    .. _AEAD: http://blog.cryptographyengineering.com/2012/05/how-to-choose-authenticated-encryption.html\n    .. __: http://csrc.nist.gov/groups/ST/toolkit/BCM/documents/proposedmodes/eax/eax-spec.pdf\n\n    :undocumented: __init__\n    '

    def __init__--- This code section failed: ---

 L.  83         0  LOAD_DEREF               'factory'
                2  LOAD_ATTR                block_size
                4  LOAD_DEREF               'self'
                6  STORE_ATTR               block_size

 L.  86         8  LOAD_GLOBAL              _copy_bytes
               10  LOAD_CONST               None
               12  LOAD_CONST               None
               14  LOAD_FAST                'nonce'
               16  CALL_FUNCTION_3       3  ''
               18  LOAD_DEREF               'self'
               20  STORE_ATTR               nonce

 L.  89        22  LOAD_FAST                'mac_len'
               24  LOAD_DEREF               'self'
               26  STORE_ATTR               _mac_len

 L.  90        28  LOAD_CONST               None
               30  LOAD_DEREF               'self'
               32  STORE_ATTR               _mac_tag

 L.  93        34  LOAD_DEREF               'self'
               36  LOAD_ATTR                update
               38  LOAD_DEREF               'self'
               40  LOAD_ATTR                encrypt
               42  LOAD_DEREF               'self'
               44  LOAD_ATTR                decrypt

 L.  94        46  LOAD_DEREF               'self'
               48  LOAD_ATTR                digest
               50  LOAD_DEREF               'self'
               52  LOAD_ATTR                verify

 L.  93        54  BUILD_LIST_5          5 
               56  LOAD_DEREF               'self'
               58  STORE_ATTR               _next

 L.  97        60  LOAD_CONST               4
               62  LOAD_DEREF               'self'
               64  LOAD_ATTR                _mac_len
               66  DUP_TOP          
               68  ROT_THREE        
               70  COMPARE_OP               <=
               72  POP_JUMP_IF_FALSE    84  'to 84'
               74  LOAD_DEREF               'self'
               76  LOAD_ATTR                block_size
               78  COMPARE_OP               <=
               80  POP_JUMP_IF_TRUE    100  'to 100'
               82  JUMP_FORWARD         86  'to 86'
             84_0  COME_FROM            72  '72'
               84  POP_TOP          
             86_0  COME_FROM            82  '82'

 L.  98        86  LOAD_GLOBAL              ValueError
               88  LOAD_STR                 "Parameter 'mac_len' must not be larger than %d"

 L.  99        90  LOAD_DEREF               'self'
               92  LOAD_ATTR                block_size

 L.  98        94  BINARY_MODULO    
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            80  '80'

 L. 102       100  LOAD_GLOBAL              len
              102  LOAD_DEREF               'self'
              104  LOAD_ATTR                nonce
              106  CALL_FUNCTION_1       1  ''
              108  LOAD_CONST               0
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   122  'to 122'

 L. 103       114  LOAD_GLOBAL              ValueError
              116  LOAD_STR                 'Nonce cannot be empty in EAX mode'
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           112  '112'

 L. 104       122  LOAD_GLOBAL              is_buffer
              124  LOAD_FAST                'nonce'
              126  CALL_FUNCTION_1       1  ''
              128  POP_JUMP_IF_TRUE    138  'to 138'

 L. 105       130  LOAD_GLOBAL              TypeError
              132  LOAD_STR                 'nonce must be bytes, bytearray or memoryview'
              134  CALL_FUNCTION_1       1  ''
              136  RAISE_VARARGS_1       1  'exception instance'
            138_0  COME_FROM           128  '128'

 L. 107       138  LOAD_CLOSURE             'cipher_params'
              140  LOAD_CLOSURE             'factory'
              142  LOAD_CLOSURE             'key'
              144  LOAD_CLOSURE             'self'
              146  BUILD_TUPLE_4         4 
              148  LOAD_LISTCOMP            '<code_object <listcomp>>'
              150  LOAD_STR                 'EaxMode.__init__.<locals>.<listcomp>'
              152  MAKE_FUNCTION_8          'closure'

 L. 112       154  LOAD_GLOBAL              range
              156  LOAD_CONST               0
              158  LOAD_CONST               3
              160  CALL_FUNCTION_2       2  ''

 L. 107       162  GET_ITER         
              164  CALL_FUNCTION_1       1  ''
              166  LOAD_DEREF               'self'
              168  STORE_ATTR               _omac

 L. 116       170  LOAD_DEREF               'self'
              172  LOAD_ATTR                _omac
              174  LOAD_CONST               0
              176  BINARY_SUBSCR    
              178  LOAD_METHOD              update
              180  LOAD_DEREF               'self'
              182  LOAD_ATTR                nonce
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          

 L. 117       188  LOAD_DEREF               'self'
              190  LOAD_ATTR                _omac
              192  LOAD_CONST               1
              194  BINARY_SUBSCR    
              196  LOAD_DEREF               'self'
              198  STORE_ATTR               _signer

 L. 120       200  LOAD_GLOBAL              bytes_to_long
              202  LOAD_DEREF               'self'
              204  LOAD_ATTR                _omac
              206  LOAD_CONST               0
              208  BINARY_SUBSCR    
              210  LOAD_METHOD              digest
              212  CALL_METHOD_0         0  ''
              214  CALL_FUNCTION_1       1  ''
              216  STORE_FAST               'counter_int'

 L. 121       218  LOAD_DEREF               'factory'
              220  LOAD_ATTR                new
              222  LOAD_DEREF               'key'

 L. 122       224  LOAD_DEREF               'factory'
              226  LOAD_ATTR                MODE_CTR

 L. 121       228  BUILD_TUPLE_2         2 

 L. 123       230  LOAD_FAST                'counter_int'

 L. 124       232  LOAD_CONST               b''

 L. 121       234  LOAD_CONST               ('initial_value', 'nonce')
              236  BUILD_CONST_KEY_MAP_2     2 

 L. 125       238  LOAD_DEREF               'cipher_params'

 L. 121       240  <164>                 1  ''
              242  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              244  LOAD_DEREF               'self'
              246  STORE_ATTR               _cipher

Parse error at or near `<164>' instruction at offset 240

    def update--- This code section failed: ---

 L. 148         0  LOAD_FAST                'self'
                2  LOAD_ATTR                update
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 149        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'update() can only be called immediately after initialization'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 152        20  LOAD_FAST                'self'
               22  LOAD_ATTR                update
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                encrypt
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                decrypt

 L. 153        32  LOAD_FAST                'self'
               34  LOAD_ATTR                digest
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                verify

 L. 152        40  BUILD_LIST_5          5 
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _next

 L. 155        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _signer
               50  LOAD_METHOD              update
               52  LOAD_FAST                'assoc_data'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L. 156        58  LOAD_FAST                'self'
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def encrypt--- This code section failed: ---

 L. 191         0  LOAD_FAST                'self'
                2  LOAD_ATTR                encrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 192        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'encrypt() can only be called after initialization or an update()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 194        20  LOAD_FAST                'self'
               22  LOAD_ATTR                encrypt
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                digest
               28  BUILD_LIST_2          2 
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _next

 L. 195        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _cipher
               38  LOAD_ATTR                encrypt
               40  LOAD_FAST                'plaintext'
               42  LOAD_FAST                'output'
               44  LOAD_CONST               ('output',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  STORE_FAST               'ct'

 L. 196        50  LOAD_FAST                'output'
               52  LOAD_CONST               None
               54  <117>                 0  ''
               56  POP_JUMP_IF_FALSE    76  'to 76'

 L. 197        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _omac
               62  LOAD_CONST               2
               64  BINARY_SUBSCR    
               66  LOAD_METHOD              update
               68  LOAD_FAST                'ct'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
               74  JUMP_FORWARD         92  'to 92'
             76_0  COME_FROM            56  '56'

 L. 199        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _omac
               80  LOAD_CONST               2
               82  BINARY_SUBSCR    
               84  LOAD_METHOD              update
               86  LOAD_FAST                'output'
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          
             92_0  COME_FROM            74  '74'

 L. 200        92  LOAD_FAST                'ct'
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def decrypt--- This code section failed: ---

 L. 235         0  LOAD_FAST                'self'
                2  LOAD_ATTR                decrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 236        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'decrypt() can only be called after initialization or an update()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 238        20  LOAD_FAST                'self'
               22  LOAD_ATTR                decrypt
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                verify
               28  BUILD_LIST_2          2 
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _next

 L. 239        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _omac
               38  LOAD_CONST               2
               40  BINARY_SUBSCR    
               42  LOAD_METHOD              update
               44  LOAD_FAST                'ciphertext'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L. 240        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _cipher
               54  LOAD_ATTR                decrypt
               56  LOAD_FAST                'ciphertext'
               58  LOAD_FAST                'output'
               60  LOAD_CONST               ('output',)
               62  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def digest--- This code section failed: ---

 L. 253         0  LOAD_FAST                'self'
                2  LOAD_ATTR                digest
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 254        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'digest() cannot be called when decrypting or validating a message'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 256        20  LOAD_FAST                'self'
               22  LOAD_ATTR                digest
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 258        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _mac_tag
               34  POP_JUMP_IF_TRUE     96  'to 96'

 L. 259        36  LOAD_CONST               b'\x00'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                block_size
               42  BINARY_MULTIPLY  
               44  STORE_FAST               'tag'

 L. 260        46  LOAD_GLOBAL              range
               48  LOAD_CONST               3
               50  CALL_FUNCTION_1       1  ''
               52  GET_ITER         
             54_0  COME_FROM            78  '78'
               54  FOR_ITER             80  'to 80'
               56  STORE_FAST               'i'

 L. 261        58  LOAD_GLOBAL              strxor
               60  LOAD_FAST                'tag'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _omac
               66  LOAD_FAST                'i'
               68  BINARY_SUBSCR    
               70  LOAD_METHOD              digest
               72  CALL_METHOD_0         0  ''
               74  CALL_FUNCTION_2       2  ''
               76  STORE_FAST               'tag'
               78  JUMP_BACK            54  'to 54'
             80_0  COME_FROM            54  '54'

 L. 262        80  LOAD_FAST                'tag'
               82  LOAD_CONST               None
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _mac_len
               88  BUILD_SLICE_2         2 
               90  BINARY_SUBSCR    
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _mac_tag
             96_0  COME_FROM            34  '34'

 L. 264        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _mac_tag
              100  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def hexdigest(self):
        """Compute the *printable* MAC tag.

        This method is like `digest`.

        :Return: the MAC, as a hexadecimal string.
        """
        return ''.join['%02x' % bord(x) for x in self.digest]

    def verify--- This code section failed: ---

 L. 292         0  LOAD_FAST                'self'
                2  LOAD_ATTR                verify
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 293        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'verify() cannot be called when encrypting a message'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 295        20  LOAD_FAST                'self'
               22  LOAD_ATTR                verify
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 297        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _mac_tag
               34  POP_JUMP_IF_TRUE     96  'to 96'

 L. 298        36  LOAD_CONST               b'\x00'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                block_size
               42  BINARY_MULTIPLY  
               44  STORE_FAST               'tag'

 L. 299        46  LOAD_GLOBAL              range
               48  LOAD_CONST               3
               50  CALL_FUNCTION_1       1  ''
               52  GET_ITER         
             54_0  COME_FROM            78  '78'
               54  FOR_ITER             80  'to 80'
               56  STORE_FAST               'i'

 L. 300        58  LOAD_GLOBAL              strxor
               60  LOAD_FAST                'tag'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _omac
               66  LOAD_FAST                'i'
               68  BINARY_SUBSCR    
               70  LOAD_METHOD              digest
               72  CALL_METHOD_0         0  ''
               74  CALL_FUNCTION_2       2  ''
               76  STORE_FAST               'tag'
               78  JUMP_BACK            54  'to 54'
             80_0  COME_FROM            54  '54'

 L. 301        80  LOAD_FAST                'tag'
               82  LOAD_CONST               None
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _mac_len
               88  BUILD_SLICE_2         2 
               90  BINARY_SUBSCR    
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _mac_tag
             96_0  COME_FROM            34  '34'

 L. 303        96  LOAD_GLOBAL              get_random_bytes
               98  LOAD_CONST               16
              100  CALL_FUNCTION_1       1  ''
              102  STORE_FAST               'secret'

 L. 305       104  LOAD_GLOBAL              BLAKE2s
              106  LOAD_ATTR                new
              108  LOAD_CONST               160
              110  LOAD_FAST                'secret'
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                _mac_tag
              116  LOAD_CONST               ('digest_bits', 'key', 'data')
              118  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              120  STORE_FAST               'mac1'

 L. 306       122  LOAD_GLOBAL              BLAKE2s
              124  LOAD_ATTR                new
              126  LOAD_CONST               160
              128  LOAD_FAST                'secret'
              130  LOAD_FAST                'received_mac_tag'
              132  LOAD_CONST               ('digest_bits', 'key', 'data')
              134  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              136  STORE_FAST               'mac2'

 L. 308       138  LOAD_FAST                'mac1'
              140  LOAD_METHOD              digest
              142  CALL_METHOD_0         0  ''
              144  LOAD_FAST                'mac2'
              146  LOAD_METHOD              digest
              148  CALL_METHOD_0         0  ''
              150  COMPARE_OP               !=
              152  POP_JUMP_IF_FALSE   162  'to 162'

 L. 309       154  LOAD_GLOBAL              ValueError
              156  LOAD_STR                 'MAC check failed'
              158  CALL_FUNCTION_1       1  ''
              160  RAISE_VARARGS_1       1  'exception instance'
            162_0  COME_FROM           152  '152'

Parse error at or near `None' instruction at offset -1

    def hexverify(self, hex_mac_tag):
        """Validate the *printable* MAC tag.

        This method is like `verify`.

        :Parameters:
          hex_mac_tag : string
            This is the *printable* MAC, as received from the sender.
        :Raises MacMismatchError:
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
        :Raises MacMismatchError:
            if the MAC does not match. The message has been tampered with
            or the key is incorrect.
        """
        pt = self.decrypt(ciphertext, output=output)
        self.verifyreceived_mac_tag
        return pt


def _create_eax_cipher--- This code section failed: ---

 L. 399         0  SETUP_FINALLY        58  'to 58'

 L. 400         2  LOAD_FAST                'kwargs'
                4  LOAD_METHOD              pop
                6  LOAD_STR                 'key'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'key'

 L. 401        12  LOAD_FAST                'kwargs'
               14  LOAD_METHOD              pop
               16  LOAD_STR                 'nonce'
               18  LOAD_CONST               None
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'nonce'

 L. 402        24  LOAD_FAST                'nonce'
               26  LOAD_CONST               None
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L. 403        32  LOAD_GLOBAL              get_random_bytes
               34  LOAD_CONST               16
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'nonce'
             40_0  COME_FROM            30  '30'

 L. 404        40  LOAD_FAST                'kwargs'
               42  LOAD_METHOD              pop
               44  LOAD_STR                 'mac_len'
               46  LOAD_FAST                'factory'
               48  LOAD_ATTR                block_size
               50  CALL_METHOD_2         2  ''
               52  STORE_FAST               'mac_len'
               54  POP_BLOCK        
               56  JUMP_FORWARD        110  'to 110'
             58_0  COME_FROM_FINALLY     0  '0'

 L. 405        58  DUP_TOP          
               60  LOAD_GLOBAL              KeyError
               62  <121>               108  ''
               64  POP_TOP          
               66  STORE_FAST               'e'
               68  POP_TOP          
               70  SETUP_FINALLY       100  'to 100'

 L. 406        72  LOAD_GLOBAL              TypeError
               74  LOAD_STR                 'Missing parameter: '
               76  LOAD_GLOBAL              str
               78  LOAD_FAST                'e'
               80  CALL_FUNCTION_1       1  ''
               82  BINARY_ADD       
               84  CALL_FUNCTION_1       1  ''
               86  RAISE_VARARGS_1       1  'exception instance'
               88  POP_BLOCK        
               90  POP_EXCEPT       
               92  LOAD_CONST               None
               94  STORE_FAST               'e'
               96  DELETE_FAST              'e'
               98  JUMP_FORWARD        110  'to 110'
            100_0  COME_FROM_FINALLY    70  '70'
              100  LOAD_CONST               None
              102  STORE_FAST               'e'
              104  DELETE_FAST              'e'
              106  <48>             
              108  <48>             
            110_0  COME_FROM            98  '98'
            110_1  COME_FROM            56  '56'

 L. 408       110  LOAD_GLOBAL              EaxMode
              112  LOAD_FAST                'factory'
              114  LOAD_FAST                'key'
              116  LOAD_FAST                'nonce'
              118  LOAD_FAST                'mac_len'
              120  LOAD_FAST                'kwargs'
              122  CALL_FUNCTION_5       5  ''
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 28