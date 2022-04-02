# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: requests\packages\idna\intranges.py
"""
Given a list of integers, made up of (hopefully) a small number of long runs
of consecutive integers, compute a representation of the form
((start1, end1), (start2, end2) ...). Then answer the question "was x present
in the original list?" in time O(log(# runs)).
"""
import bisect

def intranges_from_list--- This code section failed: ---

 L.  16         0  LOAD_GLOBAL              sorted
                2  LOAD_FAST                'list_'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'sorted_list'

 L.  17         8  BUILD_LIST_0          0 
               10  STORE_FAST               'ranges'

 L.  18        12  LOAD_CONST               -1
               14  STORE_FAST               'last_write'

 L.  19        16  LOAD_GLOBAL              range
               18  LOAD_GLOBAL              len
               20  LOAD_FAST                'sorted_list'
               22  CALL_FUNCTION_1       1  ''
               24  CALL_FUNCTION_1       1  ''
               26  GET_ITER         
             28_0  COME_FROM           128  '128'
             28_1  COME_FROM            72  '72'
               28  FOR_ITER            130  'to 130'
               30  STORE_FAST               'i'

 L.  20        32  LOAD_FAST                'i'
               34  LOAD_CONST               1
               36  BINARY_ADD       
               38  LOAD_GLOBAL              len
               40  LOAD_FAST                'sorted_list'
               42  CALL_FUNCTION_1       1  ''
               44  COMPARE_OP               <
               46  POP_JUMP_IF_FALSE    74  'to 74'

 L.  21        48  LOAD_FAST                'sorted_list'
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

 L.  22        72  JUMP_BACK            28  'to 28'
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            46  '46'

 L.  23        74  LOAD_FAST                'sorted_list'
               76  LOAD_FAST                'last_write'
               78  LOAD_CONST               1
               80  BINARY_ADD       
               82  LOAD_FAST                'i'
               84  LOAD_CONST               1
               86  BINARY_ADD       
               88  BUILD_SLICE_2         2 
               90  BINARY_SUBSCR    
               92  STORE_FAST               'current_range'

 L.  24        94  LOAD_FAST                'current_range'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  LOAD_FAST                'current_range'
              102  LOAD_CONST               -1
              104  BINARY_SUBSCR    
              106  LOAD_CONST               1
              108  BINARY_ADD       
              110  BUILD_TUPLE_2         2 
              112  STORE_FAST               'range_tuple'

 L.  25       114  LOAD_FAST                'ranges'
              116  LOAD_METHOD              append
              118  LOAD_FAST                'range_tuple'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L.  26       124  LOAD_FAST                'i'
              126  STORE_FAST               'last_write'
              128  JUMP_BACK            28  'to 28'
            130_0  COME_FROM            28  '28'

 L.  28       130  LOAD_GLOBAL              tuple
              132  LOAD_FAST                'ranges'
              134  CALL_FUNCTION_1       1  ''
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_GLOBAL' instruction at offset 130


def intranges_contain(int_, ranges):
    """Determine if `int_` falls into one of the ranges in `ranges`."""
    tuple_ = (
     int_, int_)
    pos = bisect.bisect_left(ranges, tuple_)
    if pos > 0:
        left, right = ranges[(pos - 1)]
        if left <= int_ < right:
            return True
    if pos < len(ranges):
        left, _ = ranges[pos]
        if left == int_:
            return True
    return False