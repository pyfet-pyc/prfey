# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: requests\packages\idna\core.py
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
    return unicodedata.combining(unichr(cp))


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


def check_bidi(label, check_ltr=False):
    bidi_label = False
    for idx, cp in enumerate(label, 1):
        direction = unicodedata.bidirectional(cp)
        if direction == '':
            raise IDNABidiError('Unknown directionality in label {0} at position {1}'.format(repr(label), idx))
        if direction in ('R', 'AL', 'AN'):
            bidi_label = True
            break
    else:
        if not bidi_label:
            if not check_ltr:
                return True
            direction = unicodedata.bidirectional(label[0])
            if direction in ('R', 'AL'):
                rtl = True
            elif direction == 'L':
                rtl = False
            else:
                raise IDNABidiError('First codepoint in label {0} must be directionality L, R or AL'.format(repr(label)))
            valid_ending = False
            number_type = False
            for idx, cp in enumerate(label, 1):
                direction = unicodedata.bidirectional(cp)
                if rtl:
                    if direction not in ('R', 'AL', 'AN', 'EN', 'ES', 'CS', 'ET', 'ON',
                                         'BN', 'NSM'):
                        raise IDNABidiError('Invalid direction for codepoint at position {0} in a right-to-left label'.format(idx))
                    else:
                        if direction in ('R', 'AL', 'EN', 'AN'):
                            valid_ending = True
                        elif direction != 'NSM':
                            valid_ending = False
                        if direction in ('AN', 'EN'):
                            if not number_type:
                                number_type = direction
                            elif number_type != direction:
                                raise IDNABidiError('Can not mix numeral types in a right-to-left label')
                else:
                    if direction not in ('L', 'EN', 'ES', 'CS', 'ET', 'ON', 'BN', 'NSM'):
                        raise IDNABidiError('Invalid direction for codepoint at position {0} in a left-to-right label'.format(idx))
                    if direction in ('L', 'EN'):
                        valid_ending = True
                    else:
                        if direction != 'NSM':
                            valid_ending = False

            if not valid_ending:
                raise IDNABidiError('Label ends with illegal codepoint directionality')
            return True


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
    if unicodedata.normalize('NFC', label) != label:
        raise IDNAError('Label must be in Normalization Form C')


def valid_contextj(label, pos):
    cp_value = ord(label[pos])
    if cp_value == 8204:
        if pos > 0:
            if _combining_class(ord(label[(pos - 1)])) == _virama_combining_class:
                return True
        ok = False
        for i in range(pos - 1, -1, -1):
            joining_type = idnadata.joining_types.get(ord(label[i]))
            if joining_type == 'T':
                pass
            else:
                if joining_type in ('L', 'D'):
                    ok = True
                    break
        else:
            if not ok:
                return False
            ok = False
            for i in range(pos + 1, len(label)):
                joining_type = idnadata.joining_types.get(ord(label[i]))
                if joining_type == 'T':
                    pass
                else:
                    if joining_type in ('R', 'D'):
                        ok = True
                        break
            else:
                return ok

    if cp_value == 8205:
        if pos > 0:
            if _combining_class(ord(label[(pos - 1)])) == _virama_combining_class:
                return True
        return False
    return False


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
                        if not _is_script(cp, 'Han'):
                            return False
            return True

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


def check_label(label):
    if isinstance(label, (bytes, bytearray)):
        label = label.decode('utf-8')
    if len(label) == 0:
        raise IDNAError('Empty Label')
    check_nfc(label)
    check_hyphen_ok(label)
    check_initial_combiner(label)
    for pos, cp in enumerate(label):
        cp_value = ord(cp)
        if intranges_contain(cp_value, idnadata.codepoint_classes['PVALID']):
            continue
        else:
            if intranges_contain(cp_value, idnadata.codepoint_classes['CONTEXTJ']):
                if not valid_contextj(label, pos):
                    raise InvalidCodepointContext('Joiner {0} not allowed at position {1} in {2}'.format(_unot(cp_value), pos + 1, repr(label)))
            else:
                if intranges_contain(cp_value, idnadata.codepoint_classes['CONTEXTO']):
                    if not valid_contexto(label, pos):
                        raise InvalidCodepointContext('Codepoint {0} not allowed at position {1} in {2}'.format(_unot(cp_value), pos + 1, repr(label)))
                else:
                    raise InvalidCodepoint('Codepoint {0} at position {1} of {2} not allowed'.format(_unot(cp_value), pos + 1, repr(label)))
    else:
        check_bidi(label)


def alabel--- This code section failed: ---

 L. 260         0  SETUP_FINALLY        74  'to 74'

 L. 261         2  LOAD_FAST                'label'
                4  LOAD_METHOD              encode
                6  LOAD_STR                 'ascii'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'label'

 L. 262        12  SETUP_FINALLY        26  'to 26'

 L. 263        14  LOAD_GLOBAL              ulabel
               16  LOAD_FAST                'label'
               18  CALL_FUNCTION_1       1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  JUMP_FORWARD         52  'to 52'
             26_0  COME_FROM_FINALLY    12  '12'

 L. 264        26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 265        32  LOAD_GLOBAL              IDNAError
               34  LOAD_STR                 'The label {0} is not a valid A-label'
               36  LOAD_METHOD              format
               38  LOAD_FAST                'label'
               40  CALL_METHOD_1         1  ''
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
               50  END_FINALLY      
             52_0  COME_FROM            48  '48'
             52_1  COME_FROM            24  '24'

 L. 266        52  LOAD_GLOBAL              valid_label_length
               54  LOAD_FAST                'label'
               56  CALL_FUNCTION_1       1  ''
               58  POP_JUMP_IF_TRUE     68  'to 68'

 L. 267        60  LOAD_GLOBAL              IDNAError
               62  LOAD_STR                 'Label too long'
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 268        68  LOAD_FAST                'label'
               70  POP_BLOCK        
               72  RETURN_VALUE     
             74_0  COME_FROM_FINALLY     0  '0'

 L. 269        74  DUP_TOP          
               76  LOAD_GLOBAL              UnicodeError
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE    92  'to 92'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 270        88  POP_EXCEPT       
               90  JUMP_FORWARD         94  'to 94'
             92_0  COME_FROM            80  '80'
               92  END_FINALLY      
             94_0  COME_FROM            90  '90'

 L. 272        94  LOAD_FAST                'label'
               96  POP_JUMP_IF_TRUE    106  'to 106'

 L. 273        98  LOAD_GLOBAL              IDNAError
              100  LOAD_STR                 'No Input'
              102  CALL_FUNCTION_1       1  ''
              104  RAISE_VARARGS_1       1  'exception instance'
            106_0  COME_FROM            96  '96'

 L. 275       106  LOAD_GLOBAL              unicode
              108  LOAD_FAST                'label'
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'label'

 L. 276       114  LOAD_GLOBAL              check_label
              116  LOAD_FAST                'label'
              118  CALL_FUNCTION_1       1  ''
              120  POP_TOP          

 L. 277       122  LOAD_GLOBAL              _punycode
              124  LOAD_FAST                'label'
              126  CALL_FUNCTION_1       1  ''
              128  STORE_FAST               'label'

 L. 278       130  LOAD_GLOBAL              _alabel_prefix
              132  LOAD_FAST                'label'
              134  BINARY_ADD       
              136  STORE_FAST               'label'

 L. 280       138  LOAD_GLOBAL              valid_label_length
              140  LOAD_FAST                'label'
              142  CALL_FUNCTION_1       1  ''
              144  POP_JUMP_IF_TRUE    154  'to 154'

 L. 281       146  LOAD_GLOBAL              IDNAError
              148  LOAD_STR                 'Label too long'
              150  CALL_FUNCTION_1       1  ''
              152  RAISE_VARARGS_1       1  'exception instance'
            154_0  COME_FROM           144  '144'

 L. 283       154  LOAD_FAST                'label'
              156  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 92_0


def ulabel(label):
    if not isinstance(label, (bytes, bytearray)):
        try:
            label = label.encode('ascii')
        except UnicodeError:
            check_label(label)
            return label
        else:
            label = label.lower()
            if label.startswith(_alabel_prefix):
                label = label[len(_alabel_prefix):]
            else:
                check_label(label)
                return label.decode('ascii')
            label = label.decode('punycode')
            check_label(label)
        return label


def uts46_remap--- This code section failed: ---

 L. 309         0  LOAD_CONST               1
                2  LOAD_CONST               ('uts46data',)
                4  IMPORT_NAME              uts46data
                6  IMPORT_FROM              uts46data
                8  STORE_FAST               'uts46data'
               10  POP_TOP          

 L. 310        12  LOAD_STR                 ''
               14  STORE_FAST               'output'

 L. 311        16  SETUP_FINALLY       240  'to 240'

 L. 312        18  LOAD_GLOBAL              enumerate
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

 L. 313        34  LOAD_GLOBAL              ord
               36  LOAD_FAST                'char'
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'code_point'

 L. 314        42  LOAD_FAST                'uts46data'
               44  LOAD_FAST                'code_point'
               46  LOAD_CONST               256
               48  COMPARE_OP               <
               50  POP_JUMP_IF_FALSE    56  'to 56'
               52  LOAD_FAST                'code_point'
               54  JUMP_FORWARD         74  'to 74'
             56_0  COME_FROM            50  '50'

 L. 315        56  LOAD_GLOBAL              bisect
               58  LOAD_METHOD              bisect_left
               60  LOAD_FAST                'uts46data'
               62  LOAD_FAST                'code_point'
               64  LOAD_STR                 'Z'
               66  BUILD_TUPLE_2         2 
               68  CALL_METHOD_2         2  ''
               70  LOAD_CONST               1
               72  BINARY_SUBTRACT  
             74_0  COME_FROM            54  '54'

 L. 314        74  BINARY_SUBSCR    
               76  STORE_FAST               'uts46row'

 L. 316        78  LOAD_FAST                'uts46row'
               80  LOAD_CONST               1
               82  BINARY_SUBSCR    
               84  STORE_FAST               'status'

 L. 317        86  LOAD_GLOBAL              len
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

 L. 318       110  LOAD_FAST                'status'
              112  LOAD_STR                 'V'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_TRUE    150  'to 150'

 L. 319       118  LOAD_FAST                'status'
              120  LOAD_STR                 'D'
              122  COMPARE_OP               ==

 L. 318       124  POP_JUMP_IF_FALSE   130  'to 130'

 L. 319       126  LOAD_FAST                'transitional'

 L. 318       128  POP_JUMP_IF_FALSE   150  'to 150'
            130_0  COME_FROM           124  '124'

 L. 320       130  LOAD_FAST                'status'
              132  LOAD_STR                 '3'
              134  COMPARE_OP               ==

 L. 318       136  POP_JUMP_IF_FALSE   160  'to 160'

 L. 320       138  LOAD_FAST                'std3_rules'

 L. 318       140  POP_JUMP_IF_FALSE   160  'to 160'

 L. 320       142  LOAD_FAST                'replacement'
              144  LOAD_CONST               None
              146  COMPARE_OP               is

 L. 318       148  POP_JUMP_IF_FALSE   160  'to 160'
            150_0  COME_FROM           128  '128'
            150_1  COME_FROM           116  '116'

 L. 321       150  LOAD_FAST                'output'
              152  LOAD_FAST                'char'
              154  INPLACE_ADD      
              156  STORE_FAST               'output'
              158  JUMP_BACK            26  'to 26'
            160_0  COME_FROM           148  '148'
            160_1  COME_FROM           140  '140'
            160_2  COME_FROM           136  '136'

 L. 322       160  LOAD_FAST                'replacement'
              162  LOAD_CONST               None
              164  COMPARE_OP               is-not
              166  POP_JUMP_IF_FALSE   210  'to 210'
              168  LOAD_FAST                'status'
              170  LOAD_STR                 'M'
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_TRUE    200  'to 200'

 L. 323       176  LOAD_FAST                'status'
              178  LOAD_STR                 '3'
              180  COMPARE_OP               ==

 L. 322       182  POP_JUMP_IF_FALSE   188  'to 188'

 L. 323       184  LOAD_FAST                'std3_rules'

 L. 322       186  POP_JUMP_IF_TRUE    200  'to 200'
            188_0  COME_FROM           182  '182'

 L. 324       188  LOAD_FAST                'status'
              190  LOAD_STR                 'D'
              192  COMPARE_OP               ==

 L. 322       194  POP_JUMP_IF_FALSE   210  'to 210'

 L. 324       196  LOAD_FAST                'transitional'

 L. 322       198  POP_JUMP_IF_FALSE   210  'to 210'
            200_0  COME_FROM           186  '186'
            200_1  COME_FROM           174  '174'

 L. 325       200  LOAD_FAST                'output'
              202  LOAD_FAST                'replacement'
              204  INPLACE_ADD      
              206  STORE_FAST               'output'
              208  JUMP_BACK            26  'to 26'
            210_0  COME_FROM           198  '198'
            210_1  COME_FROM           194  '194'
            210_2  COME_FROM           166  '166'

 L. 326       210  LOAD_FAST                'status'
              212  LOAD_STR                 'I'
              214  COMPARE_OP               !=
              216  POP_JUMP_IF_FALSE_BACK    26  'to 26'

 L. 327       218  LOAD_GLOBAL              IndexError
              220  CALL_FUNCTION_0       0  ''
              222  RAISE_VARARGS_1       1  'exception instance'
              224  JUMP_BACK            26  'to 26'
            226_0  COME_FROM            26  '26'

 L. 328       226  LOAD_GLOBAL              unicodedata
              228  LOAD_METHOD              normalize
              230  LOAD_STR                 'NFC'
              232  LOAD_FAST                'output'
              234  CALL_METHOD_2         2  ''
              236  POP_BLOCK        
              238  RETURN_VALUE     
            240_0  COME_FROM_FINALLY    16  '16'

 L. 329       240  DUP_TOP          
              242  LOAD_GLOBAL              IndexError
              244  COMPARE_OP               exception-match
          246_248  POP_JUMP_IF_FALSE   290  'to 290'
              250  POP_TOP          
              252  POP_TOP          
              254  POP_TOP          

 L. 330       256  LOAD_GLOBAL              InvalidCodepoint

 L. 331       258  LOAD_STR                 'Codepoint {0} not allowed at position {1} in {2}'
              260  LOAD_METHOD              format

 L. 332       262  LOAD_GLOBAL              _unot
              264  LOAD_FAST                'code_point'
              266  CALL_FUNCTION_1       1  ''

 L. 332       268  LOAD_FAST                'pos'
              270  LOAD_CONST               1
              272  BINARY_ADD       

 L. 332       274  LOAD_GLOBAL              repr
              276  LOAD_FAST                'domain'
              278  CALL_FUNCTION_1       1  ''

 L. 331       280  CALL_METHOD_3         3  ''

 L. 330       282  CALL_FUNCTION_1       1  ''
              284  RAISE_VARARGS_1       1  'exception instance'
              286  POP_EXCEPT       
              288  JUMP_FORWARD        292  'to 292'
            290_0  COME_FROM           246  '246'
              290  END_FINALLY      
            292_0  COME_FROM           288  '288'

Parse error at or near `DUP_TOP' instruction at offset 240


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
    while True:
        if labels:
            del (labels[0] or labels)[0]

    if not labels:
        raise IDNAError('Empty domain')
    if labels[(-1)] == '':
        del labels[-1]
        trailing_dot = True
    for label in labels:
        result.append(alabel(label))
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
    while True:
        if labels:
            del (labels[0] or labels)[0]

    if not labels:
        raise IDNAError('Empty domain')
    if not labels[(-1)]:
        del labels[-1]
        trailing_dot = True
    for label in labels:
        result.append(ulabel(label))
    else:
        if trailing_dot:
            result.append('')
        return '.'.join(result)