# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\distutils\command\install_headers.py
import os
import distutils.command.install_headers as old_install_headers

class install_headers(old_install_headers):

    def run--- This code section failed: ---

 L.   7         0  LOAD_FAST                'self'
                2  LOAD_ATTR                distribution
                4  LOAD_ATTR                headers
                6  STORE_FAST               'headers'

 L.   8         8  LOAD_FAST                'headers'
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L.   9        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L.  11        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              dirname
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                install_dir
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'prefix'

 L.  12        30  LOAD_FAST                'headers'
               32  GET_ITER         
               34  FOR_ITER            182  'to 182'
               36  STORE_FAST               'header'

 L.  13        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'header'
               42  LOAD_GLOBAL              tuple
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_FALSE   136  'to 136'

 L.  15        48  LOAD_FAST                'header'
               50  LOAD_CONST               0
               52  BINARY_SUBSCR    
               54  LOAD_STR                 'numpy.core'
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    98  'to 98'

 L.  16        60  LOAD_STR                 'numpy'
               62  LOAD_FAST                'header'
               64  LOAD_CONST               1
               66  BINARY_SUBSCR    
               68  BUILD_TUPLE_2         2 
               70  STORE_FAST               'header'

 L.  17        72  LOAD_GLOBAL              os
               74  LOAD_ATTR                path
               76  LOAD_METHOD              splitext
               78  LOAD_FAST                'header'
               80  LOAD_CONST               1
               82  BINARY_SUBSCR    
               84  CALL_METHOD_1         1  ''
               86  LOAD_CONST               1
               88  BINARY_SUBSCR    
               90  LOAD_STR                 '.inc'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L.  18        96  JUMP_BACK            34  'to 34'
             98_0  COME_FROM            94  '94'
             98_1  COME_FROM            58  '58'

 L.  19        98  LOAD_GLOBAL              os
              100  LOAD_ATTR                path
              102  LOAD_ATTR                join
              104  LOAD_FAST                'prefix'
              106  BUILD_LIST_1          1 
              108  LOAD_FAST                'header'
              110  LOAD_CONST               0
              112  BINARY_SUBSCR    
              114  LOAD_METHOD              split
              116  LOAD_STR                 '.'
              118  CALL_METHOD_1         1  ''
              120  BINARY_ADD       
              122  CALL_FUNCTION_EX      0  'positional arguments only'
              124  STORE_FAST               'd'

 L.  20       126  LOAD_FAST                'header'
              128  LOAD_CONST               1
              130  BINARY_SUBSCR    
              132  STORE_FAST               'header'
              134  JUMP_FORWARD        142  'to 142'
            136_0  COME_FROM            46  '46'

 L.  22       136  LOAD_FAST                'self'
              138  LOAD_ATTR                install_dir
              140  STORE_FAST               'd'
            142_0  COME_FROM           134  '134'

 L.  23       142  LOAD_FAST                'self'
              144  LOAD_METHOD              mkpath
              146  LOAD_FAST                'd'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          

 L.  24       152  LOAD_FAST                'self'
              154  LOAD_METHOD              copy_file
              156  LOAD_FAST                'header'
              158  LOAD_FAST                'd'
              160  CALL_METHOD_2         2  ''
              162  UNPACK_SEQUENCE_2     2 
              164  STORE_FAST               'out'
              166  STORE_FAST               '_'

 L.  25       168  LOAD_FAST                'self'
              170  LOAD_ATTR                outfiles
              172  LOAD_METHOD              append
              174  LOAD_FAST                'out'
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          
              180  JUMP_BACK            34  'to 34'

Parse error at or near `JUMP_FORWARD' instruction at offset 134