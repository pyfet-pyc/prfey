# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: sqlite3\dump.py


def _iterdump--- This code section failed: ---

 L.  19         0  LOAD_FAST                'connection'
                2  LOAD_METHOD              cursor
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'cu'

 L.  20         8  LOAD_STR                 'BEGIN TRANSACTION;'
               10  YIELD_VALUE      
               12  POP_TOP          

 L.  23        14  LOAD_STR                 '\n        SELECT "name", "type", "sql"\n        FROM "sqlite_master"\n            WHERE "sql" NOT NULL AND\n            "type" == \'table\'\n            ORDER BY "name"\n        '
               16  STORE_FAST               'q'

 L.  30        18  LOAD_FAST                'cu'
               20  LOAD_METHOD              execute
               22  LOAD_FAST                'q'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'schema_res'

 L.  31        28  LOAD_FAST                'schema_res'
               30  LOAD_METHOD              fetchall
               32  CALL_METHOD_0         0  ''
               34  GET_ITER         
             36_0  COME_FROM           214  '214'
             36_1  COME_FROM            88  '88'
               36  FOR_ITER            216  'to 216'
               38  UNPACK_SEQUENCE_3     3 
               40  STORE_FAST               'table_name'
               42  STORE_FAST               'type'
               44  STORE_FAST               'sql'

 L.  32        46  LOAD_FAST                'table_name'
               48  LOAD_STR                 'sqlite_sequence'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L.  33        54  LOAD_STR                 'DELETE FROM "sqlite_sequence";'
               56  YIELD_VALUE      
               58  POP_TOP          
               60  JUMP_FORWARD        104  'to 104'
             62_0  COME_FROM            52  '52'

 L.  34        62  LOAD_FAST                'table_name'
               64  LOAD_STR                 'sqlite_stat1'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    78  'to 78'

 L.  35        70  LOAD_STR                 'ANALYZE "sqlite_master";'
               72  YIELD_VALUE      
               74  POP_TOP          
               76  JUMP_FORWARD        104  'to 104'
             78_0  COME_FROM            68  '68'

 L.  36        78  LOAD_FAST                'table_name'
               80  LOAD_METHOD              startswith
               82  LOAD_STR                 'sqlite_'
               84  CALL_METHOD_1         1  ''
               86  POP_JUMP_IF_FALSE    92  'to 92'

 L.  37        88  JUMP_BACK            36  'to 36'
               90  BREAK_LOOP          104  'to 104'
             92_0  COME_FROM            86  '86'

 L.  46        92  LOAD_STR                 '{0};'
               94  LOAD_METHOD              format
               96  LOAD_FAST                'sql'
               98  CALL_METHOD_1         1  ''
              100  YIELD_VALUE      
              102  POP_TOP          
            104_0  COME_FROM            90  '90'
            104_1  COME_FROM            76  '76'
            104_2  COME_FROM            60  '60'

 L.  49       104  LOAD_FAST                'table_name'
              106  LOAD_METHOD              replace
              108  LOAD_STR                 '"'
              110  LOAD_STR                 '""'
              112  CALL_METHOD_2         2  ''
              114  STORE_FAST               'table_name_ident'

 L.  50       116  LOAD_FAST                'cu'
              118  LOAD_METHOD              execute
              120  LOAD_STR                 'PRAGMA table_info("{0}")'
              122  LOAD_METHOD              format
              124  LOAD_FAST                'table_name_ident'
              126  CALL_METHOD_1         1  ''
              128  CALL_METHOD_1         1  ''
              130  STORE_FAST               'res'

 L.  51       132  LOAD_LISTCOMP            '<code_object <listcomp>>'
              134  LOAD_STR                 '_iterdump.<locals>.<listcomp>'
              136  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              138  LOAD_FAST                'res'
              140  LOAD_METHOD              fetchall
              142  CALL_METHOD_0         0  ''
              144  GET_ITER         
              146  CALL_FUNCTION_1       1  ''
              148  STORE_FAST               'column_names'

 L.  52       150  LOAD_STR                 'SELECT \'INSERT INTO "{0}" VALUES({1})\' FROM "{0}";'
              152  LOAD_METHOD              format

 L.  53       154  LOAD_FAST                'table_name_ident'

 L.  54       156  LOAD_STR                 ','
              158  LOAD_METHOD              join
              160  LOAD_GENEXPR             '<code_object <genexpr>>'
              162  LOAD_STR                 '_iterdump.<locals>.<genexpr>'
              164  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              166  LOAD_FAST                'column_names'
              168  GET_ITER         
              170  CALL_FUNCTION_1       1  ''
              172  CALL_METHOD_1         1  ''

 L.  52       174  CALL_METHOD_2         2  ''
              176  STORE_FAST               'q'

 L.  55       178  LOAD_FAST                'cu'
              180  LOAD_METHOD              execute
              182  LOAD_FAST                'q'
              184  CALL_METHOD_1         1  ''
              186  STORE_FAST               'query_res'

 L.  56       188  LOAD_FAST                'query_res'
              190  GET_ITER         
            192_0  COME_FROM           212  '212'
              192  FOR_ITER            214  'to 214'
              194  STORE_FAST               'row'

 L.  57       196  LOAD_STR                 '{0};'
              198  LOAD_METHOD              format
              200  LOAD_FAST                'row'
              202  LOAD_CONST               0
              204  BINARY_SUBSCR    
              206  CALL_METHOD_1         1  ''
              208  YIELD_VALUE      
              210  POP_TOP          
              212  JUMP_BACK           192  'to 192'
            214_0  COME_FROM           192  '192'
              214  JUMP_BACK            36  'to 36'
            216_0  COME_FROM            36  '36'

 L.  60       216  LOAD_STR                 '\n        SELECT "name", "type", "sql"\n        FROM "sqlite_master"\n            WHERE "sql" NOT NULL AND\n            "type" IN (\'index\', \'trigger\', \'view\')\n        '
              218  STORE_FAST               'q'

 L.  66       220  LOAD_FAST                'cu'
              222  LOAD_METHOD              execute
              224  LOAD_FAST                'q'
              226  CALL_METHOD_1         1  ''
              228  STORE_FAST               'schema_res'

 L.  67       230  LOAD_FAST                'schema_res'
              232  LOAD_METHOD              fetchall
              234  CALL_METHOD_0         0  ''
              236  GET_ITER         
            238_0  COME_FROM           260  '260'
              238  FOR_ITER            262  'to 262'
              240  UNPACK_SEQUENCE_3     3 
              242  STORE_FAST               'name'
              244  STORE_FAST               'type'
              246  STORE_FAST               'sql'

 L.  68       248  LOAD_STR                 '{0};'
              250  LOAD_METHOD              format
              252  LOAD_FAST                'sql'
              254  CALL_METHOD_1         1  ''
              256  YIELD_VALUE      
              258  POP_TOP          
              260  JUMP_BACK           238  'to 238'
            262_0  COME_FROM           238  '238'

 L.  70       262  LOAD_STR                 'COMMIT;'
              264  YIELD_VALUE      
              266  POP_TOP          

Parse error at or near `LOAD_STR' instruction at offset 216