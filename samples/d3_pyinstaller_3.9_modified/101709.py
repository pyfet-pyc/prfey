# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: idna\intranges.py
"""
Given a list of integers, made up of (hopefully) a small number of long runs
of consecutive integers, compute a representation of the form
((start1, end1), (start2, end2) ...). Then answer the question "was x present
in the original list?" in time O(log(# runs)).
"""
import bisect

def intranges_from_list--- This code section failed: ---

 L.  18         0  LOAD_GLOBAL              sorted
                2  LOAD_FAST                'list_'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'sorted_list'

 L.  19         8  BUILD_LIST_0          0 
               10  STORE_FAST               'ranges'

 L.  20        12  LOAD_CONST               -1
               14  STORE_FAST               'last_write'

 L.  21        16  LOAD_GLOBAL              range
               18  LOAD_GLOBAL              len
               20  LOAD_FAST                'sorted_list'
               22  CALL_FUNCTION_1       1  ''
               24  CALL_FUNCTION_1       1  ''
               26  GET_ITER         
             28_0  COME_FROM           126  '126'
             28_1  COME_FROM            72  '72'
               28  FOR_ITER            128  'to 128'
               30  STORE_FAST               'i'

 L.  22        32  LOAD_FAST                'i'
               34  LOAD_CONST               1
               36  BINARY_ADD       
               38  LOAD_GLOBAL              len
               40  LOAD_FAST                'sorted_list'
               42  CALL_FUNCTION_1       1  ''
               44  COMPARE_OP               <
               46  POP_JUMP_IF_FALSE    74  'to 74'

 L.  23        48  LOAD_FAST                'sorted_list'
               50  LOAD_FAST                'i'
               52  BINARY_SUBSCR    
               54  LOAD_FAST                'sorted_list'
               56  LOAD_FAST                'i'
               58  LOAD_CONST               1
               60  BINARY_ADD       
               62  BINARY_SUBSCR    
               64  LOAD_CONST               1
               66  BINARY_SUBTRACT  
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    74  'to 74'

 L.  24        72  JUMP_BACK            28  'to 28'
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            46  '46'

 L.  25        74  LOAD_FAST                'sorted_list'
               76  LOAD_FAST                'last_write'
               78  LOAD_CONST               1
               80  BINARY_ADD       
               82  LOAD_FAST                'i'
               84  LOAD_CONST               1
               86  BINARY_ADD       
               88  BUILD_SLICE_2         2 
               90  BINARY_SUBSCR    
               92  STORE_FAST               'current_range'

 L.  26        94  LOAD_FAST                'ranges'
               96  LOAD_METHOD              append
               98  LOAD_GLOBAL              _encode_range
              100  LOAD_FAST                'current_range'
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'current_range'
              108  LOAD_CONST               -1
              110  BINARY_SUBSCR    
              112  LOAD_CONST               1
              114  BINARY_ADD       
              116  CALL_FUNCTION_2       2  ''
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L.  27       122  LOAD_FAST                'i'
              124  STORE_FAST               'last_write'
              126  JUMP_BACK            28  'to 28'
            128_0  COME_FROM            28  '28'

 L.  29       128  LOAD_GLOBAL              tuple
              130  LOAD_FAST                'ranges'
              132  CALL_FUNCTION_1       1  ''
              134  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_GLOBAL' instruction at offset 128


def _encode_range(start, end):
    return start << 32 | end


def _decode_range(r):
    return (
     r >> 32, r & 4294967295)


def intranges_contain(int_, ranges):
    """Determine if `int_` falls into one of the ranges in `ranges`."""
    tuple_ = _encode_rangeint_0
    pos = bisect.bisect_left(ranges, tuple_)
    if pos > 0:
        left, right = _decode_range(ranges[(pos - 1)])
        if left <= int_ < right:
            return True
    if pos < len(ranges):
        left, _ = _decode_range(ranges[pos])
        if left == int_:
            return True
    return False