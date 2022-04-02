# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: charset_normalizer\md.py
from functools import lru_cache
from typing import Optional, List
from charset_normalizer.constant import UNICODE_SECONDARY_RANGE_KEYWORD
from charset_normalizer.utils import is_punctuation, is_symbol, unicode_range, is_accentuated, is_latin, remove_accent, is_separator, is_cjk

class MessDetectorPlugin:
    __doc__ = '\n    Base abstract class used for mess detection plugins.\n    All detectors MUST extend and implement given methods.\n    '

    def eligible(self, character: str) -> bool:
        """
        Determine if given character should be fed in.
        """
        raise NotImplementedError

    def feed(self, character: str) -> None:
        """
        The main routine to be executed upon character.
        Insert the logic in witch the text would be considered chaotic.
        """
        raise NotImplementedError

    def reset(self) -> None:
        """
        Permit to reset the plugin to the initial state.
        """
        raise NotImplementedError

    @property
    def ratio(self) -> float:
        """
        Compute the chaos ratio based on what your feed() has seen.
        Must NOT be lower than 0.; No restriction gt 0.
        """
        raise NotImplementedError


class TooManySymbolOrPunctuationPlugin(MessDetectorPlugin):

    def __init__(self):
        self._punctuation_count = 0
        self._symbol_count = 0
        self._character_count = 0
        self._last_printable_char = None
        self._frenzy_symbol_in_word = False

    def eligible(self, character: str) -> bool:
        return character.isprintable()

    def feed--- This code section failed: ---

 L.  57         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                _character_count
                6  LOAD_CONST               1
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               _character_count

 L.  59        14  LOAD_FAST                'character'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _last_printable_char
               20  COMPARE_OP               !=
               22  POP_JUMP_IF_FALSE    90  'to 90'
               24  LOAD_FAST                'character'
               26  LOAD_CONST               ('<', '>', '=', ':', '/', '&', ';', '{', '}', '[', ']')
               28  <118>                 1  ''
               30  POP_JUMP_IF_FALSE    90  'to 90'

 L.  60        32  LOAD_GLOBAL              is_punctuation
               34  LOAD_FAST                'character'
               36  CALL_FUNCTION_1       1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'

 L.  61        40  LOAD_FAST                'self'
               42  DUP_TOP          
               44  LOAD_ATTR                _punctuation_count
               46  LOAD_CONST               1
               48  INPLACE_ADD      
               50  ROT_TWO          
               52  STORE_ATTR               _punctuation_count
               54  JUMP_FORWARD         90  'to 90'
             56_0  COME_FROM            38  '38'

 L.  62        56  LOAD_FAST                'character'
               58  LOAD_METHOD              isdigit
               60  CALL_METHOD_0         0  ''
               62  LOAD_CONST               False
               64  <117>                 0  ''
               66  POP_JUMP_IF_FALSE    90  'to 90'
               68  LOAD_GLOBAL              is_symbol
               70  LOAD_FAST                'character'
               72  CALL_FUNCTION_1       1  ''
               74  POP_JUMP_IF_FALSE    90  'to 90'

 L.  63        76  LOAD_FAST                'self'
               78  DUP_TOP          
               80  LOAD_ATTR                _symbol_count
               82  LOAD_CONST               2
               84  INPLACE_ADD      
               86  ROT_TWO          
               88  STORE_ATTR               _symbol_count
             90_0  COME_FROM            74  '74'
             90_1  COME_FROM            66  '66'
             90_2  COME_FROM            54  '54'
             90_3  COME_FROM            30  '30'
             90_4  COME_FROM            22  '22'

 L.  65        90  LOAD_FAST                'character'
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _last_printable_char

Parse error at or near `<118>' instruction at offset 28

    def reset(self) -> None:
        self._punctuation_count = 0
        self._character_count = 0
        self._symbol_count = 0

    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        ratio_of_punctuation = (self._punctuation_count + self._symbol_count) / self._character_count
        if ratio_of_punctuation >= 0.3:
            return ratio_of_punctuation
        return 0.0


class TooManyAccentuatedPlugin(MessDetectorPlugin):

    def __init__(self):
        self._character_count = 0
        self._accentuated_count = 0

    def eligible(self, character: str) -> bool:
        return character.isalpha()

    def feed(self, character: str) -> None:
        self._character_count += 1
        if is_accentuated(character):
            self._accentuated_count += 1

    def reset(self) -> None:
        self._character_count = 0
        self._accentuated_count = 0

    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        ratio_of_accentuation = self._accentuated_count / self._character_count
        if ratio_of_accentuation >= 0.35:
            return ratio_of_accentuation
        return 0.0


class UnprintablePlugin(MessDetectorPlugin):

    def __init__(self):
        self._unprintable_count = 0
        self._character_count = 0

    def eligible(self, character: str) -> bool:
        return True

    def feed--- This code section failed: ---

 L. 119         0  LOAD_FAST                'character'
                2  LOAD_CONST               frozenset({'\n', '\r', '\t'})
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    34  'to 34'
                8  LOAD_FAST                'character'
               10  LOAD_METHOD              isprintable
               12  CALL_METHOD_0         0  ''
               14  LOAD_CONST               False
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    34  'to 34'

 L. 120        20  LOAD_FAST                'self'
               22  DUP_TOP          
               24  LOAD_ATTR                _unprintable_count
               26  LOAD_CONST               1
               28  INPLACE_ADD      
               30  ROT_TWO          
               32  STORE_ATTR               _unprintable_count
             34_0  COME_FROM            18  '18'
             34_1  COME_FROM             6  '6'

 L. 121        34  LOAD_FAST                'self'
               36  DUP_TOP          
               38  LOAD_ATTR                _character_count
               40  LOAD_CONST               1
               42  INPLACE_ADD      
               44  ROT_TWO          
               46  STORE_ATTR               _character_count

Parse error at or near `None' instruction at offset -1

    def reset(self) -> None:
        self._unprintable_count = 0

    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        return self._unprintable_count * 8 / self._character_count


class SuspiciousDuplicateAccentPlugin(MessDetectorPlugin):

    def __init__(self):
        self._successive_count = 0
        self._character_count = 0
        self._last_latin_character = None

    def eligible(self, character: str) -> bool:
        return is_latin(character)

    def feed--- This code section failed: ---

 L. 146         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _last_latin_character
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    60  'to 60'

 L. 147        10  LOAD_GLOBAL              is_accentuated
               12  LOAD_FAST                'character'
               14  CALL_FUNCTION_1       1  ''
               16  POP_JUMP_IF_FALSE    60  'to 60'
               18  LOAD_GLOBAL              is_accentuated
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _last_latin_character
               24  CALL_FUNCTION_1       1  ''
               26  POP_JUMP_IF_FALSE    60  'to 60'

 L. 148        28  LOAD_GLOBAL              remove_accent
               30  LOAD_FAST                'character'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_GLOBAL              remove_accent
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _last_latin_character
               40  CALL_FUNCTION_1       1  ''
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    60  'to 60'

 L. 149        46  LOAD_FAST                'self'
               48  DUP_TOP          
               50  LOAD_ATTR                _successive_count
               52  LOAD_CONST               1
               54  INPLACE_ADD      
               56  ROT_TWO          
               58  STORE_ATTR               _successive_count
             60_0  COME_FROM            44  '44'
             60_1  COME_FROM            26  '26'
             60_2  COME_FROM            16  '16'
             60_3  COME_FROM             8  '8'

 L. 150        60  LOAD_FAST                'character'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _last_latin_character

Parse error at or near `None' instruction at offset -1

    def reset(self) -> None:
        self._successive_count = 0
        self._character_count = 0
        self._last_latin_character = None

    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        return self._successive_count * 2 / self._character_count


class SuspiciousRange(MessDetectorPlugin):

    def __init__(self):
        self._suspicious_successive_range_count = 0
        self._character_count = 0
        self._last_printable_seen = None

    def eligible(self, character: str) -> bool:
        return character.isprintable()

    def feed--- This code section failed: ---

 L. 176         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                _character_count
                6  LOAD_CONST               1
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               _character_count

 L. 178        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _last_printable_seen
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    34  'to 34'

 L. 179        24  LOAD_FAST                'character'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _last_printable_seen

 L. 180        30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            22  '22'

 L. 182        34  LOAD_FAST                'character'
               36  LOAD_METHOD              isspace
               38  CALL_METHOD_0         0  ''
               40  POP_JUMP_IF_TRUE     50  'to 50'
               42  LOAD_GLOBAL              is_punctuation
               44  LOAD_FAST                'character'
               46  CALL_FUNCTION_1       1  ''
               48  POP_JUMP_IF_FALSE    60  'to 60'
             50_0  COME_FROM            40  '40'

 L. 183        50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _last_printable_seen

 L. 184        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            48  '48'

 L. 186        60  LOAD_GLOBAL              unicode_range
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _last_printable_seen
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'unicode_range_a'

 L. 187        70  LOAD_GLOBAL              unicode_range
               72  LOAD_FAST                'character'
               74  CALL_FUNCTION_1       1  ''
               76  STORE_FAST               'unicode_range_b'

 L. 189        78  LOAD_GLOBAL              is_suspiciously_successive_range
               80  LOAD_FAST                'unicode_range_a'
               82  LOAD_FAST                'unicode_range_b'
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_FALSE   102  'to 102'

 L. 190        88  LOAD_FAST                'self'
               90  DUP_TOP          
               92  LOAD_ATTR                _suspicious_successive_range_count
               94  LOAD_CONST               1
               96  INPLACE_ADD      
               98  ROT_TWO          
              100  STORE_ATTR               _suspicious_successive_range_count
            102_0  COME_FROM            86  '86'

 L. 192       102  LOAD_FAST                'character'
              104  LOAD_FAST                'self'
              106  STORE_ATTR               _last_printable_seen

Parse error at or near `<117>' instruction at offset 20

    def reset(self) -> None:
        self._character_count = 0
        self._suspicious_successive_range_count = 0
        self._last_printable_seen = None

    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        ratio_of_suspicious_range_usage = self._suspicious_successive_range_count * 2 / self._character_count
        if ratio_of_suspicious_range_usage < 0.1:
            return 0.0
        return ratio_of_suspicious_range_usage


class SuperWeirdWordPlugin(MessDetectorPlugin):

    def __init__(self):
        self._word_count = 0
        self._bad_word_count = 0
        self._is_current_word_bad = False
        self._character_count = 0
        self._bad_character_count = 0
        self._buffer = ''
        self._buffer_accent_count = 0

    def eligible(self, character: str) -> bool:
        return True

    def feed--- This code section failed: ---

 L. 229         0  LOAD_FAST                'character'
                2  LOAD_METHOD              isalpha
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_FALSE    52  'to 52'

 L. 230         8  LOAD_STR                 ''
               10  LOAD_METHOD              join
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _buffer
               16  LOAD_FAST                'character'
               18  BUILD_LIST_2          2 
               20  CALL_METHOD_1         1  ''
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _buffer

 L. 231        26  LOAD_GLOBAL              is_accentuated
               28  LOAD_FAST                'character'
               30  CALL_FUNCTION_1       1  ''
               32  POP_JUMP_IF_FALSE    48  'to 48'

 L. 232        34  LOAD_FAST                'self'
               36  DUP_TOP          
               38  LOAD_ATTR                _buffer_accent_count
               40  LOAD_CONST               1
               42  INPLACE_ADD      
               44  ROT_TWO          
               46  STORE_ATTR               _buffer_accent_count
             48_0  COME_FROM            32  '32'

 L. 233        48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM             6  '6'

 L. 234        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _buffer
               56  POP_JUMP_IF_TRUE     62  'to 62'

 L. 235        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            56  '56'

 L. 236        62  LOAD_FAST                'character'
               64  LOAD_METHOD              isspace
               66  CALL_METHOD_0         0  ''
               68  POP_JUMP_IF_TRUE     86  'to 86'
               70  LOAD_GLOBAL              is_punctuation
               72  LOAD_FAST                'character'
               74  CALL_FUNCTION_1       1  ''
               76  POP_JUMP_IF_TRUE     86  'to 86'
               78  LOAD_GLOBAL              is_separator
               80  LOAD_FAST                'character'
               82  CALL_FUNCTION_1       1  ''
               84  POP_JUMP_IF_FALSE   218  'to 218'
             86_0  COME_FROM            76  '76'
             86_1  COME_FROM            68  '68'
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _buffer
               90  POP_JUMP_IF_FALSE   218  'to 218'

 L. 237        92  LOAD_FAST                'self'
               94  DUP_TOP          
               96  LOAD_ATTR                _word_count
               98  LOAD_CONST               1
              100  INPLACE_ADD      
              102  ROT_TWO          
              104  STORE_ATTR               _word_count

 L. 238       106  LOAD_GLOBAL              len
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _buffer
              112  CALL_FUNCTION_1       1  ''
              114  STORE_FAST               'buffer_length'

 L. 240       116  LOAD_FAST                'self'
              118  DUP_TOP          
              120  LOAD_ATTR                _character_count
              122  LOAD_FAST                'buffer_length'
              124  INPLACE_ADD      
              126  ROT_TWO          
              128  STORE_ATTR               _character_count

 L. 242       130  LOAD_FAST                'buffer_length'
              132  LOAD_CONST               4
              134  COMPARE_OP               >=
              136  POP_JUMP_IF_FALSE   158  'to 158'
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                _buffer_accent_count
              142  LOAD_FAST                'buffer_length'
              144  BINARY_TRUE_DIVIDE
              146  LOAD_CONST               0.3
              148  COMPARE_OP               >=
              150  POP_JUMP_IF_FALSE   158  'to 158'

 L. 243       152  LOAD_CONST               True
              154  LOAD_FAST                'self'
              156  STORE_ATTR               _is_current_word_bad
            158_0  COME_FROM           150  '150'
            158_1  COME_FROM           136  '136'

 L. 245       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _is_current_word_bad
              162  POP_JUMP_IF_FALSE   204  'to 204'

 L. 246       164  LOAD_FAST                'self'
              166  DUP_TOP          
              168  LOAD_ATTR                _bad_word_count
              170  LOAD_CONST               1
              172  INPLACE_ADD      
              174  ROT_TWO          
              176  STORE_ATTR               _bad_word_count

 L. 247       178  LOAD_FAST                'self'
              180  DUP_TOP          
              182  LOAD_ATTR                _bad_character_count
              184  LOAD_GLOBAL              len
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                _buffer
              190  CALL_FUNCTION_1       1  ''
              192  INPLACE_ADD      
              194  ROT_TWO          
              196  STORE_ATTR               _bad_character_count

 L. 248       198  LOAD_CONST               False
              200  LOAD_FAST                'self'
              202  STORE_ATTR               _is_current_word_bad
            204_0  COME_FROM           162  '162'

 L. 250       204  LOAD_STR                 ''
              206  LOAD_FAST                'self'
              208  STORE_ATTR               _buffer

 L. 251       210  LOAD_CONST               0
              212  LOAD_FAST                'self'
              214  STORE_ATTR               _buffer_accent_count
              216  JUMP_FORWARD        272  'to 272'
            218_0  COME_FROM            90  '90'
            218_1  COME_FROM            84  '84'

 L. 252       218  LOAD_FAST                'character'
              220  LOAD_CONST               frozenset({'=', '>', '-', '<'})
              222  <118>                 1  ''
          224_226  POP_JUMP_IF_FALSE   272  'to 272'
              228  LOAD_FAST                'character'
              230  LOAD_METHOD              isdigit
              232  CALL_METHOD_0         0  ''
              234  LOAD_CONST               False
              236  <117>                 0  ''
          238_240  POP_JUMP_IF_FALSE   272  'to 272'
              242  LOAD_GLOBAL              is_symbol
              244  LOAD_FAST                'character'
              246  CALL_FUNCTION_1       1  ''
          248_250  POP_JUMP_IF_FALSE   272  'to 272'

 L. 253       252  LOAD_CONST               True
              254  LOAD_FAST                'self'
              256  STORE_ATTR               _is_current_word_bad

 L. 254       258  LOAD_FAST                'self'
              260  DUP_TOP          
              262  LOAD_ATTR                _buffer
              264  LOAD_FAST                'character'
              266  INPLACE_ADD      
              268  ROT_TWO          
              270  STORE_ATTR               _buffer
            272_0  COME_FROM           248  '248'
            272_1  COME_FROM           238  '238'
            272_2  COME_FROM           224  '224'
            272_3  COME_FROM           216  '216'

Parse error at or near `<118>' instruction at offset 222

    def reset(self) -> None:
        self._buffer = ''
        self._is_current_word_bad = False
        self._bad_word_count = 0
        self._word_count = 0
        self._character_count = 0
        self._bad_character_count = 0

    @property
    def ratio(self) -> float:
        if self._word_count <= 16:
            return 0.0
        return self._bad_character_count / self._character_count


class CjkInvalidStopPlugin(MessDetectorPlugin):
    __doc__ = "\n    GB(Chinese) based encoding often render the stop incorrectly when the content does not fit and can be easily detected.\n    Searching for the overuse of '丅' and '丄'.\n    "

    def __init__(self):
        self._wrong_stop_count = 0
        self._cjk_character_count = 0

    def eligible(self, character: str) -> bool:
        return True

    def feed--- This code section failed: ---

 L. 286         0  LOAD_FAST                'character'
                2  LOAD_CONST               ('丅', '丄')
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    26  'to 26'

 L. 287         8  LOAD_FAST                'self'
               10  DUP_TOP          
               12  LOAD_ATTR                _wrong_stop_count
               14  LOAD_CONST               1
               16  INPLACE_ADD      
               18  ROT_TWO          
               20  STORE_ATTR               _wrong_stop_count

 L. 288        22  LOAD_CONST               None
               24  RETURN_VALUE     
             26_0  COME_FROM             6  '6'

 L. 289        26  LOAD_GLOBAL              is_cjk
               28  LOAD_FAST                'character'
               30  CALL_FUNCTION_1       1  ''
               32  POP_JUMP_IF_FALSE    48  'to 48'

 L. 290        34  LOAD_FAST                'self'
               36  DUP_TOP          
               38  LOAD_ATTR                _cjk_character_count
               40  LOAD_CONST               1
               42  INPLACE_ADD      
               44  ROT_TWO          
               46  STORE_ATTR               _cjk_character_count
             48_0  COME_FROM            32  '32'

Parse error at or near `None' instruction at offset -1

    def reset(self) -> None:
        self._wrong_stop_count = 0
        self._cjk_character_count = 0

    @property
    def ratio(self) -> float:
        if self._cjk_character_count < 16:
            return 0.0
        return self._wrong_stop_count / self._cjk_character_count


class ArchaicUpperLowerPlugin(MessDetectorPlugin):

    def __init__(self):
        self._buf = False
        self._successive_upper_lower_count = 0
        self._character_count = 0
        self._last_alpha_seen = None

    def eligible(self, character: str) -> bool:
        return character.isspace() or character.isalpha()

    def feed--- This code section failed: ---

 L. 316         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _last_alpha_seen
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    86  'to 86'

 L. 317        10  LOAD_FAST                'character'
               12  LOAD_METHOD              isupper
               14  CALL_METHOD_0         0  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _last_alpha_seen
               22  LOAD_METHOD              islower
               24  CALL_METHOD_0         0  ''
               26  POP_JUMP_IF_TRUE     46  'to 46'
             28_0  COME_FROM            16  '16'
               28  LOAD_FAST                'character'
               30  LOAD_METHOD              islower
               32  CALL_METHOD_0         0  ''
               34  POP_JUMP_IF_FALSE    80  'to 80'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _last_alpha_seen
               40  LOAD_METHOD              isupper
               42  CALL_METHOD_0         0  ''
               44  POP_JUMP_IF_FALSE    80  'to 80'
             46_0  COME_FROM            26  '26'

 L. 318        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _buf
               50  LOAD_CONST               True
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    72  'to 72'

 L. 319        56  LOAD_FAST                'self'
               58  DUP_TOP          
               60  LOAD_ATTR                _successive_upper_lower_count
               62  LOAD_CONST               1
               64  INPLACE_ADD      
               66  ROT_TWO          
               68  STORE_ATTR               _successive_upper_lower_count
               70  JUMP_ABSOLUTE        86  'to 86'
             72_0  COME_FROM            54  '54'

 L. 321        72  LOAD_CONST               True
               74  LOAD_FAST                'self'
               76  STORE_ATTR               _buf
               78  JUMP_FORWARD         86  'to 86'
             80_0  COME_FROM            44  '44'
             80_1  COME_FROM            34  '34'

 L. 323        80  LOAD_CONST               False
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _buf
             86_0  COME_FROM            78  '78'
             86_1  COME_FROM             8  '8'

 L. 325        86  LOAD_FAST                'self'
               88  DUP_TOP          
               90  LOAD_ATTR                _character_count
               92  LOAD_CONST               1
               94  INPLACE_ADD      
               96  ROT_TWO          
               98  STORE_ATTR               _character_count

 L. 326       100  LOAD_FAST                'character'
              102  LOAD_FAST                'self'
              104  STORE_ATTR               _last_alpha_seen

Parse error at or near `None' instruction at offset -1

    def reset(self) -> None:
        self._character_count = 0
        self._successive_upper_lower_count = 0
        self._last_alpha_seen = None

    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        return self._successive_upper_lower_count * 2 / self._character_count


def is_suspiciously_successive_range--- This code section failed: ---

 L. 345         0  LOAD_FAST                'unicode_range_a'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  LOAD_FAST                'unicode_range_b'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    20  'to 20'
             16_0  COME_FROM             6  '6'

 L. 346        16  LOAD_CONST               True
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 348        20  LOAD_FAST                'unicode_range_a'
               22  LOAD_FAST                'unicode_range_b'
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 349        28  LOAD_CONST               False
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L. 351        32  LOAD_STR                 'Latin'
               34  LOAD_FAST                'unicode_range_a'
               36  <118>                 0  ''
               38  POP_JUMP_IF_FALSE    52  'to 52'
               40  LOAD_STR                 'Latin'
               42  LOAD_FAST                'unicode_range_b'
               44  <118>                 0  ''
               46  POP_JUMP_IF_FALSE    52  'to 52'

 L. 352        48  LOAD_CONST               False
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'
             52_1  COME_FROM            38  '38'

 L. 354        52  LOAD_STR                 'Emoticons'
               54  LOAD_FAST                'unicode_range_a'
               56  <118>                 0  ''
               58  POP_JUMP_IF_TRUE     68  'to 68'
               60  LOAD_STR                 'Emoticons'
               62  LOAD_FAST                'unicode_range_b'
               64  <118>                 0  ''
               66  POP_JUMP_IF_FALSE    72  'to 72'
             68_0  COME_FROM            58  '58'

 L. 355        68  LOAD_CONST               False
               70  RETURN_VALUE     
             72_0  COME_FROM            66  '66'

 L. 357        72  LOAD_FAST                'unicode_range_a'
               74  LOAD_METHOD              split
               76  LOAD_STR                 ' '
               78  CALL_METHOD_1         1  ''
               80  LOAD_FAST                'unicode_range_b'
               82  LOAD_METHOD              split
               84  LOAD_STR                 ' '
               86  CALL_METHOD_1         1  ''
               88  ROT_TWO          
               90  STORE_FAST               'keywords_range_a'
               92  STORE_FAST               'keywords_range_b'

 L. 359        94  LOAD_FAST                'keywords_range_a'
               96  GET_ITER         
             98_0  COME_FROM           118  '118'
               98  FOR_ITER            128  'to 128'
              100  STORE_FAST               'el'

 L. 360       102  LOAD_FAST                'el'
              104  LOAD_GLOBAL              UNICODE_SECONDARY_RANGE_KEYWORD
              106  <118>                 0  ''
              108  POP_JUMP_IF_FALSE   112  'to 112'

 L. 361       110  JUMP_BACK            98  'to 98'
            112_0  COME_FROM           108  '108'

 L. 362       112  LOAD_FAST                'el'
              114  LOAD_FAST                'keywords_range_b'
              116  <118>                 0  ''
              118  POP_JUMP_IF_FALSE    98  'to 98'

 L. 363       120  POP_TOP          
              122  LOAD_CONST               False
              124  RETURN_VALUE     
              126  JUMP_BACK            98  'to 98'

 L. 366       128  LOAD_FAST                'unicode_range_a'
              130  LOAD_CONST               ('Katakana', 'Hiragana')
              132  <118>                 0  ''
              134  POP_JUMP_IF_FALSE   148  'to 148'
              136  LOAD_FAST                'unicode_range_b'
              138  LOAD_CONST               ('Katakana', 'Hiragana')
              140  <118>                 0  ''
              142  POP_JUMP_IF_FALSE   148  'to 148'

 L. 367       144  LOAD_CONST               False
              146  RETURN_VALUE     
            148_0  COME_FROM           142  '142'
            148_1  COME_FROM           134  '134'

 L. 369       148  LOAD_FAST                'unicode_range_a'
              150  LOAD_CONST               ('Katakana', 'Hiragana')
              152  <118>                 0  ''
              154  POP_JUMP_IF_TRUE    164  'to 164'
              156  LOAD_FAST                'unicode_range_b'
              158  LOAD_CONST               ('Katakana', 'Hiragana')
              160  <118>                 0  ''
              162  POP_JUMP_IF_FALSE   184  'to 184'
            164_0  COME_FROM           154  '154'

 L. 370       164  LOAD_STR                 'CJK'
              166  LOAD_FAST                'unicode_range_a'
              168  <118>                 0  ''
              170  POP_JUMP_IF_TRUE    180  'to 180'
              172  LOAD_STR                 'CJK'
              174  LOAD_FAST                'unicode_range_b'
              176  <118>                 0  ''
              178  POP_JUMP_IF_FALSE   184  'to 184'
            180_0  COME_FROM           170  '170'

 L. 371       180  LOAD_CONST               False
              182  RETURN_VALUE     
            184_0  COME_FROM           178  '178'
            184_1  COME_FROM           162  '162'

 L. 373       184  LOAD_STR                 'Hangul'
              186  LOAD_FAST                'unicode_range_a'
              188  <118>                 0  ''
              190  POP_JUMP_IF_TRUE    200  'to 200'
              192  LOAD_STR                 'Hangul'
              194  LOAD_FAST                'unicode_range_b'
              196  <118>                 0  ''
              198  POP_JUMP_IF_FALSE   240  'to 240'
            200_0  COME_FROM           190  '190'

 L. 374       200  LOAD_STR                 'CJK'
              202  LOAD_FAST                'unicode_range_a'
              204  <118>                 0  ''
              206  POP_JUMP_IF_TRUE    216  'to 216'
              208  LOAD_STR                 'CJK'
              210  LOAD_FAST                'unicode_range_b'
              212  <118>                 0  ''
              214  POP_JUMP_IF_FALSE   220  'to 220'
            216_0  COME_FROM           206  '206'

 L. 375       216  LOAD_CONST               False
              218  RETURN_VALUE     
            220_0  COME_FROM           214  '214'

 L. 376       220  LOAD_FAST                'unicode_range_a'
              222  LOAD_STR                 'Basic Latin'
              224  COMPARE_OP               ==
              226  POP_JUMP_IF_TRUE    236  'to 236'
              228  LOAD_FAST                'unicode_range_b'
              230  LOAD_STR                 'Basic Latin'
              232  COMPARE_OP               ==
              234  POP_JUMP_IF_FALSE   240  'to 240'
            236_0  COME_FROM           226  '226'

 L. 377       236  LOAD_CONST               False
              238  RETURN_VALUE     
            240_0  COME_FROM           234  '234'
            240_1  COME_FROM           198  '198'

 L. 380       240  LOAD_STR                 'CJK'
              242  LOAD_FAST                'unicode_range_a'
              244  <118>                 0  ''
          246_248  POP_JUMP_IF_TRUE    280  'to 280'
              250  LOAD_STR                 'CJK'
              252  LOAD_FAST                'unicode_range_b'
              254  <118>                 0  ''
          256_258  POP_JUMP_IF_TRUE    280  'to 280'
              260  LOAD_FAST                'unicode_range_a'
              262  LOAD_CONST               ('Katakana', 'Hiragana')
              264  <118>                 0  ''
          266_268  POP_JUMP_IF_FALSE   328  'to 328'
              270  LOAD_FAST                'unicode_range_b'
              272  LOAD_CONST               ('Katakana', 'Hiragana')
              274  <118>                 0  ''
          276_278  POP_JUMP_IF_FALSE   328  'to 328'
            280_0  COME_FROM           256  '256'
            280_1  COME_FROM           246  '246'

 L. 381       280  LOAD_STR                 'Punctuation'
              282  LOAD_FAST                'unicode_range_a'
              284  <118>                 0  ''
          286_288  POP_JUMP_IF_TRUE    300  'to 300'
              290  LOAD_STR                 'Punctuation'
              292  LOAD_FAST                'unicode_range_b'
              294  <118>                 0  ''
          296_298  POP_JUMP_IF_FALSE   304  'to 304'
            300_0  COME_FROM           286  '286'

 L. 382       300  LOAD_CONST               False
              302  RETURN_VALUE     
            304_0  COME_FROM           296  '296'

 L. 383       304  LOAD_STR                 'Forms'
              306  LOAD_FAST                'unicode_range_a'
              308  <118>                 0  ''
          310_312  POP_JUMP_IF_TRUE    324  'to 324'
              314  LOAD_STR                 'Forms'
              316  LOAD_FAST                'unicode_range_b'
              318  <118>                 0  ''
          320_322  POP_JUMP_IF_FALSE   328  'to 328'
            324_0  COME_FROM           310  '310'

 L. 384       324  LOAD_CONST               False
              326  RETURN_VALUE     
            328_0  COME_FROM           320  '320'
            328_1  COME_FROM           276  '276'
            328_2  COME_FROM           266  '266'

 L. 386       328  LOAD_CONST               True
              330  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


@lru_cache(maxsize=2048)
def mess_ratio(decoded_sequence: str, maximum_threshold: float=0.2, debug: bool=False) -> float:
    """
    Compute a mess ratio given a decoded bytes sequence. The maximum threshold does stop the computation earlier.
    """
    detectors = []
    for md_class in MessDetectorPlugin.__subclasses__():
        detectors.appendmd_class()
    else:
        length = len(decoded_sequence)
        mean_mess_ratio = 0.0
        if length < 512:
            intermediary_mean_mess_ratio_calc = 32
        else:
            if length <= 1024:
                intermediary_mean_mess_ratio_calc = 64
            else:
                intermediary_mean_mess_ratio_calc = 128
        for character, index in zip(decoded_sequence, range(0, length)):
            for detector in detectors:
                if detector.eligiblecharacter:
                    detector.feedcharacter
                if not (index > 0 and index % intermediary_mean_mess_ratio_calc == 0):
                    if index == length - 1:
                        mean_mess_ratio = sum([dt.ratio for dt in detectors])
                        if mean_mess_ratio >= maximum_threshold:
                            break
                    if debug:
                        for dt in detectors:
                            print(dt.__class__, dt.ratio)

                else:
                    return round(mean_mess_ratio, 3)