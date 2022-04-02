# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\lib\_datasource.py
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
from __future__ import division, absolute_import, print_function
import os, sys, warnings, shutil, io
from contextlib import closing
from numpy.core.overrides import set_module
_open = open

def _check_mode(mode, encoding, newline):
    """Check mode and that encoding and newline are compatible.

    Parameters
    ----------
    mode : str
        File open mode.
    encoding : str
        File encoding.
    newline : str
        Newline for text files.

    """
    if 't' in mode:
        if 'b' in mode:
            raise ValueError('Invalid mode: %r' % (mode,))
    else:
        if encoding is not None:
            raise ValueError("Argument 'encoding' not supported in binary mode")
        if newline is not None:
            raise ValueError("Argument 'newline' not supported in binary mode")


def _python2_bz2open(fn, mode, encoding, newline):
    """Wrapper to open bz2 in text mode.

    Parameters
    ----------
    fn : str
        File name
    mode : {'r', 'w'}
        File mode. Note that bz2 Text files are not supported.
    encoding : str
        Ignored, text bz2 files not supported in Python2.
    newline : str
        Ignored, text bz2 files not supported in Python2.
    """
    import bz2
    _check_mode(mode, encoding, newline)
    if 't' in mode:
        warnings.warn('Assuming latin1 encoding for bz2 text file in Python2', RuntimeWarning,
          stacklevel=5)
        mode = mode.replace('t', '')
    return bz2.BZ2File(fn, mode)


def _python2_gzipopen(fn, mode, encoding, newline):
    """ Wrapper to open gzip in text mode.

    Parameters
    ----------
    fn : str, bytes, file
        File path or opened file.
    mode : str
        File mode. The actual files are opened as binary, but will decoded
        using the specified `encoding` and `newline`.
    encoding : str
        Encoding to be used when reading/writing as text.
    newline : str
        Newline to be used when reading/writing as text.

    """
    import gzip

    class GzipWrap(gzip.GzipFile):

        def read1(self, n):
            return self.read(n)

    _check_mode(mode, encoding, newline)
    gz_mode = mode.replace('t', '')
    if isinstance(fn, (str, bytes)):
        binary_file = GzipWrap(fn, gz_mode)
    elif hasattr(fn, 'read') or hasattr(fn, 'write'):
        binary_file = GzipWrap(None, gz_mode, fileobj=fn)
    else:
        raise TypeError('filename must be a str or bytes object, or a file')
    if 't' in mode:
        return io.TextIOWrapper(binary_file, encoding, newline=newline)
    return binary_file


class _FileOpeners(object):
    __doc__ = "\n    Container for different methods to open (un-)compressed files.\n\n    `_FileOpeners` contains a dictionary that holds one method for each\n    supported file format. Attribute lookup is implemented in such a way\n    that an instance of `_FileOpeners` itself can be indexed with the keys\n    of that dictionary. Currently uncompressed files as well as files\n    compressed with ``gzip``, ``bz2`` or ``xz`` compression are supported.\n\n    Notes\n    -----\n    `_file_openers`, an instance of `_FileOpeners`, is made available for\n    use in the `_datasource` module.\n\n    Examples\n    --------\n    >>> import gzip\n    >>> np.lib._datasource._file_openers.keys()\n    [None, '.bz2', '.gz', '.xz', '.lzma']\n    >>> np.lib._datasource._file_openers['.gz'] is gzip.open\n    True\n\n    "

    def __init__(self):
        self._loaded = False
        self._file_openers = {None: io.open}

    def _load(self):
        if self._loaded:
            return
        try:
            import bz2
            if sys.version_info[0] >= 3:
                self._file_openers['.bz2'] = bz2.open
            else:
                self._file_openers['.bz2'] = _python2_bz2open
        except ImportError:
            pass
        else:
            try:
                import gzip
                if sys.version_info[0] >= 3:
                    self._file_openers['.gz'] = gzip.open
                else:
                    self._file_openers['.gz'] = _python2_gzipopen
            except ImportError:
                pass
            else:
                try:
                    import lzma
                    self._file_openers['.xz'] = lzma.open
                    self._file_openers['.lzma'] = lzma.open
                except (ImportError, AttributeError):
                    pass
                else:
                    self._loaded = True

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
class DataSource(object):
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

    def _iszip(self, filename):
        """Test if the filename is a zip file by looking at the file extension.

        """
        fname, ext = os.path.splitext(filename)
        return ext in _file_openers.keys()

    def _iswritemode(self, mode):
        """Test if the given mode will open a file for writing."""
        _writemodes = ('w', '+')
        for c in mode:
            if c in _writemodes:
                return True
        else:
            return False

    def _splitzipext(self, filename):
        """Split zip extension from filename and return filename.

        *Returns*:
            base, zip_ext : {tuple}

        """
        if self._iszip(filename):
            return os.path.splitext(filename)
        return (
         filename, None)

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
        if sys.version_info[0] >= 3:
            from urllib.parse import urlparse
        else:
            from urlparse import urlparse
        scheme, netloc, upath, uparams, uquery, ufrag = urlparse(path)
        return bool(scheme and netloc)

    def _cache(self, path):
        """Cache the file specified by path.

        Creates a copy of the file in the datasource cache.

        """
        if sys.version_info[0] >= 3:
            from urllib.request import urlopen
            from urllib.error import URLError
        else:
            from urllib2 import urlopen
            from urllib2 import URLError
        upath = self.abspath(path)
        if not os.path.exists(os.path.dirname(upath)):
            os.makedirs(os.path.dirname(upath))
        if self._isurl(path):
            try:
                with closing(urlopen(path)) as openedurl:
                    with _open(upath, 'wb') as f:
                        shutil.copyfileobj(openedurl, f)
            except URLError:
                raise URLError('URL not found: %s' % path)

        else:
            shutil.copyfile(path, upath)
        return upath

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
                else:
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
        if sys.version_info[0] >= 3:
            from urllib.parse import urlparse
        else:
            from urlparse import urlparse
        splitpath = path.split(self._destpath, 2)
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
        while True:
            if path != last:
                last = path
                path = path.lstrip(os.sep).lstrip('/')
                path = path.lstrip(os.pardir).lstrip('..')
                drive, path = os.path.splitdrive(path)

        return path

    def exists--- This code section failed: ---

 L. 549         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              exists
                6  LOAD_FAST                'path'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 550        12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 554        16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                version_info
               20  LOAD_CONST               0
               22  BINARY_SUBSCR    
               24  LOAD_CONST               3
               26  COMPARE_OP               >=
               28  POP_JUMP_IF_FALSE    56  'to 56'

 L. 555        30  LOAD_CONST               0
               32  LOAD_CONST               ('urlopen',)
               34  IMPORT_NAME_ATTR         urllib.request
               36  IMPORT_FROM              urlopen
               38  STORE_FAST               'urlopen'
               40  POP_TOP          

 L. 556        42  LOAD_CONST               0
               44  LOAD_CONST               ('URLError',)
               46  IMPORT_NAME_ATTR         urllib.error
               48  IMPORT_FROM              URLError
               50  STORE_FAST               'URLError'
               52  POP_TOP          
               54  JUMP_FORWARD         80  'to 80'
             56_0  COME_FROM            28  '28'

 L. 558        56  LOAD_CONST               0
               58  LOAD_CONST               ('urlopen',)
               60  IMPORT_NAME              urllib2
               62  IMPORT_FROM              urlopen
               64  STORE_FAST               'urlopen'
               66  POP_TOP          

 L. 559        68  LOAD_CONST               0
               70  LOAD_CONST               ('URLError',)
               72  IMPORT_NAME              urllib2
               74  IMPORT_FROM              URLError
               76  STORE_FAST               'URLError'
               78  POP_TOP          
             80_0  COME_FROM            54  '54'

 L. 562        80  LOAD_FAST                'self'
               82  LOAD_METHOD              abspath
               84  LOAD_FAST                'path'
               86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'upath'

 L. 563        90  LOAD_GLOBAL              os
               92  LOAD_ATTR                path
               94  LOAD_METHOD              exists
               96  LOAD_FAST                'upath'
               98  CALL_METHOD_1         1  ''
              100  POP_JUMP_IF_FALSE   106  'to 106'

 L. 564       102  LOAD_CONST               True
              104  RETURN_VALUE     
            106_0  COME_FROM           100  '100'

 L. 567       106  LOAD_FAST                'self'
              108  LOAD_METHOD              _isurl
              110  LOAD_FAST                'path'
              112  CALL_METHOD_1         1  ''
              114  POP_JUMP_IF_FALSE   164  'to 164'

 L. 568       116  SETUP_FINALLY       142  'to 142'

 L. 569       118  LOAD_FAST                'urlopen'
              120  LOAD_FAST                'path'
              122  CALL_FUNCTION_1       1  ''
              124  STORE_FAST               'netfile'

 L. 570       126  LOAD_FAST                'netfile'
              128  LOAD_METHOD              close
              130  CALL_METHOD_0         0  ''
              132  POP_TOP          

 L. 571       134  DELETE_FAST              'netfile'

 L. 572       136  POP_BLOCK        
              138  LOAD_CONST               True
              140  RETURN_VALUE     
            142_0  COME_FROM_FINALLY   116  '116'

 L. 573       142  DUP_TOP          
              144  LOAD_FAST                'URLError'
              146  COMPARE_OP               exception-match
              148  POP_JUMP_IF_FALSE   162  'to 162'
              150  POP_TOP          
              152  POP_TOP          
              154  POP_TOP          

 L. 574       156  POP_EXCEPT       
              158  LOAD_CONST               False
              160  RETURN_VALUE     
            162_0  COME_FROM           148  '148'
              162  END_FINALLY      
            164_0  COME_FROM           114  '114'

 L. 575       164  LOAD_CONST               False
              166  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 142

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
                mode.replace('+', '')
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
        splitpath = path.split(self._baseurl, 2)
        if len(splitpath) == 1:
            result = os.path.join(self._baseurl, path)
        else:
            result = path
        return result

    def _findfile(self, path):
        """Extend DataSource method to prepend baseurl to ``path``."""
        return DataSource._findfile(self, self._fullpath(path))

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
        return DataSource.abspath(self, self._fullpath(path))

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
        return DataSource.exists(self, self._fullpath(path))

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