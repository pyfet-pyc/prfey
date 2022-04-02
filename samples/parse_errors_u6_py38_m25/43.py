# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: lib2to3\btm_utils.py
"""Utility functions used by the btm_matcher module"""
from . import pytree
from .pgen2 import grammar, token
from .pygram import pattern_symbols, python_symbols
syms = pattern_symbols
pysyms = python_symbols
tokens = grammar.opmap
token_labels = token
TYPE_ANY = -1
TYPE_ALTERNATIVES = -2
TYPE_GROUP = -3

class MinNode(object):
    __doc__ = 'This class serves as an intermediate representation of the\n    pattern tree during the conversion to sets of leaf-to-root\n    subpatterns'

    def __init__(self, type=None, name=None):
        self.type = type
        self.name = name
        self.children = []
        self.leaf = False
        self.parent = None
        self.alternatives = []
        self.group = []

    def __repr__(self):
        return str(self.type) + ' ' + str(self.name)

    def leaf_to_root--- This code section failed: ---

 L.  37         0  LOAD_FAST                'self'
                2  STORE_FAST               'node'

 L.  38         4  BUILD_LIST_0          0 
                6  STORE_FAST               'subp'

 L.  39         8  LOAD_FAST                'node'
               10  POP_JUMP_IF_FALSE   226  'to 226'

 L.  40        12  LOAD_FAST                'node'
               14  LOAD_ATTR                type
               16  LOAD_GLOBAL              TYPE_ALTERNATIVES
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    94  'to 94'

 L.  41        22  LOAD_FAST                'node'
               24  LOAD_ATTR                alternatives
               26  LOAD_METHOD              append
               28  LOAD_FAST                'subp'
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L.  42        34  LOAD_GLOBAL              len
               36  LOAD_FAST                'node'
               38  LOAD_ATTR                alternatives
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_GLOBAL              len
               44  LOAD_FAST                'node'
               46  LOAD_ATTR                children
               48  CALL_FUNCTION_1       1  ''
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    82  'to 82'

 L.  44        54  LOAD_GLOBAL              tuple
               56  LOAD_FAST                'node'
               58  LOAD_ATTR                alternatives
               60  CALL_FUNCTION_1       1  ''
               62  BUILD_LIST_1          1 
               64  STORE_FAST               'subp'

 L.  45        66  BUILD_LIST_0          0 
               68  LOAD_FAST                'node'
               70  STORE_ATTR               alternatives

 L.  46        72  LOAD_FAST                'node'
               74  LOAD_ATTR                parent
               76  STORE_FAST               'node'

 L.  47        78  JUMP_BACK             8  'to 8'
               80  JUMP_FORWARD         94  'to 94'
             82_0  COME_FROM            52  '52'

 L.  49        82  LOAD_FAST                'node'
               84  LOAD_ATTR                parent
               86  STORE_FAST               'node'

 L.  50        88  LOAD_CONST               None
               90  STORE_FAST               'subp'

 L.  51        92  BREAK_LOOP          226  'to 226'
             94_0  COME_FROM            80  '80'
             94_1  COME_FROM            20  '20'

 L.  53        94  LOAD_FAST                'node'
               96  LOAD_ATTR                type
               98  LOAD_GLOBAL              TYPE_GROUP
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   174  'to 174'

 L.  54       104  LOAD_FAST                'node'
              106  LOAD_ATTR                group
              108  LOAD_METHOD              append
              110  LOAD_FAST                'subp'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

 L.  56       116  LOAD_GLOBAL              len
              118  LOAD_FAST                'node'
              120  LOAD_ATTR                group
              122  CALL_FUNCTION_1       1  ''
              124  LOAD_GLOBAL              len
              126  LOAD_FAST                'node'
              128  LOAD_ATTR                children
              130  CALL_FUNCTION_1       1  ''
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE   162  'to 162'

 L.  57       136  LOAD_GLOBAL              get_characteristic_subpattern
              138  LOAD_FAST                'node'
              140  LOAD_ATTR                group
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'subp'

 L.  58       146  BUILD_LIST_0          0 
              148  LOAD_FAST                'node'
              150  STORE_ATTR               group

 L.  59       152  LOAD_FAST                'node'
              154  LOAD_ATTR                parent
              156  STORE_FAST               'node'

 L.  60       158  JUMP_BACK             8  'to 8'
              160  JUMP_FORWARD        174  'to 174'
            162_0  COME_FROM           134  '134'

 L.  62       162  LOAD_FAST                'node'
              164  LOAD_ATTR                parent
              166  STORE_FAST               'node'

 L.  63       168  LOAD_CONST               None
              170  STORE_FAST               'subp'

 L.  64       172  BREAK_LOOP          226  'to 226'
            174_0  COME_FROM           160  '160'
            174_1  COME_FROM           102  '102'

 L.  66       174  LOAD_FAST                'node'
              176  LOAD_ATTR                type
              178  LOAD_GLOBAL              token_labels
              180  LOAD_ATTR                NAME
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   206  'to 206'
              186  LOAD_FAST                'node'
              188  LOAD_ATTR                name
              190  POP_JUMP_IF_FALSE   206  'to 206'

 L.  68       192  LOAD_FAST                'subp'
              194  LOAD_METHOD              append
              196  LOAD_FAST                'node'
              198  LOAD_ATTR                name
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          
              204  JUMP_FORWARD        218  'to 218'
            206_0  COME_FROM           190  '190'
            206_1  COME_FROM           184  '184'

 L.  70       206  LOAD_FAST                'subp'
              208  LOAD_METHOD              append
              210  LOAD_FAST                'node'
              212  LOAD_ATTR                type
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
            218_0  COME_FROM           204  '204'

 L.  72       218  LOAD_FAST                'node'
              220  LOAD_ATTR                parent
              222  STORE_FAST               'node'
              224  JUMP_BACK             8  'to 8'
            226_0  COME_FROM            10  '10'

 L.  73       226  LOAD_FAST                'subp'
              228  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 160

    def get_linear_subpattern(self):
        """Drives the leaf_to_root method. The reason that
        leaf_to_root must be run multiple times is because we need to
        reject 'group' matches; for example the alternative form
        (a | b c) creates a group [b c] that needs to be matched. Since
        matching multiple linear patterns overcomes the automaton's
        capabilities, leaf_to_root merges each group into a single
        choice based on 'characteristic'ity,

        i.e. (a|b c) -> (a|b) if b more characteristic than c

        Returns: The most 'characteristic'(as defined by
          get_characteristic_subpattern) path for the compiled pattern
          tree.
        """
        for l in self.leaves():
            subp = l.leaf_to_root()
            if subp:
                return subp

    def leaves(self):
        """Generator that returns the leaves of the tree"""
        for child in self.children:
            (yield from child.leaves())
        else:
            if not self.children:
                (yield self)


def reduce_tree--- This code section failed: ---

 L. 111         0  LOAD_CONST               None
                2  STORE_FAST               'new_node'

 L. 113         4  LOAD_FAST                'node'
                6  LOAD_ATTR                type
                8  LOAD_GLOBAL              syms
               10  LOAD_ATTR                Matcher
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 115        16  LOAD_FAST                'node'
               18  LOAD_ATTR                children
               20  LOAD_CONST               0
               22  BINARY_SUBSCR    
               24  STORE_FAST               'node'
             26_0  COME_FROM            14  '14'

 L. 117        26  LOAD_FAST                'node'
               28  LOAD_ATTR                type
               30  LOAD_GLOBAL              syms
               32  LOAD_ATTR                Alternatives
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE   144  'to 144'

 L. 119        38  LOAD_GLOBAL              len
               40  LOAD_FAST                'node'
               42  LOAD_ATTR                children
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_CONST               2
               48  COMPARE_OP               <=
               50  POP_JUMP_IF_FALSE    70  'to 70'

 L. 121        52  LOAD_GLOBAL              reduce_tree
               54  LOAD_FAST                'node'
               56  LOAD_ATTR                children
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'parent'
               64  CALL_FUNCTION_2       2  ''
               66  STORE_FAST               'new_node'
               68  JUMP_FORWARD        914  'to 914'
             70_0  COME_FROM            50  '50'

 L. 124        70  LOAD_GLOBAL              MinNode
               72  LOAD_GLOBAL              TYPE_ALTERNATIVES
               74  LOAD_CONST               ('type',)
               76  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               78  STORE_FAST               'new_node'

 L. 126        80  LOAD_FAST                'node'
               82  LOAD_ATTR                children
               84  GET_ITER         
             86_0  COME_FROM           124  '124'
               86  FOR_ITER            140  'to 140'
               88  STORE_FAST               'child'

 L. 127        90  LOAD_FAST                'node'
               92  LOAD_ATTR                children
               94  LOAD_METHOD              index
               96  LOAD_FAST                'child'
               98  CALL_METHOD_1         1  ''
              100  LOAD_CONST               2
              102  BINARY_MODULO    
              104  POP_JUMP_IF_FALSE   108  'to 108'

 L. 128       106  JUMP_BACK            86  'to 86'
            108_0  COME_FROM           104  '104'

 L. 129       108  LOAD_GLOBAL              reduce_tree
              110  LOAD_FAST                'child'
              112  LOAD_FAST                'new_node'
              114  CALL_FUNCTION_2       2  ''
              116  STORE_FAST               'reduced'

 L. 130       118  LOAD_FAST                'reduced'
              120  LOAD_CONST               None
              122  COMPARE_OP               is-not
              124  POP_JUMP_IF_FALSE    86  'to 86'

 L. 131       126  LOAD_FAST                'new_node'
              128  LOAD_ATTR                children
              130  LOAD_METHOD              append
              132  LOAD_FAST                'reduced'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
              138  JUMP_BACK            86  'to 86'
          140_142  JUMP_FORWARD        914  'to 914'
            144_0  COME_FROM            36  '36'

 L. 132       144  LOAD_FAST                'node'
              146  LOAD_ATTR                type
              148  LOAD_GLOBAL              syms
              150  LOAD_ATTR                Alternative
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   250  'to 250'

 L. 133       156  LOAD_GLOBAL              len
              158  LOAD_FAST                'node'
              160  LOAD_ATTR                children
              162  CALL_FUNCTION_1       1  ''
              164  LOAD_CONST               1
              166  COMPARE_OP               >
              168  POP_JUMP_IF_FALSE   230  'to 230'

 L. 135       170  LOAD_GLOBAL              MinNode
              172  LOAD_GLOBAL              TYPE_GROUP
              174  LOAD_CONST               ('type',)
              176  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              178  STORE_FAST               'new_node'

 L. 136       180  LOAD_FAST                'node'
              182  LOAD_ATTR                children
              184  GET_ITER         
            186_0  COME_FROM           202  '202'
              186  FOR_ITER            218  'to 218'
              188  STORE_FAST               'child'

 L. 137       190  LOAD_GLOBAL              reduce_tree
              192  LOAD_FAST                'child'
              194  LOAD_FAST                'new_node'
              196  CALL_FUNCTION_2       2  ''
              198  STORE_FAST               'reduced'

 L. 138       200  LOAD_FAST                'reduced'
              202  POP_JUMP_IF_FALSE   186  'to 186'

 L. 139       204  LOAD_FAST                'new_node'
              206  LOAD_ATTR                children
              208  LOAD_METHOD              append
              210  LOAD_FAST                'reduced'
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          
              216  JUMP_BACK           186  'to 186'

 L. 140       218  LOAD_FAST                'new_node'
              220  LOAD_ATTR                children
              222  POP_JUMP_IF_TRUE    246  'to 246'

 L. 142       224  LOAD_CONST               None
              226  STORE_FAST               'new_node'
              228  JUMP_FORWARD        914  'to 914'
            230_0  COME_FROM           168  '168'

 L. 145       230  LOAD_GLOBAL              reduce_tree
              232  LOAD_FAST                'node'
              234  LOAD_ATTR                children
              236  LOAD_CONST               0
              238  BINARY_SUBSCR    
              240  LOAD_FAST                'parent'
              242  CALL_FUNCTION_2       2  ''
              244  STORE_FAST               'new_node'
            246_0  COME_FROM           222  '222'
          246_248  JUMP_FORWARD        914  'to 914'
            250_0  COME_FROM           154  '154'

 L. 147       250  LOAD_FAST                'node'
              252  LOAD_ATTR                type
              254  LOAD_GLOBAL              syms
              256  LOAD_ATTR                Unit
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_FALSE   914  'to 914'

 L. 148       264  LOAD_GLOBAL              isinstance
              266  LOAD_FAST                'node'
              268  LOAD_ATTR                children
              270  LOAD_CONST               0
              272  BINARY_SUBSCR    
              274  LOAD_GLOBAL              pytree
              276  LOAD_ATTR                Leaf
              278  CALL_FUNCTION_2       2  ''
          280_282  POP_JUMP_IF_FALSE   318  'to 318'

 L. 149       284  LOAD_FAST                'node'
              286  LOAD_ATTR                children
              288  LOAD_CONST               0
              290  BINARY_SUBSCR    
              292  LOAD_ATTR                value
              294  LOAD_STR                 '('
              296  COMPARE_OP               ==

 L. 148   298_300  POP_JUMP_IF_FALSE   318  'to 318'

 L. 151       302  LOAD_GLOBAL              reduce_tree
              304  LOAD_FAST                'node'
              306  LOAD_ATTR                children
              308  LOAD_CONST               1
              310  BINARY_SUBSCR    
              312  LOAD_FAST                'parent'
              314  CALL_FUNCTION_2       2  ''
              316  RETURN_VALUE     
            318_0  COME_FROM           298  '298'
            318_1  COME_FROM           280  '280'

 L. 152       318  LOAD_GLOBAL              isinstance
              320  LOAD_FAST                'node'
              322  LOAD_ATTR                children
              324  LOAD_CONST               0
              326  BINARY_SUBSCR    
              328  LOAD_GLOBAL              pytree
              330  LOAD_ATTR                Leaf
              332  CALL_FUNCTION_2       2  ''
          334_336  POP_JUMP_IF_FALSE   356  'to 356'

 L. 153       338  LOAD_FAST                'node'
              340  LOAD_ATTR                children
              342  LOAD_CONST               0
              344  BINARY_SUBSCR    
              346  LOAD_ATTR                value
              348  LOAD_STR                 '['
              350  COMPARE_OP               ==

 L. 152   352_354  POP_JUMP_IF_TRUE    408  'to 408'
            356_0  COME_FROM           334  '334'

 L. 155       356  LOAD_GLOBAL              len
              358  LOAD_FAST                'node'
              360  LOAD_ATTR                children
              362  CALL_FUNCTION_1       1  ''
              364  LOAD_CONST               1
              366  COMPARE_OP               >

 L. 152   368_370  POP_JUMP_IF_FALSE   412  'to 412'

 L. 156       372  LOAD_GLOBAL              hasattr
              374  LOAD_FAST                'node'
              376  LOAD_ATTR                children
              378  LOAD_CONST               1
              380  BINARY_SUBSCR    
              382  LOAD_STR                 'value'
              384  CALL_FUNCTION_2       2  ''

 L. 152   386_388  POP_JUMP_IF_FALSE   412  'to 412'

 L. 157       390  LOAD_FAST                'node'
              392  LOAD_ATTR                children
              394  LOAD_CONST               1
              396  BINARY_SUBSCR    
              398  LOAD_ATTR                value
              400  LOAD_STR                 '['
              402  COMPARE_OP               ==

 L. 152   404_406  POP_JUMP_IF_FALSE   412  'to 412'
            408_0  COME_FROM           352  '352'

 L. 159       408  LOAD_CONST               None
              410  RETURN_VALUE     
            412_0  COME_FROM           404  '404'
            412_1  COME_FROM           386  '386'
            412_2  COME_FROM           368  '368'

 L. 161       412  LOAD_CONST               True
              414  STORE_FAST               'leaf'

 L. 162       416  LOAD_CONST               None
              418  STORE_FAST               'details_node'

 L. 163       420  LOAD_CONST               None
              422  STORE_FAST               'alternatives_node'

 L. 164       424  LOAD_CONST               False
              426  STORE_FAST               'has_repeater'

 L. 165       428  LOAD_CONST               None
              430  STORE_FAST               'repeater_node'

 L. 166       432  LOAD_CONST               False
              434  STORE_FAST               'has_variable_name'

 L. 168       436  LOAD_FAST                'node'
              438  LOAD_ATTR                children
              440  GET_ITER         
            442_0  COME_FROM           532  '532'
            442_1  COME_FROM           520  '520'
              442  FOR_ITER            544  'to 544'
              444  STORE_FAST               'child'

 L. 169       446  LOAD_FAST                'child'
              448  LOAD_ATTR                type
              450  LOAD_GLOBAL              syms
              452  LOAD_ATTR                Details
              454  COMPARE_OP               ==
          456_458  POP_JUMP_IF_FALSE   470  'to 470'

 L. 170       460  LOAD_CONST               False
              462  STORE_FAST               'leaf'

 L. 171       464  LOAD_FAST                'child'
              466  STORE_FAST               'details_node'
              468  JUMP_FORWARD        512  'to 512'
            470_0  COME_FROM           456  '456'

 L. 172       470  LOAD_FAST                'child'
              472  LOAD_ATTR                type
              474  LOAD_GLOBAL              syms
              476  LOAD_ATTR                Repeater
              478  COMPARE_OP               ==
          480_482  POP_JUMP_IF_FALSE   494  'to 494'

 L. 173       484  LOAD_CONST               True
              486  STORE_FAST               'has_repeater'

 L. 174       488  LOAD_FAST                'child'
              490  STORE_FAST               'repeater_node'
              492  JUMP_FORWARD        512  'to 512'
            494_0  COME_FROM           480  '480'

 L. 175       494  LOAD_FAST                'child'
              496  LOAD_ATTR                type
              498  LOAD_GLOBAL              syms
              500  LOAD_ATTR                Alternatives
              502  COMPARE_OP               ==
          504_506  POP_JUMP_IF_FALSE   512  'to 512'

 L. 176       508  LOAD_FAST                'child'
              510  STORE_FAST               'alternatives_node'
            512_0  COME_FROM           504  '504'
            512_1  COME_FROM           492  '492'
            512_2  COME_FROM           468  '468'

 L. 177       512  LOAD_GLOBAL              hasattr
              514  LOAD_FAST                'child'
              516  LOAD_STR                 'value'
              518  CALL_FUNCTION_2       2  ''
          520_522  POP_JUMP_IF_FALSE   442  'to 442'
              524  LOAD_FAST                'child'
              526  LOAD_ATTR                value
              528  LOAD_STR                 '='
              530  COMPARE_OP               ==
          532_534  POP_JUMP_IF_FALSE   442  'to 442'

 L. 178       536  LOAD_CONST               True
              538  STORE_FAST               'has_variable_name'
          540_542  JUMP_BACK           442  'to 442'

 L. 181       544  LOAD_FAST                'has_variable_name'
          546_548  POP_JUMP_IF_FALSE   596  'to 596'

 L. 183       550  LOAD_FAST                'node'
              552  LOAD_ATTR                children
              554  LOAD_CONST               2
              556  BINARY_SUBSCR    
              558  STORE_FAST               'name_leaf'

 L. 184       560  LOAD_GLOBAL              hasattr
              562  LOAD_FAST                'name_leaf'
              564  LOAD_STR                 'value'
              566  CALL_FUNCTION_2       2  ''
          568_570  POP_JUMP_IF_FALSE   606  'to 606'
              572  LOAD_FAST                'name_leaf'
              574  LOAD_ATTR                value
              576  LOAD_STR                 '('
              578  COMPARE_OP               ==
          580_582  POP_JUMP_IF_FALSE   606  'to 606'

 L. 186       584  LOAD_FAST                'node'
              586  LOAD_ATTR                children
              588  LOAD_CONST               3
              590  BINARY_SUBSCR    
              592  STORE_FAST               'name_leaf'
              594  JUMP_FORWARD        606  'to 606'
            596_0  COME_FROM           546  '546'

 L. 188       596  LOAD_FAST                'node'
              598  LOAD_ATTR                children
              600  LOAD_CONST               0
              602  BINARY_SUBSCR    
              604  STORE_FAST               'name_leaf'
            606_0  COME_FROM           594  '594'
            606_1  COME_FROM           580  '580'
            606_2  COME_FROM           568  '568'

 L. 191       606  LOAD_FAST                'name_leaf'
              608  LOAD_ATTR                type
              610  LOAD_GLOBAL              token_labels
              612  LOAD_ATTR                NAME
              614  COMPARE_OP               ==
          616_618  POP_JUMP_IF_FALSE   698  'to 698'

 L. 193       620  LOAD_FAST                'name_leaf'
              622  LOAD_ATTR                value
              624  LOAD_STR                 'any'
              626  COMPARE_OP               ==
          628_630  POP_JUMP_IF_FALSE   644  'to 644'

 L. 194       632  LOAD_GLOBAL              MinNode
              634  LOAD_GLOBAL              TYPE_ANY
              636  LOAD_CONST               ('type',)
              638  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              640  STORE_FAST               'new_node'
              642  JUMP_FORWARD        696  'to 696'
            644_0  COME_FROM           628  '628'

 L. 196       644  LOAD_GLOBAL              hasattr
              646  LOAD_GLOBAL              token_labels
              648  LOAD_FAST                'name_leaf'
              650  LOAD_ATTR                value
              652  CALL_FUNCTION_2       2  ''
          654_656  POP_JUMP_IF_FALSE   678  'to 678'

 L. 197       658  LOAD_GLOBAL              MinNode
              660  LOAD_GLOBAL              getattr
              662  LOAD_GLOBAL              token_labels
              664  LOAD_FAST                'name_leaf'
              666  LOAD_ATTR                value
              668  CALL_FUNCTION_2       2  ''
              670  LOAD_CONST               ('type',)
              672  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              674  STORE_FAST               'new_node'
              676  JUMP_FORWARD        696  'to 696'
            678_0  COME_FROM           654  '654'

 L. 199       678  LOAD_GLOBAL              MinNode
              680  LOAD_GLOBAL              getattr
              682  LOAD_GLOBAL              pysyms
              684  LOAD_FAST                'name_leaf'
              686  LOAD_ATTR                value
              688  CALL_FUNCTION_2       2  ''
              690  LOAD_CONST               ('type',)
              692  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              694  STORE_FAST               'new_node'
            696_0  COME_FROM           676  '676'
            696_1  COME_FROM           642  '642'
              696  JUMP_FORWARD        790  'to 790'
            698_0  COME_FROM           616  '616'

 L. 201       698  LOAD_FAST                'name_leaf'
              700  LOAD_ATTR                type
              702  LOAD_GLOBAL              token_labels
              704  LOAD_ATTR                STRING
              706  COMPARE_OP               ==
          708_710  POP_JUMP_IF_FALSE   766  'to 766'

 L. 204       712  LOAD_FAST                'name_leaf'
              714  LOAD_ATTR                value
              716  LOAD_METHOD              strip
              718  LOAD_STR                 "'"
              720  CALL_METHOD_1         1  ''
              722  STORE_FAST               'name'

 L. 205       724  LOAD_FAST                'name'
              726  LOAD_GLOBAL              tokens
              728  COMPARE_OP               in
          730_732  POP_JUMP_IF_FALSE   750  'to 750'

 L. 206       734  LOAD_GLOBAL              MinNode
              736  LOAD_GLOBAL              tokens
              738  LOAD_FAST                'name'
              740  BINARY_SUBSCR    
              742  LOAD_CONST               ('type',)
              744  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              746  STORE_FAST               'new_node'
              748  JUMP_FORWARD        764  'to 764'
            750_0  COME_FROM           730  '730'

 L. 208       750  LOAD_GLOBAL              MinNode
              752  LOAD_GLOBAL              token_labels
              754  LOAD_ATTR                NAME
              756  LOAD_FAST                'name'
              758  LOAD_CONST               ('type', 'name')
              760  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              762  STORE_FAST               'new_node'
            764_0  COME_FROM           748  '748'
              764  JUMP_FORWARD        790  'to 790'
            766_0  COME_FROM           708  '708'

 L. 209       766  LOAD_FAST                'name_leaf'
              768  LOAD_ATTR                type
              770  LOAD_GLOBAL              syms
              772  LOAD_ATTR                Alternatives
              774  COMPARE_OP               ==
          776_778  POP_JUMP_IF_FALSE   790  'to 790'

 L. 210       780  LOAD_GLOBAL              reduce_tree
              782  LOAD_FAST                'alternatives_node'
              784  LOAD_FAST                'parent'
              786  CALL_FUNCTION_2       2  ''
              788  STORE_FAST               'new_node'
            790_0  COME_FROM           776  '776'
            790_1  COME_FROM           764  '764'
            790_2  COME_FROM           696  '696'

 L. 213       790  LOAD_FAST                'has_repeater'
          792_794  POP_JUMP_IF_FALSE   844  'to 844'

 L. 214       796  LOAD_FAST                'repeater_node'
              798  LOAD_ATTR                children
              800  LOAD_CONST               0
              802  BINARY_SUBSCR    
              804  LOAD_ATTR                value
              806  LOAD_STR                 '*'
              808  COMPARE_OP               ==
          810_812  POP_JUMP_IF_FALSE   820  'to 820'

 L. 216       814  LOAD_CONST               None
              816  STORE_FAST               'new_node'
              818  JUMP_FORWARD        844  'to 844'
            820_0  COME_FROM           810  '810'

 L. 217       820  LOAD_FAST                'repeater_node'
              822  LOAD_ATTR                children
              824  LOAD_CONST               0
              826  BINARY_SUBSCR    
              828  LOAD_ATTR                value
              830  LOAD_STR                 '+'
              832  COMPARE_OP               ==
          834_836  POP_JUMP_IF_FALSE   840  'to 840'

 L. 219       838  BREAK_LOOP          844  'to 844'
            840_0  COME_FROM           834  '834'
            840_1  COME_FROM            68  '68'

 L. 222       840  LOAD_GLOBAL              NotImplementedError
              842  RAISE_VARARGS_1       1  'exception instance'
            844_0  COME_FROM           838  '838'
            844_1  COME_FROM           818  '818'
            844_2  COME_FROM           792  '792'

 L. 226       844  LOAD_FAST                'details_node'
          846_848  POP_JUMP_IF_FALSE   914  'to 914'
              850  LOAD_FAST                'new_node'
              852  LOAD_CONST               None
              854  COMPARE_OP               is-not
          856_858  POP_JUMP_IF_FALSE   914  'to 914'

 L. 227       860  LOAD_FAST                'details_node'
              862  LOAD_ATTR                children
              864  LOAD_CONST               1
              866  LOAD_CONST               -1
              868  BUILD_SLICE_2         2 
              870  BINARY_SUBSCR    
              872  GET_ITER         
            874_0  COME_FROM           894  '894'
              874  FOR_ITER            914  'to 914'
              876  STORE_FAST               'child'

 L. 229       878  LOAD_GLOBAL              reduce_tree
              880  LOAD_FAST                'child'
              882  LOAD_FAST                'new_node'
              884  CALL_FUNCTION_2       2  ''
              886  STORE_FAST               'reduced'

 L. 230       888  LOAD_FAST                'reduced'
              890  LOAD_CONST               None
              892  COMPARE_OP               is-not
            894_0  COME_FROM           228  '228'
          894_896  POP_JUMP_IF_FALSE   874  'to 874'

 L. 231       898  LOAD_FAST                'new_node'
              900  LOAD_ATTR                children
              902  LOAD_METHOD              append
              904  LOAD_FAST                'reduced'
              906  CALL_METHOD_1         1  ''
              908  POP_TOP          
          910_912  JUMP_BACK           874  'to 874'
            914_0  COME_FROM           856  '856'
            914_1  COME_FROM           846  '846'
            914_2  COME_FROM           260  '260'
            914_3  COME_FROM           246  '246'
            914_4  COME_FROM           140  '140'

 L. 232       914  LOAD_FAST                'new_node'
          916_918  POP_JUMP_IF_FALSE   926  'to 926'

 L. 233       920  LOAD_FAST                'parent'
              922  LOAD_FAST                'new_node'
              924  STORE_ATTR               parent
            926_0  COME_FROM           916  '916'

 L. 234       926  LOAD_FAST                'new_node'
              928  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 894_0


def get_characteristic_subpattern(subpatterns):
    """Picks the most characteristic from a list of linear patterns
    Current order used is:
    names > common_names > common_chars
    """
    if not isinstancesubpatternslist:
        return subpatterns
    if len(subpatterns) == 1:
        return subpatterns[0]
    subpatterns_with_names = []
    subpatterns_with_common_names = []
    common_names = [
     'in', 'for', 'if', 'not', 'None']
    subpatterns_with_common_chars = []
    common_chars = '[]().,:'
    for subpattern in subpatterns:
        if any(rec_testsubpattern(lambda x: type(x) is str)):
            if any(rec_testsubpattern(lambda x: isinstancexstr and x in common_chars)):
                subpatterns_with_common_chars.appendsubpattern
            elif any(rec_testsubpattern(lambda x: isinstancexstr and x in common_names)):
                subpatterns_with_common_names.appendsubpattern
            else:
                subpatterns_with_names.appendsubpattern
        if subpatterns_with_names:
            subpatterns = subpatterns_with_names
        else:
            if subpatterns_with_common_names:
                subpatterns = subpatterns_with_common_names
            else:
                if subpatterns_with_common_chars:
                    subpatterns = subpatterns_with_common_chars
        return max(subpatterns, key=len)


def rec_test(sequence, test_func):
    """Tests test_func on all items of sequence and items of included
    sub-iterables"""
    for x in sequence:
        if isinstancex(list, tuple):
            (yield from rec_testxtest_func)
        else:
            (yield test_func(x))