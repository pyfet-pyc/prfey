# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\dsa.py
import abc, typing
from cryptography import utils
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.primitives import _serialization, hashes
from cryptography.hazmat.primitives.asymmetric import AsymmetricSignatureContext, AsymmetricVerificationContext, utils as asym_utils

class DSAParameters(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def generate_private_key(self) -> 'DSAPrivateKey':
        """
        Generates and returns a DSAPrivateKey.
        """
        pass

    @abc.abstractmethod
    def parameter_numbers(self) -> 'DSAParameterNumbers':
        """
        Returns a DSAParameterNumbers.
        """
        pass


DSAParametersWithNumbers = DSAParameters

class DSAPrivateKey(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        The bit length of the prime modulus.
        """
        pass

    @abc.abstractmethod
    def public_key(self) -> 'DSAPublicKey':
        """
        The DSAPublicKey associated with this private key.
        """
        pass

    @abc.abstractmethod
    def parameters(self) -> DSAParameters:
        """
        The DSAParameters object associated with this private key.
        """
        pass

    @abc.abstractmethod
    def signer(self, signature_algorithm: hashes.HashAlgorithm) -> AsymmetricSignatureContext:
        """
        Returns an AsymmetricSignatureContext used for signing data.
        """
        pass

    @abc.abstractmethod
    def sign(self, data: bytes, algorithm: typing.Union[(asym_utils.Prehashed, hashes.HashAlgorithm)]) -> bytes:
        """
        Signs the data
        """
        pass

    @abc.abstractmethod
    def private_numbers(self) -> 'DSAPrivateNumbers':
        """
        Returns a DSAPrivateNumbers.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding: _serialization.Encoding, format: _serialization.PrivateFormat, encryption_algorithm: _serialization.KeySerializationEncryption) -> bytes:
        """
        Returns the key serialized as bytes.
        """
        pass


DSAPrivateKeyWithSerialization = DSAPrivateKey

class DSAPublicKey(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        The bit length of the prime modulus.
        """
        pass

    @abc.abstractmethod
    def parameters(self) -> DSAParameters:
        """
        The DSAParameters object associated with this public key.
        """
        pass

    @abc.abstractmethod
    def verifier(self, signature: bytes, signature_algorithm: hashes.HashAlgorithm) -> AsymmetricVerificationContext:
        """
        Returns an AsymmetricVerificationContext used for signing data.
        """
        pass

    @abc.abstractmethod
    def public_numbers(self) -> 'DSAPublicNumbers':
        """
        Returns a DSAPublicNumbers.
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding: _serialization.Encoding, format: _serialization.PublicFormat) -> bytes:
        """
        Returns the key serialized as bytes.
        """
        pass

    @abc.abstractmethod
    def verify(self, signature: bytes, data: bytes, algorithm: typing.Union[(asym_utils.Prehashed, hashes.HashAlgorithm)]):
        """
        Verifies the signature of the data.
        """
        pass


DSAPublicKeyWithSerialization = DSAPublicKey

class DSAParameterNumbers(object):

    def __init__(self, p: int, q: int, g: int):
        if not (isinstance(p, int) and isinstance(q, int) and isinstance(g, int)):
            raise TypeError('DSAParameterNumbers p, q, and g arguments must be integers.')
        self._p = p
        self._q = q
        self._g = g

    p = utils.read_only_property('_p')
    q = utils.read_only_property('_q')
    g = utils.read_only_property('_g')

    def parameters(self, backend=None) -> DSAParameters:
        backend = _get_backend(backend)
        return backend.load_dsa_parameter_numbers(self)

    def __eq__(self, other):
        if not isinstance(other, DSAParameterNumbers):
            return NotImplemented
        return self.p == other.p and self.q == other.q and self.g == other.g

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '<DSAParameterNumbers(p={self.p}, q={self.q}, g={self.g})>'.format(self=self)


class DSAPublicNumbers(object):

    def __init__(self, y: int, parameter_numbers: DSAParameterNumbers):
        if not isinstance(y, int):
            raise TypeError('DSAPublicNumbers y argument must be an integer.')
        if not isinstance(parameter_numbers, DSAParameterNumbers):
            raise TypeError('parameter_numbers must be a DSAParameterNumbers instance.')
        self._y = y
        self._parameter_numbers = parameter_numbers

    y = utils.read_only_property('_y')
    parameter_numbers = utils.read_only_property('_parameter_numbers')

    def public_key(self, backend=None) -> DSAPublicKey:
        backend = _get_backend(backend)
        return backend.load_dsa_public_numbers(self)

    def __eq__(self, other):
        if not isinstance(other, DSAPublicNumbers):
            return NotImplemented
        return self.y == other.y and self.parameter_numbers == other.parameter_numbers

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '<DSAPublicNumbers(y={self.y}, parameter_numbers={self.parameter_numbers})>'.format(self=self)


class DSAPrivateNumbers(object):

    def __init__(self, x: int, public_numbers: DSAPublicNumbers):
        if not isinstance(x, int):
            raise TypeError('DSAPrivateNumbers x argument must be an integer.')
        if not isinstance(public_numbers, DSAPublicNumbers):
            raise TypeError('public_numbers must be a DSAPublicNumbers instance.')
        self._public_numbers = public_numbers
        self._x = x

    x = utils.read_only_property('_x')
    public_numbers = utils.read_only_property('_public_numbers')

    def private_key(self, backend=None) -> DSAPrivateKey:
        backend = _get_backend(backend)
        return backend.load_dsa_private_numbers(self)

    def __eq__(self, other):
        if not isinstance(other, DSAPrivateNumbers):
            return NotImplemented
        return self.x == other.x and self.public_numbers == other.public_numbers

    def __ne__(self, other):
        return not self == other


def generate_parameters(key_size: int, backend=None) -> DSAParameters:
    backend = _get_backend(backend)
    return backend.generate_dsa_parameters(key_size)


def generate_private_key(key_size: int, backend=None) -> DSAPrivateKey:
    backend = _get_backend(backend)
    return backend.generate_dsa_private_key_and_parameters(key_size)


def _check_dsa_parameters--- This code section failed: ---

 L. 269         0  LOAD_FAST                'parameters'
                2  LOAD_ATTR                p
                4  LOAD_METHOD              bit_length
                6  CALL_METHOD_0         0  ''
                8  LOAD_CONST               (1024, 2048, 3072, 4096)
               10  <118>                 1  ''
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L. 270        14  LOAD_GLOBAL              ValueError

 L. 271        16  LOAD_STR                 'p must be exactly 1024, 2048, 3072, or 4096 bits long'

 L. 270        18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            12  '12'

 L. 273        22  LOAD_FAST                'parameters'
               24  LOAD_ATTR                q
               26  LOAD_METHOD              bit_length
               28  CALL_METHOD_0         0  ''
               30  LOAD_CONST               (160, 224, 256)
               32  <118>                 1  ''
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 274        36  LOAD_GLOBAL              ValueError
               38  LOAD_STR                 'q must be exactly 160, 224, or 256 bits long'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'

 L. 276        44  LOAD_CONST               1
               46  LOAD_FAST                'parameters'
               48  LOAD_ATTR                g
               50  DUP_TOP          
               52  ROT_THREE        
               54  COMPARE_OP               <
               56  POP_JUMP_IF_FALSE    68  'to 68'
               58  LOAD_FAST                'parameters'
               60  LOAD_ATTR                p
               62  COMPARE_OP               <
               64  POP_JUMP_IF_TRUE     78  'to 78'
               66  JUMP_FORWARD         70  'to 70'
             68_0  COME_FROM            56  '56'
               68  POP_TOP          
             70_0  COME_FROM            66  '66'

 L. 277        70  LOAD_GLOBAL              ValueError
               72  LOAD_STR                 "g, p don't satisfy 1 < g < p."
               74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            64  '64'

Parse error at or near `None' instruction at offset -1


def _check_dsa_private_numbers(numbers: DSAPrivateNumbers):
    parameters = numbers.public_numbers.parameter_numbers
    _check_dsa_parameters(parameters)
    if numbers.x <= 0 or numbers.x >= parameters.q:
        raise ValueError('x must be > 0 and < q.')
    if numbers.public_numbers.y != pow(parameters.g, numbers.x, parameters.p):
        raise ValueError('y must be equal to (g ** x % p).')