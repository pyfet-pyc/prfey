# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: lib2to3\patcomp.py
"""Pattern compiler.

The grammar is taken from PatternGrammar.txt.

The compiler compiles a pattern to a pytree.*Pattern instance.
"""
__author__ = 'Guido van Rossum <guido@python.org>'
import io
from .pgen2 import driver, literals, token, tokenize, parse, grammar
from . import pytree
from . import pygram

class PatternSyntaxError(Exception):
    pass


def tokenize_wrapper--- This code section failed: ---

 L.  30         0  LOAD_GLOBAL              token
                2  LOAD_ATTR                NEWLINE
                4  LOAD_GLOBAL              token
                6  LOAD_ATTR                INDENT
                8  LOAD_GLOBAL              token
               10  LOAD_ATTR                DEDENT
               12  BUILD_SET_3           3 
               14  STORE_FAST               'skip'

 L.  31        16  LOAD_GLOBAL              tokenize
               18  LOAD_METHOD              generate_tokens
               20  LOAD_GLOBAL              io
               22  LOAD_METHOD              StringIO
               24  LOAD_FAST                'input'
               26  CALL_METHOD_1         1  ''
               28  LOAD_ATTR                readline
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'tokens'

 L.  32        34  LOAD_FAST                'tokens'
               36  GET_ITER         
             38_0  COME_FROM            70  '70'
             38_1  COME_FROM            62  '62'
               38  FOR_ITER             72  'to 72'
               40  STORE_FAST               'quintuple'

 L.  33        42  LOAD_FAST                'quintuple'
               44  UNPACK_SEQUENCE_5     5 
               46  STORE_FAST               'type'
               48  STORE_FAST               'value'
               50  STORE_FAST               'start'
               52  STORE_FAST               'end'
               54  STORE_FAST               'line_text'

 L.  34        56  LOAD_FAST                'type'
               58  LOAD_FAST                'skip'
               60  <118>                 1  ''
               62  POP_JUMP_IF_FALSE_BACK    38  'to 38'

 L.  35        64  LOAD_FAST                'quintuple'
               66  YIELD_VALUE      
               68  POP_TOP          
               70  JUMP_BACK            38  'to 38'
             72_0  COME_FROM            38  '38'

Parse error at or near `<118>' instruction at offset 60


class PatternCompiler(object):

    def __init__--- This code section failed: ---

 L.  45         0  LOAD_FAST                'grammar_file'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    26  'to 26'

 L.  46         8  LOAD_GLOBAL              pygram
               10  LOAD_ATTR                pattern_grammar
               12  LOAD_FAST                'self'
               14  STORE_ATTR               grammar

 L.  47        16  LOAD_GLOBAL              pygram
               18  LOAD_ATTR                pattern_symbols
               20  LOAD_FAST                'self'
               22  STORE_ATTR               syms
               24  JUMP_FORWARD         52  'to 52'
             26_0  COME_FROM             6  '6'

 L.  49        26  LOAD_GLOBAL              driver
               28  LOAD_METHOD              load_grammar
               30  LOAD_FAST                'grammar_file'
               32  CALL_METHOD_1         1  ''
               34  LOAD_FAST                'self'
               36  STORE_ATTR               grammar

 L.  50        38  LOAD_GLOBAL              pygram
               40  LOAD_METHOD              Symbols
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                grammar
               46  CALL_METHOD_1         1  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               syms
             52_0  COME_FROM            24  '24'

 L.  51        52  LOAD_GLOBAL              pygram
               54  LOAD_ATTR                python_grammar
               56  LOAD_FAST                'self'
               58  STORE_ATTR               pygrammar

 L.  52        60  LOAD_GLOBAL              pygram
               62  LOAD_ATTR                python_symbols
               64  LOAD_FAST                'self'
               66  STORE_ATTR               pysyms

 L.  53        68  LOAD_GLOBAL              driver
               70  LOAD_ATTR                Driver
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                grammar
               76  LOAD_GLOBAL              pattern_convert
               78  LOAD_CONST               ('convert',)
               80  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               driver

Parse error at or near `None' instruction at offset -1

    def compile_pattern--- This code section failed: ---

 L.  57         0  LOAD_GLOBAL              tokenize_wrapper
                2  LOAD_FAST                'input'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'tokens'

 L.  58         8  SETUP_FINALLY        30  'to 30'

 L.  59        10  LOAD_FAST                'self'
               12  LOAD_ATTR                driver
               14  LOAD_ATTR                parse_tokens
               16  LOAD_FAST                'tokens'
               18  LOAD_FAST                'debug'
               20  LOAD_CONST               ('debug',)
               22  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               24  STORE_FAST               'root'
               26  POP_BLOCK        
               28  JUMP_FORWARD         82  'to 82'
             30_0  COME_FROM_FINALLY     8  '8'

 L.  60        30  DUP_TOP          
               32  LOAD_GLOBAL              parse
               34  LOAD_ATTR                ParseError
               36  <121>                80  ''
               38  POP_TOP          
               40  STORE_FAST               'e'
               42  POP_TOP          
               44  SETUP_FINALLY        72  'to 72'

 L.  61        46  LOAD_GLOBAL              PatternSyntaxError
               48  LOAD_GLOBAL              str
               50  LOAD_FAST                'e'
               52  CALL_FUNCTION_1       1  ''
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_CONST               None
               58  RAISE_VARARGS_2       2  'exception instance with __cause__'
               60  POP_BLOCK        
               62  POP_EXCEPT       
               64  LOAD_CONST               None
               66  STORE_FAST               'e'
               68  DELETE_FAST              'e'
               70  JUMP_FORWARD         82  'to 82'
             72_0  COME_FROM_FINALLY    44  '44'
               72  LOAD_CONST               None
               74  STORE_FAST               'e'
               76  DELETE_FAST              'e'
               78  <48>             
               80  <48>             
             82_0  COME_FROM            70  '70'
             82_1  COME_FROM            28  '28'

 L.  62        82  LOAD_FAST                'with_tree'
               84  POP_JUMP_IF_FALSE   100  'to 100'

 L.  63        86  LOAD_FAST                'self'
               88  LOAD_METHOD              compile_node
               90  LOAD_FAST                'root'
               92  CALL_METHOD_1         1  ''
               94  LOAD_FAST                'root'
               96  BUILD_TUPLE_2         2 
               98  RETURN_VALUE     
            100_0  COME_FROM            84  '84'

 L.  65       100  LOAD_FAST                'self'
              102  LOAD_METHOD              compile_node
              104  LOAD_FAST                'root'
              106  CALL_METHOD_1         1  ''
              108  RETURN_VALUE     

Parse error at or near `<121>' instruction at offset 36

    def compile_node--- This code section failed: ---

 L.  74         0  LOAD_FAST                'node'
                2  LOAD_ATTR                type
                4  LOAD_DEREF               'self'
                6  LOAD_ATTR                syms
                8  LOAD_ATTR                Matcher
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE    24  'to 24'

 L.  75        14  LOAD_FAST                'node'
               16  LOAD_ATTR                children
               18  LOAD_CONST               0
               20  BINARY_SUBSCR    
               22  STORE_FAST               'node'
             24_0  COME_FROM            12  '12'

 L.  77        24  LOAD_FAST                'node'
               26  LOAD_ATTR                type
               28  LOAD_DEREF               'self'
               30  LOAD_ATTR                syms
               32  LOAD_ATTR                Alternatives
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE   122  'to 122'

 L.  79        38  LOAD_CLOSURE             'self'
               40  BUILD_TUPLE_1         1 
               42  LOAD_LISTCOMP            '<code_object <listcomp>>'
               44  LOAD_STR                 'PatternCompiler.compile_node.<locals>.<listcomp>'
               46  MAKE_FUNCTION_8          'closure'
               48  LOAD_FAST                'node'
               50  LOAD_ATTR                children
               52  LOAD_CONST               None
               54  LOAD_CONST               None
               56  LOAD_CONST               2
               58  BUILD_SLICE_3         3 
               60  BINARY_SUBSCR    
               62  GET_ITER         
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'alts'

 L.  80        68  LOAD_GLOBAL              len
               70  LOAD_FAST                'alts'
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_CONST               1
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE    88  'to 88'

 L.  81        80  LOAD_FAST                'alts'
               82  LOAD_CONST               0
               84  BINARY_SUBSCR    
               86  RETURN_VALUE     
             88_0  COME_FROM            78  '78'

 L.  82        88  LOAD_GLOBAL              pytree
               90  LOAD_ATTR                WildcardPattern
               92  LOAD_LISTCOMP            '<code_object <listcomp>>'
               94  LOAD_STR                 'PatternCompiler.compile_node.<locals>.<listcomp>'
               96  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               98  LOAD_FAST                'alts'
              100  GET_ITER         
              102  CALL_FUNCTION_1       1  ''
              104  LOAD_CONST               1
              106  LOAD_CONST               1
              108  LOAD_CONST               ('min', 'max')
              110  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              112  STORE_FAST               'p'

 L.  83       114  LOAD_FAST                'p'
              116  LOAD_METHOD              optimize
              118  CALL_METHOD_0         0  ''
              120  RETURN_VALUE     
            122_0  COME_FROM            36  '36'

 L.  85       122  LOAD_FAST                'node'
              124  LOAD_ATTR                type
              126  LOAD_DEREF               'self'
              128  LOAD_ATTR                syms
              130  LOAD_ATTR                Alternative
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE   202  'to 202'

 L.  86       136  LOAD_CLOSURE             'self'
              138  BUILD_TUPLE_1         1 
              140  LOAD_LISTCOMP            '<code_object <listcomp>>'
              142  LOAD_STR                 'PatternCompiler.compile_node.<locals>.<listcomp>'
              144  MAKE_FUNCTION_8          'closure'
              146  LOAD_FAST                'node'
              148  LOAD_ATTR                children
              150  GET_ITER         
              152  CALL_FUNCTION_1       1  ''
              154  STORE_FAST               'units'

 L.  87       156  LOAD_GLOBAL              len
              158  LOAD_FAST                'units'
              160  CALL_FUNCTION_1       1  ''
              162  LOAD_CONST               1
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   176  'to 176'

 L.  88       168  LOAD_FAST                'units'
              170  LOAD_CONST               0
              172  BINARY_SUBSCR    
              174  RETURN_VALUE     
            176_0  COME_FROM           166  '166'

 L.  89       176  LOAD_GLOBAL              pytree
              178  LOAD_ATTR                WildcardPattern
              180  LOAD_FAST                'units'
              182  BUILD_LIST_1          1 
              184  LOAD_CONST               1
              186  LOAD_CONST               1
              188  LOAD_CONST               ('min', 'max')
              190  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              192  STORE_FAST               'p'

 L.  90       194  LOAD_FAST                'p'
              196  LOAD_METHOD              optimize
              198  CALL_METHOD_0         0  ''
              200  RETURN_VALUE     
            202_0  COME_FROM           134  '134'

 L.  92       202  LOAD_FAST                'node'
              204  LOAD_ATTR                type
              206  LOAD_DEREF               'self'
              208  LOAD_ATTR                syms
              210  LOAD_ATTR                NegatedUnit
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE   254  'to 254'

 L.  93       216  LOAD_DEREF               'self'
              218  LOAD_METHOD              compile_basic
              220  LOAD_FAST                'node'
              222  LOAD_ATTR                children
              224  LOAD_CONST               1
              226  LOAD_CONST               None
              228  BUILD_SLICE_2         2 
              230  BINARY_SUBSCR    
              232  CALL_METHOD_1         1  ''
              234  STORE_FAST               'pattern'

 L.  94       236  LOAD_GLOBAL              pytree
              238  LOAD_METHOD              NegatedPattern
              240  LOAD_FAST                'pattern'
              242  CALL_METHOD_1         1  ''
              244  STORE_FAST               'p'

 L.  95       246  LOAD_FAST                'p'
              248  LOAD_METHOD              optimize
              250  CALL_METHOD_0         0  ''
              252  RETURN_VALUE     
            254_0  COME_FROM           214  '214'

 L.  97       254  LOAD_FAST                'node'
              256  LOAD_ATTR                type
              258  LOAD_DEREF               'self'
              260  LOAD_ATTR                syms
              262  LOAD_ATTR                Unit
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_TRUE    274  'to 274'
              270  <74>             
              272  RAISE_VARARGS_1       1  'exception instance'
            274_0  COME_FROM           266  '266'

 L.  99       274  LOAD_CONST               None
              276  STORE_FAST               'name'

 L. 100       278  LOAD_FAST                'node'
              280  LOAD_ATTR                children
              282  STORE_FAST               'nodes'

 L. 101       284  LOAD_GLOBAL              len
              286  LOAD_FAST                'nodes'
              288  CALL_FUNCTION_1       1  ''
              290  LOAD_CONST               3
              292  COMPARE_OP               >=
          294_296  POP_JUMP_IF_FALSE   338  'to 338'
              298  LOAD_FAST                'nodes'
              300  LOAD_CONST               1
              302  BINARY_SUBSCR    
              304  LOAD_ATTR                type
              306  LOAD_GLOBAL              token
              308  LOAD_ATTR                EQUAL
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   338  'to 338'

 L. 102       316  LOAD_FAST                'nodes'
              318  LOAD_CONST               0
              320  BINARY_SUBSCR    
              322  LOAD_ATTR                value
              324  STORE_FAST               'name'

 L. 103       326  LOAD_FAST                'nodes'
              328  LOAD_CONST               2
              330  LOAD_CONST               None
              332  BUILD_SLICE_2         2 
              334  BINARY_SUBSCR    
              336  STORE_FAST               'nodes'
            338_0  COME_FROM           312  '312'
            338_1  COME_FROM           294  '294'

 L. 104       338  LOAD_CONST               None
              340  STORE_FAST               'repeat'

 L. 105       342  LOAD_GLOBAL              len
              344  LOAD_FAST                'nodes'
              346  CALL_FUNCTION_1       1  ''
              348  LOAD_CONST               2
              350  COMPARE_OP               >=
          352_354  POP_JUMP_IF_FALSE   396  'to 396'
              356  LOAD_FAST                'nodes'
              358  LOAD_CONST               -1
              360  BINARY_SUBSCR    
              362  LOAD_ATTR                type
              364  LOAD_DEREF               'self'
              366  LOAD_ATTR                syms
              368  LOAD_ATTR                Repeater
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   396  'to 396'

 L. 106       376  LOAD_FAST                'nodes'
              378  LOAD_CONST               -1
              380  BINARY_SUBSCR    
              382  STORE_FAST               'repeat'

 L. 107       384  LOAD_FAST                'nodes'
              386  LOAD_CONST               None
              388  LOAD_CONST               -1
              390  BUILD_SLICE_2         2 
              392  BINARY_SUBSCR    
              394  STORE_FAST               'nodes'
            396_0  COME_FROM           372  '372'
            396_1  COME_FROM           352  '352'

 L. 110       396  LOAD_DEREF               'self'
              398  LOAD_METHOD              compile_basic
              400  LOAD_FAST                'nodes'
              402  LOAD_FAST                'repeat'
              404  CALL_METHOD_2         2  ''
              406  STORE_FAST               'pattern'

 L. 112       408  LOAD_FAST                'repeat'
              410  LOAD_CONST               None
              412  <117>                 1  ''
          414_416  POP_JUMP_IF_FALSE   664  'to 664'

 L. 113       418  LOAD_FAST                'repeat'
              420  LOAD_ATTR                type
              422  LOAD_DEREF               'self'
              424  LOAD_ATTR                syms
              426  LOAD_ATTR                Repeater
              428  COMPARE_OP               ==
          430_432  POP_JUMP_IF_TRUE    438  'to 438'
              434  <74>             
              436  RAISE_VARARGS_1       1  'exception instance'
            438_0  COME_FROM           430  '430'

 L. 114       438  LOAD_FAST                'repeat'
              440  LOAD_ATTR                children
              442  STORE_FAST               'children'

 L. 115       444  LOAD_FAST                'children'
              446  LOAD_CONST               0
              448  BINARY_SUBSCR    
              450  STORE_FAST               'child'

 L. 116       452  LOAD_FAST                'child'
              454  LOAD_ATTR                type
              456  LOAD_GLOBAL              token
              458  LOAD_ATTR                STAR
              460  COMPARE_OP               ==
          462_464  POP_JUMP_IF_FALSE   478  'to 478'

 L. 117       466  LOAD_CONST               0
              468  STORE_FAST               'min'

 L. 118       470  LOAD_GLOBAL              pytree
              472  LOAD_ATTR                HUGE
              474  STORE_FAST               'max'
              476  JUMP_FORWARD        616  'to 616'
            478_0  COME_FROM           462  '462'

 L. 119       478  LOAD_FAST                'child'
              480  LOAD_ATTR                type
              482  LOAD_GLOBAL              token
              484  LOAD_ATTR                PLUS
              486  COMPARE_OP               ==
          488_490  POP_JUMP_IF_FALSE   504  'to 504'

 L. 120       492  LOAD_CONST               1
              494  STORE_FAST               'min'

 L. 121       496  LOAD_GLOBAL              pytree
              498  LOAD_ATTR                HUGE
              500  STORE_FAST               'max'
              502  JUMP_FORWARD        616  'to 616'
            504_0  COME_FROM           488  '488'

 L. 122       504  LOAD_FAST                'child'
              506  LOAD_ATTR                type
              508  LOAD_GLOBAL              token
              510  LOAD_ATTR                LBRACE
              512  COMPARE_OP               ==
          514_516  POP_JUMP_IF_FALSE   606  'to 606'

 L. 123       518  LOAD_FAST                'children'
              520  LOAD_CONST               -1
              522  BINARY_SUBSCR    
              524  LOAD_ATTR                type
              526  LOAD_GLOBAL              token
              528  LOAD_ATTR                RBRACE
              530  COMPARE_OP               ==
          532_534  POP_JUMP_IF_TRUE    540  'to 540'
              536  <74>             
              538  RAISE_VARARGS_1       1  'exception instance'
            540_0  COME_FROM           532  '532'

 L. 124       540  LOAD_GLOBAL              len
              542  LOAD_FAST                'children'
              544  CALL_FUNCTION_1       1  ''
              546  LOAD_CONST               (3, 5)
              548  <118>                 0  ''
          550_552  POP_JUMP_IF_TRUE    558  'to 558'
              554  <74>             
              556  RAISE_VARARGS_1       1  'exception instance'
            558_0  COME_FROM           550  '550'

 L. 125       558  LOAD_DEREF               'self'
              560  LOAD_METHOD              get_int
              562  LOAD_FAST                'children'
              564  LOAD_CONST               1
              566  BINARY_SUBSCR    
              568  CALL_METHOD_1         1  ''
              570  DUP_TOP          
              572  STORE_FAST               'min'
              574  STORE_FAST               'max'

 L. 126       576  LOAD_GLOBAL              len
              578  LOAD_FAST                'children'
              580  CALL_FUNCTION_1       1  ''
              582  LOAD_CONST               5
              584  COMPARE_OP               ==
          586_588  POP_JUMP_IF_FALSE   616  'to 616'

 L. 127       590  LOAD_DEREF               'self'
              592  LOAD_METHOD              get_int
              594  LOAD_FAST                'children'
              596  LOAD_CONST               3
              598  BINARY_SUBSCR    
              600  CALL_METHOD_1         1  ''
              602  STORE_FAST               'max'
              604  JUMP_FORWARD        616  'to 616'
            606_0  COME_FROM           514  '514'

 L. 129       606  LOAD_CONST               False
          608_610  POP_JUMP_IF_TRUE    616  'to 616'
              612  <74>             
              614  RAISE_VARARGS_1       1  'exception instance'
            616_0  COME_FROM           608  '608'
            616_1  COME_FROM           604  '604'
            616_2  COME_FROM           586  '586'
            616_3  COME_FROM           502  '502'
            616_4  COME_FROM           476  '476'

 L. 130       616  LOAD_FAST                'min'
              618  LOAD_CONST               1
              620  COMPARE_OP               !=
          622_624  POP_JUMP_IF_TRUE    636  'to 636'
              626  LOAD_FAST                'max'
              628  LOAD_CONST               1
              630  COMPARE_OP               !=
          632_634  POP_JUMP_IF_FALSE   664  'to 664'
            636_0  COME_FROM           622  '622'

 L. 131       636  LOAD_FAST                'pattern'
              638  LOAD_METHOD              optimize
              640  CALL_METHOD_0         0  ''
              642  STORE_FAST               'pattern'

 L. 132       644  LOAD_GLOBAL              pytree
              646  LOAD_ATTR                WildcardPattern
              648  LOAD_FAST                'pattern'
              650  BUILD_LIST_1          1 
              652  BUILD_LIST_1          1 
              654  LOAD_FAST                'min'
              656  LOAD_FAST                'max'
              658  LOAD_CONST               ('min', 'max')
              660  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              662  STORE_FAST               'pattern'
            664_0  COME_FROM           632  '632'
            664_1  COME_FROM           414  '414'

 L. 134       664  LOAD_FAST                'name'
              666  LOAD_CONST               None
              668  <117>                 1  ''
          670_672  POP_JUMP_IF_FALSE   680  'to 680'

 L. 135       674  LOAD_FAST                'name'
              676  LOAD_FAST                'pattern'
              678  STORE_ATTR               name
            680_0  COME_FROM           670  '670'

 L. 136       680  LOAD_FAST                'pattern'
              682  LOAD_METHOD              optimize
              684  CALL_METHOD_0         0  ''
              686  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 270

    def compile_basic--- This code section failed: ---

 L. 140         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'nodes'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               1
                8  COMPARE_OP               >=
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L. 141        16  LOAD_FAST                'nodes'
               18  LOAD_CONST               0
               20  BINARY_SUBSCR    
               22  STORE_FAST               'node'

 L. 142        24  LOAD_FAST                'node'
               26  LOAD_ATTR                type
               28  LOAD_GLOBAL              token
               30  LOAD_ATTR                STRING
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    68  'to 68'

 L. 143        36  LOAD_GLOBAL              str
               38  LOAD_GLOBAL              literals
               40  LOAD_METHOD              evalString
               42  LOAD_FAST                'node'
               44  LOAD_ATTR                value
               46  CALL_METHOD_1         1  ''
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'value'

 L. 144        52  LOAD_GLOBAL              pytree
               54  LOAD_METHOD              LeafPattern
               56  LOAD_GLOBAL              _type_of_literal
               58  LOAD_FAST                'value'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_FAST                'value'
               64  CALL_METHOD_2         2  ''
               66  RETURN_VALUE     
             68_0  COME_FROM            34  '34'

 L. 145        68  LOAD_FAST                'node'
               70  LOAD_ATTR                type
               72  LOAD_GLOBAL              token
               74  LOAD_ATTR                NAME
               76  COMPARE_OP               ==
            78_80  POP_JUMP_IF_FALSE   262  'to 262'

 L. 146        82  LOAD_FAST                'node'
               84  LOAD_ATTR                value
               86  STORE_FAST               'value'

 L. 147        88  LOAD_FAST                'value'
               90  LOAD_METHOD              isupper
               92  CALL_METHOD_0         0  ''
               94  POP_JUMP_IF_FALSE   150  'to 150'

 L. 148        96  LOAD_FAST                'value'
               98  LOAD_GLOBAL              TOKEN_MAP
              100  <118>                 1  ''
              102  POP_JUMP_IF_FALSE   116  'to 116'

 L. 149       104  LOAD_GLOBAL              PatternSyntaxError
              106  LOAD_STR                 'Invalid token: %r'
              108  LOAD_FAST                'value'
              110  BINARY_MODULO    
              112  CALL_FUNCTION_1       1  ''
              114  RAISE_VARARGS_1       1  'exception instance'
            116_0  COME_FROM           102  '102'

 L. 150       116  LOAD_FAST                'nodes'
              118  LOAD_CONST               1
              120  LOAD_CONST               None
              122  BUILD_SLICE_2         2 
              124  BINARY_SUBSCR    
              126  POP_JUMP_IF_FALSE   136  'to 136'

 L. 151       128  LOAD_GLOBAL              PatternSyntaxError
              130  LOAD_STR                 "Can't have details for token"
              132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           126  '126'

 L. 152       136  LOAD_GLOBAL              pytree
              138  LOAD_METHOD              LeafPattern
              140  LOAD_GLOBAL              TOKEN_MAP
              142  LOAD_FAST                'value'
              144  BINARY_SUBSCR    
              146  CALL_METHOD_1         1  ''
              148  RETURN_VALUE     
            150_0  COME_FROM            94  '94'

 L. 154       150  LOAD_FAST                'value'
              152  LOAD_STR                 'any'
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   164  'to 164'

 L. 155       158  LOAD_CONST               None
              160  STORE_FAST               'type'
              162  JUMP_FORWARD        208  'to 208'
            164_0  COME_FROM           156  '156'

 L. 156       164  LOAD_FAST                'value'
              166  LOAD_METHOD              startswith
              168  LOAD_STR                 '_'
              170  CALL_METHOD_1         1  ''
              172  POP_JUMP_IF_TRUE    208  'to 208'

 L. 157       174  LOAD_GLOBAL              getattr
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                pysyms
              180  LOAD_FAST                'value'
              182  LOAD_CONST               None
              184  CALL_FUNCTION_3       3  ''
              186  STORE_FAST               'type'

 L. 158       188  LOAD_FAST                'type'
              190  LOAD_CONST               None
              192  <117>                 0  ''
              194  POP_JUMP_IF_FALSE   208  'to 208'

 L. 159       196  LOAD_GLOBAL              PatternSyntaxError
              198  LOAD_STR                 'Invalid symbol: %r'
              200  LOAD_FAST                'value'
              202  BINARY_MODULO    
              204  CALL_FUNCTION_1       1  ''
              206  RAISE_VARARGS_1       1  'exception instance'
            208_0  COME_FROM           194  '194'
            208_1  COME_FROM           172  '172'
            208_2  COME_FROM           162  '162'

 L. 160       208  LOAD_FAST                'nodes'
              210  LOAD_CONST               1
              212  LOAD_CONST               None
              214  BUILD_SLICE_2         2 
              216  BINARY_SUBSCR    
              218  POP_JUMP_IF_FALSE   244  'to 244'

 L. 161       220  LOAD_FAST                'self'
              222  LOAD_METHOD              compile_node
              224  LOAD_FAST                'nodes'
              226  LOAD_CONST               1
              228  BINARY_SUBSCR    
              230  LOAD_ATTR                children
              232  LOAD_CONST               1
              234  BINARY_SUBSCR    
              236  CALL_METHOD_1         1  ''
              238  BUILD_LIST_1          1 
              240  STORE_FAST               'content'
              242  JUMP_FORWARD        248  'to 248'
            244_0  COME_FROM           218  '218'

 L. 163       244  LOAD_CONST               None
              246  STORE_FAST               'content'
            248_0  COME_FROM           242  '242'

 L. 164       248  LOAD_GLOBAL              pytree
              250  LOAD_METHOD              NodePattern
              252  LOAD_FAST                'type'
              254  LOAD_FAST                'content'
              256  CALL_METHOD_2         2  ''
              258  RETURN_VALUE     
              260  JUMP_FORWARD        348  'to 348'
            262_0  COME_FROM            78  '78'

 L. 165       262  LOAD_FAST                'node'
              264  LOAD_ATTR                value
              266  LOAD_STR                 '('
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   288  'to 288'

 L. 166       274  LOAD_FAST                'self'
              276  LOAD_METHOD              compile_node
              278  LOAD_FAST                'nodes'
              280  LOAD_CONST               1
              282  BINARY_SUBSCR    
              284  CALL_METHOD_1         1  ''
              286  RETURN_VALUE     
            288_0  COME_FROM           270  '270'

 L. 167       288  LOAD_FAST                'node'
              290  LOAD_ATTR                value
              292  LOAD_STR                 '['
              294  COMPARE_OP               ==
          296_298  POP_JUMP_IF_FALSE   348  'to 348'

 L. 168       300  LOAD_FAST                'repeat'
              302  LOAD_CONST               None
              304  <117>                 0  ''
          306_308  POP_JUMP_IF_TRUE    314  'to 314'
              310  <74>             
              312  RAISE_VARARGS_1       1  'exception instance'
            314_0  COME_FROM           306  '306'

 L. 169       314  LOAD_FAST                'self'
              316  LOAD_METHOD              compile_node
              318  LOAD_FAST                'nodes'
              320  LOAD_CONST               1
              322  BINARY_SUBSCR    
              324  CALL_METHOD_1         1  ''
              326  STORE_FAST               'subpattern'

 L. 170       328  LOAD_GLOBAL              pytree
              330  LOAD_ATTR                WildcardPattern
              332  LOAD_FAST                'subpattern'
              334  BUILD_LIST_1          1 
              336  BUILD_LIST_1          1 
              338  LOAD_CONST               0
              340  LOAD_CONST               1
              342  LOAD_CONST               ('min', 'max')
              344  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              346  RETURN_VALUE     
            348_0  COME_FROM           296  '296'
            348_1  COME_FROM           260  '260'

 L. 171       348  LOAD_CONST               False
          350_352  POP_JUMP_IF_TRUE    362  'to 362'
              354  <74>             
              356  LOAD_FAST                'node'
              358  CALL_FUNCTION_1       1  ''
              360  RAISE_VARARGS_1       1  'exception instance'
            362_0  COME_FROM           350  '350'

Parse error at or near `None' instruction at offset -1

    def get_int--- This code section failed: ---

 L. 174         0  LOAD_FAST                'node'
                2  LOAD_ATTR                type
                4  LOAD_GLOBAL              token
                6  LOAD_ATTR                NUMBER
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L. 175        16  LOAD_GLOBAL              int
               18  LOAD_FAST                'node'
               20  LOAD_ATTR                value
               22  CALL_FUNCTION_1       1  ''
               24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


TOKEN_MAP = {'NAME':token.NAME, 
 'STRING':token.STRING, 
 'NUMBER':token.NUMBER, 
 'TOKEN':None}

def _type_of_literal--- This code section failed: ---

 L. 186         0  LOAD_FAST                'value'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  LOAD_METHOD              isalpha
                8  CALL_METHOD_0         0  ''
               10  POP_JUMP_IF_FALSE    18  'to 18'

 L. 187        12  LOAD_GLOBAL              token
               14  LOAD_ATTR                NAME
               16  RETURN_VALUE     
             18_0  COME_FROM            10  '10'

 L. 188        18  LOAD_FAST                'value'
               20  LOAD_GLOBAL              grammar
               22  LOAD_ATTR                opmap
               24  <118>                 0  ''
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L. 189        28  LOAD_GLOBAL              grammar
               30  LOAD_ATTR                opmap
               32  LOAD_FAST                'value'
               34  BINARY_SUBSCR    
               36  RETURN_VALUE     
             38_0  COME_FROM            26  '26'

 L. 191        38  LOAD_CONST               None
               40  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 24


def pattern_convert--- This code section failed: ---

 L. 196         0  LOAD_FAST                'raw_node_info'
                2  UNPACK_SEQUENCE_4     4 
                4  STORE_FAST               'type'
                6  STORE_FAST               'value'
                8  STORE_FAST               'context'
               10  STORE_FAST               'children'

 L. 197        12  LOAD_FAST                'children'
               14  POP_JUMP_IF_TRUE     26  'to 26'
               16  LOAD_FAST                'type'
               18  LOAD_FAST                'grammar'
               20  LOAD_ATTR                number2symbol
               22  <118>                 0  ''
               24  POP_JUMP_IF_FALSE    42  'to 42'
             26_0  COME_FROM            14  '14'

 L. 198        26  LOAD_GLOBAL              pytree
               28  LOAD_ATTR                Node
               30  LOAD_FAST                'type'
               32  LOAD_FAST                'children'
               34  LOAD_FAST                'context'
               36  LOAD_CONST               ('context',)
               38  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               40  RETURN_VALUE     
             42_0  COME_FROM            24  '24'

 L. 200        42  LOAD_GLOBAL              pytree
               44  LOAD_ATTR                Leaf
               46  LOAD_FAST                'type'
               48  LOAD_FAST                'value'
               50  LOAD_FAST                'context'
               52  LOAD_CONST               ('context',)
               54  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               56  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 22


def compile_pattern(pattern):
    return PatternCompiler().compile_patternpattern