# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\_vendor\packaging\utils.py
from __future__ import absolute_import, division, print_function
import re
from .version import InvalidVersion, Version
_canonicalize_regex = re.compile('[-_.]+')

def canonicalize_name(name):
    return _canonicalize_regex.sub('-', name).lower()


def canonicalize_version--- This code section failed: ---

 L.  25         0  SETUP_FINALLY        14  'to 14'

 L.  26         2  LOAD_GLOBAL              Version
                4  LOAD_FAST                'version'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'version'
               10  POP_BLOCK        
               12  JUMP_FORWARD         36  'to 36'
             14_0  COME_FROM_FINALLY     0  '0'

 L.  27        14  DUP_TOP          
               16  LOAD_GLOBAL              InvalidVersion
               18  <121>                34  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  29        26  LOAD_FAST                'version'
               28  ROT_FOUR         
               30  POP_EXCEPT       
               32  RETURN_VALUE     
               34  <48>             
             36_0  COME_FROM            12  '12'

 L.  31        36  BUILD_LIST_0          0 
               38  STORE_FAST               'parts'

 L.  34        40  LOAD_FAST                'version'
               42  LOAD_ATTR                epoch
               44  LOAD_CONST               0
               46  COMPARE_OP               !=
               48  POP_JUMP_IF_FALSE    68  'to 68'

 L.  35        50  LOAD_FAST                'parts'
               52  LOAD_METHOD              append
               54  LOAD_STR                 '{0}!'
               56  LOAD_METHOD              format
               58  LOAD_FAST                'version'
               60  LOAD_ATTR                epoch
               62  CALL_METHOD_1         1  ''
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          
             68_0  COME_FROM            48  '48'

 L.  39        68  LOAD_FAST                'parts'
               70  LOAD_METHOD              append
               72  LOAD_GLOBAL              re
               74  LOAD_METHOD              sub
               76  LOAD_STR                 '(\\.0)+$'
               78  LOAD_STR                 ''
               80  LOAD_STR                 '.'
               82  LOAD_METHOD              join
               84  LOAD_GENEXPR             '<code_object <genexpr>>'
               86  LOAD_STR                 'canonicalize_version.<locals>.<genexpr>'
               88  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               90  LOAD_FAST                'version'
               92  LOAD_ATTR                release
               94  GET_ITER         
               96  CALL_FUNCTION_1       1  ''
               98  CALL_METHOD_1         1  ''
              100  CALL_METHOD_3         3  ''
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L.  42       106  LOAD_FAST                'version'
              108  LOAD_ATTR                pre
              110  LOAD_CONST               None
              112  <117>                 1  ''
              114  POP_JUMP_IF_FALSE   144  'to 144'

 L.  43       116  LOAD_FAST                'parts'
              118  LOAD_METHOD              append
              120  LOAD_STR                 ''
              122  LOAD_METHOD              join
              124  LOAD_GENEXPR             '<code_object <genexpr>>'
              126  LOAD_STR                 'canonicalize_version.<locals>.<genexpr>'
              128  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              130  LOAD_FAST                'version'
              132  LOAD_ATTR                pre
              134  GET_ITER         
              136  CALL_FUNCTION_1       1  ''
              138  CALL_METHOD_1         1  ''
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM           114  '114'

 L.  46       144  LOAD_FAST                'version'
              146  LOAD_ATTR                post
              148  LOAD_CONST               None
              150  <117>                 1  ''
              152  POP_JUMP_IF_FALSE   172  'to 172'

 L.  47       154  LOAD_FAST                'parts'
              156  LOAD_METHOD              append
              158  LOAD_STR                 '.post{0}'
              160  LOAD_METHOD              format
              162  LOAD_FAST                'version'
              164  LOAD_ATTR                post
              166  CALL_METHOD_1         1  ''
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
            172_0  COME_FROM           152  '152'

 L.  50       172  LOAD_FAST                'version'
              174  LOAD_ATTR                dev
              176  LOAD_CONST               None
              178  <117>                 1  ''
              180  POP_JUMP_IF_FALSE   200  'to 200'

 L.  51       182  LOAD_FAST                'parts'
              184  LOAD_METHOD              append
              186  LOAD_STR                 '.dev{0}'
              188  LOAD_METHOD              format
              190  LOAD_FAST                'version'
              192  LOAD_ATTR                dev
              194  CALL_METHOD_1         1  ''
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          
            200_0  COME_FROM           180  '180'

 L.  54       200  LOAD_FAST                'version'
              202  LOAD_ATTR                local
              204  LOAD_CONST               None
              206  <117>                 1  ''
              208  POP_JUMP_IF_FALSE   228  'to 228'

 L.  55       210  LOAD_FAST                'parts'
              212  LOAD_METHOD              append
              214  LOAD_STR                 '+{0}'
              216  LOAD_METHOD              format
              218  LOAD_FAST                'version'
              220  LOAD_ATTR                local
              222  CALL_METHOD_1         1  ''
              224  CALL_METHOD_1         1  ''
              226  POP_TOP          
            228_0  COME_FROM           208  '208'

 L.  57       228  LOAD_STR                 ''
              230  LOAD_METHOD              join
              232  LOAD_FAST                'parts'
              234  CALL_METHOD_1         1  ''
              236  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 18