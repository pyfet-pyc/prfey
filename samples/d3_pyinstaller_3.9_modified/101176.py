# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Hash\SHA1.py
from Crypto.Util.py3compat import *
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, SmartPointer, create_string_buffer, get_raw_buffer, c_size_t, c_uint8_ptr
_raw_sha1_lib = load_pycryptodome_raw_lib('Crypto.Hash._SHA1', '\n                        #define SHA1_DIGEST_SIZE 20\n\n                        int SHA1_init(void **shaState);\n                        int SHA1_destroy(void *shaState);\n                        int SHA1_update(void *hs,\n                                          const uint8_t *buf,\n                                          size_t len);\n                        int SHA1_digest(const void *shaState,\n                                          uint8_t digest[SHA1_DIGEST_SIZE]);\n                        int SHA1_copy(const void *src, void *dst);\n\n                        int SHA1_pbkdf2_hmac_assist(const void *inner,\n                                            const void *outer,\n                                            const uint8_t first_digest[SHA1_DIGEST_SIZE],\n                                            uint8_t final_digest[SHA1_DIGEST_SIZE],\n                                            size_t iterations);\n                        ')

class SHA1Hash(object):
    __doc__ = 'A SHA-1 hash object.\n    Do not instantiate directly.\n    Use the :func:`new` function.\n\n    :ivar oid: ASN.1 Object ID\n    :vartype oid: string\n\n    :ivar block_size: the size in bytes of the internal message block,\n                      input to the compression function\n    :vartype block_size: integer\n\n    :ivar digest_size: the size in bytes of the resulting hash\n    :vartype digest_size: integer\n    '
    digest_size = 20
    block_size = 64
    oid = '1.3.14.3.2.26'

    def __init__(self, data=None):
        state = VoidPointer()
        result = _raw_sha1_lib.SHA1_init(state.address_of())
        if result:
            raise ValueError('Error %d while instantiating SHA1' % result)
        self._state = SmartPointer(state.get(), _raw_sha1_lib.SHA1_destroy)
        if data:
            self.update(data)

    def update(self, data):
        """Continue hashing of a message by consuming the next chunk of data.

        Args:
            data (byte string/byte array/memoryview): The next chunk of the message being hashed.
        """
        result = _raw_sha1_lib.SHA1_update(self._state.get(), c_uint8_ptr(data), c_size_t(len(data)))
        if result:
            raise ValueError('Error %d while instantiating SHA1' % result)

    def digest(self):
        """Return the **binary** (non-printable) digest of the message that has been hashed so far.

        :return: The hash digest, computed over the data processed so far.
                 Binary form.
        :rtype: byte string
        """
        bfr = create_string_buffer(self.digest_size)
        result = _raw_sha1_lib.SHA1_digest(self._state.get(), bfr)
        if result:
            raise ValueError('Error %d while instantiating SHA1' % result)
        return get_raw_buffer(bfr)

    def hexdigest(self):
        """Return the **printable** digest of the message that has been hashed so far.

        :return: The hash digest, computed over the data processed so far.
                 Hexadecimal encoded.
        :rtype: string
        """
        return ''.join(['%02x' % bord(x) for x in self.digest()])

    def copy(self):
        """Return a copy ("clone") of the hash object.

        The copy will have the same internal state as the original hash
        object.
        This can be used to efficiently compute the digests of strings that
        share a common initial substring.

        :return: A hash object of the same type
        """
        clone = SHA1Hash()
        result = _raw_sha1_lib.SHA1_copy(self._state.get(), clone._state.get())
        if result:
            raise ValueError('Error %d while copying SHA1' % result)
        return clone

    def new(self, data=None):
        """Create a fresh SHA-1 hash object."""
        return SHA1Hash(data)


def new(data=None):
    """Create a new hash object.

    :parameter data:
        Optional. The very first chunk of the message to hash.
        It is equivalent to an early call to :meth:`SHA1Hash.update`.
    :type data: byte string/byte array/memoryview

    :Return: A :class:`SHA1Hash` hash object
    """
    return SHA1Hash().new(data)


digest_size = SHA1Hash.digest_size
block_size = SHA1Hash.block_size

def _pbkdf2_hmac_assist--- This code section failed: ---

 L. 171         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'first_digest'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              digest_size
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L. 172        16  LOAD_FAST                'iterations'
               18  LOAD_CONST               0
               20  COMPARE_OP               >
               22  POP_JUMP_IF_TRUE     28  'to 28'
               24  <74>             
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'

 L. 174        28  LOAD_GLOBAL              create_string_buffer
               30  LOAD_GLOBAL              digest_size
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'bfr'

 L. 175        36  LOAD_GLOBAL              _raw_sha1_lib
               38  LOAD_METHOD              SHA1_pbkdf2_hmac_assist

 L. 176        40  LOAD_FAST                'inner'
               42  LOAD_ATTR                _state
               44  LOAD_METHOD              get
               46  CALL_METHOD_0         0  ''

 L. 177        48  LOAD_FAST                'outer'
               50  LOAD_ATTR                _state
               52  LOAD_METHOD              get
               54  CALL_METHOD_0         0  ''

 L. 178        56  LOAD_FAST                'first_digest'

 L. 179        58  LOAD_FAST                'bfr'

 L. 180        60  LOAD_GLOBAL              c_size_t
               62  LOAD_FAST                'iterations'
               64  CALL_FUNCTION_1       1  ''

 L. 175        66  CALL_METHOD_5         5  ''
               68  STORE_FAST               'result'

 L. 182        70  LOAD_FAST                'result'
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L. 183        74  LOAD_GLOBAL              ValueError
               76  LOAD_STR                 'Error %d with PBKDF2-HMAC assis for SHA1'
               78  LOAD_FAST                'result'
               80  BINARY_MODULO    
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            72  '72'

 L. 185        86  LOAD_GLOBAL              get_raw_buffer
               88  LOAD_FAST                'bfr'
               90  CALL_FUNCTION_1       1  ''
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1