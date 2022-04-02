# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: requests\packages\chardet\__init__.py
__version__ = '2.3.0'
from sys import version_info

def detect--- This code section failed: ---

 L.  23         0  LOAD_GLOBAL              version_info
                2  LOAD_CONST               (3, 0)
                4  COMPARE_OP               <
                6  POP_JUMP_IF_FALSE    18  'to 18'
                8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'aBuf'
               12  LOAD_GLOBAL              unicode
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     36  'to 36'
             18_0  COME_FROM             6  '6'

 L.  24        18  LOAD_GLOBAL              version_info
               20  LOAD_CONST               (3, 0)
               22  COMPARE_OP               >=

 L.  23        24  POP_JUMP_IF_FALSE    44  'to 44'

 L.  24        26  LOAD_GLOBAL              isinstance
               28  LOAD_FAST                'aBuf'
               30  LOAD_GLOBAL              bytes
               32  CALL_FUNCTION_2       2  ''

 L.  23        34  POP_JUMP_IF_TRUE     44  'to 44'
             36_0  COME_FROM            16  '16'

 L.  25        36  LOAD_GLOBAL              ValueError
               38  LOAD_STR                 'Expected a bytes object, not a unicode object'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'
             44_1  COME_FROM            24  '24'

 L.  27        44  LOAD_CONST               1
               46  LOAD_CONST               ('universaldetector',)
               48  IMPORT_NAME              
               50  IMPORT_FROM              universaldetector
               52  STORE_FAST               'universaldetector'
               54  POP_TOP          

 L.  28        56  LOAD_FAST                'universaldetector'
               58  LOAD_METHOD              UniversalDetector
               60  CALL_METHOD_0         0  ''
               62  STORE_FAST               'u'

 L.  29        64  LOAD_FAST                'u'
               66  LOAD_METHOD              reset
               68  CALL_METHOD_0         0  ''
               70  POP_TOP          

 L.  30        72  LOAD_FAST                'u'
               74  LOAD_METHOD              feed
               76  LOAD_FAST                'aBuf'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L.  31        82  LOAD_FAST                'u'
               84  LOAD_METHOD              close
               86  CALL_METHOD_0         0  ''
               88  POP_TOP          

 L.  32        90  LOAD_FAST                'u'
               92  LOAD_ATTR                result
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 94