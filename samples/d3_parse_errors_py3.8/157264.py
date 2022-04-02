# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\lib\npyio.py
import sys, os, re, functools, itertools, warnings, weakref, contextlib
from operator import itemgetter, index as opindex
from collections.abc import Mapping
import numpy as np
from . import format
from ._datasource import DataSource
from numpy.core import overrides
from numpy.core.multiarray import packbits, unpackbits
from numpy.core.overrides import set_array_function_like_doc, set_module
from numpy.core._internal import recursive
from ._iotools import LineSplitter, NameValidator, StringConverter, ConverterError, ConverterLockError, ConversionWarning, _is_string_like, has_nested_fields, flatten_dtype, easy_dtype, _decode_line
from numpy.compat import asbytes, asstr, asunicode, os_fspath, os_PathLike, pickle, contextlib_nullcontext

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

class BagObj:
    __doc__ = '\n    BagObj(obj)\n\n    Convert attribute look-ups to getitems on the object passed in.\n\n    Parameters\n    ----------\n    obj : class instance\n        Object on which attribute look-up is performed.\n\n    Examples\n    --------\n    >>> from numpy.lib.npyio import BagObj as BO\n    >>> class BagDemo:\n    ...     def __getitem__(self, key): # An instance of BagObj(BagDemo)\n    ...                                 # will call this method when any\n    ...                                 # attribute look-up is required\n    ...         result = "Doesn\'t matter what you want, "\n    ...         return result + "you\'re gonna get this"\n    ...\n    >>> demo_obj = BagDemo()\n    >>> bagobj = BO(demo_obj)\n    >>> bagobj.hello_there\n    "Doesn\'t matter what you want, you\'re gonna get this"\n    >>> bagobj.I_can_be_anything\n    "Doesn\'t matter what you want, you\'re gonna get this"\n\n    '

    def __init__(self, obj):
        self._obj = weakref.proxy(obj)

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, '_obj')[key]
        except KeyError:
            raise AttributeError(key) from None

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
    zip = None
    fid = None

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

 L. 396         0  LOAD_FAST                'encoding'
                2  LOAD_CONST               ('ASCII', 'latin1', 'bytes')
                4  COMPARE_OP               not-in
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 408         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 "encoding must be 'ASCII', 'latin1', or 'bytes'"
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 410        16  LOAD_GLOBAL              dict
               18  LOAD_FAST                'encoding'
               20  LOAD_FAST                'fix_imports'
               22  LOAD_CONST               ('encoding', 'fix_imports')
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               26  STORE_FAST               'pickle_kwargs'

 L. 412        28  LOAD_GLOBAL              contextlib
               30  LOAD_METHOD              ExitStack
               32  CALL_METHOD_0         0  ''
            34_36  SETUP_WITH          370  'to 370'
               38  STORE_FAST               'stack'

 L. 413        40  LOAD_GLOBAL              hasattr
               42  LOAD_FAST                'file'
               44  LOAD_STR                 'read'
               46  CALL_FUNCTION_2       2  ''
               48  POP_JUMP_IF_FALSE    60  'to 60'

 L. 414        50  LOAD_FAST                'file'
               52  STORE_FAST               'fid'

 L. 415        54  LOAD_CONST               False
               56  STORE_FAST               'own_fid'
               58  JUMP_FORWARD         84  'to 84'
             60_0  COME_FROM            48  '48'

 L. 417        60  LOAD_FAST                'stack'
               62  LOAD_METHOD              enter_context
               64  LOAD_GLOBAL              open
               66  LOAD_GLOBAL              os_fspath
               68  LOAD_FAST                'file'
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_STR                 'rb'
               74  CALL_FUNCTION_2       2  ''
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'fid'

 L. 418        80  LOAD_CONST               True
               82  STORE_FAST               'own_fid'
             84_0  COME_FROM            58  '58'

 L. 421        84  LOAD_CONST               b'PK\x03\x04'
               86  STORE_FAST               '_ZIP_PREFIX'

 L. 422        88  LOAD_CONST               b'PK\x05\x06'
               90  STORE_FAST               '_ZIP_SUFFIX'

 L. 423        92  LOAD_GLOBAL              len
               94  LOAD_GLOBAL              format
               96  LOAD_ATTR                MAGIC_PREFIX
               98  CALL_FUNCTION_1       1  ''
              100  STORE_FAST               'N'

 L. 424       102  LOAD_FAST                'fid'
              104  LOAD_METHOD              read
              106  LOAD_FAST                'N'
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'magic'

 L. 427       112  LOAD_FAST                'fid'
              114  LOAD_METHOD              seek
              116  LOAD_GLOBAL              min
              118  LOAD_FAST                'N'
              120  LOAD_GLOBAL              len
              122  LOAD_FAST                'magic'
              124  CALL_FUNCTION_1       1  ''
              126  CALL_FUNCTION_2       2  ''
              128  UNARY_NEGATIVE   
              130  LOAD_CONST               1
              132  CALL_METHOD_2         2  ''
              134  POP_TOP          

 L. 428       136  LOAD_FAST                'magic'
              138  LOAD_METHOD              startswith
              140  LOAD_FAST                '_ZIP_PREFIX'
              142  CALL_METHOD_1         1  ''
              144  POP_JUMP_IF_TRUE    156  'to 156'
              146  LOAD_FAST                'magic'
              148  LOAD_METHOD              startswith
              150  LOAD_FAST                '_ZIP_SUFFIX'
              152  CALL_METHOD_1         1  ''
              154  POP_JUMP_IF_FALSE   196  'to 196'
            156_0  COME_FROM           144  '144'

 L. 431       156  LOAD_FAST                'stack'
              158  LOAD_METHOD              pop_all
              160  CALL_METHOD_0         0  ''
              162  POP_TOP          

 L. 432       164  LOAD_GLOBAL              NpzFile
              166  LOAD_FAST                'fid'
              168  LOAD_FAST                'own_fid'
              170  LOAD_FAST                'allow_pickle'

 L. 433       172  LOAD_FAST                'pickle_kwargs'

 L. 432       174  LOAD_CONST               ('own_fid', 'allow_pickle', 'pickle_kwargs')
              176  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              178  STORE_FAST               'ret'

 L. 434       180  LOAD_FAST                'ret'
              182  POP_BLOCK        
              184  ROT_TWO          
              186  BEGIN_FINALLY    
              188  WITH_CLEANUP_START
              190  WITH_CLEANUP_FINISH
              192  POP_FINALLY           0  ''
              194  RETURN_VALUE     
            196_0  COME_FROM           154  '154'

 L. 435       196  LOAD_FAST                'magic'
              198  LOAD_GLOBAL              format
              200  LOAD_ATTR                MAGIC_PREFIX
              202  COMPARE_OP               ==
          204_206  POP_JUMP_IF_FALSE   268  'to 268'

 L. 437       208  LOAD_FAST                'mmap_mode'
              210  POP_JUMP_IF_FALSE   238  'to 238'

 L. 438       212  LOAD_GLOBAL              format
              214  LOAD_ATTR                open_memmap
              216  LOAD_FAST                'file'
              218  LOAD_FAST                'mmap_mode'
              220  LOAD_CONST               ('mode',)
              222  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              224  POP_BLOCK        
              226  ROT_TWO          
              228  BEGIN_FINALLY    
              230  WITH_CLEANUP_START
              232  WITH_CLEANUP_FINISH
              234  POP_FINALLY           0  ''
              236  RETURN_VALUE     
            238_0  COME_FROM           210  '210'

 L. 440       238  LOAD_GLOBAL              format
              240  LOAD_ATTR                read_array
              242  LOAD_FAST                'fid'
              244  LOAD_FAST                'allow_pickle'

 L. 441       246  LOAD_FAST                'pickle_kwargs'

 L. 440       248  LOAD_CONST               ('allow_pickle', 'pickle_kwargs')
              250  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              252  POP_BLOCK        
              254  ROT_TWO          
              256  BEGIN_FINALLY    
              258  WITH_CLEANUP_START
              260  WITH_CLEANUP_FINISH
              262  POP_FINALLY           0  ''
              264  RETURN_VALUE     
              266  JUMP_FORWARD        366  'to 366'
            268_0  COME_FROM           204  '204'

 L. 444       268  LOAD_FAST                'allow_pickle'
          270_272  POP_JUMP_IF_TRUE    282  'to 282'

 L. 445       274  LOAD_GLOBAL              ValueError
              276  LOAD_STR                 'Cannot load file containing pickled data when allow_pickle=False'
              278  CALL_FUNCTION_1       1  ''
              280  RAISE_VARARGS_1       1  'exception instance'
            282_0  COME_FROM           270  '270'

 L. 447       282  SETUP_FINALLY       312  'to 312'

 L. 448       284  LOAD_GLOBAL              pickle
              286  LOAD_ATTR                load
              288  LOAD_FAST                'fid'
              290  BUILD_TUPLE_1         1 
              292  LOAD_FAST                'pickle_kwargs'
              294  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              296  POP_BLOCK        
              298  POP_BLOCK        
              300  ROT_TWO          
              302  BEGIN_FINALLY    
              304  WITH_CLEANUP_START
              306  WITH_CLEANUP_FINISH
              308  POP_FINALLY           0  ''
              310  RETURN_VALUE     
            312_0  COME_FROM_FINALLY   282  '282'

 L. 449       312  DUP_TOP          
              314  LOAD_GLOBAL              Exception
              316  COMPARE_OP               exception-match
          318_320  POP_JUMP_IF_FALSE   364  'to 364'
              322  POP_TOP          
              324  STORE_FAST               'e'
              326  POP_TOP          
              328  SETUP_FINALLY       352  'to 352'

 L. 450       330  LOAD_GLOBAL              IOError

 L. 451       332  LOAD_STR                 'Failed to interpret file %s as a pickle'
              334  LOAD_GLOBAL              repr
              336  LOAD_FAST                'file'
              338  CALL_FUNCTION_1       1  ''
              340  BINARY_MODULO    

 L. 450       342  CALL_FUNCTION_1       1  ''

 L. 451       344  LOAD_FAST                'e'

 L. 450       346  RAISE_VARARGS_2       2  'exception instance with __cause__'
              348  POP_BLOCK        
              350  BEGIN_FINALLY    
            352_0  COME_FROM_FINALLY   328  '328'
              352  LOAD_CONST               None
              354  STORE_FAST               'e'
              356  DELETE_FAST              'e'
              358  END_FINALLY      
              360  POP_EXCEPT       
              362  JUMP_FORWARD        366  'to 366'
            364_0  COME_FROM           318  '318'
              364  END_FINALLY      
            366_0  COME_FROM           362  '362'
            366_1  COME_FROM           266  '266'
              366  POP_BLOCK        
              368  BEGIN_FINALLY    
            370_0  COME_FROM_WITH       34  '34'
              370  WITH_CLEANUP_START
              372  WITH_CLEANUP_FINISH
              374  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 298


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
    if hasattr(file, 'write'):
        file_ctx = contextlib_nullcontext(file)
    else:
        file = os_fspath(file)
        if not file.endswith('.npy'):
            file = file + '.npy'
        file_ctx = open(file, 'wb')
    with file_ctx as fid:
        arr = np.asanyarray(arr)
        format.write_array(fid, arr, allow_pickle=allow_pickle, pickle_kwargs=dict(fix_imports=fix_imports))


def _savez_dispatcher(file, *args, **kwds):
    yield from args
    yield from kwds.values()
    if False:
        yield None


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
    yield from args
    yield from kwds.values()
    if False:
        yield None


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
        for key, val in namedict.items():
            fname = key + '.npy'
            val = np.asanyarray(val)
            with zipf.open(fname, 'w', force_zip64=True) as fid:
                format.write_array(fid, val, allow_pickle=allow_pickle,
                  pickle_kwargs=pickle_kwargs)
        else:
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

def _loadtxt_dispatcher(fname, dtype=None, comments=None, delimiter=None, converters=None, skiprows=None, usecols=None, unpack=None, ndmin=None, encoding=None, max_rows=None, *, like=None):
    return (
     like,)


@set_array_function_like_doc
@set_module('numpy')
def loadtxt--- This code section failed: ---

 L. 901         0  LOAD_FAST                'like'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    40  'to 40'

 L. 902         8  LOAD_GLOBAL              _loadtxt_with_like

 L. 903        10  LOAD_FAST                'fname'

 L. 903        12  LOAD_FAST                'dtype'

 L. 903        14  LOAD_DEREF               'comments'

 L. 903        16  LOAD_DEREF               'delimiter'

 L. 904        18  LOAD_DEREF               'converters'

 L. 904        20  LOAD_DEREF               'skiprows'

 L. 904        22  LOAD_DEREF               'usecols'

 L. 905        24  LOAD_FAST                'unpack'

 L. 905        26  LOAD_FAST                'ndmin'

 L. 905        28  LOAD_DEREF               'encoding'

 L. 906        30  LOAD_DEREF               'max_rows'

 L. 906        32  LOAD_FAST                'like'

 L. 902        34  LOAD_CONST               ('dtype', 'comments', 'delimiter', 'converters', 'skiprows', 'usecols', 'unpack', 'ndmin', 'encoding', 'max_rows', 'like')
               36  CALL_FUNCTION_KW_12    12  '12 total positional and keyword args'
               38  RETURN_VALUE     
             40_0  COME_FROM             6  '6'

 L. 914        40  LOAD_GLOBAL              recursive

 L. 915        42  LOAD_CODE                <code_object flatten_dtype_internal>
               44  LOAD_STR                 'loadtxt.<locals>.flatten_dtype_internal'
               46  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'flatten_dtype_internal'

 L. 944        52  LOAD_GLOBAL              recursive

 L. 945        54  LOAD_CODE                <code_object pack_items>
               56  LOAD_STR                 'loadtxt.<locals>.pack_items'
               58  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               60  CALL_FUNCTION_1       1  ''
               62  STORE_DEREF              'pack_items'

 L. 961        64  LOAD_CLOSURE             'comments'
               66  LOAD_CLOSURE             'delimiter'
               68  LOAD_CLOSURE             'encoding'
               70  LOAD_CLOSURE             'regex_comments'
               72  BUILD_TUPLE_4         4 
               74  LOAD_CODE                <code_object split_line>
               76  LOAD_STR                 'loadtxt.<locals>.split_line'
               78  MAKE_FUNCTION_8          'closure'
               80  STORE_DEREF              'split_line'

 L. 970        82  LOAD_CLOSURE             'N'
               84  LOAD_CLOSURE             'converters'
               86  LOAD_CLOSURE             'fh'
               88  LOAD_CLOSURE             'first_line'
               90  LOAD_CLOSURE             'max_rows'
               92  LOAD_CLOSURE             'pack_items'
               94  LOAD_CLOSURE             'packing'
               96  LOAD_CLOSURE             'skiprows'
               98  LOAD_CLOSURE             'split_line'
              100  LOAD_CLOSURE             'usecols'
              102  BUILD_TUPLE_10       10 
              104  LOAD_CODE                <code_object read_data>
              106  LOAD_STR                 'loadtxt.<locals>.read_data'
              108  MAKE_FUNCTION_8          'closure'
              110  STORE_FAST               'read_data'

 L.1013       112  LOAD_FAST                'ndmin'
              114  LOAD_CONST               (0, 1, 2)
              116  COMPARE_OP               not-in
              118  POP_JUMP_IF_FALSE   132  'to 132'

 L.1014       120  LOAD_GLOBAL              ValueError
              122  LOAD_STR                 'Illegal value of ndmin keyword: %s'
              124  LOAD_FAST                'ndmin'
              126  BINARY_MODULO    
              128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
            132_0  COME_FROM           118  '118'

 L.1017       132  LOAD_DEREF               'comments'
              134  LOAD_CONST               None
              136  COMPARE_OP               is-not
              138  POP_JUMP_IF_FALSE   204  'to 204'

 L.1018       140  LOAD_GLOBAL              isinstance
              142  LOAD_DEREF               'comments'
              144  LOAD_GLOBAL              str
              146  LOAD_GLOBAL              bytes
              148  BUILD_TUPLE_2         2 
              150  CALL_FUNCTION_2       2  ''
              152  POP_JUMP_IF_FALSE   160  'to 160'

 L.1019       154  LOAD_DEREF               'comments'
              156  BUILD_LIST_1          1 
              158  STORE_DEREF              'comments'
            160_0  COME_FROM           152  '152'

 L.1020       160  LOAD_LISTCOMP            '<code_object <listcomp>>'
              162  LOAD_STR                 'loadtxt.<locals>.<listcomp>'
              164  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              166  LOAD_DEREF               'comments'
              168  GET_ITER         
              170  CALL_FUNCTION_1       1  ''
              172  STORE_DEREF              'comments'

 L.1022       174  LOAD_GENEXPR             '<code_object <genexpr>>'
              176  LOAD_STR                 'loadtxt.<locals>.<genexpr>'
              178  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              180  LOAD_DEREF               'comments'
              182  GET_ITER         
              184  CALL_FUNCTION_1       1  ''
              186  STORE_DEREF              'comments'

 L.1023       188  LOAD_GLOBAL              re
              190  LOAD_METHOD              compile
              192  LOAD_STR                 '|'
              194  LOAD_METHOD              join
              196  LOAD_DEREF               'comments'
              198  CALL_METHOD_1         1  ''
              200  CALL_METHOD_1         1  ''
              202  STORE_DEREF              'regex_comments'
            204_0  COME_FROM           138  '138'

 L.1025       204  LOAD_DEREF               'delimiter'
              206  LOAD_CONST               None
              208  COMPARE_OP               is-not
              210  POP_JUMP_IF_FALSE   220  'to 220'

 L.1026       212  LOAD_GLOBAL              _decode_line
              214  LOAD_DEREF               'delimiter'
              216  CALL_FUNCTION_1       1  ''
              218  STORE_DEREF              'delimiter'
            220_0  COME_FROM           210  '210'

 L.1028       220  LOAD_DEREF               'converters'
              222  STORE_FAST               'user_converters'

 L.1030       224  LOAD_CONST               False
              226  STORE_FAST               'byte_converters'

 L.1031       228  LOAD_DEREF               'encoding'
              230  LOAD_STR                 'bytes'
              232  COMPARE_OP               ==
              234  POP_JUMP_IF_FALSE   244  'to 244'

 L.1032       236  LOAD_CONST               None
              238  STORE_DEREF              'encoding'

 L.1033       240  LOAD_CONST               True
              242  STORE_FAST               'byte_converters'
            244_0  COME_FROM           234  '234'

 L.1035       244  LOAD_DEREF               'usecols'
              246  LOAD_CONST               None
              248  COMPARE_OP               is-not
          250_252  POP_JUMP_IF_FALSE   380  'to 380'

 L.1037       254  SETUP_FINALLY       268  'to 268'

 L.1038       256  LOAD_GLOBAL              list
              258  LOAD_DEREF               'usecols'
              260  CALL_FUNCTION_1       1  ''
              262  STORE_FAST               'usecols_as_list'
              264  POP_BLOCK        
              266  JUMP_FORWARD        296  'to 296'
            268_0  COME_FROM_FINALLY   254  '254'

 L.1039       268  DUP_TOP          
              270  LOAD_GLOBAL              TypeError
              272  COMPARE_OP               exception-match
          274_276  POP_JUMP_IF_FALSE   294  'to 294'
              278  POP_TOP          
              280  POP_TOP          
              282  POP_TOP          

 L.1040       284  LOAD_DEREF               'usecols'
              286  BUILD_LIST_1          1 
              288  STORE_FAST               'usecols_as_list'
              290  POP_EXCEPT       
              292  JUMP_FORWARD        296  'to 296'
            294_0  COME_FROM           274  '274'
              294  END_FINALLY      
            296_0  COME_FROM           292  '292'
            296_1  COME_FROM           266  '266'

 L.1041       296  LOAD_FAST                'usecols_as_list'
              298  GET_ITER         
            300_0  COME_FROM           372  '372'
            300_1  COME_FROM           368  '368'
            300_2  COME_FROM           316  '316'
              300  FOR_ITER            376  'to 376'
              302  STORE_FAST               'col_idx'

 L.1042       304  SETUP_FINALLY       318  'to 318'

 L.1043       306  LOAD_GLOBAL              opindex
              308  LOAD_FAST                'col_idx'
              310  CALL_FUNCTION_1       1  ''
              312  POP_TOP          
              314  POP_BLOCK        
              316  JUMP_BACK           300  'to 300'
            318_0  COME_FROM_FINALLY   304  '304'

 L.1044       318  DUP_TOP          
              320  LOAD_GLOBAL              TypeError
              322  COMPARE_OP               exception-match
          324_326  POP_JUMP_IF_FALSE   370  'to 370'
              328  POP_TOP          
              330  STORE_FAST               'e'
              332  POP_TOP          
              334  SETUP_FINALLY       358  'to 358'

 L.1046       336  LOAD_STR                 'usecols must be an int or a sequence of ints but it contains at least one element of type %s'

 L.1048       338  LOAD_GLOBAL              type
              340  LOAD_FAST                'col_idx'
              342  CALL_FUNCTION_1       1  ''

 L.1046       344  BINARY_MODULO    

 L.1045       346  BUILD_TUPLE_1         1 
              348  LOAD_FAST                'e'
              350  STORE_ATTR               args

 L.1050       352  RAISE_VARARGS_0       0  'reraise'
              354  POP_BLOCK        
              356  BEGIN_FINALLY    
            358_0  COME_FROM_FINALLY   334  '334'
              358  LOAD_CONST               None
              360  STORE_FAST               'e'
              362  DELETE_FAST              'e'
              364  END_FINALLY      
              366  POP_EXCEPT       
              368  JUMP_BACK           300  'to 300'
            370_0  COME_FROM           324  '324'
              370  END_FINALLY      
          372_374  JUMP_BACK           300  'to 300'
            376_0  COME_FROM           300  '300'

 L.1052       376  LOAD_FAST                'usecols_as_list'
              378  STORE_DEREF              'usecols'
            380_0  COME_FROM           250  '250'

 L.1055       380  LOAD_GLOBAL              np
              382  LOAD_METHOD              dtype
              384  LOAD_FAST                'dtype'
              386  CALL_METHOD_1         1  ''
              388  STORE_FAST               'dtype'

 L.1056       390  LOAD_GLOBAL              _getconv
              392  LOAD_FAST                'dtype'
              394  CALL_FUNCTION_1       1  ''
              396  STORE_DEREF              'defconv'

 L.1058       398  LOAD_FAST                'flatten_dtype_internal'
              400  LOAD_FAST                'dtype'
              402  CALL_FUNCTION_1       1  ''
              404  UNPACK_SEQUENCE_2     2 
              406  STORE_FAST               'dtype_types'
              408  STORE_DEREF              'packing'

 L.1060       410  LOAD_CONST               False
              412  STORE_FAST               'fown'

 L.1061       414  SETUP_FINALLY       516  'to 516'

 L.1062       416  LOAD_GLOBAL              isinstance
              418  LOAD_FAST                'fname'
              420  LOAD_GLOBAL              os_PathLike
              422  CALL_FUNCTION_2       2  ''
          424_426  POP_JUMP_IF_FALSE   436  'to 436'

 L.1063       428  LOAD_GLOBAL              os_fspath
              430  LOAD_FAST                'fname'
              432  CALL_FUNCTION_1       1  ''
              434  STORE_FAST               'fname'
            436_0  COME_FROM           424  '424'

 L.1064       436  LOAD_GLOBAL              _is_string_like
              438  LOAD_FAST                'fname'
              440  CALL_FUNCTION_1       1  ''
          442_444  POP_JUMP_IF_FALSE   492  'to 492'

 L.1065       446  LOAD_GLOBAL              np
              448  LOAD_ATTR                lib
              450  LOAD_ATTR                _datasource
              452  LOAD_ATTR                open
              454  LOAD_FAST                'fname'
              456  LOAD_STR                 'rt'
              458  LOAD_DEREF               'encoding'
              460  LOAD_CONST               ('encoding',)
              462  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              464  STORE_DEREF              'fh'

 L.1066       466  LOAD_GLOBAL              getattr
              468  LOAD_DEREF               'fh'
              470  LOAD_STR                 'encoding'
              472  LOAD_STR                 'latin1'
              474  CALL_FUNCTION_3       3  ''
              476  STORE_DEREF              'fencoding'

 L.1067       478  LOAD_GLOBAL              iter
              480  LOAD_DEREF               'fh'
              482  CALL_FUNCTION_1       1  ''
              484  STORE_DEREF              'fh'

 L.1068       486  LOAD_CONST               True
              488  STORE_FAST               'fown'
              490  JUMP_FORWARD        512  'to 512'
            492_0  COME_FROM           442  '442'

 L.1070       492  LOAD_GLOBAL              iter
              494  LOAD_FAST                'fname'
              496  CALL_FUNCTION_1       1  ''
              498  STORE_DEREF              'fh'

 L.1071       500  LOAD_GLOBAL              getattr
              502  LOAD_FAST                'fname'
              504  LOAD_STR                 'encoding'
              506  LOAD_STR                 'latin1'
              508  CALL_FUNCTION_3       3  ''
              510  STORE_DEREF              'fencoding'
            512_0  COME_FROM           490  '490'
              512  POP_BLOCK        
              514  JUMP_FORWARD        562  'to 562'
            516_0  COME_FROM_FINALLY   414  '414'

 L.1072       516  DUP_TOP          
              518  LOAD_GLOBAL              TypeError
              520  COMPARE_OP               exception-match
          522_524  POP_JUMP_IF_FALSE   560  'to 560'
              526  POP_TOP          
              528  STORE_FAST               'e'
              530  POP_TOP          
              532  SETUP_FINALLY       548  'to 548'

 L.1073       534  LOAD_GLOBAL              ValueError

 L.1074       536  LOAD_STR                 'fname must be a string, file handle, or generator'

 L.1073       538  CALL_FUNCTION_1       1  ''

 L.1075       540  LOAD_FAST                'e'

 L.1073       542  RAISE_VARARGS_2       2  'exception instance with __cause__'
              544  POP_BLOCK        
              546  BEGIN_FINALLY    
            548_0  COME_FROM_FINALLY   532  '532'
              548  LOAD_CONST               None
              550  STORE_FAST               'e'
              552  DELETE_FAST              'e'
              554  END_FINALLY      
              556  POP_EXCEPT       
              558  JUMP_FORWARD        562  'to 562'
            560_0  COME_FROM           522  '522'
              560  END_FINALLY      
            562_0  COME_FROM           558  '558'
            562_1  COME_FROM           514  '514'

 L.1078       562  LOAD_DEREF               'encoding'
              564  LOAD_CONST               None
              566  COMPARE_OP               is-not
          568_570  POP_JUMP_IF_FALSE   578  'to 578'

 L.1079       572  LOAD_DEREF               'encoding'
              574  STORE_DEREF              'fencoding'
              576  JUMP_FORWARD        604  'to 604'
            578_0  COME_FROM           568  '568'

 L.1082       578  LOAD_DEREF               'fencoding'
              580  LOAD_CONST               None
              582  COMPARE_OP               is
          584_586  POP_JUMP_IF_FALSE   604  'to 604'

 L.1083       588  LOAD_CONST               0
              590  LOAD_CONST               None
              592  IMPORT_NAME              locale
              594  STORE_FAST               'locale'

 L.1084       596  LOAD_FAST                'locale'
              598  LOAD_METHOD              getpreferredencoding
              600  CALL_METHOD_0         0  ''
              602  STORE_DEREF              'fencoding'
            604_0  COME_FROM           584  '584'
            604_1  COME_FROM           576  '576'

 L.1086   604_606  SETUP_FINALLY      1054  'to 1054'

 L.1088       608  LOAD_GLOBAL              range
              610  LOAD_DEREF               'skiprows'
              612  CALL_FUNCTION_1       1  ''
              614  GET_ITER         
            616_0  COME_FROM           628  '628'
              616  FOR_ITER            632  'to 632'
              618  STORE_FAST               'i'

 L.1089       620  LOAD_GLOBAL              next
              622  LOAD_DEREF               'fh'
              624  CALL_FUNCTION_1       1  ''
              626  POP_TOP          
          628_630  JUMP_BACK           616  'to 616'
            632_0  COME_FROM           616  '616'

 L.1093       632  LOAD_CONST               None
              634  STORE_FAST               'first_vals'

 L.1094       636  SETUP_FINALLY       668  'to 668'
            638_0  COME_FROM           660  '660'

 L.1095       638  LOAD_FAST                'first_vals'
          640_642  POP_JUMP_IF_TRUE    664  'to 664'

 L.1096       644  LOAD_GLOBAL              next
              646  LOAD_DEREF               'fh'
              648  CALL_FUNCTION_1       1  ''
              650  STORE_DEREF              'first_line'

 L.1097       652  LOAD_DEREF               'split_line'
              654  LOAD_DEREF               'first_line'
              656  CALL_FUNCTION_1       1  ''
              658  STORE_FAST               'first_vals'
          660_662  JUMP_BACK           638  'to 638'
            664_0  COME_FROM           640  '640'
              664  POP_BLOCK        
              666  JUMP_FORWARD        716  'to 716'
            668_0  COME_FROM_FINALLY   636  '636'

 L.1098       668  DUP_TOP          
              670  LOAD_GLOBAL              StopIteration
              672  COMPARE_OP               exception-match
          674_676  POP_JUMP_IF_FALSE   714  'to 714'
              678  POP_TOP          
              680  POP_TOP          
              682  POP_TOP          

 L.1100       684  LOAD_STR                 ''
              686  STORE_DEREF              'first_line'

 L.1101       688  BUILD_LIST_0          0 
              690  STORE_FAST               'first_vals'

 L.1102       692  LOAD_GLOBAL              warnings
              694  LOAD_ATTR                warn
              696  LOAD_STR                 'loadtxt: Empty input file: "%s"'
              698  LOAD_FAST                'fname'
              700  BINARY_MODULO    

 L.1103       702  LOAD_CONST               2

 L.1102       704  LOAD_CONST               ('stacklevel',)
              706  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              708  POP_TOP          
              710  POP_EXCEPT       
              712  JUMP_FORWARD        716  'to 716'
            714_0  COME_FROM           674  '674'
              714  END_FINALLY      
            716_0  COME_FROM           712  '712'
            716_1  COME_FROM           666  '666'

 L.1104       716  LOAD_GLOBAL              len
              718  LOAD_DEREF               'usecols'
          720_722  JUMP_IF_TRUE_OR_POP   726  'to 726'
              724  LOAD_FAST                'first_vals'
            726_0  COME_FROM           720  '720'
              726  CALL_FUNCTION_1       1  ''
              728  STORE_DEREF              'N'

 L.1108       730  LOAD_GLOBAL              len
              732  LOAD_FAST                'dtype_types'
              734  CALL_FUNCTION_1       1  ''
              736  LOAD_CONST               1
              738  COMPARE_OP               >
          740_742  POP_JUMP_IF_FALSE   760  'to 760'

 L.1111       744  LOAD_LISTCOMP            '<code_object <listcomp>>'
              746  LOAD_STR                 'loadtxt.<locals>.<listcomp>'
              748  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              750  LOAD_FAST                'dtype_types'
              752  GET_ITER         
              754  CALL_FUNCTION_1       1  ''
              756  STORE_DEREF              'converters'
              758  JUMP_FORWARD        802  'to 802'
            760_0  COME_FROM           740  '740'

 L.1114       760  LOAD_CLOSURE             'defconv'
              762  BUILD_TUPLE_1         1 
              764  LOAD_LISTCOMP            '<code_object <listcomp>>'
              766  LOAD_STR                 'loadtxt.<locals>.<listcomp>'
              768  MAKE_FUNCTION_8          'closure'
              770  LOAD_GLOBAL              range
              772  LOAD_DEREF               'N'
              774  CALL_FUNCTION_1       1  ''
              776  GET_ITER         
              778  CALL_FUNCTION_1       1  ''
              780  STORE_DEREF              'converters'

 L.1115       782  LOAD_DEREF               'N'
              784  LOAD_CONST               1
              786  COMPARE_OP               >
          788_790  POP_JUMP_IF_FALSE   802  'to 802'

 L.1116       792  LOAD_DEREF               'N'
              794  LOAD_GLOBAL              tuple
              796  BUILD_TUPLE_2         2 
              798  BUILD_LIST_1          1 
              800  STORE_DEREF              'packing'
            802_0  COME_FROM           788  '788'
            802_1  COME_FROM           758  '758'

 L.1119       802  LOAD_FAST                'user_converters'
          804_806  JUMP_IF_TRUE_OR_POP   810  'to 810'
              808  BUILD_MAP_0           0 
            810_0  COME_FROM           804  '804'
              810  LOAD_METHOD              items
              812  CALL_METHOD_0         0  ''
              814  GET_ITER         
            816_0  COME_FROM           916  '916'
            816_1  COME_FROM           906  '906'
            816_2  COME_FROM           864  '864'
              816  FOR_ITER            920  'to 920'
              818  UNPACK_SEQUENCE_2     2 
              820  STORE_FAST               'i'
              822  STORE_FAST               'conv'

 L.1120       824  LOAD_DEREF               'usecols'
          826_828  POP_JUMP_IF_FALSE   874  'to 874'

 L.1121       830  SETUP_FINALLY       846  'to 846'

 L.1122       832  LOAD_DEREF               'usecols'
              834  LOAD_METHOD              index
              836  LOAD_FAST                'i'
              838  CALL_METHOD_1         1  ''
              840  STORE_FAST               'i'
              842  POP_BLOCK        
              844  JUMP_FORWARD        874  'to 874'
            846_0  COME_FROM_FINALLY   830  '830'

 L.1123       846  DUP_TOP          
              848  LOAD_GLOBAL              ValueError
              850  COMPARE_OP               exception-match
          852_854  POP_JUMP_IF_FALSE   872  'to 872'
              856  POP_TOP          
              858  POP_TOP          
              860  POP_TOP          

 L.1125       862  POP_EXCEPT       
          864_866  JUMP_BACK           816  'to 816'
              868  POP_EXCEPT       
              870  JUMP_FORWARD        874  'to 874'
            872_0  COME_FROM           852  '852'
              872  END_FINALLY      
            874_0  COME_FROM           870  '870'
            874_1  COME_FROM           844  '844'
            874_2  COME_FROM           826  '826'

 L.1126       874  LOAD_FAST                'byte_converters'
          876_878  POP_JUMP_IF_FALSE   908  'to 908'

 L.1130       880  LOAD_CODE                <code_object tobytes_first>
              882  LOAD_STR                 'loadtxt.<locals>.tobytes_first'
              884  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              886  STORE_FAST               'tobytes_first'

 L.1134       888  LOAD_GLOBAL              functools
              890  LOAD_ATTR                partial
              892  LOAD_FAST                'tobytes_first'
              894  LOAD_FAST                'conv'
              896  LOAD_CONST               ('conv',)
              898  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              900  LOAD_DEREF               'converters'
              902  LOAD_FAST                'i'
              904  STORE_SUBSCR     
              906  JUMP_BACK           816  'to 816'
            908_0  COME_FROM           876  '876'

 L.1136       908  LOAD_FAST                'conv'
              910  LOAD_DEREF               'converters'
              912  LOAD_FAST                'i'
              914  STORE_SUBSCR     
          916_918  JUMP_BACK           816  'to 816'
            920_0  COME_FROM           816  '816'

 L.1138       920  LOAD_CLOSURE             'fencoding'
              922  BUILD_TUPLE_1         1 
              924  LOAD_LISTCOMP            '<code_object <listcomp>>'
              926  LOAD_STR                 'loadtxt.<locals>.<listcomp>'
              928  MAKE_FUNCTION_8          'closure'

 L.1139       930  LOAD_DEREF               'converters'

 L.1138       932  GET_ITER         
              934  CALL_FUNCTION_1       1  ''
              936  STORE_DEREF              'converters'

 L.1145       938  LOAD_CONST               None
              940  STORE_DEREF              'X'

 L.1146       942  LOAD_FAST                'read_data'
              944  LOAD_GLOBAL              _loadtxt_chunksize
              946  CALL_FUNCTION_1       1  ''
              948  GET_ITER         
            950_0  COME_FROM          1046  '1046'
            950_1  COME_FROM           976  '976'
              950  FOR_ITER           1050  'to 1050'
              952  STORE_FAST               'x'

 L.1147       954  LOAD_DEREF               'X'
              956  LOAD_CONST               None
              958  COMPARE_OP               is
          960_962  POP_JUMP_IF_FALSE   978  'to 978'

 L.1148       964  LOAD_GLOBAL              np
              966  LOAD_METHOD              array
              968  LOAD_FAST                'x'
              970  LOAD_FAST                'dtype'
              972  CALL_METHOD_2         2  ''
              974  STORE_DEREF              'X'
              976  JUMP_BACK           950  'to 950'
            978_0  COME_FROM           960  '960'

 L.1150       978  LOAD_GLOBAL              list
              980  LOAD_DEREF               'X'
              982  LOAD_ATTR                shape
              984  CALL_FUNCTION_1       1  ''
              986  STORE_FAST               'nshape'

 L.1151       988  LOAD_FAST                'nshape'
              990  LOAD_CONST               0
              992  BINARY_SUBSCR    
              994  STORE_FAST               'pos'

 L.1152       996  LOAD_FAST                'nshape'
              998  LOAD_CONST               0
             1000  DUP_TOP_TWO      
             1002  BINARY_SUBSCR    
             1004  LOAD_GLOBAL              len
             1006  LOAD_FAST                'x'
             1008  CALL_FUNCTION_1       1  ''
             1010  INPLACE_ADD      
             1012  ROT_THREE        
             1014  STORE_SUBSCR     

 L.1153      1016  LOAD_DEREF               'X'
             1018  LOAD_ATTR                resize
             1020  LOAD_FAST                'nshape'
             1022  LOAD_CONST               False
             1024  LOAD_CONST               ('refcheck',)
             1026  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1028  POP_TOP          

 L.1154      1030  LOAD_FAST                'x'
             1032  LOAD_DEREF               'X'
             1034  LOAD_FAST                'pos'
             1036  LOAD_CONST               None
             1038  BUILD_SLICE_2         2 
             1040  LOAD_CONST               Ellipsis
             1042  BUILD_TUPLE_2         2 
             1044  STORE_SUBSCR     
         1046_1048  JUMP_BACK           950  'to 950'
           1050_0  COME_FROM           950  '950'
             1050  POP_BLOCK        
             1052  BEGIN_FINALLY    
           1054_0  COME_FROM_FINALLY   604  '604'

 L.1156      1054  LOAD_FAST                'fown'
         1056_1058  POP_JUMP_IF_FALSE  1068  'to 1068'

 L.1157      1060  LOAD_DEREF               'fh'
             1062  LOAD_METHOD              close
             1064  CALL_METHOD_0         0  ''
             1066  POP_TOP          
           1068_0  COME_FROM          1056  '1056'
             1068  END_FINALLY      

 L.1159      1070  LOAD_DEREF               'X'
             1072  LOAD_CONST               None
             1074  COMPARE_OP               is
         1076_1078  POP_JUMP_IF_FALSE  1092  'to 1092'

 L.1160      1080  LOAD_GLOBAL              np
             1082  LOAD_METHOD              array
             1084  BUILD_LIST_0          0 
             1086  LOAD_FAST                'dtype'
             1088  CALL_METHOD_2         2  ''
             1090  STORE_DEREF              'X'
           1092_0  COME_FROM          1076  '1076'

 L.1164      1092  LOAD_DEREF               'X'
             1094  LOAD_ATTR                ndim
             1096  LOAD_CONST               3
             1098  COMPARE_OP               ==
         1100_1102  POP_JUMP_IF_FALSE  1130  'to 1130'
             1104  LOAD_DEREF               'X'
             1106  LOAD_ATTR                shape
             1108  LOAD_CONST               None
             1110  LOAD_CONST               2
             1112  BUILD_SLICE_2         2 
             1114  BINARY_SUBSCR    
             1116  LOAD_CONST               (1, 1)
             1118  COMPARE_OP               ==
         1120_1122  POP_JUMP_IF_FALSE  1130  'to 1130'

 L.1165      1124  LOAD_CONST               (1, -1)
             1126  LOAD_DEREF               'X'
             1128  STORE_ATTR               shape
           1130_0  COME_FROM          1120  '1120'
           1130_1  COME_FROM          1100  '1100'

 L.1169      1130  LOAD_DEREF               'X'
             1132  LOAD_ATTR                ndim
             1134  LOAD_FAST                'ndmin'
             1136  COMPARE_OP               >
         1138_1140  POP_JUMP_IF_FALSE  1152  'to 1152'

 L.1170      1142  LOAD_GLOBAL              np
             1144  LOAD_METHOD              squeeze
             1146  LOAD_DEREF               'X'
             1148  CALL_METHOD_1         1  ''
             1150  STORE_DEREF              'X'
           1152_0  COME_FROM          1138  '1138'

 L.1173      1152  LOAD_DEREF               'X'
             1154  LOAD_ATTR                ndim
             1156  LOAD_FAST                'ndmin'
             1158  COMPARE_OP               <
         1160_1162  POP_JUMP_IF_FALSE  1208  'to 1208'

 L.1174      1164  LOAD_FAST                'ndmin'
             1166  LOAD_CONST               1
             1168  COMPARE_OP               ==
         1170_1172  POP_JUMP_IF_FALSE  1186  'to 1186'

 L.1175      1174  LOAD_GLOBAL              np
             1176  LOAD_METHOD              atleast_1d
             1178  LOAD_DEREF               'X'
             1180  CALL_METHOD_1         1  ''
             1182  STORE_DEREF              'X'
             1184  JUMP_FORWARD       1208  'to 1208'
           1186_0  COME_FROM          1170  '1170'

 L.1176      1186  LOAD_FAST                'ndmin'
             1188  LOAD_CONST               2
             1190  COMPARE_OP               ==
         1192_1194  POP_JUMP_IF_FALSE  1208  'to 1208'

 L.1177      1196  LOAD_GLOBAL              np
             1198  LOAD_METHOD              atleast_2d
             1200  LOAD_DEREF               'X'
             1202  CALL_METHOD_1         1  ''
             1204  LOAD_ATTR                T
             1206  STORE_DEREF              'X'
           1208_0  COME_FROM          1192  '1192'
           1208_1  COME_FROM          1184  '1184'
           1208_2  COME_FROM          1160  '1160'

 L.1179      1208  LOAD_FAST                'unpack'
         1210_1212  POP_JUMP_IF_FALSE  1256  'to 1256'

 L.1180      1214  LOAD_GLOBAL              len
             1216  LOAD_FAST                'dtype_types'
             1218  CALL_FUNCTION_1       1  ''
             1220  LOAD_CONST               1
             1222  COMPARE_OP               >
         1224_1226  POP_JUMP_IF_FALSE  1248  'to 1248'

 L.1182      1228  LOAD_CLOSURE             'X'
             1230  BUILD_TUPLE_1         1 
             1232  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1234  LOAD_STR                 'loadtxt.<locals>.<listcomp>'
             1236  MAKE_FUNCTION_8          'closure'
             1238  LOAD_FAST                'dtype'
             1240  LOAD_ATTR                names
             1242  GET_ITER         
             1244  CALL_FUNCTION_1       1  ''
             1246  RETURN_VALUE     
           1248_0  COME_FROM          1224  '1224'

 L.1184      1248  LOAD_DEREF               'X'
             1250  LOAD_ATTR                T
             1252  RETURN_VALUE     
             1254  JUMP_FORWARD       1260  'to 1260'
           1256_0  COME_FROM          1210  '1210'

 L.1186      1256  LOAD_DEREF               'X'
             1258  RETURN_VALUE     
           1260_0  COME_FROM          1254  '1254'

Parse error at or near `COME_FROM' instruction at offset 872_0


_loadtxt_with_like = array_function_dispatch(_loadtxt_dispatcher)(loadtxt)

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

    class WriteWrap:
        __doc__ = 'Convert to bytes on bytestream inputs.\n\n        '

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
        elif isinstance(fmt, str):
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
            except TypeError as e:
                try:
                    raise TypeError("Mismatch between array dtype ('%s') and format specifier ('%s')" % (
                     str(X.dtype), format)) from e
                finally:
                    e = None
                    del e

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

 L.1508         0  LOAD_CONST               False
                2  STORE_FAST               'own_fh'

 L.1509         4  LOAD_GLOBAL              hasattr
                6  LOAD_FAST                'file'
                8  LOAD_STR                 'read'
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_TRUE     38  'to 38'

 L.1510        14  LOAD_GLOBAL              np
               16  LOAD_ATTR                lib
               18  LOAD_ATTR                _datasource
               20  LOAD_ATTR                open
               22  LOAD_FAST                'file'
               24  LOAD_STR                 'rt'
               26  LOAD_FAST                'encoding'
               28  LOAD_CONST               ('encoding',)
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  STORE_FAST               'file'

 L.1511        34  LOAD_CONST               True
               36  STORE_FAST               'own_fh'
             38_0  COME_FROM            12  '12'

 L.1513        38  SETUP_FINALLY       248  'to 248'

 L.1514        40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'dtype'
               44  LOAD_GLOBAL              np
               46  LOAD_ATTR                dtype
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_TRUE     62  'to 62'

 L.1515        52  LOAD_GLOBAL              np
               54  LOAD_METHOD              dtype
               56  LOAD_FAST                'dtype'
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'dtype'
             62_0  COME_FROM            50  '50'

 L.1517        62  LOAD_FAST                'file'
               64  LOAD_METHOD              read
               66  CALL_METHOD_0         0  ''
               68  STORE_FAST               'content'

 L.1518        70  LOAD_GLOBAL              isinstance
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

 L.1519        94  LOAD_GLOBAL              asbytes
               96  LOAD_FAST                'regexp'
               98  CALL_FUNCTION_1       1  ''
              100  STORE_FAST               'regexp'
              102  JUMP_FORWARD        136  'to 136'
            104_0  COME_FROM            92  '92'
            104_1  COME_FROM            78  '78'

 L.1520       104  LOAD_GLOBAL              isinstance
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

 L.1521       128  LOAD_GLOBAL              asstr
              130  LOAD_FAST                'regexp'
              132  CALL_FUNCTION_1       1  ''
              134  STORE_FAST               'regexp'
            136_0  COME_FROM           126  '126'
            136_1  COME_FROM           116  '116'
            136_2  COME_FROM           102  '102'

 L.1523       136  LOAD_GLOBAL              hasattr
              138  LOAD_FAST                'regexp'
              140  LOAD_STR                 'match'
              142  CALL_FUNCTION_2       2  ''
              144  POP_JUMP_IF_TRUE    156  'to 156'

 L.1524       146  LOAD_GLOBAL              re
              148  LOAD_METHOD              compile
              150  LOAD_FAST                'regexp'
              152  CALL_METHOD_1         1  ''
              154  STORE_FAST               'regexp'
            156_0  COME_FROM           144  '144'

 L.1525       156  LOAD_FAST                'regexp'
              158  LOAD_METHOD              findall
              160  LOAD_FAST                'content'
              162  CALL_METHOD_1         1  ''
              164  STORE_FAST               'seq'

 L.1526       166  LOAD_FAST                'seq'
              168  POP_JUMP_IF_FALSE   226  'to 226'
              170  LOAD_GLOBAL              isinstance
              172  LOAD_FAST                'seq'
              174  LOAD_CONST               0
              176  BINARY_SUBSCR    
              178  LOAD_GLOBAL              tuple
              180  CALL_FUNCTION_2       2  ''
              182  POP_JUMP_IF_TRUE    226  'to 226'

 L.1530       184  LOAD_GLOBAL              np
              186  LOAD_METHOD              dtype
              188  LOAD_FAST                'dtype'
              190  LOAD_FAST                'dtype'
              192  LOAD_ATTR                names
              194  LOAD_CONST               0
              196  BINARY_SUBSCR    
              198  BINARY_SUBSCR    
              200  CALL_METHOD_1         1  ''
              202  STORE_FAST               'newdtype'

 L.1531       204  LOAD_GLOBAL              np
              206  LOAD_ATTR                array
              208  LOAD_FAST                'seq'
              210  LOAD_FAST                'newdtype'
              212  LOAD_CONST               ('dtype',)
              214  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              216  STORE_FAST               'output'

 L.1532       218  LOAD_FAST                'dtype'
              220  LOAD_FAST                'output'
              222  STORE_ATTR               dtype
              224  JUMP_FORWARD        240  'to 240'
            226_0  COME_FROM           182  '182'
            226_1  COME_FROM           168  '168'

 L.1534       226  LOAD_GLOBAL              np
              228  LOAD_ATTR                array
              230  LOAD_FAST                'seq'
              232  LOAD_FAST                'dtype'
              234  LOAD_CONST               ('dtype',)
              236  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              238  STORE_FAST               'output'
            240_0  COME_FROM           224  '224'

 L.1536       240  LOAD_FAST                'output'
              242  POP_BLOCK        
              244  CALL_FINALLY        248  'to 248'
              246  RETURN_VALUE     
            248_0  COME_FROM           244  '244'
            248_1  COME_FROM_FINALLY    38  '38'

 L.1538       248  LOAD_FAST                'own_fh'
          250_252  POP_JUMP_IF_FALSE   262  'to 262'

 L.1539       254  LOAD_FAST                'file'
              256  LOAD_METHOD              close
              258  CALL_METHOD_0         0  ''
              260  POP_TOP          
            262_0  COME_FROM           250  '250'
              262  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 244


def _genfromtxt_dispatcher(fname, dtype=None, comments=None, delimiter=None, skip_header=None, skip_footer=None, converters=None, missing_values=None, filling_values=None, usecols=None, names=None, excludelist=None, deletechars=None, replace_space=None, autostrip=None, case_sensitive=None, defaultfmt=None, unpack=None, usemask=None, loose=None, invalid_raise=None, max_rows=None, encoding=None, *, like=None):
    return (
     like,)


@set_array_function_like_doc
@set_module('numpy')
def genfromtxt--- This code section failed: ---

 L.1749         0  LOAD_FAST                'like'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    64  'to 64'

 L.1750         8  LOAD_GLOBAL              _genfromtxt_with_like

 L.1751        10  LOAD_FAST                'fname'

 L.1751        12  LOAD_DEREF               'dtype'

 L.1751        14  LOAD_FAST                'comments'

 L.1751        16  LOAD_FAST                'delimiter'

 L.1752        18  LOAD_DEREF               'skip_header'

 L.1752        20  LOAD_FAST                'skip_footer'

 L.1753        22  LOAD_FAST                'converters'

 L.1753        24  LOAD_FAST                'missing_values'

 L.1754        26  LOAD_FAST                'filling_values'

 L.1754        28  LOAD_FAST                'usecols'

 L.1754        30  LOAD_DEREF               'names'

 L.1755        32  LOAD_FAST                'excludelist'

 L.1755        34  LOAD_FAST                'deletechars'

 L.1756        36  LOAD_FAST                'replace_space'

 L.1756        38  LOAD_FAST                'autostrip'

 L.1757        40  LOAD_FAST                'case_sensitive'

 L.1757        42  LOAD_DEREF               'defaultfmt'

 L.1758        44  LOAD_FAST                'unpack'

 L.1758        46  LOAD_FAST                'usemask'

 L.1758        48  LOAD_FAST                'loose'

 L.1759        50  LOAD_FAST                'invalid_raise'

 L.1759        52  LOAD_FAST                'max_rows'

 L.1759        54  LOAD_FAST                'encoding'

 L.1760        56  LOAD_FAST                'like'

 L.1750        58  LOAD_CONST               ('dtype', 'comments', 'delimiter', 'skip_header', 'skip_footer', 'converters', 'missing_values', 'filling_values', 'usecols', 'names', 'excludelist', 'deletechars', 'replace_space', 'autostrip', 'case_sensitive', 'defaultfmt', 'unpack', 'usemask', 'loose', 'invalid_raise', 'max_rows', 'encoding', 'like')
               60  CALL_FUNCTION_KW_24    24  '24 total positional and keyword args'
               62  RETURN_VALUE     
             64_0  COME_FROM             6  '6'

 L.1763        64  LOAD_FAST                'max_rows'
               66  LOAD_CONST               None
               68  COMPARE_OP               is-not
               70  POP_JUMP_IF_FALSE   100  'to 100'

 L.1764        72  LOAD_FAST                'skip_footer'
               74  POP_JUMP_IF_FALSE    84  'to 84'

 L.1765        76  LOAD_GLOBAL              ValueError

 L.1766        78  LOAD_STR                 "The keywords 'skip_footer' and 'max_rows' can not be specified at the same time."

 L.1765        80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            74  '74'

 L.1768        84  LOAD_FAST                'max_rows'
               86  LOAD_CONST               1
               88  COMPARE_OP               <
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L.1769        92  LOAD_GLOBAL              ValueError
               94  LOAD_STR                 "'max_rows' must be at least 1."
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            90  '90'
            100_1  COME_FROM            70  '70'

 L.1771       100  LOAD_FAST                'usemask'
              102  POP_JUMP_IF_FALSE   120  'to 120'

 L.1772       104  LOAD_CONST               0
              106  LOAD_CONST               ('MaskedArray', 'make_mask_descr')
              108  IMPORT_NAME_ATTR         numpy.ma
              110  IMPORT_FROM              MaskedArray
              112  STORE_FAST               'MaskedArray'
              114  IMPORT_FROM              make_mask_descr
              116  STORE_FAST               'make_mask_descr'
              118  POP_TOP          
            120_0  COME_FROM           102  '102'

 L.1774       120  LOAD_FAST                'converters'
              122  JUMP_IF_TRUE_OR_POP   126  'to 126'
              124  BUILD_MAP_0           0 
            126_0  COME_FROM           122  '122'
              126  STORE_FAST               'user_converters'

 L.1775       128  LOAD_GLOBAL              isinstance
              130  LOAD_FAST                'user_converters'
              132  LOAD_GLOBAL              dict
              134  CALL_FUNCTION_2       2  ''
              136  POP_JUMP_IF_TRUE    154  'to 154'

 L.1776       138  LOAD_GLOBAL              TypeError

 L.1777       140  LOAD_STR                 "The input argument 'converter' should be a valid dictionary (got '%s' instead)"

 L.1778       142  LOAD_GLOBAL              type
              144  LOAD_FAST                'user_converters'
              146  CALL_FUNCTION_1       1  ''

 L.1777       148  BINARY_MODULO    

 L.1776       150  CALL_FUNCTION_1       1  ''
              152  RAISE_VARARGS_1       1  'exception instance'
            154_0  COME_FROM           136  '136'

 L.1780       154  LOAD_FAST                'encoding'
              156  LOAD_STR                 'bytes'
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   172  'to 172'

 L.1781       162  LOAD_CONST               None
              164  STORE_FAST               'encoding'

 L.1782       166  LOAD_CONST               True
              168  STORE_FAST               'byte_converters'
              170  JUMP_FORWARD        176  'to 176'
            172_0  COME_FROM           160  '160'

 L.1784       172  LOAD_CONST               False
              174  STORE_FAST               'byte_converters'
            176_0  COME_FROM           170  '170'

 L.1787       176  SETUP_FINALLY       262  'to 262'

 L.1788       178  LOAD_GLOBAL              isinstance
              180  LOAD_FAST                'fname'
              182  LOAD_GLOBAL              os_PathLike
              184  CALL_FUNCTION_2       2  ''
              186  POP_JUMP_IF_FALSE   196  'to 196'

 L.1789       188  LOAD_GLOBAL              os_fspath
              190  LOAD_FAST                'fname'
              192  CALL_FUNCTION_1       1  ''
              194  STORE_FAST               'fname'
            196_0  COME_FROM           186  '186'

 L.1790       196  LOAD_GLOBAL              isinstance
              198  LOAD_FAST                'fname'
              200  LOAD_GLOBAL              str
              202  CALL_FUNCTION_2       2  ''
              204  POP_JUMP_IF_FALSE   238  'to 238'

 L.1791       206  LOAD_GLOBAL              np
              208  LOAD_ATTR                lib
              210  LOAD_ATTR                _datasource
              212  LOAD_ATTR                open
              214  LOAD_FAST                'fname'
              216  LOAD_STR                 'rt'
              218  LOAD_FAST                'encoding'
              220  LOAD_CONST               ('encoding',)
              222  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              224  STORE_FAST               'fid'

 L.1792       226  LOAD_GLOBAL              contextlib
              228  LOAD_METHOD              closing
              230  LOAD_FAST                'fid'
              232  CALL_METHOD_1         1  ''
              234  STORE_FAST               'fid_ctx'
              236  JUMP_FORWARD        250  'to 250'
            238_0  COME_FROM           204  '204'

 L.1794       238  LOAD_FAST                'fname'
              240  STORE_FAST               'fid'

 L.1795       242  LOAD_GLOBAL              contextlib_nullcontext
              244  LOAD_FAST                'fid'
              246  CALL_FUNCTION_1       1  ''
              248  STORE_FAST               'fid_ctx'
            250_0  COME_FROM           236  '236'

 L.1796       250  LOAD_GLOBAL              iter
              252  LOAD_FAST                'fid'
              254  CALL_FUNCTION_1       1  ''
              256  STORE_FAST               'fhd'
              258  POP_BLOCK        
              260  JUMP_FORWARD        316  'to 316'
            262_0  COME_FROM_FINALLY   176  '176'

 L.1797       262  DUP_TOP          
              264  LOAD_GLOBAL              TypeError
              266  COMPARE_OP               exception-match
          268_270  POP_JUMP_IF_FALSE   314  'to 314'
              272  POP_TOP          
              274  STORE_FAST               'e'
              276  POP_TOP          
              278  SETUP_FINALLY       302  'to 302'

 L.1798       280  LOAD_GLOBAL              TypeError

 L.1799       282  LOAD_STR                 'fname must be a string, filehandle, list of strings, or generator. Got %s instead.'

 L.1800       284  LOAD_GLOBAL              type
              286  LOAD_FAST                'fname'
              288  CALL_FUNCTION_1       1  ''

 L.1799       290  BINARY_MODULO    

 L.1798       292  CALL_FUNCTION_1       1  ''

 L.1800       294  LOAD_FAST                'e'

 L.1798       296  RAISE_VARARGS_2       2  'exception instance with __cause__'
              298  POP_BLOCK        
              300  BEGIN_FINALLY    
            302_0  COME_FROM_FINALLY   278  '278'
              302  LOAD_CONST               None
              304  STORE_FAST               'e'
              306  DELETE_FAST              'e'
              308  END_FINALLY      
              310  POP_EXCEPT       
              312  JUMP_FORWARD        316  'to 316'
            314_0  COME_FROM           268  '268'
              314  END_FINALLY      
            316_0  COME_FROM           312  '312'
            316_1  COME_FROM           260  '260'

 L.1802       316  LOAD_FAST                'fid_ctx'
          318_320  SETUP_WITH         2356  'to 2356'
              322  POP_TOP          

 L.1803       324  LOAD_GLOBAL              LineSplitter
              326  LOAD_FAST                'delimiter'
              328  LOAD_FAST                'comments'

 L.1804       330  LOAD_FAST                'autostrip'

 L.1804       332  LOAD_FAST                'encoding'

 L.1803       334  LOAD_CONST               ('delimiter', 'comments', 'autostrip', 'encoding')
              336  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              338  STORE_FAST               'split_line'

 L.1805       340  LOAD_GLOBAL              NameValidator
              342  LOAD_FAST                'excludelist'

 L.1806       344  LOAD_FAST                'deletechars'

 L.1807       346  LOAD_FAST                'case_sensitive'

 L.1808       348  LOAD_FAST                'replace_space'

 L.1805       350  LOAD_CONST               ('excludelist', 'deletechars', 'case_sensitive', 'replace_space')
              352  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              354  STORE_FAST               'validate_names'

 L.1811       356  SETUP_FINALLY       476  'to 476'

 L.1812       358  LOAD_GLOBAL              range
              360  LOAD_DEREF               'skip_header'
              362  CALL_FUNCTION_1       1  ''
              364  GET_ITER         
            366_0  COME_FROM           378  '378'
              366  FOR_ITER            382  'to 382'
              368  STORE_DEREF              'i'

 L.1813       370  LOAD_GLOBAL              next
              372  LOAD_FAST                'fhd'
              374  CALL_FUNCTION_1       1  ''
              376  POP_TOP          
          378_380  JUMP_BACK           366  'to 366'
            382_0  COME_FROM           366  '366'

 L.1816       382  LOAD_CONST               None
              384  STORE_FAST               'first_values'
            386_0  COME_FROM           468  '468'

 L.1818       386  LOAD_FAST                'first_values'
          388_390  POP_JUMP_IF_TRUE    472  'to 472'

 L.1819       392  LOAD_GLOBAL              _decode_line
              394  LOAD_GLOBAL              next
              396  LOAD_FAST                'fhd'
              398  CALL_FUNCTION_1       1  ''
              400  LOAD_FAST                'encoding'
              402  CALL_FUNCTION_2       2  ''
              404  STORE_FAST               'first_line'

 L.1820       406  LOAD_DEREF               'names'
              408  LOAD_CONST               True
              410  COMPARE_OP               is
          412_414  POP_JUMP_IF_FALSE   460  'to 460'
              416  LOAD_FAST                'comments'
              418  LOAD_CONST               None
              420  COMPARE_OP               is-not
          422_424  POP_JUMP_IF_FALSE   460  'to 460'

 L.1821       426  LOAD_FAST                'comments'
              428  LOAD_FAST                'first_line'
              430  COMPARE_OP               in
          432_434  POP_JUMP_IF_FALSE   460  'to 460'

 L.1823       436  LOAD_STR                 ''
              438  LOAD_METHOD              join
              440  LOAD_FAST                'first_line'
              442  LOAD_METHOD              split
              444  LOAD_FAST                'comments'
              446  CALL_METHOD_1         1  ''
              448  LOAD_CONST               1
              450  LOAD_CONST               None
              452  BUILD_SLICE_2         2 
              454  BINARY_SUBSCR    
              456  CALL_METHOD_1         1  ''

 L.1822       458  STORE_FAST               'first_line'
            460_0  COME_FROM           432  '432'
            460_1  COME_FROM           422  '422'
            460_2  COME_FROM           412  '412'

 L.1824       460  LOAD_FAST                'split_line'
              462  LOAD_FAST                'first_line'
              464  CALL_FUNCTION_1       1  ''
              466  STORE_FAST               'first_values'
          468_470  JUMP_BACK           386  'to 386'
            472_0  COME_FROM           388  '388'
              472  POP_BLOCK        
              474  JUMP_FORWARD        524  'to 524'
            476_0  COME_FROM_FINALLY   356  '356'

 L.1825       476  DUP_TOP          
              478  LOAD_GLOBAL              StopIteration
              480  COMPARE_OP               exception-match
          482_484  POP_JUMP_IF_FALSE   522  'to 522'
              486  POP_TOP          
              488  POP_TOP          
              490  POP_TOP          

 L.1827       492  LOAD_STR                 ''
              494  STORE_FAST               'first_line'

 L.1828       496  BUILD_LIST_0          0 
              498  STORE_FAST               'first_values'

 L.1829       500  LOAD_GLOBAL              warnings
              502  LOAD_ATTR                warn
              504  LOAD_STR                 'genfromtxt: Empty input file: "%s"'
              506  LOAD_FAST                'fname'
              508  BINARY_MODULO    
              510  LOAD_CONST               2
              512  LOAD_CONST               ('stacklevel',)
              514  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              516  POP_TOP          
              518  POP_EXCEPT       
              520  JUMP_FORWARD        524  'to 524'
            522_0  COME_FROM           482  '482'
              522  END_FINALLY      
            524_0  COME_FROM           520  '520'
            524_1  COME_FROM           474  '474'

 L.1832       524  LOAD_DEREF               'names'
              526  LOAD_CONST               True
              528  COMPARE_OP               is
          530_532  POP_JUMP_IF_FALSE   572  'to 572'

 L.1833       534  LOAD_FAST                'first_values'
              536  LOAD_CONST               0
              538  BINARY_SUBSCR    
              540  LOAD_METHOD              strip
              542  CALL_METHOD_0         0  ''
              544  STORE_FAST               'fval'

 L.1834       546  LOAD_FAST                'comments'
              548  LOAD_CONST               None
              550  COMPARE_OP               is-not
          552_554  POP_JUMP_IF_FALSE   572  'to 572'

 L.1835       556  LOAD_FAST                'fval'
              558  LOAD_FAST                'comments'
              560  COMPARE_OP               in
          562_564  POP_JUMP_IF_FALSE   572  'to 572'

 L.1836       566  LOAD_FAST                'first_values'
              568  LOAD_CONST               0
              570  DELETE_SUBSCR    
            572_0  COME_FROM           562  '562'
            572_1  COME_FROM           552  '552'
            572_2  COME_FROM           530  '530'

 L.1839       572  LOAD_FAST                'usecols'
              574  LOAD_CONST               None
              576  COMPARE_OP               is-not
          578_580  POP_JUMP_IF_FALSE   672  'to 672'

 L.1840       582  SETUP_FINALLY       608  'to 608'

 L.1841       584  LOAD_LISTCOMP            '<code_object <listcomp>>'
              586  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
              588  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              590  LOAD_FAST                'usecols'
              592  LOAD_METHOD              split
              594  LOAD_STR                 ','
              596  CALL_METHOD_1         1  ''
              598  GET_ITER         
              600  CALL_FUNCTION_1       1  ''
              602  STORE_FAST               'usecols'
              604  POP_BLOCK        
              606  JUMP_FORWARD        672  'to 672'
            608_0  COME_FROM_FINALLY   582  '582'

 L.1842       608  DUP_TOP          
              610  LOAD_GLOBAL              AttributeError
              612  COMPARE_OP               exception-match
          614_616  POP_JUMP_IF_FALSE   670  'to 670'
              618  POP_TOP          
              620  POP_TOP          
              622  POP_TOP          

 L.1843       624  SETUP_FINALLY       638  'to 638'

 L.1844       626  LOAD_GLOBAL              list
              628  LOAD_FAST                'usecols'
              630  CALL_FUNCTION_1       1  ''
              632  STORE_FAST               'usecols'
              634  POP_BLOCK        
              636  JUMP_FORWARD        666  'to 666'
            638_0  COME_FROM_FINALLY   624  '624'

 L.1845       638  DUP_TOP          
              640  LOAD_GLOBAL              TypeError
              642  COMPARE_OP               exception-match
          644_646  POP_JUMP_IF_FALSE   664  'to 664'
              648  POP_TOP          
              650  POP_TOP          
              652  POP_TOP          

 L.1846       654  LOAD_FAST                'usecols'
              656  BUILD_LIST_1          1 
              658  STORE_FAST               'usecols'
              660  POP_EXCEPT       
              662  JUMP_FORWARD        666  'to 666'
            664_0  COME_FROM           644  '644'
              664  END_FINALLY      
            666_0  COME_FROM           662  '662'
            666_1  COME_FROM           636  '636'
              666  POP_EXCEPT       
              668  JUMP_FORWARD        672  'to 672'
            670_0  COME_FROM           614  '614'
              670  END_FINALLY      
            672_0  COME_FROM           668  '668'
            672_1  COME_FROM           606  '606'
            672_2  COME_FROM           578  '578'

 L.1847       672  LOAD_GLOBAL              len
              674  LOAD_FAST                'usecols'
          676_678  JUMP_IF_TRUE_OR_POP   682  'to 682'
              680  LOAD_FAST                'first_values'
            682_0  COME_FROM           676  '676'
              682  CALL_FUNCTION_1       1  ''
              684  STORE_FAST               'nbcols'

 L.1850       686  LOAD_DEREF               'names'
              688  LOAD_CONST               True
              690  COMPARE_OP               is
          692_694  POP_JUMP_IF_FALSE   720  'to 720'

 L.1851       696  LOAD_FAST                'validate_names'
              698  LOAD_LISTCOMP            '<code_object <listcomp>>'
              700  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
              702  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              704  LOAD_FAST                'first_values'
              706  GET_ITER         
              708  CALL_FUNCTION_1       1  ''
              710  CALL_FUNCTION_1       1  ''
              712  STORE_DEREF              'names'

 L.1852       714  LOAD_STR                 ''
              716  STORE_FAST               'first_line'
              718  JUMP_FORWARD        770  'to 770'
            720_0  COME_FROM           692  '692'

 L.1853       720  LOAD_GLOBAL              _is_string_like
              722  LOAD_DEREF               'names'
              724  CALL_FUNCTION_1       1  ''
          726_728  POP_JUMP_IF_FALSE   756  'to 756'

 L.1854       730  LOAD_FAST                'validate_names'
              732  LOAD_LISTCOMP            '<code_object <listcomp>>'
              734  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
              736  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              738  LOAD_DEREF               'names'
              740  LOAD_METHOD              split
              742  LOAD_STR                 ','
              744  CALL_METHOD_1         1  ''
              746  GET_ITER         
              748  CALL_FUNCTION_1       1  ''
              750  CALL_FUNCTION_1       1  ''
              752  STORE_DEREF              'names'
              754  JUMP_FORWARD        770  'to 770'
            756_0  COME_FROM           726  '726'

 L.1855       756  LOAD_DEREF               'names'
          758_760  POP_JUMP_IF_FALSE   770  'to 770'

 L.1856       762  LOAD_FAST                'validate_names'
              764  LOAD_DEREF               'names'
              766  CALL_FUNCTION_1       1  ''
              768  STORE_DEREF              'names'
            770_0  COME_FROM           758  '758'
            770_1  COME_FROM           754  '754'
            770_2  COME_FROM           718  '718'

 L.1858       770  LOAD_DEREF               'dtype'
              772  LOAD_CONST               None
              774  COMPARE_OP               is-not
          776_778  POP_JUMP_IF_FALSE   802  'to 802'

 L.1859       780  LOAD_GLOBAL              easy_dtype
              782  LOAD_DEREF               'dtype'
              784  LOAD_DEREF               'defaultfmt'
              786  LOAD_DEREF               'names'

 L.1860       788  LOAD_FAST                'excludelist'

 L.1861       790  LOAD_FAST                'deletechars'

 L.1862       792  LOAD_FAST                'case_sensitive'

 L.1863       794  LOAD_FAST                'replace_space'

 L.1859       796  LOAD_CONST               ('defaultfmt', 'names', 'excludelist', 'deletechars', 'case_sensitive', 'replace_space')
              798  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              800  STORE_DEREF              'dtype'
            802_0  COME_FROM           776  '776'

 L.1865       802  LOAD_DEREF               'names'
              804  LOAD_CONST               None
              806  COMPARE_OP               is-not
          808_810  POP_JUMP_IF_FALSE   820  'to 820'

 L.1866       812  LOAD_GLOBAL              list
              814  LOAD_DEREF               'names'
              816  CALL_FUNCTION_1       1  ''
              818  STORE_DEREF              'names'
            820_0  COME_FROM           808  '808'

 L.1868       820  LOAD_FAST                'usecols'
          822_824  POP_JUMP_IF_FALSE  1008  'to 1008'

 L.1869       826  LOAD_GLOBAL              enumerate
              828  LOAD_FAST                'usecols'
              830  CALL_FUNCTION_1       1  ''
              832  GET_ITER         
            834_0  COME_FROM           894  '894'
            834_1  COME_FROM           874  '874'
            834_2  COME_FROM           866  '866'
              834  FOR_ITER            898  'to 898'
              836  UNPACK_SEQUENCE_2     2 
              838  STORE_DEREF              'i'
              840  STORE_FAST               'current'

 L.1871       842  LOAD_GLOBAL              _is_string_like
              844  LOAD_FAST                'current'
              846  CALL_FUNCTION_1       1  ''
          848_850  POP_JUMP_IF_FALSE   868  'to 868'

 L.1872       852  LOAD_DEREF               'names'
              854  LOAD_METHOD              index
              856  LOAD_FAST                'current'
              858  CALL_METHOD_1         1  ''
              860  LOAD_FAST                'usecols'
              862  LOAD_DEREF               'i'
              864  STORE_SUBSCR     
              866  JUMP_BACK           834  'to 834'
            868_0  COME_FROM           848  '848'

 L.1873       868  LOAD_FAST                'current'
              870  LOAD_CONST               0
              872  COMPARE_OP               <
          874_876  POP_JUMP_IF_FALSE_BACK   834  'to 834'

 L.1874       878  LOAD_FAST                'current'
              880  LOAD_GLOBAL              len
              882  LOAD_FAST                'first_values'
              884  CALL_FUNCTION_1       1  ''
              886  BINARY_ADD       
              888  LOAD_FAST                'usecols'
              890  LOAD_DEREF               'i'
              892  STORE_SUBSCR     
          894_896  JUMP_BACK           834  'to 834'
            898_0  COME_FROM           834  '834'

 L.1876       898  LOAD_DEREF               'dtype'
              900  LOAD_CONST               None
              902  COMPARE_OP               is-not
          904_906  POP_JUMP_IF_FALSE   964  'to 964'
              908  LOAD_GLOBAL              len
              910  LOAD_DEREF               'dtype'
              912  CALL_FUNCTION_1       1  ''
              914  LOAD_FAST                'nbcols'
              916  COMPARE_OP               >
          918_920  POP_JUMP_IF_FALSE   964  'to 964'

 L.1877       922  LOAD_DEREF               'dtype'
              924  LOAD_ATTR                descr
              926  STORE_DEREF              'descr'

 L.1878       928  LOAD_GLOBAL              np
              930  LOAD_METHOD              dtype
              932  LOAD_CLOSURE             'descr'
              934  BUILD_TUPLE_1         1 
              936  LOAD_LISTCOMP            '<code_object <listcomp>>'
              938  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
              940  MAKE_FUNCTION_8          'closure'
              942  LOAD_FAST                'usecols'
              944  GET_ITER         
              946  CALL_FUNCTION_1       1  ''
              948  CALL_METHOD_1         1  ''
              950  STORE_DEREF              'dtype'

 L.1879       952  LOAD_GLOBAL              list
              954  LOAD_DEREF               'dtype'
              956  LOAD_ATTR                names
              958  CALL_FUNCTION_1       1  ''
              960  STORE_DEREF              'names'
              962  JUMP_FORWARD       1006  'to 1006'
            964_0  COME_FROM           918  '918'
            964_1  COME_FROM           904  '904'

 L.1881       964  LOAD_DEREF               'names'
              966  LOAD_CONST               None
              968  COMPARE_OP               is-not
          970_972  POP_JUMP_IF_FALSE  1038  'to 1038'
              974  LOAD_GLOBAL              len
              976  LOAD_DEREF               'names'
              978  CALL_FUNCTION_1       1  ''
              980  LOAD_FAST                'nbcols'
              982  COMPARE_OP               >
          984_986  POP_JUMP_IF_FALSE  1038  'to 1038'

 L.1882       988  LOAD_CLOSURE             'names'
              990  BUILD_TUPLE_1         1 
              992  LOAD_LISTCOMP            '<code_object <listcomp>>'
              994  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
              996  MAKE_FUNCTION_8          'closure'
              998  LOAD_FAST                'usecols'
             1000  GET_ITER         
             1002  CALL_FUNCTION_1       1  ''
             1004  STORE_DEREF              'names'
           1006_0  COME_FROM           962  '962'
             1006  JUMP_FORWARD       1038  'to 1038'
           1008_0  COME_FROM           822  '822'

 L.1883      1008  LOAD_DEREF               'names'
             1010  LOAD_CONST               None
             1012  COMPARE_OP               is-not
         1014_1016  POP_JUMP_IF_FALSE  1038  'to 1038'
             1018  LOAD_DEREF               'dtype'
             1020  LOAD_CONST               None
             1022  COMPARE_OP               is-not
         1024_1026  POP_JUMP_IF_FALSE  1038  'to 1038'

 L.1884      1028  LOAD_GLOBAL              list
             1030  LOAD_DEREF               'dtype'
             1032  LOAD_ATTR                names
             1034  CALL_FUNCTION_1       1  ''
             1036  STORE_DEREF              'names'
           1038_0  COME_FROM          1024  '1024'
           1038_1  COME_FROM          1014  '1014'
           1038_2  COME_FROM          1006  '1006'
           1038_3  COME_FROM           984  '984'
           1038_4  COME_FROM           970  '970'

 L.1888      1038  LOAD_FAST                'missing_values'
         1040_1042  JUMP_IF_TRUE_OR_POP  1046  'to 1046'
             1044  LOAD_CONST               ()
           1046_0  COME_FROM          1040  '1040'
             1046  STORE_FAST               'user_missing_values'

 L.1889      1048  LOAD_GLOBAL              isinstance
             1050  LOAD_FAST                'user_missing_values'
             1052  LOAD_GLOBAL              bytes
             1054  CALL_FUNCTION_2       2  ''
         1056_1058  POP_JUMP_IF_FALSE  1070  'to 1070'

 L.1890      1060  LOAD_FAST                'user_missing_values'
             1062  LOAD_METHOD              decode
             1064  LOAD_STR                 'latin1'
             1066  CALL_METHOD_1         1  ''
             1068  STORE_FAST               'user_missing_values'
           1070_0  COME_FROM          1056  '1056'

 L.1893      1070  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1072  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             1074  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1076  LOAD_GLOBAL              range
             1078  LOAD_FAST                'nbcols'
             1080  CALL_FUNCTION_1       1  ''
             1082  GET_ITER         
             1084  CALL_FUNCTION_1       1  ''
             1086  STORE_FAST               'missing_values'

 L.1896      1088  LOAD_GLOBAL              isinstance
             1090  LOAD_FAST                'user_missing_values'
             1092  LOAD_GLOBAL              dict
             1094  CALL_FUNCTION_2       2  ''
         1096_1098  POP_JUMP_IF_FALSE  1310  'to 1310'

 L.1898      1100  LOAD_FAST                'user_missing_values'
             1102  LOAD_METHOD              items
             1104  CALL_METHOD_0         0  ''
             1106  GET_ITER         
           1108_0  COME_FROM          1304  '1304'
           1108_1  COME_FROM          1288  '1288'
           1108_2  COME_FROM          1160  '1160'
             1108  FOR_ITER           1308  'to 1308'
             1110  UNPACK_SEQUENCE_2     2 
             1112  STORE_FAST               'key'
             1114  STORE_FAST               'val'

 L.1900      1116  LOAD_GLOBAL              _is_string_like
             1118  LOAD_FAST                'key'
             1120  CALL_FUNCTION_1       1  ''
         1122_1124  POP_JUMP_IF_FALSE  1170  'to 1170'

 L.1901      1126  SETUP_FINALLY      1142  'to 1142'

 L.1903      1128  LOAD_DEREF               'names'
             1130  LOAD_METHOD              index
             1132  LOAD_FAST                'key'
             1134  CALL_METHOD_1         1  ''
             1136  STORE_FAST               'key'
             1138  POP_BLOCK        
             1140  JUMP_FORWARD       1170  'to 1170'
           1142_0  COME_FROM_FINALLY  1126  '1126'

 L.1904      1142  DUP_TOP          
             1144  LOAD_GLOBAL              ValueError
             1146  COMPARE_OP               exception-match
         1148_1150  POP_JUMP_IF_FALSE  1168  'to 1168'
             1152  POP_TOP          
             1154  POP_TOP          
             1156  POP_TOP          

 L.1906      1158  POP_EXCEPT       
         1160_1162  JUMP_BACK          1108  'to 1108'
             1164  POP_EXCEPT       
             1166  JUMP_FORWARD       1170  'to 1170'
           1168_0  COME_FROM          1148  '1148'
             1168  END_FINALLY      
           1170_0  COME_FROM          1166  '1166'
           1170_1  COME_FROM          1140  '1140'
           1170_2  COME_FROM          1122  '1122'

 L.1908      1170  LOAD_FAST                'usecols'
         1172_1174  POP_JUMP_IF_FALSE  1214  'to 1214'

 L.1909      1176  SETUP_FINALLY      1192  'to 1192'

 L.1910      1178  LOAD_FAST                'usecols'
             1180  LOAD_METHOD              index
             1182  LOAD_FAST                'key'
             1184  CALL_METHOD_1         1  ''
             1186  STORE_FAST               'key'
             1188  POP_BLOCK        
             1190  JUMP_FORWARD       1214  'to 1214'
           1192_0  COME_FROM_FINALLY  1176  '1176'

 L.1911      1192  DUP_TOP          
             1194  LOAD_GLOBAL              ValueError
             1196  COMPARE_OP               exception-match
         1198_1200  POP_JUMP_IF_FALSE  1212  'to 1212'
             1202  POP_TOP          
             1204  POP_TOP          
             1206  POP_TOP          

 L.1912      1208  POP_EXCEPT       
             1210  BREAK_LOOP         1214  'to 1214'
           1212_0  COME_FROM          1198  '1198'
             1212  END_FINALLY      
           1214_0  COME_FROM          1210  '1210'
           1214_1  COME_FROM          1190  '1190'
           1214_2  COME_FROM          1172  '1172'

 L.1914      1214  LOAD_GLOBAL              isinstance
             1216  LOAD_FAST                'val'
             1218  LOAD_GLOBAL              list
             1220  LOAD_GLOBAL              tuple
             1222  BUILD_TUPLE_2         2 
             1224  CALL_FUNCTION_2       2  ''
         1226_1228  POP_JUMP_IF_FALSE  1246  'to 1246'

 L.1915      1230  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1232  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             1234  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1236  LOAD_FAST                'val'
             1238  GET_ITER         
             1240  CALL_FUNCTION_1       1  ''
             1242  STORE_FAST               'val'
             1244  JUMP_FORWARD       1256  'to 1256'
           1246_0  COME_FROM          1226  '1226'

 L.1917      1246  LOAD_GLOBAL              str
             1248  LOAD_FAST                'val'
             1250  CALL_FUNCTION_1       1  ''
             1252  BUILD_LIST_1          1 
             1254  STORE_FAST               'val'
           1256_0  COME_FROM          1244  '1244'

 L.1919      1256  LOAD_FAST                'key'
             1258  LOAD_CONST               None
             1260  COMPARE_OP               is
         1262_1264  POP_JUMP_IF_FALSE  1290  'to 1290'

 L.1921      1266  LOAD_FAST                'missing_values'
             1268  GET_ITER         
           1270_0  COME_FROM          1284  '1284'
             1270  FOR_ITER           1288  'to 1288'
             1272  STORE_FAST               'miss'

 L.1922      1274  LOAD_FAST                'miss'
             1276  LOAD_METHOD              extend
             1278  LOAD_FAST                'val'
             1280  CALL_METHOD_1         1  ''
             1282  POP_TOP          
         1284_1286  JUMP_BACK          1270  'to 1270'
           1288_0  COME_FROM          1270  '1270'
             1288  JUMP_BACK          1108  'to 1108'
           1290_0  COME_FROM          1262  '1262'

 L.1924      1290  LOAD_FAST                'missing_values'
             1292  LOAD_FAST                'key'
             1294  BINARY_SUBSCR    
             1296  LOAD_METHOD              extend
             1298  LOAD_FAST                'val'
             1300  CALL_METHOD_1         1  ''
             1302  POP_TOP          
         1304_1306  JUMP_BACK          1108  'to 1108'
           1308_0  COME_FROM          1108  '1108'
             1308  JUMP_FORWARD       1452  'to 1452'
           1310_0  COME_FROM          1096  '1096'

 L.1926      1310  LOAD_GLOBAL              isinstance
             1312  LOAD_FAST                'user_missing_values'
             1314  LOAD_GLOBAL              list
             1316  LOAD_GLOBAL              tuple
             1318  BUILD_TUPLE_2         2 
             1320  CALL_FUNCTION_2       2  ''
         1322_1324  POP_JUMP_IF_FALSE  1378  'to 1378'

 L.1927      1326  LOAD_GLOBAL              zip
             1328  LOAD_FAST                'user_missing_values'
             1330  LOAD_FAST                'missing_values'
             1332  CALL_FUNCTION_2       2  ''
             1334  GET_ITER         
           1336_0  COME_FROM          1372  '1372'
           1336_1  COME_FROM          1358  '1358'
             1336  FOR_ITER           1376  'to 1376'
             1338  UNPACK_SEQUENCE_2     2 
             1340  STORE_FAST               'value'
             1342  STORE_FAST               'entry'

 L.1928      1344  LOAD_GLOBAL              str
             1346  LOAD_FAST                'value'
             1348  CALL_FUNCTION_1       1  ''
             1350  STORE_FAST               'value'

 L.1929      1352  LOAD_FAST                'value'
             1354  LOAD_FAST                'entry'
             1356  COMPARE_OP               not-in
         1358_1360  POP_JUMP_IF_FALSE_BACK  1336  'to 1336'

 L.1930      1362  LOAD_FAST                'entry'
             1364  LOAD_METHOD              append
             1366  LOAD_FAST                'value'
             1368  CALL_METHOD_1         1  ''
             1370  POP_TOP          
         1372_1374  JUMP_BACK          1336  'to 1336'
           1376_0  COME_FROM          1336  '1336'
             1376  JUMP_FORWARD       1452  'to 1452'
           1378_0  COME_FROM          1322  '1322'

 L.1932      1378  LOAD_GLOBAL              isinstance
             1380  LOAD_FAST                'user_missing_values'
             1382  LOAD_GLOBAL              str
             1384  CALL_FUNCTION_2       2  ''
         1386_1388  POP_JUMP_IF_FALSE  1424  'to 1424'

 L.1933      1390  LOAD_FAST                'user_missing_values'
             1392  LOAD_METHOD              split
             1394  LOAD_STR                 ','
             1396  CALL_METHOD_1         1  ''
             1398  STORE_FAST               'user_value'

 L.1934      1400  LOAD_FAST                'missing_values'
             1402  GET_ITER         
           1404_0  COME_FROM          1418  '1418'
             1404  FOR_ITER           1422  'to 1422'
             1406  STORE_FAST               'entry'

 L.1935      1408  LOAD_FAST                'entry'
             1410  LOAD_METHOD              extend
             1412  LOAD_FAST                'user_value'
             1414  CALL_METHOD_1         1  ''
             1416  POP_TOP          
         1418_1420  JUMP_BACK          1404  'to 1404'
           1422_0  COME_FROM          1404  '1404'
             1422  JUMP_FORWARD       1452  'to 1452'
           1424_0  COME_FROM          1386  '1386'

 L.1938      1424  LOAD_FAST                'missing_values'
             1426  GET_ITER         
           1428_0  COME_FROM          1448  '1448'
             1428  FOR_ITER           1452  'to 1452'
             1430  STORE_FAST               'entry'

 L.1939      1432  LOAD_FAST                'entry'
             1434  LOAD_METHOD              extend
             1436  LOAD_GLOBAL              str
             1438  LOAD_FAST                'user_missing_values'
             1440  CALL_FUNCTION_1       1  ''
             1442  BUILD_LIST_1          1 
             1444  CALL_METHOD_1         1  ''
             1446  POP_TOP          
         1448_1450  JUMP_BACK          1428  'to 1428'
           1452_0  COME_FROM          1428  '1428'
           1452_1  COME_FROM          1422  '1422'
           1452_2  COME_FROM          1376  '1376'
           1452_3  COME_FROM          1308  '1308'

 L.1943      1452  LOAD_FAST                'filling_values'
             1454  STORE_FAST               'user_filling_values'

 L.1944      1456  LOAD_FAST                'user_filling_values'
             1458  LOAD_CONST               None
             1460  COMPARE_OP               is
         1462_1464  POP_JUMP_IF_FALSE  1470  'to 1470'

 L.1945      1466  BUILD_LIST_0          0 
             1468  STORE_FAST               'user_filling_values'
           1470_0  COME_FROM          1462  '1462'

 L.1947      1470  LOAD_CONST               None
             1472  BUILD_LIST_1          1 
             1474  LOAD_FAST                'nbcols'
             1476  BINARY_MULTIPLY  
             1478  STORE_FAST               'filling_values'

 L.1949      1480  LOAD_GLOBAL              isinstance
             1482  LOAD_FAST                'user_filling_values'
             1484  LOAD_GLOBAL              dict
             1486  CALL_FUNCTION_2       2  ''
         1488_1490  POP_JUMP_IF_FALSE  1620  'to 1620'

 L.1950      1492  LOAD_FAST                'user_filling_values'
             1494  LOAD_METHOD              items
             1496  CALL_METHOD_0         0  ''
             1498  GET_ITER         
           1500_0  COME_FROM          1614  '1614'
           1500_1  COME_FROM          1552  '1552'
             1500  FOR_ITER           1618  'to 1618'
             1502  UNPACK_SEQUENCE_2     2 
             1504  STORE_FAST               'key'
             1506  STORE_FAST               'val'

 L.1951      1508  LOAD_GLOBAL              _is_string_like
             1510  LOAD_FAST                'key'
             1512  CALL_FUNCTION_1       1  ''
         1514_1516  POP_JUMP_IF_FALSE  1562  'to 1562'

 L.1952      1518  SETUP_FINALLY      1534  'to 1534'

 L.1954      1520  LOAD_DEREF               'names'
             1522  LOAD_METHOD              index
             1524  LOAD_FAST                'key'
             1526  CALL_METHOD_1         1  ''
             1528  STORE_FAST               'key'
             1530  POP_BLOCK        
             1532  JUMP_FORWARD       1562  'to 1562'
           1534_0  COME_FROM_FINALLY  1518  '1518'

 L.1955      1534  DUP_TOP          
             1536  LOAD_GLOBAL              ValueError
             1538  COMPARE_OP               exception-match
         1540_1542  POP_JUMP_IF_FALSE  1560  'to 1560'
             1544  POP_TOP          
             1546  POP_TOP          
             1548  POP_TOP          

 L.1957      1550  POP_EXCEPT       
         1552_1554  JUMP_BACK          1500  'to 1500'
             1556  POP_EXCEPT       
             1558  JUMP_FORWARD       1562  'to 1562'
           1560_0  COME_FROM          1540  '1540'
             1560  END_FINALLY      
           1562_0  COME_FROM          1558  '1558'
           1562_1  COME_FROM          1532  '1532'
           1562_2  COME_FROM          1514  '1514'

 L.1959      1562  LOAD_FAST                'usecols'
         1564_1566  POP_JUMP_IF_FALSE  1606  'to 1606'

 L.1960      1568  SETUP_FINALLY      1584  'to 1584'

 L.1961      1570  LOAD_FAST                'usecols'
             1572  LOAD_METHOD              index
             1574  LOAD_FAST                'key'
             1576  CALL_METHOD_1         1  ''
             1578  STORE_FAST               'key'
             1580  POP_BLOCK        
             1582  JUMP_FORWARD       1606  'to 1606'
           1584_0  COME_FROM_FINALLY  1568  '1568'

 L.1962      1584  DUP_TOP          
             1586  LOAD_GLOBAL              ValueError
             1588  COMPARE_OP               exception-match
         1590_1592  POP_JUMP_IF_FALSE  1604  'to 1604'
             1594  POP_TOP          
             1596  POP_TOP          
             1598  POP_TOP          

 L.1963      1600  POP_EXCEPT       
             1602  BREAK_LOOP         1606  'to 1606'
           1604_0  COME_FROM          1590  '1590'
             1604  END_FINALLY      
           1606_0  COME_FROM          1602  '1602'
           1606_1  COME_FROM          1582  '1582'
           1606_2  COME_FROM          1564  '1564'

 L.1965      1606  LOAD_FAST                'val'
             1608  LOAD_FAST                'filling_values'
             1610  LOAD_FAST                'key'
             1612  STORE_SUBSCR     
         1614_1616  JUMP_BACK          1500  'to 1500'
           1618_0  COME_FROM          1500  '1500'
             1618  JUMP_FORWARD       1692  'to 1692'
           1620_0  COME_FROM          1488  '1488'

 L.1967      1620  LOAD_GLOBAL              isinstance
             1622  LOAD_FAST                'user_filling_values'
             1624  LOAD_GLOBAL              list
             1626  LOAD_GLOBAL              tuple
             1628  BUILD_TUPLE_2         2 
             1630  CALL_FUNCTION_2       2  ''
         1632_1634  POP_JUMP_IF_FALSE  1682  'to 1682'

 L.1968      1636  LOAD_GLOBAL              len
             1638  LOAD_FAST                'user_filling_values'
             1640  CALL_FUNCTION_1       1  ''
             1642  STORE_FAST               'n'

 L.1969      1644  LOAD_FAST                'n'
             1646  LOAD_FAST                'nbcols'
             1648  COMPARE_OP               <=
         1650_1652  POP_JUMP_IF_FALSE  1668  'to 1668'

 L.1970      1654  LOAD_FAST                'user_filling_values'
             1656  LOAD_FAST                'filling_values'
             1658  LOAD_CONST               None
             1660  LOAD_FAST                'n'
             1662  BUILD_SLICE_2         2 
             1664  STORE_SUBSCR     
             1666  JUMP_FORWARD       1680  'to 1680'
           1668_0  COME_FROM          1650  '1650'

 L.1972      1668  LOAD_FAST                'user_filling_values'
             1670  LOAD_CONST               None
             1672  LOAD_FAST                'nbcols'
             1674  BUILD_SLICE_2         2 
             1676  BINARY_SUBSCR    
             1678  STORE_FAST               'filling_values'
           1680_0  COME_FROM          1666  '1666'
             1680  JUMP_FORWARD       1692  'to 1692'
           1682_0  COME_FROM          1632  '1632'

 L.1975      1682  LOAD_FAST                'user_filling_values'
             1684  BUILD_LIST_1          1 
             1686  LOAD_FAST                'nbcols'
             1688  BINARY_MULTIPLY  
             1690  STORE_FAST               'filling_values'
           1692_0  COME_FROM          1680  '1680'
           1692_1  COME_FROM          1618  '1618'

 L.1978      1692  LOAD_DEREF               'dtype'
             1694  LOAD_CONST               None
             1696  COMPARE_OP               is
         1698_1700  POP_JUMP_IF_FALSE  1724  'to 1724'

 L.1981      1702  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1704  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             1706  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1982      1708  LOAD_GLOBAL              zip
             1710  LOAD_FAST                'missing_values'
             1712  LOAD_FAST                'filling_values'
             1714  CALL_FUNCTION_2       2  ''

 L.1981      1716  GET_ITER         
             1718  CALL_FUNCTION_1       1  ''
             1720  STORE_FAST               'converters'
             1722  JUMP_FORWARD       1806  'to 1806'
           1724_0  COME_FROM          1698  '1698'

 L.1984      1724  LOAD_GLOBAL              flatten_dtype
             1726  LOAD_DEREF               'dtype'
             1728  LOAD_CONST               True
             1730  LOAD_CONST               ('flatten_base',)
             1732  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1734  STORE_FAST               'dtype_flat'

 L.1986      1736  LOAD_GLOBAL              len
             1738  LOAD_FAST                'dtype_flat'
             1740  CALL_FUNCTION_1       1  ''
             1742  LOAD_CONST               1
             1744  COMPARE_OP               >
         1746_1748  POP_JUMP_IF_FALSE  1778  'to 1778'

 L.1988      1750  LOAD_GLOBAL              zip
             1752  LOAD_FAST                'dtype_flat'
             1754  LOAD_FAST                'missing_values'
             1756  LOAD_FAST                'filling_values'
             1758  CALL_FUNCTION_3       3  ''
             1760  STORE_FAST               'zipit'

 L.1989      1762  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1764  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             1766  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1991      1768  LOAD_FAST                'zipit'

 L.1989      1770  GET_ITER         
             1772  CALL_FUNCTION_1       1  ''
             1774  STORE_FAST               'converters'
             1776  JUMP_FORWARD       1806  'to 1806'
           1778_0  COME_FROM          1746  '1746'

 L.1994      1778  LOAD_GLOBAL              zip
             1780  LOAD_FAST                'missing_values'
             1782  LOAD_FAST                'filling_values'
             1784  CALL_FUNCTION_2       2  ''
             1786  STORE_FAST               'zipit'

 L.1995      1788  LOAD_CLOSURE             'dtype'
             1790  BUILD_TUPLE_1         1 
             1792  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1794  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             1796  MAKE_FUNCTION_8          'closure'

 L.1997      1798  LOAD_FAST                'zipit'

 L.1995      1800  GET_ITER         
             1802  CALL_FUNCTION_1       1  ''
             1804  STORE_FAST               'converters'
           1806_0  COME_FROM          1776  '1776'
           1806_1  COME_FROM          1722  '1722'

 L.1999      1806  BUILD_LIST_0          0 
             1808  STORE_FAST               'uc_update'

 L.2000      1810  LOAD_FAST                'user_converters'
             1812  LOAD_METHOD              items
             1814  CALL_METHOD_0         0  ''
             1816  GET_ITER         
           1818_0  COME_FROM          2062  '2062'
           1818_1  COME_FROM          1926  '1926'
           1818_2  COME_FROM          1874  '1874'
             1818  FOR_ITER           2066  'to 2066'
             1820  UNPACK_SEQUENCE_2     2 
             1822  STORE_FAST               'j'
             1824  STORE_DEREF              'conv'

 L.2002      1826  LOAD_GLOBAL              _is_string_like
             1828  LOAD_FAST                'j'
             1830  CALL_FUNCTION_1       1  ''
         1832_1834  POP_JUMP_IF_FALSE  1886  'to 1886'

 L.2003      1836  SETUP_FINALLY      1856  'to 1856'

 L.2004      1838  LOAD_DEREF               'names'
             1840  LOAD_METHOD              index
             1842  LOAD_FAST                'j'
             1844  CALL_METHOD_1         1  ''
             1846  STORE_FAST               'j'

 L.2005      1848  LOAD_FAST                'j'
             1850  STORE_DEREF              'i'
             1852  POP_BLOCK        
             1854  JUMP_FORWARD       1884  'to 1884'
           1856_0  COME_FROM_FINALLY  1836  '1836'

 L.2006      1856  DUP_TOP          
             1858  LOAD_GLOBAL              ValueError
             1860  COMPARE_OP               exception-match
         1862_1864  POP_JUMP_IF_FALSE  1882  'to 1882'
             1866  POP_TOP          
             1868  POP_TOP          
             1870  POP_TOP          

 L.2007      1872  POP_EXCEPT       
         1874_1876  JUMP_BACK          1818  'to 1818'
             1878  POP_EXCEPT       
             1880  JUMP_FORWARD       1884  'to 1884'
           1882_0  COME_FROM          1862  '1862'
             1882  END_FINALLY      
           1884_0  COME_FROM          1880  '1880'
           1884_1  COME_FROM          1854  '1854'
             1884  JUMP_FORWARD       1942  'to 1942'
           1886_0  COME_FROM          1832  '1832'

 L.2008      1886  LOAD_FAST                'usecols'
         1888_1890  POP_JUMP_IF_FALSE  1938  'to 1938'

 L.2009      1892  SETUP_FINALLY      1908  'to 1908'

 L.2010      1894  LOAD_FAST                'usecols'
             1896  LOAD_METHOD              index
             1898  LOAD_FAST                'j'
             1900  CALL_METHOD_1         1  ''
             1902  STORE_DEREF              'i'
             1904  POP_BLOCK        
             1906  JUMP_FORWARD       1936  'to 1936'
           1908_0  COME_FROM_FINALLY  1892  '1892'

 L.2011      1908  DUP_TOP          
             1910  LOAD_GLOBAL              ValueError
             1912  COMPARE_OP               exception-match
         1914_1916  POP_JUMP_IF_FALSE  1934  'to 1934'
             1918  POP_TOP          
             1920  POP_TOP          
             1922  POP_TOP          

 L.2013      1924  POP_EXCEPT       
         1926_1928  JUMP_BACK          1818  'to 1818'
             1930  POP_EXCEPT       
             1932  JUMP_FORWARD       1936  'to 1936'
           1934_0  COME_FROM          1914  '1914'
             1934  END_FINALLY      
           1936_0  COME_FROM          1932  '1932'
           1936_1  COME_FROM          1906  '1906'
             1936  JUMP_FORWARD       1942  'to 1942'
           1938_0  COME_FROM          1888  '1888'

 L.2015      1938  LOAD_FAST                'j'
             1940  STORE_DEREF              'i'
           1942_0  COME_FROM          1936  '1936'
           1942_1  COME_FROM          1884  '1884'

 L.2017      1942  LOAD_GLOBAL              len
             1944  LOAD_FAST                'first_line'
             1946  CALL_FUNCTION_1       1  ''
         1948_1950  POP_JUMP_IF_FALSE  1962  'to 1962'

 L.2018      1952  LOAD_FAST                'first_values'
             1954  LOAD_FAST                'j'
             1956  BINARY_SUBSCR    
             1958  STORE_FAST               'testing_value'
             1960  JUMP_FORWARD       1966  'to 1966'
           1962_0  COME_FROM          1948  '1948'

 L.2020      1962  LOAD_CONST               None
             1964  STORE_FAST               'testing_value'
           1966_0  COME_FROM          1960  '1960'

 L.2021      1966  LOAD_DEREF               'conv'
             1968  LOAD_GLOBAL              bytes
             1970  COMPARE_OP               is
         1972_1974  POP_JUMP_IF_FALSE  1982  'to 1982'

 L.2022      1976  LOAD_GLOBAL              asbytes
             1978  STORE_FAST               'user_conv'
             1980  JUMP_FORWARD       2016  'to 2016'
           1982_0  COME_FROM          1972  '1972'

 L.2023      1982  LOAD_FAST                'byte_converters'
         1984_1986  POP_JUMP_IF_FALSE  2012  'to 2012'

 L.2026      1988  LOAD_CODE                <code_object tobytes_first>
             1990  LOAD_STR                 'genfromtxt.<locals>.tobytes_first'
             1992  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1994  STORE_FAST               'tobytes_first'

 L.2030      1996  LOAD_GLOBAL              functools
             1998  LOAD_ATTR                partial
             2000  LOAD_FAST                'tobytes_first'
             2002  LOAD_DEREF               'conv'
             2004  LOAD_CONST               ('conv',)
             2006  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2008  STORE_FAST               'user_conv'
             2010  JUMP_FORWARD       2016  'to 2016'
           2012_0  COME_FROM          1984  '1984'

 L.2032      2012  LOAD_DEREF               'conv'
             2014  STORE_FAST               'user_conv'
           2016_0  COME_FROM          2010  '2010'
           2016_1  COME_FROM          1980  '1980'

 L.2033      2016  LOAD_FAST                'converters'
             2018  LOAD_DEREF               'i'
             2020  BINARY_SUBSCR    
             2022  LOAD_ATTR                update
             2024  LOAD_FAST                'user_conv'
             2026  LOAD_CONST               True

 L.2034      2028  LOAD_FAST                'testing_value'

 L.2035      2030  LOAD_FAST                'filling_values'
             2032  LOAD_DEREF               'i'
             2034  BINARY_SUBSCR    

 L.2036      2036  LOAD_FAST                'missing_values'
             2038  LOAD_DEREF               'i'
             2040  BINARY_SUBSCR    

 L.2033      2042  LOAD_CONST               ('locked', 'testing_value', 'default', 'missing_values')
             2044  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2046  POP_TOP          

 L.2037      2048  LOAD_FAST                'uc_update'
             2050  LOAD_METHOD              append
             2052  LOAD_DEREF               'i'
             2054  LOAD_FAST                'user_conv'
             2056  BUILD_TUPLE_2         2 
             2058  CALL_METHOD_1         1  ''
             2060  POP_TOP          
         2062_2064  JUMP_BACK          1818  'to 1818'
           2066_0  COME_FROM          1818  '1818'

 L.2039      2066  LOAD_FAST                'user_converters'
             2068  LOAD_METHOD              update
             2070  LOAD_FAST                'uc_update'
             2072  CALL_METHOD_1         1  ''
             2074  POP_TOP          

 L.2046      2076  BUILD_LIST_0          0 
             2078  STORE_DEREF              'rows'

 L.2047      2080  LOAD_DEREF               'rows'
             2082  LOAD_ATTR                append
             2084  STORE_FAST               'append_to_rows'

 L.2049      2086  LOAD_FAST                'usemask'
         2088_2090  POP_JUMP_IF_FALSE  2102  'to 2102'

 L.2050      2092  BUILD_LIST_0          0 
             2094  STORE_FAST               'masks'

 L.2051      2096  LOAD_FAST                'masks'
             2098  LOAD_ATTR                append
             2100  STORE_FAST               'append_to_masks'
           2102_0  COME_FROM          2088  '2088'

 L.2053      2102  BUILD_LIST_0          0 
             2104  STORE_FAST               'invalid'

 L.2054      2106  LOAD_FAST                'invalid'
             2108  LOAD_ATTR                append
             2110  STORE_FAST               'append_to_invalid'

 L.2057      2112  LOAD_GLOBAL              enumerate
             2114  LOAD_GLOBAL              itertools
             2116  LOAD_METHOD              chain
             2118  LOAD_FAST                'first_line'
             2120  BUILD_LIST_1          1 
             2122  LOAD_FAST                'fhd'
             2124  CALL_METHOD_2         2  ''
             2126  CALL_FUNCTION_1       1  ''
             2128  GET_ITER         
           2130_0  COME_FROM          2348  '2348'
           2130_1  COME_FROM          2338  '2338'
           2130_2  COME_FROM          2278  '2278'
           2130_3  COME_FROM          2236  '2236'
           2130_4  COME_FROM          2164  '2164'
             2130  FOR_ITER           2352  'to 2352'
             2132  UNPACK_SEQUENCE_2     2 
             2134  STORE_DEREF              'i'
             2136  STORE_FAST               'line'

 L.2058      2138  LOAD_FAST                'split_line'
             2140  LOAD_FAST                'line'
             2142  CALL_FUNCTION_1       1  ''
             2144  STORE_DEREF              'values'

 L.2059      2146  LOAD_GLOBAL              len
             2148  LOAD_DEREF               'values'
             2150  CALL_FUNCTION_1       1  ''
             2152  STORE_FAST               'nbvalues'

 L.2061      2154  LOAD_FAST                'nbvalues'
             2156  LOAD_CONST               0
             2158  COMPARE_OP               ==
         2160_2162  POP_JUMP_IF_FALSE  2168  'to 2168'

 L.2062  2164_2166  JUMP_BACK          2130  'to 2130'
           2168_0  COME_FROM          2160  '2160'

 L.2063      2168  LOAD_FAST                'usecols'
         2170_2172  POP_JUMP_IF_FALSE  2248  'to 2248'

 L.2065      2174  SETUP_FINALLY      2198  'to 2198'

 L.2066      2176  LOAD_CLOSURE             'values'
             2178  BUILD_TUPLE_1         1 
             2180  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2182  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2184  MAKE_FUNCTION_8          'closure'
             2186  LOAD_FAST                'usecols'
             2188  GET_ITER         
             2190  CALL_FUNCTION_1       1  ''
             2192  STORE_DEREF              'values'
             2194  POP_BLOCK        
             2196  JUMP_FORWARD       2246  'to 2246'
           2198_0  COME_FROM_FINALLY  2174  '2174'

 L.2067      2198  DUP_TOP          
             2200  LOAD_GLOBAL              IndexError
             2202  COMPARE_OP               exception-match
         2204_2206  POP_JUMP_IF_FALSE  2244  'to 2244'
             2208  POP_TOP          
             2210  POP_TOP          
             2212  POP_TOP          

 L.2068      2214  LOAD_FAST                'append_to_invalid'
             2216  LOAD_DEREF               'i'
             2218  LOAD_DEREF               'skip_header'
             2220  BINARY_ADD       
             2222  LOAD_CONST               1
             2224  BINARY_ADD       
             2226  LOAD_FAST                'nbvalues'
             2228  BUILD_TUPLE_2         2 
             2230  CALL_FUNCTION_1       1  ''
             2232  POP_TOP          

 L.2069      2234  POP_EXCEPT       
         2236_2238  JUMP_BACK          2130  'to 2130'
             2240  POP_EXCEPT       
             2242  JUMP_FORWARD       2246  'to 2246'
           2244_0  COME_FROM          2204  '2204'
             2244  END_FINALLY      
           2246_0  COME_FROM          2242  '2242'
           2246_1  COME_FROM          2196  '2196'
             2246  JUMP_FORWARD       2282  'to 2282'
           2248_0  COME_FROM          2170  '2170'

 L.2070      2248  LOAD_FAST                'nbvalues'
             2250  LOAD_FAST                'nbcols'
             2252  COMPARE_OP               !=
         2254_2256  POP_JUMP_IF_FALSE  2282  'to 2282'

 L.2071      2258  LOAD_FAST                'append_to_invalid'
             2260  LOAD_DEREF               'i'
             2262  LOAD_DEREF               'skip_header'
             2264  BINARY_ADD       
             2266  LOAD_CONST               1
             2268  BINARY_ADD       
             2270  LOAD_FAST                'nbvalues'
             2272  BUILD_TUPLE_2         2 
             2274  CALL_FUNCTION_1       1  ''
             2276  POP_TOP          

 L.2072  2278_2280  JUMP_BACK          2130  'to 2130'
           2282_0  COME_FROM          2254  '2254'
           2282_1  COME_FROM          2246  '2246'

 L.2074      2282  LOAD_FAST                'append_to_rows'
             2284  LOAD_GLOBAL              tuple
             2286  LOAD_DEREF               'values'
             2288  CALL_FUNCTION_1       1  ''
             2290  CALL_FUNCTION_1       1  ''
             2292  POP_TOP          

 L.2075      2294  LOAD_FAST                'usemask'
         2296_2298  POP_JUMP_IF_FALSE  2328  'to 2328'

 L.2076      2300  LOAD_FAST                'append_to_masks'
             2302  LOAD_GLOBAL              tuple
             2304  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2306  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2308  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.2077      2310  LOAD_GLOBAL              zip
             2312  LOAD_DEREF               'values'

 L.2078      2314  LOAD_FAST                'missing_values'

 L.2077      2316  CALL_FUNCTION_2       2  ''

 L.2076      2318  GET_ITER         
             2320  CALL_FUNCTION_1       1  ''
             2322  CALL_FUNCTION_1       1  ''
             2324  CALL_FUNCTION_1       1  ''
             2326  POP_TOP          
           2328_0  COME_FROM          2296  '2296'

 L.2079      2328  LOAD_GLOBAL              len
             2330  LOAD_DEREF               'rows'
             2332  CALL_FUNCTION_1       1  ''
             2334  LOAD_FAST                'max_rows'
             2336  COMPARE_OP               ==
         2338_2340  POP_JUMP_IF_FALSE_BACK  2130  'to 2130'

 L.2080      2342  POP_TOP          
         2344_2346  BREAK_LOOP         2352  'to 2352'
         2348_2350  JUMP_BACK          2130  'to 2130'
           2352_0  COME_FROM          2344  '2344'
           2352_1  COME_FROM          2130  '2130'
             2352  POP_BLOCK        
             2354  BEGIN_FINALLY    
           2356_0  COME_FROM_WITH      318  '318'
             2356  WITH_CLEANUP_START
             2358  WITH_CLEANUP_FINISH
             2360  END_FINALLY      

 L.2083      2362  LOAD_DEREF               'dtype'
             2364  LOAD_CONST               None
             2366  COMPARE_OP               is
         2368_2370  POP_JUMP_IF_FALSE  2568  'to 2568'

 L.2084      2372  LOAD_GLOBAL              enumerate
             2374  LOAD_FAST                'converters'
             2376  CALL_FUNCTION_1       1  ''
             2378  GET_ITER         
           2380_0  COME_FROM          2564  '2564'
           2380_1  COME_FROM          2560  '2560'
           2380_2  COME_FROM          2420  '2420'
             2380  FOR_ITER           2568  'to 2568'
             2382  UNPACK_SEQUENCE_2     2 
             2384  STORE_DEREF              'i'
             2386  STORE_FAST               'converter'

 L.2085      2388  LOAD_CLOSURE             'i'
             2390  BUILD_TUPLE_1         1 
             2392  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2394  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2396  MAKE_FUNCTION_8          'closure'
             2398  LOAD_DEREF               'rows'
             2400  GET_ITER         
             2402  CALL_FUNCTION_1       1  ''
             2404  STORE_FAST               'current_column'

 L.2086      2406  SETUP_FINALLY      2422  'to 2422'

 L.2087      2408  LOAD_FAST                'converter'
             2410  LOAD_METHOD              iterupgrade
             2412  LOAD_FAST                'current_column'
             2414  CALL_METHOD_1         1  ''
             2416  POP_TOP          
             2418  POP_BLOCK        
             2420  JUMP_BACK          2380  'to 2380'
           2422_0  COME_FROM_FINALLY  2406  '2406'

 L.2088      2422  DUP_TOP          
             2424  LOAD_GLOBAL              ConverterLockError
             2426  COMPARE_OP               exception-match
         2428_2430  POP_JUMP_IF_FALSE  2562  'to 2562'
             2432  POP_TOP          
             2434  POP_TOP          
             2436  POP_TOP          

 L.2089      2438  LOAD_STR                 'Converter #%i is locked and cannot be upgraded: '
             2440  LOAD_DEREF               'i'
             2442  BINARY_MODULO    
             2444  STORE_FAST               'errmsg'

 L.2090      2446  LOAD_GLOBAL              map
             2448  LOAD_GLOBAL              itemgetter
             2450  LOAD_DEREF               'i'
             2452  CALL_FUNCTION_1       1  ''
             2454  LOAD_DEREF               'rows'
             2456  CALL_FUNCTION_2       2  ''
             2458  STORE_FAST               'current_column'

 L.2091      2460  LOAD_GLOBAL              enumerate
             2462  LOAD_FAST                'current_column'
             2464  CALL_FUNCTION_1       1  ''
             2466  GET_ITER         
           2468_0  COME_FROM          2554  '2554'
           2468_1  COME_FROM          2550  '2550'
           2468_2  COME_FROM          2490  '2490'
             2468  FOR_ITER           2558  'to 2558'
             2470  UNPACK_SEQUENCE_2     2 
             2472  STORE_FAST               'j'
             2474  STORE_FAST               'value'

 L.2092      2476  SETUP_FINALLY      2492  'to 2492'

 L.2093      2478  LOAD_FAST                'converter'
             2480  LOAD_METHOD              upgrade
             2482  LOAD_FAST                'value'
             2484  CALL_METHOD_1         1  ''
             2486  POP_TOP          
             2488  POP_BLOCK        
             2490  JUMP_BACK          2468  'to 2468'
           2492_0  COME_FROM_FINALLY  2476  '2476'

 L.2094      2492  DUP_TOP          
             2494  LOAD_GLOBAL              ConverterError
             2496  LOAD_GLOBAL              ValueError
             2498  BUILD_TUPLE_2         2 
             2500  COMPARE_OP               exception-match
         2502_2504  POP_JUMP_IF_FALSE  2552  'to 2552'
             2506  POP_TOP          
             2508  POP_TOP          
             2510  POP_TOP          

 L.2095      2512  LOAD_FAST                'errmsg'
             2514  LOAD_STR                 "(occurred line #%i for value '%s')"
             2516  INPLACE_ADD      
             2518  STORE_FAST               'errmsg'

 L.2096      2520  LOAD_FAST                'errmsg'
             2522  LOAD_FAST                'j'
             2524  LOAD_CONST               1
             2526  BINARY_ADD       
             2528  LOAD_DEREF               'skip_header'
             2530  BINARY_ADD       
             2532  LOAD_FAST                'value'
             2534  BUILD_TUPLE_2         2 
             2536  INPLACE_MODULO   
             2538  STORE_FAST               'errmsg'

 L.2097      2540  LOAD_GLOBAL              ConverterError
             2542  LOAD_FAST                'errmsg'
             2544  CALL_FUNCTION_1       1  ''
             2546  RAISE_VARARGS_1       1  'exception instance'
             2548  POP_EXCEPT       
             2550  JUMP_BACK          2468  'to 2468'
           2552_0  COME_FROM          2502  '2502'
             2552  END_FINALLY      
         2554_2556  JUMP_BACK          2468  'to 2468'
           2558_0  COME_FROM          2468  '2468'
             2558  POP_EXCEPT       
             2560  JUMP_BACK          2380  'to 2380'
           2562_0  COME_FROM          2428  '2428'
             2562  END_FINALLY      
         2564_2566  JUMP_BACK          2380  'to 2380'
           2568_0  COME_FROM          2380  '2380'
           2568_1  COME_FROM          2368  '2368'

 L.2100      2568  LOAD_GLOBAL              len
             2570  LOAD_FAST                'invalid'
             2572  CALL_FUNCTION_1       1  ''
             2574  STORE_FAST               'nbinvalid'

 L.2101      2576  LOAD_FAST                'nbinvalid'
             2578  LOAD_CONST               0
             2580  COMPARE_OP               >
         2582_2584  POP_JUMP_IF_FALSE  2750  'to 2750'

 L.2102      2586  LOAD_GLOBAL              len
             2588  LOAD_DEREF               'rows'
             2590  CALL_FUNCTION_1       1  ''
             2592  LOAD_FAST                'nbinvalid'
             2594  BINARY_ADD       
             2596  LOAD_FAST                'skip_footer'
             2598  BINARY_SUBTRACT  
             2600  STORE_DEREF              'nbrows'

 L.2104      2602  LOAD_STR                 '    Line #%%i (got %%i columns instead of %i)'
             2604  LOAD_FAST                'nbcols'
             2606  BINARY_MODULO    
             2608  STORE_DEREF              'template'

 L.2105      2610  LOAD_FAST                'skip_footer'
             2612  LOAD_CONST               0
             2614  COMPARE_OP               >
         2616_2618  POP_JUMP_IF_FALSE  2668  'to 2668'

 L.2106      2620  LOAD_GLOBAL              len
             2622  LOAD_CLOSURE             'nbrows'
             2624  LOAD_CLOSURE             'skip_header'
             2626  BUILD_TUPLE_2         2 
             2628  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2630  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2632  MAKE_FUNCTION_8          'closure'
             2634  LOAD_FAST                'invalid'
             2636  GET_ITER         
             2638  CALL_FUNCTION_1       1  ''
             2640  CALL_FUNCTION_1       1  ''
             2642  STORE_FAST               'nbinvalid_skipped'

 L.2108      2644  LOAD_FAST                'invalid'
             2646  LOAD_CONST               None
             2648  LOAD_FAST                'nbinvalid'
             2650  LOAD_FAST                'nbinvalid_skipped'
             2652  BINARY_SUBTRACT  
             2654  BUILD_SLICE_2         2 
             2656  BINARY_SUBSCR    
             2658  STORE_FAST               'invalid'

 L.2109      2660  LOAD_FAST                'skip_footer'
             2662  LOAD_FAST                'nbinvalid_skipped'
             2664  INPLACE_SUBTRACT 
             2666  STORE_FAST               'skip_footer'
           2668_0  COME_FROM          2616  '2616'

 L.2115      2668  LOAD_CLOSURE             'template'
             2670  BUILD_TUPLE_1         1 
             2672  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2674  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2676  MAKE_FUNCTION_8          'closure'

 L.2116      2678  LOAD_FAST                'invalid'

 L.2115      2680  GET_ITER         
             2682  CALL_FUNCTION_1       1  ''
             2684  STORE_FAST               'errmsg'

 L.2117      2686  LOAD_GLOBAL              len
             2688  LOAD_FAST                'errmsg'
             2690  CALL_FUNCTION_1       1  ''
         2692_2694  POP_JUMP_IF_FALSE  2750  'to 2750'

 L.2118      2696  LOAD_FAST                'errmsg'
             2698  LOAD_METHOD              insert
             2700  LOAD_CONST               0
             2702  LOAD_STR                 'Some errors were detected !'
             2704  CALL_METHOD_2         2  ''
             2706  POP_TOP          

 L.2119      2708  LOAD_STR                 '\n'
             2710  LOAD_METHOD              join
             2712  LOAD_FAST                'errmsg'
             2714  CALL_METHOD_1         1  ''
             2716  STORE_FAST               'errmsg'

 L.2121      2718  LOAD_FAST                'invalid_raise'
         2720_2722  POP_JUMP_IF_FALSE  2734  'to 2734'

 L.2122      2724  LOAD_GLOBAL              ValueError
             2726  LOAD_FAST                'errmsg'
             2728  CALL_FUNCTION_1       1  ''
             2730  RAISE_VARARGS_1       1  'exception instance'
             2732  JUMP_FORWARD       2750  'to 2750'
           2734_0  COME_FROM          2720  '2720'

 L.2125      2734  LOAD_GLOBAL              warnings
             2736  LOAD_ATTR                warn
             2738  LOAD_FAST                'errmsg'
             2740  LOAD_GLOBAL              ConversionWarning
             2742  LOAD_CONST               2
             2744  LOAD_CONST               ('stacklevel',)
             2746  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2748  POP_TOP          
           2750_0  COME_FROM          2732  '2732'
           2750_1  COME_FROM          2692  '2692'
           2750_2  COME_FROM          2582  '2582'

 L.2128      2750  LOAD_FAST                'skip_footer'
             2752  LOAD_CONST               0
             2754  COMPARE_OP               >
         2756_2758  POP_JUMP_IF_FALSE  2794  'to 2794'

 L.2129      2760  LOAD_DEREF               'rows'
             2762  LOAD_CONST               None
             2764  LOAD_FAST                'skip_footer'
             2766  UNARY_NEGATIVE   
             2768  BUILD_SLICE_2         2 
             2770  BINARY_SUBSCR    
             2772  STORE_DEREF              'rows'

 L.2130      2774  LOAD_FAST                'usemask'
         2776_2778  POP_JUMP_IF_FALSE  2794  'to 2794'

 L.2131      2780  LOAD_FAST                'masks'
             2782  LOAD_CONST               None
             2784  LOAD_FAST                'skip_footer'
             2786  UNARY_NEGATIVE   
             2788  BUILD_SLICE_2         2 
             2790  BINARY_SUBSCR    
             2792  STORE_FAST               'masks'
           2794_0  COME_FROM          2776  '2776'
           2794_1  COME_FROM          2756  '2756'

 L.2135      2794  LOAD_FAST                'loose'
         2796_2798  POP_JUMP_IF_FALSE  2832  'to 2832'

 L.2136      2800  LOAD_GLOBAL              list

 L.2137      2802  LOAD_GLOBAL              zip
             2804  LOAD_CLOSURE             'rows'
             2806  BUILD_TUPLE_1         1 
             2808  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2810  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2812  MAKE_FUNCTION_8          'closure'

 L.2138      2814  LOAD_GLOBAL              enumerate
             2816  LOAD_FAST                'converters'
             2818  CALL_FUNCTION_1       1  ''

 L.2137      2820  GET_ITER         
             2822  CALL_FUNCTION_1       1  ''
             2824  CALL_FUNCTION_EX      0  'positional arguments only'

 L.2136      2826  CALL_FUNCTION_1       1  ''
             2828  STORE_DEREF              'rows'
             2830  JUMP_FORWARD       2862  'to 2862'
           2832_0  COME_FROM          2796  '2796'

 L.2140      2832  LOAD_GLOBAL              list

 L.2141      2834  LOAD_GLOBAL              zip
             2836  LOAD_CLOSURE             'rows'
             2838  BUILD_TUPLE_1         1 
             2840  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2842  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2844  MAKE_FUNCTION_8          'closure'

 L.2142      2846  LOAD_GLOBAL              enumerate
             2848  LOAD_FAST                'converters'
             2850  CALL_FUNCTION_1       1  ''

 L.2141      2852  GET_ITER         
             2854  CALL_FUNCTION_1       1  ''
             2856  CALL_FUNCTION_EX      0  'positional arguments only'

 L.2140      2858  CALL_FUNCTION_1       1  ''
             2860  STORE_DEREF              'rows'
           2862_0  COME_FROM          2830  '2830'

 L.2145      2862  LOAD_DEREF               'rows'
             2864  STORE_FAST               'data'

 L.2146      2866  LOAD_DEREF               'dtype'
             2868  LOAD_CONST               None
             2870  COMPARE_OP               is
         2872_2874  POP_JUMP_IF_FALSE  3290  'to 3290'

 L.2148      2876  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2878  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2880  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             2882  LOAD_FAST                'converters'
             2884  GET_ITER         
             2886  CALL_FUNCTION_1       1  ''
             2888  STORE_FAST               'column_types'

 L.2150      2890  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2892  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2894  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             2896  LOAD_GLOBAL              enumerate
             2898  LOAD_FAST                'column_types'
             2900  CALL_FUNCTION_1       1  ''
             2902  GET_ITER         
             2904  CALL_FUNCTION_1       1  ''
             2906  STORE_DEREF              'strcolidx'

 L.2153      2908  LOAD_FAST                'byte_converters'
         2910_2912  POP_JUMP_IF_FALSE  3018  'to 3018'
             2914  LOAD_DEREF               'strcolidx'
         2916_2918  POP_JUMP_IF_FALSE  3018  'to 3018'

 L.2155      2920  LOAD_GLOBAL              warnings
             2922  LOAD_ATTR                warn

 L.2156      2924  LOAD_STR                 'Reading unicode strings without specifying the encoding argument is deprecated. Set the encoding, use None for the system default.'

 L.2159      2926  LOAD_GLOBAL              np
             2928  LOAD_ATTR                VisibleDeprecationWarning

 L.2159      2930  LOAD_CONST               2

 L.2155      2932  LOAD_CONST               ('stacklevel',)
             2934  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2936  POP_TOP          

 L.2160      2938  LOAD_CLOSURE             'strcolidx'
             2940  BUILD_TUPLE_1         1 
             2942  LOAD_CODE                <code_object encode_unicode_cols>
             2944  LOAD_STR                 'genfromtxt.<locals>.encode_unicode_cols'
             2946  MAKE_FUNCTION_8          'closure'
             2948  STORE_DEREF              'encode_unicode_cols'

 L.2166      2950  SETUP_FINALLY      2974  'to 2974'

 L.2167      2952  LOAD_CLOSURE             'encode_unicode_cols'
             2954  BUILD_TUPLE_1         1 
             2956  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2958  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             2960  MAKE_FUNCTION_8          'closure'
             2962  LOAD_FAST                'data'
             2964  GET_ITER         
             2966  CALL_FUNCTION_1       1  ''
             2968  STORE_FAST               'data'
             2970  POP_BLOCK        
             2972  JUMP_FORWARD       2996  'to 2996'
           2974_0  COME_FROM_FINALLY  2950  '2950'

 L.2168      2974  DUP_TOP          
             2976  LOAD_GLOBAL              UnicodeEncodeError
             2978  COMPARE_OP               exception-match
         2980_2982  POP_JUMP_IF_FALSE  2994  'to 2994'
             2984  POP_TOP          
             2986  POP_TOP          
             2988  POP_TOP          

 L.2169      2990  POP_EXCEPT       
             2992  BREAK_LOOP         3018  'to 3018'
           2994_0  COME_FROM          2980  '2980'
             2994  END_FINALLY      
           2996_0  COME_FROM          2972  '2972'

 L.2171      2996  LOAD_DEREF               'strcolidx'
             2998  GET_ITER         
           3000_0  COME_FROM          3014  '3014'
             3000  FOR_ITER           3018  'to 3018'
             3002  STORE_DEREF              'i'

 L.2172      3004  LOAD_GLOBAL              np
             3006  LOAD_ATTR                bytes_
             3008  LOAD_FAST                'column_types'
             3010  LOAD_DEREF               'i'
             3012  STORE_SUBSCR     
         3014_3016  JUMP_BACK          3000  'to 3000'
           3018_0  COME_FROM          3000  '3000'
           3018_1  COME_FROM          2992  '2992'
           3018_2  COME_FROM          2916  '2916'
           3018_3  COME_FROM          2910  '2910'

 L.2175      3018  LOAD_FAST                'column_types'
             3020  LOAD_CONST               None
             3022  LOAD_CONST               None
             3024  BUILD_SLICE_2         2 
             3026  BINARY_SUBSCR    
             3028  STORE_FAST               'sized_column_types'

 L.2176      3030  LOAD_GLOBAL              enumerate
             3032  LOAD_FAST                'column_types'
             3034  CALL_FUNCTION_1       1  ''
             3036  GET_ITER         
           3038_0  COME_FROM          3096  '3096'
           3038_1  COME_FROM          3058  '3058'
             3038  FOR_ITER           3100  'to 3100'
             3040  UNPACK_SEQUENCE_2     2 
             3042  STORE_DEREF              'i'
             3044  STORE_FAST               'col_type'

 L.2177      3046  LOAD_GLOBAL              np
             3048  LOAD_METHOD              issubdtype
             3050  LOAD_FAST                'col_type'
             3052  LOAD_GLOBAL              np
             3054  LOAD_ATTR                character
             3056  CALL_METHOD_2         2  ''
         3058_3060  POP_JUMP_IF_FALSE_BACK  3038  'to 3038'

 L.2178      3062  LOAD_GLOBAL              max
             3064  LOAD_CLOSURE             'i'
             3066  BUILD_TUPLE_1         1 
             3068  LOAD_GENEXPR             '<code_object <genexpr>>'
             3070  LOAD_STR                 'genfromtxt.<locals>.<genexpr>'
             3072  MAKE_FUNCTION_8          'closure'
             3074  LOAD_FAST                'data'
             3076  GET_ITER         
             3078  CALL_FUNCTION_1       1  ''
             3080  CALL_FUNCTION_1       1  ''
             3082  STORE_FAST               'n_chars'

 L.2179      3084  LOAD_FAST                'col_type'
             3086  LOAD_FAST                'n_chars'
             3088  BUILD_TUPLE_2         2 
             3090  LOAD_FAST                'sized_column_types'
             3092  LOAD_DEREF               'i'
             3094  STORE_SUBSCR     
         3096_3098  JUMP_BACK          3038  'to 3038'
           3100_0  COME_FROM          3038  '3038'

 L.2181      3100  LOAD_DEREF               'names'
             3102  LOAD_CONST               None
             3104  COMPARE_OP               is
         3106_3108  POP_JUMP_IF_FALSE  3214  'to 3214'

 L.2183      3110  LOAD_SETCOMP             '<code_object <setcomp>>'
             3112  LOAD_STR                 'genfromtxt.<locals>.<setcomp>'
             3114  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.2185      3116  LOAD_GLOBAL              zip
             3118  LOAD_FAST                'converters'
             3120  LOAD_FAST                'column_types'
             3122  CALL_FUNCTION_2       2  ''

 L.2183      3124  GET_ITER         
             3126  CALL_FUNCTION_1       1  ''
             3128  STORE_FAST               'base'

 L.2187      3130  LOAD_GLOBAL              len
             3132  LOAD_FAST                'base'
             3134  CALL_FUNCTION_1       1  ''
             3136  LOAD_CONST               1
             3138  COMPARE_OP               ==
         3140_3142  POP_JUMP_IF_FALSE  3162  'to 3162'

 L.2188      3144  LOAD_FAST                'base'
             3146  UNPACK_SEQUENCE_1     1 
             3148  STORE_FAST               'uniform_type'

 L.2189      3150  LOAD_FAST                'uniform_type'
             3152  LOAD_GLOBAL              bool
             3154  ROT_TWO          
             3156  STORE_FAST               'ddtype'
             3158  STORE_FAST               'mdtype'
             3160  JUMP_FORWARD       3212  'to 3212'
           3162_0  COME_FROM          3140  '3140'

 L.2191      3162  LOAD_CLOSURE             'defaultfmt'
             3164  BUILD_TUPLE_1         1 
             3166  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3168  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3170  MAKE_FUNCTION_8          'closure'

 L.2192      3172  LOAD_GLOBAL              enumerate
             3174  LOAD_FAST                'sized_column_types'
             3176  CALL_FUNCTION_1       1  ''

 L.2191      3178  GET_ITER         
             3180  CALL_FUNCTION_1       1  ''
             3182  STORE_FAST               'ddtype'

 L.2193      3184  LOAD_FAST                'usemask'
         3186_3188  POP_JUMP_IF_FALSE  3252  'to 3252'

 L.2194      3190  LOAD_CLOSURE             'defaultfmt'
             3192  BUILD_TUPLE_1         1 
             3194  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3196  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3198  MAKE_FUNCTION_8          'closure'

 L.2195      3200  LOAD_GLOBAL              enumerate
             3202  LOAD_FAST                'sized_column_types'
             3204  CALL_FUNCTION_1       1  ''

 L.2194      3206  GET_ITER         
             3208  CALL_FUNCTION_1       1  ''
             3210  STORE_FAST               'mdtype'
           3212_0  COME_FROM          3160  '3160'
             3212  JUMP_FORWARD       3252  'to 3252'
           3214_0  COME_FROM          3106  '3106'

 L.2197      3214  LOAD_GLOBAL              list
             3216  LOAD_GLOBAL              zip
             3218  LOAD_DEREF               'names'
             3220  LOAD_FAST                'sized_column_types'
             3222  CALL_FUNCTION_2       2  ''
             3224  CALL_FUNCTION_1       1  ''
             3226  STORE_FAST               'ddtype'

 L.2198      3228  LOAD_GLOBAL              list
             3230  LOAD_GLOBAL              zip
             3232  LOAD_DEREF               'names'
             3234  LOAD_GLOBAL              bool
             3236  BUILD_LIST_1          1 
             3238  LOAD_GLOBAL              len
             3240  LOAD_FAST                'sized_column_types'
             3242  CALL_FUNCTION_1       1  ''
             3244  BINARY_MULTIPLY  
             3246  CALL_FUNCTION_2       2  ''
             3248  CALL_FUNCTION_1       1  ''
             3250  STORE_FAST               'mdtype'
           3252_0  COME_FROM          3212  '3212'
           3252_1  COME_FROM          3186  '3186'

 L.2199      3252  LOAD_GLOBAL              np
             3254  LOAD_ATTR                array
             3256  LOAD_FAST                'data'
             3258  LOAD_FAST                'ddtype'
             3260  LOAD_CONST               ('dtype',)
             3262  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3264  STORE_DEREF              'output'

 L.2200      3266  LOAD_FAST                'usemask'
         3268_3270  POP_JUMP_IF_FALSE  3722  'to 3722'

 L.2201      3272  LOAD_GLOBAL              np
             3274  LOAD_ATTR                array
             3276  LOAD_FAST                'masks'
             3278  LOAD_FAST                'mdtype'
             3280  LOAD_CONST               ('dtype',)
             3282  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3284  STORE_FAST               'outputmask'
         3286_3288  JUMP_FORWARD       3722  'to 3722'
           3290_0  COME_FROM          2872  '2872'

 L.2204      3290  LOAD_DEREF               'names'
         3292_3294  POP_JUMP_IF_FALSE  3314  'to 3314'
             3296  LOAD_DEREF               'dtype'
             3298  LOAD_ATTR                names
             3300  LOAD_CONST               None
             3302  COMPARE_OP               is-not
         3304_3306  POP_JUMP_IF_FALSE  3314  'to 3314'

 L.2205      3308  LOAD_DEREF               'names'
             3310  LOAD_DEREF               'dtype'
             3312  STORE_ATTR               names
           3314_0  COME_FROM          3304  '3304'
           3314_1  COME_FROM          3292  '3292'

 L.2207      3314  LOAD_GLOBAL              len
             3316  LOAD_FAST                'dtype_flat'
             3318  CALL_FUNCTION_1       1  ''
             3320  LOAD_CONST               1
             3322  COMPARE_OP               >
         3324_3326  POP_JUMP_IF_FALSE  3474  'to 3474'

 L.2212      3328  LOAD_STR                 'O'
             3330  LOAD_GENEXPR             '<code_object <genexpr>>'
             3332  LOAD_STR                 'genfromtxt.<locals>.<genexpr>'
             3334  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3336  LOAD_FAST                'dtype_flat'
             3338  GET_ITER         
             3340  CALL_FUNCTION_1       1  ''
             3342  COMPARE_OP               in
         3344_3346  POP_JUMP_IF_FALSE  3384  'to 3384'

 L.2213      3348  LOAD_GLOBAL              has_nested_fields
             3350  LOAD_DEREF               'dtype'
             3352  CALL_FUNCTION_1       1  ''
         3354_3356  POP_JUMP_IF_FALSE  3368  'to 3368'

 L.2214      3358  LOAD_GLOBAL              NotImplementedError

 L.2215      3360  LOAD_STR                 'Nested fields involving objects are not supported...'

 L.2214      3362  CALL_FUNCTION_1       1  ''
             3364  RAISE_VARARGS_1       1  'exception instance'
             3366  JUMP_FORWARD       3382  'to 3382'
           3368_0  COME_FROM          3354  '3354'

 L.2217      3368  LOAD_GLOBAL              np
             3370  LOAD_ATTR                array
             3372  LOAD_FAST                'data'
             3374  LOAD_DEREF               'dtype'
             3376  LOAD_CONST               ('dtype',)
             3378  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3380  STORE_DEREF              'output'
           3382_0  COME_FROM          3366  '3366'
             3382  JUMP_FORWARD       3418  'to 3418'
           3384_0  COME_FROM          3344  '3344'

 L.2219      3384  LOAD_GLOBAL              np
             3386  LOAD_ATTR                array
             3388  LOAD_FAST                'data'
             3390  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3392  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3394  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3396  LOAD_FAST                'dtype_flat'
             3398  GET_ITER         
             3400  CALL_FUNCTION_1       1  ''
             3402  LOAD_CONST               ('dtype',)
             3404  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3406  STORE_DEREF              'rows'

 L.2220      3408  LOAD_DEREF               'rows'
             3410  LOAD_METHOD              view
             3412  LOAD_DEREF               'dtype'
             3414  CALL_METHOD_1         1  ''
             3416  STORE_DEREF              'output'
           3418_0  COME_FROM          3382  '3382'

 L.2222      3418  LOAD_FAST                'usemask'
         3420_3422  POP_JUMP_IF_FALSE  3722  'to 3722'

 L.2223      3424  LOAD_GLOBAL              np
             3426  LOAD_ATTR                array

 L.2224      3428  LOAD_FAST                'masks'

 L.2224      3430  LOAD_GLOBAL              np
             3432  LOAD_METHOD              dtype
             3434  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3436  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3438  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3440  LOAD_FAST                'dtype_flat'
             3442  GET_ITER         
             3444  CALL_FUNCTION_1       1  ''
             3446  CALL_METHOD_1         1  ''

 L.2223      3448  LOAD_CONST               ('dtype',)
             3450  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3452  STORE_FAST               'rowmasks'

 L.2226      3454  LOAD_FAST                'make_mask_descr'
             3456  LOAD_DEREF               'dtype'
             3458  CALL_FUNCTION_1       1  ''
             3460  STORE_FAST               'mdtype'

 L.2227      3462  LOAD_FAST                'rowmasks'
             3464  LOAD_METHOD              view
             3466  LOAD_FAST                'mdtype'
             3468  CALL_METHOD_1         1  ''
             3470  STORE_FAST               'outputmask'
             3472  JUMP_FORWARD       3722  'to 3722'
           3474_0  COME_FROM          3324  '3324'

 L.2231      3474  LOAD_FAST                'user_converters'
         3476_3478  POP_JUMP_IF_FALSE  3656  'to 3656'

 L.2232      3480  LOAD_CONST               True
             3482  STORE_FAST               'ishomogeneous'

 L.2233      3484  BUILD_LIST_0          0 
             3486  STORE_DEREF              'descr'

 L.2234      3488  LOAD_GLOBAL              enumerate
             3490  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3492  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3494  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3496  LOAD_FAST                'converters'
             3498  GET_ITER         
             3500  CALL_FUNCTION_1       1  ''
             3502  CALL_FUNCTION_1       1  ''
             3504  GET_ITER         
           3506_0  COME_FROM          3610  '3610'
           3506_1  COME_FROM          3594  '3594'
             3506  FOR_ITER           3614  'to 3614'
             3508  UNPACK_SEQUENCE_2     2 
             3510  STORE_DEREF              'i'
             3512  STORE_FAST               'ttype'

 L.2236      3514  LOAD_DEREF               'i'
             3516  LOAD_FAST                'user_converters'
             3518  COMPARE_OP               in
         3520_3522  POP_JUMP_IF_FALSE  3596  'to 3596'

 L.2237      3524  LOAD_FAST                'ishomogeneous'
             3526  LOAD_FAST                'ttype'
             3528  LOAD_DEREF               'dtype'
             3530  LOAD_ATTR                type
             3532  COMPARE_OP               ==
             3534  INPLACE_AND      
             3536  STORE_FAST               'ishomogeneous'

 L.2238      3538  LOAD_GLOBAL              np
             3540  LOAD_METHOD              issubdtype
             3542  LOAD_FAST                'ttype'
             3544  LOAD_GLOBAL              np
             3546  LOAD_ATTR                character
             3548  CALL_METHOD_2         2  ''
         3550_3552  POP_JUMP_IF_FALSE  3580  'to 3580'

 L.2239      3554  LOAD_FAST                'ttype'
             3556  LOAD_GLOBAL              max
             3558  LOAD_CLOSURE             'i'
             3560  BUILD_TUPLE_1         1 
             3562  LOAD_GENEXPR             '<code_object <genexpr>>'
             3564  LOAD_STR                 'genfromtxt.<locals>.<genexpr>'
             3566  MAKE_FUNCTION_8          'closure'
             3568  LOAD_FAST                'data'
             3570  GET_ITER         
             3572  CALL_FUNCTION_1       1  ''
             3574  CALL_FUNCTION_1       1  ''
             3576  BUILD_TUPLE_2         2 
             3578  STORE_FAST               'ttype'
           3580_0  COME_FROM          3550  '3550'

 L.2240      3580  LOAD_DEREF               'descr'
             3582  LOAD_METHOD              append
             3584  LOAD_STR                 ''
             3586  LOAD_FAST                'ttype'
             3588  BUILD_TUPLE_2         2 
             3590  CALL_METHOD_1         1  ''
             3592  POP_TOP          
             3594  JUMP_BACK          3506  'to 3506'
           3596_0  COME_FROM          3520  '3520'

 L.2242      3596  LOAD_DEREF               'descr'
             3598  LOAD_METHOD              append
             3600  LOAD_STR                 ''
             3602  LOAD_DEREF               'dtype'
             3604  BUILD_TUPLE_2         2 
             3606  CALL_METHOD_1         1  ''
             3608  POP_TOP          
         3610_3612  JUMP_BACK          3506  'to 3506'
           3614_0  COME_FROM          3506  '3506'

 L.2244      3614  LOAD_FAST                'ishomogeneous'
         3616_3618  POP_JUMP_IF_TRUE   3656  'to 3656'

 L.2246      3620  LOAD_GLOBAL              len
             3622  LOAD_DEREF               'descr'
             3624  CALL_FUNCTION_1       1  ''
             3626  LOAD_CONST               1
             3628  COMPARE_OP               >
         3630_3632  POP_JUMP_IF_FALSE  3646  'to 3646'

 L.2247      3634  LOAD_GLOBAL              np
             3636  LOAD_METHOD              dtype
             3638  LOAD_DEREF               'descr'
             3640  CALL_METHOD_1         1  ''
             3642  STORE_DEREF              'dtype'
             3644  JUMP_FORWARD       3656  'to 3656'
           3646_0  COME_FROM          3630  '3630'

 L.2250      3646  LOAD_GLOBAL              np
             3648  LOAD_METHOD              dtype
             3650  LOAD_FAST                'ttype'
             3652  CALL_METHOD_1         1  ''
             3654  STORE_DEREF              'dtype'
           3656_0  COME_FROM          3644  '3644'
           3656_1  COME_FROM          3616  '3616'
           3656_2  COME_FROM          3476  '3476'

 L.2252      3656  LOAD_GLOBAL              np
             3658  LOAD_METHOD              array
             3660  LOAD_FAST                'data'
             3662  LOAD_DEREF               'dtype'
             3664  CALL_METHOD_2         2  ''
             3666  STORE_DEREF              'output'

 L.2253      3668  LOAD_FAST                'usemask'
         3670_3672  POP_JUMP_IF_FALSE  3722  'to 3722'

 L.2254      3674  LOAD_DEREF               'dtype'
             3676  LOAD_ATTR                names
             3678  LOAD_CONST               None
             3680  COMPARE_OP               is-not
         3682_3684  POP_JUMP_IF_FALSE  3704  'to 3704'

 L.2255      3686  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3688  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3690  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3692  LOAD_DEREF               'dtype'
             3694  LOAD_ATTR                names
             3696  GET_ITER         
             3698  CALL_FUNCTION_1       1  ''
             3700  STORE_FAST               'mdtype'
             3702  JUMP_FORWARD       3708  'to 3708'
           3704_0  COME_FROM          3682  '3682'

 L.2257      3704  LOAD_GLOBAL              bool
             3706  STORE_FAST               'mdtype'
           3708_0  COME_FROM          3702  '3702'

 L.2258      3708  LOAD_GLOBAL              np
             3710  LOAD_ATTR                array
             3712  LOAD_FAST                'masks'
             3714  LOAD_FAST                'mdtype'
             3716  LOAD_CONST               ('dtype',)
             3718  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3720  STORE_FAST               'outputmask'
           3722_0  COME_FROM          3670  '3670'
           3722_1  COME_FROM          3472  '3472'
           3722_2  COME_FROM          3420  '3420'
           3722_3  COME_FROM          3286  '3286'
           3722_4  COME_FROM          3268  '3268'

 L.2260      3722  LOAD_DEREF               'output'
             3724  LOAD_ATTR                dtype
             3726  LOAD_ATTR                names
             3728  STORE_DEREF              'names'

 L.2261      3730  LOAD_FAST                'usemask'
         3732_3734  POP_JUMP_IF_FALSE  3820  'to 3820'
             3736  LOAD_DEREF               'names'
         3738_3740  POP_JUMP_IF_FALSE  3820  'to 3820'

 L.2262      3742  LOAD_GLOBAL              zip
             3744  LOAD_DEREF               'names'
             3746  LOAD_FAST                'converters'
             3748  CALL_FUNCTION_2       2  ''
             3750  GET_ITER         
           3752_0  COME_FROM          3816  '3816'
             3752  FOR_ITER           3820  'to 3820'
             3754  UNPACK_SEQUENCE_2     2 
             3756  STORE_FAST               'name'
             3758  STORE_DEREF              'conv'

 L.2263      3760  LOAD_CLOSURE             'conv'
             3762  BUILD_TUPLE_1         1 
             3764  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3766  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3768  MAKE_FUNCTION_8          'closure'
             3770  LOAD_DEREF               'conv'
             3772  LOAD_ATTR                missing_values
             3774  GET_ITER         
             3776  CALL_FUNCTION_1       1  ''
             3778  STORE_FAST               'missing_values'

 L.2265      3780  LOAD_FAST                'missing_values'
             3782  GET_ITER         
           3784_0  COME_FROM          3812  '3812'
             3784  FOR_ITER           3816  'to 3816'
             3786  STORE_FAST               'mval'

 L.2266      3788  LOAD_FAST                'outputmask'
             3790  LOAD_FAST                'name'
             3792  DUP_TOP_TWO      
             3794  BINARY_SUBSCR    
             3796  LOAD_DEREF               'output'
             3798  LOAD_FAST                'name'
             3800  BINARY_SUBSCR    
             3802  LOAD_FAST                'mval'
             3804  COMPARE_OP               ==
             3806  INPLACE_OR       
             3808  ROT_THREE        
             3810  STORE_SUBSCR     
         3812_3814  JUMP_BACK          3784  'to 3784'
           3816_0  COME_FROM          3784  '3784'
         3816_3818  JUMP_BACK          3752  'to 3752'
           3820_0  COME_FROM          3752  '3752'
           3820_1  COME_FROM          3738  '3738'
           3820_2  COME_FROM          3732  '3732'

 L.2268      3820  LOAD_FAST                'usemask'
         3822_3824  POP_JUMP_IF_FALSE  3842  'to 3842'

 L.2269      3826  LOAD_DEREF               'output'
             3828  LOAD_METHOD              view
             3830  LOAD_FAST                'MaskedArray'
             3832  CALL_METHOD_1         1  ''
             3834  STORE_DEREF              'output'

 L.2270      3836  LOAD_FAST                'outputmask'
             3838  LOAD_DEREF               'output'
             3840  STORE_ATTR               _mask
           3842_0  COME_FROM          3822  '3822'

 L.2271      3842  LOAD_GLOBAL              np
             3844  LOAD_METHOD              squeeze
             3846  LOAD_DEREF               'output'
             3848  CALL_METHOD_1         1  ''
             3850  STORE_DEREF              'output'

 L.2272      3852  LOAD_FAST                'unpack'
         3854_3856  POP_JUMP_IF_FALSE  3918  'to 3918'

 L.2273      3858  LOAD_DEREF               'names'
             3860  LOAD_CONST               None
             3862  COMPARE_OP               is
         3864_3866  POP_JUMP_IF_FALSE  3874  'to 3874'

 L.2274      3868  LOAD_DEREF               'output'
             3870  LOAD_ATTR                T
             3872  RETURN_VALUE     
           3874_0  COME_FROM          3864  '3864'

 L.2275      3874  LOAD_GLOBAL              len
             3876  LOAD_DEREF               'names'
             3878  CALL_FUNCTION_1       1  ''
             3880  LOAD_CONST               1
             3882  COMPARE_OP               ==
         3884_3886  POP_JUMP_IF_FALSE  3900  'to 3900'

 L.2277      3888  LOAD_DEREF               'output'
             3890  LOAD_DEREF               'names'
             3892  LOAD_CONST               0
             3894  BINARY_SUBSCR    
             3896  BINARY_SUBSCR    
             3898  RETURN_VALUE     
           3900_0  COME_FROM          3884  '3884'

 L.2281      3900  LOAD_CLOSURE             'output'
             3902  BUILD_TUPLE_1         1 
             3904  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3906  LOAD_STR                 'genfromtxt.<locals>.<listcomp>'
             3908  MAKE_FUNCTION_8          'closure'
             3910  LOAD_DEREF               'names'
             3912  GET_ITER         
             3914  CALL_FUNCTION_1       1  ''
             3916  RETURN_VALUE     
           3918_0  COME_FROM          3854  '3854'

 L.2282      3918  LOAD_DEREF               'output'
             3920  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 1168_0


_genfromtxt_with_like = array_function_dispatch(_genfromtxt_dispatcher)(genfromtxt)

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