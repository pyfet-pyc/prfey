# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: multiprocessing\heap.py
import bisect
from collections import defaultdict
import mmap, os, sys, tempfile, threading
from .context import reduction, assert_spawning
from . import util
__all__ = [
 'BufferWrapper']
if sys.platform == 'win32':
    import _winapi

    class Arena(object):
        __doc__ = '\n        A shared memory area backed by anonymous memory (Windows).\n        '
        _rand = tempfile._RandomNameSequence()

        def __init__--- This code section failed: ---

 L.  39         0  LOAD_FAST                'size'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               size

 L.  40         6  LOAD_GLOBAL              range
                8  LOAD_CONST               100
               10  CALL_FUNCTION_1       1  ''
               12  GET_ITER         
             14_0  COME_FROM            80  '80'
               14  FOR_ITER             82  'to 82'
               16  STORE_FAST               'i'

 L.  41        18  LOAD_STR                 'pym-%d-%s'
               20  LOAD_GLOBAL              os
               22  LOAD_METHOD              getpid
               24  CALL_METHOD_0         0  ''
               26  LOAD_GLOBAL              next
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _rand
               32  CALL_FUNCTION_1       1  ''
               34  BUILD_TUPLE_2         2 
               36  BINARY_MODULO    
               38  STORE_FAST               'name'

 L.  42        40  LOAD_GLOBAL              mmap
               42  LOAD_ATTR                mmap
               44  LOAD_CONST               -1
               46  LOAD_FAST                'size'
               48  LOAD_FAST                'name'
               50  LOAD_CONST               ('tagname',)
               52  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               54  STORE_FAST               'buf'

 L.  43        56  LOAD_GLOBAL              _winapi
               58  LOAD_METHOD              GetLastError
               60  CALL_METHOD_0         0  ''
               62  LOAD_CONST               0
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    72  'to 72'

 L.  44        68  POP_TOP          
               70  BREAK_LOOP           90  'to 90'
             72_0  COME_FROM            66  '66'

 L.  46        72  LOAD_FAST                'buf'
               74  LOAD_METHOD              close
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          
               80  JUMP_BACK            14  'to 14'
             82_0  COME_FROM            14  '14'

 L.  48        82  LOAD_GLOBAL              FileExistsError
               84  LOAD_STR                 'Cannot find name for new mmap'
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            70  '70'

 L.  49        90  LOAD_FAST                'name'
               92  LOAD_FAST                'self'
               94  STORE_ATTR               name

 L.  50        96  LOAD_FAST                'buf'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               buffer

 L.  51       102  LOAD_FAST                'self'
              104  LOAD_ATTR                size
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                name
              110  BUILD_TUPLE_2         2 
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _state

Parse error at or near `LOAD_FAST' instruction at offset 112

        def __getstate__(self):
            assert_spawning(self)
            return self._state

        def __setstate__(self, state):
            self.size, self.name = self._state = state
            self.buffer = mmap.mmap((-1), (self.size), tagname=(self.name))


else:

    class Arena(object):
        __doc__ = '\n        A shared memory area backed by a temporary file (POSIX).\n        '
        if sys.platform == 'linux':
            _dir_candidates = [
             '/dev/shm']
        else:
            _dir_candidates = []

        def __init__(self, size, fd=-1):
            self.size = size
            self.fd = fd
            if fd == -1:
                self.fd, name = tempfile.mkstemp(prefix=('pym-%d-' % os.getpid()),
                  dir=(self._choose_dir(size)))
                os.unlink(name)
                util.Finalize(self, os.close, (self.fd,))
                os.ftruncate(self.fd, size)
            self.buffer = mmap.mmap(self.fd, self.size)

        def _choose_dir(self, size):
            for d in self._dir_candidates:
                st = os.statvfs(d)
                if st.f_bavail * st.f_frsize >= size:
                    return d
            else:
                return util.get_temp_dir()


    def reduce_arena(a):
        if a.fd == -1:
            raise ValueError('Arena is unpicklable because forking was enabled when it was created')
        return (
         rebuild_arena, (a.size, reduction.DupFd(a.fd)))


    def rebuild_arena(size, dupfd):
        return Arena(size, dupfd.detach())


    reduction.register(Arena, reduce_arena)

class Heap(object):
    _alignment = 8
    _DISCARD_FREE_SPACE_LARGER_THAN = 4194304
    _DOUBLE_ARENA_SIZE_UNTIL = 4194304

    def __init__(self, size=mmap.PAGESIZE):
        self._lastpid = os.getpid()
        self._lock = threading.Lock()
        self._size = size
        self._lengths = []
        self._len_to_seq = {}
        self._start_to_block = {}
        self._stop_to_block = {}
        self._allocated_blocks = defaultdict(set)
        self._arenas = []
        self._pending_free_blocks = []
        self._n_mallocs = 0
        self._n_frees = 0

    @staticmethod
    def _roundup(n, alignment):
        mask = alignment - 1
        return n + mask & ~mask

    def _new_arena(self, size):
        length = self._roundup(max(self._size, size), mmap.PAGESIZE)
        if self._size < self._DOUBLE_ARENA_SIZE_UNTIL:
            self._size *= 2
        util.info('allocating a new mmap of length %d', length)
        arena = Arena(length)
        self._arenas.append(arena)
        return (
         arena, 0, length)

    def _discard_arena--- This code section failed: ---

 L. 172         0  LOAD_FAST                'arena'
                2  LOAD_ATTR                size
                4  STORE_FAST               'length'

 L. 175         6  LOAD_FAST                'length'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _DISCARD_FREE_SPACE_LARGER_THAN
               12  COMPARE_OP               <
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 176        16  LOAD_CONST               None
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 177        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _allocated_blocks
               24  LOAD_METHOD              pop
               26  LOAD_FAST                'arena'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'blocks'

 L. 178        32  LOAD_FAST                'blocks'
               34  POP_JUMP_IF_FALSE    40  'to 40'
               36  <74>             
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            34  '34'

 L. 179        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _start_to_block
               44  LOAD_FAST                'arena'
               46  LOAD_CONST               0
               48  BUILD_TUPLE_2         2 
               50  DELETE_SUBSCR    

 L. 180        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _stop_to_block
               56  LOAD_FAST                'arena'
               58  LOAD_FAST                'length'
               60  BUILD_TUPLE_2         2 
               62  DELETE_SUBSCR    

 L. 181        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _arenas
               68  LOAD_METHOD              remove
               70  LOAD_FAST                'arena'
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          

 L. 182        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _len_to_seq
               80  LOAD_FAST                'length'
               82  BINARY_SUBSCR    
               84  STORE_FAST               'seq'

 L. 183        86  LOAD_FAST                'seq'
               88  LOAD_METHOD              remove
               90  LOAD_FAST                'arena'
               92  LOAD_CONST               0
               94  LOAD_FAST                'length'
               96  BUILD_TUPLE_3         3 
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L. 184       102  LOAD_FAST                'seq'
              104  POP_JUMP_IF_TRUE    126  'to 126'

 L. 185       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _len_to_seq
              110  LOAD_FAST                'length'
              112  DELETE_SUBSCR    

 L. 186       114  LOAD_FAST                'self'
              116  LOAD_ATTR                _lengths
              118  LOAD_METHOD              remove
              120  LOAD_FAST                'length'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
            126_0  COME_FROM           104  '104'

Parse error at or near `<74>' instruction at offset 36

    def _malloc(self, size):
        i = bisect.bisect_left(self._lengths, size)
        if i == len(self._lengths):
            return self._new_arena(size)
        length = self._lengths[i]
        seq = self._len_to_seq[length]
        block = seq.pop()
        if not seq:
            del self._len_to_seq[length]
            del self._lengths[i]
        arena, start, stop = block
        del self._start_to_block[(arena, start)]
        del self._stop_to_block[(arena, stop)]
        return block

    def _add_free_block--- This code section failed: ---

 L. 207         0  LOAD_FAST                'block'
                2  UNPACK_SEQUENCE_3     3 
                4  STORE_FAST               'arena'
                6  STORE_FAST               'start'
                8  STORE_FAST               'stop'

 L. 209        10  SETUP_FINALLY        30  'to 30'

 L. 210        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _stop_to_block
               16  LOAD_FAST                'arena'
               18  LOAD_FAST                'start'
               20  BUILD_TUPLE_2         2 
               22  BINARY_SUBSCR    
               24  STORE_FAST               'prev_block'
               26  POP_BLOCK        
               28  JUMP_FORWARD         48  'to 48'
             30_0  COME_FROM_FINALLY    10  '10'

 L. 211        30  DUP_TOP          
               32  LOAD_GLOBAL              KeyError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 212        42  POP_EXCEPT       
               44  JUMP_FORWARD         62  'to 62'
               46  <48>             
             48_0  COME_FROM            28  '28'

 L. 214        48  LOAD_FAST                'self'
               50  LOAD_METHOD              _absorb
               52  LOAD_FAST                'prev_block'
               54  CALL_METHOD_1         1  ''
               56  UNPACK_SEQUENCE_2     2 
               58  STORE_FAST               'start'
               60  STORE_FAST               '_'
             62_0  COME_FROM            44  '44'

 L. 216        62  SETUP_FINALLY        82  'to 82'

 L. 217        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _start_to_block
               68  LOAD_FAST                'arena'
               70  LOAD_FAST                'stop'
               72  BUILD_TUPLE_2         2 
               74  BINARY_SUBSCR    
               76  STORE_FAST               'next_block'
               78  POP_BLOCK        
               80  JUMP_FORWARD        100  'to 100'
             82_0  COME_FROM_FINALLY    62  '62'

 L. 218        82  DUP_TOP          
               84  LOAD_GLOBAL              KeyError
               86  <121>                98  ''
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L. 219        94  POP_EXCEPT       
               96  JUMP_FORWARD        114  'to 114'
               98  <48>             
            100_0  COME_FROM            80  '80'

 L. 221       100  LOAD_FAST                'self'
              102  LOAD_METHOD              _absorb
              104  LOAD_FAST                'next_block'
              106  CALL_METHOD_1         1  ''
              108  UNPACK_SEQUENCE_2     2 
              110  STORE_FAST               '_'
              112  STORE_FAST               'stop'
            114_0  COME_FROM            96  '96'

 L. 223       114  LOAD_FAST                'arena'
              116  LOAD_FAST                'start'
              118  LOAD_FAST                'stop'
              120  BUILD_TUPLE_3         3 
              122  STORE_FAST               'block'

 L. 224       124  LOAD_FAST                'stop'
              126  LOAD_FAST                'start'
              128  BINARY_SUBTRACT  
              130  STORE_FAST               'length'

 L. 226       132  SETUP_FINALLY       154  'to 154'

 L. 227       134  LOAD_FAST                'self'
              136  LOAD_ATTR                _len_to_seq
              138  LOAD_FAST                'length'
              140  BINARY_SUBSCR    
              142  LOAD_METHOD              append
              144  LOAD_FAST                'block'
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          
              150  POP_BLOCK        
              152  JUMP_FORWARD        198  'to 198'
            154_0  COME_FROM_FINALLY   132  '132'

 L. 228       154  DUP_TOP          
              156  LOAD_GLOBAL              KeyError
              158  <121>               196  ''
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L. 229       166  LOAD_FAST                'block'
              168  BUILD_LIST_1          1 
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                _len_to_seq
              174  LOAD_FAST                'length'
              176  STORE_SUBSCR     

 L. 230       178  LOAD_GLOBAL              bisect
              180  LOAD_METHOD              insort
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                _lengths
              186  LOAD_FAST                'length'
              188  CALL_METHOD_2         2  ''
              190  POP_TOP          
              192  POP_EXCEPT       
              194  JUMP_FORWARD        198  'to 198'
              196  <48>             
            198_0  COME_FROM           194  '194'
            198_1  COME_FROM           152  '152'

 L. 232       198  LOAD_FAST                'block'
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                _start_to_block
              204  LOAD_FAST                'arena'
              206  LOAD_FAST                'start'
              208  BUILD_TUPLE_2         2 
              210  STORE_SUBSCR     

 L. 233       212  LOAD_FAST                'block'
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                _stop_to_block
              218  LOAD_FAST                'arena'
              220  LOAD_FAST                'stop'
              222  BUILD_TUPLE_2         2 
              224  STORE_SUBSCR     

Parse error at or near `<121>' instruction at offset 34

    def _absorb(self, block):
        arena, start, stop = block
        del self._start_to_block[(arena, start)]
        del self._stop_to_block[(arena, stop)]
        length = stop - start
        seq = self._len_to_seq[length]
        seq.remove(block)
        if not seq:
            del self._len_to_seq[length]
            self._lengths.remove(length)
        return (
         start, stop)

    def _remove_allocated_block(self, block):
        arena, start, stop = block
        blocks = self._allocated_blocks[arena]
        blocks.remove((start, stop))
        if not blocks:
            self._discard_arena(arena)

    def _free_pending_blocks--- This code section failed: ---
              0_0  COME_FROM            58  '58'

 L. 261         0  SETUP_FINALLY        16  'to 16'

 L. 262         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _pending_free_blocks
                6  LOAD_METHOD              pop
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'block'
               12  POP_BLOCK        
               14  JUMP_FORWARD         38  'to 38'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 263        16  DUP_TOP          
               18  LOAD_GLOBAL              IndexError
               20  <121>                36  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 264        28  POP_EXCEPT       
               30  BREAK_LOOP           60  'to 60'
               32  POP_EXCEPT       
               34  JUMP_FORWARD         38  'to 38'
               36  <48>             
             38_0  COME_FROM            34  '34'
             38_1  COME_FROM            14  '14'

 L. 265        38  LOAD_FAST                'self'
               40  LOAD_METHOD              _add_free_block
               42  LOAD_FAST                'block'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 266        48  LOAD_FAST                'self'
               50  LOAD_METHOD              _remove_allocated_block
               52  LOAD_FAST                'block'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          
               58  JUMP_BACK             0  'to 0'
             60_0  COME_FROM            30  '30'

Parse error at or near `<121>' instruction at offset 20

    def free--- This code section failed: ---

 L. 278         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              getpid
                4  CALL_METHOD_0         0  ''
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _lastpid
               10  COMPARE_OP               !=
               12  POP_JUMP_IF_FALSE    36  'to 36'

 L. 279        14  LOAD_GLOBAL              ValueError

 L. 280        16  LOAD_STR                 'My pid ({0:n}) is not last pid {1:n}'
               18  LOAD_METHOD              format

 L. 281        20  LOAD_GLOBAL              os
               22  LOAD_METHOD              getpid
               24  CALL_METHOD_0         0  ''
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _lastpid

 L. 280        30  CALL_METHOD_2         2  ''

 L. 279        32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            12  '12'

 L. 282        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _lock
               40  LOAD_METHOD              acquire
               42  LOAD_CONST               False
               44  CALL_METHOD_1         1  ''
               46  POP_JUMP_IF_TRUE     62  'to 62'

 L. 285        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _pending_free_blocks
               52  LOAD_METHOD              append
               54  LOAD_FAST                'block'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  JUMP_FORWARD        132  'to 132'
             62_0  COME_FROM            46  '46'

 L. 288        62  SETUP_FINALLY       120  'to 120'

 L. 289        64  LOAD_FAST                'self'
               66  DUP_TOP          
               68  LOAD_ATTR                _n_frees
               70  LOAD_CONST               1
               72  INPLACE_ADD      
               74  ROT_TWO          
               76  STORE_ATTR               _n_frees

 L. 290        78  LOAD_FAST                'self'
               80  LOAD_METHOD              _free_pending_blocks
               82  CALL_METHOD_0         0  ''
               84  POP_TOP          

 L. 291        86  LOAD_FAST                'self'
               88  LOAD_METHOD              _add_free_block
               90  LOAD_FAST                'block'
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          

 L. 292        96  LOAD_FAST                'self'
               98  LOAD_METHOD              _remove_allocated_block
              100  LOAD_FAST                'block'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          
              106  POP_BLOCK        

 L. 294       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _lock
              112  LOAD_METHOD              release
              114  CALL_METHOD_0         0  ''
              116  POP_TOP          
              118  JUMP_FORWARD        132  'to 132'
            120_0  COME_FROM_FINALLY    62  '62'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                _lock
              124  LOAD_METHOD              release
              126  CALL_METHOD_0         0  ''
              128  POP_TOP          
              130  <48>             
            132_0  COME_FROM           118  '118'
            132_1  COME_FROM            60  '60'

Parse error at or near `POP_TOP' instruction at offset 116

    def malloc--- This code section failed: ---

 L. 298         0  LOAD_FAST                'size'
                2  LOAD_CONST               0
                4  COMPARE_OP               <
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 299         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Size {0:n} out of range'
               12  LOAD_METHOD              format
               14  LOAD_FAST                'size'
               16  CALL_METHOD_1         1  ''
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM             6  '6'

 L. 300        22  LOAD_GLOBAL              sys
               24  LOAD_ATTR                maxsize
               26  LOAD_FAST                'size'
               28  COMPARE_OP               <=
               30  POP_JUMP_IF_FALSE    46  'to 46'

 L. 301        32  LOAD_GLOBAL              OverflowError
               34  LOAD_STR                 'Size {0:n} too large'
               36  LOAD_METHOD              format
               38  LOAD_FAST                'size'
               40  CALL_METHOD_1         1  ''
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            30  '30'

 L. 302        46  LOAD_GLOBAL              os
               48  LOAD_METHOD              getpid
               50  CALL_METHOD_0         0  ''
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _lastpid
               56  COMPARE_OP               !=
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L. 303        60  LOAD_FAST                'self'
               62  LOAD_METHOD              __init__
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          
             68_0  COME_FROM            58  '58'

 L. 304        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _lock
               72  SETUP_WITH          210  'to 210'
               74  POP_TOP          

 L. 305        76  LOAD_FAST                'self'
               78  DUP_TOP          
               80  LOAD_ATTR                _n_mallocs
               82  LOAD_CONST               1
               84  INPLACE_ADD      
               86  ROT_TWO          
               88  STORE_ATTR               _n_mallocs

 L. 307        90  LOAD_FAST                'self'
               92  LOAD_METHOD              _free_pending_blocks
               94  CALL_METHOD_0         0  ''
               96  POP_TOP          

 L. 308        98  LOAD_FAST                'self'
              100  LOAD_METHOD              _roundup
              102  LOAD_GLOBAL              max
              104  LOAD_FAST                'size'
              106  LOAD_CONST               1
              108  CALL_FUNCTION_2       2  ''
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                _alignment
              114  CALL_METHOD_2         2  ''
              116  STORE_FAST               'size'

 L. 309       118  LOAD_FAST                'self'
              120  LOAD_METHOD              _malloc
              122  LOAD_FAST                'size'
              124  CALL_METHOD_1         1  ''
              126  UNPACK_SEQUENCE_3     3 
              128  STORE_FAST               'arena'
              130  STORE_FAST               'start'
              132  STORE_FAST               'stop'

 L. 310       134  LOAD_FAST                'start'
              136  LOAD_FAST                'size'
              138  BINARY_ADD       
              140  STORE_FAST               'real_stop'

 L. 311       142  LOAD_FAST                'real_stop'
              144  LOAD_FAST                'stop'
              146  COMPARE_OP               <
              148  POP_JUMP_IF_FALSE   166  'to 166'

 L. 314       150  LOAD_FAST                'self'
              152  LOAD_METHOD              _add_free_block
              154  LOAD_FAST                'arena'
              156  LOAD_FAST                'real_stop'
              158  LOAD_FAST                'stop'
              160  BUILD_TUPLE_3         3 
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          
            166_0  COME_FROM           148  '148'

 L. 315       166  LOAD_FAST                'self'
              168  LOAD_ATTR                _allocated_blocks
              170  LOAD_FAST                'arena'
              172  BINARY_SUBSCR    
              174  LOAD_METHOD              add
              176  LOAD_FAST                'start'
              178  LOAD_FAST                'real_stop'
              180  BUILD_TUPLE_2         2 
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          

 L. 316       186  LOAD_FAST                'arena'
              188  LOAD_FAST                'start'
              190  LOAD_FAST                'real_stop'
              192  BUILD_TUPLE_3         3 
              194  POP_BLOCK        
              196  ROT_TWO          
              198  LOAD_CONST               None
              200  DUP_TOP          
              202  DUP_TOP          
              204  CALL_FUNCTION_3       3  ''
              206  POP_TOP          
              208  RETURN_VALUE     
            210_0  COME_FROM_WITH       72  '72'
              210  <49>             
              212  POP_JUMP_IF_TRUE    216  'to 216'
              214  <48>             
            216_0  COME_FROM           212  '212'
              216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          
              222  POP_EXCEPT       
              224  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 198


class BufferWrapper(object):
    _heap = Heap()

    def __init__(self, size):
        if size < 0:
            raise ValueError('Size {0:n} out of range'.format(size))
        if sys.maxsize <= size:
            raise OverflowError('Size {0:n} too large'.format(size))
        block = BufferWrapper._heap.malloc(size)
        self._state = (block, size)
        util.Finalize(self, (BufferWrapper._heap.free), args=(block,))

    def create_memoryview(self):
        (arena, start, stop), size = self._state
        return memoryview(arena.buffer)[start:start + size]