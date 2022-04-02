# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\paramiko\file.py
from paramiko.common import linefeed_byte_value, crlf, cr_byte, linefeed_byte, cr_byte_value
from paramiko.py3compat import BytesIO, PY2, u, bytes_types, text_type
from paramiko.util import ClosingContextManager

class BufferedFile(ClosingContextManager):
    __doc__ = '\n    Reusable base class to implement Python-style file buffering around a\n    simpler stream.\n    '
    _DEFAULT_BUFSIZE = 8192
    SEEK_SET = 0
    SEEK_CUR = 1
    SEEK_END = 2
    FLAG_READ = 1
    FLAG_WRITE = 2
    FLAG_APPEND = 4
    FLAG_BINARY = 16
    FLAG_BUFFERED = 32
    FLAG_LINE_BUFFERED = 64
    FLAG_UNIVERSAL_NEWLINE = 128

    def __init__(self):
        self.newlines = None
        self._flags = 0
        self._bufsize = self._DEFAULT_BUFSIZE
        self._wbuffer = BytesIO()
        self._rbuffer = bytes()
        self._at_trailing_cr = False
        self._closed = False
        self._pos = self._realpos = 0
        self._size = 0

    def __del__(self):
        self.close()

    def __iter__(self):
        """
        Returns an iterator that can be used to iterate over the lines in this
        file.  This iterator happens to return the file itself, since a file is
        its own iterator.

        :raises: ``ValueError`` -- if the file is closed.
        """
        if self._closed:
            raise ValueError('I/O operation on closed file')
        return self

    def close(self):
        """
        Close the file.  Future read and write operations will fail.
        """
        self.flush()
        self._closed = True

    def flush(self):
        """
        Write out any data in the write buffer.  This may do nothing if write
        buffering is not turned on.
        """
        self._write_all(self._wbuffer.getvalue())
        self._wbuffer = BytesIO()

    if PY2:

        def next(self):
            """
            Returns the next line from the input, or raises
            ``StopIteration`` when EOF is hit.  Unlike Python file
            objects, it's okay to mix calls to `next` and `readline`.

            :raises: ``StopIteration`` -- when the end of the file is reached.

            :returns: a line (`str`) read from the file.
            """
            line = self.readline()
            if not line:
                raise StopIteration
            return line

    else:

        def __next__(self):
            """
            Returns the next line from the input, or raises ``StopIteration``
            when EOF is hit.  Unlike python file objects, it's okay to mix
            calls to `.next` and `.readline`.

            :raises: ``StopIteration`` -- when the end of the file is reached.

            :returns: a line (`str`) read from the file.
            """
            line = self.readline()
            if not line:
                raise StopIteration
            return line

    def readable(self):
        """
        Check if the file can be read from.

        :returns:
            `True` if the file can be read from. If `False`, `read` will raise
            an exception.
        """
        return self._flags & self.FLAG_READ == self.FLAG_READ

    def writable(self):
        """
        Check if the file can be written to.

        :returns:
            `True` if the file can be written to. If `False`, `write` will
            raise an exception.
        """
        return self._flags & self.FLAG_WRITE == self.FLAG_WRITE

    def seekable(self):
        """
        Check if the file supports random access.

        :returns:
            `True` if the file supports random access. If `False`, `seek` will
            raise an exception.
        """
        return False

    def readinto(self, buff):
        """
        Read up to ``len(buff)`` bytes into ``bytearray`` *buff* and return the
        number of bytes read.

        :returns:
            The number of bytes read.
        """
        data = self.read(len(buff))
        buff[:len(data)] = data
        return len(data)

    def read(self, size=None):
        """
        Read at most ``size`` bytes from the file (less if we hit the end of
        the file first).  If the ``size`` argument is negative or omitted,
        read all the remaining data in the file.

        .. note::
            ``'b'`` mode flag is ignored (``self.FLAG_BINARY`` in
            ``self._flags``), because SSH treats all files as binary, since we
            have no idea what encoding the file is in, or even if the file is
            text data.

        :param int size: maximum number of bytes to read
        :returns:
            data read from the file (as bytes), or an empty string if EOF was
            encountered immediately
        """
        if self._closed:
            raise IOError('File is closed')
        if not self._flags & self.FLAG_READ:
            raise IOError('File is not open for reading')
        if size is None or (size < 0):
            result = self._rbuffer
            self._rbuffer = bytes()
            self._pos += len(result)
            while True:
                try:
                    new_data = self._read(self._DEFAULT_BUFSIZE)
                except EOFError:
                    new_data = None

                if new_data is None or len(new_data) == 0:
                    break
                else:
                    result += new_data
                    self._realpos += len(new_data)
                    self._pos += len(new_data)

            return result
        if size <= len(self._rbuffer):
            result = self._rbuffer[:size]
            self._rbuffer = self._rbuffer[size:]
            self._pos += len(result)
            return result
        while len(self._rbuffer) < size:
            read_size = size - len(self._rbuffer)
            if self._flags & self.FLAG_BUFFERED:
                read_size = max(self._bufsize, read_size)
            try:
                new_data = self._read(read_size)
            except EOFError:
                new_data = None

            if new_data is None or len(new_data) == 0:
                break
            else:
                self._rbuffer += new_data
                self._realpos += len(new_data)

        result = self._rbuffer[:size]
        self._rbuffer = self._rbuffer[size:]
        self._pos += len(result)
        return result

    def readline--- This code section failed: ---

 L. 254         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _closed
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L. 255         6  LOAD_GLOBAL              IOError
                8  LOAD_STR                 'File is closed'
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 256        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _flags
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                FLAG_READ
               22  BINARY_AND       
               24  POP_JUMP_IF_TRUE     34  'to 34'

 L. 257        26  LOAD_GLOBAL              IOError
               28  LOAD_STR                 'File not open for reading'
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L. 258        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _rbuffer
               38  STORE_FAST               'line'

 L. 259        40  LOAD_CONST               False
               42  STORE_FAST               'truncated'

 L. 260     44_46  SETUP_LOOP          388  'to 388'
             48_0  COME_FROM           384  '384'

 L. 262        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _at_trailing_cr
               52  POP_JUMP_IF_FALSE   130  'to 130'

 L. 263        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _flags
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                FLAG_UNIVERSAL_NEWLINE
               62  BINARY_AND       
               64  POP_JUMP_IF_FALSE   130  'to 130'

 L. 264        66  LOAD_GLOBAL              len
               68  LOAD_FAST                'line'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  LOAD_CONST               0
               74  COMPARE_OP               >
               76  POP_JUMP_IF_FALSE   130  'to 130'

 L. 268        78  LOAD_FAST                'line'
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  LOAD_GLOBAL              linefeed_byte_value
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   114  'to 114'

 L. 269        90  LOAD_FAST                'line'
               92  LOAD_CONST               1
               94  LOAD_CONST               None
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  STORE_FAST               'line'

 L. 270       102  LOAD_FAST                'self'
              104  LOAD_METHOD              _record_newline
              106  LOAD_GLOBAL              crlf
              108  CALL_METHOD_1         1  '1 positional argument'
              110  POP_TOP          
              112  JUMP_FORWARD        124  'to 124'
            114_0  COME_FROM            88  '88'

 L. 272       114  LOAD_FAST                'self'
              116  LOAD_METHOD              _record_newline
              118  LOAD_GLOBAL              cr_byte
              120  CALL_METHOD_1         1  '1 positional argument'
              122  POP_TOP          
            124_0  COME_FROM           112  '112'

 L. 273       124  LOAD_CONST               False
              126  LOAD_FAST                'self'
              128  STORE_ATTR               _at_trailing_cr
            130_0  COME_FROM            76  '76'
            130_1  COME_FROM            64  '64'
            130_2  COME_FROM            52  '52'

 L. 276       130  LOAD_FAST                'size'
              132  LOAD_CONST               None
              134  COMPARE_OP               is-not
              136  POP_JUMP_IF_FALSE   204  'to 204'
              138  LOAD_FAST                'size'
              140  LOAD_CONST               0
              142  COMPARE_OP               >=
              144  POP_JUMP_IF_FALSE   204  'to 204'

 L. 277       146  LOAD_GLOBAL              len
              148  LOAD_FAST                'line'
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  LOAD_FAST                'size'
              154  COMPARE_OP               >=
              156  POP_JUMP_IF_FALSE   190  'to 190'

 L. 279       158  LOAD_FAST                'line'
              160  LOAD_FAST                'size'
              162  LOAD_CONST               None
              164  BUILD_SLICE_2         2 
              166  BINARY_SUBSCR    
              168  LOAD_FAST                'self'
              170  STORE_ATTR               _rbuffer

 L. 280       172  LOAD_FAST                'line'
              174  LOAD_CONST               None
              176  LOAD_FAST                'size'
              178  BUILD_SLICE_2         2 
              180  BINARY_SUBSCR    
              182  STORE_FAST               'line'

 L. 281       184  LOAD_CONST               True
              186  STORE_FAST               'truncated'

 L. 282       188  BREAK_LOOP       
            190_0  COME_FROM           156  '156'

 L. 283       190  LOAD_FAST                'size'
              192  LOAD_GLOBAL              len
              194  LOAD_FAST                'line'
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  BINARY_SUBTRACT  
              200  STORE_FAST               'n'
              202  JUMP_FORWARD        210  'to 210'
            204_0  COME_FROM           144  '144'
            204_1  COME_FROM           136  '136'

 L. 285       204  LOAD_FAST                'self'
              206  LOAD_ATTR                _bufsize
              208  STORE_FAST               'n'
            210_0  COME_FROM           202  '202'

 L. 286       210  LOAD_GLOBAL              linefeed_byte
              212  LOAD_FAST                'line'
              214  COMPARE_OP               in
              216  POP_JUMP_IF_TRUE    238  'to 238'

 L. 287       218  LOAD_FAST                'self'
              220  LOAD_ATTR                _flags
              222  LOAD_FAST                'self'
              224  LOAD_ATTR                FLAG_UNIVERSAL_NEWLINE
              226  BINARY_AND       
              228  POP_JUMP_IF_FALSE   240  'to 240'
              230  LOAD_GLOBAL              cr_byte
              232  LOAD_FAST                'line'
              234  COMPARE_OP               in
              236  POP_JUMP_IF_FALSE   240  'to 240'
            238_0  COME_FROM           216  '216'

 L. 289       238  BREAK_LOOP       
            240_0  COME_FROM           236  '236'
            240_1  COME_FROM           228  '228'

 L. 290       240  SETUP_EXCEPT        256  'to 256'

 L. 291       242  LOAD_FAST                'self'
              244  LOAD_METHOD              _read
              246  LOAD_FAST                'n'
              248  CALL_METHOD_1         1  '1 positional argument'
              250  STORE_FAST               'new_data'
              252  POP_BLOCK        
              254  JUMP_FORWARD        282  'to 282'
            256_0  COME_FROM_EXCEPT    240  '240'

 L. 292       256  DUP_TOP          
              258  LOAD_GLOBAL              EOFError
              260  COMPARE_OP               exception-match
          262_264  POP_JUMP_IF_FALSE   280  'to 280'
              266  POP_TOP          
              268  POP_TOP          
              270  POP_TOP          

 L. 293       272  LOAD_CONST               None
              274  STORE_FAST               'new_data'
              276  POP_EXCEPT       
              278  JUMP_FORWARD        282  'to 282'
            280_0  COME_FROM           262  '262'
              280  END_FINALLY      
            282_0  COME_FROM           278  '278'
            282_1  COME_FROM           254  '254'

 L. 294       282  LOAD_FAST                'new_data'
              284  LOAD_CONST               None
              286  COMPARE_OP               is
          288_290  POP_JUMP_IF_TRUE    306  'to 306'
              292  LOAD_GLOBAL              len
              294  LOAD_FAST                'new_data'
              296  CALL_FUNCTION_1       1  '1 positional argument'
              298  LOAD_CONST               0
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   358  'to 358'
            306_0  COME_FROM           288  '288'

 L. 295       306  LOAD_GLOBAL              bytes
              308  CALL_FUNCTION_0       0  '0 positional arguments'
              310  LOAD_FAST                'self'
              312  STORE_ATTR               _rbuffer

 L. 296       314  LOAD_FAST                'self'
              316  DUP_TOP          
              318  LOAD_ATTR                _pos
              320  LOAD_GLOBAL              len
              322  LOAD_FAST                'line'
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  INPLACE_ADD      
              328  ROT_TWO          
              330  STORE_ATTR               _pos

 L. 297       332  LOAD_FAST                'self'
              334  LOAD_ATTR                _flags
              336  LOAD_FAST                'self'
              338  LOAD_ATTR                FLAG_BINARY
              340  BINARY_AND       
          342_344  POP_JUMP_IF_FALSE   350  'to 350'
              346  LOAD_FAST                'line'
              348  RETURN_VALUE     
            350_0  COME_FROM           342  '342'
              350  LOAD_GLOBAL              u
              352  LOAD_FAST                'line'
              354  CALL_FUNCTION_1       1  '1 positional argument'
              356  RETURN_VALUE     
            358_0  COME_FROM           302  '302'

 L. 298       358  LOAD_FAST                'line'
              360  LOAD_FAST                'new_data'
              362  INPLACE_ADD      
              364  STORE_FAST               'line'

 L. 299       366  LOAD_FAST                'self'
              368  DUP_TOP          
              370  LOAD_ATTR                _realpos
              372  LOAD_GLOBAL              len
              374  LOAD_FAST                'new_data'
              376  CALL_FUNCTION_1       1  '1 positional argument'
              378  INPLACE_ADD      
              380  ROT_TWO          
              382  STORE_ATTR               _realpos
              384  JUMP_BACK            48  'to 48'
              386  POP_BLOCK        
            388_0  COME_FROM_LOOP       44  '44'

 L. 301       388  LOAD_FAST                'line'
              390  LOAD_METHOD              find
              392  LOAD_GLOBAL              linefeed_byte
              394  CALL_METHOD_1         1  '1 positional argument'
              396  STORE_FAST               'pos'

 L. 302       398  LOAD_FAST                'self'
              400  LOAD_ATTR                _flags
              402  LOAD_FAST                'self'
              404  LOAD_ATTR                FLAG_UNIVERSAL_NEWLINE
              406  BINARY_AND       
          408_410  POP_JUMP_IF_FALSE   456  'to 456'

 L. 303       412  LOAD_FAST                'line'
              414  LOAD_METHOD              find
              416  LOAD_GLOBAL              cr_byte
              418  CALL_METHOD_1         1  '1 positional argument'
              420  STORE_FAST               'rpos'

 L. 304       422  LOAD_FAST                'rpos'
              424  LOAD_CONST               0
              426  COMPARE_OP               >=
          428_430  POP_JUMP_IF_FALSE   456  'to 456'
              432  LOAD_FAST                'rpos'
              434  LOAD_FAST                'pos'
              436  COMPARE_OP               <
          438_440  POP_JUMP_IF_TRUE    452  'to 452'
              442  LOAD_FAST                'pos'
              444  LOAD_CONST               0
              446  COMPARE_OP               <
          448_450  POP_JUMP_IF_FALSE   456  'to 456'
            452_0  COME_FROM           438  '438'

 L. 305       452  LOAD_FAST                'rpos'
              454  STORE_FAST               'pos'
            456_0  COME_FROM           448  '448'
            456_1  COME_FROM           428  '428'
            456_2  COME_FROM           408  '408'

 L. 306       456  LOAD_FAST                'pos'
              458  LOAD_CONST               -1
              460  COMPARE_OP               ==
          462_464  POP_JUMP_IF_FALSE   510  'to 510'

 L. 308       466  LOAD_FAST                'self'
              468  DUP_TOP          
              470  LOAD_ATTR                _pos
              472  LOAD_GLOBAL              len
              474  LOAD_FAST                'line'
              476  CALL_FUNCTION_1       1  '1 positional argument'
              478  INPLACE_ADD      
              480  ROT_TWO          
              482  STORE_ATTR               _pos

 L. 309       484  LOAD_FAST                'self'
              486  LOAD_ATTR                _flags
              488  LOAD_FAST                'self'
              490  LOAD_ATTR                FLAG_BINARY
              492  BINARY_AND       
          494_496  POP_JUMP_IF_FALSE   502  'to 502'
              498  LOAD_FAST                'line'
              500  RETURN_VALUE     
            502_0  COME_FROM           494  '494'
              502  LOAD_GLOBAL              u
              504  LOAD_FAST                'line'
              506  CALL_FUNCTION_1       1  '1 positional argument'
              508  RETURN_VALUE     
            510_0  COME_FROM           462  '462'

 L. 310       510  LOAD_FAST                'pos'
              512  LOAD_CONST               1
              514  BINARY_ADD       
              516  STORE_FAST               'xpos'

 L. 312       518  LOAD_FAST                'line'
              520  LOAD_FAST                'pos'
              522  BINARY_SUBSCR    
              524  LOAD_GLOBAL              cr_byte_value
              526  COMPARE_OP               ==
          528_530  POP_JUMP_IF_FALSE   568  'to 568'

 L. 313       532  LOAD_FAST                'xpos'
              534  LOAD_GLOBAL              len
              536  LOAD_FAST                'line'
              538  CALL_FUNCTION_1       1  '1 positional argument'
              540  COMPARE_OP               <
          542_544  POP_JUMP_IF_FALSE   568  'to 568'

 L. 314       546  LOAD_FAST                'line'
              548  LOAD_FAST                'xpos'
              550  BINARY_SUBSCR    
              552  LOAD_GLOBAL              linefeed_byte_value
              554  COMPARE_OP               ==
          556_558  POP_JUMP_IF_FALSE   568  'to 568'

 L. 316       560  LOAD_FAST                'xpos'
              562  LOAD_CONST               1
              564  INPLACE_ADD      
              566  STORE_FAST               'xpos'
            568_0  COME_FROM           556  '556'
            568_1  COME_FROM           542  '542'
            568_2  COME_FROM           528  '528'

 L. 320       568  LOAD_FAST                'truncated'
          570_572  POP_JUMP_IF_FALSE   596  'to 596'

 L. 321       574  LOAD_FAST                'line'
              576  LOAD_FAST                'xpos'
              578  LOAD_CONST               None
              580  BUILD_SLICE_2         2 
              582  BINARY_SUBSCR    
              584  LOAD_FAST                'self'
              586  LOAD_ATTR                _rbuffer
              588  BINARY_ADD       
              590  LOAD_FAST                'self'
              592  STORE_ATTR               _rbuffer
              594  JUMP_FORWARD        610  'to 610'
            596_0  COME_FROM           570  '570'

 L. 323       596  LOAD_FAST                'line'
              598  LOAD_FAST                'xpos'
              600  LOAD_CONST               None
              602  BUILD_SLICE_2         2 
              604  BINARY_SUBSCR    
              606  LOAD_FAST                'self'
              608  STORE_ATTR               _rbuffer
            610_0  COME_FROM           594  '594'

 L. 325       610  LOAD_FAST                'line'
              612  LOAD_FAST                'pos'
              614  LOAD_FAST                'xpos'
              616  BUILD_SLICE_2         2 
              618  BINARY_SUBSCR    
              620  STORE_FAST               'lf'

 L. 326       622  LOAD_FAST                'line'
              624  LOAD_CONST               None
              626  LOAD_FAST                'pos'
              628  BUILD_SLICE_2         2 
              630  BINARY_SUBSCR    
              632  LOAD_GLOBAL              linefeed_byte
              634  BINARY_ADD       
              636  STORE_FAST               'line'

 L. 327       638  LOAD_GLOBAL              len
              640  LOAD_FAST                'self'
              642  LOAD_ATTR                _rbuffer
              644  CALL_FUNCTION_1       1  '1 positional argument'
              646  LOAD_CONST               0
              648  COMPARE_OP               ==
          650_652  POP_JUMP_IF_FALSE   672  'to 672'
              654  LOAD_FAST                'lf'
              656  LOAD_GLOBAL              cr_byte
              658  COMPARE_OP               ==
          660_662  POP_JUMP_IF_FALSE   672  'to 672'

 L. 330       664  LOAD_CONST               True
              666  LOAD_FAST                'self'
              668  STORE_ATTR               _at_trailing_cr
              670  JUMP_FORWARD        682  'to 682'
            672_0  COME_FROM           660  '660'
            672_1  COME_FROM           650  '650'

 L. 332       672  LOAD_FAST                'self'
              674  LOAD_METHOD              _record_newline
              676  LOAD_FAST                'lf'
              678  CALL_METHOD_1         1  '1 positional argument'
              680  POP_TOP          
            682_0  COME_FROM           670  '670'

 L. 333       682  LOAD_FAST                'self'
              684  DUP_TOP          
              686  LOAD_ATTR                _pos
              688  LOAD_GLOBAL              len
              690  LOAD_FAST                'line'
              692  CALL_FUNCTION_1       1  '1 positional argument'
              694  INPLACE_ADD      
              696  ROT_TWO          
              698  STORE_ATTR               _pos

 L. 334       700  LOAD_FAST                'self'
              702  LOAD_ATTR                _flags
              704  LOAD_FAST                'self'
              706  LOAD_ATTR                FLAG_BINARY
              708  BINARY_AND       
          710_712  POP_JUMP_IF_FALSE   718  'to 718'
              714  LOAD_FAST                'line'
              716  RETURN_VALUE     
            718_0  COME_FROM           710  '710'
              718  LOAD_GLOBAL              u
              720  LOAD_FAST                'line'
              722  CALL_FUNCTION_1       1  '1 positional argument'
              724  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_GLOBAL' instruction at offset 210

    def readlines(self, sizehint=None):
        """
        Read all remaining lines using `readline` and return them as a list.
        If the optional ``sizehint`` argument is present, instead of reading up
        to EOF, whole lines totalling approximately sizehint bytes (possibly
        after rounding up to an internal buffer size) are read.

        :param int sizehint: desired maximum number of bytes to read.
        :returns: list of lines read from the file.
        """
        lines = []
        byte_count = 0
        while 1:
            line = self.readline()
            if len(line) == 0:
                break
            else:
                lines.append(line)
                byte_count += len(line)
            if sizehint is not None:
                if byte_count >= sizehint:
                    break

        return lines

    def seek(self, offset, whence=0):
        """
        Set the file's current position, like stdio's ``fseek``.  Not all file
        objects support seeking.

        .. note::
            If a file is opened in append mode (``'a'`` or ``'a+'``), any seek
            operations will be undone at the next write (as the file position
            will move back to the end of the file).

        :param int offset:
            position to move to within the file, relative to ``whence``.
        :param int whence:
            type of movement: 0 = absolute; 1 = relative to the current
            position; 2 = relative to the end of the file.

        :raises: ``IOError`` -- if the file doesn't support random access.
        """
        raise IOError('File does not support seeking.')

    def tell(self):
        """
        Return the file's current position.  This may not be accurate or
        useful if the underlying file doesn't support random access, or was
        opened in append mode.

        :returns: file position (`number <int>` of bytes).
        """
        return self._pos

    def write(self, data):
        """
        Write data to the file.  If write buffering is on (``bufsize`` was
        specified and non-zero), some or all of the data may not actually be
        written yet.  (Use `flush` or `close` to force buffered data to be
        written out.)

        :param data: ``str``/``bytes`` data to write
        """
        if isinstance(data, text_type):
            data = data.encode('utf-8')
        if self._closed:
            raise IOError('File is closed')
        if not self._flags & self.FLAG_WRITE:
            raise IOError('File not open for writing')
        if not self._flags & self.FLAG_BUFFERED:
            self._write_all(data)
            return
        self._wbuffer.write(data)
        if self._flags & self.FLAG_LINE_BUFFERED:
            last_newline_pos = data.rfind(linefeed_byte)
            if last_newline_pos >= 0:
                wbuf = self._wbuffer.getvalue()
                last_newline_pos += len(wbuf) - len(data)
                self._write_all(wbuf[:last_newline_pos + 1])
                self._wbuffer = BytesIO()
                self._wbuffer.write(wbuf[last_newline_pos + 1:])
            return
        if self._wbuffer.tell() >= self._bufsize:
            self.flush()

    def writelines(self, sequence):
        """
        Write a sequence of strings to the file.  The sequence can be any
        iterable object producing strings, typically a list of strings.  (The
        name is intended to match `readlines`; `writelines` does not add line
        separators.)

        :param sequence: an iterable sequence of strings.
        """
        for line in sequence:
            self.write(line)

    def xreadlines(self):
        """
        Identical to ``iter(f)``.  This is a deprecated file interface that
        predates Python iterator support.
        """
        return self

    @property
    def closed(self):
        return self._closed

    def _read(self, size):
        """
        (subclass override)
        Read data from the stream.  Return ``None`` or raise ``EOFError`` to
        indicate EOF.
        """
        raise EOFError()

    def _write(self, data):
        """
        (subclass override)
        Write data into the stream.
        """
        raise IOError('write not implemented')

    def _get_size(self):
        """
        (subclass override)
        Return the size of the file.  This is called from within `_set_mode`
        if the file is opened in append mode, so the file position can be
        tracked and `seek` and `tell` will work correctly.  If the file is
        a stream that can't be randomly accessed, you don't need to override
        this method,
        """
        return 0

    def _set_mode(self, mode='r', bufsize=-1):
        """
        Subclasses call this method to initialize the BufferedFile.
        """
        self._bufsize = self._DEFAULT_BUFSIZE
        if bufsize < 0:
            bufsize = 0
        if bufsize == 1:
            self._flags |= self.FLAG_BUFFERED | self.FLAG_LINE_BUFFERED
        elif bufsize > 1:
            self._bufsize = bufsize
            self._flags |= self.FLAG_BUFFERED
            self._flags &= ~self.FLAG_LINE_BUFFERED
        elif bufsize == 0:
            self._flags &= ~(self.FLAG_BUFFERED | self.FLAG_LINE_BUFFERED)
        if 'r' in mode or ('+' in mode):
            self._flags |= self.FLAG_READ
        if 'w' in mode or ('+' in mode):
            self._flags |= self.FLAG_WRITE
        if 'a' in mode:
            self._flags |= self.FLAG_WRITE | self.FLAG_APPEND
            self._size = self._get_size()
            self._pos = self._realpos = self._size
        if 'b' in mode:
            self._flags |= self.FLAG_BINARY
        if 'U' in mode:
            self._flags |= self.FLAG_UNIVERSAL_NEWLINE
            self.newlines = None

    def _write_all(self, data):
        while len(data) > 0:
            count = self._write(data)
            data = data[count:]
            if self._flags & self.FLAG_APPEND:
                self._size += count
                self._pos = self._realpos = self._size
            else:
                self._pos += count
                self._realpos += count

    def _record_newline(self, newline):
        if not self._flags & self.FLAG_UNIVERSAL_NEWLINE:
            return
        if self.newlines is None:
            self.newlines = newline
        elif self.newlines != newline and isinstance(self.newlines, bytes_types):
            self.newlines = (self.newlines, newline)
        elif newline not in self.newlines:
            self.newlines += (newline,)