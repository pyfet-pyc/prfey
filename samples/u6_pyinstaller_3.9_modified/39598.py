# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: charset_normalizer\cd.py
from codecs import IncrementalDecoder
from functools import lru_cache
from typing import List, Set, Optional, Tuple, Dict
import importlib
from charset_normalizer.models import CoherenceMatches
from charset_normalizer.utils import unicode_range, is_unicode_range_secondary, is_multi_byte_encoding
from charset_normalizer.md import is_suspiciously_successive_range
from charset_normalizer.assets import FREQUENCIES
from collections import Counter

def encoding_unicode_range--- This code section failed: ---

 L.  17         0  LOAD_GLOBAL              is_multi_byte_encoding
                2  LOAD_FAST                'iana_name'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  18         8  LOAD_GLOBAL              IOError
               10  LOAD_STR                 'Function not supported on multi-byte code page'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  20        16  LOAD_GLOBAL              importlib
               18  LOAD_METHOD              import_module
               20  LOAD_STR                 'encodings.{}'
               22  LOAD_METHOD              format
               24  LOAD_FAST                'iana_name'
               26  CALL_METHOD_1         1  ''
               28  CALL_METHOD_1         1  ''
               30  LOAD_ATTR                IncrementalDecoder
               32  STORE_FAST               'decoder'

 L.  22        34  LOAD_FAST                'decoder'
               36  LOAD_STR                 'ignore'
               38  LOAD_CONST               ('errors',)
               40  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               42  STORE_FAST               'p'

 L.  23        44  LOAD_GLOBAL              set
               46  CALL_FUNCTION_0       0  ''
               48  STORE_FAST               'seen_ranges'

 L.  25        50  LOAD_GLOBAL              range
               52  LOAD_CONST               48
               54  LOAD_CONST               255
               56  CALL_FUNCTION_2       2  ''
               58  GET_ITER         
             60_0  COME_FROM           112  '112'
             60_1  COME_FROM            82  '82'
               60  FOR_ITER            126  'to 126'
               62  STORE_FAST               'i'

 L.  26        64  LOAD_FAST                'p'
               66  LOAD_METHOD              decode

 L.  27        68  LOAD_GLOBAL              bytes
               70  LOAD_FAST                'i'
               72  BUILD_LIST_1          1 
               74  CALL_FUNCTION_1       1  ''

 L.  26        76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'chunk'

 L.  30        80  LOAD_FAST                'chunk'
               82  POP_JUMP_IF_FALSE    60  'to 60'

 L.  31        84  LOAD_GLOBAL              unicode_range
               86  LOAD_FAST                'chunk'
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'character_range'

 L.  33        92  LOAD_FAST                'character_range'
               94  LOAD_CONST               None
               96  <117>                 0  ''
               98  POP_JUMP_IF_FALSE   102  'to 102'

 L.  34       100  JUMP_BACK            60  'to 60'
            102_0  COME_FROM            98  '98'

 L.  36       102  LOAD_GLOBAL              is_unicode_range_secondary
              104  LOAD_FAST                'character_range'
              106  CALL_FUNCTION_1       1  ''
              108  LOAD_CONST               False
              110  <117>                 0  ''
              112  POP_JUMP_IF_FALSE    60  'to 60'

 L.  37       114  LOAD_FAST                'seen_ranges'
              116  LOAD_METHOD              add
              118  LOAD_FAST                'character_range'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
              124  JUMP_BACK            60  'to 60'

 L.  39       126  LOAD_GLOBAL              sorted
              128  LOAD_GLOBAL              list
              130  LOAD_FAST                'seen_ranges'
              132  CALL_FUNCTION_1       1  ''
              134  CALL_FUNCTION_1       1  ''
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 96


def unicode_range_languages--- This code section failed: ---

 L.  46         0  BUILD_LIST_0          0 
                2  STORE_FAST               'languages'

 L.  48         4  LOAD_GLOBAL              FREQUENCIES
                6  LOAD_METHOD              items
                8  CALL_METHOD_0         0  ''
               10  GET_ITER         
               12  FOR_ITER             58  'to 58'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'language'
               18  STORE_FAST               'characters'

 L.  49        20  LOAD_FAST                'characters'
               22  GET_ITER         
             24_0  COME_FROM            38  '38'
               24  FOR_ITER             56  'to 56'
               26  STORE_FAST               'character'

 L.  50        28  LOAD_GLOBAL              unicode_range
               30  LOAD_FAST                'character'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_FAST                'primary_range'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    24  'to 24'

 L.  51        40  LOAD_FAST                'languages'
               42  LOAD_METHOD              append
               44  LOAD_FAST                'language'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L.  52        50  POP_TOP          
               52  CONTINUE             12  'to 12'
               54  JUMP_BACK            24  'to 24'
               56  JUMP_BACK            12  'to 12'

 L.  54        58  LOAD_FAST                'languages'
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 52


@lru_cache()
def encoding_languages--- This code section failed: ---

 L.  63         0  LOAD_GLOBAL              encoding_unicode_range
                2  LOAD_FAST                'iana_name'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'unicode_ranges'

 L.  64         8  LOAD_CONST               None
               10  STORE_FAST               'primary_range'

 L.  66        12  LOAD_FAST                'unicode_ranges'
               14  GET_ITER         
             16_0  COME_FROM            26  '26'
               16  FOR_ITER             38  'to 38'
               18  STORE_FAST               'specified_range'

 L.  67        20  LOAD_STR                 'Latin'
               22  LOAD_FAST                'specified_range'
               24  <118>                 1  ''
               26  POP_JUMP_IF_FALSE    16  'to 16'

 L.  68        28  LOAD_FAST                'specified_range'
               30  STORE_FAST               'primary_range'

 L.  69        32  POP_TOP          
               34  BREAK_LOOP           38  'to 38'
               36  JUMP_BACK            16  'to 16'

 L.  71        38  LOAD_FAST                'primary_range'
               40  LOAD_CONST               None
               42  <117>                 0  ''
               44  POP_JUMP_IF_FALSE    52  'to 52'

 L.  72        46  LOAD_STR                 'Latin Based'
               48  BUILD_LIST_1          1 
               50  RETURN_VALUE     
             52_0  COME_FROM            44  '44'

 L.  74        52  LOAD_GLOBAL              unicode_range_languages
               54  LOAD_FAST                'primary_range'
               56  CALL_FUNCTION_1       1  ''
               58  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 24


def mb_encoding_languages--- This code section failed: ---

 L.  82         0  LOAD_FAST                'iana_name'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 'shift_'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     38  'to 38'
               10  LOAD_FAST                'iana_name'
               12  LOAD_METHOD              startswith
               14  LOAD_STR                 'iso2022_jp'
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_TRUE     38  'to 38'
               20  LOAD_FAST                'iana_name'
               22  LOAD_METHOD              startswith
               24  LOAD_STR                 'euc_j'
               26  CALL_METHOD_1         1  ''
               28  POP_JUMP_IF_TRUE     38  'to 38'
               30  LOAD_FAST                'iana_name'
               32  LOAD_CONST               frozenset({'cp932'})
               34  <118>                 0  ''
               36  POP_JUMP_IF_FALSE    44  'to 44'
             38_0  COME_FROM            28  '28'
             38_1  COME_FROM            18  '18'
             38_2  COME_FROM             8  '8'

 L.  83        38  LOAD_STR                 'Japanese'
               40  BUILD_LIST_1          1 
               42  RETURN_VALUE     
             44_0  COME_FROM            36  '36'

 L.  84        44  LOAD_FAST                'iana_name'
               46  LOAD_METHOD              startswith
               48  LOAD_STR                 'gb'
               50  CALL_METHOD_1         1  ''
               52  POP_JUMP_IF_TRUE     62  'to 62'
               54  LOAD_FAST                'iana_name'
               56  LOAD_CONST               frozenset({'cp950', 'big5', 'big5hkscs'})
               58  <118>                 0  ''
               60  POP_JUMP_IF_FALSE    70  'to 70'
             62_0  COME_FROM            52  '52'

 L.  85        62  LOAD_STR                 'Chinese'
               64  LOAD_STR                 'Classical Chinese'
               66  BUILD_LIST_2          2 
               68  RETURN_VALUE     
             70_0  COME_FROM            60  '60'

 L.  86        70  LOAD_FAST                'iana_name'
               72  LOAD_METHOD              startswith
               74  LOAD_STR                 'iso2022_kr'
               76  CALL_METHOD_1         1  ''
               78  POP_JUMP_IF_TRUE     88  'to 88'
               80  LOAD_FAST                'iana_name'
               82  LOAD_CONST               frozenset({'euc_kr', 'cp949', 'johab'})
               84  <118>                 0  ''
               86  POP_JUMP_IF_FALSE    94  'to 94'
             88_0  COME_FROM            78  '78'

 L.  87        88  LOAD_STR                 'Korean'
               90  BUILD_LIST_1          1 
               92  RETURN_VALUE     
             94_0  COME_FROM            86  '86'

 L.  89        94  BUILD_LIST_0          0 
               96  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def alphabet_languages--- This code section failed: ---

 L.  96         0  BUILD_LIST_0          0 
                2  STORE_FAST               'languages'

 L.  98         4  LOAD_GLOBAL              FREQUENCIES
                6  LOAD_METHOD              items
                8  CALL_METHOD_0         0  ''
               10  GET_ITER         
             12_0  COME_FROM            68  '68'
               12  FOR_ITER             82  'to 82'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'language'
               18  STORE_FAST               'language_characters'

 L.  99        20  LOAD_CONST               0
               22  STORE_FAST               'character_match_count'

 L. 100        24  LOAD_GLOBAL              len
               26  LOAD_FAST                'language_characters'
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'character_count'

 L. 102        32  LOAD_FAST                'language_characters'
               34  GET_ITER         
             36_0  COME_FROM            46  '46'
               36  FOR_ITER             58  'to 58'
               38  STORE_FAST               'character'

 L. 103        40  LOAD_FAST                'character'
               42  LOAD_FAST                'characters'
               44  <118>                 0  ''
               46  POP_JUMP_IF_FALSE    36  'to 36'

 L. 104        48  LOAD_FAST                'character_match_count'
               50  LOAD_CONST               1
               52  INPLACE_ADD      
               54  STORE_FAST               'character_match_count'
               56  JUMP_BACK            36  'to 36'

 L. 106        58  LOAD_FAST                'character_match_count'
               60  LOAD_FAST                'character_count'
               62  BINARY_TRUE_DIVIDE
               64  LOAD_CONST               0.2
               66  COMPARE_OP               >=
               68  POP_JUMP_IF_FALSE    12  'to 12'

 L. 107        70  LOAD_FAST                'languages'
               72  LOAD_METHOD              append
               74  LOAD_FAST                'language'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  JUMP_BACK            12  'to 12'

 L. 109        82  LOAD_FAST                'languages'
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 44


def characters_popularity_compare--- This code section failed: ---

 L. 118         0  LOAD_FAST                'language'
                2  LOAD_GLOBAL              FREQUENCIES
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 119         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 '{} not available'
               12  LOAD_METHOD              format
               14  LOAD_FAST                'language'
               16  CALL_METHOD_1         1  ''
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM             6  '6'

 L. 121        22  LOAD_CONST               0
               24  STORE_FAST               'character_approved_count'

 L. 123        26  LOAD_FAST                'ordered_characters'
               28  GET_ITER         
             30_0  COME_FROM           278  '278'
            30_32  FOR_ITER            292  'to 292'
               34  STORE_FAST               'character'

 L. 124        36  LOAD_FAST                'character'
               38  LOAD_GLOBAL              FREQUENCIES
               40  LOAD_FAST                'language'
               42  BINARY_SUBSCR    
               44  <118>                 1  ''
               46  POP_JUMP_IF_FALSE    50  'to 50'

 L. 125        48  JUMP_BACK            30  'to 30'
             50_0  COME_FROM            46  '46'

 L. 127        50  LOAD_GLOBAL              FREQUENCIES
               52  LOAD_FAST                'language'
               54  BINARY_SUBSCR    
               56  LOAD_CONST               0
               58  LOAD_GLOBAL              FREQUENCIES
               60  LOAD_FAST                'language'
               62  BINARY_SUBSCR    
               64  LOAD_METHOD              index
               66  LOAD_FAST                'character'
               68  CALL_METHOD_1         1  ''
               70  BUILD_SLICE_2         2 
               72  BINARY_SUBSCR    
               74  STORE_FAST               'characters_before_source'

 L. 128        76  LOAD_GLOBAL              FREQUENCIES
               78  LOAD_FAST                'language'
               80  BINARY_SUBSCR    
               82  LOAD_GLOBAL              FREQUENCIES
               84  LOAD_FAST                'language'
               86  BINARY_SUBSCR    
               88  LOAD_METHOD              index
               90  LOAD_FAST                'character'
               92  CALL_METHOD_1         1  ''
               94  LOAD_CONST               None
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  STORE_FAST               'characters_after_source'

 L. 130       102  LOAD_FAST                'ordered_characters'
              104  LOAD_CONST               0
              106  LOAD_FAST                'ordered_characters'
              108  LOAD_METHOD              index
              110  LOAD_FAST                'character'
              112  CALL_METHOD_1         1  ''
              114  BUILD_SLICE_2         2 
              116  BINARY_SUBSCR    
              118  STORE_DEREF              'characters_before'

 L. 131       120  LOAD_FAST                'ordered_characters'
              122  LOAD_FAST                'ordered_characters'
              124  LOAD_METHOD              index
              126  LOAD_FAST                'character'
              128  CALL_METHOD_1         1  ''
              130  LOAD_CONST               None
              132  BUILD_SLICE_2         2 
              134  BINARY_SUBSCR    
              136  STORE_DEREF              'characters_after'

 L. 133       138  LOAD_CLOSURE             'characters_before'
              140  BUILD_TUPLE_1         1 
              142  LOAD_LISTCOMP            '<code_object <listcomp>>'
              144  LOAD_STR                 'characters_popularity_compare.<locals>.<listcomp>'
              146  MAKE_FUNCTION_8          'closure'
              148  LOAD_FAST                'characters_before_source'
              150  GET_ITER         
              152  CALL_FUNCTION_1       1  ''
              154  LOAD_METHOD              count
              156  LOAD_CONST               True
              158  CALL_METHOD_1         1  ''
              160  STORE_FAST               'before_match_count'

 L. 134       162  LOAD_CLOSURE             'characters_after'
              164  BUILD_TUPLE_1         1 
              166  LOAD_LISTCOMP            '<code_object <listcomp>>'
              168  LOAD_STR                 'characters_popularity_compare.<locals>.<listcomp>'
              170  MAKE_FUNCTION_8          'closure'
              172  LOAD_FAST                'characters_after_source'
              174  GET_ITER         
              176  CALL_FUNCTION_1       1  ''
              178  LOAD_METHOD              count
              180  LOAD_CONST               True
              182  CALL_METHOD_1         1  ''
              184  STORE_FAST               'after_match_count'

 L. 136       186  LOAD_GLOBAL              len
              188  LOAD_FAST                'characters_before_source'
              190  CALL_FUNCTION_1       1  ''
              192  LOAD_CONST               0
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_FALSE   216  'to 216'
              198  LOAD_FAST                'before_match_count'
              200  LOAD_CONST               4
              202  COMPARE_OP               <=
              204  POP_JUMP_IF_FALSE   216  'to 216'

 L. 137       206  LOAD_FAST                'character_approved_count'
              208  LOAD_CONST               1
              210  INPLACE_ADD      
              212  STORE_FAST               'character_approved_count'

 L. 138       214  JUMP_BACK            30  'to 30'
            216_0  COME_FROM           204  '204'
            216_1  COME_FROM           196  '196'

 L. 140       216  LOAD_GLOBAL              len
              218  LOAD_FAST                'characters_after_source'
              220  CALL_FUNCTION_1       1  ''
              222  LOAD_CONST               0
              224  COMPARE_OP               ==
              226  POP_JUMP_IF_FALSE   246  'to 246'
              228  LOAD_FAST                'after_match_count'
              230  LOAD_CONST               4
              232  COMPARE_OP               <=
              234  POP_JUMP_IF_FALSE   246  'to 246'

 L. 141       236  LOAD_FAST                'character_approved_count'
              238  LOAD_CONST               1
              240  INPLACE_ADD      
              242  STORE_FAST               'character_approved_count'

 L. 142       244  JUMP_BACK            30  'to 30'
            246_0  COME_FROM           234  '234'
            246_1  COME_FROM           226  '226'

 L. 144       246  LOAD_FAST                'before_match_count'
              248  LOAD_GLOBAL              len
              250  LOAD_FAST                'characters_before_source'
              252  CALL_FUNCTION_1       1  ''
              254  BINARY_TRUE_DIVIDE
              256  LOAD_CONST               0.4
              258  COMPARE_OP               >=
          260_262  POP_JUMP_IF_TRUE    280  'to 280'
              264  LOAD_FAST                'after_match_count'
              266  LOAD_GLOBAL              len
              268  LOAD_FAST                'characters_after_source'
              270  CALL_FUNCTION_1       1  ''
              272  BINARY_TRUE_DIVIDE
              274  LOAD_CONST               0.4
              276  COMPARE_OP               >=
              278  POP_JUMP_IF_FALSE    30  'to 30'
            280_0  COME_FROM           260  '260'

 L. 145       280  LOAD_FAST                'character_approved_count'
              282  LOAD_CONST               1
              284  INPLACE_ADD      
              286  STORE_FAST               'character_approved_count'

 L. 146       288  CONTINUE             30  'to 30'
              290  JUMP_BACK            30  'to 30'

 L. 148       292  LOAD_FAST                'character_approved_count'
              294  LOAD_GLOBAL              len
              296  LOAD_FAST                'ordered_characters'
              298  CALL_FUNCTION_1       1  ''
              300  BINARY_TRUE_DIVIDE
              302  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def alpha_unicode_split--- This code section failed: ---

 L. 157         0  BUILD_MAP_0           0 
                2  STORE_FAST               'layers'

 L. 159         4  LOAD_FAST                'decoded_sequence'
                6  GET_ITER         
                8  FOR_ITER            126  'to 126'
               10  STORE_FAST               'character'

 L. 160        12  LOAD_FAST                'character'
               14  LOAD_METHOD              isalpha
               16  CALL_METHOD_0         0  ''
               18  LOAD_CONST               False
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    26  'to 26'

 L. 161        24  JUMP_BACK             8  'to 8'
             26_0  COME_FROM            22  '22'

 L. 163        26  LOAD_GLOBAL              unicode_range
               28  LOAD_FAST                'character'
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'character_range'

 L. 165        34  LOAD_CONST               None
               36  STORE_FAST               'layer_target_range'

 L. 167        38  LOAD_FAST                'layers'
               40  GET_ITER         
             42_0  COME_FROM            58  '58'
               42  FOR_ITER             70  'to 70'
               44  STORE_FAST               'discovered_range'

 L. 168        46  LOAD_GLOBAL              is_suspiciously_successive_range
               48  LOAD_FAST                'discovered_range'
               50  LOAD_FAST                'character_range'
               52  CALL_FUNCTION_2       2  ''
               54  LOAD_CONST               False
               56  <117>                 0  ''
               58  POP_JUMP_IF_FALSE    42  'to 42'

 L. 169        60  LOAD_FAST                'discovered_range'
               62  STORE_FAST               'layer_target_range'

 L. 170        64  POP_TOP          
               66  BREAK_LOOP           70  'to 70'
               68  JUMP_BACK            42  'to 42'

 L. 172        70  LOAD_FAST                'layer_target_range'
               72  LOAD_CONST               None
               74  <117>                 0  ''
               76  POP_JUMP_IF_FALSE    82  'to 82'

 L. 173        78  LOAD_FAST                'character_range'
               80  STORE_FAST               'layer_target_range'
             82_0  COME_FROM            76  '76'

 L. 175        82  LOAD_FAST                'layer_target_range'
               84  LOAD_FAST                'layers'
               86  <118>                 1  ''
               88  POP_JUMP_IF_FALSE   104  'to 104'

 L. 176        90  LOAD_FAST                'character'
               92  LOAD_METHOD              lower
               94  CALL_METHOD_0         0  ''
               96  LOAD_FAST                'layers'
               98  LOAD_FAST                'layer_target_range'
              100  STORE_SUBSCR     

 L. 177       102  JUMP_BACK             8  'to 8'
            104_0  COME_FROM            88  '88'

 L. 179       104  LOAD_FAST                'layers'
              106  LOAD_FAST                'layer_target_range'
              108  DUP_TOP_TWO      
              110  BINARY_SUBSCR    
              112  LOAD_FAST                'character'
              114  LOAD_METHOD              lower
              116  CALL_METHOD_0         0  ''
              118  INPLACE_ADD      
              120  ROT_THREE        
              122  STORE_SUBSCR     
              124  JUMP_BACK             8  'to 8'

 L. 181       126  LOAD_GLOBAL              list
              128  LOAD_FAST                'layers'
              130  LOAD_METHOD              values
              132  CALL_METHOD_0         0  ''
              134  CALL_FUNCTION_1       1  ''
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 20


def merge_coherence_ratios--- This code section failed: ---

 L. 189         0  BUILD_MAP_0           0 
                2  STORE_FAST               'per_language_ratios'

 L. 190         4  BUILD_LIST_0          0 
                6  STORE_FAST               'merge'

 L. 192         8  LOAD_FAST                'results'
               10  GET_ITER         
               12  FOR_ITER             70  'to 70'
               14  STORE_FAST               'result'

 L. 193        16  LOAD_FAST                'result'
               18  GET_ITER         
               20  FOR_ITER             68  'to 68'
               22  STORE_FAST               'sub_result'

 L. 194        24  LOAD_FAST                'sub_result'
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'language'
               30  STORE_FAST               'ratio'

 L. 195        32  LOAD_FAST                'language'
               34  LOAD_FAST                'per_language_ratios'
               36  <118>                 1  ''
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L. 196        40  LOAD_FAST                'ratio'
               42  BUILD_LIST_1          1 
               44  LOAD_FAST                'per_language_ratios'
               46  LOAD_FAST                'language'
               48  STORE_SUBSCR     

 L. 197        50  JUMP_BACK            20  'to 20'
             52_0  COME_FROM            38  '38'

 L. 198        52  LOAD_FAST                'per_language_ratios'
               54  LOAD_FAST                'language'
               56  BINARY_SUBSCR    
               58  LOAD_METHOD              append

 L. 199        60  LOAD_FAST                'ratio'

 L. 198        62  CALL_METHOD_1         1  ''
               64  POP_TOP          
               66  JUMP_BACK            20  'to 20'
               68  JUMP_BACK            12  'to 12'

 L. 202        70  LOAD_FAST                'per_language_ratios'
               72  GET_ITER         
               74  FOR_ITER            120  'to 120'
               76  STORE_FAST               'language'

 L. 203        78  LOAD_FAST                'merge'
               80  LOAD_METHOD              append

 L. 205        82  LOAD_FAST                'language'

 L. 206        84  LOAD_GLOBAL              round

 L. 207        86  LOAD_GLOBAL              sum

 L. 208        88  LOAD_FAST                'per_language_ratios'
               90  LOAD_FAST                'language'
               92  BINARY_SUBSCR    

 L. 207        94  CALL_FUNCTION_1       1  ''

 L. 209        96  LOAD_GLOBAL              len
               98  LOAD_FAST                'per_language_ratios'
              100  LOAD_FAST                'language'
              102  BINARY_SUBSCR    
              104  CALL_FUNCTION_1       1  ''

 L. 207       106  BINARY_TRUE_DIVIDE

 L. 210       108  LOAD_CONST               4

 L. 206       110  CALL_FUNCTION_2       2  ''

 L. 204       112  BUILD_TUPLE_2         2 

 L. 203       114  CALL_METHOD_1         1  ''
              116  POP_TOP          
              118  JUMP_BACK            74  'to 74'

 L. 215       120  LOAD_GLOBAL              sorted
              122  LOAD_FAST                'merge'
              124  LOAD_LAMBDA              '<code_object <lambda>>'
              126  LOAD_STR                 'merge_coherence_ratios.<locals>.<lambda>'
              128  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              130  LOAD_CONST               True
              132  LOAD_CONST               ('key', 'reverse')
              134  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 36


@lru_cache(maxsize=2048)
def coherence_ratio--- This code section failed: ---

 L. 225         0  BUILD_LIST_0          0 
                2  STORE_FAST               'results'

 L. 227         4  LOAD_CONST               0
                6  STORE_FAST               'sufficient_match_count'

 L. 229         8  LOAD_FAST                'lg_inclusion'
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 230        16  LOAD_FAST                'lg_inclusion'
               18  LOAD_METHOD              split
               20  LOAD_STR                 ','
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'lg_inclusion'
             26_0  COME_FROM            14  '14'

 L. 232        26  LOAD_FAST                'lg_inclusion'
               28  LOAD_CONST               None
               30  <117>                 1  ''
               32  POP_JUMP_IF_FALSE    52  'to 52'
               34  LOAD_STR                 'Latin Based'
               36  LOAD_FAST                'lg_inclusion'
               38  <118>                 0  ''
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 233        42  LOAD_FAST                'lg_inclusion'
               44  LOAD_METHOD              remove
               46  LOAD_STR                 'Latin Based'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
             52_0  COME_FROM            40  '40'
             52_1  COME_FROM            32  '32'

 L. 235        52  LOAD_GLOBAL              alpha_unicode_split
               54  LOAD_FAST                'decoded_sequence'
               56  CALL_FUNCTION_1       1  ''
               58  GET_ITER         
               60  FOR_ITER            212  'to 212'
               62  STORE_FAST               'layer'

 L. 236        64  LOAD_GLOBAL              Counter
               66  LOAD_FAST                'layer'
               68  CALL_FUNCTION_1       1  ''
               70  STORE_FAST               'sequence_frequencies'

 L. 237        72  LOAD_FAST                'sequence_frequencies'
               74  LOAD_METHOD              most_common
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'most_common'

 L. 239        80  LOAD_GLOBAL              sum
               82  LOAD_LISTCOMP            '<code_object <listcomp>>'
               84  LOAD_STR                 'coherence_ratio.<locals>.<listcomp>'
               86  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               88  LOAD_FAST                'most_common'
               90  GET_ITER         
               92  CALL_FUNCTION_1       1  ''
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'character_count'

 L. 241        98  LOAD_FAST                'character_count'
              100  LOAD_CONST               32
              102  COMPARE_OP               <=
              104  POP_JUMP_IF_FALSE   108  'to 108'

 L. 242       106  JUMP_BACK            60  'to 60'
            108_0  COME_FROM           104  '104'

 L. 244       108  LOAD_LISTCOMP            '<code_object <listcomp>>'
              110  LOAD_STR                 'coherence_ratio.<locals>.<listcomp>'
              112  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              114  LOAD_FAST                'most_common'
              116  GET_ITER         
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'popular_character_ordered'

 L. 246       122  LOAD_FAST                'lg_inclusion'
              124  JUMP_IF_TRUE_OR_POP   132  'to 132'
              126  LOAD_GLOBAL              alphabet_languages
              128  LOAD_FAST                'popular_character_ordered'
              130  CALL_FUNCTION_1       1  ''
            132_0  COME_FROM           124  '124'
              132  GET_ITER         
            134_0  COME_FROM           202  '202'
              134  FOR_ITER            210  'to 210'
              136  STORE_FAST               'language'

 L. 247       138  LOAD_GLOBAL              characters_popularity_compare
              140  LOAD_FAST                'language'
              142  LOAD_FAST                'popular_character_ordered'
              144  CALL_FUNCTION_2       2  ''
              146  STORE_FAST               'ratio'

 L. 249       148  LOAD_FAST                'ratio'
              150  LOAD_FAST                'threshold'
              152  COMPARE_OP               <
              154  POP_JUMP_IF_FALSE   160  'to 160'

 L. 250       156  JUMP_BACK           134  'to 134'
              158  JUMP_FORWARD        176  'to 176'
            160_0  COME_FROM           154  '154'

 L. 251       160  LOAD_FAST                'ratio'
              162  LOAD_CONST               0.8
              164  COMPARE_OP               >=
              166  POP_JUMP_IF_FALSE   176  'to 176'

 L. 252       168  LOAD_FAST                'sufficient_match_count'
              170  LOAD_CONST               1
              172  INPLACE_ADD      
              174  STORE_FAST               'sufficient_match_count'
            176_0  COME_FROM           166  '166'
            176_1  COME_FROM           158  '158'

 L. 254       176  LOAD_FAST                'results'
              178  LOAD_METHOD              append

 L. 255       180  LOAD_FAST                'language'
              182  LOAD_GLOBAL              round
              184  LOAD_FAST                'ratio'
              186  LOAD_CONST               4
              188  CALL_FUNCTION_2       2  ''
              190  BUILD_TUPLE_2         2 

 L. 254       192  CALL_METHOD_1         1  ''
              194  POP_TOP          

 L. 258       196  LOAD_FAST                'sufficient_match_count'
              198  LOAD_CONST               3
              200  COMPARE_OP               >=
              202  POP_JUMP_IF_FALSE   134  'to 134'

 L. 259       204  POP_TOP          
              206  CONTINUE             60  'to 60'
              208  JUMP_BACK           134  'to 134'
              210  JUMP_BACK            60  'to 60'

 L. 261       212  LOAD_GLOBAL              sorted
              214  LOAD_FAST                'results'
              216  LOAD_LAMBDA              '<code_object <lambda>>'
              218  LOAD_STR                 'coherence_ratio.<locals>.<lambda>'
              220  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              222  LOAD_CONST               True
              224  LOAD_CONST               ('key', 'reverse')
              226  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              228  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 12