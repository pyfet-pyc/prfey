# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\x509\ocsp.py
import abc, datetime, typing
from enum import Enum
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509.base import _EARLIEST_UTC_TIME, _PRIVATE_KEY_TYPES, _convert_to_naive_utc_time, _reject_duplicate_extension
_OIDS_TO_HASH = {'1.3.14.3.2.26':hashes.SHA1(), 
 '2.16.840.1.101.3.4.2.4':hashes.SHA224(), 
 '2.16.840.1.101.3.4.2.1':hashes.SHA256(), 
 '2.16.840.1.101.3.4.2.2':hashes.SHA384(), 
 '2.16.840.1.101.3.4.2.3':hashes.SHA512()}

class OCSPResponderEncoding(Enum):
    HASH = 'By Hash'
    NAME = 'By Name'


class OCSPResponseStatus(Enum):
    SUCCESSFUL = 0
    MALFORMED_REQUEST = 1
    INTERNAL_ERROR = 2
    TRY_LATER = 3
    SIG_REQUIRED = 5
    UNAUTHORIZED = 6


_RESPONSE_STATUS_TO_ENUM = {x:x.value for x in OCSPResponseStatus}
_ALLOWED_HASHES = (
 hashes.SHA1,
 hashes.SHA224,
 hashes.SHA256,
 hashes.SHA384,
 hashes.SHA512)

def _verify_algorithm(algorithm):
    if not isinstance(algorithm, _ALLOWED_HASHES):
        raise ValueError('Algorithm must be SHA1, SHA224, SHA256, SHA384, or SHA512')


class OCSPCertStatus(Enum):
    GOOD = 0
    REVOKED = 1
    UNKNOWN = 2


_CERT_STATUS_TO_ENUM = {x:x.value for x in OCSPCertStatus}

class _SingleResponse(object):

    def __init__--- This code section failed: ---

 L.  82         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'cert'
                4  LOAD_GLOBAL              x509
                6  LOAD_ATTR                Certificate
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    24  'to 24'
               12  LOAD_GLOBAL              isinstance

 L.  83        14  LOAD_FAST                'issuer'
               16  LOAD_GLOBAL              x509
               18  LOAD_ATTR                Certificate

 L.  82        20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_TRUE     32  'to 32'
             24_0  COME_FROM            10  '10'

 L.  85        24  LOAD_GLOBAL              TypeError
               26  LOAD_STR                 'cert and issuer must be a Certificate'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'

 L.  87        32  LOAD_GLOBAL              _verify_algorithm
               34  LOAD_FAST                'algorithm'
               36  CALL_FUNCTION_1       1  ''
               38  POP_TOP          

 L.  88        40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'this_update'
               44  LOAD_GLOBAL              datetime
               46  LOAD_ATTR                datetime
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_TRUE     60  'to 60'

 L.  89        52  LOAD_GLOBAL              TypeError
               54  LOAD_STR                 'this_update must be a datetime object'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'

 L.  90        60  LOAD_FAST                'next_update'
               62  LOAD_CONST               None
               64  <117>                 1  ''
               66  POP_JUMP_IF_FALSE    88  'to 88'
               68  LOAD_GLOBAL              isinstance

 L.  91        70  LOAD_FAST                'next_update'
               72  LOAD_GLOBAL              datetime
               74  LOAD_ATTR                datetime

 L.  90        76  CALL_FUNCTION_2       2  ''
               78  POP_JUMP_IF_TRUE     88  'to 88'

 L.  93        80  LOAD_GLOBAL              TypeError
               82  LOAD_STR                 'next_update must be a datetime object or None'
               84  CALL_FUNCTION_1       1  ''
               86  RAISE_VARARGS_1       1  'exception instance'
             88_0  COME_FROM            78  '78'
             88_1  COME_FROM            66  '66'

 L.  95        88  LOAD_FAST                'cert'
               90  LOAD_FAST                'self'
               92  STORE_ATTR               _cert

 L.  96        94  LOAD_FAST                'issuer'
               96  LOAD_FAST                'self'
               98  STORE_ATTR               _issuer

 L.  97       100  LOAD_FAST                'algorithm'
              102  LOAD_FAST                'self'
              104  STORE_ATTR               _algorithm

 L.  98       106  LOAD_FAST                'this_update'
              108  LOAD_FAST                'self'
              110  STORE_ATTR               _this_update

 L.  99       112  LOAD_FAST                'next_update'
              114  LOAD_FAST                'self'
              116  STORE_ATTR               _next_update

 L. 101       118  LOAD_GLOBAL              isinstance
              120  LOAD_FAST                'cert_status'
              122  LOAD_GLOBAL              OCSPCertStatus
              124  CALL_FUNCTION_2       2  ''
              126  POP_JUMP_IF_TRUE    136  'to 136'

 L. 102       128  LOAD_GLOBAL              TypeError

 L. 103       130  LOAD_STR                 'cert_status must be an item from the OCSPCertStatus enum'

 L. 102       132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           126  '126'

 L. 105       136  LOAD_FAST                'cert_status'
              138  LOAD_GLOBAL              OCSPCertStatus
              140  LOAD_ATTR                REVOKED
              142  <117>                 1  ''
              144  POP_JUMP_IF_FALSE   180  'to 180'

 L. 106       146  LOAD_FAST                'revocation_time'
              148  LOAD_CONST               None
              150  <117>                 1  ''
              152  POP_JUMP_IF_FALSE   162  'to 162'

 L. 107       154  LOAD_GLOBAL              ValueError

 L. 108       156  LOAD_STR                 'revocation_time can only be provided if the certificate is revoked'

 L. 107       158  CALL_FUNCTION_1       1  ''
              160  RAISE_VARARGS_1       1  'exception instance'
            162_0  COME_FROM           152  '152'

 L. 111       162  LOAD_FAST                'revocation_reason'
              164  LOAD_CONST               None
              166  <117>                 1  ''
              168  POP_JUMP_IF_FALSE   252  'to 252'

 L. 112       170  LOAD_GLOBAL              ValueError

 L. 113       172  LOAD_STR                 'revocation_reason can only be provided if the certificate is revoked'

 L. 112       174  CALL_FUNCTION_1       1  ''
              176  RAISE_VARARGS_1       1  'exception instance'
              178  JUMP_FORWARD        252  'to 252'
            180_0  COME_FROM           144  '144'

 L. 117       180  LOAD_GLOBAL              isinstance
              182  LOAD_FAST                'revocation_time'
              184  LOAD_GLOBAL              datetime
              186  LOAD_ATTR                datetime
              188  CALL_FUNCTION_2       2  ''
              190  POP_JUMP_IF_TRUE    200  'to 200'

 L. 118       192  LOAD_GLOBAL              TypeError
              194  LOAD_STR                 'revocation_time must be a datetime object'
              196  CALL_FUNCTION_1       1  ''
              198  RAISE_VARARGS_1       1  'exception instance'
            200_0  COME_FROM           190  '190'

 L. 120       200  LOAD_GLOBAL              _convert_to_naive_utc_time
              202  LOAD_FAST                'revocation_time'
              204  CALL_FUNCTION_1       1  ''
              206  STORE_FAST               'revocation_time'

 L. 121       208  LOAD_FAST                'revocation_time'
              210  LOAD_GLOBAL              _EARLIEST_UTC_TIME
              212  COMPARE_OP               <
              214  POP_JUMP_IF_FALSE   224  'to 224'

 L. 122       216  LOAD_GLOBAL              ValueError

 L. 123       218  LOAD_STR                 'The revocation_time must be on or after 1950 January 1.'

 L. 122       220  CALL_FUNCTION_1       1  ''
              222  RAISE_VARARGS_1       1  'exception instance'
            224_0  COME_FROM           214  '214'

 L. 127       224  LOAD_FAST                'revocation_reason'
              226  LOAD_CONST               None
              228  <117>                 1  ''
              230  POP_JUMP_IF_FALSE   252  'to 252'
              232  LOAD_GLOBAL              isinstance

 L. 128       234  LOAD_FAST                'revocation_reason'
              236  LOAD_GLOBAL              x509
              238  LOAD_ATTR                ReasonFlags

 L. 127       240  CALL_FUNCTION_2       2  ''
              242  POP_JUMP_IF_TRUE    252  'to 252'

 L. 130       244  LOAD_GLOBAL              TypeError

 L. 131       246  LOAD_STR                 'revocation_reason must be an item from the ReasonFlags enum or None'

 L. 130       248  CALL_FUNCTION_1       1  ''
              250  RAISE_VARARGS_1       1  'exception instance'
            252_0  COME_FROM           242  '242'
            252_1  COME_FROM           230  '230'
            252_2  COME_FROM           178  '178'
            252_3  COME_FROM           168  '168'

 L. 135       252  LOAD_FAST                'cert_status'
              254  LOAD_FAST                'self'
              256  STORE_ATTR               _cert_status

 L. 136       258  LOAD_FAST                'revocation_time'
              260  LOAD_FAST                'self'
              262  STORE_ATTR               _revocation_time

 L. 137       264  LOAD_FAST                'revocation_reason'
              266  LOAD_FAST                'self'
              268  STORE_ATTR               _revocation_reason

Parse error at or near `<117>' instruction at offset 64


class OCSPRequest(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def issuer_key_hash(self) -> bytes:
        """
        The hash of the issuer public key
        """
        pass

    @abc.abstractproperty
    def issuer_name_hash(self) -> bytes:
        """
        The hash of the issuer name
        """
        pass

    @abc.abstractproperty
    def hash_algorithm(self) -> hashes.HashAlgorithm:
        """
        The hash algorithm used in the issuer name and key hashes
        """
        pass

    @abc.abstractproperty
    def serial_number(self) -> int:
        """
        The serial number of the cert whose status is being checked
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding: serialization.Encoding) -> bytes:
        """
        Serializes the request to DER
        """
        pass

    @abc.abstractproperty
    def extensions(self) -> x509.Extensions:
        """
        The list of request extensions. Not single request extensions.
        """
        pass


class OCSPResponse(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def response_status(self) -> OCSPResponseStatus:
        """
        The status of the response. This is a value from the OCSPResponseStatus
        enumeration
        """
        pass

    @abc.abstractproperty
    def signature_algorithm_oid(self) -> x509.ObjectIdentifier:
        """
        The ObjectIdentifier of the signature algorithm
        """
        pass

    @abc.abstractproperty
    def signature_hash_algorithm(self) -> typing.Optional[hashes.HashAlgorithm]:
        """
        Returns a HashAlgorithm corresponding to the type of the digest signed
        """
        pass

    @abc.abstractproperty
    def signature(self) -> bytes:
        """
        The signature bytes
        """
        pass

    @abc.abstractproperty
    def tbs_response_bytes(self) -> bytes:
        """
        The tbsResponseData bytes
        """
        pass

    @abc.abstractproperty
    def certificates(self) -> typing.List[x509.Certificate]:
        """
        A list of certificates used to help build a chain to verify the OCSP
        response. This situation occurs when the OCSP responder uses a delegate
        certificate.
        """
        pass

    @abc.abstractproperty
    def responder_key_hash(self) -> typing.Optional[bytes]:
        """
        The responder's key hash or None
        """
        pass

    @abc.abstractproperty
    def responder_name(self) -> typing.Optional[x509.Name]:
        """
        The responder's Name or None
        """
        pass

    @abc.abstractproperty
    def produced_at(self) -> datetime.datetime:
        """
        The time the response was produced
        """
        pass

    @abc.abstractproperty
    def certificate_status(self) -> OCSPCertStatus:
        """
        The status of the certificate (an element from the OCSPCertStatus enum)
        """
        pass

    @abc.abstractproperty
    def revocation_time(self) -> typing.Optional[datetime.datetime]:
        """
        The date of when the certificate was revoked or None if not
        revoked.
        """
        pass

    @abc.abstractproperty
    def revocation_reason(self) -> typing.Optional[x509.ReasonFlags]:
        """
        The reason the certificate was revoked or None if not specified or
        not revoked.
        """
        pass

    @abc.abstractproperty
    def this_update(self) -> datetime.datetime:
        """
        The most recent time at which the status being indicated is known by
        the responder to have been correct
        """
        pass

    @abc.abstractproperty
    def next_update(self) -> typing.Optional[datetime.datetime]:
        """
        The time when newer information will be available
        """
        pass

    @abc.abstractproperty
    def issuer_key_hash(self) -> bytes:
        """
        The hash of the issuer public key
        """
        pass

    @abc.abstractproperty
    def issuer_name_hash(self) -> bytes:
        """
        The hash of the issuer name
        """
        pass

    @abc.abstractproperty
    def hash_algorithm(self) -> hashes.HashAlgorithm:
        """
        The hash algorithm used in the issuer name and key hashes
        """
        pass

    @abc.abstractproperty
    def serial_number(self) -> int:
        """
        The serial number of the cert whose status is being checked
        """
        pass

    @abc.abstractproperty
    def extensions(self) -> x509.Extensions:
        """
        The list of response extensions. Not single response extensions.
        """
        pass

    @abc.abstractproperty
    def single_extensions(self) -> x509.Extensions:
        """
        The list of single response extensions. Not response extensions.
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding: serialization.Encoding) -> bytes:
        """
        Serializes the response to DER
        """
        pass


class OCSPRequestBuilder(object):

    def __init__(self, request=None, extensions=[]):
        self._request = request
        self._extensions = extensions

    def add_certificate--- This code section failed: ---

 L. 325         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _request
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 326        10  LOAD_GLOBAL              ValueError
               12  LOAD_STR                 'Only one certificate can be added to a request'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 328        18  LOAD_GLOBAL              _verify_algorithm
               20  LOAD_FAST                'algorithm'
               22  CALL_FUNCTION_1       1  ''
               24  POP_TOP          

 L. 329        26  LOAD_GLOBAL              isinstance
               28  LOAD_FAST                'cert'
               30  LOAD_GLOBAL              x509
               32  LOAD_ATTR                Certificate
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    50  'to 50'
               38  LOAD_GLOBAL              isinstance

 L. 330        40  LOAD_FAST                'issuer'
               42  LOAD_GLOBAL              x509
               44  LOAD_ATTR                Certificate

 L. 329        46  CALL_FUNCTION_2       2  ''
               48  POP_JUMP_IF_TRUE     58  'to 58'
             50_0  COME_FROM            36  '36'

 L. 332        50  LOAD_GLOBAL              TypeError
               52  LOAD_STR                 'cert and issuer must be a Certificate'
               54  CALL_FUNCTION_1       1  ''
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            48  '48'

 L. 334        58  LOAD_GLOBAL              OCSPRequestBuilder
               60  LOAD_FAST                'cert'
               62  LOAD_FAST                'issuer'
               64  LOAD_FAST                'algorithm'
               66  BUILD_TUPLE_3         3 
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _extensions
               72  CALL_FUNCTION_2       2  ''
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def add_extension(self, extval: x509.ExtensionType, critical: bool) -> 'OCSPRequestBuilder':
        if not isinstance(extval, x509.ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = x509.Extension(extval.oid, critical, extval)
        _reject_duplicate_extension(extension, self._extensions)
        return OCSPRequestBuilder(self._request, self._extensions + [extension])

    def build--- This code section failed: ---

 L. 350         0  LOAD_CONST               0
                2  LOAD_CONST               ('backend',)
                4  IMPORT_NAME_ATTR         cryptography.hazmat.backends.openssl.backend
                6  IMPORT_FROM              backend
                8  STORE_FAST               'backend'
               10  POP_TOP          

 L. 352        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _request
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 353        22  LOAD_GLOBAL              ValueError
               24  LOAD_STR                 'You must add a certificate before building'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L. 355        30  LOAD_FAST                'backend'
               32  LOAD_METHOD              create_ocsp_request
               34  LOAD_FAST                'self'
               36  CALL_METHOD_1         1  ''
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18


class OCSPResponseBuilder(object):

    def __init__(self, response=None, responder_id=None, certs=None, extensions=[]):
        self._response = response
        self._responder_id = responder_id
        self._certs = certs
        self._extensions = extensions

    def add_response--- This code section failed: ---

 L. 378         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _response
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 379        10  LOAD_GLOBAL              ValueError
               12  LOAD_STR                 'Only one response per OCSPResponse.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 381        18  LOAD_GLOBAL              _SingleResponse

 L. 382        20  LOAD_FAST                'cert'

 L. 383        22  LOAD_FAST                'issuer'

 L. 384        24  LOAD_FAST                'algorithm'

 L. 385        26  LOAD_FAST                'cert_status'

 L. 386        28  LOAD_FAST                'this_update'

 L. 387        30  LOAD_FAST                'next_update'

 L. 388        32  LOAD_FAST                'revocation_time'

 L. 389        34  LOAD_FAST                'revocation_reason'

 L. 381        36  CALL_FUNCTION_8       8  ''
               38  STORE_FAST               'singleresp'

 L. 391        40  LOAD_GLOBAL              OCSPResponseBuilder

 L. 392        42  LOAD_FAST                'singleresp'

 L. 393        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _responder_id

 L. 394        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _certs

 L. 395        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _extensions

 L. 391        56  CALL_FUNCTION_4       4  ''
               58  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def responder_id--- This code section failed: ---

 L. 401         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _responder_id
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 402        10  LOAD_GLOBAL              ValueError
               12  LOAD_STR                 'responder_id can only be set once'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 403        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'responder_cert'
               22  LOAD_GLOBAL              x509
               24  LOAD_ATTR                Certificate
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_TRUE     38  'to 38'

 L. 404        30  LOAD_GLOBAL              TypeError
               32  LOAD_STR                 'responder_cert must be a Certificate'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 405        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'encoding'
               42  LOAD_GLOBAL              OCSPResponderEncoding
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_TRUE     56  'to 56'

 L. 406        48  LOAD_GLOBAL              TypeError

 L. 407        50  LOAD_STR                 'encoding must be an element from OCSPResponderEncoding'

 L. 406        52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L. 410        56  LOAD_GLOBAL              OCSPResponseBuilder

 L. 411        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _response

 L. 412        62  LOAD_FAST                'responder_cert'
               64  LOAD_FAST                'encoding'
               66  BUILD_TUPLE_2         2 

 L. 413        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _certs

 L. 414        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _extensions

 L. 410        76  CALL_FUNCTION_4       4  ''
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def certificates--- This code section failed: ---

 L. 420         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _certs
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 421        10  LOAD_GLOBAL              ValueError
               12  LOAD_STR                 'certificates may only be set once'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 422        18  LOAD_GLOBAL              list
               20  LOAD_FAST                'certs'
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'certs'

 L. 423        26  LOAD_GLOBAL              len
               28  LOAD_FAST                'certs'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_CONST               0
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 424        38  LOAD_GLOBAL              ValueError
               40  LOAD_STR                 'certs must not be an empty list'
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            36  '36'

 L. 425        46  LOAD_GLOBAL              all
               48  LOAD_GENEXPR             '<code_object <genexpr>>'
               50  LOAD_STR                 'OCSPResponseBuilder.certificates.<locals>.<genexpr>'
               52  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               54  LOAD_FAST                'certs'
               56  GET_ITER         
               58  CALL_FUNCTION_1       1  ''
               60  CALL_FUNCTION_1       1  ''
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L. 426        64  LOAD_GLOBAL              TypeError
               66  LOAD_STR                 'certs must be a list of Certificates'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L. 427        72  LOAD_GLOBAL              OCSPResponseBuilder

 L. 428        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _response

 L. 429        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _responder_id

 L. 430        82  LOAD_FAST                'certs'

 L. 431        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _extensions

 L. 427        88  CALL_FUNCTION_4       4  ''
               90  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def add_extension(self, extval: x509.ExtensionType, critical: bool) -> 'OCSPResponseBuilder':
        if not isinstance(extval, x509.ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = x509.Extension(extval.oid, critical, extval)
        _reject_duplicate_extension(extension, self._extensions)
        return OCSPResponseBuilderself._responseself._responder_idself._certs(self._extensions + [extension])

    def sign--- This code section failed: ---

 L. 455         0  LOAD_CONST               0
                2  LOAD_CONST               ('backend',)
                4  IMPORT_NAME_ATTR         cryptography.hazmat.backends.openssl.backend
                6  IMPORT_FROM              backend
                8  STORE_FAST               'backend'
               10  POP_TOP          

 L. 457        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _response
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 458        22  LOAD_GLOBAL              ValueError
               24  LOAD_STR                 'You must add a response before signing'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L. 459        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _responder_id
               34  LOAD_CONST               None
               36  <117>                 0  ''
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 460        40  LOAD_GLOBAL              ValueError
               42  LOAD_STR                 'You must add a responder_id before signing'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L. 462        48  LOAD_FAST                'backend'
               50  LOAD_METHOD              create_ocsp_response

 L. 463        52  LOAD_GLOBAL              OCSPResponseStatus
               54  LOAD_ATTR                SUCCESSFUL
               56  LOAD_FAST                'self'
               58  LOAD_FAST                'private_key'
               60  LOAD_FAST                'algorithm'

 L. 462        62  CALL_METHOD_4         4  ''
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18

    @classmethod
    def build_unsuccessful--- This code section failed: ---

 L. 470         0  LOAD_CONST               0
                2  LOAD_CONST               ('backend',)
                4  IMPORT_NAME_ATTR         cryptography.hazmat.backends.openssl.backend
                6  IMPORT_FROM              backend
                8  STORE_FAST               'backend'
               10  POP_TOP          

 L. 472        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'response_status'
               16  LOAD_GLOBAL              OCSPResponseStatus
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     30  'to 30'

 L. 473        22  LOAD_GLOBAL              TypeError

 L. 474        24  LOAD_STR                 'response_status must be an item from OCSPResponseStatus'

 L. 473        26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L. 476        30  LOAD_FAST                'response_status'
               32  LOAD_GLOBAL              OCSPResponseStatus
               34  LOAD_ATTR                SUCCESSFUL
               36  <117>                 0  ''
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 477        40  LOAD_GLOBAL              ValueError
               42  LOAD_STR                 'response_status cannot be SUCCESSFUL'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L. 479        48  LOAD_FAST                'backend'
               50  LOAD_METHOD              create_ocsp_response
               52  LOAD_FAST                'response_status'
               54  LOAD_CONST               None
               56  LOAD_CONST               None
               58  LOAD_CONST               None
               60  CALL_METHOD_4         4  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 36


def load_der_ocsp_request(data: bytes) -> OCSPRequest:
    import cryptography.hazmat.backends.openssl.backend as backend
    return backend.load_der_ocsp_requestdata


def load_der_ocsp_response(data: bytes) -> OCSPResponse:
    import cryptography.hazmat.backends.openssl.backend as backend
    return backend.load_der_ocsp_responsedata