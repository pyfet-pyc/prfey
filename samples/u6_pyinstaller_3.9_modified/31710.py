# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pyasn1\codec\ber\eoo.py
from pyasn1.type import base
from pyasn1.type import tag
__all__ = [
 'endOfOctets']

class EndOfOctets(base.SimpleAsn1Type):
    defaultValue = 0
    tagSet = tag.initTagSet(tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 0))
    _instance = None

    def __new__--- This code section failed: ---

 L.  22         0  LOAD_FAST                'cls'
                2  LOAD_ATTR                _instance
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    36  'to 36'

 L.  23        10  LOAD_GLOBAL              object
               12  LOAD_ATTR                __new__
               14  LOAD_FAST                'cls'
               16  BUILD_LIST_1          1 
               18  LOAD_FAST                'args'
               20  CALL_FINALLY         23  'to 23'
               22  WITH_CLEANUP_FINISH
               24  BUILD_MAP_0           0 
               26  LOAD_FAST                'kwargs'
               28  <164>                 1  ''
               30  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               32  LOAD_FAST                'cls'
               34  STORE_ATTR               _instance
             36_0  COME_FROM             8  '8'

 L.  25        36  LOAD_FAST                'cls'
               38  LOAD_ATTR                _instance
               40  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


endOfOctets = EndOfOctets()