# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: zipp.py
import io, posixpath, zipfile, itertools, contextlib, sys, pathlib
if sys.version_info < (3, 7):
    from collections import OrderedDict
else:
    OrderedDict = dict

def _parents(path):
    """
    Given a path with elements separated by
    posixpath.sep, generate all parents of that path.

    >>> list(_parents('b/d'))
    ['b']
    >>> list(_parents('/b/d/'))
    ['/b']
    >>> list(_parents('b/d/f/'))
    ['b/d', 'b']
    >>> list(_parents('b'))
    []
    >>> list(_parents(''))
    []
    """
    return itertools.islice(_ancestry(path), 1, None)


def _ancestry(path):
    """
    Given a path with elements separated by
    posixpath.sep, generate all elements of that path

    >>> list(_ancestry('b/d'))
    ['b/d', 'b']
    >>> list(_ancestry('/b/d/'))
    ['/b/d', '/b']
    >>> list(_ancestry('b/d/f/'))
    ['b/d/f', 'b/d', 'b']
    >>> list(_ancestry('b'))
    ['b']
    >>> list(_ancestry(''))
    []
    """
    path = path.rstrip(posixpath.sep)
    while path:
        if path != posixpath.sep:
            yield path
            path, tail = posixpath.split(path)


_dedupe = OrderedDict.fromkeys

def _difference(minuend, subtrahend):
    """
    Return items in minuend not in subtrahend, retaining order
    with O(1) lookup.
    """
    return itertools.filterfalse(set(subtrahend).__contains__, minuend)


class CompleteDirs(zipfile.ZipFile):
    __doc__ = '\n    A ZipFile subclass that ensures that implied directories\n    are always included in the namelist.\n    '

    @staticmethod
    def _implied_dirs(names):
        parents = itertools.chain.from_iterable(map(_parents, names))
        as_dirs = (p + posixpath.sep for p in parents)
        return _dedupe(_difference(as_dirs, names))

    def namelist(self):
        names = super(CompleteDirs, self).namelist()
        return names + list(self._implied_dirs(names))

    def _name_set(self):
        return set(self.namelist())

    def resolve_dir--- This code section failed: ---

 L.  92         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _name_set
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'names'

 L.  93         8  LOAD_FAST                'name'
               10  LOAD_STR                 '/'
               12  BINARY_ADD       
               14  STORE_FAST               'dirname'

 L.  94        16  LOAD_FAST                'name'
               18  LOAD_FAST                'names'
               20  <118>                 1  ''
               22  JUMP_IF_FALSE_OR_POP    30  'to 30'
               24  LOAD_FAST                'dirname'
               26  LOAD_FAST                'names'
               28  <118>                 0  ''
             30_0  COME_FROM            22  '22'
               30  STORE_FAST               'dir_match'

 L.  95        32  LOAD_FAST                'dir_match'
               34  POP_JUMP_IF_FALSE    40  'to 40'
               36  LOAD_FAST                'dirname'
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'
               40  LOAD_FAST                'name'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 20

    @classmethod
    def make--- This code section failed: ---

 L. 103         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'source'
                4  LOAD_GLOBAL              CompleteDirs
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 104        10  LOAD_FAST                'source'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 106        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'source'
               18  LOAD_GLOBAL              zipfile
               20  LOAD_ATTR                ZipFile
               22  CALL_FUNCTION_2       2  ''
               24  POP_JUMP_IF_TRUE     38  'to 38'

 L. 107        26  LOAD_FAST                'cls'
               28  LOAD_GLOBAL              _pathlib_compat
               30  LOAD_FAST                'source'
               32  CALL_FUNCTION_1       1  ''
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
             38_0  COME_FROM            24  '24'

 L. 110        38  LOAD_STR                 'r'
               40  LOAD_FAST                'source'
               42  LOAD_ATTR                mode
               44  <118>                 1  ''
               46  POP_JUMP_IF_FALSE    52  'to 52'

 L. 111        48  LOAD_GLOBAL              CompleteDirs
               50  STORE_FAST               'cls'
             52_0  COME_FROM            46  '46'

 L. 113        52  LOAD_FAST                'cls'
               54  LOAD_FAST                'source'
               56  STORE_ATTR               __class__

 L. 114        58  LOAD_FAST                'source'
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 44


class FastLookup(CompleteDirs):
    __doc__ = '\n    ZipFile subclass to ensure implicit\n    dirs exist and are resolved rapidly.\n    '

    def namelist--- This code section failed: ---

 L. 124         0  LOAD_GLOBAL              contextlib
                2  LOAD_METHOD              suppress
                4  LOAD_GLOBAL              AttributeError
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           32  'to 32'
               10  POP_TOP          

 L. 125        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _FastLookup__names
               16  POP_BLOCK        
               18  ROT_TWO          
               20  LOAD_CONST               None
               22  DUP_TOP          
               24  DUP_TOP          
               26  CALL_FUNCTION_3       3  ''
               28  POP_TOP          
               30  RETURN_VALUE     
             32_0  COME_FROM_WITH        8  '8'
               32  <49>             
               34  POP_JUMP_IF_TRUE     38  'to 38'
               36  <48>             
             38_0  COME_FROM            34  '34'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          
               44  POP_EXCEPT       
               46  POP_TOP          

 L. 126        48  LOAD_GLOBAL              super
               50  LOAD_GLOBAL              FastLookup
               52  LOAD_FAST                'self'
               54  CALL_FUNCTION_2       2  ''
               56  LOAD_METHOD              namelist
               58  CALL_METHOD_0         0  ''
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _FastLookup__names

 L. 127        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _FastLookup__names
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 20

    def _name_set--- This code section failed: ---

 L. 130         0  LOAD_GLOBAL              contextlib
                2  LOAD_METHOD              suppress
                4  LOAD_GLOBAL              AttributeError
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           32  'to 32'
               10  POP_TOP          

 L. 131        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _FastLookup__lookup
               16  POP_BLOCK        
               18  ROT_TWO          
               20  LOAD_CONST               None
               22  DUP_TOP          
               24  DUP_TOP          
               26  CALL_FUNCTION_3       3  ''
               28  POP_TOP          
               30  RETURN_VALUE     
             32_0  COME_FROM_WITH        8  '8'
               32  <49>             
               34  POP_JUMP_IF_TRUE     38  'to 38'
               36  <48>             
             38_0  COME_FROM            34  '34'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          
               44  POP_EXCEPT       
               46  POP_TOP          

 L. 132        48  LOAD_GLOBAL              super
               50  LOAD_GLOBAL              FastLookup
               52  LOAD_FAST                'self'
               54  CALL_FUNCTION_2       2  ''
               56  LOAD_METHOD              _name_set
               58  CALL_METHOD_0         0  ''
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _FastLookup__lookup

 L. 133        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _FastLookup__lookup
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 20


def _pathlib_compat--- This code section failed: ---

 L. 141         0  SETUP_FINALLY        12  'to 12'

 L. 142         2  LOAD_FAST                'path'
                4  LOAD_METHOD              __fspath__
                6  CALL_METHOD_0         0  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 143        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  <121>                36  ''
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 144        24  LOAD_GLOBAL              str
               26  LOAD_FAST                'path'
               28  CALL_FUNCTION_1       1  ''
               30  ROT_FOUR         
               32  POP_EXCEPT       
               34  RETURN_VALUE     
               36  <48>             

Parse error at or near `<121>' instruction at offset 16


class Path:
    __doc__ = "\n    A pathlib-compatible interface for zip files.\n\n    Consider a zip file with this structure::\n\n        .\n        ├── a.txt\n        └── b\n            ├── c.txt\n            └── d\n                └── e.txt\n\n    >>> data = io.BytesIO()\n    >>> zf = zipfile.ZipFile(data, 'w')\n    >>> zf.writestr('a.txt', 'content of a')\n    >>> zf.writestr('b/c.txt', 'content of c')\n    >>> zf.writestr('b/d/e.txt', 'content of e')\n    >>> zf.filename = 'mem/abcde.zip'\n\n    Path accepts the zipfile object itself or a filename\n\n    >>> root = Path(zf)\n\n    From there, several path operations are available.\n\n    Directory iteration (including the zip file itself):\n\n    >>> a, b = root.iterdir()\n    >>> a\n    Path('mem/abcde.zip', 'a.txt')\n    >>> b\n    Path('mem/abcde.zip', 'b/')\n\n    name property:\n\n    >>> b.name\n    'b'\n\n    join with divide operator:\n\n    >>> c = b / 'c.txt'\n    >>> c\n    Path('mem/abcde.zip', 'b/c.txt')\n    >>> c.name\n    'c.txt'\n\n    Read text:\n\n    >>> c.read_text()\n    'content of c'\n\n    existence:\n\n    >>> c.exists()\n    True\n    >>> (b / 'missing.txt').exists()\n    False\n\n    Coercion to string:\n\n    >>> import os\n    >>> str(c).replace(os.sep, posixpath.sep)\n    'mem/abcde.zip/b/c.txt'\n\n    At the root, ``name``, ``filename``, and ``parent``\n    resolve to the zipfile. Note these attributes are not\n    valid and will raise a ``ValueError`` if the zipfile\n    has no filename.\n\n    >>> root.name\n    'abcde.zip'\n    >>> str(root.filename).replace(os.sep, posixpath.sep)\n    'mem/abcde.zip'\n    >>> str(root.parent)\n    'mem'\n    "
    _Path__repr = '{self.__class__.__name__}({self.root.filename!r}, {self.at!r})'

    def __init__(self, root, at=''):
        """
        Construct a Path from a ZipFile or filename.

        Note: When the source is an existing ZipFile object,
        its type (__class__) will be mutated to a
        specialized type. If the caller wishes to retain the
        original type, the caller should either create a
        separate ZipFile object or pass a filename.
        """
        self.root = FastLookup.make(root)
        self.at = at

    def open--- This code section failed: ---

 L. 246         0  LOAD_FAST                'self'
                2  LOAD_METHOD              is_dir
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 247         8  LOAD_GLOBAL              IsADirectoryError
               10  LOAD_FAST                'self'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 248        16  LOAD_FAST                'mode'
               18  LOAD_CONST               0
               20  BINARY_SUBSCR    
               22  STORE_FAST               'zip_mode'

 L. 249        24  LOAD_FAST                'self'
               26  LOAD_METHOD              exists
               28  CALL_METHOD_0         0  ''
               30  POP_JUMP_IF_TRUE     48  'to 48'
               32  LOAD_FAST                'zip_mode'
               34  LOAD_STR                 'r'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 250        40  LOAD_GLOBAL              FileNotFoundError
               42  LOAD_FAST                'self'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'
             48_1  COME_FROM            30  '30'

 L. 251        48  LOAD_FAST                'self'
               50  LOAD_ATTR                root
               52  LOAD_ATTR                open
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                at
               58  LOAD_FAST                'zip_mode'
               60  LOAD_FAST                'pwd'
               62  LOAD_CONST               ('pwd',)
               64  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               66  STORE_FAST               'stream'

 L. 252        68  LOAD_STR                 'b'
               70  LOAD_FAST                'mode'
               72  <118>                 0  ''
               74  POP_JUMP_IF_FALSE    96  'to 96'

 L. 253        76  LOAD_FAST                'args'
               78  POP_JUMP_IF_TRUE     84  'to 84'
               80  LOAD_FAST                'kwargs'
               82  POP_JUMP_IF_FALSE    92  'to 92'
             84_0  COME_FROM            78  '78'

 L. 254        84  LOAD_GLOBAL              ValueError
               86  LOAD_STR                 'encoding args invalid for binary operation'
               88  CALL_FUNCTION_1       1  ''
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            82  '82'

 L. 255        92  LOAD_FAST                'stream'
               94  RETURN_VALUE     
             96_0  COME_FROM            74  '74'

 L. 256        96  LOAD_GLOBAL              io
               98  LOAD_ATTR                TextIOWrapper
              100  LOAD_FAST                'stream'
              102  BUILD_LIST_1          1 
              104  LOAD_FAST                'args'
              106  CALL_FINALLY        109  'to 109'
              108  WITH_CLEANUP_FINISH
              110  BUILD_MAP_0           0 
              112  LOAD_FAST                'kwargs'
              114  <164>                 1  ''
              116  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 72

    @property
    def name(self):
        return pathlib.Path(self.at).name or self.filename.name

    @property
    def filename(self):
        return pathlib.Path(self.root.filename).joinpath(self.at)

    def read_text--- This code section failed: ---

 L. 267         0  LOAD_FAST                'self'
                2  LOAD_ATTR                open
                4  LOAD_STR                 'r'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  SETUP_WITH           48  'to 48'
               24  STORE_FAST               'strm'

 L. 268        26  LOAD_FAST                'strm'
               28  LOAD_METHOD              read
               30  CALL_METHOD_0         0  ''
               32  POP_BLOCK        
               34  ROT_TWO          
               36  LOAD_CONST               None
               38  DUP_TOP          
               40  DUP_TOP          
               42  CALL_FUNCTION_3       3  ''
               44  POP_TOP          
               46  RETURN_VALUE     
             48_0  COME_FROM_WITH       22  '22'
               48  <49>             
               50  POP_JUMP_IF_TRUE     54  'to 54'
               52  <48>             
             54_0  COME_FROM            50  '50'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          
               60  POP_EXCEPT       
               62  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def read_bytes--- This code section failed: ---

 L. 271         0  LOAD_FAST                'self'
                2  LOAD_METHOD              open
                4  LOAD_STR                 'rb'
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           34  'to 34'
               10  STORE_FAST               'strm'

 L. 272        12  LOAD_FAST                'strm'
               14  LOAD_METHOD              read
               16  CALL_METHOD_0         0  ''
               18  POP_BLOCK        
               20  ROT_TWO          
               22  LOAD_CONST               None
               24  DUP_TOP          
               26  DUP_TOP          
               28  CALL_FUNCTION_3       3  ''
               30  POP_TOP          
               32  RETURN_VALUE     
             34_0  COME_FROM_WITH        8  '8'
               34  <49>             
               36  POP_JUMP_IF_TRUE     40  'to 40'
               38  <48>             
             40_0  COME_FROM            36  '36'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          
               46  POP_EXCEPT       
               48  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 22

    def _is_child(self, path):
        return posixpath.dirname(path.at.rstrip('/')) == self.at.rstrip('/')

    def _next(self, at):
        return self.__class__(self.root, at)

    def is_dir(self):
        return not self.at or self.at.endswith('/')

    def is_file(self):
        return self.exists() and not self.is_dir()

    def exists--- This code section failed: ---

 L. 287         0  LOAD_FAST                'self'
                2  LOAD_ATTR                at
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                root
                8  LOAD_METHOD              _name_set
               10  CALL_METHOD_0         0  ''
               12  <118>                 0  ''
               14  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def iterdir(self):
        if not self.is_dir():
            raise ValueError("Can't listdir a file")
        subs = map(self._next, self.root.namelist())
        return filter(self._is_child, subs)

    def __str__(self):
        return posixpath.join(self.root.filename, self.at)

    def __repr__(self):
        return self._Path__repr.format(self=self)

    def joinpath--- This code section failed: ---

 L. 302         0  LOAD_GLOBAL              posixpath
                2  LOAD_ATTR                join
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                at
                8  BUILD_LIST_1          1 
               10  LOAD_GLOBAL              map
               12  LOAD_GLOBAL              _pathlib_compat
               14  LOAD_FAST                'other'
               16  CALL_FUNCTION_2       2  ''
               18  CALL_FINALLY         21  'to 21'
               20  WITH_CLEANUP_FINISH
               22  CALL_FUNCTION_EX      0  'positional arguments only'
               24  STORE_FAST               'next'

 L. 303        26  LOAD_FAST                'self'
               28  LOAD_METHOD              _next
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                root
               34  LOAD_METHOD              resolve_dir
               36  LOAD_FAST                'next'
               38  CALL_METHOD_1         1  ''
               40  CALL_METHOD_1         1  ''
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    __truediv__ = joinpath

    @property
    def parent(self):
        if not self.at:
            return self.filename.parent
        parent_at = posixpath.dirname(self.at.rstrip('/'))
        if parent_at:
            parent_at += '/'
        return self._next(parent_at)