# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\asymmetric\rsa.py
import abc, typing
from math import gcd
from cryptography import utils
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.backends.interfaces import RSABackend
from cryptography.hazmat.primitives import _serialization, hashes
from cryptography.hazmat.primitives._asymmetric import AsymmetricPadding
from cryptography.hazmat.primitives.asymmetric import AsymmetricSignatureContext, AsymmetricVerificationContext, utils as asym_utils

class RSAPrivateKey(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def signer(self, padding: AsymmetricPadding, algorithm: hashes.HashAlgorithm) -> AsymmetricSignatureContext:
        """
        Returns an AsymmetricSignatureContext used for signing data.
        """
        pass

    @abc.abstractmethod
    def decrypt(self, ciphertext: bytes, padding: AsymmetricPadding) -> bytes:
        """
        Decrypts the provided ciphertext.
        """
        pass

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        The bit length of the public modulus.
        """
        pass

    @abc.abstractmethod
    def public_key(self) -> 'RSAPublicKey':
        """
        The RSAPublicKey associated with this private key.
        """
        pass

    @abc.abstractmethod
    def sign(self, data: bytes, padding: AsymmetricPadding, algorithm: typing.Union[(asym_utils.Prehashed, hashes.HashAlgorithm)]) -> bytes:
        """
        Signs the data.
        """
        pass

    @abc.abstractmethod
    def private_numbers(self) -> 'RSAPrivateNumbers':
        """
        Returns an RSAPrivateNumbers.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding: _serialization.Encoding, format: _serialization.PrivateFormat, encryption_algorithm: _serialization.KeySerializationEncryption) -> bytes:
        """
        Returns the key serialized as bytes.
        """
        pass


RSAPrivateKeyWithSerialization = RSAPrivateKey

class RSAPublicKey(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def verifier(self, signature: bytes, padding: AsymmetricPadding, algorithm: hashes.HashAlgorithm) -> AsymmetricVerificationContext:
        """
        Returns an AsymmetricVerificationContext used for verifying signatures.
        """
        pass

    @abc.abstractmethod
    def encrypt(self, plaintext: bytes, padding: AsymmetricPadding) -> bytes:
        """
        Encrypts the given plaintext.
        """
        pass

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        The bit length of the public modulus.
        """
        pass

    @abc.abstractmethod
    def public_numbers(self) -> 'RSAPublicNumbers':
        """
        Returns an RSAPublicNumbers
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding: _serialization.Encoding, format: _serialization.PublicFormat) -> bytes:
        """
        Returns the key serialized as bytes.
        """
        pass

    @abc.abstractmethod
    def verify(self, signature: bytes, data: bytes, padding: AsymmetricPadding, algorithm: typing.Union[(asym_utils.Prehashed, hashes.HashAlgorithm)]) -> None:
        """
        Verifies the signature of the data.
        """
        pass

    @abc.abstractmethod
    def recover_data_from_signature(self, signature: bytes, padding: AsymmetricPadding, algorithm: typing.Optional[hashes.HashAlgorithm]) -> bytes:
        """
        Recovers the original data from the signature.
        """
        pass


RSAPublicKeyWithSerialization = RSAPublicKey

def generate_private_key(public_exponent: int, key_size: int, backend=None) -> RSAPrivateKey:
    backend = _get_backend(backend)
    if not isinstance(backend, RSABackend):
        raise UnsupportedAlgorithm('Backend object does not implement RSABackend.', _Reasons.BACKEND_MISSING_INTERFACE)
    _verify_rsa_parameters(public_exponent, key_size)
    return backend.generate_rsa_private_key(public_exponent, key_size)


def _verify_rsa_parameters--- This code section failed: ---

 L. 164         0  LOAD_FAST                'public_exponent'
                2  LOAD_CONST               (3, 65537)
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 165         8  LOAD_GLOBAL              ValueError

 L. 166        10  LOAD_STR                 'public_exponent must be either 3 (for legacy compatibility) or 65537. Almost everyone should choose 65537 here!'

 L. 165        12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 170        16  LOAD_FAST                'key_size'
               18  LOAD_CONST               512
               20  COMPARE_OP               <
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 171        24  LOAD_GLOBAL              ValueError
               26  LOAD_STR                 'key_size must be at least 512-bits.'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'

Parse error at or near `None' instruction at offset -1


def _check_private_key_components(p: int, q: int, private_exponent: int, dmp1: int, dmq1: int, iqmp: int, public_exponent: int, modulus: int) -> None:
    if modulus < 3:
        raise ValueError('modulus must be >= 3.')
    if p >= modulus:
        raise ValueError('p must be < modulus.')
    if q >= modulus:
        raise ValueError('q must be < modulus.')
    if dmp1 >= modulus:
        raise ValueError('dmp1 must be < modulus.')
    if dmq1 >= modulus:
        raise ValueError('dmq1 must be < modulus.')
    if iqmp >= modulus:
        raise ValueError('iqmp must be < modulus.')
    if private_exponent >= modulus:
        raise ValueError('private_exponent must be < modulus.')
    if public_exponent < 3 or (public_exponent >= modulus):
        raise ValueError('public_exponent must be >= 3 and < modulus.')
    if public_exponent & 1 == 0:
        raise ValueError('public_exponent must be odd.')
    if dmp1 & 1 == 0:
        raise ValueError('dmp1 must be odd.')
    if dmq1 & 1 == 0:
        raise ValueError('dmq1 must be odd.')
    if p * q != modulus:
        raise ValueError('p*q must equal modulus.')


def _check_public_key_components(e: int, n: int) -> None:
    if n < 3:
        raise ValueError('n must be >= 3.')
    if e < 3 or (e >= n):
        raise ValueError('e must be >= 3 and < n.')
    if e & 1 == 0:
        raise ValueError('e must be odd.')


def _modinv(e: int, m: int) -> int:
    """
    Modular Multiplicative Inverse. Returns x such that: (x*e) mod m == 1
    """
    x1, x2 = (1, 0)
    a, b = e, m
    while True:
        if b > 0:
            q, r = divmod(a, b)
            xn = x1 - q * x2
            a, b, x1, x2 = (b, r, x2, xn)

    return x1 % m


def rsa_crt_iqmp(p: int, q: int) -> int:
    """
    Compute the CRT (q ** -1) % p value from RSA primes p and q.
    """
    return _modinv(q, p)


def rsa_crt_dmp1(private_exponent: int, p: int) -> int:
    """
    Compute the CRT private_exponent % (p - 1) value from the RSA
    private_exponent (d) and p.
    """
    return private_exponent % (p - 1)


def rsa_crt_dmq1(private_exponent: int, q: int) -> int:
    """
    Compute the CRT private_exponent % (q - 1) value from the RSA
    private_exponent (d) and q.
    """
    return private_exponent % (q - 1)


_MAX_RECOVERY_ATTEMPTS = 1000

def rsa_recover_prime_factors--- This code section failed: ---

 L. 282         0  LOAD_FAST                'd'
                2  LOAD_FAST                'e'
                4  BINARY_MULTIPLY  
                6  LOAD_CONST               1
                8  BINARY_SUBTRACT  
               10  STORE_FAST               'ktot'

 L. 285        12  LOAD_FAST                'ktot'
               14  STORE_FAST               't'
             16_0  COME_FROM            36  '36'

 L. 286        16  LOAD_FAST                't'
               18  LOAD_CONST               2
               20  BINARY_MODULO    
               22  LOAD_CONST               0
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L. 287        28  LOAD_FAST                't'
               30  LOAD_CONST               2
               32  BINARY_FLOOR_DIVIDE
               34  STORE_FAST               't'
               36  JUMP_BACK            16  'to 16'
             38_0  COME_FROM            26  '26'

 L. 293        38  LOAD_CONST               False
               40  STORE_FAST               'spotted'

 L. 294        42  LOAD_CONST               2
               44  STORE_FAST               'a'
             46_0  COME_FROM           156  '156'

 L. 295        46  LOAD_FAST                'spotted'
               48  POP_JUMP_IF_TRUE    158  'to 158'
               50  LOAD_FAST                'a'
               52  LOAD_GLOBAL              _MAX_RECOVERY_ATTEMPTS
               54  COMPARE_OP               <
               56  POP_JUMP_IF_FALSE   158  'to 158'

 L. 296        58  LOAD_FAST                't'
               60  STORE_FAST               'k'
             62_0  COME_FROM           146  '146'

 L. 298        62  LOAD_FAST                'k'
               64  LOAD_FAST                'ktot'
               66  COMPARE_OP               <
               68  POP_JUMP_IF_FALSE   148  'to 148'

 L. 299        70  LOAD_GLOBAL              pow
               72  LOAD_FAST                'a'
               74  LOAD_FAST                'k'
               76  LOAD_FAST                'n'
               78  CALL_FUNCTION_3       3  ''
               80  STORE_FAST               'cand'

 L. 301        82  LOAD_FAST                'cand'
               84  LOAD_CONST               1
               86  COMPARE_OP               !=
               88  POP_JUMP_IF_FALSE   138  'to 138'
               90  LOAD_FAST                'cand'
               92  LOAD_FAST                'n'
               94  LOAD_CONST               1
               96  BINARY_SUBTRACT  
               98  COMPARE_OP               !=
              100  POP_JUMP_IF_FALSE   138  'to 138'
              102  LOAD_GLOBAL              pow
              104  LOAD_FAST                'cand'
              106  LOAD_CONST               2
              108  LOAD_FAST                'n'
              110  CALL_FUNCTION_3       3  ''
              112  LOAD_CONST               1
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   138  'to 138'

 L. 304       118  LOAD_GLOBAL              gcd
              120  LOAD_FAST                'cand'
              122  LOAD_CONST               1
              124  BINARY_ADD       
              126  LOAD_FAST                'n'
              128  CALL_FUNCTION_2       2  ''
              130  STORE_FAST               'p'

 L. 305       132  LOAD_CONST               True
              134  STORE_FAST               'spotted'

 L. 306       136  JUMP_FORWARD        148  'to 148'
            138_0  COME_FROM           116  '116'
            138_1  COME_FROM           100  '100'
            138_2  COME_FROM            88  '88'

 L. 307       138  LOAD_FAST                'k'
              140  LOAD_CONST               2
              142  INPLACE_MULTIPLY 
              144  STORE_FAST               'k'
              146  JUMP_BACK            62  'to 62'
            148_0  COME_FROM           136  '136'
            148_1  COME_FROM            68  '68'

 L. 309       148  LOAD_FAST                'a'
              150  LOAD_CONST               2
              152  INPLACE_ADD      
              154  STORE_FAST               'a'
              156  JUMP_BACK            46  'to 46'
            158_0  COME_FROM            56  '56'
            158_1  COME_FROM            48  '48'

 L. 310       158  LOAD_FAST                'spotted'
              160  POP_JUMP_IF_TRUE    170  'to 170'

 L. 311       162  LOAD_GLOBAL              ValueError
              164  LOAD_STR                 'Unable to compute factors p and q from exponent d.'
              166  CALL_FUNCTION_1       1  ''
              168  RAISE_VARARGS_1       1  'exception instance'
            170_0  COME_FROM           160  '160'

 L. 313       170  LOAD_GLOBAL              divmod
              172  LOAD_FAST                'n'
              174  LOAD_FAST                'p'
              176  CALL_FUNCTION_2       2  ''
              178  UNPACK_SEQUENCE_2     2 
              180  STORE_FAST               'q'
              182  STORE_FAST               'r'

 L. 314       184  LOAD_FAST                'r'
              186  LOAD_CONST               0
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_TRUE    196  'to 196'
              192  <74>             
              194  RAISE_VARARGS_1       1  'exception instance'
            196_0  COME_FROM           190  '190'

 L. 315       196  LOAD_GLOBAL              sorted
              198  LOAD_FAST                'p'
              200  LOAD_FAST                'q'
              202  BUILD_TUPLE_2         2 
              204  LOAD_CONST               True
              206  LOAD_CONST               ('reverse',)
              208  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              210  UNPACK_SEQUENCE_2     2 
              212  STORE_FAST               'p'
              214  STORE_FAST               'q'

 L. 316       216  LOAD_FAST                'p'
              218  LOAD_FAST                'q'
              220  BUILD_TUPLE_2         2 
              222  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 192


class RSAPrivateNumbers(object):

    def __init__(self, p: int, q: int, d: int, dmp1: int, dmq1: int, iqmp: int, public_numbers: 'RSAPublicNumbers'):
        if isinstance(p, int):
            if isinstance(q, int):
                if isinstance(d, int):
                    if isinstance(dmp1, int):
                        if not (isinstance(dmq1, int) and isinstance(iqmp, int)):
                            raise TypeError('RSAPrivateNumbers p, q, d, dmp1, dmq1, iqmp arguments must all be an integers.')
        if not isinstance(public_numbers, RSAPublicNumbers):
            raise TypeError('RSAPrivateNumbers public_numbers must be an RSAPublicNumbers instance.')
        self._p = p
        self._q = q
        self._d = d
        self._dmp1 = dmp1
        self._dmq1 = dmq1
        self._iqmp = iqmp
        self._public_numbers = public_numbers

    p = utils.read_only_property('_p')
    q = utils.read_only_property('_q')
    d = utils.read_only_property('_d')
    dmp1 = utils.read_only_property('_dmp1')
    dmq1 = utils.read_only_property('_dmq1')
    iqmp = utils.read_only_property('_iqmp')
    public_numbers = utils.read_only_property('_public_numbers')

    def private_key(self, backend=None) -> RSAPrivateKey:
        backend = _get_backend(backend)
        return backend.load_rsa_private_numbers(self)

    def __eq__(self, other):
        if not isinstance(other, RSAPrivateNumbers):
            return NotImplemented
        return self.p == other.p and self.q == other.q and self.d == other.d and self.dmp1 == other.dmp1 and self.dmq1 == other.dmq1 and self.iqmp == other.iqmp and self.public_numbers == other.public_numbers

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((
         self.p,
         self.q,
         self.d,
         self.dmp1,
         self.dmq1,
         self.iqmp,
         self.public_numbers))


class RSAPublicNumbers(object):

    def __init__(self, e: int, n: int):
        if not (isinstance(e, int) and isinstance(n, int)):
            raise TypeError('RSAPublicNumbers arguments must be integers.')
        self._e = e
        self._n = n

    e = utils.read_only_property('_e')
    n = utils.read_only_property('_n')

    def public_key(self, backend=None) -> RSAPublicKey:
        backend = _get_backend(backend)
        return backend.load_rsa_public_numbers(self)

    def __repr__(self):
        return '<RSAPublicNumbers(e={0.e}, n={0.n})>'.format(self)

    def __eq__(self, other):
        if not isinstance(other, RSAPublicNumbers):
            return NotImplemented
        return self.e == other.e and self.n == other.n

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.e, self.n))