# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PyInstaller\loader\pyimod02_archive.py
# Compiled at: 1995-09-27 16:18:56
# Size of source mod 2**32: 11427 bytes
import marshal, struct, sys, zlib, _thread as thread
CRYPT_BLOCK_SIZE = 16
PYZ_TYPE_MODULE = 0
PYZ_TYPE_PKG = 1
PYZ_TYPE_DATA = 2
PYZ_TYPE_NSPKG = 3

class FilePos(object):
    __doc__ = '\n    This class keeps track of the file object representing and current position\n    in a file.\n    '

    def __init__(self):
        self.file = None
        self.pos = 0


class ArchiveFile(object):
    __doc__ = '\n    File class support auto open when access member from file object\n    This class is use to avoid file locking on windows\n    '

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._filePos = {}

    def local--- This code section failed: ---

 L.  75         0  LOAD_GLOBAL              thread
                2  LOAD_METHOD              get_ident
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'ti'

 L.  76         8  LOAD_FAST                'ti'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _filePos
               14  <118>                 1  ''
               16  POP_JUMP_IF_FALSE    30  'to 30'

 L.  77        18  LOAD_GLOBAL              FilePos
               20  CALL_FUNCTION_0       0  ''
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _filePos
               26  LOAD_FAST                'ti'
               28  STORE_SUBSCR     
             30_0  COME_FROM            16  '16'

 L.  78        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _filePos
               34  LOAD_FAST                'ti'
               36  BINARY_SUBSCR    
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 14

    def __getattr__--- This code section failed: ---

 L.  85         0  LOAD_FAST                'self'
                2  LOAD_METHOD              local
                4  CALL_METHOD_0         0  ''
                6  LOAD_ATTR                file
                8  STORE_FAST               'file'

 L.  86        10  LOAD_FAST                'file'
               12  POP_JUMP_IF_TRUE     18  'to 18'
               14  <74>             
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM            12  '12'

 L.  87        18  LOAD_GLOBAL              getattr
               20  LOAD_FAST                'file'
               22  LOAD_FAST                'name'
               24  CALL_FUNCTION_2       2  ''
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 14

    def __enter__--- This code section failed: ---

 L.  94         0  LOAD_FAST                'self'
                2  LOAD_METHOD              local
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'fp'

 L.  95         8  LOAD_FAST                'fp'
               10  LOAD_ATTR                file
               12  POP_JUMP_IF_FALSE    18  'to 18'
               14  <74>             
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM            12  '12'

 L.  97        18  LOAD_GLOBAL              open
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                args
               24  BUILD_MAP_0           0 
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                kwargs
               30  <164>                 1  ''
               32  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               34  LOAD_FAST                'fp'
               36  STORE_ATTR               file

 L.  98        38  LOAD_FAST                'fp'
               40  LOAD_ATTR                file
               42  LOAD_METHOD              seek
               44  LOAD_FAST                'fp'
               46  LOAD_ATTR                pos
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

Parse error at or near `<74>' instruction at offset 14

    def __exit__--- This code section failed: ---

 L. 105         0  LOAD_FAST                'self'
                2  LOAD_METHOD              local
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'fp'

 L. 106         8  LOAD_FAST                'fp'
               10  LOAD_ATTR                file
               12  POP_JUMP_IF_TRUE     18  'to 18'
               14  <74>             
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM            12  '12'

 L. 109        18  LOAD_FAST                'fp'
               20  LOAD_ATTR                file
               22  LOAD_METHOD              tell
               24  CALL_METHOD_0         0  ''
               26  LOAD_FAST                'fp'
               28  STORE_ATTR               pos

 L. 110        30  LOAD_FAST                'fp'
               32  LOAD_ATTR                file
               34  LOAD_METHOD              close
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          

 L. 111        40  LOAD_CONST               None
               42  LOAD_FAST                'fp'
               44  STORE_ATTR               file

Parse error at or near `<74>' instruction at offset 14


class ArchiveReadError(RuntimeError):
    pass


class ArchiveReader(object):
    __doc__ = '\n    A base class for a repository of python code objects.\n    The extract method is used by imputil.ArchiveImporter\n    to get code objects by name (fully qualified name), so\n    an enduser "import a.b" would become\n      extract(\'a.__init__\')\n      extract(\'a.b\')\n    '
    MAGIC = b'PYL\x00'
    HDRLEN = 12
    TOCPOS = 8
    os = None
    _bincache = None

    def __init__--- This code section failed: ---

 L. 137         0  LOAD_CONST               None
                2  LOAD_FAST                'self'
                4  STORE_ATTR               toc

 L. 138         6  LOAD_FAST                'path'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               path

 L. 139        12  LOAD_FAST                'start'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               start

 L. 145        18  LOAD_CONST               0
               20  LOAD_CONST               None
               22  IMPORT_NAME              _frozen_importlib
               24  STORE_FAST               '_frozen_importlib'

 L. 146        26  LOAD_FAST                '_frozen_importlib'
               28  LOAD_ATTR                _bootstrap_external
               30  LOAD_ATTR                MAGIC_NUMBER
               32  LOAD_FAST                'self'
               34  STORE_ATTR               pymagic

 L. 148        36  LOAD_FAST                'path'
               38  LOAD_CONST               None
               40  <117>                 1  ''
               42  POP_JUMP_IF_FALSE   112  'to 112'

 L. 149        44  LOAD_GLOBAL              ArchiveFile
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                path
               50  LOAD_STR                 'rb'
               52  CALL_FUNCTION_2       2  ''
               54  LOAD_FAST                'self'
               56  STORE_ATTR               lib

 L. 150        58  LOAD_FAST                'self'
               60  LOAD_ATTR                lib
               62  SETUP_WITH           96  'to 96'
               64  POP_TOP          

 L. 151        66  LOAD_FAST                'self'
               68  LOAD_METHOD              checkmagic
               70  CALL_METHOD_0         0  ''
               72  POP_TOP          

 L. 152        74  LOAD_FAST                'self'
               76  LOAD_METHOD              loadtoc
               78  CALL_METHOD_0         0  ''
               80  POP_TOP          
               82  POP_BLOCK        
               84  LOAD_CONST               None
               86  DUP_TOP          
               88  DUP_TOP          
               90  CALL_FUNCTION_3       3  ''
               92  POP_TOP          
               94  JUMP_FORWARD        112  'to 112'
             96_0  COME_FROM_WITH       62  '62'
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
            112_1  COME_FROM            42  '42'

Parse error at or near `<117>' instruction at offset 40

    def loadtoc(self):
        """
        Overridable.
        Default: After magic comes an int (4 byte native) giving the
        position of the TOC within self.lib.
        Default: The TOC is a marshal-able string.
        """
        self.lib.seek(self.start + self.TOCPOS)
        offset, = struct.unpack('!i', self.lib.read4)
        self.lib.seek(self.start + offset)
        self.toc = dict(marshal.loadsself.lib.read)

    def is_package--- This code section failed: ---

 L. 176         0  LOAD_FAST                'self'
                2  LOAD_ATTR                toc
                4  LOAD_METHOD              get
                6  LOAD_FAST                'name'
                8  LOAD_CONST               (0, None)
               10  CALL_METHOD_2         2  ''
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'ispkg'
               16  STORE_FAST               'pos'

 L. 177        18  LOAD_FAST                'pos'
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 178        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L. 179        30  LOAD_GLOBAL              bool
               32  LOAD_FAST                'ispkg'
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 22

    def extract--- This code section failed: ---

 L. 196         0  LOAD_FAST                'self'
                2  LOAD_ATTR                toc
                4  LOAD_METHOD              get
                6  LOAD_FAST                'name'
                8  LOAD_CONST               (0, None)
               10  CALL_METHOD_2         2  ''
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'ispkg'
               16  STORE_FAST               'pos'

 L. 197        18  LOAD_FAST                'pos'
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 198        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L. 199        30  LOAD_FAST                'self'
               32  LOAD_ATTR                lib
               34  SETUP_WITH           86  'to 86'
               36  POP_TOP          

 L. 200        38  LOAD_FAST                'self'
               40  LOAD_ATTR                lib
               42  LOAD_METHOD              seek
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                start
               48  LOAD_FAST                'pos'
               50  BINARY_ADD       
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L. 202        56  LOAD_GLOBAL              marshal
               58  LOAD_METHOD              loads
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                lib
               64  LOAD_METHOD              read
               66  CALL_METHOD_0         0  ''
               68  CALL_METHOD_1         1  ''
               70  STORE_FAST               'obj'
               72  POP_BLOCK        
               74  LOAD_CONST               None
               76  DUP_TOP          
               78  DUP_TOP          
               80  CALL_FUNCTION_3       3  ''
               82  POP_TOP          
               84  JUMP_FORWARD        102  'to 102'
             86_0  COME_FROM_WITH       34  '34'
               86  <49>             
               88  POP_JUMP_IF_TRUE     92  'to 92'
               90  <48>             
             92_0  COME_FROM            88  '88'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          
               98  POP_EXCEPT       
              100  POP_TOP          
            102_0  COME_FROM            84  '84'

 L. 203       102  LOAD_FAST                'ispkg'
              104  LOAD_FAST                'obj'
              106  BUILD_TUPLE_2         2 
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 22

    def contents(self):
        """
        Return a list of the contents
        Default implementation assumes self.toc is a dict like object.
        Not required by ArchiveImporter.
        """
        return list(self.toc.keys)

    def checkmagic(self):
        """
        Overridable.
        Check to see if the file object self.lib actually has a file
        we understand.
        """
        self.lib.seekself.start
        if self.lib.readlen(self.MAGIC) != self.MAGIC:
            raise ArchiveReadError('%s is not a valid %s archive file' % (
             self.path, self.__class__.__name__))
        if self.lib.readlen(self.pymagic) != self.pymagic:
            raise ArchiveReadError('%s has version mismatch to dll' % self.path)
        self.lib.read4


class Cipher(object):
    __doc__ = '\n    This class is used only to decrypt Python modules.\n    '

    def __init__--- This code section failed: ---

 L. 243         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              pyimod00_crypto_key
                6  STORE_FAST               'pyimod00_crypto_key'

 L. 244         8  LOAD_FAST                'pyimod00_crypto_key'
               10  LOAD_ATTR                key
               12  STORE_FAST               'key'

 L. 246        14  LOAD_GLOBAL              type
               16  LOAD_FAST                'key'
               18  CALL_FUNCTION_1       1  ''
               20  LOAD_GLOBAL              str
               22  <117>                 0  ''
               24  POP_JUMP_IF_TRUE     30  'to 30'
               26  <74>             
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            24  '24'

 L. 247        30  LOAD_GLOBAL              len
               32  LOAD_FAST                'key'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_GLOBAL              CRYPT_BLOCK_SIZE
               38  COMPARE_OP               >
               40  POP_JUMP_IF_FALSE    58  'to 58'

 L. 248        42  LOAD_FAST                'key'
               44  LOAD_CONST               0
               46  LOAD_GLOBAL              CRYPT_BLOCK_SIZE
               48  BUILD_SLICE_2         2 
               50  BINARY_SUBSCR    
               52  LOAD_FAST                'self'
               54  STORE_ATTR               key
               56  JUMP_FORWARD         70  'to 70'
             58_0  COME_FROM            40  '40'

 L. 250        58  LOAD_FAST                'key'
               60  LOAD_METHOD              zfill
               62  LOAD_GLOBAL              CRYPT_BLOCK_SIZE
               64  CALL_METHOD_1         1  ''
               66  LOAD_FAST                'self'
               68  STORE_ATTR               key
             70_0  COME_FROM            56  '56'

 L. 251        70  LOAD_GLOBAL              len
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                key
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              CRYPT_BLOCK_SIZE
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_TRUE     88  'to 88'
               84  <74>             
               86  RAISE_VARARGS_1       1  'exception instance'
             88_0  COME_FROM            82  '82'

 L. 253        88  LOAD_CONST               0
               90  LOAD_CONST               None
               92  IMPORT_NAME              tinyaes
               94  STORE_FAST               'tinyaes'

 L. 254        96  LOAD_FAST                'tinyaes'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _aesmod

 L. 257       102  LOAD_GLOBAL              sys
              104  LOAD_ATTR                modules
              106  LOAD_STR                 'tinyaes'
              108  DELETE_SUBSCR    

Parse error at or near `<117>' instruction at offset 22

    def __create_cipher(self, iv):
        return self._aesmod.AES(self.key.encode, iv)

    def decrypt(self, data):
        cipher = self._Cipher__create_cipherdata[:CRYPT_BLOCK_SIZE]
        return cipher.CTR_xcrypt_bufferdata[CRYPT_BLOCK_SIZE:]


class ZlibArchiveReader(ArchiveReader):
    __doc__ = '\n    ZlibArchive - an archive with compressed entries. Archive is read\n    from the executable created by PyInstaller.\n\n    This archive is used for bundling python modules inside the executable.\n\n    NOTE: The whole ZlibArchive (PYZ) is compressed so it is not necessary\n          to compress single modules with zlib.\n    '
    MAGIC = b'PYZ\x00'
    TOCPOS = 8
    HDRLEN = ArchiveReader.HDRLEN + 5

    def __init__--- This code section failed: ---

 L. 284         0  LOAD_FAST                'path'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 285         8  LOAD_CONST               0
               10  STORE_FAST               'offset'
               12  JUMP_FORWARD        128  'to 128'
             14_0  COME_FROM             6  '6'

 L. 286        14  LOAD_FAST                'offset'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE   128  'to 128'

 L. 287        22  LOAD_GLOBAL              range
               24  LOAD_GLOBAL              len
               26  LOAD_FAST                'path'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               1
               32  BINARY_SUBTRACT  
               34  LOAD_CONST               -1
               36  LOAD_CONST               -1
               38  CALL_FUNCTION_3       3  ''
               40  GET_ITER         
             42_0  COME_FROM           122  '122'
             42_1  COME_FROM            98  '98'
             42_2  COME_FROM            56  '56'
               42  FOR_ITER            124  'to 124'
               44  STORE_FAST               'i'

 L. 288        46  LOAD_FAST                'path'
               48  LOAD_FAST                'i'
               50  BINARY_SUBSCR    
               52  LOAD_STR                 '?'
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE_BACK    42  'to 42'

 L. 289        58  SETUP_FINALLY        84  'to 84'

 L. 290        60  LOAD_GLOBAL              int
               62  LOAD_FAST                'path'
               64  LOAD_FAST                'i'
               66  LOAD_CONST               1
               68  BINARY_ADD       
               70  LOAD_CONST               None
               72  BUILD_SLICE_2         2 
               74  BINARY_SUBSCR    
               76  CALL_FUNCTION_1       1  ''
               78  STORE_FAST               'offset'
               80  POP_BLOCK        
               82  JUMP_FORWARD        106  'to 106'
             84_0  COME_FROM_FINALLY    58  '58'

 L. 291        84  DUP_TOP          
               86  LOAD_GLOBAL              ValueError
               88  <121>               104  ''
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 294        96  POP_EXCEPT       
               98  JUMP_BACK            42  'to 42'
              100  POP_EXCEPT       
              102  JUMP_FORWARD        106  'to 106'
              104  <48>             
            106_0  COME_FROM           102  '102'
            106_1  COME_FROM            82  '82'

 L. 295       106  LOAD_FAST                'path'
              108  LOAD_CONST               None
              110  LOAD_FAST                'i'
              112  BUILD_SLICE_2         2 
              114  BINARY_SUBSCR    
              116  STORE_FAST               'path'

 L. 296       118  POP_TOP          
              120  BREAK_LOOP          128  'to 128'
              122  JUMP_BACK            42  'to 42'
            124_0  COME_FROM            42  '42'

 L. 298       124  LOAD_CONST               0
              126  STORE_FAST               'offset'
            128_0  COME_FROM           120  '120'
            128_1  COME_FROM            20  '20'
            128_2  COME_FROM            12  '12'

 L. 300       128  LOAD_GLOBAL              super
              130  LOAD_GLOBAL              ZlibArchiveReader
              132  LOAD_FAST                'self'
              134  CALL_FUNCTION_2       2  ''
              136  LOAD_METHOD              __init__
              138  LOAD_FAST                'path'
              140  LOAD_FAST                'offset'
              142  CALL_METHOD_2         2  ''
              144  POP_TOP          

 L. 304       146  SETUP_FINALLY       168  'to 168'

 L. 305       148  LOAD_CONST               0
              150  LOAD_CONST               None
              152  IMPORT_NAME              pyimod00_crypto_key
              154  STORE_FAST               'pyimod00_crypto_key'

 L. 306       156  LOAD_GLOBAL              Cipher
              158  CALL_FUNCTION_0       0  ''
              160  LOAD_FAST                'self'
              162  STORE_ATTR               cipher
              164  POP_BLOCK        
              166  JUMP_FORWARD        192  'to 192'
            168_0  COME_FROM_FINALLY   146  '146'

 L. 307       168  DUP_TOP          
              170  LOAD_GLOBAL              ImportError
              172  <121>               190  ''
              174  POP_TOP          
              176  POP_TOP          
              178  POP_TOP          

 L. 308       180  LOAD_CONST               None
              182  LOAD_FAST                'self'
              184  STORE_ATTR               cipher
              186  POP_EXCEPT       
              188  JUMP_FORWARD        192  'to 192'
              190  <48>             
            192_0  COME_FROM           188  '188'
            192_1  COME_FROM           166  '166'

Parse error at or near `None' instruction at offset -1

    def is_package--- This code section failed: ---

 L. 311         0  LOAD_FAST                'self'
                2  LOAD_ATTR                toc
                4  LOAD_METHOD              get
                6  LOAD_FAST                'name'
                8  LOAD_CONST               (0, None, 0)
               10  CALL_METHOD_2         2  ''
               12  UNPACK_SEQUENCE_3     3 
               14  STORE_FAST               'typ'
               16  STORE_FAST               'pos'
               18  STORE_FAST               'length'

 L. 312        20  LOAD_FAST                'pos'
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 313        28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L. 314        32  LOAD_FAST                'typ'
               34  LOAD_GLOBAL              PYZ_TYPE_PKG
               36  LOAD_GLOBAL              PYZ_TYPE_NSPKG
               38  BUILD_TUPLE_2         2 
               40  <118>                 0  ''
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def is_pep420_namespace_package--- This code section failed: ---

 L. 317         0  LOAD_FAST                'self'
                2  LOAD_ATTR                toc
                4  LOAD_METHOD              get
                6  LOAD_FAST                'name'
                8  LOAD_CONST               (0, None, 0)
               10  CALL_METHOD_2         2  ''
               12  UNPACK_SEQUENCE_3     3 
               14  STORE_FAST               'typ'
               16  STORE_FAST               'pos'
               18  STORE_FAST               'length'

 L. 318        20  LOAD_FAST                'pos'
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 319        28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L. 320        32  LOAD_FAST                'typ'
               34  LOAD_GLOBAL              PYZ_TYPE_NSPKG
               36  COMPARE_OP               ==
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def extract--- This code section failed: ---

 L. 323         0  LOAD_FAST                'self'
                2  LOAD_ATTR                toc
                4  LOAD_METHOD              get
                6  LOAD_FAST                'name'
                8  LOAD_CONST               (0, None, 0)
               10  CALL_METHOD_2         2  ''
               12  UNPACK_SEQUENCE_3     3 
               14  STORE_FAST               'typ'
               16  STORE_FAST               'pos'
               18  STORE_FAST               'length'

 L. 324        20  LOAD_FAST                'pos'
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 325        28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L. 326        32  LOAD_FAST                'self'
               34  LOAD_ATTR                lib
               36  SETUP_WITH           84  'to 84'
               38  POP_TOP          

 L. 327        40  LOAD_FAST                'self'
               42  LOAD_ATTR                lib
               44  LOAD_METHOD              seek
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                start
               50  LOAD_FAST                'pos'
               52  BINARY_ADD       
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L. 328        58  LOAD_FAST                'self'
               60  LOAD_ATTR                lib
               62  LOAD_METHOD              read
               64  LOAD_FAST                'length'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'obj'
               70  POP_BLOCK        
               72  LOAD_CONST               None
               74  DUP_TOP          
               76  DUP_TOP          
               78  CALL_FUNCTION_3       3  ''
               80  POP_TOP          
               82  JUMP_FORWARD        100  'to 100'
             84_0  COME_FROM_WITH       36  '36'
               84  <49>             
               86  POP_JUMP_IF_TRUE     90  'to 90'
               88  <48>             
             90_0  COME_FROM            86  '86'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          
               96  POP_EXCEPT       
               98  POP_TOP          
            100_0  COME_FROM            82  '82'

 L. 329       100  SETUP_FINALLY       158  'to 158'

 L. 330       102  LOAD_FAST                'self'
              104  LOAD_ATTR                cipher
              106  POP_JUMP_IF_FALSE   120  'to 120'

 L. 331       108  LOAD_FAST                'self'
              110  LOAD_ATTR                cipher
              112  LOAD_METHOD              decrypt
              114  LOAD_FAST                'obj'
              116  CALL_METHOD_1         1  ''
              118  STORE_FAST               'obj'
            120_0  COME_FROM           106  '106'

 L. 332       120  LOAD_GLOBAL              zlib
              122  LOAD_METHOD              decompress
              124  LOAD_FAST                'obj'
              126  CALL_METHOD_1         1  ''
              128  STORE_FAST               'obj'

 L. 333       130  LOAD_FAST                'typ'
              132  LOAD_GLOBAL              PYZ_TYPE_MODULE
              134  LOAD_GLOBAL              PYZ_TYPE_PKG
              136  LOAD_GLOBAL              PYZ_TYPE_NSPKG
              138  BUILD_TUPLE_3         3 
              140  <118>                 0  ''
              142  POP_JUMP_IF_FALSE   154  'to 154'

 L. 334       144  LOAD_GLOBAL              marshal
              146  LOAD_METHOD              loads
              148  LOAD_FAST                'obj'
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'obj'
            154_0  COME_FROM           142  '142'
              154  POP_BLOCK        
              156  JUMP_FORWARD        208  'to 208'
            158_0  COME_FROM_FINALLY   100  '100'

 L. 335       158  DUP_TOP          
              160  LOAD_GLOBAL              EOFError
              162  <121>               206  ''
              164  POP_TOP          
              166  STORE_FAST               'e'
              168  POP_TOP          
              170  SETUP_FINALLY       198  'to 198'

 L. 336       172  LOAD_GLOBAL              ImportError
              174  LOAD_STR                 "PYZ entry '%s' failed to unmarshal"

 L. 337       176  LOAD_FAST                'name'

 L. 336       178  BINARY_MODULO    
              180  CALL_FUNCTION_1       1  ''

 L. 337       182  LOAD_FAST                'e'

 L. 336       184  RAISE_VARARGS_2       2  'exception instance with __cause__'
              186  POP_BLOCK        
              188  POP_EXCEPT       
              190  LOAD_CONST               None
              192  STORE_FAST               'e'
              194  DELETE_FAST              'e'
              196  JUMP_FORWARD        208  'to 208'
            198_0  COME_FROM_FINALLY   170  '170'
              198  LOAD_CONST               None
              200  STORE_FAST               'e'
              202  DELETE_FAST              'e'
              204  <48>             
              206  <48>             
            208_0  COME_FROM           196  '196'
            208_1  COME_FROM           156  '156'

 L. 338       208  LOAD_FAST                'typ'
              210  LOAD_FAST                'obj'
              212  BUILD_TUPLE_2         2 
              214  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24