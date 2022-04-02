# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pyasn1\type\tagmap.py
from pyasn1 import error
__all__ = [
 'TagMap']

class TagMap(object):
    __doc__ = 'Map *TagSet* objects to ASN.1 types\n\n    Create an object mapping *TagSet* object to ASN.1 type.\n\n    *TagMap* objects are immutable and duck-type read-only Python\n    :class:`dict` objects holding *TagSet* objects as keys and ASN.1\n    type objects as values.\n\n    Parameters\n    ----------\n    presentTypes: :py:class:`dict`\n        Map of :class:`~pyasn1.type.tag.TagSet` to ASN.1 objects considered\n        as being unconditionally present in the *TagMap*.\n\n    skipTypes: :py:class:`dict`\n        A collection of :class:`~pyasn1.type.tag.TagSet` objects considered\n        as absent in the *TagMap* even when *defaultType* is present.\n\n    defaultType: ASN.1 type object\n        An ASN.1 type object callee *TagMap* returns for any *TagSet* key not present\n        in *presentTypes* (unless given key is present in *skipTypes*).\n    '

    def __init__(self, presentTypes=None, skipTypes=None, defaultType=None):
        self._TagMap__presentTypes = presentTypes or {}
        self._TagMap__skipTypes = skipTypes or {}
        self._TagMap__defaultType = defaultType

    def __contains__--- This code section failed: ---

 L.  41         0  LOAD_FAST                'tagSet'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _TagMap__presentTypes
                6  <118>                 0  ''
                8  JUMP_IF_TRUE_OR_POP    28  'to 28'

 L.  42        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _TagMap__defaultType
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  JUMP_IF_FALSE_OR_POP    28  'to 28'
               20  LOAD_FAST                'tagSet'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _TagMap__skipTypes
               26  <118>                 1  ''
             28_0  COME_FROM            18  '18'
             28_1  COME_FROM             8  '8'

 L.  41        28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __getitem__--- This code section failed: ---

 L.  45         0  SETUP_FINALLY        14  'to 14'

 L.  46         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _TagMap__presentTypes
                6  LOAD_FAST                'tagSet'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  47        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  <121>                80  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  48        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _TagMap__defaultType
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L.  49        36  LOAD_GLOBAL              KeyError
               38  CALL_FUNCTION_0       0  ''
               40  RAISE_VARARGS_1       1  'exception instance'
               42  JUMP_FORWARD         76  'to 76'
             44_0  COME_FROM            34  '34'

 L.  50        44  LOAD_FAST                'tagSet'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _TagMap__skipTypes
               50  <118>                 0  ''
               52  POP_JUMP_IF_FALSE    66  'to 66'

 L.  51        54  LOAD_GLOBAL              error
               56  LOAD_METHOD              PyAsn1Error
               58  LOAD_STR                 'Key in negative map'
               60  CALL_METHOD_1         1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
               64  JUMP_FORWARD         76  'to 76'
             66_0  COME_FROM            52  '52'

 L.  53        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _TagMap__defaultType
               70  ROT_FOUR         
               72  POP_EXCEPT       
               74  RETURN_VALUE     
             76_0  COME_FROM            64  '64'
             76_1  COME_FROM            42  '42'
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
               80  <48>             
             82_0  COME_FROM            78  '78'

Parse error at or near `<121>' instruction at offset 18

    def __iter__(self):
        return iter(self._TagMap__presentTypes)

    def __repr__--- This code section failed: ---

 L.  59         0  LOAD_STR                 '%s object'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                __class__
                6  LOAD_ATTR                __name__
                8  BINARY_MODULO    
               10  STORE_FAST               'representation'

 L.  61        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _TagMap__presentTypes
               16  POP_JUMP_IF_FALSE    36  'to 36'

 L.  62        18  LOAD_FAST                'representation'
               20  LOAD_STR                 ', present %s'
               22  LOAD_GLOBAL              repr
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _TagMap__presentTypes
               28  CALL_FUNCTION_1       1  ''
               30  BINARY_MODULO    
               32  INPLACE_ADD      
               34  STORE_FAST               'representation'
             36_0  COME_FROM            16  '16'

 L.  64        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _TagMap__skipTypes
               40  POP_JUMP_IF_FALSE    60  'to 60'

 L.  65        42  LOAD_FAST                'representation'
               44  LOAD_STR                 ', skip %s'
               46  LOAD_GLOBAL              repr
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _TagMap__skipTypes
               52  CALL_FUNCTION_1       1  ''
               54  BINARY_MODULO    
               56  INPLACE_ADD      
               58  STORE_FAST               'representation'
             60_0  COME_FROM            40  '40'

 L.  67        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _TagMap__defaultType
               64  LOAD_CONST               None
               66  <117>                 1  ''
               68  POP_JUMP_IF_FALSE    88  'to 88'

 L.  68        70  LOAD_FAST                'representation'
               72  LOAD_STR                 ', default %s'
               74  LOAD_GLOBAL              repr
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                _TagMap__defaultType
               80  CALL_FUNCTION_1       1  ''
               82  BINARY_MODULO    
               84  INPLACE_ADD      
               86  STORE_FAST               'representation'
             88_0  COME_FROM            68  '68'

 L.  70        88  LOAD_STR                 '<%s>'
               90  LOAD_FAST                'representation'
               92  BINARY_MODULO    
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 66

    @property
    def presentTypes(self):
        """Return *TagSet* to ASN.1 type map present in callee *TagMap*"""
        return self._TagMap__presentTypes

    @property
    def skipTypes(self):
        """Return *TagSet* collection unconditionally absent in callee *TagMap*"""
        return self._TagMap__skipTypes

    @property
    def defaultType(self):
        """Return default ASN.1 type being returned for any missing *TagSet*"""
        return self._TagMap__defaultType

    def getPosMap(self):
        return self.presentTypes

    def getNegMap(self):
        return self.skipTypes

    def getDef(self):
        return self.defaultType