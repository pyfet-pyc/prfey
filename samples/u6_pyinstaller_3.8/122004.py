# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
               18  POP_JUMP_IF_FALSE    48  'to 48'

 L.  77        20  LOAD_GLOBAL              _O_CREX
               22  LOAD_GLOBAL              os
               24  LOAD_ATTR                O_RDWR
               26  BINARY_OR        
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _flags

 L.  78        32  LOAD_FAST                'size'
               34  LOAD_CONST               0
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L.  79        40  LOAD_GLOBAL              ValueError
               42  LOAD_STR                 "'size' must be a positive number different from zero"
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'
             48_1  COME_FROM            18  '18'

 L.  80        48  LOAD_FAST                'name'
               50  LOAD_CONST               None
               52  COMPARE_OP               is
               54  POP_JUMP_IF_FALSE    76  'to 76'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _flags
               60  LOAD_GLOBAL              os
               62  LOAD_ATTR                O_EXCL
               64  BINARY_AND       
               66  POP_JUMP_IF_TRUE     76  'to 76'

 L.  81        68  LOAD_GLOBAL              ValueError
               70  LOAD_STR                 "'name' can only be None if create=True"
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            66  '66'
             76_1  COME_FROM            54  '54'

 L.  83        76  LOAD_GLOBAL              _USE_POSIX
            78_80  POP_JUMP_IF_FALSE   328  'to 328'

 L.  87        82  LOAD_FAST                'name'
               84  LOAD_CONST               None
               86  COMPARE_OP               is
               88  POP_JUMP_IF_FALSE   160  'to 160'

 L.  89        90  LOAD_GLOBAL              _make_filename
               92  CALL_FUNCTION_0       0  ''
               94  STORE_FAST               'name'

 L.  90        96  SETUP_FINALLY       124  'to 124'

 L.  91        98  LOAD_GLOBAL              _posixshmem
              100  LOAD_ATTR                shm_open

 L.  92       102  LOAD_FAST                'name'

 L.  93       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _flags

 L.  94       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _mode

 L.  91       112  LOAD_CONST               ('mode',)
              114  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              116  LOAD_FAST                'self'
              118  STORE_ATTR               _fd
              120  POP_BLOCK        
              122  JUMP_FORWARD        148  'to 148'
            124_0  COME_FROM_FINALLY    96  '96'

 L.  96       124  DUP_TOP          
              126  LOAD_GLOBAL              FileExistsError
              128  COMPARE_OP               exception-match
              130  POP_JUMP_IF_FALSE   146  'to 146'
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L.  97       138  POP_EXCEPT       
              140  JUMP_BACK            90  'to 90'
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           130  '130'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM           122  '122'

 L.  98       148  LOAD_FAST                'name'
              150  LOAD_FAST                'self'
              152  STORE_ATTR               _name

 L.  99       154  BREAK_LOOP          206  'to 206'
              156  JUMP_BACK            90  'to 90'
              158  JUMP_FORWARD        206  'to 206'
            160_0  COME_FROM            88  '88'

 L. 101       160  LOAD_FAST                'self'
              162  LOAD_ATTR                _prepend_leading_slash
              164  POP_JUMP_IF_FALSE   174  'to 174'
              166  LOAD_STR                 '/'
              168  LOAD_FAST                'name'
              170  BINARY_ADD       
              172  JUMP_FORWARD        176  'to 176'
            174_0  COME_FROM           164  '164'
              174  LOAD_FAST                'name'
            176_0  COME_FROM           172  '172'
              176  STORE_FAST               'name'

 L. 102       178  LOAD_GLOBAL              _posixshmem
              180  LOAD_ATTR                shm_open

 L. 103       182  LOAD_FAST                'name'

 L. 104       184  LOAD_FAST                'self'
              186  LOAD_ATTR                _flags

 L. 105       188  LOAD_FAST                'self'
              190  LOAD_ATTR                _mode

 L. 102       192  LOAD_CONST               ('mode',)
              194  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              196  LOAD_FAST                'self'
              198  STORE_ATTR               _fd

 L. 107       200  LOAD_FAST                'name'
              202  LOAD_FAST                'self'
              204  STORE_ATTR               _name
            206_0  COME_FROM           158  '158'

 L. 108       206  SETUP_FINALLY       268  'to 268'

 L. 109       208  LOAD_FAST                'create'
              210  POP_JUMP_IF_FALSE   230  'to 230'
              212  LOAD_FAST                'size'
              214  POP_JUMP_IF_FALSE   230  'to 230'

 L. 110       216  LOAD_GLOBAL              os
              218  LOAD_METHOD              ftruncate
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                _fd
              224  LOAD_FAST                'size'
              226  CALL_METHOD_2         2  ''
              228  POP_TOP          
            230_0  COME_FROM           214  '214'
            230_1  COME_FROM           210  '210'

 L. 111       230  LOAD_GLOBAL              os
              232  LOAD_METHOD              fstat
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                _fd
              238  CALL_METHOD_1         1  ''
              240  STORE_FAST               'stats'

 L. 112       242  LOAD_FAST                'stats'
              244  LOAD_ATTR                st_size
              246  STORE_FAST               'size'

 L. 113       248  LOAD_GLOBAL              mmap
              250  LOAD_METHOD              mmap
              252  LOAD_FAST                'self'
              254  LOAD_ATTR                _fd
              256  LOAD_FAST                'size'
              258  CALL_METHOD_2         2  ''
              260  LOAD_FAST                'self'
              262  STORE_ATTR               _mmap
              264  POP_BLOCK        
              266  JUMP_FORWARD        300  'to 300'
            268_0  COME_FROM_FINALLY   206  '206'

 L. 114       268  DUP_TOP          
              270  LOAD_GLOBAL              OSError
              272  COMPARE_OP               exception-match
          274_276  POP_JUMP_IF_FALSE   298  'to 298'
              278  POP_TOP          
              280  POP_TOP          
              282  POP_TOP          

 L. 115       284  LOAD_FAST                'self'
              286  LOAD_METHOD              unlink
              288  CALL_METHOD_0         0  ''
              290  POP_TOP          

 L. 116       292  RAISE_VARARGS_0       0  'reraise'
              294  POP_EXCEPT       
              296  JUMP_FORWARD        300  'to 300'
            298_0  COME_FROM           274  '274'
              298  END_FINALLY      
            300_0  COME_FROM           296  '296'
            300_1  COME_FROM           266  '266'

 L. 118       300  LOAD_CONST               1
              302  LOAD_CONST               ('register',)
              304  IMPORT_NAME              resource_tracker
              306  IMPORT_FROM              register
              308  STORE_FAST               'register'
              310  POP_TOP          

 L. 119       312  LOAD_FAST                'register'
              314  LOAD_FAST                'self'
              316  LOAD_ATTR                _name
              318  LOAD_STR                 'shared_memory'
              320  CALL_FUNCTION_2       2  ''
              322  POP_TOP          
          324_326  JUMP_FORWARD        598  'to 598'
            328_0  COME_FROM            78  '78'

 L. 125       328  LOAD_FAST                'create'
          330_332  POP_JUMP_IF_FALSE   510  'to 510'

 L. 127       334  LOAD_FAST                'name'
              336  LOAD_CONST               None
              338  COMPARE_OP               is
          340_342  POP_JUMP_IF_FALSE   350  'to 350'
              344  LOAD_GLOBAL              _make_filename
              346  CALL_FUNCTION_0       0  ''
              348  JUMP_FORWARD        352  'to 352'
            350_0  COME_FROM           340  '340'
              350  LOAD_FAST                'name'
            352_0  COME_FROM           348  '348'
              352  STORE_FAST               'temp_name'

 L. 130       354  LOAD_GLOBAL              _winapi
              356  LOAD_METHOD              CreateFileMapping

 L. 131       358  LOAD_GLOBAL              _winapi
              360  LOAD_ATTR                INVALID_HANDLE_VALUE

 L. 132       362  LOAD_GLOBAL              _winapi
              364  LOAD_ATTR                NULL

 L. 133       366  LOAD_GLOBAL              _winapi
              368  LOAD_ATTR                PAGE_READWRITE

 L. 134       370  LOAD_FAST                'size'
              372  LOAD_CONST               32
              374  BINARY_RSHIFT    
              376  LOAD_CONST               4294967295
              378  BINARY_AND       

 L. 135       380  LOAD_FAST                'size'
              382  LOAD_CONST               4294967295
              384  BINARY_AND       

 L. 136       386  LOAD_FAST                'temp_name'

 L. 130       388  CALL_METHOD_6         6  ''
              390  STORE_FAST               'h_map'

 L. 138       392  SETUP_FINALLY       482  'to 482'

 L. 139       394  LOAD_GLOBAL              _winapi
              396  LOAD_METHOD              GetLastError
              398  CALL_METHOD_0         0  ''
              400  STORE_FAST               'last_error_code'

 L. 140       402  LOAD_FAST                'last_error_code'
              404  LOAD_GLOBAL              _winapi
              406  LOAD_ATTR                ERROR_ALREADY_EXISTS
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   460  'to 460'

 L. 141       414  LOAD_FAST                'name'
              416  LOAD_CONST               None
              418  COMPARE_OP               is-not
          420_422  POP_JUMP_IF_FALSE   452  'to 452'

 L. 142       424  LOAD_GLOBAL              FileExistsError

 L. 143       426  LOAD_GLOBAL              errno
              428  LOAD_ATTR                EEXIST

 L. 144       430  LOAD_GLOBAL              os
              432  LOAD_METHOD              strerror
              434  LOAD_GLOBAL              errno
              436  LOAD_ATTR                EEXIST
              438  CALL_METHOD_1         1  ''

 L. 145       440  LOAD_FAST                'name'

 L. 146       442  LOAD_GLOBAL              _winapi
              444  LOAD_ATTR                ERROR_ALREADY_EXISTS

 L. 142       446  CALL_FUNCTION_4       4  ''
              448  RAISE_VARARGS_1       1  'exception instance'
              450  JUMP_FORWARD        460  'to 460'
            452_0  COME_FROM           420  '420'

 L. 149       452  POP_BLOCK        
              454  CALL_FINALLY        482  'to 482'
          456_458  JUMP_BACK           334  'to 334'
            460_0  COME_FROM           450  '450'
            460_1  COME_FROM           410  '410'

 L. 150       460  LOAD_GLOBAL              mmap
              462  LOAD_ATTR                mmap
              464  LOAD_CONST               -1
              466  LOAD_FAST                'size'
              468  LOAD_FAST                'temp_name'
              470  LOAD_CONST               ('tagname',)
              472  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              474  LOAD_FAST                'self'
              476  STORE_ATTR               _mmap
              478  POP_BLOCK        
              480  BEGIN_FINALLY    
            482_0  COME_FROM           454  '454'
            482_1  COME_FROM_FINALLY   392  '392'

 L. 152       482  LOAD_GLOBAL              _winapi
              484  LOAD_METHOD              CloseHandle
              486  LOAD_FAST                'h_map'
              488  CALL_METHOD_1         1  ''
              490  POP_TOP          
              492  END_FINALLY      

 L. 153       494  LOAD_FAST                'temp_name'
              496  LOAD_FAST                'self'
              498  STORE_ATTR               _name

 L. 154   500_502  BREAK_LOOP          598  'to 598'
          504_506  JUMP_BACK           334  'to 334'
              508  JUMP_FORWARD        598  'to 598'
            510_0  COME_FROM           330  '330'

 L. 157       510  LOAD_FAST                'name'
              512  LOAD_FAST                'self'
              514  STORE_ATTR               _name

 L. 160       516  LOAD_GLOBAL              _winapi
              518  LOAD_METHOD              OpenFileMapping

 L. 161       520  LOAD_GLOBAL              _winapi
              522  LOAD_ATTR                FILE_MAP_READ

 L. 162       524  LOAD_CONST               False

 L. 163       526  LOAD_FAST                'name'

 L. 160       528  CALL_METHOD_3         3  ''
              530  STORE_FAST               'h_map'

 L. 165       532  SETUP_FINALLY       558  'to 558'

 L. 166       534  LOAD_GLOBAL              _winapi
              536  LOAD_METHOD              MapViewOfFile

 L. 167       538  LOAD_FAST                'h_map'

 L. 168       540  LOAD_GLOBAL              _winapi
              542  LOAD_ATTR                FILE_MAP_READ

 L. 169       544  LOAD_CONST               0

 L. 170       546  LOAD_CONST               0

 L. 171       548  LOAD_CONST               0

 L. 166       550  CALL_METHOD_5         5  ''
              552  STORE_FAST               'p_buf'
              554  POP_BLOCK        
              556  BEGIN_FINALLY    
            558_0  COME_FROM_FINALLY   532  '532'

 L. 174       558  LOAD_GLOBAL              _winapi
              560  LOAD_METHOD              CloseHandle
              562  LOAD_FAST                'h_map'
              564  CALL_METHOD_1         1  ''
              566  POP_TOP          
              568  END_FINALLY      

 L. 175       570  LOAD_GLOBAL              _winapi
              572  LOAD_METHOD              VirtualQuerySize
              574  LOAD_FAST                'p_buf'
              576  CALL_METHOD_1         1  ''
              578  STORE_FAST               'size'

 L. 176       580  LOAD_GLOBAL              mmap
              582  LOAD_ATTR                mmap
              584  LOAD_CONST               -1
              586  LOAD_FAST                'size'
              588  LOAD_FAST                'name'
              590  LOAD_CONST               ('tagname',)
              592  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              594  LOAD_FAST                'self'
              596  STORE_ATTR               _mmap
            598_0  COME_FROM           508  '508'
            598_1  COME_FROM           324  '324'

 L. 178       598  LOAD_FAST                'size'
              600  LOAD_FAST                'self'
              602  STORE_ATTR               _size

 L. 179       604  LOAD_GLOBAL              memoryview
              606  LOAD_FAST                'self'
              608  LOAD_ATTR                _mmap
              610  CALL_FUNCTION_1       1  ''
              612  LOAD_FAST                'self'
              614  STORE_ATTR               _buf

Parse error at or near `POP_EXCEPT' instruction at offset 142

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
                encoded_value = value
            else:
                encoded_value = value.encode(_encoding) if isinstance(value, str) else value
                if len(encoded_value) > self._allocated_bytes[position]:
                    raise ValueError('bytes/str item exceeds available storage')
                elif current_format[(-1)] == 's':
                    new_format = current_format
                else:
                    new_format = self._types_mapping[str] % (
                     self._allocated_bytes[position],)
            self._set_packing_format_and_transformpositionnew_formatvalue
            struct.pack_into(new_format, self.shm.buf, offset, encoded_value)

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