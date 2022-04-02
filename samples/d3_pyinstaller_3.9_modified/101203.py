# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\fancy_getopt.py
"""distutils.fancy_getopt

Wrapper around the standard getopt module that provides the following
additional features:
  * short and long options are tied together
  * options have help strings, so fancy_getopt could potentially
    create a complete usage summary
  * options set attributes of a passed-in object
"""
import sys, string, re, getopt
from distutils.errors import *
longopt_pat = '[a-zA-Z](?:[a-zA-Z0-9-]*)'
longopt_re = re.compile('^%s$' % longopt_pat)
neg_alias_re = re.compile('^(%s)=!(%s)$' % (longopt_pat, longopt_pat))
longopt_xlate = str.maketrans('-', '_')

class FancyGetopt:
    __doc__ = 'Wrapper around the standard \'getopt()\' module that provides some\n    handy extra functionality:\n      * short and long options are tied together\n      * options have help strings, and help text can be assembled\n        from them\n      * options set attributes of a passed-in object\n      * boolean options can have "negative aliases" -- eg. if\n        --quiet is the "negative alias" of --verbose, then "--quiet"\n        on the command line sets \'verbose\' to false\n    '

    def __init__(self, option_table=None):
        self.option_table = option_table
        self.option_index = {}
        if self.option_table:
            self._build_index()
        self.alias = {}
        self.negative_alias = {}
        self.short_opts = []
        self.long_opts = []
        self.short2long = {}
        self.attr_name = {}
        self.takes_arg = {}
        self.option_order = []

    def _build_index(self):
        self.option_index.clear()
        for option in self.option_table:
            self.option_index[option[0]] = option

    def set_option_table(self, option_table):
        self.option_table = option_table
        self._build_index()

    def add_option--- This code section failed: ---

 L.  91         0  LOAD_FAST                'long_option'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                option_index
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L.  92        10  LOAD_GLOBAL              DistutilsGetoptError

 L.  93        12  LOAD_STR                 "option conflict: already an option '%s'"
               14  LOAD_FAST                'long_option'
               16  BINARY_MODULO    

 L.  92        18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
               22  JUMP_FORWARD         56  'to 56'
             24_0  COME_FROM             8  '8'

 L.  95        24  LOAD_FAST                'long_option'
               26  LOAD_FAST                'short_option'
               28  LOAD_FAST                'help_string'
               30  BUILD_TUPLE_3         3 
               32  STORE_FAST               'option'

 L.  96        34  LOAD_FAST                'self'
               36  LOAD_ATTR                option_table
               38  LOAD_METHOD              append
               40  LOAD_FAST                'option'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L.  97        46  LOAD_FAST                'option'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                option_index
               52  LOAD_FAST                'long_option'
               54  STORE_SUBSCR     
             56_0  COME_FROM            22  '22'

Parse error at or near `None' instruction at offset -1

    def has_option--- This code section failed: ---

 L. 102         0  LOAD_FAST                'long_option'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                option_index
                6  <118>                 0  ''
                8  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def get_attr_name(self, long_option):
        """Translate long option name 'long_option' to the form it
        has as an attribute of some object: ie., translate hyphens
        to underscores."""
        return long_option.translate(longopt_xlate)

    def _check_alias_dict--- This code section failed: ---

 L. 111         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'aliases'
                4  LOAD_GLOBAL              dict
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 112        14  LOAD_FAST                'aliases'
               16  LOAD_METHOD              items
               18  CALL_METHOD_0         0  ''
               20  GET_ITER         
             22_0  COME_FROM            86  '86'
             22_1  COME_FROM            66  '66'
               22  FOR_ITER             88  'to 88'
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'alias'
               28  STORE_FAST               'opt'

 L. 113        30  LOAD_FAST                'alias'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                option_index
               36  <118>                 1  ''
               38  POP_JUMP_IF_FALSE    58  'to 58'

 L. 114        40  LOAD_GLOBAL              DistutilsGetoptError
               42  LOAD_STR                 "invalid %s '%s': option '%s' not defined"

 L. 115        44  LOAD_FAST                'what'
               46  LOAD_FAST                'alias'
               48  LOAD_FAST                'alias'
               50  BUILD_TUPLE_3         3 

 L. 114        52  BINARY_MODULO    
               54  CALL_FUNCTION_1       1  ''
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            38  '38'

 L. 116        58  LOAD_FAST                'opt'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                option_index
               64  <118>                 1  ''
               66  POP_JUMP_IF_FALSE_BACK    22  'to 22'

 L. 117        68  LOAD_GLOBAL              DistutilsGetoptError
               70  LOAD_STR                 "invalid %s '%s': aliased option '%s' not defined"

 L. 118        72  LOAD_FAST                'what'
               74  LOAD_FAST                'alias'
               76  LOAD_FAST                'opt'
               78  BUILD_TUPLE_3         3 

 L. 117        80  BINARY_MODULO    
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
               86  JUMP_BACK            22  'to 22'
             88_0  COME_FROM            22  '22'

Parse error at or near `None' instruction at offset -1

    def set_aliases(self, alias):
        """Set the aliases for this option parser."""
        self._check_alias_dict(alias, 'alias')
        self.alias = alias

    def set_negative_aliases(self, negative_alias):
        """Set the negative aliases for this option parser.
        'negative_alias' should be a dictionary mapping option names to
        option names, both the key and value must already be defined
        in the option table."""
        self._check_alias_dict(negative_alias, 'negative alias')
        self.negative_alias = negative_alias

    def _grok_option_table--- This code section failed: ---

 L. 138         0  BUILD_LIST_0          0 
                2  LOAD_FAST                'self'
                4  STORE_ATTR               long_opts

 L. 139         6  BUILD_LIST_0          0 
                8  LOAD_FAST                'self'
               10  STORE_ATTR               short_opts

 L. 140        12  LOAD_FAST                'self'
               14  LOAD_ATTR                short2long
               16  LOAD_METHOD              clear
               18  CALL_METHOD_0         0  ''
               20  POP_TOP          

 L. 141        22  BUILD_MAP_0           0 
               24  LOAD_FAST                'self'
               26  STORE_ATTR               repeat

 L. 143        28  LOAD_FAST                'self'
               30  LOAD_ATTR                option_table
               32  GET_ITER         
             34_0  COME_FROM           454  '454'
             34_1  COME_FROM           426  '426'
            34_36  FOR_ITER            456  'to 456'
               38  STORE_FAST               'option'

 L. 144        40  LOAD_GLOBAL              len
               42  LOAD_FAST                'option'
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_CONST               3
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    68  'to 68'

 L. 145        52  LOAD_FAST                'option'
               54  UNPACK_SEQUENCE_3     3 
               56  STORE_FAST               'long'
               58  STORE_FAST               'short'
               60  STORE_FAST               'help'

 L. 146        62  LOAD_CONST               0
               64  STORE_FAST               'repeat'
               66  JUMP_FORWARD        108  'to 108'
             68_0  COME_FROM            50  '50'

 L. 147        68  LOAD_GLOBAL              len
               70  LOAD_FAST                'option'
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_CONST               4
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE    94  'to 94'

 L. 148        80  LOAD_FAST                'option'
               82  UNPACK_SEQUENCE_4     4 
               84  STORE_FAST               'long'
               86  STORE_FAST               'short'
               88  STORE_FAST               'help'
               90  STORE_FAST               'repeat'
               92  JUMP_FORWARD        108  'to 108'
             94_0  COME_FROM            78  '78'

 L. 152        94  LOAD_GLOBAL              ValueError
               96  LOAD_STR                 'invalid option tuple: %r'
               98  LOAD_FAST                'option'
              100  BUILD_TUPLE_1         1 
              102  BINARY_MODULO    
              104  CALL_FUNCTION_1       1  ''
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            92  '92'
            108_1  COME_FROM            66  '66'

 L. 155       108  LOAD_GLOBAL              isinstance
              110  LOAD_FAST                'long'
              112  LOAD_GLOBAL              str
              114  CALL_FUNCTION_2       2  ''
              116  POP_JUMP_IF_FALSE   130  'to 130'
              118  LOAD_GLOBAL              len
              120  LOAD_FAST                'long'
              122  CALL_FUNCTION_1       1  ''
              124  LOAD_CONST               2
              126  COMPARE_OP               <
              128  POP_JUMP_IF_FALSE   142  'to 142'
            130_0  COME_FROM           116  '116'

 L. 156       130  LOAD_GLOBAL              DistutilsGetoptError
              132  LOAD_STR                 "invalid long option '%s': must be a string of length >= 2"

 L. 157       134  LOAD_FAST                'long'

 L. 156       136  BINARY_MODULO    
              138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
            142_0  COME_FROM           128  '128'

 L. 159       142  LOAD_FAST                'short'
              144  LOAD_CONST               None
              146  <117>                 0  ''
              148  POP_JUMP_IF_TRUE    184  'to 184'

 L. 160       150  LOAD_GLOBAL              isinstance
              152  LOAD_FAST                'short'
              154  LOAD_GLOBAL              str
              156  CALL_FUNCTION_2       2  ''

 L. 159       158  POP_JUMP_IF_FALSE   172  'to 172'

 L. 160       160  LOAD_GLOBAL              len
              162  LOAD_FAST                'short'
              164  CALL_FUNCTION_1       1  ''
              166  LOAD_CONST               1
              168  COMPARE_OP               ==

 L. 159       170  POP_JUMP_IF_TRUE    184  'to 184'
            172_0  COME_FROM           158  '158'

 L. 161       172  LOAD_GLOBAL              DistutilsGetoptError
              174  LOAD_STR                 "invalid short option '%s': must a single character or None"

 L. 162       176  LOAD_FAST                'short'

 L. 161       178  BINARY_MODULO    
              180  CALL_FUNCTION_1       1  ''
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM           170  '170'
            184_1  COME_FROM           148  '148'

 L. 164       184  LOAD_FAST                'repeat'
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                repeat
              190  LOAD_FAST                'long'
              192  STORE_SUBSCR     

 L. 165       194  LOAD_FAST                'self'
              196  LOAD_ATTR                long_opts
              198  LOAD_METHOD              append
              200  LOAD_FAST                'long'
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          

 L. 167       206  LOAD_FAST                'long'
              208  LOAD_CONST               -1
              210  BINARY_SUBSCR    
              212  LOAD_STR                 '='
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE   254  'to 254'

 L. 168       218  LOAD_FAST                'short'
              220  POP_JUMP_IF_FALSE   230  'to 230'
              222  LOAD_FAST                'short'
              224  LOAD_STR                 ':'
              226  BINARY_ADD       
              228  STORE_FAST               'short'
            230_0  COME_FROM           220  '220'

 L. 169       230  LOAD_FAST                'long'
              232  LOAD_CONST               0
              234  LOAD_CONST               -1
              236  BUILD_SLICE_2         2 
              238  BINARY_SUBSCR    
              240  STORE_FAST               'long'

 L. 170       242  LOAD_CONST               1
              244  LOAD_FAST                'self'
              246  LOAD_ATTR                takes_arg
              248  LOAD_FAST                'long'
              250  STORE_SUBSCR     
              252  JUMP_FORWARD        324  'to 324'
            254_0  COME_FROM           216  '216'

 L. 174       254  LOAD_FAST                'self'
              256  LOAD_ATTR                negative_alias
              258  LOAD_METHOD              get
              260  LOAD_FAST                'long'
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               'alias_to'

 L. 175       266  LOAD_FAST                'alias_to'
              268  LOAD_CONST               None
              270  <117>                 1  ''
          272_274  POP_JUMP_IF_FALSE   314  'to 314'

 L. 176       276  LOAD_FAST                'self'
              278  LOAD_ATTR                takes_arg
              280  LOAD_FAST                'alias_to'
              282  BINARY_SUBSCR    
          284_286  POP_JUMP_IF_FALSE   304  'to 304'

 L. 177       288  LOAD_GLOBAL              DistutilsGetoptError

 L. 178       290  LOAD_STR                 "invalid negative alias '%s': aliased option '%s' takes a value"

 L. 180       292  LOAD_FAST                'long'
              294  LOAD_FAST                'alias_to'
              296  BUILD_TUPLE_2         2 

 L. 178       298  BINARY_MODULO    

 L. 177       300  CALL_FUNCTION_1       1  ''
              302  RAISE_VARARGS_1       1  'exception instance'
            304_0  COME_FROM           284  '284'

 L. 182       304  LOAD_FAST                'long'
              306  LOAD_FAST                'self'
              308  LOAD_ATTR                long_opts
              310  LOAD_CONST               -1
              312  STORE_SUBSCR     
            314_0  COME_FROM           272  '272'

 L. 183       314  LOAD_CONST               0
              316  LOAD_FAST                'self'
              318  LOAD_ATTR                takes_arg
              320  LOAD_FAST                'long'
              322  STORE_SUBSCR     
            324_0  COME_FROM           252  '252'

 L. 187       324  LOAD_FAST                'self'
              326  LOAD_ATTR                alias
              328  LOAD_METHOD              get
              330  LOAD_FAST                'long'
              332  CALL_METHOD_1         1  ''
              334  STORE_FAST               'alias_to'

 L. 188       336  LOAD_FAST                'alias_to'
              338  LOAD_CONST               None
              340  <117>                 1  ''
          342_344  POP_JUMP_IF_FALSE   384  'to 384'

 L. 189       346  LOAD_FAST                'self'
              348  LOAD_ATTR                takes_arg
              350  LOAD_FAST                'long'
              352  BINARY_SUBSCR    
              354  LOAD_FAST                'self'
              356  LOAD_ATTR                takes_arg
              358  LOAD_FAST                'alias_to'
              360  BINARY_SUBSCR    
              362  COMPARE_OP               !=
          364_366  POP_JUMP_IF_FALSE   384  'to 384'

 L. 190       368  LOAD_GLOBAL              DistutilsGetoptError

 L. 191       370  LOAD_STR                 "invalid alias '%s': inconsistent with aliased option '%s' (one of them takes a value, the other doesn't"

 L. 194       372  LOAD_FAST                'long'
              374  LOAD_FAST                'alias_to'
              376  BUILD_TUPLE_2         2 

 L. 191       378  BINARY_MODULO    

 L. 190       380  CALL_FUNCTION_1       1  ''
              382  RAISE_VARARGS_1       1  'exception instance'
            384_0  COME_FROM           364  '364'
            384_1  COME_FROM           342  '342'

 L. 200       384  LOAD_GLOBAL              longopt_re
              386  LOAD_METHOD              match
              388  LOAD_FAST                'long'
              390  CALL_METHOD_1         1  ''
          392_394  POP_JUMP_IF_TRUE    408  'to 408'

 L. 201       396  LOAD_GLOBAL              DistutilsGetoptError

 L. 202       398  LOAD_STR                 "invalid long option name '%s' (must be letters, numbers, hyphens only"

 L. 203       400  LOAD_FAST                'long'

 L. 202       402  BINARY_MODULO    

 L. 201       404  CALL_FUNCTION_1       1  ''
              406  RAISE_VARARGS_1       1  'exception instance'
            408_0  COME_FROM           392  '392'

 L. 205       408  LOAD_FAST                'self'
              410  LOAD_METHOD              get_attr_name
              412  LOAD_FAST                'long'
              414  CALL_METHOD_1         1  ''
              416  LOAD_FAST                'self'
              418  LOAD_ATTR                attr_name
              420  LOAD_FAST                'long'
              422  STORE_SUBSCR     

 L. 206       424  LOAD_FAST                'short'
              426  POP_JUMP_IF_FALSE_BACK    34  'to 34'

 L. 207       428  LOAD_FAST                'self'
              430  LOAD_ATTR                short_opts
              432  LOAD_METHOD              append
              434  LOAD_FAST                'short'
              436  CALL_METHOD_1         1  ''
              438  POP_TOP          

 L. 208       440  LOAD_FAST                'long'
              442  LOAD_FAST                'self'
              444  LOAD_ATTR                short2long
              446  LOAD_FAST                'short'
              448  LOAD_CONST               0
              450  BINARY_SUBSCR    
              452  STORE_SUBSCR     
              454  JUMP_BACK            34  'to 34'
            456_0  COME_FROM            34  '34'

Parse error at or near `<117>' instruction at offset 146

    def getopt--- This code section failed: ---

 L. 221         0  LOAD_FAST                'args'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 222         8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                argv
               12  LOAD_CONST               1
               14  LOAD_CONST               None
               16  BUILD_SLICE_2         2 
               18  BINARY_SUBSCR    
               20  STORE_FAST               'args'
             22_0  COME_FROM             6  '6'

 L. 223        22  LOAD_FAST                'object'
               24  LOAD_CONST               None
               26  <117>                 0  ''
               28  POP_JUMP_IF_FALSE    42  'to 42'

 L. 224        30  LOAD_GLOBAL              OptionDummy
               32  CALL_FUNCTION_0       0  ''
               34  STORE_FAST               'object'

 L. 225        36  LOAD_CONST               True
               38  STORE_FAST               'created_object'
               40  JUMP_FORWARD         46  'to 46'
             42_0  COME_FROM            28  '28'

 L. 227        42  LOAD_CONST               False
               44  STORE_FAST               'created_object'
             46_0  COME_FROM            40  '40'

 L. 229        46  LOAD_FAST                'self'
               48  LOAD_METHOD              _grok_option_table
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          

 L. 231        54  LOAD_STR                 ' '
               56  LOAD_METHOD              join
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                short_opts
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'short_opts'

 L. 232        66  SETUP_FINALLY        92  'to 92'

 L. 233        68  LOAD_GLOBAL              getopt
               70  LOAD_METHOD              getopt
               72  LOAD_FAST                'args'
               74  LOAD_FAST                'short_opts'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                long_opts
               80  CALL_METHOD_3         3  ''
               82  UNPACK_SEQUENCE_2     2 
               84  STORE_FAST               'opts'
               86  STORE_FAST               'args'
               88  POP_BLOCK        
               90  JUMP_FORWARD        138  'to 138'
             92_0  COME_FROM_FINALLY    66  '66'

 L. 234        92  DUP_TOP          
               94  LOAD_GLOBAL              getopt
               96  LOAD_ATTR                error
               98  <121>               136  ''
              100  POP_TOP          
              102  STORE_FAST               'msg'
              104  POP_TOP          
              106  SETUP_FINALLY       128  'to 128'

 L. 235       108  LOAD_GLOBAL              DistutilsArgError
              110  LOAD_FAST                'msg'
              112  CALL_FUNCTION_1       1  ''
              114  RAISE_VARARGS_1       1  'exception instance'
              116  POP_BLOCK        
              118  POP_EXCEPT       
              120  LOAD_CONST               None
              122  STORE_FAST               'msg'
              124  DELETE_FAST              'msg'
              126  JUMP_FORWARD        138  'to 138'
            128_0  COME_FROM_FINALLY   106  '106'
              128  LOAD_CONST               None
              130  STORE_FAST               'msg'
              132  DELETE_FAST              'msg'
              134  <48>             
              136  <48>             
            138_0  COME_FROM           126  '126'
            138_1  COME_FROM            90  '90'

 L. 237       138  LOAD_FAST                'opts'
              140  GET_ITER         
            142_0  COME_FROM           394  '394'
              142  FOR_ITER            396  'to 396'
              144  UNPACK_SEQUENCE_2     2 
              146  STORE_FAST               'opt'
              148  STORE_FAST               'val'

 L. 238       150  LOAD_GLOBAL              len
              152  LOAD_FAST                'opt'
              154  CALL_FUNCTION_1       1  ''
              156  LOAD_CONST               2
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   190  'to 190'
              162  LOAD_FAST                'opt'
              164  LOAD_CONST               0
              166  BINARY_SUBSCR    
              168  LOAD_STR                 '-'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   190  'to 190'

 L. 239       174  LOAD_FAST                'self'
              176  LOAD_ATTR                short2long
              178  LOAD_FAST                'opt'
              180  LOAD_CONST               1
              182  BINARY_SUBSCR    
              184  BINARY_SUBSCR    
              186  STORE_FAST               'opt'
              188  JUMP_FORWARD        234  'to 234'
            190_0  COME_FROM           172  '172'
            190_1  COME_FROM           160  '160'

 L. 241       190  LOAD_GLOBAL              len
              192  LOAD_FAST                'opt'
              194  CALL_FUNCTION_1       1  ''
              196  LOAD_CONST               2
              198  COMPARE_OP               >
              200  POP_JUMP_IF_FALSE   218  'to 218'
              202  LOAD_FAST                'opt'
              204  LOAD_CONST               None
              206  LOAD_CONST               2
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  LOAD_STR                 '--'
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_TRUE    222  'to 222'
            218_0  COME_FROM           200  '200'
              218  <74>             
              220  RAISE_VARARGS_1       1  'exception instance'
            222_0  COME_FROM           216  '216'

 L. 242       222  LOAD_FAST                'opt'
              224  LOAD_CONST               2
              226  LOAD_CONST               None
              228  BUILD_SLICE_2         2 
              230  BINARY_SUBSCR    
              232  STORE_FAST               'opt'
            234_0  COME_FROM           188  '188'

 L. 244       234  LOAD_FAST                'self'
              236  LOAD_ATTR                alias
              238  LOAD_METHOD              get
              240  LOAD_FAST                'opt'
              242  CALL_METHOD_1         1  ''
              244  STORE_FAST               'alias'

 L. 245       246  LOAD_FAST                'alias'
              248  POP_JUMP_IF_FALSE   254  'to 254'

 L. 246       250  LOAD_FAST                'alias'
              252  STORE_FAST               'opt'
            254_0  COME_FROM           248  '248'

 L. 248       254  LOAD_FAST                'self'
              256  LOAD_ATTR                takes_arg
              258  LOAD_FAST                'opt'
              260  BINARY_SUBSCR    
          262_264  POP_JUMP_IF_TRUE    316  'to 316'

 L. 249       266  LOAD_FAST                'val'
              268  LOAD_STR                 ''
              270  COMPARE_OP               ==
          272_274  POP_JUMP_IF_TRUE    284  'to 284'
              276  <74>             
              278  LOAD_STR                 "boolean option can't have value"
              280  CALL_FUNCTION_1       1  ''
              282  RAISE_VARARGS_1       1  'exception instance'
            284_0  COME_FROM           272  '272'

 L. 250       284  LOAD_FAST                'self'
              286  LOAD_ATTR                negative_alias
              288  LOAD_METHOD              get
              290  LOAD_FAST                'opt'
              292  CALL_METHOD_1         1  ''
              294  STORE_FAST               'alias'

 L. 251       296  LOAD_FAST                'alias'
          298_300  POP_JUMP_IF_FALSE   312  'to 312'

 L. 252       302  LOAD_FAST                'alias'
              304  STORE_FAST               'opt'

 L. 253       306  LOAD_CONST               0
              308  STORE_FAST               'val'
              310  JUMP_FORWARD        316  'to 316'
            312_0  COME_FROM           298  '298'

 L. 255       312  LOAD_CONST               1
              314  STORE_FAST               'val'
            316_0  COME_FROM           310  '310'
            316_1  COME_FROM           262  '262'

 L. 257       316  LOAD_FAST                'self'
              318  LOAD_ATTR                attr_name
              320  LOAD_FAST                'opt'
              322  BINARY_SUBSCR    
              324  STORE_FAST               'attr'

 L. 260       326  LOAD_FAST                'val'
          328_330  POP_JUMP_IF_FALSE   366  'to 366'
              332  LOAD_FAST                'self'
              334  LOAD_ATTR                repeat
              336  LOAD_METHOD              get
              338  LOAD_FAST                'attr'
              340  CALL_METHOD_1         1  ''
              342  LOAD_CONST               None
              344  <117>                 1  ''
          346_348  POP_JUMP_IF_FALSE   366  'to 366'

 L. 261       350  LOAD_GLOBAL              getattr
              352  LOAD_FAST                'object'
              354  LOAD_FAST                'attr'
              356  LOAD_CONST               0
              358  CALL_FUNCTION_3       3  ''
              360  LOAD_CONST               1
              362  BINARY_ADD       
              364  STORE_FAST               'val'
            366_0  COME_FROM           346  '346'
            366_1  COME_FROM           328  '328'

 L. 262       366  LOAD_GLOBAL              setattr
              368  LOAD_FAST                'object'
              370  LOAD_FAST                'attr'
              372  LOAD_FAST                'val'
              374  CALL_FUNCTION_3       3  ''
              376  POP_TOP          

 L. 263       378  LOAD_FAST                'self'
              380  LOAD_ATTR                option_order
              382  LOAD_METHOD              append
              384  LOAD_FAST                'opt'
              386  LOAD_FAST                'val'
              388  BUILD_TUPLE_2         2 
              390  CALL_METHOD_1         1  ''
              392  POP_TOP          
              394  JUMP_BACK           142  'to 142'
            396_0  COME_FROM           142  '142'

 L. 266       396  LOAD_FAST                'created_object'
          398_400  POP_JUMP_IF_FALSE   410  'to 410'

 L. 267       402  LOAD_FAST                'args'
              404  LOAD_FAST                'object'
              406  BUILD_TUPLE_2         2 
              408  RETURN_VALUE     
            410_0  COME_FROM           398  '398'

 L. 269       410  LOAD_FAST                'args'
              412  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def get_option_order--- This code section failed: ---

 L. 276         0  LOAD_FAST                'self'
                2  LOAD_ATTR                option_order
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 277        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 "'getopt()' hasn't been called yet"
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
               18  JUMP_FORWARD         26  'to 26'
             20_0  COME_FROM             8  '8'

 L. 279        20  LOAD_FAST                'self'
               22  LOAD_ATTR                option_order
               24  RETURN_VALUE     
             26_0  COME_FROM            18  '18'

Parse error at or near `None' instruction at offset -1

    def generate_help--- This code section failed: ---

 L. 289         0  LOAD_CONST               0
                2  STORE_FAST               'max_opt'

 L. 290         4  LOAD_FAST                'self'
                6  LOAD_ATTR                option_table
                8  GET_ITER         
             10_0  COME_FROM            86  '86'
             10_1  COME_FROM            80  '80'
               10  FOR_ITER             88  'to 88'
               12  STORE_FAST               'option'

 L. 291        14  LOAD_FAST                'option'
               16  LOAD_CONST               0
               18  BINARY_SUBSCR    
               20  STORE_FAST               'long'

 L. 292        22  LOAD_FAST                'option'
               24  LOAD_CONST               1
               26  BINARY_SUBSCR    
               28  STORE_FAST               'short'

 L. 293        30  LOAD_GLOBAL              len
               32  LOAD_FAST                'long'
               34  CALL_FUNCTION_1       1  ''
               36  STORE_FAST               'l'

 L. 294        38  LOAD_FAST                'long'
               40  LOAD_CONST               -1
               42  BINARY_SUBSCR    
               44  LOAD_STR                 '='
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    58  'to 58'

 L. 295        50  LOAD_FAST                'l'
               52  LOAD_CONST               1
               54  BINARY_SUBTRACT  
               56  STORE_FAST               'l'
             58_0  COME_FROM            48  '48'

 L. 296        58  LOAD_FAST                'short'
               60  LOAD_CONST               None
               62  <117>                 1  ''
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L. 297        66  LOAD_FAST                'l'
               68  LOAD_CONST               5
               70  BINARY_ADD       
               72  STORE_FAST               'l'
             74_0  COME_FROM            64  '64'

 L. 298        74  LOAD_FAST                'l'
               76  LOAD_FAST                'max_opt'
               78  COMPARE_OP               >
               80  POP_JUMP_IF_FALSE_BACK    10  'to 10'

 L. 299        82  LOAD_FAST                'l'
               84  STORE_FAST               'max_opt'
               86  JUMP_BACK            10  'to 10'
             88_0  COME_FROM            10  '10'

 L. 301        88  LOAD_FAST                'max_opt'
               90  LOAD_CONST               2
               92  BINARY_ADD       
               94  LOAD_CONST               2
               96  BINARY_ADD       
               98  LOAD_CONST               2
              100  BINARY_ADD       
              102  STORE_FAST               'opt_width'

 L. 325       104  LOAD_CONST               78
              106  STORE_FAST               'line_width'

 L. 326       108  LOAD_FAST                'line_width'
              110  LOAD_FAST                'opt_width'
              112  BINARY_SUBTRACT  
              114  STORE_FAST               'text_width'

 L. 327       116  LOAD_STR                 ' '
              118  LOAD_FAST                'opt_width'
              120  BINARY_MULTIPLY  
              122  STORE_FAST               'big_indent'

 L. 328       124  LOAD_FAST                'header'
              126  POP_JUMP_IF_FALSE   136  'to 136'

 L. 329       128  LOAD_FAST                'header'
              130  BUILD_LIST_1          1 
              132  STORE_FAST               'lines'
              134  JUMP_FORWARD        142  'to 142'
            136_0  COME_FROM           126  '126'

 L. 331       136  LOAD_STR                 'Option summary:'
              138  BUILD_LIST_1          1 
              140  STORE_FAST               'lines'
            142_0  COME_FROM           134  '134'

 L. 333       142  LOAD_FAST                'self'
              144  LOAD_ATTR                option_table
              146  GET_ITER         
            148_0  COME_FROM           356  '356'
              148  FOR_ITER            358  'to 358'
              150  STORE_FAST               'option'

 L. 334       152  LOAD_FAST                'option'
              154  LOAD_CONST               None
              156  LOAD_CONST               3
              158  BUILD_SLICE_2         2 
              160  BINARY_SUBSCR    
              162  UNPACK_SEQUENCE_3     3 
              164  STORE_FAST               'long'
              166  STORE_FAST               'short'
              168  STORE_FAST               'help'

 L. 335       170  LOAD_GLOBAL              wrap_text
              172  LOAD_FAST                'help'
              174  LOAD_FAST                'text_width'
              176  CALL_FUNCTION_2       2  ''
              178  STORE_FAST               'text'

 L. 336       180  LOAD_FAST                'long'
              182  LOAD_CONST               -1
              184  BINARY_SUBSCR    
              186  LOAD_STR                 '='
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   204  'to 204'

 L. 337       192  LOAD_FAST                'long'
              194  LOAD_CONST               0
              196  LOAD_CONST               -1
              198  BUILD_SLICE_2         2 
              200  BINARY_SUBSCR    
              202  STORE_FAST               'long'
            204_0  COME_FROM           190  '190'

 L. 340       204  LOAD_FAST                'short'
              206  LOAD_CONST               None
              208  <117>                 0  ''
          210_212  POP_JUMP_IF_FALSE   264  'to 264'

 L. 341       214  LOAD_FAST                'text'
              216  POP_JUMP_IF_FALSE   244  'to 244'

 L. 342       218  LOAD_FAST                'lines'
              220  LOAD_METHOD              append
              222  LOAD_STR                 '  --%-*s  %s'
              224  LOAD_FAST                'max_opt'
              226  LOAD_FAST                'long'
              228  LOAD_FAST                'text'
              230  LOAD_CONST               0
              232  BINARY_SUBSCR    
              234  BUILD_TUPLE_3         3 
              236  BINARY_MODULO    
              238  CALL_METHOD_1         1  ''
              240  POP_TOP          
              242  JUMP_FORWARD        262  'to 262'
            244_0  COME_FROM           216  '216'

 L. 344       244  LOAD_FAST                'lines'
              246  LOAD_METHOD              append
              248  LOAD_STR                 '  --%-*s  '
              250  LOAD_FAST                'max_opt'
              252  LOAD_FAST                'long'
              254  BUILD_TUPLE_2         2 
              256  BINARY_MODULO    
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          
            262_0  COME_FROM           242  '242'
              262  JUMP_FORWARD        322  'to 322'
            264_0  COME_FROM           210  '210'

 L. 349       264  LOAD_STR                 '%s (-%s)'
              266  LOAD_FAST                'long'
              268  LOAD_FAST                'short'
              270  BUILD_TUPLE_2         2 
              272  BINARY_MODULO    
              274  STORE_FAST               'opt_names'

 L. 350       276  LOAD_FAST                'text'
          278_280  POP_JUMP_IF_FALSE   308  'to 308'

 L. 351       282  LOAD_FAST                'lines'
              284  LOAD_METHOD              append
              286  LOAD_STR                 '  --%-*s  %s'

 L. 352       288  LOAD_FAST                'max_opt'
              290  LOAD_FAST                'opt_names'
              292  LOAD_FAST                'text'
              294  LOAD_CONST               0
              296  BINARY_SUBSCR    
              298  BUILD_TUPLE_3         3 

 L. 351       300  BINARY_MODULO    
              302  CALL_METHOD_1         1  ''
              304  POP_TOP          
              306  JUMP_FORWARD        322  'to 322'
            308_0  COME_FROM           278  '278'

 L. 354       308  LOAD_FAST                'lines'
              310  LOAD_METHOD              append
              312  LOAD_STR                 '  --%-*s'
              314  LOAD_FAST                'opt_names'
              316  BINARY_MODULO    
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          
            322_0  COME_FROM           306  '306'
            322_1  COME_FROM           262  '262'

 L. 356       322  LOAD_FAST                'text'
              324  LOAD_CONST               1
              326  LOAD_CONST               None
              328  BUILD_SLICE_2         2 
              330  BINARY_SUBSCR    
              332  GET_ITER         
            334_0  COME_FROM           352  '352'
              334  FOR_ITER            356  'to 356'
              336  STORE_FAST               'l'

 L. 357       338  LOAD_FAST                'lines'
              340  LOAD_METHOD              append
              342  LOAD_FAST                'big_indent'
              344  LOAD_FAST                'l'
              346  BINARY_ADD       
              348  CALL_METHOD_1         1  ''
              350  POP_TOP          
          352_354  JUMP_BACK           334  'to 334'
            356_0  COME_FROM           334  '334'
              356  JUMP_BACK           148  'to 148'
            358_0  COME_FROM           148  '148'

 L. 358       358  LOAD_FAST                'lines'
              360  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 62

    def print_help--- This code section failed: ---

 L. 361         0  LOAD_FAST                'file'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 362         8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                stdout
               12  STORE_FAST               'file'
             14_0  COME_FROM             6  '6'

 L. 363        14  LOAD_FAST                'self'
               16  LOAD_METHOD              generate_help
               18  LOAD_FAST                'header'
               20  CALL_METHOD_1         1  ''
               22  GET_ITER         
             24_0  COME_FROM            42  '42'
               24  FOR_ITER             44  'to 44'
               26  STORE_FAST               'line'

 L. 364        28  LOAD_FAST                'file'
               30  LOAD_METHOD              write
               32  LOAD_FAST                'line'
               34  LOAD_STR                 '\n'
               36  BINARY_ADD       
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          
               42  JUMP_BACK            24  'to 24'
             44_0  COME_FROM            24  '24'

Parse error at or near `None' instruction at offset -1


def fancy_getopt(options, negative_opt, object, args):
    parser = FancyGetopt(options)
    parser.set_negative_aliases(negative_opt)
    return parser.getopt(args, object)


WS_TRANS = {' ':ord(_wschar) for _wschar in string.whitespace}

def wrap_text--- This code section failed: ---

 L. 381         0  LOAD_FAST                'text'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 382         8  BUILD_LIST_0          0 
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 383        12  LOAD_GLOBAL              len
               14  LOAD_FAST                'text'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_FAST                'width'
               20  COMPARE_OP               <=
               22  POP_JUMP_IF_FALSE    30  'to 30'

 L. 384        24  LOAD_FAST                'text'
               26  BUILD_LIST_1          1 
               28  RETURN_VALUE     
             30_0  COME_FROM            22  '22'

 L. 386        30  LOAD_FAST                'text'
               32  LOAD_METHOD              expandtabs
               34  CALL_METHOD_0         0  ''
               36  STORE_FAST               'text'

 L. 387        38  LOAD_FAST                'text'
               40  LOAD_METHOD              translate
               42  LOAD_GLOBAL              WS_TRANS
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'text'

 L. 388        48  LOAD_GLOBAL              re
               50  LOAD_METHOD              split
               52  LOAD_STR                 '( +|-+)'
               54  LOAD_FAST                'text'
               56  CALL_METHOD_2         2  ''
               58  STORE_FAST               'chunks'

 L. 389        60  LOAD_LISTCOMP            '<code_object <listcomp>>'
               62  LOAD_STR                 'wrap_text.<locals>.<listcomp>'
               64  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               66  LOAD_FAST                'chunks'
               68  GET_ITER         
               70  CALL_FUNCTION_1       1  ''
               72  STORE_FAST               'chunks'

 L. 390        74  BUILD_LIST_0          0 
               76  STORE_FAST               'lines'
             78_0  COME_FROM           276  '276'

 L. 392        78  LOAD_FAST                'chunks'
            80_82  POP_JUMP_IF_FALSE   278  'to 278'

 L. 393        84  BUILD_LIST_0          0 
               86  STORE_FAST               'cur_line'

 L. 394        88  LOAD_CONST               0
               90  STORE_FAST               'cur_len'
             92_0  COME_FROM           178  '178'
             92_1  COME_FROM           148  '148'

 L. 396        92  LOAD_FAST                'chunks'
               94  POP_JUMP_IF_FALSE   180  'to 180'

 L. 397        96  LOAD_GLOBAL              len
               98  LOAD_FAST                'chunks'
              100  LOAD_CONST               0
              102  BINARY_SUBSCR    
              104  CALL_FUNCTION_1       1  ''
              106  STORE_FAST               'l'

 L. 398       108  LOAD_FAST                'cur_len'
              110  LOAD_FAST                'l'
              112  BINARY_ADD       
              114  LOAD_FAST                'width'
              116  COMPARE_OP               <=
              118  POP_JUMP_IF_FALSE   150  'to 150'

 L. 399       120  LOAD_FAST                'cur_line'
              122  LOAD_METHOD              append
              124  LOAD_FAST                'chunks'
              126  LOAD_CONST               0
              128  BINARY_SUBSCR    
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          

 L. 400       134  LOAD_FAST                'chunks'
              136  LOAD_CONST               0
              138  DELETE_SUBSCR    

 L. 401       140  LOAD_FAST                'cur_len'
              142  LOAD_FAST                'l'
              144  BINARY_ADD       
              146  STORE_FAST               'cur_len'
              148  JUMP_BACK            92  'to 92'
            150_0  COME_FROM           118  '118'

 L. 404       150  LOAD_FAST                'cur_line'
              152  POP_JUMP_IF_FALSE   180  'to 180'
              154  LOAD_FAST                'cur_line'
              156  LOAD_CONST               -1
              158  BINARY_SUBSCR    
              160  LOAD_CONST               0
              162  BINARY_SUBSCR    
              164  LOAD_STR                 ' '
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_FALSE   180  'to 180'

 L. 405       170  LOAD_FAST                'cur_line'
              172  LOAD_CONST               -1
              174  DELETE_SUBSCR    

 L. 406       176  JUMP_FORWARD        180  'to 180'
              178  JUMP_BACK            92  'to 92'
            180_0  COME_FROM           176  '176'
            180_1  COME_FROM           168  '168'
            180_2  COME_FROM           152  '152'
            180_3  COME_FROM            94  '94'

 L. 408       180  LOAD_FAST                'chunks'
          182_184  POP_JUMP_IF_FALSE   260  'to 260'

 L. 412       186  LOAD_FAST                'cur_len'
              188  LOAD_CONST               0
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_FALSE   236  'to 236'

 L. 413       194  LOAD_FAST                'cur_line'
              196  LOAD_METHOD              append
              198  LOAD_FAST                'chunks'
              200  LOAD_CONST               0
              202  BINARY_SUBSCR    
              204  LOAD_CONST               0
              206  LOAD_FAST                'width'
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 414       216  LOAD_FAST                'chunks'
              218  LOAD_CONST               0
              220  BINARY_SUBSCR    
              222  LOAD_FAST                'width'
              224  LOAD_CONST               None
              226  BUILD_SLICE_2         2 
              228  BINARY_SUBSCR    
              230  LOAD_FAST                'chunks'
              232  LOAD_CONST               0
              234  STORE_SUBSCR     
            236_0  COME_FROM           192  '192'

 L. 419       236  LOAD_FAST                'chunks'
              238  LOAD_CONST               0
              240  BINARY_SUBSCR    
              242  LOAD_CONST               0
              244  BINARY_SUBSCR    
              246  LOAD_STR                 ' '
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   260  'to 260'

 L. 420       254  LOAD_FAST                'chunks'
              256  LOAD_CONST               0
              258  DELETE_SUBSCR    
            260_0  COME_FROM           250  '250'
            260_1  COME_FROM           182  '182'

 L. 424       260  LOAD_FAST                'lines'
              262  LOAD_METHOD              append
              264  LOAD_STR                 ''
              266  LOAD_METHOD              join
              268  LOAD_FAST                'cur_line'
              270  CALL_METHOD_1         1  ''
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          
              276  JUMP_BACK            78  'to 78'
            278_0  COME_FROM            80  '80'

 L. 426       278  LOAD_FAST                'lines'
              280  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def translate_longopt(opt):
    """Convert a long option name to a valid Python identifier by
    changing "-" to "_".
    """
    return opt.translate(longopt_xlate)


class OptionDummy:
    __doc__ = 'Dummy class just used as a place to hold command-line option\n    values as instance attributes.'

    def __init__(self, options=[]):
        """Create a new OptionDummy instance.  The attributes listed in
        'options' will be initialized to None."""
        for opt in options:
            setattrselfoptNone


if __name__ == '__main__':
    text = 'Tra-la-la, supercalifragilisticexpialidocious.\nHow *do* you spell that odd word, anyways?\n(Someone ask Mary -- she\'ll know [or she\'ll\nsay, "How should I know?"].)'
    for w in (10, 20, 30, 40):
        print('width: %d' % w)
        print('\n'.join(wrap_text(text, w)))
        print()