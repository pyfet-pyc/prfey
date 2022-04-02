# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: tracemalloc.py
from collections.abc import Sequence, Iterable
from functools import total_ordering
import fnmatch, linecache, os.path, pickle
from _tracemalloc import *
from _tracemalloc import _get_object_traceback, _get_traces

def _format_size(size, sign):
    for unit in ('B', 'KiB', 'MiB', 'GiB', 'TiB'):
        if abs(size) < 100:
            if unit != 'B':
                if sign:
                    return '%+.1f %s' % (size, unit)
                return '%.1f %s' % (size, unit)
        if abs(size) < 10240 or unit == 'TiB':
            if sign:
                return '%+.0f %s' % (size, unit)
            else:
                return '%.0f %s' % (size, unit)
        else:
            size /= 1024


class Statistic:
    __doc__ = '\n    Statistic difference on memory allocations between two Snapshot instance.\n    '
    __slots__ = ('traceback', 'size', 'count')

    def __init__(self, traceback, size, count):
        self.traceback = traceback
        self.size = size
        self.count = count

    def __hash__(self):
        return hash((self.traceback, self.size, self.count))

    def __eq__(self, other):
        if not isinstance(other, Statistic):
            return NotImplemented
        return self.traceback == other.traceback and self.size == other.size and self.count == other.count

    def __str__(self):
        text = '%s: size=%s, count=%i' % (
         self.traceback,
         _format_size(self.size, False),
         self.count)
        if self.count:
            average = self.size / self.count
            text += ', average=%s' % _format_size(average, False)
        return text

    def __repr__(self):
        return '<Statistic traceback=%r size=%i count=%i>' % (
         self.traceback, self.size, self.count)

    def _sort_key(self):
        return (
         self.size, self.count, self.traceback)


class StatisticDiff:
    __doc__ = '\n    Statistic difference on memory allocations between an old and a new\n    Snapshot instance.\n    '
    __slots__ = ('traceback', 'size', 'size_diff', 'count', 'count_diff')

    def __init__(self, traceback, size, size_diff, count, count_diff):
        self.traceback = traceback
        self.size = size
        self.size_diff = size_diff
        self.count = count
        self.count_diff = count_diff

    def __hash__(self):
        return hash((self.traceback, self.size, self.size_diff,
         self.count, self.count_diff))

    def __eq__(self, other):
        if not isinstance(other, StatisticDiff):
            return NotImplemented
        return self.traceback == other.traceback and self.size == other.size and self.size_diff == other.size_diff and self.count == other.count and self.count_diff == other.count_diff

    def __str__(self):
        text = '%s: size=%s (%s), count=%i (%+i)' % (
         self.traceback,
         _format_size(self.size, False),
         _format_size(self.size_diff, True),
         self.count,
         self.count_diff)
        if self.count:
            average = self.size / self.count
            text += ', average=%s' % _format_size(average, False)
        return text

    def __repr__(self):
        return '<StatisticDiff traceback=%r size=%i (%+i) count=%i (%+i)>' % (
         self.traceback, self.size, self.size_diff,
         self.count, self.count_diff)

    def _sort_key(self):
        return (
         abs(self.size_diff), self.size,
         abs(self.count_diff), self.count,
         self.traceback)


def _compare_grouped_stats--- This code section failed: ---

 L. 121         0  BUILD_LIST_0          0 
                2  STORE_FAST               'statistics'

 L. 122         4  LOAD_FAST                'new_group'
                6  LOAD_METHOD              items
                8  CALL_METHOD_0         0  ''
               10  GET_ITER         
             12_0  COME_FROM           112  '112'
               12  FOR_ITER            114  'to 114'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'traceback'
               18  STORE_FAST               'stat'

 L. 123        20  LOAD_FAST                'old_group'
               22  LOAD_METHOD              pop
               24  LOAD_FAST                'traceback'
               26  LOAD_CONST               None
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'previous'

 L. 124        32  LOAD_FAST                'previous'
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    78  'to 78'

 L. 125        40  LOAD_GLOBAL              StatisticDiff
               42  LOAD_FAST                'traceback'

 L. 126        44  LOAD_FAST                'stat'
               46  LOAD_ATTR                size
               48  LOAD_FAST                'stat'
               50  LOAD_ATTR                size
               52  LOAD_FAST                'previous'
               54  LOAD_ATTR                size
               56  BINARY_SUBTRACT  

 L. 127        58  LOAD_FAST                'stat'
               60  LOAD_ATTR                count
               62  LOAD_FAST                'stat'
               64  LOAD_ATTR                count
               66  LOAD_FAST                'previous'
               68  LOAD_ATTR                count
               70  BINARY_SUBTRACT  

 L. 125        72  CALL_FUNCTION_5       5  ''
               74  STORE_FAST               'stat'
               76  JUMP_FORWARD        102  'to 102'
             78_0  COME_FROM            38  '38'

 L. 129        78  LOAD_GLOBAL              StatisticDiff
               80  LOAD_FAST                'traceback'

 L. 130        82  LOAD_FAST                'stat'
               84  LOAD_ATTR                size
               86  LOAD_FAST                'stat'
               88  LOAD_ATTR                size

 L. 131        90  LOAD_FAST                'stat'
               92  LOAD_ATTR                count
               94  LOAD_FAST                'stat'
               96  LOAD_ATTR                count

 L. 129        98  CALL_FUNCTION_5       5  ''
              100  STORE_FAST               'stat'
            102_0  COME_FROM            76  '76'

 L. 132       102  LOAD_FAST                'statistics'
              104  LOAD_METHOD              append
              106  LOAD_FAST                'stat'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
              112  JUMP_BACK            12  'to 12'
            114_0  COME_FROM            12  '12'

 L. 134       114  LOAD_FAST                'old_group'
              116  LOAD_METHOD              items
              118  CALL_METHOD_0         0  ''
              120  GET_ITER         
            122_0  COME_FROM           164  '164'
              122  FOR_ITER            166  'to 166'
              124  UNPACK_SEQUENCE_2     2 
              126  STORE_FAST               'traceback'
              128  STORE_FAST               'stat'

 L. 135       130  LOAD_GLOBAL              StatisticDiff
              132  LOAD_FAST                'traceback'
              134  LOAD_CONST               0
              136  LOAD_FAST                'stat'
              138  LOAD_ATTR                size
              140  UNARY_NEGATIVE   
              142  LOAD_CONST               0
              144  LOAD_FAST                'stat'
              146  LOAD_ATTR                count
              148  UNARY_NEGATIVE   
              150  CALL_FUNCTION_5       5  ''
              152  STORE_FAST               'stat'

 L. 136       154  LOAD_FAST                'statistics'
              156  LOAD_METHOD              append
              158  LOAD_FAST                'stat'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
              164  JUMP_BACK           122  'to 122'
            166_0  COME_FROM           122  '122'

 L. 137       166  LOAD_FAST                'statistics'
              168  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 36


@total_ordering
class Frame:
    __doc__ = '\n    Frame of a traceback.\n    '
    __slots__ = ('_frame', )

    def __init__(self, frame):
        self._frame = frame

    @property
    def filename(self):
        return self._frame[0]

    @property
    def lineno(self):
        return self._frame[1]

    def __eq__(self, other):
        if not isinstance(other, Frame):
            return NotImplemented
        return self._frame == other._frame

    def __lt__(self, other):
        if not isinstance(other, Frame):
            return NotImplemented
        return self._frame < other._frame

    def __hash__(self):
        return hash(self._frame)

    def __str__(self):
        return '%s:%s' % (self.filename, self.lineno)

    def __repr__(self):
        return '<Frame filename=%r lineno=%r>' % (self.filename, self.lineno)


@total_ordering
class Traceback(Sequence):
    __doc__ = '\n    Sequence of Frame instances sorted from the oldest frame\n    to the most recent frame.\n    '
    __slots__ = ('_frames', '_total_nframe')

    def __init__(self, frames, total_nframe=None):
        Sequence.__init__self
        self._frames = tuple(reversed(frames))
        self._total_nframe = total_nframe

    @property
    def total_nframe(self):
        return self._total_nframe

    def __len__(self):
        return len(self._frames)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return tuple((Frame(trace) for trace in self._frames[index]))
        return Frame(self._frames[index])

    def __contains__--- This code section failed: ---

 L. 210         0  LOAD_FAST                'frame'
                2  LOAD_ATTR                _frame
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _frames
                8  <118>                 0  ''
               10  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __hash__(self):
        return hash(self._frames)

    def __eq__(self, other):
        if not isinstance(other, Traceback):
            return NotImplemented
        return self._frames == other._frames

    def __lt__(self, other):
        if not isinstance(other, Traceback):
            return NotImplemented
        return self._frames < other._frames

    def __str__(self):
        return str(self[0])

    def __repr__--- This code section failed: ---

 L. 229         0  LOAD_STR                 '<Traceback '
                2  LOAD_GLOBAL              tuple
                4  LOAD_FAST                'self'
                6  CALL_FUNCTION_1       1  ''
                8  FORMAT_VALUE          0  ''
               10  BUILD_STRING_2        2 
               12  STORE_FAST               's'

 L. 230        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _total_nframe
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    34  'to 34'

 L. 231        24  LOAD_FAST                's'
               26  LOAD_STR                 '>'
               28  INPLACE_ADD      
               30  STORE_FAST               's'
               32  JUMP_FORWARD         52  'to 52'
             34_0  COME_FROM            22  '22'

 L. 233        34  LOAD_FAST                's'
               36  LOAD_STR                 ' total_nframe='
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                total_nframe
               42  FORMAT_VALUE          0  ''
               44  LOAD_STR                 '>'
               46  BUILD_STRING_3        3 
               48  INPLACE_ADD      
               50  STORE_FAST               's'
             52_0  COME_FROM            32  '32'

 L. 234        52  LOAD_FAST                's'
               54  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 20

    def format--- This code section failed: ---

 L. 237         0  BUILD_LIST_0          0 
                2  STORE_FAST               'lines'

 L. 238         4  LOAD_FAST                'limit'
                6  LOAD_CONST               None
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    50  'to 50'

 L. 239        12  LOAD_FAST                'limit'
               14  LOAD_CONST               0
               16  COMPARE_OP               >
               18  POP_JUMP_IF_FALSE    36  'to 36'

 L. 240        20  LOAD_FAST                'self'
               22  LOAD_FAST                'limit'
               24  UNARY_NEGATIVE   
               26  LOAD_CONST               None
               28  BUILD_SLICE_2         2 
               30  BINARY_SUBSCR    
               32  STORE_FAST               'frame_slice'
               34  JUMP_FORWARD         54  'to 54'
             36_0  COME_FROM            18  '18'

 L. 242        36  LOAD_FAST                'self'
               38  LOAD_CONST               None
               40  LOAD_FAST                'limit'
               42  BUILD_SLICE_2         2 
               44  BINARY_SUBSCR    
               46  STORE_FAST               'frame_slice'
               48  JUMP_FORWARD         54  'to 54'
             50_0  COME_FROM            10  '10'

 L. 244        50  LOAD_FAST                'self'
               52  STORE_FAST               'frame_slice'
             54_0  COME_FROM            48  '48'
             54_1  COME_FROM            34  '34'

 L. 246        54  LOAD_FAST                'most_recent_first'
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 247        58  LOAD_GLOBAL              reversed
               60  LOAD_FAST                'frame_slice'
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'frame_slice'
             66_0  COME_FROM            56  '56'

 L. 248        66  LOAD_FAST                'frame_slice'
               68  GET_ITER         
             70_0  COME_FROM           134  '134'
             70_1  COME_FROM           118  '118'
               70  FOR_ITER            136  'to 136'
               72  STORE_FAST               'frame'

 L. 249        74  LOAD_FAST                'lines'
               76  LOAD_METHOD              append
               78  LOAD_STR                 '  File "%s", line %s'

 L. 250        80  LOAD_FAST                'frame'
               82  LOAD_ATTR                filename
               84  LOAD_FAST                'frame'
               86  LOAD_ATTR                lineno
               88  BUILD_TUPLE_2         2 

 L. 249        90  BINARY_MODULO    
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          

 L. 251        96  LOAD_GLOBAL              linecache
               98  LOAD_METHOD              getline
              100  LOAD_FAST                'frame'
              102  LOAD_ATTR                filename
              104  LOAD_FAST                'frame'
              106  LOAD_ATTR                lineno
              108  CALL_METHOD_2         2  ''
              110  LOAD_METHOD              strip
              112  CALL_METHOD_0         0  ''
              114  STORE_FAST               'line'

 L. 252       116  LOAD_FAST                'line'
              118  POP_JUMP_IF_FALSE_BACK    70  'to 70'

 L. 253       120  LOAD_FAST                'lines'
              122  LOAD_METHOD              append
              124  LOAD_STR                 '    %s'
              126  LOAD_FAST                'line'
              128  BINARY_MODULO    
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          
              134  JUMP_BACK            70  'to 70'
            136_0  COME_FROM            70  '70'

 L. 254       136  LOAD_FAST                'lines'
              138  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 8


def get_object_traceback--- This code section failed: ---

 L. 265         0  LOAD_GLOBAL              _get_object_traceback
                2  LOAD_FAST                'obj'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'frames'

 L. 266         8  LOAD_FAST                'frames'
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 267        16  LOAD_GLOBAL              Traceback
               18  LOAD_FAST                'frames'
               20  CALL_FUNCTION_1       1  ''
               22  RETURN_VALUE     
             24_0  COME_FROM            14  '14'

 L. 269        24  LOAD_CONST               None
               26  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 12


class Trace:
    __doc__ = '\n    Trace of a memory block.\n    '
    __slots__ = ('_trace', )

    def __init__(self, trace):
        self._trace = trace

    @property
    def domain(self):
        return self._trace[0]

    @property
    def size(self):
        return self._trace[1]

    @property
    def traceback(self):
        return Traceback(*self._trace[2:])

    def __eq__(self, other):
        if not isinstance(other, Trace):
            return NotImplemented
        return self._trace == other._trace

    def __hash__(self):
        return hash(self._trace)

    def __str__(self):
        return '%s: %s' % (self.traceback, _format_size(self.size, False))

    def __repr__(self):
        return '<Trace domain=%s size=%s, traceback=%r>' % (
         self.domain, _format_size(self.size, False), self.traceback)


class _Traces(Sequence):

    def __init__(self, traces):
        Sequence.__init__self
        self._traces = traces

    def __len__(self):
        return len(self._traces)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return tuple((Trace(trace) for trace in self._traces[index]))
        return Trace(self._traces[index])

    def __contains__--- This code section failed: ---

 L. 327         0  LOAD_FAST                'trace'
                2  LOAD_ATTR                _trace
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _traces
                8  <118>                 0  ''
               10  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __eq__(self, other):
        if not isinstance(other, _Traces):
            return NotImplemented
        return self._traces == other._traces

    def __repr__(self):
        return '<Traces len=%s>' % len(self)


def _normalize_filename(filename):
    filename = os.path.normcasefilename
    if filename.endswith'.pyc':
        filename = filename[:-1]
    return filename


class BaseFilter:

    def __init__(self, inclusive):
        self.inclusive = inclusive

    def _match(self, trace):
        raise NotImplementedError


class Filter(BaseFilter):

    def __init__(self, inclusive, filename_pattern, lineno=None, all_frames=False, domain=None):
        super().__init__inclusive
        self.inclusive = inclusive
        self._filename_pattern = _normalize_filename(filename_pattern)
        self.lineno = lineno
        self.all_frames = all_frames
        self.domain = domain

    @property
    def filename_pattern(self):
        return self._filename_pattern

    def _match_frame_impl--- This code section failed: ---

 L. 368         0  LOAD_GLOBAL              _normalize_filename
                2  LOAD_FAST                'filename'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'filename'

 L. 369         8  LOAD_GLOBAL              fnmatch
               10  LOAD_METHOD              fnmatch
               12  LOAD_FAST                'filename'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _filename_pattern
               18  CALL_METHOD_2         2  ''
               20  POP_JUMP_IF_TRUE     26  'to 26'

 L. 370        22  LOAD_CONST               False
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 371        26  LOAD_FAST                'self'
               28  LOAD_ATTR                lineno
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L. 372        36  LOAD_CONST               True
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L. 374        40  LOAD_FAST                'lineno'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                lineno
               46  COMPARE_OP               ==
               48  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 32

    def _match_frame(self, filename, lineno):
        return self._match_frame_implfilenamelineno ^ (not self.inclusive)

    def _match_traceback(self, traceback):
        if self.all_frames:
            if any((self._match_frame_implfilenamelineno for filename, lineno in traceback)):
                return self.inclusive
            return not self.inclusive
        else:
            filename, lineno = traceback[0]
            return self._match_framefilenamelineno

    def _match--- This code section failed: ---

 L. 391         0  LOAD_FAST                'trace'
                2  UNPACK_SEQUENCE_4     4 
                4  STORE_FAST               'domain'
                6  STORE_FAST               'size'
                8  STORE_FAST               'traceback'
               10  STORE_FAST               'total_nframe'

 L. 392        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _match_traceback
               16  LOAD_FAST                'traceback'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'res'

 L. 393        22  LOAD_FAST                'self'
               24  LOAD_ATTR                domain
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    66  'to 66'

 L. 394        32  LOAD_FAST                'self'
               34  LOAD_ATTR                inclusive
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 395        38  LOAD_FAST                'res'
               40  JUMP_IF_FALSE_OR_POP    50  'to 50'
               42  LOAD_FAST                'domain'
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                domain
               48  COMPARE_OP               ==
             50_0  COME_FROM            40  '40'
               50  RETURN_VALUE     
             52_0  COME_FROM            36  '36'

 L. 397        52  LOAD_FAST                'res'
               54  JUMP_IF_TRUE_OR_POP    64  'to 64'
               56  LOAD_FAST                'domain'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                domain
               62  COMPARE_OP               !=
             64_0  COME_FROM            54  '54'
               64  RETURN_VALUE     
             66_0  COME_FROM            30  '30'

 L. 398        66  LOAD_FAST                'res'
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 28


class DomainFilter(BaseFilter):

    def __init__(self, inclusive, domain):
        super().__init__inclusive
        self._domain = domain

    @property
    def domain(self):
        return self._domain

    def _match(self, trace):
        domain, size, traceback, total_nframe = trace
        return (domain == self.domain) ^ (not self.inclusive)


class Snapshot:
    __doc__ = '\n    Snapshot of traces of memory blocks allocated by Python.\n    '

    def __init__(self, traces, traceback_limit):
        self.traces = _Traces(traces)
        self.traceback_limit = traceback_limit

    def dump--- This code section failed: ---

 L. 430         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'filename'
                4  LOAD_STR                 'wb'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           42  'to 42'
               10  STORE_FAST               'fp'

 L. 431        12  LOAD_GLOBAL              pickle
               14  LOAD_METHOD              dump
               16  LOAD_FAST                'self'
               18  LOAD_FAST                'fp'
               20  LOAD_GLOBAL              pickle
               22  LOAD_ATTR                HIGHEST_PROTOCOL
               24  CALL_METHOD_3         3  ''
               26  POP_TOP          
               28  POP_BLOCK        
               30  LOAD_CONST               None
               32  DUP_TOP          
               34  DUP_TOP          
               36  CALL_FUNCTION_3       3  ''
               38  POP_TOP          
               40  JUMP_FORWARD         58  'to 58'
             42_0  COME_FROM_WITH        8  '8'
               42  <49>             
               44  POP_JUMP_IF_TRUE     48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          
               54  POP_EXCEPT       
               56  POP_TOP          
             58_0  COME_FROM            40  '40'

Parse error at or near `DUP_TOP' instruction at offset 32

    @staticmethod
    def load--- This code section failed: ---

 L. 438         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'filename'
                4  LOAD_STR                 'rb'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           36  'to 36'
               10  STORE_FAST               'fp'

 L. 439        12  LOAD_GLOBAL              pickle
               14  LOAD_METHOD              load
               16  LOAD_FAST                'fp'
               18  CALL_METHOD_1         1  ''
               20  POP_BLOCK        
               22  ROT_TWO          
               24  LOAD_CONST               None
               26  DUP_TOP          
               28  DUP_TOP          
               30  CALL_FUNCTION_3       3  ''
               32  POP_TOP          
               34  RETURN_VALUE     
             36_0  COME_FROM_WITH        8  '8'
               36  <49>             
               38  POP_JUMP_IF_TRUE     42  'to 42'
               40  <48>             
             42_0  COME_FROM            38  '38'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          
               48  POP_EXCEPT       
               50  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 24

    def _filter_trace(self, include_filters, exclude_filters, trace):
        if include_filters:
            if not any((trace_filter._matchtrace for trace_filter in include_filters)):
                return False
            if exclude_filters:
                if any((not trace_filter._matchtrace for trace_filter in exclude_filters)):
                    return False
            return True

    def filter_traces(self, filters):
        """
        Create a new Snapshot instance with a filtered traces sequence, filters
        is a list of Filter or DomainFilter instances.  If filters is an empty
        list, return a new Snapshot instance with a copy of the traces.
        """
        if not isinstance(filters, Iterable):
            raise TypeError('filters must be a list of filters, not %s' % type(filters).__name__)
        if filters:
            include_filters = []
            exclude_filters = []
            for trace_filter in filters:
                if trace_filter.inclusive:
                    include_filters.appendtrace_filter
                else:
                    exclude_filters.appendtrace_filter
            else:
                new_traces = [trace for trace in self.traces._traces if self._filter_traceinclude_filtersexclude_filterstrace]

        else:
            new_traces = self.traces._traces.copy
        return Snapshot(new_traces, self.traceback_limit)

    def _group_by--- This code section failed: ---

 L. 478         0  LOAD_FAST                'key_type'
                2  LOAD_CONST               ('traceback', 'filename', 'lineno')
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 479         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'unknown key_type: %r'
               12  LOAD_FAST                'key_type'
               14  BUILD_TUPLE_1         1 
               16  BINARY_MODULO    
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM             6  '6'

 L. 480        22  LOAD_FAST                'cumulative'
               24  POP_JUMP_IF_FALSE    46  'to 46'
               26  LOAD_FAST                'key_type'
               28  LOAD_CONST               ('lineno', 'filename')
               30  <118>                 1  ''
               32  POP_JUMP_IF_FALSE    46  'to 46'

 L. 481        34  LOAD_GLOBAL              ValueError
               36  LOAD_STR                 'cumulative mode cannot by used with key type %r'

 L. 482        38  LOAD_FAST                'key_type'

 L. 481        40  BINARY_MODULO    
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            32  '32'
             46_1  COME_FROM            24  '24'

 L. 484        46  BUILD_MAP_0           0 
               48  STORE_FAST               'stats'

 L. 485        50  BUILD_MAP_0           0 
               52  STORE_FAST               'tracebacks'

 L. 486        54  LOAD_FAST                'cumulative'
            56_58  POP_JUMP_IF_TRUE    268  'to 268'

 L. 487        60  LOAD_FAST                'self'
               62  LOAD_ATTR                traces
               64  LOAD_ATTR                _traces
               66  GET_ITER         
             68_0  COME_FROM           264  '264'
             68_1  COME_FROM           260  '260'
             68_2  COME_FROM           226  '226'
               68  FOR_ITER            266  'to 266'
               70  STORE_FAST               'trace'

 L. 488        72  LOAD_FAST                'trace'
               74  UNPACK_SEQUENCE_4     4 
               76  STORE_FAST               'domain'
               78  STORE_FAST               'size'
               80  STORE_FAST               'trace_traceback'
               82  STORE_FAST               'total_nframe'

 L. 489        84  SETUP_FINALLY        98  'to 98'

 L. 490        86  LOAD_FAST                'tracebacks'
               88  LOAD_FAST                'trace_traceback'
               90  BINARY_SUBSCR    
               92  STORE_FAST               'traceback'
               94  POP_BLOCK        
               96  JUMP_FORWARD        186  'to 186'
             98_0  COME_FROM_FINALLY    84  '84'

 L. 491        98  DUP_TOP          
              100  LOAD_GLOBAL              KeyError
              102  <121>               184  ''
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 492       110  LOAD_FAST                'key_type'
              112  LOAD_STR                 'traceback'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   124  'to 124'

 L. 493       118  LOAD_FAST                'trace_traceback'
              120  STORE_FAST               'frames'
              122  JUMP_FORWARD        164  'to 164'
            124_0  COME_FROM           116  '116'

 L. 494       124  LOAD_FAST                'key_type'
              126  LOAD_STR                 'lineno'
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   146  'to 146'

 L. 495       132  LOAD_FAST                'trace_traceback'
              134  LOAD_CONST               None
              136  LOAD_CONST               1
              138  BUILD_SLICE_2         2 
              140  BINARY_SUBSCR    
              142  STORE_FAST               'frames'
              144  JUMP_FORWARD        164  'to 164'
            146_0  COME_FROM           130  '130'

 L. 497       146  LOAD_FAST                'trace_traceback'
              148  LOAD_CONST               0
              150  BINARY_SUBSCR    
              152  LOAD_CONST               0
              154  BINARY_SUBSCR    
              156  LOAD_CONST               0
              158  BUILD_TUPLE_2         2 
              160  BUILD_TUPLE_1         1 
              162  STORE_FAST               'frames'
            164_0  COME_FROM           144  '144'
            164_1  COME_FROM           122  '122'

 L. 498       164  LOAD_GLOBAL              Traceback
              166  LOAD_FAST                'frames'
              168  CALL_FUNCTION_1       1  ''
              170  STORE_FAST               'traceback'

 L. 499       172  LOAD_FAST                'traceback'
              174  LOAD_FAST                'tracebacks'
              176  LOAD_FAST                'trace_traceback'
              178  STORE_SUBSCR     
              180  POP_EXCEPT       
              182  JUMP_FORWARD        186  'to 186'
              184  <48>             
            186_0  COME_FROM           182  '182'
            186_1  COME_FROM            96  '96'

 L. 500       186  SETUP_FINALLY       228  'to 228'

 L. 501       188  LOAD_FAST                'stats'
              190  LOAD_FAST                'traceback'
              192  BINARY_SUBSCR    
              194  STORE_FAST               'stat'

 L. 502       196  LOAD_FAST                'stat'
              198  DUP_TOP          
              200  LOAD_ATTR                size
              202  LOAD_FAST                'size'
              204  INPLACE_ADD      
              206  ROT_TWO          
              208  STORE_ATTR               size

 L. 503       210  LOAD_FAST                'stat'
              212  DUP_TOP          
              214  LOAD_ATTR                count
              216  LOAD_CONST               1
              218  INPLACE_ADD      
              220  ROT_TWO          
              222  STORE_ATTR               count
              224  POP_BLOCK        
              226  JUMP_BACK            68  'to 68'
            228_0  COME_FROM_FINALLY   186  '186'

 L. 504       228  DUP_TOP          
              230  LOAD_GLOBAL              KeyError
          232_234  <121>               262  ''
              236  POP_TOP          
              238  POP_TOP          
              240  POP_TOP          

 L. 505       242  LOAD_GLOBAL              Statistic
              244  LOAD_FAST                'traceback'
              246  LOAD_FAST                'size'
              248  LOAD_CONST               1
              250  CALL_FUNCTION_3       3  ''
              252  LOAD_FAST                'stats'
              254  LOAD_FAST                'traceback'
              256  STORE_SUBSCR     
              258  POP_EXCEPT       
              260  JUMP_BACK            68  'to 68'
              262  <48>             
              264  JUMP_BACK            68  'to 68'
            266_0  COME_FROM            68  '68'
              266  JUMP_FORWARD        468  'to 468'
            268_0  COME_FROM            56  '56'

 L. 508       268  LOAD_FAST                'self'
              270  LOAD_ATTR                traces
              272  LOAD_ATTR                _traces
              274  GET_ITER         
            276_0  COME_FROM           464  '464'
              276  FOR_ITER            468  'to 468'
              278  STORE_FAST               'trace'

 L. 509       280  LOAD_FAST                'trace'
              282  UNPACK_SEQUENCE_4     4 
              284  STORE_FAST               'domain'
              286  STORE_FAST               'size'
              288  STORE_FAST               'trace_traceback'
              290  STORE_FAST               'total_nframe'

 L. 510       292  LOAD_FAST                'trace_traceback'
              294  GET_ITER         
            296_0  COME_FROM           460  '460'
            296_1  COME_FROM           456  '456'
            296_2  COME_FROM           422  '422'
              296  FOR_ITER            464  'to 464'
              298  STORE_FAST               'frame'

 L. 511       300  SETUP_FINALLY       314  'to 314'

 L. 512       302  LOAD_FAST                'tracebacks'
              304  LOAD_FAST                'frame'
              306  BINARY_SUBSCR    
              308  STORE_FAST               'traceback'
              310  POP_BLOCK        
              312  JUMP_FORWARD        382  'to 382'
            314_0  COME_FROM_FINALLY   300  '300'

 L. 513       314  DUP_TOP          
              316  LOAD_GLOBAL              KeyError
          318_320  <121>               380  ''
              322  POP_TOP          
              324  POP_TOP          
              326  POP_TOP          

 L. 514       328  LOAD_FAST                'key_type'
              330  LOAD_STR                 'lineno'
              332  COMPARE_OP               ==
          334_336  POP_JUMP_IF_FALSE   346  'to 346'

 L. 515       338  LOAD_FAST                'frame'
              340  BUILD_TUPLE_1         1 
              342  STORE_FAST               'frames'
              344  JUMP_FORWARD        360  'to 360'
            346_0  COME_FROM           334  '334'

 L. 517       346  LOAD_FAST                'frame'
              348  LOAD_CONST               0
              350  BINARY_SUBSCR    
              352  LOAD_CONST               0
              354  BUILD_TUPLE_2         2 
              356  BUILD_TUPLE_1         1 
              358  STORE_FAST               'frames'
            360_0  COME_FROM           344  '344'

 L. 518       360  LOAD_GLOBAL              Traceback
              362  LOAD_FAST                'frames'
              364  CALL_FUNCTION_1       1  ''
              366  STORE_FAST               'traceback'

 L. 519       368  LOAD_FAST                'traceback'
              370  LOAD_FAST                'tracebacks'
              372  LOAD_FAST                'frame'
              374  STORE_SUBSCR     
              376  POP_EXCEPT       
              378  JUMP_FORWARD        382  'to 382'
              380  <48>             
            382_0  COME_FROM           378  '378'
            382_1  COME_FROM           312  '312'

 L. 520       382  SETUP_FINALLY       424  'to 424'

 L. 521       384  LOAD_FAST                'stats'
              386  LOAD_FAST                'traceback'
              388  BINARY_SUBSCR    
              390  STORE_FAST               'stat'

 L. 522       392  LOAD_FAST                'stat'
              394  DUP_TOP          
              396  LOAD_ATTR                size
              398  LOAD_FAST                'size'
              400  INPLACE_ADD      
              402  ROT_TWO          
              404  STORE_ATTR               size

 L. 523       406  LOAD_FAST                'stat'
              408  DUP_TOP          
              410  LOAD_ATTR                count
              412  LOAD_CONST               1
              414  INPLACE_ADD      
              416  ROT_TWO          
              418  STORE_ATTR               count
              420  POP_BLOCK        
              422  JUMP_BACK           296  'to 296'
            424_0  COME_FROM_FINALLY   382  '382'

 L. 524       424  DUP_TOP          
              426  LOAD_GLOBAL              KeyError
          428_430  <121>               458  ''
              432  POP_TOP          
              434  POP_TOP          
              436  POP_TOP          

 L. 525       438  LOAD_GLOBAL              Statistic
              440  LOAD_FAST                'traceback'
              442  LOAD_FAST                'size'
              444  LOAD_CONST               1
              446  CALL_FUNCTION_3       3  ''
              448  LOAD_FAST                'stats'
              450  LOAD_FAST                'traceback'
              452  STORE_SUBSCR     
              454  POP_EXCEPT       
              456  JUMP_BACK           296  'to 296'
              458  <48>             
          460_462  JUMP_BACK           296  'to 296'
            464_0  COME_FROM           296  '296'
          464_466  JUMP_BACK           276  'to 276'
            468_0  COME_FROM           276  '276'
            468_1  COME_FROM           266  '266'

 L. 526       468  LOAD_FAST                'stats'
              470  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def statistics(self, key_type, cumulative=False):
        """
        Group statistics by key_type. Return a sorted list of Statistic
        instances.
        """
        grouped = self._group_bykey_typecumulative
        statistics = list(grouped.values)
        statistics.sort(reverse=True, key=(Statistic._sort_key))
        return statistics

    def compare_to(self, old_snapshot, key_type, cumulative=False):
        """
        Compute the differences with an old snapshot old_snapshot. Get
        statistics as a sorted list of StatisticDiff instances, grouped by
        group_by.
        """
        new_group = self._group_bykey_typecumulative
        old_group = old_snapshot._group_bykey_typecumulative
        statistics = _compare_grouped_stats(old_group, new_group)
        statistics.sort(reverse=True, key=(StatisticDiff._sort_key))
        return statistics


def take_snapshot():
    """
    Take a snapshot of traces of memory blocks allocated by Python.
    """
    if not is_tracing():
        raise RuntimeError('the tracemalloc module must be tracing memory allocations to take a snapshot')
    traces = _get_traces()
    traceback_limit = get_traceback_limit()
    return Snapshot(traces, traceback_limit)