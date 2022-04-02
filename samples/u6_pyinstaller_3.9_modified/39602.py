# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: charset_normalizer\models.py
import warnings
import encodings.aliases as aliases
from hashlib import sha256
from json import dumps
from typing import Optional, List, Tuple, Set
from collections import Counter
from re import sub, compile as re_compile
from charset_normalizer.constant import TOO_BIG_SEQUENCE
from charset_normalizer.md import mess_ratio
from charset_normalizer.utils import iana_name, is_multi_byte_encoding, unicode_range

class CharsetMatch:

    def __init__(self, payload: bytes, guessed_encoding: str, mean_mess_ratio: float, has_sig_or_bom: bool, languages: 'CoherenceMatches', decoded_payload: Optional[str]=None):
        self._payload = payload
        self._encoding = guessed_encoding
        self._mean_mess_ratio = mean_mess_ratio
        self._languages = languages
        self._has_sig_or_bom = has_sig_or_bom
        self._unicode_ranges = None
        self._leaves = []
        self._mean_coherence_ratio = 0.0
        self._output_payload = None
        self._output_encoding = None
        self._string = decoded_payload

    def __eq__(self, other) -> bool:
        if not isinstance(other, CharsetMatch):
            raise TypeError('__eq__ cannot be invoked on {} and {}.'.format(str(other.__class__), str(self.__class__)))
        return self.encoding == other.encoding and self.fingerprint == other.fingerprint

    def __lt__(self, other) -> bool:
        """
        Implemented to make sorted available upon CharsetMatches items.
        """
        if not isinstance(other, CharsetMatch):
            raise ValueError
        chaos_difference = abs(self.chaos - other.chaos)
        if chaos_difference < 0.01:
            return self.coherence > other.coherence
        return self.chaos < other.chaos

    @property
    def chaos_secondary_pass(self) -> float:
        """
        Check once again chaos in decoded text, except this time, with full content.
        Use with caution, this can be very slow.
        Notice: Will be removed in 3.0
        """
        warnings.warn('chaos_secondary_pass is deprecated and will be removed in 3.0', DeprecationWarning)
        return mess_ratio(str(self), 1.0)

    @property
    def coherence_non_latin(self) -> float:
        """
        Coherence ratio on the first non-latin language detected if ANY.
        Notice: Will be removed in 3.0
        """
        warnings.warn('coherence_non_latin is deprecated and will be removed in 3.0', DeprecationWarning)
        return 0.0

    @property
    def w_counter(self) -> Counter:
        """
        Word counter instance on decoded text.
        Notice: Will be removed in 3.0
        """
        warnings.warn('w_counter is deprecated and will be removed in 3.0', DeprecationWarning)
        not_printable_pattern = re_compile('[0-9\\W\\n\\r\\t]+')
        string_printable_only = sub(not_printable_pattern, ' ', str(self).lower())
        return Counter(string_printable_only.split())

    def __str__--- This code section failed: ---

 L.  96         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _string
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L.  97        10  LOAD_GLOBAL              str
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _payload
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _encoding
               20  LOAD_STR                 'strict'
               22  CALL_FUNCTION_3       3  ''
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _string
             28_0  COME_FROM             8  '8'

 L.  98        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _string
               32  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __repr__(self) -> str:
        return "<CharsetMatch '{}' bytes({})>".format(self.encoding, self.fingerprint)

    def add_submatch(self, other: 'CharsetMatch') -> None:
        if not isinstance(other, CharsetMatch) or other == self:
            raise ValueError('Unable to add instance <{}> as a submatch of a CharsetMatch'.format(other.__class__))
        other._string = None
        self._leaves.append(other)

    @property
    def encoding(self) -> str:
        return self._encoding

    @property
    def encoding_aliases(self) -> List[str]:
        """
        Encoding name are known by many name, using this could help when searching for IBM855 when it's listed as CP855.
        """
        also_known_as = []
        for u, p in aliases.items():
            if self.encoding == u:
                also_known_as.append(p)
            else:
                if self.encoding == p:
                    also_known_as.append(u)
                return also_known_as

    @property
    def bom(self) -> bool:
        return self._has_sig_or_bom

    @property
    def byte_order_mark(self) -> bool:
        return self._has_sig_or_bom

    @property
    def languages(self) -> List[str]:
        """
        Return the complete list of possible languages found in decoded sequence.
        Usually not really useful. Returned list may be empty even if 'language' property return something != 'Unknown'.
        """
        return [e[0] for e in self._languages]

    @property
    def language--- This code section failed: ---

 L. 149         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _languages
                4  POP_JUMP_IF_TRUE     98  'to 98'

 L. 152         6  LOAD_STR                 'ascii'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                could_be_from_charset
               12  <118>                 0  ''
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 153        16  LOAD_STR                 'English'
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 156        20  LOAD_CONST               0
               22  LOAD_CONST               ('mb_encoding_languages', 'encoding_languages')
               24  IMPORT_NAME_ATTR         charset_normalizer.cd
               26  IMPORT_FROM              mb_encoding_languages
               28  STORE_FAST               'mb_encoding_languages'
               30  IMPORT_FROM              encoding_languages
               32  STORE_FAST               'encoding_languages'
               34  POP_TOP          

 L. 158        36  LOAD_GLOBAL              is_multi_byte_encoding
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                encoding
               42  CALL_FUNCTION_1       1  ''
               44  POP_JUMP_IF_FALSE    56  'to 56'
               46  LOAD_FAST                'mb_encoding_languages'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                encoding
               52  CALL_FUNCTION_1       1  ''
               54  JUMP_FORWARD         64  'to 64'
             56_0  COME_FROM            44  '44'
               56  LOAD_FAST                'encoding_languages'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                encoding
               62  CALL_FUNCTION_1       1  ''
             64_0  COME_FROM            54  '54'
               64  STORE_FAST               'languages'

 L. 160        66  LOAD_GLOBAL              len
               68  LOAD_FAST                'languages'
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_CONST               0
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_TRUE     86  'to 86'
               78  LOAD_STR                 'Latin Based'
               80  LOAD_FAST                'languages'
               82  <118>                 0  ''
               84  POP_JUMP_IF_FALSE    90  'to 90'
             86_0  COME_FROM            76  '76'

 L. 161        86  LOAD_STR                 'Unknown'
               88  RETURN_VALUE     
             90_0  COME_FROM            84  '84'

 L. 163        90  LOAD_FAST                'languages'
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  RETURN_VALUE     
             98_0  COME_FROM             4  '4'

 L. 165        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _languages
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  LOAD_CONST               0
              108  BINARY_SUBSCR    
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 12

    @property
    def chaos(self) -> float:
        return self._mean_mess_ratio

    @property
    def coherence(self) -> float:
        if not self._languages:
            return 0.0
        return self._languages[0][1]

    @property
    def percent_chaos(self) -> float:
        return round((self.chaos * 100), ndigits=3)

    @property
    def percent_coherence(self) -> float:
        return round((self.coherence * 100), ndigits=3)

    @property
    def raw(self) -> bytes:
        """
        Original untouched bytes.
        """
        return self._payload

    @property
    def submatch(self) -> List['CharsetMatch']:
        return self._leaves

    @property
    def has_submatch(self) -> bool:
        return len(self._leaves) > 0

    @property
    def alphabets--- This code section failed: ---

 L. 202         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _unicode_ranges
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 203        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _unicode_ranges
               14  RETURN_VALUE     
             16_0  COME_FROM             8  '8'

 L. 204        16  LOAD_GLOBAL              set
               18  CALL_FUNCTION_0       0  ''
               20  STORE_FAST               'detected_ranges'

 L. 205        22  LOAD_GLOBAL              str
               24  LOAD_FAST                'self'
               26  CALL_FUNCTION_1       1  ''
               28  GET_ITER         
               30  FOR_ITER             50  'to 50'
               32  STORE_FAST               'character'

 L. 206        34  LOAD_FAST                'detected_ranges'
               36  LOAD_METHOD              add

 L. 207        38  LOAD_GLOBAL              unicode_range
               40  LOAD_FAST                'character'
               42  CALL_FUNCTION_1       1  ''

 L. 206        44  CALL_METHOD_1         1  ''
               46  POP_TOP          
               48  JUMP_BACK            30  'to 30'

 L. 209        50  LOAD_GLOBAL              sorted
               52  LOAD_GLOBAL              list
               54  LOAD_FAST                'detected_ranges'
               56  CALL_FUNCTION_1       1  ''
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _unicode_ranges

 L. 210        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _unicode_ranges
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @property
    def could_be_from_charset(self) -> List[str]:
        """
        The complete list of encoding that output the exact SAME str result and therefore could be the originating
        encoding.
        This list does include the encoding available in property 'encoding'.
        """
        return [
         self._encoding] + [m.encoding for m in self._leaves]

    def first(self) -> 'CharsetMatch':
        """
        Kept for BC reasons. Will be removed in 3.0.
        """
        return self

    def best(self) -> 'CharsetMatch':
        """
        Kept for BC reasons. Will be removed in 3.0.
        """
        return self

    def output--- This code section failed: ---

 L. 238         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _output_encoding
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_TRUE     20  'to 20'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _output_encoding
               14  LOAD_FAST                'encoding'
               16  COMPARE_OP               !=
               18  POP_JUMP_IF_FALSE    44  'to 44'
             20_0  COME_FROM             8  '8'

 L. 239        20  LOAD_FAST                'encoding'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _output_encoding

 L. 240        26  LOAD_GLOBAL              str
               28  LOAD_FAST                'self'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_METHOD              encode
               34  LOAD_FAST                'encoding'
               36  LOAD_STR                 'replace'
               38  CALL_METHOD_2         2  ''
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _output_payload
             44_0  COME_FROM            18  '18'

 L. 242        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _output_payload
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @property
    def fingerprint(self) -> str:
        """
        Retrieve the unique SHA256 computed using the transformed (re-encoded) payload. Not the original one.
        """
        return sha256(self.output()).hexdigest()


class CharsetMatches:
    __doc__ = '\n    Container with every CharsetMatch items ordered by default from most probable to the less one.\n    Act like a list(iterable) but does not implements all related methods.\n    '

    def __init__(self, results: List[CharsetMatch]=None):
        self._results = sorted(results) if results else []

    def __iter__(self):
        for result in self._results:
            (yield result)

    def __getitem__--- This code section failed: ---

 L. 269         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'item'
                4  LOAD_GLOBAL              int
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 270        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _results
               14  LOAD_FAST                'item'
               16  BINARY_SUBSCR    
               18  RETURN_VALUE     
             20_0  COME_FROM             8  '8'

 L. 271        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'item'
               24  LOAD_GLOBAL              str
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    70  'to 70'

 L. 272        30  LOAD_GLOBAL              iana_name
               32  LOAD_FAST                'item'
               34  LOAD_CONST               False
               36  CALL_FUNCTION_2       2  ''
               38  STORE_FAST               'item'

 L. 273        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _results
               44  GET_ITER         
             46_0  COME_FROM            58  '58'
               46  FOR_ITER             70  'to 70'
               48  STORE_FAST               'result'

 L. 274        50  LOAD_FAST                'item'
               52  LOAD_FAST                'result'
               54  LOAD_ATTR                could_be_from_charset
               56  <118>                 0  ''
               58  POP_JUMP_IF_FALSE    46  'to 46'

 L. 275        60  LOAD_FAST                'result'
               62  ROT_TWO          
               64  POP_TOP          
               66  RETURN_VALUE     
               68  JUMP_BACK            46  'to 46'
             70_0  COME_FROM            28  '28'

 L. 276        70  LOAD_GLOBAL              KeyError
               72  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<118>' instruction at offset 56

    def __len__(self) -> int:
        return len(self._results)

    def append(self, item: CharsetMatch) -> None:
        """
        Insert a single match. Will be inserted accordingly to preserve sort.
        Can be inserted as a submatch.
        """
        if not isinstance(item, CharsetMatch):
            raise ValueError("Cannot append instance '{}' to CharsetMatches".format(str(item.__class__)))
        if len(item.raw) <= TOO_BIG_SEQUENCE:
            for match in self._results:
                if match.fingerprint == item.fingerprint:
                    match.add_submatch(item)
                    return None

        self._results.append(item)
        self._results = sorted(self._results)

    def best(self) -> Optional['CharsetMatch']:
        """
        Simply return the first match. Strict equivalent to matches[0].
        """
        if not self._results:
            return
        return self._results[0]

    def first(self) -> Optional['CharsetMatch']:
        """
        Redundant method, call the method best(). Kept for BC reasons.
        """
        return self.best()


CoherenceMatch = Tuple[(str, float)]
CoherenceMatches = List[CoherenceMatch]

class CliDetectionResult:

    def __init__(self, path: str, encoding: str, encoding_aliases: List[str], alternative_encodings: List[str], language: str, alphabets: List[str], has_sig_or_bom: bool, chaos: float, coherence: float, unicode_path: Optional[str], is_preferred: bool):
        self.path = path
        self.unicode_path = unicode_path
        self.encoding = encoding
        self.encoding_aliases = encoding_aliases
        self.alternative_encodings = alternative_encodings
        self.language = language
        self.alphabets = alphabets
        self.has_sig_or_bom = has_sig_or_bom
        self.chaos = chaos
        self.coherence = coherence
        self.is_preferred = is_preferred

    @property
    def __dict__(self):
        return {'path':self.path, 
         'encoding':self.encoding, 
         'encoding_aliases':self.encoding_aliases, 
         'alternative_encodings':self.alternative_encodings, 
         'language':self.language, 
         'alphabets':self.alphabets, 
         'has_sig_or_bom':self.has_sig_or_bom, 
         'chaos':self.chaos, 
         'coherence':self.coherence, 
         'unicode_path':self.unicode_path, 
         'is_preferred':self.is_preferred}

    def to_json(self) -> str:
        return dumps((self.__dict__),
          ensure_ascii=True,
          indent=4)


CharsetNormalizerMatch = CharsetMatch