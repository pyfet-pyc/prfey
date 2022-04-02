# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\dh.py
import abc, typing
from cryptography import utils
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.primitives import serialization
_MIN_MODULUS_SIZE = 512

def generate_parameters(generator, key_size, backend=None) -> 'DHParameters':
    backend = _get_backend(backend)
    return backend.generate_dh_parameters(generator, key_size)


class DHParameterNumbers(object):

    def __init__--- This code section failed: ---

 L.  24         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'p'
                4  LOAD_GLOBAL              int
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'
               10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'g'
               14  LOAD_GLOBAL              int
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_TRUE     28  'to 28'
             20_0  COME_FROM             8  '8'

 L.  25        20  LOAD_GLOBAL              TypeError
               22  LOAD_STR                 'p and g must be integers'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L.  26        28  LOAD_FAST                'q'
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    54  'to 54'
               36  LOAD_GLOBAL              isinstance
               38  LOAD_FAST                'q'
               40  LOAD_GLOBAL              int
               42  CALL_FUNCTION_2       2  ''
               44  POP_JUMP_IF_TRUE     54  'to 54'

 L.  27        46  LOAD_GLOBAL              TypeError
               48  LOAD_STR                 'q must be integer or None'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'
             54_1  COME_FROM            34  '34'

 L.  29        54  LOAD_FAST                'g'
               56  LOAD_CONST               2
               58  COMPARE_OP               <
               60  POP_JUMP_IF_FALSE    70  'to 70'

 L.  30        62  LOAD_GLOBAL              ValueError
               64  LOAD_STR                 'DH generator must be 2 or greater'
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            60  '60'

 L.  32        70  LOAD_FAST                'p'
               72  LOAD_METHOD              bit_length
               74  CALL_METHOD_0         0  ''
               76  LOAD_GLOBAL              _MIN_MODULUS_SIZE
               78  COMPARE_OP               <
               80  POP_JUMP_IF_FALSE    96  'to 96'

 L.  33        82  LOAD_GLOBAL              ValueError

 L.  34        84  LOAD_STR                 'p (modulus) must be at least {}-bit'
               86  LOAD_METHOD              format
               88  LOAD_GLOBAL              _MIN_MODULUS_SIZE
               90  CALL_METHOD_1         1  ''

 L.  33        92  CALL_FUNCTION_1       1  ''
               94  RAISE_VARARGS_1       1  'exception instance'
             96_0  COME_FROM            80  '80'

 L.  37        96  LOAD_FAST                'p'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _p

 L.  38       102  LOAD_FAST                'g'
              104  LOAD_FAST                'self'
              106  STORE_ATTR               _g

 L.  39       108  LOAD_FAST                'q'
              110  LOAD_FAST                'self'
              112  STORE_ATTR               _q

Parse error at or near `<117>' instruction at offset 32

    def __eq__(self, other):
        if not isinstanceotherDHParameterNumbers:
            return NotImplemented
        return self._p == other._p and self._g == other._g and self._q == other._q

    def __ne__(self, other):
        return not self == other

    def parameters(self, backend=None):
        backend = _get_backend(backend)
        return backend.load_dh_parameter_numbers(self)

    p = utils.read_only_property('_p')
    g = utils.read_only_property('_g')
    q = utils.read_only_property('_q')


class DHPublicNumbers(object):

    def __init__(self, y, parameter_numbers: DHParameterNumbers):
        if not isinstanceyint:
            raise TypeError('y must be an integer.')
        if not isinstanceparameter_numbersDHParameterNumbers:
            raise TypeError('parameters must be an instance of DHParameterNumbers.')
        self._y = y
        self._parameter_numbers = parameter_numbers

    def __eq__(self, other):
        if not isinstanceotherDHPublicNumbers:
            return NotImplemented
        return self._y == other._y and self._parameter_numbers == other._parameter_numbers

    def __ne__(self, other):
        return not self == other

    def public_key(self, backend=None) -> 'DHPublicKey':
        backend = _get_backend(backend)
        return backend.load_dh_public_numbers(self)

    y = utils.read_only_property('_y')
    parameter_numbers = utils.read_only_property('_parameter_numbers')


class DHPrivateNumbers(object):

    def __init__(self, x, public_numbers: DHPublicNumbers):
        if not isinstancexint:
            raise TypeError('x must be an integer.')
        if not isinstancepublic_numbersDHPublicNumbers:
            raise TypeError('public_numbers must be an instance of DHPublicNumbers.')
        self._x = x
        self._public_numbers = public_numbers

    def __eq__(self, other):
        if not isinstanceotherDHPrivateNumbers:
            return NotImplemented
        return self._x == other._x and self._public_numbers == other._public_numbers

    def __ne__(self, other):
        return not self == other

    def private_key(self, backend=None) -> 'DHPrivateKey':
        backend = _get_backend(backend)
        return backend.load_dh_private_numbers(self)

    public_numbers = utils.read_only_property('_public_numbers')
    x = utils.read_only_property('_x')


class DHParameters(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def generate_private_key(self) -> 'DHPrivateKey':
        """
        Generates and returns a DHPrivateKey.
        """
        pass

    @abc.abstractmethod
    def parameter_bytes(self, encoding: 'serialization.Encoding', format: 'serialization.ParameterFormat') -> bytes:
        """
        Returns the parameters serialized as bytes.
        """
        pass

    @abc.abstractmethod
    def parameter_numbers(self) -> DHParameterNumbers:
        """
        Returns a DHParameterNumbers.
        """
        pass


DHParametersWithSerialization = DHParameters

class DHPublicKey(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        The bit length of the prime modulus.
        """
        pass

    @abc.abstractmethod
    def parameters(self) -> DHParameters:
        """
        The DHParameters object associated with this public key.
        """
        pass

    @abc.abstractmethod
    def public_numbers(self) -> DHPublicNumbers:
        """
        Returns a DHPublicNumbers.
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding: 'serialization.Encoding', format: 'serialization.PublicFormat') -> bytes:
        """
        Returns the key serialized as bytes.
        """
        pass


DHPublicKeyWithSerialization = DHPublicKey

class DHPrivateKey(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        The bit length of the prime modulus.
        """
        pass

    @abc.abstractmethod
    def public_key(self) -> DHPublicKey:
        """
        The DHPublicKey associated with this private key.
        """
        pass

    @abc.abstractmethod
    def parameters(self) -> DHParameters:
        """
        The DHParameters object associated with this private key.
        """
        pass

    @abc.abstractmethod
    def exchange(self, peer_public_key: DHPublicKey) -> bytes:
        """
        Given peer's DHPublicKey, carry out the key exchange and
        return shared key as bytes.
        """
        pass

    @abc.abstractmethod
    def private_numbers(self) -> DHPrivateNumbers:
        """
        Returns a DHPrivateNumbers.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding: 'serialization.Encoding', format: 'serialization.PrivateFormat', encryption_algorithm: 'serialization.KeySerializationEncryption') -> bytes:
        """
        Returns the key serialized as bytes.
        """
        pass


DHPrivateKeyWithSerialization = DHPrivateKey