# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\ec.py
from __future__ import absolute_import, division, print_function
import abc, warnings, six
from cryptography import utils
from cryptography.hazmat._oid import ObjectIdentifier
from cryptography.hazmat.backends import _get_backend

class EllipticCurveOID(object):
    SECP192R1 = ObjectIdentifier('1.2.840.10045.3.1.1')
    SECP224R1 = ObjectIdentifier('1.3.132.0.33')
    SECP256K1 = ObjectIdentifier('1.3.132.0.10')
    SECP256R1 = ObjectIdentifier('1.2.840.10045.3.1.7')
    SECP384R1 = ObjectIdentifier('1.3.132.0.34')
    SECP521R1 = ObjectIdentifier('1.3.132.0.35')
    BRAINPOOLP256R1 = ObjectIdentifier('1.3.36.3.3.2.8.1.1.7')
    BRAINPOOLP384R1 = ObjectIdentifier('1.3.36.3.3.2.8.1.1.11')
    BRAINPOOLP512R1 = ObjectIdentifier('1.3.36.3.3.2.8.1.1.13')
    SECT163K1 = ObjectIdentifier('1.3.132.0.1')
    SECT163R2 = ObjectIdentifier('1.3.132.0.15')
    SECT233K1 = ObjectIdentifier('1.3.132.0.26')
    SECT233R1 = ObjectIdentifier('1.3.132.0.27')
    SECT283K1 = ObjectIdentifier('1.3.132.0.16')
    SECT283R1 = ObjectIdentifier('1.3.132.0.17')
    SECT409K1 = ObjectIdentifier('1.3.132.0.36')
    SECT409R1 = ObjectIdentifier('1.3.132.0.37')
    SECT571K1 = ObjectIdentifier('1.3.132.0.38')
    SECT571R1 = ObjectIdentifier('1.3.132.0.39')


@six.add_metaclass(abc.ABCMeta)
class EllipticCurve(object):

    @abc.abstractproperty
    def name(self):
        """
        The name of the curve. e.g. secp256r1.
        """
        pass

    @abc.abstractproperty
    def key_size(self):
        """
        Bit size of a secret scalar for the curve.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class EllipticCurveSignatureAlgorithm(object):

    @abc.abstractproperty
    def algorithm(self):
        """
        The digest algorithm used with this signature.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class EllipticCurvePrivateKey(object):

    @abc.abstractmethod
    def signer(self, signature_algorithm):
        """
        Returns an AsymmetricSignatureContext used for signing data.
        """
        pass

    @abc.abstractmethod
    def exchange(self, algorithm, peer_public_key):
        """
        Performs a key exchange operation using the provided algorithm with the
        provided peer's public key.
        """
        pass

    @abc.abstractmethod
    def public_key(self):
        """
        The EllipticCurvePublicKey for this private key.
        """
        pass

    @abc.abstractproperty
    def curve(self):
        """
        The EllipticCurve that this key is on.
        """
        pass

    @abc.abstractproperty
    def key_size(self):
        """
        Bit size of a secret scalar for the curve.
        """
        pass

    @abc.abstractmethod
    def sign(self, data, signature_algorithm):
        """
        Signs the data
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class EllipticCurvePrivateKeyWithSerialization(EllipticCurvePrivateKey):

    @abc.abstractmethod
    def private_numbers(self):
        """
        Returns an EllipticCurvePrivateNumbers.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding, format, encryption_algorithm):
        """
        Returns the key serialized as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class EllipticCurvePublicKey(object):

    @abc.abstractmethod
    def verifier(self, signature, signature_algorithm):
        """
        Returns an AsymmetricVerificationContext used for signing data.
        """
        pass

    @abc.abstractproperty
    def curve(self):
        """
        The EllipticCurve that this key is on.
        """
        pass

    @abc.abstractproperty
    def key_size(self):
        """
        Bit size of a secret scalar for the curve.
        """
        pass

    @abc.abstractmethod
    def public_numbers(self):
        """
        Returns an EllipticCurvePublicNumbers.
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding, format):
        """
        Returns the key serialized as bytes.
        """
        pass

    @abc.abstractmethod
    def verify(self, signature, data, signature_algorithm):
        """
        Verifies the signature of the data.
        """
        pass

    @classmethod
    def from_encoded_point--- This code section failed: ---

 L. 158         0  LOAD_GLOBAL              utils
                2  LOAD_METHOD              _check_bytes
                4  LOAD_STR                 'data'
                6  LOAD_FAST                'data'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 160        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'curve'
               16  LOAD_GLOBAL              EllipticCurve
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     30  'to 30'

 L. 161        22  LOAD_GLOBAL              TypeError
               24  LOAD_STR                 'curve must be an EllipticCurve instance'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L. 163        30  LOAD_GLOBAL              len
               32  LOAD_FAST                'data'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_CONST               0
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    50  'to 50'

 L. 164        42  LOAD_GLOBAL              ValueError
               44  LOAD_STR                 'data must not be an empty byte string'
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            40  '40'

 L. 166        50  LOAD_GLOBAL              six
               52  LOAD_METHOD              indexbytes
               54  LOAD_FAST                'data'
               56  LOAD_CONST               0
               58  CALL_METHOD_2         2  ''
               60  LOAD_CONST               (2, 3, 4)
               62  <118>                 1  ''
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L. 167        66  LOAD_GLOBAL              ValueError
               68  LOAD_STR                 'Unsupported elliptic curve point type'
               70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            64  '64'

 L. 169        74  LOAD_CONST               0
               76  LOAD_CONST               ('backend',)
               78  IMPORT_NAME_ATTR         cryptography.hazmat.backends.openssl.backend
               80  IMPORT_FROM              backend
               82  STORE_FAST               'backend'
               84  POP_TOP          

 L. 171        86  LOAD_FAST                'backend'
               88  LOAD_METHOD              load_elliptic_curve_public_bytes
               90  LOAD_FAST                'curve'
               92  LOAD_FAST                'data'
               94  CALL_METHOD_2         2  ''
               96  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 62


EllipticCurvePublicKeyWithSerialization = EllipticCurvePublicKey

@utils.register_interface(EllipticCurve)
class SECT571R1(object):
    name = 'sect571r1'
    key_size = 570


@utils.register_interface(EllipticCurve)
class SECT409R1(object):
    name = 'sect409r1'
    key_size = 409


@utils.register_interface(EllipticCurve)
class SECT283R1(object):
    name = 'sect283r1'
    key_size = 283


@utils.register_interface(EllipticCurve)
class SECT233R1(object):
    name = 'sect233r1'
    key_size = 233


@utils.register_interface(EllipticCurve)
class SECT163R2(object):
    name = 'sect163r2'
    key_size = 163


@utils.register_interface(EllipticCurve)
class SECT571K1(object):
    name = 'sect571k1'
    key_size = 571


@utils.register_interface(EllipticCurve)
class SECT409K1(object):
    name = 'sect409k1'
    key_size = 409


@utils.register_interface(EllipticCurve)
class SECT283K1(object):
    name = 'sect283k1'
    key_size = 283


@utils.register_interface(EllipticCurve)
class SECT233K1(object):
    name = 'sect233k1'
    key_size = 233


@utils.register_interface(EllipticCurve)
class SECT163K1(object):
    name = 'sect163k1'
    key_size = 163


@utils.register_interface(EllipticCurve)
class SECP521R1(object):
    name = 'secp521r1'
    key_size = 521


@utils.register_interface(EllipticCurve)
class SECP384R1(object):
    name = 'secp384r1'
    key_size = 384


@utils.register_interface(EllipticCurve)
class SECP256R1(object):
    name = 'secp256r1'
    key_size = 256


@utils.register_interface(EllipticCurve)
class SECP256K1(object):
    name = 'secp256k1'
    key_size = 256


@utils.register_interface(EllipticCurve)
class SECP224R1(object):
    name = 'secp224r1'
    key_size = 224


@utils.register_interface(EllipticCurve)
class SECP192R1(object):
    name = 'secp192r1'
    key_size = 192


@utils.register_interface(EllipticCurve)
class BrainpoolP256R1(object):
    name = 'brainpoolP256r1'
    key_size = 256


@utils.register_interface(EllipticCurve)
class BrainpoolP384R1(object):
    name = 'brainpoolP384r1'
    key_size = 384


@utils.register_interface(EllipticCurve)
class BrainpoolP512R1(object):
    name = 'brainpoolP512r1'
    key_size = 512


_CURVE_TYPES = {'prime192v1':SECP192R1, 
 'prime256v1':SECP256R1, 
 'secp192r1':SECP192R1, 
 'secp224r1':SECP224R1, 
 'secp256r1':SECP256R1, 
 'secp384r1':SECP384R1, 
 'secp521r1':SECP521R1, 
 'secp256k1':SECP256K1, 
 'sect163k1':SECT163K1, 
 'sect233k1':SECT233K1, 
 'sect283k1':SECT283K1, 
 'sect409k1':SECT409K1, 
 'sect571k1':SECT571K1, 
 'sect163r2':SECT163R2, 
 'sect233r1':SECT233R1, 
 'sect283r1':SECT283R1, 
 'sect409r1':SECT409R1, 
 'sect571r1':SECT571R1, 
 'brainpoolP256r1':BrainpoolP256R1, 
 'brainpoolP384r1':BrainpoolP384R1, 
 'brainpoolP512r1':BrainpoolP512R1}

@utils.register_interface(EllipticCurveSignatureAlgorithm)
class ECDSA(object):

    def __init__(self, algorithm):
        self._algorithm = algorithm

    algorithm = utils.read_only_property('_algorithm')


def generate_private_key(curve, backend=None):
    backend = _get_backend(backend)
    return backend.generate_elliptic_curve_private_key(curve)


def derive_private_key(private_value, curve, backend=None):
    backend = _get_backend(backend)
    if not isinstanceprivate_valuesix.integer_types:
        raise TypeError('private_value must be an integer type.')
    if private_value <= 0:
        raise ValueError('private_value must be a positive integer.')
    if not isinstancecurveEllipticCurve:
        raise TypeError('curve must provide the EllipticCurve interface.')
    return backend.derive_elliptic_curve_private_keyprivate_valuecurve


class EllipticCurvePublicNumbers(object):

    def __init__(self, x, y, curve):
        if not (isinstancexsix.integer_types and isinstanceysix.integer_types):
            raise TypeError('x and y must be integers.')
        if not isinstancecurveEllipticCurve:
            raise TypeError('curve must provide the EllipticCurve interface.')
        self._y = y
        self._x = x
        self._curve = curve

    def public_key(self, backend=None):
        backend = _get_backend(backend)
        return backend.load_elliptic_curve_public_numbers(self)

    def encode_point(self):
        warnings.warn('encode_point has been deprecated on EllipticCurvePublicNumbers and will be removed in a future version. Please use EllipticCurvePublicKey.public_bytes to obtain both compressed and uncompressed point encoding.',
          (utils.PersistentlyDeprecated2019),
          stacklevel=2)
        byte_length = (self.curve.key_size + 7) // 8
        return b'\x04' + utils.int_to_bytesself.xbyte_length + utils.int_to_bytesself.ybyte_length

    @classmethod
    def from_encoded_point(cls, curve, data):
        if not isinstancecurveEllipticCurve:
            raise TypeError('curve must be an EllipticCurve instance')
        else:
            warnings.warn('Support for unsafe construction of public numbers from encoded data will be removed in a future version. Please use EllipticCurvePublicKey.from_encoded_point',
              (utils.PersistentlyDeprecated2019),
              stacklevel=2)
            if data.startswith(b'\x04'):
                byte_length = (curve.key_size + 7) // 8
                if len(data) == 2 * byte_length + 1:
                    x = utils.int_from_bytesdata[1:byte_length + 1]'big'
                    y = utils.int_from_bytesdata[byte_length + 1:]'big'
                    return cls(x, y, curve)
                    raise ValueError('Invalid elliptic curve point data length')
                else:
                    pass
            raise ValueError('Unsupported elliptic curve point type')

    curve = utils.read_only_property('_curve')
    x = utils.read_only_property('_x')
    y = utils.read_only_property('_y')

    def __eq__(self, other):
        if not isinstanceotherEllipticCurvePublicNumbers:
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.curve.name == other.curve.name and self.curve.key_size == other.curve.key_size

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.x, self.y, self.curve.name, self.curve.key_size))

    def __repr__(self):
        return '<EllipticCurvePublicNumbers(curve={0.curve.name}, x={0.x}, y={0.y}>'.format(self)


class EllipticCurvePrivateNumbers(object):

    def __init__(self, private_value, public_numbers):
        if not isinstanceprivate_valuesix.integer_types:
            raise TypeError('private_value must be an integer.')
        if not isinstancepublic_numbersEllipticCurvePublicNumbers:
            raise TypeError('public_numbers must be an EllipticCurvePublicNumbers instance.')
        self._private_value = private_value
        self._public_numbers = public_numbers

    def private_key(self, backend=None):
        backend = _get_backend(backend)
        return backend.load_elliptic_curve_private_numbers(self)

    private_value = utils.read_only_property('_private_value')
    public_numbers = utils.read_only_property('_public_numbers')

    def __eq__(self, other):
        if not isinstanceotherEllipticCurvePrivateNumbers:
            return NotImplemented
        return self.private_value == other.private_value and self.public_numbers == other.public_numbers

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.private_value, self.public_numbers))


class ECDH(object):
    pass


_OID_TO_CURVE = {EllipticCurveOID.SECP192R1: SECP192R1, 
 EllipticCurveOID.SECP224R1: SECP224R1, 
 EllipticCurveOID.SECP256K1: SECP256K1, 
 EllipticCurveOID.SECP256R1: SECP256R1, 
 EllipticCurveOID.SECP384R1: SECP384R1, 
 EllipticCurveOID.SECP521R1: SECP521R1, 
 EllipticCurveOID.BRAINPOOLP256R1: BrainpoolP256R1, 
 EllipticCurveOID.BRAINPOOLP384R1: BrainpoolP384R1, 
 EllipticCurveOID.BRAINPOOLP512R1: BrainpoolP512R1, 
 EllipticCurveOID.SECT163K1: SECT163K1, 
 EllipticCurveOID.SECT163R2: SECT163R2, 
 EllipticCurveOID.SECT233K1: SECT233K1, 
 EllipticCurveOID.SECT233R1: SECT233R1, 
 EllipticCurveOID.SECT283K1: SECT283K1, 
 EllipticCurveOID.SECT283R1: SECT283R1, 
 EllipticCurveOID.SECT409K1: SECT409K1, 
 EllipticCurveOID.SECT409R1: SECT409R1, 
 EllipticCurveOID.SECT571K1: SECT571K1, 
 EllipticCurveOID.SECT571R1: SECT571R1}

def get_curve_for_oid--- This code section failed: ---

 L. 496         0  SETUP_FINALLY        12  'to 12'

 L. 497         2  LOAD_GLOBAL              _OID_TO_CURVE
                4  LOAD_FAST                'oid'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 498        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  <121>                36  ''
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 499        24  LOAD_GLOBAL              LookupError

 L. 500        26  LOAD_STR                 'The provided object identifier has no matching elliptic curve class'

 L. 499        28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
               32  POP_EXCEPT       
               34  JUMP_FORWARD         38  'to 38'
               36  <48>             
             38_0  COME_FROM            34  '34'

Parse error at or near `<121>' instruction at offset 16