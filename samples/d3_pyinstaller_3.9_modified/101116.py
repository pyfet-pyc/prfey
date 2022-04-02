# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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

    def __init__--- This code section failed: ---

 L.  40         0  LOAD_FAST                'fp'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _fp

 L.  41         6  LOAD_CONST               False
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _eof

 L.  42        12  LOAD_CONST               0
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _pos

 L.  45        18  LOAD_CONST               -1
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _size

 L.  51        24  LOAD_FAST                'decomp_factory'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _decomp_factory

 L.  52        30  LOAD_FAST                'decomp_args'
               32  LOAD_FAST                'self'
               34  STORE_ATTR               _decomp_args

 L.  53        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _decomp_factory
               40  BUILD_TUPLE_0         0 
               42  BUILD_MAP_0           0 
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _decomp_args
               48  <164>                 1  ''
               50  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _decompressor

 L.  57        56  LOAD_FAST                'trailing_error'
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _trailing_error

Parse error at or near `<164>' instruction at offset 48

    def close(self):
        self._decompressor = None
        return super().close()

    def seekable(self):
        return self._fp.seekable()

    def readinto--- This code section failed: ---

 L.  67         0  LOAD_GLOBAL              memoryview
                2  LOAD_FAST                'b'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           96  'to 96'
                8  STORE_FAST               'view'
               10  LOAD_FAST                'view'
               12  LOAD_METHOD              cast
               14  LOAD_STR                 'B'
               16  CALL_METHOD_1         1  ''
               18  SETUP_WITH           66  'to 66'
               20  STORE_FAST               'byte_view'

 L.  68        22  LOAD_FAST                'self'
               24  LOAD_METHOD              read
               26  LOAD_GLOBAL              len
               28  LOAD_FAST                'byte_view'
               30  CALL_FUNCTION_1       1  ''
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'data'

 L.  69        36  LOAD_FAST                'data'
               38  LOAD_FAST                'byte_view'
               40  LOAD_CONST               None
               42  LOAD_GLOBAL              len
               44  LOAD_FAST                'data'
               46  CALL_FUNCTION_1       1  ''
               48  BUILD_SLICE_2         2 
               50  STORE_SUBSCR     
               52  POP_BLOCK        
               54  LOAD_CONST               None
               56  DUP_TOP          
               58  DUP_TOP          
               60  CALL_FUNCTION_3       3  ''
               62  POP_TOP          
               64  JUMP_FORWARD         82  'to 82'
             66_0  COME_FROM_WITH       18  '18'
               66  <49>             
               68  POP_JUMP_IF_TRUE     72  'to 72'
               70  <48>             
             72_0  COME_FROM            68  '68'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          
               78  POP_EXCEPT       
               80  POP_TOP          
             82_0  COME_FROM            64  '64'
               82  POP_BLOCK        
               84  LOAD_CONST               None
               86  DUP_TOP          
               88  DUP_TOP          
               90  CALL_FUNCTION_3       3  ''
               92  POP_TOP          
               94  JUMP_FORWARD        112  'to 112'
             96_0  COME_FROM_WITH        6  '6'
               96  <49>             
               98  POP_JUMP_IF_TRUE    102  'to 102'
              100  <48>             
            102_0  COME_FROM            98  '98'
              102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          
              108  POP_EXCEPT       
              110  POP_TOP          
            112_0  COME_FROM            94  '94'

 L.  70       112  LOAD_GLOBAL              len
              114  LOAD_FAST                'data'
              116  CALL_FUNCTION_1       1  ''
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 56

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
             34_0  COME_FROM           192  '192'
             34_1  COME_FROM           188  '188'

 L.  82        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _decompressor
               38  LOAD_ATTR                eof
               40  POP_JUMP_IF_FALSE   134  'to 134'

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

 L.  86        66  JUMP_FORWARD        194  'to 194'
             68_0  COME_FROM            64  '64'

 L.  88        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _decomp_factory
               72  BUILD_TUPLE_0         0 
               74  BUILD_MAP_0           0 

 L.  89        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _decomp_args

 L.  88        80  <164>                 1  ''
               82  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               84  LOAD_FAST                'self'
               86  STORE_ATTR               _decompressor

 L.  90        88  SETUP_FINALLY       108  'to 108'

 L.  91        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _decompressor
               94  LOAD_METHOD              decompress
               96  LOAD_FAST                'rawblock'
               98  LOAD_FAST                'size'
              100  CALL_METHOD_2         2  ''
              102  STORE_FAST               'data'
              104  POP_BLOCK        
              106  JUMP_FORWARD        186  'to 186'
            108_0  COME_FROM_FINALLY    88  '88'

 L.  92       108  DUP_TOP          
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                _trailing_error
              114  <121>               130  ''
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L.  94       122  POP_EXCEPT       
              124  BREAK_LOOP          194  'to 194'
              126  POP_EXCEPT       
              128  JUMP_FORWARD        186  'to 186'
              130  <48>             
              132  JUMP_FORWARD        186  'to 186'
            134_0  COME_FROM            40  '40'

 L.  96       134  LOAD_FAST                'self'
              136  LOAD_ATTR                _decompressor
              138  LOAD_ATTR                needs_input
              140  POP_JUMP_IF_FALSE   168  'to 168'

 L.  97       142  LOAD_FAST                'self'
              144  LOAD_ATTR                _fp
              146  LOAD_METHOD              read
              148  LOAD_GLOBAL              BUFFER_SIZE
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'rawblock'

 L.  98       154  LOAD_FAST                'rawblock'
              156  POP_JUMP_IF_TRUE    172  'to 172'

 L.  99       158  LOAD_GLOBAL              EOFError
              160  LOAD_STR                 'Compressed file ended before the end-of-stream marker was reached'
              162  CALL_FUNCTION_1       1  ''
              164  RAISE_VARARGS_1       1  'exception instance'
              166  JUMP_FORWARD        172  'to 172'
            168_0  COME_FROM           140  '140'

 L. 102       168  LOAD_CONST               b''
              170  STORE_FAST               'rawblock'
            172_0  COME_FROM           166  '166'
            172_1  COME_FROM           156  '156'

 L. 103       172  LOAD_FAST                'self'
              174  LOAD_ATTR                _decompressor
              176  LOAD_METHOD              decompress
              178  LOAD_FAST                'rawblock'
              180  LOAD_FAST                'size'
              182  CALL_METHOD_2         2  ''
              184  STORE_FAST               'data'
            186_0  COME_FROM           132  '132'
            186_1  COME_FROM           128  '128'
            186_2  COME_FROM           106  '106'

 L. 104       186  LOAD_FAST                'data'
              188  POP_JUMP_IF_FALSE_BACK    34  'to 34'

 L. 105       190  JUMP_FORWARD        194  'to 194'
              192  JUMP_BACK            34  'to 34'
            194_0  COME_FROM           190  '190'
            194_1  COME_FROM           124  '124'
            194_2  COME_FROM            66  '66'

 L. 106       194  LOAD_FAST                'data'
              196  POP_JUMP_IF_TRUE    216  'to 216'

 L. 107       198  LOAD_CONST               True
              200  LOAD_FAST                'self'
              202  STORE_ATTR               _eof

 L. 108       204  LOAD_FAST                'self'
              206  LOAD_ATTR                _pos
              208  LOAD_FAST                'self'
              210  STORE_ATTR               _size

 L. 109       212  LOAD_CONST               b''
              214  RETURN_VALUE     
            216_0  COME_FROM           196  '196'

 L. 110       216  LOAD_FAST                'self'
              218  DUP_TOP          
              220  LOAD_ATTR                _pos
              222  LOAD_GLOBAL              len
              224  LOAD_FAST                'data'
              226  CALL_FUNCTION_1       1  ''
              228  INPLACE_ADD      
              230  ROT_TWO          
              232  STORE_ATTR               _pos

 L. 111       234  LOAD_FAST                'data'
              236  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 80

    def _rewind--- This code section failed: ---

 L. 115         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _fp
                4  LOAD_METHOD              seek
                6  LOAD_CONST               0
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 116        12  LOAD_CONST               False
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _eof

 L. 117        18  LOAD_CONST               0
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _pos

 L. 118        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _decomp_factory
               28  BUILD_TUPLE_0         0 
               30  BUILD_MAP_0           0 
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _decomp_args
               36  <164>                 1  ''
               38  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _decompressor

Parse error at or near `<164>' instruction at offset 36

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