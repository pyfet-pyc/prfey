# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\serialization\pkcs7.py
from __future__ import absolute_import, division, print_function
from enum import Enum
from cryptography import x509
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.utils import _check_byteslike

def load_pem_pkcs7_certificates(data):
    backend = _get_backend(None)
    return backend.load_pem_pkcs7_certificates(data)


def load_der_pkcs7_certificates(data):
    backend = _get_backend(None)
    return backend.load_der_pkcs7_certificates(data)


class PKCS7SignatureBuilder(object):

    def __init__(self, data=None, signers=[], additional_certs=[]):
        self._data = data
        self._signers = signers
        self._additional_certs = additional_certs

    def set_data--- This code section failed: ---

 L.  33         0  LOAD_GLOBAL              _check_byteslike
                2  LOAD_STR                 'data'
                4  LOAD_FAST                'data'
                6  CALL_FUNCTION_2       2  ''
                8  POP_TOP          

 L.  34        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _data
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L.  35        20  LOAD_GLOBAL              ValueError
               22  LOAD_STR                 'data may only be set once'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L.  37        28  LOAD_GLOBAL              PKCS7SignatureBuilder
               30  LOAD_FAST                'data'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _signers
               36  CALL_FUNCTION_2       2  ''
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    def add_signer(self, certificate, private_key, hash_algorithm):
        if not isinstancehash_algorithm(
         hashes.SHA1,
         hashes.SHA224,
         hashes.SHA256,
         hashes.SHA384,
         hashes.SHA512):
            raise TypeError('hash_algorithm must be one of hashes.SHA1, SHA224, SHA256, SHA384, or SHA512')
        if not isinstancecertificatex509.Certificate:
            raise TypeError('certificate must be a x509.Certificate')
        if not isinstanceprivate_key(rsa.RSAPrivateKey, ec.EllipticCurvePrivateKey):
            raise TypeError('Only RSA & EC keys are supported at this time.')
        return PKCS7SignatureBuilderself._data(self._signers + [(certificate, private_key, hash_algorithm)])

    def add_certificate(self, certificate):
        if not isinstancecertificatex509.Certificate:
            raise TypeError('certificate must be a x509.Certificate')
        return PKCS7SignatureBuilder(self._data, self._signers, self._additional_certs + [certificate])

    def sign--- This code section failed: ---

 L.  76         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _signers
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_CONST               0
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L.  77        14  LOAD_GLOBAL              ValueError
               16  LOAD_STR                 'Must have at least one signer'
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            12  '12'

 L.  78        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _data
               26  LOAD_CONST               None
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L.  79        32  LOAD_GLOBAL              ValueError
               34  LOAD_STR                 'You must add data to sign'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            30  '30'

 L.  80        40  LOAD_GLOBAL              list
               42  LOAD_FAST                'options'
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'options'

 L.  81        48  LOAD_GLOBAL              all
               50  LOAD_GENEXPR             '<code_object <genexpr>>'
               52  LOAD_STR                 'PKCS7SignatureBuilder.sign.<locals>.<genexpr>'
               54  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               56  LOAD_FAST                'options'
               58  GET_ITER         
               60  CALL_FUNCTION_1       1  ''
               62  CALL_FUNCTION_1       1  ''
               64  POP_JUMP_IF_TRUE     74  'to 74'

 L.  82        66  LOAD_GLOBAL              ValueError
               68  LOAD_STR                 'options must be from the PKCS7Options enum'
               70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            64  '64'

 L.  83        74  LOAD_FAST                'encoding'

 L.  84        76  LOAD_GLOBAL              serialization
               78  LOAD_ATTR                Encoding
               80  LOAD_ATTR                PEM

 L.  85        82  LOAD_GLOBAL              serialization
               84  LOAD_ATTR                Encoding
               86  LOAD_ATTR                DER

 L.  86        88  LOAD_GLOBAL              serialization
               90  LOAD_ATTR                Encoding
               92  LOAD_ATTR                SMIME

 L.  83        94  BUILD_TUPLE_3         3 
               96  <118>                 1  ''
               98  POP_JUMP_IF_FALSE   108  'to 108'

 L.  88       100  LOAD_GLOBAL              ValueError

 L.  89       102  LOAD_STR                 'Must be PEM, DER, or SMIME from the Encoding enum'

 L.  88       104  CALL_FUNCTION_1       1  ''
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            98  '98'

 L.  95       108  LOAD_GLOBAL              PKCS7Options
              110  LOAD_ATTR                Text
              112  LOAD_FAST                'options'
              114  <118>                 0  ''

 L.  94       116  POP_JUMP_IF_FALSE   136  'to 136'

 L.  96       118  LOAD_GLOBAL              PKCS7Options
              120  LOAD_ATTR                DetachedSignature
              122  LOAD_FAST                'options'
              124  <118>                 1  ''

 L.  94       126  POP_JUMP_IF_FALSE   136  'to 136'

 L.  98       128  LOAD_GLOBAL              ValueError

 L.  99       130  LOAD_STR                 'When passing the Text option you must also pass DetachedSignature'

 L.  98       132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           126  '126'
            136_1  COME_FROM           116  '116'

 L. 103       136  LOAD_GLOBAL              PKCS7Options
              138  LOAD_ATTR                Text
              140  LOAD_FAST                'options'
              142  <118>                 0  ''
              144  POP_JUMP_IF_FALSE   174  'to 174'
              146  LOAD_FAST                'encoding'

 L. 104       148  LOAD_GLOBAL              serialization
              150  LOAD_ATTR                Encoding
              152  LOAD_ATTR                DER

 L. 105       154  LOAD_GLOBAL              serialization
              156  LOAD_ATTR                Encoding
              158  LOAD_ATTR                PEM

 L. 103       160  BUILD_TUPLE_2         2 
              162  <118>                 0  ''
              164  POP_JUMP_IF_FALSE   174  'to 174'

 L. 107       166  LOAD_GLOBAL              ValueError

 L. 108       168  LOAD_STR                 'The Text option is only available for SMIME serialization'

 L. 107       170  CALL_FUNCTION_1       1  ''
              172  RAISE_VARARGS_1       1  'exception instance'
            174_0  COME_FROM           164  '164'
            174_1  COME_FROM           144  '144'

 L. 114       174  LOAD_GLOBAL              PKCS7Options
              176  LOAD_ATTR                NoAttributes
              178  LOAD_FAST                'options'
              180  <118>                 0  ''

 L. 113       182  POP_JUMP_IF_FALSE   202  'to 202'

 L. 115       184  LOAD_GLOBAL              PKCS7Options
              186  LOAD_ATTR                NoCapabilities
              188  LOAD_FAST                'options'
              190  <118>                 0  ''

 L. 113       192  POP_JUMP_IF_FALSE   202  'to 202'

 L. 117       194  LOAD_GLOBAL              ValueError

 L. 118       196  LOAD_STR                 'NoAttributes is a superset of NoCapabilities. Do not pass both values.'

 L. 117       198  CALL_FUNCTION_1       1  ''
              200  RAISE_VARARGS_1       1  'exception instance'
            202_0  COME_FROM           192  '192'
            202_1  COME_FROM           182  '182'

 L. 122       202  LOAD_GLOBAL              _get_backend
              204  LOAD_FAST                'backend'
              206  CALL_FUNCTION_1       1  ''
              208  STORE_FAST               'backend'

 L. 123       210  LOAD_FAST                'backend'
              212  LOAD_METHOD              pkcs7_sign
              214  LOAD_FAST                'self'
              216  LOAD_FAST                'encoding'
              218  LOAD_FAST                'options'
              220  CALL_METHOD_3         3  ''
              222  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 28


class PKCS7Options(Enum):
    Text = 'Add text/plain MIME type'
    Binary = "Don't translate input data into canonical MIME format"
    DetachedSignature = "Don't embed data in the PKCS7 structure"
    NoCapabilities = "Don't embed SMIME capabilities"
    NoAttributes = "Don't embed authenticatedAttributes"
    NoCerts = "Don't embed signer certificate"