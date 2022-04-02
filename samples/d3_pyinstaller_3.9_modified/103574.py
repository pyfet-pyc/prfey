# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: lib2to3\refactor.py
"""Refactoring framework.

Used as a main program, this can refactor any number of files and/or
recursively descend down directories.  Imported as a module, this
provides infrastructure to write your own refactoring tool.
"""
__author__ = 'Guido van Rossum <guido@python.org>'
import io, os, pkgutil, sys, logging, operator, collections
from itertools import chain
from .pgen2 import driver, tokenize, token
from .fixer_util import find_root
from . import pytree, pygram
from . import btm_matcher as bm

def get_all_fix_names(fixer_pkg, remove_prefix=True):
    """Return a sorted list of all available fix names in the given package."""
    pkg = __import__(fixer_pkg, [], [], ['*'])
    fix_names = []
    for finder, name, ispkg in pkgutil.iter_modules(pkg.__path__):
        if name.startswith('fix_'):
            if remove_prefix:
                name = name[4:]
            else:
                fix_names.append(name)
    else:
        return fix_names


class _EveryNode(Exception):
    pass


def _get_head_types--- This code section failed: ---

 L.  51         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'pat'
                4  LOAD_GLOBAL              pytree
                6  LOAD_ATTR                NodePattern
                8  LOAD_GLOBAL              pytree
               10  LOAD_ATTR                LeafPattern
               12  BUILD_TUPLE_2         2 
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    40  'to 40'

 L.  55        18  LOAD_FAST                'pat'
               20  LOAD_ATTR                type
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L.  56        28  LOAD_GLOBAL              _EveryNode
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            26  '26'

 L.  57        32  LOAD_FAST                'pat'
               34  LOAD_ATTR                type
               36  BUILD_SET_1           1 
               38  RETURN_VALUE     
             40_0  COME_FROM            16  '16'

 L.  59        40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'pat'
               44  LOAD_GLOBAL              pytree
               46  LOAD_ATTR                NegatedPattern
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_FALSE    72  'to 72'

 L.  60        52  LOAD_FAST                'pat'
               54  LOAD_ATTR                content
               56  POP_JUMP_IF_FALSE    68  'to 68'

 L.  61        58  LOAD_GLOBAL              _get_head_types
               60  LOAD_FAST                'pat'
               62  LOAD_ATTR                content
               64  CALL_FUNCTION_1       1  ''
               66  RETURN_VALUE     
             68_0  COME_FROM            56  '56'

 L.  62        68  LOAD_GLOBAL              _EveryNode
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            50  '50'

 L.  64        72  LOAD_GLOBAL              isinstance
               74  LOAD_FAST                'pat'
               76  LOAD_GLOBAL              pytree
               78  LOAD_ATTR                WildcardPattern
               80  CALL_FUNCTION_2       2  ''
               82  POP_JUMP_IF_FALSE   130  'to 130'

 L.  66        84  LOAD_GLOBAL              set
               86  CALL_FUNCTION_0       0  ''
               88  STORE_FAST               'r'

 L.  67        90  LOAD_FAST                'pat'
               92  LOAD_ATTR                content
               94  GET_ITER         
             96_0  COME_FROM           124  '124'
               96  FOR_ITER            126  'to 126'
               98  STORE_FAST               'p'

 L.  68       100  LOAD_FAST                'p'
              102  GET_ITER         
            104_0  COME_FROM           122  '122'
              104  FOR_ITER            124  'to 124'
              106  STORE_FAST               'x'

 L.  69       108  LOAD_FAST                'r'
              110  LOAD_METHOD              update
              112  LOAD_GLOBAL              _get_head_types
              114  LOAD_FAST                'x'
              116  CALL_FUNCTION_1       1  ''
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          
              122  JUMP_BACK           104  'to 104'
            124_0  COME_FROM           104  '104'
              124  JUMP_BACK            96  'to 96'
            126_0  COME_FROM            96  '96'

 L.  70       126  LOAD_FAST                'r'
              128  RETURN_VALUE     
            130_0  COME_FROM            82  '82'

 L.  72       130  LOAD_GLOBAL              Exception
              132  LOAD_STR                 "Oh no! I don't understand pattern %s"
              134  LOAD_FAST                'pat'
              136  BINARY_MODULO    
              138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 24


def _get_headnode_dict--- This code section failed: ---

 L.  78         0  LOAD_GLOBAL              collections
                2  LOAD_METHOD              defaultdict
                4  LOAD_GLOBAL              list
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'head_nodes'

 L.  79        10  BUILD_LIST_0          0 
               12  STORE_FAST               'every'

 L.  80        14  LOAD_FAST                'fixer_list'
               16  GET_ITER         
             18_0  COME_FROM           136  '136'
             18_1  COME_FROM           124  '124'
             18_2  COME_FROM            96  '96'
               18  FOR_ITER            138  'to 138'
               20  STORE_FAST               'fixer'

 L.  81        22  LOAD_FAST                'fixer'
               24  LOAD_ATTR                pattern
               26  POP_JUMP_IF_FALSE    98  'to 98'

 L.  82        28  SETUP_FINALLY        44  'to 44'

 L.  83        30  LOAD_GLOBAL              _get_head_types
               32  LOAD_FAST                'fixer'
               34  LOAD_ATTR                pattern
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'heads'
               40  POP_BLOCK        
               42  JUMP_FORWARD         72  'to 72'
             44_0  COME_FROM_FINALLY    28  '28'

 L.  84        44  DUP_TOP          
               46  LOAD_GLOBAL              _EveryNode
               48  <121>                70  ''
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L.  85        56  LOAD_FAST                'every'
               58  LOAD_METHOD              append
               60  LOAD_FAST                'fixer'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
               66  POP_EXCEPT       
               68  JUMP_FORWARD        136  'to 136'
               70  <48>             
             72_0  COME_FROM            42  '42'

 L.  87        72  LOAD_FAST                'heads'
               74  GET_ITER         
             76_0  COME_FROM            94  '94'
               76  FOR_ITER             96  'to 96'
               78  STORE_FAST               'node_type'

 L.  88        80  LOAD_FAST                'head_nodes'
               82  LOAD_FAST                'node_type'
               84  BINARY_SUBSCR    
               86  LOAD_METHOD              append
               88  LOAD_FAST                'fixer'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          
               94  JUMP_BACK            76  'to 76'
             96_0  COME_FROM            76  '76'
               96  JUMP_BACK            18  'to 18'
             98_0  COME_FROM            26  '26'

 L.  90        98  LOAD_FAST                'fixer'
              100  LOAD_ATTR                _accept_type
              102  LOAD_CONST               None
              104  <117>                 1  ''
              106  POP_JUMP_IF_FALSE   126  'to 126'

 L.  91       108  LOAD_FAST                'head_nodes'
              110  LOAD_FAST                'fixer'
              112  LOAD_ATTR                _accept_type
              114  BINARY_SUBSCR    
              116  LOAD_METHOD              append
              118  LOAD_FAST                'fixer'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
              124  JUMP_BACK            18  'to 18'
            126_0  COME_FROM           106  '106'

 L.  93       126  LOAD_FAST                'every'
              128  LOAD_METHOD              append
              130  LOAD_FAST                'fixer'
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
            136_0  COME_FROM            68  '68'
              136  JUMP_BACK            18  'to 18'
            138_0  COME_FROM            18  '18'

 L.  94       138  LOAD_GLOBAL              chain
              140  LOAD_GLOBAL              pygram
              142  LOAD_ATTR                python_grammar
              144  LOAD_ATTR                symbol2number
              146  LOAD_METHOD              values
              148  CALL_METHOD_0         0  ''

 L.  95       150  LOAD_GLOBAL              pygram
              152  LOAD_ATTR                python_grammar
              154  LOAD_ATTR                tokens

 L.  94       156  CALL_FUNCTION_2       2  ''
              158  GET_ITER         
            160_0  COME_FROM           178  '178'
              160  FOR_ITER            180  'to 180'
              162  STORE_FAST               'node_type'

 L.  96       164  LOAD_FAST                'head_nodes'
              166  LOAD_FAST                'node_type'
              168  BINARY_SUBSCR    
              170  LOAD_METHOD              extend
              172  LOAD_FAST                'every'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          
              178  JUMP_BACK           160  'to 160'
            180_0  COME_FROM           160  '160'

 L.  97       180  LOAD_GLOBAL              dict
              182  LOAD_FAST                'head_nodes'
              184  CALL_FUNCTION_1       1  ''
              186  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 48


def get_fixers_from_package(pkg_name):
    """
    Return the fully qualified names for fixers in the package pkg_name.
    """
    return [pkg_name + '.' + fix_name for fix_name in get_all_fix_namespkg_nameFalse]


def _identity(obj):
    return obj


def _detect_future_features--- This code section failed: ---

 L. 112         0  LOAD_CONST               False
                2  STORE_FAST               'have_docstring'

 L. 113         4  LOAD_GLOBAL              tokenize
                6  LOAD_METHOD              generate_tokens
                8  LOAD_GLOBAL              io
               10  LOAD_METHOD              StringIO
               12  LOAD_FAST                'source'
               14  CALL_METHOD_1         1  ''
               16  LOAD_ATTR                readline
               18  CALL_METHOD_1         1  ''
               20  STORE_DEREF              'gen'

 L. 114        22  LOAD_CLOSURE             'gen'
               24  BUILD_TUPLE_1         1 
               26  LOAD_CODE                <code_object advance>
               28  LOAD_STR                 '_detect_future_features.<locals>.advance'
               30  MAKE_FUNCTION_8          'closure'
               32  STORE_FAST               'advance'

 L. 117        34  LOAD_GLOBAL              frozenset
               36  LOAD_GLOBAL              token
               38  LOAD_ATTR                NEWLINE
               40  LOAD_GLOBAL              tokenize
               42  LOAD_ATTR                NL
               44  LOAD_GLOBAL              token
               46  LOAD_ATTR                COMMENT
               48  BUILD_SET_3           3 
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'ignore'

 L. 118        54  LOAD_GLOBAL              set
               56  CALL_FUNCTION_0       0  ''
               58  STORE_FAST               'features'

 L. 119        60  SETUP_FINALLY       314  'to 314'
             62_0  COME_FROM           308  '308'
             62_1  COME_FROM           302  '302'
             62_2  COME_FROM           106  '106'
             62_3  COME_FROM            82  '82'
             62_4  COME_FROM            80  '80'

 L. 121        62  LOAD_FAST                'advance'
               64  CALL_FUNCTION_0       0  ''
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               'tp'
               70  STORE_FAST               'value'

 L. 122        72  LOAD_FAST                'tp'
               74  LOAD_FAST                'ignore'
               76  <118>                 0  ''
               78  POP_JUMP_IF_FALSE    84  'to 84'

 L. 123        80  CONTINUE             62  'to 62'
               82  JUMP_BACK            62  'to 62'
             84_0  COME_FROM            78  '78'

 L. 124        84  LOAD_FAST                'tp'
               86  LOAD_GLOBAL              token
               88  LOAD_ATTR                STRING
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   108  'to 108'

 L. 125        94  LOAD_FAST                'have_docstring'
               96  POP_JUMP_IF_FALSE   102  'to 102'

 L. 126    98_100  JUMP_FORWARD        310  'to 310'
            102_0  COME_FROM            96  '96'

 L. 127       102  LOAD_CONST               True
              104  STORE_FAST               'have_docstring'
              106  JUMP_BACK            62  'to 62'
            108_0  COME_FROM            92  '92'

 L. 128       108  LOAD_FAST                'tp'
              110  LOAD_GLOBAL              token
              112  LOAD_ATTR                NAME
              114  COMPARE_OP               ==
          116_118  POP_JUMP_IF_FALSE   310  'to 310'
              120  LOAD_FAST                'value'
              122  LOAD_STR                 'from'
              124  COMPARE_OP               ==
          126_128  POP_JUMP_IF_FALSE   310  'to 310'

 L. 129       130  LOAD_FAST                'advance'
              132  CALL_FUNCTION_0       0  ''
              134  UNPACK_SEQUENCE_2     2 
              136  STORE_FAST               'tp'
              138  STORE_FAST               'value'

 L. 130       140  LOAD_FAST                'tp'
              142  LOAD_GLOBAL              token
              144  LOAD_ATTR                NAME
              146  COMPARE_OP               !=
              148  POP_JUMP_IF_TRUE    158  'to 158'
              150  LOAD_FAST                'value'
              152  LOAD_STR                 '__future__'
              154  COMPARE_OP               !=
              156  POP_JUMP_IF_FALSE   162  'to 162'
            158_0  COME_FROM           148  '148'

 L. 131   158_160  JUMP_FORWARD        310  'to 310'
            162_0  COME_FROM           156  '156'

 L. 132       162  LOAD_FAST                'advance'
              164  CALL_FUNCTION_0       0  ''
              166  UNPACK_SEQUENCE_2     2 
              168  STORE_FAST               'tp'
              170  STORE_FAST               'value'

 L. 133       172  LOAD_FAST                'tp'
              174  LOAD_GLOBAL              token
              176  LOAD_ATTR                NAME
              178  COMPARE_OP               !=
              180  POP_JUMP_IF_TRUE    190  'to 190'
              182  LOAD_FAST                'value'
              184  LOAD_STR                 'import'
              186  COMPARE_OP               !=
              188  POP_JUMP_IF_FALSE   194  'to 194'
            190_0  COME_FROM           180  '180'

 L. 134   190_192  JUMP_FORWARD        310  'to 310'
            194_0  COME_FROM           188  '188'

 L. 135       194  LOAD_FAST                'advance'
              196  CALL_FUNCTION_0       0  ''
              198  UNPACK_SEQUENCE_2     2 
              200  STORE_FAST               'tp'
              202  STORE_FAST               'value'

 L. 136       204  LOAD_FAST                'tp'
              206  LOAD_GLOBAL              token
              208  LOAD_ATTR                OP
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   232  'to 232'
              214  LOAD_FAST                'value'
              216  LOAD_STR                 '('
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_FALSE   232  'to 232'

 L. 137       222  LOAD_FAST                'advance'
              224  CALL_FUNCTION_0       0  ''
              226  UNPACK_SEQUENCE_2     2 
              228  STORE_FAST               'tp'
              230  STORE_FAST               'value'
            232_0  COME_FROM           300  '300'
            232_1  COME_FROM           220  '220'
            232_2  COME_FROM           212  '212'

 L. 138       232  LOAD_FAST                'tp'
              234  LOAD_GLOBAL              token
              236  LOAD_ATTR                NAME
              238  COMPARE_OP               ==
          240_242  POP_JUMP_IF_FALSE   308  'to 308'

 L. 139       244  LOAD_FAST                'features'
              246  LOAD_METHOD              add
              248  LOAD_FAST                'value'
              250  CALL_METHOD_1         1  ''
              252  POP_TOP          

 L. 140       254  LOAD_FAST                'advance'
              256  CALL_FUNCTION_0       0  ''
              258  UNPACK_SEQUENCE_2     2 
              260  STORE_FAST               'tp'
              262  STORE_FAST               'value'

 L. 141       264  LOAD_FAST                'tp'
              266  LOAD_GLOBAL              token
              268  LOAD_ATTR                OP
              270  COMPARE_OP               !=
          272_274  POP_JUMP_IF_TRUE    302  'to 302'
              276  LOAD_FAST                'value'
              278  LOAD_STR                 ','
              280  COMPARE_OP               !=
          282_284  POP_JUMP_IF_FALSE   290  'to 290'

 L. 142   286_288  JUMP_FORWARD        308  'to 308'
            290_0  COME_FROM           282  '282'

 L. 143       290  LOAD_FAST                'advance'
              292  CALL_FUNCTION_0       0  ''
              294  UNPACK_SEQUENCE_2     2 
              296  STORE_FAST               'tp'
              298  STORE_FAST               'value'
              300  JUMP_BACK           232  'to 232'
            302_0  COME_FROM           272  '272'
              302  JUMP_BACK            62  'to 62'

 L. 145   304_306  JUMP_FORWARD        310  'to 310'
            308_0  COME_FROM           286  '286'
            308_1  COME_FROM           240  '240'
              308  JUMP_BACK            62  'to 62'
            310_0  COME_FROM           304  '304'
            310_1  COME_FROM           190  '190'
            310_2  COME_FROM           158  '158'
            310_3  COME_FROM           126  '126'
            310_4  COME_FROM           116  '116'
            310_5  COME_FROM            98  '98'
              310  POP_BLOCK        
              312  JUMP_FORWARD        334  'to 334'
            314_0  COME_FROM_FINALLY    60  '60'

 L. 146       314  DUP_TOP          
              316  LOAD_GLOBAL              StopIteration
          318_320  <121>               332  ''
              322  POP_TOP          
              324  POP_TOP          
              326  POP_TOP          

 L. 147       328  POP_EXCEPT       
              330  JUMP_FORWARD        334  'to 334'
              332  <48>             
            334_0  COME_FROM           330  '330'
            334_1  COME_FROM           312  '312'

 L. 148       334  LOAD_GLOBAL              frozenset
              336  LOAD_FAST                'features'
              338  CALL_FUNCTION_1       1  ''
              340  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 76


class FixerError(Exception):
    __doc__ = 'A fixer could not be loaded.'


class RefactoringTool(object):
    _default_options = {'print_function':False, 
     'exec_function':False, 
     'write_unchanged_files':False}
    CLASS_PREFIX = 'Fix'
    FILE_PREFIX = 'fix_'

    def __init__--- This code section failed: ---

 L. 172         0  LOAD_FAST                'fixer_names'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               fixers

 L. 173         6  LOAD_FAST                'explicit'
                8  JUMP_IF_TRUE_OR_POP    12  'to 12'
               10  BUILD_LIST_0          0 
             12_0  COME_FROM             8  '8'
               12  LOAD_FAST                'self'
               14  STORE_ATTR               explicit

 L. 174        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _default_options
               20  LOAD_METHOD              copy
               22  CALL_METHOD_0         0  ''
               24  LOAD_FAST                'self'
               26  STORE_ATTR               options

 L. 175        28  LOAD_FAST                'options'
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    48  'to 48'

 L. 176        36  LOAD_FAST                'self'
               38  LOAD_ATTR                options
               40  LOAD_METHOD              update
               42  LOAD_FAST                'options'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
             48_0  COME_FROM            34  '34'

 L. 177        48  LOAD_GLOBAL              pygram
               50  LOAD_ATTR                python_grammar
               52  LOAD_METHOD              copy
               54  CALL_METHOD_0         0  ''
               56  LOAD_FAST                'self'
               58  STORE_ATTR               grammar

 L. 179        60  LOAD_FAST                'self'
               62  LOAD_ATTR                options
               64  LOAD_STR                 'print_function'
               66  BINARY_SUBSCR    
               68  POP_JUMP_IF_FALSE    82  'to 82'

 L. 180        70  LOAD_FAST                'self'
               72  LOAD_ATTR                grammar
               74  LOAD_ATTR                keywords
               76  LOAD_STR                 'print'
               78  DELETE_SUBSCR    
               80  JUMP_FORWARD        102  'to 102'
             82_0  COME_FROM            68  '68'

 L. 181        82  LOAD_FAST                'self'
               84  LOAD_ATTR                options
               86  LOAD_STR                 'exec_function'
               88  BINARY_SUBSCR    
               90  POP_JUMP_IF_FALSE   102  'to 102'

 L. 182        92  LOAD_FAST                'self'
               94  LOAD_ATTR                grammar
               96  LOAD_ATTR                keywords
               98  LOAD_STR                 'exec'
              100  DELETE_SUBSCR    
            102_0  COME_FROM            90  '90'
            102_1  COME_FROM            80  '80'

 L. 187       102  LOAD_FAST                'self'
              104  LOAD_ATTR                options
              106  LOAD_METHOD              get
              108  LOAD_STR                 'write_unchanged_files'
              110  CALL_METHOD_1         1  ''
              112  LOAD_FAST                'self'
              114  STORE_ATTR               write_unchanged_files

 L. 188       116  BUILD_LIST_0          0 
              118  LOAD_FAST                'self'
              120  STORE_ATTR               errors

 L. 189       122  LOAD_GLOBAL              logging
              124  LOAD_METHOD              getLogger
              126  LOAD_STR                 'RefactoringTool'
              128  CALL_METHOD_1         1  ''
              130  LOAD_FAST                'self'
              132  STORE_ATTR               logger

 L. 190       134  BUILD_LIST_0          0 
              136  LOAD_FAST                'self'
              138  STORE_ATTR               fixer_log

 L. 191       140  LOAD_CONST               False
              142  LOAD_FAST                'self'
              144  STORE_ATTR               wrote

 L. 192       146  LOAD_GLOBAL              driver
              148  LOAD_ATTR                Driver
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                grammar

 L. 193       154  LOAD_GLOBAL              pytree
              156  LOAD_ATTR                convert

 L. 194       158  LOAD_FAST                'self'
              160  LOAD_ATTR                logger

 L. 192       162  LOAD_CONST               ('convert', 'logger')
              164  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              166  LOAD_FAST                'self'
              168  STORE_ATTR               driver

 L. 195       170  LOAD_FAST                'self'
              172  LOAD_METHOD              get_fixers
              174  CALL_METHOD_0         0  ''
              176  UNPACK_SEQUENCE_2     2 
              178  LOAD_FAST                'self'
              180  STORE_ATTR               pre_order
              182  LOAD_FAST                'self'
              184  STORE_ATTR               post_order

 L. 198       186  BUILD_LIST_0          0 
              188  LOAD_FAST                'self'
              190  STORE_ATTR               files

 L. 200       192  LOAD_GLOBAL              bm
              194  LOAD_METHOD              BottomMatcher
              196  CALL_METHOD_0         0  ''
              198  LOAD_FAST                'self'
              200  STORE_ATTR               BM

 L. 201       202  BUILD_LIST_0          0 
              204  LOAD_FAST                'self'
              206  STORE_ATTR               bmi_pre_order

 L. 202       208  BUILD_LIST_0          0 
              210  LOAD_FAST                'self'
              212  STORE_ATTR               bmi_post_order

 L. 204       214  LOAD_GLOBAL              chain
              216  LOAD_FAST                'self'
              218  LOAD_ATTR                post_order
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                pre_order
              224  CALL_FUNCTION_2       2  ''
              226  GET_ITER         
            228_0  COME_FROM           300  '300'
            228_1  COME_FROM           286  '286'
            228_2  COME_FROM           276  '276'
            228_3  COME_FROM           250  '250'
              228  FOR_ITER            302  'to 302'
              230  STORE_FAST               'fixer'

 L. 205       232  LOAD_FAST                'fixer'
              234  LOAD_ATTR                BM_compatible
              236  POP_JUMP_IF_FALSE   252  'to 252'

 L. 206       238  LOAD_FAST                'self'
              240  LOAD_ATTR                BM
              242  LOAD_METHOD              add_fixer
              244  LOAD_FAST                'fixer'
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          
              250  JUMP_BACK           228  'to 228'
            252_0  COME_FROM           236  '236'

 L. 209       252  LOAD_FAST                'fixer'
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                pre_order
              258  <118>                 0  ''
          260_262  POP_JUMP_IF_FALSE   278  'to 278'

 L. 210       264  LOAD_FAST                'self'
              266  LOAD_ATTR                bmi_pre_order
              268  LOAD_METHOD              append
              270  LOAD_FAST                'fixer'
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          
              276  JUMP_BACK           228  'to 228'
            278_0  COME_FROM           260  '260'

 L. 211       278  LOAD_FAST                'fixer'
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                post_order
              284  <118>                 0  ''
              286  POP_JUMP_IF_FALSE_BACK   228  'to 228'

 L. 212       288  LOAD_FAST                'self'
              290  LOAD_ATTR                bmi_post_order
              292  LOAD_METHOD              append
              294  LOAD_FAST                'fixer'
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          
              300  JUMP_BACK           228  'to 228'
            302_0  COME_FROM           228  '228'

 L. 214       302  LOAD_GLOBAL              _get_headnode_dict
              304  LOAD_FAST                'self'
              306  LOAD_ATTR                bmi_pre_order
              308  CALL_FUNCTION_1       1  ''
              310  LOAD_FAST                'self'
              312  STORE_ATTR               bmi_pre_order_heads

 L. 215       314  LOAD_GLOBAL              _get_headnode_dict
              316  LOAD_FAST                'self'
              318  LOAD_ATTR                bmi_post_order
              320  CALL_FUNCTION_1       1  ''
              322  LOAD_FAST                'self'
              324  STORE_ATTR               bmi_post_order_heads

Parse error at or near `<117>' instruction at offset 32

    def get_fixers--- This code section failed: ---

 L. 227         0  BUILD_LIST_0          0 
                2  STORE_FAST               'pre_order_fixers'

 L. 228         4  BUILD_LIST_0          0 
                6  STORE_FAST               'post_order_fixers'

 L. 229         8  LOAD_FAST                'self'
               10  LOAD_ATTR                fixers
               12  GET_ITER         
             14_0  COME_FROM           298  '298'
             14_1  COME_FROM           282  '282'
             14_2  COME_FROM           258  '258'
             14_3  COME_FROM           222  '222'
            14_16  FOR_ITER            300  'to 300'
               18  STORE_FAST               'fix_mod_path'

 L. 230        20  LOAD_GLOBAL              __import__
               22  LOAD_FAST                'fix_mod_path'
               24  BUILD_MAP_0           0 
               26  BUILD_MAP_0           0 
               28  LOAD_STR                 '*'
               30  BUILD_LIST_1          1 
               32  CALL_FUNCTION_4       4  ''
               34  STORE_FAST               'mod'

 L. 231        36  LOAD_FAST                'fix_mod_path'
               38  LOAD_METHOD              rsplit
               40  LOAD_STR                 '.'
               42  LOAD_CONST               1
               44  CALL_METHOD_2         2  ''
               46  LOAD_CONST               -1
               48  BINARY_SUBSCR    
               50  STORE_FAST               'fix_name'

 L. 232        52  LOAD_FAST                'fix_name'
               54  LOAD_METHOD              startswith
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                FILE_PREFIX
               60  CALL_METHOD_1         1  ''
               62  POP_JUMP_IF_FALSE    82  'to 82'

 L. 233        64  LOAD_FAST                'fix_name'
               66  LOAD_GLOBAL              len
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                FILE_PREFIX
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_CONST               None
               76  BUILD_SLICE_2         2 
               78  BINARY_SUBSCR    
               80  STORE_FAST               'fix_name'
             82_0  COME_FROM            62  '62'

 L. 234        82  LOAD_FAST                'fix_name'
               84  LOAD_METHOD              split
               86  LOAD_STR                 '_'
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'parts'

 L. 235        92  LOAD_FAST                'self'
               94  LOAD_ATTR                CLASS_PREFIX
               96  LOAD_STR                 ''
               98  LOAD_METHOD              join
              100  LOAD_LISTCOMP            '<code_object <listcomp>>'
              102  LOAD_STR                 'RefactoringTool.get_fixers.<locals>.<listcomp>'
              104  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              106  LOAD_FAST                'parts'
              108  GET_ITER         
              110  CALL_FUNCTION_1       1  ''
              112  CALL_METHOD_1         1  ''
              114  BINARY_ADD       
              116  STORE_FAST               'class_name'

 L. 236       118  SETUP_FINALLY       134  'to 134'

 L. 237       120  LOAD_GLOBAL              getattr
              122  LOAD_FAST                'mod'
              124  LOAD_FAST                'class_name'
              126  CALL_FUNCTION_2       2  ''
              128  STORE_FAST               'fix_class'
              130  POP_BLOCK        
              132  JUMP_FORWARD        170  'to 170'
            134_0  COME_FROM_FINALLY   118  '118'

 L. 238       134  DUP_TOP          
              136  LOAD_GLOBAL              AttributeError
              138  <121>               168  ''
              140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L. 239       146  LOAD_GLOBAL              FixerError
              148  LOAD_STR                 "Can't find %s.%s"
              150  LOAD_FAST                'fix_name'
              152  LOAD_FAST                'class_name'
              154  BUILD_TUPLE_2         2 
              156  BINARY_MODULO    
              158  CALL_FUNCTION_1       1  ''
              160  LOAD_CONST               None
              162  RAISE_VARARGS_2       2  'exception instance with __cause__'
              164  POP_EXCEPT       
              166  JUMP_FORWARD        170  'to 170'
              168  <48>             
            170_0  COME_FROM           166  '166'
            170_1  COME_FROM           132  '132'

 L. 240       170  LOAD_FAST                'fix_class'
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                options
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                fixer_log
              180  CALL_FUNCTION_2       2  ''
              182  STORE_FAST               'fixer'

 L. 241       184  LOAD_FAST                'fixer'
              186  LOAD_ATTR                explicit
              188  POP_JUMP_IF_FALSE   224  'to 224'
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                explicit
              194  LOAD_CONST               True
              196  <117>                 1  ''
              198  POP_JUMP_IF_FALSE   224  'to 224'

 L. 242       200  LOAD_FAST                'fix_mod_path'
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                explicit
              206  <118>                 1  ''

 L. 241       208  POP_JUMP_IF_FALSE   224  'to 224'

 L. 243       210  LOAD_FAST                'self'
              212  LOAD_METHOD              log_message
              214  LOAD_STR                 'Skipping optional fixer: %s'
              216  LOAD_FAST                'fix_name'
              218  CALL_METHOD_2         2  ''
              220  POP_TOP          

 L. 244       222  JUMP_BACK            14  'to 14'
            224_0  COME_FROM           208  '208'
            224_1  COME_FROM           198  '198'
            224_2  COME_FROM           188  '188'

 L. 246       224  LOAD_FAST                'self'
              226  LOAD_METHOD              log_debug
              228  LOAD_STR                 'Adding transformation: %s'
              230  LOAD_FAST                'fix_name'
              232  CALL_METHOD_2         2  ''
              234  POP_TOP          

 L. 247       236  LOAD_FAST                'fixer'
              238  LOAD_ATTR                order
              240  LOAD_STR                 'pre'
              242  COMPARE_OP               ==
          244_246  POP_JUMP_IF_FALSE   260  'to 260'

 L. 248       248  LOAD_FAST                'pre_order_fixers'
              250  LOAD_METHOD              append
              252  LOAD_FAST                'fixer'
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          
              258  JUMP_BACK            14  'to 14'
            260_0  COME_FROM           244  '244'

 L. 249       260  LOAD_FAST                'fixer'
              262  LOAD_ATTR                order
              264  LOAD_STR                 'post'
              266  COMPARE_OP               ==
          268_270  POP_JUMP_IF_FALSE   284  'to 284'

 L. 250       272  LOAD_FAST                'post_order_fixers'
              274  LOAD_METHOD              append
              276  LOAD_FAST                'fixer'
              278  CALL_METHOD_1         1  ''
              280  POP_TOP          
              282  JUMP_BACK            14  'to 14'
            284_0  COME_FROM           268  '268'

 L. 252       284  LOAD_GLOBAL              FixerError
              286  LOAD_STR                 'Illegal fixer order: %r'
              288  LOAD_FAST                'fixer'
              290  LOAD_ATTR                order
              292  BINARY_MODULO    
              294  CALL_FUNCTION_1       1  ''
              296  RAISE_VARARGS_1       1  'exception instance'
              298  JUMP_BACK            14  'to 14'
            300_0  COME_FROM            14  '14'

 L. 254       300  LOAD_GLOBAL              operator
              302  LOAD_METHOD              attrgetter
              304  LOAD_STR                 'run_order'
              306  CALL_METHOD_1         1  ''
              308  STORE_FAST               'key_func'

 L. 255       310  LOAD_FAST                'pre_order_fixers'
              312  LOAD_ATTR                sort
              314  LOAD_FAST                'key_func'
              316  LOAD_CONST               ('key',)
              318  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              320  POP_TOP          

 L. 256       322  LOAD_FAST                'post_order_fixers'
              324  LOAD_ATTR                sort
              326  LOAD_FAST                'key_func'
              328  LOAD_CONST               ('key',)
              330  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              332  POP_TOP          

 L. 257       334  LOAD_FAST                'pre_order_fixers'
              336  LOAD_FAST                'post_order_fixers'
              338  BUILD_TUPLE_2         2 
              340  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 138

    def log_error(self, msg, *args, **kwds):
        """Called when an error occurs."""
        raise

    def log_message(self, msg, *args):
        """Hook to log a message."""
        if args:
            msg = msg % args
        self.logger.info(msg)

    def log_debug(self, msg, *args):
        if args:
            msg = msg % args
        self.logger.debug(msg)

    def print_output(self, old_text, new_text, filename, equal):
        """Called with the old version, new version, and filename of a
        refactored file."""
        pass

    def refactor(self, items, write=False, doctests_only=False):
        """Refactor a list of files and directories."""
        for dir_or_file in items:
            if os.path.isdir(dir_or_file):
                self.refactor_dir(dir_or_file, write, doctests_only)
            else:
                self.refactor_file(dir_or_file, write, doctests_only)

    def refactor_dir(self, dir_name, write=False, doctests_only=False):
        """Descends down a directory and refactor every Python file found.

        Python files are assumed to have a .py extension.

        Files and subdirectories starting with '.' are skipped.
        """
        py_ext = os.extsep + 'py'
        for dirpath, dirnames, filenames in os.walk(dir_name):
            self.log_debug'Descending into %s'dirpath
            dirnames.sort
            filenames.sort
            for name in filenames:
                if not name.startswith('.'):
                    if os.path.splitext(name)[1] == py_ext:
                        fullname = os.path.joindirpathname
                        self.refactor_file(fullname, write, doctests_only)
                    dirnames[:] = [dn for dn in dirnames if not dn.startswith('.')]

    def _read_python_source--- This code section failed: ---

 L. 312         0  SETUP_FINALLY        16  'to 16'

 L. 313         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'filename'
                6  LOAD_STR                 'rb'
                8  CALL_FUNCTION_2       2  ''
               10  STORE_FAST               'f'
               12  POP_BLOCK        
               14  JUMP_FORWARD         68  'to 68'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 314        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  <121>                66  ''
               22  POP_TOP          
               24  STORE_FAST               'err'
               26  POP_TOP          
               28  SETUP_FINALLY        58  'to 58'

 L. 315        30  LOAD_FAST                'self'
               32  LOAD_METHOD              log_error
               34  LOAD_STR                 "Can't open %s: %s"
               36  LOAD_FAST                'filename'
               38  LOAD_FAST                'err'
               40  CALL_METHOD_3         3  ''
               42  POP_TOP          

 L. 316        44  POP_BLOCK        
               46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  STORE_FAST               'err'
               52  DELETE_FAST              'err'
               54  LOAD_CONST               (None, None)
               56  RETURN_VALUE     
             58_0  COME_FROM_FINALLY    28  '28'
               58  LOAD_CONST               None
               60  STORE_FAST               'err'
               62  DELETE_FAST              'err'
               64  <48>             
               66  <48>             
             68_0  COME_FROM            14  '14'

 L. 317        68  SETUP_FINALLY        98  'to 98'

 L. 318        70  LOAD_GLOBAL              tokenize
               72  LOAD_METHOD              detect_encoding
               74  LOAD_FAST                'f'
               76  LOAD_ATTR                readline
               78  CALL_METHOD_1         1  ''
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  STORE_FAST               'encoding'
               86  POP_BLOCK        

 L. 320        88  LOAD_FAST                'f'
               90  LOAD_METHOD              close
               92  CALL_METHOD_0         0  ''
               94  POP_TOP          
               96  JUMP_FORWARD        108  'to 108'
             98_0  COME_FROM_FINALLY    68  '68'
               98  LOAD_FAST                'f'
              100  LOAD_METHOD              close
              102  CALL_METHOD_0         0  ''
              104  POP_TOP          
              106  <48>             
            108_0  COME_FROM            96  '96'

 L. 321       108  LOAD_GLOBAL              io
              110  LOAD_ATTR                open
              112  LOAD_FAST                'filename'
              114  LOAD_STR                 'r'
              116  LOAD_FAST                'encoding'
              118  LOAD_STR                 ''
              120  LOAD_CONST               ('encoding', 'newline')
              122  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              124  SETUP_WITH          154  'to 154'
              126  STORE_FAST               'f'

 L. 322       128  LOAD_FAST                'f'
              130  LOAD_METHOD              read
              132  CALL_METHOD_0         0  ''
              134  LOAD_FAST                'encoding'
              136  BUILD_TUPLE_2         2 
              138  POP_BLOCK        
              140  ROT_TWO          
              142  LOAD_CONST               None
              144  DUP_TOP          
              146  DUP_TOP          
              148  CALL_FUNCTION_3       3  ''
              150  POP_TOP          
              152  RETURN_VALUE     
            154_0  COME_FROM_WITH      124  '124'
              154  <49>             
              156  POP_JUMP_IF_TRUE    160  'to 160'
              158  <48>             
            160_0  COME_FROM           156  '156'
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          
              166  POP_EXCEPT       
              168  POP_TOP          

Parse error at or near `<121>' instruction at offset 20

    def refactor_file--- This code section failed: ---

 L. 326         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _read_python_source
                4  LOAD_FAST                'filename'
                6  CALL_METHOD_1         1  ''
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'input'
               12  STORE_FAST               'encoding'

 L. 327        14  LOAD_FAST                'input'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 329        22  LOAD_CONST               None
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 330        26  LOAD_FAST                'input'
               28  LOAD_STR                 '\n'
               30  INPLACE_ADD      
               32  STORE_FAST               'input'

 L. 331        34  LOAD_FAST                'doctests_only'
               36  POP_JUMP_IF_FALSE   110  'to 110'

 L. 332        38  LOAD_FAST                'self'
               40  LOAD_METHOD              log_debug
               42  LOAD_STR                 'Refactoring doctests in %s'
               44  LOAD_FAST                'filename'
               46  CALL_METHOD_2         2  ''
               48  POP_TOP          

 L. 333        50  LOAD_FAST                'self'
               52  LOAD_METHOD              refactor_docstring
               54  LOAD_FAST                'input'
               56  LOAD_FAST                'filename'
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'output'

 L. 334        62  LOAD_FAST                'self'
               64  LOAD_ATTR                write_unchanged_files
               66  POP_JUMP_IF_TRUE     76  'to 76'
               68  LOAD_FAST                'output'
               70  LOAD_FAST                'input'
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_FALSE    96  'to 96'
             76_0  COME_FROM            66  '66'

 L. 335        76  LOAD_FAST                'self'
               78  LOAD_METHOD              processed_file
               80  LOAD_FAST                'output'
               82  LOAD_FAST                'filename'
               84  LOAD_FAST                'input'
               86  LOAD_FAST                'write'
               88  LOAD_FAST                'encoding'
               90  CALL_METHOD_5         5  ''
               92  POP_TOP          
               94  JUMP_FORWARD        182  'to 182'
             96_0  COME_FROM            74  '74'

 L. 337        96  LOAD_FAST                'self'
               98  LOAD_METHOD              log_debug
              100  LOAD_STR                 'No doctest changes in %s'
              102  LOAD_FAST                'filename'
              104  CALL_METHOD_2         2  ''
              106  POP_TOP          
              108  JUMP_FORWARD        182  'to 182'
            110_0  COME_FROM            36  '36'

 L. 339       110  LOAD_FAST                'self'
              112  LOAD_METHOD              refactor_string
              114  LOAD_FAST                'input'
              116  LOAD_FAST                'filename'
              118  CALL_METHOD_2         2  ''
              120  STORE_FAST               'tree'

 L. 340       122  LOAD_FAST                'self'
              124  LOAD_ATTR                write_unchanged_files
              126  POP_JUMP_IF_TRUE    138  'to 138'
              128  LOAD_FAST                'tree'
              130  POP_JUMP_IF_FALSE   170  'to 170'
              132  LOAD_FAST                'tree'
              134  LOAD_ATTR                was_changed
              136  POP_JUMP_IF_FALSE   170  'to 170'
            138_0  COME_FROM           126  '126'

 L. 342       138  LOAD_FAST                'self'
              140  LOAD_ATTR                processed_file
              142  LOAD_GLOBAL              str
              144  LOAD_FAST                'tree'
              146  CALL_FUNCTION_1       1  ''
              148  LOAD_CONST               None
              150  LOAD_CONST               -1
              152  BUILD_SLICE_2         2 
              154  BINARY_SUBSCR    
              156  LOAD_FAST                'filename'

 L. 343       158  LOAD_FAST                'write'
              160  LOAD_FAST                'encoding'

 L. 342       162  LOAD_CONST               ('write', 'encoding')
              164  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              166  POP_TOP          
              168  JUMP_FORWARD        182  'to 182'
            170_0  COME_FROM           136  '136'
            170_1  COME_FROM           130  '130'

 L. 345       170  LOAD_FAST                'self'
              172  LOAD_METHOD              log_debug
              174  LOAD_STR                 'No changes in %s'
              176  LOAD_FAST                'filename'
              178  CALL_METHOD_2         2  ''
              180  POP_TOP          
            182_0  COME_FROM           168  '168'
            182_1  COME_FROM           108  '108'
            182_2  COME_FROM            94  '94'

Parse error at or near `<117>' instruction at offset 18

    def refactor_string--- This code section failed: ---

 L. 358         0  LOAD_GLOBAL              _detect_future_features
                2  LOAD_FAST                'data'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'features'

 L. 359         8  LOAD_STR                 'print_function'
               10  LOAD_FAST                'features'
               12  <118>                 0  ''
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 360        16  LOAD_GLOBAL              pygram
               18  LOAD_ATTR                python_grammar_no_print_statement
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                driver
               24  STORE_ATTR               grammar
             26_0  COME_FROM            14  '14'

 L. 361        26  SETUP_FINALLY       130  'to 130'
               28  SETUP_FINALLY        46  'to 46'

 L. 362        30  LOAD_FAST                'self'
               32  LOAD_ATTR                driver
               34  LOAD_METHOD              parse_string
               36  LOAD_FAST                'data'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'tree'
               42  POP_BLOCK        
               44  JUMP_FORWARD        116  'to 116'
             46_0  COME_FROM_FINALLY    28  '28'

 L. 363        46  DUP_TOP          
               48  LOAD_GLOBAL              Exception
               50  <121>               114  ''
               52  POP_TOP          
               54  STORE_FAST               'err'
               56  POP_TOP          
               58  SETUP_FINALLY       106  'to 106'

 L. 364        60  LOAD_FAST                'self'
               62  LOAD_METHOD              log_error
               64  LOAD_STR                 "Can't parse %s: %s: %s"

 L. 365        66  LOAD_FAST                'name'
               68  LOAD_FAST                'err'
               70  LOAD_ATTR                __class__
               72  LOAD_ATTR                __name__
               74  LOAD_FAST                'err'

 L. 364        76  CALL_METHOD_4         4  ''
               78  POP_TOP          

 L. 366        80  POP_BLOCK        
               82  POP_EXCEPT       
               84  LOAD_CONST               None
               86  STORE_FAST               'err'
               88  DELETE_FAST              'err'
               90  POP_BLOCK        

 L. 368        92  LOAD_FAST                'self'
               94  LOAD_ATTR                grammar
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                driver
              100  STORE_ATTR               grammar

 L. 366       102  LOAD_CONST               None
              104  RETURN_VALUE     
            106_0  COME_FROM_FINALLY    58  '58'
              106  LOAD_CONST               None
              108  STORE_FAST               'err'
              110  DELETE_FAST              'err'
              112  <48>             
              114  <48>             
            116_0  COME_FROM            44  '44'
              116  POP_BLOCK        

 L. 368       118  LOAD_FAST                'self'
              120  LOAD_ATTR                grammar
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                driver
              126  STORE_ATTR               grammar
              128  JUMP_FORWARD        142  'to 142'
            130_0  COME_FROM_FINALLY    26  '26'
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                grammar
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                driver
              138  STORE_ATTR               grammar
              140  <48>             
            142_0  COME_FROM           128  '128'

 L. 369       142  LOAD_FAST                'features'
              144  LOAD_FAST                'tree'
              146  STORE_ATTR               future_features

 L. 370       148  LOAD_FAST                'self'
              150  LOAD_METHOD              log_debug
              152  LOAD_STR                 'Refactoring %s'
              154  LOAD_FAST                'name'
              156  CALL_METHOD_2         2  ''
              158  POP_TOP          

 L. 371       160  LOAD_FAST                'self'
              162  LOAD_METHOD              refactor_tree
              164  LOAD_FAST                'tree'
              166  LOAD_FAST                'name'
              168  CALL_METHOD_2         2  ''
              170  POP_TOP          

 L. 372       172  LOAD_FAST                'tree'
              174  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 12

    def refactor_stdin--- This code section failed: ---

 L. 375         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                stdin
                4  LOAD_METHOD              read
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'input'

 L. 376        10  LOAD_FAST                'doctests_only'
               12  POP_JUMP_IF_FALSE    78  'to 78'

 L. 377        14  LOAD_FAST                'self'
               16  LOAD_METHOD              log_debug
               18  LOAD_STR                 'Refactoring doctests in stdin'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L. 378        24  LOAD_FAST                'self'
               26  LOAD_METHOD              refactor_docstring
               28  LOAD_FAST                'input'
               30  LOAD_STR                 '<stdin>'
               32  CALL_METHOD_2         2  ''
               34  STORE_FAST               'output'

 L. 379        36  LOAD_FAST                'self'
               38  LOAD_ATTR                write_unchanged_files
               40  POP_JUMP_IF_TRUE     50  'to 50'
               42  LOAD_FAST                'output'
               44  LOAD_FAST                'input'
               46  COMPARE_OP               !=
               48  POP_JUMP_IF_FALSE    66  'to 66'
             50_0  COME_FROM            40  '40'

 L. 380        50  LOAD_FAST                'self'
               52  LOAD_METHOD              processed_file
               54  LOAD_FAST                'output'
               56  LOAD_STR                 '<stdin>'
               58  LOAD_FAST                'input'
               60  CALL_METHOD_3         3  ''
               62  POP_TOP          
               64  JUMP_FORWARD        136  'to 136'
             66_0  COME_FROM            48  '48'

 L. 382        66  LOAD_FAST                'self'
               68  LOAD_METHOD              log_debug
               70  LOAD_STR                 'No doctest changes in stdin'
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          
               76  JUMP_FORWARD        136  'to 136'
             78_0  COME_FROM            12  '12'

 L. 384        78  LOAD_FAST                'self'
               80  LOAD_METHOD              refactor_string
               82  LOAD_FAST                'input'
               84  LOAD_STR                 '<stdin>'
               86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'tree'

 L. 385        90  LOAD_FAST                'self'
               92  LOAD_ATTR                write_unchanged_files
               94  POP_JUMP_IF_TRUE    106  'to 106'
               96  LOAD_FAST                'tree'
               98  POP_JUMP_IF_FALSE   126  'to 126'
              100  LOAD_FAST                'tree'
              102  LOAD_ATTR                was_changed
              104  POP_JUMP_IF_FALSE   126  'to 126'
            106_0  COME_FROM            94  '94'

 L. 386       106  LOAD_FAST                'self'
              108  LOAD_METHOD              processed_file
              110  LOAD_GLOBAL              str
              112  LOAD_FAST                'tree'
              114  CALL_FUNCTION_1       1  ''
              116  LOAD_STR                 '<stdin>'
              118  LOAD_FAST                'input'
              120  CALL_METHOD_3         3  ''
              122  POP_TOP          
              124  JUMP_FORWARD        136  'to 136'
            126_0  COME_FROM           104  '104'
            126_1  COME_FROM            98  '98'

 L. 388       126  LOAD_FAST                'self'
              128  LOAD_METHOD              log_debug
              130  LOAD_STR                 'No changes in stdin'
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
            136_0  COME_FROM           124  '124'
            136_1  COME_FROM            76  '76'
            136_2  COME_FROM            64  '64'

Parse error at or near `COME_FROM' instruction at offset 136_1

    def refactor_tree--- This code section failed: ---

 L. 406         0  LOAD_GLOBAL              chain
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                pre_order
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                post_order
               10  CALL_FUNCTION_2       2  ''
               12  GET_ITER         
             14_0  COME_FROM            30  '30'
               14  FOR_ITER             32  'to 32'
               16  STORE_FAST               'fixer'

 L. 407        18  LOAD_FAST                'fixer'
               20  LOAD_METHOD              start_tree
               22  LOAD_FAST                'tree'
               24  LOAD_FAST                'name'
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          
               30  JUMP_BACK            14  'to 14'
             32_0  COME_FROM            14  '14'

 L. 410        32  LOAD_FAST                'self'
               34  LOAD_METHOD              traverse_by
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                bmi_pre_order_heads
               40  LOAD_FAST                'tree'
               42  LOAD_METHOD              pre_order
               44  CALL_METHOD_0         0  ''
               46  CALL_METHOD_2         2  ''
               48  POP_TOP          

 L. 411        50  LOAD_FAST                'self'
               52  LOAD_METHOD              traverse_by
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                bmi_post_order_heads
               58  LOAD_FAST                'tree'
               60  LOAD_METHOD              post_order
               62  CALL_METHOD_0         0  ''
               64  CALL_METHOD_2         2  ''
               66  POP_TOP          

 L. 414        68  LOAD_FAST                'self'
               70  LOAD_ATTR                BM
               72  LOAD_METHOD              run
               74  LOAD_FAST                'tree'
               76  LOAD_METHOD              leaves
               78  CALL_METHOD_0         0  ''
               80  CALL_METHOD_1         1  ''
               82  STORE_FAST               'match_set'
             84_0  COME_FROM           432  '432'

 L. 416        84  LOAD_GLOBAL              any
               86  LOAD_FAST                'match_set'
               88  LOAD_METHOD              values
               90  CALL_METHOD_0         0  ''
               92  CALL_FUNCTION_1       1  ''
            94_96  POP_JUMP_IF_FALSE   434  'to 434'

 L. 417        98  LOAD_FAST                'self'
              100  LOAD_ATTR                BM
              102  LOAD_ATTR                fixers
              104  GET_ITER         
            106_0  COME_FROM           430  '430'
            106_1  COME_FROM           126  '126'
            106_2  COME_FROM           118  '118'
          106_108  FOR_ITER            432  'to 432'
              110  STORE_FAST               'fixer'

 L. 418       112  LOAD_FAST                'fixer'
              114  LOAD_FAST                'match_set'
              116  <118>                 0  ''
              118  POP_JUMP_IF_FALSE_BACK   106  'to 106'
              120  LOAD_FAST                'match_set'
              122  LOAD_FAST                'fixer'
              124  BINARY_SUBSCR    
              126  POP_JUMP_IF_FALSE_BACK   106  'to 106'

 L. 420       128  LOAD_FAST                'match_set'
              130  LOAD_FAST                'fixer'
              132  BINARY_SUBSCR    
              134  LOAD_ATTR                sort
              136  LOAD_GLOBAL              pytree
              138  LOAD_ATTR                Base
              140  LOAD_ATTR                depth
              142  LOAD_CONST               True
              144  LOAD_CONST               ('key', 'reverse')
              146  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              148  POP_TOP          

 L. 422       150  LOAD_FAST                'fixer'
              152  LOAD_ATTR                keep_line_order
              154  POP_JUMP_IF_FALSE   176  'to 176'

 L. 425       156  LOAD_FAST                'match_set'
              158  LOAD_FAST                'fixer'
              160  BINARY_SUBSCR    
              162  LOAD_ATTR                sort
              164  LOAD_GLOBAL              pytree
              166  LOAD_ATTR                Base
              168  LOAD_ATTR                get_lineno
              170  LOAD_CONST               ('key',)
              172  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              174  POP_TOP          
            176_0  COME_FROM           154  '154'

 L. 427       176  LOAD_GLOBAL              list
              178  LOAD_FAST                'match_set'
              180  LOAD_FAST                'fixer'
              182  BINARY_SUBSCR    
              184  CALL_FUNCTION_1       1  ''
              186  GET_ITER         
            188_0  COME_FROM           428  '428'
            188_1  COME_FROM           310  '310'
            188_2  COME_FROM           290  '290'
            188_3  COME_FROM           276  '276'
            188_4  COME_FROM           248  '248'
              188  FOR_ITER            430  'to 430'
              190  STORE_FAST               'node'

 L. 428       192  LOAD_FAST                'node'
              194  LOAD_FAST                'match_set'
              196  LOAD_FAST                'fixer'
              198  BINARY_SUBSCR    
              200  <118>                 0  ''
              202  POP_JUMP_IF_FALSE   218  'to 218'

 L. 429       204  LOAD_FAST                'match_set'
              206  LOAD_FAST                'fixer'
              208  BINARY_SUBSCR    
              210  LOAD_METHOD              remove
              212  LOAD_FAST                'node'
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
            218_0  COME_FROM           202  '202'

 L. 431       218  SETUP_FINALLY       232  'to 232'

 L. 432       220  LOAD_GLOBAL              find_root
              222  LOAD_FAST                'node'
              224  CALL_FUNCTION_1       1  ''
              226  POP_TOP          
              228  POP_BLOCK        
              230  JUMP_FORWARD        256  'to 256'
            232_0  COME_FROM_FINALLY   218  '218'

 L. 433       232  DUP_TOP          
              234  LOAD_GLOBAL              ValueError
          236_238  <121>               254  ''
              240  POP_TOP          
              242  POP_TOP          
              244  POP_TOP          

 L. 436       246  POP_EXCEPT       
              248  JUMP_BACK           188  'to 188'
              250  POP_EXCEPT       
              252  JUMP_FORWARD        256  'to 256'
              254  <48>             
            256_0  COME_FROM           252  '252'
            256_1  COME_FROM           230  '230'

 L. 438       256  LOAD_FAST                'node'
              258  LOAD_ATTR                fixers_applied
          260_262  POP_JUMP_IF_FALSE   278  'to 278'
              264  LOAD_FAST                'fixer'
              266  LOAD_FAST                'node'
              268  LOAD_ATTR                fixers_applied
              270  <118>                 0  ''
          272_274  POP_JUMP_IF_FALSE   278  'to 278'

 L. 440       276  JUMP_BACK           188  'to 188'
            278_0  COME_FROM           272  '272'
            278_1  COME_FROM           260  '260'

 L. 442       278  LOAD_FAST                'fixer'
              280  LOAD_METHOD              match
              282  LOAD_FAST                'node'
              284  CALL_METHOD_1         1  ''
              286  STORE_FAST               'results'

 L. 444       288  LOAD_FAST                'results'
              290  POP_JUMP_IF_FALSE_BACK   188  'to 188'

 L. 445       292  LOAD_FAST                'fixer'
              294  LOAD_METHOD              transform
              296  LOAD_FAST                'node'
              298  LOAD_FAST                'results'
              300  CALL_METHOD_2         2  ''
              302  STORE_FAST               'new'

 L. 446       304  LOAD_FAST                'new'
              306  LOAD_CONST               None
              308  <117>                 1  ''
              310  POP_JUMP_IF_FALSE_BACK   188  'to 188'

 L. 447       312  LOAD_FAST                'node'
              314  LOAD_METHOD              replace
              316  LOAD_FAST                'new'
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          

 L. 449       322  LOAD_FAST                'new'
              324  LOAD_METHOD              post_order
              326  CALL_METHOD_0         0  ''
              328  GET_ITER         
            330_0  COME_FROM           360  '360'
              330  FOR_ITER            364  'to 364'
              332  STORE_FAST               'node'

 L. 452       334  LOAD_FAST                'node'
              336  LOAD_ATTR                fixers_applied
          338_340  POP_JUMP_IF_TRUE    348  'to 348'

 L. 453       342  BUILD_LIST_0          0 
              344  LOAD_FAST                'node'
              346  STORE_ATTR               fixers_applied
            348_0  COME_FROM           338  '338'

 L. 454       348  LOAD_FAST                'node'
              350  LOAD_ATTR                fixers_applied
              352  LOAD_METHOD              append
              354  LOAD_FAST                'fixer'
              356  CALL_METHOD_1         1  ''
              358  POP_TOP          
          360_362  JUMP_BACK           330  'to 330'
            364_0  COME_FROM           330  '330'

 L. 458       364  LOAD_FAST                'self'
              366  LOAD_ATTR                BM
              368  LOAD_METHOD              run
              370  LOAD_FAST                'new'
              372  LOAD_METHOD              leaves
              374  CALL_METHOD_0         0  ''
              376  CALL_METHOD_1         1  ''
              378  STORE_FAST               'new_matches'

 L. 459       380  LOAD_FAST                'new_matches'
              382  GET_ITER         
            384_0  COME_FROM           424  '424'
              384  FOR_ITER            428  'to 428'
              386  STORE_FAST               'fxr'

 L. 460       388  LOAD_FAST                'fxr'
              390  LOAD_FAST                'match_set'
              392  <118>                 1  ''
          394_396  POP_JUMP_IF_FALSE   406  'to 406'

 L. 461       398  BUILD_LIST_0          0 
              400  LOAD_FAST                'match_set'
              402  LOAD_FAST                'fxr'
              404  STORE_SUBSCR     
            406_0  COME_FROM           394  '394'

 L. 463       406  LOAD_FAST                'match_set'
              408  LOAD_FAST                'fxr'
              410  BINARY_SUBSCR    
              412  LOAD_METHOD              extend
              414  LOAD_FAST                'new_matches'
              416  LOAD_FAST                'fxr'
              418  BINARY_SUBSCR    
              420  CALL_METHOD_1         1  ''
              422  POP_TOP          
          424_426  JUMP_BACK           384  'to 384'
            428_0  COME_FROM           384  '384'
              428  JUMP_BACK           188  'to 188'
            430_0  COME_FROM           188  '188'
              430  JUMP_BACK           106  'to 106'
            432_0  COME_FROM           106  '106'
              432  JUMP_BACK            84  'to 84'
            434_0  COME_FROM            94  '94'

 L. 465       434  LOAD_GLOBAL              chain
              436  LOAD_FAST                'self'
              438  LOAD_ATTR                pre_order
              440  LOAD_FAST                'self'
              442  LOAD_ATTR                post_order
              444  CALL_FUNCTION_2       2  ''
              446  GET_ITER         
            448_0  COME_FROM           464  '464'
              448  FOR_ITER            468  'to 468'
              450  STORE_FAST               'fixer'

 L. 466       452  LOAD_FAST                'fixer'
              454  LOAD_METHOD              finish_tree
              456  LOAD_FAST                'tree'
              458  LOAD_FAST                'name'
              460  CALL_METHOD_2         2  ''
              462  POP_TOP          
          464_466  JUMP_BACK           448  'to 448'
            468_0  COME_FROM           448  '448'

 L. 467       468  LOAD_FAST                'tree'
              470  LOAD_ATTR                was_changed
              472  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 116

    def traverse_by--- This code section failed: ---

 L. 481         0  LOAD_FAST                'fixers'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 482         4  LOAD_CONST               None
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 483         8  LOAD_FAST                'traversal'
               10  GET_ITER         
             12_0  COME_FROM            80  '80'
               12  FOR_ITER             82  'to 82'
               14  STORE_FAST               'node'

 L. 484        16  LOAD_FAST                'fixers'
               18  LOAD_FAST                'node'
               20  LOAD_ATTR                type
               22  BINARY_SUBSCR    
               24  GET_ITER         
             26_0  COME_FROM            78  '78'
             26_1  COME_FROM            62  '62'
             26_2  COME_FROM            42  '42'
               26  FOR_ITER             80  'to 80'
               28  STORE_FAST               'fixer'

 L. 485        30  LOAD_FAST                'fixer'
               32  LOAD_METHOD              match
               34  LOAD_FAST                'node'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'results'

 L. 486        40  LOAD_FAST                'results'
               42  POP_JUMP_IF_FALSE_BACK    26  'to 26'

 L. 487        44  LOAD_FAST                'fixer'
               46  LOAD_METHOD              transform
               48  LOAD_FAST                'node'
               50  LOAD_FAST                'results'
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'new'

 L. 488        56  LOAD_FAST                'new'
               58  LOAD_CONST               None
               60  <117>                 1  ''
               62  POP_JUMP_IF_FALSE_BACK    26  'to 26'

 L. 489        64  LOAD_FAST                'node'
               66  LOAD_METHOD              replace
               68  LOAD_FAST                'new'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          

 L. 490        74  LOAD_FAST                'new'
               76  STORE_FAST               'node'
               78  JUMP_BACK            26  'to 26'
             80_0  COME_FROM            26  '26'
               80  JUMP_BACK            12  'to 12'
             82_0  COME_FROM            12  '12'

Parse error at or near `<117>' instruction at offset 60

    def processed_file--- This code section failed: ---

 L. 497         0  LOAD_FAST                'self'
                2  LOAD_ATTR                files
                4  LOAD_METHOD              append
                6  LOAD_FAST                'filename'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 498        12  LOAD_FAST                'old_text'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    46  'to 46'

 L. 499        20  LOAD_FAST                'self'
               22  LOAD_METHOD              _read_python_source
               24  LOAD_FAST                'filename'
               26  CALL_METHOD_1         1  ''
               28  LOAD_CONST               0
               30  BINARY_SUBSCR    
               32  STORE_FAST               'old_text'

 L. 500        34  LOAD_FAST                'old_text'
               36  LOAD_CONST               None
               38  <117>                 0  ''
               40  POP_JUMP_IF_FALSE    46  'to 46'

 L. 501        42  LOAD_CONST               None
               44  RETURN_VALUE     
             46_0  COME_FROM            40  '40'
             46_1  COME_FROM            18  '18'

 L. 502        46  LOAD_FAST                'old_text'
               48  LOAD_FAST                'new_text'
               50  COMPARE_OP               ==
               52  STORE_FAST               'equal'

 L. 503        54  LOAD_FAST                'self'
               56  LOAD_METHOD              print_output
               58  LOAD_FAST                'old_text'
               60  LOAD_FAST                'new_text'
               62  LOAD_FAST                'filename'
               64  LOAD_FAST                'equal'
               66  CALL_METHOD_4         4  ''
               68  POP_TOP          

 L. 504        70  LOAD_FAST                'equal'
               72  POP_JUMP_IF_FALSE    96  'to 96'

 L. 505        74  LOAD_FAST                'self'
               76  LOAD_METHOD              log_debug
               78  LOAD_STR                 'No changes to %s'
               80  LOAD_FAST                'filename'
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L. 506        86  LOAD_FAST                'self'
               88  LOAD_ATTR                write_unchanged_files
               90  POP_JUMP_IF_TRUE     96  'to 96'

 L. 507        92  LOAD_CONST               None
               94  RETURN_VALUE     
             96_0  COME_FROM            90  '90'
             96_1  COME_FROM            72  '72'

 L. 508        96  LOAD_FAST                'write'
               98  POP_JUMP_IF_FALSE   118  'to 118'

 L. 509       100  LOAD_FAST                'self'
              102  LOAD_METHOD              write_file
              104  LOAD_FAST                'new_text'
              106  LOAD_FAST                'filename'
              108  LOAD_FAST                'old_text'
              110  LOAD_FAST                'encoding'
              112  CALL_METHOD_4         4  ''
              114  POP_TOP          
              116  JUMP_FORWARD        130  'to 130'
            118_0  COME_FROM            98  '98'

 L. 511       118  LOAD_FAST                'self'
              120  LOAD_METHOD              log_debug
              122  LOAD_STR                 'Not writing changes to %s'
              124  LOAD_FAST                'filename'
              126  CALL_METHOD_2         2  ''
              128  POP_TOP          
            130_0  COME_FROM           116  '116'

Parse error at or near `<117>' instruction at offset 16

    def write_file--- This code section failed: ---

 L. 520         0  SETUP_FINALLY        24  'to 24'

 L. 521         2  LOAD_GLOBAL              io
                4  LOAD_ATTR                open
                6  LOAD_FAST                'filename'
                8  LOAD_STR                 'w'
               10  LOAD_FAST                'encoding'
               12  LOAD_STR                 ''
               14  LOAD_CONST               ('encoding', 'newline')
               16  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               18  STORE_FAST               'fp'
               20  POP_BLOCK        
               22  JUMP_FORWARD         76  'to 76'
             24_0  COME_FROM_FINALLY     0  '0'

 L. 522        24  DUP_TOP          
               26  LOAD_GLOBAL              OSError
               28  <121>                74  ''
               30  POP_TOP          
               32  STORE_FAST               'err'
               34  POP_TOP          
               36  SETUP_FINALLY        66  'to 66'

 L. 523        38  LOAD_FAST                'self'
               40  LOAD_METHOD              log_error
               42  LOAD_STR                 "Can't create %s: %s"
               44  LOAD_FAST                'filename'
               46  LOAD_FAST                'err'
               48  CALL_METHOD_3         3  ''
               50  POP_TOP          

 L. 524        52  POP_BLOCK        
               54  POP_EXCEPT       
               56  LOAD_CONST               None
               58  STORE_FAST               'err'
               60  DELETE_FAST              'err'
               62  LOAD_CONST               None
               64  RETURN_VALUE     
             66_0  COME_FROM_FINALLY    36  '36'
               66  LOAD_CONST               None
               68  STORE_FAST               'err'
               70  DELETE_FAST              'err'
               72  <48>             
               74  <48>             
             76_0  COME_FROM            22  '22'

 L. 526        76  LOAD_FAST                'fp'
               78  SETUP_WITH          162  'to 162'
               80  POP_TOP          

 L. 527        82  SETUP_FINALLY        98  'to 98'

 L. 528        84  LOAD_FAST                'fp'
               86  LOAD_METHOD              write
               88  LOAD_FAST                'new_text'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          
               94  POP_BLOCK        
               96  JUMP_FORWARD        148  'to 148'
             98_0  COME_FROM_FINALLY    82  '82'

 L. 529        98  DUP_TOP          
              100  LOAD_GLOBAL              OSError
              102  <121>               146  ''
              104  POP_TOP          
              106  STORE_FAST               'err'
              108  POP_TOP          
              110  SETUP_FINALLY       138  'to 138'

 L. 530       112  LOAD_FAST                'self'
              114  LOAD_METHOD              log_error
              116  LOAD_STR                 "Can't write %s: %s"
              118  LOAD_FAST                'filename'
              120  LOAD_FAST                'err'
              122  CALL_METHOD_3         3  ''
              124  POP_TOP          
              126  POP_BLOCK        
              128  POP_EXCEPT       
              130  LOAD_CONST               None
              132  STORE_FAST               'err'
              134  DELETE_FAST              'err'
              136  JUMP_FORWARD        148  'to 148'
            138_0  COME_FROM_FINALLY   110  '110'
              138  LOAD_CONST               None
              140  STORE_FAST               'err'
              142  DELETE_FAST              'err'
              144  <48>             
              146  <48>             
            148_0  COME_FROM           136  '136'
            148_1  COME_FROM            96  '96'
              148  POP_BLOCK        
              150  LOAD_CONST               None
              152  DUP_TOP          
              154  DUP_TOP          
              156  CALL_FUNCTION_3       3  ''
              158  POP_TOP          
              160  JUMP_FORWARD        178  'to 178'
            162_0  COME_FROM_WITH       78  '78'
              162  <49>             
              164  POP_JUMP_IF_TRUE    168  'to 168'
              166  <48>             
            168_0  COME_FROM           164  '164'
              168  POP_TOP          
              170  POP_TOP          
              172  POP_TOP          
              174  POP_EXCEPT       
              176  POP_TOP          
            178_0  COME_FROM           160  '160'

 L. 531       178  LOAD_FAST                'self'
              180  LOAD_METHOD              log_debug
              182  LOAD_STR                 'Wrote changes to %s'
              184  LOAD_FAST                'filename'
              186  CALL_METHOD_2         2  ''
              188  POP_TOP          

 L. 532       190  LOAD_CONST               True
              192  LOAD_FAST                'self'
              194  STORE_ATTR               wrote

Parse error at or near `<121>' instruction at offset 28

    PS1 = '>>> '
    PS2 = '... '

    def refactor_docstring--- This code section failed: ---

 L. 549         0  BUILD_LIST_0          0 
                2  STORE_FAST               'result'

 L. 550         4  LOAD_CONST               None
                6  STORE_FAST               'block'

 L. 551         8  LOAD_CONST               None
               10  STORE_FAST               'block_lineno'

 L. 552        12  LOAD_CONST               None
               14  STORE_FAST               'indent'

 L. 553        16  LOAD_CONST               0
               18  STORE_FAST               'lineno'

 L. 554        20  LOAD_FAST                'input'
               22  LOAD_ATTR                splitlines
               24  LOAD_CONST               True
               26  LOAD_CONST               ('keepends',)
               28  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               30  GET_ITER         
             32_0  COME_FROM           232  '232'
             32_1  COME_FROM           182  '182'
             32_2  COME_FROM           124  '124'
               32  FOR_ITER            234  'to 234'
               34  STORE_FAST               'line'

 L. 555        36  LOAD_FAST                'lineno'
               38  LOAD_CONST               1
               40  INPLACE_ADD      
               42  STORE_FAST               'lineno'

 L. 556        44  LOAD_FAST                'line'
               46  LOAD_METHOD              lstrip
               48  CALL_METHOD_0         0  ''
               50  LOAD_METHOD              startswith
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                PS1
               56  CALL_METHOD_1         1  ''
               58  POP_JUMP_IF_FALSE   126  'to 126'

 L. 557        60  LOAD_FAST                'block'
               62  LOAD_CONST               None
               64  <117>                 1  ''
               66  POP_JUMP_IF_FALSE    90  'to 90'

 L. 558        68  LOAD_FAST                'result'
               70  LOAD_METHOD              extend
               72  LOAD_FAST                'self'
               74  LOAD_METHOD              refactor_doctest
               76  LOAD_FAST                'block'
               78  LOAD_FAST                'block_lineno'

 L. 559        80  LOAD_FAST                'indent'
               82  LOAD_FAST                'filename'

 L. 558        84  CALL_METHOD_4         4  ''
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
             90_0  COME_FROM            66  '66'

 L. 560        90  LOAD_FAST                'lineno'
               92  STORE_FAST               'block_lineno'

 L. 561        94  LOAD_FAST                'line'
               96  BUILD_LIST_1          1 
               98  STORE_FAST               'block'

 L. 562       100  LOAD_FAST                'line'
              102  LOAD_METHOD              find
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                PS1
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'i'

 L. 563       112  LOAD_FAST                'line'
              114  LOAD_CONST               None
              116  LOAD_FAST                'i'
              118  BUILD_SLICE_2         2 
              120  BINARY_SUBSCR    
              122  STORE_FAST               'indent'
              124  JUMP_BACK            32  'to 32'
            126_0  COME_FROM            58  '58'

 L. 564       126  LOAD_FAST                'indent'
              128  LOAD_CONST               None
              130  <117>                 1  ''
              132  POP_JUMP_IF_FALSE   184  'to 184'

 L. 565       134  LOAD_FAST                'line'
              136  LOAD_METHOD              startswith
              138  LOAD_FAST                'indent'
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                PS2
              144  BINARY_ADD       
              146  CALL_METHOD_1         1  ''

 L. 564       148  POP_JUMP_IF_TRUE    172  'to 172'

 L. 566       150  LOAD_FAST                'line'
              152  LOAD_FAST                'indent'
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                PS2
              158  LOAD_METHOD              rstrip
              160  CALL_METHOD_0         0  ''
              162  BINARY_ADD       
              164  LOAD_STR                 '\n'
              166  BINARY_ADD       
              168  COMPARE_OP               ==

 L. 564       170  POP_JUMP_IF_FALSE   184  'to 184'
            172_0  COME_FROM           148  '148'

 L. 567       172  LOAD_FAST                'block'
              174  LOAD_METHOD              append
              176  LOAD_FAST                'line'
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          
              182  JUMP_BACK            32  'to 32'
            184_0  COME_FROM           170  '170'
            184_1  COME_FROM           132  '132'

 L. 569       184  LOAD_FAST                'block'
              186  LOAD_CONST               None
              188  <117>                 1  ''
              190  POP_JUMP_IF_FALSE   214  'to 214'

 L. 570       192  LOAD_FAST                'result'
              194  LOAD_METHOD              extend
              196  LOAD_FAST                'self'
              198  LOAD_METHOD              refactor_doctest
              200  LOAD_FAST                'block'
              202  LOAD_FAST                'block_lineno'

 L. 571       204  LOAD_FAST                'indent'
              206  LOAD_FAST                'filename'

 L. 570       208  CALL_METHOD_4         4  ''
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          
            214_0  COME_FROM           190  '190'

 L. 572       214  LOAD_CONST               None
              216  STORE_FAST               'block'

 L. 573       218  LOAD_CONST               None
              220  STORE_FAST               'indent'

 L. 574       222  LOAD_FAST                'result'
              224  LOAD_METHOD              append
              226  LOAD_FAST                'line'
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          
              232  JUMP_BACK            32  'to 32'
            234_0  COME_FROM            32  '32'

 L. 575       234  LOAD_FAST                'block'
              236  LOAD_CONST               None
              238  <117>                 1  ''
          240_242  POP_JUMP_IF_FALSE   266  'to 266'

 L. 576       244  LOAD_FAST                'result'
              246  LOAD_METHOD              extend
              248  LOAD_FAST                'self'
              250  LOAD_METHOD              refactor_doctest
              252  LOAD_FAST                'block'
              254  LOAD_FAST                'block_lineno'

 L. 577       256  LOAD_FAST                'indent'
              258  LOAD_FAST                'filename'

 L. 576       260  CALL_METHOD_4         4  ''
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          
            266_0  COME_FROM           240  '240'

 L. 578       266  LOAD_STR                 ''
              268  LOAD_METHOD              join
              270  LOAD_FAST                'result'
              272  CALL_METHOD_1         1  ''
              274  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 64

    def refactor_doctest--- This code section failed: ---

 L. 588         0  SETUP_FINALLY        20  'to 20'

 L. 589         2  LOAD_DEREF               'self'
                4  LOAD_METHOD              parse_block
                6  LOAD_FAST                'block'
                8  LOAD_FAST                'lineno'
               10  LOAD_DEREF               'indent'
               12  CALL_METHOD_3         3  ''
               14  STORE_FAST               'tree'
               16  POP_BLOCK        
               18  JUMP_FORWARD        124  'to 124'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 590        20  DUP_TOP          
               22  LOAD_GLOBAL              Exception
               24  <121>               122  ''
               26  POP_TOP          
               28  STORE_FAST               'err'
               30  POP_TOP          
               32  SETUP_FINALLY       114  'to 114'

 L. 591        34  LOAD_DEREF               'self'
               36  LOAD_ATTR                logger
               38  LOAD_METHOD              isEnabledFor
               40  LOAD_GLOBAL              logging
               42  LOAD_ATTR                DEBUG
               44  CALL_METHOD_1         1  ''
               46  POP_JUMP_IF_FALSE    76  'to 76'

 L. 592        48  LOAD_FAST                'block'
               50  GET_ITER         
             52_0  COME_FROM            74  '74'
               52  FOR_ITER             76  'to 76'
               54  STORE_FAST               'line'

 L. 593        56  LOAD_DEREF               'self'
               58  LOAD_METHOD              log_debug
               60  LOAD_STR                 'Source: %s'
               62  LOAD_FAST                'line'
               64  LOAD_METHOD              rstrip
               66  LOAD_STR                 '\n'
               68  CALL_METHOD_1         1  ''
               70  CALL_METHOD_2         2  ''
               72  POP_TOP          
               74  JUMP_BACK            52  'to 52'
             76_0  COME_FROM            52  '52'
             76_1  COME_FROM            46  '46'

 L. 594        76  LOAD_DEREF               'self'
               78  LOAD_METHOD              log_error
               80  LOAD_STR                 "Can't parse docstring in %s line %s: %s: %s"

 L. 595        82  LOAD_FAST                'filename'
               84  LOAD_FAST                'lineno'
               86  LOAD_FAST                'err'
               88  LOAD_ATTR                __class__
               90  LOAD_ATTR                __name__
               92  LOAD_FAST                'err'

 L. 594        94  CALL_METHOD_5         5  ''
               96  POP_TOP          

 L. 596        98  LOAD_FAST                'block'
              100  POP_BLOCK        
              102  ROT_FOUR         
              104  POP_EXCEPT       
              106  LOAD_CONST               None
              108  STORE_FAST               'err'
              110  DELETE_FAST              'err'
              112  RETURN_VALUE     
            114_0  COME_FROM_FINALLY    32  '32'
              114  LOAD_CONST               None
              116  STORE_FAST               'err'
              118  DELETE_FAST              'err'
              120  <48>             
              122  <48>             
            124_0  COME_FROM            18  '18'

 L. 597       124  LOAD_DEREF               'self'
              126  LOAD_METHOD              refactor_tree
              128  LOAD_FAST                'tree'
              130  LOAD_FAST                'filename'
              132  CALL_METHOD_2         2  ''
          134_136  POP_JUMP_IF_FALSE   298  'to 298'

 L. 598       138  LOAD_GLOBAL              str
              140  LOAD_FAST                'tree'
              142  CALL_FUNCTION_1       1  ''
              144  LOAD_ATTR                splitlines
              146  LOAD_CONST               True
              148  LOAD_CONST               ('keepends',)
              150  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              152  STORE_FAST               'new'

 L. 600       154  LOAD_FAST                'new'
              156  LOAD_CONST               None
              158  LOAD_FAST                'lineno'
              160  LOAD_CONST               1
              162  BINARY_SUBTRACT  
              164  BUILD_SLICE_2         2 
              166  BINARY_SUBSCR    
              168  LOAD_FAST                'new'
              170  LOAD_FAST                'lineno'
              172  LOAD_CONST               1
              174  BINARY_SUBTRACT  
              176  LOAD_CONST               None
              178  BUILD_SLICE_2         2 
              180  BINARY_SUBSCR    
              182  ROT_TWO          
              184  STORE_FAST               'clipped'
              186  STORE_FAST               'new'

 L. 601       188  LOAD_FAST                'clipped'
              190  LOAD_STR                 '\n'
              192  BUILD_LIST_1          1 
              194  LOAD_FAST                'lineno'
              196  LOAD_CONST               1
              198  BINARY_SUBTRACT  
              200  BINARY_MULTIPLY  
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_TRUE    214  'to 214'
              206  <74>             
              208  LOAD_FAST                'clipped'
              210  CALL_FUNCTION_1       1  ''
              212  RAISE_VARARGS_1       1  'exception instance'
            214_0  COME_FROM           204  '204'

 L. 602       214  LOAD_FAST                'new'
              216  LOAD_CONST               -1
              218  BINARY_SUBSCR    
              220  LOAD_METHOD              endswith
              222  LOAD_STR                 '\n'
              224  CALL_METHOD_1         1  ''
          226_228  POP_JUMP_IF_TRUE    246  'to 246'

 L. 603       230  LOAD_FAST                'new'
              232  LOAD_CONST               -1
              234  DUP_TOP_TWO      
              236  BINARY_SUBSCR    
              238  LOAD_STR                 '\n'
              240  INPLACE_ADD      
              242  ROT_THREE        
              244  STORE_SUBSCR     
            246_0  COME_FROM           226  '226'

 L. 604       246  LOAD_DEREF               'indent'
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                PS1
              252  BINARY_ADD       
              254  LOAD_FAST                'new'
              256  LOAD_METHOD              pop
              258  LOAD_CONST               0
              260  CALL_METHOD_1         1  ''
              262  BINARY_ADD       
              264  BUILD_LIST_1          1 
              266  STORE_FAST               'block'

 L. 605       268  LOAD_FAST                'new'
          270_272  POP_JUMP_IF_FALSE   298  'to 298'

 L. 606       274  LOAD_FAST                'block'
              276  LOAD_CLOSURE             'indent'
              278  LOAD_CLOSURE             'self'
              280  BUILD_TUPLE_2         2 
              282  LOAD_LISTCOMP            '<code_object <listcomp>>'
              284  LOAD_STR                 'RefactoringTool.refactor_doctest.<locals>.<listcomp>'
              286  MAKE_FUNCTION_8          'closure'
              288  LOAD_FAST                'new'
              290  GET_ITER         
              292  CALL_FUNCTION_1       1  ''
              294  INPLACE_ADD      
              296  STORE_FAST               'block'
            298_0  COME_FROM           270  '270'
            298_1  COME_FROM           134  '134'

 L. 607       298  LOAD_FAST                'block'
              300  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 24

    def summarize--- This code section failed: ---

 L. 610         0  LOAD_FAST                'self'
                2  LOAD_ATTR                wrote
                4  POP_JUMP_IF_FALSE    12  'to 12'

 L. 611         6  LOAD_STR                 'were'
                8  STORE_FAST               'were'
               10  JUMP_FORWARD         16  'to 16'
             12_0  COME_FROM             4  '4'

 L. 613        12  LOAD_STR                 'need to be'
               14  STORE_FAST               'were'
             16_0  COME_FROM            10  '10'

 L. 614        16  LOAD_FAST                'self'
               18  LOAD_ATTR                files
               20  POP_JUMP_IF_TRUE     36  'to 36'

 L. 615        22  LOAD_FAST                'self'
               24  LOAD_METHOD              log_message
               26  LOAD_STR                 'No files %s modified.'
               28  LOAD_FAST                'were'
               30  CALL_METHOD_2         2  ''
               32  POP_TOP          
               34  JUMP_FORWARD         70  'to 70'
             36_0  COME_FROM            20  '20'

 L. 617        36  LOAD_FAST                'self'
               38  LOAD_METHOD              log_message
               40  LOAD_STR                 'Files that %s modified:'
               42  LOAD_FAST                'were'
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 618        48  LOAD_FAST                'self'
               50  LOAD_ATTR                files
               52  GET_ITER         
             54_0  COME_FROM            68  '68'
               54  FOR_ITER             70  'to 70'
               56  STORE_FAST               'file'

 L. 619        58  LOAD_FAST                'self'
               60  LOAD_METHOD              log_message
               62  LOAD_FAST                'file'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          
               68  JUMP_BACK            54  'to 54'
             70_0  COME_FROM            54  '54'
             70_1  COME_FROM            34  '34'

 L. 620        70  LOAD_FAST                'self'
               72  LOAD_ATTR                fixer_log
               74  POP_JUMP_IF_FALSE   108  'to 108'

 L. 621        76  LOAD_FAST                'self'
               78  LOAD_METHOD              log_message
               80  LOAD_STR                 'Warnings/messages while refactoring:'
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          

 L. 622        86  LOAD_FAST                'self'
               88  LOAD_ATTR                fixer_log
               90  GET_ITER         
             92_0  COME_FROM           106  '106'
               92  FOR_ITER            108  'to 108'
               94  STORE_FAST               'message'

 L. 623        96  LOAD_FAST                'self'
               98  LOAD_METHOD              log_message
              100  LOAD_FAST                'message'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          
              106  JUMP_BACK            92  'to 92'
            108_0  COME_FROM            92  '92'
            108_1  COME_FROM            74  '74'

 L. 624       108  LOAD_FAST                'self'
              110  LOAD_ATTR                errors
              112  POP_JUMP_IF_FALSE   200  'to 200'

 L. 625       114  LOAD_GLOBAL              len
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                errors
              120  CALL_FUNCTION_1       1  ''
              122  LOAD_CONST               1
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   140  'to 140'

 L. 626       128  LOAD_FAST                'self'
              130  LOAD_METHOD              log_message
              132  LOAD_STR                 'There was 1 error:'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
              138  JUMP_FORWARD        158  'to 158'
            140_0  COME_FROM           126  '126'

 L. 628       140  LOAD_FAST                'self'
              142  LOAD_METHOD              log_message
              144  LOAD_STR                 'There were %d errors:'
              146  LOAD_GLOBAL              len
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                errors
              152  CALL_FUNCTION_1       1  ''
              154  CALL_METHOD_2         2  ''
              156  POP_TOP          
            158_0  COME_FROM           138  '138'

 L. 629       158  LOAD_FAST                'self'
              160  LOAD_ATTR                errors
              162  GET_ITER         
            164_0  COME_FROM           198  '198'
              164  FOR_ITER            200  'to 200'
              166  UNPACK_SEQUENCE_3     3 
              168  STORE_FAST               'msg'
              170  STORE_FAST               'args'
              172  STORE_FAST               'kwds'

 L. 630       174  LOAD_FAST                'self'
              176  LOAD_ATTR                log_message
              178  LOAD_FAST                'msg'
              180  BUILD_LIST_1          1 
              182  LOAD_FAST                'args'
              184  CALL_FINALLY        187  'to 187'
              186  WITH_CLEANUP_FINISH
              188  BUILD_MAP_0           0 
              190  LOAD_FAST                'kwds'
              192  <164>                 1  ''
              194  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              196  POP_TOP          
              198  JUMP_BACK           164  'to 164'
            200_0  COME_FROM           164  '164'
            200_1  COME_FROM           112  '112'

Parse error at or near `CALL_FINALLY' instruction at offset 184

    def parse_block(self, block, lineno, indent):
        """Parses a block into a tree.

        This is necessary to get correct line number / offset information
        in the parser diagnostics and embedded into the parse tree.
        """
        tree = self.driver.parse_tokens(self.wrap_toks(block, lineno, indent))
        tree.future_features = frozenset
        return tree

    def wrap_toks(self, block, lineno, indent):
        """Wraps a tokenize stream to systematically modify start/end."""
        tokens = tokenize.generate_tokens(self.gen_linesblockindent.__next__)
        for type, value, (line0, col0), (line1, col1), line_text in tokens:
            line0 += lineno - 1
            line1 += lineno - 1
            yield (
             type, value, (line0, col0), (line1, col1), line_text)

    def gen_lines(self, block, indent):
        """Generates lines as expected by tokenize from a list of lines.

        This strips the first len(indent + self.PS1) characters off each line.
        """
        prefix1 = indent + self.PS1
        prefix2 = indent + self.PS2
        prefix = prefix1
        for line in block:
            if line.startswith(prefix):
                yield line[len(prefix):]
            elif line == prefix.rstrip + '\n':
                yield '\n'
            else:
                raise AssertionError('line=%r, prefix=%r' % (line, prefix))
            prefix = prefix2
        else:
            while True:
                yield ''


class MultiprocessingUnsupported(Exception):
    pass


class MultiprocessRefactoringTool(RefactoringTool):

    def __init__--- This code section failed: ---

 L. 683         0  LOAD_GLOBAL              super
                2  LOAD_GLOBAL              MultiprocessRefactoringTool
                4  LOAD_FAST                'self'
                6  CALL_FUNCTION_2       2  ''
                8  LOAD_ATTR                __init__
               10  LOAD_FAST                'args'
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  POP_TOP          

 L. 684        22  LOAD_CONST               None
               24  LOAD_FAST                'self'
               26  STORE_ATTR               queue

 L. 685        28  LOAD_CONST               None
               30  LOAD_FAST                'self'
               32  STORE_ATTR               output_lock

Parse error at or near `None' instruction at offset -1

    def refactor--- This code section failed: ---

 L. 689         0  LOAD_FAST                'num_processes'
                2  LOAD_CONST               1
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    28  'to 28'

 L. 690         8  LOAD_GLOBAL              super
               10  LOAD_GLOBAL              MultiprocessRefactoringTool
               12  LOAD_DEREF               'self'
               14  CALL_FUNCTION_2       2  ''
               16  LOAD_METHOD              refactor

 L. 691        18  LOAD_FAST                'items'
               20  LOAD_FAST                'write'
               22  LOAD_FAST                'doctests_only'

 L. 690        24  CALL_METHOD_3         3  ''
               26  RETURN_VALUE     
             28_0  COME_FROM             6  '6'

 L. 692        28  SETUP_FINALLY        42  'to 42'

 L. 693        30  LOAD_CONST               0
               32  LOAD_CONST               None
               34  IMPORT_NAME              multiprocessing
               36  STORE_DEREF              'multiprocessing'
               38  POP_BLOCK        
               40  JUMP_FORWARD         64  'to 64'
             42_0  COME_FROM_FINALLY    28  '28'

 L. 694        42  DUP_TOP          
               44  LOAD_GLOBAL              ImportError
               46  <121>                62  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 695        54  LOAD_GLOBAL              MultiprocessingUnsupported
               56  RAISE_VARARGS_1       1  'exception instance'
               58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
               62  <48>             
             64_0  COME_FROM            60  '60'
             64_1  COME_FROM            40  '40'

 L. 696        64  LOAD_DEREF               'self'
               66  LOAD_ATTR                queue
               68  LOAD_CONST               None
               70  <117>                 1  ''
               72  POP_JUMP_IF_FALSE    82  'to 82'

 L. 697        74  LOAD_GLOBAL              RuntimeError
               76  LOAD_STR                 'already doing multiple processes'
               78  CALL_FUNCTION_1       1  ''
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            72  '72'

 L. 698        82  LOAD_DEREF               'multiprocessing'
               84  LOAD_METHOD              JoinableQueue
               86  CALL_METHOD_0         0  ''
               88  LOAD_DEREF               'self'
               90  STORE_ATTR               queue

 L. 699        92  LOAD_DEREF               'multiprocessing'
               94  LOAD_METHOD              Lock
               96  CALL_METHOD_0         0  ''
               98  LOAD_DEREF               'self'
              100  STORE_ATTR               output_lock

 L. 700       102  LOAD_CLOSURE             'multiprocessing'
              104  LOAD_CLOSURE             'self'
              106  BUILD_TUPLE_2         2 
              108  LOAD_LISTCOMP            '<code_object <listcomp>>'
              110  LOAD_STR                 'MultiprocessRefactoringTool.refactor.<locals>.<listcomp>'
              112  MAKE_FUNCTION_8          'closure'

 L. 701       114  LOAD_GLOBAL              range
              116  LOAD_FAST                'num_processes'
              118  CALL_FUNCTION_1       1  ''

 L. 700       120  GET_ITER         
              122  CALL_FUNCTION_1       1  ''
              124  STORE_FAST               'processes'

 L. 702       126  SETUP_FINALLY       238  'to 238'

 L. 703       128  LOAD_FAST                'processes'
              130  GET_ITER         
            132_0  COME_FROM           144  '144'
              132  FOR_ITER            146  'to 146'
              134  STORE_FAST               'p'

 L. 704       136  LOAD_FAST                'p'
              138  LOAD_METHOD              start
              140  CALL_METHOD_0         0  ''
              142  POP_TOP          
              144  JUMP_BACK           132  'to 132'
            146_0  COME_FROM           132  '132'

 L. 705       146  LOAD_GLOBAL              super
              148  LOAD_GLOBAL              MultiprocessRefactoringTool
              150  LOAD_DEREF               'self'
              152  CALL_FUNCTION_2       2  ''
              154  LOAD_METHOD              refactor
              156  LOAD_FAST                'items'
              158  LOAD_FAST                'write'

 L. 706       160  LOAD_FAST                'doctests_only'

 L. 705       162  CALL_METHOD_3         3  ''
              164  POP_TOP          
              166  POP_BLOCK        

 L. 708       168  LOAD_DEREF               'self'
              170  LOAD_ATTR                queue
              172  LOAD_METHOD              join
              174  CALL_METHOD_0         0  ''
              176  POP_TOP          

 L. 709       178  LOAD_GLOBAL              range
              180  LOAD_FAST                'num_processes'
              182  CALL_FUNCTION_1       1  ''
              184  GET_ITER         
            186_0  COME_FROM           202  '202'
              186  FOR_ITER            204  'to 204'
              188  STORE_FAST               'i'

 L. 710       190  LOAD_DEREF               'self'
              192  LOAD_ATTR                queue
              194  LOAD_METHOD              put
              196  LOAD_CONST               None
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          
              202  JUMP_BACK           186  'to 186'
            204_0  COME_FROM           186  '186'

 L. 711       204  LOAD_FAST                'processes'
              206  GET_ITER         
            208_0  COME_FROM           228  '228'
            208_1  COME_FROM           218  '218'
              208  FOR_ITER            230  'to 230'
              210  STORE_FAST               'p'

 L. 712       212  LOAD_FAST                'p'
              214  LOAD_METHOD              is_alive
              216  CALL_METHOD_0         0  ''
              218  POP_JUMP_IF_FALSE_BACK   208  'to 208'

 L. 713       220  LOAD_FAST                'p'
              222  LOAD_METHOD              join
              224  CALL_METHOD_0         0  ''
              226  POP_TOP          
              228  JUMP_BACK           208  'to 208'
            230_0  COME_FROM           208  '208'

 L. 714       230  LOAD_CONST               None
              232  LOAD_DEREF               'self'
              234  STORE_ATTR               queue
              236  JUMP_FORWARD        314  'to 314'
            238_0  COME_FROM_FINALLY   126  '126'

 L. 708       238  LOAD_DEREF               'self'
              240  LOAD_ATTR                queue
              242  LOAD_METHOD              join
              244  CALL_METHOD_0         0  ''
              246  POP_TOP          

 L. 709       248  LOAD_GLOBAL              range
              250  LOAD_FAST                'num_processes'
              252  CALL_FUNCTION_1       1  ''
              254  GET_ITER         
            256_0  COME_FROM           272  '272'
              256  FOR_ITER            276  'to 276'
              258  STORE_FAST               'i'

 L. 710       260  LOAD_DEREF               'self'
              262  LOAD_ATTR                queue
              264  LOAD_METHOD              put
              266  LOAD_CONST               None
              268  CALL_METHOD_1         1  ''
              270  POP_TOP          
          272_274  JUMP_BACK           256  'to 256'
            276_0  COME_FROM           256  '256'

 L. 711       276  LOAD_FAST                'processes'
              278  GET_ITER         
            280_0  COME_FROM           302  '302'
            280_1  COME_FROM           290  '290'
              280  FOR_ITER            306  'to 306'
              282  STORE_FAST               'p'

 L. 712       284  LOAD_FAST                'p'
              286  LOAD_METHOD              is_alive
              288  CALL_METHOD_0         0  ''
          290_292  POP_JUMP_IF_FALSE_BACK   280  'to 280'

 L. 713       294  LOAD_FAST                'p'
              296  LOAD_METHOD              join
              298  CALL_METHOD_0         0  ''
              300  POP_TOP          
          302_304  JUMP_BACK           280  'to 280'
            306_0  COME_FROM           280  '280'

 L. 714       306  LOAD_CONST               None
              308  LOAD_DEREF               'self'
              310  STORE_ATTR               queue
              312  <48>             
            314_0  COME_FROM           236  '236'

Parse error at or near `<121>' instruction at offset 46

    def _child--- This code section failed: ---

 L. 717         0  LOAD_FAST                'self'
                2  LOAD_ATTR                queue
                4  LOAD_METHOD              get
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'task'
             10_0  COME_FROM            86  '86'

 L. 718        10  LOAD_FAST                'task'
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    88  'to 88'

 L. 719        18  LOAD_FAST                'task'
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'args'
               24  STORE_FAST               'kwargs'

 L. 720        26  SETUP_FINALLY        64  'to 64'

 L. 721        28  LOAD_GLOBAL              super
               30  LOAD_GLOBAL              MultiprocessRefactoringTool
               32  LOAD_FAST                'self'
               34  CALL_FUNCTION_2       2  ''
               36  LOAD_ATTR                refactor_file

 L. 722        38  LOAD_FAST                'args'

 L. 721        40  BUILD_MAP_0           0 

 L. 722        42  LOAD_FAST                'kwargs'

 L. 721        44  <164>                 1  ''
               46  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               48  POP_TOP          
               50  POP_BLOCK        

 L. 724        52  LOAD_FAST                'self'
               54  LOAD_ATTR                queue
               56  LOAD_METHOD              task_done
               58  CALL_METHOD_0         0  ''
               60  POP_TOP          
               62  JUMP_FORWARD         76  'to 76'
             64_0  COME_FROM_FINALLY    26  '26'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                queue
               68  LOAD_METHOD              task_done
               70  CALL_METHOD_0         0  ''
               72  POP_TOP          
               74  <48>             
             76_0  COME_FROM            62  '62'

 L. 725        76  LOAD_FAST                'self'
               78  LOAD_ATTR                queue
               80  LOAD_METHOD              get
               82  CALL_METHOD_0         0  ''
               84  STORE_FAST               'task'
               86  JUMP_BACK            10  'to 10'
             88_0  COME_FROM            16  '16'

Parse error at or near `<117>' instruction at offset 14

    def refactor_file--- This code section failed: ---

 L. 728         0  LOAD_FAST                'self'
                2  LOAD_ATTR                queue
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L. 729        10  LOAD_FAST                'self'
               12  LOAD_ATTR                queue
               14  LOAD_METHOD              put
               16  LOAD_FAST                'args'
               18  LOAD_FAST                'kwargs'
               20  BUILD_TUPLE_2         2 
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
               26  JUMP_FORWARD         50  'to 50'
             28_0  COME_FROM             8  '8'

 L. 731        28  LOAD_GLOBAL              super
               30  LOAD_GLOBAL              MultiprocessRefactoringTool
               32  LOAD_FAST                'self'
               34  CALL_FUNCTION_2       2  ''
               36  LOAD_ATTR                refactor_file

 L. 732        38  LOAD_FAST                'args'

 L. 731        40  BUILD_MAP_0           0 

 L. 732        42  LOAD_FAST                'kwargs'

 L. 731        44  <164>                 1  ''
               46  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               48  RETURN_VALUE     
             50_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1