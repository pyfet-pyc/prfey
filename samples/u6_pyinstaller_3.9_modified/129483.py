# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\padding.py
import typing
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives._asymmetric import AsymmetricPadding
from cryptography.hazmat.primitives.asymmetric import rsa

class PKCS1v15(AsymmetricPadding):
    name = 'EMSA-PKCS1-v1_5'


class PSS(AsymmetricPadding):
    MAX_LENGTH = object()
    name = 'EMSA-PSS'

    def __init__--- This code section failed: ---

 L.  22         0  LOAD_FAST                'mgf'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _mgf

 L.  25         6  LOAD_GLOBAL              isinstance
                8  LOAD_FAST                'salt_length'
               10  LOAD_GLOBAL              int
               12  CALL_FUNCTION_2       2  ''

 L.  24        14  POP_JUMP_IF_TRUE     34  'to 34'

 L.  26        16  LOAD_FAST                'salt_length'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                MAX_LENGTH
               22  <117>                 1  ''

 L.  24        24  POP_JUMP_IF_FALSE    34  'to 34'

 L.  28        26  LOAD_GLOBAL              TypeError
               28  LOAD_STR                 'salt_length must be an integer.'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'
             34_1  COME_FROM            14  '14'

 L.  30        34  LOAD_FAST                'salt_length'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                MAX_LENGTH
               40  <117>                 1  ''
               42  POP_JUMP_IF_FALSE    60  'to 60'
               44  LOAD_FAST                'salt_length'
               46  LOAD_CONST               0
               48  COMPARE_OP               <
               50  POP_JUMP_IF_FALSE    60  'to 60'

 L.  31        52  LOAD_GLOBAL              ValueError
               54  LOAD_STR                 'salt_length must be zero or greater.'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'
             60_1  COME_FROM            42  '42'

 L.  33        60  LOAD_FAST                'salt_length'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _salt_length

Parse error at or near `<117>' instruction at offset 22


class OAEP(AsymmetricPadding):
    name = 'EME-OAEP'

    def __init__(self, mgf: 'MGF1', algorithm: hashes.HashAlgorithm, label: typing.Optional[bytes]):
        if not isinstancealgorithmhashes.HashAlgorithm:
            raise TypeError('Expected instance of hashes.HashAlgorithm.')
        self._mgf = mgf
        self._algorithm = algorithm
        self._label = label


class MGF1(object):
    MAX_LENGTH = object()

    def __init__(self, algorithm: hashes.HashAlgorithm):
        if not isinstancealgorithmhashes.HashAlgorithm:
            raise TypeError('Expected instance of hashes.HashAlgorithm.')
        self._algorithm = algorithm


def calculate_max_pss_salt_length--- This code section failed: ---

 L.  67         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'key'
                4  LOAD_GLOBAL              rsa
                6  LOAD_ATTR                RSAPrivateKey
                8  LOAD_GLOBAL              rsa
               10  LOAD_ATTR                RSAPublicKey
               12  BUILD_TUPLE_2         2 
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     26  'to 26'

 L.  68        18  LOAD_GLOBAL              TypeError
               20  LOAD_STR                 'key must be an RSA public or private key'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L.  70        26  LOAD_FAST                'key'
               28  LOAD_ATTR                key_size
               30  LOAD_CONST               6
               32  BINARY_ADD       
               34  LOAD_CONST               8
               36  BINARY_FLOOR_DIVIDE
               38  STORE_FAST               'emlen'

 L.  71        40  LOAD_FAST                'emlen'
               42  LOAD_FAST                'hash_algorithm'
               44  LOAD_ATTR                digest_size
               46  BINARY_SUBTRACT  
               48  LOAD_CONST               2
               50  BINARY_SUBTRACT  
               52  STORE_FAST               'salt_length'

 L.  72        54  LOAD_FAST                'salt_length'
               56  LOAD_CONST               0
               58  COMPARE_OP               >=
               60  POP_JUMP_IF_TRUE     66  'to 66'
               62  <74>             
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            60  '60'

 L.  73        66  LOAD_FAST                'salt_length'
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 62