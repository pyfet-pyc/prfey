# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\lib\format.py
r"""
Binary serialization

NPY format
==========

A simple format for saving numpy arrays to disk with the full
information about them.

The ``.npy`` format is the standard binary file format in NumPy for
persisting a *single* arbitrary NumPy array on disk. The format stores all
of the shape and dtype information necessary to reconstruct the array
correctly even on another machine with a different architecture.
The format is designed to be as simple as possible while achieving
its limited goals.

The ``.npz`` format is the standard format for persisting *multiple* NumPy
arrays on disk. A ``.npz`` file is a zip file containing multiple ``.npy``
files, one for each array.

Capabilities
------------

- Can represent all NumPy arrays including nested record arrays and
  object arrays.

- Represents the data in its native binary form.

- Supports Fortran-contiguous arrays directly.

- Stores all of the necessary information to reconstruct the array
  including shape and dtype on a machine of a different
  architecture.  Both little-endian and big-endian arrays are
  supported, and a file with little-endian numbers will yield
  a little-endian array on any machine reading the file. The
  types are described in terms of their actual sizes. For example,
  if a machine with a 64-bit C "long int" writes out an array with
  "long ints", a reading machine with 32-bit C "long ints" will yield
  an array with 64-bit integers.

- Is straightforward to reverse engineer. Datasets often live longer than
  the programs that created them. A competent developer should be
  able to create a solution in their preferred programming language to
  read most ``.npy`` files that he has been given without much
  documentation.

- Allows memory-mapping of the data. See `open_memmep`.

- Can be read from a filelike stream object instead of an actual file.

- Stores object arrays, i.e. arrays containing elements that are arbitrary
  Python objects. Files with object arrays are not to be mmapable, but
  can be read and written to disk.

Limitations
-----------

- Arbitrary subclasses of numpy.ndarray are not completely preserved.
  Subclasses will be accepted for writing, but only the array data will
  be written out. A regular numpy.ndarray object will be created
  upon reading the file.

.. warning::

  Due to limitations in the interpretation of structured dtypes, dtypes
  with fields with empty names will have the names replaced by 'f0', 'f1',
  etc. Such arrays will not round-trip through the format entirely
  accurately. The data is intact; only the field names will differ. We are
  working on a fix for this. This fix will not require a change in the
  file format. The arrays with such structures can still be saved and
  restored, and the correct dtype may be restored by using the
  ``loadedarray.view(correct_dtype)`` method.

File extensions
---------------

We recommend using the ``.npy`` and ``.npz`` extensions for files saved
in this format. This is by no means a requirement; applications may wish
to use these file formats but use an extension specific to the
application. In the absence of an obvious alternative, however,
we suggest using ``.npy`` and ``.npz``.

Version numbering
-----------------

The version numbering of these formats is independent of NumPy version
numbering. If the format is upgraded, the code in `numpy.io` will still
be able to read and write Version 1.0 files.

Format Version 1.0
------------------

The first 6 bytes are a magic string: exactly ``\x93NUMPY``.

The next 1 byte is an unsigned byte: the major version number of the file
format, e.g. ``\x01``.

The next 1 byte is an unsigned byte: the minor version number of the file
format, e.g. ``\x00``. Note: the version of the file format is not tied
to the version of the numpy package.

The next 2 bytes form a little-endian unsigned short int: the length of
the header data HEADER_LEN.

The next HEADER_LEN bytes form the header data describing the array's
format. It is an ASCII string which contains a Python literal expression
of a dictionary. It is terminated by a newline (``\n``) and padded with
spaces (``\x20``) to make the total of
``len(magic string) + 2 + len(length) + HEADER_LEN`` be evenly divisible
by 64 for alignment purposes.

The dictionary contains three keys:

    "descr" : dtype.descr
      An object that can be passed as an argument to the `numpy.dtype`
      constructor to create the array's dtype.
    "fortran_order" : bool
      Whether the array data is Fortran-contiguous or not. Since
      Fortran-contiguous arrays are a common form of non-C-contiguity,
      we allow them to be written directly to disk for efficiency.
    "shape" : tuple of int
      The shape of the array.

For repeatability and readability, the dictionary keys are sorted in
alphabetic order. This is for convenience only. A writer SHOULD implement
this if possible. A reader MUST NOT depend on this.

Following the header comes the array data. If the dtype contains Python
objects (i.e. ``dtype.hasobject is True``), then the data is a Python
pickle of the array. Otherwise the data is the contiguous (either C-
or Fortran-, depending on ``fortran_order``) bytes of the array.
Consumers can figure out the number of bytes by multiplying the number
of elements given by the shape (noting that ``shape=()`` means there is
1 element) by ``dtype.itemsize``.

Format Version 2.0
------------------

The version 1.0 format only allowed the array header to have a total size of
65535 bytes.  This can be exceeded by structured arrays with a large number of
columns.  The version 2.0 format extends the header size to 4 GiB.
`numpy.save` will automatically save in 2.0 format if the data requires it,
else it will always use the more compatible 1.0 format.

The description of the fourth element of the header therefore has become:
"The next 4 bytes form a little-endian unsigned int: the length of the header
data HEADER_LEN."

Format Version 3.0
------------------

This version replaces the ASCII string (which in practice was latin1) with
a utf8-encoded string, so supports structured types with any unicode field
names.

Notes
-----
The ``.npy`` format, including motivation for creating it and a comparison of
alternatives, is described in the `"npy-format" NEP
<https://www.numpy.org/neps/nep-0001-npy-format.html>`_, however details have
evolved with time and this document is more current.

"""
import numpy, io, warnings
from numpy.lib.utils import safe_eval
from numpy.compat import isfileobj, os_fspath, pickle
__all__ = []
MAGIC_PREFIX = b'\x93NUMPY'
MAGIC_LEN = len(MAGIC_PREFIX) + 2
ARRAY_ALIGN = 64
BUFFER_SIZE = 262144
_header_size_info = {(1, 0):('<H', 'latin1'), 
 (2, 0):('<I', 'latin1'), 
 (3, 0):('<I', 'utf8')}

def _check_version(version):
    if version not in ((1, 0), (2, 0), (3, 0), None):
        msg = 'we only support format version (1,0), (2,0), and (3,0), not %s'
        raise ValueError(msg % (version,))


def magic(major, minor):
    """ Return the magic string for the given file format version.

    Parameters
    ----------
    major : int in [0, 255]
    minor : int in [0, 255]

    Returns
    -------
    magic : str

    Raises
    ------
    ValueError if the version cannot be formatted.
    """
    if major < 0 or (major > 255):
        raise ValueError('major version must be 0 <= major < 256')
    if minor < 0 or (minor > 255):
        raise ValueError('minor version must be 0 <= minor < 256')
    return MAGIC_PREFIX + bytes([major, minor])


def read_magic(fp):
    """ Read the magic string to get the version of the file format.

    Parameters
    ----------
    fp : filelike object

    Returns
    -------
    major : int
    minor : int
    """
    magic_str = _read_bytes(fp, MAGIC_LEN, 'magic string')
    if magic_str[:-2] != MAGIC_PREFIX:
        msg = 'the magic string is not correct; expected %r, got %r'
        raise ValueError(msg % (MAGIC_PREFIX, magic_str[:-2]))
    major, minor = magic_str[-2:]
    return (
     major, minor)


def _has_metadata(dt):
    if dt.metadata is not None:
        return True
    if dt.names is not None:
        return any((_has_metadata(dt[k]) for k in dt.names))
    if dt.subdtype is not None:
        return _has_metadata(dt.base)
    return False


def dtype_to_descr(dtype):
    """
    Get a serializable descriptor from the dtype.

    The .descr attribute of a dtype object cannot be round-tripped through
    the dtype() constructor. Simple types, like dtype('float32'), have
    a descr which looks like a record array with one field with '' as
    a name. The dtype() constructor interprets this as a request to give
    a default name.  Instead, we construct descriptor that can be passed to
    dtype().

    Parameters
    ----------
    dtype : dtype
        The dtype of the array that will be written to disk.

    Returns
    -------
    descr : object
        An object that can be passed to `numpy.dtype()` in order to
        replicate the input dtype.

    """
    if _has_metadata(dtype):
        warnings.warn('metadata on a dtype may be saved or ignored, but will raise if saved when read. Use another form of storage.', UserWarning,
          stacklevel=2)
    if dtype.names is not None:
        return dtype.descr
    return dtype.str


def descr_to_dtype(descr):
    """
    descr may be stored as dtype.descr, which is a list of
    (name, format, [shape]) tuples where format may be a str or a tuple.
    Offsets are not explicitly saved, rather empty fields with
    name, format == '', '|Vn' are added as padding.

    This function reverses the process, eliminating the empty padding fields.
    """
    if isinstance(descr, str):
        return numpy.dtype(descr)
    if isinstance(descr, tuple):
        dt = descr_to_dtype(descr[0])
        return numpy.dtype((dt, descr[1]))
    titles = []
    names = []
    formats = []
    offsets = []
    offset = 0
    for field in descr:
        if len(field) == 2:
            name, descr_str = field
            dt = descr_to_dtype(descr_str)
        else:
            name, descr_str, shape = field
            dt = numpy.dtype((descr_to_dtype(descr_str), shape))
        is_pad = name == '' and dt.type is numpy.void and dt.names is None
        if not is_pad:
            title, name = name if isinstance(name, tuple) else (None, name)
            titles.append(title)
            names.append(name)
            formats.append(dt)
            offsets.append(offset)
        else:
            offset += dt.itemsize
    else:
        return numpy.dtype({'names':names,  'formats':formats,  'titles':titles,  'offsets':offsets, 
         'itemsize':offset})


def header_data_from_array_1_0(array):
    """ Get the dictionary of header metadata from a numpy.ndarray.

    Parameters
    ----------
    array : numpy.ndarray

    Returns
    -------
    d : dict
        This has the appropriate entries for writing its string representation
        to the header of the file.
    """
    d = {'shape': array.shape}
    if array.flags.c_contiguous:
        d['fortran_order'] = False
    elif array.flags.f_contiguous:
        d['fortran_order'] = True
    else:
        d['fortran_order'] = False
    d['descr'] = dtype_to_descr(array.dtype)
    return d


def _wrap_header(header, version):
    """
    Takes a stringified header, and attaches the prefix and padding to it
    """
    import struct
    assert version is not None
    fmt, encoding = _header_size_info[version]
    if not isinstance(header, bytes):
        header = header.encode(encoding)
    hlen = len(header) + 1
    padlen = ARRAY_ALIGN - (MAGIC_LEN + struct.calcsize(fmt) + hlen) % ARRAY_ALIGN
    try:
        header_prefix = magic(*version) + struct.pack(fmt, hlen + padlen)
    except struct.error:
        msg = 'Header length {} too big for version={}'.format(hlen, version)
        raise ValueError(msg)
    else:
        return header_prefix + header + b' ' * padlen + b'\n'


def _wrap_header_guess_version--- This code section failed: ---

 L. 383         0  SETUP_FINALLY        14  'to 14'

 L. 384         2  LOAD_GLOBAL              _wrap_header
                4  LOAD_FAST                'header'
                6  LOAD_CONST               (1, 0)
                8  CALL_FUNCTION_2       2  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 385        14  DUP_TOP          
               16  LOAD_GLOBAL              ValueError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    32  'to 32'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 386        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            20  '20'
               32  END_FINALLY      
             34_0  COME_FROM            30  '30'

 L. 388        34  SETUP_FINALLY        50  'to 50'

 L. 389        36  LOAD_GLOBAL              _wrap_header
               38  LOAD_FAST                'header'
               40  LOAD_CONST               (2, 0)
               42  CALL_FUNCTION_2       2  ''
               44  STORE_FAST               'ret'
               46  POP_BLOCK        
               48  JUMP_FORWARD         70  'to 70'
             50_0  COME_FROM_FINALLY    34  '34'

 L. 390        50  DUP_TOP          
               52  LOAD_GLOBAL              UnicodeEncodeError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    68  'to 68'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 391        64  POP_EXCEPT       
               66  JUMP_FORWARD         90  'to 90'
             68_0  COME_FROM            56  '56'
               68  END_FINALLY      
             70_0  COME_FROM            48  '48'

 L. 393        70  LOAD_GLOBAL              warnings
               72  LOAD_ATTR                warn
               74  LOAD_STR                 'Stored array in format 2.0. It can only beread by NumPy >= 1.9'

 L. 394        76  LOAD_GLOBAL              UserWarning

 L. 394        78  LOAD_CONST               2

 L. 393        80  LOAD_CONST               ('stacklevel',)
               82  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               84  POP_TOP          

 L. 395        86  LOAD_FAST                'ret'
               88  RETURN_VALUE     
             90_0  COME_FROM            66  '66'

 L. 397        90  LOAD_GLOBAL              _wrap_header
               92  LOAD_FAST                'header'
               94  LOAD_CONST               (3, 0)
               96  CALL_FUNCTION_2       2  ''
               98  STORE_FAST               'header'

 L. 398       100  LOAD_GLOBAL              warnings
              102  LOAD_ATTR                warn
              104  LOAD_STR                 'Stored array in format 3.0. It can only be read by NumPy >= 1.17'

 L. 399       106  LOAD_GLOBAL              UserWarning

 L. 399       108  LOAD_CONST               2

 L. 398       110  LOAD_CONST               ('stacklevel',)
              112  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              114  POP_TOP          

 L. 400       116  LOAD_FAST                'header'
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 32_0


def _write_array_header(fp, d, version=None):
    """ Write the header for an array and returns the version used

    Parameters
    ----------
    fp : filelike object
    d : dict
        This has the appropriate entries for writing its string representation
        to the header of the file.
    version: tuple or None
        None means use oldest that works
        explicit version will raise a ValueError if the format does not
        allow saving this data.  Default: None
    """
    header = [
     '{']
    for key, value in sorted(d.items()):
        header.append("'%s': %s, " % (key, repr(value)))
    else:
        header.append('}')
        header = ''.join(header)
        header = _filter_header(header)
        if version is None:
            header = _wrap_header_guess_version(header)
        else:
            header = _wrap_header(header, version)
        fp.write(header)


def write_array_header_1_0(fp, d):
    """ Write the header for an array using the 1.0 format.

    Parameters
    ----------
    fp : filelike object
    d : dict
        This has the appropriate entries for writing its string
        representation to the header of the file.
    """
    _write_array_header(fp, d, (1, 0))


def write_array_header_2_0(fp, d):
    """ Write the header for an array using the 2.0 format.
        The 2.0 format allows storing very large structured arrays.

    .. versionadded:: 1.9.0

    Parameters
    ----------
    fp : filelike object
    d : dict
        This has the appropriate entries for writing its string
        representation to the header of the file.
    """
    _write_array_header(fp, d, (2, 0))


def read_array_header_1_0(fp):
    """
    Read an array header from a filelike object using the 1.0 file format
    version.

    This will leave the file object located just after the header.

    Parameters
    ----------
    fp : filelike object
        A file object or something with a `.read()` method like a file.

    Returns
    -------
    shape : tuple of int
        The shape of the array.
    fortran_order : bool
        The array data will be written out directly if it is either
        C-contiguous or Fortran-contiguous. Otherwise, it will be made
        contiguous before writing it out.
    dtype : dtype
        The dtype of the file's data.

    Raises
    ------
    ValueError
        If the data is invalid.

    """
    return _read_array_header(fp, version=(1, 0))


def read_array_header_2_0(fp):
    """
    Read an array header from a filelike object using the 2.0 file format
    version.

    This will leave the file object located just after the header.

    .. versionadded:: 1.9.0

    Parameters
    ----------
    fp : filelike object
        A file object or something with a `.read()` method like a file.

    Returns
    -------
    shape : tuple of int
        The shape of the array.
    fortran_order : bool
        The array data will be written out directly if it is either
        C-contiguous or Fortran-contiguous. Otherwise, it will be made
        contiguous before writing it out.
    dtype : dtype
        The dtype of the file's data.

    Raises
    ------
    ValueError
        If the data is invalid.

    """
    return _read_array_header(fp, version=(2, 0))


def _filter_header--- This code section failed: ---

 L. 540         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              tokenize
                6  STORE_FAST               'tokenize'

 L. 541         8  LOAD_CONST               0
               10  LOAD_CONST               ('StringIO',)
               12  IMPORT_NAME              io
               14  IMPORT_FROM              StringIO
               16  STORE_FAST               'StringIO'
               18  POP_TOP          

 L. 543        20  BUILD_LIST_0          0 
               22  STORE_FAST               'tokens'

 L. 544        24  LOAD_CONST               False
               26  STORE_FAST               'last_token_was_number'

 L. 545        28  LOAD_FAST                'tokenize'
               30  LOAD_METHOD              generate_tokens
               32  LOAD_FAST                'StringIO'
               34  LOAD_FAST                's'
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_ATTR                readline
               40  CALL_METHOD_1         1  ''
               42  GET_ITER         
             44_0  COME_FROM           110  '110'
             44_1  COME_FROM            86  '86'
               44  FOR_ITER            112  'to 112'
               46  STORE_FAST               'token'

 L. 546        48  LOAD_FAST                'token'
               50  LOAD_CONST               0
               52  BINARY_SUBSCR    
               54  STORE_FAST               'token_type'

 L. 547        56  LOAD_FAST                'token'
               58  LOAD_CONST               1
               60  BINARY_SUBSCR    
               62  STORE_FAST               'token_string'

 L. 548        64  LOAD_FAST                'last_token_was_number'
               66  POP_JUMP_IF_FALSE    90  'to 90'

 L. 549        68  LOAD_FAST                'token_type'
               70  LOAD_FAST                'tokenize'
               72  LOAD_ATTR                NAME
               74  COMPARE_OP               ==

 L. 548        76  POP_JUMP_IF_FALSE    90  'to 90'

 L. 550        78  LOAD_FAST                'token_string'
               80  LOAD_STR                 'L'
               82  COMPARE_OP               ==

 L. 548        84  POP_JUMP_IF_FALSE    90  'to 90'

 L. 551        86  JUMP_BACK            44  'to 44'
               88  BREAK_LOOP          100  'to 100'
             90_0  COME_FROM            84  '84'
             90_1  COME_FROM            76  '76'
             90_2  COME_FROM            66  '66'

 L. 553        90  LOAD_FAST                'tokens'
               92  LOAD_METHOD              append
               94  LOAD_FAST                'token'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
            100_0  COME_FROM            88  '88'

 L. 554       100  LOAD_FAST                'token_type'
              102  LOAD_FAST                'tokenize'
              104  LOAD_ATTR                NUMBER
              106  COMPARE_OP               ==
              108  STORE_FAST               'last_token_was_number'
              110  JUMP_BACK            44  'to 44'
            112_0  COME_FROM            44  '44'

 L. 555       112  LOAD_FAST                'tokenize'
              114  LOAD_METHOD              untokenize
              116  LOAD_FAST                'tokens'
              118  CALL_METHOD_1         1  ''
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 112


def _read_array_header(fp, version):
    """
    see read_array_header_1_0
    """
    import struct
    hinfo = _header_size_info.get(version)
    if hinfo is None:
        raise ValueError('Invalid version {!r}'.format(version))
    hlength_type, encoding = hinfo
    hlength_str = _read_bytes(fp, struct.calcsize(hlength_type), 'array header length')
    header_length = struct.unpack(hlength_type, hlength_str)[0]
    header = _read_bytes(fp, header_length, 'array header')
    header = header.decode(encoding)
    header = _filter_header(header)
    try:
        d = safe_eval(header)
    except SyntaxError as e:
        try:
            msg = 'Cannot parse header: {!r}\nException: {!r}'
            raise ValueError(msg.format(header, e))
        finally:
            e = None
            del e

    else:
        if not isinstance(d, dict):
            msg = 'Header is not a dictionary: {!r}'
            raise ValueError(msg.format(d))
        else:
            keys = sorted(d.keys())
            if keys != ['descr', 'fortran_order', 'shape']:
                msg = 'Header does not contain the correct keys: {!r}'
                raise ValueError(msg.format(keys))
            if not (isinstance(d['shape'], tuple) and numpy.all([isinstance(x, int) for x in d['shape']])):
                msg = 'shape is not valid: {!r}'
                raise ValueError(msg.format(d['shape']))
            if not isinstance(d['fortran_order'], bool):
                msg = 'fortran_order is not a valid bool: {!r}'
                raise ValueError(msg.format(d['fortran_order']))
            try:
                dtype = descr_to_dtype(d['descr'])
            except TypeError:
                msg = 'descr is not a valid dtype descriptor: {!r}'
                raise ValueError(msg.format(d['descr']))
            else:
                return (
                 d['shape'], d['fortran_order'], dtype)


def write_array(fp, array, version=None, allow_pickle=True, pickle_kwargs=None):
    """
    Write an array to an NPY file, including a header.

    If the array is neither C-contiguous nor Fortran-contiguous AND the
    file_like object is not a real file object, this function will have to
    copy data in memory.

    Parameters
    ----------
    fp : file_like object
        An open, writable file object, or similar object with a
        ``.write()`` method.
    array : ndarray
        The array to write to disk.
    version : (int, int) or None, optional
        The version number of the format. None means use the oldest
        supported version that is able to store the data.  Default: None
    allow_pickle : bool, optional
        Whether to allow writing pickled data. Default: True
    pickle_kwargs : dict, optional
        Additional keyword arguments to pass to pickle.dump, excluding
        'protocol'. These are only useful when pickling objects in object
        arrays on Python 3 to Python 2 compatible format.

    Raises
    ------
    ValueError
        If the array cannot be persisted. This includes the case of
        allow_pickle=False and array being an object array.
    Various other errors
        If the array contains Python objects as part of its dtype, the
        process of pickling them may raise various errors if the objects
        are not picklable.

    """
    _check_version(version)
    _write_array_header(fp, header_data_from_array_1_0(array), version)
    if array.itemsize == 0:
        buffersize = 0
    else:
        buffersize = max(16777216 // array.itemsize, 1)
    if array.dtype.hasobject:
        if not allow_pickle:
            raise ValueError('Object arrays cannot be saved when allow_pickle=False')
        if pickle_kwargs is None:
            pickle_kwargs = {}
        (pickle.dump)(array, fp, protocol=3, **pickle_kwargs)
    else:
        pass
    if array.flags.f_contiguous and not array.flags.c_contiguous:
        if isfileobj(fp):
            array.T.tofile(fp)
        else:
            for chunk in numpy.nditer(array,
              flags=['external_loop', 'buffered', 'zerosize_ok'], buffersize=buffersize,
              order='F'):
                fp.write(chunk.tobytes('C'))

    elif isfileobj(fp):
        array.tofile(fp)
    else:
        for chunk in numpy.nditer(array,
          flags=['external_loop', 'buffered', 'zerosize_ok'], buffersize=buffersize,
          order='C'):
            fp.write(chunk.tobytes('C'))


def read_array(fp, allow_pickle=False, pickle_kwargs=None):
    """
    Read an array from an NPY file.

    Parameters
    ----------
    fp : file_like object
        If this is not a real file object, then this may take extra memory
        and time.
    allow_pickle : bool, optional
        Whether to allow writing pickled data. Default: False

        .. versionchanged:: 1.16.3
            Made default False in response to CVE-2019-6446.

    pickle_kwargs : dict
        Additional keyword arguments to pass to pickle.load. These are only
        useful when loading object arrays saved on Python 2 when using
        Python 3.

    Returns
    -------
    array : ndarray
        The array from the data on disk.

    Raises
    ------
    ValueError
        If the data is invalid, or allow_pickle=False and the file contains
        an object array.

    """
    version = read_magic(fp)
    _check_version(version)
    shape, fortran_order, dtype = _read_array_header(fp, version)
    if len(shape) == 0:
        count = 1
    else:
        count = numpy.multiply.reduce(shape, dtype=(numpy.int64))
    if dtype.hasobject:
        if not allow_pickle:
            raise ValueError('Object arrays cannot be loaded when allow_pickle=False')
        if pickle_kwargs is None:
            pickle_kwargs = {}
        try:
            array = (pickle.load)(fp, **pickle_kwargs)
        except UnicodeError as err:
            try:
                raise UnicodeError('Unpickling a python object failed: %r\nYou may need to pass the encoding= option to numpy.load' % (
                 err,))
            finally:
                err = None
                del err

    else:
        if isfileobj(fp):
            array = numpy.fromfile(fp, dtype=dtype, count=count)
        else:
            array = numpy.ndarray(count, dtype=dtype)
            if dtype.itemsize > 0:
                max_read_count = BUFFER_SIZE // min(BUFFER_SIZE, dtype.itemsize)
                for i in range(0, count, max_read_count):
                    read_count = min(max_read_count, count - i)
                    read_size = int(read_count * dtype.itemsize)
                    data = _read_bytes(fp, read_size, 'array data')
                    array[i:i + read_count] = numpy.frombuffer(data, dtype=dtype, count=read_count)

        if fortran_order:
            array.shape = shape[::-1]
            array = array.transpose()
        else:
            array.shape = shape
    return array


def open_memmap(filename, mode='r+', dtype=None, shape=None, fortran_order=False, version=None):
    """
    Open a .npy file as a memory-mapped array.

    This may be used to read an existing file or create a new one.

    Parameters
    ----------
    filename : str or path-like
        The name of the file on disk.  This may *not* be a file-like
        object.
    mode : str, optional
        The mode in which to open the file; the default is 'r+'.  In
        addition to the standard file modes, 'c' is also accepted to mean
        "copy on write."  See `memmap` for the available mode strings.
    dtype : data-type, optional
        The data type of the array if we are creating a new file in "write"
        mode, if not, `dtype` is ignored.  The default value is None, which
        results in a data-type of `float64`.
    shape : tuple of int
        The shape of the array if we are creating a new file in "write"
        mode, in which case this parameter is required.  Otherwise, this
        parameter is ignored and is thus optional.
    fortran_order : bool, optional
        Whether the array should be Fortran-contiguous (True) or
        C-contiguous (False, the default) if we are creating a new file in
        "write" mode.
    version : tuple of int (major, minor) or None
        If the mode is a "write" mode, then this is the version of the file
        format used to create the file.  None means use the oldest
        supported version that is able to store the data.  Default: None

    Returns
    -------
    marray : memmap
        The memory-mapped array.

    Raises
    ------
    ValueError
        If the data or the mode is invalid.
    IOError
        If the file is not found or cannot be opened correctly.

    See Also
    --------
    memmap

    """
    if isfileobj(filename):
        raise ValueError('Filename must be a string or a path-like object.  Memmap cannot use existing file handles.')
    if 'w' in mode:
        _check_version(version)
        dtype = numpy.dtype(dtype)
        if dtype.hasobject:
            msg = "Array can't be memory-mapped: Python objects in dtype."
            raise ValueError(msg)
        d = dict(descr=(dtype_to_descr(dtype)),
          fortran_order=fortran_order,
          shape=shape)
        with open(os_fspath(filename), mode + 'b') as fp:
            _write_array_header(fp, d, version)
            offset = fp.tell()
    else:
        with open(os_fspath(filename), 'rb') as fp:
            version = read_magic(fp)
            _check_version(version)
            shape, fortran_order, dtype = _read_array_header(fp, version)
            if dtype.hasobject:
                msg = "Array can't be memory-mapped: Python objects in dtype."
                raise ValueError(msg)
            offset = fp.tell()
    if fortran_order:
        order = 'F'
    else:
        order = 'C'
    if mode == 'w+':
        mode = 'r+'
    marray = numpy.memmap(filename, dtype=dtype, shape=shape, order=order, mode=mode,
      offset=offset)
    return marray


def _read_bytes(fp, size, error_template='ran out of data'):
    """
    Read from file-like object until size bytes are read.
    Raises ValueError if not EOF is encountered before size bytes are read.
    Non-blocking objects only supported if they derive from io objects.

    Required as e.g. ZipExtFile in python 2.6 can return less data than
    requested.
    """
    data = bytes()
    while True:
        try:
            r = fp.read(size - len(data))
            data += r
            if len(r) == 0 or (len(data) == size):
                break
        except io.BlockingIOError:
            pass

    if len(data) != size:
        msg = 'EOF: reading %s, expected %d bytes got %d'
        raise ValueError(msg % (error_template, size, len(data)))
    else:
        return data