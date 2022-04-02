# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: c:\users\ps\appdata\local\programs\python\python38-32\lib\site-packages\PyInstaller\loader\pyimod02_archive.py
# Compiled at: 1995-09-27 16:18:56
# Size of source mod 2**32: 12498 bytes
import marshal, struct, sys, zlib
if sys.version_info[0] == 2:
    import thread
else:
    import _thread as thread
CRYPT_BLOCK_SIZE = 16
PYZ_TYPE_MODULE = 0
PYZ_TYPE_PKG = 1
PYZ_TYPE_DATA = 2

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

    def local(self):
        """
        Return an instance of FilePos for the current thread. This is a crude
        # re-implementation of threading.local, which isn't a built-in module
        # and therefore isn't available.
        """
        ti = thread.get_ident()
        if ti not in self._filePos:
            self._filePos[ti] = FilePos()
        return self._filePos[ti]

    def __getattr__(self, name):
        """
        Make this class act like a file, by invoking most methods on its
        underlying file object.
        """
        file = self.local().file
        assert file
        return getattr(file, name)

    def __enter__(self):
        """
        Open file and seek to pos record from last close.
        """
        fp = self.local()
        assert not fp.file
        fp.file = open(*self.args, **self.kwargs)
        fp.file.seek(fp.pos)

    def __exit__(self, type, value, traceback):
        """
        Close file and record pos.
        """
        fp = self.local()
        assert fp.file
        fp.pos = fp.file.tell()
        fp.file.close()
        fp.file = None


class ArchiveReadError(RuntimeError):
    pass


class ArchiveReader(object):
    __doc__ = '\n    A base class for a repository of python code objects.\n    The extract method is used by imputil.ArchiveImporter\n    to get code objects by name (fully qualified name), so\n    an enduser "import a.b" would become\n      extract(\'a.__init__\')\n      extract(\'a.b\')\n    '
    MAGIC = b'PYL\x00'
    HDRLEN = 12
    TOCPOS = 8
    os = None
    _bincache = None

    def __init__(self, path=None, start=0):
        """
        Initialize an Archive. If path is omitted, it will be an empty Archive.
        """
        self.toc = None
        self.path = path
        self.start = start
        if sys.version_info[0] == 2:
            import imp
            self.pymagic = imp.get_magic()
        else:
            import _frozen_importlib
            self.pymagic = _frozen_importlib._bootstrap_external.MAGIC_NUMBER
        if path is not None:
            self.lib = ArchiveFile(self.path, 'rb')
            with self.lib:
                self.checkmagic()
                self.loadtoc()

    def loadtoc(self):
        """
        Overridable.
        Default: After magic comes an int (4 byte native) giving the
        position of the TOC within self.lib.
        Default: The TOC is a marshal-able string.
        """
        self.lib.seek(self.start + self.TOCPOS)
        offset, = struct.unpack('!i', self.lib.read(4))
        self.lib.seek(self.start + offset)
        self.toc = dict(marshal.loads(self.lib.read()))

    def is_package(self, name):
        ispkg, pos = self.toc.get(name, (0, None))
        if pos is None:
            return
        return bool(ispkg)

    def extract(self, name):
        """
        Get the object corresponding to name, or None.
        For use with imputil ArchiveImporter, object is a python code object.
        'name' is the name as specified in an 'import name'.
        'import a.b' will become:
        extract('a') (return None because 'a' is not a code object)
        extract('a.__init__') (return a code object)
        extract('a.b') (return a code object)
        Default implementation:
          self.toc is a dict
          self.toc[name] is pos
          self.lib has the code object marshal-ed at pos
        """
        ispkg, pos = self.toc.get(name, (0, None))
        if pos is None:
            return
        with self.lib:
            self.lib.seek(self.start + pos)
            obj = marshal.loads(self.lib.read())
        return (
         ispkg, obj)

    def contents(self):
        """
        Return a list of the contents
        Default implementation assumes self.toc is a dict like object.
        Not required by ArchiveImporter.
        """
        return list(self.toc.keys())

    def checkmagic(self):
        """
        Overridable.
        Check to see if the file object self.lib actually has a file
        we understand.
        """
        self.lib.seek(self.start)
        if self.lib.read(len(self.MAGIC)) != self.MAGIC:
            raise ArchiveReadError('%s is not a valid %s archive file' % (
             self.path, self.__class__.__name__))
        if self.lib.read(len(self.pymagic)) != self.pymagic:
            raise ArchiveReadError('%s has version mismatch to dll' % self.path)
        self.lib.read(4)


class Cipher(object):
    __doc__ = '\n    This class is used only to decrypt Python modules.\n    '

    def __init__(self):
        import pyimod00_crypto_key
        key = pyimod00_crypto_key.key
        if not type(key) is str:
            raise AssertionError
        elif len(key) > CRYPT_BLOCK_SIZE:
            self.key = key[0:CRYPT_BLOCK_SIZE]
        else:
            self.key = key.zfill(CRYPT_BLOCK_SIZE)
        assert len(self.key) == CRYPT_BLOCK_SIZE
        self._aes = self._import_aesmod()

    def _import_aesmod(self):
        """
        Tries to import the AES module from PyCrypto.

        PyCrypto 2.4 and 2.6 uses different name of the AES extension.
        """
        modname = 'Crypto.Cipher._AES'
        if sys.version_info[0] == 2:
            from pyimod03_importers import CExtensionImporter
            importer = CExtensionImporter()
            mod = importer.find_module(modname)
            if not mod:
                modname = 'Crypto.Cipher.AES'
                mod = importer.find_module(modname)
                if not mod:
                    raise ImportError(modname)
            mod = mod.load_module(modname)
        else:
            kwargs = dict(fromlist=['Crypto', 'Cipher'])
            try:
                mod = __import__(modname, **kwargs)
            except ImportError:
                modname = 'Crypto.Cipher.AES'
                mod = __import__(modname, **kwargs)
            else:
                if modname in sys.modules:
                    del sys.modules[modname]
                return mod

    def __create_cipher(self, iv):
        return self._aes.new(self.key, self._aes.MODE_CFB, iv)

    def decrypt(self, data):
        return self._Cipher__create_cipher(data[:CRYPT_BLOCK_SIZE]).decrypt(data[CRYPT_BLOCK_SIZE:])


class ZlibArchiveReader(ArchiveReader):
    __doc__ = '\n    ZlibArchive - an archive with compressed entries. Archive is read\n    from the executable created by PyInstaller.\n\n    This archive is used for bundling python modules inside the executable.\n\n    NOTE: The whole ZlibArchive (PYZ) is compressed so it is not necessary\n          to compress single modules with zlib.\n    '
    MAGIC = b'PYZ\x00'
    TOCPOS = 8
    HDRLEN = ArchiveReader.HDRLEN + 5

    def __init__--- This code section failed: ---

 L. 327         0  LOAD_FAST                'path'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 328         8  LOAD_CONST               0
               10  STORE_FAST               'offset'
               12  JUMP_FORWARD        130  'to 130'
             14_0  COME_FROM             6  '6'

 L. 329        14  LOAD_FAST                'offset'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE   130  'to 130'

 L. 330        22  LOAD_GLOBAL              range
               24  LOAD_GLOBAL              len
               26  LOAD_FAST                'path'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               1
               32  BINARY_SUBTRACT  
               34  LOAD_CONST               -1
               36  LOAD_CONST               -1
               38  CALL_FUNCTION_3       3  ''
               40  GET_ITER         
             42_0  COME_FROM            56  '56'
               42  FOR_ITER            126  'to 126'
               44  STORE_FAST               'i'

 L. 331        46  LOAD_FAST                'path'
               48  LOAD_FAST                'i'
               50  BINARY_SUBSCR    
               52  LOAD_STR                 '?'
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE    42  'to 42'

 L. 332        58  SETUP_FINALLY        84  'to 84'

 L. 333        60  LOAD_GLOBAL              int
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
               82  JUMP_FORWARD        108  'to 108'
             84_0  COME_FROM_FINALLY    58  '58'

 L. 334        84  DUP_TOP          
               86  LOAD_GLOBAL              ValueError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   106  'to 106'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L. 337        98  POP_EXCEPT       
              100  JUMP_BACK            42  'to 42'
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            90  '90'
              106  END_FINALLY      
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            82  '82'

 L. 338       108  LOAD_FAST                'path'
              110  LOAD_CONST               None
              112  LOAD_FAST                'i'
              114  BUILD_SLICE_2         2 
              116  BINARY_SUBSCR    
              118  STORE_FAST               'path'

 L. 339       120  POP_TOP          
              122  BREAK_LOOP          130  'to 130'
              124  JUMP_BACK            42  'to 42'

 L. 341       126  LOAD_CONST               0
              128  STORE_FAST               'offset'
            130_0  COME_FROM            20  '20'
            130_1  COME_FROM            12  '12'

 L. 343       130  LOAD_GLOBAL              super
              132  LOAD_GLOBAL              ZlibArchiveReader
              134  LOAD_FAST                'self'
              136  CALL_FUNCTION_2       2  ''
              138  LOAD_METHOD              __init__
              140  LOAD_FAST                'path'
              142  LOAD_FAST                'offset'
              144  CALL_METHOD_2         2  ''
              146  POP_TOP          

 L. 347       148  SETUP_FINALLY       170  'to 170'

 L. 348       150  LOAD_CONST               0
              152  LOAD_CONST               None
              154  IMPORT_NAME              pyimod00_crypto_key
              156  STORE_FAST               'pyimod00_crypto_key'

 L. 349       158  LOAD_GLOBAL              Cipher
              160  CALL_FUNCTION_0       0  ''
              162  LOAD_FAST                'self'
              164  STORE_ATTR               cipher
              166  POP_BLOCK        
              168  JUMP_FORWARD        196  'to 196'
            170_0  COME_FROM_FINALLY   148  '148'

 L. 350       170  DUP_TOP          
              172  LOAD_GLOBAL              ImportError
              174  COMPARE_OP               exception-match
              176  POP_JUMP_IF_FALSE   194  'to 194'
              178  POP_TOP          
              180  POP_TOP          
              182  POP_TOP          

 L. 351       184  LOAD_CONST               None
              186  LOAD_FAST                'self'
              188  STORE_ATTR               cipher
              190  POP_EXCEPT       
              192  JUMP_FORWARD        196  'to 196'
            194_0  COME_FROM           176  '176'
              194  END_FINALLY      
            196_0  COME_FROM           192  '192'
            196_1  COME_FROM           168  '168'

Parse error at or near `POP_EXCEPT' instruction at offset 102

    def is_package(self, name):
        typ, pos, length = self.toc.get(name, (0, None, 0))
        if pos is None:
            return
        return typ == PYZ_TYPE_PKG

    def extract(self, name):
        typ, pos, length = self.toc.get(name, (0, None, 0))
        if pos is None:
            return
        with self.lib:
            self.lib.seek(self.start + pos)
            obj = self.lib.read(length)
        try:
            if self.cipher:
                obj = self.cipher.decrypt(obj)
            obj = zlib.decompress(obj)
            if typ in (PYZ_TYPE_MODULE, PYZ_TYPE_PKG):
                obj = marshal.loads(obj)
        except EOFError:
            raise ImportError("PYZ entry '%s' failed to unmarshal" % name)
        else:
            return (
             typ, obj)