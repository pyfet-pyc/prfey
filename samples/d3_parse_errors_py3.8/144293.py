# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\requests\packages\urllib3\util\response.py


def is_fp_closed--- This code section failed: ---

 L.   9         0  SETUP_FINALLY        10  'to 10'

 L.  11         2  LOAD_FAST                'obj'
                4  LOAD_ATTR                closed
                6  POP_BLOCK        
                8  RETURN_VALUE     
             10_0  COME_FROM_FINALLY     0  '0'

 L.  12        10  DUP_TOP          
               12  LOAD_GLOBAL              AttributeError
               14  COMPARE_OP               exception-match
               16  POP_JUMP_IF_FALSE    28  'to 28'
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L.  13        24  POP_EXCEPT       
               26  JUMP_FORWARD         30  'to 30'
             28_0  COME_FROM            16  '16'
               28  END_FINALLY      
             30_0  COME_FROM            26  '26'

 L.  15        30  SETUP_FINALLY        44  'to 44'

 L.  18        32  LOAD_FAST                'obj'
               34  LOAD_ATTR                fp
               36  LOAD_CONST               None
               38  COMPARE_OP               is
               40  POP_BLOCK        
               42  RETURN_VALUE     
             44_0  COME_FROM_FINALLY    30  '30'

 L.  19        44  DUP_TOP          
               46  LOAD_GLOBAL              AttributeError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    62  'to 62'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L.  20        58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
             62_0  COME_FROM            50  '50'
               62  END_FINALLY      
             64_0  COME_FROM            60  '60'

 L.  22        64  LOAD_GLOBAL              ValueError
               66  LOAD_STR                 'Unable to determine whether fp is closed.'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `COME_FROM' instruction at offset 28_0