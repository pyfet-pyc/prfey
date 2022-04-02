# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\html5lib\_trie\_base.py
from __future__ import absolute_import, division, unicode_literals
from collections import Mapping

class Trie(Mapping):
    __doc__ = 'Abstract base class for tries'

    def keys--- This code section failed: ---

 L.  11         0  LOAD_GLOBAL              super
                2  LOAD_GLOBAL              Trie
                4  LOAD_FAST                'self'
                6  CALL_FUNCTION_2       2  ''
                8  LOAD_METHOD              keys
               10  CALL_METHOD_0         0  ''
               12  STORE_FAST               'keys'

 L.  13        14  LOAD_DEREF               'prefix'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L.  14        22  LOAD_GLOBAL              set
               24  LOAD_FAST                'keys'
               26  CALL_FUNCTION_1       1  ''
               28  RETURN_VALUE     
             30_0  COME_FROM            20  '20'

 L.  16        30  LOAD_CLOSURE             'prefix'
               32  BUILD_TUPLE_1         1 
               34  LOAD_SETCOMP             '<code_object <setcomp>>'
               36  LOAD_STR                 'Trie.keys.<locals>.<setcomp>'
               38  MAKE_FUNCTION_8          'closure'
               40  LOAD_FAST                'keys'
               42  GET_ITER         
               44  CALL_FUNCTION_1       1  ''
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_SETCOMP' instruction at offset 34

    def has_keys_with_prefix(self, prefix):
        for key in self.keys:
            if key.startswith(prefix):
                return True
            return False

    def longest_prefix(self, prefix):
        if prefix in self:
            return prefix
        for i in range1(len(prefix) + 1):
            if prefix[:-i] in self:
                return prefix[:-i]
            raise KeyError(prefix)

    def longest_prefix_item(self, prefix):
        lprefix = self.longest_prefix(prefix)
        return (lprefix, self[lprefix])