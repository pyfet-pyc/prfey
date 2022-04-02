# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\ciphers\base.py
from __future__ import absolute_import, division, print_function
import abc, six
from cryptography import utils
from cryptography.exceptions import AlreadyFinalized, AlreadyUpdated, NotYetFinalized, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.backends.interfaces import CipherBackend
from cryptography.hazmat.primitives.ciphers import modes

@six.add_metaclass(abc.ABCMeta)
class CipherAlgorithm(object):

    @abc.abstractproperty
    def name(self):
        """
        A string naming this mode (e.g. "AES", "Camellia").
        """
        pass

    @abc.abstractproperty
    def key_size(self):
        """
        The size of the key being used as an integer in bits (e.g. 128, 256).
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class BlockCipherAlgorithm(object):

    @abc.abstractproperty
    def block_size(self):
        """
        The size of a block as an integer in bits (e.g. 64, 128).
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class CipherContext(object):

    @abc.abstractmethod
    def update(self, data):
        """
        Processes the provided bytes through the cipher and returns the results
        as bytes.
        """
        pass

    @abc.abstractmethod
    def update_into(self, data, buf):
        """
        Processes the provided bytes and writes the resulting data into the
        provided buffer. Returns the number of bytes written.
        """
        pass

    @abc.abstractmethod
    def finalize(self):
        """
        Returns the results of processing the final block as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class AEADCipherContext(object):

    @abc.abstractmethod
    def authenticate_additional_data(self, data):
        """
        Authenticates the provided bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class AEADDecryptionContext(object):

    @abc.abstractmethod
    def finalize_with_tag(self, tag):
        """
        Returns the results of processing the final block as bytes and allows
        delayed passing of the authentication tag.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class AEADEncryptionContext(object):

    @abc.abstractproperty
    def tag(self):
        """
        Returns tag bytes. This is only available after encryption is
        finalized.
        """
        pass


class Cipher(object):

    def __init__--- This code section failed: ---

 L. 102         0  LOAD_GLOBAL              _get_backend
                2  LOAD_FAST                'backend'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'backend'

 L. 103         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'backend'
               12  LOAD_GLOBAL              CipherBackend
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     30  'to 30'

 L. 104        18  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 105        20  LOAD_STR                 'Backend object does not implement CipherBackend.'

 L. 106        22  LOAD_GLOBAL              _Reasons
               24  LOAD_ATTR                BACKEND_MISSING_INTERFACE

 L. 104        26  CALL_FUNCTION_2       2  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            16  '16'

 L. 109        30  LOAD_GLOBAL              isinstance
               32  LOAD_FAST                'algorithm'
               34  LOAD_GLOBAL              CipherAlgorithm
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_TRUE     48  'to 48'

 L. 110        40  LOAD_GLOBAL              TypeError
               42  LOAD_STR                 'Expected interface of CipherAlgorithm.'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L. 112        48  LOAD_FAST                'mode'
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_FALSE    66  'to 66'

 L. 113        56  LOAD_FAST                'mode'
               58  LOAD_METHOD              validate_for_algorithm
               60  LOAD_FAST                'algorithm'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
             66_0  COME_FROM            54  '54'

 L. 115        66  LOAD_FAST                'algorithm'
               68  LOAD_FAST                'self'
               70  STORE_ATTR               algorithm

 L. 116        72  LOAD_FAST                'mode'
               74  LOAD_FAST                'self'
               76  STORE_ATTR               mode

 L. 117        78  LOAD_FAST                'backend'
               80  LOAD_FAST                'self'
               82  STORE_ATTR               _backend

Parse error at or near `<117>' instruction at offset 52

    def encryptor--- This code section failed: ---

 L. 120         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                mode
                6  LOAD_GLOBAL              modes
                8  LOAD_ATTR                ModeWithAuthenticationTag
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    34  'to 34'

 L. 121        14  LOAD_FAST                'self'
               16  LOAD_ATTR                mode
               18  LOAD_ATTR                tag
               20  LOAD_CONST               None
               22  <117>                 1  ''
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L. 122        26  LOAD_GLOBAL              ValueError

 L. 123        28  LOAD_STR                 'Authentication tag must be None when encrypting.'

 L. 122        30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'
             34_1  COME_FROM            12  '12'

 L. 125        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _backend
               38  LOAD_METHOD              create_symmetric_encryption_ctx

 L. 126        40  LOAD_FAST                'self'
               42  LOAD_ATTR                algorithm
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                mode

 L. 125        48  CALL_METHOD_2         2  ''
               50  STORE_FAST               'ctx'

 L. 128        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _wrap_ctx
               56  LOAD_FAST                'ctx'
               58  LOAD_CONST               True
               60  LOAD_CONST               ('encrypt',)
               62  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 22

    def decryptor(self):
        ctx = self._backend.create_symmetric_decryption_ctxself.algorithmself.mode
        return self._wrap_ctx(ctx, encrypt=False)

    def _wrap_ctx(self, ctx, encrypt):
        if isinstanceself.modemodes.ModeWithAuthenticationTag:
            if encrypt:
                return _AEADEncryptionContext(ctx)
            return _AEADCipherContext(ctx)
        else:
            return _CipherContext(ctx)


@utils.register_interface(CipherContext)
class _CipherContext(object):

    def __init__(self, ctx):
        self._ctx = ctx

    def update--- This code section failed: ---

 L. 152         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 153        10  LOAD_GLOBAL              AlreadyFinalized
               12  LOAD_STR                 'Context was already finalized.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 154        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _ctx
               22  LOAD_METHOD              update
               24  LOAD_FAST                'data'
               26  CALL_METHOD_1         1  ''
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def update_into--- This code section failed: ---

 L. 157         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 158        10  LOAD_GLOBAL              AlreadyFinalized
               12  LOAD_STR                 'Context was already finalized.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 159        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _ctx
               22  LOAD_METHOD              update_into
               24  LOAD_FAST                'data'
               26  LOAD_FAST                'buf'
               28  CALL_METHOD_2         2  ''
               30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def finalize--- This code section failed: ---

 L. 162         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 163        10  LOAD_GLOBAL              AlreadyFinalized
               12  LOAD_STR                 'Context was already finalized.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 164        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _ctx
               22  LOAD_METHOD              finalize
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'data'

 L. 165        28  LOAD_CONST               None
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _ctx

 L. 166        34  LOAD_FAST                'data'
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


@utils.register_interface(AEADCipherContext)
@utils.register_interface(CipherContext)
@utils.register_interface(AEADDecryptionContext)
class _AEADCipherContext(object):

    def __init__(self, ctx):
        self._ctx = ctx
        self._bytes_processed = 0
        self._aad_bytes_processed = 0
        self._tag = None
        self._updated = False

    def _check_limit--- This code section failed: ---

 L. 181         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 182        10  LOAD_GLOBAL              AlreadyFinalized
               12  LOAD_STR                 'Context was already finalized.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 183        18  LOAD_CONST               True
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _updated

 L. 184        24  LOAD_FAST                'self'
               26  DUP_TOP          
               28  LOAD_ATTR                _bytes_processed
               30  LOAD_FAST                'data_size'
               32  INPLACE_ADD      
               34  ROT_TWO          
               36  STORE_ATTR               _bytes_processed

 L. 185        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _bytes_processed
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _ctx
               46  LOAD_ATTR                _mode
               48  LOAD_ATTR                _MAX_ENCRYPTED_BYTES
               50  COMPARE_OP               >
               52  POP_JUMP_IF_FALSE    82  'to 82'

 L. 186        54  LOAD_GLOBAL              ValueError

 L. 187        56  LOAD_STR                 '{} has a maximum encrypted byte limit of {}'
               58  LOAD_METHOD              format

 L. 188        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _ctx
               64  LOAD_ATTR                _mode
               66  LOAD_ATTR                name
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _ctx
               72  LOAD_ATTR                _mode
               74  LOAD_ATTR                _MAX_ENCRYPTED_BYTES

 L. 187        76  CALL_METHOD_2         2  ''

 L. 186        78  CALL_FUNCTION_1       1  ''
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            52  '52'

Parse error at or near `None' instruction at offset -1

    def update(self, data):
        self._check_limit(len(data))
        return self._ctx.update(data)

    def update_into(self, data, buf):
        self._check_limit(len(data))
        return self._ctx.update_intodatabuf

    def finalize--- This code section failed: ---

 L. 201         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 202        10  LOAD_GLOBAL              AlreadyFinalized
               12  LOAD_STR                 'Context was already finalized.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 203        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _ctx
               22  LOAD_METHOD              finalize
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'data'

 L. 204        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _ctx
               32  LOAD_ATTR                tag
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _tag

 L. 205        38  LOAD_CONST               None
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _ctx

 L. 206        44  LOAD_FAST                'data'
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def finalize_with_tag--- This code section failed: ---

 L. 209         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 210        10  LOAD_GLOBAL              AlreadyFinalized
               12  LOAD_STR                 'Context was already finalized.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 211        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _ctx
               22  LOAD_METHOD              finalize_with_tag
               24  LOAD_FAST                'tag'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'data'

 L. 212        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _ctx
               34  LOAD_ATTR                tag
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _tag

 L. 213        40  LOAD_CONST               None
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _ctx

 L. 214        46  LOAD_FAST                'data'
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def authenticate_additional_data--- This code section failed: ---

 L. 217         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 218        10  LOAD_GLOBAL              AlreadyFinalized
               12  LOAD_STR                 'Context was already finalized.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 219        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _updated
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 220        24  LOAD_GLOBAL              AlreadyUpdated
               26  LOAD_STR                 'Update has been called on this context.'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'

 L. 222        32  LOAD_FAST                'self'
               34  DUP_TOP          
               36  LOAD_ATTR                _aad_bytes_processed
               38  LOAD_GLOBAL              len
               40  LOAD_FAST                'data'
               42  CALL_FUNCTION_1       1  ''
               44  INPLACE_ADD      
               46  ROT_TWO          
               48  STORE_ATTR               _aad_bytes_processed

 L. 223        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _aad_bytes_processed
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _ctx
               58  LOAD_ATTR                _mode
               60  LOAD_ATTR                _MAX_AAD_BYTES
               62  COMPARE_OP               >
               64  POP_JUMP_IF_FALSE    94  'to 94'

 L. 224        66  LOAD_GLOBAL              ValueError

 L. 225        68  LOAD_STR                 '{} has a maximum AAD byte limit of {}'
               70  LOAD_METHOD              format

 L. 226        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _ctx
               76  LOAD_ATTR                _mode
               78  LOAD_ATTR                name
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _ctx
               84  LOAD_ATTR                _mode
               86  LOAD_ATTR                _MAX_AAD_BYTES

 L. 225        88  CALL_METHOD_2         2  ''

 L. 224        90  CALL_FUNCTION_1       1  ''
               92  RAISE_VARARGS_1       1  'exception instance'
             94_0  COME_FROM            64  '64'

 L. 230        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _ctx
               98  LOAD_METHOD              authenticate_additional_data
              100  LOAD_FAST                'data'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

Parse error at or near `None' instruction at offset -1


@utils.register_interface(AEADEncryptionContext)
class _AEADEncryptionContext(_AEADCipherContext):

    @property
    def tag--- This code section failed: ---

 L. 237         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 238        10  LOAD_GLOBAL              NotYetFinalized

 L. 239        12  LOAD_STR                 'You must finalize encryption before getting the tag.'

 L. 238        14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 241        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _tag
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1