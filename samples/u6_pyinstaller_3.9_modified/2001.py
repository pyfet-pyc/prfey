# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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

def _check_version--- This code section failed: ---

 L. 191         0  LOAD_FAST                'version'
                2  LOAD_CONST               ((1, 0), (2, 0), (3, 0), None)
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    26  'to 26'

 L. 192         8  LOAD_STR                 'we only support format version (1,0), (2,0), and (3,0), not %s'
               10  STORE_FAST               'msg'

 L. 193        12  LOAD_GLOBAL              ValueError
               14  LOAD_FAST                'msg'
               16  LOAD_FAST                'version'
               18  BUILD_TUPLE_1         1 
               20  BINARY_MODULO    
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1


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
    if major < 0 or major > 255:
        raise ValueError('major version must be 0 <= major < 256')
    if minor < 0 or minor > 255:
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
    return (major, minor)


def _has_metadata--- This code section failed: ---

 L. 237         0  LOAD_DEREF               'dt'
                2  LOAD_ATTR                metadata
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 238        10  LOAD_CONST               True
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 239        14  LOAD_DEREF               'dt'
               16  LOAD_ATTR                names
               18  LOAD_CONST               None
               20  <117>                 1  ''
               22  POP_JUMP_IF_FALSE    48  'to 48'

 L. 240        24  LOAD_GLOBAL              any
               26  LOAD_CLOSURE             'dt'
               28  BUILD_TUPLE_1         1 
               30  LOAD_GENEXPR             '<code_object <genexpr>>'
               32  LOAD_STR                 '_has_metadata.<locals>.<genexpr>'
               34  MAKE_FUNCTION_8          'closure'
               36  LOAD_DEREF               'dt'
               38  LOAD_ATTR                names
               40  GET_ITER         
               42  CALL_FUNCTION_1       1  ''
               44  CALL_FUNCTION_1       1  ''
               46  RETURN_VALUE     
             48_0  COME_FROM            22  '22'

 L. 241        48  LOAD_DEREF               'dt'
               50  LOAD_ATTR                subdtype
               52  LOAD_CONST               None
               54  <117>                 1  ''
               56  POP_JUMP_IF_FALSE    68  'to 68'

 L. 242        58  LOAD_GLOBAL              _has_metadata
               60  LOAD_DEREF               'dt'
               62  LOAD_ATTR                base
               64  CALL_FUNCTION_1       1  ''
               66  RETURN_VALUE     
             68_0  COME_FROM            56  '56'

 L. 244        68  LOAD_CONST               False
               70  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def dtype_to_descr--- This code section failed: ---

 L. 269         0  LOAD_GLOBAL              _has_metadata
                2  LOAD_FAST                'dtype'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L. 270         8  LOAD_GLOBAL              warnings
               10  LOAD_ATTR                warn
               12  LOAD_STR                 'metadata on a dtype may be saved or ignored, but will raise if saved when read. Use another form of storage.'

 L. 272        14  LOAD_GLOBAL              UserWarning
               16  LOAD_CONST               2

 L. 270        18  LOAD_CONST               ('stacklevel',)
               20  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               22  POP_TOP          
             24_0  COME_FROM             6  '6'

 L. 273        24  LOAD_FAST                'dtype'
               26  LOAD_ATTR                names
               28  LOAD_CONST               None
               30  <117>                 1  ''
               32  POP_JUMP_IF_FALSE    40  'to 40'

 L. 278        34  LOAD_FAST                'dtype'
               36  LOAD_ATTR                descr
               38  RETURN_VALUE     
             40_0  COME_FROM            32  '32'

 L. 280        40  LOAD_FAST                'dtype'
               42  LOAD_ATTR                str
               44  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 30


def descr_to_dtype--- This code section failed: ---

 L. 291         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'descr'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 293        10  LOAD_GLOBAL              numpy
               12  LOAD_METHOD              dtype
               14  LOAD_FAST                'descr'
               16  CALL_METHOD_1         1  ''
               18  RETURN_VALUE     
             20_0  COME_FROM             8  '8'

 L. 294        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'descr'
               24  LOAD_GLOBAL              tuple
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    60  'to 60'

 L. 296        30  LOAD_GLOBAL              descr_to_dtype
               32  LOAD_FAST                'descr'
               34  LOAD_CONST               0
               36  BINARY_SUBSCR    
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'dt'

 L. 297        42  LOAD_GLOBAL              numpy
               44  LOAD_METHOD              dtype
               46  LOAD_FAST                'dt'
               48  LOAD_FAST                'descr'
               50  LOAD_CONST               1
               52  BINARY_SUBSCR    
               54  BUILD_TUPLE_2         2 
               56  CALL_METHOD_1         1  ''
               58  RETURN_VALUE     
             60_0  COME_FROM            28  '28'

 L. 299        60  BUILD_LIST_0          0 
               62  STORE_FAST               'titles'

 L. 300        64  BUILD_LIST_0          0 
               66  STORE_FAST               'names'

 L. 301        68  BUILD_LIST_0          0 
               70  STORE_FAST               'formats'

 L. 302        72  BUILD_LIST_0          0 
               74  STORE_FAST               'offsets'

 L. 303        76  LOAD_CONST               0
               78  STORE_FAST               'offset'

 L. 304        80  LOAD_FAST                'descr'
               82  GET_ITER         
               84  FOR_ITER            258  'to 258'
               86  STORE_FAST               'field'

 L. 305        88  LOAD_GLOBAL              len
               90  LOAD_FAST                'field'
               92  CALL_FUNCTION_1       1  ''
               94  LOAD_CONST               2
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   118  'to 118'

 L. 306       100  LOAD_FAST                'field'
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'name'
              106  STORE_FAST               'descr_str'

 L. 307       108  LOAD_GLOBAL              descr_to_dtype
              110  LOAD_FAST                'descr_str'
              112  CALL_FUNCTION_1       1  ''
              114  STORE_FAST               'dt'
              116  JUMP_FORWARD        146  'to 146'
            118_0  COME_FROM            98  '98'

 L. 309       118  LOAD_FAST                'field'
              120  UNPACK_SEQUENCE_3     3 
              122  STORE_FAST               'name'
              124  STORE_FAST               'descr_str'
              126  STORE_FAST               'shape'

 L. 310       128  LOAD_GLOBAL              numpy
              130  LOAD_METHOD              dtype
              132  LOAD_GLOBAL              descr_to_dtype
              134  LOAD_FAST                'descr_str'
              136  CALL_FUNCTION_1       1  ''
              138  LOAD_FAST                'shape'
              140  BUILD_TUPLE_2         2 
              142  CALL_METHOD_1         1  ''
              144  STORE_FAST               'dt'
            146_0  COME_FROM           116  '116'

 L. 314       146  LOAD_FAST                'name'
              148  LOAD_STR                 ''
              150  COMPARE_OP               ==
              152  JUMP_IF_FALSE_OR_POP   174  'to 174'
              154  LOAD_FAST                'dt'
              156  LOAD_ATTR                type
              158  LOAD_GLOBAL              numpy
              160  LOAD_ATTR                void
              162  <117>                 0  ''
              164  JUMP_IF_FALSE_OR_POP   174  'to 174'
              166  LOAD_FAST                'dt'
              168  LOAD_ATTR                names
              170  LOAD_CONST               None
              172  <117>                 0  ''
            174_0  COME_FROM           164  '164'
            174_1  COME_FROM           152  '152'
              174  STORE_FAST               'is_pad'

 L. 315       176  LOAD_FAST                'is_pad'
              178  POP_JUMP_IF_TRUE    246  'to 246'

 L. 316       180  LOAD_GLOBAL              isinstance
              182  LOAD_FAST                'name'
              184  LOAD_GLOBAL              tuple
              186  CALL_FUNCTION_2       2  ''
              188  POP_JUMP_IF_FALSE   194  'to 194'
              190  LOAD_FAST                'name'
              192  JUMP_FORWARD        200  'to 200'
            194_0  COME_FROM           188  '188'
              194  LOAD_CONST               None
              196  LOAD_FAST                'name'
              198  BUILD_TUPLE_2         2 
            200_0  COME_FROM           192  '192'
              200  UNPACK_SEQUENCE_2     2 
              202  STORE_FAST               'title'
              204  STORE_FAST               'name'

 L. 317       206  LOAD_FAST                'titles'
              208  LOAD_METHOD              append
              210  LOAD_FAST                'title'
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 318       216  LOAD_FAST                'names'
              218  LOAD_METHOD              append
              220  LOAD_FAST                'name'
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          

 L. 319       226  LOAD_FAST                'formats'
              228  LOAD_METHOD              append
              230  LOAD_FAST                'dt'
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          

 L. 320       236  LOAD_FAST                'offsets'
              238  LOAD_METHOD              append
              240  LOAD_FAST                'offset'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          
            246_0  COME_FROM           178  '178'

 L. 321       246  LOAD_FAST                'offset'
              248  LOAD_FAST                'dt'
              250  LOAD_ATTR                itemsize
              252  INPLACE_ADD      
              254  STORE_FAST               'offset'
              256  JUMP_BACK            84  'to 84'

 L. 323       258  LOAD_GLOBAL              numpy
              260  LOAD_METHOD              dtype
              262  LOAD_FAST                'names'
              264  LOAD_FAST                'formats'
              266  LOAD_FAST                'titles'

 L. 324       268  LOAD_FAST                'offsets'
              270  LOAD_FAST                'offset'

 L. 323       272  LOAD_CONST               ('names', 'formats', 'titles', 'offsets', 'itemsize')
              274  BUILD_CONST_KEY_MAP_5     5 
              276  CALL_METHOD_1         1  ''
              278  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 162


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
    else:
        if array.flags.f_contiguous:
            d['fortran_order'] = True
        else:
            d['fortran_order'] = False
    d['descr'] = dtype_to_descr(array.dtype)
    return d


def _wrap_header--- This code section failed: ---

 L. 358         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              struct
                6  STORE_FAST               'struct'

 L. 359         8  LOAD_FAST                'version'
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_TRUE     20  'to 20'
               16  <74>             
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            14  '14'

 L. 360        20  LOAD_GLOBAL              _header_size_info
               22  LOAD_FAST                'version'
               24  BINARY_SUBSCR    
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'fmt'
               30  STORE_FAST               'encoding'

 L. 361        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'header'
               36  LOAD_GLOBAL              bytes
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_TRUE     52  'to 52'

 L. 362        42  LOAD_FAST                'header'
               44  LOAD_METHOD              encode
               46  LOAD_FAST                'encoding'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'header'
             52_0  COME_FROM            40  '40'

 L. 363        52  LOAD_GLOBAL              len
               54  LOAD_FAST                'header'
               56  CALL_FUNCTION_1       1  ''
               58  LOAD_CONST               1
               60  BINARY_ADD       
               62  STORE_FAST               'hlen'

 L. 364        64  LOAD_GLOBAL              ARRAY_ALIGN
               66  LOAD_GLOBAL              MAGIC_LEN
               68  LOAD_FAST                'struct'
               70  LOAD_METHOD              calcsize
               72  LOAD_FAST                'fmt'
               74  CALL_METHOD_1         1  ''
               76  BINARY_ADD       
               78  LOAD_FAST                'hlen'
               80  BINARY_ADD       
               82  LOAD_GLOBAL              ARRAY_ALIGN
               84  BINARY_MODULO    
               86  BINARY_SUBTRACT  
               88  STORE_FAST               'padlen'

 L. 365        90  SETUP_FINALLY       120  'to 120'

 L. 366        92  LOAD_GLOBAL              magic
               94  LOAD_FAST                'version'
               96  CALL_FUNCTION_EX      0  'positional arguments only'
               98  LOAD_FAST                'struct'
              100  LOAD_METHOD              pack
              102  LOAD_FAST                'fmt'
              104  LOAD_FAST                'hlen'
              106  LOAD_FAST                'padlen'
              108  BINARY_ADD       
              110  CALL_METHOD_2         2  ''
              112  BINARY_ADD       
              114  STORE_FAST               'header_prefix'
              116  POP_BLOCK        
              118  JUMP_FORWARD        160  'to 160'
            120_0  COME_FROM_FINALLY    90  '90'

 L. 367       120  DUP_TOP          
              122  LOAD_FAST                'struct'
              124  LOAD_ATTR                error
              126  <121>               158  ''
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L. 368       134  LOAD_STR                 'Header length {} too big for version={}'
              136  LOAD_METHOD              format
              138  LOAD_FAST                'hlen'
              140  LOAD_FAST                'version'
              142  CALL_METHOD_2         2  ''
              144  STORE_FAST               'msg'

 L. 369       146  LOAD_GLOBAL              ValueError
              148  LOAD_FAST                'msg'
              150  CALL_FUNCTION_1       1  ''
              152  RAISE_VARARGS_1       1  'exception instance'
              154  POP_EXCEPT       
              156  JUMP_FORWARD        160  'to 160'
              158  <48>             
            160_0  COME_FROM           156  '156'
            160_1  COME_FROM           118  '118'

 L. 376       160  LOAD_FAST                'header_prefix'
              162  LOAD_FAST                'header'
              164  BINARY_ADD       
              166  LOAD_CONST               b' '
              168  LOAD_FAST                'padlen'
              170  BINARY_MULTIPLY  
              172  BINARY_ADD       
              174  LOAD_CONST               b'\n'
              176  BINARY_ADD       
              178  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 12


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
               18  <121>                30  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 386        26  POP_EXCEPT       
               28  JUMP_FORWARD         32  'to 32'
               30  <48>             
             32_0  COME_FROM            28  '28'

 L. 388        32  SETUP_FINALLY        48  'to 48'

 L. 389        34  LOAD_GLOBAL              _wrap_header
               36  LOAD_FAST                'header'
               38  LOAD_CONST               (2, 0)
               40  CALL_FUNCTION_2       2  ''
               42  STORE_FAST               'ret'
               44  POP_BLOCK        
               46  JUMP_FORWARD         66  'to 66'
             48_0  COME_FROM_FINALLY    32  '32'

 L. 390        48  DUP_TOP          
               50  LOAD_GLOBAL              UnicodeEncodeError
               52  <121>                64  ''
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 391        60  POP_EXCEPT       
               62  JUMP_FORWARD         86  'to 86'
               64  <48>             
             66_0  COME_FROM            46  '46'

 L. 393        66  LOAD_GLOBAL              warnings
               68  LOAD_ATTR                warn
               70  LOAD_STR                 'Stored array in format 2.0. It can only beread by NumPy >= 1.9'

 L. 394        72  LOAD_GLOBAL              UserWarning
               74  LOAD_CONST               2

 L. 393        76  LOAD_CONST               ('stacklevel',)
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               80  POP_TOP          

 L. 395        82  LOAD_FAST                'ret'
               84  RETURN_VALUE     
             86_0  COME_FROM            62  '62'

 L. 397        86  LOAD_GLOBAL              _wrap_header
               88  LOAD_FAST                'header'
               90  LOAD_CONST               (3, 0)
               92  CALL_FUNCTION_2       2  ''
               94  STORE_FAST               'header'

 L. 398        96  LOAD_GLOBAL              warnings
               98  LOAD_ATTR                warn
              100  LOAD_STR                 'Stored array in format 3.0. It can only be read by NumPy >= 1.17'

 L. 399       102  LOAD_GLOBAL              UserWarning
              104  LOAD_CONST               2

 L. 398       106  LOAD_CONST               ('stacklevel',)
              108  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              110  POP_TOP          

 L. 400       112  LOAD_FAST                'header'
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 18


def _write_array_header--- This code section failed: ---

 L. 417         0  LOAD_STR                 '{'
                2  BUILD_LIST_1          1 
                4  STORE_FAST               'header'

 L. 418         6  LOAD_GLOBAL              sorted
                8  LOAD_FAST                'd'
               10  LOAD_METHOD              items
               12  CALL_METHOD_0         0  ''
               14  CALL_FUNCTION_1       1  ''
               16  GET_ITER         
               18  FOR_ITER             50  'to 50'
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'key'
               24  STORE_FAST               'value'

 L. 420        26  LOAD_FAST                'header'
               28  LOAD_METHOD              append
               30  LOAD_STR                 "'%s': %s, "
               32  LOAD_FAST                'key'
               34  LOAD_GLOBAL              repr
               36  LOAD_FAST                'value'
               38  CALL_FUNCTION_1       1  ''
               40  BUILD_TUPLE_2         2 
               42  BINARY_MODULO    
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
               48  JUMP_BACK            18  'to 18'

 L. 421        50  LOAD_FAST                'header'
               52  LOAD_METHOD              append
               54  LOAD_STR                 '}'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L. 422        60  LOAD_STR                 ''
               62  LOAD_METHOD              join
               64  LOAD_FAST                'header'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'header'

 L. 423        70  LOAD_GLOBAL              _filter_header
               72  LOAD_FAST                'header'
               74  CALL_FUNCTION_1       1  ''
               76  STORE_FAST               'header'

 L. 424        78  LOAD_FAST                'version'
               80  LOAD_CONST               None
               82  <117>                 0  ''
               84  POP_JUMP_IF_FALSE    96  'to 96'

 L. 425        86  LOAD_GLOBAL              _wrap_header_guess_version
               88  LOAD_FAST                'header'
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'header'
               94  JUMP_FORWARD        106  'to 106'
             96_0  COME_FROM            84  '84'

 L. 427        96  LOAD_GLOBAL              _wrap_header
               98  LOAD_FAST                'header'
              100  LOAD_FAST                'version'
              102  CALL_FUNCTION_2       2  ''
              104  STORE_FAST               'header'
            106_0  COME_FROM            94  '94'

 L. 428       106  LOAD_FAST                'fp'
              108  LOAD_METHOD              write
              110  LOAD_FAST                'header'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

Parse error at or near `<117>' instruction at offset 82


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
               88  JUMP_FORWARD        100  'to 100'
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

 L. 555       112  LOAD_FAST                'tokenize'
              114  LOAD_METHOD              untokenize
              116  LOAD_FAST                'tokens'
              118  CALL_METHOD_1         1  ''
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 88


def _read_array_header--- This code section failed: ---

 L. 564         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              struct
                6  STORE_FAST               'struct'

 L. 565         8  LOAD_GLOBAL              _header_size_info
               10  LOAD_METHOD              get
               12  LOAD_FAST                'version'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'hinfo'

 L. 566        18  LOAD_FAST                'hinfo'
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE    40  'to 40'

 L. 567        26  LOAD_GLOBAL              ValueError
               28  LOAD_STR                 'Invalid version {!r}'
               30  LOAD_METHOD              format
               32  LOAD_FAST                'version'
               34  CALL_METHOD_1         1  ''
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            24  '24'

 L. 568        40  LOAD_FAST                'hinfo'
               42  UNPACK_SEQUENCE_2     2 
               44  STORE_FAST               'hlength_type'
               46  STORE_FAST               'encoding'

 L. 570        48  LOAD_GLOBAL              _read_bytes
               50  LOAD_FAST                'fp'
               52  LOAD_FAST                'struct'
               54  LOAD_METHOD              calcsize
               56  LOAD_FAST                'hlength_type'
               58  CALL_METHOD_1         1  ''
               60  LOAD_STR                 'array header length'
               62  CALL_FUNCTION_3       3  ''
               64  STORE_FAST               'hlength_str'

 L. 571        66  LOAD_FAST                'struct'
               68  LOAD_METHOD              unpack
               70  LOAD_FAST                'hlength_type'
               72  LOAD_FAST                'hlength_str'
               74  CALL_METHOD_2         2  ''
               76  LOAD_CONST               0
               78  BINARY_SUBSCR    
               80  STORE_FAST               'header_length'

 L. 572        82  LOAD_GLOBAL              _read_bytes
               84  LOAD_FAST                'fp'
               86  LOAD_FAST                'header_length'
               88  LOAD_STR                 'array header'
               90  CALL_FUNCTION_3       3  ''
               92  STORE_FAST               'header'

 L. 573        94  LOAD_FAST                'header'
               96  LOAD_METHOD              decode
               98  LOAD_FAST                'encoding'
              100  CALL_METHOD_1         1  ''
              102  STORE_FAST               'header'

 L. 581       104  LOAD_GLOBAL              _filter_header
              106  LOAD_FAST                'header'
              108  CALL_FUNCTION_1       1  ''
              110  STORE_FAST               'header'

 L. 582       112  SETUP_FINALLY       126  'to 126'

 L. 583       114  LOAD_GLOBAL              safe_eval
              116  LOAD_FAST                'header'
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'd'
              122  POP_BLOCK        
              124  JUMP_FORWARD        182  'to 182'
            126_0  COME_FROM_FINALLY   112  '112'

 L. 584       126  DUP_TOP          
              128  LOAD_GLOBAL              SyntaxError
              130  <121>               180  ''
              132  POP_TOP          
              134  STORE_FAST               'e'
              136  POP_TOP          
              138  SETUP_FINALLY       172  'to 172'

 L. 585       140  LOAD_STR                 'Cannot parse header: {!r}\nException: {!r}'
              142  STORE_FAST               'msg'

 L. 586       144  LOAD_GLOBAL              ValueError
              146  LOAD_FAST                'msg'
              148  LOAD_METHOD              format
              150  LOAD_FAST                'header'
              152  LOAD_FAST                'e'
              154  CALL_METHOD_2         2  ''
              156  CALL_FUNCTION_1       1  ''
              158  RAISE_VARARGS_1       1  'exception instance'
              160  POP_BLOCK        
              162  POP_EXCEPT       
              164  LOAD_CONST               None
              166  STORE_FAST               'e'
              168  DELETE_FAST              'e'
              170  JUMP_FORWARD        182  'to 182'
            172_0  COME_FROM_FINALLY   138  '138'
              172  LOAD_CONST               None
              174  STORE_FAST               'e'
              176  DELETE_FAST              'e'
              178  <48>             
              180  <48>             
            182_0  COME_FROM           170  '170'
            182_1  COME_FROM           124  '124'

 L. 587       182  LOAD_GLOBAL              isinstance
              184  LOAD_FAST                'd'
              186  LOAD_GLOBAL              dict
              188  CALL_FUNCTION_2       2  ''
              190  POP_JUMP_IF_TRUE    210  'to 210'

 L. 588       192  LOAD_STR                 'Header is not a dictionary: {!r}'
              194  STORE_FAST               'msg'

 L. 589       196  LOAD_GLOBAL              ValueError
              198  LOAD_FAST                'msg'
              200  LOAD_METHOD              format
              202  LOAD_FAST                'd'
              204  CALL_METHOD_1         1  ''
              206  CALL_FUNCTION_1       1  ''
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           190  '190'

 L. 590       210  LOAD_GLOBAL              sorted
              212  LOAD_FAST                'd'
              214  LOAD_METHOD              keys
              216  CALL_METHOD_0         0  ''
              218  CALL_FUNCTION_1       1  ''
              220  STORE_FAST               'keys'

 L. 591       222  LOAD_FAST                'keys'
              224  BUILD_LIST_0          0 
              226  LOAD_CONST               ('descr', 'fortran_order', 'shape')
              228  CALL_FINALLY        231  'to 231'
              230  COMPARE_OP               !=
              232  POP_JUMP_IF_FALSE   252  'to 252'

 L. 592       234  LOAD_STR                 'Header does not contain the correct keys: {!r}'
              236  STORE_FAST               'msg'

 L. 593       238  LOAD_GLOBAL              ValueError
              240  LOAD_FAST                'msg'
              242  LOAD_METHOD              format
              244  LOAD_FAST                'keys'
              246  CALL_METHOD_1         1  ''
              248  CALL_FUNCTION_1       1  ''
              250  RAISE_VARARGS_1       1  'exception instance'
            252_0  COME_FROM           232  '232'

 L. 596       252  LOAD_GLOBAL              isinstance
              254  LOAD_FAST                'd'
              256  LOAD_STR                 'shape'
              258  BINARY_SUBSCR    
              260  LOAD_GLOBAL              tuple
              262  CALL_FUNCTION_2       2  ''
          264_266  POP_JUMP_IF_FALSE   294  'to 294'

 L. 597       268  LOAD_GLOBAL              numpy
              270  LOAD_METHOD              all
              272  LOAD_LISTCOMP            '<code_object <listcomp>>'
              274  LOAD_STR                 '_read_array_header.<locals>.<listcomp>'
              276  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              278  LOAD_FAST                'd'
              280  LOAD_STR                 'shape'
              282  BINARY_SUBSCR    
              284  GET_ITER         
              286  CALL_FUNCTION_1       1  ''
              288  CALL_METHOD_1         1  ''

 L. 596   290_292  POP_JUMP_IF_TRUE    316  'to 316'
            294_0  COME_FROM           264  '264'

 L. 598       294  LOAD_STR                 'shape is not valid: {!r}'
              296  STORE_FAST               'msg'

 L. 599       298  LOAD_GLOBAL              ValueError
              300  LOAD_FAST                'msg'
              302  LOAD_METHOD              format
              304  LOAD_FAST                'd'
              306  LOAD_STR                 'shape'
              308  BINARY_SUBSCR    
              310  CALL_METHOD_1         1  ''
              312  CALL_FUNCTION_1       1  ''
              314  RAISE_VARARGS_1       1  'exception instance'
            316_0  COME_FROM           290  '290'

 L. 600       316  LOAD_GLOBAL              isinstance
              318  LOAD_FAST                'd'
              320  LOAD_STR                 'fortran_order'
              322  BINARY_SUBSCR    
              324  LOAD_GLOBAL              bool
              326  CALL_FUNCTION_2       2  ''
          328_330  POP_JUMP_IF_TRUE    354  'to 354'

 L. 601       332  LOAD_STR                 'fortran_order is not a valid bool: {!r}'
              334  STORE_FAST               'msg'

 L. 602       336  LOAD_GLOBAL              ValueError
              338  LOAD_FAST                'msg'
              340  LOAD_METHOD              format
              342  LOAD_FAST                'd'
              344  LOAD_STR                 'fortran_order'
              346  BINARY_SUBSCR    
              348  CALL_METHOD_1         1  ''
              350  CALL_FUNCTION_1       1  ''
              352  RAISE_VARARGS_1       1  'exception instance'
            354_0  COME_FROM           328  '328'

 L. 603       354  SETUP_FINALLY       372  'to 372'

 L. 604       356  LOAD_GLOBAL              descr_to_dtype
              358  LOAD_FAST                'd'
              360  LOAD_STR                 'descr'
              362  BINARY_SUBSCR    
              364  CALL_FUNCTION_1       1  ''
              366  STORE_FAST               'dtype'
              368  POP_BLOCK        
              370  JUMP_FORWARD        414  'to 414'
            372_0  COME_FROM_FINALLY   354  '354'

 L. 605       372  DUP_TOP          
              374  LOAD_GLOBAL              TypeError
          376_378  <121>               412  ''
              380  POP_TOP          
              382  POP_TOP          
              384  POP_TOP          

 L. 606       386  LOAD_STR                 'descr is not a valid dtype descriptor: {!r}'
              388  STORE_FAST               'msg'

 L. 607       390  LOAD_GLOBAL              ValueError
              392  LOAD_FAST                'msg'
              394  LOAD_METHOD              format
              396  LOAD_FAST                'd'
              398  LOAD_STR                 'descr'
              400  BINARY_SUBSCR    
              402  CALL_METHOD_1         1  ''
              404  CALL_FUNCTION_1       1  ''
              406  RAISE_VARARGS_1       1  'exception instance'
              408  POP_EXCEPT       
              410  JUMP_FORWARD        414  'to 414'
              412  <48>             
            414_0  COME_FROM           410  '410'
            414_1  COME_FROM           370  '370'

 L. 609       414  LOAD_FAST                'd'
              416  LOAD_STR                 'shape'
              418  BINARY_SUBSCR    
              420  LOAD_FAST                'd'
              422  LOAD_STR                 'fortran_order'
              424  BINARY_SUBSCR    
              426  LOAD_FAST                'dtype'
              428  BUILD_TUPLE_3         3 
              430  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 22


def write_array--- This code section failed: ---

 L. 647         0  LOAD_GLOBAL              _check_version
                2  LOAD_FAST                'version'
                4  CALL_FUNCTION_1       1  ''
                6  POP_TOP          

 L. 648         8  LOAD_GLOBAL              _write_array_header
               10  LOAD_FAST                'fp'
               12  LOAD_GLOBAL              header_data_from_array_1_0
               14  LOAD_FAST                'array'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_FAST                'version'
               20  CALL_FUNCTION_3       3  ''
               22  POP_TOP          

 L. 650        24  LOAD_FAST                'array'
               26  LOAD_ATTR                itemsize
               28  LOAD_CONST               0
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    40  'to 40'

 L. 651        34  LOAD_CONST               0
               36  STORE_FAST               'buffersize'
               38  JUMP_FORWARD         56  'to 56'
             40_0  COME_FROM            32  '32'

 L. 654        40  LOAD_GLOBAL              max
               42  LOAD_CONST               16777216
               44  LOAD_FAST                'array'
               46  LOAD_ATTR                itemsize
               48  BINARY_FLOOR_DIVIDE
               50  LOAD_CONST               1
               52  CALL_FUNCTION_2       2  ''
               54  STORE_FAST               'buffersize'
             56_0  COME_FROM            38  '38'

 L. 656        56  LOAD_FAST                'array'
               58  LOAD_ATTR                dtype
               60  LOAD_ATTR                hasobject
               62  POP_JUMP_IF_FALSE   114  'to 114'

 L. 659        64  LOAD_FAST                'allow_pickle'
               66  POP_JUMP_IF_TRUE     76  'to 76'

 L. 660        68  LOAD_GLOBAL              ValueError
               70  LOAD_STR                 'Object arrays cannot be saved when allow_pickle=False'
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            66  '66'

 L. 662        76  LOAD_FAST                'pickle_kwargs'
               78  LOAD_CONST               None
               80  <117>                 0  ''
               82  POP_JUMP_IF_FALSE    88  'to 88'

 L. 663        84  BUILD_MAP_0           0 
               86  STORE_FAST               'pickle_kwargs'
             88_0  COME_FROM            82  '82'

 L. 664        88  LOAD_GLOBAL              pickle
               90  LOAD_ATTR                dump
               92  LOAD_FAST                'array'
               94  LOAD_FAST                'fp'
               96  BUILD_TUPLE_2         2 
               98  LOAD_STR                 'protocol'
              100  LOAD_CONST               3
              102  BUILD_MAP_1           1 
              104  LOAD_FAST                'pickle_kwargs'
              106  <164>                 1  ''
              108  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              110  POP_TOP          
              112  JUMP_FORWARD        262  'to 262'
            114_0  COME_FROM            62  '62'

 L. 665       114  LOAD_FAST                'array'
              116  LOAD_ATTR                flags
              118  LOAD_ATTR                f_contiguous
              120  POP_JUMP_IF_FALSE   198  'to 198'
              122  LOAD_FAST                'array'
              124  LOAD_ATTR                flags
              126  LOAD_ATTR                c_contiguous
              128  POP_JUMP_IF_TRUE    198  'to 198'

 L. 666       130  LOAD_GLOBAL              isfileobj
              132  LOAD_FAST                'fp'
              134  CALL_FUNCTION_1       1  ''
              136  POP_JUMP_IF_FALSE   152  'to 152'

 L. 667       138  LOAD_FAST                'array'
              140  LOAD_ATTR                T
              142  LOAD_METHOD              tofile
              144  LOAD_FAST                'fp'
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          
              150  JUMP_FORWARD        196  'to 196'
            152_0  COME_FROM           136  '136'

 L. 669       152  LOAD_GLOBAL              numpy
              154  LOAD_ATTR                nditer

 L. 670       156  LOAD_FAST                'array'
              158  BUILD_LIST_0          0 
              160  LOAD_CONST               ('external_loop', 'buffered', 'zerosize_ok')
              162  CALL_FINALLY        165  'to 165'

 L. 671       164  LOAD_FAST                'buffersize'
              166  LOAD_STR                 'F'

 L. 669       168  LOAD_CONST               ('flags', 'buffersize', 'order')
              170  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              172  GET_ITER         
              174  FOR_ITER            196  'to 196'
              176  STORE_FAST               'chunk'

 L. 672       178  LOAD_FAST                'fp'
              180  LOAD_METHOD              write
              182  LOAD_FAST                'chunk'
              184  LOAD_METHOD              tobytes
              186  LOAD_STR                 'C'
              188  CALL_METHOD_1         1  ''
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          
              194  JUMP_BACK           174  'to 174'
            196_0  COME_FROM           150  '150'
              196  JUMP_FORWARD        262  'to 262'
            198_0  COME_FROM           128  '128'
            198_1  COME_FROM           120  '120'

 L. 674       198  LOAD_GLOBAL              isfileobj
              200  LOAD_FAST                'fp'
              202  CALL_FUNCTION_1       1  ''
              204  POP_JUMP_IF_FALSE   218  'to 218'

 L. 675       206  LOAD_FAST                'array'
              208  LOAD_METHOD              tofile
              210  LOAD_FAST                'fp'
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          
              216  JUMP_FORWARD        262  'to 262'
            218_0  COME_FROM           204  '204'

 L. 677       218  LOAD_GLOBAL              numpy
              220  LOAD_ATTR                nditer

 L. 678       222  LOAD_FAST                'array'
              224  BUILD_LIST_0          0 
              226  LOAD_CONST               ('external_loop', 'buffered', 'zerosize_ok')
              228  CALL_FINALLY        231  'to 231'

 L. 679       230  LOAD_FAST                'buffersize'
              232  LOAD_STR                 'C'

 L. 677       234  LOAD_CONST               ('flags', 'buffersize', 'order')
              236  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              238  GET_ITER         
              240  FOR_ITER            262  'to 262'
              242  STORE_FAST               'chunk'

 L. 680       244  LOAD_FAST                'fp'
              246  LOAD_METHOD              write
              248  LOAD_FAST                'chunk'
              250  LOAD_METHOD              tobytes
              252  LOAD_STR                 'C'
              254  CALL_METHOD_1         1  ''
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          
              260  JUMP_BACK           240  'to 240'
            262_0  COME_FROM           216  '216'
            262_1  COME_FROM           196  '196'
            262_2  COME_FROM           112  '112'

Parse error at or near `<117>' instruction at offset 80


def read_array--- This code section failed: ---

 L. 715         0  LOAD_GLOBAL              read_magic
                2  LOAD_FAST                'fp'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'version'

 L. 716         8  LOAD_GLOBAL              _check_version
               10  LOAD_FAST                'version'
               12  CALL_FUNCTION_1       1  ''
               14  POP_TOP          

 L. 717        16  LOAD_GLOBAL              _read_array_header
               18  LOAD_FAST                'fp'
               20  LOAD_FAST                'version'
               22  CALL_FUNCTION_2       2  ''
               24  UNPACK_SEQUENCE_3     3 
               26  STORE_FAST               'shape'
               28  STORE_FAST               'fortran_order'
               30  STORE_FAST               'dtype'

 L. 718        32  LOAD_GLOBAL              len
               34  LOAD_FAST                'shape'
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_CONST               0
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    50  'to 50'

 L. 719        44  LOAD_CONST               1
               46  STORE_FAST               'count'
               48  JUMP_FORWARD         68  'to 68'
             50_0  COME_FROM            42  '42'

 L. 721        50  LOAD_GLOBAL              numpy
               52  LOAD_ATTR                multiply
               54  LOAD_ATTR                reduce
               56  LOAD_FAST                'shape'
               58  LOAD_GLOBAL              numpy
               60  LOAD_ATTR                int64
               62  LOAD_CONST               ('dtype',)
               64  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               66  STORE_FAST               'count'
             68_0  COME_FROM            48  '48'

 L. 724        68  LOAD_FAST                'dtype'
               70  LOAD_ATTR                hasobject
               72  POP_JUMP_IF_FALSE   174  'to 174'

 L. 726        74  LOAD_FAST                'allow_pickle'
               76  POP_JUMP_IF_TRUE     86  'to 86'

 L. 727        78  LOAD_GLOBAL              ValueError
               80  LOAD_STR                 'Object arrays cannot be loaded when allow_pickle=False'
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            76  '76'

 L. 729        86  LOAD_FAST                'pickle_kwargs'
               88  LOAD_CONST               None
               90  <117>                 0  ''
               92  POP_JUMP_IF_FALSE    98  'to 98'

 L. 730        94  BUILD_MAP_0           0 
               96  STORE_FAST               'pickle_kwargs'
             98_0  COME_FROM            92  '92'

 L. 731        98  SETUP_FINALLY       122  'to 122'

 L. 732       100  LOAD_GLOBAL              pickle
              102  LOAD_ATTR                load
              104  LOAD_FAST                'fp'
              106  BUILD_TUPLE_1         1 
              108  BUILD_MAP_0           0 
              110  LOAD_FAST                'pickle_kwargs'
              112  <164>                 1  ''
              114  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              116  STORE_FAST               'array'
              118  POP_BLOCK        
              120  JUMP_FORWARD        172  'to 172'
            122_0  COME_FROM_FINALLY    98  '98'

 L. 733       122  DUP_TOP          
              124  LOAD_GLOBAL              UnicodeError
              126  <121>               170  ''
              128  POP_TOP          
              130  STORE_FAST               'err'
              132  POP_TOP          
              134  SETUP_FINALLY       162  'to 162'

 L. 735       136  LOAD_GLOBAL              UnicodeError
              138  LOAD_STR                 'Unpickling a python object failed: %r\nYou may need to pass the encoding= option to numpy.load'

 L. 737       140  LOAD_FAST                'err'
              142  BUILD_TUPLE_1         1 

 L. 735       144  BINARY_MODULO    
              146  CALL_FUNCTION_1       1  ''
              148  RAISE_VARARGS_1       1  'exception instance'
              150  POP_BLOCK        
              152  POP_EXCEPT       
              154  LOAD_CONST               None
              156  STORE_FAST               'err'
              158  DELETE_FAST              'err'
              160  JUMP_FORWARD        172  'to 172'
            162_0  COME_FROM_FINALLY   134  '134'
              162  LOAD_CONST               None
              164  STORE_FAST               'err'
              166  DELETE_FAST              'err'
              168  <48>             
              170  <48>             
            172_0  COME_FROM           160  '160'
            172_1  COME_FROM           120  '120'
              172  JUMP_FORWARD        366  'to 366'
            174_0  COME_FROM            72  '72'

 L. 739       174  LOAD_GLOBAL              isfileobj
              176  LOAD_FAST                'fp'
              178  CALL_FUNCTION_1       1  ''
              180  POP_JUMP_IF_FALSE   200  'to 200'

 L. 741       182  LOAD_GLOBAL              numpy
              184  LOAD_ATTR                fromfile
              186  LOAD_FAST                'fp'
              188  LOAD_FAST                'dtype'
              190  LOAD_FAST                'count'
              192  LOAD_CONST               ('dtype', 'count')
              194  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              196  STORE_FAST               'array'
              198  JUMP_FORWARD        328  'to 328'
            200_0  COME_FROM           180  '180'

 L. 754       200  LOAD_GLOBAL              numpy
              202  LOAD_ATTR                ndarray
              204  LOAD_FAST                'count'
              206  LOAD_FAST                'dtype'
              208  LOAD_CONST               ('dtype',)
              210  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              212  STORE_FAST               'array'

 L. 756       214  LOAD_FAST                'dtype'
              216  LOAD_ATTR                itemsize
              218  LOAD_CONST               0
              220  COMPARE_OP               >
          222_224  POP_JUMP_IF_FALSE   328  'to 328'

 L. 758       226  LOAD_GLOBAL              BUFFER_SIZE
              228  LOAD_GLOBAL              min
              230  LOAD_GLOBAL              BUFFER_SIZE
              232  LOAD_FAST                'dtype'
              234  LOAD_ATTR                itemsize
              236  CALL_FUNCTION_2       2  ''
              238  BINARY_FLOOR_DIVIDE
              240  STORE_FAST               'max_read_count'

 L. 760       242  LOAD_GLOBAL              range
              244  LOAD_CONST               0
              246  LOAD_FAST                'count'
              248  LOAD_FAST                'max_read_count'
              250  CALL_FUNCTION_3       3  ''
              252  GET_ITER         
              254  FOR_ITER            328  'to 328'
              256  STORE_FAST               'i'

 L. 761       258  LOAD_GLOBAL              min
              260  LOAD_FAST                'max_read_count'
              262  LOAD_FAST                'count'
              264  LOAD_FAST                'i'
              266  BINARY_SUBTRACT  
              268  CALL_FUNCTION_2       2  ''
              270  STORE_FAST               'read_count'

 L. 762       272  LOAD_GLOBAL              int
              274  LOAD_FAST                'read_count'
              276  LOAD_FAST                'dtype'
              278  LOAD_ATTR                itemsize
              280  BINARY_MULTIPLY  
              282  CALL_FUNCTION_1       1  ''
              284  STORE_FAST               'read_size'

 L. 763       286  LOAD_GLOBAL              _read_bytes
              288  LOAD_FAST                'fp'
              290  LOAD_FAST                'read_size'
              292  LOAD_STR                 'array data'
              294  CALL_FUNCTION_3       3  ''
              296  STORE_FAST               'data'

 L. 764       298  LOAD_GLOBAL              numpy
              300  LOAD_ATTR                frombuffer
              302  LOAD_FAST                'data'
              304  LOAD_FAST                'dtype'

 L. 765       306  LOAD_FAST                'read_count'

 L. 764       308  LOAD_CONST               ('dtype', 'count')
              310  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              312  LOAD_FAST                'array'
              314  LOAD_FAST                'i'
              316  LOAD_FAST                'i'
              318  LOAD_FAST                'read_count'
              320  BINARY_ADD       
              322  BUILD_SLICE_2         2 
              324  STORE_SUBSCR     
              326  JUMP_BACK           254  'to 254'
            328_0  COME_FROM           222  '222'
            328_1  COME_FROM           198  '198'

 L. 767       328  LOAD_FAST                'fortran_order'
          330_332  POP_JUMP_IF_FALSE   360  'to 360'

 L. 768       334  LOAD_FAST                'shape'
              336  LOAD_CONST               None
              338  LOAD_CONST               None
              340  LOAD_CONST               -1
              342  BUILD_SLICE_3         3 
              344  BINARY_SUBSCR    
              346  LOAD_FAST                'array'
              348  STORE_ATTR               shape

 L. 769       350  LOAD_FAST                'array'
              352  LOAD_METHOD              transpose
              354  CALL_METHOD_0         0  ''
              356  STORE_FAST               'array'
              358  JUMP_FORWARD        366  'to 366'
            360_0  COME_FROM           330  '330'

 L. 771       360  LOAD_FAST                'shape'
              362  LOAD_FAST                'array'
              364  STORE_ATTR               shape
            366_0  COME_FROM           358  '358'
            366_1  COME_FROM           172  '172'

 L. 773       366  LOAD_FAST                'array'
              368  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 90


def open_memmap--- This code section failed: ---

 L. 826         0  LOAD_GLOBAL              isfileobj
                2  LOAD_FAST                'filename'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 827         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Filename must be a string or a path-like object.  Memmap cannot use existing file handles.'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 830        16  LOAD_STR                 'w'
               18  LOAD_FAST                'mode'
               20  <118>                 0  ''
               22  POP_JUMP_IF_FALSE   150  'to 150'

 L. 833        24  LOAD_GLOBAL              _check_version
               26  LOAD_FAST                'version'
               28  CALL_FUNCTION_1       1  ''
               30  POP_TOP          

 L. 836        32  LOAD_GLOBAL              numpy
               34  LOAD_METHOD              dtype
               36  LOAD_FAST                'dtype'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'dtype'

 L. 837        42  LOAD_FAST                'dtype'
               44  LOAD_ATTR                hasobject
               46  POP_JUMP_IF_FALSE    60  'to 60'

 L. 838        48  LOAD_STR                 "Array can't be memory-mapped: Python objects in dtype."
               50  STORE_FAST               'msg'

 L. 839        52  LOAD_GLOBAL              ValueError
               54  LOAD_FAST                'msg'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            46  '46'

 L. 840        60  LOAD_GLOBAL              dict

 L. 841        62  LOAD_GLOBAL              dtype_to_descr
               64  LOAD_FAST                'dtype'
               66  CALL_FUNCTION_1       1  ''

 L. 842        68  LOAD_FAST                'fortran_order'

 L. 843        70  LOAD_FAST                'shape'

 L. 840        72  LOAD_CONST               ('descr', 'fortran_order', 'shape')
               74  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               76  STORE_FAST               'd'

 L. 846        78  LOAD_GLOBAL              open
               80  LOAD_GLOBAL              os_fspath
               82  LOAD_FAST                'filename'
               84  CALL_FUNCTION_1       1  ''
               86  LOAD_FAST                'mode'
               88  LOAD_STR                 'b'
               90  BINARY_ADD       
               92  CALL_FUNCTION_2       2  ''
               94  SETUP_WITH          132  'to 132'
               96  STORE_FAST               'fp'

 L. 847        98  LOAD_GLOBAL              _write_array_header
              100  LOAD_FAST                'fp'
              102  LOAD_FAST                'd'
              104  LOAD_FAST                'version'
              106  CALL_FUNCTION_3       3  ''
              108  POP_TOP          

 L. 848       110  LOAD_FAST                'fp'
              112  LOAD_METHOD              tell
              114  CALL_METHOD_0         0  ''
              116  STORE_FAST               'offset'
              118  POP_BLOCK        
              120  LOAD_CONST               None
              122  DUP_TOP          
              124  DUP_TOP          
              126  CALL_FUNCTION_3       3  ''
              128  POP_TOP          
              130  JUMP_ABSOLUTE       254  'to 254'
            132_0  COME_FROM_WITH       94  '94'
              132  <49>             
              134  POP_JUMP_IF_TRUE    138  'to 138'
              136  <48>             
            138_0  COME_FROM           134  '134'
              138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          
              144  POP_EXCEPT       
              146  POP_TOP          
              148  JUMP_FORWARD        254  'to 254'
            150_0  COME_FROM            22  '22'

 L. 851       150  LOAD_GLOBAL              open
              152  LOAD_GLOBAL              os_fspath
              154  LOAD_FAST                'filename'
              156  CALL_FUNCTION_1       1  ''
              158  LOAD_STR                 'rb'
              160  CALL_FUNCTION_2       2  ''
              162  SETUP_WITH          238  'to 238'
              164  STORE_FAST               'fp'

 L. 852       166  LOAD_GLOBAL              read_magic
              168  LOAD_FAST                'fp'
              170  CALL_FUNCTION_1       1  ''
              172  STORE_FAST               'version'

 L. 853       174  LOAD_GLOBAL              _check_version
              176  LOAD_FAST                'version'
              178  CALL_FUNCTION_1       1  ''
              180  POP_TOP          

 L. 855       182  LOAD_GLOBAL              _read_array_header
              184  LOAD_FAST                'fp'
              186  LOAD_FAST                'version'
              188  CALL_FUNCTION_2       2  ''
              190  UNPACK_SEQUENCE_3     3 
              192  STORE_FAST               'shape'
              194  STORE_FAST               'fortran_order'
              196  STORE_FAST               'dtype'

 L. 856       198  LOAD_FAST                'dtype'
              200  LOAD_ATTR                hasobject
              202  POP_JUMP_IF_FALSE   216  'to 216'

 L. 857       204  LOAD_STR                 "Array can't be memory-mapped: Python objects in dtype."
              206  STORE_FAST               'msg'

 L. 858       208  LOAD_GLOBAL              ValueError
              210  LOAD_FAST                'msg'
              212  CALL_FUNCTION_1       1  ''
              214  RAISE_VARARGS_1       1  'exception instance'
            216_0  COME_FROM           202  '202'

 L. 859       216  LOAD_FAST                'fp'
              218  LOAD_METHOD              tell
              220  CALL_METHOD_0         0  ''
              222  STORE_FAST               'offset'
              224  POP_BLOCK        
              226  LOAD_CONST               None
              228  DUP_TOP          
              230  DUP_TOP          
              232  CALL_FUNCTION_3       3  ''
              234  POP_TOP          
              236  JUMP_FORWARD        254  'to 254'
            238_0  COME_FROM_WITH      162  '162'
              238  <49>             
              240  POP_JUMP_IF_TRUE    244  'to 244'
              242  <48>             
            244_0  COME_FROM           240  '240'
              244  POP_TOP          
              246  POP_TOP          
              248  POP_TOP          
              250  POP_EXCEPT       
              252  POP_TOP          
            254_0  COME_FROM           236  '236'
            254_1  COME_FROM           148  '148'

 L. 861       254  LOAD_FAST                'fortran_order'
          256_258  POP_JUMP_IF_FALSE   266  'to 266'

 L. 862       260  LOAD_STR                 'F'
              262  STORE_FAST               'order'
              264  JUMP_FORWARD        270  'to 270'
            266_0  COME_FROM           256  '256'

 L. 864       266  LOAD_STR                 'C'
              268  STORE_FAST               'order'
            270_0  COME_FROM           264  '264'

 L. 868       270  LOAD_FAST                'mode'
              272  LOAD_STR                 'w+'
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_FALSE   284  'to 284'

 L. 869       280  LOAD_STR                 'r+'
              282  STORE_FAST               'mode'
            284_0  COME_FROM           276  '276'

 L. 871       284  LOAD_GLOBAL              numpy
              286  LOAD_ATTR                memmap
              288  LOAD_FAST                'filename'
              290  LOAD_FAST                'dtype'
              292  LOAD_FAST                'shape'
              294  LOAD_FAST                'order'

 L. 872       296  LOAD_FAST                'mode'
              298  LOAD_FAST                'offset'

 L. 871       300  LOAD_CONST               ('dtype', 'shape', 'order', 'mode', 'offset')
              302  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              304  STORE_FAST               'marray'

 L. 874       306  LOAD_FAST                'marray'
              308  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 20


def _read_bytes--- This code section failed: ---

 L. 886         0  LOAD_GLOBAL              bytes
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'data'

 L. 891         6  SETUP_FINALLY        66  'to 66'

 L. 892         8  LOAD_FAST                'fp'
               10  LOAD_METHOD              read
               12  LOAD_FAST                'size'
               14  LOAD_GLOBAL              len
               16  LOAD_FAST                'data'
               18  CALL_FUNCTION_1       1  ''
               20  BINARY_SUBTRACT  
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'r'

 L. 893        26  LOAD_FAST                'data'
               28  LOAD_FAST                'r'
               30  INPLACE_ADD      
               32  STORE_FAST               'data'

 L. 894        34  LOAD_GLOBAL              len
               36  LOAD_FAST                'r'
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_CONST               0
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_TRUE     58  'to 58'
               46  LOAD_GLOBAL              len
               48  LOAD_FAST                'data'
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_FAST                'size'
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE    62  'to 62'
             58_0  COME_FROM            44  '44'

 L. 895        58  POP_BLOCK        
               60  BREAK_LOOP           88  'to 88'
             62_0  COME_FROM            56  '56'
               62  POP_BLOCK        
               64  JUMP_BACK             6  'to 6'
             66_0  COME_FROM_FINALLY     6  '6'

 L. 896        66  DUP_TOP          
               68  LOAD_GLOBAL              io
               70  LOAD_ATTR                BlockingIOError
               72  <121>                84  ''
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L. 897        80  POP_EXCEPT       
               82  JUMP_BACK             6  'to 6'
               84  <48>             
               86  JUMP_BACK             6  'to 6'

 L. 898        88  LOAD_GLOBAL              len
               90  LOAD_FAST                'data'
               92  CALL_FUNCTION_1       1  ''
               94  LOAD_FAST                'size'
               96  COMPARE_OP               !=
               98  POP_JUMP_IF_FALSE   128  'to 128'

 L. 899       100  LOAD_STR                 'EOF: reading %s, expected %d bytes got %d'
              102  STORE_FAST               'msg'

 L. 900       104  LOAD_GLOBAL              ValueError
              106  LOAD_FAST                'msg'
              108  LOAD_FAST                'error_template'
              110  LOAD_FAST                'size'
              112  LOAD_GLOBAL              len
              114  LOAD_FAST                'data'
              116  CALL_FUNCTION_1       1  ''
              118  BUILD_TUPLE_3         3 
              120  BINARY_MODULO    
              122  CALL_FUNCTION_1       1  ''
              124  RAISE_VARARGS_1       1  'exception instance'
              126  JUMP_FORWARD        132  'to 132'
            128_0  COME_FROM            98  '98'

 L. 902       128  LOAD_FAST                'data'
              130  RETURN_VALUE     
            132_0  COME_FROM           126  '126'

Parse error at or near `<121>' instruction at offset 72