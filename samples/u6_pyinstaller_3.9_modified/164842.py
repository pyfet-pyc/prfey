# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: simplejson\errors.py
"""Error classes used by simplejson
"""
__all__ = [
 'JSONDecodeError']

def linecol(doc, pos):
    lineno = doc.count('\n', 0, pos) + 1
    if lineno == 1:
        colno = pos + 1
    else:
        colno = pos - doc.rindex('\n', 0, pos)
    return (
     lineno, colno)


def errmsg--- This code section failed: ---

 L.  16         0  LOAD_GLOBAL              linecol
                2  LOAD_FAST                'doc'
                4  LOAD_FAST                'pos'
                6  CALL_FUNCTION_2       2  ''
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'lineno'
               12  STORE_FAST               'colno'

 L.  17        14  LOAD_FAST                'msg'
               16  LOAD_METHOD              replace
               18  LOAD_STR                 '%r'
               20  LOAD_GLOBAL              repr
               22  LOAD_FAST                'doc'
               24  LOAD_FAST                'pos'
               26  LOAD_FAST                'pos'
               28  LOAD_CONST               1
               30  BINARY_ADD       
               32  BUILD_SLICE_2         2 
               34  BINARY_SUBSCR    
               36  CALL_FUNCTION_1       1  ''
               38  CALL_METHOD_2         2  ''
               40  STORE_FAST               'msg'

 L.  18        42  LOAD_FAST                'end'
               44  LOAD_CONST               None
               46  <117>                 0  ''
               48  POP_JUMP_IF_FALSE    70  'to 70'

 L.  19        50  LOAD_STR                 '%s: line %d column %d (char %d)'
               52  STORE_FAST               'fmt'

 L.  20        54  LOAD_FAST                'fmt'
               56  LOAD_FAST                'msg'
               58  LOAD_FAST                'lineno'
               60  LOAD_FAST                'colno'
               62  LOAD_FAST                'pos'
               64  BUILD_TUPLE_4         4 
               66  BINARY_MODULO    
               68  RETURN_VALUE     
             70_0  COME_FROM            48  '48'

 L.  21        70  LOAD_GLOBAL              linecol
               72  LOAD_FAST                'doc'
               74  LOAD_FAST                'end'
               76  CALL_FUNCTION_2       2  ''
               78  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST               'endlineno'
               82  STORE_FAST               'endcolno'

 L.  22        84  LOAD_STR                 '%s: line %d column %d - line %d column %d (char %d - %d)'
               86  STORE_FAST               'fmt'

 L.  23        88  LOAD_FAST                'fmt'
               90  LOAD_FAST                'msg'
               92  LOAD_FAST                'lineno'
               94  LOAD_FAST                'colno'
               96  LOAD_FAST                'endlineno'
               98  LOAD_FAST                'endcolno'
              100  LOAD_FAST                'pos'
              102  LOAD_FAST                'end'
              104  BUILD_TUPLE_7         7 
              106  BINARY_MODULO    
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 46


class JSONDecodeError(ValueError):
    __doc__ = 'Subclass of ValueError with the following additional properties:\n\n    msg: The unformatted error message\n    doc: The JSON document being parsed\n    pos: The start index of doc where parsing failed\n    end: The end index of doc where parsing failed (may be None)\n    lineno: The line corresponding to pos\n    colno: The column corresponding to pos\n    endlineno: The line corresponding to end (may be None)\n    endcolno: The column corresponding to end (may be None)\n\n    '

    def __init__--- This code section failed: ---

 L.  41         0  LOAD_GLOBAL              ValueError
                2  LOAD_METHOD              __init__
                4  LOAD_FAST                'self'
                6  LOAD_GLOBAL              errmsg
                8  LOAD_FAST                'msg'
               10  LOAD_FAST                'doc'
               12  LOAD_FAST                'pos'
               14  LOAD_FAST                'end'
               16  LOAD_CONST               ('end',)
               18  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               20  CALL_METHOD_2         2  ''
               22  POP_TOP          

 L.  42        24  LOAD_FAST                'msg'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               msg

 L.  43        30  LOAD_FAST                'doc'
               32  LOAD_FAST                'self'
               34  STORE_ATTR               doc

 L.  44        36  LOAD_FAST                'pos'
               38  LOAD_FAST                'self'
               40  STORE_ATTR               pos

 L.  45        42  LOAD_FAST                'end'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               end

 L.  46        48  LOAD_GLOBAL              linecol
               50  LOAD_FAST                'doc'
               52  LOAD_FAST                'pos'
               54  CALL_FUNCTION_2       2  ''
               56  UNPACK_SEQUENCE_2     2 
               58  LOAD_FAST                'self'
               60  STORE_ATTR               lineno
               62  LOAD_FAST                'self'
               64  STORE_ATTR               colno

 L.  47        66  LOAD_FAST                'end'
               68  LOAD_CONST               None
               70  <117>                 1  ''
               72  POP_JUMP_IF_FALSE    94  'to 94'

 L.  48        74  LOAD_GLOBAL              linecol
               76  LOAD_FAST                'doc'
               78  LOAD_FAST                'end'
               80  CALL_FUNCTION_2       2  ''
               82  UNPACK_SEQUENCE_2     2 
               84  LOAD_FAST                'self'
               86  STORE_ATTR               endlineno
               88  LOAD_FAST                'self'
               90  STORE_ATTR               endcolno
               92  JUMP_FORWARD        106  'to 106'
             94_0  COME_FROM            72  '72'

 L.  50        94  LOAD_CONST               (None, None)
               96  UNPACK_SEQUENCE_2     2 
               98  LOAD_FAST                'self'
              100  STORE_ATTR               endlineno
              102  LOAD_FAST                'self'
              104  STORE_ATTR               endcolno
            106_0  COME_FROM            92  '92'

Parse error at or near `<117>' instruction at offset 70

    def __reduce__(self):
        return (
         self.__class__, (self.msg, self.doc, self.pos, self.end))