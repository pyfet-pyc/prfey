# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: xml\etree\ElementPath.py
import re
xpath_tokenizer_re = re.compile('(\'[^\']*\'|\\"[^\\"]*\\"|::|//?|\\.\\.|\\(\\)|[/.*:\\[\\]\\(\\)@=])|((?:\\{[^}]+\\})?[^/\\[\\]\\(\\)@=\\s]+)|\\s+')

def xpath_tokenizer--- This code section failed: ---

 L.  74         0  LOAD_FAST                'namespaces'
                2  POP_JUMP_IF_FALSE    14  'to 14'
                4  LOAD_FAST                'namespaces'
                6  LOAD_METHOD              get
                8  LOAD_STR                 ''
               10  CALL_METHOD_1         1  ''
               12  JUMP_FORWARD         16  'to 16'
             14_0  COME_FROM             2  '2'
               14  LOAD_CONST               None
             16_0  COME_FROM            12  '12'
               16  STORE_FAST               'default_namespace'

 L.  75        18  LOAD_CONST               False
               20  STORE_FAST               'parsing_attribute'

 L.  76        22  LOAD_GLOBAL              xpath_tokenizer_re
               24  LOAD_METHOD              findall
               26  LOAD_FAST                'pattern'
               28  CALL_METHOD_1         1  ''
               30  GET_ITER         
             32_0  COME_FROM           208  '208'
             32_1  COME_FROM           192  '192'
               32  FOR_ITER            210  'to 210'
               34  STORE_FAST               'token'

 L.  77        36  LOAD_FAST                'token'
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'ttype'
               42  STORE_FAST               'tag'

 L.  78        44  LOAD_FAST                'tag'
               46  POP_JUMP_IF_FALSE   194  'to 194'
               48  LOAD_FAST                'tag'
               50  LOAD_CONST               0
               52  BINARY_SUBSCR    
               54  LOAD_STR                 '{'
               56  COMPARE_OP               !=
               58  POP_JUMP_IF_FALSE   194  'to 194'

 L.  79        60  LOAD_STR                 ':'
               62  LOAD_FAST                'tag'
               64  <118>                 0  ''
               66  POP_JUMP_IF_FALSE   154  'to 154'

 L.  80        68  LOAD_FAST                'tag'
               70  LOAD_METHOD              split
               72  LOAD_STR                 ':'
               74  LOAD_CONST               1
               76  CALL_METHOD_2         2  ''
               78  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST               'prefix'
               82  STORE_FAST               'uri'

 L.  81        84  SETUP_FINALLY       120  'to 120'

 L.  82        86  LOAD_FAST                'namespaces'
               88  POP_JUMP_IF_TRUE     94  'to 94'

 L.  83        90  LOAD_GLOBAL              KeyError
               92  RAISE_VARARGS_1       1  'exception instance'
             94_0  COME_FROM            88  '88'

 L.  84        94  LOAD_FAST                'ttype'
               96  LOAD_STR                 '{%s}%s'
               98  LOAD_FAST                'namespaces'
              100  LOAD_FAST                'prefix'
              102  BINARY_SUBSCR    
              104  LOAD_FAST                'uri'
              106  BUILD_TUPLE_2         2 
              108  BINARY_MODULO    
              110  BUILD_TUPLE_2         2 
              112  YIELD_VALUE      
              114  POP_TOP          
              116  POP_BLOCK        
              118  JUMP_FORWARD        188  'to 188'
            120_0  COME_FROM_FINALLY    84  '84'

 L.  85       120  DUP_TOP          
              122  LOAD_GLOBAL              KeyError
              124  <121>               150  ''
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L.  86       132  LOAD_GLOBAL              SyntaxError
              134  LOAD_STR                 'prefix %r not found in prefix map'
              136  LOAD_FAST                'prefix'
              138  BINARY_MODULO    
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_CONST               None
              144  RAISE_VARARGS_2       2  'exception instance with __cause__'
              146  POP_EXCEPT       
              148  JUMP_FORWARD        188  'to 188'
              150  <48>             
              152  JUMP_FORWARD        188  'to 188'
            154_0  COME_FROM            66  '66'

 L.  87       154  LOAD_FAST                'default_namespace'
              156  POP_JUMP_IF_FALSE   182  'to 182'
              158  LOAD_FAST                'parsing_attribute'
              160  POP_JUMP_IF_TRUE    182  'to 182'

 L.  88       162  LOAD_FAST                'ttype'
              164  LOAD_STR                 '{%s}%s'
              166  LOAD_FAST                'default_namespace'
              168  LOAD_FAST                'tag'
              170  BUILD_TUPLE_2         2 
              172  BINARY_MODULO    
              174  BUILD_TUPLE_2         2 
              176  YIELD_VALUE      
              178  POP_TOP          
              180  JUMP_FORWARD        188  'to 188'
            182_0  COME_FROM           160  '160'
            182_1  COME_FROM           156  '156'

 L.  90       182  LOAD_FAST                'token'
              184  YIELD_VALUE      
              186  POP_TOP          
            188_0  COME_FROM           180  '180'
            188_1  COME_FROM           152  '152'
            188_2  COME_FROM           148  '148'
            188_3  COME_FROM           118  '118'

 L.  91       188  LOAD_CONST               False
              190  STORE_FAST               'parsing_attribute'
              192  JUMP_BACK            32  'to 32'
            194_0  COME_FROM            58  '58'
            194_1  COME_FROM            46  '46'

 L.  93       194  LOAD_FAST                'token'
              196  YIELD_VALUE      
              198  POP_TOP          

 L.  94       200  LOAD_FAST                'ttype'
              202  LOAD_STR                 '@'
              204  COMPARE_OP               ==
              206  STORE_FAST               'parsing_attribute'
              208  JUMP_BACK            32  'to 32'
            210_0  COME_FROM            32  '32'

Parse error at or near `<118>' instruction at offset 64


def get_parent_map--- This code section failed: ---

 L.  98         0  LOAD_FAST                'context'
                2  LOAD_ATTR                parent_map
                4  STORE_FAST               'parent_map'

 L.  99         6  LOAD_FAST                'parent_map'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    58  'to 58'

 L. 100        14  BUILD_MAP_0           0 
               16  DUP_TOP          
               18  LOAD_FAST                'context'
               20  STORE_ATTR               parent_map
               22  STORE_FAST               'parent_map'

 L. 101        24  LOAD_FAST                'context'
               26  LOAD_ATTR                root
               28  LOAD_METHOD              iter
               30  CALL_METHOD_0         0  ''
               32  GET_ITER         
             34_0  COME_FROM            56  '56'
               34  FOR_ITER             58  'to 58'
               36  STORE_FAST               'p'

 L. 102        38  LOAD_FAST                'p'
               40  GET_ITER         
             42_0  COME_FROM            54  '54'
               42  FOR_ITER             56  'to 56'
               44  STORE_FAST               'e'

 L. 103        46  LOAD_FAST                'p'
               48  LOAD_FAST                'parent_map'
               50  LOAD_FAST                'e'
               52  STORE_SUBSCR     
               54  JUMP_BACK            42  'to 42'
             56_0  COME_FROM            42  '42'
               56  JUMP_BACK            34  'to 34'
             58_0  COME_FROM            34  '34'
             58_1  COME_FROM            12  '12'

 L. 104        58  LOAD_FAST                'parent_map'
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10


def _is_wildcard_tag(tag):
    return tag[:3] == '{*}' or tag[-2:] == '}*'


def _prepare_tag(tag):
    _isinstance, _str = isinstance, str
    if tag == '{*}*':

        def select(context, result):
            for elem in result:
                if _isinstance(elem.tag, _str):
                    yield elem

    elif tag == '{}*':

        def select(context, result):
            for elem in result:
                el_tag = elem.tag
                if _isinstance(el_tag, _str):
                    if el_tag[0] != '{':
                        yield elem

    elif tag[:3] == '{*}':
        suffix = tag[2:]
        no_ns = slice(-len(suffix), None)
        tag = tag[3:]

        def select(context, result):
            for elem in result:
                el_tag = elem.tag
                if not el_tag == tag:
                    if _isinstance(el_tag, _str):
                        if el_tag[no_ns] == suffix:
                            pass
                yield elem

    elif tag[-2:] == '}*':
        ns = tag[:-1]
        ns_only = slice(None, len(ns))

        def select(context, result):
            for elem in result:
                el_tag = elem.tag
                if _isinstance(el_tag, _str):
                    if el_tag[ns_only] == ns:
                        yield elem

    else:
        raise RuntimeError(f"internal parser error, got {tag}")
    return select


def prepare_child(next, token):
    tag = token[1]
    if _is_wildcard_tag(tag):
        select_tag = _prepare_tag(tag)

        def select(context, result):

            def select_child(result):
                for elem in result:
                    yield from elem

                if False:
                    yield None

            return select_tag(context, select_child(result))

    else:
        if tag[:2] == '{}':
            tag = tag[2:]

        def select(context, result):
            for elem in result:
                for e in elem:
                    if e.tag == tag:
                        yield e

    return select


def prepare_star(next, token):

    def select(context, result):
        for elem in result:
            yield from elem

        if False:
            yield None

    return select


def prepare_self(next, token):

    def select(context, result):
        yield from result
        if False:
            yield None

    return select


def prepare_descendant--- This code section failed: ---

 L. 183         0  SETUP_FINALLY        12  'to 12'

 L. 184         2  LOAD_FAST                'next'
                4  CALL_FUNCTION_0       0  ''
                6  STORE_FAST               'token'
                8  POP_BLOCK        
               10  JUMP_FORWARD         32  'to 32'
             12_0  COME_FROM_FINALLY     0  '0'

 L. 185        12  DUP_TOP          
               14  LOAD_GLOBAL              StopIteration
               16  <121>                30  ''
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 186        24  POP_EXCEPT       
               26  LOAD_CONST               None
               28  RETURN_VALUE     
               30  <48>             
             32_0  COME_FROM            10  '10'

 L. 187        32  LOAD_FAST                'token'
               34  LOAD_CONST               0
               36  BINARY_SUBSCR    
               38  LOAD_STR                 '*'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    50  'to 50'

 L. 188        44  LOAD_STR                 '*'
               46  STORE_DEREF              'tag'
               48  JUMP_FORWARD         76  'to 76'
             50_0  COME_FROM            42  '42'

 L. 189        50  LOAD_FAST                'token'
               52  LOAD_CONST               0
               54  BINARY_SUBSCR    
               56  POP_JUMP_IF_TRUE     68  'to 68'

 L. 190        58  LOAD_FAST                'token'
               60  LOAD_CONST               1
               62  BINARY_SUBSCR    
               64  STORE_DEREF              'tag'
               66  JUMP_FORWARD         76  'to 76'
             68_0  COME_FROM            56  '56'

 L. 192        68  LOAD_GLOBAL              SyntaxError
               70  LOAD_STR                 'invalid descendant'
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            66  '66'
             76_1  COME_FROM            48  '48'

 L. 194        76  LOAD_GLOBAL              _is_wildcard_tag
               78  LOAD_DEREF               'tag'
               80  CALL_FUNCTION_1       1  ''
               82  POP_JUMP_IF_FALSE   106  'to 106'

 L. 195        84  LOAD_GLOBAL              _prepare_tag
               86  LOAD_DEREF               'tag'
               88  CALL_FUNCTION_1       1  ''
               90  STORE_DEREF              'select_tag'

 L. 196        92  LOAD_CLOSURE             'select_tag'
               94  BUILD_TUPLE_1         1 
               96  LOAD_CODE                <code_object select>
               98  LOAD_STR                 'prepare_descendant.<locals>.select'
              100  MAKE_FUNCTION_8          'closure'
              102  STORE_FAST               'select'
              104  JUMP_FORWARD        146  'to 146'
            106_0  COME_FROM            82  '82'

 L. 204       106  LOAD_DEREF               'tag'
              108  LOAD_CONST               None
              110  LOAD_CONST               2
              112  BUILD_SLICE_2         2 
              114  BINARY_SUBSCR    
              116  LOAD_STR                 '{}'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   134  'to 134'

 L. 205       122  LOAD_DEREF               'tag'
              124  LOAD_CONST               2
              126  LOAD_CONST               None
              128  BUILD_SLICE_2         2 
              130  BINARY_SUBSCR    
              132  STORE_DEREF              'tag'
            134_0  COME_FROM           120  '120'

 L. 206       134  LOAD_CLOSURE             'tag'
              136  BUILD_TUPLE_1         1 
              138  LOAD_CODE                <code_object select>
              140  LOAD_STR                 'prepare_descendant.<locals>.select'
              142  MAKE_FUNCTION_8          'closure'
              144  STORE_FAST               'select'
            146_0  COME_FROM           104  '104'

 L. 211       146  LOAD_FAST                'select'
              148  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 16


def prepare_parent(next, token):

    def select--- This code section failed: ---

 L. 216         0  LOAD_GLOBAL              get_parent_map
                2  LOAD_FAST                'context'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'parent_map'

 L. 217         8  BUILD_MAP_0           0 
               10  STORE_FAST               'result_map'

 L. 218        12  LOAD_FAST                'result'
               14  GET_ITER         
             16_0  COME_FROM            58  '58'
             16_1  COME_FROM            42  '42'
             16_2  COME_FROM            26  '26'
               16  FOR_ITER             60  'to 60'
               18  STORE_FAST               'elem'

 L. 219        20  LOAD_FAST                'elem'
               22  LOAD_FAST                'parent_map'
               24  <118>                 0  ''
               26  POP_JUMP_IF_FALSE_BACK    16  'to 16'

 L. 220        28  LOAD_FAST                'parent_map'
               30  LOAD_FAST                'elem'
               32  BINARY_SUBSCR    
               34  STORE_FAST               'parent'

 L. 221        36  LOAD_FAST                'parent'
               38  LOAD_FAST                'result_map'
               40  <118>                 1  ''
               42  POP_JUMP_IF_FALSE_BACK    16  'to 16'

 L. 222        44  LOAD_CONST               None
               46  LOAD_FAST                'result_map'
               48  LOAD_FAST                'parent'
               50  STORE_SUBSCR     

 L. 223        52  LOAD_FAST                'parent'
               54  YIELD_VALUE      
               56  POP_TOP          
               58  JUMP_BACK            16  'to 16'
             60_0  COME_FROM            16  '16'

Parse error at or near `<118>' instruction at offset 24

    return select


def prepare_predicate--- This code section failed: ---

 L. 230         0  BUILD_LIST_0          0 
                2  STORE_FAST               'signature'

 L. 231         4  BUILD_LIST_0          0 
                6  STORE_FAST               'predicate'
              8_0  COME_FROM           144  '144'
              8_1  COME_FROM            62  '62'

 L. 233         8  SETUP_FINALLY        20  'to 20'

 L. 234        10  LOAD_FAST                'next'
               12  CALL_FUNCTION_0       0  ''
               14  STORE_FAST               'token'
               16  POP_BLOCK        
               18  JUMP_FORWARD         40  'to 40'
             20_0  COME_FROM_FINALLY     8  '8'

 L. 235        20  DUP_TOP          
               22  LOAD_GLOBAL              StopIteration
               24  <121>                38  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 236        32  POP_EXCEPT       
               34  LOAD_CONST               None
               36  RETURN_VALUE     
               38  <48>             
             40_0  COME_FROM            18  '18'

 L. 237        40  LOAD_FAST                'token'
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  LOAD_STR                 ']'
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    54  'to 54'

 L. 238        52  JUMP_FORWARD        146  'to 146'
             54_0  COME_FROM            50  '50'

 L. 239        54  LOAD_FAST                'token'
               56  LOAD_CONST               ('', '')
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    64  'to 64'

 L. 241        62  JUMP_BACK             8  'to 8'
             64_0  COME_FROM            60  '60'

 L. 242        64  LOAD_FAST                'token'
               66  LOAD_CONST               0
               68  BINARY_SUBSCR    
               70  POP_JUMP_IF_FALSE   112  'to 112'
               72  LOAD_FAST                'token'
               74  LOAD_CONST               0
               76  BINARY_SUBSCR    
               78  LOAD_CONST               None
               80  LOAD_CONST               1
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    
               86  LOAD_STR                 '\'"'
               88  <118>                 0  ''
               90  POP_JUMP_IF_FALSE   112  'to 112'

 L. 243        92  LOAD_STR                 "'"
               94  LOAD_FAST                'token'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  LOAD_CONST               1
              102  LOAD_CONST               -1
              104  BUILD_SLICE_2         2 
              106  BINARY_SUBSCR    
              108  BUILD_TUPLE_2         2 
              110  STORE_FAST               'token'
            112_0  COME_FROM            90  '90'
            112_1  COME_FROM            70  '70'

 L. 244       112  LOAD_FAST                'signature'
              114  LOAD_METHOD              append
              116  LOAD_FAST                'token'
              118  LOAD_CONST               0
              120  BINARY_SUBSCR    
              122  JUMP_IF_TRUE_OR_POP   126  'to 126'
              124  LOAD_STR                 '-'
            126_0  COME_FROM           122  '122'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          

 L. 245       130  LOAD_FAST                'predicate'
              132  LOAD_METHOD              append
              134  LOAD_FAST                'token'
              136  LOAD_CONST               1
              138  BINARY_SUBSCR    
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  JUMP_BACK             8  'to 8'
            146_0  COME_FROM            52  '52'

 L. 246       146  LOAD_STR                 ''
              148  LOAD_METHOD              join
              150  LOAD_FAST                'signature'
              152  CALL_METHOD_1         1  ''
              154  STORE_FAST               'signature'

 L. 248       156  LOAD_FAST                'signature'
              158  LOAD_STR                 '@-'
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   188  'to 188'

 L. 250       164  LOAD_FAST                'predicate'
              166  LOAD_CONST               1
              168  BINARY_SUBSCR    
              170  STORE_DEREF              'key'

 L. 251       172  LOAD_CLOSURE             'key'
              174  BUILD_TUPLE_1         1 
              176  LOAD_CODE                <code_object select>
              178  LOAD_STR                 'prepare_predicate.<locals>.select'
              180  MAKE_FUNCTION_8          'closure'
              182  STORE_FAST               'select'

 L. 255       184  LOAD_FAST                'select'
              186  RETURN_VALUE     
            188_0  COME_FROM           162  '162'

 L. 256       188  LOAD_FAST                'signature'
              190  LOAD_STR                 "@-='"
              192  COMPARE_OP               ==
              194  POP_JUMP_IF_FALSE   230  'to 230'

 L. 258       196  LOAD_FAST                'predicate'
              198  LOAD_CONST               1
              200  BINARY_SUBSCR    
              202  STORE_DEREF              'key'

 L. 259       204  LOAD_FAST                'predicate'
              206  LOAD_CONST               -1
              208  BINARY_SUBSCR    
              210  STORE_DEREF              'value'

 L. 260       212  LOAD_CLOSURE             'key'
              214  LOAD_CLOSURE             'value'
              216  BUILD_TUPLE_2         2 
              218  LOAD_CODE                <code_object select>
              220  LOAD_STR                 'prepare_predicate.<locals>.select'
              222  MAKE_FUNCTION_8          'closure'
              224  STORE_FAST               'select'

 L. 264       226  LOAD_FAST                'select'
              228  RETURN_VALUE     
            230_0  COME_FROM           194  '194'

 L. 265       230  LOAD_FAST                'signature'
              232  LOAD_STR                 '-'
              234  COMPARE_OP               ==
          236_238  POP_JUMP_IF_FALSE   282  'to 282'
              240  LOAD_GLOBAL              re
              242  LOAD_METHOD              match
              244  LOAD_STR                 '\\-?\\d+$'
              246  LOAD_FAST                'predicate'
              248  LOAD_CONST               0
              250  BINARY_SUBSCR    
              252  CALL_METHOD_2         2  ''
          254_256  POP_JUMP_IF_TRUE    282  'to 282'

 L. 267       258  LOAD_FAST                'predicate'
              260  LOAD_CONST               0
              262  BINARY_SUBSCR    
              264  STORE_DEREF              'tag'

 L. 268       266  LOAD_CLOSURE             'tag'
              268  BUILD_TUPLE_1         1 
              270  LOAD_CODE                <code_object select>
              272  LOAD_STR                 'prepare_predicate.<locals>.select'
              274  MAKE_FUNCTION_8          'closure'
              276  STORE_FAST               'select'

 L. 272       278  LOAD_FAST                'select'
              280  RETURN_VALUE     
            282_0  COME_FROM           254  '254'
            282_1  COME_FROM           236  '236'

 L. 273       282  LOAD_FAST                'signature'
              284  LOAD_STR                 ".='"
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_TRUE    320  'to 320'
              292  LOAD_FAST                'signature'
              294  LOAD_STR                 "-='"
              296  COMPARE_OP               ==
          298_300  POP_JUMP_IF_FALSE   374  'to 374'
              302  LOAD_GLOBAL              re
              304  LOAD_METHOD              match
              306  LOAD_STR                 '\\-?\\d+$'
              308  LOAD_FAST                'predicate'
              310  LOAD_CONST               0
              312  BINARY_SUBSCR    
              314  CALL_METHOD_2         2  ''
          316_318  POP_JUMP_IF_TRUE    374  'to 374'
            320_0  COME_FROM           288  '288'

 L. 275       320  LOAD_FAST                'predicate'
              322  LOAD_CONST               0
              324  BINARY_SUBSCR    
              326  STORE_DEREF              'tag'

 L. 276       328  LOAD_FAST                'predicate'
              330  LOAD_CONST               -1
              332  BINARY_SUBSCR    
              334  STORE_DEREF              'value'

 L. 277       336  LOAD_DEREF               'tag'
          338_340  POP_JUMP_IF_FALSE   358  'to 358'

 L. 278       342  LOAD_CLOSURE             'tag'
              344  LOAD_CLOSURE             'value'
              346  BUILD_TUPLE_2         2 
              348  LOAD_CODE                <code_object select>
              350  LOAD_STR                 'prepare_predicate.<locals>.select'
              352  MAKE_FUNCTION_8          'closure'
              354  STORE_FAST               'select'
              356  JUMP_FORWARD        370  'to 370'
            358_0  COME_FROM           338  '338'

 L. 285       358  LOAD_CLOSURE             'value'
              360  BUILD_TUPLE_1         1 
              362  LOAD_CODE                <code_object select>
              364  LOAD_STR                 'prepare_predicate.<locals>.select'
              366  MAKE_FUNCTION_8          'closure'
              368  STORE_FAST               'select'
            370_0  COME_FROM           356  '356'

 L. 289       370  LOAD_FAST                'select'
              372  RETURN_VALUE     
            374_0  COME_FROM           316  '316'
            374_1  COME_FROM           298  '298'

 L. 290       374  LOAD_FAST                'signature'
              376  LOAD_STR                 '-'
              378  COMPARE_OP               ==
          380_382  POP_JUMP_IF_TRUE    404  'to 404'
              384  LOAD_FAST                'signature'
              386  LOAD_STR                 '-()'
              388  COMPARE_OP               ==
          390_392  POP_JUMP_IF_TRUE    404  'to 404'
              394  LOAD_FAST                'signature'
              396  LOAD_STR                 '-()-'
              398  COMPARE_OP               ==
          400_402  POP_JUMP_IF_FALSE   572  'to 572'
            404_0  COME_FROM           390  '390'
            404_1  COME_FROM           380  '380'

 L. 292       404  LOAD_FAST                'signature'
              406  LOAD_STR                 '-'
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   450  'to 450'

 L. 294       414  LOAD_GLOBAL              int
              416  LOAD_FAST                'predicate'
              418  LOAD_CONST               0
              420  BINARY_SUBSCR    
              422  CALL_FUNCTION_1       1  ''
              424  LOAD_CONST               1
              426  BINARY_SUBTRACT  
              428  STORE_DEREF              'index'

 L. 295       430  LOAD_DEREF               'index'
              432  LOAD_CONST               0
              434  COMPARE_OP               <
          436_438  POP_JUMP_IF_FALSE   556  'to 556'

 L. 296       440  LOAD_GLOBAL              SyntaxError
              442  LOAD_STR                 'XPath position >= 1 expected'
              444  CALL_FUNCTION_1       1  ''
              446  RAISE_VARARGS_1       1  'exception instance'
              448  JUMP_FORWARD        556  'to 556'
            450_0  COME_FROM           410  '410'

 L. 298       450  LOAD_FAST                'predicate'
              452  LOAD_CONST               0
              454  BINARY_SUBSCR    
              456  LOAD_STR                 'last'
              458  COMPARE_OP               !=
          460_462  POP_JUMP_IF_FALSE   472  'to 472'

 L. 299       464  LOAD_GLOBAL              SyntaxError
              466  LOAD_STR                 'unsupported function'
              468  CALL_FUNCTION_1       1  ''
              470  RAISE_VARARGS_1       1  'exception instance'
            472_0  COME_FROM           460  '460'

 L. 300       472  LOAD_FAST                'signature'
              474  LOAD_STR                 '-()-'
              476  COMPARE_OP               ==
          478_480  POP_JUMP_IF_FALSE   552  'to 552'

 L. 301       482  SETUP_FINALLY       504  'to 504'

 L. 302       484  LOAD_GLOBAL              int
              486  LOAD_FAST                'predicate'
              488  LOAD_CONST               2
              490  BINARY_SUBSCR    
              492  CALL_FUNCTION_1       1  ''
              494  LOAD_CONST               1
              496  BINARY_SUBTRACT  
              498  STORE_DEREF              'index'
              500  POP_BLOCK        
              502  JUMP_FORWARD        532  'to 532'
            504_0  COME_FROM_FINALLY   482  '482'

 L. 303       504  DUP_TOP          
              506  LOAD_GLOBAL              ValueError
          508_510  <121>               530  ''
              512  POP_TOP          
              514  POP_TOP          
              516  POP_TOP          

 L. 304       518  LOAD_GLOBAL              SyntaxError
              520  LOAD_STR                 'unsupported expression'
              522  CALL_FUNCTION_1       1  ''
              524  RAISE_VARARGS_1       1  'exception instance'
              526  POP_EXCEPT       
              528  JUMP_FORWARD        532  'to 532'
              530  <48>             
            532_0  COME_FROM           528  '528'
            532_1  COME_FROM           502  '502'

 L. 305       532  LOAD_DEREF               'index'
              534  LOAD_CONST               -2
              536  COMPARE_OP               >
          538_540  POP_JUMP_IF_FALSE   556  'to 556'

 L. 306       542  LOAD_GLOBAL              SyntaxError
              544  LOAD_STR                 'XPath offset from last() must be negative'
              546  CALL_FUNCTION_1       1  ''
              548  RAISE_VARARGS_1       1  'exception instance'
              550  JUMP_FORWARD        556  'to 556'
            552_0  COME_FROM           478  '478'

 L. 308       552  LOAD_CONST               -1
              554  STORE_DEREF              'index'
            556_0  COME_FROM           550  '550'
            556_1  COME_FROM           538  '538'
            556_2  COME_FROM           448  '448'
            556_3  COME_FROM           436  '436'

 L. 309       556  LOAD_CLOSURE             'index'
              558  BUILD_TUPLE_1         1 
              560  LOAD_CODE                <code_object select>
              562  LOAD_STR                 'prepare_predicate.<locals>.select'
              564  MAKE_FUNCTION_8          'closure'
              566  STORE_FAST               'select'

 L. 320       568  LOAD_FAST                'select'
              570  RETURN_VALUE     
            572_0  COME_FROM           400  '400'

 L. 321       572  LOAD_GLOBAL              SyntaxError
              574  LOAD_STR                 'invalid predicate'
              576  CALL_FUNCTION_1       1  ''
              578  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<121>' instruction at offset 24


ops = {'':prepare_child, 
 '*':prepare_star, 
 '.':prepare_self, 
 '..':prepare_parent, 
 '//':prepare_descendant, 
 '[':prepare_predicate}
_cache = {}

class _SelectorContext:
    parent_map = None

    def __init__(self, root):
        self.root = root


def iterfind--- This code section failed: ---

 L. 346         0  LOAD_FAST                'path'
                2  LOAD_CONST               -1
                4  LOAD_CONST               None
                6  BUILD_SLICE_2         2 
                8  BINARY_SUBSCR    
               10  LOAD_STR                 '/'
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 347        16  LOAD_FAST                'path'
               18  LOAD_STR                 '*'
               20  BINARY_ADD       
               22  STORE_FAST               'path'
             24_0  COME_FROM            14  '14'

 L. 349        24  LOAD_FAST                'path'
               26  BUILD_TUPLE_1         1 
               28  STORE_FAST               'cache_key'

 L. 350        30  LOAD_FAST                'namespaces'
               32  POP_JUMP_IF_FALSE    54  'to 54'

 L. 351        34  LOAD_FAST                'cache_key'
               36  LOAD_GLOBAL              tuple
               38  LOAD_GLOBAL              sorted
               40  LOAD_FAST                'namespaces'
               42  LOAD_METHOD              items
               44  CALL_METHOD_0         0  ''
               46  CALL_FUNCTION_1       1  ''
               48  CALL_FUNCTION_1       1  ''
               50  INPLACE_ADD      
               52  STORE_FAST               'cache_key'
             54_0  COME_FROM            32  '32'

 L. 353        54  SETUP_FINALLY        68  'to 68'

 L. 354        56  LOAD_GLOBAL              _cache
               58  LOAD_FAST                'cache_key'
               60  BINARY_SUBSCR    
               62  STORE_FAST               'selector'
               64  POP_BLOCK        
               66  JUMP_FORWARD        312  'to 312'
             68_0  COME_FROM_FINALLY    54  '54'

 L. 355        68  DUP_TOP          
               70  LOAD_GLOBAL              KeyError
            72_74  <121>               310  ''
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 356        82  LOAD_GLOBAL              len
               84  LOAD_GLOBAL              _cache
               86  CALL_FUNCTION_1       1  ''
               88  LOAD_CONST               100
               90  COMPARE_OP               >
               92  POP_JUMP_IF_FALSE   102  'to 102'

 L. 357        94  LOAD_GLOBAL              _cache
               96  LOAD_METHOD              clear
               98  CALL_METHOD_0         0  ''
              100  POP_TOP          
            102_0  COME_FROM            92  '92'

 L. 358       102  LOAD_FAST                'path'
              104  LOAD_CONST               None
              106  LOAD_CONST               1
              108  BUILD_SLICE_2         2 
              110  BINARY_SUBSCR    
              112  LOAD_STR                 '/'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   126  'to 126'

 L. 359       118  LOAD_GLOBAL              SyntaxError
              120  LOAD_STR                 'cannot use absolute path on element'
              122  CALL_FUNCTION_1       1  ''
              124  RAISE_VARARGS_1       1  'exception instance'
            126_0  COME_FROM           116  '116'

 L. 360       126  LOAD_GLOBAL              iter
              128  LOAD_GLOBAL              xpath_tokenizer
              130  LOAD_FAST                'path'
              132  LOAD_FAST                'namespaces'
              134  CALL_FUNCTION_2       2  ''
              136  CALL_FUNCTION_1       1  ''
              138  LOAD_ATTR                __next__
              140  STORE_FAST               'next'

 L. 361       142  SETUP_FINALLY       154  'to 154'

 L. 362       144  LOAD_FAST                'next'
              146  CALL_FUNCTION_0       0  ''
              148  STORE_FAST               'token'
              150  POP_BLOCK        
              152  JUMP_FORWARD        176  'to 176'
            154_0  COME_FROM_FINALLY   142  '142'

 L. 363       154  DUP_TOP          
              156  LOAD_GLOBAL              StopIteration
              158  <121>               174  ''
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L. 364       166  POP_EXCEPT       
              168  POP_EXCEPT       
              170  LOAD_CONST               None
              172  RETURN_VALUE     
              174  <48>             
            176_0  COME_FROM           152  '152'

 L. 365       176  BUILD_LIST_0          0 
              178  STORE_FAST               'selector'
            180_0  COME_FROM           296  '296'
            180_1  COME_FROM           292  '292'
            180_2  COME_FROM           268  '268'

 L. 367       180  SETUP_FINALLY       210  'to 210'

 L. 368       182  LOAD_FAST                'selector'
              184  LOAD_METHOD              append
              186  LOAD_GLOBAL              ops
              188  LOAD_FAST                'token'
              190  LOAD_CONST               0
              192  BINARY_SUBSCR    
              194  BINARY_SUBSCR    
              196  LOAD_FAST                'next'
              198  LOAD_FAST                'token'
              200  CALL_FUNCTION_2       2  ''
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          
              206  POP_BLOCK        
              208  JUMP_FORWARD        238  'to 238'
            210_0  COME_FROM_FINALLY   180  '180'

 L. 369       210  DUP_TOP          
              212  LOAD_GLOBAL              StopIteration
              214  <121>               236  ''
              216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L. 370       222  LOAD_GLOBAL              SyntaxError
              224  LOAD_STR                 'invalid path'
              226  CALL_FUNCTION_1       1  ''
              228  LOAD_CONST               None
              230  RAISE_VARARGS_2       2  'exception instance with __cause__'
              232  POP_EXCEPT       
              234  JUMP_FORWARD        238  'to 238'
              236  <48>             
            238_0  COME_FROM           234  '234'
            238_1  COME_FROM           208  '208'

 L. 371       238  SETUP_FINALLY       270  'to 270'

 L. 372       240  LOAD_FAST                'next'
              242  CALL_FUNCTION_0       0  ''
              244  STORE_FAST               'token'

 L. 373       246  LOAD_FAST                'token'
              248  LOAD_CONST               0
              250  BINARY_SUBSCR    
              252  LOAD_STR                 '/'
              254  COMPARE_OP               ==
          256_258  POP_JUMP_IF_FALSE   266  'to 266'

 L. 374       260  LOAD_FAST                'next'
              262  CALL_FUNCTION_0       0  ''
              264  STORE_FAST               'token'
            266_0  COME_FROM           256  '256'
              266  POP_BLOCK        
              268  JUMP_BACK           180  'to 180'
            270_0  COME_FROM_FINALLY   238  '238'

 L. 375       270  DUP_TOP          
              272  LOAD_GLOBAL              StopIteration
          274_276  <121>               294  ''
              278  POP_TOP          
              280  POP_TOP          
              282  POP_TOP          

 L. 376       284  POP_EXCEPT       
          286_288  BREAK_LOOP          298  'to 298'
              290  POP_EXCEPT       
              292  JUMP_BACK           180  'to 180'
              294  <48>             
              296  JUMP_BACK           180  'to 180'
            298_0  COME_FROM           286  '286'

 L. 377       298  LOAD_FAST                'selector'
              300  LOAD_GLOBAL              _cache
              302  LOAD_FAST                'cache_key'
              304  STORE_SUBSCR     
              306  POP_EXCEPT       
              308  JUMP_FORWARD        312  'to 312'
              310  <48>             
            312_0  COME_FROM           308  '308'
            312_1  COME_FROM            66  '66'

 L. 379       312  LOAD_FAST                'elem'
              314  BUILD_LIST_1          1 
              316  STORE_FAST               'result'

 L. 380       318  LOAD_GLOBAL              _SelectorContext
              320  LOAD_FAST                'elem'
              322  CALL_FUNCTION_1       1  ''
              324  STORE_FAST               'context'

 L. 381       326  LOAD_FAST                'selector'
              328  GET_ITER         
            330_0  COME_FROM           344  '344'
              330  FOR_ITER            348  'to 348'
              332  STORE_FAST               'select'

 L. 382       334  LOAD_FAST                'select'
              336  LOAD_FAST                'context'
              338  LOAD_FAST                'result'
              340  CALL_FUNCTION_2       2  ''
              342  STORE_FAST               'result'
          344_346  JUMP_BACK           330  'to 330'
            348_0  COME_FROM           330  '330'

 L. 383       348  LOAD_FAST                'result'
              350  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 72_74


def find(elem, path, namespaces=None):
    return next(iterfind(elem, path, namespaces), None)


def findall(elem, path, namespaces=None):
    return list(iterfind(elem, path, namespaces))


def findtext--- This code section failed: ---

 L. 401         0  SETUP_FINALLY        30  'to 30'

 L. 402         2  LOAD_GLOBAL              next
                4  LOAD_GLOBAL              iterfind
                6  LOAD_FAST                'elem'
                8  LOAD_FAST                'path'
               10  LOAD_FAST                'namespaces'
               12  CALL_FUNCTION_3       3  ''
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'elem'

 L. 403        18  LOAD_FAST                'elem'
               20  LOAD_ATTR                text
               22  JUMP_IF_TRUE_OR_POP    26  'to 26'
               24  LOAD_STR                 ''
             26_0  COME_FROM            22  '22'
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY     0  '0'

 L. 404        30  DUP_TOP          
               32  LOAD_GLOBAL              StopIteration
               34  <121>                50  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 405        42  LOAD_FAST                'default'
               44  ROT_FOUR         
               46  POP_EXCEPT       
               48  RETURN_VALUE     
               50  <48>             

Parse error at or near `<121>' instruction at offset 34