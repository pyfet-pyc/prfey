# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: _compression.py
"""Internal classes used by the gzip, lzma and bz2 modules"""
import io
BUFFER_SIZE = io.DEFAULT_BUFFER_SIZE

class BaseStream(io.BufferedIOBase):
    __doc__ = 'Mode-checking helper functions.'

    def _check_not_closed(self):
        if self.closed:
            raise ValueError('I/O operation on closed file')

    def _check_can_read(self):
        if not self.readable():
            raise io.UnsupportedOperation('File not open for reading')

    def _check_can_write(self):
        if not self.writable():
            raise io.UnsupportedOperation('File not open for writing')

    def _check_can_seek(self):
        if not self.readable():
            raise io.UnsupportedOperation('Seeking is only supported on files open for reading')
        if not self.seekable():
            raise io.UnsupportedOperation('The underlying file object does not support seeking')


class DecompressReader(io.RawIOBase):
    __doc__ = 'Adapts the decompressor API to a RawIOBase reader API'

    def readable(self):
        return True

    def __init__(self, fp, decomp_factory, trailing_error=(), **decomp_args):
        self._fp = fp
        self._eof = False
        self._pos = 0
        self._size = -1
        self._decomp_factory = decomp_factory
        self._decomp_args = decomp_args
        self._decompressor = (self._decomp_factory)(**self._decomp_args)
        self._trailing_error = trailing_error

    def close(self):
        self._decompressor = None
        return super().close()

    def seekable(self):
        return self._fp.seekable()

    def readinto(self, b):
        with memoryview(b) as view:
            with view.cast('B') as byte_view:
                data = self.read(len(byte_view))
                byte_view[:len(data)] = data
        return len(data)

    def read--- This code section failed: ---

 L.  73         0  LOAD_FAST                'size'
                2  LOAD_CONST               0
                4  COMPARE_OP               <
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  74         8  LOAD_FAST                'self'
               10  LOAD_METHOD              readall
               12  CALL_METHOD_0         0  ''
               14  RETURN_VALUE     
             16_0  COME_FROM             6  '6'

 L.  76        16  LOAD_FAST                'size'
               18  POP_JUMP_IF_FALSE    26  'to 26'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _eof
               24  POP_JUMP_IF_FALSE    30  'to 30'
             26_0  COME_FROM            18  '18'

 L.  77        26  LOAD_CONST               b''
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L.  78        30  LOAD_CONST               None
               32  STORE_FAST               'data'
             34_0  COME_FROM           190  '190'
             34_1  COME_FROM           186  '186'

 L.  82        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _decompressor
               38  LOAD_ATTR                eof
               40  POP_JUMP_IF_FALSE   132  'to 132'

 L.  83        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _decompressor
               46  LOAD_ATTR                unused_data
               48  JUMP_IF_TRUE_OR_POP    60  'to 60'

 L.  84        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _fp
               54  LOAD_METHOD              read
               56  LOAD_GLOBAL              BUFFER_SIZE
               58  CALL_METHOD_1         1  ''
             60_0  COME_FROM            48  '48'

 L.  83        60  STORE_FAST               'rawblock'

 L.  85        62  LOAD_FAST                'rawblock'
               64  POP_JUMP_IF_TRUE     68  'to 68'

 L.  86        66  JUMP_FORWARD        192  'to 192'
             68_0  COME_FROM            64  '64'

 L.  88        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _decomp_factory
               72  BUILD_TUPLE_0         0 

 L.  89        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _decomp_args

 L.  88        78  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               80  LOAD_FAST                'self'
               82  STORE_ATTR               _decompressor

 L.  90        84  SETUP_FINALLY       104  'to 104'

 L.  91        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _decompressor
               90  LOAD_METHOD              decompress
               92  LOAD_FAST                'rawblock'
               94  LOAD_FAST                'size'
               96  CALL_METHOD_2         2  ''
               98  STORE_FAST               'data'
              100  POP_BLOCK        
              102  JUMP_FORWARD        184  'to 184'
            104_0  COME_FROM_FINALLY    84  '84'

 L.  92       104  DUP_TOP          
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                _trailing_error
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   128  'to 128'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L.  94       120  POP_EXCEPT       
              122  BREAK_LOOP          192  'to 192'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        184  'to 184'
            128_0  COME_FROM           112  '112'
              128  END_FINALLY      
              130  JUMP_FORWARD        184  'to 184'
            132_0  COME_FROM            40  '40'

 L.  96       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _decompressor
              136  LOAD_ATTR                needs_input
              138  POP_JUMP_IF_FALSE   166  'to 166'

 L.  97       140  LOAD_FAST                'self'
              142  LOAD_ATTR                _fp
              144  LOAD_METHOD              read
              146  LOAD_GLOBAL              BUFFER_SIZE
              148  CALL_METHOD_1         1  ''
              150  STORE_FAST               'rawblock'

 L.  98       152  LOAD_FAST                'rawblock'
              154  POP_JUMP_IF_TRUE    170  'to 170'

 L.  99       156  LOAD_GLOBAL              EOFError
              158  LOAD_STR                 'Compressed file ended before the end-of-stream marker was reached'
              160  CALL_FUNCTION_1       1  ''
              162  RAISE_VARARGS_1       1  'exception instance'
              164  JUMP_FORWARD        170  'to 170'
            166_0  COME_FROM           138  '138'

 L. 102       166  LOAD_CONST               b''
              168  STORE_FAST               'rawblock'
            170_0  COME_FROM           164  '164'
            170_1  COME_FROM           154  '154'

 L. 103       170  LOAD_FAST                'self'
              172  LOAD_ATTR                _decompressor
              174  LOAD_METHOD              decompress
              176  LOAD_FAST                'rawblock'
              178  LOAD_FAST                'size'
              180  CALL_METHOD_2         2  ''
              182  STORE_FAST               'data'
            184_0  COME_FROM           130  '130'
            184_1  COME_FROM           126  '126'
            184_2  COME_FROM           102  '102'

 L. 104       184  LOAD_FAST                'data'
              186  POP_JUMP_IF_FALSE_BACK    34  'to 34'

 L. 105       188  JUMP_FORWARD        192  'to 192'
              190  JUMP_BACK            34  'to 34'
            192_0  COME_FROM           188  '188'
            192_1  COME_FROM           122  '122'
            192_2  COME_FROM            66  '66'

 L. 106       192  LOAD_FAST                'data'
              194  POP_JUMP_IF_TRUE    214  'to 214'

 L. 107       196  LOAD_CONST               True
              198  LOAD_FAST                'self'
              200  STORE_ATTR               _eof

 L. 108       202  LOAD_FAST                'self'
              204  LOAD_ATTR                _pos
              206  LOAD_FAST                'self'
              208  STORE_ATTR               _size

 L. 109       210  LOAD_CONST               b''
              212  RETURN_VALUE     
            214_0  COME_FROM           194  '194'

 L. 110       214  LOAD_FAST                'self'
              216  DUP_TOP          
              218  LOAD_ATTR                _pos
              220  LOAD_GLOBAL              len
              222  LOAD_FAST                'data'
              224  CALL_FUNCTION_1       1  ''
              226  INPLACE_ADD      
              228  ROT_TWO          
              230  STORE_ATTR               _pos

 L. 111       232  LOAD_FAST                'data'
              234  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 190

    def _rewind(self):
        self._fp.seek(0)
        self._eof = False
        self._pos = 0
        self._decompressor = (self._decomp_factory)(**self._decomp_args)

    def seek(self, offset, whence=io.SEEK_SET):
        if whence == io.SEEK_SET:
            pass
        elif whence == io.SEEK_CUR:
            offset = self._pos + offset
        elif whence == io.SEEK_END:
            if self._size < 0:
                while self.read(io.DEFAULT_BUFFER_SIZE):
                    pass

            offset = self._size + offset
        else:
            raise ValueError('Invalid value for whence: {}'.format(whence))
        if offset < self._pos:
            self._rewind()
        else:
            offset -= self._pos
        while True:
            if offset > 0:
                data = self.read(min(io.DEFAULT_BUFFER_SIZE, offset))
                if not data:
                    pass
                else:
                    offset -= len(data)

        return self._pos

    def tell(self):
        """Return the current file position."""
        return self._pos