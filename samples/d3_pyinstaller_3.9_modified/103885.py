# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\x509\base.py
from __future__ import absolute_import, division, print_function
import abc, datetime, os
from enum import Enum
import six
from cryptography import utils
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.primitives.asymmetric import dsa, ec, ed25519, ed448, rsa
from cryptography.x509.extensions import Extension, ExtensionType
from cryptography.x509.name import Name
from cryptography.x509.oid import ObjectIdentifier
_EARLIEST_UTC_TIME = datetime.datetime(1950, 1, 1)

class AttributeNotFound(Exception):

    def __init__(self, msg, oid):
        super(AttributeNotFound, self).__init__(msg)
        self.oid = oid


def _reject_duplicate_extension(extension, extensions):
    for e in extensions:
        if e.oid == extension.oid:
            raise ValueError('This extension has already been set.')


def _reject_duplicate_attribute(oid, attributes):
    for attr_oid, _ in attributes:
        if attr_oid == oid:
            raise ValueError('This attribute has already been set.')


def _convert_to_naive_utc_time--- This code section failed: ---

 L.  57         0  LOAD_FAST                'time'
                2  LOAD_ATTR                tzinfo
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    50  'to 50'

 L.  58        10  LOAD_FAST                'time'
               12  LOAD_METHOD              utcoffset
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'offset'

 L.  59        18  LOAD_FAST                'offset'
               20  POP_JUMP_IF_FALSE    26  'to 26'
               22  LOAD_FAST                'offset'
               24  JUMP_FORWARD         32  'to 32'
             26_0  COME_FROM            20  '20'
               26  LOAD_GLOBAL              datetime
               28  LOAD_METHOD              timedelta
               30  CALL_METHOD_0         0  ''
             32_0  COME_FROM            24  '24'
               32  STORE_FAST               'offset'

 L.  60        34  LOAD_FAST                'time'
               36  LOAD_ATTR                replace
               38  LOAD_CONST               None
               40  LOAD_CONST               ('tzinfo',)
               42  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               44  LOAD_FAST                'offset'
               46  BINARY_SUBTRACT  
               48  RETURN_VALUE     
             50_0  COME_FROM             8  '8'

 L.  62        50  LOAD_FAST                'time'
               52  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


class Version(Enum):
    v1 = 0
    v3 = 2


def load_pem_x509_certificate(data, backend=None):
    backend = _get_backend(backend)
    return backend.load_pem_x509_certificate(data)


def load_der_x509_certificate(data, backend=None):
    backend = _get_backend(backend)
    return backend.load_der_x509_certificate(data)


def load_pem_x509_csr(data, backend=None):
    backend = _get_backend(backend)
    return backend.load_pem_x509_csr(data)


def load_der_x509_csr(data, backend=None):
    backend = _get_backend(backend)
    return backend.load_der_x509_csr(data)


def load_pem_x509_crl(data, backend=None):
    backend = _get_backend(backend)
    return backend.load_pem_x509_crl(data)


def load_der_x509_crl(data, backend=None):
    backend = _get_backend(backend)
    return backend.load_der_x509_crl(data)


class InvalidVersion(Exception):

    def __init__(self, msg, parsed_version):
        super(InvalidVersion, self).__init__(msg)
        self.parsed_version = parsed_version


@six.add_metaclass(abc.ABCMeta)
class Certificate(object):

    @abc.abstractmethod
    def fingerprint(self, algorithm):
        """
        Returns bytes using digest passed.
        """
        pass

    @abc.abstractproperty
    def serial_number(self):
        """
        Returns certificate serial number
        """
        pass

    @abc.abstractproperty
    def version(self):
        """
        Returns the certificate version
        """
        pass

    @abc.abstractmethod
    def public_key(self):
        """
        Returns the public key
        """
        pass

    @abc.abstractproperty
    def not_valid_before(self):
        """
        Not before time (represented as UTC datetime)
        """
        pass

    @abc.abstractproperty
    def not_valid_after(self):
        """
        Not after time (represented as UTC datetime)
        """
        pass

    @abc.abstractproperty
    def issuer(self):
        """
        Returns the issuer name object.
        """
        pass

    @abc.abstractproperty
    def subject(self):
        """
        Returns the subject name object.
        """
        pass

    @abc.abstractproperty
    def signature_hash_algorithm(self):
        """
        Returns a HashAlgorithm corresponding to the type of the digest signed
        in the certificate.
        """
        pass

    @abc.abstractproperty
    def signature_algorithm_oid(self):
        """
        Returns the ObjectIdentifier of the signature algorithm.
        """
        pass

    @abc.abstractproperty
    def extensions(self):
        """
        Returns an Extensions object.
        """
        pass

    @abc.abstractproperty
    def signature(self):
        """
        Returns the signature bytes.
        """
        pass

    @abc.abstractproperty
    def tbs_certificate_bytes(self):
        """
        Returns the tbsCertificate payload bytes as defined in RFC 5280.
        """
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        """
        Checks equality.
        """
        pass

    @abc.abstractmethod
    def __ne__(self, other):
        """
        Checks not equal.
        """
        pass

    @abc.abstractmethod
    def __hash__(self):
        """
        Computes a hash.
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding):
        """
        Serializes the certificate to PEM or DER format.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class CertificateRevocationList(object):

    @abc.abstractmethod
    def public_bytes(self, encoding):
        """
        Serializes the CRL to PEM or DER format.
        """
        pass

    @abc.abstractmethod
    def fingerprint(self, algorithm):
        """
        Returns bytes using digest passed.
        """
        pass

    @abc.abstractmethod
    def get_revoked_certificate_by_serial_number(self, serial_number):
        """
        Returns an instance of RevokedCertificate or None if the serial_number
        is not in the CRL.
        """
        pass

    @abc.abstractproperty
    def signature_hash_algorithm(self):
        """
        Returns a HashAlgorithm corresponding to the type of the digest signed
        in the certificate.
        """
        pass

    @abc.abstractproperty
    def signature_algorithm_oid(self):
        """
        Returns the ObjectIdentifier of the signature algorithm.
        """
        pass

    @abc.abstractproperty
    def issuer(self):
        """
        Returns the X509Name with the issuer of this CRL.
        """
        pass

    @abc.abstractproperty
    def next_update(self):
        """
        Returns the date of next update for this CRL.
        """
        pass

    @abc.abstractproperty
    def last_update(self):
        """
        Returns the date of last update for this CRL.
        """
        pass

    @abc.abstractproperty
    def extensions(self):
        """
        Returns an Extensions object containing a list of CRL extensions.
        """
        pass

    @abc.abstractproperty
    def signature(self):
        """
        Returns the signature bytes.
        """
        pass

    @abc.abstractproperty
    def tbs_certlist_bytes(self):
        """
        Returns the tbsCertList payload bytes as defined in RFC 5280.
        """
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        """
        Checks equality.
        """
        pass

    @abc.abstractmethod
    def __ne__(self, other):
        """
        Checks not equal.
        """
        pass

    @abc.abstractmethod
    def __len__(self):
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
    def is_signature_valid(self, public_key):
        """
        Verifies signature of revocation list against given public key.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class CertificateSigningRequest(object):

    @abc.abstractmethod
    def __eq__(self, other):
        """
        Checks equality.
        """
        pass

    @abc.abstractmethod
    def __ne__(self, other):
        """
        Checks not equal.
        """
        pass

    @abc.abstractmethod
    def __hash__(self):
        """
        Computes a hash.
        """
        pass

    @abc.abstractmethod
    def public_key(self):
        """
        Returns the public key
        """
        pass

    @abc.abstractproperty
    def subject(self):
        """
        Returns the subject name object.
        """
        pass

    @abc.abstractproperty
    def signature_hash_algorithm(self):
        """
        Returns a HashAlgorithm corresponding to the type of the digest signed
        in the certificate.
        """
        pass

    @abc.abstractproperty
    def signature_algorithm_oid(self):
        """
        Returns the ObjectIdentifier of the signature algorithm.
        """
        pass

    @abc.abstractproperty
    def extensions(self):
        """
        Returns the extensions in the signing request.
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding):
        """
        Encodes the request to PEM or DER format.
        """
        pass

    @abc.abstractproperty
    def signature(self):
        """
        Returns the signature bytes.
        """
        pass

    @abc.abstractproperty
    def tbs_certrequest_bytes(self):
        """
        Returns the PKCS#10 CertificationRequestInfo bytes as defined in RFC
        2986.
        """
        pass

    @abc.abstractproperty
    def is_signature_valid(self):
        """
        Verifies signature of signing request.
        """
        pass

    @abc.abstractproperty
    def get_attribute_for_oid(self):
        """
        Get the attribute value for a given OID.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class RevokedCertificate(object):

    @abc.abstractproperty
    def serial_number(self):
        """
        Returns the serial number of the revoked certificate.
        """
        pass

    @abc.abstractproperty
    def revocation_date(self):
        """
        Returns the date of when this certificate was revoked.
        """
        pass

    @abc.abstractproperty
    def extensions(self):
        """
        Returns an Extensions object containing a list of Revoked extensions.
        """
        pass


class CertificateSigningRequestBuilder(object):

    def __init__(self, subject_name=None, extensions=[], attributes=[]):
        """
        Creates an empty X.509 certificate request (v1).
        """
        self._subject_name = subject_name
        self._extensions = extensions
        self._attributes = attributes

    def subject_name--- This code section failed: ---

 L. 436         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'name'
                4  LOAD_GLOBAL              Name
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 437        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'Expecting x509.Name object.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 438        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _subject_name
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 439        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'The subject name may only be set once.'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 440        36  LOAD_GLOBAL              CertificateSigningRequestBuilder

 L. 441        38  LOAD_FAST                'name'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _extensions
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _attributes

 L. 440        48  CALL_FUNCTION_3       3  ''
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def add_extension(self, extension, critical):
        """
        Adds an X.509 extension to the certificate request.
        """
        if not isinstance(extension, ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = Extension(extension.oid, critical, extension)
        _reject_duplicate_extension(extension, self._extensions)
        return CertificateSigningRequestBuilder(self._subject_name, self._extensions + [extension], self._attributes)

    def add_attribute(self, oid, value):
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

 L. 482         0  LOAD_GLOBAL              _get_backend
                2  LOAD_FAST                'backend'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'backend'

 L. 483         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _subject_name
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 484        18  LOAD_GLOBAL              ValueError
               20  LOAD_STR                 'A CertificateSigningRequest must have a subject'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 485        26  LOAD_FAST                'backend'
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

 L. 512         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'name'
                4  LOAD_GLOBAL              Name
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 513        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'Expecting x509.Name object.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 514        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _issuer_name
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 515        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'The issuer name may only be set once.'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 516        36  LOAD_GLOBAL              CertificateBuilder

 L. 517        38  LOAD_FAST                'name'

 L. 518        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _subject_name

 L. 519        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _public_key

 L. 520        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _serial_number

 L. 521        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _not_valid_before

 L. 522        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _not_valid_after

 L. 523        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _extensions

 L. 516        64  CALL_FUNCTION_7       7  ''
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def subject_name--- This code section failed: ---

 L. 530         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'name'
                4  LOAD_GLOBAL              Name
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 531        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'Expecting x509.Name object.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 532        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _subject_name
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 533        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'The subject name may only be set once.'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 534        36  LOAD_GLOBAL              CertificateBuilder

 L. 535        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _issuer_name

 L. 536        42  LOAD_FAST                'name'

 L. 537        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _public_key

 L. 538        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _serial_number

 L. 539        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _not_valid_before

 L. 540        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _not_valid_after

 L. 541        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _extensions

 L. 534        64  CALL_FUNCTION_7       7  ''
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def public_key--- This code section failed: ---

 L. 548         0  LOAD_GLOBAL              isinstance

 L. 549         2  LOAD_FAST                'key'

 L. 551         4  LOAD_GLOBAL              dsa
                6  LOAD_ATTR                DSAPublicKey

 L. 552         8  LOAD_GLOBAL              rsa
               10  LOAD_ATTR                RSAPublicKey

 L. 553        12  LOAD_GLOBAL              ec
               14  LOAD_ATTR                EllipticCurvePublicKey

 L. 554        16  LOAD_GLOBAL              ed25519
               18  LOAD_ATTR                Ed25519PublicKey

 L. 555        20  LOAD_GLOBAL              ed448
               22  LOAD_ATTR                Ed448PublicKey

 L. 550        24  BUILD_TUPLE_5         5 

 L. 548        26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_TRUE     38  'to 38'

 L. 558        30  LOAD_GLOBAL              TypeError

 L. 559        32  LOAD_STR                 'Expecting one of DSAPublicKey, RSAPublicKey, EllipticCurvePublicKey, Ed25519PublicKey or Ed448PublicKey.'

 L. 558        34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 563        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _public_key
               42  LOAD_CONST               None
               44  <117>                 1  ''
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L. 564        48  LOAD_GLOBAL              ValueError
               50  LOAD_STR                 'The public key may only be set once.'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L. 565        56  LOAD_GLOBAL              CertificateBuilder

 L. 566        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _issuer_name

 L. 567        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _subject_name

 L. 568        66  LOAD_FAST                'key'

 L. 569        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _serial_number

 L. 570        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _not_valid_before

 L. 571        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _not_valid_after

 L. 572        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _extensions

 L. 565        84  CALL_FUNCTION_7       7  ''
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 44

    def serial_number--- This code section failed: ---

 L. 579         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'number'
                4  LOAD_GLOBAL              six
                6  LOAD_ATTR                integer_types
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'

 L. 580        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'Serial number must be of integral type.'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 581        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _serial_number
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 582        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'The serial number may only be set once.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 583        38  LOAD_FAST                'number'
               40  LOAD_CONST               0
               42  COMPARE_OP               <=
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 584        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'The serial number should be positive.'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'

 L. 588        54  LOAD_FAST                'number'
               56  LOAD_METHOD              bit_length
               58  CALL_METHOD_0         0  ''
               60  LOAD_CONST               160
               62  COMPARE_OP               >=
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L. 589        66  LOAD_GLOBAL              ValueError

 L. 590        68  LOAD_STR                 'The serial number should not be more than 159 bits.'

 L. 589        70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            64  '64'

 L. 592        74  LOAD_GLOBAL              CertificateBuilder

 L. 593        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _issuer_name

 L. 594        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _subject_name

 L. 595        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _public_key

 L. 596        88  LOAD_FAST                'number'

 L. 597        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _not_valid_before

 L. 598        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _not_valid_after

 L. 599        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _extensions

 L. 592       102  CALL_FUNCTION_7       7  ''
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    def not_valid_before--- This code section failed: ---

 L. 606         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'time'
                4  LOAD_GLOBAL              datetime
                6  LOAD_ATTR                datetime
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'

 L. 607        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'Expecting datetime object.'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 608        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _not_valid_before
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 609        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'The not valid before may only be set once.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 610        38  LOAD_GLOBAL              _convert_to_naive_utc_time
               40  LOAD_FAST                'time'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'time'

 L. 611        46  LOAD_FAST                'time'
               48  LOAD_GLOBAL              _EARLIEST_UTC_TIME
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 612        54  LOAD_GLOBAL              ValueError

 L. 613        56  LOAD_STR                 'The not valid before date must be on or after 1950 January 1).'

 L. 612        58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 616        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _not_valid_after
               66  LOAD_CONST               None
               68  <117>                 1  ''
               70  POP_JUMP_IF_FALSE    90  'to 90'
               72  LOAD_FAST                'time'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _not_valid_after
               78  COMPARE_OP               >
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 617        82  LOAD_GLOBAL              ValueError

 L. 618        84  LOAD_STR                 'The not valid before date must be before the not valid after date.'

 L. 617        86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'
             90_1  COME_FROM            70  '70'

 L. 621        90  LOAD_GLOBAL              CertificateBuilder

 L. 622        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _issuer_name

 L. 623        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _subject_name

 L. 624       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _public_key

 L. 625       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _serial_number

 L. 626       108  LOAD_FAST                'time'

 L. 627       110  LOAD_FAST                'self'
              112  LOAD_ATTR                _not_valid_after

 L. 628       114  LOAD_FAST                'self'
              116  LOAD_ATTR                _extensions

 L. 621       118  CALL_FUNCTION_7       7  ''
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    def not_valid_after--- This code section failed: ---

 L. 635         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'time'
                4  LOAD_GLOBAL              datetime
                6  LOAD_ATTR                datetime
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'

 L. 636        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'Expecting datetime object.'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 637        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _not_valid_after
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 638        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'The not valid after may only be set once.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 639        38  LOAD_GLOBAL              _convert_to_naive_utc_time
               40  LOAD_FAST                'time'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'time'

 L. 640        46  LOAD_FAST                'time'
               48  LOAD_GLOBAL              _EARLIEST_UTC_TIME
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 641        54  LOAD_GLOBAL              ValueError

 L. 642        56  LOAD_STR                 'The not valid after date must be on or after 1950 January 1.'

 L. 641        58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 646        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _not_valid_before
               66  LOAD_CONST               None
               68  <117>                 1  ''

 L. 645        70  POP_JUMP_IF_FALSE    90  'to 90'

 L. 647        72  LOAD_FAST                'time'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _not_valid_before
               78  COMPARE_OP               <

 L. 645        80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 649        82  LOAD_GLOBAL              ValueError

 L. 650        84  LOAD_STR                 'The not valid after date must be after the not valid before date.'

 L. 649        86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'
             90_1  COME_FROM            70  '70'

 L. 653        90  LOAD_GLOBAL              CertificateBuilder

 L. 654        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _issuer_name

 L. 655        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _subject_name

 L. 656       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _public_key

 L. 657       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _serial_number

 L. 658       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _not_valid_before

 L. 659       112  LOAD_FAST                'time'

 L. 660       114  LOAD_FAST                'self'
              116  LOAD_ATTR                _extensions

 L. 653       118  CALL_FUNCTION_7       7  ''
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    def add_extension(self, extension, critical):
        """
        Adds an X.509 extension to the certificate.
        """
        if not isinstance(extension, ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = Extension(extension.oid, critical, extension)
        _reject_duplicate_extension(extension, self._extensions)
        return CertificateBuilderself._issuer_nameself._subject_nameself._public_keyself._serial_numberself._not_valid_beforeself._not_valid_after(self._extensions + [extension])

    def sign--- This code section failed: ---

 L. 687         0  LOAD_GLOBAL              _get_backend
                2  LOAD_FAST                'backend'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'backend'

 L. 688         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _subject_name
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 689        18  LOAD_GLOBAL              ValueError
               20  LOAD_STR                 'A certificate must have a subject name'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 691        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _issuer_name
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 692        36  LOAD_GLOBAL              ValueError
               38  LOAD_STR                 'A certificate must have an issuer name'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'

 L. 694        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _serial_number
               48  LOAD_CONST               None
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 695        54  LOAD_GLOBAL              ValueError
               56  LOAD_STR                 'A certificate must have a serial number'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 697        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _not_valid_before
               66  LOAD_CONST               None
               68  <117>                 0  ''
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 698        72  LOAD_GLOBAL              ValueError
               74  LOAD_STR                 'A certificate must have a not valid before time'
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            70  '70'

 L. 700        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _not_valid_after
               84  LOAD_CONST               None
               86  <117>                 0  ''
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L. 701        90  LOAD_GLOBAL              ValueError
               92  LOAD_STR                 'A certificate must have a not valid after time'
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            88  '88'

 L. 703        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _public_key
              102  LOAD_CONST               None
              104  <117>                 0  ''
              106  POP_JUMP_IF_FALSE   116  'to 116'

 L. 704       108  LOAD_GLOBAL              ValueError
              110  LOAD_STR                 'A certificate must have a public key'
              112  CALL_FUNCTION_1       1  ''
              114  RAISE_VARARGS_1       1  'exception instance'
            116_0  COME_FROM           106  '106'

 L. 706       116  LOAD_FAST                'backend'
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

 L. 725         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'issuer_name'
                4  LOAD_GLOBAL              Name
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 726        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'Expecting x509.Name object.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 727        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _issuer_name
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 728        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'The issuer name may only be set once.'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 729        36  LOAD_GLOBAL              CertificateRevocationListBuilder

 L. 730        38  LOAD_FAST                'issuer_name'

 L. 731        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _last_update

 L. 732        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _next_update

 L. 733        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _extensions

 L. 734        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _revoked_certificates

 L. 729        56  CALL_FUNCTION_5       5  ''
               58  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def last_update--- This code section failed: ---

 L. 738         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'last_update'
                4  LOAD_GLOBAL              datetime
                6  LOAD_ATTR                datetime
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'

 L. 739        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'Expecting datetime object.'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 740        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _last_update
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 741        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'Last update may only be set once.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 742        38  LOAD_GLOBAL              _convert_to_naive_utc_time
               40  LOAD_FAST                'last_update'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'last_update'

 L. 743        46  LOAD_FAST                'last_update'
               48  LOAD_GLOBAL              _EARLIEST_UTC_TIME
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 744        54  LOAD_GLOBAL              ValueError

 L. 745        56  LOAD_STR                 'The last update date must be on or after 1950 January 1.'

 L. 744        58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 747        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _next_update
               66  LOAD_CONST               None
               68  <117>                 1  ''
               70  POP_JUMP_IF_FALSE    90  'to 90'
               72  LOAD_FAST                'last_update'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _next_update
               78  COMPARE_OP               >
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 748        82  LOAD_GLOBAL              ValueError

 L. 749        84  LOAD_STR                 'The last update date must be before the next update date.'

 L. 748        86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'
             90_1  COME_FROM            70  '70'

 L. 751        90  LOAD_GLOBAL              CertificateRevocationListBuilder

 L. 752        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _issuer_name

 L. 753        96  LOAD_FAST                'last_update'

 L. 754        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _next_update

 L. 755       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _extensions

 L. 756       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _revoked_certificates

 L. 751       110  CALL_FUNCTION_5       5  ''
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    def next_update--- This code section failed: ---

 L. 760         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'next_update'
                4  LOAD_GLOBAL              datetime
                6  LOAD_ATTR                datetime
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'

 L. 761        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'Expecting datetime object.'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 762        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _next_update
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 763        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'Last update may only be set once.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 764        38  LOAD_GLOBAL              _convert_to_naive_utc_time
               40  LOAD_FAST                'next_update'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'next_update'

 L. 765        46  LOAD_FAST                'next_update'
               48  LOAD_GLOBAL              _EARLIEST_UTC_TIME
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 766        54  LOAD_GLOBAL              ValueError

 L. 767        56  LOAD_STR                 'The last update date must be on or after 1950 January 1.'

 L. 766        58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 769        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _last_update
               66  LOAD_CONST               None
               68  <117>                 1  ''
               70  POP_JUMP_IF_FALSE    90  'to 90'
               72  LOAD_FAST                'next_update'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _last_update
               78  COMPARE_OP               <
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 770        82  LOAD_GLOBAL              ValueError

 L. 771        84  LOAD_STR                 'The next update date must be after the last update date.'

 L. 770        86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'
             90_1  COME_FROM            70  '70'

 L. 773        90  LOAD_GLOBAL              CertificateRevocationListBuilder

 L. 774        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _issuer_name

 L. 775        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _last_update

 L. 776       100  LOAD_FAST                'next_update'

 L. 777       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _extensions

 L. 778       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _revoked_certificates

 L. 773       110  CALL_FUNCTION_5       5  ''
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    def add_extension(self, extension, critical):
        """
        Adds an X.509 extension to the certificate revocation list.
        """
        if not isinstance(extension, ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = Extension(extension.oid, critical, extension)
        _reject_duplicate_extension(extension, self._extensions)
        return CertificateRevocationListBuilderself._issuer_nameself._last_updateself._next_update(self._extensions + [extension])self._revoked_certificates

    def add_revoked_certificate(self, revoked_certificate):
        """
        Adds a revoked certificate to the CRL.
        """
        if not isinstance(revoked_certificate, RevokedCertificate):
            raise TypeError('Must be an instance of RevokedCertificate')
        return CertificateRevocationListBuilderself._issuer_nameself._last_updateself._next_updateself._extensions(self._revoked_certificates + [revoked_certificate])

    def sign--- This code section failed: ---

 L. 814         0  LOAD_GLOBAL              _get_backend
                2  LOAD_FAST                'backend'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'backend'

 L. 815         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _issuer_name
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 816        18  LOAD_GLOBAL              ValueError
               20  LOAD_STR                 'A CRL must have an issuer name'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 818        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _last_update
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 819        36  LOAD_GLOBAL              ValueError
               38  LOAD_STR                 'A CRL must have a last update time'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'

 L. 821        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _next_update
               48  LOAD_CONST               None
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 822        54  LOAD_GLOBAL              ValueError
               56  LOAD_STR                 'A CRL must have a next update time'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 824        62  LOAD_FAST                'backend'
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

 L. 836         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'number'
                4  LOAD_GLOBAL              six
                6  LOAD_ATTR                integer_types
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'

 L. 837        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'Serial number must be of integral type.'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 838        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _serial_number
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 839        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'The serial number may only be set once.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 840        38  LOAD_FAST                'number'
               40  LOAD_CONST               0
               42  COMPARE_OP               <=
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 841        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'The serial number should be positive'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'

 L. 845        54  LOAD_FAST                'number'
               56  LOAD_METHOD              bit_length
               58  CALL_METHOD_0         0  ''
               60  LOAD_CONST               160
               62  COMPARE_OP               >=
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L. 846        66  LOAD_GLOBAL              ValueError

 L. 847        68  LOAD_STR                 'The serial number should not be more than 159 bits.'

 L. 846        70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            64  '64'

 L. 849        74  LOAD_GLOBAL              RevokedCertificateBuilder

 L. 850        76  LOAD_FAST                'number'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _revocation_date
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                _extensions

 L. 849        86  CALL_FUNCTION_3       3  ''
               88  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    def revocation_date--- This code section failed: ---

 L. 854         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'time'
                4  LOAD_GLOBAL              datetime
                6  LOAD_ATTR                datetime
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'

 L. 855        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'Expecting datetime object.'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 856        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _revocation_date
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 857        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'The revocation date may only be set once.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 858        38  LOAD_GLOBAL              _convert_to_naive_utc_time
               40  LOAD_FAST                'time'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'time'

 L. 859        46  LOAD_FAST                'time'
               48  LOAD_GLOBAL              _EARLIEST_UTC_TIME
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 860        54  LOAD_GLOBAL              ValueError

 L. 861        56  LOAD_STR                 'The revocation date must be on or after 1950 January 1.'

 L. 860        58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 863        62  LOAD_GLOBAL              RevokedCertificateBuilder

 L. 864        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _serial_number
               68  LOAD_FAST                'time'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _extensions

 L. 863        74  CALL_FUNCTION_3       3  ''
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    def add_extension(self, extension, critical):
        if not isinstance(extension, ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = Extension(extension.oid, critical, extension)
        _reject_duplicate_extension(extension, self._extensions)
        return RevokedCertificateBuilder(self._serial_number, self._revocation_date, self._extensions + [extension])

    def build--- This code section failed: ---

 L. 880         0  LOAD_GLOBAL              _get_backend
                2  LOAD_FAST                'backend'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'backend'

 L. 881         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _serial_number
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 882        18  LOAD_GLOBAL              ValueError
               20  LOAD_STR                 'A revoked certificate must have a serial number'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 883        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _revocation_date
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 884        36  LOAD_GLOBAL              ValueError

 L. 885        38  LOAD_STR                 'A revoked certificate must have a revocation date'

 L. 884        40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'

 L. 888        44  LOAD_FAST                'backend'
               46  LOAD_METHOD              create_x509_revoked_certificate
               48  LOAD_FAST                'self'
               50  CALL_METHOD_1         1  ''
               52  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14


def random_serial_number():
    return utils.int_from_bytes(os.urandom(20), 'big') >> 1