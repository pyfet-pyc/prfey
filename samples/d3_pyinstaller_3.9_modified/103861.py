# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\hashes.py
from __future__ import absolute_import, division, print_function
import abc, six
from cryptography import utils
from cryptography.exceptions import AlreadyFinalized, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.backends.interfaces import HashBackend

@six.add_metaclass(abc.ABCMeta)
class HashAlgorithm(object):

    @abc.abstractproperty
    def name(self):
        """
        A string naming this algorithm (e.g. "sha256", "md5").
        """
        pass

    @abc.abstractproperty
    def digest_size(self):
        """
        The size of the resulting digest in bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class HashContext(object):

    @abc.abstractproperty
    def algorithm(self):
        """
        A HashAlgorithm that will be used by this context.
        """
        pass

    @abc.abstractmethod
    def update(self, data):
        """
        Processes the provided bytes through the hash.
        """
        pass

    @abc.abstractmethod
    def finalize(self):
        """
        Finalizes the hash context and returns the hash digest as bytes.
        """
        pass

    @abc.abstractmethod
    def copy(self):
        """
        Return a HashContext that is a copy of the current context.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class ExtendableOutputFunction(object):
    __doc__ = '\n    An interface for extendable output functions.\n    '


@utils.register_interface(HashContext)
class Hash(object):

    def __init__--- This code section failed: ---

 L.  73         0  LOAD_GLOBAL              _get_backend
                2  LOAD_FAST                'backend'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'backend'

 L.  74         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'backend'
               12  LOAD_GLOBAL              HashBackend
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     30  'to 30'

 L.  75        18  LOAD_GLOBAL              UnsupportedAlgorithm

 L.  76        20  LOAD_STR                 'Backend object does not implement HashBackend.'

 L.  77        22  LOAD_GLOBAL              _Reasons
               24  LOAD_ATTR                BACKEND_MISSING_INTERFACE

 L.  75        26  CALL_FUNCTION_2       2  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            16  '16'

 L.  80        30  LOAD_GLOBAL              isinstance
               32  LOAD_FAST                'algorithm'
               34  LOAD_GLOBAL              HashAlgorithm
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_TRUE     48  'to 48'

 L.  81        40  LOAD_GLOBAL              TypeError
               42  LOAD_STR                 'Expected instance of hashes.HashAlgorithm.'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L.  82        48  LOAD_FAST                'algorithm'
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _algorithm

 L.  84        54  LOAD_FAST                'backend'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _backend

 L.  86        60  LOAD_FAST                'ctx'
               62  LOAD_CONST               None
               64  <117>                 0  ''
               66  POP_JUMP_IF_FALSE    86  'to 86'

 L.  87        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _backend
               72  LOAD_METHOD              create_hash_ctx
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                algorithm
               78  CALL_METHOD_1         1  ''
               80  LOAD_FAST                'self'
               82  STORE_ATTR               _ctx
               84  JUMP_FORWARD         92  'to 92'
             86_0  COME_FROM            66  '66'

 L.  89        86  LOAD_FAST                'ctx'
               88  LOAD_FAST                'self'
               90  STORE_ATTR               _ctx
             92_0  COME_FROM            84  '84'

Parse error at or near `<117>' instruction at offset 64

    algorithm = utils.read_only_property('_algorithm')

    def update--- This code section failed: ---

 L.  94         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  95        10  LOAD_GLOBAL              AlreadyFinalized
               12  LOAD_STR                 'Context was already finalized.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L.  96        18  LOAD_GLOBAL              utils
               20  LOAD_METHOD              _check_byteslike
               22  LOAD_STR                 'data'
               24  LOAD_FAST                'data'
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          

 L.  97        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _ctx
               34  LOAD_METHOD              update
               36  LOAD_FAST                'data'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def copy--- This code section failed: ---

 L. 100         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 101        10  LOAD_GLOBAL              AlreadyFinalized
               12  LOAD_STR                 'Context was already finalized.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 102        18  LOAD_GLOBAL              Hash

 L. 103        20  LOAD_FAST                'self'
               22  LOAD_ATTR                algorithm
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _backend
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _ctx
               32  LOAD_METHOD              copy
               34  CALL_METHOD_0         0  ''

 L. 102        36  LOAD_CONST               ('backend', 'ctx')
               38  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               40  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def finalize--- This code section failed: ---

 L. 107         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 108        10  LOAD_GLOBAL              AlreadyFinalized
               12  LOAD_STR                 'Context was already finalized.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 109        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _ctx
               22  LOAD_METHOD              finalize
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'digest'

 L. 110        28  LOAD_CONST               None
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _ctx

 L. 111        34  LOAD_FAST                'digest'
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


@utils.register_interface(HashAlgorithm)
class SHA1(object):
    name = 'sha1'
    digest_size = 20
    block_size = 64


@utils.register_interface(HashAlgorithm)
class SHA512_224(object):
    name = 'sha512-224'
    digest_size = 28
    block_size = 128


@utils.register_interface(HashAlgorithm)
class SHA512_256(object):
    name = 'sha512-256'
    digest_size = 32
    block_size = 128


@utils.register_interface(HashAlgorithm)
class SHA224(object):
    name = 'sha224'
    digest_size = 28
    block_size = 64


@utils.register_interface(HashAlgorithm)
class SHA256(object):
    name = 'sha256'
    digest_size = 32
    block_size = 64


@utils.register_interface(HashAlgorithm)
class SHA384(object):
    name = 'sha384'
    digest_size = 48
    block_size = 128


@utils.register_interface(HashAlgorithm)
class SHA512(object):
    name = 'sha512'
    digest_size = 64
    block_size = 128


@utils.register_interface(HashAlgorithm)
class SHA3_224(object):
    name = 'sha3-224'
    digest_size = 28


@utils.register_interface(HashAlgorithm)
class SHA3_256(object):
    name = 'sha3-256'
    digest_size = 32


@utils.register_interface(HashAlgorithm)
class SHA3_384(object):
    name = 'sha3-384'
    digest_size = 48


@utils.register_interface(HashAlgorithm)
class SHA3_512(object):
    name = 'sha3-512'
    digest_size = 64


@utils.register_interface(HashAlgorithm)
@utils.register_interface(ExtendableOutputFunction)
class SHAKE128(object):
    name = 'shake128'

    def __init__(self, digest_size):
        if not isinstancedigest_sizesix.integer_types:
            raise TypeError('digest_size must be an integer')
        if digest_size < 1:
            raise ValueError('digest_size must be a positive integer')
        self._digest_size = digest_size

    digest_size = utils.read_only_property('_digest_size')


@utils.register_interface(HashAlgorithm)
@utils.register_interface(ExtendableOutputFunction)
class SHAKE256(object):
    name = 'shake256'

    def __init__(self, digest_size):
        if not isinstancedigest_sizesix.integer_types:
            raise TypeError('digest_size must be an integer')
        if digest_size < 1:
            raise ValueError('digest_size must be a positive integer')
        self._digest_size = digest_size

    digest_size = utils.read_only_property('_digest_size')


@utils.register_interface(HashAlgorithm)
class MD5(object):
    name = 'md5'
    digest_size = 16
    block_size = 64


@utils.register_interface(HashAlgorithm)
class BLAKE2b(object):
    name = 'blake2b'
    _max_digest_size = 64
    _min_digest_size = 1
    block_size = 128

    def __init__(self, digest_size):
        if digest_size != 64:
            raise ValueError('Digest size must be 64')
        self._digest_size = digest_size

    digest_size = utils.read_only_property('_digest_size')


@utils.register_interface(HashAlgorithm)
class BLAKE2s(object):
    name = 'blake2s'
    block_size = 64
    _max_digest_size = 32
    _min_digest_size = 1

    def __init__(self, digest_size):
        if digest_size != 32:
            raise ValueError('Digest size must be 32')
        self._digest_size = digest_size

    digest_size = utils.read_only_property('_digest_size')