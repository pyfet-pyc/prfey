# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Hash\BLAKE2s.py
from binascii import unhexlify
from Crypto.Util.py3compat import bord, tobytes
from Crypto.Random import get_random_bytes
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, SmartPointer, create_string_buffer, get_raw_buffer, c_size_t, c_uint8_ptr
_raw_blake2s_lib = load_pycryptodome_raw_lib('Crypto.Hash._BLAKE2s', '\n                        int blake2s_init(void **state,\n                                         const uint8_t *key,\n                                         size_t key_size,\n                                         size_t digest_size);\n                        int blake2s_destroy(void *state);\n                        int blake2s_update(void *state,\n                                           const uint8_t *buf,\n                                           size_t len);\n                        int blake2s_digest(const void *state,\n                                           uint8_t digest[32]);\n                        int blake2s_copy(const void *src, void *dst);\n                        ')

class BLAKE2s_Hash(object):
    __doc__ = 'A BLAKE2s hash object.\n    Do not instantiate directly. Use the :func:`new` function.\n\n    :ivar oid: ASN.1 Object ID\n    :vartype oid: string\n\n    :ivar block_size: the size in bytes of the internal message block,\n                      input to the compression function\n    :vartype block_size: integer\n\n    :ivar digest_size: the size in bytes of the resulting hash\n    :vartype digest_size: integer\n    '
    block_size = 32

    def __init__--- This code section failed: ---

 L.  79         0  LOAD_FAST                'digest_bytes'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               digest_size

 L.  81         6  LOAD_FAST                'update_after_digest'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _update_after_digest

 L.  82        12  LOAD_CONST               False
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _digest_done

 L.  85        18  LOAD_FAST                'digest_bytes'
               20  LOAD_CONST               (16, 20, 28, 32)
               22  <118>                 0  ''
               24  POP_JUMP_IF_FALSE    44  'to 44'
               26  LOAD_FAST                'key'
               28  POP_JUMP_IF_TRUE     44  'to 44'

 L.  86        30  LOAD_STR                 '1.3.6.1.4.1.1722.12.2.2.'
               32  LOAD_GLOBAL              str
               34  LOAD_FAST                'digest_bytes'
               36  CALL_FUNCTION_1       1  ''
               38  BINARY_ADD       
               40  LOAD_FAST                'self'
               42  STORE_ATTR               oid
             44_0  COME_FROM            28  '28'
             44_1  COME_FROM            24  '24'

 L.  88        44  LOAD_GLOBAL              VoidPointer
               46  CALL_FUNCTION_0       0  ''
               48  STORE_FAST               'state'

 L.  89        50  LOAD_GLOBAL              _raw_blake2s_lib
               52  LOAD_METHOD              blake2s_init
               54  LOAD_FAST                'state'
               56  LOAD_METHOD              address_of
               58  CALL_METHOD_0         0  ''

 L.  90        60  LOAD_GLOBAL              c_uint8_ptr
               62  LOAD_FAST                'key'
               64  CALL_FUNCTION_1       1  ''

 L.  91        66  LOAD_GLOBAL              c_size_t
               68  LOAD_GLOBAL              len
               70  LOAD_FAST                'key'
               72  CALL_FUNCTION_1       1  ''
               74  CALL_FUNCTION_1       1  ''

 L.  92        76  LOAD_GLOBAL              c_size_t
               78  LOAD_FAST                'digest_bytes'
               80  CALL_FUNCTION_1       1  ''

 L.  89        82  CALL_METHOD_4         4  ''
               84  STORE_FAST               'result'

 L.  94        86  LOAD_FAST                'result'
               88  POP_JUMP_IF_FALSE   102  'to 102'

 L.  95        90  LOAD_GLOBAL              ValueError
               92  LOAD_STR                 'Error %d while instantiating BLAKE2s'
               94  LOAD_FAST                'result'
               96  BINARY_MODULO    
               98  CALL_FUNCTION_1       1  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            88  '88'

 L.  96       102  LOAD_GLOBAL              SmartPointer
              104  LOAD_FAST                'state'
              106  LOAD_METHOD              get
              108  CALL_METHOD_0         0  ''

 L.  97       110  LOAD_GLOBAL              _raw_blake2s_lib
              112  LOAD_ATTR                blake2s_destroy

 L.  96       114  CALL_FUNCTION_2       2  ''
              116  LOAD_FAST                'self'
              118  STORE_ATTR               _state

 L.  98       120  LOAD_FAST                'data'
              122  POP_JUMP_IF_FALSE   134  'to 134'

 L.  99       124  LOAD_FAST                'self'
              126  LOAD_METHOD              update
              128  LOAD_FAST                'data'
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          
            134_0  COME_FROM           122  '122'

Parse error at or near `<118>' instruction at offset 22

    def update(self, data):
        """Continue hashing of a message by consuming the next chunk of data.

        Args:
            data (byte string/byte array/memoryview): The next chunk of the message being hashed.
        """
        if self._digest_done:
            if not self._update_after_digest:
                raise TypeError("You can only call 'digest' or 'hexdigest' on this object")
        result = _raw_blake2s_lib.blake2s_update(self._state.get, c_uint8_ptr(data), c_size_t(len(data)))
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
        result = _raw_blake2s_lib.blake2s_digest(self._state.get, bfr)
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
        return ''.join['%02x' % bord(x) for x in tuple(self.digest)]

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
        mac2 = new(digest_bits=160, key=secret, data=(self.digest))
        if mac1.digest != mac2.digest:
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
        self.verifyunhexlify(tobytes(hex_mac_tag))

    def new--- This code section failed: ---

 L. 191         0  LOAD_STR                 'digest_bytes'
                2  LOAD_FAST                'kwargs'
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    26  'to 26'
                8  LOAD_STR                 'digest_bits'
               10  LOAD_FAST                'kwargs'
               12  <118>                 1  ''
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 192        16  LOAD_FAST                'self'
               18  LOAD_ATTR                digest_size
               20  LOAD_FAST                'kwargs'
               22  LOAD_STR                 'digest_bytes'
               24  STORE_SUBSCR     
             26_0  COME_FROM            14  '14'
             26_1  COME_FROM             6  '6'

 L. 194        26  LOAD_GLOBAL              new
               28  BUILD_TUPLE_0         0 
               30  BUILD_MAP_0           0 
               32  LOAD_FAST                'kwargs'
               34  <164>                 1  ''
               36  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


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
               56  <118>                 1  ''
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
               88  <117>                 1  ''
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

Parse error at or near `<118>' instruction at offset 56