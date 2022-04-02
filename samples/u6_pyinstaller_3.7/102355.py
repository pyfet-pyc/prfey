# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: Crypto\Cipher\_mode_ccm.py
"""
Counter with CBC-MAC (CCM) mode.
"""
__all__ = [
 'CcmMode']
import struct
from binascii import unhexlify
from Crypto.Util.py3compat import byte_string, bord, _copy_bytes
from Crypto.Util._raw_api import is_writeable_buffer
import Crypto.Util.strxor as strxor
from Crypto.Util.number import long_to_bytes
from Crypto.Hash import BLAKE2s
from Crypto.Random import get_random_bytes

def enum(**enums):
    return type('Enum', (), enums)


MacStatus = enum(NOT_STARTED=0, PROCESSING_AUTH_DATA=1, PROCESSING_PLAINTEXT=2)

class CcmMode(object):
    __doc__ = 'Counter with CBC-MAC (CCM).\n\n    This is an Authenticated Encryption with Associated Data (`AEAD`_) mode.\n    It provides both confidentiality and authenticity.\n\n    The header of the message may be left in the clear, if needed, and it will\n    still be subject to authentication. The decryption step tells the receiver\n    if the message comes from a source that really knowns the secret key.\n    Additionally, decryption detects if any part of the message - including the\n    header - has been modified or corrupted.\n\n    This mode requires a nonce. The nonce shall never repeat for two\n    different messages encrypted with the same key, but it does not need\n    to be random.\n    Note that there is a trade-off between the size of the nonce and the\n    maximum size of a single message you can encrypt.\n\n    It is important to use a large nonce if the key is reused across several\n    messages and the nonce is chosen randomly.\n\n    It is acceptable to us a short nonce if the key is only used a few times or\n    if the nonce is taken from a counter.\n\n    The following table shows the trade-off when the nonce is chosen at\n    random. The column on the left shows how many messages it takes\n    for the keystream to repeat **on average**. In practice, you will want to\n    stop using the key way before that.\n\n    +--------------------+---------------+-------------------+\n    | Avg. # of messages |    nonce      |     Max. message  |\n    | before keystream   |    size       |     size          |\n    | repeats            |    (bytes)    |     (bytes)       |\n    +====================+===============+===================+\n    |       2^52         |      13       |        64K        |\n    +--------------------+---------------+-------------------+\n    |       2^48         |      12       |        16M        |\n    +--------------------+---------------+-------------------+\n    |       2^44         |      11       |         4G        |\n    +--------------------+---------------+-------------------+\n    |       2^40         |      10       |         1T        |\n    +--------------------+---------------+-------------------+\n    |       2^36         |       9       |        64P        |\n    +--------------------+---------------+-------------------+\n    |       2^32         |       8       |        16E        |\n    +--------------------+---------------+-------------------+\n\n    This mode is only available for ciphers that operate on 128 bits blocks\n    (e.g. AES but not TDES).\n\n    See `NIST SP800-38C`_ or RFC3610_.\n\n    .. _`NIST SP800-38C`: http://csrc.nist.gov/publications/nistpubs/800-38C/SP800-38C.pdf\n    .. _RFC3610: https://tools.ietf.org/html/rfc3610\n    .. _AEAD: http://blog.cryptographyengineering.com/2012/05/how-to-choose-authenticated-encryption.html\n\n    :undocumented: __init__\n    '

    def __init__--- This code section failed: ---

 L. 119         0  LOAD_FAST                'factory'
                2  LOAD_ATTR                block_size
                4  LOAD_FAST                'self'
                6  STORE_ATTR               block_size

 L. 122         8  LOAD_GLOBAL              _copy_bytes
               10  LOAD_CONST               None
               12  LOAD_CONST               None
               14  LOAD_FAST                'nonce'
               16  CALL_FUNCTION_3       3  '3 positional arguments'
               18  LOAD_FAST                'self'
               20  STORE_ATTR               nonce

 L. 125        22  LOAD_FAST                'factory'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _factory

 L. 126        28  LOAD_GLOBAL              _copy_bytes
               30  LOAD_CONST               None
               32  LOAD_CONST               None
               34  LOAD_FAST                'key'
               36  CALL_FUNCTION_3       3  '3 positional arguments'
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _key

 L. 127        42  LOAD_FAST                'mac_len'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _mac_len

 L. 128        48  LOAD_FAST                'msg_len'
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _msg_len

 L. 129        54  LOAD_FAST                'assoc_len'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _assoc_len

 L. 130        60  LOAD_FAST                'cipher_params'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _cipher_params

 L. 132        66  LOAD_CONST               None
               68  LOAD_FAST                'self'
               70  STORE_ATTR               _mac_tag

 L. 134        72  LOAD_FAST                'self'
               74  LOAD_ATTR                block_size
               76  LOAD_CONST               16
               78  COMPARE_OP               !=
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 135        82  LOAD_GLOBAL              ValueError
               84  LOAD_STR                 'CCM mode is only available for ciphers that operate on 128 bits blocks'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'

 L. 139        90  LOAD_FAST                'mac_len'
               92  LOAD_CONST               (4, 6, 8, 10, 12, 14, 16)
               94  COMPARE_OP               not-in
               96  POP_JUMP_IF_FALSE   110  'to 110'

 L. 140        98  LOAD_GLOBAL              ValueError
              100  LOAD_STR                 "Parameter 'mac_len' must be even and in the range 4..16 (not %d)"

 L. 141       102  LOAD_FAST                'mac_len'
              104  BINARY_MODULO    
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  RAISE_VARARGS_1       1  'exception instance'
            110_0  COME_FROM            96  '96'

 L. 144       110  LOAD_FAST                'nonce'
              112  POP_JUMP_IF_FALSE   140  'to 140'
              114  LOAD_CONST               7
              116  LOAD_GLOBAL              len
              118  LOAD_FAST                'nonce'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  DUP_TOP          
              124  ROT_THREE        
              126  COMPARE_OP               <=
              128  POP_JUMP_IF_FALSE   138  'to 138'
              130  LOAD_CONST               13
              132  COMPARE_OP               <=
              134  POP_JUMP_IF_TRUE    148  'to 148'
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM           128  '128'
              138  POP_TOP          
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM           112  '112'

 L. 145       140  LOAD_GLOBAL              ValueError
              142  LOAD_STR                 "Length of parameter 'nonce' must be in the range 7..13 bytes"
              144  CALL_FUNCTION_1       1  '1 positional argument'
              146  RAISE_VARARGS_1       1  'exception instance'
            148_0  COME_FROM           134  '134'

 L. 150       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _factory
              152  LOAD_ATTR                new
              154  LOAD_FAST                'key'

 L. 151       156  LOAD_FAST                'factory'
              158  LOAD_ATTR                MODE_CBC
              160  BUILD_TUPLE_2         2 
              162  LOAD_STR                 'iv'

 L. 152       164  LOAD_CONST               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
              166  BUILD_MAP_1           1 

 L. 153       168  LOAD_FAST                'cipher_params'
              170  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              172  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              174  LOAD_FAST                'self'
              176  STORE_ATTR               _mac

 L. 154       178  LOAD_GLOBAL              MacStatus
              180  LOAD_ATTR                NOT_STARTED
              182  LOAD_FAST                'self'
              184  STORE_ATTR               _mac_status

 L. 155       186  LOAD_CONST               None
              188  LOAD_FAST                'self'
              190  STORE_ATTR               _t

 L. 158       192  LOAD_FAST                'self'
              194  LOAD_ATTR                update
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                encrypt
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                decrypt

 L. 159       204  LOAD_FAST                'self'
              206  LOAD_ATTR                digest
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                verify
              212  BUILD_LIST_5          5 
              214  LOAD_FAST                'self'
              216  STORE_ATTR               _next

 L. 162       218  LOAD_CONST               0
              220  LOAD_FAST                'self'
              222  STORE_ATTR               _cumul_assoc_len

 L. 163       224  LOAD_CONST               0
              226  LOAD_FAST                'self'
              228  STORE_ATTR               _cumul_msg_len

 L. 168       230  BUILD_LIST_0          0 
              232  LOAD_FAST                'self'
              234  STORE_ATTR               _cache

 L. 171       236  LOAD_CONST               15
              238  LOAD_GLOBAL              len
              240  LOAD_FAST                'nonce'
              242  CALL_FUNCTION_1       1  '1 positional argument'
              244  BINARY_SUBTRACT  
              246  STORE_FAST               'q'

 L. 172       248  LOAD_FAST                'self'
              250  LOAD_ATTR                _factory
              252  LOAD_ATTR                new
              254  LOAD_FAST                'key'

 L. 173       256  LOAD_FAST                'self'
              258  LOAD_ATTR                _factory
              260  LOAD_ATTR                MODE_CTR
              262  BUILD_TUPLE_2         2 
              264  LOAD_STR                 'nonce'

 L. 174       266  LOAD_GLOBAL              struct
              268  LOAD_METHOD              pack
              270  LOAD_STR                 'B'
              272  LOAD_FAST                'q'
              274  LOAD_CONST               1
              276  BINARY_SUBTRACT  
              278  CALL_METHOD_2         2  '2 positional arguments'
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                nonce
              284  BINARY_ADD       
              286  BUILD_MAP_1           1 

 L. 175       288  LOAD_FAST                'cipher_params'
              290  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              292  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              294  LOAD_FAST                'self'
              296  STORE_ATTR               _cipher

 L. 178       298  LOAD_FAST                'self'
              300  LOAD_ATTR                _cipher
              302  LOAD_METHOD              encrypt
              304  LOAD_CONST               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
              306  CALL_METHOD_1         1  '1 positional argument'
              308  LOAD_FAST                'self'
              310  STORE_ATTR               _s_0

 L. 181       312  LOAD_CONST               None
              314  LOAD_FAST                'assoc_len'
              316  LOAD_FAST                'msg_len'
              318  BUILD_TUPLE_2         2 
              320  COMPARE_OP               not-in
          322_324  POP_JUMP_IF_FALSE   334  'to 334'

 L. 182       326  LOAD_FAST                'self'
              328  LOAD_METHOD              _start_mac
              330  CALL_METHOD_0         0  '0 positional arguments'
              332  POP_TOP          
            334_0  COME_FROM           322  '322'

Parse error at or near `POP_TOP' instruction at offset 332

    def _start_mac(self):
        assert self._mac_status == MacStatus.NOT_STARTED
        assert None not in (self._assoc_len, self._msg_len)
        assert isinstance(self._cache, list)
        q = 15 - len(self.nonce)
        flags = 64 * (self._assoc_len > 0) + 8 * ((self._mac_len - 2) // 2) + (q - 1)
        b_0 = struct.pack'B'flags + self.nonce + long_to_bytes(self._msg_len, q)
        assoc_len_encoded = b''
        if self._assoc_len > 0:
            if self._assoc_len < 65280:
                enc_size = 2
            else:
                if self._assoc_len < 4294967296:
                    assoc_len_encoded = b'\xff\xfe'
                    enc_size = 4
                else:
                    assoc_len_encoded = b'\xff\xff'
                    enc_size = 8
            assoc_len_encoded += long_to_bytes(self._assoc_len, enc_size)
        self._cache.insert0b_0
        self._cache.insert1assoc_len_encoded
        first_data_to_mac = (b'').joinself._cache
        self._cache = b''
        self._mac_status = MacStatus.PROCESSING_AUTH_DATA
        self._updatefirst_data_to_mac

    def _pad_cache_and_update(self):
        assert self._mac_status != MacStatus.NOT_STARTED
        assert len(self._cache) < self.block_size
        len_cache = len(self._cache)
        if len_cache > 0:
            self._update(b'\x00' * (self.block_size - len_cache))

    def update(self, assoc_data):
        """Protect associated data

        If there is any associated data, the caller has to invoke
        this function one or more times, before using
        ``decrypt`` or ``encrypt``.

        By *associated data* it is meant any data (e.g. packet headers) that
        will not be encrypted and will be transmitted in the clear.
        However, the receiver is still able to detect any modification to it.
        In CCM, the *associated data* is also called
        *additional authenticated data* (AAD).

        If there is no associated data, this method must not be called.

        The caller may split associated data in segments of any size, and
        invoke this method multiple times, each time with the next segment.

        :Parameters:
          assoc_data : bytes/bytearray/memoryview
            A piece of associated data. There are no restrictions on its size.
        """
        if self.update not in self._next:
            raise TypeError('update() can only be called immediately after initialization')
        self._next = [
         self.update, self.encrypt, self.decrypt,
         self.digest, self.verify]
        self._cumul_assoc_len += len(assoc_data)
        if self._assoc_len is not None:
            if self._cumul_assoc_len > self._assoc_len:
                raise ValueError('Associated data is too long')
        self._updateassoc_data
        return self

    def _update(self, assoc_data_pt=b''):
        """Update the MAC with associated data or plaintext
           (without FSM checks)"""
        if self._mac_status == MacStatus.NOT_STARTED:
            if is_writeable_buffer(assoc_data_pt):
                assoc_data_pt = _copy_bytes(None, None, assoc_data_pt)
            self._cache.appendassoc_data_pt
            return
        assert len(self._cache) < self.block_size
        if len(self._cache) > 0:
            filler = min(self.block_size - len(self._cache), len(assoc_data_pt))
            self._cache += _copy_bytes(None, filler, assoc_data_pt)
            assoc_data_pt = _copy_bytes(filler, None, assoc_data_pt)
            if len(self._cache) < self.block_size:
                return
            self._t = self._mac.encryptself._cache
            self._cache = b''
        update_len = len(assoc_data_pt) // self.block_size * self.block_size
        self._cache = _copy_bytes(update_len, None, assoc_data_pt)
        if update_len > 0:
            self._t = self._mac.encryptassoc_data_pt[:update_len][-16:]

    def encrypt(self, plaintext, output=None):
        """Encrypt data with the key set at initialization.

        A cipher object is stateful: once you have encrypted a message
        you cannot encrypt (or decrypt) another message using the same
        object.

        This method can be called only **once** if ``msg_len`` was
        not passed at initialization.

        If ``msg_len`` was given, the data to encrypt can be broken
        up in two or more pieces and `encrypt` can be called
        multiple times.

        That is, the statement:

            >>> c.encrypt(a) + c.encrypt(b)

        is equivalent to:

             >>> c.encrypt(a+b)

        This function does not add any padding to the plaintext.

        :Parameters:
          plaintext : bytes/bytearray/memoryview
            The piece of data to encrypt.
            It can be of any length.
        :Keywords:
          output : bytearray/memoryview
            The location where the ciphertext must be written to.
            If ``None``, the ciphertext is returned.
        :Return:
          If ``output`` is ``None``, the ciphertext as ``bytes``.
          Otherwise, ``None``.
        """
        if self.encrypt not in self._next:
            raise TypeError('encrypt() can only be called after initialization or an update()')
        else:
            self._next = [
             self.encrypt, self.digest]
            if self._assoc_len is None:
                assert isinstance(self._cache, list)
                self._assoc_len = sum([len(x) for x in self._cache])
                if self._msg_len is not None:
                    self._start_mac
            elif self._cumul_assoc_len < self._assoc_len:
                raise ValueError('Associated data is too short')
        if self._msg_len is None:
            self._msg_len = len(plaintext)
            self._start_mac
            self._next = [self.digest]
        self._cumul_msg_len += len(plaintext)
        if self._cumul_msg_len > self._msg_len:
            raise ValueError('Message is too long')
        if self._mac_status == MacStatus.PROCESSING_AUTH_DATA:
            self._pad_cache_and_update
            self._mac_status = MacStatus.PROCESSING_PLAINTEXT
        self._updateplaintext
        return self._cipher.encrypt(plaintext, output=output)

    def decrypt(self, ciphertext, output=None):
        """Decrypt data with the key set at initialization.

        A cipher object is stateful: once you have decrypted a message
        you cannot decrypt (or encrypt) another message with the same
        object.

        This method can be called only **once** if ``msg_len`` was
        not passed at initialization.

        If ``msg_len`` was given, the data to decrypt can be
        broken up in two or more pieces and `decrypt` can be
        called multiple times.

        That is, the statement:

            >>> c.decrypt(a) + c.decrypt(b)

        is equivalent to:

             >>> c.decrypt(a+b)

        This function does not remove any padding from the plaintext.

        :Parameters:
          ciphertext : bytes/bytearray/memoryview
            The piece of data to decrypt.
            It can be of any length.
        :Keywords:
          output : bytearray/memoryview
            The location where the plaintext must be written to.
            If ``None``, the plaintext is returned.
        :Return:
          If ``output`` is ``None``, the plaintext as ``bytes``.
          Otherwise, ``None``.
        """
        if self.decrypt not in self._next:
            raise TypeError('decrypt() can only be called after initialization or an update()')
        else:
            self._next = [
             self.decrypt, self.verify]
            if self._assoc_len is None:
                if not isinstance(self._cache, list):
                    raise AssertionError
                else:
                    self._assoc_len = sum([len(x) for x in self._cache])
                    if self._msg_len is not None:
                        self._start_mac
                    else:
                        if self._cumul_assoc_len < self._assoc_len:
                            raise ValueError('Associated data is too short')
                if self._msg_len is None:
                    self._msg_len = len(ciphertext)
                    self._start_mac
                    self._next = [self.verify]
                self._cumul_msg_len += len(ciphertext)
                if self._cumul_msg_len > self._msg_len:
                    raise ValueError('Message is too long')
                if self._mac_status == MacStatus.PROCESSING_AUTH_DATA:
                    self._pad_cache_and_update
                    self._mac_status = MacStatus.PROCESSING_PLAINTEXT
                plaintext = self._cipher.encrypt(ciphertext, output=output)
                if output is None:
                    self._updateplaintext
            else:
                self._updateoutput
        return plaintext

    def digest(self):
        """Compute the *binary* MAC tag.

        The caller invokes this function at the very end.

        This method returns the MAC that shall be sent to the receiver,
        together with the ciphertext.

        :Return: the MAC, as a byte string.
        """
        if self.digest not in self._next:
            raise TypeError('digest() cannot be called when decrypting or validating a message')
        self._next = [self.digest]
        return self._digest

    def _digest(self):
        if self._mac_tag:
            return self._mac_tag
            if self._assoc_len is None:
                assert isinstance(self._cache, list)
                self._assoc_len = sum([len(x) for x in self._cache])
                if self._msg_len is not None:
                    self._start_mac
        elif self._cumul_assoc_len < self._assoc_len:
            raise ValueError('Associated data is too short')
        if self._msg_len is None:
            self._msg_len = 0
            self._start_mac
        if self._cumul_msg_len != self._msg_len:
            raise ValueError('Message is too short')
        self._pad_cache_and_update
        self._mac_tag = strxor(self._t, self._s_0)[:self._mac_len]
        return self._mac_tag

    def hexdigest(self):
        """Compute the *printable* MAC tag.

        This method is like `digest`.

        :Return: the MAC, as a hexadecimal string.
        """
        return ''.join['%02x' % bord(x) for x in self.digest]

    def verify(self, received_mac_tag):
        """Validate the *binary* MAC tag.

        The caller invokes this function at the very end.

        This method checks if the decrypted message is indeed valid
        (that is, if the key is correct) and it has not been
        tampered with while in transit.

        :Parameters:
          received_mac_tag : bytes/bytearray/memoryview
            This is the *binary* MAC, as received from the sender.
        :Raises ValueError:
            if the MAC does not match. The message has been tampered with
            or the key is incorrect.
        """
        if self.verify not in self._next:
            raise TypeError('verify() cannot be called when encrypting a message')
        self._next = [self.verify]
        self._digest
        secret = get_random_bytes(16)
        mac1 = BLAKE2s.new(digest_bits=160, key=secret, data=(self._mac_tag))
        mac2 = BLAKE2s.new(digest_bits=160, key=secret, data=received_mac_tag)
        if mac1.digest != mac2.digest:
            raise ValueError('MAC check failed')

    def hexverify(self, hex_mac_tag):
        """Validate the *printable* MAC tag.

        This method is like `verify`.

        :Parameters:
          hex_mac_tag : string
            This is the *printable* MAC, as received from the sender.
        :Raises ValueError:
            if the MAC does not match. The message has been tampered with
            or the key is incorrect.
        """
        self.verifyunhexlify(hex_mac_tag)

    def encrypt_and_digest(self, plaintext, output=None):
        """Perform encrypt() and digest() in one step.

        :Parameters:
          plaintext : bytes/bytearray/memoryview
            The piece of data to encrypt.
        :Keywords:
          output : bytearray/memoryview
            The location where the ciphertext must be written to.
            If ``None``, the ciphertext is returned.
        :Return:
            a tuple with two items:

            - the ciphertext, as ``bytes``
            - the MAC tag, as ``bytes``

            The first item becomes ``None`` when the ``output`` parameter
            specified a location for the result.
        """
        return (
         self.encrypt(plaintext, output=output), self.digest)

    def decrypt_and_verify(self, ciphertext, received_mac_tag, output=None):
        """Perform decrypt() and verify() in one step.

        :Parameters:
          ciphertext : bytes/bytearray/memoryview
            The piece of data to decrypt.
          received_mac_tag : bytes/bytearray/memoryview
            This is the *binary* MAC, as received from the sender.
        :Keywords:
          output : bytearray/memoryview
            The location where the plaintext must be written to.
            If ``None``, the plaintext is returned.
        :Return: the plaintext as ``bytes`` or ``None`` when the ``output``
            parameter specified a location for the result.
        :Raises ValueError:
            if the MAC does not match. The message has been tampered with
            or the key is incorrect.
        """
        plaintext = self.decrypt(ciphertext, output=output)
        self.verifyreceived_mac_tag
        return plaintext


def _create_ccm_cipher(factory, **kwargs):
    """Create a new block cipher, configured in CCM mode.

    :Parameters:
      factory : module
        A symmetric cipher module from `Crypto.Cipher` (like
        `Crypto.Cipher.AES`).

    :Keywords:
      key : bytes/bytearray/memoryview
        The secret key to use in the symmetric cipher.

      nonce : bytes/bytearray/memoryview
        A value that must never be reused for any other encryption.

        Its length must be in the range ``[7..13]``.
        11 or 12 bytes are reasonable values in general. Bear in
        mind that with CCM there is a trade-off between nonce length and
        maximum message size.

        If not specified, a 11 byte long random string is used.

      mac_len : integer
        Length of the MAC, in bytes. It must be even and in
        the range ``[4..16]``. The default is 16.

      msg_len : integer
        Length of the message to (de)cipher.
        If not specified, ``encrypt`` or ``decrypt`` may only be called once.

      assoc_len : integer
        Length of the associated data.
        If not specified, all data is internally buffered.
    """
    try:
        key = key = kwargs.pop'key'
    except KeyError as e:
        try:
            raise TypeError('Missing parameter: ' + str(e))
        finally:
            e = None
            del e

    nonce = kwargs.pop'nonce'None
    if nonce is None:
        nonce = get_random_bytes(11)
    mac_len = kwargs.pop'mac_len'factory.block_size
    msg_len = kwargs.pop'msg_len'None
    assoc_len = kwargs.pop'assoc_len'None
    cipher_params = dict(kwargs)
    return CcmMode(factory, key, nonce, mac_len, msg_len, assoc_len, cipher_params)