# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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

    def __init__--- This code section failed: ---

 L.  53         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              struct
                6  STORE_FAST               'struct'

 L.  54         8  LOAD_CONST               False
               10  LOAD_FAST                'self'
               12  STORE_ATTR               closed

 L.  55        14  LOAD_FAST                'align'
               16  LOAD_FAST                'self'
               18  STORE_ATTR               align

 L.  56        20  LOAD_FAST                'bigendian'
               22  POP_JUMP_IF_FALSE    30  'to 30'

 L.  57        24  LOAD_STR                 '>'
               26  STORE_FAST               'strflag'
               28  JUMP_FORWARD         34  'to 34'
             30_0  COME_FROM            22  '22'

 L.  59        30  LOAD_STR                 '<'
               32  STORE_FAST               'strflag'
             34_0  COME_FROM            28  '28'

 L.  60        34  LOAD_FAST                'file'
               36  LOAD_FAST                'self'
               38  STORE_ATTR               file

 L.  61        40  LOAD_FAST                'file'
               42  LOAD_METHOD              read
               44  LOAD_CONST               4
               46  CALL_METHOD_1         1  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               chunkname

 L.  62        52  LOAD_GLOBAL              len
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                chunkname
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_CONST               4
               62  COMPARE_OP               <
               64  POP_JUMP_IF_FALSE    70  'to 70'

 L.  63        66  LOAD_GLOBAL              EOFError
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            64  '64'

 L.  64        70  SETUP_FINALLY       104  'to 104'

 L.  65        72  LOAD_FAST                'struct'
               74  LOAD_METHOD              unpack_from
               76  LOAD_FAST                'strflag'
               78  LOAD_STR                 'L'
               80  BINARY_ADD       
               82  LOAD_FAST                'file'
               84  LOAD_METHOD              read
               86  LOAD_CONST               4
               88  CALL_METHOD_1         1  ''
               90  CALL_METHOD_2         2  ''
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  LOAD_FAST                'self'
               98  STORE_ATTR               chunksize
              100  POP_BLOCK        
              102  JUMP_FORWARD        130  'to 130'
            104_0  COME_FROM_FINALLY    70  '70'

 L.  66       104  DUP_TOP          
              106  LOAD_FAST                'struct'
              108  LOAD_ATTR                error
              110  <121>               128  ''
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L.  67       118  LOAD_GLOBAL              EOFError
              120  LOAD_CONST               None
              122  RAISE_VARARGS_2       2  'exception instance with __cause__'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
              128  <48>             
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           102  '102'

 L.  68       130  LOAD_FAST                'inclheader'
              132  POP_JUMP_IF_FALSE   146  'to 146'

 L.  69       134  LOAD_FAST                'self'
              136  LOAD_ATTR                chunksize
              138  LOAD_CONST               8
              140  BINARY_SUBTRACT  
              142  LOAD_FAST                'self'
              144  STORE_ATTR               chunksize
            146_0  COME_FROM           132  '132'

 L.  70       146  LOAD_CONST               0
              148  LOAD_FAST                'self'
              150  STORE_ATTR               size_read

 L.  71       152  SETUP_FINALLY       170  'to 170'

 L.  72       154  LOAD_FAST                'self'
              156  LOAD_ATTR                file
              158  LOAD_METHOD              tell
              160  CALL_METHOD_0         0  ''
              162  LOAD_FAST                'self'
              164  STORE_ATTR               offset
              166  POP_BLOCK        
              168  JUMP_FORWARD        198  'to 198'
            170_0  COME_FROM_FINALLY   152  '152'

 L.  73       170  DUP_TOP          
              172  LOAD_GLOBAL              AttributeError
              174  LOAD_GLOBAL              OSError
              176  BUILD_TUPLE_2         2 
              178  <121>               196  ''
              180  POP_TOP          
              182  POP_TOP          
              184  POP_TOP          

 L.  74       186  LOAD_CONST               False
              188  LOAD_FAST                'self'
              190  STORE_ATTR               seekable
              192  POP_EXCEPT       
              194  JUMP_FORWARD        204  'to 204'
              196  <48>             
            198_0  COME_FROM           168  '168'

 L.  76       198  LOAD_CONST               True
              200  LOAD_FAST                'self'
              202  STORE_ATTR               seekable
            204_0  COME_FROM           194  '194'

Parse error at or near `<121>' instruction at offset 110

    def getname(self):
        """Return the name (ID) of the current chunk."""
        return self.chunkname

    def getsize(self):
        """Return the size of the current chunk."""
        return self.chunksize

    def close--- This code section failed: ---

 L.  87         0  LOAD_FAST                'self'
                2  LOAD_ATTR                closed
                4  POP_JUMP_IF_TRUE     34  'to 34'

 L.  88         6  SETUP_FINALLY        26  'to 26'

 L.  89         8  LOAD_FAST                'self'
               10  LOAD_METHOD              skip
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          
               16  POP_BLOCK        

 L.  91        18  LOAD_CONST               True
               20  LOAD_FAST                'self'
               22  STORE_ATTR               closed
               24  JUMP_FORWARD         34  'to 34'
             26_0  COME_FROM_FINALLY     6  '6'
               26  LOAD_CONST               True
               28  LOAD_FAST                'self'
               30  STORE_ATTR               closed
               32  <48>             
             34_0  COME_FROM            24  '24'
             34_1  COME_FROM             4  '4'

Parse error at or near `LOAD_FAST' instruction at offset 20

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
        else:
            if not self.seekable:
                raise OSError('cannot seek')
            if whence == 1:
                pos = pos + self.size_read
            else:
                if whence == 2:
                    pos = pos + self.chunksize
        if pos < 0 or pos > self.chunksize:
            raise RuntimeError
        self.file.seek(self.offset + pos)0
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
        elif self.size_read >= self.chunksize:
            return b''
        else:
            if size < 0:
                size = self.chunksize - self.size_read
            if size > self.chunksize - self.size_read:
                size = self.chunksize - self.size_read
            data = self.file.readsize
            self.size_read = self.size_read + len(data)
            if self.size_read == self.chunksize and self.align and self.chunksize & 1:
                dummy = self.file.read1
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
               18  POP_JUMP_IF_FALSE   108  'to 108'

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
               94  <121>               106  ''
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 164       102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
              106  <48>             
            108_0  COME_FROM           150  '150'
            108_1  COME_FROM           104  '104'
            108_2  COME_FROM            18  '18'

 L. 165       108  LOAD_FAST                'self'
              110  LOAD_ATTR                size_read
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                chunksize
              116  COMPARE_OP               <
              118  POP_JUMP_IF_FALSE   158  'to 158'

 L. 166       120  LOAD_GLOBAL              min
              122  LOAD_CONST               8192
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                chunksize
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                size_read
              132  BINARY_SUBTRACT  
              134  CALL_FUNCTION_2       2  ''
              136  STORE_FAST               'n'

 L. 167       138  LOAD_FAST                'self'
              140  LOAD_METHOD              read
              142  LOAD_FAST                'n'
              144  CALL_METHOD_1         1  ''
              146  STORE_FAST               'dummy'

 L. 168       148  LOAD_FAST                'dummy'
              150  POP_JUMP_IF_TRUE    108  'to 108'

 L. 169       152  LOAD_GLOBAL              EOFError
              154  RAISE_VARARGS_1       1  'exception instance'
              156  JUMP_BACK           108  'to 108'
            158_0  COME_FROM           118  '118'

Parse error at or near `RETURN_VALUE' instruction at offset 88