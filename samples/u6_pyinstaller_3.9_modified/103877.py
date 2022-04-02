# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\ciphers\modes.py
from __future__ import absolute_import, division, print_function
import abc, six
from cryptography import utils

@six.add_metaclass(abc.ABCMeta)
class Mode(object):

    @abc.abstractproperty
    def name(self):
        """
        A string naming this mode (e.g. "ECB", "CBC").
        """
        pass

    @abc.abstractmethod
    def validate_for_algorithm(self, algorithm):
        """
        Checks that all the necessary invariants of this (mode, algorithm)
        combination are met.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class ModeWithInitializationVector(object):

    @abc.abstractproperty
    def initialization_vector(self):
        """
        The value of the initialization vector for this mode as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class ModeWithTweak(object):

    @abc.abstractproperty
    def tweak(self):
        """
        The value of the tweak for this mode as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class ModeWithNonce(object):

    @abc.abstractproperty
    def nonce(self):
        """
        The value of the nonce for this mode as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class ModeWithAuthenticationTag(object):

    @abc.abstractproperty
    def tag(self):
        """
        The value of the tag supplied to the constructor of this mode.
        """
        pass


def _check_aes_key_length(self, algorithm):
    if algorithm.key_size > 256:
        if algorithm.name == 'AES':
            raise ValueError('Only 128, 192, and 256 bit keys are allowed for this AES mode')


def _check_iv_length(self, algorithm):
    if len(self.initialization_vector) * 8 != algorithm.block_size:
        raise ValueError('Invalid IV size ({}) for {}.'.format(len(self.initialization_vector), self.name))


def _check_iv_and_key_length(self, algorithm):
    _check_aes_key_length(self, algorithm)
    _check_iv_length(self, algorithm)


@utils.register_interface(Mode)
@utils.register_interface(ModeWithInitializationVector)
class CBC(object):
    name = 'CBC'

    def __init__(self, initialization_vector):
        utils._check_byteslike('initialization_vector', initialization_vector)
        self._initialization_vector = initialization_vector

    initialization_vector = utils.read_only_property('_initialization_vector')
    validate_for_algorithm = _check_iv_and_key_length


@utils.register_interface(Mode)
@utils.register_interface(ModeWithTweak)
class XTS(object):
    name = 'XTS'

    def __init__(self, tweak):
        utils._check_byteslike('tweak', tweak)
        if len(tweak) != 16:
            raise ValueError('tweak must be 128-bits (16 bytes)')
        self._tweak = tweak

    tweak = utils.read_only_property('_tweak')

    def validate_for_algorithm--- This code section failed: ---

 L. 116         0  LOAD_FAST                'algorithm'
                2  LOAD_ATTR                key_size
                4  LOAD_CONST               (256, 512)
                6  <118>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 117        10  LOAD_GLOBAL              ValueError

 L. 118        12  LOAD_STR                 'The XTS specification requires a 256-bit key for AES-128-XTS and 512-bit key for AES-256-XTS'

 L. 117        14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1


@utils.register_interface(Mode)
class ECB(object):
    name = 'ECB'
    validate_for_algorithm = _check_aes_key_length


@utils.register_interface(Mode)
@utils.register_interface(ModeWithInitializationVector)
class OFB(object):
    name = 'OFB'

    def __init__(self, initialization_vector):
        utils._check_byteslike('initialization_vector', initialization_vector)
        self._initialization_vector = initialization_vector

    initialization_vector = utils.read_only_property('_initialization_vector')
    validate_for_algorithm = _check_iv_and_key_length


@utils.register_interface(Mode)
@utils.register_interface(ModeWithInitializationVector)
class CFB(object):
    name = 'CFB'

    def __init__(self, initialization_vector):
        utils._check_byteslike('initialization_vector', initialization_vector)
        self._initialization_vector = initialization_vector

    initialization_vector = utils.read_only_property('_initialization_vector')
    validate_for_algorithm = _check_iv_and_key_length


@utils.register_interface(Mode)
@utils.register_interface(ModeWithInitializationVector)
class CFB8(object):
    name = 'CFB8'

    def __init__(self, initialization_vector):
        utils._check_byteslike('initialization_vector', initialization_vector)
        self._initialization_vector = initialization_vector

    initialization_vector = utils.read_only_property('_initialization_vector')
    validate_for_algorithm = _check_iv_and_key_length


@utils.register_interface(Mode)
@utils.register_interface(ModeWithNonce)
class CTR(object):
    name = 'CTR'

    def __init__(self, nonce):
        utils._check_byteslike('nonce', nonce)
        self._nonce = nonce

    nonce = utils.read_only_property('_nonce')

    def validate_for_algorithm(self, algorithm):
        _check_aes_key_length(self, algorithm)
        if len(self.nonce) * 8 != algorithm.block_size:
            raise ValueError('Invalid nonce size ({}) for {}.'.format(len(self.nonce), self.name))


@utils.register_interface(Mode)
@utils.register_interface(ModeWithInitializationVector)
@utils.register_interface(ModeWithAuthenticationTag)
class GCM(object):
    name = 'GCM'
    _MAX_ENCRYPTED_BYTES = 68719476704
    _MAX_AAD_BYTES = 2305843009213693952

    def __init__--- This code section failed: ---

 L. 201         0  LOAD_GLOBAL              utils
                2  LOAD_METHOD              _check_byteslike
                4  LOAD_STR                 'initialization_vector'
                6  LOAD_FAST                'initialization_vector'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 202        12  LOAD_GLOBAL              len
               14  LOAD_FAST                'initialization_vector'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_CONST               8
               20  COMPARE_OP               <
               22  POP_JUMP_IF_TRUE     36  'to 36'
               24  LOAD_GLOBAL              len
               26  LOAD_FAST                'initialization_vector'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               128
               32  COMPARE_OP               >
               34  POP_JUMP_IF_FALSE    44  'to 44'
             36_0  COME_FROM            22  '22'

 L. 203        36  LOAD_GLOBAL              ValueError

 L. 204        38  LOAD_STR                 'initialization_vector must be between 8 and 128 bytes (64 and 1024 bits).'

 L. 203        40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'

 L. 207        44  LOAD_FAST                'initialization_vector'
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _initialization_vector

 L. 208        50  LOAD_FAST                'tag'
               52  LOAD_CONST               None
               54  <117>                 1  ''
               56  POP_JUMP_IF_FALSE   112  'to 112'

 L. 209        58  LOAD_GLOBAL              utils
               60  LOAD_METHOD              _check_bytes
               62  LOAD_STR                 'tag'
               64  LOAD_FAST                'tag'
               66  CALL_METHOD_2         2  ''
               68  POP_TOP          

 L. 210        70  LOAD_FAST                'min_tag_length'
               72  LOAD_CONST               4
               74  COMPARE_OP               <
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L. 211        78  LOAD_GLOBAL              ValueError
               80  LOAD_STR                 'min_tag_length must be >= 4'
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            76  '76'

 L. 212        86  LOAD_GLOBAL              len
               88  LOAD_FAST                'tag'
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_FAST                'min_tag_length'
               94  COMPARE_OP               <
               96  POP_JUMP_IF_FALSE   112  'to 112'

 L. 213        98  LOAD_GLOBAL              ValueError

 L. 214       100  LOAD_STR                 'Authentication tag must be {} bytes or longer.'
              102  LOAD_METHOD              format

 L. 215       104  LOAD_FAST                'min_tag_length'

 L. 214       106  CALL_METHOD_1         1  ''

 L. 213       108  CALL_FUNCTION_1       1  ''
              110  RAISE_VARARGS_1       1  'exception instance'
            112_0  COME_FROM            96  '96'
            112_1  COME_FROM            56  '56'

 L. 218       112  LOAD_FAST                'tag'
              114  LOAD_FAST                'self'
              116  STORE_ATTR               _tag

 L. 219       118  LOAD_FAST                'min_tag_length'
              120  LOAD_FAST                'self'
              122  STORE_ATTR               _min_tag_length

Parse error at or near `<117>' instruction at offset 54

    tag = utils.read_only_property('_tag')
    initialization_vector = utils.read_only_property('_initialization_vector')

    def validate_for_algorithm(self, algorithm):
        _check_aes_key_length(self, algorithm)