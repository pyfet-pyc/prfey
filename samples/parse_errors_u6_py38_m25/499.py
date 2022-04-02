# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: multiprocessing\shared_memory.py
"""Provides shared memory for direct access across processes.

The API of this package is currently provisional. Refer to the
documentation for details.
"""
__all__ = [
 'SharedMemory', 'ShareableList']
from functools import partial
import mmap, os, errno, struct, secrets
if os.name == 'nt':
    import _winapi
    _USE_POSIX = False
else:
    import _posixshmem
    _USE_POSIX = True
_O_CREX = os.O_CREAT | os.O_EXCL
_SHM_SAFE_NAME_LENGTH = 14
if _USE_POSIX:
    _SHM_NAME_PREFIX = '/psm_'
else:
    _SHM_NAME_PREFIX = 'wnsm_'

def _make_filename():
    """Create a random filename for the shared memory object."""
    nbytes = (_SHM_SAFE_NAME_LENGTH - len(_SHM_NAME_PREFIX)) // 2
    assert nbytes >= 2, '_SHM_NAME_PREFIX too long'
    name = _SHM_NAME_PREFIX + secrets.token_hex(nbytes)
    assert len(name) <= _SHM_SAFE_NAME_LENGTH
    return name


class SharedMemory:
    __doc__ = 'Creates a new shared memory block or attaches to an existing\n    shared memory block.\n\n    Every shared memory block is assigned a unique name.  This enables\n    one process to create a shared memory block with a particular name\n    so that a different process can attach to that same shared memory\n    block using that same name.\n\n    As a resource for sharing data across processes, shared memory blocks\n    may outlive the original process that created them.  When one process\n    no longer needs access to a shared memory block that might still be\n    needed by other processes, the close() method should be called.\n    When a shared memory block is no longer needed by any process, the\n    unlink() method should be called to ensure proper cleanup.'
    _name = None
    _fd = -1
    _mmap = None
    _buf = None
    _flags = os.O_RDWR
    _mode = 384
    _prepend_leading_slash = True if _USE_POSIX else False

    def __init__--- This code section failed: ---

 L.  74         0  LOAD_FAST                'size'
                2  LOAD_CONST               0
                4  COMPARE_OP               >=
                6  POP_JUMP_IF_TRUE     16  'to 16'

 L.  75         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 "'size' must be a positive integer"
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  76        16  LOAD_FAST                'create'
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L.  77        20  LOAD_GLOBAL              _O_CREX
               22  LOAD_GLOBAL              os
               24  LOAD_ATTR                O_RDWR
               26  BINARY_OR        
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _flags
             32_0  COME_FROM            18  '18'

 L.  78        32  LOAD_FAST                'name'
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  POP_JUMP_IF_FALSE    60  'to 60'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _flags
               44  LOAD_GLOBAL              os
               46  LOAD_ATTR                O_EXCL
               48  BINARY_AND       
               50  POP_JUMP_IF_TRUE     60  'to 60'

 L.  79        52  LOAD_GLOBAL              ValueError
               54  LOAD_STR                 "'name' can only be None if create=True"
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'
             60_1  COME_FROM            38  '38'

 L.  81        60  LOAD_GLOBAL              _USE_POSIX
            62_64  POP_JUMP_IF_FALSE   312  'to 312'

 L.  85        66  LOAD_FAST                'name'
               68  LOAD_CONST               None
               70  COMPARE_OP               is
               72  POP_JUMP_IF_FALSE   144  'to 144'

 L.  87        74  LOAD_GLOBAL              _make_filename
               76  CALL_FUNCTION_0       0  ''
               78  STORE_FAST               'name'

 L.  88        80  SETUP_FINALLY       108  'to 108'

 L.  89        82  LOAD_GLOBAL              _posixshmem
               84  LOAD_ATTR                shm_open

 L.  90        86  LOAD_FAST                'name'

 L.  91        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _flags

 L.  92        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _mode

 L.  89        96  LOAD_CONST               ('mode',)
               98  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              100  LOAD_FAST                'self'
              102  STORE_ATTR               _fd
              104  POP_BLOCK        
              106  JUMP_FORWARD        132  'to 132'
            108_0  COME_FROM_FINALLY    80  '80'

 L.  94       108  DUP_TOP          
              110  LOAD_GLOBAL              FileExistsError
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   130  'to 130'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L.  95       122  POP_EXCEPT       
              124  JUMP_BACK            74  'to 74'
              126  POP_EXCEPT       
              128  JUMP_FORWARD        132  'to 132'
            130_0  COME_FROM           114  '114'
              130  END_FINALLY      
            132_0  COME_FROM           128  '128'
            132_1  COME_FROM           106  '106'

 L.  96       132  LOAD_FAST                'name'
              134  LOAD_FAST                'self'
              136  STORE_ATTR               _name

 L.  97       138  BREAK_LOOP          190  'to 190'
              140  JUMP_BACK            74  'to 74'
              142  JUMP_FORWARD        190  'to 190'
            144_0  COME_FROM            72  '72'

 L.  99       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _prepend_leading_slash
              148  POP_JUMP_IF_FALSE   158  'to 158'
              150  LOAD_STR                 '/'
              152  LOAD_FAST                'name'
              154  BINARY_ADD       
              156  JUMP_FORWARD        160  'to 160'
            158_0  COME_FROM           148  '148'
              158  LOAD_FAST                'name'
            160_0  COME_FROM           156  '156'
              160  STORE_FAST               'name'

 L. 100       162  LOAD_GLOBAL              _posixshmem
              164  LOAD_ATTR                shm_open

 L. 101       166  LOAD_FAST                'name'

 L. 102       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _flags

 L. 103       172  LOAD_FAST                'self'
              174  LOAD_ATTR                _mode

 L. 100       176  LOAD_CONST               ('mode',)
              178  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              180  LOAD_FAST                'self'
              182  STORE_ATTR               _fd

 L. 105       184  LOAD_FAST                'name'
              186  LOAD_FAST                'self'
              188  STORE_ATTR               _name
            190_0  COME_FROM           142  '142'

 L. 106       190  SETUP_FINALLY       252  'to 252'

 L. 107       192  LOAD_FAST                'create'
              194  POP_JUMP_IF_FALSE   214  'to 214'
              196  LOAD_FAST                'size'
              198  POP_JUMP_IF_FALSE   214  'to 214'

 L. 108       200  LOAD_GLOBAL              os
              202  LOAD_METHOD              ftruncate
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                _fd
              208  LOAD_FAST                'size'
              210  CALL_METHOD_2         2  ''
              212  POP_TOP          
            214_0  COME_FROM           198  '198'
            214_1  COME_FROM           194  '194'

 L. 109       214  LOAD_GLOBAL              os
              216  LOAD_METHOD              fstat
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                _fd
              222  CALL_METHOD_1         1  ''
              224  STORE_FAST               'stats'

 L. 110       226  LOAD_FAST                'stats'
              228  LOAD_ATTR                st_size
              230  STORE_FAST               'size'

 L. 111       232  LOAD_GLOBAL              mmap
              234  LOAD_METHOD              mmap
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                _fd
              240  LOAD_FAST                'size'
              242  CALL_METHOD_2         2  ''
              244  LOAD_FAST                'self'
              246  STORE_ATTR               _mmap
              248  POP_BLOCK        
              250  JUMP_FORWARD        284  'to 284'
            252_0  COME_FROM_FINALLY   190  '190'

 L. 112       252  DUP_TOP          
              254  LOAD_GLOBAL              OSError
              256  COMPARE_OP               exception-match
          258_260  POP_JUMP_IF_FALSE   282  'to 282'
              262  POP_TOP          
              264  POP_TOP          
              266  POP_TOP          

 L. 113       268  LOAD_FAST                'self'
              270  LOAD_METHOD              unlink
              272  CALL_METHOD_0         0  ''
              274  POP_TOP          

 L. 114       276  RAISE_VARARGS_0       0  'reraise'
              278  POP_EXCEPT       
              280  JUMP_FORWARD        284  'to 284'
            282_0  COME_FROM           258  '258'
              282  END_FINALLY      
            284_0  COME_FROM           280  '280'
            284_1  COME_FROM           250  '250'

 L. 116       284  LOAD_CONST               1
              286  LOAD_CONST               ('register',)
              288  IMPORT_NAME              resource_tracker
              290  IMPORT_FROM              register
              292  STORE_FAST               'register'
              294  POP_TOP          

 L. 117       296  LOAD_FAST                'register'
              298  LOAD_FAST                'self'
              300  LOAD_ATTR                _name
              302  LOAD_STR                 'shared_memory'
              304  CALL_FUNCTION_2       2  ''
              306  POP_TOP          
          308_310  JUMP_FORWARD        582  'to 582'
            312_0  COME_FROM            62  '62'

 L. 123       312  LOAD_FAST                'create'
          314_316  POP_JUMP_IF_FALSE   494  'to 494'

 L. 125       318  LOAD_FAST                'name'
              320  LOAD_CONST               None
              322  COMPARE_OP               is
          324_326  POP_JUMP_IF_FALSE   334  'to 334'
              328  LOAD_GLOBAL              _make_filename
              330  CALL_FUNCTION_0       0  ''
              332  JUMP_FORWARD        336  'to 336'
            334_0  COME_FROM           324  '324'
              334  LOAD_FAST                'name'
            336_0  COME_FROM           332  '332'
              336  STORE_FAST               'temp_name'

 L. 128       338  LOAD_GLOBAL              _winapi
              340  LOAD_METHOD              CreateFileMapping

 L. 129       342  LOAD_GLOBAL              _winapi
              344  LOAD_ATTR                INVALID_HANDLE_VALUE

 L. 130       346  LOAD_GLOBAL              _winapi
              348  LOAD_ATTR                NULL

 L. 131       350  LOAD_GLOBAL              _winapi
              352  LOAD_ATTR                PAGE_READWRITE

 L. 132       354  LOAD_FAST                'size'
              356  LOAD_CONST               32
              358  BINARY_RSHIFT    
              360  LOAD_CONST               4294967295
              362  BINARY_AND       

 L. 133       364  LOAD_FAST                'size'
              366  LOAD_CONST               4294967295
              368  BINARY_AND       

 L. 134       370  LOAD_FAST                'temp_name'

 L. 128       372  CALL_METHOD_6         6  ''
              374  STORE_FAST               'h_map'

 L. 136       376  SETUP_FINALLY       466  'to 466'

 L. 137       378  LOAD_GLOBAL              _winapi
              380  LOAD_METHOD              GetLastError
              382  CALL_METHOD_0         0  ''
              384  STORE_FAST               'last_error_code'

 L. 138       386  LOAD_FAST                'last_error_code'
              388  LOAD_GLOBAL              _winapi
              390  LOAD_ATTR                ERROR_ALREADY_EXISTS
              392  COMPARE_OP               ==
          394_396  POP_JUMP_IF_FALSE   444  'to 444'

 L. 139       398  LOAD_FAST                'name'
              400  LOAD_CONST               None
              402  COMPARE_OP               is-not
          404_406  POP_JUMP_IF_FALSE   436  'to 436'

 L. 140       408  LOAD_GLOBAL              FileExistsError

 L. 141       410  LOAD_GLOBAL              errno
              412  LOAD_ATTR                EEXIST

 L. 142       414  LOAD_GLOBAL              os
              416  LOAD_METHOD              strerror
              418  LOAD_GLOBAL              errno
              420  LOAD_ATTR                EEXIST
              422  CALL_METHOD_1         1  ''

 L. 143       424  LOAD_FAST                'name'

 L. 144       426  LOAD_GLOBAL              _winapi
              428  LOAD_ATTR                ERROR_ALREADY_EXISTS

 L. 140       430  CALL_FUNCTION_4       4  ''
              432  RAISE_VARARGS_1       1  'exception instance'
              434  JUMP_FORWARD        444  'to 444'
            436_0  COME_FROM           404  '404'

 L. 147       436  POP_BLOCK        
              438  CALL_FINALLY        466  'to 466'
          440_442  JUMP_BACK           318  'to 318'
            444_0  COME_FROM           434  '434'
            444_1  COME_FROM           394  '394'

 L. 148       444  LOAD_GLOBAL              mmap
              446  LOAD_ATTR                mmap
              448  LOAD_CONST               -1
              450  LOAD_FAST                'size'
              452  LOAD_FAST                'temp_name'
              454  LOAD_CONST               ('tagname',)
              456  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              458  LOAD_FAST                'self'
              460  STORE_ATTR               _mmap
              462  POP_BLOCK        
              464  BEGIN_FINALLY    
            466_0  COME_FROM           438  '438'
            466_1  COME_FROM_FINALLY   376  '376'

 L. 150       466  LOAD_GLOBAL              _winapi
              468  LOAD_METHOD              CloseHandle
              470  LOAD_FAST                'h_map'
              472  CALL_METHOD_1         1  ''
              474  POP_TOP          
              476  END_FINALLY      

 L. 151       478  LOAD_FAST                'temp_name'
              480  LOAD_FAST                'self'
              482  STORE_ATTR               _name

 L. 152   484_486  BREAK_LOOP          582  'to 582'
          488_490  JUMP_BACK           318  'to 318'
              492  JUMP_FORWARD        582  'to 582'
            494_0  COME_FROM           314  '314'

 L. 155       494  LOAD_FAST                'name'
              496  LOAD_FAST                'self'
              498  STORE_ATTR               _name

 L. 158       500  LOAD_GLOBAL              _winapi
              502  LOAD_METHOD              OpenFileMapping

 L. 159       504  LOAD_GLOBAL              _winapi
              506  LOAD_ATTR                FILE_MAP_READ

 L. 160       508  LOAD_CONST               False

 L. 161       510  LOAD_FAST                'name'

 L. 158       512  CALL_METHOD_3         3  ''
              514  STORE_FAST               'h_map'

 L. 163       516  SETUP_FINALLY       542  'to 542'

 L. 164       518  LOAD_GLOBAL              _winapi
              520  LOAD_METHOD              MapViewOfFile

 L. 165       522  LOAD_FAST                'h_map'

 L. 166       524  LOAD_GLOBAL              _winapi
              526  LOAD_ATTR                FILE_MAP_READ

 L. 167       528  LOAD_CONST               0

 L. 168       530  LOAD_CONST               0

 L. 169       532  LOAD_CONST               0

 L. 164       534  CALL_METHOD_5         5  ''
              536  STORE_FAST               'p_buf'
              538  POP_BLOCK        
              540  BEGIN_FINALLY    
            542_0  COME_FROM_FINALLY   516  '516'

 L. 172       542  LOAD_GLOBAL              _winapi
              544  LOAD_METHOD              CloseHandle
              546  LOAD_FAST                'h_map'
              548  CALL_METHOD_1         1  ''
              550  POP_TOP          
              552  END_FINALLY      

 L. 173       554  LOAD_GLOBAL              _winapi
              556  LOAD_METHOD              VirtualQuerySize
              558  LOAD_FAST                'p_buf'
              560  CALL_METHOD_1         1  ''
              562  STORE_FAST               'size'

 L. 174       564  LOAD_GLOBAL              mmap
              566  LOAD_ATTR                mmap
              568  LOAD_CONST               -1
              570  LOAD_FAST                'size'
              572  LOAD_FAST                'name'
              574  LOAD_CONST               ('tagname',)
              576  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              578  LOAD_FAST                'self'
              580  STORE_ATTR               _mmap
            582_0  COME_FROM           492  '492'
            582_1  COME_FROM           308  '308'

 L. 176       582  LOAD_FAST                'size'
              584  LOAD_FAST                'self'
              586  STORE_ATTR               _size

 L. 177       588  LOAD_GLOBAL              memoryview
              590  LOAD_FAST                'self'
              592  LOAD_ATTR                _mmap
              594  CALL_FUNCTION_1       1  ''
              596  LOAD_FAST                'self'
              598  STORE_ATTR               _buf

Parse error at or near `POP_EXCEPT' instruction at offset 126

    def __del__(self):
        try:
            self.close
        except OSError:
            pass

    def __reduce__(self):
        return (
         self.__class__,
         (
          self.name,
          False,
          self.size))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, size={self.size})"

    @property
    def buf(self):
        """A memoryview of contents of the shared memory block."""
        return self._buf

    @property
    def name(self):
        """Unique name that identifies the shared memory block."""
        reported_name = self._name
        if _USE_POSIX:
            if self._prepend_leading_slash:
                if self._name.startswith('/'):
                    reported_name = self._name[1:]
        return reported_name

    @property
    def size(self):
        """Size in bytes."""
        return self._size

    def close(self):
        """Closes access to the shared memory from this instance but does
        not destroy the shared memory block."""
        if self._buf is not None:
            self._buf.release
            self._buf = None
        else:
            if self._mmap is not None:
                self._mmap.close
                self._mmap = None
            if _USE_POSIX and self._fd >= 0:
                os.close(self._fd)
                self._fd = -1

    def unlink(self):
        """Requests that the underlying shared memory block be destroyed.

        In order to ensure proper cleanup of resources, unlink should be
        called once (and only once) across all processes which have access
        to the shared memory block."""
        if _USE_POSIX:
            if self._name:
                from .resource_tracker import unregister
                _posixshmem.shm_unlink(self._name)
                unregister(self._name, 'shared_memory')


_encoding = 'utf8'

class ShareableList:
    __doc__ = 'Pattern for a mutable list-like object shareable via a shared\n    memory block.  It differs from the built-in list type in that these\n    lists can not change their overall length (i.e. no append, insert,\n    etc.)\n\n    Because values are packed into a memoryview as bytes, the struct\n    packing format for any storable value must require no more than 8\n    characters to describe its format.'
    _types_mapping = {int: 'q', 
     float: 'd', 
     bool: 'xxxxxxx?', 
     str: '%ds', 
     bytes: '%ds', 
     (None).__class__: 'xxxxxx?x'}
    _alignment = 8
    _back_transforms_mapping = {0:lambda value: value, 
     1:lambda value: value.rstrip(b'\x00').decode(_encoding), 
     2:lambda value: value.rstrip(b'\x00'), 
     3:lambda _value: None}

    @staticmethod
    def _extract_recreation_code(value):
        """Used in concert with _back_transforms_mapping to convert values
        into the appropriate Python objects when retrieving them from
        the list as well as when storing them."""
        if not isinstance(value, (str, bytes, (None).__class__)):
            return 0
        if isinstance(value, str):
            return 1
        if isinstance(value, bytes):
            return 2
        return 3

    def __init__(self, sequence=None, *, name=None):
        if sequence is not None:
            _formats = [self._types_mapping[type(item)] if not isinstance(item, (str, bytes)) else self._types_mapping[type(item)] % (
             self._alignment * (len(item) // self._alignment + 1),) for item in sequence]
            self._list_len = len(_formats)
            assert sum((len(fmt) <= 8 for fmt in _formats)) == self._list_len
            self._allocated_bytes = tuple(((self._alignment if fmt[(-1)] != 's' else int(fmt[:-1])) for fmt in _formats))
            _recreation_codes = [self._extract_recreation_code(item) for item in sequence]
            requested_size = struct.calcsize('q' + self._format_size_metainfo + ''.join(_formats) + self._format_packing_metainfo + self._format_back_transform_codes)
        else:
            requested_size = 8
        if name is not None:
            if sequence is None:
                self.shm = SharedMemory(name)
            else:
                self.shm = SharedMemory(name, create=True, size=requested_size)
        elif sequence is not None:
            _enc = _encoding
            (struct.pack_into)('q' + self._format_size_metainfo, self.shm.buf, 0, self._list_len, *self._allocated_bytes)
            (struct.pack_into)(''.join(_formats), self.shm.buf, self._offset_data_start, *((v.encode(_enc) if isinstance(v, str) else v) for v in sequence))
            (struct.pack_into)(self._format_packing_metainfo, self.shm.buf, self._offset_packing_formats, *(v.encode(_enc) for v in _formats))
            (struct.pack_into)(self._format_back_transform_codes, self.shm.buf, self._offset_back_transform_codes, *_recreation_codes)
        else:
            self._list_len = len(self)
            self._allocated_bytes = struct.unpack_fromself._format_size_metainfoself.shm.buf8

    def _get_packing_format(self, position):
        """Gets the packing format for a single value stored in the list."""
        position = position if position >= 0 else position + self._list_len
        if position >= self._list_len or self._list_len < 0:
            raise IndexError('Requested position out of range.')
        v = struct.unpack_from'8s'self.shm.buf(self._offset_packing_formats + position * 8)[0]
        fmt = v.rstrip(b'\x00')
        fmt_as_str = fmt.decode(_encoding)
        return fmt_as_str

    def _get_back_transform(self, position):
        """Gets the back transformation function for a single value."""
        position = position if position >= 0 else position + self._list_len
        if position >= self._list_len or self._list_len < 0:
            raise IndexError('Requested position out of range.')
        transform_code = struct.unpack_from'b'self.shm.buf(self._offset_back_transform_codes + position)[0]
        transform_function = self._back_transforms_mapping[transform_code]
        return transform_function

    def _set_packing_format_and_transform(self, position, fmt_as_str, value):
        """Sets the packing format and back transformation code for a
        single value in the list at the specified position."""
        position = position if position >= 0 else position + self._list_len
        if position >= self._list_len or self._list_len < 0:
            raise IndexError('Requested position out of range.')
        struct.pack_into('8s', self.shm.buf, self._offset_packing_formats + position * 8, fmt_as_str.encode(_encoding))
        transform_code = self._extract_recreation_code(value)
        struct.pack_into('b', self.shm.buf, self._offset_back_transform_codes + position, transform_code)

    def __getitem__(self, position):
        try:
            offset = self._offset_data_start + sum(self._allocated_bytes[:position])
            v, = struct.unpack_fromself._get_packing_format(position)self.shm.bufoffset
        except IndexError:
            raise IndexError('index out of range')
        else:
            back_transform = self._get_back_transform(position)
            v = back_transform(v)
            return v

    def __setitem__(self, position, value):
        try:
            offset = self._offset_data_start + sum(self._allocated_bytes[:position])
            current_format = self._get_packing_format(position)
        except IndexError:
            raise IndexError('assignment index out of range')
        else:
            if not isinstance(value, (str, bytes)):
                new_format = self._types_mapping[type(value)]
            else:
                if len(value) > self._allocated_bytes[position]:
                    raise ValueError('exceeds available storage for existing str')
                elif current_format[(-1)] == 's':
                    new_format = current_format
                else:
                    new_format = self._types_mapping[str] % (
                     self._allocated_bytes[position],)
            self._set_packing_format_and_transformpositionnew_formatvalue
            value = value.encode(_encoding) if isinstance(value, str) else value
            struct.pack_into(new_format, self.shm.buf, offset, value)

    def __reduce__(self):
        return (partial((self.__class__), name=(self.shm.name)), ())

    def __len__(self):
        return struct.unpack_from'q'self.shm.buf0[0]

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self)}, name={self.shm.name!r})"

    @property
    def format(self):
        """The struct packing format used by all currently stored values."""
        return ''.join((self._get_packing_format(i) for i in range(self._list_len)))

    @property
    def _format_size_metainfo(self):
        """The struct packing format used for metainfo on storage sizes."""
        return f"{self._list_len}q"

    @property
    def _format_packing_metainfo(self):
        """The struct packing format used for the values' packing formats."""
        return '8s' * self._list_len

    @property
    def _format_back_transform_codes(self):
        """The struct packing format used for the values' back transforms."""
        return 'b' * self._list_len

    @property
    def _offset_data_start(self):
        return (self._list_len + 1) * 8

    @property
    def _offset_packing_formats(self):
        return self._offset_data_start + sum(self._allocated_bytes)

    @property
    def _offset_back_transform_codes(self):
        return self._offset_packing_formats + self._list_len * 8

    def count(self, value):
        """L.count(value) -> integer -- return number of occurrences of value."""
        return sum((value == entry for entry in self))

    def index(self, value):
        """L.index(value) -> integer -- return first index of value.
        Raises ValueError if the value is not present."""
        for position, entry in enumerate(self):
            if value == entry:
                return position
        else:
            raise ValueError(f"{value!r} not in this container")