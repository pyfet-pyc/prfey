# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\lib\_datasource.py
"""A file interface for handling local and remote data files.

The goal of datasource is to abstract some of the file system operations
when dealing with data files so the researcher doesn't have to know all the
low-level details.  Through datasource, a researcher can obtain and use a
file with one function call, regardless of location of the file.

DataSource is meant to augment standard python libraries, not replace them.
It should work seamlessly with standard file IO operations and the os
module.

DataSource files can originate locally or remotely:

- local files : '/home/guido/src/local/data.txt'
- URLs (http, ftp, ...) : 'http://www.scipy.org/not/real/data.txt'

DataSource files can also be compressed or uncompressed.  Currently only
gzip, bz2 and xz are supported.

Example::

    >>> # Create a DataSource, use os.curdir (default) for local storage.
    >>> from numpy import DataSource
    >>> ds = DataSource()
    >>>
    >>> # Open a remote file.
    >>> # DataSource downloads the file, stores it locally in:
    >>> #     './www.google.com/index.html'
    >>> # opens the file and returns a file object.
    >>> fp = ds.open('http://www.google.com/') # doctest: +SKIP
    >>>
    >>> # Use the file as you normally would
    >>> fp.read() # doctest: +SKIP
    >>> fp.close() # doctest: +SKIP

"""
import os, shutil, io
from contextlib import closing
from numpy.core.overrides import set_module
_open = open

def _check_mode--- This code section failed: ---

 L.  61         0  LOAD_STR                 't'
                2  LOAD_FAST                'mode'
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    32  'to 32'

 L.  62         8  LOAD_STR                 'b'
               10  LOAD_FAST                'mode'
               12  <118>                 0  ''
               14  POP_JUMP_IF_FALSE    64  'to 64'

 L.  63        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'Invalid mode: %r'
               20  LOAD_FAST                'mode'
               22  BUILD_TUPLE_1         1 
               24  BINARY_MODULO    
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
               30  JUMP_FORWARD         64  'to 64'
             32_0  COME_FROM             6  '6'

 L.  65        32  LOAD_FAST                'encoding'
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L.  66        40  LOAD_GLOBAL              ValueError
               42  LOAD_STR                 "Argument 'encoding' not supported in binary mode"
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L.  67        48  LOAD_FAST                'newline'
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_FALSE    64  'to 64'

 L.  68        56  LOAD_GLOBAL              ValueError
               58  LOAD_STR                 "Argument 'newline' not supported in binary mode"
               60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            54  '54'
             64_1  COME_FROM            30  '30'
             64_2  COME_FROM            14  '14'

Parse error at or near `None' instruction at offset -1


class _FileOpeners:
    __doc__ = "\n    Container for different methods to open (un-)compressed files.\n\n    `_FileOpeners` contains a dictionary that holds one method for each\n    supported file format. Attribute lookup is implemented in such a way\n    that an instance of `_FileOpeners` itself can be indexed with the keys\n    of that dictionary. Currently uncompressed files as well as files\n    compressed with ``gzip``, ``bz2`` or ``xz`` compression are supported.\n\n    Notes\n    -----\n    `_file_openers`, an instance of `_FileOpeners`, is made available for\n    use in the `_datasource` module.\n\n    Examples\n    --------\n    >>> import gzip\n    >>> np.lib._datasource._file_openers.keys()\n    [None, '.bz2', '.gz', '.xz', '.lzma']\n    >>> np.lib._datasource._file_openers['.gz'] is gzip.open\n    True\n\n    "

    def __init__(self):
        self._loaded = False
        self._file_openers = {None: io.open}

    def _load--- This code section failed: ---

 L. 106         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _loaded
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 107         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 109        10  SETUP_FINALLY        36  'to 36'

 L. 110        12  LOAD_CONST               0
               14  LOAD_CONST               None
               16  IMPORT_NAME              bz2
               18  STORE_FAST               'bz2'

 L. 111        20  LOAD_FAST                'bz2'
               22  LOAD_ATTR                open
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _file_openers
               28  LOAD_STR                 '.bz2'
               30  STORE_SUBSCR     
               32  POP_BLOCK        
               34  JUMP_FORWARD         54  'to 54'
             36_0  COME_FROM_FINALLY    10  '10'

 L. 112        36  DUP_TOP          
               38  LOAD_GLOBAL              ImportError
               40  <121>                52  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 113        48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
               52  <48>             
             54_0  COME_FROM            50  '50'
             54_1  COME_FROM            34  '34'

 L. 115        54  SETUP_FINALLY        80  'to 80'

 L. 116        56  LOAD_CONST               0
               58  LOAD_CONST               None
               60  IMPORT_NAME              gzip
               62  STORE_FAST               'gzip'

 L. 117        64  LOAD_FAST                'gzip'
               66  LOAD_ATTR                open
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _file_openers
               72  LOAD_STR                 '.gz'
               74  STORE_SUBSCR     
               76  POP_BLOCK        
               78  JUMP_FORWARD         98  'to 98'
             80_0  COME_FROM_FINALLY    54  '54'

 L. 118        80  DUP_TOP          
               82  LOAD_GLOBAL              ImportError
               84  <121>                96  ''
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 119        92  POP_EXCEPT       
               94  JUMP_FORWARD         98  'to 98'
               96  <48>             
             98_0  COME_FROM            94  '94'
             98_1  COME_FROM            78  '78'

 L. 121        98  SETUP_FINALLY       136  'to 136'

 L. 122       100  LOAD_CONST               0
              102  LOAD_CONST               None
              104  IMPORT_NAME              lzma
              106  STORE_FAST               'lzma'

 L. 123       108  LOAD_FAST                'lzma'
              110  LOAD_ATTR                open
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                _file_openers
              116  LOAD_STR                 '.xz'
              118  STORE_SUBSCR     

 L. 124       120  LOAD_FAST                'lzma'
              122  LOAD_ATTR                open
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                _file_openers
              128  LOAD_STR                 '.lzma'
              130  STORE_SUBSCR     
              132  POP_BLOCK        
              134  JUMP_FORWARD        158  'to 158'
            136_0  COME_FROM_FINALLY    98  '98'

 L. 125       136  DUP_TOP          
              138  LOAD_GLOBAL              ImportError
              140  LOAD_GLOBAL              AttributeError
              142  BUILD_TUPLE_2         2 
              144  <121>               156  ''
              146  POP_TOP          
              148  POP_TOP          
              150  POP_TOP          

 L. 128       152  POP_EXCEPT       
              154  JUMP_FORWARD        158  'to 158'
              156  <48>             
            158_0  COME_FROM           154  '154'
            158_1  COME_FROM           134  '134'

 L. 130       158  LOAD_CONST               True
              160  LOAD_FAST                'self'
              162  STORE_ATTR               _loaded

Parse error at or near `<121>' instruction at offset 40

    def keys(self):
        """
        Return the keys of currently supported file openers.

        Parameters
        ----------
        None

        Returns
        -------
        keys : list
            The keys are None for uncompressed files and the file extension
            strings (i.e. ``'.gz'``, ``'.xz'``) for supported compression
            methods.

        """
        self._load()
        return list(self._file_openers.keys())

    def __getitem__(self, key):
        self._load()
        return self._file_openers[key]


_file_openers = _FileOpeners()

def open(path, mode='r', destpath=os.curdir, encoding=None, newline=None):
    """
    Open `path` with `mode` and return the file object.

    If ``path`` is an URL, it will be downloaded, stored in the
    `DataSource` `destpath` directory and opened from there.

    Parameters
    ----------
    path : str
        Local file path or URL to open.
    mode : str, optional
        Mode to open `path`. Mode 'r' for reading, 'w' for writing, 'a' to
        append. Available modes depend on the type of object specified by
        path.  Default is 'r'.
    destpath : str, optional
        Path to the directory where the source file gets downloaded to for
        use.  If `destpath` is None, a temporary directory will be created.
        The default path is the current directory.
    encoding : {None, str}, optional
        Open text file with given encoding. The default encoding will be
        what `io.open` uses.
    newline : {None, str}, optional
        Newline to use when reading text file.

    Returns
    -------
    out : file object
        The opened file.

    Notes
    -----
    This is a convenience function that instantiates a `DataSource` and
    returns the file object from ``DataSource.open(path)``.

    """
    ds = DataSource(destpath)
    return ds.open(path, mode, encoding=encoding, newline=newline)


@set_module('numpy')
class DataSource:
    __doc__ = "\n    DataSource(destpath='.')\n\n    A generic data source file (file, http, ftp, ...).\n\n    DataSources can be local files or remote files/URLs.  The files may\n    also be compressed or uncompressed. DataSource hides some of the\n    low-level details of downloading the file, allowing you to simply pass\n    in a valid file path (or URL) and obtain a file object.\n\n    Parameters\n    ----------\n    destpath : str or None, optional\n        Path to the directory where the source file gets downloaded to for\n        use.  If `destpath` is None, a temporary directory will be created.\n        The default path is the current directory.\n\n    Notes\n    -----\n    URLs require a scheme string (``http://``) to be used, without it they\n    will fail::\n\n        >>> repos = np.DataSource()\n        >>> repos.exists('www.google.com/index.html')\n        False\n        >>> repos.exists('http://www.google.com/index.html')\n        True\n\n    Temporary directories are deleted when the DataSource is deleted.\n\n    Examples\n    --------\n    ::\n\n        >>> ds = np.DataSource('/home/guido')\n        >>> urlname = 'http://www.google.com/'\n        >>> gfile = ds.open('http://www.google.com/')\n        >>> ds.abspath(urlname)\n        '/home/guido/www.google.com/index.html'\n\n        >>> ds = np.DataSource(None)  # use with temporary file\n        >>> ds.open('/home/guido/foobar.txt')\n        <open file '/home/guido.foobar.txt', mode 'r' at 0x91d4430>\n        >>> ds.abspath('/home/guido/foobar.txt')\n        '/tmp/.../home/guido/foobar.txt'\n\n    "

    def __init__(self, destpath=os.curdir):
        """Create a DataSource with a local path at destpath."""
        if destpath:
            self._destpath = os.path.abspath(destpath)
            self._istmpdest = False
        else:
            import tempfile
            self._destpath = tempfile.mkdtemp()
            self._istmpdest = True

    def __del__(self):
        if hasattr(self, '_istmpdest'):
            if self._istmpdest:
                shutil.rmtree(self._destpath)

    def _iszip--- This code section failed: ---

 L. 267         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              splitext
                6  LOAD_FAST                'filename'
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'fname'
               14  STORE_FAST               'ext'

 L. 268        16  LOAD_FAST                'ext'
               18  LOAD_GLOBAL              _file_openers
               20  LOAD_METHOD              keys
               22  CALL_METHOD_0         0  ''
               24  <118>                 0  ''
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 24

    def _iswritemode--- This code section failed: ---

 L. 274         0  LOAD_CONST               ('w', '+')
                2  STORE_FAST               '_writemodes'

 L. 275         4  LOAD_FAST                'mode'
                6  GET_ITER         
              8_0  COME_FROM            18  '18'
                8  FOR_ITER             28  'to 28'
               10  STORE_FAST               'c'

 L. 276        12  LOAD_FAST                'c'
               14  LOAD_FAST                '_writemodes'
               16  <118>                 0  ''
               18  POP_JUMP_IF_FALSE     8  'to 8'

 L. 277        20  POP_TOP          
               22  LOAD_CONST               True
               24  RETURN_VALUE     
               26  JUMP_BACK             8  'to 8'

 L. 278        28  LOAD_CONST               False
               30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 16

    def _splitzipext(self, filename):
        """Split zip extension from filename and return filename.

        *Returns*:
            base, zip_ext : {tuple}

        """
        if self._iszip(filename):
            return os.path.splitext(filename)
        return (filename, None)

    def _possible_names(self, filename):
        """Return a tuple containing compressed filename variations."""
        names = [
         filename]
        for zipext in self._iszip(filename) or _file_openers.keys():
            if zipext:
                names.append(filename + zipext)
            else:
                return names

    def _isurl(self, path):
        """Test if path is a net location.  Tests the scheme and netloc."""
        from urllib.parse import urlparse
        scheme, netloc, upath, uparams, uquery, ufrag = urlparse(path)
        return bool(scheme and netloc)

    def _cache--- This code section failed: ---

 L. 325         0  LOAD_CONST               0
                2  LOAD_CONST               ('urlopen',)
                4  IMPORT_NAME_ATTR         urllib.request
                6  IMPORT_FROM              urlopen
                8  STORE_FAST               'urlopen'
               10  POP_TOP          

 L. 326        12  LOAD_CONST               0
               14  LOAD_CONST               ('URLError',)
               16  IMPORT_NAME_ATTR         urllib.error
               18  IMPORT_FROM              URLError
               20  STORE_FAST               'URLError'
               22  POP_TOP          

 L. 328        24  LOAD_FAST                'self'
               26  LOAD_METHOD              abspath
               28  LOAD_FAST                'path'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'upath'

 L. 331        34  LOAD_GLOBAL              os
               36  LOAD_ATTR                path
               38  LOAD_METHOD              exists
               40  LOAD_GLOBAL              os
               42  LOAD_ATTR                path
               44  LOAD_METHOD              dirname
               46  LOAD_FAST                'upath'
               48  CALL_METHOD_1         1  ''
               50  CALL_METHOD_1         1  ''
               52  POP_JUMP_IF_TRUE     72  'to 72'

 L. 332        54  LOAD_GLOBAL              os
               56  LOAD_METHOD              makedirs
               58  LOAD_GLOBAL              os
               60  LOAD_ATTR                path
               62  LOAD_METHOD              dirname
               64  LOAD_FAST                'upath'
               66  CALL_METHOD_1         1  ''
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          
             72_0  COME_FROM            52  '52'

 L. 335        72  LOAD_FAST                'self'
               74  LOAD_METHOD              _isurl
               76  LOAD_FAST                'path'
               78  CALL_METHOD_1         1  ''
               80  POP_JUMP_IF_FALSE   218  'to 218'

 L. 336        82  SETUP_FINALLY       186  'to 186'

 L. 337        84  LOAD_GLOBAL              closing
               86  LOAD_FAST                'urlopen'
               88  LOAD_FAST                'path'
               90  CALL_FUNCTION_1       1  ''
               92  CALL_FUNCTION_1       1  ''
               94  SETUP_WITH          166  'to 166'
               96  STORE_FAST               'openedurl'

 L. 338        98  LOAD_GLOBAL              _open
              100  LOAD_FAST                'upath'
              102  LOAD_STR                 'wb'
              104  CALL_FUNCTION_2       2  ''
              106  SETUP_WITH          136  'to 136'
              108  STORE_FAST               'f'

 L. 339       110  LOAD_GLOBAL              shutil
              112  LOAD_METHOD              copyfileobj
              114  LOAD_FAST                'openedurl'
              116  LOAD_FAST                'f'
              118  CALL_METHOD_2         2  ''
              120  POP_TOP          
              122  POP_BLOCK        
              124  LOAD_CONST               None
              126  DUP_TOP          
              128  DUP_TOP          
              130  CALL_FUNCTION_3       3  ''
              132  POP_TOP          
              134  JUMP_FORWARD        152  'to 152'
            136_0  COME_FROM_WITH      106  '106'
              136  <49>             
              138  POP_JUMP_IF_TRUE    142  'to 142'
              140  <48>             
            142_0  COME_FROM           138  '138'
              142  POP_TOP          
              144  POP_TOP          
              146  POP_TOP          
              148  POP_EXCEPT       
              150  POP_TOP          
            152_0  COME_FROM           134  '134'
              152  POP_BLOCK        
              154  LOAD_CONST               None
              156  DUP_TOP          
              158  DUP_TOP          
              160  CALL_FUNCTION_3       3  ''
              162  POP_TOP          
              164  JUMP_FORWARD        182  'to 182'
            166_0  COME_FROM_WITH       94  '94'
              166  <49>             
              168  POP_JUMP_IF_TRUE    172  'to 172'
              170  <48>             
            172_0  COME_FROM           168  '168'
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          
              178  POP_EXCEPT       
              180  POP_TOP          
            182_0  COME_FROM           164  '164'
              182  POP_BLOCK        
              184  JUMP_ABSOLUTE       230  'to 230'
            186_0  COME_FROM_FINALLY    82  '82'

 L. 340       186  DUP_TOP          
              188  LOAD_FAST                'URLError'
              190  <121>               214  ''
              192  POP_TOP          
              194  POP_TOP          
              196  POP_TOP          

 L. 341       198  LOAD_FAST                'URLError'
              200  LOAD_STR                 'URL not found: %s'
              202  LOAD_FAST                'path'
              204  BINARY_MODULO    
              206  CALL_FUNCTION_1       1  ''
              208  RAISE_VARARGS_1       1  'exception instance'
              210  POP_EXCEPT       
              212  JUMP_ABSOLUTE       230  'to 230'
              214  <48>             
              216  JUMP_FORWARD        230  'to 230'
            218_0  COME_FROM            80  '80'

 L. 343       218  LOAD_GLOBAL              shutil
              220  LOAD_METHOD              copyfile
              222  LOAD_FAST                'path'
              224  LOAD_FAST                'upath'
              226  CALL_METHOD_2         2  ''
              228  POP_TOP          
            230_0  COME_FROM_EXCEPT_CLAUSE   216  '216'
            230_1  COME_FROM_EXCEPT_CLAUSE   212  '212'

 L. 344       230  LOAD_FAST                'upath'
              232  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 126

    def _findfile(self, path):
        """Searches for ``path`` and returns full path if found.

        If path is an URL, _findfile will cache a local copy and return the
        path to the cached file.  If path is a local file, _findfile will
        return a path to that local file.

        The search will include possible compressed versions of the file
        and return the first occurrence found.

        """
        if not self._isurl(path):
            filelist = self._possible_names(path)
            filelist += self._possible_names(self.abspath(path))
        else:
            filelist = self._possible_names(self.abspath(path))
            filelist = filelist + self._possible_names(path)
        for name in filelist:
            if self.exists(name):
                if self._isurl(name):
                    name = self._cache(name)
                return name

    def abspath(self, path):
        """
        Return absolute path of file in the DataSource directory.

        If `path` is an URL, then `abspath` will return either the location
        the file exists locally or the location it would exist when opened
        using the `open` method.

        Parameters
        ----------
        path : str
            Can be a local file or a remote URL.

        Returns
        -------
        out : str
            Complete path, including the `DataSource` destination directory.

        Notes
        -----
        The functionality is based on `os.path.abspath`.

        """
        from urllib.parse import urlparse
        splitpath = path.splitself._destpath2
        if len(splitpath) > 1:
            path = splitpath[1]
        scheme, netloc, upath, uparams, uquery, ufrag = urlparse(path)
        netloc = self._sanitize_relative_path(netloc)
        upath = self._sanitize_relative_path(upath)
        return os.path.join(self._destpath, netloc, upath)

    def _sanitize_relative_path(self, path):
        """Return a sanitised relative path for which
        os.path.abspath(os.path.join(base, path)).startswith(base)
        """
        last = None
        path = os.path.normpath(path)
        while path != last:
            last = path
            path = path.lstrip(os.sep).lstrip('/')
            path = path.lstrip(os.pardir).lstrip('..')
            drive, path = os.path.splitdrive(path)

        return path

    def exists--- This code section failed: ---

 L. 465         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              exists
                6  LOAD_FAST                'path'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 466        12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 470        16  LOAD_CONST               0
               18  LOAD_CONST               ('urlopen',)
               20  IMPORT_NAME_ATTR         urllib.request
               22  IMPORT_FROM              urlopen
               24  STORE_FAST               'urlopen'
               26  POP_TOP          

 L. 471        28  LOAD_CONST               0
               30  LOAD_CONST               ('URLError',)
               32  IMPORT_NAME_ATTR         urllib.error
               34  IMPORT_FROM              URLError
               36  STORE_FAST               'URLError'
               38  POP_TOP          

 L. 474        40  LOAD_FAST                'self'
               42  LOAD_METHOD              abspath
               44  LOAD_FAST                'path'
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               'upath'

 L. 475        50  LOAD_GLOBAL              os
               52  LOAD_ATTR                path
               54  LOAD_METHOD              exists
               56  LOAD_FAST                'upath'
               58  CALL_METHOD_1         1  ''
               60  POP_JUMP_IF_FALSE    66  'to 66'

 L. 476        62  LOAD_CONST               True
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'

 L. 479        66  LOAD_FAST                'self'
               68  LOAD_METHOD              _isurl
               70  LOAD_FAST                'path'
               72  CALL_METHOD_1         1  ''
               74  POP_JUMP_IF_FALSE   122  'to 122'

 L. 480        76  SETUP_FINALLY       102  'to 102'

 L. 481        78  LOAD_FAST                'urlopen'
               80  LOAD_FAST                'path'
               82  CALL_FUNCTION_1       1  ''
               84  STORE_FAST               'netfile'

 L. 482        86  LOAD_FAST                'netfile'
               88  LOAD_METHOD              close
               90  CALL_METHOD_0         0  ''
               92  POP_TOP          

 L. 483        94  DELETE_FAST              'netfile'

 L. 484        96  POP_BLOCK        
               98  LOAD_CONST               True
              100  RETURN_VALUE     
            102_0  COME_FROM_FINALLY    76  '76'

 L. 485       102  DUP_TOP          
              104  LOAD_FAST                'URLError'
              106  <121>               120  ''
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 486       114  POP_EXCEPT       
              116  LOAD_CONST               False
              118  RETURN_VALUE     
              120  <48>             
            122_0  COME_FROM            74  '74'

 L. 487       122  LOAD_CONST               False
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 100

    def open(self, path, mode='r', encoding=None, newline=None):
        """
        Open and return file-like object.

        If `path` is an URL, it will be downloaded, stored in the
        `DataSource` directory and opened from there.

        Parameters
        ----------
        path : str
            Local file path or URL to open.
        mode : {'r', 'w', 'a'}, optional
            Mode to open `path`.  Mode 'r' for reading, 'w' for writing,
            'a' to append. Available modes depend on the type of object
            specified by `path`. Default is 'r'.
        encoding : {None, str}, optional
            Open text file with given encoding. The default encoding will be
            what `io.open` uses.
        newline : {None, str}, optional
            Newline to use when reading text file.

        Returns
        -------
        out : file object
            File object.

        """
        if self._isurl(path):
            if self._iswritemode(mode):
                raise ValueError('URLs are not writeable')
        found = self._findfile(path)
        if found:
            _fname, ext = self._splitzipext(found)
            if ext == 'bz2':
                mode.replace'+'''
            return _file_openers[ext](found, mode=mode, encoding=encoding,
              newline=newline)
        raise IOError('%s not found.' % path)


class Repository(DataSource):
    __doc__ = "\n    Repository(baseurl, destpath='.')\n\n    A data repository where multiple DataSource's share a base\n    URL/directory.\n\n    `Repository` extends `DataSource` by prepending a base URL (or\n    directory) to all the files it handles. Use `Repository` when you will\n    be working with multiple files from one base URL.  Initialize\n    `Repository` with the base URL, then refer to each file by its filename\n    only.\n\n    Parameters\n    ----------\n    baseurl : str\n        Path to the local directory or remote location that contains the\n        data files.\n    destpath : str or None, optional\n        Path to the directory where the source file gets downloaded to for\n        use.  If `destpath` is None, a temporary directory will be created.\n        The default path is the current directory.\n\n    Examples\n    --------\n    To analyze all files in the repository, do something like this\n    (note: this is not self-contained code)::\n\n        >>> repos = np.lib._datasource.Repository('/home/user/data/dir/')\n        >>> for filename in filelist:\n        ...     fp = repos.open(filename)\n        ...     fp.analyze()\n        ...     fp.close()\n\n    Similarly you could use a URL for a repository::\n\n        >>> repos = np.lib._datasource.Repository('http://www.xyz.edu/data')\n\n    "

    def __init__(self, baseurl, destpath=os.curdir):
        """Create a Repository with a shared url or directory of baseurl."""
        DataSource.__init__(self, destpath=destpath)
        self._baseurl = baseurl

    def __del__(self):
        DataSource.__del__(self)

    def _fullpath(self, path):
        """Return complete path for path.  Prepends baseurl if necessary."""
        splitpath = path.splitself._baseurl2
        if len(splitpath) == 1:
            result = os.path.joinself._baseurlpath
        else:
            result = path
        return result

    def _findfile(self, path):
        """Extend DataSource method to prepend baseurl to ``path``."""
        return DataSource._findfileselfself._fullpath(path)

    def abspath(self, path):
        """
        Return absolute path of file in the Repository directory.

        If `path` is an URL, then `abspath` will return either the location
        the file exists locally or the location it would exist when opened
        using the `open` method.

        Parameters
        ----------
        path : str
            Can be a local file or a remote URL. This may, but does not
            have to, include the `baseurl` with which the `Repository` was
            initialized.

        Returns
        -------
        out : str
            Complete path, including the `DataSource` destination directory.

        """
        return DataSource.abspathselfself._fullpath(path)

    def exists(self, path):
        """
        Test if path exists prepending Repository base URL to path.

        Test if `path` exists as (and in this order):

        - a local file.
        - a remote URL that has been downloaded and stored locally in the
          `DataSource` directory.
        - a remote URL that has not been downloaded, but is valid and
          accessible.

        Parameters
        ----------
        path : str
            Can be a local file or a remote URL. This may, but does not
            have to, include the `baseurl` with which the `Repository` was
            initialized.

        Returns
        -------
        out : bool
            True if `path` exists.

        Notes
        -----
        When `path` is an URL, `exists` will return True if it's either
        stored locally in the `DataSource` directory, or is a valid remote
        URL.  `DataSource` does not discriminate between the two, the file
        is accessible if it exists in either location.

        """
        return DataSource.existsselfself._fullpath(path)

    def open(self, path, mode='r', encoding=None, newline=None):
        """
        Open and return file-like object prepending Repository base URL.

        If `path` is an URL, it will be downloaded, stored in the
        DataSource directory and opened from there.

        Parameters
        ----------
        path : str
            Local file path or URL to open. This may, but does not have to,
            include the `baseurl` with which the `Repository` was
            initialized.
        mode : {'r', 'w', 'a'}, optional
            Mode to open `path`.  Mode 'r' for reading, 'w' for writing,
            'a' to append. Available modes depend on the type of object
            specified by `path`. Default is 'r'.
        encoding : {None, str}, optional
            Open text file with given encoding. The default encoding will be
            what `io.open` uses.
        newline : {None, str}, optional
            Newline to use when reading text file.

        Returns
        -------
        out : file object
            File object.

        """
        return DataSource.open(self, (self._fullpath(path)), mode, encoding=encoding,
          newline=newline)

    def listdir(self):
        """
        List files in the source Repository.

        Returns
        -------
        files : list of str
            List of file names (not containing a directory part).

        Notes
        -----
        Does not currently work for remote repositories.

        """
        if self._isurl(self._baseurl):
            raise NotImplementedError('Directory listing of URLs, not supported yet.')
        else:
            return os.listdir(self._baseurl)