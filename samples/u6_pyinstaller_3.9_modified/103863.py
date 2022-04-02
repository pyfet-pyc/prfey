# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\dh.py
from __future__ import absolute_import, division, print_function
import abc, six
from cryptography import utils
from cryptography.hazmat.backends import _get_backend
_MIN_MODULUS_SIZE = 512

def generate_parameters(generator, key_size, backend=None):
    backend = _get_backend(backend)
    return backend.generate_dh_parameters(generator, key_size)


class DHPrivateNumbers(object):

    def __init__(self, x, public_numbers):
        if not isinstance(x, six.integer_types):
            raise TypeError('x must be an integer.')
        if not isinstance(public_numbers, DHPublicNumbers):
            raise TypeError('public_numbers must be an instance of DHPublicNumbers.')
        self._x = x
        self._public_numbers = public_numbers

    def __eq__(self, other):
        if not isinstance(other, DHPrivateNumbers):
            return NotImplemented
        return self._x == other._x and self._public_numbers == other._public_numbers

    def __ne__(self, other):
        return not self == other

    def private_key(self, backend=None):
        backend = _get_backend(backend)
        return backend.load_dh_private_numbers(self)

    public_numbers = utils.read_only_property('_public_numbers')
    x = utils.read_only_property('_x')


class DHPublicNumbers(object):

    def __init__(self, y, parameter_numbers):
        if not isinstance(y, six.integer_types):
            raise TypeError('y must be an integer.')
        if not isinstance(parameter_numbers, DHParameterNumbers):
            raise TypeError('parameters must be an instance of DHParameterNumbers.')
        self._y = y
        self._parameter_numbers = parameter_numbers

    def __eq__(self, other):
        if not isinstance(other, DHPublicNumbers):
            return NotImplemented
        return self._y == other._y and self._parameter_numbers == other._parameter_numbers

    def __ne__(self, other):
        return not self == other

    def public_key(self, backend=None):
        backend = _get_backend(backend)
        return backend.load_dh_public_numbers(self)

    y = utils.read_only_property('_y')
    parameter_numbers = utils.read_only_property('_parameter_numbers')


class DHParameterNumbers(object):

    def __init__--- This code section failed: ---

 L.  91         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'p'
                4  LOAD_GLOBAL              six
                6  LOAD_ATTR                integer_types
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    24  'to 24'
               12  LOAD_GLOBAL              isinstance

 L.  92        14  LOAD_FAST                'g'
               16  LOAD_GLOBAL              six
               18  LOAD_ATTR                integer_types

 L.  91        20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_TRUE     32  'to 32'
             24_0  COME_FROM            10  '10'

 L.  94        24  LOAD_GLOBAL              TypeError
               26  LOAD_STR                 'p and g must be integers'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'

 L.  95        32  LOAD_FAST                'q'
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    60  'to 60'
               40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'q'
               44  LOAD_GLOBAL              six
               46  LOAD_ATTR                integer_types
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_TRUE     60  'to 60'

 L.  96        52  LOAD_GLOBAL              TypeError
               54  LOAD_STR                 'q must be integer or None'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'
             60_1  COME_FROM            38  '38'

 L.  98        60  LOAD_FAST                'g'
               62  LOAD_CONST               2
               64  COMPARE_OP               <
               66  POP_JUMP_IF_FALSE    76  'to 76'

 L.  99        68  LOAD_GLOBAL              ValueError
               70  LOAD_STR                 'DH generator must be 2 or greater'
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            66  '66'

 L. 101        76  LOAD_FAST                'p'
               78  LOAD_METHOD              bit_length
               80  CALL_METHOD_0         0  ''
               82  LOAD_GLOBAL              _MIN_MODULUS_SIZE
               84  COMPARE_OP               <
               86  POP_JUMP_IF_FALSE   102  'to 102'

 L. 102        88  LOAD_GLOBAL              ValueError

 L. 103        90  LOAD_STR                 'p (modulus) must be at least {}-bit'
               92  LOAD_METHOD              format
               94  LOAD_GLOBAL              _MIN_MODULUS_SIZE
               96  CALL_METHOD_1         1  ''

 L. 102        98  CALL_FUNCTION_1       1  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            86  '86'

 L. 106       102  LOAD_FAST                'p'
              104  LOAD_FAST                'self'
              106  STORE_ATTR               _p

 L. 107       108  LOAD_FAST                'g'
              110  LOAD_FAST                'self'
              112  STORE_ATTR               _g

 L. 108       114  LOAD_FAST                'q'
              116  LOAD_FAST                'self'
              118  STORE_ATTR               _q

Parse error at or near `<117>' instruction at offset 36

    def __eq__(self, other):
        if not isinstance(other, DHParameterNumbers):
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


@six.add_metaclass(abc.ABCMeta)
class DHParameters(object):

    @abc.abstractmethod
    def generate_private_key(self):
        """
        Generates and returns a DHPrivateKey.
        """
        pass

    @abc.abstractmethod
    def parameter_bytes(self, encoding, format):
        """
        Returns the parameters serialized as bytes.
        """
        pass

    @abc.abstractmethod
    def parameter_numbers(self):
        """
        Returns a DHParameterNumbers.
        """
        pass


DHParametersWithSerialization = DHParameters

@six.add_metaclass(abc.ABCMeta)
class DHPrivateKey(object):

    @abc.abstractproperty
    def key_size(self):
        """
        The bit length of the prime modulus.
        """
        pass

    @abc.abstractmethod
    def public_key(self):
        """
        The DHPublicKey associated with this private key.
        """
        pass

    @abc.abstractmethod
    def parameters(self):
        """
        The DHParameters object associated with this private key.
        """
        pass

    @abc.abstractmethod
    def exchange(self, peer_public_key):
        """
        Given peer's DHPublicKey, carry out the key exchange and
        return shared key as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class DHPrivateKeyWithSerialization(DHPrivateKey):

    @abc.abstractmethod
    def private_numbers(self):
        """
        Returns a DHPrivateNumbers.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding, format, encryption_algorithm):
        """
        Returns the key serialized as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class DHPublicKey(object):

    @abc.abstractproperty
    def key_size(self):
        """
        The bit length of the prime modulus.
        """
        pass

    @abc.abstractmethod
    def parameters(self):
        """
        The DHParameters object associated with this public key.
        """
        pass

    @abc.abstractmethod
    def public_numbers(self):
        """
        Returns a DHPublicNumbers.
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding, format):
        """
        Returns the key serialized as bytes.
        """
        pass


DHPublicKeyWithSerialization = DHPublicKey