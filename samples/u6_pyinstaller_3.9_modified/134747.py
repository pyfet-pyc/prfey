# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pyaes\blockfeeder.py
from .aes import AESBlockModeOfOperation, AESSegmentModeOfOperation, AESStreamModeOfOperation
from .util import append_PKCS7_padding, strip_PKCS7_padding, to_bufferable
PADDING_NONE = 'none'
PADDING_DEFAULT = 'default'

def _block_can_consume(self, size):
    if size >= 16:
        return 16
    return 0


def _block_final_encrypt(self, data, padding=PADDING_DEFAULT):
    if padding == PADDING_DEFAULT:
        data = append_PKCS7_padding(data)
    else:
        if padding == PADDING_NONE:
            if len(data) != 16:
                raise Exception('invalid data length for final block')
        else:
            raise Exception('invalid padding option')
    if len(data) == 32:
        return self.encrypt(data[:16]) + self.encrypt(data[16:])
    return self.encrypt(data)


def _block_final_decrypt(self, data, padding=PADDING_DEFAULT):
    if padding == PADDING_DEFAULT:
        return strip_PKCS7_padding(self.decrypt(data))
    if padding == PADDING_NONE:
        if len(data) != 16:
            raise Exception('invalid data length for final block')
        return self.decrypt(data)
    raise Exception('invalid padding option')


AESBlockModeOfOperation._can_consume = _block_can_consume
AESBlockModeOfOperation._final_encrypt = _block_final_encrypt
AESBlockModeOfOperation._final_decrypt = _block_final_decrypt

def _segment_can_consume(self, size):
    return self.segment_bytes * int(size // self.segment_bytes)


def _segment_final_encrypt(self, data, padding=PADDING_DEFAULT):
    if padding != PADDING_DEFAULT:
        raise Exception('invalid padding option')
    faux_padding = chr(0) * (self.segment_bytes - len(data) % self.segment_bytes)
    padded = data + to_bufferable(faux_padding)
    return self.encrypt(padded)[:len(data)]


def _segment_final_decrypt(self, data, padding=PADDING_DEFAULT):
    if padding != PADDING_DEFAULT:
        raise Exception('invalid padding option')
    faux_padding = chr(0) * (self.segment_bytes - len(data) % self.segment_bytes)
    padded = data + to_bufferable(faux_padding)
    return self.decrypt(padded)[:len(data)]


AESSegmentModeOfOperation._can_consume = _segment_can_consume
AESSegmentModeOfOperation._final_encrypt = _segment_final_encrypt
AESSegmentModeOfOperation._final_decrypt = _segment_final_decrypt

def _stream_can_consume(self, size):
    return size


def _stream_final_encrypt--- This code section failed: ---

 L. 127         0  LOAD_FAST                'padding'
                2  LOAD_GLOBAL              PADDING_NONE
                4  LOAD_GLOBAL              PADDING_DEFAULT
                6  BUILD_TUPLE_2         2 
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 128        12  LOAD_GLOBAL              Exception
               14  LOAD_STR                 'invalid padding option'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 130        20  LOAD_FAST                'self'
               22  LOAD_METHOD              encrypt
               24  LOAD_FAST                'data'
               26  CALL_METHOD_1         1  ''
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _stream_final_decrypt--- This code section failed: ---

 L. 133         0  LOAD_FAST                'padding'
                2  LOAD_GLOBAL              PADDING_NONE
                4  LOAD_GLOBAL              PADDING_DEFAULT
                6  BUILD_TUPLE_2         2 
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 134        12  LOAD_GLOBAL              Exception
               14  LOAD_STR                 'invalid padding option'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 136        20  LOAD_FAST                'self'
               22  LOAD_METHOD              decrypt
               24  LOAD_FAST                'data'
               26  CALL_METHOD_1         1  ''
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


AESStreamModeOfOperation._can_consume = _stream_can_consume
AESStreamModeOfOperation._final_encrypt = _stream_final_encrypt
AESStreamModeOfOperation._final_decrypt = _stream_final_decrypt

class BlockFeeder(object):
    __doc__ = 'The super-class for objects to handle chunking a stream of bytes\n       into the appropriate block size for the underlying mode of operation\n       and applying (or stripping) padding, as necessary.'

    def __init__(self, mode, feed, final, padding=PADDING_DEFAULT):
        self._mode = mode
        self._feed = feed
        self._final = final
        self._buffer = to_bufferable('')
        self._padding = padding

    def feed--- This code section failed: ---

 L. 164         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _buffer
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 165        10  LOAD_GLOBAL              ValueError
               12  LOAD_STR                 'already finished feeder'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 168        18  LOAD_FAST                'data'
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE    52  'to 52'

 L. 169        26  LOAD_FAST                'self'
               28  LOAD_METHOD              _final
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                _buffer
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                _padding
               38  CALL_METHOD_2         2  ''
               40  STORE_FAST               'result'

 L. 170        42  LOAD_CONST               None
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _buffer

 L. 171        48  LOAD_FAST                'result'
               50  RETURN_VALUE     
             52_0  COME_FROM            24  '24'

 L. 173        52  LOAD_FAST                'self'
               54  DUP_TOP          
               56  LOAD_ATTR                _buffer
               58  LOAD_GLOBAL              to_bufferable
               60  LOAD_FAST                'data'
               62  CALL_FUNCTION_1       1  ''
               64  INPLACE_ADD      
               66  ROT_TWO          
               68  STORE_ATTR               _buffer

 L. 176        70  LOAD_GLOBAL              to_bufferable
               72  LOAD_STR                 ''
               74  CALL_FUNCTION_1       1  ''
               76  STORE_FAST               'result'

 L. 177        78  LOAD_GLOBAL              len
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _buffer
               84  CALL_FUNCTION_1       1  ''
               86  LOAD_CONST               16
               88  COMPARE_OP               >
               90  POP_JUMP_IF_FALSE   166  'to 166'

 L. 178        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _mode
               96  LOAD_METHOD              _can_consume
               98  LOAD_GLOBAL              len
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                _buffer
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_CONST               16
              108  BINARY_SUBTRACT  
              110  CALL_METHOD_1         1  ''
              112  STORE_FAST               'can_consume'

 L. 179       114  LOAD_FAST                'can_consume'
              116  LOAD_CONST               0
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   124  'to 124'
              122  JUMP_ABSOLUTE       166  'to 166'
            124_0  COME_FROM           120  '120'

 L. 180       124  LOAD_FAST                'result'
              126  LOAD_FAST                'self'
              128  LOAD_METHOD              _feed
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                _buffer
              134  LOAD_CONST               None
              136  LOAD_FAST                'can_consume'
              138  BUILD_SLICE_2         2 
              140  BINARY_SUBSCR    
              142  CALL_METHOD_1         1  ''
              144  INPLACE_ADD      
              146  STORE_FAST               'result'

 L. 181       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _buffer
              152  LOAD_FAST                'can_consume'
              154  LOAD_CONST               None
              156  BUILD_SLICE_2         2 
              158  BINARY_SUBSCR    
              160  LOAD_FAST                'self'
              162  STORE_ATTR               _buffer
              164  JUMP_BACK            78  'to 78'
            166_0  COME_FROM            90  '90'

 L. 183       166  LOAD_FAST                'result'
              168  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class Encrypter(BlockFeeder):
    __doc__ = 'Accepts bytes of plaintext and returns encrypted ciphertext.'

    def __init__(self, mode, padding=PADDING_DEFAULT):
        BlockFeeder.__init__(self, mode, mode.encrypt, mode._final_encrypt, padding)


class Decrypter(BlockFeeder):
    __doc__ = 'Accepts bytes of ciphertext and returns decrypted plaintext.'

    def __init__(self, mode, padding=PADDING_DEFAULT):
        BlockFeeder.__init__(self, mode, mode.decrypt, mode._final_decrypt, padding)


BLOCK_SIZE = 8192

def _feed_stream(feeder, in_stream, out_stream, block_size=BLOCK_SIZE):
    """Uses feeder to read and convert from in_stream and write to out_stream."""
    while True:
        chunk = in_stream.read(block_size)
        if not chunk:
            break
        converted = feeder.feed(chunk)
        out_stream.write(converted)

    converted = feeder.feed()
    out_stream.write(converted)


def encrypt_stream(mode, in_stream, out_stream, block_size=BLOCK_SIZE, padding=PADDING_DEFAULT):
    """Encrypts a stream of bytes from in_stream to out_stream using mode."""
    encrypter = Encrypter(mode, padding=padding)
    _feed_stream(encrypter, in_stream, out_stream, block_size)


def decrypt_stream(mode, in_stream, out_stream, block_size=BLOCK_SIZE, padding=PADDING_DEFAULT):
    """Decrypts a stream of bytes from in_stream to out_stream using mode."""
    decrypter = Decrypter(mode, padding=padding)
    _feed_stream(decrypter, in_stream, out_stream, block_size)