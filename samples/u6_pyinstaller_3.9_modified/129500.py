# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\x509\base.py
import abc, datetime, os, typing
from enum import Enum
from cryptography.hazmat._types import _PRIVATE_KEY_TYPES, _PUBLIC_KEY_TYPES
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dsa, ec, ed25519, ed448, rsa
from cryptography.x509.extensions import Extension, ExtensionType, Extensions
from cryptography.x509.name import Name
from cryptography.x509.oid import ObjectIdentifier
_EARLIEST_UTC_TIME = datetime.datetime(1950, 1, 1)

class AttributeNotFound(Exception):

    def __init__(self, msg, oid):
        super(AttributeNotFound, self).__init__(msg)
        self.oid = oid


def _reject_duplicate_extension(extension: Extension, extensions: typing.List[Extension]):
    for e in extensions:
        if e.oid == extension.oid:
            raise ValueError('This extension has already been set.')


def _reject_duplicate_attribute(oid: ObjectIdentifier, attributes: typing.List[typing.Tuple[(ObjectIdentifier, bytes)]]):
    for attr_oid, _ in attributes:
        if attr_oid == oid:
            raise ValueError('This attribute has already been set.')


def _convert_to_naive_utc_time--- This code section failed: ---

 L.  61         0  LOAD_FAST                'time'
                2  LOAD_ATTR                tzinfo
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    50  'to 50'

 L.  62        10  LOAD_FAST                'time'
               12  LOAD_METHOD              utcoffset
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'offset'

 L.  63        18  LOAD_FAST                'offset'
               20  POP_JUMP_IF_FALSE    26  'to 26'
               22  LOAD_FAST                'offset'
               24  JUMP_FORWARD         32  'to 32'
             26_0  COME_FROM            20  '20'
               26  LOAD_GLOBAL              datetime
               28  LOAD_METHOD              timedelta
               30  CALL_METHOD_0         0  ''
             32_0  COME_FROM            24  '24'
               32  STORE_FAST               'offset'

 L.  64        34  LOAD_FAST                'time'
               36  LOAD_ATTR                replace
               38  LOAD_CONST               None
               40  LOAD_CONST               ('tzinfo',)
               42  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               44  LOAD_FAST                'offset'
               46  BINARY_SUBTRACT  
               48  RETURN_VALUE     
             50_0  COME_FROM             8  '8'

 L.  66        50  LOAD_FAST                'time'
               52  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


class Version(Enum):
    v1 = 0
    v3 = 2


class InvalidVersion(Exception):

    def __init__(self, msg, parsed_version):
        super(InvalidVersion, self).__init__(msg)
        self.parsed_version = parsed_version


class Certificate(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def fingerprint(self, algorithm: hashes.HashAlgorithm) -> bytes:
        """
        Returns bytes using digest passed.
        """
        pass

    @abc.abstractproperty
    def serial_number(self) -> int:
        """
        Returns certificate serial number
        """
        pass

    @abc.abstractproperty
    def version(self) -> Version:
        """
        Returns the certificate version
        """
        pass

    @abc.abstractmethod
    def public_key(self) -> _PUBLIC_KEY_TYPES:
        """
        Returns the public key
        """
        pass

    @abc.abstractproperty
    def not_valid_before(self) -> datetime.datetime:
        """
        Not before time (represented as UTC datetime)
        """
        pass

    @abc.abstractproperty
    def not_valid_after(self) -> datetime.datetime:
        """
        Not after time (represented as UTC datetime)
        """
        pass

    @abc.abstractproperty
    def issuer(self) -> Name:
        """
        Returns the issuer name object.
        """
        pass

    @abc.abstractproperty
    def subject(self) -> Name:
        """
        Returns the subject name object.
        """
        pass

    @abc.abstractproperty
    def signature_hash_algorithm(self) -> typing.Optional[hashes.HashAlgorithm]:
        """
        Returns a HashAlgorithm corresponding to the type of the digest signed
        in the certificate.
        """
        pass

    @abc.abstractproperty
    def signature_algorithm_oid(self) -> ObjectIdentifier:
        """
        Returns the ObjectIdentifier of the signature algorithm.
        """
        pass

    @abc.abstractproperty
    def extensions(self) -> Extensions:
        """
        Returns an Extensions object.
        """
        pass

    @abc.abstractproperty
    def signature(self) -> bytes:
        """
        Returns the signature bytes.
        """
        pass

    @abc.abstractproperty
    def tbs_certificate_bytes(self) -> bytes:
        """
        Returns the tbsCertificate payload bytes as defined in RFC 5280.
        """
        pass

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Checks equality.
        """
        pass

    @abc.abstractmethod
    def __ne__(self, other: object) -> bool:
        """
        Checks not equal.
        """
        pass

    @abc.abstractmethod
    def __hash__(self) -> int:
        """
        Computes a hash.
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding: serialization.Encoding) -> bytes:
        """
        Serializes the certificate to PEM or DER format.
        """
        pass


class RevokedCertificate(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def serial_number(self) -> int:
        """
        Returns the serial number of the revoked certificate.
        """
        pass

    @abc.abstractproperty
    def revocation_date(self) -> datetime.datetime:
        """
        Returns the date of when this certificate was revoked.
        """
        pass

    @abc.abstractproperty
    def extensions(self) -> Extensions:
        """
        Returns an Extensions object containing a list of Revoked extensions.
        """
        pass


class CertificateRevocationList(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def public_bytes(self, encoding: serialization.Encoding) -> bytes:
        """
        Serializes the CRL to PEM or DER format.
        """
        pass

    @abc.abstractmethod
    def fingerprint(self, algorithm: hashes.HashAlgorithm) -> bytes:
        """
        Returns bytes using digest passed.
        """
        pass

    @abc.abstractmethod
    def get_revoked_certificate_by_serial_number(self, serial_number: int) -> typing.Optional[RevokedCertificate]:
        """
        Returns an instance of RevokedCertificate or None if the serial_number
        is not in the CRL.
        """
        pass

    @abc.abstractproperty
    def signature_hash_algorithm(self) -> hashes.HashAlgorithm:
        """
        Returns a HashAlgorithm corresponding to the type of the digest signed
        in the certificate.
        """
        pass

    @abc.abstractproperty
    def signature_algorithm_oid(self) -> ObjectIdentifier:
        """
        Returns the ObjectIdentifier of the signature algorithm.
        """
        pass

    @abc.abstractproperty
    def issuer(self) -> Name:
        """
        Returns the X509Name with the issuer of this CRL.
        """
        pass

    @abc.abstractproperty
    def next_update(self) -> datetime.datetime:
        """
        Returns the date of next update for this CRL.
        """
        pass

    @abc.abstractproperty
    def last_update(self) -> datetime.datetime:
        """
        Returns the date of last update for this CRL.
        """
        pass

    @abc.abstractproperty
    def extensions(self) -> Extensions:
        """
        Returns an Extensions object containing a list of CRL extensions.
        """
        pass

    @abc.abstractproperty
    def signature(self) -> bytes:
        """
        Returns the signature bytes.
        """
        pass

    @abc.abstractproperty
    def tbs_certlist_bytes(self) -> bytes:
        """
        Returns the tbsCertList payload bytes as defined in RFC 5280.
        """
        pass

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Checks equality.
        """
        pass

    @abc.abstractmethod
    def __ne__(self, other: object) -> bool:
        """
        Checks not equal.
        """
        pass

    @abc.abstractmethod
    def __len__(self) -> int:
        """
        Number of revoked certificates in the CRL.
        """
        pass

    @abc.abstractmethod
    def __getitem__(self, idx):
        """
        Returns a revoked certificate (or slice of revoked certificates).
        """
        pass

    @abc.abstractmethod
    def __iter__(self):
        """
        Iterator over the revoked certificates
        """
        pass

    @abc.abstractmethod
    def is_signature_valid(self, public_key: _PUBLIC_KEY_TYPES) -> bool:
        """
        Verifies signature of revocation list against given public key.
        """
        pass


class CertificateSigningRequest(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Checks equality.
        """
        pass

    @abc.abstractmethod
    def __ne__(self, other: object) -> bool:
        """
        Checks not equal.
        """
        pass

    @abc.abstractmethod
    def __hash__(self) -> int:
        """
        Computes a hash.
        """
        pass

    @abc.abstractmethod
    def public_key(self) -> _PUBLIC_KEY_TYPES:
        """
        Returns the public key
        """
        pass

    @abc.abstractproperty
    def subject(self) -> Name:
        """
        Returns the subject name object.
        """
        pass

    @abc.abstractproperty
    def signature_hash_algorithm(self) -> hashes.HashAlgorithm:
        """
        Returns a HashAlgorithm corresponding to the type of the digest signed
        in the certificate.
        """
        pass

    @abc.abstractproperty
    def signature_algorithm_oid(self) -> ObjectIdentifier:
        """
        Returns the ObjectIdentifier of the signature algorithm.
        """
        pass

    @abc.abstractproperty
    def extensions(self) -> Extensions:
        """
        Returns the extensions in the signing request.
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding: serialization.Encoding) -> bytes:
        """
        Encodes the request to PEM or DER format.
        """
        pass

    @abc.abstractproperty
    def signature(self) -> bytes:
        """
        Returns the signature bytes.
        """
        pass

    @abc.abstractproperty
    def tbs_certrequest_bytes(self) -> bytes:
        """
        Returns the PKCS#10 CertificationRequestInfo bytes as defined in RFC
        2986.
        """
        pass

    @abc.abstractproperty
    def is_signature_valid(self) -> bool:
        """
        Verifies signature of signing request.
        """
        pass

    @abc.abstractmethod
    def get_attribute_for_oid(self, oid: ObjectIdentifier) -> bytes:
        """
        Get the attribute value for a given OID.
        """
        pass


def load_pem_x509_certificate(data: bytes, backend=None) -> Certificate:
    backend = _get_backend(backend)
    return backend.load_pem_x509_certificate(data)


def load_der_x509_certificate(data: bytes, backend=None) -> Certificate:
    backend = _get_backend(backend)
    return backend.load_der_x509_certificate(data)


def load_pem_x509_csr(data: bytes, backend=None) -> CertificateSigningRequest:
    backend = _get_backend(backend)
    return backend.load_pem_x509_csr(data)


def load_der_x509_csr(data: bytes, backend=None) -> CertificateSigningRequest:
    backend = _get_backend(backend)
    return backend.load_der_x509_csr(data)


def load_pem_x509_crl(data: bytes, backend=None) -> CertificateRevocationList:
    backend = _get_backend(backend)
    return backend.load_pem_x509_crl(data)


def load_der_x509_crl(data: bytes, backend=None) -> CertificateRevocationList:
    backend = _get_backend(backend)
    return backend.load_der_x509_crl(data)


class CertificateSigningRequestBuilder(object):

    def __init__(self, subject_name=None, extensions=[], attributes=[]):
        """
        Creates an empty X.509 certificate request (v1).
        """
        self._subject_name = subject_name
        self._extensions = extensions
        self._attributes = attributes

    def subject_name--- This code section failed: ---

 L. 440         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'name'
                4  LOAD_GLOBAL              Name
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 441        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'Expecting x509.Name object.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 442        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _subject_name
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 443        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'The subject name may only be set once.'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 444        36  LOAD_GLOBAL              CertificateSigningRequestBuilder

 L. 445        38  LOAD_FAST                'name'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _extensions
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _attributes

 L. 444        48  CALL_FUNCTION_3       3  ''
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def add_extension(self, extval: ExtensionType, critical: bool):
        """
        Adds an X.509 extension to the certificate request.
        """
        if not isinstance(extval, ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = Extension(extval.oid, critical, extval)
        _reject_duplicate_extension(extension, self._extensions)
        return CertificateSigningRequestBuilder(self._subject_name, self._extensions + [extension], self._attributes)

    def add_attribute(self, oid: ObjectIdentifier, value: bytes):
        """
        Adds an X.509 attribute with an OID and associated value.
        """
        if not isinstance(oid, ObjectIdentifier):
            raise TypeError('oid must be an ObjectIdentifier')
        if not isinstance(value, bytes):
            raise TypeError('value must be bytes')
        _reject_duplicate_attribute(oid, self._attributes)
        return CertificateSigningRequestBuilder(self._subject_name, self._extensions, self._attributes + [(oid, value)])

    def sign--- This code section failed: ---

 L. 491         0  LOAD_GLOBAL              _get_backend
                2  LOAD_FAST                'backend'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'backend'

 L. 492         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _subject_name
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 493        18  LOAD_GLOBAL              ValueError
               20  LOAD_STR                 'A CertificateSigningRequest must have a subject'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 494        26  LOAD_FAST                'backend'
               28  LOAD_METHOD              create_x509_csr
               30  LOAD_FAST                'self'
               32  LOAD_FAST                'private_key'
               34  LOAD_FAST                'algorithm'
               36  CALL_METHOD_3         3  ''
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14


class CertificateBuilder(object):

    def __init__(self, issuer_name=None, subject_name=None, public_key=None, serial_number=None, not_valid_before=None, not_valid_after=None, extensions=[]):
        self._version = Version.v3
        self._issuer_name = issuer_name
        self._subject_name = subject_name
        self._public_key = public_key
        self._serial_number = serial_number
        self._not_valid_before = not_valid_before
        self._not_valid_after = not_valid_after
        self._extensions = extensions

    def issuer_name--- This code section failed: ---

 L. 521         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'name'
                4  LOAD_GLOBAL              Name
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 522        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'Expecting x509.Name object.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 523        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _issuer_name
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 524        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'The issuer name may only be set once.'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 525        36  LOAD_GLOBAL              CertificateBuilder

 L. 526        38  LOAD_FAST                'name'

 L. 527        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _subject_name

 L. 528        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _public_key

 L. 529        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _serial_number

 L. 530        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _not_valid_before

 L. 531        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _not_valid_after

 L. 532        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _extensions

 L. 525        64  CALL_FUNCTION_7       7  ''
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def subject_name--- This code section failed: ---

 L. 539         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'name'
                4  LOAD_GLOBAL              Name
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 540        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'Expecting x509.Name object.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 541        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _subject_name
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 542        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'The subject name may only be set once.'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 543        36  LOAD_GLOBAL              CertificateBuilder

 L. 544        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _issuer_name

 L. 545        42  LOAD_FAST                'name'

 L. 546        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _public_key

 L. 547        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _serial_number

 L. 548        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _not_valid_before

 L. 549        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _not_valid_after

 L. 550        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _extensions

 L. 543        64  CALL_FUNCTION_7       7  ''
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def public_key--- This code section failed: ---

 L. 560         0  LOAD_GLOBAL              isinstance

 L. 561         2  LOAD_FAST                'key'

 L. 563         4  LOAD_GLOBAL              dsa
                6  LOAD_ATTR                DSAPublicKey

 L. 564         8  LOAD_GLOBAL              rsa
               10  LOAD_ATTR                RSAPublicKey

 L. 565        12  LOAD_GLOBAL              ec
               14  LOAD_ATTR                EllipticCurvePublicKey

 L. 566        16  LOAD_GLOBAL              ed25519
               18  LOAD_ATTR                Ed25519PublicKey

 L. 567        20  LOAD_GLOBAL              ed448
               22  LOAD_ATTR                Ed448PublicKey

 L. 562        24  BUILD_TUPLE_5         5 

 L. 560        26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_TRUE     38  'to 38'

 L. 570        30  LOAD_GLOBAL              TypeError

 L. 571        32  LOAD_STR                 'Expecting one of DSAPublicKey, RSAPublicKey, EllipticCurvePublicKey, Ed25519PublicKey or Ed448PublicKey.'

 L. 570        34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 575        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _public_key
               42  LOAD_CONST               None
               44  <117>                 1  ''
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L. 576        48  LOAD_GLOBAL              ValueError
               50  LOAD_STR                 'The public key may only be set once.'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L. 577        56  LOAD_GLOBAL              CertificateBuilder

 L. 578        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _issuer_name

 L. 579        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _subject_name

 L. 580        66  LOAD_FAST                'key'

 L. 581        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _serial_number

 L. 582        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _not_valid_before

 L. 583        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _not_valid_after

 L. 584        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _extensions

 L. 577        84  CALL_FUNCTION_7       7  ''
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 44

    def serial_number--- This code section failed: ---

 L. 591         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'number'
                4  LOAD_GLOBAL              int
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 592        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'Serial number must be of integral type.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 593        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _serial_number
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 594        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'The serial number may only be set once.'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 595        36  LOAD_FAST                'number'
               38  LOAD_CONST               0
               40  COMPARE_OP               <=
               42  POP_JUMP_IF_FALSE    52  'to 52'

 L. 596        44  LOAD_GLOBAL              ValueError
               46  LOAD_STR                 'The serial number should be positive.'
               48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            42  '42'

 L. 600        52  LOAD_FAST                'number'
               54  LOAD_METHOD              bit_length
               56  CALL_METHOD_0         0  ''
               58  LOAD_CONST               160
               60  COMPARE_OP               >=
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L. 601        64  LOAD_GLOBAL              ValueError

 L. 602        66  LOAD_STR                 'The serial number should not be more than 159 bits.'

 L. 601        68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L. 604        72  LOAD_GLOBAL              CertificateBuilder

 L. 605        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _issuer_name

 L. 606        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _subject_name

 L. 607        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _public_key

 L. 608        86  LOAD_FAST                'number'

 L. 609        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _not_valid_before

 L. 610        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _not_valid_after

 L. 611        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _extensions

 L. 604       100  CALL_FUNCTION_7       7  ''
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def not_valid_before--- This code section failed: ---

 L. 618         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'time'
                4  LOAD_GLOBAL              datetime
                6  LOAD_ATTR                datetime
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'

 L. 619        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'Expecting datetime object.'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 620        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _not_valid_before
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 621        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'The not valid before may only be set once.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 622        38  LOAD_GLOBAL              _convert_to_naive_utc_time
               40  LOAD_FAST                'time'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'time'

 L. 623        46  LOAD_FAST                'time'
               48  LOAD_GLOBAL              _EARLIEST_UTC_TIME
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 624        54  LOAD_GLOBAL              ValueError

 L. 625        56  LOAD_STR                 'The not valid before date must be on or after 1950 January 1).'

 L. 624        58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 628        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _not_valid_after
               66  LOAD_CONST               None
               68  <117>                 1  ''
               70  POP_JUMP_IF_FALSE    90  'to 90'
               72  LOAD_FAST                'time'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _not_valid_after
               78  COMPARE_OP               >
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 629        82  LOAD_GLOBAL              ValueError

 L. 630        84  LOAD_STR                 'The not valid before date must be before the not valid after date.'

 L. 629        86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'
             90_1  COME_FROM            70  '70'

 L. 633        90  LOAD_GLOBAL              CertificateBuilder

 L. 634        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _issuer_name

 L. 635        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _subject_name

 L. 636       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _public_key

 L. 637       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _serial_number

 L. 638       108  LOAD_FAST                'time'

 L. 639       110  LOAD_FAST                'self'
              112  LOAD_ATTR                _not_valid_after

 L. 640       114  LOAD_FAST                'self'
              116  LOAD_ATTR                _extensions

 L. 633       118  CALL_FUNCTION_7       7  ''
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    def not_valid_after--- This code section failed: ---

 L. 647         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'time'
                4  LOAD_GLOBAL              datetime
                6  LOAD_ATTR                datetime
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'

 L. 648        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'Expecting datetime object.'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 649        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _not_valid_after
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 650        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'The not valid after may only be set once.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 651        38  LOAD_GLOBAL              _convert_to_naive_utc_time
               40  LOAD_FAST                'time'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'time'

 L. 652        46  LOAD_FAST                'time'
               48  LOAD_GLOBAL              _EARLIEST_UTC_TIME
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 653        54  LOAD_GLOBAL              ValueError

 L. 654        56  LOAD_STR                 'The not valid after date must be on or after 1950 January 1.'

 L. 653        58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 658        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _not_valid_before
               66  LOAD_CONST               None
               68  <117>                 1  ''

 L. 657        70  POP_JUMP_IF_FALSE    90  'to 90'

 L. 659        72  LOAD_FAST                'time'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _not_valid_before
               78  COMPARE_OP               <

 L. 657        80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 661        82  LOAD_GLOBAL              ValueError

 L. 662        84  LOAD_STR                 'The not valid after date must be after the not valid before date.'

 L. 661        86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'
             90_1  COME_FROM            70  '70'

 L. 665        90  LOAD_GLOBAL              CertificateBuilder

 L. 666        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _issuer_name

 L. 667        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _subject_name

 L. 668       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _public_key

 L. 669       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _serial_number

 L. 670       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _not_valid_before

 L. 671       112  LOAD_FAST                'time'

 L. 672       114  LOAD_FAST                'self'
              116  LOAD_ATTR                _extensions

 L. 665       118  CALL_FUNCTION_7       7  ''
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    def add_extension(self, extval: ExtensionType, critical: bool):
        """
        Adds an X.509 extension to the certificate.
        """
        if not isinstance(extval, ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = Extension(extval.oid, critical, extval)
        _reject_duplicate_extension(extension, self._extensions)
        return CertificateBuilderself._issuer_nameself._subject_nameself._public_keyself._serial_numberself._not_valid_beforeself._not_valid_after(self._extensions + [extension])

    def sign--- This code section failed: ---

 L. 704         0  LOAD_GLOBAL              _get_backend
                2  LOAD_FAST                'backend'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'backend'

 L. 705         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _subject_name
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 706        18  LOAD_GLOBAL              ValueError
               20  LOAD_STR                 'A certificate must have a subject name'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 708        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _issuer_name
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 709        36  LOAD_GLOBAL              ValueError
               38  LOAD_STR                 'A certificate must have an issuer name'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'

 L. 711        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _serial_number
               48  LOAD_CONST               None
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 712        54  LOAD_GLOBAL              ValueError
               56  LOAD_STR                 'A certificate must have a serial number'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 714        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _not_valid_before
               66  LOAD_CONST               None
               68  <117>                 0  ''
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 715        72  LOAD_GLOBAL              ValueError
               74  LOAD_STR                 'A certificate must have a not valid before time'
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            70  '70'

 L. 717        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _not_valid_after
               84  LOAD_CONST               None
               86  <117>                 0  ''
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L. 718        90  LOAD_GLOBAL              ValueError
               92  LOAD_STR                 'A certificate must have a not valid after time'
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            88  '88'

 L. 720        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _public_key
              102  LOAD_CONST               None
              104  <117>                 0  ''
              106  POP_JUMP_IF_FALSE   116  'to 116'

 L. 721       108  LOAD_GLOBAL              ValueError
              110  LOAD_STR                 'A certificate must have a public key'
              112  CALL_FUNCTION_1       1  ''
              114  RAISE_VARARGS_1       1  'exception instance'
            116_0  COME_FROM           106  '106'

 L. 723       116  LOAD_FAST                'backend'
              118  LOAD_METHOD              create_x509_certificate
              120  LOAD_FAST                'self'
              122  LOAD_FAST                'private_key'
              124  LOAD_FAST                'algorithm'
              126  CALL_METHOD_3         3  ''
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14


class CertificateRevocationListBuilder(object):

    def __init__(self, issuer_name=None, last_update=None, next_update=None, extensions=[], revoked_certificates=[]):
        self._issuer_name = issuer_name
        self._last_update = last_update
        self._next_update = next_update
        self._extensions = extensions
        self._revoked_certificates = revoked_certificates

    def issuer_name--- This code section failed: ---

 L. 742         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'issuer_name'
                4  LOAD_GLOBAL              Name
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 743        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'Expecting x509.Name object.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 744        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _issuer_name
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 745        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'The issuer name may only be set once.'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 746        36  LOAD_GLOBAL              CertificateRevocationListBuilder

 L. 747        38  LOAD_FAST                'issuer_name'

 L. 748        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _last_update

 L. 749        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _next_update

 L. 750        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _extensions

 L. 751        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _revoked_certificates

 L. 746        56  CALL_FUNCTION_5       5  ''
               58  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def last_update--- This code section failed: ---

 L. 755         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'last_update'
                4  LOAD_GLOBAL              datetime
                6  LOAD_ATTR                datetime
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'

 L. 756        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'Expecting datetime object.'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 757        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _last_update
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 758        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'Last update may only be set once.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 759        38  LOAD_GLOBAL              _convert_to_naive_utc_time
               40  LOAD_FAST                'last_update'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'last_update'

 L. 760        46  LOAD_FAST                'last_update'
               48  LOAD_GLOBAL              _EARLIEST_UTC_TIME
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 761        54  LOAD_GLOBAL              ValueError

 L. 762        56  LOAD_STR                 'The last update date must be on or after 1950 January 1.'

 L. 761        58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 764        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _next_update
               66  LOAD_CONST               None
               68  <117>                 1  ''
               70  POP_JUMP_IF_FALSE    90  'to 90'
               72  LOAD_FAST                'last_update'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _next_update
               78  COMPARE_OP               >
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 765        82  LOAD_GLOBAL              ValueError

 L. 766        84  LOAD_STR                 'The last update date must be before the next update date.'

 L. 765        86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'
             90_1  COME_FROM            70  '70'

 L. 768        90  LOAD_GLOBAL              CertificateRevocationListBuilder

 L. 769        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _issuer_name

 L. 770        96  LOAD_FAST                'last_update'

 L. 771        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _next_update

 L. 772       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _extensions

 L. 773       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _revoked_certificates

 L. 768       110  CALL_FUNCTION_5       5  ''
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    def next_update--- This code section failed: ---

 L. 777         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'next_update'
                4  LOAD_GLOBAL              datetime
                6  LOAD_ATTR                datetime
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'

 L. 778        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'Expecting datetime object.'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 779        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _next_update
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 780        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'Last update may only be set once.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 781        38  LOAD_GLOBAL              _convert_to_naive_utc_time
               40  LOAD_FAST                'next_update'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'next_update'

 L. 782        46  LOAD_FAST                'next_update'
               48  LOAD_GLOBAL              _EARLIEST_UTC_TIME
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 783        54  LOAD_GLOBAL              ValueError

 L. 784        56  LOAD_STR                 'The last update date must be on or after 1950 January 1.'

 L. 783        58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 786        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _last_update
               66  LOAD_CONST               None
               68  <117>                 1  ''
               70  POP_JUMP_IF_FALSE    90  'to 90'
               72  LOAD_FAST                'next_update'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _last_update
               78  COMPARE_OP               <
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 787        82  LOAD_GLOBAL              ValueError

 L. 788        84  LOAD_STR                 'The next update date must be after the last update date.'

 L. 787        86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'
             90_1  COME_FROM            70  '70'

 L. 790        90  LOAD_GLOBAL              CertificateRevocationListBuilder

 L. 791        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _issuer_name

 L. 792        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _last_update

 L. 793       100  LOAD_FAST                'next_update'

 L. 794       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _extensions

 L. 795       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _revoked_certificates

 L. 790       110  CALL_FUNCTION_5       5  ''
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    def add_extension(self, extval: ExtensionType, critical: bool):
        """
        Adds an X.509 extension to the certificate revocation list.
        """
        if not isinstance(extval, ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = Extension(extval.oid, critical, extval)
        _reject_duplicate_extension(extension, self._extensions)
        return CertificateRevocationListBuilderself._issuer_nameself._last_updateself._next_update(self._extensions + [extension])self._revoked_certificates

    def add_revoked_certificate(self, revoked_certificate: RevokedCertificate):
        """
        Adds a revoked certificate to the CRL.
        """
        if not isinstance(revoked_certificate, RevokedCertificate):
            raise TypeError('Must be an instance of RevokedCertificate')
        return CertificateRevocationListBuilderself._issuer_nameself._last_updateself._next_updateself._extensions(self._revoked_certificates + [revoked_certificate])

    def sign--- This code section failed: ---

 L. 836         0  LOAD_GLOBAL              _get_backend
                2  LOAD_FAST                'backend'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'backend'

 L. 837         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _issuer_name
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 838        18  LOAD_GLOBAL              ValueError
               20  LOAD_STR                 'A CRL must have an issuer name'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 840        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _last_update
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 841        36  LOAD_GLOBAL              ValueError
               38  LOAD_STR                 'A CRL must have a last update time'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'

 L. 843        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _next_update
               48  LOAD_CONST               None
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 844        54  LOAD_GLOBAL              ValueError
               56  LOAD_STR                 'A CRL must have a next update time'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 846        62  LOAD_FAST                'backend'
               64  LOAD_METHOD              create_x509_crl
               66  LOAD_FAST                'self'
               68  LOAD_FAST                'private_key'
               70  LOAD_FAST                'algorithm'
               72  CALL_METHOD_3         3  ''
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14


class RevokedCertificateBuilder(object):

    def __init__(self, serial_number=None, revocation_date=None, extensions=[]):
        self._serial_number = serial_number
        self._revocation_date = revocation_date
        self._extensions = extensions

    def serial_number--- This code section failed: ---

 L. 858         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'number'
                4  LOAD_GLOBAL              int
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 859        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'Serial number must be of integral type.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 860        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _serial_number
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 861        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'The serial number may only be set once.'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 862        36  LOAD_FAST                'number'
               38  LOAD_CONST               0
               40  COMPARE_OP               <=
               42  POP_JUMP_IF_FALSE    52  'to 52'

 L. 863        44  LOAD_GLOBAL              ValueError
               46  LOAD_STR                 'The serial number should be positive'
               48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            42  '42'

 L. 867        52  LOAD_FAST                'number'
               54  LOAD_METHOD              bit_length
               56  CALL_METHOD_0         0  ''
               58  LOAD_CONST               160
               60  COMPARE_OP               >=
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L. 868        64  LOAD_GLOBAL              ValueError

 L. 869        66  LOAD_STR                 'The serial number should not be more than 159 bits.'

 L. 868        68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L. 871        72  LOAD_GLOBAL              RevokedCertificateBuilder

 L. 872        74  LOAD_FAST                'number'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                _revocation_date
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _extensions

 L. 871        84  CALL_FUNCTION_3       3  ''
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def revocation_date--- This code section failed: ---

 L. 876         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'time'
                4  LOAD_GLOBAL              datetime
                6  LOAD_ATTR                datetime
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'

 L. 877        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'Expecting datetime object.'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 878        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _revocation_date
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 879        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'The revocation date may only be set once.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 880        38  LOAD_GLOBAL              _convert_to_naive_utc_time
               40  LOAD_FAST                'time'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'time'

 L. 881        46  LOAD_FAST                'time'
               48  LOAD_GLOBAL              _EARLIEST_UTC_TIME
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 882        54  LOAD_GLOBAL              ValueError

 L. 883        56  LOAD_STR                 'The revocation date must be on or after 1950 January 1.'

 L. 882        58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 885        62  LOAD_GLOBAL              RevokedCertificateBuilder

 L. 886        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _serial_number
               68  LOAD_FAST                'time'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _extensions

 L. 885        74  CALL_FUNCTION_3       3  ''
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    def add_extension(self, extval: ExtensionType, critical: bool):
        if not isinstance(extval, ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = Extension(extval.oid, critical, extval)
        _reject_duplicate_extension(extension, self._extensions)
        return RevokedCertificateBuilder(self._serial_number, self._revocation_date, self._extensions + [extension])

    def build--- This code section failed: ---

 L. 902         0  LOAD_GLOBAL              _get_backend
                2  LOAD_FAST                'backend'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'backend'

 L. 903         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _serial_number
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 904        18  LOAD_GLOBAL              ValueError
               20  LOAD_STR                 'A revoked certificate must have a serial number'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 905        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _revocation_date
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 906        36  LOAD_GLOBAL              ValueError

 L. 907        38  LOAD_STR                 'A revoked certificate must have a revocation date'

 L. 906        40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'

 L. 910        44  LOAD_FAST                'backend'
               46  LOAD_METHOD              create_x509_revoked_certificate
               48  LOAD_FAST                'self'
               50  CALL_METHOD_1         1  ''
               52  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14


def random_serial_number() -> int:
    return int.from_bytes(os.urandom(20), 'big') >> 1