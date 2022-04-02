# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: idna\core.py
from . import idnadata
import bisect, unicodedata, re, sys
from .intranges import intranges_contain
_virama_combining_class = 9
_alabel_prefix = b'xn--'
_unicode_dots_re = re.compile('[.。．｡]')
if sys.version_info[0] == 3:
    unicode = str
    unichr = chr

class IDNAError(UnicodeError):
    __doc__ = ' Base exception for all IDNA-encoding related problems '


class IDNABidiError(IDNAError):
    __doc__ = ' Exception when bidirectional requirements are not satisfied '


class InvalidCodepoint(IDNAError):
    __doc__ = ' Exception when a disallowed or unallocated codepoint is used '


class InvalidCodepointContext(IDNAError):
    __doc__ = ' Exception when the codepoint is not valid in the context it is used '


def _combining_class(cp):
    v = unicodedata.combining(unichr(cp))
    if v == 0:
        if not unicodedata.name(unichr(cp)):
            raise ValueError('Unknown character in unicodedata')
        return v


def _is_script(cp, script):
    return intranges_contain(ord(cp), idnadata.scripts[script])


def _punycode(s):
    return s.encode('punycode')


def _unot(s):
    return 'U+{0:04X}'.format(s)


def valid_label_length(label):
    if len(label) > 63:
        return False
    return True


def valid_string_length(label, trailing_dot):
    if len(label) > (254 if trailing_dot else 253):
        return False
    return True


def check_bidi--- This code section failed: ---

 L.  70         0  LOAD_CONST               False
                2  STORE_FAST               'bidi_label'

 L.  71         4  LOAD_GLOBAL              enumerate
                6  LOAD_FAST                'label'
                8  LOAD_CONST               1
               10  CALL_FUNCTION_2       2  ''
               12  GET_ITER         
             14_0  COME_FROM            72  '72'
             14_1  COME_FROM            66  '66'
               14  FOR_ITER             74  'to 74'
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'idx'
               20  STORE_FAST               'cp'

 L.  72        22  LOAD_GLOBAL              unicodedata
               24  LOAD_METHOD              bidirectional
               26  LOAD_FAST                'cp'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'direction'

 L.  73        32  LOAD_FAST                'direction'
               34  LOAD_STR                 ''
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    60  'to 60'

 L.  75        40  LOAD_GLOBAL              IDNABidiError
               42  LOAD_STR                 'Unknown directionality in label {0} at position {1}'
               44  LOAD_METHOD              format
               46  LOAD_GLOBAL              repr
               48  LOAD_FAST                'label'
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_FAST                'idx'
               54  CALL_METHOD_2         2  ''
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            38  '38'

 L.  76        60  LOAD_FAST                'direction'
               62  LOAD_CONST               ('R', 'AL', 'AN')
               64  <118>                 0  ''
               66  POP_JUMP_IF_FALSE_BACK    14  'to 14'

 L.  77        68  LOAD_CONST               True
               70  STORE_FAST               'bidi_label'
               72  JUMP_BACK            14  'to 14'
             74_0  COME_FROM            14  '14'

 L.  78        74  LOAD_FAST                'bidi_label'
               76  POP_JUMP_IF_TRUE     86  'to 86'
               78  LOAD_FAST                'check_ltr'
               80  POP_JUMP_IF_TRUE     86  'to 86'

 L.  79        82  LOAD_CONST               True
               84  RETURN_VALUE     
             86_0  COME_FROM            80  '80'
             86_1  COME_FROM            76  '76'

 L.  82        86  LOAD_GLOBAL              unicodedata
               88  LOAD_METHOD              bidirectional
               90  LOAD_FAST                'label'
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'direction'

 L.  83       100  LOAD_FAST                'direction'
              102  LOAD_CONST               ('R', 'AL')
              104  <118>                 0  ''
              106  POP_JUMP_IF_FALSE   114  'to 114'

 L.  84       108  LOAD_CONST               True
              110  STORE_FAST               'rtl'
              112  JUMP_FORWARD        146  'to 146'
            114_0  COME_FROM           106  '106'

 L.  85       114  LOAD_FAST                'direction'
              116  LOAD_STR                 'L'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   128  'to 128'

 L.  86       122  LOAD_CONST               False
              124  STORE_FAST               'rtl'
              126  JUMP_FORWARD        146  'to 146'
            128_0  COME_FROM           120  '120'

 L.  88       128  LOAD_GLOBAL              IDNABidiError
              130  LOAD_STR                 'First codepoint in label {0} must be directionality L, R or AL'
              132  LOAD_METHOD              format
              134  LOAD_GLOBAL              repr
              136  LOAD_FAST                'label'
              138  CALL_FUNCTION_1       1  ''
              140  CALL_METHOD_1         1  ''
              142  CALL_FUNCTION_1       1  ''
              144  RAISE_VARARGS_1       1  'exception instance'
            146_0  COME_FROM           126  '126'
            146_1  COME_FROM           112  '112'

 L.  90       146  LOAD_CONST               False
              148  STORE_FAST               'valid_ending'

 L.  91       150  LOAD_CONST               False
              152  STORE_FAST               'number_type'

 L.  92       154  LOAD_GLOBAL              enumerate
              156  LOAD_FAST                'label'
              158  LOAD_CONST               1
              160  CALL_FUNCTION_2       2  ''
              162  GET_ITER         
            164_0  COME_FROM           330  '330'
            164_1  COME_FROM           324  '324'
            164_2  COME_FROM           316  '316'
            164_3  COME_FROM           276  '276'
              164  FOR_ITER            332  'to 332'
              166  UNPACK_SEQUENCE_2     2 
              168  STORE_FAST               'idx'
              170  STORE_FAST               'cp'

 L.  93       172  LOAD_GLOBAL              unicodedata
              174  LOAD_METHOD              bidirectional
              176  LOAD_FAST                'cp'
              178  CALL_METHOD_1         1  ''
              180  STORE_FAST               'direction'

 L.  95       182  LOAD_FAST                'rtl'
          184_186  POP_JUMP_IF_FALSE   278  'to 278'

 L.  97       188  LOAD_FAST                'direction'
              190  LOAD_CONST               ('R', 'AL', 'AN', 'EN', 'ES', 'CS', 'ET', 'ON', 'BN', 'NSM')
              192  <118>                 1  ''
              194  POP_JUMP_IF_FALSE   210  'to 210'

 L.  98       196  LOAD_GLOBAL              IDNABidiError
              198  LOAD_STR                 'Invalid direction for codepoint at position {0} in a right-to-left label'
              200  LOAD_METHOD              format
              202  LOAD_FAST                'idx'
              204  CALL_METHOD_1         1  ''
              206  CALL_FUNCTION_1       1  ''
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           194  '194'

 L. 100       210  LOAD_FAST                'direction'
              212  LOAD_CONST               ('R', 'AL', 'EN', 'AN')
              214  <118>                 0  ''
              216  POP_JUMP_IF_FALSE   224  'to 224'

 L. 101       218  LOAD_CONST               True
              220  STORE_FAST               'valid_ending'
              222  JUMP_FORWARD        236  'to 236'
            224_0  COME_FROM           216  '216'

 L. 102       224  LOAD_FAST                'direction'
              226  LOAD_STR                 'NSM'
              228  COMPARE_OP               !=
              230  POP_JUMP_IF_FALSE   236  'to 236'

 L. 103       232  LOAD_CONST               False
              234  STORE_FAST               'valid_ending'
            236_0  COME_FROM           230  '230'
            236_1  COME_FROM           222  '222'

 L. 105       236  LOAD_FAST                'direction'
              238  LOAD_CONST               ('AN', 'EN')
              240  <118>                 0  ''
          242_244  POP_JUMP_IF_FALSE   330  'to 330'

 L. 106       246  LOAD_FAST                'number_type'
          248_250  POP_JUMP_IF_TRUE    258  'to 258'

 L. 107       252  LOAD_FAST                'direction'
              254  STORE_FAST               'number_type'
              256  JUMP_FORWARD        276  'to 276'
            258_0  COME_FROM           248  '248'

 L. 109       258  LOAD_FAST                'number_type'
              260  LOAD_FAST                'direction'
              262  COMPARE_OP               !=
          264_266  POP_JUMP_IF_FALSE   330  'to 330'

 L. 110       268  LOAD_GLOBAL              IDNABidiError
              270  LOAD_STR                 'Can not mix numeral types in a right-to-left label'
              272  CALL_FUNCTION_1       1  ''
              274  RAISE_VARARGS_1       1  'exception instance'
            276_0  COME_FROM           256  '256'
              276  JUMP_BACK           164  'to 164'
            278_0  COME_FROM           184  '184'

 L. 113       278  LOAD_FAST                'direction'
              280  LOAD_CONST               ('L', 'EN', 'ES', 'CS', 'ET', 'ON', 'BN', 'NSM')
              282  <118>                 1  ''
          284_286  POP_JUMP_IF_FALSE   302  'to 302'

 L. 114       288  LOAD_GLOBAL              IDNABidiError
              290  LOAD_STR                 'Invalid direction for codepoint at position {0} in a left-to-right label'
              292  LOAD_METHOD              format
              294  LOAD_FAST                'idx'
              296  CALL_METHOD_1         1  ''
              298  CALL_FUNCTION_1       1  ''
              300  RAISE_VARARGS_1       1  'exception instance'
            302_0  COME_FROM           284  '284'

 L. 116       302  LOAD_FAST                'direction'
              304  LOAD_CONST               ('L', 'EN')
              306  <118>                 0  ''
          308_310  POP_JUMP_IF_FALSE   318  'to 318'

 L. 117       312  LOAD_CONST               True
              314  STORE_FAST               'valid_ending'
              316  JUMP_BACK           164  'to 164'
            318_0  COME_FROM           308  '308'

 L. 118       318  LOAD_FAST                'direction'
              320  LOAD_STR                 'NSM'
              322  COMPARE_OP               !=
              324  POP_JUMP_IF_FALSE_BACK   164  'to 164'

 L. 119       326  LOAD_CONST               False
              328  STORE_FAST               'valid_ending'
            330_0  COME_FROM           264  '264'
            330_1  COME_FROM           242  '242'
              330  JUMP_BACK           164  'to 164'
            332_0  COME_FROM           164  '164'

 L. 121       332  LOAD_FAST                'valid_ending'
          334_336  POP_JUMP_IF_TRUE    346  'to 346'

 L. 122       338  LOAD_GLOBAL              IDNABidiError
              340  LOAD_STR                 'Label ends with illegal codepoint directionality'
              342  CALL_FUNCTION_1       1  ''
              344  RAISE_VARARGS_1       1  'exception instance'
            346_0  COME_FROM           334  '334'

 L. 124       346  LOAD_CONST               True
              348  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 64


def check_initial_combiner(label):
    if unicodedata.category(label[0])[0] == 'M':
        raise IDNAError('Label begins with an illegal combining character')
    return True


def check_hyphen_ok(label):
    if label[2:4] == '--':
        raise IDNAError('Label has disallowed hyphens in 3rd and 4th position')
    if label[0] == '-' or (label[(-1)] == '-'):
        raise IDNAError('Label must not start or end with a hyphen')
    return True


def check_nfc(label):
    if unicodedata.normalize'NFC'label != label:
        raise IDNAError('Label must be in Normalization Form C')


def valid_contextj--- This code section failed: ---

 L. 151         0  LOAD_GLOBAL              ord
                2  LOAD_FAST                'label'
                4  LOAD_FAST                'pos'
                6  BINARY_SUBSCR    
                8  CALL_FUNCTION_1       1  ''
               10  STORE_FAST               'cp_value'

 L. 153        12  LOAD_FAST                'cp_value'
               14  LOAD_CONST               8204
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE   246  'to 246'

 L. 155        20  LOAD_FAST                'pos'
               22  LOAD_CONST               0
               24  COMPARE_OP               >
               26  POP_JUMP_IF_FALSE    56  'to 56'

 L. 156        28  LOAD_GLOBAL              _combining_class
               30  LOAD_GLOBAL              ord
               32  LOAD_FAST                'label'
               34  LOAD_FAST                'pos'
               36  LOAD_CONST               1
               38  BINARY_SUBTRACT  
               40  BINARY_SUBSCR    
               42  CALL_FUNCTION_1       1  ''
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_GLOBAL              _virama_combining_class
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L. 157        52  LOAD_CONST               True
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'
             56_1  COME_FROM            26  '26'

 L. 159        56  LOAD_CONST               False
               58  STORE_FAST               'ok'

 L. 160        60  LOAD_GLOBAL              range
               62  LOAD_FAST                'pos'
               64  LOAD_CONST               1
               66  BINARY_SUBTRACT  
               68  LOAD_CONST               -1
               70  LOAD_CONST               -1
               72  CALL_FUNCTION_3       3  ''
               74  GET_ITER         
             76_0  COME_FROM           142  '142'
             76_1  COME_FROM           132  '132'
             76_2  COME_FROM           112  '112'
               76  FOR_ITER            144  'to 144'
               78  STORE_FAST               'i'

 L. 161        80  LOAD_GLOBAL              idnadata
               82  LOAD_ATTR                joining_types
               84  LOAD_METHOD              get
               86  LOAD_GLOBAL              ord
               88  LOAD_FAST                'label'
               90  LOAD_FAST                'i'
               92  BINARY_SUBSCR    
               94  CALL_FUNCTION_1       1  ''
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'joining_type'

 L. 162       100  LOAD_FAST                'joining_type'
              102  LOAD_GLOBAL              ord
              104  LOAD_STR                 'T'
              106  CALL_FUNCTION_1       1  ''
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   114  'to 114'

 L. 163       112  JUMP_BACK            76  'to 76'
            114_0  COME_FROM           110  '110'

 L. 164       114  LOAD_FAST                'joining_type'
              116  LOAD_GLOBAL              ord
              118  LOAD_STR                 'L'
              120  CALL_FUNCTION_1       1  ''
              122  LOAD_GLOBAL              ord
              124  LOAD_STR                 'D'
              126  CALL_FUNCTION_1       1  ''
              128  BUILD_TUPLE_2         2 
              130  <118>                 0  ''
              132  POP_JUMP_IF_FALSE_BACK    76  'to 76'

 L. 165       134  LOAD_CONST               True
              136  STORE_FAST               'ok'

 L. 166       138  POP_TOP          
              140  BREAK_LOOP          144  'to 144'
              142  JUMP_BACK            76  'to 76'
            144_0  COME_FROM           140  '140'
            144_1  COME_FROM            76  '76'

 L. 168       144  LOAD_FAST                'ok'
              146  POP_JUMP_IF_TRUE    152  'to 152'

 L. 169       148  LOAD_CONST               False
              150  RETURN_VALUE     
            152_0  COME_FROM           146  '146'

 L. 171       152  LOAD_CONST               False
              154  STORE_FAST               'ok'

 L. 172       156  LOAD_GLOBAL              range
              158  LOAD_FAST                'pos'
              160  LOAD_CONST               1
              162  BINARY_ADD       
              164  LOAD_GLOBAL              len
              166  LOAD_FAST                'label'
              168  CALL_FUNCTION_1       1  ''
              170  CALL_FUNCTION_2       2  ''
              172  GET_ITER         
            174_0  COME_FROM           240  '240'
            174_1  COME_FROM           230  '230'
            174_2  COME_FROM           210  '210'
              174  FOR_ITER            242  'to 242'
              176  STORE_FAST               'i'

 L. 173       178  LOAD_GLOBAL              idnadata
              180  LOAD_ATTR                joining_types
              182  LOAD_METHOD              get
              184  LOAD_GLOBAL              ord
              186  LOAD_FAST                'label'
              188  LOAD_FAST                'i'
              190  BINARY_SUBSCR    
              192  CALL_FUNCTION_1       1  ''
              194  CALL_METHOD_1         1  ''
              196  STORE_FAST               'joining_type'

 L. 174       198  LOAD_FAST                'joining_type'
              200  LOAD_GLOBAL              ord
              202  LOAD_STR                 'T'
              204  CALL_FUNCTION_1       1  ''
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   212  'to 212'

 L. 175       210  JUMP_BACK           174  'to 174'
            212_0  COME_FROM           208  '208'

 L. 176       212  LOAD_FAST                'joining_type'
              214  LOAD_GLOBAL              ord
              216  LOAD_STR                 'R'
              218  CALL_FUNCTION_1       1  ''
              220  LOAD_GLOBAL              ord
              222  LOAD_STR                 'D'
              224  CALL_FUNCTION_1       1  ''
              226  BUILD_TUPLE_2         2 
              228  <118>                 0  ''
              230  POP_JUMP_IF_FALSE_BACK   174  'to 174'

 L. 177       232  LOAD_CONST               True
              234  STORE_FAST               'ok'

 L. 178       236  POP_TOP          
              238  BREAK_LOOP          242  'to 242'
              240  JUMP_BACK           174  'to 174'
            242_0  COME_FROM           238  '238'
            242_1  COME_FROM           174  '174'

 L. 179       242  LOAD_FAST                'ok'
              244  RETURN_VALUE     
            246_0  COME_FROM            18  '18'

 L. 181       246  LOAD_FAST                'cp_value'
              248  LOAD_CONST               8205
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   300  'to 300'

 L. 183       256  LOAD_FAST                'pos'
              258  LOAD_CONST               0
              260  COMPARE_OP               >
          262_264  POP_JUMP_IF_FALSE   296  'to 296'

 L. 184       266  LOAD_GLOBAL              _combining_class
              268  LOAD_GLOBAL              ord
              270  LOAD_FAST                'label'
              272  LOAD_FAST                'pos'
              274  LOAD_CONST               1
              276  BINARY_SUBTRACT  
              278  BINARY_SUBSCR    
              280  CALL_FUNCTION_1       1  ''
              282  CALL_FUNCTION_1       1  ''
              284  LOAD_GLOBAL              _virama_combining_class
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_FALSE   296  'to 296'

 L. 185       292  LOAD_CONST               True
              294  RETURN_VALUE     
            296_0  COME_FROM           288  '288'
            296_1  COME_FROM           262  '262'

 L. 186       296  LOAD_CONST               False
              298  RETURN_VALUE     
            300_0  COME_FROM           252  '252'

 L. 190       300  LOAD_CONST               False
              302  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 130


def valid_contexto(label, pos, exception=False):
    cp_value = ord(label[pos])
    if cp_value == 183:
        if 0 < pos < len(label) - 1:
            if ord(label[(pos - 1)]) == 108:
                if ord(label[(pos + 1)]) == 108:
                    return True
        return False
    if cp_value == 885:
        if pos < len(label) - 1:
            if len(label) > 1:
                return _is_script(label[(pos + 1)], 'Greek')
        return False
    if cp_value == 1523 or (cp_value == 1524):
        if pos > 0:
            return _is_script(label[(pos - 1)], 'Hebrew')
        return False
    if cp_value == 12539:
        for cp in label:
            if cp == '・':
                pass
            else:
                if not _is_script(cp, 'Hiragana'):
                    if not _is_script(cp, 'Katakana'):
                        if _is_script(cp, 'Han'):
                            pass
                else:
                    return True
            return False

        if 1632 <= cp_value <= 1641:
            for cp in label:
                if 1776 <= ord(cp) <= 1785:
                    return False
            else:
                return True

        if 1776 <= cp_value <= 1785:
            for cp in label:
                if 1632 <= ord(cp) <= 1641:
                    return False
            else:
                return True


def check_label--- This code section failed: ---

 L. 236         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'label'
                4  LOAD_GLOBAL              bytes
                6  LOAD_GLOBAL              bytearray
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    24  'to 24'

 L. 237        14  LOAD_FAST                'label'
               16  LOAD_METHOD              decode
               18  LOAD_STR                 'utf-8'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'label'
             24_0  COME_FROM            12  '12'

 L. 238        24  LOAD_GLOBAL              len
               26  LOAD_FAST                'label'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               0
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 239        36  LOAD_GLOBAL              IDNAError
               38  LOAD_STR                 'Empty Label'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'

 L. 241        44  LOAD_GLOBAL              check_nfc
               46  LOAD_FAST                'label'
               48  CALL_FUNCTION_1       1  ''
               50  POP_TOP          

 L. 242        52  LOAD_GLOBAL              check_hyphen_ok
               54  LOAD_FAST                'label'
               56  CALL_FUNCTION_1       1  ''
               58  POP_TOP          

 L. 243        60  LOAD_GLOBAL              check_initial_combiner
               62  LOAD_FAST                'label'
               64  CALL_FUNCTION_1       1  ''
               66  POP_TOP          

 L. 245        68  LOAD_GLOBAL              enumerate
               70  LOAD_FAST                'label'
               72  CALL_FUNCTION_1       1  ''
               74  GET_ITER         
             76_0  COME_FROM           316  '316'
             76_1  COME_FROM           284  '284'
             76_2  COME_FROM           222  '222'
             76_3  COME_FROM           110  '110'
             76_4  COME_FROM           108  '108'
               76  FOR_ITER            318  'to 318'
               78  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST               'pos'
               82  STORE_FAST               'cp'

 L. 246        84  LOAD_GLOBAL              ord
               86  LOAD_FAST                'cp'
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'cp_value'

 L. 247        92  LOAD_GLOBAL              intranges_contain
               94  LOAD_FAST                'cp_value'
               96  LOAD_GLOBAL              idnadata
               98  LOAD_ATTR                codepoint_classes
              100  LOAD_STR                 'PVALID'
              102  BINARY_SUBSCR    
              104  CALL_FUNCTION_2       2  ''
              106  POP_JUMP_IF_FALSE   112  'to 112'

 L. 248       108  CONTINUE             76  'to 76'
              110  JUMP_BACK            76  'to 76'
            112_0  COME_FROM           106  '106'

 L. 249       112  LOAD_GLOBAL              intranges_contain
              114  LOAD_FAST                'cp_value'
              116  LOAD_GLOBAL              idnadata
              118  LOAD_ATTR                codepoint_classes
              120  LOAD_STR                 'CONTEXTJ'
              122  BINARY_SUBSCR    
              124  CALL_FUNCTION_2       2  ''
              126  POP_JUMP_IF_FALSE   224  'to 224'

 L. 250       128  SETUP_FINALLY       174  'to 174'

 L. 251       130  LOAD_GLOBAL              valid_contextj
              132  LOAD_FAST                'label'
              134  LOAD_FAST                'pos'
              136  CALL_FUNCTION_2       2  ''
              138  POP_JUMP_IF_TRUE    170  'to 170'

 L. 252       140  LOAD_GLOBAL              InvalidCodepointContext
              142  LOAD_STR                 'Joiner {0} not allowed at position {1} in {2}'
              144  LOAD_METHOD              format

 L. 253       146  LOAD_GLOBAL              _unot
              148  LOAD_FAST                'cp_value'
              150  CALL_FUNCTION_1       1  ''
              152  LOAD_FAST                'pos'
              154  LOAD_CONST               1
              156  BINARY_ADD       
              158  LOAD_GLOBAL              repr
              160  LOAD_FAST                'label'
              162  CALL_FUNCTION_1       1  ''

 L. 252       164  CALL_METHOD_3         3  ''
              166  CALL_FUNCTION_1       1  ''
              168  RAISE_VARARGS_1       1  'exception instance'
            170_0  COME_FROM           138  '138'
              170  POP_BLOCK        
              172  JUMP_FORWARD        222  'to 222'
            174_0  COME_FROM_FINALLY   128  '128'

 L. 254       174  DUP_TOP          
              176  LOAD_GLOBAL              ValueError
              178  <121>               220  ''
              180  POP_TOP          
              182  POP_TOP          
              184  POP_TOP          

 L. 255       186  LOAD_GLOBAL              IDNAError
              188  LOAD_STR                 'Unknown codepoint adjacent to joiner {0} at position {1} in {2}'
              190  LOAD_METHOD              format

 L. 256       192  LOAD_GLOBAL              _unot
              194  LOAD_FAST                'cp_value'
              196  CALL_FUNCTION_1       1  ''
              198  LOAD_FAST                'pos'
              200  LOAD_CONST               1
              202  BINARY_ADD       
              204  LOAD_GLOBAL              repr
              206  LOAD_FAST                'label'
              208  CALL_FUNCTION_1       1  ''

 L. 255       210  CALL_METHOD_3         3  ''
              212  CALL_FUNCTION_1       1  ''
              214  RAISE_VARARGS_1       1  'exception instance'
              216  POP_EXCEPT       
              218  JUMP_FORWARD        222  'to 222'
              220  <48>             
            222_0  COME_FROM           218  '218'
            222_1  COME_FROM           172  '172'
              222  JUMP_BACK            76  'to 76'
            224_0  COME_FROM           126  '126'

 L. 257       224  LOAD_GLOBAL              intranges_contain
              226  LOAD_FAST                'cp_value'
              228  LOAD_GLOBAL              idnadata
              230  LOAD_ATTR                codepoint_classes
              232  LOAD_STR                 'CONTEXTO'
              234  BINARY_SUBSCR    
              236  CALL_FUNCTION_2       2  ''
          238_240  POP_JUMP_IF_FALSE   286  'to 286'

 L. 258       242  LOAD_GLOBAL              valid_contexto
              244  LOAD_FAST                'label'
              246  LOAD_FAST                'pos'
              248  CALL_FUNCTION_2       2  ''
          250_252  POP_JUMP_IF_TRUE    316  'to 316'

 L. 259       254  LOAD_GLOBAL              InvalidCodepointContext
              256  LOAD_STR                 'Codepoint {0} not allowed at position {1} in {2}'
              258  LOAD_METHOD              format
              260  LOAD_GLOBAL              _unot
              262  LOAD_FAST                'cp_value'
              264  CALL_FUNCTION_1       1  ''
              266  LOAD_FAST                'pos'
              268  LOAD_CONST               1
              270  BINARY_ADD       
              272  LOAD_GLOBAL              repr
              274  LOAD_FAST                'label'
              276  CALL_FUNCTION_1       1  ''
              278  CALL_METHOD_3         3  ''
              280  CALL_FUNCTION_1       1  ''
              282  RAISE_VARARGS_1       1  'exception instance'
              284  JUMP_BACK            76  'to 76'
            286_0  COME_FROM           238  '238'

 L. 261       286  LOAD_GLOBAL              InvalidCodepoint
              288  LOAD_STR                 'Codepoint {0} at position {1} of {2} not allowed'
              290  LOAD_METHOD              format
              292  LOAD_GLOBAL              _unot
              294  LOAD_FAST                'cp_value'
              296  CALL_FUNCTION_1       1  ''
              298  LOAD_FAST                'pos'
              300  LOAD_CONST               1
              302  BINARY_ADD       
              304  LOAD_GLOBAL              repr
              306  LOAD_FAST                'label'
              308  CALL_FUNCTION_1       1  ''
              310  CALL_METHOD_3         3  ''
              312  CALL_FUNCTION_1       1  ''
              314  RAISE_VARARGS_1       1  'exception instance'
            316_0  COME_FROM           250  '250'
              316  JUMP_BACK            76  'to 76'
            318_0  COME_FROM            76  '76'

 L. 263       318  LOAD_GLOBAL              check_bidi
              320  LOAD_FAST                'label'
              322  CALL_FUNCTION_1       1  ''
              324  POP_TOP          

Parse error at or near `<121>' instruction at offset 178


def alabel--- This code section failed: ---

 L. 268         0  SETUP_FINALLY        42  'to 42'

 L. 269         2  LOAD_FAST                'label'
                4  LOAD_METHOD              encode
                6  LOAD_STR                 'ascii'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'label'

 L. 270        12  LOAD_GLOBAL              ulabel
               14  LOAD_FAST                'label'
               16  CALL_FUNCTION_1       1  ''
               18  POP_TOP          

 L. 271        20  LOAD_GLOBAL              valid_label_length
               22  LOAD_FAST                'label'
               24  CALL_FUNCTION_1       1  ''
               26  POP_JUMP_IF_TRUE     36  'to 36'

 L. 272        28  LOAD_GLOBAL              IDNAError
               30  LOAD_STR                 'Label too long'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 273        36  LOAD_FAST                'label'
               38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY     0  '0'

 L. 274        42  DUP_TOP          
               44  LOAD_GLOBAL              UnicodeEncodeError
               46  <121>                58  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 275        54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
               58  <48>             
             60_0  COME_FROM            56  '56'

 L. 277        60  LOAD_FAST                'label'
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L. 278        64  LOAD_GLOBAL              IDNAError
               66  LOAD_STR                 'No Input'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L. 280        72  LOAD_GLOBAL              unicode
               74  LOAD_FAST                'label'
               76  CALL_FUNCTION_1       1  ''
               78  STORE_FAST               'label'

 L. 281        80  LOAD_GLOBAL              check_label
               82  LOAD_FAST                'label'
               84  CALL_FUNCTION_1       1  ''
               86  POP_TOP          

 L. 282        88  LOAD_GLOBAL              _punycode
               90  LOAD_FAST                'label'
               92  CALL_FUNCTION_1       1  ''
               94  STORE_FAST               'label'

 L. 283        96  LOAD_GLOBAL              _alabel_prefix
               98  LOAD_FAST                'label'
              100  BINARY_ADD       
              102  STORE_FAST               'label'

 L. 285       104  LOAD_GLOBAL              valid_label_length
              106  LOAD_FAST                'label'
              108  CALL_FUNCTION_1       1  ''
              110  POP_JUMP_IF_TRUE    120  'to 120'

 L. 286       112  LOAD_GLOBAL              IDNAError
              114  LOAD_STR                 'Label too long'
              116  CALL_FUNCTION_1       1  ''
              118  RAISE_VARARGS_1       1  'exception instance'
            120_0  COME_FROM           110  '110'

 L. 288       120  LOAD_FAST                'label'
              122  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 46


def ulabel--- This code section failed: ---

 L. 293         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'label'
                4  LOAD_GLOBAL              bytes
                6  LOAD_GLOBAL              bytearray
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_TRUE     60  'to 60'

 L. 294        14  SETUP_FINALLY        30  'to 30'

 L. 295        16  LOAD_FAST                'label'
               18  LOAD_METHOD              encode
               20  LOAD_STR                 'ascii'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'label'
               26  POP_BLOCK        
               28  JUMP_FORWARD         60  'to 60'
             30_0  COME_FROM_FINALLY    14  '14'

 L. 296        30  DUP_TOP          
               32  LOAD_GLOBAL              UnicodeEncodeError
               34  <121>                58  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 297        42  LOAD_GLOBAL              check_label
               44  LOAD_FAST                'label'
               46  CALL_FUNCTION_1       1  ''
               48  POP_TOP          

 L. 298        50  LOAD_FAST                'label'
               52  ROT_FOUR         
               54  POP_EXCEPT       
               56  RETURN_VALUE     
               58  <48>             
             60_0  COME_FROM            28  '28'
             60_1  COME_FROM            12  '12'

 L. 300        60  LOAD_FAST                'label'
               62  LOAD_METHOD              lower
               64  CALL_METHOD_0         0  ''
               66  STORE_FAST               'label'

 L. 301        68  LOAD_FAST                'label'
               70  LOAD_METHOD              startswith
               72  LOAD_GLOBAL              _alabel_prefix
               74  CALL_METHOD_1         1  ''
               76  POP_JUMP_IF_FALSE    96  'to 96'

 L. 302        78  LOAD_FAST                'label'
               80  LOAD_GLOBAL              len
               82  LOAD_GLOBAL              _alabel_prefix
               84  CALL_FUNCTION_1       1  ''
               86  LOAD_CONST               None
               88  BUILD_SLICE_2         2 
               90  BINARY_SUBSCR    
               92  STORE_FAST               'label'
               94  JUMP_FORWARD        114  'to 114'
             96_0  COME_FROM            76  '76'

 L. 304        96  LOAD_GLOBAL              check_label
               98  LOAD_FAST                'label'
              100  CALL_FUNCTION_1       1  ''
              102  POP_TOP          

 L. 305       104  LOAD_FAST                'label'
              106  LOAD_METHOD              decode
              108  LOAD_STR                 'ascii'
              110  CALL_METHOD_1         1  ''
              112  RETURN_VALUE     
            114_0  COME_FROM            94  '94'

 L. 307       114  LOAD_FAST                'label'
              116  LOAD_METHOD              decode
              118  LOAD_STR                 'punycode'
              120  CALL_METHOD_1         1  ''
              122  STORE_FAST               'label'

 L. 308       124  LOAD_GLOBAL              check_label
              126  LOAD_FAST                'label'
              128  CALL_FUNCTION_1       1  ''
              130  POP_TOP          

 L. 309       132  LOAD_FAST                'label'
              134  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 34


def uts46_remap--- This code section failed: ---

 L. 314         0  LOAD_CONST               1
                2  LOAD_CONST               ('uts46data',)
                4  IMPORT_NAME              uts46data
                6  IMPORT_FROM              uts46data
                8  STORE_FAST               'uts46data'
               10  POP_TOP          

 L. 315        12  LOAD_STR                 ''
               14  STORE_FAST               'output'

 L. 316        16  SETUP_FINALLY       240  'to 240'

 L. 317        18  LOAD_GLOBAL              enumerate
               20  LOAD_FAST                'domain'
               22  CALL_FUNCTION_1       1  ''
               24  GET_ITER         
             26_0  COME_FROM           224  '224'
             26_1  COME_FROM           216  '216'
             26_2  COME_FROM           208  '208'
             26_3  COME_FROM           158  '158'
               26  FOR_ITER            226  'to 226'
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'pos'
               32  STORE_FAST               'char'

 L. 318        34  LOAD_GLOBAL              ord
               36  LOAD_FAST                'char'
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'code_point'

 L. 319        42  LOAD_FAST                'uts46data'
               44  LOAD_FAST                'code_point'
               46  LOAD_CONST               256
               48  COMPARE_OP               <
               50  POP_JUMP_IF_FALSE    56  'to 56'
               52  LOAD_FAST                'code_point'
               54  JUMP_FORWARD         74  'to 74'
             56_0  COME_FROM            50  '50'

 L. 320        56  LOAD_GLOBAL              bisect
               58  LOAD_METHOD              bisect_left
               60  LOAD_FAST                'uts46data'
               62  LOAD_FAST                'code_point'
               64  LOAD_STR                 'Z'
               66  BUILD_TUPLE_2         2 
               68  CALL_METHOD_2         2  ''
               70  LOAD_CONST               1
               72  BINARY_SUBTRACT  
             74_0  COME_FROM            54  '54'

 L. 319        74  BINARY_SUBSCR    
               76  STORE_FAST               'uts46row'

 L. 321        78  LOAD_FAST                'uts46row'
               80  LOAD_CONST               1
               82  BINARY_SUBSCR    
               84  STORE_FAST               'status'

 L. 322        86  LOAD_GLOBAL              len
               88  LOAD_FAST                'uts46row'
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_CONST               3
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   106  'to 106'
               98  LOAD_FAST                'uts46row'
              100  LOAD_CONST               2
              102  BINARY_SUBSCR    
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            96  '96'
              106  LOAD_CONST               None
            108_0  COME_FROM           104  '104'
              108  STORE_FAST               'replacement'

 L. 323       110  LOAD_FAST                'status'
              112  LOAD_STR                 'V'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_TRUE    150  'to 150'

 L. 324       118  LOAD_FAST                'status'
              120  LOAD_STR                 'D'
              122  COMPARE_OP               ==

 L. 323       124  POP_JUMP_IF_FALSE   130  'to 130'

 L. 324       126  LOAD_FAST                'transitional'

 L. 323       128  POP_JUMP_IF_FALSE   150  'to 150'
            130_0  COME_FROM           124  '124'

 L. 325       130  LOAD_FAST                'status'
              132  LOAD_STR                 '3'
              134  COMPARE_OP               ==

 L. 323       136  POP_JUMP_IF_FALSE   160  'to 160'

 L. 325       138  LOAD_FAST                'std3_rules'

 L. 323       140  POP_JUMP_IF_TRUE    160  'to 160'

 L. 325       142  LOAD_FAST                'replacement'
              144  LOAD_CONST               None
              146  <117>                 0  ''

 L. 323       148  POP_JUMP_IF_FALSE   160  'to 160'
            150_0  COME_FROM           128  '128'
            150_1  COME_FROM           116  '116'

 L. 326       150  LOAD_FAST                'output'
              152  LOAD_FAST                'char'
              154  INPLACE_ADD      
              156  STORE_FAST               'output'
              158  JUMP_BACK            26  'to 26'
            160_0  COME_FROM           148  '148'
            160_1  COME_FROM           140  '140'
            160_2  COME_FROM           136  '136'

 L. 327       160  LOAD_FAST                'replacement'
              162  LOAD_CONST               None
              164  <117>                 1  ''
              166  POP_JUMP_IF_FALSE   210  'to 210'
              168  LOAD_FAST                'status'
              170  LOAD_STR                 'M'
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_TRUE    200  'to 200'

 L. 328       176  LOAD_FAST                'status'
              178  LOAD_STR                 '3'
              180  COMPARE_OP               ==

 L. 327       182  POP_JUMP_IF_FALSE   188  'to 188'

 L. 328       184  LOAD_FAST                'std3_rules'

 L. 327       186  POP_JUMP_IF_FALSE   200  'to 200'
            188_0  COME_FROM           182  '182'

 L. 329       188  LOAD_FAST                'status'
              190  LOAD_STR                 'D'
              192  COMPARE_OP               ==

 L. 327       194  POP_JUMP_IF_FALSE   210  'to 210'

 L. 329       196  LOAD_FAST                'transitional'

 L. 327       198  POP_JUMP_IF_FALSE   210  'to 210'
            200_0  COME_FROM           186  '186'
            200_1  COME_FROM           174  '174'

 L. 330       200  LOAD_FAST                'output'
              202  LOAD_FAST                'replacement'
              204  INPLACE_ADD      
              206  STORE_FAST               'output'
              208  JUMP_BACK            26  'to 26'
            210_0  COME_FROM           198  '198'
            210_1  COME_FROM           194  '194'
            210_2  COME_FROM           166  '166'

 L. 331       210  LOAD_FAST                'status'
              212  LOAD_STR                 'I'
              214  COMPARE_OP               !=
              216  POP_JUMP_IF_FALSE_BACK    26  'to 26'

 L. 332       218  LOAD_GLOBAL              IndexError
              220  CALL_FUNCTION_0       0  ''
              222  RAISE_VARARGS_1       1  'exception instance'
              224  JUMP_BACK            26  'to 26'
            226_0  COME_FROM            26  '26'

 L. 333       226  LOAD_GLOBAL              unicodedata
              228  LOAD_METHOD              normalize
              230  LOAD_STR                 'NFC'
              232  LOAD_FAST                'output'
              234  CALL_METHOD_2         2  ''
              236  POP_BLOCK        
              238  RETURN_VALUE     
            240_0  COME_FROM_FINALLY    16  '16'

 L. 334       240  DUP_TOP          
              242  LOAD_GLOBAL              IndexError
          244_246  <121>               288  ''
              248  POP_TOP          
              250  POP_TOP          
              252  POP_TOP          

 L. 335       254  LOAD_GLOBAL              InvalidCodepoint

 L. 336       256  LOAD_STR                 'Codepoint {0} not allowed at position {1} in {2}'
              258  LOAD_METHOD              format

 L. 337       260  LOAD_GLOBAL              _unot
              262  LOAD_FAST                'code_point'
              264  CALL_FUNCTION_1       1  ''
              266  LOAD_FAST                'pos'
              268  LOAD_CONST               1
              270  BINARY_ADD       
              272  LOAD_GLOBAL              repr
              274  LOAD_FAST                'domain'
              276  CALL_FUNCTION_1       1  ''

 L. 336       278  CALL_METHOD_3         3  ''

 L. 335       280  CALL_FUNCTION_1       1  ''
              282  RAISE_VARARGS_1       1  'exception instance'
              284  POP_EXCEPT       
              286  JUMP_FORWARD        290  'to 290'
              288  <48>             
            290_0  COME_FROM           286  '286'

Parse error at or near `<117>' instruction at offset 146


def encode(s, strict=False, uts46=False, std3_rules=False, transitional=False):
    if isinstance(s, (bytes, bytearray)):
        s = s.decode('ascii')
    if uts46:
        s = uts46_remap(s, std3_rules, transitional)
    trailing_dot = False
    result = []
    if strict:
        labels = s.split('.')
    else:
        labels = _unicode_dots_re.split(s)
    if not labels or labels == ['']:
        raise IDNAError('Empty domain')
    if labels[(-1)] == '':
        del labels[-1]
        trailing_dot = True
    for label in labels:
        s = alabel(label)
        if s:
            result.append(s)
        else:
            raise IDNAError('Empty label')
    else:
        if trailing_dot:
            result.append(b'')
        s = (b'.').join(result)
        if not valid_string_length(s, trailing_dot):
            raise IDNAError('Domain too long')
        return s


def decode(s, strict=False, uts46=False, std3_rules=False):
    if isinstance(s, (bytes, bytearray)):
        s = s.decode('ascii')
    if uts46:
        s = uts46_remap(s, std3_rules, False)
    trailing_dot = False
    result = []
    if not strict:
        labels = _unicode_dots_re.split(s)
    else:
        labels = s.split('.')
    if not labels or labels == ['']:
        raise IDNAError('Empty domain')
    if not labels[(-1)]:
        del labels[-1]
        trailing_dot = True
    for label in labels:
        s = ulabel(label)
        if s:
            result.append(s)
        else:
            raise IDNAError('Empty label')
    else:
        if trailing_dot:
            result.append('')
        return '.'.join(result)