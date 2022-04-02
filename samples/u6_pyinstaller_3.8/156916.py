# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\Crypto\Hash\BLAKE2s.py
from binascii import unhexlify
from Crypto.Util.py3compat import bord, tobytes
from Crypto.Random import get_random_bytes
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, SmartPointer, create_string_buffer, get_raw_buffer, c_size_t, c_uint8_ptr
_raw_blake2s_lib = load_pycryptodome_raw_lib('Crypto.Hash._BLAKE2s', '\n                        int blake2s_init(void **state,\n                                         const uint8_t *key,\n                                         size_t key_size,\n                                         size_t digest_size);\n                        int blake2s_destroy(void *state);\n                        int blake2s_update(void *state,\n                                           const uint8_t *buf,\n                                           size_t len);\n                        int blake2s_digest(const void *state,\n                                           uint8_t digest[32]);\n                        int blake2s_copy(const void *src, void *dst);\n                        ')

class BLAKE2s_Hash(object):
    __doc__ = 'A BLAKE2s hash object.\n    Do not instantiate directly. Use the :func:`new` function.\n\n    :ivar oid: ASN.1 Object ID\n    :vartype oid: string\n\n    :ivar block_size: the size in bytes of the internal message block,\n                      input to the compression function\n    :vartype block_size: integer\n\n    :ivar digest_size: the size in bytes of the resulting hash\n    :vartype digest_size: integer\n    '
    block_size = 32

    def __init__(self, data, key, digest_bytes, update_after_digest):
        self.digest_size = digest_bytes
        self._update_after_digest = update_after_digest
        self._digest_done = False
        if digest_bytes in (16, 20, 28, 32):
            if not key:
                self.oid = '1.3.6.1.4.1.1722.12.2.2.' + str(digest_bytes)
        state = VoidPointer()
        result = _raw_blake2s_lib.blake2s_init(state.address_of(), c_uint8_ptr(key), c_size_t(len(key)), c_size_t(digest_bytes))
        if result:
            raise ValueError('Error %d while instantiating BLAKE2s' % result)
        self._state = SmartPointer(state.get(), _raw_blake2s_lib.blake2s_destroy)
        if data:
            self.update(data)

    def update(self, data):
        """Continue hashing of a message by consuming the next chunk of data.

        Args:
            data (byte string/byte array/memoryview): The next chunk of the message being hashed.
        """
        if self._digest_done:
            if not self._update_after_digest:
                raise TypeError("You can only call 'digest' or 'hexdigest' on this object")
        result = _raw_blake2s_lib.blake2s_update(self._state.get(), c_uint8_ptr(data), c_size_t(len(data)))
        if result:
            raise ValueError('Error %d while hashing BLAKE2s data' % result)
        return self

    def digest(self):
        """Return the **binary** (non-printable) digest of the message that has been hashed so far.

        :return: The hash digest, computed over the data processed so far.
                 Binary form.
        :rtype: byte string
        """
        bfr = create_string_buffer(32)
        result = _raw_blake2s_lib.blake2s_digest(self._state.get(), bfr)
        if result:
            raise ValueError('Error %d while creating BLAKE2s digest' % result)
        self._digest_done = True
        return get_raw_buffer(bfr)[:self.digest_size]

    def hexdigest(self):
        """Return the **printable** digest of the message that has been hashed so far.

        :return: The hash digest, computed over the data processed so far.
                 Hexadecimal encoded.
        :rtype: string
        """
        return ''.join(['%02x' % bord(x) for x in tuple(self.digest())])

    def verify(self, mac_tag):
        """Verify that a given **binary** MAC (computed by another party)
        is valid.

        Args:
          mac_tag (byte string/byte array/memoryview): the expected MAC of the message.

        Raises:
            ValueError: if the MAC does not match. It means that the message
                has been tampered with or that the MAC key is incorrect.
        """
        secret = get_random_bytes(16)
        mac1 = new(digest_bits=160, key=secret, data=mac_tag)
        mac2 = new(digest_bits=160, key=secret, data=(self.digest()))
        if mac1.digest() != mac2.digest():
            raise ValueError('MAC check failed')

    def hexverify(self, hex_mac_tag):
        """Verify that a given **printable** MAC (computed by another party)
        is valid.

        Args:
            hex_mac_tag (string): the expected MAC of the message, as a hexadecimal string.

        Raises:
            ValueError: if the MAC does not match. It means that the message
                has been tampered with or that the MAC key is incorrect.
        """
        self.verify(unhexlify(tobytes(hex_mac_tag)))

    def new(self, **kwargs):
        """Return a new instance of a BLAKE2s hash object.
        See :func:`new`.
        """
        if 'digest_bytes' not in kwargs:
            if 'digest_bits' not in kwargs:
                kwargs['digest_bytes'] = self.digest_size
        return new(**kwargs)


def new--- This code section failed: ---

 L. 222         0  LOAD_FAST                'kwargs'
                2  LOAD_METHOD              pop
                4  LOAD_STR                 'data'
                6  LOAD_CONST               None
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'data'

 L. 223        12  LOAD_FAST                'kwargs'
               14  LOAD_METHOD              pop
               16  LOAD_STR                 'update_after_digest'
               18  LOAD_CONST               False
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'update_after_digest'

 L. 225        24  LOAD_FAST                'kwargs'
               26  LOAD_METHOD              pop
               28  LOAD_STR                 'digest_bytes'
               30  LOAD_CONST               None
               32  CALL_METHOD_2         2  ''
               34  STORE_FAST               'digest_bytes'

 L. 226        36  LOAD_FAST                'kwargs'
               38  LOAD_METHOD              pop
               40  LOAD_STR                 'digest_bits'
               42  LOAD_CONST               None
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'digest_bits'

 L. 227        48  LOAD_CONST               None
               50  LOAD_FAST                'digest_bytes'
               52  LOAD_FAST                'digest_bits'
               54  BUILD_TUPLE_2         2 
               56  COMPARE_OP               not-in
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L. 228        60  LOAD_GLOBAL              TypeError
               62  LOAD_STR                 'Only one digest parameter must be provided'
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 229        68  LOAD_CONST               (None, None)
               70  LOAD_FAST                'digest_bytes'
               72  LOAD_FAST                'digest_bits'
               74  BUILD_TUPLE_2         2 
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE    84  'to 84'

 L. 230        80  LOAD_CONST               32
               82  STORE_FAST               'digest_bytes'
             84_0  COME_FROM            78  '78'

 L. 231        84  LOAD_FAST                'digest_bytes'
               86  LOAD_CONST               None
               88  COMPARE_OP               is-not
               90  POP_JUMP_IF_FALSE   124  'to 124'

 L. 232        92  LOAD_CONST               1
               94  LOAD_FAST                'digest_bytes'
               96  DUP_TOP          
               98  ROT_THREE        
              100  COMPARE_OP               <=
              102  POP_JUMP_IF_FALSE   112  'to 112'
              104  LOAD_CONST               32
              106  COMPARE_OP               <=
              108  POP_JUMP_IF_TRUE    172  'to 172'
              110  JUMP_FORWARD        114  'to 114'
            112_0  COME_FROM           102  '102'
              112  POP_TOP          
            114_0  COME_FROM           110  '110'

 L. 233       114  LOAD_GLOBAL              ValueError
              116  LOAD_STR                 "'digest_bytes' not in range 1..32"
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
              122  JUMP_FORWARD        172  'to 172'
            124_0  COME_FROM            90  '90'

 L. 235       124  LOAD_CONST               8
              126  LOAD_FAST                'digest_bits'
              128  DUP_TOP          
              130  ROT_THREE        
              132  COMPARE_OP               <=
              134  POP_JUMP_IF_FALSE   144  'to 144'
              136  LOAD_CONST               256
              138  COMPARE_OP               <=
              140  POP_JUMP_IF_FALSE   156  'to 156'
              142  JUMP_FORWARD        148  'to 148'
            144_0  COME_FROM           134  '134'
              144  POP_TOP          
              146  JUMP_FORWARD        156  'to 156'
            148_0  COME_FROM           142  '142'
              148  LOAD_FAST                'digest_bits'
              150  LOAD_CONST               8
              152  BINARY_MODULO    
              154  POP_JUMP_IF_FALSE   164  'to 164'
            156_0  COME_FROM           146  '146'
            156_1  COME_FROM           140  '140'

 L. 236       156  LOAD_GLOBAL              ValueError
              158  LOAD_STR                 "'digest_bytes' not in range 8..256, with steps of 8"
              160  CALL_FUNCTION_1       1  ''
              162  RAISE_VARARGS_1       1  'exception instance'
            164_0  COME_FROM           154  '154'

 L. 238       164  LOAD_FAST                'digest_bits'
              166  LOAD_CONST               8
              168  BINARY_FLOOR_DIVIDE
              170  STORE_FAST               'digest_bytes'
            172_0  COME_FROM           122  '122'
            172_1  COME_FROM           108  '108'

 L. 240       172  LOAD_FAST                'kwargs'
              174  LOAD_METHOD              pop
              176  LOAD_STR                 'key'
              178  LOAD_CONST               b''
              180  CALL_METHOD_2         2  ''
              182  STORE_FAST               'key'

 L. 241       184  LOAD_GLOBAL              len
              186  LOAD_FAST                'key'
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_CONST               32
              192  COMPARE_OP               >
              194  POP_JUMP_IF_FALSE   204  'to 204'

 L. 242       196  LOAD_GLOBAL              ValueError
              198  LOAD_STR                 'BLAKE2s key cannot exceed 32 bytes'
              200  CALL_FUNCTION_1       1  ''
              202  RAISE_VARARGS_1       1  'exception instance'
            204_0  COME_FROM           194  '194'

 L. 244       204  LOAD_FAST                'kwargs'
              206  POP_JUMP_IF_FALSE   224  'to 224'

 L. 245       208  LOAD_GLOBAL              TypeError
              210  LOAD_STR                 'Unknown parameters: '
              212  LOAD_GLOBAL              str
              214  LOAD_FAST                'kwargs'
              216  CALL_FUNCTION_1       1  ''
              218  BINARY_ADD       
              220  CALL_FUNCTION_1       1  ''
              222  RAISE_VARARGS_1       1  'exception instance'
            224_0  COME_FROM           206  '206'

 L. 247       224  LOAD_GLOBAL              BLAKE2s_Hash
              226  LOAD_FAST                'data'
              228  LOAD_FAST                'key'
              230  LOAD_FAST                'digest_bytes'
              232  LOAD_FAST                'update_after_digest'
              234  CALL_FUNCTION_4       4  ''
              236  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 236