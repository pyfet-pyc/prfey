# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\padding.py
from __future__ import absolute_import, division, print_function
import abc, six
from cryptography import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa

@six.add_metaclass(abc.ABCMeta)
class AsymmetricPadding(object):

    @abc.abstractproperty
    def name(self):
        """
        A string naming this padding (e.g. "PSS", "PKCS1").
        """
        pass


@utils.register_interface(AsymmetricPadding)
class PKCS1v15(object):
    name = 'EMSA-PKCS1-v1_5'


@utils.register_interface(AsymmetricPadding)
class PSS(object):
    MAX_LENGTH = object()
    name = 'EMSA-PSS'

    def __init__--- This code section failed: ---

 L.  36         0  LOAD_FAST                'mgf'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _mgf

 L.  39         6  LOAD_GLOBAL              isinstance
                8  LOAD_FAST                'salt_length'
               10  LOAD_GLOBAL              six
               12  LOAD_ATTR                integer_types
               14  CALL_FUNCTION_2       2  ''

 L.  38        16  POP_JUMP_IF_TRUE     36  'to 36'

 L.  40        18  LOAD_FAST                'salt_length'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                MAX_LENGTH
               24  <117>                 1  ''

 L.  38        26  POP_JUMP_IF_FALSE    36  'to 36'

 L.  42        28  LOAD_GLOBAL              TypeError
               30  LOAD_STR                 'salt_length must be an integer.'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'
             36_1  COME_FROM            16  '16'

 L.  44        36  LOAD_FAST                'salt_length'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                MAX_LENGTH
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    62  'to 62'
               46  LOAD_FAST                'salt_length'
               48  LOAD_CONST               0
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L.  45        54  LOAD_GLOBAL              ValueError
               56  LOAD_STR                 'salt_length must be zero or greater.'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'
             62_1  COME_FROM            44  '44'

 L.  47        62  LOAD_FAST                'salt_length'
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _salt_length

Parse error at or near `<117>' instruction at offset 24


@utils.register_interface(AsymmetricPadding)
class OAEP(object):
    name = 'EME-OAEP'

    def __init__(self, mgf, algorithm, label):
        if not isinstancealgorithmhashes.HashAlgorithm:
            raise TypeError('Expected instance of hashes.HashAlgorithm.')
        self._mgf = mgf
        self._algorithm = algorithm
        self._label = label


class MGF1(object):
    MAX_LENGTH = object()

    def __init__(self, algorithm):
        if not isinstancealgorithmhashes.HashAlgorithm:
            raise TypeError('Expected instance of hashes.HashAlgorithm.')
        self._algorithm = algorithm


def calculate_max_pss_salt_length--- This code section failed: ---

 L.  74         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'key'
                4  LOAD_GLOBAL              rsa
                6  LOAD_ATTR                RSAPrivateKey
                8  LOAD_GLOBAL              rsa
               10  LOAD_ATTR                RSAPublicKey
               12  BUILD_TUPLE_2         2 
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     26  'to 26'

 L.  75        18  LOAD_GLOBAL              TypeError
               20  LOAD_STR                 'key must be an RSA public or private key'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L.  77        26  LOAD_FAST                'key'
               28  LOAD_ATTR                key_size
               30  LOAD_CONST               6
               32  BINARY_ADD       
               34  LOAD_CONST               8
               36  BINARY_FLOOR_DIVIDE
               38  STORE_FAST               'emlen'

 L.  78        40  LOAD_FAST                'emlen'
               42  LOAD_FAST                'hash_algorithm'
               44  LOAD_ATTR                digest_size
               46  BINARY_SUBTRACT  
               48  LOAD_CONST               2
               50  BINARY_SUBTRACT  
               52  STORE_FAST               'salt_length'

 L.  79        54  LOAD_FAST                'salt_length'
               56  LOAD_CONST               0
               58  COMPARE_OP               >=
               60  POP_JUMP_IF_TRUE     66  'to 66'
               62  <74>             
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            60  '60'

 L.  80        66  LOAD_FAST                'salt_length'
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 62