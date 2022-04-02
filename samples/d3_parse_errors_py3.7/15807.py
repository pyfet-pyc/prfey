# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\idna\core.py
from . import idnadata
import bisect, unicodedata, re, sys
from .intranges import intranges_contain
_virama_combining_class = 9
_alabel_prefix = 'xn--'
_unicode_dots_re = re.compile('[.。．｡]')
if sys.version_info[0] >= 3:
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


def check_bidi(label, check_ltr=False):
    bidi_label = False
    for idx, cp in enumerate(label, 1):
        direction = unicodedata.bidirectional(cp)
        if direction == '':
            raise IDNABidiError('Unknown directionality in label {0} at position {1}'.format(repr(label), idx))
        if direction in ('R', 'AL', 'AN'):
            bidi_label = True

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
            if joining_type == ord('T'):
                continue
            if joining_type in [ord('L'), ord('D')]:
                ok = True
                break

        if not ok:
            return False
        ok = False
        for i in range(pos + 1, len(label)):
            joining_type = idnadata.joining_types.get(ord(label[i]))
            if joining_type == ord('T'):
                continue
            if joining_type in [ord('R'), ord('D')]:
                ok = True
                break

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
                continue
            if not _is_script(cp, 'Hiragana'):
                if not _is_script(cp, 'Katakana'):
                    if _is_script(cp, 'Han'):
                        pass
            return True

        return False
    if 1632 <= cp_value <= 1641:
        for cp in label:
            if 1776 <= ord(cp) <= 1785:
                return False

        return True
    if 1776 <= cp_value <= 1785:
        for cp in label:
            if 1632 <= ord(cp) <= 1641:
                return False

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
                try:
                    if not valid_contextj(label, pos):
                        raise InvalidCodepointContext('Joiner {0} not allowed at position {1} in {2}'.format(_unot(cp_value), pos + 1, repr(label)))
                except ValueError:
                    raise IDNAError('Unknown codepoint adjacent to joiner {0} at position {1} in {2}'.format(_unot(cp_value), pos + 1, repr(label)))

            else:
                if intranges_contain(cp_value, idnadata.codepoint_classes['CONTEXTO']):
                    assert valid_contexto(label, pos), 'Codepoint {0} not allowed at position {1} in {2}'.format(_unot(cp_value), pos + 1, repr(label))
                else:
                    raise InvalidCodepoint('Codepoint {0} at position {1} of {2} not allowed'.format(_unot(cp_value), pos + 1, repr(label)))

    check_bidi(label)


def alabel(label):
    try:
        label = label.encode('ascii')
        ulabel(label)
        if not valid_label_length(label):
            raise IDNAError('Label too long')
        return label
    except UnicodeEncodeError:
        pass

    if not label:
        raise IDNAError('No Input')
    label = unicode(label)
    check_label(label)
    label = _punycode(label)
    label = _alabel_prefix + label
    if not valid_label_length(label):
        raise IDNAError('Label too long')
    return label


def ulabel(label):
    if not isinstance(label, (bytes, bytearray)):
        try:
            label = label.encode('ascii')
        except UnicodeEncodeError:
            check_label(label)
            return label

        label = label.lower()
        if label.startswith(_alabel_prefix):
            label = label[len(_alabel_prefix):]
            if not label:
                raise IDNAError('Malformed A-label, no Punycode eligible content found')
            if label.decode('ascii')[(-1)] == '-':
                raise IDNAError('A-label must not end with a hyphen')
        else:
            check_label(label)
            return label.decode('ascii')
        label = label.decode('punycode')
        check_label(label)
        return label


def uts46_remap--- This code section failed: ---

 L. 318         0  LOAD_CONST               1
                2  LOAD_CONST               ('uts46data',)
                4  IMPORT_NAME              uts46data
                6  IMPORT_FROM              uts46data
                8  STORE_FAST               'uts46data'
               10  POP_TOP          

 L. 319        12  LOAD_STR                 ''
               14  STORE_FAST               'output'

 L. 320        16  SETUP_EXCEPT        242  'to 242'

 L. 321        18  SETUP_LOOP          230  'to 230'
               20  LOAD_GLOBAL              enumerate
               22  LOAD_FAST                'domain'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  GET_ITER         
             28_0  COME_FROM           226  '226'
             28_1  COME_FROM           218  '218'
             28_2  COME_FROM           210  '210'
             28_3  COME_FROM           160  '160'
               28  FOR_ITER            228  'to 228'
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'pos'
               34  STORE_FAST               'char'

 L. 322        36  LOAD_GLOBAL              ord
               38  LOAD_FAST                'char'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  STORE_FAST               'code_point'

 L. 323        44  LOAD_FAST                'uts46data'
               46  LOAD_FAST                'code_point'
               48  LOAD_CONST               256
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    58  'to 58'
               54  LOAD_FAST                'code_point'
               56  JUMP_FORWARD         76  'to 76'
             58_0  COME_FROM            52  '52'

 L. 324        58  LOAD_GLOBAL              bisect
               60  LOAD_METHOD              bisect_left
               62  LOAD_FAST                'uts46data'
               64  LOAD_FAST                'code_point'
               66  LOAD_STR                 'Z'
               68  BUILD_TUPLE_2         2 
               70  CALL_METHOD_2         2  '2 positional arguments'
               72  LOAD_CONST               1
               74  BINARY_SUBTRACT  
             76_0  COME_FROM            56  '56'
               76  BINARY_SUBSCR    
               78  STORE_FAST               'uts46row'

 L. 325        80  LOAD_FAST                'uts46row'
               82  LOAD_CONST               1
               84  BINARY_SUBSCR    
               86  STORE_FAST               'status'

 L. 326        88  LOAD_GLOBAL              len
               90  LOAD_FAST                'uts46row'
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  LOAD_CONST               3
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   108  'to 108'
              100  LOAD_FAST                'uts46row'
              102  LOAD_CONST               2
              104  BINARY_SUBSCR    
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            98  '98'
              108  LOAD_CONST               None
            110_0  COME_FROM           106  '106'
              110  STORE_FAST               'replacement'

 L. 327       112  LOAD_FAST                'status'
              114  LOAD_STR                 'V'
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_TRUE    152  'to 152'

 L. 328       120  LOAD_FAST                'status'
              122  LOAD_STR                 'D'
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   132  'to 132'
              128  LOAD_FAST                'transitional'
              130  POP_JUMP_IF_FALSE   152  'to 152'
            132_0  COME_FROM           126  '126'

 L. 329       132  LOAD_FAST                'status'
              134  LOAD_STR                 '3'
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   162  'to 162'
              140  LOAD_FAST                'std3_rules'
              142  POP_JUMP_IF_TRUE    162  'to 162'
              144  LOAD_FAST                'replacement'
              146  LOAD_CONST               None
              148  COMPARE_OP               is
              150  POP_JUMP_IF_FALSE   162  'to 162'
            152_0  COME_FROM           130  '130'
            152_1  COME_FROM           118  '118'

 L. 330       152  LOAD_FAST                'output'
              154  LOAD_FAST                'char'
              156  INPLACE_ADD      
              158  STORE_FAST               'output'
              160  JUMP_BACK            28  'to 28'
            162_0  COME_FROM           150  '150'
            162_1  COME_FROM           142  '142'
            162_2  COME_FROM           138  '138'

 L. 331       162  LOAD_FAST                'replacement'
              164  LOAD_CONST               None
              166  COMPARE_OP               is-not
              168  POP_JUMP_IF_FALSE   212  'to 212'
              170  LOAD_FAST                'status'
              172  LOAD_STR                 'M'
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_TRUE    202  'to 202'

 L. 332       178  LOAD_FAST                'status'
              180  LOAD_STR                 '3'
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   190  'to 190'
              186  LOAD_FAST                'std3_rules'
              188  POP_JUMP_IF_FALSE   202  'to 202'
            190_0  COME_FROM           184  '184'

 L. 333       190  LOAD_FAST                'status'
              192  LOAD_STR                 'D'
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_FALSE   212  'to 212'
              198  LOAD_FAST                'transitional'
              200  POP_JUMP_IF_FALSE   212  'to 212'
            202_0  COME_FROM           188  '188'
            202_1  COME_FROM           176  '176'

 L. 334       202  LOAD_FAST                'output'
              204  LOAD_FAST                'replacement'
              206  INPLACE_ADD      
              208  STORE_FAST               'output'
              210  JUMP_BACK            28  'to 28'
            212_0  COME_FROM           200  '200'
            212_1  COME_FROM           196  '196'
            212_2  COME_FROM           168  '168'

 L. 335       212  LOAD_FAST                'status'
              214  LOAD_STR                 'I'
              216  COMPARE_OP               !=
              218  POP_JUMP_IF_FALSE_BACK    28  'to 28'

 L. 336       220  LOAD_GLOBAL              IndexError
              222  CALL_FUNCTION_0       0  '0 positional arguments'
              224  RAISE_VARARGS_1       1  'exception instance'
              226  JUMP_BACK            28  'to 28'
              228  POP_BLOCK        
            230_0  COME_FROM_LOOP       18  '18'

 L. 337       230  LOAD_GLOBAL              unicodedata
              232  LOAD_METHOD              normalize
              234  LOAD_STR                 'NFC'
              236  LOAD_FAST                'output'
              238  CALL_METHOD_2         2  '2 positional arguments'
              240  RETURN_VALUE     
            242_0  COME_FROM_EXCEPT     16  '16'

 L. 338       242  DUP_TOP          
              244  LOAD_GLOBAL              IndexError
              246  COMPARE_OP               exception-match
          248_250  POP_JUMP_IF_FALSE   292  'to 292'
              252  POP_TOP          
              254  POP_TOP          
              256  POP_TOP          

 L. 339       258  LOAD_GLOBAL              InvalidCodepoint

 L. 340       260  LOAD_STR                 'Codepoint {0} not allowed at position {1} in {2}'
              262  LOAD_METHOD              format

 L. 341       264  LOAD_GLOBAL              _unot
              266  LOAD_FAST                'code_point'
              268  CALL_FUNCTION_1       1  '1 positional argument'
              270  LOAD_FAST                'pos'
              272  LOAD_CONST               1
              274  BINARY_ADD       
              276  LOAD_GLOBAL              repr
              278  LOAD_FAST                'domain'
              280  CALL_FUNCTION_1       1  '1 positional argument'
              282  CALL_METHOD_3         3  '3 positional arguments'
              284  CALL_FUNCTION_1       1  '1 positional argument'
              286  RAISE_VARARGS_1       1  'exception instance'
              288  POP_EXCEPT       
              290  JUMP_FORWARD        294  'to 294'
            292_0  COME_FROM           248  '248'
              292  END_FINALLY      
            294_0  COME_FROM           290  '290'

Parse error at or near `COME_FROM_LOOP' instruction at offset 230_0


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

    if trailing_dot:
        result.append('')
    s = '.'.join(result)
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

    if trailing_dot:
        result.append('')
    return '.'.join(result)