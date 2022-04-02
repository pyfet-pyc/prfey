# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: multiprocessing\shared_memory.py
"""Provides shared memory for direct access across processes.

The API of this package is currently provisional. Refer to the
documentation for details.
"""
__all__ = [
 'SharedMemory', 'ShareableList']
from functools import partial
import mmap, os, errno, struct, secrets, types
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

def _make_filename--- This code section failed: ---

 L.  42         0  LOAD_GLOBAL              _SHM_SAFE_NAME_LENGTH
                2  LOAD_GLOBAL              len
                4  LOAD_GLOBAL              _SHM_NAME_PREFIX
                6  CALL_FUNCTION_1       1  ''
                8  BINARY_SUBTRACT  
               10  LOAD_CONST               2
               12  BINARY_FLOOR_DIVIDE
               14  STORE_FAST               'nbytes'

 L.  43        16  LOAD_FAST                'nbytes'
               18  LOAD_CONST               2
               20  COMPARE_OP               >=
               22  POP_JUMP_IF_TRUE     32  'to 32'
               24  <74>             
               26  LOAD_STR                 '_SHM_NAME_PREFIX too long'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'

 L.  44        32  LOAD_GLOBAL              _SHM_NAME_PREFIX
               34  LOAD_GLOBAL              secrets
               36  LOAD_METHOD              token_hex
               38  LOAD_FAST                'nbytes'
               40  CALL_METHOD_1         1  ''
               42  BINARY_ADD       
               44  STORE_FAST               'name'

 L.  45        46  LOAD_GLOBAL              len
               48  LOAD_FAST                'name'
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_GLOBAL              _SHM_SAFE_NAME_LENGTH
               54  COMPARE_OP               <=
               56  POP_JUMP_IF_TRUE     62  'to 62'
               58  <74>             
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            56  '56'

 L.  46        62  LOAD_FAST                'name'
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 24


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

 L.  75         0  LOAD_FAST                'size'
                2  LOAD_CONST               0
                4  COMPARE_OP               >=
                6  POP_JUMP_IF_TRUE     16  'to 16'

 L.  76         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 "'size' must be a positive integer"
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  77        16  LOAD_FAST                'create'
               18  POP_JUMP_IF_FALSE    48  'to 48'

 L.  78        20  LOAD_GLOBAL              _O_CREX
               22  LOAD_GLOBAL              os
               24  LOAD_ATTR                O_RDWR
               26  BINARY_OR        
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _flags

 L.  79        32  LOAD_FAST                'size'
               34  LOAD_CONST               0
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L.  80        40  LOAD_GLOBAL              ValueError
               42  LOAD_STR                 "'size' must be a positive number different from zero"
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'
             48_1  COME_FROM            18  '18'

 L.  81        48  LOAD_FAST                'name'
               50  LOAD_CONST               None
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    76  'to 76'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _flags
               60  LOAD_GLOBAL              os
               62  LOAD_ATTR                O_EXCL
               64  BINARY_AND       
               66  POP_JUMP_IF_TRUE     76  'to 76'

 L.  82        68  LOAD_GLOBAL              ValueError
               70  LOAD_STR                 "'name' can only be None if create=True"
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            66  '66'
             76_1  COME_FROM            54  '54'

 L.  84        76  LOAD_GLOBAL              _USE_POSIX
            78_80  POP_JUMP_IF_FALSE   324  'to 324'

 L.  88        82  LOAD_FAST                'name'
               84  LOAD_CONST               None
               86  <117>                 0  ''
               88  POP_JUMP_IF_FALSE   158  'to 158'

 L.  90        90  LOAD_GLOBAL              _make_filename
               92  CALL_FUNCTION_0       0  ''
               94  STORE_FAST               'name'

 L.  91        96  SETUP_FINALLY       124  'to 124'

 L.  92        98  LOAD_GLOBAL              _posixshmem
              100  LOAD_ATTR                shm_open

 L.  93       102  LOAD_FAST                'name'

 L.  94       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _flags

 L.  95       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _mode

 L.  92       112  LOAD_CONST               ('mode',)
              114  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              116  LOAD_FAST                'self'
              118  STORE_ATTR               _fd
              120  POP_BLOCK        
              122  JUMP_FORWARD        146  'to 146'
            124_0  COME_FROM_FINALLY    96  '96'

 L.  97       124  DUP_TOP          
              126  LOAD_GLOBAL              FileExistsError
              128  <121>               144  ''
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L.  98       136  POP_EXCEPT       
              138  JUMP_BACK            90  'to 90'
              140  POP_EXCEPT       
              142  JUMP_FORWARD        146  'to 146'
              144  <48>             
            146_0  COME_FROM           142  '142'
            146_1  COME_FROM           122  '122'

 L.  99       146  LOAD_FAST                'name'
              148  LOAD_FAST                'self'
              150  STORE_ATTR               _name

 L. 100       152  BREAK_LOOP          204  'to 204'
              154  JUMP_BACK            90  'to 90'
              156  JUMP_FORWARD        204  'to 204'
            158_0  COME_FROM            88  '88'

 L. 102       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _prepend_leading_slash
              162  POP_JUMP_IF_FALSE   172  'to 172'
              164  LOAD_STR                 '/'
              166  LOAD_FAST                'name'
              168  BINARY_ADD       
              170  JUMP_FORWARD        174  'to 174'
            172_0  COME_FROM           162  '162'
              172  LOAD_FAST                'name'
            174_0  COME_FROM           170  '170'
              174  STORE_FAST               'name'

 L. 103       176  LOAD_GLOBAL              _posixshmem
              178  LOAD_ATTR                shm_open

 L. 104       180  LOAD_FAST                'name'

 L. 105       182  LOAD_FAST                'self'
              184  LOAD_ATTR                _flags

 L. 106       186  LOAD_FAST                'self'
              188  LOAD_ATTR                _mode

 L. 103       190  LOAD_CONST               ('mode',)
              192  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              194  LOAD_FAST                'self'
              196  STORE_ATTR               _fd

 L. 108       198  LOAD_FAST                'name'
              200  LOAD_FAST                'self'
              202  STORE_ATTR               _name
            204_0  COME_FROM           156  '156'

 L. 109       204  SETUP_FINALLY       266  'to 266'

 L. 110       206  LOAD_FAST                'create'
              208  POP_JUMP_IF_FALSE   228  'to 228'
              210  LOAD_FAST                'size'
              212  POP_JUMP_IF_FALSE   228  'to 228'

 L. 111       214  LOAD_GLOBAL              os
              216  LOAD_METHOD              ftruncate
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                _fd
              222  LOAD_FAST                'size'
              224  CALL_METHOD_2         2  ''
              226  POP_TOP          
            228_0  COME_FROM           212  '212'
            228_1  COME_FROM           208  '208'

 L. 112       228  LOAD_GLOBAL              os
              230  LOAD_METHOD              fstat
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                _fd
              236  CALL_METHOD_1         1  ''
              238  STORE_FAST               'stats'

 L. 113       240  LOAD_FAST                'stats'
              242  LOAD_ATTR                st_size
              244  STORE_FAST               'size'

 L. 114       246  LOAD_GLOBAL              mmap
              248  LOAD_METHOD              mmap
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                _fd
              254  LOAD_FAST                'size'
              256  CALL_METHOD_2         2  ''
              258  LOAD_FAST                'self'
              260  STORE_ATTR               _mmap
              262  POP_BLOCK        
              264  JUMP_FORWARD        296  'to 296'
            266_0  COME_FROM_FINALLY   204  '204'

 L. 115       266  DUP_TOP          
              268  LOAD_GLOBAL              OSError
          270_272  <121>               294  ''
              274  POP_TOP          
              276  POP_TOP          
              278  POP_TOP          

 L. 116       280  LOAD_FAST                'self'
              282  LOAD_METHOD              unlink
              284  CALL_METHOD_0         0  ''
              286  POP_TOP          

 L. 117       288  RAISE_VARARGS_0       0  'reraise'
              290  POP_EXCEPT       
              292  JUMP_FORWARD        296  'to 296'
              294  <48>             
            296_0  COME_FROM           292  '292'
            296_1  COME_FROM           264  '264'

 L. 119       296  LOAD_CONST               1
              298  LOAD_CONST               ('register',)
              300  IMPORT_NAME              resource_tracker
              302  IMPORT_FROM              register
              304  STORE_FAST               'register'
              306  POP_TOP          

 L. 120       308  LOAD_FAST                'register'
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                _name
              314  LOAD_STR                 'shared_memory'
              316  CALL_FUNCTION_2       2  ''
              318  POP_TOP          
          320_322  JUMP_FORWARD        622  'to 622'
            324_0  COME_FROM            78  '78'

 L. 126       324  LOAD_FAST                'create'
          326_328  POP_JUMP_IF_FALSE   524  'to 524'

 L. 128       330  LOAD_FAST                'name'
              332  LOAD_CONST               None
              334  <117>                 0  ''
          336_338  POP_JUMP_IF_FALSE   346  'to 346'
              340  LOAD_GLOBAL              _make_filename
              342  CALL_FUNCTION_0       0  ''
              344  JUMP_FORWARD        348  'to 348'
            346_0  COME_FROM           336  '336'
              346  LOAD_FAST                'name'
            348_0  COME_FROM           344  '344'
              348  STORE_FAST               'temp_name'

 L. 131       350  LOAD_GLOBAL              _winapi
              352  LOAD_METHOD              CreateFileMapping

 L. 132       354  LOAD_GLOBAL              _winapi
              356  LOAD_ATTR                INVALID_HANDLE_VALUE

 L. 133       358  LOAD_GLOBAL              _winapi
              360  LOAD_ATTR                NULL

 L. 134       362  LOAD_GLOBAL              _winapi
              364  LOAD_ATTR                PAGE_READWRITE

 L. 135       366  LOAD_FAST                'size'
              368  LOAD_CONST               32
              370  BINARY_RSHIFT    
              372  LOAD_CONST               4294967295
              374  BINARY_AND       

 L. 136       376  LOAD_FAST                'size'
              378  LOAD_CONST               4294967295
              380  BINARY_AND       

 L. 137       382  LOAD_FAST                'temp_name'

 L. 131       384  CALL_METHOD_6         6  ''
              386  STORE_FAST               'h_map'

 L. 139       388  SETUP_FINALLY       496  'to 496'

 L. 140       390  LOAD_GLOBAL              _winapi
              392  LOAD_METHOD              GetLastError
              394  CALL_METHOD_0         0  ''
              396  STORE_FAST               'last_error_code'

 L. 141       398  LOAD_FAST                'last_error_code'
              400  LOAD_GLOBAL              _winapi
              402  LOAD_ATTR                ERROR_ALREADY_EXISTS
              404  COMPARE_OP               ==
          406_408  POP_JUMP_IF_FALSE   464  'to 464'

 L. 142       410  LOAD_FAST                'name'
              412  LOAD_CONST               None
              414  <117>                 1  ''
          416_418  POP_JUMP_IF_FALSE   448  'to 448'

 L. 143       420  LOAD_GLOBAL              FileExistsError

 L. 144       422  LOAD_GLOBAL              errno
              424  LOAD_ATTR                EEXIST

 L. 145       426  LOAD_GLOBAL              os
              428  LOAD_METHOD              strerror
              430  LOAD_GLOBAL              errno
              432  LOAD_ATTR                EEXIST
              434  CALL_METHOD_1         1  ''

 L. 146       436  LOAD_FAST                'name'

 L. 147       438  LOAD_GLOBAL              _winapi
              440  LOAD_ATTR                ERROR_ALREADY_EXISTS

 L. 143       442  CALL_FUNCTION_4       4  ''
              444  RAISE_VARARGS_1       1  'exception instance'
              446  JUMP_FORWARD        464  'to 464'
            448_0  COME_FROM           416  '416'

 L. 150       448  POP_BLOCK        

 L. 153       450  LOAD_GLOBAL              _winapi
              452  LOAD_METHOD              CloseHandle
              454  LOAD_FAST                'h_map'
              456  CALL_METHOD_1         1  ''
              458  POP_TOP          

 L. 150   460_462  JUMP_BACK           330  'to 330'
            464_0  COME_FROM           446  '446'
            464_1  COME_FROM           406  '406'

 L. 151       464  LOAD_GLOBAL              mmap
              466  LOAD_ATTR                mmap
              468  LOAD_CONST               -1
              470  LOAD_FAST                'size'
              472  LOAD_FAST                'temp_name'
              474  LOAD_CONST               ('tagname',)
              476  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              478  LOAD_FAST                'self'
              480  STORE_ATTR               _mmap
              482  POP_BLOCK        

 L. 153       484  LOAD_GLOBAL              _winapi
              486  LOAD_METHOD              CloseHandle
              488  LOAD_FAST                'h_map'
              490  CALL_METHOD_1         1  ''
              492  POP_TOP          
              494  JUMP_FORWARD        508  'to 508'
            496_0  COME_FROM_FINALLY   388  '388'
              496  LOAD_GLOBAL              _winapi
              498  LOAD_METHOD              CloseHandle
              500  LOAD_FAST                'h_map'
              502  CALL_METHOD_1         1  ''
              504  POP_TOP          
              506  <48>             
            508_0  COME_FROM           494  '494'

 L. 154       508  LOAD_FAST                'temp_name'
              510  LOAD_FAST                'self'
              512  STORE_ATTR               _name

 L. 155   514_516  BREAK_LOOP          622  'to 622'
          518_520  JUMP_BACK           330  'to 330'
              522  JUMP_FORWARD        622  'to 622'
            524_0  COME_FROM           326  '326'

 L. 158       524  LOAD_FAST                'name'
              526  LOAD_FAST                'self'
              528  STORE_ATTR               _name

 L. 161       530  LOAD_GLOBAL              _winapi
              532  LOAD_METHOD              OpenFileMapping

 L. 162       534  LOAD_GLOBAL              _winapi
              536  LOAD_ATTR                FILE_MAP_READ

 L. 163       538  LOAD_CONST               False

 L. 164       540  LOAD_FAST                'name'

 L. 161       542  CALL_METHOD_3         3  ''
              544  STORE_FAST               'h_map'

 L. 166       546  SETUP_FINALLY       582  'to 582'

 L. 167       548  LOAD_GLOBAL              _winapi
              550  LOAD_METHOD              MapViewOfFile

 L. 168       552  LOAD_FAST                'h_map'

 L. 169       554  LOAD_GLOBAL              _winapi
              556  LOAD_ATTR                FILE_MAP_READ

 L. 170       558  LOAD_CONST               0

 L. 171       560  LOAD_CONST               0

 L. 172       562  LOAD_CONST               0

 L. 167       564  CALL_METHOD_5         5  ''
              566  STORE_FAST               'p_buf'
              568  POP_BLOCK        

 L. 175       570  LOAD_GLOBAL              _winapi
              572  LOAD_METHOD              CloseHandle
              574  LOAD_FAST                'h_map'
              576  CALL_METHOD_1         1  ''
              578  POP_TOP          
              580  JUMP_FORWARD        594  'to 594'
            582_0  COME_FROM_FINALLY   546  '546'
              582  LOAD_GLOBAL              _winapi
              584  LOAD_METHOD              CloseHandle
              586  LOAD_FAST                'h_map'
              588  CALL_METHOD_1         1  ''
              590  POP_TOP          
              592  <48>             
            594_0  COME_FROM           580  '580'

 L. 176       594  LOAD_GLOBAL              _winapi
              596  LOAD_METHOD              VirtualQuerySize
              598  LOAD_FAST                'p_buf'
              600  CALL_METHOD_1         1  ''
              602  STORE_FAST               'size'

 L. 177       604  LOAD_GLOBAL              mmap
              606  LOAD_ATTR                mmap
              608  LOAD_CONST               -1
              610  LOAD_FAST                'size'
              612  LOAD_FAST                'name'
              614  LOAD_CONST               ('tagname',)
              616  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              618  LOAD_FAST                'self'
              620  STORE_ATTR               _mmap
            622_0  COME_FROM           522  '522'
            622_1  COME_FROM           320  '320'

 L. 179       622  LOAD_FAST                'size'
              624  LOAD_FAST                'self'
              626  STORE_ATTR               _size

 L. 180       628  LOAD_GLOBAL              memoryview
              630  LOAD_FAST                'self'
              632  LOAD_ATTR                _mmap
              634  CALL_FUNCTION_1       1  ''
              636  LOAD_FAST                'self'
              638  STORE_ATTR               _buf

Parse error at or near `<117>' instruction at offset 52

    def __del__--- This code section failed: ---

 L. 183         0  SETUP_FINALLY        14  'to 14'

 L. 184         2  LOAD_FAST                'self'
                4  LOAD_METHOD              close
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          
               10  POP_BLOCK        
               12  JUMP_FORWARD         32  'to 32'
             14_0  COME_FROM_FINALLY     0  '0'

 L. 185        14  DUP_TOP          
               16  LOAD_GLOBAL              OSError
               18  <121>                30  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 186        26  POP_EXCEPT       
               28  JUMP_FORWARD         32  'to 32'
               30  <48>             
             32_0  COME_FROM            28  '28'
             32_1  COME_FROM            12  '12'

Parse error at or near `<121>' instruction at offset 18

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
                if self._name.startswith'/':
                    reported_name = self._name[1:]
        return reported_name

    @property
    def size(self):
        """Size in bytes."""
        return self._size

    def close--- This code section failed: ---

 L. 223         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _buf
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 224        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _buf
               14  LOAD_METHOD              release
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 225        20  LOAD_CONST               None
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _buf
             26_0  COME_FROM             8  '8'

 L. 226        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _mmap
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    52  'to 52'

 L. 227        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _mmap
               40  LOAD_METHOD              close
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          

 L. 228        46  LOAD_CONST               None
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _mmap
             52_0  COME_FROM            34  '34'

 L. 229        52  LOAD_GLOBAL              _USE_POSIX
               54  POP_JUMP_IF_FALSE    84  'to 84'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _fd
               60  LOAD_CONST               0
               62  COMPARE_OP               >=
               64  POP_JUMP_IF_FALSE    84  'to 84'

 L. 230        66  LOAD_GLOBAL              os
               68  LOAD_METHOD              close
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _fd
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L. 231        78  LOAD_CONST               -1
               80  LOAD_FAST                'self'
               82  STORE_ATTR               _fd
             84_0  COME_FROM            64  '64'
             84_1  COME_FROM            54  '54'

Parse error at or near `None' instruction at offset -1

    def unlink(self):
        """Requests that the underlying shared memory block be destroyed.

        In order to ensure proper cleanup of resources, unlink should be
        called once (and only once) across all processes which have access
        to the shared memory block."""
        if _USE_POSIX:
            if self._name:
                from .resource_tracker import unregister
                _posixshmem.shm_unlinkself._name
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
     1:lambda value: value.rstripb'\x00'.decode_encoding, 
     2:lambda value: value.rstripb'\x00', 
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

    def __init__--- This code section failed: ---

 L. 297         0  LOAD_FAST                'name'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  LOAD_FAST                'sequence'
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE   226  'to 226'
             16_0  COME_FROM             6  '6'

 L. 298        16  LOAD_FAST                'sequence'
               18  JUMP_IF_TRUE_OR_POP    22  'to 22'
               20  LOAD_CONST               ()
             22_0  COME_FROM            18  '18'
               22  STORE_FAST               'sequence'

 L. 299        24  LOAD_CLOSURE             'self'
               26  BUILD_TUPLE_1         1 
               28  LOAD_LISTCOMP            '<code_object <listcomp>>'
               30  LOAD_STR                 'ShareableList.__init__.<locals>.<listcomp>'
               32  MAKE_FUNCTION_8          'closure'

 L. 305        34  LOAD_FAST                'sequence'

 L. 299        36  GET_ITER         
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               '_formats'

 L. 307        42  LOAD_GLOBAL              len
               44  LOAD_FAST                '_formats'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_DEREF               'self'
               50  STORE_ATTR               _list_len

 L. 308        52  LOAD_GLOBAL              sum
               54  LOAD_GENEXPR             '<code_object <genexpr>>'
               56  LOAD_STR                 'ShareableList.__init__.<locals>.<genexpr>'
               58  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               60  LOAD_FAST                '_formats'
               62  GET_ITER         
               64  CALL_FUNCTION_1       1  ''
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_DEREF               'self'
               70  LOAD_ATTR                _list_len
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_TRUE     80  'to 80'
               76  <74>             
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            74  '74'

 L. 309        80  LOAD_CONST               0
               82  STORE_FAST               'offset'

 L. 313        84  LOAD_CONST               0
               86  BUILD_LIST_1          1 
               88  LOAD_DEREF               'self'
               90  STORE_ATTR               _allocated_offsets

 L. 314        92  LOAD_FAST                '_formats'
               94  GET_ITER         
               96  FOR_ITER            152  'to 152'
               98  STORE_FAST               'fmt'

 L. 315       100  LOAD_FAST                'offset'
              102  LOAD_FAST                'fmt'
              104  LOAD_CONST               -1
              106  BINARY_SUBSCR    
              108  LOAD_STR                 's'
              110  COMPARE_OP               !=
              112  POP_JUMP_IF_FALSE   120  'to 120'
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                _alignment
              118  JUMP_FORWARD        134  'to 134'
            120_0  COME_FROM           112  '112'
              120  LOAD_GLOBAL              int
              122  LOAD_FAST                'fmt'
              124  LOAD_CONST               None
              126  LOAD_CONST               -1
              128  BUILD_SLICE_2         2 
              130  BINARY_SUBSCR    
              132  CALL_FUNCTION_1       1  ''
            134_0  COME_FROM           118  '118'
              134  INPLACE_ADD      
              136  STORE_FAST               'offset'

 L. 316       138  LOAD_DEREF               'self'
              140  LOAD_ATTR                _allocated_offsets
              142  LOAD_METHOD              append
              144  LOAD_FAST                'offset'
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          
              150  JUMP_BACK            96  'to 96'

 L. 317       152  LOAD_CLOSURE             'self'
              154  BUILD_TUPLE_1         1 
              156  LOAD_LISTCOMP            '<code_object <listcomp>>'
              158  LOAD_STR                 'ShareableList.__init__.<locals>.<listcomp>'
              160  MAKE_FUNCTION_8          'closure'

 L. 318       162  LOAD_FAST                'sequence'

 L. 317       164  GET_ITER         
              166  CALL_FUNCTION_1       1  ''
              168  STORE_FAST               '_recreation_codes'

 L. 320       170  LOAD_GLOBAL              struct
              172  LOAD_METHOD              calcsize

 L. 321       174  LOAD_STR                 'q'
              176  LOAD_DEREF               'self'
              178  LOAD_ATTR                _format_size_metainfo
              180  BINARY_ADD       

 L. 322       182  LOAD_STR                 ''
              184  LOAD_METHOD              join
              186  LOAD_FAST                '_formats'
              188  CALL_METHOD_1         1  ''

 L. 321       190  BINARY_ADD       

 L. 323       192  LOAD_DEREF               'self'
              194  LOAD_ATTR                _format_packing_metainfo

 L. 321       196  BINARY_ADD       

 L. 324       198  LOAD_DEREF               'self'
              200  LOAD_ATTR                _format_back_transform_codes

 L. 321       202  BINARY_ADD       

 L. 320       204  CALL_METHOD_1         1  ''
              206  STORE_FAST               'requested_size'

 L. 327       208  LOAD_GLOBAL              SharedMemory
              210  LOAD_FAST                'name'
              212  LOAD_CONST               True
              214  LOAD_FAST                'requested_size'
              216  LOAD_CONST               ('create', 'size')
              218  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              220  LOAD_DEREF               'self'
              222  STORE_ATTR               shm
              224  JUMP_FORWARD        236  'to 236'
            226_0  COME_FROM            14  '14'

 L. 329       226  LOAD_GLOBAL              SharedMemory
              228  LOAD_FAST                'name'
              230  CALL_FUNCTION_1       1  ''
              232  LOAD_DEREF               'self'
              234  STORE_ATTR               shm
            236_0  COME_FROM           224  '224'

 L. 331       236  LOAD_FAST                'sequence'
              238  LOAD_CONST               None
              240  <117>                 1  ''
          242_244  POP_JUMP_IF_FALSE   412  'to 412'

 L. 332       246  LOAD_GLOBAL              _encoding
              248  STORE_DEREF              '_enc'

 L. 333       250  LOAD_GLOBAL              struct
              252  LOAD_ATTR                pack_into

 L. 334       254  LOAD_STR                 'q'
              256  LOAD_DEREF               'self'
              258  LOAD_ATTR                _format_size_metainfo
              260  BINARY_ADD       

 L. 335       262  LOAD_DEREF               'self'
              264  LOAD_ATTR                shm
              266  LOAD_ATTR                buf

 L. 336       268  LOAD_CONST               0

 L. 337       270  LOAD_DEREF               'self'
              272  LOAD_ATTR                _list_len

 L. 333       274  BUILD_LIST_4          4 

 L. 338       276  LOAD_DEREF               'self'
              278  LOAD_ATTR                _allocated_offsets

 L. 333       280  CALL_FINALLY        283  'to 283'
              282  WITH_CLEANUP_FINISH
              284  CALL_FUNCTION_EX      0  'positional arguments only'
              286  POP_TOP          

 L. 340       288  LOAD_GLOBAL              struct
              290  LOAD_ATTR                pack_into

 L. 341       292  LOAD_STR                 ''
              294  LOAD_METHOD              join
              296  LOAD_FAST                '_formats'
              298  CALL_METHOD_1         1  ''

 L. 342       300  LOAD_DEREF               'self'
              302  LOAD_ATTR                shm
              304  LOAD_ATTR                buf

 L. 343       306  LOAD_DEREF               'self'
              308  LOAD_ATTR                _offset_data_start

 L. 340       310  BUILD_LIST_3          3 

 L. 344       312  LOAD_CLOSURE             '_enc'
              314  BUILD_TUPLE_1         1 
              316  LOAD_GENEXPR             '<code_object <genexpr>>'
              318  LOAD_STR                 'ShareableList.__init__.<locals>.<genexpr>'
              320  MAKE_FUNCTION_8          'closure'
              322  LOAD_FAST                'sequence'
              324  GET_ITER         
              326  CALL_FUNCTION_1       1  ''

 L. 340       328  CALL_FINALLY        331  'to 331'
              330  WITH_CLEANUP_FINISH
              332  CALL_FUNCTION_EX      0  'positional arguments only'
              334  POP_TOP          

 L. 346       336  LOAD_GLOBAL              struct
              338  LOAD_ATTR                pack_into

 L. 347       340  LOAD_DEREF               'self'
              342  LOAD_ATTR                _format_packing_metainfo

 L. 348       344  LOAD_DEREF               'self'
              346  LOAD_ATTR                shm
              348  LOAD_ATTR                buf

 L. 349       350  LOAD_DEREF               'self'
              352  LOAD_ATTR                _offset_packing_formats

 L. 346       354  BUILD_LIST_3          3 

 L. 350       356  LOAD_CLOSURE             '_enc'
              358  BUILD_TUPLE_1         1 
              360  LOAD_GENEXPR             '<code_object <genexpr>>'
              362  LOAD_STR                 'ShareableList.__init__.<locals>.<genexpr>'
              364  MAKE_FUNCTION_8          'closure'
              366  LOAD_FAST                '_formats'
              368  GET_ITER         
              370  CALL_FUNCTION_1       1  ''

 L. 346       372  CALL_FINALLY        375  'to 375'
              374  WITH_CLEANUP_FINISH
              376  CALL_FUNCTION_EX      0  'positional arguments only'
              378  POP_TOP          

 L. 352       380  LOAD_GLOBAL              struct
              382  LOAD_ATTR                pack_into

 L. 353       384  LOAD_DEREF               'self'
              386  LOAD_ATTR                _format_back_transform_codes

 L. 354       388  LOAD_DEREF               'self'
              390  LOAD_ATTR                shm
              392  LOAD_ATTR                buf

 L. 355       394  LOAD_DEREF               'self'
              396  LOAD_ATTR                _offset_back_transform_codes

 L. 352       398  BUILD_LIST_3          3 

 L. 356       400  LOAD_FAST                '_recreation_codes'

 L. 352       402  CALL_FINALLY        405  'to 405'
              404  WITH_CLEANUP_FINISH
              406  CALL_FUNCTION_EX      0  'positional arguments only'
              408  POP_TOP          
              410  JUMP_FORWARD        448  'to 448'
            412_0  COME_FROM           242  '242'

 L. 360       412  LOAD_GLOBAL              len
              414  LOAD_DEREF               'self'
              416  CALL_FUNCTION_1       1  ''
              418  LOAD_DEREF               'self'
              420  STORE_ATTR               _list_len

 L. 361       422  LOAD_GLOBAL              list

 L. 362       424  LOAD_GLOBAL              struct
              426  LOAD_METHOD              unpack_from

 L. 363       428  LOAD_DEREF               'self'
              430  LOAD_ATTR                _format_size_metainfo

 L. 364       432  LOAD_DEREF               'self'
              434  LOAD_ATTR                shm
              436  LOAD_ATTR                buf

 L. 365       438  LOAD_CONST               8

 L. 362       440  CALL_METHOD_3         3  ''

 L. 361       442  CALL_FUNCTION_1       1  ''
              444  LOAD_DEREF               'self'
              446  STORE_ATTR               _allocated_offsets
            448_0  COME_FROM           410  '410'

Parse error at or near `None' instruction at offset -1

    def _get_packing_format(self, position):
        """Gets the packing format for a single value stored in the list."""
        position = position if position >= 0 else position + self._list_len
        if position >= self._list_len or self._list_len < 0:
            raise IndexError('Requested position out of range.')
        v = struct.unpack_from'8s'self.shm.buf(self._offset_packing_formats + position * 8)[0]
        fmt = v.rstripb'\x00'
        fmt_as_str = fmt.decode_encoding
        return fmt_as_str

    def _get_back_transform(self, position):
        """Gets the back transformation function for a single value."""
        if position >= self._list_len or self._list_len < 0:
            raise IndexError('Requested position out of range.')
        transform_code = struct.unpack_from'b'self.shm.buf(self._offset_back_transform_codes + position)[0]
        transform_function = self._back_transforms_mapping[transform_code]
        return transform_function

    def _set_packing_format_and_transform(self, position, fmt_as_str, value):
        """Sets the packing format and back transformation code for a
        single value in the list at the specified position."""
        if position >= self._list_len or self._list_len < 0:
            raise IndexError('Requested position out of range.')
        struct.pack_into('8s', self.shm.buf, self._offset_packing_formats + position * 8, fmt_as_str.encode_encoding)
        transform_code = self._extract_recreation_codevalue
        struct.pack_into('b', self.shm.buf, self._offset_back_transform_codes + position, transform_code)

    def __getitem__--- This code section failed: ---

 L. 423         0  LOAD_FAST                'position'
                2  LOAD_CONST               0
                4  COMPARE_OP               >=
                6  POP_JUMP_IF_FALSE    12  'to 12'
                8  LOAD_FAST                'position'
               10  JUMP_FORWARD         20  'to 20'
             12_0  COME_FROM             6  '6'
               12  LOAD_FAST                'position'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _list_len
               18  BINARY_ADD       
             20_0  COME_FROM            10  '10'
               20  STORE_FAST               'position'

 L. 424        22  SETUP_FINALLY        70  'to 70'

 L. 425        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _offset_data_start
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _allocated_offsets
               32  LOAD_FAST                'position'
               34  BINARY_SUBSCR    
               36  BINARY_ADD       
               38  STORE_FAST               'offset'

 L. 426        40  LOAD_GLOBAL              struct
               42  LOAD_METHOD              unpack_from

 L. 427        44  LOAD_FAST                'self'
               46  LOAD_METHOD              _get_packing_format
               48  LOAD_FAST                'position'
               50  CALL_METHOD_1         1  ''

 L. 428        52  LOAD_FAST                'self'
               54  LOAD_ATTR                shm
               56  LOAD_ATTR                buf

 L. 429        58  LOAD_FAST                'offset'

 L. 426        60  CALL_METHOD_3         3  ''
               62  UNPACK_SEQUENCE_1     1 
               64  STORE_FAST               'v'
               66  POP_BLOCK        
               68  JUMP_FORWARD         96  'to 96'
             70_0  COME_FROM_FINALLY    22  '22'

 L. 431        70  DUP_TOP          
               72  LOAD_GLOBAL              IndexError
               74  <121>                94  ''
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 432        82  LOAD_GLOBAL              IndexError
               84  LOAD_STR                 'index out of range'
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
               90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
               94  <48>             
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            68  '68'

 L. 434        96  LOAD_FAST                'self'
               98  LOAD_METHOD              _get_back_transform
              100  LOAD_FAST                'position'
              102  CALL_METHOD_1         1  ''
              104  STORE_FAST               'back_transform'

 L. 435       106  LOAD_FAST                'back_transform'
              108  LOAD_FAST                'v'
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'v'

 L. 437       114  LOAD_FAST                'v'
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 74

    def __setitem__--- This code section failed: ---

 L. 440         0  LOAD_FAST                'position'
                2  LOAD_CONST               0
                4  COMPARE_OP               >=
                6  POP_JUMP_IF_FALSE    12  'to 12'
                8  LOAD_FAST                'position'
               10  JUMP_FORWARD         20  'to 20'
             12_0  COME_FROM             6  '6'
               12  LOAD_FAST                'position'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _list_len
               18  BINARY_ADD       
             20_0  COME_FROM            10  '10'
               20  STORE_FAST               'position'

 L. 441        22  SETUP_FINALLY        58  'to 58'

 L. 442        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _allocated_offsets
               28  LOAD_FAST                'position'
               30  BINARY_SUBSCR    
               32  STORE_FAST               'item_offset'

 L. 443        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _offset_data_start
               38  LOAD_FAST                'item_offset'
               40  BINARY_ADD       
               42  STORE_FAST               'offset'

 L. 444        44  LOAD_FAST                'self'
               46  LOAD_METHOD              _get_packing_format
               48  LOAD_FAST                'position'
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'current_format'
               54  POP_BLOCK        
               56  JUMP_FORWARD         84  'to 84'
             58_0  COME_FROM_FINALLY    22  '22'

 L. 445        58  DUP_TOP          
               60  LOAD_GLOBAL              IndexError
               62  <121>                82  ''
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 446        70  LOAD_GLOBAL              IndexError
               72  LOAD_STR                 'assignment index out of range'
               74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
               78  POP_EXCEPT       
               80  JUMP_FORWARD         84  'to 84'
               82  <48>             
             84_0  COME_FROM            80  '80'
             84_1  COME_FROM            56  '56'

 L. 448        84  LOAD_GLOBAL              isinstance
               86  LOAD_FAST                'value'
               88  LOAD_GLOBAL              str
               90  LOAD_GLOBAL              bytes
               92  BUILD_TUPLE_2         2 
               94  CALL_FUNCTION_2       2  ''
               96  POP_JUMP_IF_TRUE    118  'to 118'

 L. 449        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _types_mapping
              102  LOAD_GLOBAL              type
              104  LOAD_FAST                'value'
              106  CALL_FUNCTION_1       1  ''
              108  BINARY_SUBSCR    
              110  STORE_FAST               'new_format'

 L. 450       112  LOAD_FAST                'value'
              114  STORE_FAST               'encoded_value'
              116  JUMP_FORWARD        214  'to 214'
            118_0  COME_FROM            96  '96'

 L. 452       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _allocated_offsets
              122  LOAD_FAST                'position'
              124  LOAD_CONST               1
              126  BINARY_ADD       
              128  BINARY_SUBSCR    
              130  LOAD_FAST                'item_offset'
              132  BINARY_SUBTRACT  
              134  STORE_FAST               'allocated_length'

 L. 455       136  LOAD_GLOBAL              isinstance
              138  LOAD_FAST                'value'
              140  LOAD_GLOBAL              str
              142  CALL_FUNCTION_2       2  ''

 L. 454       144  POP_JUMP_IF_FALSE   156  'to 156'
              146  LOAD_FAST                'value'
              148  LOAD_METHOD              encode
              150  LOAD_GLOBAL              _encoding
              152  CALL_METHOD_1         1  ''
              154  JUMP_FORWARD        158  'to 158'
            156_0  COME_FROM           144  '144'

 L. 455       156  LOAD_FAST                'value'
            158_0  COME_FROM           154  '154'

 L. 454       158  STORE_FAST               'encoded_value'

 L. 456       160  LOAD_GLOBAL              len
              162  LOAD_FAST                'encoded_value'
              164  CALL_FUNCTION_1       1  ''
              166  LOAD_FAST                'allocated_length'
              168  COMPARE_OP               >
              170  POP_JUMP_IF_FALSE   180  'to 180'

 L. 457       172  LOAD_GLOBAL              ValueError
              174  LOAD_STR                 'bytes/str item exceeds available storage'
              176  CALL_FUNCTION_1       1  ''
              178  RAISE_VARARGS_1       1  'exception instance'
            180_0  COME_FROM           170  '170'

 L. 458       180  LOAD_FAST                'current_format'
              182  LOAD_CONST               -1
              184  BINARY_SUBSCR    
              186  LOAD_STR                 's'
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   198  'to 198'

 L. 459       192  LOAD_FAST                'current_format'
              194  STORE_FAST               'new_format'
              196  JUMP_FORWARD        214  'to 214'
            198_0  COME_FROM           190  '190'

 L. 461       198  LOAD_FAST                'self'
              200  LOAD_ATTR                _types_mapping
              202  LOAD_GLOBAL              str
              204  BINARY_SUBSCR    

 L. 462       206  LOAD_FAST                'allocated_length'

 L. 461       208  BUILD_TUPLE_1         1 
              210  BINARY_MODULO    
              212  STORE_FAST               'new_format'
            214_0  COME_FROM           196  '196'
            214_1  COME_FROM           116  '116'

 L. 465       214  LOAD_FAST                'self'
              216  LOAD_METHOD              _set_packing_format_and_transform

 L. 466       218  LOAD_FAST                'position'

 L. 467       220  LOAD_FAST                'new_format'

 L. 468       222  LOAD_FAST                'value'

 L. 465       224  CALL_METHOD_3         3  ''
              226  POP_TOP          

 L. 470       228  LOAD_GLOBAL              struct
              230  LOAD_METHOD              pack_into
              232  LOAD_FAST                'new_format'
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                shm
              238  LOAD_ATTR                buf
              240  LOAD_FAST                'offset'
              242  LOAD_FAST                'encoded_value'
              244  CALL_METHOD_4         4  ''
              246  POP_TOP          

Parse error at or near `<121>' instruction at offset 62

    def __reduce__(self):
        return (
         partial((self.__class__), name=(self.shm.name)), ())

    def __len__(self):
        return struct.unpack_from'q'self.shm.buf0[0]

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self)}, name={self.shm.name!r})"

    @property
    def format(self):
        """The struct packing format used by all currently stored items."""
        return ''.join(self._get_packing_formati for i in range(self._list_len))

    @property
    def _format_size_metainfo(self):
        """The struct packing format used for the items' storage offsets."""
        return 'q' * (self._list_len + 1)

    @property
    def _format_packing_metainfo(self):
        """The struct packing format used for the items' packing formats."""
        return '8s' * self._list_len

    @property
    def _format_back_transform_codes(self):
        """The struct packing format used for the items' back transforms."""
        return 'b' * self._list_len

    @property
    def _offset_data_start(self):
        return (self._list_len + 2) * 8

    @property
    def _offset_packing_formats(self):
        return self._offset_data_start + self._allocated_offsets[(-1)]

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

    __class_getitem__ = classmethod(types.GenericAlias)