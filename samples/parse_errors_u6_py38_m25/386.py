# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
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
               70  JUMP_ABSOLUTE        90  'to 90'
             72_0  COME_FROM            66  '66'

 L.  46        72  LOAD_FAST                'buf'
               74  LOAD_METHOD              close
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          
               80  JUMP_BACK            14  'to 14'

 L.  48        82  LOAD_GLOBAL              FileExistsError
               84  LOAD_STR                 'Cannot find name for new mmap'
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'

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

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 70

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
                return util.get_temp_dir()


    def reduce_arena(a):
        if a.fd == -1:
            raise ValueError('Arena is unpicklable because forking was enabled when it was created')
        return (rebuild_arena, (a.size, reduction.DupFd(a.fd)))


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
        return (arena, 0, length)

    def _discard_arena(self, arena):
        length = arena.size
        if length < self._DISCARD_FREE_SPACE_LARGER_THAN:
            return
        blocks = self._allocated_blocks.pop(arena)
        assert not blocks
        del self._start_to_block[(arena, 0)]
        del self._stop_to_block[(arena, length)]
        self._arenas.remove(arena)
        seq = self._len_to_seq[length]
        seq.remove((arena, 0, length))
        if not seq:
            del self._len_to_seq[length]
            self._lengths.remove(length)

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

    def _add_free_block(self, block):
        arena, start, stop = block
        try:
            prev_block = self._stop_to_block[(arena, start)]
        except KeyError:
            pass
        else:
            start, _ = self._absorb(prev_block)
        try:
            next_block = self._start_to_block[(arena, stop)]
        except KeyError:
            pass
        else:
            _, stop = self._absorb(next_block)
        block = (arena, start, stop)
        length = stop - start
        try:
            self._len_to_seq[length].append(block)
        except KeyError:
            self._len_to_seq[length] = [
             block]
            bisect.insort(self._lengths, length)
        else:
            self._start_to_block[(arena, start)] = block
            self._stop_to_block[(arena, stop)] = block

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
        return (start, stop)

    def _remove_allocated_block(self, block):
        arena, start, stop = block
        blocks = self._allocated_blocks[arena]
        blocks.remove((start, stop))
        if not blocks:
            self._discard_arena(arena)

    def _free_pending_blocks(self):
        while True:
            try:
                block = self._pending_free_blocks.pop()
            except IndexError:
                break
            else:
                self._add_free_block(block)
                self._remove_allocated_block(block)

    def free(self, block):
        if os.getpid() != self._lastpid:
            raise ValueError('My pid ({0:n}) is not last pid {1:n}'.format(os.getpid(), self._lastpid))
        elif not self._lock.acquire(False):
            self._pending_free_blocks.append(block)
        else:
            try:
                self._n_frees += 1
                self._free_pending_blocks()
                self._add_free_block(block)
                self._remove_allocated_block(block)
            finally:
                self._lock.release()

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
               72  SETUP_WITH          208  'to 208'
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
              198  BEGIN_FINALLY    
              200  WITH_CLEANUP_START
              202  WITH_CLEANUP_FINISH
              204  POP_FINALLY           0  ''
              206  RETURN_VALUE     
            208_0  COME_FROM_WITH       72  '72'
              208  WITH_CLEANUP_START
              210  WITH_CLEANUP_FINISH
              212  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 196


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