# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: requests\hooks.py
"""
requests.hooks
~~~~~~~~~~~~~~

This module provides the capabilities for the Requests hooks system.

Available hooks:

``response``:
    The response generated from a Request.
"""
HOOKS = [
 'response']

def default_hooks():
    return {[]:event for event in HOOKS}


def dispatch_hook--- This code section failed: ---

 L.  25         0  LOAD_FAST                'hooks'
                2  JUMP_IF_TRUE_OR_POP     6  'to 6'
                4  BUILD_MAP_0           0 
              6_0  COME_FROM             2  '2'
                6  STORE_FAST               'hooks'

 L.  26         8  LOAD_FAST                'hooks'
               10  LOAD_METHOD              get
               12  LOAD_FAST                'key'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'hooks'

 L.  27        18  LOAD_FAST                'hooks'
               20  POP_JUMP_IF_FALSE    76  'to 76'

 L.  28        22  LOAD_GLOBAL              hasattr
               24  LOAD_FAST                'hooks'
               26  LOAD_STR                 '__call__'
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE    38  'to 38'

 L.  29        32  LOAD_FAST                'hooks'
               34  BUILD_LIST_1          1 
               36  STORE_FAST               'hooks'
             38_0  COME_FROM            30  '30'

 L.  30        38  LOAD_FAST                'hooks'
               40  GET_ITER         
             42_0  COME_FROM            68  '68'
               42  FOR_ITER             76  'to 76'
               44  STORE_FAST               'hook'

 L.  31        46  LOAD_FAST                'hook'
               48  LOAD_FAST                'hook_data'
               50  BUILD_TUPLE_1         1 
               52  BUILD_MAP_0           0 
               54  LOAD_FAST                'kwargs'
               56  <164>                 1  ''
               58  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               60  STORE_FAST               '_hook_data'

 L.  32        62  LOAD_FAST                '_hook_data'
               64  LOAD_CONST               None
               66  <117>                 1  ''
               68  POP_JUMP_IF_FALSE    42  'to 42'

 L.  33        70  LOAD_FAST                '_hook_data'
               72  STORE_FAST               'hook_data'
               74  JUMP_BACK            42  'to 42'
             76_0  COME_FROM            20  '20'

 L.  34        76  LOAD_FAST                'hook_data'
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 56