# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pycparser\ast_transforms.py
from . import c_ast

def fix_switch_cases--- This code section failed: ---

 L.  64         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'switch_node'
                4  LOAD_GLOBAL              c_ast
                6  LOAD_ATTR                Switch
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L.  65        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'switch_node'
               20  LOAD_ATTR                stmt
               22  LOAD_GLOBAL              c_ast
               24  LOAD_ATTR                Compound
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_TRUE     34  'to 34'

 L.  66        30  LOAD_FAST                'switch_node'
               32  RETURN_VALUE     
             34_0  COME_FROM            28  '28'

 L.  70        34  LOAD_GLOBAL              c_ast
               36  LOAD_METHOD              Compound
               38  BUILD_LIST_0          0 
               40  LOAD_FAST                'switch_node'
               42  LOAD_ATTR                stmt
               44  LOAD_ATTR                coord
               46  CALL_METHOD_2         2  ''
               48  STORE_FAST               'new_compound'

 L.  73        50  LOAD_CONST               None
               52  STORE_FAST               'last_case'

 L.  78        54  LOAD_FAST                'switch_node'
               56  LOAD_ATTR                stmt
               58  LOAD_ATTR                block_items
               60  JUMP_IF_TRUE_OR_POP    64  'to 64'
               62  BUILD_LIST_0          0 
             64_0  COME_FROM            60  '60'
               64  GET_ITER         
             66_0  COME_FROM           158  '158'
             66_1  COME_FROM           144  '144'
             66_2  COME_FROM           122  '122'
               66  FOR_ITER            160  'to 160'
               68  STORE_FAST               'child'

 L.  79        70  LOAD_GLOBAL              isinstance
               72  LOAD_FAST                'child'
               74  LOAD_GLOBAL              c_ast
               76  LOAD_ATTR                Case
               78  LOAD_GLOBAL              c_ast
               80  LOAD_ATTR                Default
               82  BUILD_TUPLE_2         2 
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_FALSE   124  'to 124'

 L.  84        88  LOAD_FAST                'new_compound'
               90  LOAD_ATTR                block_items
               92  LOAD_METHOD              append
               94  LOAD_FAST                'child'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L.  85       100  LOAD_GLOBAL              _extract_nested_case
              102  LOAD_FAST                'child'
              104  LOAD_FAST                'new_compound'
              106  LOAD_ATTR                block_items
              108  CALL_FUNCTION_2       2  ''
              110  POP_TOP          

 L.  86       112  LOAD_FAST                'new_compound'
              114  LOAD_ATTR                block_items
              116  LOAD_CONST               -1
              118  BINARY_SUBSCR    
              120  STORE_FAST               'last_case'
              122  JUMP_BACK            66  'to 66'
            124_0  COME_FROM            86  '86'

 L.  90       124  LOAD_FAST                'last_case'
              126  LOAD_CONST               None
              128  <117>                 0  ''
              130  POP_JUMP_IF_FALSE   146  'to 146'

 L.  91       132  LOAD_FAST                'new_compound'
              134  LOAD_ATTR                block_items
              136  LOAD_METHOD              append
              138  LOAD_FAST                'child'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  JUMP_BACK            66  'to 66'
            146_0  COME_FROM           130  '130'

 L.  93       146  LOAD_FAST                'last_case'
              148  LOAD_ATTR                stmts
              150  LOAD_METHOD              append
              152  LOAD_FAST                'child'
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          
              158  JUMP_BACK            66  'to 66'
            160_0  COME_FROM            66  '66'

 L.  95       160  LOAD_FAST                'new_compound'
              162  LOAD_FAST                'switch_node'
              164  STORE_ATTR               stmt

 L.  96       166  LOAD_FAST                'switch_node'
              168  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _extract_nested_case(case_node, stmts_list):
    """ Recursively extract consecutive Case statements that are made nested
        by the parser and add them to the stmts_list.
    """
    if isinstancecase_node.stmts[0](c_ast.Case, c_ast.Default):
        stmts_list.appendcase_node.stmts.pop()
        _extract_nested_casestmts_list[(-1)]stmts_list