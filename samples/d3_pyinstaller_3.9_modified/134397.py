# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: attr\_funcs.py
from __future__ import absolute_import, division, print_function
import copy
from ._compat import iteritems
from ._make import NOTHING, _obj_setattr, fields
from .exceptions import AttrsAttributeNotFoundError

def asdict--- This code section failed: ---

 L.  50         0  LOAD_GLOBAL              fields
                2  LOAD_FAST                'inst'
                4  LOAD_ATTR                __class__
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'attrs'

 L.  51        10  LOAD_DEREF               'dict_factory'
               12  CALL_FUNCTION_0       0  ''
               14  STORE_FAST               'rv'

 L.  52        16  LOAD_FAST                'attrs'
               18  GET_ITER         
             20_0  COME_FROM           270  '270'
             20_1  COME_FROM           258  '258'
             20_2  COME_FROM            54  '54'
               20  FOR_ITER            272  'to 272'
               22  STORE_FAST               'a'

 L.  53        24  LOAD_GLOBAL              getattr
               26  LOAD_FAST                'inst'
               28  LOAD_FAST                'a'
               30  LOAD_ATTR                name
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'v'

 L.  54        36  LOAD_DEREF               'filter'
               38  LOAD_CONST               None
               40  <117>                 1  ''
               42  POP_JUMP_IF_FALSE    56  'to 56'
               44  LOAD_DEREF               'filter'
               46  LOAD_FAST                'a'
               48  LOAD_FAST                'v'
               50  CALL_FUNCTION_2       2  ''
               52  POP_JUMP_IF_TRUE     56  'to 56'

 L.  55        54  JUMP_BACK            20  'to 20'
             56_0  COME_FROM            52  '52'
             56_1  COME_FROM            42  '42'

 L.  57        56  LOAD_DEREF               'value_serializer'
               58  LOAD_CONST               None
               60  <117>                 1  ''
               62  POP_JUMP_IF_FALSE    76  'to 76'

 L.  58        64  LOAD_DEREF               'value_serializer'
               66  LOAD_FAST                'inst'
               68  LOAD_FAST                'a'
               70  LOAD_FAST                'v'
               72  CALL_FUNCTION_3       3  ''
               74  STORE_FAST               'v'
             76_0  COME_FROM            62  '62'

 L.  60        76  LOAD_FAST                'recurse'
               78  LOAD_CONST               True
               80  <117>                 0  ''
            82_84  POP_JUMP_IF_FALSE   260  'to 260'

 L.  61        86  LOAD_GLOBAL              has
               88  LOAD_FAST                'v'
               90  LOAD_ATTR                __class__
               92  CALL_FUNCTION_1       1  ''
               94  POP_JUMP_IF_FALSE   122  'to 122'

 L.  62        96  LOAD_GLOBAL              asdict

 L.  63        98  LOAD_FAST                'v'

 L.  64       100  LOAD_CONST               True

 L.  65       102  LOAD_DEREF               'filter'

 L.  66       104  LOAD_DEREF               'dict_factory'

 L.  67       106  LOAD_DEREF               'retain_collection_types'

 L.  68       108  LOAD_DEREF               'value_serializer'

 L.  62       110  CALL_FUNCTION_6       6  ''
              112  LOAD_FAST                'rv'
              114  LOAD_FAST                'a'
              116  LOAD_ATTR                name
              118  STORE_SUBSCR     
              120  JUMP_FORWARD        258  'to 258'
            122_0  COME_FROM            94  '94'

 L.  70       122  LOAD_GLOBAL              isinstance
              124  LOAD_FAST                'v'
              126  LOAD_GLOBAL              tuple
              128  LOAD_GLOBAL              list
              130  LOAD_GLOBAL              set
              132  LOAD_GLOBAL              frozenset
              134  BUILD_TUPLE_4         4 
              136  CALL_FUNCTION_2       2  ''
              138  POP_JUMP_IF_FALSE   194  'to 194'

 L.  71       140  LOAD_DEREF               'retain_collection_types'
              142  LOAD_CONST               True
              144  <117>                 0  ''
              146  POP_JUMP_IF_FALSE   154  'to 154'
              148  LOAD_FAST                'v'
              150  LOAD_ATTR                __class__
              152  JUMP_FORWARD        156  'to 156'
            154_0  COME_FROM           146  '146'
              154  LOAD_GLOBAL              list
            156_0  COME_FROM           152  '152'
              156  STORE_FAST               'cf'

 L.  72       158  LOAD_FAST                'cf'

 L.  73       160  LOAD_CLOSURE             'dict_factory'
              162  LOAD_CLOSURE             'filter'
              164  LOAD_CLOSURE             'retain_collection_types'
              166  LOAD_CLOSURE             'value_serializer'
              168  BUILD_TUPLE_4         4 
              170  LOAD_LISTCOMP            '<code_object <listcomp>>'
              172  LOAD_STR                 'asdict.<locals>.<listcomp>'
              174  MAKE_FUNCTION_8          'closure'

 L.  81       176  LOAD_FAST                'v'

 L.  73       178  GET_ITER         
              180  CALL_FUNCTION_1       1  ''

 L.  72       182  CALL_FUNCTION_1       1  ''
              184  LOAD_FAST                'rv'
              186  LOAD_FAST                'a'
              188  LOAD_ATTR                name
              190  STORE_SUBSCR     
              192  JUMP_FORWARD        258  'to 258'
            194_0  COME_FROM           138  '138'

 L.  84       194  LOAD_GLOBAL              isinstance
              196  LOAD_FAST                'v'
              198  LOAD_GLOBAL              dict
              200  CALL_FUNCTION_2       2  ''
              202  POP_JUMP_IF_FALSE   248  'to 248'

 L.  85       204  LOAD_DEREF               'dict_factory'
              206  STORE_DEREF              'df'

 L.  86       208  LOAD_DEREF               'df'
              210  LOAD_CLOSURE             'df'
              212  LOAD_CLOSURE             'filter'
              214  LOAD_CLOSURE             'retain_collection_types'
              216  LOAD_CLOSURE             'value_serializer'
              218  BUILD_TUPLE_4         4 
              220  LOAD_GENEXPR             '<code_object <genexpr>>'
              222  LOAD_STR                 'asdict.<locals>.<genexpr>'
              224  MAKE_FUNCTION_8          'closure'

 L. 103       226  LOAD_GLOBAL              iteritems
              228  LOAD_FAST                'v'
              230  CALL_FUNCTION_1       1  ''

 L.  86       232  GET_ITER         
              234  CALL_FUNCTION_1       1  ''
              236  CALL_FUNCTION_1       1  ''
              238  LOAD_FAST                'rv'
              240  LOAD_FAST                'a'
              242  LOAD_ATTR                name
              244  STORE_SUBSCR     
              246  JUMP_FORWARD        258  'to 258'
            248_0  COME_FROM           202  '202'

 L. 106       248  LOAD_FAST                'v'
              250  LOAD_FAST                'rv'
              252  LOAD_FAST                'a'
              254  LOAD_ATTR                name
              256  STORE_SUBSCR     
            258_0  COME_FROM           246  '246'
            258_1  COME_FROM           192  '192'
            258_2  COME_FROM           120  '120'
              258  JUMP_BACK            20  'to 20'
            260_0  COME_FROM            82  '82'

 L. 108       260  LOAD_FAST                'v'
              262  LOAD_FAST                'rv'
              264  LOAD_FAST                'a'
              266  LOAD_ATTR                name
              268  STORE_SUBSCR     
              270  JUMP_BACK            20  'to 20'
            272_0  COME_FROM            20  '20'

 L. 109       272  LOAD_FAST                'rv'
              274  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 40


def _asdict_anything--- This code section failed: ---

 L. 122         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'val'
                4  LOAD_ATTR                __class__
                6  LOAD_STR                 '__attrs_attrs__'
                8  LOAD_CONST               None
               10  CALL_FUNCTION_3       3  ''
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    38  'to 38'

 L. 124        18  LOAD_GLOBAL              asdict

 L. 125        20  LOAD_FAST                'val'

 L. 126        22  LOAD_CONST               True

 L. 127        24  LOAD_DEREF               'filter'

 L. 128        26  LOAD_DEREF               'dict_factory'

 L. 129        28  LOAD_DEREF               'retain_collection_types'

 L. 130        30  LOAD_DEREF               'value_serializer'

 L. 124        32  CALL_FUNCTION_6       6  ''
               34  STORE_FAST               'rv'
               36  JUMP_FORWARD        176  'to 176'
             38_0  COME_FROM            16  '16'

 L. 132        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'val'
               42  LOAD_GLOBAL              tuple
               44  LOAD_GLOBAL              list
               46  LOAD_GLOBAL              set
               48  LOAD_GLOBAL              frozenset
               50  BUILD_TUPLE_4         4 
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_FALSE   104  'to 104'

 L. 133        56  LOAD_DEREF               'retain_collection_types'
               58  LOAD_CONST               True
               60  <117>                 0  ''
               62  POP_JUMP_IF_FALSE    70  'to 70'
               64  LOAD_FAST                'val'
               66  LOAD_ATTR                __class__
               68  JUMP_FORWARD         72  'to 72'
             70_0  COME_FROM            62  '62'
               70  LOAD_GLOBAL              list
             72_0  COME_FROM            68  '68'
               72  STORE_FAST               'cf'

 L. 134        74  LOAD_FAST                'cf'

 L. 135        76  LOAD_CLOSURE             'dict_factory'
               78  LOAD_CLOSURE             'filter'
               80  LOAD_CLOSURE             'retain_collection_types'
               82  LOAD_CLOSURE             'value_serializer'
               84  BUILD_TUPLE_4         4 
               86  LOAD_LISTCOMP            '<code_object <listcomp>>'
               88  LOAD_STR                 '_asdict_anything.<locals>.<listcomp>'
               90  MAKE_FUNCTION_8          'closure'

 L. 143        92  LOAD_FAST                'val'

 L. 135        94  GET_ITER         
               96  CALL_FUNCTION_1       1  ''

 L. 134        98  CALL_FUNCTION_1       1  ''
              100  STORE_FAST               'rv'
              102  JUMP_FORWARD        176  'to 176'
            104_0  COME_FROM            54  '54'

 L. 146       104  LOAD_GLOBAL              isinstance
              106  LOAD_FAST                'val'
              108  LOAD_GLOBAL              dict
              110  CALL_FUNCTION_2       2  ''
              112  POP_JUMP_IF_FALSE   152  'to 152'

 L. 147       114  LOAD_DEREF               'dict_factory'
              116  STORE_DEREF              'df'

 L. 148       118  LOAD_DEREF               'df'
              120  LOAD_CLOSURE             'df'
              122  LOAD_CLOSURE             'filter'
              124  LOAD_CLOSURE             'retain_collection_types'
              126  LOAD_CLOSURE             'value_serializer'
              128  BUILD_TUPLE_4         4 
              130  LOAD_GENEXPR             '<code_object <genexpr>>'
              132  LOAD_STR                 '_asdict_anything.<locals>.<genexpr>'
              134  MAKE_FUNCTION_8          'closure'

 L. 157       136  LOAD_GLOBAL              iteritems
              138  LOAD_FAST                'val'
              140  CALL_FUNCTION_1       1  ''

 L. 148       142  GET_ITER         
              144  CALL_FUNCTION_1       1  ''
              146  CALL_FUNCTION_1       1  ''
              148  STORE_FAST               'rv'
              150  JUMP_FORWARD        176  'to 176'
            152_0  COME_FROM           112  '112'

 L. 160       152  LOAD_FAST                'val'
              154  STORE_FAST               'rv'

 L. 161       156  LOAD_DEREF               'value_serializer'
              158  LOAD_CONST               None
              160  <117>                 1  ''
              162  POP_JUMP_IF_FALSE   176  'to 176'

 L. 162       164  LOAD_DEREF               'value_serializer'
              166  LOAD_CONST               None
              168  LOAD_CONST               None
              170  LOAD_FAST                'rv'
              172  CALL_FUNCTION_3       3  ''
              174  STORE_FAST               'rv'
            176_0  COME_FROM           162  '162'
            176_1  COME_FROM           150  '150'
            176_2  COME_FROM           102  '102'
            176_3  COME_FROM            36  '36'

 L. 164       176  LOAD_FAST                'rv'
              178  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def astuple--- This code section failed: ---

 L. 200         0  LOAD_GLOBAL              fields
                2  LOAD_FAST                'inst'
                4  LOAD_ATTR                __class__
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'attrs'

 L. 201        10  BUILD_LIST_0          0 
               12  STORE_FAST               'rv'

 L. 202        14  LOAD_FAST                'retain_collection_types'
               16  STORE_DEREF              'retain'

 L. 203        18  LOAD_FAST                'attrs'
               20  GET_ITER         
             22_0  COME_FROM           258  '258'
             22_1  COME_FROM           246  '246'
             22_2  COME_FROM            56  '56'
               22  FOR_ITER            260  'to 260'
               24  STORE_FAST               'a'

 L. 204        26  LOAD_GLOBAL              getattr
               28  LOAD_FAST                'inst'
               30  LOAD_FAST                'a'
               32  LOAD_ATTR                name
               34  CALL_FUNCTION_2       2  ''
               36  STORE_FAST               'v'

 L. 205        38  LOAD_DEREF               'filter'
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    58  'to 58'
               46  LOAD_DEREF               'filter'
               48  LOAD_FAST                'a'
               50  LOAD_FAST                'v'
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_TRUE     58  'to 58'

 L. 206        56  JUMP_BACK            22  'to 22'
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            44  '44'

 L. 207        58  LOAD_FAST                'recurse'
               60  LOAD_CONST               True
               62  <117>                 0  ''
               64  POP_JUMP_IF_FALSE   248  'to 248'

 L. 208        66  LOAD_GLOBAL              has
               68  LOAD_FAST                'v'
               70  LOAD_ATTR                __class__
               72  CALL_FUNCTION_1       1  ''
               74  POP_JUMP_IF_FALSE   102  'to 102'

 L. 209        76  LOAD_FAST                'rv'
               78  LOAD_METHOD              append

 L. 210        80  LOAD_GLOBAL              astuple

 L. 211        82  LOAD_FAST                'v'

 L. 212        84  LOAD_CONST               True

 L. 213        86  LOAD_DEREF               'filter'

 L. 214        88  LOAD_DEREF               'tuple_factory'

 L. 215        90  LOAD_DEREF               'retain'

 L. 210        92  LOAD_CONST               ('recurse', 'filter', 'tuple_factory', 'retain_collection_types')
               94  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'

 L. 209        96  CALL_METHOD_1         1  ''
               98  POP_TOP          
              100  JUMP_FORWARD        246  'to 246'
            102_0  COME_FROM            74  '74'

 L. 218       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                'v'
              106  LOAD_GLOBAL              tuple
              108  LOAD_GLOBAL              list
              110  LOAD_GLOBAL              set
              112  LOAD_GLOBAL              frozenset
              114  BUILD_TUPLE_4         4 
              116  CALL_FUNCTION_2       2  ''
              118  POP_JUMP_IF_FALSE   172  'to 172'

 L. 219       120  LOAD_DEREF               'retain'
              122  LOAD_CONST               True
              124  <117>                 0  ''
              126  POP_JUMP_IF_FALSE   134  'to 134'
              128  LOAD_FAST                'v'
              130  LOAD_ATTR                __class__
              132  JUMP_FORWARD        136  'to 136'
            134_0  COME_FROM           126  '126'
              134  LOAD_GLOBAL              list
            136_0  COME_FROM           132  '132'
              136  STORE_FAST               'cf'

 L. 220       138  LOAD_FAST                'rv'
              140  LOAD_METHOD              append

 L. 221       142  LOAD_FAST                'cf'

 L. 222       144  LOAD_CLOSURE             'filter'
              146  LOAD_CLOSURE             'retain'
              148  LOAD_CLOSURE             'tuple_factory'
              150  BUILD_TUPLE_3         3 
              152  LOAD_LISTCOMP            '<code_object <listcomp>>'
              154  LOAD_STR                 'astuple.<locals>.<listcomp>'
              156  MAKE_FUNCTION_8          'closure'

 L. 232       158  LOAD_FAST                'v'

 L. 222       160  GET_ITER         
              162  CALL_FUNCTION_1       1  ''

 L. 221       164  CALL_FUNCTION_1       1  ''

 L. 220       166  CALL_METHOD_1         1  ''
              168  POP_TOP          
              170  JUMP_FORWARD        246  'to 246'
            172_0  COME_FROM           118  '118'

 L. 236       172  LOAD_GLOBAL              isinstance
              174  LOAD_FAST                'v'
              176  LOAD_GLOBAL              dict
              178  CALL_FUNCTION_2       2  ''
              180  POP_JUMP_IF_FALSE   236  'to 236'

 L. 237       182  LOAD_DEREF               'retain'
              184  LOAD_CONST               True
              186  <117>                 0  ''
              188  POP_JUMP_IF_FALSE   196  'to 196'
              190  LOAD_FAST                'v'
              192  LOAD_ATTR                __class__
              194  JUMP_FORWARD        198  'to 198'
            196_0  COME_FROM           188  '188'
              196  LOAD_GLOBAL              dict
            198_0  COME_FROM           194  '194'
              198  STORE_FAST               'df'

 L. 238       200  LOAD_FAST                'rv'
              202  LOAD_METHOD              append

 L. 239       204  LOAD_FAST                'df'
              206  LOAD_CLOSURE             'retain'
              208  LOAD_CLOSURE             'tuple_factory'
              210  BUILD_TUPLE_2         2 
              212  LOAD_GENEXPR             '<code_object <genexpr>>'
              214  LOAD_STR                 'astuple.<locals>.<genexpr>'
              216  MAKE_FUNCTION_8          'closure'

 L. 256       218  LOAD_GLOBAL              iteritems
              220  LOAD_FAST                'v'
              222  CALL_FUNCTION_1       1  ''

 L. 239       224  GET_ITER         
              226  CALL_FUNCTION_1       1  ''
              228  CALL_FUNCTION_1       1  ''

 L. 238       230  CALL_METHOD_1         1  ''
              232  POP_TOP          
              234  JUMP_FORWARD        246  'to 246'
            236_0  COME_FROM           180  '180'

 L. 260       236  LOAD_FAST                'rv'
              238  LOAD_METHOD              append
              240  LOAD_FAST                'v'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          
            246_0  COME_FROM           234  '234'
            246_1  COME_FROM           170  '170'
            246_2  COME_FROM           100  '100'
              246  JUMP_BACK            22  'to 22'
            248_0  COME_FROM            64  '64'

 L. 262       248  LOAD_FAST                'rv'
              250  LOAD_METHOD              append
              252  LOAD_FAST                'v'
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          
              258  JUMP_BACK            22  'to 22'
            260_0  COME_FROM            22  '22'

 L. 264       260  LOAD_DEREF               'tuple_factory'
              262  LOAD_GLOBAL              list
              264  <117>                 0  ''
          266_268  POP_JUMP_IF_FALSE   274  'to 274'
              270  LOAD_FAST                'rv'
              272  RETURN_VALUE     
            274_0  COME_FROM           266  '266'
              274  LOAD_DEREF               'tuple_factory'
              276  LOAD_FAST                'rv'
              278  CALL_FUNCTION_1       1  ''
              280  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 42


def has--- This code section failed: ---

 L. 276         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'cls'
                4  LOAD_STR                 '__attrs_attrs__'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  ''
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def assoc--- This code section failed: ---

 L. 296         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              warnings
                6  STORE_FAST               'warnings'

 L. 298         8  LOAD_FAST                'warnings'
               10  LOAD_ATTR                warn

 L. 299        12  LOAD_STR                 'assoc is deprecated and will be removed after 2018/01.'

 L. 300        14  LOAD_GLOBAL              DeprecationWarning

 L. 301        16  LOAD_CONST               2

 L. 298        18  LOAD_CONST               ('stacklevel',)
               20  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               22  POP_TOP          

 L. 303        24  LOAD_GLOBAL              copy
               26  LOAD_METHOD              copy
               28  LOAD_FAST                'inst'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'new'

 L. 304        34  LOAD_GLOBAL              fields
               36  LOAD_FAST                'inst'
               38  LOAD_ATTR                __class__
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'attrs'

 L. 305        44  LOAD_GLOBAL              iteritems
               46  LOAD_FAST                'changes'
               48  CALL_FUNCTION_1       1  ''
               50  GET_ITER         
             52_0  COME_FROM           112  '112'
               52  FOR_ITER            114  'to 114'
               54  UNPACK_SEQUENCE_2     2 
               56  STORE_FAST               'k'
               58  STORE_FAST               'v'

 L. 306        60  LOAD_GLOBAL              getattr
               62  LOAD_FAST                'attrs'
               64  LOAD_FAST                'k'
               66  LOAD_GLOBAL              NOTHING
               68  CALL_FUNCTION_3       3  ''
               70  STORE_FAST               'a'

 L. 307        72  LOAD_FAST                'a'
               74  LOAD_GLOBAL              NOTHING
               76  <117>                 0  ''
               78  POP_JUMP_IF_FALSE   100  'to 100'

 L. 308        80  LOAD_GLOBAL              AttrsAttributeNotFoundError

 L. 309        82  LOAD_STR                 '{k} is not an attrs attribute on {cl}.'
               84  LOAD_ATTR                format

 L. 310        86  LOAD_FAST                'k'
               88  LOAD_FAST                'new'
               90  LOAD_ATTR                __class__

 L. 309        92  LOAD_CONST               ('k', 'cl')
               94  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 308        96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            78  '78'

 L. 313       100  LOAD_GLOBAL              _obj_setattr
              102  LOAD_FAST                'new'
              104  LOAD_FAST                'k'
              106  LOAD_FAST                'v'
              108  CALL_FUNCTION_3       3  ''
              110  POP_TOP          
              112  JUMP_BACK            52  'to 52'
            114_0  COME_FROM            52  '52'

 L. 314       114  LOAD_FAST                'new'
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 76


def evolve--- This code section failed: ---

 L. 333         0  LOAD_FAST                'inst'
                2  LOAD_ATTR                __class__
                4  STORE_FAST               'cls'

 L. 334         6  LOAD_GLOBAL              fields
                8  LOAD_FAST                'cls'
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'attrs'

 L. 335        14  LOAD_FAST                'attrs'
               16  GET_ITER         
             18_0  COME_FROM            86  '86'
             18_1  COME_FROM            70  '70'
             18_2  COME_FROM            28  '28'
               18  FOR_ITER             88  'to 88'
               20  STORE_FAST               'a'

 L. 336        22  LOAD_FAST                'a'
               24  LOAD_ATTR                init
               26  POP_JUMP_IF_TRUE     30  'to 30'

 L. 337        28  JUMP_BACK            18  'to 18'
             30_0  COME_FROM            26  '26'

 L. 338        30  LOAD_FAST                'a'
               32  LOAD_ATTR                name
               34  STORE_FAST               'attr_name'

 L. 339        36  LOAD_FAST                'attr_name'
               38  LOAD_CONST               0
               40  BINARY_SUBSCR    
               42  LOAD_STR                 '_'
               44  COMPARE_OP               !=
               46  POP_JUMP_IF_FALSE    52  'to 52'
               48  LOAD_FAST                'attr_name'
               50  JUMP_FORWARD         62  'to 62'
             52_0  COME_FROM            46  '46'
               52  LOAD_FAST                'attr_name'
               54  LOAD_CONST               1
               56  LOAD_CONST               None
               58  BUILD_SLICE_2         2 
               60  BINARY_SUBSCR    
             62_0  COME_FROM            50  '50'
               62  STORE_FAST               'init_name'

 L. 340        64  LOAD_FAST                'init_name'
               66  LOAD_FAST                'changes'
               68  <118>                 1  ''
               70  POP_JUMP_IF_FALSE_BACK    18  'to 18'

 L. 341        72  LOAD_GLOBAL              getattr
               74  LOAD_FAST                'inst'
               76  LOAD_FAST                'attr_name'
               78  CALL_FUNCTION_2       2  ''
               80  LOAD_FAST                'changes'
               82  LOAD_FAST                'init_name'
               84  STORE_SUBSCR     
               86  JUMP_BACK            18  'to 18'
             88_0  COME_FROM            18  '18'

 L. 343        88  LOAD_FAST                'cls'
               90  BUILD_TUPLE_0         0 
               92  BUILD_MAP_0           0 
               94  LOAD_FAST                'changes'
               96  <164>                 1  ''
               98  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              100  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 68


def resolve_types--- This code section failed: ---

 L. 380         0  SETUP_FINALLY        12  'to 12'

 L. 383         2  LOAD_FAST                'cls'
                4  LOAD_ATTR                __attrs_types_resolved__
                6  POP_TOP          
                8  POP_BLOCK        
               10  JUMP_FORWARD        114  'to 114'
             12_0  COME_FROM_FINALLY     0  '0'

 L. 384        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  <121>               112  ''
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 385        24  LOAD_CONST               0
               26  LOAD_CONST               None
               28  IMPORT_NAME              typing
               30  STORE_FAST               'typing'

 L. 387        32  LOAD_FAST                'typing'
               34  LOAD_ATTR                get_type_hints
               36  LOAD_FAST                'cls'
               38  LOAD_FAST                'globalns'
               40  LOAD_FAST                'localns'
               42  LOAD_CONST               ('globalns', 'localns')
               44  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               46  STORE_FAST               'hints'

 L. 388        48  LOAD_FAST                'attribs'
               50  LOAD_CONST               None
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    64  'to 64'
               56  LOAD_GLOBAL              fields
               58  LOAD_FAST                'cls'
               60  CALL_FUNCTION_1       1  ''
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            54  '54'
               64  LOAD_FAST                'attribs'
             66_0  COME_FROM            62  '62'
               66  GET_ITER         
             68_0  COME_FROM           100  '100'
             68_1  COME_FROM            80  '80'
               68  FOR_ITER            102  'to 102'
               70  STORE_FAST               'field'

 L. 389        72  LOAD_FAST                'field'
               74  LOAD_ATTR                name
               76  LOAD_FAST                'hints'
               78  <118>                 0  ''
               80  POP_JUMP_IF_FALSE_BACK    68  'to 68'

 L. 391        82  LOAD_GLOBAL              _obj_setattr
               84  LOAD_FAST                'field'
               86  LOAD_STR                 'type'
               88  LOAD_FAST                'hints'
               90  LOAD_FAST                'field'
               92  LOAD_ATTR                name
               94  BINARY_SUBSCR    
               96  CALL_FUNCTION_3       3  ''
               98  POP_TOP          
              100  JUMP_BACK            68  'to 68'
            102_0  COME_FROM            68  '68'

 L. 392       102  LOAD_CONST               True
              104  LOAD_FAST                'cls'
              106  STORE_ATTR               __attrs_types_resolved__
              108  POP_EXCEPT       
              110  JUMP_FORWARD        114  'to 114'
              112  <48>             
            114_0  COME_FROM           110  '110'
            114_1  COME_FROM            10  '10'

 L. 395       114  LOAD_FAST                'cls'
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 16