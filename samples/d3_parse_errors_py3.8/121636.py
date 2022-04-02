# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: chunk.py
"""Simple class to read IFF chunks.

An IFF chunk (used in formats such as AIFF, TIFF, RMFF (RealMedia File
Format)) has the following structure:

+----------------+
| ID (4 bytes)   |
+----------------+
| size (4 bytes) |
+----------------+
| data           |
| ...            |
+----------------+

The ID is a 4-byte string which identifies the type of chunk.

The size field (a 32-bit value, encoded using big-endian byte order)
gives the size of the whole chunk, including the 8-byte header.

Usually an IFF-type file consists of one or more chunks.  The proposed
usage of the Chunk class defined here is to instantiate an instance at
the start of each chunk and read from the instance until it reaches
the end, after which a new instance can be instantiated.  At the end
of the file, creating a new instance will fail with an EOFError
exception.

Usage:
while True:
    try:
        chunk = Chunk(file)
    except EOFError:
        break
    chunktype = chunk.getname()
    while True:
        data = chunk.read(nbytes)
        if not data:
            pass
        # do something with data

The interface is file-like.  The implemented methods are:
read, close, seek, tell, isatty.
Extra methods are: skip() (called by close, skips to the end of the chunk),
getname() (returns the name (ID) of the chunk)

The __init__ method has one required argument, a file-like object
(including a chunk instance), and one optional argument, a flag which
specifies whether or not chunks are aligned on 2-byte boundaries.  The
default is 1, i.e. aligned.
"""

class Chunk:

    def __init__(self, file, align=True, bigendian=True, inclheader=False):
        import struct
        self.closed = False
        self.align = align
        if bigendian:
            strflag = '>'
        else:
            strflag = '<'
        self.file = file
        self.chunkname = file.read(4)
        if len(self.chunkname) < 4:
            raise EOFError
        try:
            self.chunksize = struct.unpack_from(strflag + 'L', file.read(4))[0]
        except struct.error:
            raise EOFError from None
        else:
            if inclheader:
                self.chunksize = self.chunksize - 8
            self.size_read = 0
            try:
                self.offset = self.file.tell()
            except (AttributeError, OSError):
                self.seekable = False
            else:
                self.seekable = True

    def getname(self):
        """Return the name (ID) of the current chunk."""
        return self.chunkname

    def getsize(self):
        """Return the size of the current chunk."""
        return self.chunksize

    def close(self):
        if not self.closed:
            try:
                self.skip()
            finally:
                self.closed = True

    def isatty(self):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        return False

    def seek(self, pos, whence=0):
        """Seek to specified position into the chunk.
        Default position is 0 (start of chunk).
        If the file is not seekable, this will result in an error.
        """
        if self.closed:
            raise ValueError('I/O operation on closed file')
        if not self.seekable:
            raise OSError('cannot seek')
        if whence == 1:
            pos = pos + self.size_read
        elif whence == 2:
            pos = pos + self.chunksize
        if pos < 0 or (pos > self.chunksize):
            raise RuntimeError
        self.file.seek(self.offset + pos, 0)
        self.size_read = pos

    def tell(self):
        if self.closed:
            raise ValueError('I/O operation on closed file')
        return self.size_read

    def read(self, size=-1):
        """Read at most size bytes from the chunk.
        If size is omitted or negative, read until the end
        of the chunk.
        """
        if self.closed:
            raise ValueError('I/O operation on closed file')
        if self.size_read >= self.chunksize:
            return b''
        if size < 0:
            size = self.chunksize - self.size_read
        if size > self.chunksize - self.size_read:
            size = self.chunksize - self.size_read
        data = self.file.read(size)
        self.size_read = self.size_read + len(data)
        if self.size_read == self.chunksize:
            if self.align:
                if self.chunksize & 1:
                    dummy = self.file.read(1)
                    self.size_read = self.size_read + len(dummy)
        return data

    def skip--- This code section failed: ---

 L. 152         0  LOAD_FAST                'self'
                2  LOAD_ATTR                closed
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L. 153         6  LOAD_GLOBAL              ValueError
                8  LOAD_STR                 'I/O operation on closed file'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 154        14  LOAD_FAST                'self'
               16  LOAD_ATTR                seekable
               18  POP_JUMP_IF_FALSE   110  'to 110'

 L. 155        20  SETUP_FINALLY        90  'to 90'

 L. 156        22  LOAD_FAST                'self'
               24  LOAD_ATTR                chunksize
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                size_read
               30  BINARY_SUBTRACT  
               32  STORE_FAST               'n'

 L. 158        34  LOAD_FAST                'self'
               36  LOAD_ATTR                align
               38  POP_JUMP_IF_FALSE    58  'to 58'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                chunksize
               44  LOAD_CONST               1
               46  BINARY_AND       
               48  POP_JUMP_IF_FALSE    58  'to 58'

 L. 159        50  LOAD_FAST                'n'
               52  LOAD_CONST               1
               54  BINARY_ADD       
               56  STORE_FAST               'n'
             58_0  COME_FROM            48  '48'
             58_1  COME_FROM            38  '38'

 L. 160        58  LOAD_FAST                'self'
               60  LOAD_ATTR                file
               62  LOAD_METHOD              seek
               64  LOAD_FAST                'n'
               66  LOAD_CONST               1
               68  CALL_METHOD_2         2  ''
               70  POP_TOP          

 L. 161        72  LOAD_FAST                'self'
               74  LOAD_ATTR                size_read
               76  LOAD_FAST                'n'
               78  BINARY_ADD       
               80  LOAD_FAST                'self'
               82  STORE_ATTR               size_read

 L. 162        84  POP_BLOCK        
               86  LOAD_CONST               None
               88  RETURN_VALUE     
             90_0  COME_FROM_FINALLY    20  '20'

 L. 163        90  DUP_TOP          
               92  LOAD_GLOBAL              OSError
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   108  'to 108'
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 164       104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            96  '96'
              108  END_FINALLY      
            110_0  COME_FROM           158  '158'
            110_1  COME_FROM           152  '152'
            110_2  COME_FROM           106  '106'
            110_3  COME_FROM            18  '18'

 L. 165       110  LOAD_FAST                'self'
              112  LOAD_ATTR                size_read
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                chunksize
              118  COMPARE_OP               <
              120  POP_JUMP_IF_FALSE   160  'to 160'

 L. 166       122  LOAD_GLOBAL              min
              124  LOAD_CONST               8192
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                chunksize
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                size_read
              134  BINARY_SUBTRACT  
              136  CALL_FUNCTION_2       2  ''
              138  STORE_FAST               'n'

 L. 167       140  LOAD_FAST                'self'
              142  LOAD_METHOD              read
              144  LOAD_FAST                'n'
              146  CALL_METHOD_1         1  ''
              148  STORE_FAST               'dummy'

 L. 168       150  LOAD_FAST                'dummy'
              152  POP_JUMP_IF_TRUE_BACK   110  'to 110'

 L. 169       154  LOAD_GLOBAL              EOFError
              156  RAISE_VARARGS_1       1  'exception instance'
              158  JUMP_BACK           110  'to 110'
            160_0  COME_FROM           120  '120'

Parse error at or near `DUP_TOP' instruction at offset 90