# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: email\contentmanager.py
import binascii, email.charset, email.message, email.errors
from email import quoprimime

class ContentManager:

    def __init__(self):
        self.get_handlers = {}
        self.set_handlers = {}

    def add_get_handler(self, key, handler):
        self.get_handlers[key] = handler

    def get_content--- This code section failed: ---

 L.  17         0  LOAD_FAST                'msg'
                2  LOAD_METHOD              get_content_type
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'content_type'

 L.  18         8  LOAD_FAST                'content_type'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                get_handlers
               14  <118>                 0  ''
               16  POP_JUMP_IF_FALSE    46  'to 46'

 L.  19        18  LOAD_FAST                'self'
               20  LOAD_ATTR                get_handlers
               22  LOAD_FAST                'content_type'
               24  BINARY_SUBSCR    
               26  LOAD_FAST                'msg'
               28  BUILD_LIST_1          1 
               30  LOAD_FAST                'args'
               32  CALL_FINALLY         35  'to 35'
               34  WITH_CLEANUP_FINISH
               36  BUILD_MAP_0           0 
               38  LOAD_FAST                'kw'
               40  <164>                 1  ''
               42  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               44  RETURN_VALUE     
             46_0  COME_FROM            16  '16'

 L.  20        46  LOAD_FAST                'msg'
               48  LOAD_METHOD              get_content_maintype
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'maintype'

 L.  21        54  LOAD_FAST                'maintype'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                get_handlers
               60  <118>                 0  ''
               62  POP_JUMP_IF_FALSE    92  'to 92'

 L.  22        64  LOAD_FAST                'self'
               66  LOAD_ATTR                get_handlers
               68  LOAD_FAST                'maintype'
               70  BINARY_SUBSCR    
               72  LOAD_FAST                'msg'
               74  BUILD_LIST_1          1 
               76  LOAD_FAST                'args'
               78  CALL_FINALLY         81  'to 81'
               80  WITH_CLEANUP_FINISH
               82  BUILD_MAP_0           0 
               84  LOAD_FAST                'kw'
               86  <164>                 1  ''
               88  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               90  RETURN_VALUE     
             92_0  COME_FROM            62  '62'

 L.  23        92  LOAD_STR                 ''
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                get_handlers
               98  <118>                 0  ''
              100  POP_JUMP_IF_FALSE   130  'to 130'

 L.  24       102  LOAD_FAST                'self'
              104  LOAD_ATTR                get_handlers
              106  LOAD_STR                 ''
              108  BINARY_SUBSCR    
              110  LOAD_FAST                'msg'
              112  BUILD_LIST_1          1 
              114  LOAD_FAST                'args'
              116  CALL_FINALLY        119  'to 119'
              118  WITH_CLEANUP_FINISH
              120  BUILD_MAP_0           0 
              122  LOAD_FAST                'kw'
              124  <164>                 1  ''
              126  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              128  RETURN_VALUE     
            130_0  COME_FROM           100  '100'

 L.  25       130  LOAD_GLOBAL              KeyError
              132  LOAD_FAST                'content_type'
              134  CALL_FUNCTION_1       1  ''
              136  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<118>' instruction at offset 14

    def add_set_handler(self, typekey, handler):
        self.set_handlers[typekey] = handler

    def set_content--- This code section failed: ---

 L.  31         0  LOAD_FAST                'msg'
                2  LOAD_METHOD              get_content_maintype
                4  CALL_METHOD_0         0  ''
                6  LOAD_STR                 'multipart'
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  34        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'set_content not valid on multipart'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L.  35        20  LOAD_FAST                'self'
               22  LOAD_METHOD              _find_set_handler
               24  LOAD_FAST                'msg'
               26  LOAD_FAST                'obj'
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'handler'

 L.  36        32  LOAD_FAST                'msg'
               34  LOAD_METHOD              clear_content
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          

 L.  37        40  LOAD_FAST                'handler'
               42  LOAD_FAST                'msg'
               44  LOAD_FAST                'obj'
               46  BUILD_LIST_2          2 
               48  LOAD_FAST                'args'
               50  CALL_FINALLY         53  'to 53'
               52  WITH_CLEANUP_FINISH
               54  BUILD_MAP_0           0 
               56  LOAD_FAST                'kw'
               58  <164>                 1  ''
               60  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               62  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 50

    def _find_set_handler--- This code section failed: ---

 L.  40         0  LOAD_CONST               None
                2  STORE_FAST               'full_path_for_error'

 L.  41         4  LOAD_GLOBAL              type
                6  LOAD_FAST                'obj'
                8  CALL_FUNCTION_1       1  ''
               10  LOAD_ATTR                __mro__
               12  GET_ITER         
             14_0  COME_FROM           156  '156'
               14  FOR_ITER            174  'to 174'
               16  STORE_FAST               'typ'

 L.  42        18  LOAD_FAST                'typ'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                set_handlers
               24  <118>                 0  ''
               26  POP_JUMP_IF_FALSE    42  'to 42'

 L.  43        28  LOAD_FAST                'self'
               30  LOAD_ATTR                set_handlers
               32  LOAD_FAST                'typ'
               34  BINARY_SUBSCR    
               36  ROT_TWO          
               38  POP_TOP          
               40  RETURN_VALUE     
             42_0  COME_FROM            26  '26'

 L.  44        42  LOAD_FAST                'typ'
               44  LOAD_ATTR                __qualname__
               46  STORE_FAST               'qname'

 L.  45        48  LOAD_GLOBAL              getattr
               50  LOAD_FAST                'typ'
               52  LOAD_STR                 '__module__'
               54  LOAD_STR                 ''
               56  CALL_FUNCTION_3       3  ''
               58  STORE_FAST               'modname'

 L.  46        60  LOAD_FAST                'modname'
               62  POP_JUMP_IF_FALSE    78  'to 78'
               64  LOAD_STR                 '.'
               66  LOAD_METHOD              join
               68  LOAD_FAST                'modname'
               70  LOAD_FAST                'qname'
               72  BUILD_TUPLE_2         2 
               74  CALL_METHOD_1         1  ''
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            62  '62'
               78  LOAD_FAST                'qname'
             80_0  COME_FROM            76  '76'
               80  STORE_FAST               'full_path'

 L.  47        82  LOAD_FAST                'full_path_for_error'
               84  LOAD_CONST               None
               86  <117>                 0  ''
               88  POP_JUMP_IF_FALSE    94  'to 94'

 L.  48        90  LOAD_FAST                'full_path'
               92  STORE_FAST               'full_path_for_error'
             94_0  COME_FROM            88  '88'

 L.  49        94  LOAD_FAST                'full_path'
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                set_handlers
              100  <118>                 0  ''
              102  POP_JUMP_IF_FALSE   118  'to 118'

 L.  50       104  LOAD_FAST                'self'
              106  LOAD_ATTR                set_handlers
              108  LOAD_FAST                'full_path'
              110  BINARY_SUBSCR    
              112  ROT_TWO          
              114  POP_TOP          
              116  RETURN_VALUE     
            118_0  COME_FROM           102  '102'

 L.  51       118  LOAD_FAST                'qname'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                set_handlers
              124  <118>                 0  ''
              126  POP_JUMP_IF_FALSE   142  'to 142'

 L.  52       128  LOAD_FAST                'self'
              130  LOAD_ATTR                set_handlers
              132  LOAD_FAST                'qname'
              134  BINARY_SUBSCR    
              136  ROT_TWO          
              138  POP_TOP          
              140  RETURN_VALUE     
            142_0  COME_FROM           126  '126'

 L.  53       142  LOAD_FAST                'typ'
              144  LOAD_ATTR                __name__
              146  STORE_FAST               'name'

 L.  54       148  LOAD_FAST                'name'
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                set_handlers
              154  <118>                 0  ''
              156  POP_JUMP_IF_FALSE    14  'to 14'

 L.  55       158  LOAD_FAST                'self'
              160  LOAD_ATTR                set_handlers
              162  LOAD_FAST                'name'
              164  BINARY_SUBSCR    
              166  ROT_TWO          
              168  POP_TOP          
              170  RETURN_VALUE     
              172  JUMP_BACK            14  'to 14'

 L.  56       174  LOAD_CONST               None
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                set_handlers
              180  <118>                 0  ''
              182  POP_JUMP_IF_FALSE   194  'to 194'

 L.  57       184  LOAD_FAST                'self'
              186  LOAD_ATTR                set_handlers
              188  LOAD_CONST               None
              190  BINARY_SUBSCR    
              192  RETURN_VALUE     
            194_0  COME_FROM           182  '182'

 L.  58       194  LOAD_GLOBAL              KeyError
              196  LOAD_FAST                'full_path_for_error'
              198  CALL_FUNCTION_1       1  ''
              200  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<118>' instruction at offset 24


raw_data_manager = ContentManager()

def get_text_content(msg, errors='replace'):
    content = msg.get_payload(decode=True)
    charset = msg.get_param('charset', 'ASCII')
    return content.decode(charset, errors=errors)


raw_data_manager.add_get_handler('text', get_text_content)

def get_non_text_content(msg):
    return msg.get_payload(decode=True)


for maintype in 'audio image video application'.split():
    raw_data_manager.add_get_handler(maintype, get_non_text_content)
else:

    def get_message_content(msg):
        return msg.get_payload0


    for subtype in 'rfc822 external-body'.split():
        raw_data_manager.add_get_handler('message/' + subtype, get_message_content)
    else:

        def get_and_fixup_unknown_message_content(msg):
            return bytes(msg.get_payload0)


        raw_data_manager.add_get_handler('message', get_and_fixup_unknown_message_content)

        def _prepare_set--- This code section failed: ---

 L.  96         0  LOAD_STR                 '/'
                2  LOAD_METHOD              join
                4  LOAD_FAST                'maintype'
                6  LOAD_FAST                'subtype'
                8  BUILD_TUPLE_2         2 
               10  CALL_METHOD_1         1  ''
               12  LOAD_FAST                'msg'
               14  LOAD_STR                 'Content-Type'
               16  STORE_SUBSCR     

 L.  97        18  LOAD_FAST                'headers'
               20  POP_JUMP_IF_FALSE   168  'to 168'

 L.  98        22  LOAD_GLOBAL              hasattr
               24  LOAD_FAST                'headers'
               26  LOAD_CONST               0
               28  BINARY_SUBSCR    
               30  LOAD_STR                 'name'
               32  CALL_FUNCTION_2       2  ''
               34  POP_JUMP_IF_TRUE     60  'to 60'

 L.  99        36  LOAD_FAST                'msg'
               38  LOAD_ATTR                policy
               40  STORE_DEREF              'mp'

 L. 100        42  LOAD_CLOSURE             'mp'
               44  BUILD_TUPLE_1         1 
               46  LOAD_LISTCOMP            '<code_object <listcomp>>'
               48  LOAD_STR                 '_prepare_set.<locals>.<listcomp>'
               50  MAKE_FUNCTION_8          'closure'

 L. 101        52  LOAD_FAST                'headers'

 L. 100        54  GET_ITER         
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'headers'
             60_0  COME_FROM            34  '34'

 L. 102        60  SETUP_FINALLY       102  'to 102'

 L. 103        62  LOAD_FAST                'headers'
               64  GET_ITER         
               66  FOR_ITER             98  'to 98'
               68  STORE_FAST               'header'

 L. 104        70  LOAD_FAST                'header'
               72  LOAD_ATTR                defects
               74  POP_JUMP_IF_FALSE    86  'to 86'

 L. 105        76  LOAD_FAST                'header'
               78  LOAD_ATTR                defects
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            74  '74'

 L. 106        86  LOAD_FAST                'header'
               88  LOAD_FAST                'msg'
               90  LOAD_FAST                'header'
               92  LOAD_ATTR                name
               94  STORE_SUBSCR     
               96  JUMP_BACK            66  'to 66'
               98  POP_BLOCK        
              100  JUMP_FORWARD        168  'to 168'
            102_0  COME_FROM_FINALLY    60  '60'

 L. 107       102  DUP_TOP          
              104  LOAD_GLOBAL              email
              106  LOAD_ATTR                errors
              108  LOAD_ATTR                HeaderDefect
              110  <121>               166  ''
              112  POP_TOP          
              114  STORE_FAST               'exc'
              116  POP_TOP          
              118  SETUP_FINALLY       158  'to 158'

 L. 108       120  LOAD_GLOBAL              ValueError
              122  LOAD_STR                 'Invalid header: {}'
              124  LOAD_METHOD              format

 L. 109       126  LOAD_FAST                'header'
              128  LOAD_ATTR                fold
              130  LOAD_FAST                'msg'
              132  LOAD_ATTR                policy
              134  LOAD_CONST               ('policy',)
              136  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 108       138  CALL_METHOD_1         1  ''
              140  CALL_FUNCTION_1       1  ''

 L. 109       142  LOAD_FAST                'exc'

 L. 108       144  RAISE_VARARGS_2       2  'exception instance with __cause__'
              146  POP_BLOCK        
              148  POP_EXCEPT       
              150  LOAD_CONST               None
              152  STORE_FAST               'exc'
              154  DELETE_FAST              'exc'
              156  JUMP_FORWARD        168  'to 168'
            158_0  COME_FROM_FINALLY   118  '118'
              158  LOAD_CONST               None
              160  STORE_FAST               'exc'
              162  DELETE_FAST              'exc'
              164  <48>             
              166  <48>             
            168_0  COME_FROM           156  '156'
            168_1  COME_FROM           100  '100'
            168_2  COME_FROM            20  '20'

Parse error at or near `<121>' instruction at offset 110


        def _finalize_set--- This code section failed: ---

 L. 113         0  LOAD_FAST                'disposition'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'
                8  LOAD_FAST                'filename'
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 114        16  LOAD_STR                 'attachment'
               18  STORE_FAST               'disposition'
             20_0  COME_FROM            14  '14'
             20_1  COME_FROM             6  '6'

 L. 115        20  LOAD_FAST                'disposition'
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 116        28  LOAD_FAST                'disposition'
               30  LOAD_FAST                'msg'
               32  LOAD_STR                 'Content-Disposition'
               34  STORE_SUBSCR     
             36_0  COME_FROM            26  '26'

 L. 117        36  LOAD_FAST                'filename'
               38  LOAD_CONST               None
               40  <117>                 1  ''
               42  POP_JUMP_IF_FALSE    62  'to 62'

 L. 118        44  LOAD_FAST                'msg'
               46  LOAD_ATTR                set_param
               48  LOAD_STR                 'filename'

 L. 119        50  LOAD_FAST                'filename'

 L. 120        52  LOAD_STR                 'Content-Disposition'

 L. 121        54  LOAD_CONST               True

 L. 118        56  LOAD_CONST               ('header', 'replace')
               58  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               60  POP_TOP          
             62_0  COME_FROM            42  '42'

 L. 122        62  LOAD_FAST                'cid'
               64  LOAD_CONST               None
               66  <117>                 1  ''
               68  POP_JUMP_IF_FALSE    78  'to 78'

 L. 123        70  LOAD_FAST                'cid'
               72  LOAD_FAST                'msg'
               74  LOAD_STR                 'Content-ID'
               76  STORE_SUBSCR     
             78_0  COME_FROM            68  '68'

 L. 124        78  LOAD_FAST                'params'
               80  LOAD_CONST               None
               82  <117>                 1  ''
               84  POP_JUMP_IF_FALSE   116  'to 116'

 L. 125        86  LOAD_FAST                'params'
               88  LOAD_METHOD              items
               90  CALL_METHOD_0         0  ''
               92  GET_ITER         
               94  FOR_ITER            116  'to 116'
               96  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST               'key'
              100  STORE_FAST               'value'

 L. 126       102  LOAD_FAST                'msg'
              104  LOAD_METHOD              set_param
              106  LOAD_FAST                'key'
              108  LOAD_FAST                'value'
              110  CALL_METHOD_2         2  ''
              112  POP_TOP          
              114  JUMP_BACK            94  'to 94'
            116_0  COME_FROM            84  '84'

Parse error at or near `None' instruction at offset -1


        def _encode_base64(data, max_line_length):
            encoded_lines = []
            unencoded_bytes_per_line = max_line_length // 4 * 3
            for i in range0len(data)unencoded_bytes_per_line:
                thisline = data[i:i + unencoded_bytes_per_line]
                encoded_lines.appendbinascii.b2a_base64thisline.decode'ascii'
            else:
                return ''.joinencoded_lines


        def _encode_text--- This code section failed: ---

 L. 143         0  LOAD_FAST                'string'
                2  LOAD_METHOD              encode
                4  LOAD_FAST                'charset'
                6  CALL_METHOD_1         1  ''
                8  LOAD_METHOD              splitlines
               10  CALL_METHOD_0         0  ''
               12  STORE_FAST               'lines'

 L. 144        14  LOAD_FAST                'policy'
               16  LOAD_ATTR                linesep
               18  LOAD_METHOD              encode
               20  LOAD_STR                 'ascii'
               22  CALL_METHOD_1         1  ''
               24  STORE_DEREF              'linesep'

 L. 145        26  LOAD_CLOSURE             'linesep'
               28  BUILD_TUPLE_1         1 
               30  LOAD_CODE                <code_object embedded_body>
               32  LOAD_STR                 '_encode_text.<locals>.embedded_body'
               34  MAKE_FUNCTION_8          'closure'
               36  STORE_FAST               'embedded_body'

 L. 146        38  LOAD_CODE                <code_object normal_body>
               40  LOAD_STR                 '_encode_text.<locals>.normal_body'
               42  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               44  STORE_FAST               'normal_body'

 L. 147        46  LOAD_FAST                'cte'
               48  LOAD_CONST               None
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE   244  'to 244'

 L. 149        54  LOAD_GLOBAL              max
               56  LOAD_GENEXPR             '<code_object <genexpr>>'
               58  LOAD_STR                 '_encode_text.<locals>.<genexpr>'
               60  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               62  LOAD_FAST                'lines'
               64  GET_ITER         
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_CONST               0
               70  LOAD_CONST               ('default',)
               72  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               74  LOAD_FAST                'policy'
               76  LOAD_ATTR                max_line_length
               78  COMPARE_OP               <=
               80  POP_JUMP_IF_FALSE   152  'to 152'

 L. 150        82  SETUP_FINALLY       104  'to 104'

 L. 151        84  LOAD_STR                 '7bit'
               86  LOAD_FAST                'normal_body'
               88  LOAD_FAST                'lines'
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_METHOD              decode
               94  LOAD_STR                 'ascii'
               96  CALL_METHOD_1         1  ''
               98  BUILD_TUPLE_2         2 
              100  POP_BLOCK        
              102  RETURN_VALUE     
            104_0  COME_FROM_FINALLY    82  '82'

 L. 152       104  DUP_TOP          
              106  LOAD_GLOBAL              UnicodeDecodeError
              108  <121>               120  ''
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 153       116  POP_EXCEPT       
              118  JUMP_FORWARD        122  'to 122'
              120  <48>             
            122_0  COME_FROM           118  '118'

 L. 154       122  LOAD_FAST                'policy'
              124  LOAD_ATTR                cte_type
              126  LOAD_STR                 '8bit'
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   152  'to 152'

 L. 155       132  LOAD_STR                 '8bit'
              134  LOAD_FAST                'normal_body'
              136  LOAD_FAST                'lines'
              138  CALL_FUNCTION_1       1  ''
              140  LOAD_METHOD              decode
              142  LOAD_STR                 'ascii'
              144  LOAD_STR                 'surrogateescape'
              146  CALL_METHOD_2         2  ''
              148  BUILD_TUPLE_2         2 
              150  RETURN_VALUE     
            152_0  COME_FROM           130  '130'
            152_1  COME_FROM            80  '80'

 L. 156       152  LOAD_FAST                'embedded_body'
              154  LOAD_FAST                'lines'
              156  LOAD_CONST               None
              158  LOAD_CONST               10
              160  BUILD_SLICE_2         2 
              162  BINARY_SUBSCR    
              164  CALL_FUNCTION_1       1  ''
              166  STORE_FAST               'sniff'

 L. 157       168  LOAD_GLOBAL              quoprimime
              170  LOAD_METHOD              body_encode
              172  LOAD_FAST                'sniff'
              174  LOAD_METHOD              decode
              176  LOAD_STR                 'latin-1'
              178  CALL_METHOD_1         1  ''

 L. 158       180  LOAD_FAST                'policy'
              182  LOAD_ATTR                max_line_length

 L. 157       184  CALL_METHOD_2         2  ''
              186  STORE_FAST               'sniff_qp'

 L. 159       188  LOAD_GLOBAL              binascii
              190  LOAD_METHOD              b2a_base64
              192  LOAD_FAST                'sniff'
              194  CALL_METHOD_1         1  ''
              196  STORE_FAST               'sniff_base64'

 L. 161       198  LOAD_GLOBAL              len
              200  LOAD_FAST                'sniff_qp'
              202  CALL_FUNCTION_1       1  ''
              204  LOAD_GLOBAL              len
              206  LOAD_FAST                'sniff_base64'
              208  CALL_FUNCTION_1       1  ''
              210  COMPARE_OP               >
              212  POP_JUMP_IF_FALSE   220  'to 220'

 L. 162       214  LOAD_STR                 'base64'
              216  STORE_FAST               'cte'
              218  JUMP_FORWARD        244  'to 244'
            220_0  COME_FROM           212  '212'

 L. 164       220  LOAD_STR                 'quoted-printable'
              222  STORE_FAST               'cte'

 L. 165       224  LOAD_GLOBAL              len
              226  LOAD_FAST                'lines'
              228  CALL_FUNCTION_1       1  ''
              230  LOAD_CONST               10
              232  COMPARE_OP               <=
              234  POP_JUMP_IF_FALSE   244  'to 244'

 L. 166       236  LOAD_FAST                'cte'
              238  LOAD_FAST                'sniff_qp'
              240  BUILD_TUPLE_2         2 
              242  RETURN_VALUE     
            244_0  COME_FROM           234  '234'
            244_1  COME_FROM           218  '218'
            244_2  COME_FROM            52  '52'

 L. 167       244  LOAD_FAST                'cte'
              246  LOAD_STR                 '7bit'
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   270  'to 270'

 L. 168       254  LOAD_FAST                'normal_body'
              256  LOAD_FAST                'lines'
              258  CALL_FUNCTION_1       1  ''
              260  LOAD_METHOD              decode
              262  LOAD_STR                 'ascii'
              264  CALL_METHOD_1         1  ''
              266  STORE_FAST               'data'
              268  JUMP_FORWARD        376  'to 376'
            270_0  COME_FROM           250  '250'

 L. 169       270  LOAD_FAST                'cte'
              272  LOAD_STR                 '8bit'
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_FALSE   298  'to 298'

 L. 170       280  LOAD_FAST                'normal_body'
              282  LOAD_FAST                'lines'
              284  CALL_FUNCTION_1       1  ''
              286  LOAD_METHOD              decode
              288  LOAD_STR                 'ascii'
              290  LOAD_STR                 'surrogateescape'
              292  CALL_METHOD_2         2  ''
              294  STORE_FAST               'data'
              296  JUMP_FORWARD        376  'to 376'
            298_0  COME_FROM           276  '276'

 L. 171       298  LOAD_FAST                'cte'
              300  LOAD_STR                 'quoted-printable'
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_FALSE   334  'to 334'

 L. 172       308  LOAD_GLOBAL              quoprimime
              310  LOAD_METHOD              body_encode
              312  LOAD_FAST                'normal_body'
              314  LOAD_FAST                'lines'
              316  CALL_FUNCTION_1       1  ''
              318  LOAD_METHOD              decode
              320  LOAD_STR                 'latin-1'
              322  CALL_METHOD_1         1  ''

 L. 173       324  LOAD_FAST                'policy'
              326  LOAD_ATTR                max_line_length

 L. 172       328  CALL_METHOD_2         2  ''
              330  STORE_FAST               'data'
              332  JUMP_FORWARD        376  'to 376'
            334_0  COME_FROM           304  '304'

 L. 174       334  LOAD_FAST                'cte'
              336  LOAD_STR                 'base64'
              338  COMPARE_OP               ==
          340_342  POP_JUMP_IF_FALSE   362  'to 362'

 L. 175       344  LOAD_GLOBAL              _encode_base64
              346  LOAD_FAST                'embedded_body'
              348  LOAD_FAST                'lines'
              350  CALL_FUNCTION_1       1  ''
              352  LOAD_FAST                'policy'
              354  LOAD_ATTR                max_line_length
              356  CALL_FUNCTION_2       2  ''
              358  STORE_FAST               'data'
              360  JUMP_FORWARD        376  'to 376'
            362_0  COME_FROM           340  '340'

 L. 177       362  LOAD_GLOBAL              ValueError
              364  LOAD_STR                 'Unknown content transfer encoding {}'
              366  LOAD_METHOD              format
              368  LOAD_FAST                'cte'
              370  CALL_METHOD_1         1  ''
              372  CALL_FUNCTION_1       1  ''
              374  RAISE_VARARGS_1       1  'exception instance'
            376_0  COME_FROM           360  '360'
            376_1  COME_FROM           332  '332'
            376_2  COME_FROM           296  '296'
            376_3  COME_FROM           268  '268'

 L. 178       376  LOAD_FAST                'cte'
              378  LOAD_FAST                'data'
              380  BUILD_TUPLE_2         2 
              382  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 108


        def set_text_content(msg, string, subtype='plain', charset='utf-8', cte=None, disposition=None, filename=None, cid=None, params=None, headers=None):
            _prepare_set(msg, 'text', subtype, headers)
            cte, payload = _encode_text(string, charset, cte, msg.policy)
            msg.set_payloadpayload
            msg.set_param('charset', (email.charset.ALIASES.get(charset, charset)),
              replace=True)
            msg['Content-Transfer-Encoding'] = cte
            _finalize_set(msg, disposition, filename, cid, params)


        raw_data_manager.add_set_handler(str, set_text_content)

        def set_message_content--- This code section failed: ---

 L. 198         0  LOAD_FAST                'subtype'
                2  LOAD_STR                 'partial'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 199         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'message/partial is not supported for Message objects'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 200        16  LOAD_FAST                'subtype'
               18  LOAD_STR                 'rfc822'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    64  'to 64'

 L. 201        24  LOAD_FAST                'cte'
               26  LOAD_CONST               (None, '7bit', '8bit', 'binary')
               28  <118>                 1  ''
               30  POP_JUMP_IF_FALSE    46  'to 46'

 L. 203        32  LOAD_GLOBAL              ValueError

 L. 204        34  LOAD_STR                 'message/rfc822 parts do not support cte={}'
               36  LOAD_METHOD              format
               38  LOAD_FAST                'cte'
               40  CALL_METHOD_1         1  ''

 L. 203        42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            30  '30'

 L. 210        46  LOAD_FAST                'cte'
               48  LOAD_CONST               None
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE    58  'to 58'
               54  LOAD_STR                 '8bit'
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            52  '52'
               58  LOAD_FAST                'cte'
             60_0  COME_FROM            56  '56'
               60  STORE_FAST               'cte'
               62  JUMP_FORWARD        112  'to 112'
             64_0  COME_FROM            22  '22'

 L. 211        64  LOAD_FAST                'subtype'
               66  LOAD_STR                 'external-body'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE   100  'to 100'

 L. 212        72  LOAD_FAST                'cte'
               74  LOAD_CONST               (None, '7bit')
               76  <118>                 1  ''
               78  POP_JUMP_IF_FALSE    94  'to 94'

 L. 214        80  LOAD_GLOBAL              ValueError

 L. 215        82  LOAD_STR                 'message/external-body parts do not support cte={}'
               84  LOAD_METHOD              format
               86  LOAD_FAST                'cte'
               88  CALL_METHOD_1         1  ''

 L. 214        90  CALL_FUNCTION_1       1  ''
               92  RAISE_VARARGS_1       1  'exception instance'
             94_0  COME_FROM            78  '78'

 L. 216        94  LOAD_STR                 '7bit'
               96  STORE_FAST               'cte'
               98  JUMP_FORWARD        112  'to 112'
            100_0  COME_FROM            70  '70'

 L. 217       100  LOAD_FAST                'cte'
              102  LOAD_CONST               None
              104  <117>                 0  ''
              106  POP_JUMP_IF_FALSE   112  'to 112'

 L. 220       108  LOAD_STR                 '7bit'
              110  STORE_FAST               'cte'
            112_0  COME_FROM           106  '106'
            112_1  COME_FROM            98  '98'
            112_2  COME_FROM            62  '62'

 L. 221       112  LOAD_GLOBAL              _prepare_set
              114  LOAD_FAST                'msg'
              116  LOAD_STR                 'message'
              118  LOAD_FAST                'subtype'
              120  LOAD_FAST                'headers'
              122  CALL_FUNCTION_4       4  ''
              124  POP_TOP          

 L. 222       126  LOAD_FAST                'msg'
              128  LOAD_METHOD              set_payload
              130  LOAD_FAST                'message'
              132  BUILD_LIST_1          1 
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          

 L. 223       138  LOAD_FAST                'cte'
              140  LOAD_FAST                'msg'
              142  LOAD_STR                 'Content-Transfer-Encoding'
              144  STORE_SUBSCR     

 L. 224       146  LOAD_GLOBAL              _finalize_set
              148  LOAD_FAST                'msg'
              150  LOAD_FAST                'disposition'
              152  LOAD_FAST                'filename'
              154  LOAD_FAST                'cid'
              156  LOAD_FAST                'params'
              158  CALL_FUNCTION_5       5  ''
              160  POP_TOP          

Parse error at or near `<118>' instruction at offset 28


        raw_data_manager.add_set_handler(email.message.Message, set_message_content)

        def set_bytes_content--- This code section failed: ---

 L. 231         0  LOAD_GLOBAL              _prepare_set
                2  LOAD_FAST                'msg'
                4  LOAD_FAST                'maintype'
                6  LOAD_FAST                'subtype'
                8  LOAD_FAST                'headers'
               10  CALL_FUNCTION_4       4  ''
               12  POP_TOP          

 L. 232        14  LOAD_FAST                'cte'
               16  LOAD_STR                 'base64'
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    40  'to 40'

 L. 233        22  LOAD_GLOBAL              _encode_base64
               24  LOAD_FAST                'data'
               26  LOAD_FAST                'msg'
               28  LOAD_ATTR                policy
               30  LOAD_ATTR                max_line_length
               32  LOAD_CONST               ('max_line_length',)
               34  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               36  STORE_FAST               'data'
               38  JUMP_FORWARD        118  'to 118'
             40_0  COME_FROM            20  '20'

 L. 234        40  LOAD_FAST                'cte'
               42  LOAD_STR                 'quoted-printable'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    78  'to 78'

 L. 238        48  LOAD_GLOBAL              binascii
               50  LOAD_ATTR                b2a_qp
               52  LOAD_FAST                'data'
               54  LOAD_CONST               False
               56  LOAD_CONST               False
               58  LOAD_CONST               True
               60  LOAD_CONST               ('istext', 'header', 'quotetabs')
               62  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               64  STORE_FAST               'data'

 L. 239        66  LOAD_FAST                'data'
               68  LOAD_METHOD              decode
               70  LOAD_STR                 'ascii'
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'data'
               76  JUMP_FORWARD        118  'to 118'
             78_0  COME_FROM            46  '46'

 L. 240        78  LOAD_FAST                'cte'
               80  LOAD_STR                 '7bit'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE    98  'to 98'

 L. 243        86  LOAD_FAST                'data'
               88  LOAD_METHOD              encode
               90  LOAD_STR                 'ascii'
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
               96  JUMP_FORWARD        118  'to 118'
             98_0  COME_FROM            84  '84'

 L. 244        98  LOAD_FAST                'cte'
              100  LOAD_CONST               ('8bit', 'binary')
              102  <118>                 0  ''
              104  POP_JUMP_IF_FALSE   118  'to 118'

 L. 245       106  LOAD_FAST                'data'
              108  LOAD_METHOD              decode
              110  LOAD_STR                 'ascii'
              112  LOAD_STR                 'surrogateescape'
              114  CALL_METHOD_2         2  ''
              116  STORE_FAST               'data'
            118_0  COME_FROM           104  '104'
            118_1  COME_FROM            96  '96'
            118_2  COME_FROM            76  '76'
            118_3  COME_FROM            38  '38'

 L. 246       118  LOAD_FAST                'msg'
              120  LOAD_METHOD              set_payload
              122  LOAD_FAST                'data'
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          

 L. 247       128  LOAD_FAST                'cte'
              130  LOAD_FAST                'msg'
              132  LOAD_STR                 'Content-Transfer-Encoding'
              134  STORE_SUBSCR     

 L. 248       136  LOAD_GLOBAL              _finalize_set
              138  LOAD_FAST                'msg'
              140  LOAD_FAST                'disposition'
              142  LOAD_FAST                'filename'
              144  LOAD_FAST                'cid'
              146  LOAD_FAST                'params'
              148  CALL_FUNCTION_5       5  ''
              150  POP_TOP          

Parse error at or near `<118>' instruction at offset 102


        for typ in (
         bytes, bytearray, memoryview):
            raw_data_manager.add_set_handler(typ, set_bytes_content)