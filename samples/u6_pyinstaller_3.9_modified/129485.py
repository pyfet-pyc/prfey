# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\utils.py
import typing
from cryptography import utils
from cryptography.hazmat._der import DERReader, INTEGER, SEQUENCE, encode_der, encode_der_integer
from cryptography.hazmat.primitives import hashes

def decode_dss_signature--- This code section failed: ---

 L.  20         0  LOAD_GLOBAL              DERReader
                2  LOAD_FAST                'signature'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_METHOD              read_single_element
                8  LOAD_GLOBAL              SEQUENCE
               10  CALL_METHOD_1         1  ''
               12  SETUP_WITH           66  'to 66'
               14  STORE_FAST               'seq'

 L.  21        16  LOAD_FAST                'seq'
               18  LOAD_METHOD              read_element
               20  LOAD_GLOBAL              INTEGER
               22  CALL_METHOD_1         1  ''
               24  LOAD_METHOD              as_integer
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'r'

 L.  22        30  LOAD_FAST                'seq'
               32  LOAD_METHOD              read_element
               34  LOAD_GLOBAL              INTEGER
               36  CALL_METHOD_1         1  ''
               38  LOAD_METHOD              as_integer
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               's'

 L.  23        44  LOAD_FAST                'r'
               46  LOAD_FAST                's'
               48  BUILD_TUPLE_2         2 
               50  POP_BLOCK        
               52  ROT_TWO          
               54  LOAD_CONST               None
               56  DUP_TOP          
               58  DUP_TOP          
               60  CALL_FUNCTION_3       3  ''
               62  POP_TOP          
               64  RETURN_VALUE     
             66_0  COME_FROM_WITH       12  '12'
               66  <49>             
               68  POP_JUMP_IF_TRUE     72  'to 72'
               70  <48>             
             72_0  COME_FROM            68  '68'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          
               78  POP_EXCEPT       
               80  POP_TOP          

Parse error at or near `ROT_TWO' instruction at offset 52


def encode_dss_signature(r: int, s: int) -> bytes:
    return encode_der(SEQUENCE, encode_der(INTEGER, encode_der_integer(r)), encode_der(INTEGER, encode_der_integer(s)))


class Prehashed(object):

    def __init__(self, algorithm: hashes.HashAlgorithm):
        if not isinstance(algorithm, hashes.HashAlgorithm):
            raise TypeError('Expected instance of HashAlgorithm.')
        self._algorithm = algorithm
        self._digest_size = algorithm.digest_size

    digest_size = utils.read_only_property'_digest_size'