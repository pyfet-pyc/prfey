# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: chardet\hebrewprober.py
from .charsetprober import CharSetProber
from .enums import ProbingState

class HebrewProber(CharSetProber):
    FINAL_KAF = 234
    NORMAL_KAF = 235
    FINAL_MEM = 237
    NORMAL_MEM = 238
    FINAL_NUN = 239
    NORMAL_NUN = 240
    FINAL_PE = 243
    NORMAL_PE = 244
    FINAL_TSADI = 245
    NORMAL_TSADI = 246
    MIN_FINAL_CHAR_DISTANCE = 5
    MIN_MODEL_DISTANCE = 0.01
    VISUAL_HEBREW_NAME = 'ISO-8859-8'
    LOGICAL_HEBREW_NAME = 'windows-1255'

    def __init__(self):
        super(HebrewProber, self).__init__()
        self._final_char_logical_score = None
        self._final_char_visual_score = None
        self._prev = None
        self._before_prev = None
        self._logical_prober = None
        self._visual_prober = None
        self.reset()

    def reset(self):
        self._final_char_logical_score = 0
        self._final_char_visual_score = 0
        self._prev = ' '
        self._before_prev = ' '

    def set_model_probers(self, logicalProber, visualProber):
        self._logical_prober = logicalProber
        self._visual_prober = visualProber

    def is_final--- This code section failed: ---

 L. 179         0  LOAD_FAST                'c'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                FINAL_KAF
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                FINAL_MEM
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                FINAL_NUN

 L. 180        14  LOAD_FAST                'self'
               16  LOAD_ATTR                FINAL_PE
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                FINAL_TSADI

 L. 179        22  BUILD_TUPLE_5         5 
               24  <118>                 0  ''
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 24

    def is_non_final--- This code section failed: ---

 L. 193         0  LOAD_FAST                'c'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                NORMAL_KAF
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                NORMAL_MEM

 L. 194        10  LOAD_FAST                'self'
               12  LOAD_ATTR                NORMAL_NUN
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                NORMAL_PE

 L. 193        18  BUILD_TUPLE_4         4 
               20  <118>                 0  ''
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 20

    def feed(self, byte_str):
        if self.state == ProbingState.NOT_ME:
            return ProbingState.NOT_ME
        byte_str = self.filter_high_byte_only(byte_str)
        for cur in byte_str:
            if cur == ' ':
                if self._before_prev != ' ':
                    if self.is_final(self._prev):
                        self._final_char_logical_score += 1
                    elif self.is_non_final(self._prev):
                        self._final_char_visual_score += 1
            elif self._before_prev == ' ':
                if self.is_final(self._prev):
                    if cur != ' ':
                        self._final_char_visual_score += 1
            self._before_prev = self._prev
            self._prev = cur
        else:
            return ProbingState.DETECTING

    @property
    def charset_name(self):
        finalsub = self._final_char_logical_score - self._final_char_visual_score
        if finalsub >= self.MIN_FINAL_CHAR_DISTANCE:
            return self.LOGICAL_HEBREW_NAME
        if finalsub <= -self.MIN_FINAL_CHAR_DISTANCE:
            return self.VISUAL_HEBREW_NAME
        modelsub = self._logical_prober.get_confidence() - self._visual_prober.get_confidence()
        if modelsub > self.MIN_MODEL_DISTANCE:
            return self.LOGICAL_HEBREW_NAME
        if modelsub < -self.MIN_MODEL_DISTANCE:
            return self.VISUAL_HEBREW_NAME
        if finalsub < 0.0:
            return self.VISUAL_HEBREW_NAME
        return self.LOGICAL_HEBREW_NAME

    @property
    def language(self):
        return 'Hebrew'

    @property
    def state(self):
        if self._logical_prober.state == ProbingState.NOT_ME:
            if self._visual_prober.state == ProbingState.NOT_ME:
                return ProbingState.NOT_ME
        return ProbingState.DETECTING