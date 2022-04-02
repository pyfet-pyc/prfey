# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Hash\HMAC.py
from Crypto.Util.py3compat import bord, tobytes, _memoryview
from binascii import unhexlify
from Crypto.Hash import MD5
from Crypto.Hash import BLAKE2s
import Crypto.Util.strxor as strxor
from Crypto.Random import get_random_bytes
__all__ = [
 'new', 'HMAC']

class HMAC(object):
    __doc__ = 'An HMAC hash object.\n    Do not instantiate directly. Use the :func:`new` function.\n\n    :ivar digest_size: the size in bytes of the resulting MAC tag\n    :vartype digest_size: integer\n    '

    def __init__--- This code section failed: ---

 L.  56         0  LOAD_FAST                'digestmod'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  57         8  LOAD_GLOBAL              MD5
               10  STORE_FAST               'digestmod'
             12_0  COME_FROM             6  '6'

 L.  59        12  LOAD_FAST                'msg'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L.  60        20  LOAD_CONST               b''
               22  STORE_FAST               'msg'
             24_0  COME_FROM            18  '18'

 L.  63        24  LOAD_FAST                'digestmod'
               26  LOAD_ATTR                digest_size
               28  LOAD_FAST                'self'
               30  STORE_ATTR               digest_size

 L.  65        32  LOAD_FAST                'digestmod'
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _digestmod

 L.  67        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'key'
               42  LOAD_GLOBAL              _memoryview
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L.  68        48  LOAD_FAST                'key'
               50  LOAD_METHOD              tobytes
               52  CALL_METHOD_0         0  ''
               54  STORE_FAST               'key'
             56_0  COME_FROM            46  '46'

 L.  70        56  SETUP_FINALLY       136  'to 136'

 L.  71        58  LOAD_GLOBAL              len
               60  LOAD_FAST                'key'
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_FAST                'digestmod'
               66  LOAD_ATTR                block_size
               68  COMPARE_OP               <=
               70  POP_JUMP_IF_FALSE    96  'to 96'

 L.  73        72  LOAD_FAST                'key'
               74  LOAD_CONST               b'\x00'
               76  LOAD_FAST                'digestmod'
               78  LOAD_ATTR                block_size
               80  LOAD_GLOBAL              len
               82  LOAD_FAST                'key'
               84  CALL_FUNCTION_1       1  ''
               86  BINARY_SUBTRACT  
               88  BINARY_MULTIPLY  
               90  BINARY_ADD       
               92  STORE_FAST               'key_0'
               94  JUMP_FORWARD        132  'to 132'
             96_0  COME_FROM            70  '70'

 L.  76        96  LOAD_FAST                'digestmod'
               98  LOAD_METHOD              new
              100  LOAD_FAST                'key'
              102  CALL_METHOD_1         1  ''
              104  LOAD_METHOD              digest
              106  CALL_METHOD_0         0  ''
              108  STORE_FAST               'hash_k'

 L.  77       110  LOAD_FAST                'hash_k'
              112  LOAD_CONST               b'\x00'
              114  LOAD_FAST                'digestmod'
              116  LOAD_ATTR                block_size
              118  LOAD_GLOBAL              len
              120  LOAD_FAST                'hash_k'
              122  CALL_FUNCTION_1       1  ''
              124  BINARY_SUBTRACT  
              126  BINARY_MULTIPLY  
              128  BINARY_ADD       
              130  STORE_FAST               'key_0'
            132_0  COME_FROM            94  '94'
              132  POP_BLOCK        
              134  JUMP_FORWARD        162  'to 162'
            136_0  COME_FROM_FINALLY    56  '56'

 L.  78       136  DUP_TOP          
              138  LOAD_GLOBAL              AttributeError
              140  <121>               160  ''
              142  POP_TOP          
              144  POP_TOP          
              146  POP_TOP          

 L.  80       148  LOAD_GLOBAL              ValueError
              150  LOAD_STR                 'Hash type incompatible to HMAC'
              152  CALL_FUNCTION_1       1  ''
              154  RAISE_VARARGS_1       1  'exception instance'
              156  POP_EXCEPT       
              158  JUMP_FORWARD        162  'to 162'
              160  <48>             
            162_0  COME_FROM           158  '158'
            162_1  COME_FROM           134  '134'

 L.  83       162  LOAD_GLOBAL              strxor
              164  LOAD_FAST                'key_0'
              166  LOAD_CONST               b'6'
              168  LOAD_GLOBAL              len
              170  LOAD_FAST                'key_0'
              172  CALL_FUNCTION_1       1  ''
              174  BINARY_MULTIPLY  
              176  CALL_FUNCTION_2       2  ''
              178  STORE_FAST               'key_0_ipad'

 L.  86       180  LOAD_FAST                'digestmod'
              182  LOAD_METHOD              new
              184  LOAD_FAST                'key_0_ipad'
              186  CALL_METHOD_1         1  ''
              188  LOAD_FAST                'self'
              190  STORE_ATTR               _inner

 L.  87       192  LOAD_FAST                'self'
              194  LOAD_ATTR                _inner
              196  LOAD_METHOD              update
              198  LOAD_FAST                'msg'
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          

 L.  90       204  LOAD_GLOBAL              strxor
              206  LOAD_FAST                'key_0'
              208  LOAD_CONST               b'\\'
              210  LOAD_GLOBAL              len
              212  LOAD_FAST                'key_0'
              214  CALL_FUNCTION_1       1  ''
              216  BINARY_MULTIPLY  
              218  CALL_FUNCTION_2       2  ''
              220  STORE_FAST               'key_0_opad'

 L.  93       222  LOAD_FAST                'digestmod'
              224  LOAD_METHOD              new
              226  LOAD_FAST                'key_0_opad'
              228  CALL_METHOD_1         1  ''
              230  LOAD_FAST                'self'
              232  STORE_ATTR               _outer

Parse error at or near `None' instruction at offset -1

    def update(self, msg):
        """Authenticate the next chunk of message.

        Args:
            data (byte string/byte array/memoryview): The next chunk of data
        """
        self._inner.updatemsg
        return self

    def _pbkdf2_hmac_assist(self, first_digest, iterations):
        """Carry out the expensive inner loop for PBKDF2-HMAC"""
        result = self._digestmod._pbkdf2_hmac_assist(self._inner, self._outer, first_digest, iterations)
        return result

    def copy(self):
        """Return a copy ("clone") of the HMAC object.

        The copy will have the same internal state as the original HMAC
        object.
        This can be used to efficiently compute the MAC tag of byte
        strings that share a common initial substring.

        :return: An :class:`HMAC`
        """
        new_hmac = HMAC(b'fake key', digestmod=(self._digestmod))
        new_hmac._inner = self._inner.copy
        new_hmac._outer = self._outer.copy
        return new_hmac

    def digest(self):
        """Return the **binary** (non-printable) MAC tag of the message
        authenticated so far.

        :return: The MAC tag digest, computed over the data processed so far.
                 Binary form.
        :rtype: byte string
        """
        frozen_outer_hash = self._outer.copy
        frozen_outer_hash.updateself._inner.digest
        return frozen_outer_hash.digest

    def verify(self, mac_tag):
        """Verify that a given **binary** MAC (computed by another party)
        is valid.

        Args:
          mac_tag (byte string/byte string/memoryview): the expected MAC of the message.

        Raises:
            ValueError: if the MAC does not match. It means that the message
                has been tampered with or that the MAC key is incorrect.
        """
        secret = get_random_bytes(16)
        mac1 = BLAKE2s.new(digest_bits=160, key=secret, data=mac_tag)
        mac2 = BLAKE2s.new(digest_bits=160, key=secret, data=(self.digest))
        if mac1.digest != mac2.digest:
            raise ValueError('MAC check failed')

    def hexdigest(self):
        """Return the **printable** MAC tag of the message authenticated so far.

        :return: The MAC tag, computed over the data processed so far.
                 Hexadecimal encoded.
        :rtype: string
        """
        return ''.join['%02x' % bord(x) for x in tuple(self.digest)]

    def hexverify(self, hex_mac_tag):
        """Verify that a given **printable** MAC (computed by another party)
        is valid.

        Args:
            hex_mac_tag (string): the expected MAC of the message,
                as a hexadecimal string.

        Raises:
            ValueError: if the MAC does not match. It means that the message
                has been tampered with or that the MAC key is incorrect.
        """
        self.verifyunhexlify(tobytes(hex_mac_tag))


def new(key, msg=b'', digestmod=None):
    """Create a new MAC object.

    Args:
        key (bytes/bytearray/memoryview):
            key for the MAC object.
            It must be long enough to match the expected security level of the
            MAC.
        msg (bytes/bytearray/memoryview):
            Optional. The very first chunk of the message to authenticate.
            It is equivalent to an early call to :meth:`HMAC.update`.
        digestmod (module):
            The hash to use to implement the HMAC.
            Default is :mod:`Crypto.Hash.MD5`.

    Returns:
        An :class:`HMAC` object
    """
    return HMAC(key, msg, digestmod)