# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Hash\MD5.py
from Crypto.Util.py3compat import *
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, SmartPointer, create_string_buffer, get_raw_buffer, c_size_t, c_uint8_ptr
_raw_md5_lib = load_pycryptodome_raw_lib('Crypto.Hash._MD5', '\n                        #define MD5_DIGEST_SIZE 16\n\n                        int MD5_init(void **shaState);\n                        int MD5_destroy(void *shaState);\n                        int MD5_update(void *hs,\n                                          const uint8_t *buf,\n                                          size_t len);\n                        int MD5_digest(const void *shaState,\n                                          uint8_t digest[MD5_DIGEST_SIZE]);\n                        int MD5_copy(const void *src, void *dst);\n\n                        int MD5_pbkdf2_hmac_assist(const void *inner,\n                                            const void *outer,\n                                            const uint8_t first_digest[MD5_DIGEST_SIZE],\n                                            uint8_t final_digest[MD5_DIGEST_SIZE],\n                                            size_t iterations);\n                        ')

class MD5Hash(object):
    __doc__ = 'A MD5 hash object.\n    Do not instantiate directly.\n    Use the :func:`new` function.\n\n    :ivar oid: ASN.1 Object ID\n    :vartype oid: string\n\n    :ivar block_size: the size in bytes of the internal message block,\n                      input to the compression function\n    :vartype block_size: integer\n\n    :ivar digest_size: the size in bytes of the resulting hash\n    :vartype digest_size: integer\n    '
    digest_size = 16
    block_size = 64
    oid = '1.2.840.113549.2.5'

    def __init__(self, data=None):
        state = VoidPointer()
        result = _raw_md5_lib.MD5_init(state.address_of())
        if result:
            raise ValueError('Error %d while instantiating MD5' % result)
        self._state = SmartPointer(state.get(), _raw_md5_lib.MD5_destroy)
        if data:
            self.update(data)

    def update(self, data):
        """Continue hashing of a message by consuming the next chunk of data.

        Args:
            data (byte string/byte array/memoryview): The next chunk of the message being hashed.
        """
        result = _raw_md5_lib.MD5_update(self._state.get(), c_uint8_ptr(data), c_size_t(len(data)))
        if result:
            raise ValueError('Error %d while instantiating MD5' % result)

    def digest(self):
        """Return the **binary** (non-printable) digest of the message that has been hashed so far.

        :return: The hash digest, computed over the data processed so far.
                 Binary form.
        :rtype: byte string
        """
        bfr = create_string_buffer(self.digest_size)
        result = _raw_md5_lib.MD5_digest(self._state.get(), bfr)
        if result:
            raise ValueError('Error %d while instantiating MD5' % result)
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
        clone = MD5Hash()
        result = _raw_md5_lib.MD5_copy(self._state.get(), clone._state.get())
        if result:
            raise ValueError('Error %d while copying MD5' % result)
        return clone

    def new(self, data=None):
        """Create a fresh SHA-1 hash object."""
        return MD5Hash(data)


def new(data=None):
    """Create a new hash object.

    :parameter data:
        Optional. The very first chunk of the message to hash.
        It is equivalent to an early call to :meth:`MD5Hash.update`.
    :type data: byte string/byte array/memoryview

    :Return: A :class:`MD5Hash` hash object
    """
    return MD5Hash().new(data)


digest_size = 16
block_size = 64

def _pbkdf2_hmac_assist--- This code section failed: ---

 L. 170         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'first_digest'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              digest_size
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L. 171        16  LOAD_FAST                'iterations'
               18  LOAD_CONST               0
               20  COMPARE_OP               >
               22  POP_JUMP_IF_TRUE     28  'to 28'
               24  <74>             
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'

 L. 173        28  LOAD_GLOBAL              create_string_buffer
               30  LOAD_GLOBAL              digest_size
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'bfr'

 L. 174        36  LOAD_GLOBAL              _raw_md5_lib
               38  LOAD_METHOD              MD5_pbkdf2_hmac_assist

 L. 175        40  LOAD_FAST                'inner'
               42  LOAD_ATTR                _state
               44  LOAD_METHOD              get
               46  CALL_METHOD_0         0  ''

 L. 176        48  LOAD_FAST                'outer'
               50  LOAD_ATTR                _state
               52  LOAD_METHOD              get
               54  CALL_METHOD_0         0  ''

 L. 177        56  LOAD_FAST                'first_digest'

 L. 178        58  LOAD_FAST                'bfr'

 L. 179        60  LOAD_GLOBAL              c_size_t
               62  LOAD_FAST                'iterations'
               64  CALL_FUNCTION_1       1  ''

 L. 174        66  CALL_METHOD_5         5  ''
               68  STORE_FAST               'result'

 L. 181        70  LOAD_FAST                'result'
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L. 182        74  LOAD_GLOBAL              ValueError
               76  LOAD_STR                 'Error %d with PBKDF2-HMAC assis for MD5'
               78  LOAD_FAST                'result'
               80  BINARY_MODULO    
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            72  '72'

 L. 184        86  LOAD_GLOBAL              get_raw_buffer
               88  LOAD_FAST                'bfr'
               90  CALL_FUNCTION_1       1  ''
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1