# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Cipher\_mode_openpgp.py
"""
OpenPGP mode.
"""
__all__ = [
 'OpenPgpMode']
from Crypto.Util.py3compat import _copy_bytes
from Crypto.Random import get_random_bytes

class OpenPgpMode(object):
    __doc__ = 'OpenPGP mode.\n\n    This mode is a variant of CFB, and it is only used in PGP and\n    OpenPGP_ applications. If in doubt, use another mode.\n\n    An Initialization Vector (*IV*) is required.\n\n    Unlike CFB, the *encrypted* IV (not the IV itself) is\n    transmitted to the receiver.\n\n    The IV is a random data block. For legacy reasons, two of its bytes are\n    duplicated to act as a checksum for the correctness of the key, which is now\n    known to be insecure and is ignored. The encrypted IV is therefore 2 bytes\n    longer than the clean IV.\n\n    .. _OpenPGP: http://tools.ietf.org/html/rfc4880\n\n    :undocumented: __init__\n    '

    def __init__--- This code section failed: ---

 L.  64         0  LOAD_FAST                'factory'
                2  LOAD_ATTR                block_size
                4  LOAD_FAST                'self'
                6  STORE_ATTR               block_size

 L.  66         8  LOAD_CONST               False
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _done_first_block

 L.  69        14  LOAD_FAST                'factory'
               16  LOAD_ATTR                new

 L.  70        18  LOAD_FAST                'key'

 L.  71        20  LOAD_FAST                'factory'
               22  LOAD_ATTR                MODE_CFB

 L.  69        24  BUILD_TUPLE_2         2 

 L.  72        26  LOAD_CONST               b'\x00'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                block_size
               32  BINARY_MULTIPLY  

 L.  73        34  LOAD_FAST                'self'
               36  LOAD_ATTR                block_size
               38  LOAD_CONST               8
               40  BINARY_MULTIPLY  

 L.  69        42  LOAD_CONST               ('IV', 'segment_size')
               44  BUILD_CONST_KEY_MAP_2     2 

 L.  74        46  LOAD_FAST                'cipher_params'

 L.  69        48  <164>                 1  ''
               50  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               52  STORE_FAST               'IV_cipher'

 L.  76        54  LOAD_GLOBAL              _copy_bytes
               56  LOAD_CONST               None
               58  LOAD_CONST               None
               60  LOAD_FAST                'iv'
               62  CALL_FUNCTION_3       3  ''
               64  STORE_FAST               'iv'

 L.  79        66  LOAD_GLOBAL              len
               68  LOAD_FAST                'iv'
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                block_size
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   106  'to 106'

 L.  81        80  LOAD_FAST                'IV_cipher'
               82  LOAD_METHOD              encrypt
               84  LOAD_FAST                'iv'
               86  LOAD_FAST                'iv'
               88  LOAD_CONST               -2
               90  LOAD_CONST               None
               92  BUILD_SLICE_2         2 
               94  BINARY_SUBSCR    
               96  BINARY_ADD       
               98  CALL_METHOD_1         1  ''
              100  LOAD_FAST                'self'
              102  STORE_ATTR               _encrypted_IV
              104  JUMP_FORWARD        174  'to 174'
            106_0  COME_FROM            78  '78'

 L.  82       106  LOAD_GLOBAL              len
              108  LOAD_FAST                'iv'
              110  CALL_FUNCTION_1       1  ''
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                block_size
              116  LOAD_CONST               2
              118  BINARY_ADD       
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   150  'to 150'

 L.  84       124  LOAD_FAST                'iv'
              126  LOAD_FAST                'self'
              128  STORE_ATTR               _encrypted_IV

 L.  87       130  LOAD_FAST                'IV_cipher'
              132  LOAD_METHOD              decrypt
              134  LOAD_FAST                'iv'
              136  CALL_METHOD_1         1  ''
              138  LOAD_CONST               None
              140  LOAD_CONST               -2
              142  BUILD_SLICE_2         2 
              144  BINARY_SUBSCR    
              146  STORE_FAST               'iv'
              148  JUMP_FORWARD        174  'to 174'
            150_0  COME_FROM           122  '122'

 L.  89       150  LOAD_GLOBAL              ValueError
              152  LOAD_STR                 'Length of IV must be %d or %d bytes for MODE_OPENPGP'

 L.  91       154  LOAD_FAST                'self'
              156  LOAD_ATTR                block_size
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                block_size
              162  LOAD_CONST               2
              164  BINARY_ADD       
              166  BUILD_TUPLE_2         2 

 L.  89       168  BINARY_MODULO    
              170  CALL_FUNCTION_1       1  ''
              172  RAISE_VARARGS_1       1  'exception instance'
            174_0  COME_FROM           148  '148'
            174_1  COME_FROM           104  '104'

 L.  93       174  LOAD_FAST                'iv'
              176  DUP_TOP          
              178  LOAD_FAST                'self'
              180  STORE_ATTR               iv
              182  LOAD_FAST                'self'
              184  STORE_ATTR               IV

 L.  96       186  LOAD_FAST                'factory'
              188  LOAD_ATTR                new

 L.  97       190  LOAD_FAST                'key'

 L.  98       192  LOAD_FAST                'factory'
              194  LOAD_ATTR                MODE_CFB

 L.  96       196  BUILD_TUPLE_2         2 

 L.  99       198  LOAD_FAST                'self'
              200  LOAD_ATTR                _encrypted_IV
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                block_size
              206  UNARY_NEGATIVE   
              208  LOAD_CONST               None
              210  BUILD_SLICE_2         2 
              212  BINARY_SUBSCR    

 L. 100       214  LOAD_FAST                'self'
              216  LOAD_ATTR                block_size
              218  LOAD_CONST               8
              220  BINARY_MULTIPLY  

 L.  96       222  LOAD_CONST               ('IV', 'segment_size')
              224  BUILD_CONST_KEY_MAP_2     2 

 L. 101       226  LOAD_FAST                'cipher_params'

 L.  96       228  <164>                 1  ''
              230  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              232  LOAD_FAST                'self'
              234  STORE_ATTR               _cipher

Parse error at or near `<164>' instruction at offset 48

    def encrypt(self, plaintext):
        """Encrypt data with the key and the parameters set at initialization.

        A cipher object is stateful: once you have encrypted a message
        you cannot encrypt (or decrypt) another message using the same
        object.

        The data to encrypt can be broken up in two or
        more pieces and `encrypt` can be called multiple times.

        That is, the statement:

            >>> c.encrypt(a) + c.encrypt(b)

        is equivalent to:

             >>> c.encrypt(a+b)

        This function does not add any padding to the plaintext.

        :Parameters:
          plaintext : bytes/bytearray/memoryview
            The piece of data to encrypt.

        :Return:
            the encrypted data, as a byte string.
            It is as long as *plaintext* with one exception:
            when encrypting the first message chunk,
            the encypted IV is prepended to the returned ciphertext.
        """
        res = self._cipher.encryptplaintext
        if not self._done_first_block:
            res = self._encrypted_IV + res
            self._done_first_block = True
        return res

    def decrypt(self, ciphertext):
        """Decrypt data with the key and the parameters set at initialization.

        A cipher object is stateful: once you have decrypted a message
        you cannot decrypt (or encrypt) another message with the same
        object.

        The data to decrypt can be broken up in two or
        more pieces and `decrypt` can be called multiple times.

        That is, the statement:

            >>> c.decrypt(a) + c.decrypt(b)

        is equivalent to:

             >>> c.decrypt(a+b)

        This function does not remove any padding from the plaintext.

        :Parameters:
          ciphertext : bytes/bytearray/memoryview
            The piece of data to decrypt.

        :Return: the decrypted data (byte string).
        """
        return self._cipher.decryptciphertext


def _create_openpgp_cipher--- This code section failed: ---

 L. 190         0  LOAD_FAST                'kwargs'
                2  LOAD_METHOD              pop
                4  LOAD_STR                 'IV'
                6  LOAD_CONST               None
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'iv'

 L. 191        12  LOAD_FAST                'kwargs'
               14  LOAD_METHOD              pop
               16  LOAD_STR                 'iv'
               18  LOAD_CONST               None
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'IV'

 L. 193        24  LOAD_CONST               (None, None)
               26  LOAD_FAST                'iv'
               28  LOAD_FAST                'IV'
               30  BUILD_TUPLE_2         2 
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    46  'to 46'

 L. 194        36  LOAD_GLOBAL              get_random_bytes
               38  LOAD_FAST                'factory'
               40  LOAD_ATTR                block_size
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'iv'
             46_0  COME_FROM            34  '34'

 L. 195        46  LOAD_FAST                'iv'
               48  LOAD_CONST               None
               50  <117>                 1  ''
               52  POP_JUMP_IF_FALSE    72  'to 72'

 L. 196        54  LOAD_FAST                'IV'
               56  LOAD_CONST               None
               58  <117>                 1  ''
               60  POP_JUMP_IF_FALSE    76  'to 76'

 L. 197        62  LOAD_GLOBAL              TypeError
               64  LOAD_STR                 "You must either use 'iv' or 'IV', not both"
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
               70  JUMP_FORWARD         76  'to 76'
             72_0  COME_FROM            52  '52'

 L. 199        72  LOAD_FAST                'IV'
               74  STORE_FAST               'iv'
             76_0  COME_FROM            70  '70'
             76_1  COME_FROM            60  '60'

 L. 201        76  SETUP_FINALLY        92  'to 92'

 L. 202        78  LOAD_FAST                'kwargs'
               80  LOAD_METHOD              pop
               82  LOAD_STR                 'key'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'key'
               88  POP_BLOCK        
               90  JUMP_FORWARD        144  'to 144'
             92_0  COME_FROM_FINALLY    76  '76'

 L. 203        92  DUP_TOP          
               94  LOAD_GLOBAL              KeyError
               96  <121>               142  ''
               98  POP_TOP          
              100  STORE_FAST               'e'
              102  POP_TOP          
              104  SETUP_FINALLY       134  'to 134'

 L. 204       106  LOAD_GLOBAL              TypeError
              108  LOAD_STR                 'Missing component: '
              110  LOAD_GLOBAL              str
              112  LOAD_FAST                'e'
              114  CALL_FUNCTION_1       1  ''
              116  BINARY_ADD       
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
              122  POP_BLOCK        
              124  POP_EXCEPT       
              126  LOAD_CONST               None
              128  STORE_FAST               'e'
              130  DELETE_FAST              'e'
              132  JUMP_FORWARD        144  'to 144'
            134_0  COME_FROM_FINALLY   104  '104'
              134  LOAD_CONST               None
              136  STORE_FAST               'e'
              138  DELETE_FAST              'e'
              140  <48>             
              142  <48>             
            144_0  COME_FROM           132  '132'
            144_1  COME_FROM            90  '90'

 L. 206       144  LOAD_GLOBAL              OpenPgpMode
              146  LOAD_FAST                'factory'
              148  LOAD_FAST                'key'
              150  LOAD_FAST                'iv'
              152  LOAD_FAST                'kwargs'
              154  CALL_FUNCTION_4       4  ''
              156  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 50