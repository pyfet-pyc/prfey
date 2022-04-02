# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: attr\_version_info.py
from __future__ import absolute_import, division, print_function
from functools import total_ordering
from ._funcs import astuple
from ._make import attrib, attrs

@total_ordering
@attrs(eq=False, order=False, slots=True, frozen=True)
class VersionInfo(object):
    __doc__ = '\n    A version object that can be compared to tuple of length 1--4:\n\n    >>> attr.VersionInfo(19, 1, 0, "final")  <= (19, 2)\n    True\n    >>> attr.VersionInfo(19, 1, 0, "final") < (19, 1, 1)\n    True\n    >>> vi = attr.VersionInfo(19, 2, 0, "final")\n    >>> vi < (19, 1, 1)\n    False\n    >>> vi < (19,)\n    False\n    >>> vi == (19, 2,)\n    True\n    >>> vi == (19, 2, 1)\n    False\n\n    .. versionadded:: 19.2\n    '
    year = attrib(type=int)
    minor = attrib(type=int)
    micro = attrib(type=int)
    releaselevel = attrib(type=str)

    @classmethod
    def _from_version_string(cls, s):
        """
        Parse *s* and return a _VersionInfo.
        """
        v = s.split('.')
        if len(v) == 3:
            v.append('final')
        return cls(year=(int(v[0])),
          minor=(int(v[1])),
          micro=(int(v[2])),
          releaselevel=(v[3]))

    def _ensure_tuple--- This code section failed: ---

 L.  58         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  LOAD_FAST                'other'
                6  LOAD_ATTR                __class__
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  59        12  LOAD_GLOBAL              astuple
               14  LOAD_FAST                'other'
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'other'
             20_0  COME_FROM            10  '10'

 L.  61        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'other'
               24  LOAD_GLOBAL              tuple
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_TRUE     34  'to 34'

 L.  62        30  LOAD_GLOBAL              NotImplementedError
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            28  '28'

 L.  64        34  LOAD_CONST               1
               36  LOAD_GLOBAL              len
               38  LOAD_FAST                'other'
               40  CALL_FUNCTION_1       1  ''
               42  DUP_TOP          
               44  ROT_THREE        
               46  COMPARE_OP               <=
               48  POP_JUMP_IF_FALSE    58  'to 58'
               50  LOAD_CONST               4
               52  COMPARE_OP               <=
               54  POP_JUMP_IF_TRUE     64  'to 64'
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            48  '48'
               58  POP_TOP          
             60_0  COME_FROM            56  '56'

 L.  65        60  LOAD_GLOBAL              NotImplementedError
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            54  '54'

 L.  67        64  LOAD_GLOBAL              astuple
               66  LOAD_FAST                'self'
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_CONST               None
               72  LOAD_GLOBAL              len
               74  LOAD_FAST                'other'
               76  CALL_FUNCTION_1       1  ''
               78  BUILD_SLICE_2         2 
               80  BINARY_SUBSCR    
               82  LOAD_FAST                'other'
               84  BUILD_TUPLE_2         2 
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __eq__--- This code section failed: ---

 L.  70         0  SETUP_FINALLY        20  'to 20'

 L.  71         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _ensure_tuple
                6  LOAD_FAST                'other'
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'us'
               14  STORE_FAST               'them'
               16  POP_BLOCK        
               18  JUMP_FORWARD         42  'to 42'
             20_0  COME_FROM_FINALLY     0  '0'

 L.  72        20  DUP_TOP          
               22  LOAD_GLOBAL              NotImplementedError
               24  <121>                40  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  73        32  LOAD_GLOBAL              NotImplemented
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
               40  <48>             
             42_0  COME_FROM            18  '18'

 L.  75        42  LOAD_FAST                'us'
               44  LOAD_FAST                'them'
               46  COMPARE_OP               ==
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 24

    def __lt__--- This code section failed: ---

 L.  78         0  SETUP_FINALLY        20  'to 20'

 L.  79         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _ensure_tuple
                6  LOAD_FAST                'other'
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'us'
               14  STORE_FAST               'them'
               16  POP_BLOCK        
               18  JUMP_FORWARD         42  'to 42'
             20_0  COME_FROM_FINALLY     0  '0'

 L.  80        20  DUP_TOP          
               22  LOAD_GLOBAL              NotImplementedError
               24  <121>                40  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  81        32  LOAD_GLOBAL              NotImplemented
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
               40  <48>             
             42_0  COME_FROM            18  '18'

 L.  85        42  LOAD_FAST                'us'
               44  LOAD_FAST                'them'
               46  COMPARE_OP               <
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 24