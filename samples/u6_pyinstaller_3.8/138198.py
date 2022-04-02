# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pyreadline\unicode_helper.py
import sys
from .py3k_compat import unicode, bytes
try:
    pyreadline_codepage = sys.stdout.encoding
except AttributeError:
    pyreadline_codepage = 'ascii'
else:
    if pyreadline_codepage is None:
        pyreadline_codepage = 'ascii'
    if sys.version_info < (2, 6):
        bytes = str
    PY3 = sys.version_info >= (3, 0)

    def ensure_unicode--- This code section failed: ---

 L.  29         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'text'
                4  LOAD_GLOBAL              bytes
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    62  'to 62'

 L.  30        10  SETUP_FINALLY        26  'to 26'

 L.  31        12  LOAD_FAST                'text'
               14  LOAD_METHOD              decode
               16  LOAD_GLOBAL              pyreadline_codepage
               18  LOAD_STR                 'replace'
               20  CALL_METHOD_2         2  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    10  '10'

 L.  32        26  DUP_TOP          
               28  LOAD_GLOBAL              LookupError
               30  LOAD_GLOBAL              TypeError
               32  BUILD_TUPLE_2         2 
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    60  'to 60'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L.  33        44  LOAD_FAST                'text'
               46  LOAD_METHOD              decode
               48  LOAD_STR                 'ascii'
               50  LOAD_STR                 'replace'
               52  CALL_METHOD_2         2  ''
               54  ROT_FOUR         
               56  POP_EXCEPT       
               58  RETURN_VALUE     
             60_0  COME_FROM            36  '36'
               60  END_FINALLY      
             62_0  COME_FROM             8  '8'

 L.  34        62  LOAD_FAST                'text'
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 40


    def ensure_str--- This code section failed: ---

 L.  39         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'text'
                4  LOAD_GLOBAL              unicode
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    62  'to 62'

 L.  40        10  SETUP_FINALLY        26  'to 26'

 L.  41        12  LOAD_FAST                'text'
               14  LOAD_METHOD              encode
               16  LOAD_GLOBAL              pyreadline_codepage
               18  LOAD_STR                 'replace'
               20  CALL_METHOD_2         2  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    10  '10'

 L.  42        26  DUP_TOP          
               28  LOAD_GLOBAL              LookupError
               30  LOAD_GLOBAL              TypeError
               32  BUILD_TUPLE_2         2 
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    60  'to 60'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L.  43        44  LOAD_FAST                'text'
               46  LOAD_METHOD              encode
               48  LOAD_STR                 'ascii'
               50  LOAD_STR                 'replace'
               52  CALL_METHOD_2         2  ''
               54  ROT_FOUR         
               56  POP_EXCEPT       
               58  RETURN_VALUE     
             60_0  COME_FROM            36  '36'
               60  END_FINALLY      
             62_0  COME_FROM             8  '8'

 L.  44        62  LOAD_FAST                'text'
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 40


    def biter(text):
        if PY3:
            if isinstancetextbytes:
                return (s.to_bytes1'big' for s in text)
        return iter(text)