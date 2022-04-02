# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: chardet\universaldetector.py
"""
Module containing the UniversalDetector detector class, which is the primary
class a user of ``chardet`` should use.

:author: Mark Pilgrim (initial port to Python)
:author: Shy Shalom (original C code)
:author: Dan Blanchard (major refactoring for 3.0)
:author: Ian Cordasco
"""
import codecs, logging, re
from .charsetgroupprober import CharSetGroupProber
from .enums import InputState, LanguageFilter, ProbingState
from .escprober import EscCharSetProber
from .latin1prober import Latin1Prober
from .mbcsgroupprober import MBCSGroupProber
from .sbcsgroupprober import SBCSGroupProber

class UniversalDetector(object):
    __doc__ = '\n    The ``UniversalDetector`` class underlies the ``chardet.detect`` function\n    and coordinates all of the different charset probers.\n\n    To get a ``dict`` containing an encoding and its confidence, you can simply\n    run:\n\n    .. code::\n\n            u = UniversalDetector()\n            u.feed(some_bytes)\n            u.close()\n            detected = u.result\n\n    '
    MINIMUM_THRESHOLD = 0.2
    HIGH_BYTE_DETECTOR = re.compile(b'[\x80-\xff]')
    ESC_DETECTOR = re.compile(b'(\x1b|~{)')
    WIN_BYTE_DETECTOR = re.compile(b'[\x80-\x9f]')
    ISO_WIN_MAP = {'iso-8859-1':'Windows-1252',  'iso-8859-2':'Windows-1250', 
     'iso-8859-5':'Windows-1251', 
     'iso-8859-6':'Windows-1256', 
     'iso-8859-7':'Windows-1253', 
     'iso-8859-8':'Windows-1255', 
     'iso-8859-9':'Windows-1254', 
     'iso-8859-13':'Windows-1257'}

    def __init__(self, lang_filter=LanguageFilter.ALL):
        self._esc_charset_prober = None
        self._charset_probers = []
        self.result = None
        self.done = None
        self._got_data = None
        self._input_state = None
        self._last_char = None
        self.lang_filter = lang_filter
        self.logger = logging.getLogger(__name__)
        self._has_win_bytes = None
        self.reset()

    def reset(self):
        """
        Reset the UniversalDetector and all of its probers back to their
        initial states.  This is called by ``__init__``, so you only need to
        call this directly in between analyses of different documents.
        """
        self.result = {'encoding':None, 
         'confidence':0.0,  'language':None}
        self.done = False
        self._got_data = False
        self._has_win_bytes = False
        self._input_state = InputState.PURE_ASCII
        self._last_char = b''
        if self._esc_charset_prober:
            self._esc_charset_prober.reset()
        for prober in self._charset_probers:
            prober.reset()

    def feed--- This code section failed: ---

 L. 125         0  LOAD_FAST                'self'
                2  LOAD_ATTR                done
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 126         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 128        10  LOAD_GLOBAL              len
               12  LOAD_FAST                'byte_str'
               14  CALL_FUNCTION_1       1  ''
               16  POP_JUMP_IF_TRUE     22  'to 22'

 L. 129        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 131        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'byte_str'
               26  LOAD_GLOBAL              bytearray
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_TRUE     40  'to 40'

 L. 132        32  LOAD_GLOBAL              bytearray
               34  LOAD_FAST                'byte_str'
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'byte_str'
             40_0  COME_FROM            30  '30'

 L. 135        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _got_data
               44  POP_JUMP_IF_TRUE    222  'to 222'

 L. 137        46  LOAD_FAST                'byte_str'
               48  LOAD_METHOD              startswith
               50  LOAD_GLOBAL              codecs
               52  LOAD_ATTR                BOM_UTF8
               54  CALL_METHOD_1         1  ''
               56  POP_JUMP_IF_FALSE    74  'to 74'

 L. 139        58  LOAD_STR                 'UTF-8-SIG'

 L. 140        60  LOAD_CONST               1.0

 L. 141        62  LOAD_STR                 ''

 L. 139        64  LOAD_CONST               ('encoding', 'confidence', 'language')
               66  BUILD_CONST_KEY_MAP_3     3 
               68  LOAD_FAST                'self'
               70  STORE_ATTR               result
               72  JUMP_FORWARD        192  'to 192'
             74_0  COME_FROM            56  '56'

 L. 142        74  LOAD_FAST                'byte_str'
               76  LOAD_METHOD              startswith
               78  LOAD_GLOBAL              codecs
               80  LOAD_ATTR                BOM_UTF32_LE

 L. 143        82  LOAD_GLOBAL              codecs
               84  LOAD_ATTR                BOM_UTF32_BE

 L. 142        86  BUILD_TUPLE_2         2 
               88  CALL_METHOD_1         1  ''
               90  POP_JUMP_IF_FALSE   108  'to 108'

 L. 146        92  LOAD_STR                 'UTF-32'

 L. 147        94  LOAD_CONST               1.0

 L. 148        96  LOAD_STR                 ''

 L. 146        98  LOAD_CONST               ('encoding', 'confidence', 'language')
              100  BUILD_CONST_KEY_MAP_3     3 
              102  LOAD_FAST                'self'
              104  STORE_ATTR               result
              106  JUMP_FORWARD        192  'to 192'
            108_0  COME_FROM            90  '90'

 L. 149       108  LOAD_FAST                'byte_str'
              110  LOAD_METHOD              startswith
              112  LOAD_CONST               b'\xfe\xff\x00\x00'
              114  CALL_METHOD_1         1  ''
              116  POP_JUMP_IF_FALSE   134  'to 134'

 L. 151       118  LOAD_STR                 'X-ISO-10646-UCS-4-3412'

 L. 152       120  LOAD_CONST               1.0

 L. 153       122  LOAD_STR                 ''

 L. 151       124  LOAD_CONST               ('encoding', 'confidence', 'language')
              126  BUILD_CONST_KEY_MAP_3     3 
              128  LOAD_FAST                'self'
              130  STORE_ATTR               result
              132  JUMP_FORWARD        192  'to 192'
            134_0  COME_FROM           116  '116'

 L. 154       134  LOAD_FAST                'byte_str'
              136  LOAD_METHOD              startswith
              138  LOAD_CONST               b'\x00\x00\xff\xfe'
              140  CALL_METHOD_1         1  ''
              142  POP_JUMP_IF_FALSE   160  'to 160'

 L. 156       144  LOAD_STR                 'X-ISO-10646-UCS-4-2143'

 L. 157       146  LOAD_CONST               1.0

 L. 158       148  LOAD_STR                 ''

 L. 156       150  LOAD_CONST               ('encoding', 'confidence', 'language')
              152  BUILD_CONST_KEY_MAP_3     3 
              154  LOAD_FAST                'self'
              156  STORE_ATTR               result
              158  JUMP_FORWARD        192  'to 192'
            160_0  COME_FROM           142  '142'

 L. 159       160  LOAD_FAST                'byte_str'
              162  LOAD_METHOD              startswith
              164  LOAD_GLOBAL              codecs
              166  LOAD_ATTR                BOM_LE
              168  LOAD_GLOBAL              codecs
              170  LOAD_ATTR                BOM_BE
              172  BUILD_TUPLE_2         2 
              174  CALL_METHOD_1         1  ''
              176  POP_JUMP_IF_FALSE   192  'to 192'

 L. 162       178  LOAD_STR                 'UTF-16'

 L. 163       180  LOAD_CONST               1.0

 L. 164       182  LOAD_STR                 ''

 L. 162       184  LOAD_CONST               ('encoding', 'confidence', 'language')
              186  BUILD_CONST_KEY_MAP_3     3 
              188  LOAD_FAST                'self'
              190  STORE_ATTR               result
            192_0  COME_FROM           176  '176'
            192_1  COME_FROM           158  '158'
            192_2  COME_FROM           132  '132'
            192_3  COME_FROM           106  '106'
            192_4  COME_FROM            72  '72'

 L. 166       192  LOAD_CONST               True
              194  LOAD_FAST                'self'
              196  STORE_ATTR               _got_data

 L. 167       198  LOAD_FAST                'self'
              200  LOAD_ATTR                result
              202  LOAD_STR                 'encoding'
              204  BINARY_SUBSCR    
              206  LOAD_CONST               None
              208  <117>                 1  ''
              210  POP_JUMP_IF_FALSE   222  'to 222'

 L. 168       212  LOAD_CONST               True
              214  LOAD_FAST                'self'
              216  STORE_ATTR               done

 L. 169       218  LOAD_CONST               None
              220  RETURN_VALUE     
            222_0  COME_FROM           210  '210'
            222_1  COME_FROM            44  '44'

 L. 173       222  LOAD_FAST                'self'
              224  LOAD_ATTR                _input_state
              226  LOAD_GLOBAL              InputState
              228  LOAD_ATTR                PURE_ASCII
              230  COMPARE_OP               ==
          232_234  POP_JUMP_IF_FALSE   302  'to 302'

 L. 174       236  LOAD_FAST                'self'
              238  LOAD_ATTR                HIGH_BYTE_DETECTOR
              240  LOAD_METHOD              search
              242  LOAD_FAST                'byte_str'
              244  CALL_METHOD_1         1  ''
          246_248  POP_JUMP_IF_FALSE   260  'to 260'

 L. 175       250  LOAD_GLOBAL              InputState
              252  LOAD_ATTR                HIGH_BYTE
              254  LOAD_FAST                'self'
              256  STORE_ATTR               _input_state
              258  JUMP_FORWARD        302  'to 302'
            260_0  COME_FROM           246  '246'

 L. 176       260  LOAD_FAST                'self'
              262  LOAD_ATTR                _input_state
              264  LOAD_GLOBAL              InputState
              266  LOAD_ATTR                PURE_ASCII
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   302  'to 302'

 L. 177       274  LOAD_FAST                'self'
              276  LOAD_ATTR                ESC_DETECTOR
              278  LOAD_METHOD              search
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                _last_char
              284  LOAD_FAST                'byte_str'
              286  BINARY_ADD       
              288  CALL_METHOD_1         1  ''

 L. 176   290_292  POP_JUMP_IF_FALSE   302  'to 302'

 L. 178       294  LOAD_GLOBAL              InputState
              296  LOAD_ATTR                ESC_ASCII
              298  LOAD_FAST                'self'
              300  STORE_ATTR               _input_state
            302_0  COME_FROM           290  '290'
            302_1  COME_FROM           270  '270'
            302_2  COME_FROM           258  '258'
            302_3  COME_FROM           232  '232'

 L. 180       302  LOAD_FAST                'byte_str'
              304  LOAD_CONST               -1
              306  LOAD_CONST               None
              308  BUILD_SLICE_2         2 
              310  BINARY_SUBSCR    
              312  LOAD_FAST                'self'
              314  STORE_ATTR               _last_char

 L. 186       316  LOAD_FAST                'self'
              318  LOAD_ATTR                _input_state
              320  LOAD_GLOBAL              InputState
              322  LOAD_ATTR                ESC_ASCII
              324  COMPARE_OP               ==
          326_328  POP_JUMP_IF_FALSE   406  'to 406'

 L. 187       330  LOAD_FAST                'self'
              332  LOAD_ATTR                _esc_charset_prober
          334_336  POP_JUMP_IF_TRUE    350  'to 350'

 L. 188       338  LOAD_GLOBAL              EscCharSetProber
              340  LOAD_FAST                'self'
              342  LOAD_ATTR                lang_filter
              344  CALL_FUNCTION_1       1  ''
              346  LOAD_FAST                'self'
              348  STORE_ATTR               _esc_charset_prober
            350_0  COME_FROM           334  '334'

 L. 189       350  LOAD_FAST                'self'
              352  LOAD_ATTR                _esc_charset_prober
              354  LOAD_METHOD              feed
              356  LOAD_FAST                'byte_str'
              358  CALL_METHOD_1         1  ''
              360  LOAD_GLOBAL              ProbingState
              362  LOAD_ATTR                FOUND_IT
              364  COMPARE_OP               ==
          366_368  POP_JUMP_IF_FALSE   570  'to 570'

 L. 191       370  LOAD_FAST                'self'
              372  LOAD_ATTR                _esc_charset_prober
              374  LOAD_ATTR                charset_name

 L. 193       376  LOAD_FAST                'self'
              378  LOAD_ATTR                _esc_charset_prober
              380  LOAD_METHOD              get_confidence
              382  CALL_METHOD_0         0  ''

 L. 195       384  LOAD_FAST                'self'
              386  LOAD_ATTR                _esc_charset_prober
              388  LOAD_ATTR                language

 L. 190       390  LOAD_CONST               ('encoding', 'confidence', 'language')
              392  BUILD_CONST_KEY_MAP_3     3 
              394  LOAD_FAST                'self'
              396  STORE_ATTR               result

 L. 196       398  LOAD_CONST               True
              400  LOAD_FAST                'self'
              402  STORE_ATTR               done
              404  JUMP_FORWARD        570  'to 570'
            406_0  COME_FROM           326  '326'

 L. 203       406  LOAD_FAST                'self'
              408  LOAD_ATTR                _input_state
              410  LOAD_GLOBAL              InputState
              412  LOAD_ATTR                HIGH_BYTE
              414  COMPARE_OP               ==
          416_418  POP_JUMP_IF_FALSE   570  'to 570'

 L. 204       420  LOAD_FAST                'self'
              422  LOAD_ATTR                _charset_probers
          424_426  POP_JUMP_IF_TRUE    484  'to 484'

 L. 205       428  LOAD_GLOBAL              MBCSGroupProber
              430  LOAD_FAST                'self'
              432  LOAD_ATTR                lang_filter
              434  CALL_FUNCTION_1       1  ''
              436  BUILD_LIST_1          1 
              438  LOAD_FAST                'self'
              440  STORE_ATTR               _charset_probers

 L. 207       442  LOAD_FAST                'self'
              444  LOAD_ATTR                lang_filter
              446  LOAD_GLOBAL              LanguageFilter
              448  LOAD_ATTR                NON_CJK
              450  BINARY_AND       
          452_454  POP_JUMP_IF_FALSE   470  'to 470'

 L. 208       456  LOAD_FAST                'self'
              458  LOAD_ATTR                _charset_probers
              460  LOAD_METHOD              append
              462  LOAD_GLOBAL              SBCSGroupProber
              464  CALL_FUNCTION_0       0  ''
              466  CALL_METHOD_1         1  ''
              468  POP_TOP          
            470_0  COME_FROM           452  '452'

 L. 209       470  LOAD_FAST                'self'
              472  LOAD_ATTR                _charset_probers
              474  LOAD_METHOD              append
              476  LOAD_GLOBAL              Latin1Prober
              478  CALL_FUNCTION_0       0  ''
              480  CALL_METHOD_1         1  ''
              482  POP_TOP          
            484_0  COME_FROM           424  '424'

 L. 210       484  LOAD_FAST                'self'
              486  LOAD_ATTR                _charset_probers
              488  GET_ITER         
            490_0  COME_FROM           546  '546'
            490_1  COME_FROM           508  '508'
              490  FOR_ITER            550  'to 550'
              492  STORE_FAST               'prober'

 L. 211       494  LOAD_FAST                'prober'
              496  LOAD_METHOD              feed
              498  LOAD_FAST                'byte_str'
              500  CALL_METHOD_1         1  ''
              502  LOAD_GLOBAL              ProbingState
              504  LOAD_ATTR                FOUND_IT
              506  COMPARE_OP               ==
          508_510  POP_JUMP_IF_FALSE_BACK   490  'to 490'

 L. 212       512  LOAD_FAST                'prober'
              514  LOAD_ATTR                charset_name

 L. 213       516  LOAD_FAST                'prober'
              518  LOAD_METHOD              get_confidence
              520  CALL_METHOD_0         0  ''

 L. 214       522  LOAD_FAST                'prober'
              524  LOAD_ATTR                language

 L. 212       526  LOAD_CONST               ('encoding', 'confidence', 'language')
              528  BUILD_CONST_KEY_MAP_3     3 
              530  LOAD_FAST                'self'
              532  STORE_ATTR               result

 L. 215       534  LOAD_CONST               True
              536  LOAD_FAST                'self'
              538  STORE_ATTR               done

 L. 216       540  POP_TOP          
          542_544  BREAK_LOOP          550  'to 550'
          546_548  JUMP_BACK           490  'to 490'
            550_0  COME_FROM           542  '542'
            550_1  COME_FROM           490  '490'

 L. 217       550  LOAD_FAST                'self'
              552  LOAD_ATTR                WIN_BYTE_DETECTOR
              554  LOAD_METHOD              search
              556  LOAD_FAST                'byte_str'
              558  CALL_METHOD_1         1  ''
          560_562  POP_JUMP_IF_FALSE   570  'to 570'

 L. 218       564  LOAD_CONST               True
              566  LOAD_FAST                'self'
              568  STORE_ATTR               _has_win_bytes
            570_0  COME_FROM           560  '560'
            570_1  COME_FROM           416  '416'
            570_2  COME_FROM           404  '404'
            570_3  COME_FROM           366  '366'

Parse error at or near `<117>' instruction at offset 208

    def close--- This code section failed: ---

 L. 229         0  LOAD_FAST                'self'
                2  LOAD_ATTR                done
                4  POP_JUMP_IF_FALSE    12  'to 12'

 L. 230         6  LOAD_FAST                'self'
                8  LOAD_ATTR                result
               10  RETURN_VALUE     
             12_0  COME_FROM             4  '4'

 L. 231        12  LOAD_CONST               True
               14  LOAD_FAST                'self'
               16  STORE_ATTR               done

 L. 233        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _got_data
               22  POP_JUMP_IF_TRUE     38  'to 38'

 L. 234        24  LOAD_FAST                'self'
               26  LOAD_ATTR                logger
               28  LOAD_METHOD              debug
               30  LOAD_STR                 'no data received!'
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          
               36  JUMP_FORWARD        216  'to 216'
             38_0  COME_FROM            22  '22'

 L. 237        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _input_state
               42  LOAD_GLOBAL              InputState
               44  LOAD_ATTR                PURE_ASCII
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    66  'to 66'

 L. 238        50  LOAD_STR                 'ascii'

 L. 239        52  LOAD_CONST               1.0

 L. 240        54  LOAD_STR                 ''

 L. 238        56  LOAD_CONST               ('encoding', 'confidence', 'language')
               58  BUILD_CONST_KEY_MAP_3     3 
               60  LOAD_FAST                'self'
               62  STORE_ATTR               result
               64  JUMP_FORWARD        216  'to 216'
             66_0  COME_FROM            48  '48'

 L. 243        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _input_state
               70  LOAD_GLOBAL              InputState
               72  LOAD_ATTR                HIGH_BYTE
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE   216  'to 216'

 L. 244        78  LOAD_CONST               None
               80  STORE_FAST               'prober_confidence'

 L. 245        82  LOAD_CONST               0.0
               84  STORE_FAST               'max_prober_confidence'

 L. 246        86  LOAD_CONST               None
               88  STORE_FAST               'max_prober'

 L. 247        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _charset_probers
               94  GET_ITER         
             96_0  COME_FROM           130  '130'
             96_1  COME_FROM           120  '120'
             96_2  COME_FROM           104  '104'
               96  FOR_ITER            132  'to 132'
               98  STORE_FAST               'prober'

 L. 248       100  LOAD_FAST                'prober'
              102  POP_JUMP_IF_TRUE    106  'to 106'

 L. 249       104  JUMP_BACK            96  'to 96'
            106_0  COME_FROM           102  '102'

 L. 250       106  LOAD_FAST                'prober'
              108  LOAD_METHOD              get_confidence
              110  CALL_METHOD_0         0  ''
              112  STORE_FAST               'prober_confidence'

 L. 251       114  LOAD_FAST                'prober_confidence'
              116  LOAD_FAST                'max_prober_confidence'
              118  COMPARE_OP               >
              120  POP_JUMP_IF_FALSE_BACK    96  'to 96'

 L. 252       122  LOAD_FAST                'prober_confidence'
              124  STORE_FAST               'max_prober_confidence'

 L. 253       126  LOAD_FAST                'prober'
              128  STORE_FAST               'max_prober'
              130  JUMP_BACK            96  'to 96'
            132_0  COME_FROM            96  '96'

 L. 254       132  LOAD_FAST                'max_prober'
              134  POP_JUMP_IF_FALSE   216  'to 216'
              136  LOAD_FAST                'max_prober_confidence'
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                MINIMUM_THRESHOLD
              142  COMPARE_OP               >
              144  POP_JUMP_IF_FALSE   216  'to 216'

 L. 255       146  LOAD_FAST                'max_prober'
              148  LOAD_ATTR                charset_name
              150  STORE_FAST               'charset_name'

 L. 256       152  LOAD_FAST                'max_prober'
              154  LOAD_ATTR                charset_name
              156  LOAD_METHOD              lower
              158  CALL_METHOD_0         0  ''
              160  STORE_FAST               'lower_charset_name'

 L. 257       162  LOAD_FAST                'max_prober'
              164  LOAD_METHOD              get_confidence
              166  CALL_METHOD_0         0  ''
              168  STORE_FAST               'confidence'

 L. 260       170  LOAD_FAST                'lower_charset_name'
              172  LOAD_METHOD              startswith
              174  LOAD_STR                 'iso-8859'
              176  CALL_METHOD_1         1  ''
              178  POP_JUMP_IF_FALSE   200  'to 200'

 L. 261       180  LOAD_FAST                'self'
              182  LOAD_ATTR                _has_win_bytes
              184  POP_JUMP_IF_FALSE   200  'to 200'

 L. 262       186  LOAD_FAST                'self'
              188  LOAD_ATTR                ISO_WIN_MAP
              190  LOAD_METHOD              get
              192  LOAD_FAST                'lower_charset_name'

 L. 263       194  LOAD_FAST                'charset_name'

 L. 262       196  CALL_METHOD_2         2  ''
              198  STORE_FAST               'charset_name'
            200_0  COME_FROM           184  '184'
            200_1  COME_FROM           178  '178'

 L. 264       200  LOAD_FAST                'charset_name'

 L. 265       202  LOAD_FAST                'confidence'

 L. 266       204  LOAD_FAST                'max_prober'
              206  LOAD_ATTR                language

 L. 264       208  LOAD_CONST               ('encoding', 'confidence', 'language')
              210  BUILD_CONST_KEY_MAP_3     3 
              212  LOAD_FAST                'self'
              214  STORE_ATTR               result
            216_0  COME_FROM           144  '144'
            216_1  COME_FROM           134  '134'
            216_2  COME_FROM            76  '76'
            216_3  COME_FROM            64  '64'
            216_4  COME_FROM            36  '36'

 L. 269       216  LOAD_FAST                'self'
              218  LOAD_ATTR                logger
              220  LOAD_METHOD              getEffectiveLevel
              222  CALL_METHOD_0         0  ''
              224  LOAD_GLOBAL              logging
              226  LOAD_ATTR                DEBUG
              228  COMPARE_OP               <=
          230_232  POP_JUMP_IF_FALSE   366  'to 366'

 L. 270       234  LOAD_FAST                'self'
              236  LOAD_ATTR                result
              238  LOAD_STR                 'encoding'
              240  BINARY_SUBSCR    
              242  LOAD_CONST               None
              244  <117>                 0  ''
          246_248  POP_JUMP_IF_FALSE   366  'to 366'

 L. 271       250  LOAD_FAST                'self'
              252  LOAD_ATTR                logger
              254  LOAD_METHOD              debug
              256  LOAD_STR                 'no probers hit minimum threshold'
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          

 L. 272       262  LOAD_FAST                'self'
              264  LOAD_ATTR                _charset_probers
              266  GET_ITER         
            268_0  COME_FROM           362  '362'
            268_1  COME_FROM           334  '334'
            268_2  COME_FROM           278  '278'
              268  FOR_ITER            366  'to 366'
              270  STORE_FAST               'group_prober'

 L. 273       272  LOAD_FAST                'group_prober'
          274_276  POP_JUMP_IF_TRUE    282  'to 282'

 L. 274   278_280  JUMP_BACK           268  'to 268'
            282_0  COME_FROM           274  '274'

 L. 275       282  LOAD_GLOBAL              isinstance
              284  LOAD_FAST                'group_prober'
              286  LOAD_GLOBAL              CharSetGroupProber
              288  CALL_FUNCTION_2       2  ''
          290_292  POP_JUMP_IF_FALSE   336  'to 336'

 L. 276       294  LOAD_FAST                'group_prober'
              296  LOAD_ATTR                probers
              298  GET_ITER         
            300_0  COME_FROM           330  '330'
              300  FOR_ITER            334  'to 334'
              302  STORE_FAST               'prober'

 L. 277       304  LOAD_FAST                'self'
              306  LOAD_ATTR                logger
              308  LOAD_METHOD              debug
              310  LOAD_STR                 '%s %s confidence = %s'

 L. 278       312  LOAD_FAST                'prober'
              314  LOAD_ATTR                charset_name

 L. 279       316  LOAD_FAST                'prober'
              318  LOAD_ATTR                language

 L. 280       320  LOAD_FAST                'prober'
              322  LOAD_METHOD              get_confidence
              324  CALL_METHOD_0         0  ''

 L. 277       326  CALL_METHOD_4         4  ''
              328  POP_TOP          
          330_332  JUMP_BACK           300  'to 300'
            334_0  COME_FROM           300  '300'
              334  JUMP_BACK           268  'to 268'
            336_0  COME_FROM           290  '290'

 L. 282       336  LOAD_FAST                'self'
              338  LOAD_ATTR                logger
              340  LOAD_METHOD              debug
              342  LOAD_STR                 '%s %s confidence = %s'

 L. 283       344  LOAD_FAST                'group_prober'
              346  LOAD_ATTR                charset_name

 L. 284       348  LOAD_FAST                'group_prober'
              350  LOAD_ATTR                language

 L. 285       352  LOAD_FAST                'group_prober'
              354  LOAD_METHOD              get_confidence
              356  CALL_METHOD_0         0  ''

 L. 282       358  CALL_METHOD_4         4  ''
              360  POP_TOP          
          362_364  JUMP_BACK           268  'to 268'
            366_0  COME_FROM           268  '268'
            366_1  COME_FROM           246  '246'
            366_2  COME_FROM           230  '230'

 L. 286       366  LOAD_FAST                'self'
              368  LOAD_ATTR                result
              370  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 244