# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\lib\npyio.py
from __future__ import division, absolute_import, print_function
import sys, os, re, functools, itertools, warnings, weakref, contextlib
from operator import itemgetter, index as opindex
import numpy as np
from . import format
from ._datasource import DataSource
from numpy.core import overrides
from numpy.core.multiarray import packbits, unpackbits
from numpy.core.overrides import set_module
from numpy.core._internal import recursive
from ._iotools import LineSplitter, NameValidator, StringConverter, ConverterError, ConverterLockError, ConversionWarning, _is_string_like, has_nested_fields, flatten_dtype, easy_dtype, _decode_line
from numpy.compat import asbytes, asstr, asunicode, bytes, basestring, os_fspath, os_PathLike, pickle, contextlib_nullcontext
if sys.version_info[0] >= 3:
    from collections.abc import Mapping
else:
    from future_builtins import map
    from collections import Mapping

@set_module('numpy')
def loads(*args, **kwargs):
    warnings.warn('np.loads is deprecated, use pickle.loads instead',
      DeprecationWarning,
      stacklevel=2)
    return (pickle.loads)(*args, **kwargs)


__all__ = [
 'savetxt', 'loadtxt', 'genfromtxt', 'ndfromtxt', 'mafromtxt',
 'recfromtxt', 'recfromcsv', 'load', 'loads', 'save', 'savez',
 'savez_compressed', 'packbits', 'unpackbits', 'fromregex', 'DataSource']
array_function_dispatch = functools.partial((overrides.array_function_dispatch),
  module='numpy')

class BagObj(object):
    __doc__ = '\n    BagObj(obj)\n\n    Convert attribute look-ups to getitems on the object passed in.\n\n    Parameters\n    ----------\n    obj : class instance\n        Object on which attribute look-up is performed.\n\n    Examples\n    --------\n    >>> from numpy.lib.npyio import BagObj as BO\n    >>> class BagDemo(object):\n    ...     def __getitem__(self, key): # An instance of BagObj(BagDemo)\n    ...                                 # will call this method when any\n    ...                                 # attribute look-up is required\n    ...         result = "Doesn\'t matter what you want, "\n    ...         return result + "you\'re gonna get this"\n    ...\n    >>> demo_obj = BagDemo()\n    >>> bagobj = BO(demo_obj)\n    >>> bagobj.hello_there\n    "Doesn\'t matter what you want, you\'re gonna get this"\n    >>> bagobj.I_can_be_anything\n    "Doesn\'t matter what you want, you\'re gonna get this"\n\n    '

    def __init__(self, obj):
        self._obj = weakref.proxy(obj)

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, '_obj')[key]
        except KeyError:
            raise AttributeError(key)

    def __dir__(self):
        """
        Enables dir(bagobj) to list the files in an NpzFile.

        This also enables tab-completion in an interpreter or IPython.
        """
        return list(object.__getattribute__(self, '_obj').keys())


def zipfile_factory(file, *args, **kwargs):
    """
    Create a ZipFile.

    Allows for Zip64, and the `file` argument can accept file, str, or
    pathlib.Path objects. `args` and `kwargs` are passed to the zipfile.ZipFile
    constructor.
    """
    if not hasattr(file, 'read'):
        file = os_fspath(file)
    import zipfile
    kwargs['allowZip64'] = True
    return (zipfile.ZipFile)(file, *args, **kwargs)


class NpzFile(Mapping):
    __doc__ = "\n    NpzFile(fid)\n\n    A dictionary-like object with lazy-loading of files in the zipped\n    archive provided on construction.\n\n    `NpzFile` is used to load files in the NumPy ``.npz`` data archive\n    format. It assumes that files in the archive have a ``.npy`` extension,\n    other files are ignored.\n\n    The arrays and file strings are lazily loaded on either\n    getitem access using ``obj['key']`` or attribute lookup using\n    ``obj.f.key``. A list of all files (without ``.npy`` extensions) can\n    be obtained with ``obj.files`` and the ZipFile object itself using\n    ``obj.zip``.\n\n    Attributes\n    ----------\n    files : list of str\n        List of all files in the archive with a ``.npy`` extension.\n    zip : ZipFile instance\n        The ZipFile object initialized with the zipped archive.\n    f : BagObj instance\n        An object on which attribute can be performed as an alternative\n        to getitem access on the `NpzFile` instance itself.\n    allow_pickle : bool, optional\n        Allow loading pickled data. Default: False\n\n        .. versionchanged:: 1.16.3\n            Made default False in response to CVE-2019-6446.\n\n    pickle_kwargs : dict, optional\n        Additional keyword arguments to pass on to pickle.load.\n        These are only useful when loading object arrays saved on\n        Python 2 when using Python 3.\n\n    Parameters\n    ----------\n    fid : file or str\n        The zipped archive to open. This is either a file-like object\n        or a string containing the path to the archive.\n    own_fid : bool, optional\n        Whether NpzFile should close the file handle.\n        Requires that `fid` is a file-like object.\n\n    Examples\n    --------\n    >>> from tempfile import TemporaryFile\n    >>> outfile = TemporaryFile()\n    >>> x = np.arange(10)\n    >>> y = np.sin(x)\n    >>> np.savez(outfile, x=x, y=y)\n    >>> _ = outfile.seek(0)\n\n    >>> npz = np.load(outfile)\n    >>> isinstance(npz, np.lib.io.NpzFile)\n    True\n    >>> sorted(npz.files)\n    ['x', 'y']\n    >>> npz['x']  # getitem access\n    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])\n    >>> npz.f.x  # attribute lookup\n    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])\n\n    "

    def __init__(self, fid, own_fid=False, allow_pickle=False, pickle_kwargs=None):
        _zip = zipfile_factory(fid)
        self._files = _zip.namelist()
        self.files = []
        self.allow_pickle = allow_pickle
        self.pickle_kwargs = pickle_kwargs
        for x in self._files:
            if x.endswith('.npy'):
                self.files.append(x[:-4])
            else:
                self.files.append(x)
        else:
            self.zip = _zip
            self.f = BagObj(self)
            if own_fid:
                self.fid = fid
            else:
                self.fid = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """
        Close the file.

        """
        if self.zip is not None:
            self.zip.close()
            self.zip = None
        if self.fid is not None:
            self.fid.close()
            self.fid = None
        self.f = None

    def __del__(self):
        self.close()

    def __iter__(self):
        return iter(self.files)

    def __len__(self):
        return len(self.files)

    def __getitem__(self, key):
        member = False
        if key in self._files:
            member = True
        elif key in self.files:
            member = True
            key += '.npy'
        if member:
            bytes = self.zip.open(key)
            magic = bytes.read(len(format.MAGIC_PREFIX))
            bytes.close()
            if magic == format.MAGIC_PREFIX:
                bytes = self.zip.open(key)
                return format.read_array(bytes, allow_pickle=(self.allow_pickle),
                  pickle_kwargs=(self.pickle_kwargs))
            return self.zip.read(key)
        else:
            raise KeyError('%s is not a file in the archive' % key)

    if sys.version_info.major == 3:

        def iteritems(self):
            warnings.warn('NpzFile.iteritems is deprecated in python 3, to match the removal of dict.itertems. Use .items() instead.',
              DeprecationWarning,
              stacklevel=2)
            return self.items()

        def iterkeys(self):
            warnings.warn('NpzFile.iterkeys is deprecated in python 3, to match the removal of dict.iterkeys. Use .keys() instead.',
              DeprecationWarning,
              stacklevel=2)
            return self.keys()


@set_module('numpy')
def load--- This code section failed: ---

 L. 403         0  LOAD_FAST                'encoding'
                2  LOAD_CONST               ('ASCII', 'latin1', 'bytes')
                4  COMPARE_OP               not-in
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 415         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 "encoding must be 'ASCII', 'latin1', or 'bytes'"
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 417        16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                version_info
               20  LOAD_CONST               0
               22  BINARY_SUBSCR    
               24  LOAD_CONST               3
               26  COMPARE_OP               >=
               28  POP_JUMP_IF_FALSE    44  'to 44'

 L. 418        30  LOAD_GLOBAL              dict
               32  LOAD_FAST                'encoding'
               34  LOAD_FAST                'fix_imports'
               36  LOAD_CONST               ('encoding', 'fix_imports')
               38  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               40  STORE_FAST               'pickle_kwargs'
               42  JUMP_FORWARD         48  'to 48'
             44_0  COME_FROM            28  '28'

 L. 421        44  BUILD_MAP_0           0 
               46  STORE_FAST               'pickle_kwargs'
             48_0  COME_FROM            42  '42'

 L. 424        48  LOAD_GLOBAL              hasattr
               50  LOAD_FAST                'file'
               52  LOAD_STR                 'read'
               54  CALL_FUNCTION_2       2  ''
               56  POP_JUMP_IF_FALSE    68  'to 68'

 L. 425        58  LOAD_FAST                'file'
               60  STORE_FAST               'fid'

 L. 426        62  LOAD_CONST               False
               64  STORE_FAST               'own_fid'
               66  JUMP_FORWARD         86  'to 86'
             68_0  COME_FROM            56  '56'

 L. 428        68  LOAD_GLOBAL              open
               70  LOAD_GLOBAL              os_fspath
               72  LOAD_FAST                'file'
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_STR                 'rb'
               78  CALL_FUNCTION_2       2  ''
               80  STORE_FAST               'fid'

 L. 429        82  LOAD_CONST               True
               84  STORE_FAST               'own_fid'
             86_0  COME_FROM            66  '66'

 L. 431        86  SETUP_FINALLY       320  'to 320'

 L. 433        88  LOAD_CONST               b'PK\x03\x04'
               90  STORE_FAST               '_ZIP_PREFIX'

 L. 434        92  LOAD_CONST               b'PK\x05\x06'
               94  STORE_FAST               '_ZIP_SUFFIX'

 L. 435        96  LOAD_GLOBAL              len
               98  LOAD_GLOBAL              format
              100  LOAD_ATTR                MAGIC_PREFIX
              102  CALL_FUNCTION_1       1  ''
              104  STORE_FAST               'N'

 L. 436       106  LOAD_FAST                'fid'
              108  LOAD_METHOD              read
              110  LOAD_FAST                'N'
              112  CALL_METHOD_1         1  ''
              114  STORE_FAST               'magic'

 L. 439       116  LOAD_FAST                'fid'
              118  LOAD_METHOD              seek
              120  LOAD_GLOBAL              min
              122  LOAD_FAST                'N'
              124  LOAD_GLOBAL              len
              126  LOAD_FAST                'magic'
              128  CALL_FUNCTION_1       1  ''
              130  CALL_FUNCTION_2       2  ''
              132  UNARY_NEGATIVE   
              134  LOAD_CONST               1
              136  CALL_METHOD_2         2  ''
              138  POP_TOP          

 L. 440       140  LOAD_FAST                'magic'
              142  LOAD_METHOD              startswith
              144  LOAD_FAST                '_ZIP_PREFIX'
              146  CALL_METHOD_1         1  ''
              148  POP_JUMP_IF_TRUE    160  'to 160'
              150  LOAD_FAST                'magic'
              152  LOAD_METHOD              startswith
              154  LOAD_FAST                '_ZIP_SUFFIX'
              156  CALL_METHOD_1         1  ''
              158  POP_JUMP_IF_FALSE   188  'to 188'
            160_0  COME_FROM           148  '148'

 L. 443       160  LOAD_GLOBAL              NpzFile
              162  LOAD_FAST                'fid'
              164  LOAD_FAST                'own_fid'
              166  LOAD_FAST                'allow_pickle'

 L. 444       168  LOAD_FAST                'pickle_kwargs'

 L. 443       170  LOAD_CONST               ('own_fid', 'allow_pickle', 'pickle_kwargs')
              172  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              174  STORE_FAST               'ret'

 L. 445       176  LOAD_CONST               False
              178  STORE_FAST               'own_fid'

 L. 446       180  LOAD_FAST                'ret'
              182  POP_BLOCK        
              184  CALL_FINALLY        320  'to 320'
              186  RETURN_VALUE     
            188_0  COME_FROM           158  '158'

 L. 447       188  LOAD_FAST                'magic'
              190  LOAD_GLOBAL              format
              192  LOAD_ATTR                MAGIC_PREFIX
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_FALSE   242  'to 242'

 L. 449       198  LOAD_FAST                'mmap_mode'
              200  POP_JUMP_IF_FALSE   220  'to 220'

 L. 450       202  LOAD_GLOBAL              format
              204  LOAD_ATTR                open_memmap
              206  LOAD_FAST                'file'
              208  LOAD_FAST                'mmap_mode'
              210  LOAD_CONST               ('mode',)
              212  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              214  POP_BLOCK        
              216  CALL_FINALLY        320  'to 320'
              218  RETURN_VALUE     
            220_0  COME_FROM           200  '200'

 L. 452       220  LOAD_GLOBAL              format
              222  LOAD_ATTR                read_array
              224  LOAD_FAST                'fid'
              226  LOAD_FAST                'allow_pickle'

 L. 453       228  LOAD_FAST                'pickle_kwargs'

 L. 452       230  LOAD_CONST               ('allow_pickle', 'pickle_kwargs')
              232  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              234  POP_BLOCK        
              236  CALL_FINALLY        320  'to 320'
              238  RETURN_VALUE     
              240  JUMP_FORWARD        316  'to 316'
            242_0  COME_FROM           196  '196'

 L. 456       242  LOAD_FAST                'allow_pickle'
          244_246  POP_JUMP_IF_TRUE    256  'to 256'

 L. 457       248  LOAD_GLOBAL              ValueError
              250  LOAD_STR                 'Cannot load file containing pickled data when allow_pickle=False'
              252  CALL_FUNCTION_1       1  ''
              254  RAISE_VARARGS_1       1  'exception instance'
            256_0  COME_FROM           244  '244'

 L. 459       256  SETUP_FINALLY       278  'to 278'

 L. 460       258  LOAD_GLOBAL              pickle
              260  LOAD_ATTR                load
              262  LOAD_FAST                'fid'
              264  BUILD_TUPLE_1         1 
              266  LOAD_FAST                'pickle_kwargs'
              268  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              270  POP_BLOCK        
              272  POP_BLOCK        
              274  CALL_FINALLY        320  'to 320'
              276  RETURN_VALUE     
            278_0  COME_FROM_FINALLY   256  '256'

 L. 461       278  DUP_TOP          
              280  LOAD_GLOBAL              Exception
              282  COMPARE_OP               exception-match
          284_286  POP_JUMP_IF_FALSE   314  'to 314'
              288  POP_TOP          
              290  POP_TOP          
              292  POP_TOP          

 L. 462       294  LOAD_GLOBAL              IOError

 L. 463       296  LOAD_STR                 'Failed to interpret file %s as a pickle'
              298  LOAD_GLOBAL              repr
              300  LOAD_FAST                'file'
              302  CALL_FUNCTION_1       1  ''
              304  BINARY_MODULO    

 L. 462       306  CALL_FUNCTION_1       1  ''
              308  RAISE_VARARGS_1       1  'exception instance'
              310  POP_EXCEPT       
              312  JUMP_FORWARD        316  'to 316'
            314_0  COME_FROM           284  '284'
              314  END_FINALLY      
            316_0  COME_FROM           312  '312'
            316_1  COME_FROM           240  '240'
              316  POP_BLOCK        
              318  BEGIN_FINALLY    
            320_0  COME_FROM           274  '274'
            320_1  COME_FROM           236  '236'
            320_2  COME_FROM           216  '216'
            320_3  COME_FROM           184  '184'
            320_4  COME_FROM_FINALLY    86  '86'

 L. 465       320  LOAD_FAST                'own_fid'
          322_324  POP_JUMP_IF_FALSE   334  'to 334'

 L. 466       326  LOAD_FAST                'fid'
              328  LOAD_METHOD              close
              330  CALL_METHOD_0         0  ''
              332  POP_TOP          
            334_0  COME_FROM           322  '322'
              334  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 184


def _save_dispatcher(file, arr, allow_pickle=None, fix_imports=None):
    return (
     arr,)


@array_function_dispatch(_save_dispatcher)
def save(file, arr, allow_pickle=True, fix_imports=True):
    """
    Save an array to a binary file in NumPy ``.npy`` format.

    Parameters
    ----------
    file : file, str, or pathlib.Path
        File or filename to which the data is saved.  If file is a file-object,
        then the filename is unchanged.  If file is a string or Path, a ``.npy``
        extension will be appended to the filename if it does not already
        have one.
    arr : array_like
        Array data to be saved.
    allow_pickle : bool, optional
        Allow saving object arrays using Python pickles. Reasons for disallowing
        pickles include security (loading pickled data can execute arbitrary
        code) and portability (pickled objects may not be loadable on different
        Python installations, for example if the stored objects require libraries
        that are not available, and not all pickled data is compatible between
        Python 2 and Python 3).
        Default: True
    fix_imports : bool, optional
        Only useful in forcing objects in object arrays on Python 3 to be
        pickled in a Python 2 compatible way. If `fix_imports` is True, pickle
        will try to map the new Python 3 names to the old module names used in
        Python 2, so that the pickle data stream is readable with Python 2.

    See Also
    --------
    savez : Save several arrays into a ``.npz`` archive
    savetxt, load

    Notes
    -----
    For a description of the ``.npy`` format, see :py:mod:`numpy.lib.format`.

    Any data saved to the file is appended to the end of the file.

    Examples
    --------
    >>> from tempfile import TemporaryFile
    >>> outfile = TemporaryFile()

    >>> x = np.arange(10)
    >>> np.save(outfile, x)

    >>> _ = outfile.seek(0) # Only needed here to simulate closing & reopening file
    >>> np.load(outfile)
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    >>> with open('test.npy', 'wb') as f:
    ...     np.save(f, np.array([1, 2]))
    ...     np.save(f, np.array([1, 3]))
    >>> with open('test.npy', 'rb') as f:
    ...     a = np.load(f)
    ...     b = np.load(f)
    >>> print(a, b)
    # [1 2] [1 3]
    """
    own_fid = False
    if hasattr(file, 'write'):
        fid = file
    else:
        file = os_fspath(file)
        if not file.endswith('.npy'):
            file = file + '.npy'
        fid = open(file, 'wb')
        own_fid = True
    if sys.version_info[0] >= 3:
        pickle_kwargs = dict(fix_imports=fix_imports)
    else:
        pickle_kwargs = None
    try:
        arr = np.asanyarray(arr)
        format.write_array(fid, arr, allow_pickle=allow_pickle, pickle_kwargs=pickle_kwargs)
    finally:
        if own_fid:
            fid.close()


def _savez_dispatcher(file, *args, **kwds):
    for a in args:
        yield a
    else:
        for v in kwds.values():
            yield v


@array_function_dispatch(_savez_dispatcher)
def savez(file, *args, **kwds):
    r"""Save several arrays into a single file in uncompressed ``.npz`` format.

    If arguments are passed in with no keywords, the corresponding variable
    names, in the ``.npz`` file, are 'arr_0', 'arr_1', etc. If keyword
    arguments are given, the corresponding variable names, in the ``.npz``
    file will match the keyword names.

    Parameters
    ----------
    file : str or file
        Either the filename (string) or an open file (file-like object)
        where the data will be saved. If file is a string or a Path, the
        ``.npz`` extension will be appended to the filename if it is not
        already there.
    args : Arguments, optional
        Arrays to save to the file. Since it is not possible for Python to
        know the names of the arrays outside `savez`, the arrays will be saved
        with names "arr_0", "arr_1", and so on. These arguments can be any
        expression.
    kwds : Keyword arguments, optional
        Arrays to save to the file. Arrays will be saved in the file with the
        keyword names.

    Returns
    -------
    None

    See Also
    --------
    save : Save a single array to a binary file in NumPy format.
    savetxt : Save an array to a file as plain text.
    savez_compressed : Save several arrays into a compressed ``.npz`` archive

    Notes
    -----
    The ``.npz`` file format is a zipped archive of files named after the
    variables they contain.  The archive is not compressed and each file
    in the archive contains one variable in ``.npy`` format. For a
    description of the ``.npy`` format, see :py:mod:`numpy.lib.format`.

    When opening the saved ``.npz`` file with `load` a `NpzFile` object is
    returned. This is a dictionary-like object which can be queried for
    its list of arrays (with the ``.files`` attribute), and for the arrays
    themselves.

    When saving dictionaries, the dictionary keys become filenames
    inside the ZIP archive. Therefore, keys should be valid filenames.
    E.g., avoid keys that begin with ``/`` or contain ``.``.

    Examples
    --------
    >>> from tempfile import TemporaryFile
    >>> outfile = TemporaryFile()
    >>> x = np.arange(10)
    >>> y = np.sin(x)

    Using `savez` with \*args, the arrays are saved with default names.

    >>> np.savez(outfile, x, y)
    >>> _ = outfile.seek(0) # Only needed here to simulate closing & reopening file
    >>> npzfile = np.load(outfile)
    >>> npzfile.files
    ['arr_0', 'arr_1']
    >>> npzfile['arr_0']
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    Using `savez` with \**kwds, the arrays are saved with the keyword names.

    >>> outfile = TemporaryFile()
    >>> np.savez(outfile, x=x, y=y)
    >>> _ = outfile.seek(0)
    >>> npzfile = np.load(outfile)
    >>> sorted(npzfile.files)
    ['x', 'y']
    >>> npzfile['x']
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    """
    _savez(file, args, kwds, False)


def _savez_compressed_dispatcher(file, *args, **kwds):
    for a in args:
        yield a
    else:
        for v in kwds.values():
            yield v


@array_function_dispatch(_savez_compressed_dispatcher)
def savez_compressed(file, *args, **kwds):
    """
    Save several arrays into a single file in compressed ``.npz`` format.

    If keyword arguments are given, then filenames are taken from the keywords.
    If arguments are passed in with no keywords, then stored filenames are
    arr_0, arr_1, etc.

    Parameters
    ----------
    file : str or file
        Either the filename (string) or an open file (file-like object)
        where the data will be saved. If file is a string or a Path, the
        ``.npz`` extension will be appended to the filename if it is not
        already there.
    args : Arguments, optional
        Arrays to save to the file. Since it is not possible for Python to
        know the names of the arrays outside `savez`, the arrays will be saved
        with names "arr_0", "arr_1", and so on. These arguments can be any
        expression.
    kwds : Keyword arguments, optional
        Arrays to save to the file. Arrays will be saved in the file with the
        keyword names.

    Returns
    -------
    None

    See Also
    --------
    numpy.save : Save a single array to a binary file in NumPy format.
    numpy.savetxt : Save an array to a file as plain text.
    numpy.savez : Save several arrays into an uncompressed ``.npz`` file format
    numpy.load : Load the files created by savez_compressed.

    Notes
    -----
    The ``.npz`` file format is a zipped archive of files named after the
    variables they contain.  The archive is compressed with
    ``zipfile.ZIP_DEFLATED`` and each file in the archive contains one variable
    in ``.npy`` format. For a description of the ``.npy`` format, see 
    :py:mod:`numpy.lib.format`.

    When opening the saved ``.npz`` file with `load` a `NpzFile` object is
    returned. This is a dictionary-like object which can be queried for
    its list of arrays (with the ``.files`` attribute), and for the arrays
    themselves.

    Examples
    --------
    >>> test_array = np.random.rand(3, 2)
    >>> test_vector = np.random.rand(4)
    >>> np.savez_compressed('/tmp/123', a=test_array, b=test_vector)
    >>> loaded = np.load('/tmp/123.npz')
    >>> print(np.array_equal(test_array, loaded['a']))
    True
    >>> print(np.array_equal(test_vector, loaded['b']))
    True

    """
    _savez(file, args, kwds, True)


def _savez(file, args, kwds, compress, allow_pickle=True, pickle_kwargs=None):
    import zipfile
    if not hasattr(file, 'write'):
        file = os_fspath(file)
        if not file.endswith('.npz'):
            file = file + '.npz'
    namedict = kwds
    for i, val in enumerate(args):
        key = 'arr_%d' % i
        if key in namedict.keys():
            raise ValueError('Cannot use un-named variables and keyword %s' % key)
        else:
            namedict[key] = val
    else:
        if compress:
            compression = zipfile.ZIP_DEFLATED
        else:
            compression = zipfile.ZIP_STORED
        zipf = zipfile_factory(file, mode='w', compression=compression)
        if sys.version_info >= (3, 6):
            for key, val in namedict.items():
                fname = key + '.npy'
                val = np.asanyarray(val)
                with zipf.open(fname, 'w', force_zip64=True) as fid:
                    format.write_array(fid, val, allow_pickle=allow_pickle,
                      pickle_kwargs=pickle_kwargs)

        else:
            import tempfile
            file_dir, file_prefix = os.path.split(file) if _is_string_like(file) else (None,
                                                                                       'tmp')
            fd, tmpfile = tempfile.mkstemp(prefix=file_prefix, dir=file_dir, suffix='-numpy.npy')
            os.close(fd)
            try:
                for key, val in namedict.items():
                    fname = key + '.npy'
                    fid = open(tmpfile, 'wb')
                    try:
                        try:
                            format.write_array(fid, (np.asanyarray(val)), allow_pickle=allow_pickle,
                              pickle_kwargs=pickle_kwargs)
                            fid.close()
                            fid = None
                            zipf.write(tmpfile, arcname=fname)
                        except IOError as exc:
                            try:
                                raise IOError('Failed to write to %s: %s' % (tmpfile, exc))
                            finally:
                                exc = None
                                del exc

                    finally:
                        if fid:
                            fid.close()

            finally:
                os.remove(tmpfile)

        zipf.close()


def _getconv(dtype):
    """ Find the correct dtype converter. Adapted from matplotlib """

    def floatconv(x):
        x.lower()
        if '0x' in x:
            return float.fromhex(x)
        return float(x)

    typ = dtype.type
    if issubclass(typ, np.bool_):
        return lambda x: bool(int(x))
    if issubclass(typ, np.uint64):
        return np.uint64
    if issubclass(typ, np.int64):
        return np.int64
    if issubclass(typ, np.integer):
        return lambda x: int(float(x))
    if issubclass(typ, np.longdouble):
        return np.longdouble
    if issubclass(typ, np.floating):
        return floatconv
    if issubclass(typ, complex):
        return lambda x: complex(asstr(x).replace('+-', '-'))
    if issubclass(typ, np.bytes_):
        return asbytes
    if issubclass(typ, np.unicode_):
        return asunicode
    return asstr


_loadtxt_chunksize = 50000

@set_module('numpy')
def loadtxt--- This code section failed: ---

 L. 938         0  LOAD_DEREF               'comments'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    72  'to 72'

 L. 939         8  LOAD_GLOBAL              isinstance
               10  LOAD_DEREF               'comments'
               12  LOAD_GLOBAL              basestring
               14  LOAD_GLOBAL              bytes
               16  BUILD_TUPLE_2         2 
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L. 940        22  LOAD_DEREF               'comments'
               24  BUILD_LIST_1          1 
               26  STORE_DEREF              'comments'
             28_0  COME_FROM            20  '20'

 L. 941        28  LOAD_LISTCOMP            '<code_object <listcomp>>'
               30  LOAD_STR                 'loadtxt.<locals>.<listcomp>'
               32  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               34  LOAD_DEREF               'comments'
               36  GET_ITER         
               38  CALL_FUNCTION_1       1  ''
               40  STORE_DEREF              'comments'

 L. 943        42  LOAD_GENEXPR             '<code_object <genexpr>>'
               44  LOAD_STR                 'loadtxt.<locals>.<genexpr>'
               46  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               48  LOAD_DEREF               'comments'
               50  GET_ITER         
               52  CALL_FUNCTION_1       1  ''
               54  STORE_DEREF              'comments'

 L. 944        56  LOAD_GLOBAL              re
               58  LOAD_METHOD              compile
               60  LOAD_STR                 '|'
               62  LOAD_METHOD              join
               64  LOAD_DEREF               'comments'
               66  CALL_METHOD_1         1  ''
               68  CALL_METHOD_1         1  ''
               70  STORE_DEREF              'regex_comments'
             72_0  COME_FROM             6  '6'

 L. 946        72  LOAD_DEREF               'delimiter'
               74  LOAD_CONST               None
               76  COMPARE_OP               is-not
               78  POP_JUMP_IF_FALSE    88  'to 88'

 L. 947        80  LOAD_GLOBAL              _decode_line
               82  LOAD_DEREF               'delimiter'
               84  CALL_FUNCTION_1       1  ''
               86  STORE_DEREF              'delimiter'
             88_0  COME_FROM            78  '78'

 L. 949        88  LOAD_DEREF               'converters'
               90  STORE_FAST               'user_converters'

 L. 951        92  LOAD_DEREF               'encoding'
               94  LOAD_STR                 'bytes'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   110  'to 110'

 L. 952       100  LOAD_CONST               None
              102  STORE_DEREF              'encoding'

 L. 953       104  LOAD_CONST               True
              106  STORE_FAST               'byte_converters'
              108  JUMP_FORWARD        114  'to 114'
            110_0  COME_FROM            98  '98'

 L. 955       110  LOAD_CONST               False
              112  STORE_FAST               'byte_converters'
            114_0  COME_FROM           108  '108'

 L. 957       114  LOAD_DEREF               'usecols'
              116  LOAD_CONST               None
              118  COMPARE_OP               is-not
              120  POP_JUMP_IF_FALSE   242  'to 242'

 L. 959       122  SETUP_FINALLY       136  'to 136'

 L. 960       124  LOAD_GLOBAL              list
              126  LOAD_DEREF               'usecols'
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'usecols_as_list'
              132  POP_BLOCK        
              134  JUMP_FORWARD        162  'to 162'
            136_0  COME_FROM_FINALLY   122  '122'

 L. 961       136  DUP_TOP          
              138  LOAD_GLOBAL              TypeError
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   160  'to 160'
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 962       150  LOAD_DEREF               'usecols'
              152  BUILD_LIST_1          1 
              154  STORE_FAST               'usecols_as_list'
              156  POP_EXCEPT       
              158  JUMP_FORWARD        162  'to 162'
            160_0  COME_FROM           142  '142'
              160  END_FINALLY      
            162_0  COME_FROM           158  '158'
            162_1  COME_FROM           134  '134'

 L. 963       162  LOAD_FAST                'usecols_as_list'
              164  GET_ITER         
            166_0  COME_FROM           236  '236'
            166_1  COME_FROM           232  '232'
            166_2  COME_FROM           182  '182'
              166  FOR_ITER            238  'to 238'
              168  STORE_FAST               'col_idx'

 L. 964       170  SETUP_FINALLY       184  'to 184'

 L. 965       172  LOAD_GLOBAL              opindex
              174  LOAD_FAST                'col_idx'
              176  CALL_FUNCTION_1       1  ''
              178  POP_TOP          
              180  POP_BLOCK        
              182  JUMP_BACK           166  'to 166'
            184_0  COME_FROM_FINALLY   170  '170'

 L. 966       184  DUP_TOP          
              186  LOAD_GLOBAL              TypeError
              188  COMPARE_OP               exception-match
              190  POP_JUMP_IF_FALSE   234  'to 234'
              192  POP_TOP          
              194  STORE_FAST               'e'
              196  POP_TOP          
              198  SETUP_FINALLY       222  'to 222'

 L. 968       200  LOAD_STR                 'usecols must be an int or a sequence of ints but it contains at least one element of type %s'

 L. 970       202  LOAD_GLOBAL              type
              204  LOAD_FAST                'col_idx'
              206  CALL_FUNCTION_1       1  ''

 L. 968       208  BINARY_MODULO    

 L. 967       210  BUILD_TUPLE_1         1 
              212  LOAD_FAST                'e'
              214  STORE_ATTR               args

 L. 972       216  RAISE_VARARGS_0       0  'reraise'
              218  POP_BLOCK        
              220  BEGIN_FINALLY    
            222_0  COME_FROM_FINALLY   198  '198'
              222  LOAD_CONST               None
              224  STORE_FAST               'e'
              226  DELETE_FAST              'e'
              228  END_FINALLY      
              230  POP_EXCEPT       
              232  JUMP_BACK           166  'to 166'
            234_0  COME_FROM           190  '190'
              234  END_FINALLY      
              236  JUMP_BACK           166  'to 166'
            238_0  COME_FROM           166  '166'

 L. 974       238  LOAD_FAST                'usecols_as_list'
              240  STORE_DEREF              'usecols'
            242_0  COME_FROM           120  '120'

 L. 976       242  LOAD_CONST               False
              244  STORE_FAST               'fown'

 L. 977       246  SETUP_FINALLY       348  'to 348'

 L. 978       248  LOAD_GLOBAL              isinstance
              250  LOAD_FAST                'fname'
              252  LOAD_GLOBAL              os_PathLike
              254  CALL_FUNCTION_2       2  ''
          256_258  POP_JUMP_IF_FALSE   268  'to 268'

 L. 979       260  LOAD_GLOBAL              os_fspath
              262  LOAD_FAST                'fname'
              264  CALL_FUNCTION_1       1  ''
              266  STORE_FAST               'fname'
            268_0  COME_FROM           256  '256'

 L. 980       268  LOAD_GLOBAL              _is_string_like
              270  LOAD_FAST                'fname'
              272  CALL_FUNCTION_1       1  ''
          274_276  POP_JUMP_IF_FALSE   324  'to 324'

 L. 981       278  LOAD_GLOBAL              np
              280  LOAD_ATTR                lib
              282  LOAD_ATTR                _datasource
              284  LOAD_ATTR                open
              286  LOAD_FAST                'fname'
              288  LOAD_STR                 'rt'
              290  LOAD_DEREF               'encoding'
              292  LOAD_CONST               ('encoding',)
              294  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              296  STORE_DEREF              'fh'

 L. 982       298  LOAD_GLOBAL              getattr
              300  LOAD_DEREF               'fh'
              302  LOAD_STR                 'encoding'
              304  LOAD_STR                 'latin1'
              306  CALL_FUNCTION_3       3  ''
              308  STORE_DEREF              'fencoding'

 L. 983       310  LOAD_GLOBAL              iter
              312  LOAD_DEREF               'fh'
              314  CALL_FUNCTION_1       1  ''
              316  STORE_DEREF              'fh'

 L. 984       318  LOAD_CONST               True
              320  STORE_FAST               'fown'
              322  JUMP_FORWARD        344  'to 344'
            324_0  COME_FROM           274  '274'

 L. 986       324  LOAD_GLOBAL              iter
              326  LOAD_FAST                'fname'
              328  CALL_FUNCTION_1       1  ''
              330  STORE_DEREF              'fh'

 L. 987       332  LOAD_GLOBAL              getattr
              334  LOAD_FAST                'fname'
              336  LOAD_STR                 'encoding'
              338  LOAD_STR                 'latin1'
              340  CALL_FUNCTION_3       3  ''
              342  STORE_DEREF              'fencoding'
            344_0  COME_FROM           322  '322'
              344  POP_BLOCK        
              346  JUMP_FORWARD        378  'to 378'
            348_0  COME_FROM_FINALLY   246  '246'

 L. 988       348  DUP_TOP          
              350  LOAD_GLOBAL              TypeError
              352  COMPARE_OP               exception-match
          354_356  POP_JUMP_IF_FALSE   376  'to 376'
              358  POP_TOP          
              360  POP_TOP          
              362  POP_TOP          

 L. 989       364  LOAD_GLOBAL              ValueError
              366  LOAD_STR                 'fname must be a string, file handle, or generator'
              368  CALL_FUNCTION_1       1  ''
              370  RAISE_VARARGS_1       1  'exception instance'
              372  POP_EXCEPT       
              374  JUMP_FORWARD        378  'to 378'
            376_0  COME_FROM           354  '354'
              376  END_FINALLY      
            378_0  COME_FROM           374  '374'
            378_1  COME_FROM           346  '346'

 L. 992       378  LOAD_DEREF               'encoding'
              380  LOAD_CONST               None
              382  COMPARE_OP               is-not
          384_386  POP_JUMP_IF_FALSE   394  'to 394'

 L. 993       388  LOAD_DEREF               'encoding'
              390  STORE_DEREF              'fencoding'
              392  JUMP_FORWARD        420  'to 420'
            394_0  COME_FROM           384  '384'

 L. 996       394  LOAD_DEREF               'fencoding'
              396  LOAD_CONST               None
              398  COMPARE_OP               is
          400_402  POP_JUMP_IF_FALSE   420  'to 420'

 L. 997       404  LOAD_CONST               0
              406  LOAD_CONST               None
              408  IMPORT_NAME              locale
              410  STORE_FAST               'locale'

 L. 998       412  LOAD_FAST                'locale'
              414  LOAD_METHOD              getpreferredencoding
              416  CALL_METHOD_0         0  ''
              418  STORE_DEREF              'fencoding'
            420_0  COME_FROM           400  '400'
            420_1  COME_FROM           392  '392'

 L.1001       420  LOAD_GLOBAL              recursive

 L.1002       422  LOAD_CODE                <code_object flatten_dtype_internal>
              424  LOAD_STR                 'loadtxt.<locals>.flatten_dtype_internal'
              426  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              428  CALL_FUNCTION_1       1  ''
              430  STORE_FAST               'flatten_dtype_internal'

 L.1031       432  LOAD_GLOBAL              recursive

 L.1032       434  LOAD_CODE                <code_object pack_items>
              436  LOAD_STR                 'loadtxt.<locals>.pack_items'
              438  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              440  CALL_FUNCTION_1       1  ''
              442  STORE_DEREF              'pack_items'

 L.1048       444  LOAD_CLOSURE             'comments'
              446  LOAD_CLOSURE             'delimiter'
              448  LOAD_CLOSURE             'encoding'
              450  LOAD_CLOSURE             'regex_comments'
              452  BUILD_TUPLE_4         4 
              454  LOAD_CODE                <code_object split_line>
              456  LOAD_STR                 'loadtxt.<locals>.split_line'
              458  MAKE_FUNCTION_8          'closure'
              460  STORE_DEREF              'split_line'

 L.1060       462  LOAD_CLOSURE             'N'
              464  LOAD_CLOSURE             'converters'
              466  LOAD_CLOSURE             'fh'
              468  LOAD_CLOSURE             'first_line'
              470  LOAD_CLOSURE             'max_rows'
              472  LOAD_CLOSURE             'pack_items'
              474  LOAD_CLOSURE             'packing'
              476  LOAD_CLOSURE             'skiprows'
              478  LOAD_CLOSURE             'split_line'
              480  LOAD_CLOSURE             'usecols'
              482  BUILD_TUPLE_10       10 
              484  LOAD_CODE                <code_object read_data>
              486  LOAD_STR                 'loadtxt.<locals>.read_data'
              488  MAKE_FUNCTION_8          'closure'
              490  STORE_FAST               'read_data'

 L.1098   492_494  SETUP_FINALLY       972  'to 972'

 L.1100       496  LOAD_GLOBAL              np
              498  LOAD_METHOD              dtype
              500  LOAD_FAST                'dtype'
              502  CALL_METHOD_1         1  ''
              504  STORE_FAST               'dtype'

 L.1101       506  LOAD_GLOBAL              _getconv
              508  LOAD_FAST                'dtype'
              510  CALL_FUNCTION_1       1  ''
              512  STORE_DEREF              'defconv'

 L.1104       514  LOAD_GLOBAL              range
              516  LOAD_DEREF               'skiprows'
              518  CALL_FUNCTION_1       1  ''
              520  GET_ITER         
            522_0  COME_FROM           534  '534'
              522  FOR_ITER            538  'to 538'
              524  STORE_FAST               'i'

 L.1105       526  LOAD_GLOBAL              next
              528  LOAD_DEREF               'fh'
              530  CALL_FUNCTION_1       1  ''
              532  POP_TOP          
          534_536  JUMP_BACK           522  'to 522'
            538_0  COME_FROM           522  '522'

 L.1109       538  LOAD_CONST               None
              540  STORE_FAST               'first_vals'

 L.1110       542  SETUP_FINALLY       574  'to 574'
            544_0  COME_FROM           566  '566'

 L.1111       544  LOAD_FAST                'first_vals'
          546_548  POP_JUMP_IF_TRUE    570  'to 570'

 L.1112       550  LOAD_GLOBAL              next
              552  LOAD_DEREF               'fh'
              554  CALL_FUNCTION_1       1  ''
              556  STORE_DEREF              'first_line'

 L.1113       558  LOAD_DEREF               'split_line'
              560  LOAD_DEREF               'first_line'
              562  CALL_FUNCTION_1       1  ''
              564  STORE_FAST               'first_vals'
          566_568  JUMP_BACK           544  'to 544'
            570_0  COME_FROM           546  '546'
              570  POP_BLOCK        
              572  JUMP_FORWARD        622  'to 622'
            574_0  COME_FROM_FINALLY   542  '542'

 L.1114       574  DUP_TOP          
              576  LOAD_GLOBAL              StopIteration
              578  COMPARE_OP               exception-match
          580_582  POP_JUMP_IF_FALSE   620  'to 620'
              584  POP_TOP          
              586  POP_TOP          
              588  POP_TOP          

 L.1116       590  LOAD_STR                 ''
              592  STORE_DEREF              'first_line'

 L.1117       594  BUILD_LIST_0          0 
              596  STORE_FAST               'first_vals'

 L.1118       598  LOAD_GLOBAL              warnings
              600  LOAD_ATTR                warn
              602  LOAD_STR                 'loadtxt: Empty input file: "%s"'
              604  LOAD_FAST                'fname'
              606  BINARY_MODULO    
              608  LOAD_CONST               2
              610  LOAD_CONST               ('stacklevel',)
              612  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              614  POP_TOP          
              616  POP_EXCEPT       
              618  JUMP_FORWARD        622  'to 622'
            620_0  COME_FROM           580  '580'
              620  END_FINALLY      
            622_0  COME_FROM           618  '618'
            622_1  COME_FROM           572  '572'

 L.1119       622  LOAD_GLOBAL              len
              624  LOAD_DEREF               'usecols'
          626_628  JUMP_IF_TRUE_OR_POP   632  'to 632'
              630  LOAD_FAST                'first_vals'
            632_0  COME_FROM           626  '626'
              632  CALL_FUNCTION_1       1  ''
              634  STORE_DEREF              'N'

 L.1121       636  LOAD_FAST                'flatten_dtype_internal'
              638  LOAD_FAST                'dtype'
              640  CALL_FUNCTION_1       1  ''
              642  UNPACK_SEQUENCE_2     2 
              644  STORE_FAST               'dtype_types'
              646  STORE_DEREF              'packing'

 L.1122       648  LOAD_GLOBAL              len
              650  LOAD_FAST                'dtype_types'
              652  CALL_FUNCTION_1       1  ''
              654  LOAD_CONST               1
              656  COMPARE_OP               >
          658_660  POP_JUMP_IF_FALSE   678  'to 678'

 L.1125       662  LOAD_LISTCOMP            '<code_object <listcomp>>'
              664  LOAD_STR                 'loadtxt.<locals>.<listcomp>'
              666  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              668  LOAD_FAST                'dtype_types'
              670  GET_ITER         
              672  CALL_FUNCTION_1       1  ''
              674  STORE_DEREF              'converters'
              676  JUMP_FORWARD        720  'to 720'
            678_0  COME_FROM           658  '658'

 L.1128       678  LOAD_CLOSURE             'defconv'
              680  BUILD_TUPLE_1         1 
              682  LOAD_LISTCOMP            '<code_object <listcomp>>'
              684  LOAD_STR                 'loadtxt.<locals>.<listcomp>'
              686  MAKE_FUNCTION_8          'closure'
              688  LOAD_GLOBAL              range
              690  LOAD_DEREF               'N'
              692  CALL_FUNCTION_1       1  ''
              694  GET_ITER         
              696  CALL_FUNCTION_1       1  ''
              698  STORE_DEREF              'converters'

 L.1129       700  LOAD_DEREF               'N'
              702  LOAD_CONST               1
              704  COMPARE_OP               >
          706_708  POP_JUMP_IF_FALSE   720  'to 720'

 L.1130       710  LOAD_DEREF               'N'
              712  LOAD_GLOBAL              tuple
              714  BUILD_TUPLE_2         2 
              716  BUILD_LIST_1          1 
              718  STORE_DEREF              'packing'
            720_0  COME_FROM           706  '706'
            720_1  COME_FROM           676  '676'

 L.1133       720  LOAD_FAST                'user_converters'
          722_724  JUMP_IF_TRUE_OR_POP   728  'to 728'
              726  BUILD_MAP_0           0 
            728_0  COME_FROM           722  '722'
              728  LOAD_METHOD              items
              730  CALL_METHOD_0         0  ''
              732  GET_ITER         
            734_0  COME_FROM           834  '834'
            734_1  COME_FROM           824  '824'
            734_2  COME_FROM           782  '782'
              734  FOR_ITER            838  'to 838'
              736  UNPACK_SEQUENCE_2     2 
              738  STORE_FAST               'i'
              740  STORE_FAST               'conv'

 L.1134       742  LOAD_DEREF               'usecols'
          744_746  POP_JUMP_IF_FALSE   792  'to 792'

 L.1135       748  SETUP_FINALLY       764  'to 764'

 L.1136       750  LOAD_DEREF               'usecols'
              752  LOAD_METHOD              index
              754  LOAD_FAST                'i'
              756  CALL_METHOD_1         1  ''
              758  STORE_FAST               'i'
              760  POP_BLOCK        
              762  JUMP_FORWARD        792  'to 792'
            764_0  COME_FROM_FINALLY   748  '748'

 L.1137       764  DUP_TOP          
              766  LOAD_GLOBAL              ValueError
              768  COMPARE_OP               exception-match
          770_772  POP_JUMP_IF_FALSE   790  'to 790'
              774  POP_TOP          
              776  POP_TOP          
              778  POP_TOP          

 L.1139       780  POP_EXCEPT       
          782_784  JUMP_BACK           734  'to 734'
              786  POP_EXCEPT       
              788  JUMP_FORWARD        792  'to 792'
            790_0  COME_FROM           770  '770'
              790  END_FINALLY      
            792_0  COME_FROM           788  '788'
            792_1  COME_FROM           762  '762'
            792_2  COME_FROM           744  '744'

 L.1140       792  LOAD_FAST                'byte_converters'
          794_796  POP_JUMP_IF_FALSE   826  'to 826'

 L.1143       798  LOAD_CODE                <code_object tobytes_first>
              800  LOAD_STR                 'loadtxt.<locals>.tobytes_first'
              802  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              804  STORE_FAST               'tobytes_first'

 L.1147       806  LOAD_GLOBAL              functools
              808  LOAD_ATTR                partial
              810  LOAD_FAST                'tobytes_first'
              812  LOAD_FAST                'conv'
              814  LOAD_CONST               ('conv',)
              816  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              818  LOAD_DEREF               'converters'
              820  LOAD_FAST                'i'
              822  STORE_SUBSCR     
              824  JUMP_BACK           734  'to 734'
            826_0  COME_FROM           794  '794'

 L.1149       826  LOAD_FAST                'conv'
              828  LOAD_DEREF               'converters'
              830  LOAD_FAST                'i'
              832  STORE_SUBSCR     
          834_836  JUMP_BACK           734  'to 734'
            838_0  COME_FROM           734  '734'

 L.1151       838  LOAD_CLOSURE             'fencoding'
              840  BUILD_TUPLE_1         1 
              842  LOAD_LISTCOMP            '<code_object <listcomp>>'
              844  LOAD_STR                 'loadtxt.<locals>.<listcomp>'
              846  MAKE_FUNCTION_8          'closure'

 L.1152       848  LOAD_DEREF               'converters'

 L.1151       850  GET_ITER         
              852  CALL_FUNCTION_1       1  ''
              854  STORE_DEREF              'converters'

 L.1158       856  LOAD_CONST               None
              858  STORE_DEREF              'X'

 L.1159       860  LOAD_FAST                'read_data'
              862  LOAD_GLOBAL              _loadtxt_chunksize
              864  CALL_FUNCTION_1       1  ''
              866  GET_ITER         
            868_0  COME_FROM           964  '964'
            868_1  COME_FROM           894  '894'
              868  FOR_ITER            968  'to 968'
              870  STORE_FAST               'x'

 L.1160       872  LOAD_DEREF               'X'
              874  LOAD_CONST               None
              876  COMPARE_OP               is
          878_880  POP_JUMP_IF_FALSE   896  'to 896'

 L.1161       882  LOAD_GLOBAL              np
              884  LOAD_METHOD              array
              886  LOAD_FAST                'x'
              888  LOAD_FAST                'dtype'
              890  CALL_METHOD_2         2  ''
              892  STORE_DEREF              'X'
              894  JUMP_BACK           868  'to 868'
            896_0  COME_FROM           878  '878'

 L.1163       896  LOAD_GLOBAL              list
              898  LOAD_DEREF               'X'
              900  LOAD_ATTR                shape
              902  CALL_FUNCTION_1       1  ''
              904  STORE_FAST               'nshape'

 L.1164       906  LOAD_FAST                'nshape'
              908  LOAD_CONST               0
              910  BINARY_SUBSCR    
              912  STORE_FAST               'pos'

 L.1165       914  LOAD_FAST                'nshape'
              916  LOAD_CONST               0
              918  DUP_TOP_TWO      
              920  BINARY_SUBSCR    
              922  LOAD_GLOBAL              len
              924  LOAD_FAST                'x'
              926  CALL_FUNCTION_1       1  ''
              928  INPLACE_ADD      
              930  ROT_THREE        
              932  STORE_SUBSCR     

 L.1166       934  LOAD_DEREF               'X'
              936  LOAD_ATTR                resize
              938  LOAD_FAST                'nshape'
              940  LOAD_CONST               False
              942  LOAD_CONST               ('refcheck',)
              944  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              946  POP_TOP          

 L.1167       948  LOAD_FAST                'x'
              950  LOAD_DEREF               'X'
              952  LOAD_FAST                'pos'
              954  LOAD_CONST               None
              956  BUILD_SLICE_2         2 
              958  LOAD_CONST               Ellipsis
              960  BUILD_TUPLE_2         2 
              962  STORE_SUBSCR     
          964_966  JUMP_BACK           868  'to 868'
            968_0  COME_FROM           868  '868'
              968  POP_BLOCK        
              970  BEGIN_FINALLY    
            972_0  COME_FROM_FINALLY   492  '492'

 L.1169       972  LOAD_FAST                'fown'
          974_976  POP_JUMP_IF_FALSE   986  'to 986'

 L.1170       978  LOAD_DEREF               'fh'
              980  LOAD_METHOD              close
              982  CALL_METHOD_0         0  ''
              984  POP_TOP          
            986_0  COME_FROM           974  '974'
              986  END_FINALLY      

 L.1172       988  LOAD_DEREF               'X'
              990  LOAD_CONST               None
              992  COMPARE_OP               is
          994_996  POP_JUMP_IF_FALSE  1010  'to 1010'

 L.1173       998  LOAD_GLOBAL              np
             1000  LOAD_METHOD              array
             1002  BUILD_LIST_0          0 
             1004  LOAD_FAST                'dtype'
             1006  CALL_METHOD_2         2  ''
             1008  STORE_DEREF              'X'
           1010_0  COME_FROM           994  '994'

 L.1177      1010  LOAD_DEREF               'X'
             1012  LOAD_ATTR                ndim
             1014  LOAD_CONST               3
             1016  COMPARE_OP               ==
         1018_1020  POP_JUMP_IF_FALSE  1048  'to 1048'
             1022  LOAD_DEREF               'X'
             1024  LOAD_ATTR                shape
             1026  LOAD_CONST               None
             1028  LOAD_CONST               2
             1030  BUILD_SLICE_2         2 
             1032  BINARY_SUBSCR    
             1034  LOAD_CONST               (1, 1)
             1036  COMPARE_OP               ==
         1038_1040  POP_JUMP_IF_FALSE  1048  'to 1048'

 L.1178      1042  LOAD_CONST               (1, -1)
             1044  LOAD_DEREF               'X'
             1046  STORE_ATTR               shape
           1048_0  COME_FROM          1038  '1038'
           1048_1  COME_FROM          1018  '1018'

 L.1182      1048  LOAD_FAST                'ndmin'
             1050  LOAD_CONST               (0, 1, 2)
             1052  COMPARE_OP               not-in
         1054_1056  POP_JUMP_IF_FALSE  1070  'to 1070'

 L.1183      1058  LOAD_GLOBAL              ValueError
             1060  LOAD_STR                 'Illegal value of ndmin keyword: %s'
             1062  LOAD_FAST                'ndmin'
             1064  BINARY_MODULO    
             1066  CALL_FUNCTION_1       1  ''
             1068  RAISE_VARARGS_1       1  'exception instance'
           1070_0  COME_FROM          1054  '1054'

 L.1185      1070  LOAD_DEREF               'X'
             1072  LOAD_ATTR                ndim
             1074  LOAD_FAST                'ndmin'
             1076  COMPARE_OP               >
         1078_1080  POP_JUMP_IF_FALSE  1092  'to 1092'

 L.1186      1082  LOAD_GLOBAL              np
             1084  LOAD_METHOD              squeeze
             1086  LOAD_DEREF               'X'
             1088  CALL_METHOD_1         1  ''
             1090  STORE_DEREF              'X'
           1092_0  COME_FROM          1078  '1078'

 L.1189      1092  LOAD_DEREF               'X'
             1094  LOAD_ATTR                ndim
             1096  LOAD_FAST                'ndmin'
             1098  COMPARE_OP               <
         1100_1102  POP_JUMP_IF_FALSE  1148  'to 1148'

 L.1190      1104  LOAD_FAST                'ndmin'
             1106  LOAD_CONST               1
             1108  COMPARE_OP               ==
         1110_1112  POP_JUMP_IF_FALSE  1126  'to 1126'

 L.1191      1114  LOAD_GLOBAL              np
             1116  LOAD_METHOD              atleast_1d
             1118  LOAD_DEREF               'X'
             1120  CALL_METHOD_1         1  ''
             1122  STORE_DEREF              'X'
             1124  JUMP_FORWARD       1148  'to 1148'
           1126_0  COME_FROM          1110  '1110'

 L.1192      1126  LOAD_FAST                'ndmin'
             1128  LOAD_CONST               2
             1130  COMPARE_OP               ==
         1132_1134  POP_JUMP_IF_FALSE  1148  'to 1148'

 L.1193      1136  LOAD_GLOBAL              np
             1138  LOAD_METHOD              atleast_2d
             1140  LOAD_DEREF               'X'
             1142  CALL_METHOD_1         1  ''
             1144  LOAD_ATTR                T
             1146  STORE_DEREF              'X'
           1148_0  COME_FROM          1132  '1132'
           1148_1  COME_FROM          1124  '1124'
           1148_2  COME_FROM          1100  '1100'

 L.1195      1148  LOAD_FAST                'unpack'
         1150_1152  POP_JUMP_IF_FALSE  1196  'to 1196'

 L.1196      1154  LOAD_GLOBAL              len
             1156  LOAD_FAST                'dtype_types'
             1158  CALL_FUNCTION_1       1  ''
             1160  LOAD_CONST               1
             1162  COMPARE_OP               >
         1164_1166  POP_JUMP_IF_FALSE  1188  'to 1188'

 L.1198      1168  LOAD_CLOSURE             'X'
             1170  BUILD_TUPLE_1         1 
             1172  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1174  LOAD_STR                 'loadtxt.<locals>.<listcomp>'
             1176  MAKE_FUNCTION_8          'closure'
             1178  LOAD_FAST                'dtype'
             1180  LOAD_ATTR                names
             1182  GET_ITER         
             1184  CALL_FUNCTION_1       1  ''
             1186  RETURN_VALUE     
           1188_0  COME_FROM          1164  '1164'

 L.1200      1188  LOAD_DEREF               'X'
             1190  LOAD_ATTR                T
             1192  RETURN_VALUE     
             1194  JUMP_FORWARD       1200  'to 1200'
           1196_0  COME_FROM          1150  '1150'

 L.1202      1196  LOAD_DEREF               'X'
             1198  RETURN_VALUE     
           1200_0  COME_FROM          1194  '1194'

Parse error at or near `COME_FROM' instruction at offset 790_0


def _savetxt_dispatcher(fname, X, fmt=None, delimiter=None, newline=None, header=None, footer=None, comments=None, encoding=None):
    return (
     X,)


@array_function_dispatch(_savetxt_dispatcher)
def savetxt(fname, X, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ', encoding=None):
    """
    Save an array to a text file.

    Parameters
    ----------
    fname : filename or file handle
        If the filename ends in ``.gz``, the file is automatically saved in
        compressed gzip format.  `loadtxt` understands gzipped files
        transparently.
    X : 1D or 2D array_like
        Data to be saved to a text file.
    fmt : str or sequence of strs, optional
        A single format (%10.5f), a sequence of formats, or a
        multi-format string, e.g. 'Iteration %d -- %10.5f', in which
        case `delimiter` is ignored. For complex `X`, the legal options
        for `fmt` are:

        * a single specifier, `fmt='%.4e'`, resulting in numbers formatted
          like `' (%s+%sj)' % (fmt, fmt)`
        * a full string specifying every real and imaginary part, e.g.
          `' %.4e %+.4ej %.4e %+.4ej %.4e %+.4ej'` for 3 columns
        * a list of specifiers, one per column - in this case, the real
          and imaginary part must have separate specifiers,
          e.g. `['%.3e + %.3ej', '(%.15e%+.15ej)']` for 2 columns
    delimiter : str, optional
        String or character separating columns.
    newline : str, optional
        String or character separating lines.

        .. versionadded:: 1.5.0
    header : str, optional
        String that will be written at the beginning of the file.

        .. versionadded:: 1.7.0
    footer : str, optional
        String that will be written at the end of the file.

        .. versionadded:: 1.7.0
    comments : str, optional
        String that will be prepended to the ``header`` and ``footer`` strings,
        to mark them as comments. Default: '# ',  as expected by e.g.
        ``numpy.loadtxt``.

        .. versionadded:: 1.7.0
    encoding : {None, str}, optional
        Encoding used to encode the outputfile. Does not apply to output
        streams. If the encoding is something other than 'bytes' or 'latin1'
        you will not be able to load the file in NumPy versions < 1.14. Default
        is 'latin1'.

        .. versionadded:: 1.14.0

    See Also
    --------
    save : Save an array to a binary file in NumPy ``.npy`` format
    savez : Save several arrays into an uncompressed ``.npz`` archive
    savez_compressed : Save several arrays into a compressed ``.npz`` archive

    Notes
    -----
    Further explanation of the `fmt` parameter
    (``%[flag]width[.precision]specifier``):

    flags:
        ``-`` : left justify

        ``+`` : Forces to precede result with + or -.

        ``0`` : Left pad the number with zeros instead of space (see width).

    width:
        Minimum number of characters to be printed. The value is not truncated
        if it has more characters.

    precision:
        - For integer specifiers (eg. ``d,i,o,x``), the minimum number of
          digits.
        - For ``e, E`` and ``f`` specifiers, the number of digits to print
          after the decimal point.
        - For ``g`` and ``G``, the maximum number of significant digits.
        - For ``s``, the maximum number of characters.

    specifiers:
        ``c`` : character

        ``d`` or ``i`` : signed decimal integer

        ``e`` or ``E`` : scientific notation with ``e`` or ``E``.

        ``f`` : decimal floating point

        ``g,G`` : use the shorter of ``e,E`` or ``f``

        ``o`` : signed octal

        ``s`` : string of characters

        ``u`` : unsigned decimal integer

        ``x,X`` : unsigned hexadecimal integer

    This explanation of ``fmt`` is not complete, for an exhaustive
    specification see [1]_.

    References
    ----------
    .. [1] `Format Specification Mini-Language
           <https://docs.python.org/library/string.html#format-specification-mini-language>`_,
           Python Documentation.

    Examples
    --------
    >>> x = y = z = np.arange(0.0,5.0,1.0)
    >>> np.savetxt('test.out', x, delimiter=',')   # X is an array
    >>> np.savetxt('test.out', (x,y,z))   # x,y,z equal sized 1D arrays
    >>> np.savetxt('test.out', x, fmt='%1.4e')   # use exponential notation

    """
    if isinstance(fmt, bytes):
        fmt = asstr(fmt)
    delimiter = asstr(delimiter)

    class WriteWrap(object):
        __doc__ = 'Convert to unicode in py2 or to bytes on bytestream inputs.\n\n        '

        def __init__(self, fh, encoding):
            self.fh = fh
            self.encoding = encoding
            self.do_write = self.first_write

        def close(self):
            self.fh.close()

        def write(self, v):
            self.do_write(v)

        def write_bytes(self, v):
            if isinstance(v, bytes):
                self.fh.write(v)
            else:
                self.fh.write(v.encode(self.encoding))

        def write_normal(self, v):
            self.fh.write(asunicode(v))

        def first_write(self, v):
            try:
                self.write_normal(v)
                self.write = self.write_normal
            except TypeError:
                self.write_bytes(v)
                self.write = self.write_bytes

    own_fh = False
    if isinstance(fname, os_PathLike):
        fname = os_fspath(fname)
    if _is_string_like(fname):
        open(fname, 'wt').close()
        fh = np.lib._datasource.open(fname, 'wt', encoding=encoding)
        own_fh = True
        if sys.version_info[0] == 2:
            fh = WriteWrap(fh, encoding or 'latin1')
    elif hasattr(fname, 'write'):
        fh = WriteWrap(fname, encoding or 'latin1')
    else:
        raise ValueError('fname must be a string or file handle')
    try:
        X = np.asarray(X)
        if X.ndim == 0 or X.ndim > 2:
            raise ValueError('Expected 1D or 2D array, got %dD array instead' % X.ndim)
        elif X.ndim == 1:
            if X.dtype.names is None:
                X = np.atleast_2d(X).T
                ncol = 1
            else:
                ncol = len(X.dtype.names)
        else:
            ncol = X.shape[1]
        iscomplex_X = np.iscomplexobj(X)
        if type(fmt) in (list, tuple):
            if len(fmt) != ncol:
                raise AttributeError('fmt has wrong shape.  %s' % str(fmt))
            format = asstr(delimiter).join(map(asstr, fmt))
        elif isinstance(fmt, basestring):
            n_fmt_chars = fmt.count('%')
            error = ValueError('fmt has wrong number of %% formats:  %s' % fmt)
            if n_fmt_chars == 1:
                if iscomplex_X:
                    fmt = [
                     ' (%s+%sj)' % (fmt, fmt)] * ncol
                else:
                    fmt = [
                     fmt] * ncol
                format = delimiter.join(fmt)
            elif iscomplex_X and n_fmt_chars != 2 * ncol:
                raise error
            elif not iscomplex_X or n_fmt_chars != ncol:
                raise error
            else:
                format = fmt
        else:
            raise ValueError('invalid fmt: %r' % (fmt,))
        if len(header) > 0:
            header = header.replace('\n', '\n' + comments)
            fh.write(comments + header + newline)
        if iscomplex_X:
            for row in X:
                row2 = []
                for number in row:
                    row2.append(number.real)
                    row2.append(number.imag)
                else:
                    s = format % tuple(row2) + newline
                    fh.write(s.replace('+-', '-'))

        else:
            pass
        for row in X:
            try:
                v = format % tuple(row) + newline
            except TypeError:
                raise TypeError("Mismatch between array dtype ('%s') and format specifier ('%s')" % (
                 str(X.dtype), format))
            else:
                fh.write(v)
        else:
            if len(footer) > 0:
                footer = footer.replace('\n', '\n' + comments)
                fh.write(comments + footer + newline)

    finally:
        if own_fh:
            fh.close()


@set_module('numpy')
def fromregex--- This code section failed: ---

 L.1522         0  LOAD_CONST               False
                2  STORE_FAST               'own_fh'

 L.1523         4  LOAD_GLOBAL              hasattr
                6  LOAD_FAST                'file'
                8  LOAD_STR                 'read'
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_TRUE     38  'to 38'

 L.1524        14  LOAD_GLOBAL              np
               16  LOAD_ATTR                lib
               18  LOAD_ATTR                _datasource
               20  LOAD_ATTR                open
               22  LOAD_FAST                'file'
               24  LOAD_STR                 'rt'
               26  LOAD_FAST                'encoding'
               28  LOAD_CONST               ('encoding',)
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  STORE_FAST               'file'

 L.1525        34  LOAD_CONST               True
               36  STORE_FAST               'own_fh'
             38_0  COME_FROM            12  '12'

 L.1527        38  SETUP_FINALLY       248  'to 248'

 L.1528        40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'dtype'
               44  LOAD_GLOBAL              np
               46  LOAD_ATTR                dtype
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_TRUE     62  'to 62'

 L.1529        52  LOAD_GLOBAL              np
               54  LOAD_METHOD              dtype
               56  LOAD_FAST                'dtype'
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'dtype'
             62_0  COME_FROM            50  '50'

 L.1531        62  LOAD_FAST                'file'
               64  LOAD_METHOD              read
               66  CALL_METHOD_0         0  ''
               68  STORE_FAST               'content'

 L.1532        70  LOAD_GLOBAL              isinstance
               72  LOAD_FAST                'content'
               74  LOAD_GLOBAL              bytes
               76  CALL_FUNCTION_2       2  ''
               78  POP_JUMP_IF_FALSE   104  'to 104'
               80  LOAD_GLOBAL              isinstance
               82  LOAD_FAST                'regexp'
               84  LOAD_GLOBAL              np
               86  LOAD_ATTR                compat
               88  LOAD_ATTR                unicode
               90  CALL_FUNCTION_2       2  ''
               92  POP_JUMP_IF_FALSE   104  'to 104'

 L.1533        94  LOAD_GLOBAL              asbytes
               96  LOAD_FAST                'regexp'
               98  CALL_FUNCTION_1       1  ''
              100  STORE_FAST               'regexp'
              102  JUMP_FORWARD        136  'to 136'
            104_0  COME_FROM            92  '92'
            104_1  COME_FROM            78  '78'

 L.1534       104  LOAD_GLOBAL              isinstance
              106  LOAD_FAST                'content'
              108  LOAD_GLOBAL              np
              110  LOAD_ATTR                compat
              112  LOAD_ATTR                unicode
              114  CALL_FUNCTION_2       2  ''
              116  POP_JUMP_IF_FALSE   136  'to 136'
              118  LOAD_GLOBAL              isinstance
              120  LOAD_FAST                'regexp'
              122  LOAD_GLOBAL              bytes
              124  CALL_FUNCTION_2       2  ''
              126  POP_JUMP_IF_FALSE   136  'to 136'

 L.1535       128  LOAD_GLOBAL              asstr
              130  LOAD_FAST                'regexp'
              132  CALL_FUNCTION_1       1  ''
              134  STORE_FAST               'regexp'
            136_0  COME_FROM           126  '126'
            136_1  COME_FROM           116  '116'
            136_2  COME_FROM           102  '102'

 L.1537       136  LOAD_GLOBAL              hasattr
              138  LOAD_FAST                'regexp'
              140  LOAD_STR                 'match'
              142  CALL_FUNCTION_2       2  ''
              144  POP_JUMP_IF_TRUE    156  'to 156'

 L.1538       146  LOAD_GLOBAL              re
              148  LOAD_METHOD              compile
              150  LOAD_FAST                'regexp'
              152  CALL_METHOD_1         1  ''
              154  STORE_FAST               'regexp'
            156_0  COME_FROM           144  '144'

 L.1539       156  LOAD_FAST                'regexp'
              158  LOAD_METHOD              findall
              160  LOAD_FAST                'content'
              162  CALL_METHOD_1         1  ''
              164  STORE_FAST               'seq'

 L.1540       166  LOAD_FAST                'seq'
              168  POP_JUMP_IF_FALSE   226  'to 226'
              170  LOAD_GLOBAL              isinstance
              172  LOAD_FAST                'seq'
              174  LOAD_CONST               0
              176  BINARY_SUBSCR    
              178  LOAD_GLOBAL              tuple
              180  CALL_FUNCTION_2       2  ''
              182  POP_JUMP_IF_TRUE    226  'to 226'

 L.1544       184  LOAD_GLOBAL              np
              186  LOAD_METHOD              dtype
              188  LOAD_FAST                'dtype'
              190  LOAD_FAST                'dtype'
              192  LOAD_ATTR                names
              194  LOAD_CONST               0
              196  BINARY_SUBSCR    
              198  BINARY_SUBSCR    
              200  CALL_METHOD_1         1  ''
              202  STORE_FAST               'newdtype'

 L.1545       204  LOAD_GLOBAL              np
              206  LOAD_ATTR                array
              208  LOAD_FAST                'seq'
              210  LOAD_FAST                'newdtype'
              212  LOAD_CONST               ('dtype',)
              214  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              216  STORE_FAST               'output'

 L.1546       218  LOAD_FAST                'dtype'
              220  LOAD_FAST                'output'
              222  STORE_ATTR               dtype
              224  JUMP_FORWARD        240  'to 240'
            226_0  COME_FROM           182  '182'
            226_1  COME_FROM           168  '168'

 L.1548       226  LOAD_GLOBAL              np
              228  LOAD_ATTR                array
              230  LOAD_FAST                'seq'
              232  LOAD_FAST                'dtype'
              234  LOAD_CONST               ('dtype',)
              236  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              238  STORE_FAST               'output'
            240_0  COME_FROM           224  '224'

 L.1550       240  LOAD_FAST                'output'
              242  POP_BLOCK        
              244  CALL_FINALLY        248  'to 248'
              246  RETURN_VALUE     
            248_0  COME_FROM           244  '244'
            248_1  COME_FROM_FINALLY    38  '38'

 L.1552       248  LOAD_FAST                'own_fh'
          250_252  POP_JUMP_IF_FALSE   262  'to 262'

 L.1553       254  LOAD_FAST                'file'
              256  LOAD_METHOD              close
              258  CALL_METHOD_0         0  ''
              260  POP_TOP          
            262_0  COME_FROM           250  '250'
              262  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 244


@set_module('numpy')
def genfromtxt--- This code section failed: ---

 L.1744         0  LOAD_FAST                'max_rows'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    36  'to 36'

 L.1745         8  LOAD_FAST                'skip_footer'
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.1746        12  LOAD_GLOBAL              ValueError

 L.1747        14  LOAD_STR                 "The keywords 'skip_footer' and 'max_rows' can not be specified at the same time."

 L.1746        16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L.1749        20  LOAD_FAST                'max_rows'
               22  LOAD_CONST               1
               24  COMPARE_OP               <
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L.1750        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 "'max_rows' must be at least 1."
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'
             36_1  COME_FROM             6  '6'

 L.1752        36  LOAD_FAST                'usemask'
               38  POP_JUMP_IF_FALSE    56  'to 56'

 L.1753        40  LOAD_CONST               0
               42  LOAD_CONST               ('MaskedArray', 'make_mask_descr')
               44  IMPORT_NAME_ATTR         numpy.ma
               46  IMPORT_FROM              MaskedArray
               48  STORE_FAST               'MaskedArray'
               50  IMPORT_FROM              make_mask_descr
               52  STORE_FAST               'make_mask_descr'
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L.1755        56  LOAD_FAST                'converters'
               58  JUMP_IF_TRUE_OR_POP    62  'to 62'
               60  BUILD_MAP_0           0 
             62_0  COME_FROM            58  '58'
               62  STORE_FAST               'user_converters'

 L.1756        64  LOAD_GLOBAL              isinstance
               66  LOAD_FAST                'user_converters'
               68  LOAD_GLOBAL              dict
               70  CALL_FUNCTION_2       2  ''
               72  POP_JUMP_IF_TRUE     90  'to 90'

 L.1757        74  LOAD_GLOBAL              TypeError

 L.1758        76  LOAD_STR                 "The input argument 'converter' should be a valid dictionary (got '%s' instead)"

 L.1759        78  LOAD_GLOBAL              type
               80  LOAD_FAST                'user_converters'
               82  CALL_FUNCTION_1       1  ''

 L.1758        84  BINARY_MODULO    

 L.1757        86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            72  '72'

 L.1761        90  LOAD_FAST                'encoding'
               92  LOAD_STR                 'bytes'
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   108  'to 108'

 L.1762        98  LOAD_CONST               None
              100  STORE_FAST               'encoding'

 L.1763       102  LOAD_CONST               True
              104  STORE_FAST               'byte_converters'
              106  JUMP_FORWARD        112  'to 112'
            108_0  COME_FROM            96  '96'

 L.1765       108  LOAD_CONST               False
              110  STORE_FAST               'byte_converters'
            112_0  COME_FROM           106  '106'

 L.1768       112  SETUP_FINALLY       198  'to 198'

 L.1769       114  LOAD_GLOBAL              isinstance
              116  LOAD_FAST                'fname'
              118  LOAD_GLOBAL              os_PathLike
              120  CALL_FUNCTION_2       2  ''
              122  POP_JUMP_IF_FALSE   132  'to 132'

 L.1770       124  LOAD_GLOBAL              os_fspath
              126  LOAD_FAST                'fname'
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'fname'
            132_0  COME_FROM           122  '122'

 L.1771       132  LOAD_GLOBAL              isinstance
              134  LOAD_FAST                'fname'
              136  LOAD_GLOBAL              basestring
              138  CALL_FUNCTION_2       2  ''
              140  POP_JUMP_IF_FALSE   174  'to 174'

 L.1772       142  LOAD_GLOBAL              np
              144  LOAD_ATTR                lib
              146  LOAD_ATTR                _datasource
              148  LOAD_ATTR                open
              150  LOAD_FAST                'fname'
              152  LOAD_STR                 'rt'
              154  LOAD_FAST                'encoding'
              156  LOAD_CONST               ('encoding',)
              158  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              160  STORE_FAST               'fid'

 L.1773       162  LOAD_GLOBAL              contextlib
              164  LOAD_METHOD              closing
              166  LOAD_FAST                'fid'
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'fid_ctx'
              172  JUMP_FORWARD        186  'to 186'
            174_0  COME_FROM           140  '140'

 L.1775       174  LOAD_FAST                'fname'
              176  STORE_FAST               'fid'

 L.1776       178  LOAD_GLOBAL              contextlib_nullcontext
              180  LOAD_FAST                'fid'
              182  CALL_FUNCTION_1       1  ''
              184  STORE_FAST               'fid_ctx'
            186_0  COME_FROM           172  '172'

 L.1777       186  LOAD_GLOBAL              iter
              188  LOAD_FAST                'fid'
              190  CALL_FUNCTION_1       1  ''
              192  STORE_FAST               'fhd'
              194  POP_BLOCK        
              196  JUMP_FORWARD        234  'to 234'
            198_0  COME_FROM_FINALLY   112  '112'

 L.1778       198  DUP_TOP          
              200  LOAD_GLOBAL              TypeError
              202  COMPARE_OP               exception-match
              204  POP_JUMP_IF_FALSE   232  'to 232'
              206  POP_TOP          
              208  POP_TOP          
              210  POP_TOP          

 L.1779       212  LOAD_GLOBAL              TypeError

 L.1780       214  LOAD_STR                 'fname must be a string, filehandle, list of strings, or generator. Got %s instead.'

 L.1781       216  LOAD_GLOBAL              type
              218  LOAD_FAST                'fname'
              220  CALL_FUNCTION_1       1  ''

 L.1780       222  BINARY_MODULO    

 L.1779       224  CALL_FUNCTION_1       1  ''
              226  RAISE_VARARGS_1       1  'exception instance'
              228  POP_EXCEPT       
              230  JUMP_FORWARD        234  'to 234'
            232_0  COME_FROM           204  '204'
              232  END_FINALLY      
            234_0  COME_FROM           230  '230'
            234_1  COME_FROM           196  '196'

 L.1783       234  LOAD_FAST                'fid_ctx'
          236_238  SETUP_WITH         2274  'to 2274'
              240  POP_TOP          

 L.1784       242  LOAD_GLOBAL              LineSplitter
              244  LOAD_FAST                'delimiter'
              246  LOAD_FAST                'comments'

 L.1785       248  LOAD_FAST                'autostrip'

 L.1785       250  LOAD_FAST                'encoding'

 L.1784       252  LOAD_CONST               ('delimiter', 'comments', 'autostrip', 'encoding')
              254  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              256  STORE_FAST               'split_line'

 L.1786       258  LOAD_GLOBAL              NameValidator
              260  LOAD_FAST                'excludelist'

 L.1787       262  LOAD_FAST                'deletechars'

 L.1788       264  LOAD_FAST                'case_sensitive'

 L.1789       266  LOAD_FAST                'replace_space'

 L.1786       268  LOAD_CONST               ('excludelist', 'deletechars', 'case_sensitive', 'replace_space')
              270  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              272  STORE_FAST               'validate_names'

 L.1792       274  SETUP_FINALLY       394  'to 394'

 L.1793       276  LOAD_GLOBAL              range
              278  LOAD_DEREF               'skip_header'
              280  CALL_FUNCTION_1       1  ''
              282  GET_ITER         
            284_0  COME_FROM           296  '296'
              284  FOR_ITER            300  'to 300'
              286  STORE_DEREF              'i'

 L.1794       288  LOAD_GLOBAL              next
              290  LOAD_FAST                'fhd'
              292  CALL_FUNCTION_1       1  ''
              294  POP_TOP          
          296_298  JUMP_BACK           284  'to 284'
            300_0  COME_FROM           284  '284'

 L.1797       300  LOAD_CONST               None
              302  STORE_FAST               'first_values'
            304_0  COME_FROM           386  '386'

 L.1799       304  LOAD_FAST                'first_values'
          306_308  POP_JUMP_IF_TRUE    390  'to 390'

 L.1800       310  LOAD_GLOBAL              _decode_line
              312  LOAD_GLOBAL              next
              314  LOAD_FAST                'fhd'
              316  CALL_FUNCTION_1       1  ''
              318  LOAD_FAST                'encoding'
              320  CALL_FUNCTION_2       2  ''
              322  STORE_FAST               'first_line'

 L.1801       324  LOAD_DEREF               'names'
              326  LOAD_CONST               True
              328  COMPARE_OP               is
          330_332  POP_JUMP_IF_FALSE   378  'to 378'
              334  LOAD_FAST                'comments'
              336  LOAD_CONST               None
              338  COMPARE_OP               is-not
          340_342  POP_JUMP_IF_FALSE   378  'to 378'

 L.1802       344  LOAD_FAST                'comments'
              346  LOAD_FAST                'first_line'
              348  COMPARE_OP               in
          350_352  POP_JUMP_IF_FALSE   378  'to 378'

 L.1804       354  LOAD_STR                 ''
              356  LOAD_METHOD              join
              358  LOAD_FAST                'first_line'
              360  LOAD_METHOD              split
              362  LOAD_FAST                'comments'
              364  CALL_METHOD_1         1  ''
              366  LOAD_CONST               1
              368  LOAD_CONST               None
              370  BUILD_SLICE_2         2 
              372  BINARY_SUBSCR    
              374  CALL_METHOD_1         1  ''

 L.1803       376  STORE_FAST               'first_line'
            378_0  COME_FROM           350  '350'
            378_1  COME_FROM           340  '340'
            378_2  COME_FROM           330  '330'

 L.1805       378  LOAD_FAST                'split_line'
              380  LOAD_FAST                'first_line'
              382  CALL_FUNCTION_1       1  ''
              384  STORE_FAST               'first_values'
          386_388  JUMP_BACK           304  'to 304'
            390_0  COME_FROM           306  '306'
              390  POP_BLOCK        
              392  JUMP_FORWARD        442  'to 442'
            394_0  COME_FROM_FINALLY   274  '274'

 L.1806       394  DUP_TOP          
              396  LOAD_GLOBAL              StopIteration
              398  COMPARE_OP               exception-match
          400_402  POP_JUMP_IF_FALSE   440  'to 440'
              404  POP_TOP          
              406  POP_TOP          
              408  POP_TOP          

 L.1808       410  LOAD_STR                 ''
              412  STORE_FAST               'first_line'

 L.1809       414  BUILD_LIST_0          0 
              416  STORE_FAST               'first_values'

 L.1810       418  LOAD_GLOBAL              warnings
              420  LOAD_ATTR                warn
              422  LOAD_STR                 'genfromtxt: Empty input file: "%s"'
              424  LOAD_FAST                'fname'
              426  BINARY_MODULO    
              428  LOAD_CONST               2
              430  LOAD_CONST               ('stacklevel',)
              432  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              434  POP_TOP          
              436  POP_EXCEPT       
              438  JUMP_FORWARD        442  'to 442'
            440_0  COME_FROM           400  '400'
              440  END_FINALLY      
            442_0  COME_FROM           438  '438'
            442_1  COME_FROM           392  '392'

 L.1813       442  LOAD_DEREF               'names'
              444  LOAD_CONST               True
              446  COMPARE_OP               is
          448_450  POP_JUMP_IF_FALSE   490  'to 490'

 L.1814       452  LOAD_FAST                'first_values'
              454  LOAD_CONST               0
              456  BINARY_SUBSCR    
              458  LOAD_METHOD              strip
              460  CALL_METHOD_0         0  ''
              462  STORE_FAST               'fval'

 L.1815       464  LOAD_FAST                'comments'
              466  LOAD_CONST               None
              468  COMPARE_OP               is-not
          470_472  POP_JUMP_IF_FALSE   490  'to 490'

 L.1816       474  LOAD_FAST                'fval'
              476  LOAD_FAST                'comments'
              478  COMPARE_OP               in
          480_482  POP_JUMP_IF_FALSE   490  'to 490'

 L.1817       484  LOAD_FAST                'first_values'
              486  LOAD_CONST               0
              488  DELETE_SUBSCR    
            490_0  COME_FROM           480  '480'
            490_1  COME_FROM           470  '470'
            490_2  COME_FROM           448  '448'

 L.1820       490  LOAD_FAST                'usecols'
              492  LOAD_CONST               None
              494  COMPARE_OP               is-not
          496_498  POP_JUMP_IF_FALSE   590  'to 590'

 L.1821       500  SETUP_FINALLY       526  'to 526'

 L.1822       502  LOAD_LISTCOMP            '<code_object <listcomp>>'
              504  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
              506  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              508  LOAD_FAST                'usecols'
              510  LOAD_METHOD              split
              512  LOAD_STR                 ','
              514  CALL_METHOD_1         1  ''
              516  GET_ITER         
              518  CALL_FUNCTION_1       1  ''
              520  STORE_FAST               'usecols'
              522  POP_BLOCK        
              524  JUMP_FORWARD        590  'to 590'
            526_0  COME_FROM_FINALLY   500  '500'

 L.1823       526  DUP_TOP          
              528  LOAD_GLOBAL              AttributeError
              530  COMPARE_OP               exception-match
          532_534  POP_JUMP_IF_FALSE   588  'to 588'
              536  POP_TOP          
              538  POP_TOP          
              540  POP_TOP          

 L.1824       542  SETUP_FINALLY       556  'to 556'

 L.1825       544  LOAD_GLOBAL              list
              546  LOAD_FAST                'usecols'
              548  CALL_FUNCTION_1       1  ''
              550  STORE_FAST               'usecols'
              552  POP_BLOCK        
              554  JUMP_FORWARD        584  'to 584'
            556_0  COME_FROM_FINALLY   542  '542'

 L.1826       556  DUP_TOP          
              558  LOAD_GLOBAL              TypeError
              560  COMPARE_OP               exception-match
          562_564  POP_JUMP_IF_FALSE   582  'to 582'
              566  POP_TOP          
              568  POP_TOP          
              570  POP_TOP          

 L.1827       572  LOAD_FAST                'usecols'
              574  BUILD_LIST_1          1 
              576  STORE_FAST               'usecols'
              578  POP_EXCEPT       
              580  JUMP_FORWARD        584  'to 584'
            582_0  COME_FROM           562  '562'
              582  END_FINALLY      
            584_0  COME_FROM           580  '580'
            584_1  COME_FROM           554  '554'
              584  POP_EXCEPT       
              586  JUMP_FORWARD        590  'to 590'
            588_0  COME_FROM           532  '532'
              588  END_FINALLY      
            590_0  COME_FROM           586  '586'
            590_1  COME_FROM           524  '524'
            590_2  COME_FROM           496  '496'

 L.1828       590  LOAD_GLOBAL              len
              592  LOAD_FAST                'usecols'
          594_596  JUMP_IF_TRUE_OR_POP   600  'to 600'
              598  LOAD_FAST                'first_values'
            600_0  COME_FROM           594  '594'
              600  CALL_FUNCTION_1       1  ''
              602  STORE_FAST               'nbcols'

 L.1831       604  LOAD_DEREF               'names'
              606  LOAD_CONST               True
              608  COMPARE_OP               is
          610_612  POP_JUMP_IF_FALSE   638  'to 638'

 L.1832       614  LOAD_FAST                'validate_names'
              616  LOAD_LISTCOMP            '<code_object <listcomp>>'
              618  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
              620  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              622  LOAD_FAST                'first_values'
              624  GET_ITER         
              626  CALL_FUNCTION_1       1  ''
              628  CALL_FUNCTION_1       1  ''
              630  STORE_DEREF              'names'

 L.1833       632  LOAD_STR                 ''
              634  STORE_FAST               'first_line'
              636  JUMP_FORWARD        688  'to 688'
            638_0  COME_FROM           610  '610'

 L.1834       638  LOAD_GLOBAL              _is_string_like
              640  LOAD_DEREF               'names'
              642  CALL_FUNCTION_1       1  ''
          644_646  POP_JUMP_IF_FALSE   674  'to 674'

 L.1835       648  LOAD_FAST                'validate_names'
              650  LOAD_LISTCOMP            '<code_object <listcomp>>'
              652  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
              654  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              656  LOAD_DEREF               'names'
              658  LOAD_METHOD              split
              660  LOAD_STR                 ','
              662  CALL_METHOD_1         1  ''
              664  GET_ITER         
              666  CALL_FUNCTION_1       1  ''
              668  CALL_FUNCTION_1       1  ''
              670  STORE_DEREF              'names'
              672  JUMP_FORWARD        688  'to 688'
            674_0  COME_FROM           644  '644'

 L.1836       674  LOAD_DEREF               'names'
          676_678  POP_JUMP_IF_FALSE   688  'to 688'

 L.1837       680  LOAD_FAST                'validate_names'
              682  LOAD_DEREF               'names'
              684  CALL_FUNCTION_1       1  ''
              686  STORE_DEREF              'names'
            688_0  COME_FROM           676  '676'
            688_1  COME_FROM           672  '672'
            688_2  COME_FROM           636  '636'

 L.1839       688  LOAD_DEREF               'dtype'
              690  LOAD_CONST               None
              692  COMPARE_OP               is-not
          694_696  POP_JUMP_IF_FALSE   720  'to 720'

 L.1840       698  LOAD_GLOBAL              easy_dtype
              700  LOAD_DEREF               'dtype'
              702  LOAD_DEREF               'defaultfmt'
              704  LOAD_DEREF               'names'

 L.1841       706  LOAD_FAST                'excludelist'

 L.1842       708  LOAD_FAST                'deletechars'

 L.1843       710  LOAD_FAST                'case_sensitive'

 L.1844       712  LOAD_FAST                'replace_space'

 L.1840       714  LOAD_CONST               ('defaultfmt', 'names', 'excludelist', 'deletechars', 'case_sensitive', 'replace_space')
              716  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              718  STORE_DEREF              'dtype'
            720_0  COME_FROM           694  '694'

 L.1846       720  LOAD_DEREF               'names'
              722  LOAD_CONST               None
              724  COMPARE_OP               is-not
          726_728  POP_JUMP_IF_FALSE   738  'to 738'

 L.1847       730  LOAD_GLOBAL              list
              732  LOAD_DEREF               'names'
              734  CALL_FUNCTION_1       1  ''
              736  STORE_DEREF              'names'
            738_0  COME_FROM           726  '726'

 L.1849       738  LOAD_FAST                'usecols'
          740_742  POP_JUMP_IF_FALSE   926  'to 926'

 L.1850       744  LOAD_GLOBAL              enumerate
              746  LOAD_FAST                'usecols'
              748  CALL_FUNCTION_1       1  ''
              750  GET_ITER         
            752_0  COME_FROM           812  '812'
            752_1  COME_FROM           792  '792'
            752_2  COME_FROM           784  '784'
              752  FOR_ITER            816  'to 816'
              754  UNPACK_SEQUENCE_2     2 
              756  STORE_DEREF              'i'
              758  STORE_FAST               'current'

 L.1852       760  LOAD_GLOBAL              _is_string_like
              762  LOAD_FAST                'current'
              764  CALL_FUNCTION_1       1  ''
          766_768  POP_JUMP_IF_FALSE   786  'to 786'

 L.1853       770  LOAD_DEREF               'names'
              772  LOAD_METHOD              index
              774  LOAD_FAST                'current'
              776  CALL_METHOD_1         1  ''
              778  LOAD_FAST                'usecols'
              780  LOAD_DEREF               'i'
              782  STORE_SUBSCR     
              784  JUMP_BACK           752  'to 752'
            786_0  COME_FROM           766  '766'

 L.1854       786  LOAD_FAST                'current'
              788  LOAD_CONST               0
              790  COMPARE_OP               <
          792_794  POP_JUMP_IF_FALSE_BACK   752  'to 752'

 L.1855       796  LOAD_FAST                'current'
              798  LOAD_GLOBAL              len
              800  LOAD_FAST                'first_values'
              802  CALL_FUNCTION_1       1  ''
              804  BINARY_ADD       
              806  LOAD_FAST                'usecols'
              808  LOAD_DEREF               'i'
              810  STORE_SUBSCR     
          812_814  JUMP_BACK           752  'to 752'
            816_0  COME_FROM           752  '752'

 L.1857       816  LOAD_DEREF               'dtype'
              818  LOAD_CONST               None
              820  COMPARE_OP               is-not
          822_824  POP_JUMP_IF_FALSE   882  'to 882'
              826  LOAD_GLOBAL              len
              828  LOAD_DEREF               'dtype'
              830  CALL_FUNCTION_1       1  ''
              832  LOAD_FAST                'nbcols'
              834  COMPARE_OP               >
          836_838  POP_JUMP_IF_FALSE   882  'to 882'

 L.1858       840  LOAD_DEREF               'dtype'
              842  LOAD_ATTR                descr
              844  STORE_DEREF              'descr'

 L.1859       846  LOAD_GLOBAL              np
              848  LOAD_METHOD              dtype
              850  LOAD_CLOSURE             'descr'
              852  BUILD_TUPLE_1         1 
              854  LOAD_LISTCOMP            '<code_object <listcomp>>'
              856  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
              858  MAKE_FUNCTION_8          'closure'
              860  LOAD_FAST                'usecols'
              862  GET_ITER         
              864  CALL_FUNCTION_1       1  ''
              866  CALL_METHOD_1         1  ''
              868  STORE_DEREF              'dtype'

 L.1860       870  LOAD_GLOBAL              list
              872  LOAD_DEREF               'dtype'
              874  LOAD_ATTR                names
              876  CALL_FUNCTION_1       1  ''
              878  STORE_DEREF              'names'
              880  JUMP_FORWARD        924  'to 924'
            882_0  COME_FROM           836  '836'
            882_1  COME_FROM           822  '822'

 L.1862       882  LOAD_DEREF               'names'
              884  LOAD_CONST               None
              886  COMPARE_OP               is-not
          888_890  POP_JUMP_IF_FALSE   956  'to 956'
              892  LOAD_GLOBAL              len
              894  LOAD_DEREF               'names'
              896  CALL_FUNCTION_1       1  ''
              898  LOAD_FAST                'nbcols'
              900  COMPARE_OP               >
          902_904  POP_JUMP_IF_FALSE   956  'to 956'

 L.1863       906  LOAD_CLOSURE             'names'
              908  BUILD_TUPLE_1         1 
              910  LOAD_LISTCOMP            '<code_object <listcomp>>'
              912  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
              914  MAKE_FUNCTION_8          'closure'
              916  LOAD_FAST                'usecols'
              918  GET_ITER         
              920  CALL_FUNCTION_1       1  ''
              922  STORE_DEREF              'names'
            924_0  COME_FROM           880  '880'
              924  JUMP_FORWARD        956  'to 956'
            926_0  COME_FROM           740  '740'

 L.1864       926  LOAD_DEREF               'names'
              928  LOAD_CONST               None
              930  COMPARE_OP               is-not
          932_934  POP_JUMP_IF_FALSE   956  'to 956'
              936  LOAD_DEREF               'dtype'
              938  LOAD_CONST               None
              940  COMPARE_OP               is-not
          942_944  POP_JUMP_IF_FALSE   956  'to 956'

 L.1865       946  LOAD_GLOBAL              list
              948  LOAD_DEREF               'dtype'
              950  LOAD_ATTR                names
              952  CALL_FUNCTION_1       1  ''
              954  STORE_DEREF              'names'
            956_0  COME_FROM           942  '942'
            956_1  COME_FROM           932  '932'
            956_2  COME_FROM           924  '924'
            956_3  COME_FROM           902  '902'
            956_4  COME_FROM           888  '888'

 L.1869       956  LOAD_FAST                'missing_values'
          958_960  JUMP_IF_TRUE_OR_POP   964  'to 964'
              962  LOAD_CONST               ()
            964_0  COME_FROM           958  '958'
              964  STORE_FAST               'user_missing_values'

 L.1870       966  LOAD_GLOBAL              isinstance
              968  LOAD_FAST                'user_missing_values'
              970  LOAD_GLOBAL              bytes
              972  CALL_FUNCTION_2       2  ''
          974_976  POP_JUMP_IF_FALSE   988  'to 988'

 L.1871       978  LOAD_FAST                'user_missing_values'
              980  LOAD_METHOD              decode
              982  LOAD_STR                 'latin1'
              984  CALL_METHOD_1         1  ''
              986  STORE_FAST               'user_missing_values'
            988_0  COME_FROM           974  '974'

 L.1874       988  LOAD_LISTCOMP            '<code_object <listcomp>>'
              990  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
              992  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              994  LOAD_GLOBAL              range
              996  LOAD_FAST                'nbcols'
              998  CALL_FUNCTION_1       1  ''
             1000  GET_ITER         
             1002  CALL_FUNCTION_1       1  ''
             1004  STORE_FAST               'missing_values'

 L.1877      1006  LOAD_GLOBAL              isinstance
             1008  LOAD_FAST                'user_missing_values'
             1010  LOAD_GLOBAL              dict
             1012  CALL_FUNCTION_2       2  ''
         1014_1016  POP_JUMP_IF_FALSE  1228  'to 1228'

 L.1879      1018  LOAD_FAST                'user_missing_values'
             1020  LOAD_METHOD              items
             1022  CALL_METHOD_0         0  ''
             1024  GET_ITER         
           1026_0  COME_FROM          1222  '1222'
           1026_1  COME_FROM          1206  '1206'
           1026_2  COME_FROM          1078  '1078'
             1026  FOR_ITER           1226  'to 1226'
             1028  UNPACK_SEQUENCE_2     2 
             1030  STORE_FAST               'key'
             1032  STORE_FAST               'val'

 L.1881      1034  LOAD_GLOBAL              _is_string_like
             1036  LOAD_FAST                'key'
             1038  CALL_FUNCTION_1       1  ''
         1040_1042  POP_JUMP_IF_FALSE  1088  'to 1088'

 L.1882      1044  SETUP_FINALLY      1060  'to 1060'

 L.1884      1046  LOAD_DEREF               'names'
             1048  LOAD_METHOD              index
             1050  LOAD_FAST                'key'
             1052  CALL_METHOD_1         1  ''
             1054  STORE_FAST               'key'
             1056  POP_BLOCK        
             1058  JUMP_FORWARD       1088  'to 1088'
           1060_0  COME_FROM_FINALLY  1044  '1044'

 L.1885      1060  DUP_TOP          
             1062  LOAD_GLOBAL              ValueError
             1064  COMPARE_OP               exception-match
         1066_1068  POP_JUMP_IF_FALSE  1086  'to 1086'
             1070  POP_TOP          
             1072  POP_TOP          
             1074  POP_TOP          

 L.1887      1076  POP_EXCEPT       
         1078_1080  JUMP_BACK          1026  'to 1026'
             1082  POP_EXCEPT       
             1084  JUMP_FORWARD       1088  'to 1088'
           1086_0  COME_FROM          1066  '1066'
             1086  END_FINALLY      
           1088_0  COME_FROM          1084  '1084'
           1088_1  COME_FROM          1058  '1058'
           1088_2  COME_FROM          1040  '1040'

 L.1889      1088  LOAD_FAST                'usecols'
         1090_1092  POP_JUMP_IF_FALSE  1132  'to 1132'

 L.1890      1094  SETUP_FINALLY      1110  'to 1110'

 L.1891      1096  LOAD_FAST                'usecols'
             1098  LOAD_METHOD              index
             1100  LOAD_FAST                'key'
             1102  CALL_METHOD_1         1  ''
             1104  STORE_FAST               'key'
             1106  POP_BLOCK        
             1108  JUMP_FORWARD       1132  'to 1132'
           1110_0  COME_FROM_FINALLY  1094  '1094'

 L.1892      1110  DUP_TOP          
             1112  LOAD_GLOBAL              ValueError
             1114  COMPARE_OP               exception-match
         1116_1118  POP_JUMP_IF_FALSE  1130  'to 1130'
             1120  POP_TOP          
             1122  POP_TOP          
             1124  POP_TOP          

 L.1893      1126  POP_EXCEPT       
             1128  BREAK_LOOP         1132  'to 1132'
           1130_0  COME_FROM          1116  '1116'
             1130  END_FINALLY      
           1132_0  COME_FROM          1128  '1128'
           1132_1  COME_FROM          1108  '1108'
           1132_2  COME_FROM          1090  '1090'

 L.1895      1132  LOAD_GLOBAL              isinstance
             1134  LOAD_FAST                'val'
             1136  LOAD_GLOBAL              list
             1138  LOAD_GLOBAL              tuple
             1140  BUILD_TUPLE_2         2 
             1142  CALL_FUNCTION_2       2  ''
         1144_1146  POP_JUMP_IF_FALSE  1164  'to 1164'

 L.1896      1148  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1150  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             1152  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1154  LOAD_FAST                'val'
             1156  GET_ITER         
             1158  CALL_FUNCTION_1       1  ''
             1160  STORE_FAST               'val'
             1162  JUMP_FORWARD       1174  'to 1174'
           1164_0  COME_FROM          1144  '1144'

 L.1898      1164  LOAD_GLOBAL              str
             1166  LOAD_FAST                'val'
             1168  CALL_FUNCTION_1       1  ''
             1170  BUILD_LIST_1          1 
             1172  STORE_FAST               'val'
           1174_0  COME_FROM          1162  '1162'

 L.1900      1174  LOAD_FAST                'key'
             1176  LOAD_CONST               None
             1178  COMPARE_OP               is
         1180_1182  POP_JUMP_IF_FALSE  1208  'to 1208'

 L.1902      1184  LOAD_FAST                'missing_values'
             1186  GET_ITER         
           1188_0  COME_FROM          1202  '1202'
             1188  FOR_ITER           1206  'to 1206'
             1190  STORE_FAST               'miss'

 L.1903      1192  LOAD_FAST                'miss'
             1194  LOAD_METHOD              extend
             1196  LOAD_FAST                'val'
             1198  CALL_METHOD_1         1  ''
             1200  POP_TOP          
         1202_1204  JUMP_BACK          1188  'to 1188'
           1206_0  COME_FROM          1188  '1188'
             1206  JUMP_BACK          1026  'to 1026'
           1208_0  COME_FROM          1180  '1180'

 L.1905      1208  LOAD_FAST                'missing_values'
             1210  LOAD_FAST                'key'
             1212  BINARY_SUBSCR    
             1214  LOAD_METHOD              extend
             1216  LOAD_FAST                'val'
             1218  CALL_METHOD_1         1  ''
             1220  POP_TOP          
         1222_1224  JUMP_BACK          1026  'to 1026'
           1226_0  COME_FROM          1026  '1026'
             1226  JUMP_FORWARD       1370  'to 1370'
           1228_0  COME_FROM          1014  '1014'

 L.1907      1228  LOAD_GLOBAL              isinstance
             1230  LOAD_FAST                'user_missing_values'
             1232  LOAD_GLOBAL              list
             1234  LOAD_GLOBAL              tuple
             1236  BUILD_TUPLE_2         2 
             1238  CALL_FUNCTION_2       2  ''
         1240_1242  POP_JUMP_IF_FALSE  1296  'to 1296'

 L.1908      1244  LOAD_GLOBAL              zip
             1246  LOAD_FAST                'user_missing_values'
             1248  LOAD_FAST                'missing_values'
             1250  CALL_FUNCTION_2       2  ''
             1252  GET_ITER         
           1254_0  COME_FROM          1290  '1290'
           1254_1  COME_FROM          1276  '1276'
             1254  FOR_ITER           1294  'to 1294'
             1256  UNPACK_SEQUENCE_2     2 
             1258  STORE_FAST               'value'
             1260  STORE_FAST               'entry'

 L.1909      1262  LOAD_GLOBAL              str
             1264  LOAD_FAST                'value'
             1266  CALL_FUNCTION_1       1  ''
             1268  STORE_FAST               'value'

 L.1910      1270  LOAD_FAST                'value'
             1272  LOAD_FAST                'entry'
             1274  COMPARE_OP               not-in
         1276_1278  POP_JUMP_IF_FALSE_BACK  1254  'to 1254'

 L.1911      1280  LOAD_FAST                'entry'
             1282  LOAD_METHOD              append
             1284  LOAD_FAST                'value'
             1286  CALL_METHOD_1         1  ''
             1288  POP_TOP          
         1290_1292  JUMP_BACK          1254  'to 1254'
           1294_0  COME_FROM          1254  '1254'
             1294  JUMP_FORWARD       1370  'to 1370'
           1296_0  COME_FROM          1240  '1240'

 L.1913      1296  LOAD_GLOBAL              isinstance
             1298  LOAD_FAST                'user_missing_values'
             1300  LOAD_GLOBAL              basestring
             1302  CALL_FUNCTION_2       2  ''
         1304_1306  POP_JUMP_IF_FALSE  1342  'to 1342'

 L.1914      1308  LOAD_FAST                'user_missing_values'
             1310  LOAD_METHOD              split
             1312  LOAD_STR                 ','
             1314  CALL_METHOD_1         1  ''
             1316  STORE_FAST               'user_value'

 L.1915      1318  LOAD_FAST                'missing_values'
             1320  GET_ITER         
           1322_0  COME_FROM          1336  '1336'
             1322  FOR_ITER           1340  'to 1340'
             1324  STORE_FAST               'entry'

 L.1916      1326  LOAD_FAST                'entry'
             1328  LOAD_METHOD              extend
             1330  LOAD_FAST                'user_value'
             1332  CALL_METHOD_1         1  ''
             1334  POP_TOP          
         1336_1338  JUMP_BACK          1322  'to 1322'
           1340_0  COME_FROM          1322  '1322'
             1340  JUMP_FORWARD       1370  'to 1370'
           1342_0  COME_FROM          1304  '1304'

 L.1919      1342  LOAD_FAST                'missing_values'
             1344  GET_ITER         
           1346_0  COME_FROM          1366  '1366'
             1346  FOR_ITER           1370  'to 1370'
             1348  STORE_FAST               'entry'

 L.1920      1350  LOAD_FAST                'entry'
             1352  LOAD_METHOD              extend
             1354  LOAD_GLOBAL              str
             1356  LOAD_FAST                'user_missing_values'
             1358  CALL_FUNCTION_1       1  ''
             1360  BUILD_LIST_1          1 
             1362  CALL_METHOD_1         1  ''
             1364  POP_TOP          
         1366_1368  JUMP_BACK          1346  'to 1346'
           1370_0  COME_FROM          1346  '1346'
           1370_1  COME_FROM          1340  '1340'
           1370_2  COME_FROM          1294  '1294'
           1370_3  COME_FROM          1226  '1226'

 L.1924      1370  LOAD_FAST                'filling_values'
             1372  STORE_FAST               'user_filling_values'

 L.1925      1374  LOAD_FAST                'user_filling_values'
             1376  LOAD_CONST               None
             1378  COMPARE_OP               is
         1380_1382  POP_JUMP_IF_FALSE  1388  'to 1388'

 L.1926      1384  BUILD_LIST_0          0 
             1386  STORE_FAST               'user_filling_values'
           1388_0  COME_FROM          1380  '1380'

 L.1928      1388  LOAD_CONST               None
             1390  BUILD_LIST_1          1 
             1392  LOAD_FAST                'nbcols'
             1394  BINARY_MULTIPLY  
             1396  STORE_FAST               'filling_values'

 L.1930      1398  LOAD_GLOBAL              isinstance
             1400  LOAD_FAST                'user_filling_values'
             1402  LOAD_GLOBAL              dict
             1404  CALL_FUNCTION_2       2  ''
         1406_1408  POP_JUMP_IF_FALSE  1538  'to 1538'

 L.1931      1410  LOAD_FAST                'user_filling_values'
             1412  LOAD_METHOD              items
             1414  CALL_METHOD_0         0  ''
             1416  GET_ITER         
           1418_0  COME_FROM          1532  '1532'
           1418_1  COME_FROM          1470  '1470'
             1418  FOR_ITER           1536  'to 1536'
             1420  UNPACK_SEQUENCE_2     2 
             1422  STORE_FAST               'key'
             1424  STORE_FAST               'val'

 L.1932      1426  LOAD_GLOBAL              _is_string_like
             1428  LOAD_FAST                'key'
             1430  CALL_FUNCTION_1       1  ''
         1432_1434  POP_JUMP_IF_FALSE  1480  'to 1480'

 L.1933      1436  SETUP_FINALLY      1452  'to 1452'

 L.1935      1438  LOAD_DEREF               'names'
             1440  LOAD_METHOD              index
             1442  LOAD_FAST                'key'
             1444  CALL_METHOD_1         1  ''
             1446  STORE_FAST               'key'
             1448  POP_BLOCK        
             1450  JUMP_FORWARD       1480  'to 1480'
           1452_0  COME_FROM_FINALLY  1436  '1436'

 L.1936      1452  DUP_TOP          
             1454  LOAD_GLOBAL              ValueError
             1456  COMPARE_OP               exception-match
         1458_1460  POP_JUMP_IF_FALSE  1478  'to 1478'
             1462  POP_TOP          
             1464  POP_TOP          
             1466  POP_TOP          

 L.1938      1468  POP_EXCEPT       
         1470_1472  JUMP_BACK          1418  'to 1418'
             1474  POP_EXCEPT       
             1476  JUMP_FORWARD       1480  'to 1480'
           1478_0  COME_FROM          1458  '1458'
             1478  END_FINALLY      
           1480_0  COME_FROM          1476  '1476'
           1480_1  COME_FROM          1450  '1450'
           1480_2  COME_FROM          1432  '1432'

 L.1940      1480  LOAD_FAST                'usecols'
         1482_1484  POP_JUMP_IF_FALSE  1524  'to 1524'

 L.1941      1486  SETUP_FINALLY      1502  'to 1502'

 L.1942      1488  LOAD_FAST                'usecols'
             1490  LOAD_METHOD              index
             1492  LOAD_FAST                'key'
             1494  CALL_METHOD_1         1  ''
             1496  STORE_FAST               'key'
             1498  POP_BLOCK        
             1500  JUMP_FORWARD       1524  'to 1524'
           1502_0  COME_FROM_FINALLY  1486  '1486'

 L.1943      1502  DUP_TOP          
             1504  LOAD_GLOBAL              ValueError
             1506  COMPARE_OP               exception-match
         1508_1510  POP_JUMP_IF_FALSE  1522  'to 1522'
             1512  POP_TOP          
             1514  POP_TOP          
             1516  POP_TOP          

 L.1944      1518  POP_EXCEPT       
             1520  BREAK_LOOP         1524  'to 1524'
           1522_0  COME_FROM          1508  '1508'
             1522  END_FINALLY      
           1524_0  COME_FROM          1520  '1520'
           1524_1  COME_FROM          1500  '1500'
           1524_2  COME_FROM          1482  '1482'

 L.1946      1524  LOAD_FAST                'val'
             1526  LOAD_FAST                'filling_values'
             1528  LOAD_FAST                'key'
             1530  STORE_SUBSCR     
         1532_1534  JUMP_BACK          1418  'to 1418'
           1536_0  COME_FROM          1418  '1418'
             1536  JUMP_FORWARD       1610  'to 1610'
           1538_0  COME_FROM          1406  '1406'

 L.1948      1538  LOAD_GLOBAL              isinstance
             1540  LOAD_FAST                'user_filling_values'
             1542  LOAD_GLOBAL              list
             1544  LOAD_GLOBAL              tuple
             1546  BUILD_TUPLE_2         2 
             1548  CALL_FUNCTION_2       2  ''
         1550_1552  POP_JUMP_IF_FALSE  1600  'to 1600'

 L.1949      1554  LOAD_GLOBAL              len
             1556  LOAD_FAST                'user_filling_values'
             1558  CALL_FUNCTION_1       1  ''
             1560  STORE_FAST               'n'

 L.1950      1562  LOAD_FAST                'n'
             1564  LOAD_FAST                'nbcols'
             1566  COMPARE_OP               <=
         1568_1570  POP_JUMP_IF_FALSE  1586  'to 1586'

 L.1951      1572  LOAD_FAST                'user_filling_values'
             1574  LOAD_FAST                'filling_values'
             1576  LOAD_CONST               None
             1578  LOAD_FAST                'n'
             1580  BUILD_SLICE_2         2 
             1582  STORE_SUBSCR     
             1584  JUMP_FORWARD       1598  'to 1598'
           1586_0  COME_FROM          1568  '1568'

 L.1953      1586  LOAD_FAST                'user_filling_values'
             1588  LOAD_CONST               None
             1590  LOAD_FAST                'nbcols'
             1592  BUILD_SLICE_2         2 
             1594  BINARY_SUBSCR    
             1596  STORE_FAST               'filling_values'
           1598_0  COME_FROM          1584  '1584'
             1598  JUMP_FORWARD       1610  'to 1610'
           1600_0  COME_FROM          1550  '1550'

 L.1956      1600  LOAD_FAST                'user_filling_values'
             1602  BUILD_LIST_1          1 
             1604  LOAD_FAST                'nbcols'
             1606  BINARY_MULTIPLY  
             1608  STORE_FAST               'filling_values'
           1610_0  COME_FROM          1598  '1598'
           1610_1  COME_FROM          1536  '1536'

 L.1959      1610  LOAD_DEREF               'dtype'
             1612  LOAD_CONST               None
             1614  COMPARE_OP               is
         1616_1618  POP_JUMP_IF_FALSE  1642  'to 1642'

 L.1962      1620  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1622  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             1624  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1963      1626  LOAD_GLOBAL              zip
             1628  LOAD_FAST                'missing_values'
             1630  LOAD_FAST                'filling_values'
             1632  CALL_FUNCTION_2       2  ''

 L.1962      1634  GET_ITER         
             1636  CALL_FUNCTION_1       1  ''
             1638  STORE_FAST               'converters'
             1640  JUMP_FORWARD       1724  'to 1724'
           1642_0  COME_FROM          1616  '1616'

 L.1965      1642  LOAD_GLOBAL              flatten_dtype
             1644  LOAD_DEREF               'dtype'
             1646  LOAD_CONST               True
             1648  LOAD_CONST               ('flatten_base',)
             1650  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1652  STORE_FAST               'dtype_flat'

 L.1967      1654  LOAD_GLOBAL              len
             1656  LOAD_FAST                'dtype_flat'
             1658  CALL_FUNCTION_1       1  ''
             1660  LOAD_CONST               1
             1662  COMPARE_OP               >
         1664_1666  POP_JUMP_IF_FALSE  1696  'to 1696'

 L.1969      1668  LOAD_GLOBAL              zip
             1670  LOAD_FAST                'dtype_flat'
             1672  LOAD_FAST                'missing_values'
             1674  LOAD_FAST                'filling_values'
             1676  CALL_FUNCTION_3       3  ''
             1678  STORE_FAST               'zipit'

 L.1970      1680  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1682  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             1684  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1972      1686  LOAD_FAST                'zipit'

 L.1970      1688  GET_ITER         
             1690  CALL_FUNCTION_1       1  ''
             1692  STORE_FAST               'converters'
             1694  JUMP_FORWARD       1724  'to 1724'
           1696_0  COME_FROM          1664  '1664'

 L.1975      1696  LOAD_GLOBAL              zip
             1698  LOAD_FAST                'missing_values'
             1700  LOAD_FAST                'filling_values'
             1702  CALL_FUNCTION_2       2  ''
             1704  STORE_FAST               'zipit'

 L.1976      1706  LOAD_CLOSURE             'dtype'
             1708  BUILD_TUPLE_1         1 
             1710  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1712  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             1714  MAKE_FUNCTION_8          'closure'

 L.1978      1716  LOAD_FAST                'zipit'

 L.1976      1718  GET_ITER         
             1720  CALL_FUNCTION_1       1  ''
             1722  STORE_FAST               'converters'
           1724_0  COME_FROM          1694  '1694'
           1724_1  COME_FROM          1640  '1640'

 L.1980      1724  BUILD_LIST_0          0 
             1726  STORE_FAST               'uc_update'

 L.1981      1728  LOAD_FAST                'user_converters'
             1730  LOAD_METHOD              items
             1732  CALL_METHOD_0         0  ''
             1734  GET_ITER         
           1736_0  COME_FROM          1980  '1980'
           1736_1  COME_FROM          1844  '1844'
           1736_2  COME_FROM          1792  '1792'
             1736  FOR_ITER           1984  'to 1984'
             1738  UNPACK_SEQUENCE_2     2 
             1740  STORE_FAST               'j'
             1742  STORE_DEREF              'conv'

 L.1983      1744  LOAD_GLOBAL              _is_string_like
             1746  LOAD_FAST                'j'
             1748  CALL_FUNCTION_1       1  ''
         1750_1752  POP_JUMP_IF_FALSE  1804  'to 1804'

 L.1984      1754  SETUP_FINALLY      1774  'to 1774'

 L.1985      1756  LOAD_DEREF               'names'
             1758  LOAD_METHOD              index
             1760  LOAD_FAST                'j'
             1762  CALL_METHOD_1         1  ''
             1764  STORE_FAST               'j'

 L.1986      1766  LOAD_FAST                'j'
             1768  STORE_DEREF              'i'
             1770  POP_BLOCK        
             1772  JUMP_FORWARD       1802  'to 1802'
           1774_0  COME_FROM_FINALLY  1754  '1754'

 L.1987      1774  DUP_TOP          
             1776  LOAD_GLOBAL              ValueError
             1778  COMPARE_OP               exception-match
         1780_1782  POP_JUMP_IF_FALSE  1800  'to 1800'
             1784  POP_TOP          
             1786  POP_TOP          
             1788  POP_TOP          

 L.1988      1790  POP_EXCEPT       
         1792_1794  JUMP_BACK          1736  'to 1736'
             1796  POP_EXCEPT       
             1798  JUMP_FORWARD       1802  'to 1802'
           1800_0  COME_FROM          1780  '1780'
             1800  END_FINALLY      
           1802_0  COME_FROM          1798  '1798'
           1802_1  COME_FROM          1772  '1772'
             1802  JUMP_FORWARD       1860  'to 1860'
           1804_0  COME_FROM          1750  '1750'

 L.1989      1804  LOAD_FAST                'usecols'
         1806_1808  POP_JUMP_IF_FALSE  1856  'to 1856'

 L.1990      1810  SETUP_FINALLY      1826  'to 1826'

 L.1991      1812  LOAD_FAST                'usecols'
             1814  LOAD_METHOD              index
             1816  LOAD_FAST                'j'
             1818  CALL_METHOD_1         1  ''
             1820  STORE_DEREF              'i'
             1822  POP_BLOCK        
             1824  JUMP_FORWARD       1854  'to 1854'
           1826_0  COME_FROM_FINALLY  1810  '1810'

 L.1992      1826  DUP_TOP          
             1828  LOAD_GLOBAL              ValueError
             1830  COMPARE_OP               exception-match
         1832_1834  POP_JUMP_IF_FALSE  1852  'to 1852'
             1836  POP_TOP          
             1838  POP_TOP          
             1840  POP_TOP          

 L.1994      1842  POP_EXCEPT       
         1844_1846  JUMP_BACK          1736  'to 1736'
             1848  POP_EXCEPT       
             1850  JUMP_FORWARD       1854  'to 1854'
           1852_0  COME_FROM          1832  '1832'
             1852  END_FINALLY      
           1854_0  COME_FROM          1850  '1850'
           1854_1  COME_FROM          1824  '1824'
             1854  JUMP_FORWARD       1860  'to 1860'
           1856_0  COME_FROM          1806  '1806'

 L.1996      1856  LOAD_FAST                'j'
             1858  STORE_DEREF              'i'
           1860_0  COME_FROM          1854  '1854'
           1860_1  COME_FROM          1802  '1802'

 L.1998      1860  LOAD_GLOBAL              len
             1862  LOAD_FAST                'first_line'
             1864  CALL_FUNCTION_1       1  ''
         1866_1868  POP_JUMP_IF_FALSE  1880  'to 1880'

 L.1999      1870  LOAD_FAST                'first_values'
             1872  LOAD_FAST                'j'
             1874  BINARY_SUBSCR    
             1876  STORE_FAST               'testing_value'
             1878  JUMP_FORWARD       1884  'to 1884'
           1880_0  COME_FROM          1866  '1866'

 L.2001      1880  LOAD_CONST               None
             1882  STORE_FAST               'testing_value'
           1884_0  COME_FROM          1878  '1878'

 L.2002      1884  LOAD_DEREF               'conv'
             1886  LOAD_GLOBAL              bytes
             1888  COMPARE_OP               is
         1890_1892  POP_JUMP_IF_FALSE  1900  'to 1900'

 L.2003      1894  LOAD_GLOBAL              asbytes
             1896  STORE_FAST               'user_conv'
             1898  JUMP_FORWARD       1934  'to 1934'
           1900_0  COME_FROM          1890  '1890'

 L.2004      1900  LOAD_FAST                'byte_converters'
         1902_1904  POP_JUMP_IF_FALSE  1930  'to 1930'

 L.2007      1906  LOAD_CODE                <code_object tobytes_first>
             1908  LOAD_STR                 'genfromtxt.<locals>.tobytes_first'
             1910  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1912  STORE_FAST               'tobytes_first'

 L.2011      1914  LOAD_GLOBAL              functools
             1916  LOAD_ATTR                partial
             1918  LOAD_FAST                'tobytes_first'
             1920  LOAD_DEREF               'conv'
             1922  LOAD_CONST               ('conv',)
             1924  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1926  STORE_FAST               'user_conv'
             1928  JUMP_FORWARD       1934  'to 1934'
           1930_0  COME_FROM          1902  '1902'

 L.2013      1930  LOAD_DEREF               'conv'
             1932  STORE_FAST               'user_conv'
           1934_0  COME_FROM          1928  '1928'
           1934_1  COME_FROM          1898  '1898'

 L.2014      1934  LOAD_FAST                'converters'
             1936  LOAD_DEREF               'i'
             1938  BINARY_SUBSCR    
             1940  LOAD_ATTR                update
             1942  LOAD_FAST                'user_conv'
             1944  LOAD_CONST               True

 L.2015      1946  LOAD_FAST                'testing_value'

 L.2016      1948  LOAD_FAST                'filling_values'
             1950  LOAD_DEREF               'i'
             1952  BINARY_SUBSCR    

 L.2017      1954  LOAD_FAST                'missing_values'
             1956  LOAD_DEREF               'i'
             1958  BINARY_SUBSCR    

 L.2014      1960  LOAD_CONST               ('locked', 'testing_value', 'default', 'missing_values')
             1962  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1964  POP_TOP          

 L.2018      1966  LOAD_FAST                'uc_update'
             1968  LOAD_METHOD              append
             1970  LOAD_DEREF               'i'
             1972  LOAD_FAST                'user_conv'
             1974  BUILD_TUPLE_2         2 
             1976  CALL_METHOD_1         1  ''
             1978  POP_TOP          
         1980_1982  JUMP_BACK          1736  'to 1736'
           1984_0  COME_FROM          1736  '1736'

 L.2020      1984  LOAD_FAST                'user_converters'
             1986  LOAD_METHOD              update
             1988  LOAD_FAST                'uc_update'
             1990  CALL_METHOD_1         1  ''
             1992  POP_TOP          

 L.2027      1994  BUILD_LIST_0          0 
             1996  STORE_DEREF              'rows'

 L.2028      1998  LOAD_DEREF               'rows'
             2000  LOAD_ATTR                append
             2002  STORE_FAST               'append_to_rows'

 L.2030      2004  LOAD_FAST                'usemask'
         2006_2008  POP_JUMP_IF_FALSE  2020  'to 2020'

 L.2031      2010  BUILD_LIST_0          0 
             2012  STORE_FAST               'masks'

 L.2032      2014  LOAD_FAST                'masks'
             2016  LOAD_ATTR                append
             2018  STORE_FAST               'append_to_masks'
           2020_0  COME_FROM          2006  '2006'

 L.2034      2020  BUILD_LIST_0          0 
             2022  STORE_FAST               'invalid'

 L.2035      2024  LOAD_FAST                'invalid'
             2026  LOAD_ATTR                append
             2028  STORE_FAST               'append_to_invalid'

 L.2038      2030  LOAD_GLOBAL              enumerate
             2032  LOAD_GLOBAL              itertools
             2034  LOAD_METHOD              chain
             2036  LOAD_FAST                'first_line'
             2038  BUILD_LIST_1          1 
             2040  LOAD_FAST                'fhd'
             2042  CALL_METHOD_2         2  ''
             2044  CALL_FUNCTION_1       1  ''
             2046  GET_ITER         
           2048_0  COME_FROM          2266  '2266'
           2048_1  COME_FROM          2256  '2256'
           2048_2  COME_FROM          2196  '2196'
           2048_3  COME_FROM          2154  '2154'
           2048_4  COME_FROM          2082  '2082'
             2048  FOR_ITER           2270  'to 2270'
             2050  UNPACK_SEQUENCE_2     2 
             2052  STORE_DEREF              'i'
             2054  STORE_FAST               'line'

 L.2039      2056  LOAD_FAST                'split_line'
             2058  LOAD_FAST                'line'
             2060  CALL_FUNCTION_1       1  ''
             2062  STORE_DEREF              'values'

 L.2040      2064  LOAD_GLOBAL              len
             2066  LOAD_DEREF               'values'
             2068  CALL_FUNCTION_1       1  ''
             2070  STORE_FAST               'nbvalues'

 L.2042      2072  LOAD_FAST                'nbvalues'
             2074  LOAD_CONST               0
             2076  COMPARE_OP               ==
         2078_2080  POP_JUMP_IF_FALSE  2086  'to 2086'

 L.2043  2082_2084  JUMP_BACK          2048  'to 2048'
           2086_0  COME_FROM          2078  '2078'

 L.2044      2086  LOAD_FAST                'usecols'
         2088_2090  POP_JUMP_IF_FALSE  2166  'to 2166'

 L.2046      2092  SETUP_FINALLY      2116  'to 2116'

 L.2047      2094  LOAD_CLOSURE             'values'
             2096  BUILD_TUPLE_1         1 
             2098  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2100  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2102  MAKE_FUNCTION_8          'closure'
             2104  LOAD_FAST                'usecols'
             2106  GET_ITER         
             2108  CALL_FUNCTION_1       1  ''
             2110  STORE_DEREF              'values'
             2112  POP_BLOCK        
             2114  JUMP_FORWARD       2164  'to 2164'
           2116_0  COME_FROM_FINALLY  2092  '2092'

 L.2048      2116  DUP_TOP          
             2118  LOAD_GLOBAL              IndexError
             2120  COMPARE_OP               exception-match
         2122_2124  POP_JUMP_IF_FALSE  2162  'to 2162'
             2126  POP_TOP          
             2128  POP_TOP          
             2130  POP_TOP          

 L.2049      2132  LOAD_FAST                'append_to_invalid'
             2134  LOAD_DEREF               'i'
             2136  LOAD_DEREF               'skip_header'
             2138  BINARY_ADD       
             2140  LOAD_CONST               1
             2142  BINARY_ADD       
             2144  LOAD_FAST                'nbvalues'
             2146  BUILD_TUPLE_2         2 
             2148  CALL_FUNCTION_1       1  ''
             2150  POP_TOP          

 L.2050      2152  POP_EXCEPT       
         2154_2156  JUMP_BACK          2048  'to 2048'
             2158  POP_EXCEPT       
             2160  JUMP_FORWARD       2164  'to 2164'
           2162_0  COME_FROM          2122  '2122'
             2162  END_FINALLY      
           2164_0  COME_FROM          2160  '2160'
           2164_1  COME_FROM          2114  '2114'
             2164  JUMP_FORWARD       2200  'to 2200'
           2166_0  COME_FROM          2088  '2088'

 L.2051      2166  LOAD_FAST                'nbvalues'
             2168  LOAD_FAST                'nbcols'
             2170  COMPARE_OP               !=
         2172_2174  POP_JUMP_IF_FALSE  2200  'to 2200'

 L.2052      2176  LOAD_FAST                'append_to_invalid'
             2178  LOAD_DEREF               'i'
             2180  LOAD_DEREF               'skip_header'
             2182  BINARY_ADD       
             2184  LOAD_CONST               1
             2186  BINARY_ADD       
             2188  LOAD_FAST                'nbvalues'
             2190  BUILD_TUPLE_2         2 
             2192  CALL_FUNCTION_1       1  ''
             2194  POP_TOP          

 L.2053  2196_2198  JUMP_BACK          2048  'to 2048'
           2200_0  COME_FROM          2172  '2172'
           2200_1  COME_FROM          2164  '2164'

 L.2055      2200  LOAD_FAST                'append_to_rows'
             2202  LOAD_GLOBAL              tuple
             2204  LOAD_DEREF               'values'
             2206  CALL_FUNCTION_1       1  ''
             2208  CALL_FUNCTION_1       1  ''
             2210  POP_TOP          

 L.2056      2212  LOAD_FAST                'usemask'
         2214_2216  POP_JUMP_IF_FALSE  2246  'to 2246'

 L.2057      2218  LOAD_FAST                'append_to_masks'
             2220  LOAD_GLOBAL              tuple
             2222  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2224  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2226  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.2058      2228  LOAD_GLOBAL              zip
             2230  LOAD_DEREF               'values'

 L.2059      2232  LOAD_FAST                'missing_values'

 L.2058      2234  CALL_FUNCTION_2       2  ''

 L.2057      2236  GET_ITER         
             2238  CALL_FUNCTION_1       1  ''
             2240  CALL_FUNCTION_1       1  ''
             2242  CALL_FUNCTION_1       1  ''
             2244  POP_TOP          
           2246_0  COME_FROM          2214  '2214'

 L.2060      2246  LOAD_GLOBAL              len
             2248  LOAD_DEREF               'rows'
             2250  CALL_FUNCTION_1       1  ''
             2252  LOAD_FAST                'max_rows'
             2254  COMPARE_OP               ==
         2256_2258  POP_JUMP_IF_FALSE_BACK  2048  'to 2048'

 L.2061      2260  POP_TOP          
         2262_2264  BREAK_LOOP         2270  'to 2270'
         2266_2268  JUMP_BACK          2048  'to 2048'
           2270_0  COME_FROM          2262  '2262'
           2270_1  COME_FROM          2048  '2048'
             2270  POP_BLOCK        
             2272  BEGIN_FINALLY    
           2274_0  COME_FROM_WITH      236  '236'
             2274  WITH_CLEANUP_START
             2276  WITH_CLEANUP_FINISH
             2278  END_FINALLY      

 L.2064      2280  LOAD_DEREF               'dtype'
             2282  LOAD_CONST               None
             2284  COMPARE_OP               is
         2286_2288  POP_JUMP_IF_FALSE  2486  'to 2486'

 L.2065      2290  LOAD_GLOBAL              enumerate
             2292  LOAD_FAST                'converters'
             2294  CALL_FUNCTION_1       1  ''
             2296  GET_ITER         
           2298_0  COME_FROM          2482  '2482'
           2298_1  COME_FROM          2478  '2478'
           2298_2  COME_FROM          2338  '2338'
             2298  FOR_ITER           2486  'to 2486'
             2300  UNPACK_SEQUENCE_2     2 
             2302  STORE_DEREF              'i'
             2304  STORE_FAST               'converter'

 L.2066      2306  LOAD_CLOSURE             'i'
             2308  BUILD_TUPLE_1         1 
             2310  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2312  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2314  MAKE_FUNCTION_8          'closure'
             2316  LOAD_DEREF               'rows'
             2318  GET_ITER         
             2320  CALL_FUNCTION_1       1  ''
             2322  STORE_FAST               'current_column'

 L.2067      2324  SETUP_FINALLY      2340  'to 2340'

 L.2068      2326  LOAD_FAST                'converter'
             2328  LOAD_METHOD              iterupgrade
             2330  LOAD_FAST                'current_column'
             2332  CALL_METHOD_1         1  ''
             2334  POP_TOP          
             2336  POP_BLOCK        
             2338  JUMP_BACK          2298  'to 2298'
           2340_0  COME_FROM_FINALLY  2324  '2324'

 L.2069      2340  DUP_TOP          
             2342  LOAD_GLOBAL              ConverterLockError
             2344  COMPARE_OP               exception-match
         2346_2348  POP_JUMP_IF_FALSE  2480  'to 2480'
             2350  POP_TOP          
             2352  POP_TOP          
             2354  POP_TOP          

 L.2070      2356  LOAD_STR                 'Converter #%i is locked and cannot be upgraded: '
             2358  LOAD_DEREF               'i'
             2360  BINARY_MODULO    
             2362  STORE_FAST               'errmsg'

 L.2071      2364  LOAD_GLOBAL              map
             2366  LOAD_GLOBAL              itemgetter
             2368  LOAD_DEREF               'i'
             2370  CALL_FUNCTION_1       1  ''
             2372  LOAD_DEREF               'rows'
             2374  CALL_FUNCTION_2       2  ''
             2376  STORE_FAST               'current_column'

 L.2072      2378  LOAD_GLOBAL              enumerate
             2380  LOAD_FAST                'current_column'
             2382  CALL_FUNCTION_1       1  ''
             2384  GET_ITER         
           2386_0  COME_FROM          2472  '2472'
           2386_1  COME_FROM          2468  '2468'
           2386_2  COME_FROM          2408  '2408'
             2386  FOR_ITER           2476  'to 2476'
             2388  UNPACK_SEQUENCE_2     2 
             2390  STORE_FAST               'j'
             2392  STORE_FAST               'value'

 L.2073      2394  SETUP_FINALLY      2410  'to 2410'

 L.2074      2396  LOAD_FAST                'converter'
             2398  LOAD_METHOD              upgrade
             2400  LOAD_FAST                'value'
             2402  CALL_METHOD_1         1  ''
             2404  POP_TOP          
             2406  POP_BLOCK        
             2408  JUMP_BACK          2386  'to 2386'
           2410_0  COME_FROM_FINALLY  2394  '2394'

 L.2075      2410  DUP_TOP          
             2412  LOAD_GLOBAL              ConverterError
             2414  LOAD_GLOBAL              ValueError
             2416  BUILD_TUPLE_2         2 
             2418  COMPARE_OP               exception-match
         2420_2422  POP_JUMP_IF_FALSE  2470  'to 2470'
             2424  POP_TOP          
             2426  POP_TOP          
             2428  POP_TOP          

 L.2076      2430  LOAD_FAST                'errmsg'
             2432  LOAD_STR                 "(occurred line #%i for value '%s')"
             2434  INPLACE_ADD      
             2436  STORE_FAST               'errmsg'

 L.2077      2438  LOAD_FAST                'errmsg'
             2440  LOAD_FAST                'j'
             2442  LOAD_CONST               1
             2444  BINARY_ADD       
             2446  LOAD_DEREF               'skip_header'
             2448  BINARY_ADD       
             2450  LOAD_FAST                'value'
             2452  BUILD_TUPLE_2         2 
             2454  INPLACE_MODULO   
             2456  STORE_FAST               'errmsg'

 L.2078      2458  LOAD_GLOBAL              ConverterError
             2460  LOAD_FAST                'errmsg'
             2462  CALL_FUNCTION_1       1  ''
             2464  RAISE_VARARGS_1       1  'exception instance'
             2466  POP_EXCEPT       
             2468  JUMP_BACK          2386  'to 2386'
           2470_0  COME_FROM          2420  '2420'
             2470  END_FINALLY      
         2472_2474  JUMP_BACK          2386  'to 2386'
           2476_0  COME_FROM          2386  '2386'
             2476  POP_EXCEPT       
             2478  JUMP_BACK          2298  'to 2298'
           2480_0  COME_FROM          2346  '2346'
             2480  END_FINALLY      
         2482_2484  JUMP_BACK          2298  'to 2298'
           2486_0  COME_FROM          2298  '2298'
           2486_1  COME_FROM          2286  '2286'

 L.2081      2486  LOAD_GLOBAL              len
             2488  LOAD_FAST                'invalid'
             2490  CALL_FUNCTION_1       1  ''
             2492  STORE_FAST               'nbinvalid'

 L.2082      2494  LOAD_FAST                'nbinvalid'
             2496  LOAD_CONST               0
             2498  COMPARE_OP               >
         2500_2502  POP_JUMP_IF_FALSE  2668  'to 2668'

 L.2083      2504  LOAD_GLOBAL              len
             2506  LOAD_DEREF               'rows'
             2508  CALL_FUNCTION_1       1  ''
             2510  LOAD_FAST                'nbinvalid'
             2512  BINARY_ADD       
             2514  LOAD_FAST                'skip_footer'
             2516  BINARY_SUBTRACT  
             2518  STORE_DEREF              'nbrows'

 L.2085      2520  LOAD_STR                 '    Line #%%i (got %%i columns instead of %i)'
             2522  LOAD_FAST                'nbcols'
             2524  BINARY_MODULO    
             2526  STORE_DEREF              'template'

 L.2086      2528  LOAD_FAST                'skip_footer'
             2530  LOAD_CONST               0
             2532  COMPARE_OP               >
         2534_2536  POP_JUMP_IF_FALSE  2586  'to 2586'

 L.2087      2538  LOAD_GLOBAL              len
             2540  LOAD_CLOSURE             'nbrows'
             2542  LOAD_CLOSURE             'skip_header'
             2544  BUILD_TUPLE_2         2 
             2546  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2548  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2550  MAKE_FUNCTION_8          'closure'
             2552  LOAD_FAST                'invalid'
             2554  GET_ITER         
             2556  CALL_FUNCTION_1       1  ''
             2558  CALL_FUNCTION_1       1  ''
             2560  STORE_FAST               'nbinvalid_skipped'

 L.2089      2562  LOAD_FAST                'invalid'
             2564  LOAD_CONST               None
             2566  LOAD_FAST                'nbinvalid'
             2568  LOAD_FAST                'nbinvalid_skipped'
             2570  BINARY_SUBTRACT  
             2572  BUILD_SLICE_2         2 
             2574  BINARY_SUBSCR    
             2576  STORE_FAST               'invalid'

 L.2090      2578  LOAD_FAST                'skip_footer'
             2580  LOAD_FAST                'nbinvalid_skipped'
             2582  INPLACE_SUBTRACT 
             2584  STORE_FAST               'skip_footer'
           2586_0  COME_FROM          2534  '2534'

 L.2096      2586  LOAD_CLOSURE             'template'
             2588  BUILD_TUPLE_1         1 
             2590  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2592  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2594  MAKE_FUNCTION_8          'closure'

 L.2097      2596  LOAD_FAST                'invalid'

 L.2096      2598  GET_ITER         
             2600  CALL_FUNCTION_1       1  ''
             2602  STORE_FAST               'errmsg'

 L.2098      2604  LOAD_GLOBAL              len
             2606  LOAD_FAST                'errmsg'
             2608  CALL_FUNCTION_1       1  ''
         2610_2612  POP_JUMP_IF_FALSE  2668  'to 2668'

 L.2099      2614  LOAD_FAST                'errmsg'
             2616  LOAD_METHOD              insert
             2618  LOAD_CONST               0
             2620  LOAD_STR                 'Some errors were detected !'
             2622  CALL_METHOD_2         2  ''
             2624  POP_TOP          

 L.2100      2626  LOAD_STR                 '\n'
             2628  LOAD_METHOD              join
             2630  LOAD_FAST                'errmsg'
             2632  CALL_METHOD_1         1  ''
             2634  STORE_FAST               'errmsg'

 L.2102      2636  LOAD_FAST                'invalid_raise'
         2638_2640  POP_JUMP_IF_FALSE  2652  'to 2652'

 L.2103      2642  LOAD_GLOBAL              ValueError
             2644  LOAD_FAST                'errmsg'
             2646  CALL_FUNCTION_1       1  ''
             2648  RAISE_VARARGS_1       1  'exception instance'
             2650  JUMP_FORWARD       2668  'to 2668'
           2652_0  COME_FROM          2638  '2638'

 L.2106      2652  LOAD_GLOBAL              warnings
             2654  LOAD_ATTR                warn
             2656  LOAD_FAST                'errmsg'
             2658  LOAD_GLOBAL              ConversionWarning
             2660  LOAD_CONST               2
             2662  LOAD_CONST               ('stacklevel',)
             2664  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2666  POP_TOP          
           2668_0  COME_FROM          2650  '2650'
           2668_1  COME_FROM          2610  '2610'
           2668_2  COME_FROM          2500  '2500'

 L.2109      2668  LOAD_FAST                'skip_footer'
             2670  LOAD_CONST               0
             2672  COMPARE_OP               >
         2674_2676  POP_JUMP_IF_FALSE  2712  'to 2712'

 L.2110      2678  LOAD_DEREF               'rows'
             2680  LOAD_CONST               None
             2682  LOAD_FAST                'skip_footer'
             2684  UNARY_NEGATIVE   
             2686  BUILD_SLICE_2         2 
             2688  BINARY_SUBSCR    
             2690  STORE_DEREF              'rows'

 L.2111      2692  LOAD_FAST                'usemask'
         2694_2696  POP_JUMP_IF_FALSE  2712  'to 2712'

 L.2112      2698  LOAD_FAST                'masks'
             2700  LOAD_CONST               None
             2702  LOAD_FAST                'skip_footer'
             2704  UNARY_NEGATIVE   
             2706  BUILD_SLICE_2         2 
             2708  BINARY_SUBSCR    
             2710  STORE_FAST               'masks'
           2712_0  COME_FROM          2694  '2694'
           2712_1  COME_FROM          2674  '2674'

 L.2116      2712  LOAD_FAST                'loose'
         2714_2716  POP_JUMP_IF_FALSE  2750  'to 2750'

 L.2117      2718  LOAD_GLOBAL              list

 L.2118      2720  LOAD_GLOBAL              zip
             2722  LOAD_CLOSURE             'rows'
             2724  BUILD_TUPLE_1         1 
             2726  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2728  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2730  MAKE_FUNCTION_8          'closure'

 L.2119      2732  LOAD_GLOBAL              enumerate
             2734  LOAD_FAST                'converters'
             2736  CALL_FUNCTION_1       1  ''

 L.2118      2738  GET_ITER         
             2740  CALL_FUNCTION_1       1  ''
             2742  CALL_FUNCTION_EX      0  'positional arguments only'

 L.2117      2744  CALL_FUNCTION_1       1  ''
             2746  STORE_DEREF              'rows'
             2748  JUMP_FORWARD       2780  'to 2780'
           2750_0  COME_FROM          2714  '2714'

 L.2121      2750  LOAD_GLOBAL              list

 L.2122      2752  LOAD_GLOBAL              zip
             2754  LOAD_CLOSURE             'rows'
             2756  BUILD_TUPLE_1         1 
             2758  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2760  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2762  MAKE_FUNCTION_8          'closure'

 L.2123      2764  LOAD_GLOBAL              enumerate
             2766  LOAD_FAST                'converters'
             2768  CALL_FUNCTION_1       1  ''

 L.2122      2770  GET_ITER         
             2772  CALL_FUNCTION_1       1  ''
             2774  CALL_FUNCTION_EX      0  'positional arguments only'

 L.2121      2776  CALL_FUNCTION_1       1  ''
             2778  STORE_DEREF              'rows'
           2780_0  COME_FROM          2748  '2748'

 L.2126      2780  LOAD_DEREF               'rows'
             2782  STORE_FAST               'data'

 L.2127      2784  LOAD_DEREF               'dtype'
             2786  LOAD_CONST               None
             2788  COMPARE_OP               is
         2790_2792  POP_JUMP_IF_FALSE  3208  'to 3208'

 L.2129      2794  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2796  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2798  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             2800  LOAD_FAST                'converters'
             2802  GET_ITER         
             2804  CALL_FUNCTION_1       1  ''
             2806  STORE_FAST               'column_types'

 L.2131      2808  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2810  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2812  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             2814  LOAD_GLOBAL              enumerate
             2816  LOAD_FAST                'column_types'
             2818  CALL_FUNCTION_1       1  ''
             2820  GET_ITER         
             2822  CALL_FUNCTION_1       1  ''
             2824  STORE_DEREF              'strcolidx'

 L.2134      2826  LOAD_FAST                'byte_converters'
         2828_2830  POP_JUMP_IF_FALSE  2936  'to 2936'
             2832  LOAD_DEREF               'strcolidx'
         2834_2836  POP_JUMP_IF_FALSE  2936  'to 2936'

 L.2136      2838  LOAD_GLOBAL              warnings
             2840  LOAD_ATTR                warn

 L.2137      2842  LOAD_STR                 'Reading unicode strings without specifying the encoding argument is deprecated. Set the encoding, use None for the system default.'

 L.2140      2844  LOAD_GLOBAL              np
             2846  LOAD_ATTR                VisibleDeprecationWarning

 L.2140      2848  LOAD_CONST               2

 L.2136      2850  LOAD_CONST               ('stacklevel',)
             2852  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2854  POP_TOP          

 L.2141      2856  LOAD_CLOSURE             'strcolidx'
             2858  BUILD_TUPLE_1         1 
             2860  LOAD_CODE                <code_object encode_unicode_cols>
             2862  LOAD_STR                 'genfromtxt.<locals>.encode_unicode_cols'
             2864  MAKE_FUNCTION_8          'closure'
             2866  STORE_DEREF              'encode_unicode_cols'

 L.2147      2868  SETUP_FINALLY      2892  'to 2892'

 L.2148      2870  LOAD_CLOSURE             'encode_unicode_cols'
             2872  BUILD_TUPLE_1         1 
             2874  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2876  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2878  MAKE_FUNCTION_8          'closure'
             2880  LOAD_FAST                'data'
             2882  GET_ITER         
             2884  CALL_FUNCTION_1       1  ''
             2886  STORE_FAST               'data'
             2888  POP_BLOCK        
             2890  JUMP_FORWARD       2914  'to 2914'
           2892_0  COME_FROM_FINALLY  2868  '2868'

 L.2149      2892  DUP_TOP          
             2894  LOAD_GLOBAL              UnicodeEncodeError
             2896  COMPARE_OP               exception-match
         2898_2900  POP_JUMP_IF_FALSE  2912  'to 2912'
             2902  POP_TOP          
             2904  POP_TOP          
             2906  POP_TOP          

 L.2150      2908  POP_EXCEPT       
             2910  BREAK_LOOP         2936  'to 2936'
           2912_0  COME_FROM          2898  '2898'
             2912  END_FINALLY      
           2914_0  COME_FROM          2890  '2890'

 L.2152      2914  LOAD_DEREF               'strcolidx'
             2916  GET_ITER         
           2918_0  COME_FROM          2932  '2932'
             2918  FOR_ITER           2936  'to 2936'
             2920  STORE_DEREF              'i'

 L.2153      2922  LOAD_GLOBAL              np
             2924  LOAD_ATTR                bytes_
             2926  LOAD_FAST                'column_types'
             2928  LOAD_DEREF               'i'
             2930  STORE_SUBSCR     
         2932_2934  JUMP_BACK          2918  'to 2918'
           2936_0  COME_FROM          2918  '2918'
           2936_1  COME_FROM          2910  '2910'
           2936_2  COME_FROM          2834  '2834'
           2936_3  COME_FROM          2828  '2828'

 L.2156      2936  LOAD_FAST                'column_types'
             2938  LOAD_CONST               None
             2940  LOAD_CONST               None
             2942  BUILD_SLICE_2         2 
             2944  BINARY_SUBSCR    
             2946  STORE_FAST               'sized_column_types'

 L.2157      2948  LOAD_GLOBAL              enumerate
             2950  LOAD_FAST                'column_types'
             2952  CALL_FUNCTION_1       1  ''
             2954  GET_ITER         
           2956_0  COME_FROM          3014  '3014'
           2956_1  COME_FROM          2976  '2976'
             2956  FOR_ITER           3018  'to 3018'
             2958  UNPACK_SEQUENCE_2     2 
             2960  STORE_DEREF              'i'
             2962  STORE_FAST               'col_type'

 L.2158      2964  LOAD_GLOBAL              np
             2966  LOAD_METHOD              issubdtype
             2968  LOAD_FAST                'col_type'
             2970  LOAD_GLOBAL              np
             2972  LOAD_ATTR                character
             2974  CALL_METHOD_2         2  ''
         2976_2978  POP_JUMP_IF_FALSE_BACK  2956  'to 2956'

 L.2159      2980  LOAD_GLOBAL              max
             2982  LOAD_CLOSURE             'i'
             2984  BUILD_TUPLE_1         1 
             2986  LOAD_GENEXPR             '<code_object <genexpr>>'
             2988  LOAD_STR                 'genfromtxt.<locals>.<genexpr>'
             2990  MAKE_FUNCTION_8          'closure'
             2992  LOAD_FAST                'data'
             2994  GET_ITER         
             2996  CALL_FUNCTION_1       1  ''
             2998  CALL_FUNCTION_1       1  ''
             3000  STORE_FAST               'n_chars'

 L.2160      3002  LOAD_FAST                'col_type'
             3004  LOAD_FAST                'n_chars'
             3006  BUILD_TUPLE_2         2 
             3008  LOAD_FAST                'sized_column_types'
             3010  LOAD_DEREF               'i'
             3012  STORE_SUBSCR     
         3014_3016  JUMP_BACK          2956  'to 2956'
           3018_0  COME_FROM          2956  '2956'

 L.2162      3018  LOAD_DEREF               'names'
             3020  LOAD_CONST               None
             3022  COMPARE_OP               is
         3024_3026  POP_JUMP_IF_FALSE  3132  'to 3132'

 L.2164      3028  LOAD_SETCOMP             '<code_object <setcomp>>'
             3030  LOAD_STR                 'genfromtxt.<locals>.<setcomp>'
             3032  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.2166      3034  LOAD_GLOBAL              zip
             3036  LOAD_FAST                'converters'
             3038  LOAD_FAST                'column_types'
             3040  CALL_FUNCTION_2       2  ''

 L.2164      3042  GET_ITER         
             3044  CALL_FUNCTION_1       1  ''
             3046  STORE_FAST               'base'

 L.2168      3048  LOAD_GLOBAL              len
             3050  LOAD_FAST                'base'
             3052  CALL_FUNCTION_1       1  ''
             3054  LOAD_CONST               1
             3056  COMPARE_OP               ==
         3058_3060  POP_JUMP_IF_FALSE  3080  'to 3080'

 L.2169      3062  LOAD_FAST                'base'
             3064  UNPACK_SEQUENCE_1     1 
             3066  STORE_FAST               'uniform_type'

 L.2170      3068  LOAD_FAST                'uniform_type'
             3070  LOAD_GLOBAL              bool
             3072  ROT_TWO          
             3074  STORE_FAST               'ddtype'
             3076  STORE_FAST               'mdtype'
             3078  JUMP_FORWARD       3130  'to 3130'
           3080_0  COME_FROM          3058  '3058'

 L.2172      3080  LOAD_CLOSURE             'defaultfmt'
             3082  BUILD_TUPLE_1         1 
             3084  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3086  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3088  MAKE_FUNCTION_8          'closure'

 L.2173      3090  LOAD_GLOBAL              enumerate
             3092  LOAD_FAST                'sized_column_types'
             3094  CALL_FUNCTION_1       1  ''

 L.2172      3096  GET_ITER         
             3098  CALL_FUNCTION_1       1  ''
             3100  STORE_FAST               'ddtype'

 L.2174      3102  LOAD_FAST                'usemask'
         3104_3106  POP_JUMP_IF_FALSE  3170  'to 3170'

 L.2175      3108  LOAD_CLOSURE             'defaultfmt'
             3110  BUILD_TUPLE_1         1 
             3112  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3114  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3116  MAKE_FUNCTION_8          'closure'

 L.2176      3118  LOAD_GLOBAL              enumerate
             3120  LOAD_FAST                'sized_column_types'
             3122  CALL_FUNCTION_1       1  ''

 L.2175      3124  GET_ITER         
             3126  CALL_FUNCTION_1       1  ''
             3128  STORE_FAST               'mdtype'
           3130_0  COME_FROM          3078  '3078'
             3130  JUMP_FORWARD       3170  'to 3170'
           3132_0  COME_FROM          3024  '3024'

 L.2178      3132  LOAD_GLOBAL              list
             3134  LOAD_GLOBAL              zip
             3136  LOAD_DEREF               'names'
             3138  LOAD_FAST                'sized_column_types'
             3140  CALL_FUNCTION_2       2  ''
             3142  CALL_FUNCTION_1       1  ''
             3144  STORE_FAST               'ddtype'

 L.2179      3146  LOAD_GLOBAL              list
             3148  LOAD_GLOBAL              zip
             3150  LOAD_DEREF               'names'
             3152  LOAD_GLOBAL              bool
             3154  BUILD_LIST_1          1 
             3156  LOAD_GLOBAL              len
             3158  LOAD_FAST                'sized_column_types'
             3160  CALL_FUNCTION_1       1  ''
             3162  BINARY_MULTIPLY  
             3164  CALL_FUNCTION_2       2  ''
             3166  CALL_FUNCTION_1       1  ''
             3168  STORE_FAST               'mdtype'
           3170_0  COME_FROM          3130  '3130'
           3170_1  COME_FROM          3104  '3104'

 L.2180      3170  LOAD_GLOBAL              np
             3172  LOAD_ATTR                array
             3174  LOAD_FAST                'data'
             3176  LOAD_FAST                'ddtype'
             3178  LOAD_CONST               ('dtype',)
             3180  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3182  STORE_FAST               'output'

 L.2181      3184  LOAD_FAST                'usemask'
         3186_3188  POP_JUMP_IF_FALSE  3640  'to 3640'

 L.2182      3190  LOAD_GLOBAL              np
             3192  LOAD_ATTR                array
             3194  LOAD_FAST                'masks'
             3196  LOAD_FAST                'mdtype'
             3198  LOAD_CONST               ('dtype',)
             3200  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3202  STORE_FAST               'outputmask'
         3204_3206  JUMP_FORWARD       3640  'to 3640'
           3208_0  COME_FROM          2790  '2790'

 L.2185      3208  LOAD_DEREF               'names'
         3210_3212  POP_JUMP_IF_FALSE  3232  'to 3232'
             3214  LOAD_DEREF               'dtype'
             3216  LOAD_ATTR                names
             3218  LOAD_CONST               None
             3220  COMPARE_OP               is-not
         3222_3224  POP_JUMP_IF_FALSE  3232  'to 3232'

 L.2186      3226  LOAD_DEREF               'names'
             3228  LOAD_DEREF               'dtype'
             3230  STORE_ATTR               names
           3232_0  COME_FROM          3222  '3222'
           3232_1  COME_FROM          3210  '3210'

 L.2188      3232  LOAD_GLOBAL              len
             3234  LOAD_FAST                'dtype_flat'
             3236  CALL_FUNCTION_1       1  ''
             3238  LOAD_CONST               1
             3240  COMPARE_OP               >
         3242_3244  POP_JUMP_IF_FALSE  3392  'to 3392'

 L.2193      3246  LOAD_STR                 'O'
             3248  LOAD_GENEXPR             '<code_object <genexpr>>'
             3250  LOAD_STR                 'genfromtxt.<locals>.<genexpr>'
             3252  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3254  LOAD_FAST                'dtype_flat'
             3256  GET_ITER         
             3258  CALL_FUNCTION_1       1  ''
             3260  COMPARE_OP               in
         3262_3264  POP_JUMP_IF_FALSE  3302  'to 3302'

 L.2194      3266  LOAD_GLOBAL              has_nested_fields
             3268  LOAD_DEREF               'dtype'
             3270  CALL_FUNCTION_1       1  ''
         3272_3274  POP_JUMP_IF_FALSE  3286  'to 3286'

 L.2195      3276  LOAD_GLOBAL              NotImplementedError

 L.2196      3278  LOAD_STR                 'Nested fields involving objects are not supported...'

 L.2195      3280  CALL_FUNCTION_1       1  ''
             3282  RAISE_VARARGS_1       1  'exception instance'
             3284  JUMP_FORWARD       3300  'to 3300'
           3286_0  COME_FROM          3272  '3272'

 L.2198      3286  LOAD_GLOBAL              np
             3288  LOAD_ATTR                array
             3290  LOAD_FAST                'data'
             3292  LOAD_DEREF               'dtype'
             3294  LOAD_CONST               ('dtype',)
             3296  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3298  STORE_FAST               'output'
           3300_0  COME_FROM          3284  '3284'
             3300  JUMP_FORWARD       3336  'to 3336'
           3302_0  COME_FROM          3262  '3262'

 L.2200      3302  LOAD_GLOBAL              np
             3304  LOAD_ATTR                array
             3306  LOAD_FAST                'data'
             3308  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3310  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3312  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3314  LOAD_FAST                'dtype_flat'
             3316  GET_ITER         
             3318  CALL_FUNCTION_1       1  ''
             3320  LOAD_CONST               ('dtype',)
             3322  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3324  STORE_DEREF              'rows'

 L.2201      3326  LOAD_DEREF               'rows'
             3328  LOAD_METHOD              view
             3330  LOAD_DEREF               'dtype'
             3332  CALL_METHOD_1         1  ''
             3334  STORE_FAST               'output'
           3336_0  COME_FROM          3300  '3300'

 L.2203      3336  LOAD_FAST                'usemask'
         3338_3340  POP_JUMP_IF_FALSE  3640  'to 3640'

 L.2204      3342  LOAD_GLOBAL              np
             3344  LOAD_ATTR                array

 L.2205      3346  LOAD_FAST                'masks'

 L.2205      3348  LOAD_GLOBAL              np
             3350  LOAD_METHOD              dtype
             3352  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3354  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3356  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3358  LOAD_FAST                'dtype_flat'
             3360  GET_ITER         
             3362  CALL_FUNCTION_1       1  ''
             3364  CALL_METHOD_1         1  ''

 L.2204      3366  LOAD_CONST               ('dtype',)
             3368  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3370  STORE_FAST               'rowmasks'

 L.2207      3372  LOAD_FAST                'make_mask_descr'
             3374  LOAD_DEREF               'dtype'
             3376  CALL_FUNCTION_1       1  ''
             3378  STORE_FAST               'mdtype'

 L.2208      3380  LOAD_FAST                'rowmasks'
             3382  LOAD_METHOD              view
             3384  LOAD_FAST                'mdtype'
             3386  CALL_METHOD_1         1  ''
             3388  STORE_FAST               'outputmask'
             3390  JUMP_FORWARD       3640  'to 3640'
           3392_0  COME_FROM          3242  '3242'

 L.2212      3392  LOAD_FAST                'user_converters'
         3394_3396  POP_JUMP_IF_FALSE  3574  'to 3574'

 L.2213      3398  LOAD_CONST               True
             3400  STORE_FAST               'ishomogeneous'

 L.2214      3402  BUILD_LIST_0          0 
             3404  STORE_DEREF              'descr'

 L.2215      3406  LOAD_GLOBAL              enumerate
             3408  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3410  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3412  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3414  LOAD_FAST                'converters'
             3416  GET_ITER         
             3418  CALL_FUNCTION_1       1  ''
             3420  CALL_FUNCTION_1       1  ''
             3422  GET_ITER         
           3424_0  COME_FROM          3528  '3528'
           3424_1  COME_FROM          3512  '3512'
             3424  FOR_ITER           3532  'to 3532'
             3426  UNPACK_SEQUENCE_2     2 
             3428  STORE_DEREF              'i'
             3430  STORE_FAST               'ttype'

 L.2217      3432  LOAD_DEREF               'i'
             3434  LOAD_FAST                'user_converters'
             3436  COMPARE_OP               in
         3438_3440  POP_JUMP_IF_FALSE  3514  'to 3514'

 L.2218      3442  LOAD_FAST                'ishomogeneous'
             3444  LOAD_FAST                'ttype'
             3446  LOAD_DEREF               'dtype'
             3448  LOAD_ATTR                type
             3450  COMPARE_OP               ==
             3452  INPLACE_AND      
             3454  STORE_FAST               'ishomogeneous'

 L.2219      3456  LOAD_GLOBAL              np
             3458  LOAD_METHOD              issubdtype
             3460  LOAD_FAST                'ttype'
             3462  LOAD_GLOBAL              np
             3464  LOAD_ATTR                character
             3466  CALL_METHOD_2         2  ''
         3468_3470  POP_JUMP_IF_FALSE  3498  'to 3498'

 L.2220      3472  LOAD_FAST                'ttype'
             3474  LOAD_GLOBAL              max
             3476  LOAD_CLOSURE             'i'
             3478  BUILD_TUPLE_1         1 
             3480  LOAD_GENEXPR             '<code_object <genexpr>>'
             3482  LOAD_STR                 'genfromtxt.<locals>.<genexpr>'
             3484  MAKE_FUNCTION_8          'closure'
             3486  LOAD_FAST                'data'
             3488  GET_ITER         
             3490  CALL_FUNCTION_1       1  ''
             3492  CALL_FUNCTION_1       1  ''
             3494  BUILD_TUPLE_2         2 
             3496  STORE_FAST               'ttype'
           3498_0  COME_FROM          3468  '3468'

 L.2221      3498  LOAD_DEREF               'descr'
             3500  LOAD_METHOD              append
             3502  LOAD_STR                 ''
             3504  LOAD_FAST                'ttype'
             3506  BUILD_TUPLE_2         2 
             3508  CALL_METHOD_1         1  ''
             3510  POP_TOP          
             3512  JUMP_BACK          3424  'to 3424'
           3514_0  COME_FROM          3438  '3438'

 L.2223      3514  LOAD_DEREF               'descr'
             3516  LOAD_METHOD              append
             3518  LOAD_STR                 ''
             3520  LOAD_DEREF               'dtype'
             3522  BUILD_TUPLE_2         2 
             3524  CALL_METHOD_1         1  ''
             3526  POP_TOP          
         3528_3530  JUMP_BACK          3424  'to 3424'
           3532_0  COME_FROM          3424  '3424'

 L.2225      3532  LOAD_FAST                'ishomogeneous'
         3534_3536  POP_JUMP_IF_TRUE   3574  'to 3574'

 L.2227      3538  LOAD_GLOBAL              len
             3540  LOAD_DEREF               'descr'
             3542  CALL_FUNCTION_1       1  ''
             3544  LOAD_CONST               1
             3546  COMPARE_OP               >
         3548_3550  POP_JUMP_IF_FALSE  3564  'to 3564'

 L.2228      3552  LOAD_GLOBAL              np
             3554  LOAD_METHOD              dtype
             3556  LOAD_DEREF               'descr'
             3558  CALL_METHOD_1         1  ''
             3560  STORE_DEREF              'dtype'
             3562  JUMP_FORWARD       3574  'to 3574'
           3564_0  COME_FROM          3548  '3548'

 L.2231      3564  LOAD_GLOBAL              np
             3566  LOAD_METHOD              dtype
             3568  LOAD_FAST                'ttype'
             3570  CALL_METHOD_1         1  ''
             3572  STORE_DEREF              'dtype'
           3574_0  COME_FROM          3562  '3562'
           3574_1  COME_FROM          3534  '3534'
           3574_2  COME_FROM          3394  '3394'

 L.2233      3574  LOAD_GLOBAL              np
             3576  LOAD_METHOD              array
             3578  LOAD_FAST                'data'
             3580  LOAD_DEREF               'dtype'
             3582  CALL_METHOD_2         2  ''
             3584  STORE_FAST               'output'

 L.2234      3586  LOAD_FAST                'usemask'
         3588_3590  POP_JUMP_IF_FALSE  3640  'to 3640'

 L.2235      3592  LOAD_DEREF               'dtype'
             3594  LOAD_ATTR                names
             3596  LOAD_CONST               None
             3598  COMPARE_OP               is-not
         3600_3602  POP_JUMP_IF_FALSE  3622  'to 3622'

 L.2236      3604  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3606  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3608  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3610  LOAD_DEREF               'dtype'
             3612  LOAD_ATTR                names
             3614  GET_ITER         
             3616  CALL_FUNCTION_1       1  ''
             3618  STORE_FAST               'mdtype'
             3620  JUMP_FORWARD       3626  'to 3626'
           3622_0  COME_FROM          3600  '3600'

 L.2238      3622  LOAD_GLOBAL              bool
             3624  STORE_FAST               'mdtype'
           3626_0  COME_FROM          3620  '3620'

 L.2239      3626  LOAD_GLOBAL              np
             3628  LOAD_ATTR                array
             3630  LOAD_FAST                'masks'
             3632  LOAD_FAST                'mdtype'
             3634  LOAD_CONST               ('dtype',)
             3636  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3638  STORE_FAST               'outputmask'
           3640_0  COME_FROM          3588  '3588'
           3640_1  COME_FROM          3390  '3390'
           3640_2  COME_FROM          3338  '3338'
           3640_3  COME_FROM          3204  '3204'
           3640_4  COME_FROM          3186  '3186'

 L.2241      3640  LOAD_FAST                'output'
             3642  LOAD_ATTR                dtype
             3644  LOAD_ATTR                names
             3646  STORE_DEREF              'names'

 L.2242      3648  LOAD_FAST                'usemask'
         3650_3652  POP_JUMP_IF_FALSE  3738  'to 3738'
             3654  LOAD_DEREF               'names'
         3656_3658  POP_JUMP_IF_FALSE  3738  'to 3738'

 L.2243      3660  LOAD_GLOBAL              zip
             3662  LOAD_DEREF               'names'
             3664  LOAD_FAST                'converters'
             3666  CALL_FUNCTION_2       2  ''
             3668  GET_ITER         
           3670_0  COME_FROM          3734  '3734'
             3670  FOR_ITER           3738  'to 3738'
             3672  UNPACK_SEQUENCE_2     2 
             3674  STORE_FAST               'name'
             3676  STORE_DEREF              'conv'

 L.2244      3678  LOAD_CLOSURE             'conv'
             3680  BUILD_TUPLE_1         1 
             3682  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3684  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3686  MAKE_FUNCTION_8          'closure'
             3688  LOAD_DEREF               'conv'
             3690  LOAD_ATTR                missing_values
             3692  GET_ITER         
             3694  CALL_FUNCTION_1       1  ''
             3696  STORE_FAST               'missing_values'

 L.2246      3698  LOAD_FAST                'missing_values'
             3700  GET_ITER         
           3702_0  COME_FROM          3730  '3730'
             3702  FOR_ITER           3734  'to 3734'
             3704  STORE_FAST               'mval'

 L.2247      3706  LOAD_FAST                'outputmask'
             3708  LOAD_FAST                'name'
             3710  DUP_TOP_TWO      
             3712  BINARY_SUBSCR    
             3714  LOAD_FAST                'output'
             3716  LOAD_FAST                'name'
             3718  BINARY_SUBSCR    
             3720  LOAD_FAST                'mval'
             3722  COMPARE_OP               ==
             3724  INPLACE_OR       
             3726  ROT_THREE        
             3728  STORE_SUBSCR     
         3730_3732  JUMP_BACK          3702  'to 3702'
           3734_0  COME_FROM          3702  '3702'
         3734_3736  JUMP_BACK          3670  'to 3670'
           3738_0  COME_FROM          3670  '3670'
           3738_1  COME_FROM          3656  '3656'
           3738_2  COME_FROM          3650  '3650'

 L.2249      3738  LOAD_FAST                'usemask'
         3740_3742  POP_JUMP_IF_FALSE  3760  'to 3760'

 L.2250      3744  LOAD_FAST                'output'
             3746  LOAD_METHOD              view
             3748  LOAD_FAST                'MaskedArray'
             3750  CALL_METHOD_1         1  ''
             3752  STORE_FAST               'output'

 L.2251      3754  LOAD_FAST                'outputmask'
             3756  LOAD_FAST                'output'
             3758  STORE_ATTR               _mask
           3760_0  COME_FROM          3740  '3740'

 L.2252      3760  LOAD_FAST                'unpack'
         3762_3764  POP_JUMP_IF_FALSE  3776  'to 3776'

 L.2253      3766  LOAD_FAST                'output'
             3768  LOAD_METHOD              squeeze
             3770  CALL_METHOD_0         0  ''
             3772  LOAD_ATTR                T
             3774  RETURN_VALUE     
           3776_0  COME_FROM          3762  '3762'

 L.2254      3776  LOAD_FAST                'output'
             3778  LOAD_METHOD              squeeze
             3780  CALL_METHOD_0         0  ''
             3782  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 1086_0


def ndfromtxt(fname, **kwargs):
    """
    Load ASCII data stored in a file and return it as a single array.

    .. deprecated:: 1.17
        ndfromtxt` is a deprecated alias of `genfromtxt` which
        overwrites the ``usemask`` argument with `False` even when
        explicitly called as ``ndfromtxt(..., usemask=True)``.
        Use `genfromtxt` instead.

    Parameters
    ----------
    fname, kwargs : For a description of input parameters, see `genfromtxt`.

    See Also
    --------
    numpy.genfromtxt : generic function.

    """
    kwargs['usemask'] = False
    warnings.warn('np.ndfromtxt is a deprecated alias of np.genfromtxt, prefer the latter.',
      DeprecationWarning,
      stacklevel=2)
    return genfromtxt(fname, **kwargs)


def mafromtxt(fname, **kwargs):
    """
    Load ASCII data stored in a text file and return a masked array.

    .. deprecated:: 1.17
        np.mafromtxt is a deprecated alias of `genfromtxt` which
        overwrites the ``usemask`` argument with `True` even when
        explicitly called as ``mafromtxt(..., usemask=False)``.
        Use `genfromtxt` instead.

    Parameters
    ----------
    fname, kwargs : For a description of input parameters, see `genfromtxt`.

    See Also
    --------
    numpy.genfromtxt : generic function to load ASCII data.

    """
    kwargs['usemask'] = True
    warnings.warn('np.mafromtxt is a deprecated alias of np.genfromtxt, prefer the latter.',
      DeprecationWarning,
      stacklevel=2)
    return genfromtxt(fname, **kwargs)


def recfromtxt(fname, **kwargs):
    """
    Load ASCII data from a file and return it in a record array.

    If ``usemask=False`` a standard `recarray` is returned,
    if ``usemask=True`` a MaskedRecords array is returned.

    Parameters
    ----------
    fname, kwargs : For a description of input parameters, see `genfromtxt`.

    See Also
    --------
    numpy.genfromtxt : generic function

    Notes
    -----
    By default, `dtype` is None, which means that the data-type of the output
    array will be determined from the data.

    """
    kwargs.setdefault('dtype', None)
    usemask = kwargs.get('usemask', False)
    output = genfromtxt(fname, **kwargs)
    if usemask:
        from numpy.ma.mrecords import MaskedRecords
        output = output.view(MaskedRecords)
    else:
        output = output.view(np.recarray)
    return output


def recfromcsv(fname, **kwargs):
    """
    Load ASCII data stored in a comma-separated file.

    The returned array is a record array (if ``usemask=False``, see
    `recarray`) or a masked record array (if ``usemask=True``,
    see `ma.mrecords.MaskedRecords`).

    Parameters
    ----------
    fname, kwargs : For a description of input parameters, see `genfromtxt`.

    See Also
    --------
    numpy.genfromtxt : generic function to load ASCII data.

    Notes
    -----
    By default, `dtype` is None, which means that the data-type of the output
    array will be determined from the data.

    """
    kwargs.setdefault('case_sensitive', 'lower')
    kwargs.setdefault('names', True)
    kwargs.setdefault('delimiter', ',')
    kwargs.setdefault('dtype', None)
    output = genfromtxt(fname, **kwargs)
    usemask = kwargs.get('usemask', False)
    if usemask:
        from numpy.ma.mrecords import MaskedRecords
        output = output.view(MaskedRecords)
    else:
        output = output.view(np.recarray)
    return output