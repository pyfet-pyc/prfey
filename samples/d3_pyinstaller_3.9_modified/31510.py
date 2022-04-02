# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\fernet.py
from __future__ import absolute_import, division, print_function
import base64, binascii, os, struct, time, six
from cryptography import utils
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC

class InvalidToken(Exception):
    pass


_MAX_CLOCK_SKEW = 60

class Fernet(object):

    def __init__(self, key, backend=None):
        backend = _get_backend(backend)
        key = base64.urlsafe_b64decode(key)
        if len(key) != 32:
            raise ValueError('Fernet key must be 32 url-safe base64-encoded bytes.')
        self._signing_key = key[:16]
        self._encryption_key = key[16:]
        self._backend = backend

    @classmethod
    def generate_key(cls):
        return base64.urlsafe_b64encode(os.urandom(32))

    def encrypt(self, data):
        return self.encrypt_at_time(data, int(time.time()))

    def encrypt_at_time(self, data, current_time):
        iv = os.urandom(16)
        return self._encrypt_from_parts(data, current_time, iv)

    def _encrypt_from_parts(self, data, current_time, iv):
        utils._check_bytes('data', data)
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        encryptor = Cipher(algorithms.AES(self._encryption_key), modes.CBC(iv), self._backend).encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        basic_parts = b'\x80' + struct.pack('>Q', current_time) + iv + ciphertext
        h = HMAC((self._signing_key), (hashes.SHA256()), backend=(self._backend))
        h.update(basic_parts)
        hmac = h.finalize()
        return base64.urlsafe_b64encode(basic_parts + hmac)

    def decrypt(self, token, ttl=None):
        timestamp, data = Fernet._get_unverified_token_data(token)
        return self._decrypt_data(data, timestamp, ttl, int(time.time()))

    def decrypt_at_time--- This code section failed: ---

 L.  79         0  LOAD_FAST                'ttl'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  80         8  LOAD_GLOBAL              ValueError

 L.  81        10  LOAD_STR                 'decrypt_at_time() can only be used with a non-None ttl'

 L.  80        12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  83        16  LOAD_GLOBAL              Fernet
               18  LOAD_METHOD              _get_unverified_token_data
               20  LOAD_FAST                'token'
               22  CALL_METHOD_1         1  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'timestamp'
               28  STORE_FAST               'data'

 L.  84        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _decrypt_data
               34  LOAD_FAST                'data'
               36  LOAD_FAST                'timestamp'
               38  LOAD_FAST                'ttl'
               40  LOAD_FAST                'current_time'
               42  CALL_METHOD_4         4  ''
               44  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def extract_timestamp(self, token):
        timestamp, data = Fernet._get_unverified_token_data(token)
        self._verify_signature(data)
        return timestamp

    @staticmethod
    def _get_unverified_token_data--- This code section failed: ---

 L.  94         0  LOAD_GLOBAL              utils
                2  LOAD_METHOD              _check_bytes
                4  LOAD_STR                 'token'
                6  LOAD_FAST                'token'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L.  95        12  SETUP_FINALLY        28  'to 28'

 L.  96        14  LOAD_GLOBAL              base64
               16  LOAD_METHOD              urlsafe_b64decode
               18  LOAD_FAST                'token'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'data'
               24  POP_BLOCK        
               26  JUMP_FORWARD         56  'to 56'
             28_0  COME_FROM_FINALLY    12  '12'

 L.  97        28  DUP_TOP          
               30  LOAD_GLOBAL              TypeError
               32  LOAD_GLOBAL              binascii
               34  LOAD_ATTR                Error
               36  BUILD_TUPLE_2         2 
               38  <121>                54  ''
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L.  98        46  LOAD_GLOBAL              InvalidToken
               48  RAISE_VARARGS_1       1  'exception instance'
               50  POP_EXCEPT       
               52  JUMP_FORWARD         56  'to 56'
               54  <48>             
             56_0  COME_FROM            52  '52'
             56_1  COME_FROM            26  '26'

 L. 100        56  LOAD_FAST                'data'
               58  POP_JUMP_IF_FALSE    76  'to 76'
               60  LOAD_GLOBAL              six
               62  LOAD_METHOD              indexbytes
               64  LOAD_FAST                'data'
               66  LOAD_CONST               0
               68  CALL_METHOD_2         2  ''
               70  LOAD_CONST               128
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_FALSE    80  'to 80'
             76_0  COME_FROM            58  '58'

 L. 101        76  LOAD_GLOBAL              InvalidToken
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            74  '74'

 L. 103        80  SETUP_FINALLY       108  'to 108'

 L. 104        82  LOAD_GLOBAL              struct
               84  LOAD_METHOD              unpack
               86  LOAD_STR                 '>Q'
               88  LOAD_FAST                'data'
               90  LOAD_CONST               1
               92  LOAD_CONST               9
               94  BUILD_SLICE_2         2 
               96  BINARY_SUBSCR    
               98  CALL_METHOD_2         2  ''
              100  UNPACK_SEQUENCE_1     1 
              102  STORE_FAST               'timestamp'
              104  POP_BLOCK        
              106  JUMP_FORWARD        132  'to 132'
            108_0  COME_FROM_FINALLY    80  '80'

 L. 105       108  DUP_TOP          
              110  LOAD_GLOBAL              struct
              112  LOAD_ATTR                error
              114  <121>               130  ''
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 106       122  LOAD_GLOBAL              InvalidToken
              124  RAISE_VARARGS_1       1  'exception instance'
              126  POP_EXCEPT       
              128  JUMP_FORWARD        132  'to 132'
              130  <48>             
            132_0  COME_FROM           128  '128'
            132_1  COME_FROM           106  '106'

 L. 107       132  LOAD_FAST                'timestamp'
              134  LOAD_FAST                'data'
              136  BUILD_TUPLE_2         2 
              138  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 38

    def _verify_signature--- This code section failed: ---

 L. 110         0  LOAD_GLOBAL              HMAC
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _signing_key
                6  LOAD_GLOBAL              hashes
                8  LOAD_METHOD              SHA256
               10  CALL_METHOD_0         0  ''
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _backend
               16  LOAD_CONST               ('backend',)
               18  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               20  STORE_FAST               'h'

 L. 111        22  LOAD_FAST                'h'
               24  LOAD_METHOD              update
               26  LOAD_FAST                'data'
               28  LOAD_CONST               None
               30  LOAD_CONST               -32
               32  BUILD_SLICE_2         2 
               34  BINARY_SUBSCR    
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 112        40  SETUP_FINALLY        64  'to 64'

 L. 113        42  LOAD_FAST                'h'
               44  LOAD_METHOD              verify
               46  LOAD_FAST                'data'
               48  LOAD_CONST               -32
               50  LOAD_CONST               None
               52  BUILD_SLICE_2         2 
               54  BINARY_SUBSCR    
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_BLOCK        
               62  JUMP_FORWARD         86  'to 86'
             64_0  COME_FROM_FINALLY    40  '40'

 L. 114        64  DUP_TOP          
               66  LOAD_GLOBAL              InvalidSignature
               68  <121>                84  ''
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 115        76  LOAD_GLOBAL              InvalidToken
               78  RAISE_VARARGS_1       1  'exception instance'
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
               84  <48>             
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            62  '62'

Parse error at or near `<121>' instruction at offset 68

    def _decrypt_data--- This code section failed: ---

 L. 118         0  LOAD_FAST                'ttl'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    40  'to 40'

 L. 119         8  LOAD_FAST                'timestamp'
               10  LOAD_FAST                'ttl'
               12  BINARY_ADD       
               14  LOAD_FAST                'current_time'
               16  COMPARE_OP               <
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 120        20  LOAD_GLOBAL              InvalidToken
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            18  '18'

 L. 122        24  LOAD_FAST                'current_time'
               26  LOAD_GLOBAL              _MAX_CLOCK_SKEW
               28  BINARY_ADD       
               30  LOAD_FAST                'timestamp'
               32  COMPARE_OP               <
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L. 123        36  LOAD_GLOBAL              InvalidToken
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            34  '34'
             40_1  COME_FROM             6  '6'

 L. 125        40  LOAD_FAST                'self'
               42  LOAD_METHOD              _verify_signature
               44  LOAD_FAST                'data'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L. 127        50  LOAD_FAST                'data'
               52  LOAD_CONST               9
               54  LOAD_CONST               25
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  STORE_FAST               'iv'

 L. 128        62  LOAD_FAST                'data'
               64  LOAD_CONST               25
               66  LOAD_CONST               -32
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  STORE_FAST               'ciphertext'

 L. 129        74  LOAD_GLOBAL              Cipher

 L. 130        76  LOAD_GLOBAL              algorithms
               78  LOAD_METHOD              AES
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _encryption_key
               84  CALL_METHOD_1         1  ''
               86  LOAD_GLOBAL              modes
               88  LOAD_METHOD              CBC
               90  LOAD_FAST                'iv'
               92  CALL_METHOD_1         1  ''
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                _backend

 L. 129        98  CALL_FUNCTION_3       3  ''
              100  LOAD_METHOD              decryptor
              102  CALL_METHOD_0         0  ''
              104  STORE_FAST               'decryptor'

 L. 132       106  LOAD_FAST                'decryptor'
              108  LOAD_METHOD              update
              110  LOAD_FAST                'ciphertext'
              112  CALL_METHOD_1         1  ''
              114  STORE_FAST               'plaintext_padded'

 L. 133       116  SETUP_FINALLY       134  'to 134'

 L. 134       118  LOAD_FAST                'plaintext_padded'
              120  LOAD_FAST                'decryptor'
              122  LOAD_METHOD              finalize
              124  CALL_METHOD_0         0  ''
              126  INPLACE_ADD      
              128  STORE_FAST               'plaintext_padded'
              130  POP_BLOCK        
              132  JUMP_FORWARD        156  'to 156'
            134_0  COME_FROM_FINALLY   116  '116'

 L. 135       134  DUP_TOP          
              136  LOAD_GLOBAL              ValueError
              138  <121>               154  ''
              140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L. 136       146  LOAD_GLOBAL              InvalidToken
              148  RAISE_VARARGS_1       1  'exception instance'
              150  POP_EXCEPT       
              152  JUMP_FORWARD        156  'to 156'
              154  <48>             
            156_0  COME_FROM           152  '152'
            156_1  COME_FROM           132  '132'

 L. 137       156  LOAD_GLOBAL              padding
              158  LOAD_METHOD              PKCS7
              160  LOAD_GLOBAL              algorithms
              162  LOAD_ATTR                AES
              164  LOAD_ATTR                block_size
              166  CALL_METHOD_1         1  ''
              168  LOAD_METHOD              unpadder
              170  CALL_METHOD_0         0  ''
              172  STORE_FAST               'unpadder'

 L. 139       174  LOAD_FAST                'unpadder'
              176  LOAD_METHOD              update
              178  LOAD_FAST                'plaintext_padded'
              180  CALL_METHOD_1         1  ''
              182  STORE_FAST               'unpadded'

 L. 140       184  SETUP_FINALLY       202  'to 202'

 L. 141       186  LOAD_FAST                'unpadded'
              188  LOAD_FAST                'unpadder'
              190  LOAD_METHOD              finalize
              192  CALL_METHOD_0         0  ''
              194  INPLACE_ADD      
              196  STORE_FAST               'unpadded'
              198  POP_BLOCK        
              200  JUMP_FORWARD        224  'to 224'
            202_0  COME_FROM_FINALLY   184  '184'

 L. 142       202  DUP_TOP          
              204  LOAD_GLOBAL              ValueError
              206  <121>               222  ''
              208  POP_TOP          
              210  POP_TOP          
              212  POP_TOP          

 L. 143       214  LOAD_GLOBAL              InvalidToken
              216  RAISE_VARARGS_1       1  'exception instance'
              218  POP_EXCEPT       
              220  JUMP_FORWARD        224  'to 224'
              222  <48>             
            224_0  COME_FROM           220  '220'
            224_1  COME_FROM           200  '200'

 L. 144       224  LOAD_FAST                'unpadded'
              226  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class MultiFernet(object):

    def __init__(self, fernets):
        fernets = list(fernets)
        if not fernets:
            raise ValueError('MultiFernet requires at least one Fernet instance')
        self._fernets = fernets

    def encrypt(self, msg):
        return self.encrypt_at_time(msg, int(time.time()))

    def encrypt_at_time(self, msg, current_time):
        return self._fernets[0].encrypt_at_time(msg, current_time)

    def rotate--- This code section failed: ---

 L. 163         0  LOAD_GLOBAL              Fernet
                2  LOAD_METHOD              _get_unverified_token_data
                4  LOAD_FAST                'msg'
                6  CALL_METHOD_1         1  ''
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'timestamp'
               12  STORE_FAST               'data'

 L. 164        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _fernets
               18  GET_ITER         
             20_0  COME_FROM            70  '70'
             20_1  COME_FROM            66  '66'
             20_2  COME_FROM            50  '50'
               20  FOR_ITER             72  'to 72'
               22  STORE_FAST               'f'

 L. 165        24  SETUP_FINALLY        52  'to 52'

 L. 166        26  LOAD_FAST                'f'
               28  LOAD_METHOD              _decrypt_data
               30  LOAD_FAST                'data'
               32  LOAD_FAST                'timestamp'
               34  LOAD_CONST               None
               36  LOAD_CONST               None
               38  CALL_METHOD_4         4  ''
               40  STORE_FAST               'p'

 L. 167        42  POP_BLOCK        
               44  POP_TOP          
               46  JUMP_FORWARD         76  'to 76'
               48  POP_BLOCK        
               50  JUMP_BACK            20  'to 20'
             52_0  COME_FROM_FINALLY    24  '24'

 L. 168        52  DUP_TOP          
               54  LOAD_GLOBAL              InvalidToken
               56  <121>                68  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 169        64  POP_EXCEPT       
               66  JUMP_BACK            20  'to 20'
               68  <48>             
               70  JUMP_BACK            20  'to 20'
             72_0  COME_FROM            20  '20'

 L. 171        72  LOAD_GLOBAL              InvalidToken
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            46  '46'

 L. 173        76  LOAD_GLOBAL              os
               78  LOAD_METHOD              urandom
               80  LOAD_CONST               16
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'iv'

 L. 174        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _fernets
               90  LOAD_CONST               0
               92  BINARY_SUBSCR    
               94  LOAD_METHOD              _encrypt_from_parts
               96  LOAD_FAST                'p'
               98  LOAD_FAST                'timestamp'
              100  LOAD_FAST                'iv'
              102  CALL_METHOD_3         3  ''
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 56

    def decrypt--- This code section failed: ---

 L. 177         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _fernets
                4  GET_ITER         
              6_0  COME_FROM            48  '48'
              6_1  COME_FROM            44  '44'
                6  FOR_ITER             50  'to 50'
                8  STORE_FAST               'f'

 L. 178        10  SETUP_FINALLY        30  'to 30'

 L. 179        12  LOAD_FAST                'f'
               14  LOAD_METHOD              decrypt
               16  LOAD_FAST                'msg'
               18  LOAD_FAST                'ttl'
               20  CALL_METHOD_2         2  ''
               22  POP_BLOCK        
               24  ROT_TWO          
               26  POP_TOP          
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY    10  '10'

 L. 180        30  DUP_TOP          
               32  LOAD_GLOBAL              InvalidToken
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 181        42  POP_EXCEPT       
               44  JUMP_BACK             6  'to 6'
               46  <48>             
               48  JUMP_BACK             6  'to 6'
             50_0  COME_FROM             6  '6'

 L. 182        50  LOAD_GLOBAL              InvalidToken
               52  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 24

    def decrypt_at_time--- This code section failed: ---

 L. 185         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _fernets
                4  GET_ITER         
              6_0  COME_FROM            50  '50'
              6_1  COME_FROM            46  '46'
                6  FOR_ITER             52  'to 52'
                8  STORE_FAST               'f'

 L. 186        10  SETUP_FINALLY        32  'to 32'

 L. 187        12  LOAD_FAST                'f'
               14  LOAD_METHOD              decrypt_at_time
               16  LOAD_FAST                'msg'
               18  LOAD_FAST                'ttl'
               20  LOAD_FAST                'current_time'
               22  CALL_METHOD_3         3  ''
               24  POP_BLOCK        
               26  ROT_TWO          
               28  POP_TOP          
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY    10  '10'

 L. 188        32  DUP_TOP          
               34  LOAD_GLOBAL              InvalidToken
               36  <121>                48  ''
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 189        44  POP_EXCEPT       
               46  JUMP_BACK             6  'to 6'
               48  <48>             
               50  JUMP_BACK             6  'to 6'
             52_0  COME_FROM             6  '6'

 L. 190        52  LOAD_GLOBAL              InvalidToken
               54  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 26