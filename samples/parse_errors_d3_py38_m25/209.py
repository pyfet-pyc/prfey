# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: distutils\dep_util.py
"""distutils.dep_util

Utility functions for simple, timestamp-based dependency of files
and groups of files; also, function based entirely on such
timestamp dependency analysis."""
import os
from distutils.errors import DistutilsFileError

def newer(source, target):
    """Return true if 'source' exists and is more recently modified than
    'target', or if 'source' exists and 'target' doesn't.  Return false if
    both exist and 'target' is the same age or younger than 'source'.
    Raise DistutilsFileError if 'source' does not exist.
    """
    if not os.path.exists(source):
        raise DistutilsFileError("file '%s' does not exist" % os.path.abspath(source))
    if not os.path.exists(target):
        return 1
    from stat import ST_MTIME
    mtime1 = os.stat(source)[ST_MTIME]
    mtime2 = os.stat(target)[ST_MTIME]
    return mtime1 > mtime2


def newer_pairwise(sources, targets):
    """Walk two filename lists in parallel, testing if each source is newer
    than its corresponding target.  Return a pair of lists (sources,
    targets) where source is newer than target, according to the semantics
    of 'newer()'.
    """
    if len(sources) != len(targets):
        raise ValueError("'sources' and 'targets' must be same length")
    n_sources = []
    n_targets = []
    for i in range(len(sources)):
        if newer(sources[i], targets[i]):
            n_sources.append(sources[i])
            n_targets.append(targets[i])
    else:
        return (
         n_sources, n_targets)


def newer_group--- This code section failed: ---

 L.  68         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              exists
                6  LOAD_FAST                'target'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L.  69        12  LOAD_CONST               1
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L.  75        16  LOAD_CONST               0
               18  LOAD_CONST               ('ST_MTIME',)
               20  IMPORT_NAME              stat
               22  IMPORT_FROM              ST_MTIME
               24  STORE_FAST               'ST_MTIME'
               26  POP_TOP          

 L.  76        28  LOAD_GLOBAL              os
               30  LOAD_METHOD              stat
               32  LOAD_FAST                'target'
               34  CALL_METHOD_1         1  ''
               36  LOAD_FAST                'ST_MTIME'
               38  BINARY_SUBSCR    
               40  STORE_FAST               'target_mtime'

 L.  77        42  LOAD_FAST                'sources'
               44  GET_ITER         
             46_0  COME_FROM           126  '126'
             46_1  COME_FROM           118  '118'
             46_2  COME_FROM            80  '80'
               46  FOR_ITER            128  'to 128'
               48  STORE_FAST               'source'

 L.  78        50  LOAD_GLOBAL              os
               52  LOAD_ATTR                path
               54  LOAD_METHOD              exists
               56  LOAD_FAST                'source'
               58  CALL_METHOD_1         1  ''
               60  POP_JUMP_IF_TRUE     98  'to 98'

 L.  79        62  LOAD_FAST                'missing'
               64  LOAD_STR                 'error'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    72  'to 72'

 L.  80        70  JUMP_FORWARD         98  'to 98'
             72_0  COME_FROM            68  '68'

 L.  81        72  LOAD_FAST                'missing'
               74  LOAD_STR                 'ignore'
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE    84  'to 84'

 L.  82        80  JUMP_BACK            46  'to 46'
               82  BREAK_LOOP           98  'to 98'
             84_0  COME_FROM            78  '78'

 L.  83        84  LOAD_FAST                'missing'
               86  LOAD_STR                 'newer'
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE    98  'to 98'

 L.  84        92  POP_TOP          
               94  LOAD_CONST               1
               96  RETURN_VALUE     
             98_0  COME_FROM            90  '90'
             98_1  COME_FROM            82  '82'
             98_2  COME_FROM            70  '70'
             98_3  COME_FROM            60  '60'

 L.  86        98  LOAD_GLOBAL              os
              100  LOAD_METHOD              stat
              102  LOAD_FAST                'source'
              104  CALL_METHOD_1         1  ''
              106  LOAD_FAST                'ST_MTIME'
              108  BINARY_SUBSCR    
              110  STORE_FAST               'source_mtime'

 L.  87       112  LOAD_FAST                'source_mtime'
              114  LOAD_FAST                'target_mtime'
              116  COMPARE_OP               >
              118  POP_JUMP_IF_FALSE_BACK    46  'to 46'

 L.  88       120  POP_TOP          
              122  LOAD_CONST               1
              124  RETURN_VALUE     
              126  JUMP_BACK            46  'to 46'
            128_0  COME_FROM            46  '46'

 L.  90       128  LOAD_CONST               0
              130  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 130