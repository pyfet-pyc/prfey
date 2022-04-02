# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Hash\SHA256.py
from Crypto.Util.py3compat import bord
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, SmartPointer, create_string_buffer, get_raw_buffer, c_size_t, c_uint8_ptr
_raw_sha256_lib = load_pycryptodome_raw_lib('Crypto.Hash._SHA256', '\n                        int SHA256_init(void **shaState);\n                        int SHA256_destroy(void *shaState);\n                        int SHA256_update(void *hs,\n                                          const uint8_t *buf,\n                                          size_t len);\n                        int SHA256_digest(const void *shaState,\n                                          uint8_t *digest,\n                                          size_t digest_size);\n                        int SHA256_copy(const void *src, void *dst);\n\n                        int SHA256_pbkdf2_hmac_assist(const void *inner,\n                                            const void *outer,\n                                            const uint8_t *first_digest,\n                                            uint8_t *final_digest,\n                                            size_t iterations,\n                                            size_t digest_size);\n                        ')

class SHA256Hash(object):
    __doc__ = 'A SHA-256 hash object.\n    Do not instantiate directly. Use the :func:`new` function.\n\n    :ivar oid: ASN.1 Object ID\n    :vartype oid: string\n\n    :ivar block_size: the size in bytes of the internal message block,\n                      input to the compression function\n    :vartype block_size: integer\n\n    :ivar digest_size: the size in bytes of the resulting hash\n    :vartype digest_size: integer\n    '
    digest_size = 32
    block_size = 64
    oid = '2.16.840.1.101.3.4.2.1'

    def __init__(self, data=None):
        state = VoidPointer()
        result = _raw_sha256_lib.SHA256_init(state.address_of())
        if result:
            raise ValueError('Error %d while instantiating SHA256' % result)
        self._state = SmartPointer(state.get(), _raw_sha256_lib.SHA256_destroy)
        if data:
            self.update(data)

    def update(self, data):
        """Continue hashing of a message by consuming the next chunk of data.

        Args:
            data (byte string/byte array/memoryview): The next chunk of the message being hashed.
        """
        result = _raw_sha256_lib.SHA256_update(self._state.get(), c_uint8_ptr(data), c_size_t(len(data)))
        if result:
            raise ValueError('Error %d while hashing data with SHA256' % result)

    def digest(self):
        """Return the **binary** (non-printable) digest of the message that has been hashed so far.

        :return: The hash digest, computed over the data processed so far.
                 Binary form.
        :rtype: byte string
        """
        bfr = create_string_buffer(self.digest_size)
        result = _raw_sha256_lib.SHA256_digest(self._state.get(), bfr, c_size_t(self.digest_size))
        if result:
            raise ValueError('Error %d while making SHA256 digest' % result)
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
        clone = SHA256Hash()
        result = _raw_sha256_lib.SHA256_copy(self._state.get(), clone._state.get())
        if result:
            raise ValueError('Error %d while copying SHA256' % result)
        return clone

    def new(self, data=None):
        """Create a fresh SHA-256 hash object."""
        return SHA256Hash(data)


def new(data=None):
    """Create a new hash object.

    :parameter data:
        Optional. The very first chunk of the message to hash.
        It is equivalent to an early call to :meth:`SHA256Hash.update`.
    :type data: byte string/byte array/memoryview

    :Return: A :class:`SHA256Hash` hash object
    """
    return SHA256Hash().new(data)


digest_size = SHA256Hash.digest_size
block_size = SHA256Hash.block_size

def _pbkdf2_hmac_assist--- This code section failed: ---

 L. 171         0  LOAD_FAST                'iterations'
                2  LOAD_CONST               0
                4  COMPARE_OP               >
                6  POP_JUMP_IF_TRUE     12  'to 12'
                8  <74>             
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             6  '6'

 L. 173        12  LOAD_GLOBAL              create_string_buffer
               14  LOAD_GLOBAL              len
               16  LOAD_FAST                'first_digest'
               18  CALL_FUNCTION_1       1  ''
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'bfr'

 L. 174        24  LOAD_GLOBAL              _raw_sha256_lib
               26  LOAD_METHOD              SHA256_pbkdf2_hmac_assist

 L. 175        28  LOAD_FAST                'inner'
               30  LOAD_ATTR                _state
               32  LOAD_METHOD              get
               34  CALL_METHOD_0         0  ''

 L. 176        36  LOAD_FAST                'outer'
               38  LOAD_ATTR                _state
               40  LOAD_METHOD              get
               42  CALL_METHOD_0         0  ''

 L. 177        44  LOAD_FAST                'first_digest'

 L. 178        46  LOAD_FAST                'bfr'

 L. 179        48  LOAD_GLOBAL              c_size_t
               50  LOAD_FAST                'iterations'
               52  CALL_FUNCTION_1       1  ''

 L. 180        54  LOAD_GLOBAL              c_size_t
               56  LOAD_GLOBAL              len
               58  LOAD_FAST                'first_digest'
               60  CALL_FUNCTION_1       1  ''
               62  CALL_FUNCTION_1       1  ''

 L. 174        64  CALL_METHOD_6         6  ''
               66  STORE_FAST               'result'

 L. 182        68  LOAD_FAST                'result'
               70  POP_JUMP_IF_FALSE    84  'to 84'

 L. 183        72  LOAD_GLOBAL              ValueError
               74  LOAD_STR                 'Error %d with PBKDF2-HMAC assist for SHA256'
               76  LOAD_FAST                'result'
               78  BINARY_MODULO    
               80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            70  '70'

 L. 185        84  LOAD_GLOBAL              get_raw_buffer
               86  LOAD_FAST                'bfr'
               88  CALL_FUNCTION_1       1  ''
               90  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1