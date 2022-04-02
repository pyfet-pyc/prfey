# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: lib2to3\pgen2\pgen.py
from . import grammar, token, tokenize

class PgenGrammar(grammar.Grammar):
    pass


class ParserGenerator(object):

    def __init__--- This code section failed: ---

 L.  13         0  LOAD_CONST               None
                2  STORE_FAST               'close_stream'

 L.  14         4  LOAD_FAST                'stream'
                6  LOAD_CONST               None
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    26  'to 26'

 L.  15        12  LOAD_GLOBAL              open
               14  LOAD_FAST                'filename'
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'stream'

 L.  16        20  LOAD_FAST                'stream'
               22  LOAD_ATTR                close
               24  STORE_FAST               'close_stream'
             26_0  COME_FROM            10  '10'

 L.  17        26  LOAD_FAST                'filename'
               28  LOAD_FAST                'self'
               30  STORE_ATTR               filename

 L.  18        32  LOAD_FAST                'stream'
               34  LOAD_FAST                'self'
               36  STORE_ATTR               stream

 L.  19        38  LOAD_GLOBAL              tokenize
               40  LOAD_METHOD              generate_tokens
               42  LOAD_FAST                'stream'
               44  LOAD_ATTR                readline
               46  CALL_METHOD_1         1  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               generator

 L.  20        52  LOAD_FAST                'self'
               54  LOAD_METHOD              gettoken
               56  CALL_METHOD_0         0  ''
               58  POP_TOP          

 L.  21        60  LOAD_FAST                'self'
               62  LOAD_METHOD              parse
               64  CALL_METHOD_0         0  ''
               66  UNPACK_SEQUENCE_2     2 
               68  LOAD_FAST                'self'
               70  STORE_ATTR               dfas
               72  LOAD_FAST                'self'
               74  STORE_ATTR               startsymbol

 L.  22        76  LOAD_FAST                'close_stream'
               78  LOAD_CONST               None
               80  <117>                 1  ''
               82  POP_JUMP_IF_FALSE    90  'to 90'

 L.  23        84  LOAD_FAST                'close_stream'
               86  CALL_FUNCTION_0       0  ''
               88  POP_TOP          
             90_0  COME_FROM            82  '82'

 L.  24        90  BUILD_MAP_0           0 
               92  LOAD_FAST                'self'
               94  STORE_ATTR               first

 L.  25        96  LOAD_FAST                'self'
               98  LOAD_METHOD              addfirstsets
              100  CALL_METHOD_0         0  ''
              102  POP_TOP          

Parse error at or near `<117>' instruction at offset 8

    def make_grammar(self):
        c = PgenGrammar
        names = list(self.dfas.keys)
        names.sort
        names.removeself.startsymbol
        names.insert(0, self.startsymbol)
        for name in names:
            i = 256 + len(c.symbol2number)
            c.symbol2number[name] = i
            c.number2symbol[i] = name
        else:
            for name in names:
                dfa = self.dfas[name]
                states = []
                for state in dfa:
                    arcs = []
                    for label, next in sorted(state.arcs.items):
                        arcs.append(self.make_label(c, label), dfa.indexnext)

                    if state.isfinal:
                        arcs.append(0, dfa.indexstate)
                    else:
                        states.appendarcs
                else:
                    c.states.appendstates
                    c.dfas[c.symbol2number[name]] = (states, self.make_first(c, name))

            else:
                c.start = c.symbol2number[self.startsymbol]
                return c

    def make_first(self, c, name):
        rawfirst = self.first[name]
        first = {}
        for label in sorted(rawfirst):
            ilabel = self.make_label(c, label)
            first[ilabel] = 1
        else:
            return first

    def make_label--- This code section failed: ---

 L.  63         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'c'
                4  LOAD_ATTR                labels
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'ilabel'

 L.  64        10  LOAD_FAST                'label'
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  LOAD_METHOD              isalpha
               18  CALL_METHOD_0         0  ''
               20  POP_JUMP_IF_FALSE   190  'to 190'

 L.  66        22  LOAD_FAST                'label'
               24  LOAD_FAST                'c'
               26  LOAD_ATTR                symbol2number
               28  <118>                 0  ''
               30  POP_JUMP_IF_FALSE    90  'to 90'

 L.  68        32  LOAD_FAST                'label'
               34  LOAD_FAST                'c'
               36  LOAD_ATTR                symbol2label
               38  <118>                 0  ''
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L.  69        42  LOAD_FAST                'c'
               44  LOAD_ATTR                symbol2label
               46  LOAD_FAST                'label'
               48  BINARY_SUBSCR    
               50  RETURN_VALUE     
             52_0  COME_FROM            40  '40'

 L.  71        52  LOAD_FAST                'c'
               54  LOAD_ATTR                labels
               56  LOAD_METHOD              append
               58  LOAD_FAST                'c'
               60  LOAD_ATTR                symbol2number
               62  LOAD_FAST                'label'
               64  BINARY_SUBSCR    
               66  LOAD_CONST               None
               68  BUILD_TUPLE_2         2 
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          

 L.  72        74  LOAD_FAST                'ilabel'
               76  LOAD_FAST                'c'
               78  LOAD_ATTR                symbol2label
               80  LOAD_FAST                'label'
               82  STORE_SUBSCR     

 L.  73        84  LOAD_FAST                'ilabel'
               86  RETURN_VALUE     
               88  JUMP_FORWARD        188  'to 188'
             90_0  COME_FROM            30  '30'

 L.  76        90  LOAD_GLOBAL              getattr
               92  LOAD_GLOBAL              token
               94  LOAD_FAST                'label'
               96  LOAD_CONST               None
               98  CALL_FUNCTION_3       3  ''
              100  STORE_FAST               'itoken'

 L.  77       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                'itoken'
              106  LOAD_GLOBAL              int
              108  CALL_FUNCTION_2       2  ''
              110  POP_JUMP_IF_TRUE    120  'to 120'
              112  <74>             
              114  LOAD_FAST                'label'
              116  CALL_FUNCTION_1       1  ''
              118  RAISE_VARARGS_1       1  'exception instance'
            120_0  COME_FROM           110  '110'

 L.  78       120  LOAD_FAST                'itoken'
              122  LOAD_GLOBAL              token
              124  LOAD_ATTR                tok_name
              126  <118>                 0  ''
              128  POP_JUMP_IF_TRUE    138  'to 138'
              130  <74>             
              132  LOAD_FAST                'label'
              134  CALL_FUNCTION_1       1  ''
              136  RAISE_VARARGS_1       1  'exception instance'
            138_0  COME_FROM           128  '128'

 L.  79       138  LOAD_FAST                'itoken'
              140  LOAD_FAST                'c'
              142  LOAD_ATTR                tokens
              144  <118>                 0  ''
              146  POP_JUMP_IF_FALSE   158  'to 158'

 L.  80       148  LOAD_FAST                'c'
              150  LOAD_ATTR                tokens
              152  LOAD_FAST                'itoken'
              154  BINARY_SUBSCR    
              156  RETURN_VALUE     
            158_0  COME_FROM           146  '146'

 L.  82       158  LOAD_FAST                'c'
              160  LOAD_ATTR                labels
              162  LOAD_METHOD              append
              164  LOAD_FAST                'itoken'
              166  LOAD_CONST               None
              168  BUILD_TUPLE_2         2 
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          

 L.  83       174  LOAD_FAST                'ilabel'
              176  LOAD_FAST                'c'
              178  LOAD_ATTR                tokens
              180  LOAD_FAST                'itoken'
              182  STORE_SUBSCR     

 L.  84       184  LOAD_FAST                'ilabel'
              186  RETURN_VALUE     
            188_0  COME_FROM            88  '88'
              188  JUMP_FORWARD        350  'to 350'
            190_0  COME_FROM            20  '20'

 L.  87       190  LOAD_FAST                'label'
              192  LOAD_CONST               0
              194  BINARY_SUBSCR    
              196  LOAD_CONST               ('"', "'")
              198  <118>                 0  ''
              200  POP_JUMP_IF_TRUE    210  'to 210'
              202  <74>             
              204  LOAD_FAST                'label'
              206  CALL_FUNCTION_1       1  ''
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           200  '200'

 L.  88       210  LOAD_GLOBAL              eval
              212  LOAD_FAST                'label'
              214  CALL_FUNCTION_1       1  ''
              216  STORE_FAST               'value'

 L.  89       218  LOAD_FAST                'value'
              220  LOAD_CONST               0
              222  BINARY_SUBSCR    
              224  LOAD_METHOD              isalpha
              226  CALL_METHOD_0         0  ''
          228_230  POP_JUMP_IF_FALSE   288  'to 288'

 L.  91       232  LOAD_FAST                'value'
              234  LOAD_FAST                'c'
              236  LOAD_ATTR                keywords
              238  <118>                 0  ''
          240_242  POP_JUMP_IF_FALSE   254  'to 254'

 L.  92       244  LOAD_FAST                'c'
              246  LOAD_ATTR                keywords
              248  LOAD_FAST                'value'
              250  BINARY_SUBSCR    
              252  RETURN_VALUE     
            254_0  COME_FROM           240  '240'

 L.  94       254  LOAD_FAST                'c'
              256  LOAD_ATTR                labels
              258  LOAD_METHOD              append
              260  LOAD_GLOBAL              token
              262  LOAD_ATTR                NAME
              264  LOAD_FAST                'value'
              266  BUILD_TUPLE_2         2 
              268  CALL_METHOD_1         1  ''
              270  POP_TOP          

 L.  95       272  LOAD_FAST                'ilabel'
              274  LOAD_FAST                'c'
              276  LOAD_ATTR                keywords
              278  LOAD_FAST                'value'
              280  STORE_SUBSCR     

 L.  96       282  LOAD_FAST                'ilabel'
              284  RETURN_VALUE     
              286  JUMP_FORWARD        350  'to 350'
            288_0  COME_FROM           228  '228'

 L.  99       288  LOAD_GLOBAL              grammar
              290  LOAD_ATTR                opmap
              292  LOAD_FAST                'value'
              294  BINARY_SUBSCR    
              296  STORE_FAST               'itoken'

 L. 100       298  LOAD_FAST                'itoken'
              300  LOAD_FAST                'c'
              302  LOAD_ATTR                tokens
              304  <118>                 0  ''
          306_308  POP_JUMP_IF_FALSE   320  'to 320'

 L. 101       310  LOAD_FAST                'c'
              312  LOAD_ATTR                tokens
              314  LOAD_FAST                'itoken'
              316  BINARY_SUBSCR    
              318  RETURN_VALUE     
            320_0  COME_FROM           306  '306'

 L. 103       320  LOAD_FAST                'c'
              322  LOAD_ATTR                labels
              324  LOAD_METHOD              append
              326  LOAD_FAST                'itoken'
              328  LOAD_CONST               None
              330  BUILD_TUPLE_2         2 
              332  CALL_METHOD_1         1  ''
              334  POP_TOP          

 L. 104       336  LOAD_FAST                'ilabel'
              338  LOAD_FAST                'c'
              340  LOAD_ATTR                tokens
              342  LOAD_FAST                'itoken'
              344  STORE_SUBSCR     

 L. 105       346  LOAD_FAST                'ilabel'
              348  RETURN_VALUE     
            350_0  COME_FROM           286  '286'
            350_1  COME_FROM           188  '188'

Parse error at or near `<118>' instruction at offset 28

    def addfirstsets--- This code section failed: ---

 L. 108         0  LOAD_GLOBAL              list
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                dfas
                6  LOAD_METHOD              keys
                8  CALL_METHOD_0         0  ''
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'names'

 L. 109        14  LOAD_FAST                'names'
               16  LOAD_METHOD              sort
               18  CALL_METHOD_0         0  ''
               20  POP_TOP          

 L. 110        22  LOAD_FAST                'names'
               24  GET_ITER         
             26_0  COME_FROM            50  '50'
             26_1  COME_FROM            38  '38'
               26  FOR_ITER             52  'to 52'
               28  STORE_FAST               'name'

 L. 111        30  LOAD_FAST                'name'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                first
               36  <118>                 1  ''
               38  POP_JUMP_IF_FALSE_BACK    26  'to 26'

 L. 112        40  LOAD_FAST                'self'
               42  LOAD_METHOD              calcfirst
               44  LOAD_FAST                'name'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
               50  JUMP_BACK            26  'to 26'
             52_0  COME_FROM            26  '26'

Parse error at or near `<118>' instruction at offset 36

    def calcfirst--- This code section failed: ---

 L. 116         0  LOAD_FAST                'self'
                2  LOAD_ATTR                dfas
                4  LOAD_FAST                'name'
                6  BINARY_SUBSCR    
                8  STORE_FAST               'dfa'

 L. 117        10  LOAD_CONST               None
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                first
               16  LOAD_FAST                'name'
               18  STORE_SUBSCR     

 L. 118        20  LOAD_FAST                'dfa'
               22  LOAD_CONST               0
               24  BINARY_SUBSCR    
               26  STORE_FAST               'state'

 L. 119        28  BUILD_MAP_0           0 
               30  STORE_FAST               'totalset'

 L. 120        32  BUILD_MAP_0           0 
               34  STORE_FAST               'overlapcheck'

 L. 121        36  LOAD_FAST                'state'
               38  LOAD_ATTR                arcs
               40  LOAD_METHOD              items
               42  CALL_METHOD_0         0  ''
               44  GET_ITER         
             46_0  COME_FROM           166  '166'
             46_1  COME_FROM           144  '144'
               46  FOR_ITER            168  'to 168'
               48  UNPACK_SEQUENCE_2     2 
               50  STORE_FAST               'label'
               52  STORE_FAST               'next'

 L. 122        54  LOAD_FAST                'label'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                dfas
               60  <118>                 0  ''
               62  POP_JUMP_IF_FALSE   146  'to 146'

 L. 123        64  LOAD_FAST                'label'
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                first
               70  <118>                 0  ''
               72  POP_JUMP_IF_FALSE   106  'to 106'

 L. 124        74  LOAD_FAST                'self'
               76  LOAD_ATTR                first
               78  LOAD_FAST                'label'
               80  BINARY_SUBSCR    
               82  STORE_FAST               'fset'

 L. 125        84  LOAD_FAST                'fset'
               86  LOAD_CONST               None
               88  <117>                 0  ''
               90  POP_JUMP_IF_FALSE   126  'to 126'

 L. 126        92  LOAD_GLOBAL              ValueError
               94  LOAD_STR                 'recursion for rule %r'
               96  LOAD_FAST                'name'
               98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
              104  JUMP_FORWARD        126  'to 126'
            106_0  COME_FROM            72  '72'

 L. 128       106  LOAD_FAST                'self'
              108  LOAD_METHOD              calcfirst
              110  LOAD_FAST                'label'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

 L. 129       116  LOAD_FAST                'self'
              118  LOAD_ATTR                first
              120  LOAD_FAST                'label'
              122  BINARY_SUBSCR    
              124  STORE_FAST               'fset'
            126_0  COME_FROM           104  '104'
            126_1  COME_FROM            90  '90'

 L. 130       126  LOAD_FAST                'totalset'
              128  LOAD_METHOD              update
              130  LOAD_FAST                'fset'
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          

 L. 131       136  LOAD_FAST                'fset'
              138  LOAD_FAST                'overlapcheck'
              140  LOAD_FAST                'label'
              142  STORE_SUBSCR     
              144  JUMP_BACK            46  'to 46'
            146_0  COME_FROM            62  '62'

 L. 133       146  LOAD_CONST               1
              148  LOAD_FAST                'totalset'
              150  LOAD_FAST                'label'
              152  STORE_SUBSCR     

 L. 134       154  LOAD_FAST                'label'
              156  LOAD_CONST               1
              158  BUILD_MAP_1           1 
              160  LOAD_FAST                'overlapcheck'
              162  LOAD_FAST                'label'
              164  STORE_SUBSCR     
              166  JUMP_BACK            46  'to 46'
            168_0  COME_FROM            46  '46'

 L. 135       168  BUILD_MAP_0           0 
              170  STORE_FAST               'inverse'

 L. 136       172  LOAD_FAST                'overlapcheck'
              174  LOAD_METHOD              items
              176  CALL_METHOD_0         0  ''
              178  GET_ITER         
            180_0  COME_FROM           238  '238'
              180  FOR_ITER            240  'to 240'
              182  UNPACK_SEQUENCE_2     2 
              184  STORE_FAST               'label'
              186  STORE_FAST               'itsfirst'

 L. 137       188  LOAD_FAST                'itsfirst'
              190  GET_ITER         
            192_0  COME_FROM           236  '236'
              192  FOR_ITER            238  'to 238'
              194  STORE_FAST               'symbol'

 L. 138       196  LOAD_FAST                'symbol'
              198  LOAD_FAST                'inverse'
              200  <118>                 0  ''
              202  POP_JUMP_IF_FALSE   228  'to 228'

 L. 139       204  LOAD_GLOBAL              ValueError
              206  LOAD_STR                 'rule %s is ambiguous; %s is in the first sets of %s as well as %s'

 L. 141       208  LOAD_FAST                'name'
              210  LOAD_FAST                'symbol'
              212  LOAD_FAST                'label'
              214  LOAD_FAST                'inverse'
              216  LOAD_FAST                'symbol'
              218  BINARY_SUBSCR    
              220  BUILD_TUPLE_4         4 

 L. 139       222  BINARY_MODULO    
              224  CALL_FUNCTION_1       1  ''
              226  RAISE_VARARGS_1       1  'exception instance'
            228_0  COME_FROM           202  '202'

 L. 142       228  LOAD_FAST                'label'
              230  LOAD_FAST                'inverse'
              232  LOAD_FAST                'symbol'
              234  STORE_SUBSCR     
              236  JUMP_BACK           192  'to 192'
            238_0  COME_FROM           192  '192'
              238  JUMP_BACK           180  'to 180'
            240_0  COME_FROM           180  '180'

 L. 143       240  LOAD_FAST                'totalset'
              242  LOAD_FAST                'self'
              244  LOAD_ATTR                first
              246  LOAD_FAST                'name'
              248  STORE_SUBSCR     

Parse error at or near `<118>' instruction at offset 60

    def parse--- This code section failed: ---

 L. 146         0  BUILD_MAP_0           0 
                2  STORE_FAST               'dfas'

 L. 147         4  LOAD_CONST               None
                6  STORE_FAST               'startsymbol'
              8_0  COME_FROM           150  '150'
              8_1  COME_FROM           144  '144'

 L. 149         8  LOAD_FAST                'self'
               10  LOAD_ATTR                type
               12  LOAD_GLOBAL              token
               14  LOAD_ATTR                ENDMARKER
               16  COMPARE_OP               !=
               18  POP_JUMP_IF_FALSE   152  'to 152'
             20_0  COME_FROM            40  '40'

 L. 150        20  LOAD_FAST                'self'
               22  LOAD_ATTR                type
               24  LOAD_GLOBAL              token
               26  LOAD_ATTR                NEWLINE
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    42  'to 42'

 L. 151        32  LOAD_FAST                'self'
               34  LOAD_METHOD              gettoken
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          
               40  JUMP_BACK            20  'to 20'
             42_0  COME_FROM            30  '30'

 L. 153        42  LOAD_FAST                'self'
               44  LOAD_METHOD              expect
               46  LOAD_GLOBAL              token
               48  LOAD_ATTR                NAME
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'name'

 L. 154        54  LOAD_FAST                'self'
               56  LOAD_METHOD              expect
               58  LOAD_GLOBAL              token
               60  LOAD_ATTR                OP
               62  LOAD_STR                 ':'
               64  CALL_METHOD_2         2  ''
               66  POP_TOP          

 L. 155        68  LOAD_FAST                'self'
               70  LOAD_METHOD              parse_rhs
               72  CALL_METHOD_0         0  ''
               74  UNPACK_SEQUENCE_2     2 
               76  STORE_FAST               'a'
               78  STORE_FAST               'z'

 L. 156        80  LOAD_FAST                'self'
               82  LOAD_METHOD              expect
               84  LOAD_GLOBAL              token
               86  LOAD_ATTR                NEWLINE
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L. 158        92  LOAD_FAST                'self'
               94  LOAD_METHOD              make_dfa
               96  LOAD_FAST                'a'
               98  LOAD_FAST                'z'
              100  CALL_METHOD_2         2  ''
              102  STORE_FAST               'dfa'

 L. 160       104  LOAD_GLOBAL              len
              106  LOAD_FAST                'dfa'
              108  CALL_FUNCTION_1       1  ''
              110  STORE_FAST               'oldlen'

 L. 161       112  LOAD_FAST                'self'
              114  LOAD_METHOD              simplify_dfa
              116  LOAD_FAST                'dfa'
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 162       122  LOAD_GLOBAL              len
              124  LOAD_FAST                'dfa'
              126  CALL_FUNCTION_1       1  ''
              128  STORE_FAST               'newlen'

 L. 163       130  LOAD_FAST                'dfa'
              132  LOAD_FAST                'dfas'
              134  LOAD_FAST                'name'
              136  STORE_SUBSCR     

 L. 165       138  LOAD_FAST                'startsymbol'
              140  LOAD_CONST               None
              142  <117>                 0  ''
              144  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L. 166       146  LOAD_FAST                'name'
              148  STORE_FAST               'startsymbol'
              150  JUMP_BACK             8  'to 8'
            152_0  COME_FROM            18  '18'

 L. 167       152  LOAD_FAST                'dfas'
              154  LOAD_FAST                'startsymbol'
              156  BUILD_TUPLE_2         2 
              158  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 142

    def make_dfa--- This code section failed: ---

 L. 174         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'start'
                4  LOAD_GLOBAL              NFAState
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 175        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'finish'
               18  LOAD_GLOBAL              NFAState
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_TRUE     28  'to 28'
               24  <74>             
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'

 L. 176        28  LOAD_CLOSURE             'addclosure'
               30  BUILD_TUPLE_1         1 
               32  LOAD_CODE                <code_object closure>
               34  LOAD_STR                 'ParserGenerator.make_dfa.<locals>.closure'
               36  MAKE_FUNCTION_8          'closure'
               38  STORE_FAST               'closure'

 L. 180        40  LOAD_CLOSURE             'addclosure'
               42  BUILD_TUPLE_1         1 
               44  LOAD_CODE                <code_object addclosure>
               46  LOAD_STR                 'ParserGenerator.make_dfa.<locals>.addclosure'
               48  MAKE_FUNCTION_8          'closure'
               50  STORE_DEREF              'addclosure'

 L. 188        52  LOAD_GLOBAL              DFAState
               54  LOAD_FAST                'closure'
               56  LOAD_FAST                'start'
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_FAST                'finish'
               62  CALL_FUNCTION_2       2  ''
               64  BUILD_LIST_1          1 
               66  STORE_FAST               'states'

 L. 189        68  LOAD_FAST                'states'
               70  GET_ITER         
             72_0  COME_FROM           212  '212'
               72  FOR_ITER            214  'to 214'
               74  STORE_FAST               'state'

 L. 190        76  BUILD_MAP_0           0 
               78  STORE_FAST               'arcs'

 L. 191        80  LOAD_FAST                'state'
               82  LOAD_ATTR                nfaset
               84  GET_ITER         
             86_0  COME_FROM           132  '132'
               86  FOR_ITER            134  'to 134'
               88  STORE_FAST               'nfastate'

 L. 192        90  LOAD_FAST                'nfastate'
               92  LOAD_ATTR                arcs
               94  GET_ITER         
             96_0  COME_FROM           130  '130'
             96_1  COME_FROM           110  '110'
               96  FOR_ITER            132  'to 132'
               98  UNPACK_SEQUENCE_2     2 
              100  STORE_FAST               'label'
              102  STORE_FAST               'next'

 L. 193       104  LOAD_FAST                'label'
              106  LOAD_CONST               None
              108  <117>                 1  ''
              110  POP_JUMP_IF_FALSE_BACK    96  'to 96'

 L. 194       112  LOAD_DEREF               'addclosure'
              114  LOAD_FAST                'next'
              116  LOAD_FAST                'arcs'
              118  LOAD_METHOD              setdefault
              120  LOAD_FAST                'label'
              122  BUILD_MAP_0           0 
              124  CALL_METHOD_2         2  ''
              126  CALL_FUNCTION_2       2  ''
              128  POP_TOP          
              130  JUMP_BACK            96  'to 96'
            132_0  COME_FROM            96  '96'
              132  JUMP_BACK            86  'to 86'
            134_0  COME_FROM            86  '86'

 L. 195       134  LOAD_GLOBAL              sorted
              136  LOAD_FAST                'arcs'
              138  LOAD_METHOD              items
              140  CALL_METHOD_0         0  ''
              142  CALL_FUNCTION_1       1  ''
              144  GET_ITER         
            146_0  COME_FROM           210  '210'
              146  FOR_ITER            212  'to 212'
              148  UNPACK_SEQUENCE_2     2 
              150  STORE_FAST               'label'
              152  STORE_FAST               'nfaset'

 L. 196       154  LOAD_FAST                'states'
              156  GET_ITER         
            158_0  COME_FROM           176  '176'
            158_1  COME_FROM           170  '170'
              158  FOR_ITER            178  'to 178'
              160  STORE_FAST               'st'

 L. 197       162  LOAD_FAST                'st'
              164  LOAD_ATTR                nfaset
              166  LOAD_FAST                'nfaset'
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE_BACK   158  'to 158'

 L. 198       172  POP_TOP          
              174  BREAK_LOOP          198  'to 198'
              176  JUMP_BACK           158  'to 158'
            178_0  COME_FROM           158  '158'

 L. 200       178  LOAD_GLOBAL              DFAState
              180  LOAD_FAST                'nfaset'
              182  LOAD_FAST                'finish'
              184  CALL_FUNCTION_2       2  ''
              186  STORE_FAST               'st'

 L. 201       188  LOAD_FAST                'states'
              190  LOAD_METHOD              append
              192  LOAD_FAST                'st'
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          
            198_0  COME_FROM           174  '174'

 L. 202       198  LOAD_FAST                'state'
              200  LOAD_METHOD              addarc
              202  LOAD_FAST                'st'
              204  LOAD_FAST                'label'
              206  CALL_METHOD_2         2  ''
              208  POP_TOP          
              210  JUMP_BACK           146  'to 146'
            212_0  COME_FROM           146  '146'
              212  JUMP_BACK            72  'to 72'
            214_0  COME_FROM            72  '72'

 L. 203       214  LOAD_FAST                'states'
              216  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def dump_nfa--- This code section failed: ---

 L. 206         0  LOAD_GLOBAL              print
                2  LOAD_STR                 'Dump of NFA for'
                4  LOAD_FAST                'name'
                6  CALL_FUNCTION_2       2  ''
                8  POP_TOP          

 L. 207        10  LOAD_FAST                'start'
               12  BUILD_LIST_1          1 
               14  STORE_FAST               'todo'

 L. 208        16  LOAD_GLOBAL              enumerate
               18  LOAD_FAST                'todo'
               20  CALL_FUNCTION_1       1  ''
               22  GET_ITER         
             24_0  COME_FROM           148  '148'
               24  FOR_ITER            150  'to 150'
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'i'
               30  STORE_FAST               'state'

 L. 209        32  LOAD_GLOBAL              print
               34  LOAD_STR                 '  State'
               36  LOAD_FAST                'i'
               38  LOAD_FAST                'state'
               40  LOAD_FAST                'finish'
               42  <117>                 0  ''
               44  POP_JUMP_IF_FALSE    50  'to 50'
               46  LOAD_STR                 '(final)'
               48  JUMP_IF_TRUE_OR_POP    52  'to 52'
             50_0  COME_FROM            44  '44'
               50  LOAD_STR                 ''
             52_0  COME_FROM            48  '48'
               52  CALL_FUNCTION_3       3  ''
               54  POP_TOP          

 L. 210        56  LOAD_FAST                'state'
               58  LOAD_ATTR                arcs
               60  GET_ITER         
             62_0  COME_FROM           146  '146'
             62_1  COME_FROM           128  '128'
               62  FOR_ITER            148  'to 148'
               64  UNPACK_SEQUENCE_2     2 
               66  STORE_FAST               'label'
               68  STORE_FAST               'next'

 L. 211        70  LOAD_FAST                'next'
               72  LOAD_FAST                'todo'
               74  <118>                 0  ''
               76  POP_JUMP_IF_FALSE    90  'to 90'

 L. 212        78  LOAD_FAST                'todo'
               80  LOAD_METHOD              index
               82  LOAD_FAST                'next'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'j'
               88  JUMP_FORWARD        108  'to 108'
             90_0  COME_FROM            76  '76'

 L. 214        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'todo'
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'j'

 L. 215        98  LOAD_FAST                'todo'
              100  LOAD_METHOD              append
              102  LOAD_FAST                'next'
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
            108_0  COME_FROM            88  '88'

 L. 216       108  LOAD_FAST                'label'
              110  LOAD_CONST               None
              112  <117>                 0  ''
              114  POP_JUMP_IF_FALSE   130  'to 130'

 L. 217       116  LOAD_GLOBAL              print
              118  LOAD_STR                 '    -> %d'
              120  LOAD_FAST                'j'
              122  BINARY_MODULO    
              124  CALL_FUNCTION_1       1  ''
              126  POP_TOP          
              128  JUMP_BACK            62  'to 62'
            130_0  COME_FROM           114  '114'

 L. 219       130  LOAD_GLOBAL              print
              132  LOAD_STR                 '    %s -> %d'
              134  LOAD_FAST                'label'
              136  LOAD_FAST                'j'
              138  BUILD_TUPLE_2         2 
              140  BINARY_MODULO    
              142  CALL_FUNCTION_1       1  ''
              144  POP_TOP          
              146  JUMP_BACK            62  'to 62'
            148_0  COME_FROM            62  '62'
              148  JUMP_BACK            24  'to 24'
            150_0  COME_FROM            24  '24'

Parse error at or near `<117>' instruction at offset 42

    def dump_dfa(self, name, dfa):
        print'Dump of DFA for'name
        for i, state in enumerate(dfa):
            print('  State', i, (state.isfinal) and '(final)' or '')
            for label, next in sorted(state.arcs.items):
                print('    %s -> %d' % (label, dfa.indexnext))

    def simplify_dfa(self, dfa):
        changes = True
        while changes:
            changes = False
            for i, state_i in enumerate(dfa):
                for j in range(i + 1)len(dfa):
                    state_j = dfa[j]
                    if state_i == state_j:
                        del dfa[j]
                        for state in dfa:
                            state.unifystate(state_j, state_i)
                        else:
                            changes = True
                            break

    def parse_rhs(self):
        a, z = self.parse_alt
        if self.value != '|':
            return (a, z)
        aa = NFAState
        zz = NFAState
        aa.addarca
        z.addarczz
        while True:
            if self.value == '|':
                self.gettoken
                a, z = self.parse_alt
                aa.addarca
                z.addarczz

        return (
         aa, zz)

    def parse_alt--- This code section failed: ---

 L. 268         0  LOAD_FAST                'self'
                2  LOAD_METHOD              parse_item
                4  CALL_METHOD_0         0  ''
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'a'
               10  STORE_FAST               'b'
             12_0  COME_FROM            66  '66'

 L. 269        12  LOAD_FAST                'self'
               14  LOAD_ATTR                value
               16  LOAD_CONST               ('(', '[')
               18  <118>                 0  ''
               20  POP_JUMP_IF_TRUE     40  'to 40'

 L. 270        22  LOAD_FAST                'self'
               24  LOAD_ATTR                type
               26  LOAD_GLOBAL              token
               28  LOAD_ATTR                NAME
               30  LOAD_GLOBAL              token
               32  LOAD_ATTR                STRING
               34  BUILD_TUPLE_2         2 
               36  <118>                 0  ''

 L. 269        38  POP_JUMP_IF_FALSE    68  'to 68'
             40_0  COME_FROM            20  '20'

 L. 271        40  LOAD_FAST                'self'
               42  LOAD_METHOD              parse_item
               44  CALL_METHOD_0         0  ''
               46  UNPACK_SEQUENCE_2     2 
               48  STORE_FAST               'c'
               50  STORE_FAST               'd'

 L. 272        52  LOAD_FAST                'b'
               54  LOAD_METHOD              addarc
               56  LOAD_FAST                'c'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L. 273        62  LOAD_FAST                'd'
               64  STORE_FAST               'b'
               66  JUMP_BACK            12  'to 12'
             68_0  COME_FROM            38  '38'

 L. 274        68  LOAD_FAST                'a'
               70  LOAD_FAST                'b'
               72  BUILD_TUPLE_2         2 
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 18

    def parse_item--- This code section failed: ---

 L. 278         0  LOAD_FAST                'self'
                2  LOAD_ATTR                value
                4  LOAD_STR                 '['
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    62  'to 62'

 L. 279        10  LOAD_FAST                'self'
               12  LOAD_METHOD              gettoken
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          

 L. 280        18  LOAD_FAST                'self'
               20  LOAD_METHOD              parse_rhs
               22  CALL_METHOD_0         0  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'a'
               28  STORE_FAST               'z'

 L. 281        30  LOAD_FAST                'self'
               32  LOAD_METHOD              expect
               34  LOAD_GLOBAL              token
               36  LOAD_ATTR                OP
               38  LOAD_STR                 ']'
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          

 L. 282        44  LOAD_FAST                'a'
               46  LOAD_METHOD              addarc
               48  LOAD_FAST                'z'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 283        54  LOAD_FAST                'a'
               56  LOAD_FAST                'z'
               58  BUILD_TUPLE_2         2 
               60  RETURN_VALUE     
             62_0  COME_FROM             8  '8'

 L. 285        62  LOAD_FAST                'self'
               64  LOAD_METHOD              parse_atom
               66  CALL_METHOD_0         0  ''
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'a'
               72  STORE_FAST               'z'

 L. 286        74  LOAD_FAST                'self'
               76  LOAD_ATTR                value
               78  STORE_FAST               'value'

 L. 287        80  LOAD_FAST                'value'
               82  LOAD_CONST               ('+', '*')
               84  <118>                 1  ''
               86  POP_JUMP_IF_FALSE    96  'to 96'

 L. 288        88  LOAD_FAST                'a'
               90  LOAD_FAST                'z'
               92  BUILD_TUPLE_2         2 
               94  RETURN_VALUE     
             96_0  COME_FROM            86  '86'

 L. 289        96  LOAD_FAST                'self'
               98  LOAD_METHOD              gettoken
              100  CALL_METHOD_0         0  ''
              102  POP_TOP          

 L. 290       104  LOAD_FAST                'z'
              106  LOAD_METHOD              addarc
              108  LOAD_FAST                'a'
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L. 291       114  LOAD_FAST                'value'
              116  LOAD_STR                 '+'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   130  'to 130'

 L. 292       122  LOAD_FAST                'a'
              124  LOAD_FAST                'z'
              126  BUILD_TUPLE_2         2 
              128  RETURN_VALUE     
            130_0  COME_FROM           120  '120'

 L. 294       130  LOAD_FAST                'a'
              132  LOAD_FAST                'a'
              134  BUILD_TUPLE_2         2 
              136  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 84

    def parse_atom--- This code section failed: ---

 L. 298         0  LOAD_FAST                'self'
                2  LOAD_ATTR                value
                4  LOAD_STR                 '('
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    52  'to 52'

 L. 299        10  LOAD_FAST                'self'
               12  LOAD_METHOD              gettoken
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          

 L. 300        18  LOAD_FAST                'self'
               20  LOAD_METHOD              parse_rhs
               22  CALL_METHOD_0         0  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'a'
               28  STORE_FAST               'z'

 L. 301        30  LOAD_FAST                'self'
               32  LOAD_METHOD              expect
               34  LOAD_GLOBAL              token
               36  LOAD_ATTR                OP
               38  LOAD_STR                 ')'
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          

 L. 302        44  LOAD_FAST                'a'
               46  LOAD_FAST                'z'
               48  BUILD_TUPLE_2         2 
               50  RETURN_VALUE     
             52_0  COME_FROM             8  '8'

 L. 303        52  LOAD_FAST                'self'
               54  LOAD_ATTR                type
               56  LOAD_GLOBAL              token
               58  LOAD_ATTR                NAME
               60  LOAD_GLOBAL              token
               62  LOAD_ATTR                STRING
               64  BUILD_TUPLE_2         2 
               66  <118>                 0  ''
               68  POP_JUMP_IF_FALSE   112  'to 112'

 L. 304        70  LOAD_GLOBAL              NFAState
               72  CALL_FUNCTION_0       0  ''
               74  STORE_FAST               'a'

 L. 305        76  LOAD_GLOBAL              NFAState
               78  CALL_FUNCTION_0       0  ''
               80  STORE_FAST               'z'

 L. 306        82  LOAD_FAST                'a'
               84  LOAD_METHOD              addarc
               86  LOAD_FAST                'z'
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                value
               92  CALL_METHOD_2         2  ''
               94  POP_TOP          

 L. 307        96  LOAD_FAST                'self'
               98  LOAD_METHOD              gettoken
              100  CALL_METHOD_0         0  ''
              102  POP_TOP          

 L. 308       104  LOAD_FAST                'a'
              106  LOAD_FAST                'z'
              108  BUILD_TUPLE_2         2 
              110  RETURN_VALUE     
            112_0  COME_FROM            68  '68'

 L. 310       112  LOAD_FAST                'self'
              114  LOAD_METHOD              raise_error
              116  LOAD_STR                 'expected (...) or NAME or STRING, got %s/%s'

 L. 311       118  LOAD_FAST                'self'
              120  LOAD_ATTR                type
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                value

 L. 310       126  CALL_METHOD_3         3  ''
              128  POP_TOP          

Parse error at or near `<118>' instruction at offset 66

    def expect--- This code section failed: ---

 L. 314         0  LOAD_FAST                'self'
                2  LOAD_ATTR                type
                4  LOAD_FAST                'type'
                6  COMPARE_OP               !=
                8  POP_JUMP_IF_TRUE     28  'to 28'
               10  LOAD_FAST                'value'
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    50  'to 50'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                value
               22  LOAD_FAST                'value'
               24  COMPARE_OP               !=
               26  POP_JUMP_IF_FALSE    50  'to 50'
             28_0  COME_FROM             8  '8'

 L. 315        28  LOAD_FAST                'self'
               30  LOAD_METHOD              raise_error
               32  LOAD_STR                 'expected %s/%s, got %s/%s'

 L. 316        34  LOAD_FAST                'type'
               36  LOAD_FAST                'value'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                type
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                value

 L. 315        46  CALL_METHOD_5         5  ''
               48  POP_TOP          
             50_0  COME_FROM            26  '26'
             50_1  COME_FROM            16  '16'

 L. 317        50  LOAD_FAST                'self'
               52  LOAD_ATTR                value
               54  STORE_FAST               'value'

 L. 318        56  LOAD_FAST                'self'
               58  LOAD_METHOD              gettoken
               60  CALL_METHOD_0         0  ''
               62  POP_TOP          

 L. 319        64  LOAD_FAST                'value'
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def gettoken--- This code section failed: ---

 L. 322         0  LOAD_GLOBAL              next
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                generator
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'tup'
             10_0  COME_FROM            40  '40'

 L. 323        10  LOAD_FAST                'tup'
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  LOAD_GLOBAL              tokenize
               18  LOAD_ATTR                COMMENT
               20  LOAD_GLOBAL              tokenize
               22  LOAD_ATTR                NL
               24  BUILD_TUPLE_2         2 
               26  <118>                 0  ''
               28  POP_JUMP_IF_FALSE    42  'to 42'

 L. 324        30  LOAD_GLOBAL              next
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                generator
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'tup'
               40  JUMP_BACK            10  'to 10'
             42_0  COME_FROM            28  '28'

 L. 325        42  LOAD_FAST                'tup'
               44  UNPACK_SEQUENCE_5     5 
               46  LOAD_FAST                'self'
               48  STORE_ATTR               type
               50  LOAD_FAST                'self'
               52  STORE_ATTR               value
               54  LOAD_FAST                'self'
               56  STORE_ATTR               begin
               58  LOAD_FAST                'self'
               60  STORE_ATTR               end
               62  LOAD_FAST                'self'
               64  STORE_ATTR               line

Parse error at or near `<118>' instruction at offset 26

    def raise_error--- This code section failed: ---

 L. 329         0  LOAD_FAST                'args'
                2  POP_JUMP_IF_FALSE    56  'to 56'

 L. 330         4  SETUP_FINALLY        18  'to 18'

 L. 331         6  LOAD_FAST                'msg'
                8  LOAD_FAST                'args'
               10  BINARY_MODULO    
               12  STORE_FAST               'msg'
               14  POP_BLOCK        
               16  JUMP_FORWARD         56  'to 56'
             18_0  COME_FROM_FINALLY     4  '4'

 L. 332        18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 333        24  LOAD_STR                 ' '
               26  LOAD_METHOD              join
               28  LOAD_FAST                'msg'
               30  BUILD_LIST_1          1 
               32  LOAD_GLOBAL              list
               34  LOAD_GLOBAL              map
               36  LOAD_GLOBAL              str
               38  LOAD_FAST                'args'
               40  CALL_FUNCTION_2       2  ''
               42  CALL_FUNCTION_1       1  ''
               44  BINARY_ADD       
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               'msg'
               50  POP_EXCEPT       
               52  JUMP_FORWARD         56  'to 56'
               54  <48>             
             56_0  COME_FROM            52  '52'
             56_1  COME_FROM            16  '16'
             56_2  COME_FROM             2  '2'

 L. 334        56  LOAD_GLOBAL              SyntaxError
               58  LOAD_FAST                'msg'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                filename
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                end
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    

 L. 335        72  LOAD_FAST                'self'
               74  LOAD_ATTR                end
               76  LOAD_CONST               1
               78  BINARY_SUBSCR    
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                line

 L. 334        84  BUILD_TUPLE_4         4 
               86  CALL_FUNCTION_2       2  ''
               88  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<48>' instruction at offset 54


class NFAState(object):

    def __init__(self):
        self.arcs = []

    def addarc--- This code section failed: ---

 L. 343         0  LOAD_FAST                'label'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     22  'to 22'
                8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'label'
               12  LOAD_GLOBAL              str
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     22  'to 22'
               18  <74>             
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            16  '16'
             22_1  COME_FROM             6  '6'

 L. 344        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'next'
               26  LOAD_GLOBAL              NFAState
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_TRUE     36  'to 36'
               32  <74>             
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            30  '30'

 L. 345        36  LOAD_FAST                'self'
               38  LOAD_ATTR                arcs
               40  LOAD_METHOD              append
               42  LOAD_FAST                'label'
               44  LOAD_FAST                'next'
               46  BUILD_TUPLE_2         2 
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

Parse error at or near `None' instruction at offset -1


class DFAState(object):

    def __init__--- This code section failed: ---

 L. 350         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'nfaset'
                4  LOAD_GLOBAL              dict
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 351        14  LOAD_GLOBAL              isinstance
               16  LOAD_GLOBAL              next
               18  LOAD_GLOBAL              iter
               20  LOAD_FAST                'nfaset'
               22  CALL_FUNCTION_1       1  ''
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_GLOBAL              NFAState
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_TRUE     36  'to 36'
               32  <74>             
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            30  '30'

 L. 352        36  LOAD_GLOBAL              isinstance
               38  LOAD_FAST                'final'
               40  LOAD_GLOBAL              NFAState
               42  CALL_FUNCTION_2       2  ''
               44  POP_JUMP_IF_TRUE     50  'to 50'
               46  <74>             
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            44  '44'

 L. 353        50  LOAD_FAST                'nfaset'
               52  LOAD_FAST                'self'
               54  STORE_ATTR               nfaset

 L. 354        56  LOAD_FAST                'final'
               58  LOAD_FAST                'nfaset'
               60  <118>                 0  ''
               62  LOAD_FAST                'self'
               64  STORE_ATTR               isfinal

 L. 355        66  BUILD_MAP_0           0 
               68  LOAD_FAST                'self'
               70  STORE_ATTR               arcs

Parse error at or near `None' instruction at offset -1

    def addarc--- This code section failed: ---

 L. 358         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'label'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 359        14  LOAD_FAST                'label'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                arcs
               20  <118>                 1  ''
               22  POP_JUMP_IF_TRUE     28  'to 28'
               24  <74>             
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'

 L. 360        28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'next'
               32  LOAD_GLOBAL              DFAState
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_TRUE     42  'to 42'
               38  <74>             
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            36  '36'

 L. 361        42  LOAD_FAST                'next'
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                arcs
               48  LOAD_FAST                'label'
               50  STORE_SUBSCR     

Parse error at or near `None' instruction at offset -1

    def unifystate--- This code section failed: ---

 L. 364         0  LOAD_FAST                'self'
                2  LOAD_ATTR                arcs
                4  LOAD_METHOD              items
                6  CALL_METHOD_0         0  ''
                8  GET_ITER         
             10_0  COME_FROM            36  '36'
             10_1  COME_FROM            24  '24'
               10  FOR_ITER             38  'to 38'
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'label'
               16  STORE_FAST               'next'

 L. 365        18  LOAD_FAST                'next'
               20  LOAD_FAST                'old'
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE_BACK    10  'to 10'

 L. 366        26  LOAD_FAST                'new'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                arcs
               32  LOAD_FAST                'label'
               34  STORE_SUBSCR     
               36  JUMP_BACK            10  'to 10'
             38_0  COME_FROM            10  '10'

Parse error at or near `<117>' instruction at offset 22

    def __eq__--- This code section failed: ---

 L. 370         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'other'
                4  LOAD_GLOBAL              DFAState
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 371        14  LOAD_FAST                'self'
               16  LOAD_ATTR                isfinal
               18  LOAD_FAST                'other'
               20  LOAD_ATTR                isfinal
               22  COMPARE_OP               !=
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 372        26  LOAD_CONST               False
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L. 375        30  LOAD_GLOBAL              len
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                arcs
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_GLOBAL              len
               40  LOAD_FAST                'other'
               42  LOAD_ATTR                arcs
               44  CALL_FUNCTION_1       1  ''
               46  COMPARE_OP               !=
               48  POP_JUMP_IF_FALSE    54  'to 54'

 L. 376        50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'

 L. 377        54  LOAD_FAST                'self'
               56  LOAD_ATTR                arcs
               58  LOAD_METHOD              items
               60  CALL_METHOD_0         0  ''
               62  GET_ITER         
             64_0  COME_FROM            94  '94'
             64_1  COME_FROM            86  '86'
               64  FOR_ITER             96  'to 96'
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               'label'
               70  STORE_FAST               'next'

 L. 378        72  LOAD_FAST                'next'
               74  LOAD_FAST                'other'
               76  LOAD_ATTR                arcs
               78  LOAD_METHOD              get
               80  LOAD_FAST                'label'
               82  CALL_METHOD_1         1  ''
               84  <117>                 1  ''
               86  POP_JUMP_IF_FALSE_BACK    64  'to 64'

 L. 379        88  POP_TOP          
               90  LOAD_CONST               False
               92  RETURN_VALUE     
               94  JUMP_BACK            64  'to 64'
             96_0  COME_FROM            64  '64'

 L. 380        96  LOAD_CONST               True
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    __hash__ = None


def generate_grammar(filename='Grammar.txt'):
    p = ParserGenerator(filename)
    return p.make_grammar