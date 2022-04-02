# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\requests\packages\chardet\universaldetector.py
from . import constants
import sys, codecs
from .latin1prober import Latin1Prober
from .mbcsgroupprober import MBCSGroupProber
from .sbcsgroupprober import SBCSGroupProber
from .escprober import EscCharSetProber
import re
MINIMUM_THRESHOLD = 0.2
ePureAscii = 0
eEscAscii = 1
eHighbyte = 2

class UniversalDetector:

    def __init__(self):
        self._highBitDetector = re.compile(b'[\x80-\xff]')
        self._escDetector = re.compile(b'(\x1b|~{)')
        self._mEscCharSetProber = None
        self._mCharSetProbers = []
        self.reset()

    def reset(self):
        self.result = {'encoding':None, 
         'confidence':0.0}
        self.done = False
        self._mStart = True
        self._mGotData = False
        self._mInputState = ePureAscii
        self._mLastChar = b''
        if self._mEscCharSetProber:
            self._mEscCharSetProber.reset()
        for prober in self._mCharSetProbers:
            prober.reset()

    def feed--- This code section failed: ---

 L.  65         0  LOAD_FAST                'self'
                2  LOAD_ATTR                done
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L.  66         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L.  68        10  LOAD_GLOBAL              len
               12  LOAD_FAST                'aBuf'
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'aLen'

 L.  69        18  LOAD_FAST                'aLen'
               20  POP_JUMP_IF_TRUE     26  'to 26'

 L.  70        22  LOAD_CONST               None
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L.  72        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _mGotData
               30  POP_JUMP_IF_TRUE    250  'to 250'

 L.  74        32  LOAD_FAST                'aBuf'
               34  LOAD_CONST               None
               36  LOAD_CONST               3
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  LOAD_GLOBAL              codecs
               44  LOAD_ATTR                BOM_UTF8
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    64  'to 64'

 L.  76        50  LOAD_STR                 'UTF-8-SIG'
               52  LOAD_CONST               1.0
               54  LOAD_CONST               ('encoding', 'confidence')
               56  BUILD_CONST_KEY_MAP_2     2 
               58  LOAD_FAST                'self'
               60  STORE_ATTR               result
               62  JUMP_FORWARD        250  'to 250'
             64_0  COME_FROM            48  '48'

 L.  77        64  LOAD_FAST                'aBuf'
               66  LOAD_CONST               None
               68  LOAD_CONST               4
               70  BUILD_SLICE_2         2 
               72  BINARY_SUBSCR    
               74  LOAD_GLOBAL              codecs
               76  LOAD_ATTR                BOM_UTF32_LE
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    96  'to 96'

 L.  79        82  LOAD_STR                 'UTF-32LE'
               84  LOAD_CONST               1.0
               86  LOAD_CONST               ('encoding', 'confidence')
               88  BUILD_CONST_KEY_MAP_2     2 
               90  LOAD_FAST                'self'
               92  STORE_ATTR               result
               94  JUMP_FORWARD        250  'to 250'
             96_0  COME_FROM            80  '80'

 L.  80        96  LOAD_FAST                'aBuf'
               98  LOAD_CONST               None
              100  LOAD_CONST               4
              102  BUILD_SLICE_2         2 
              104  BINARY_SUBSCR    
              106  LOAD_GLOBAL              codecs
              108  LOAD_ATTR                BOM_UTF32_BE
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   128  'to 128'

 L.  82       114  LOAD_STR                 'UTF-32BE'
              116  LOAD_CONST               1.0
              118  LOAD_CONST               ('encoding', 'confidence')
              120  BUILD_CONST_KEY_MAP_2     2 
              122  LOAD_FAST                'self'
              124  STORE_ATTR               result
              126  JUMP_FORWARD        250  'to 250'
            128_0  COME_FROM           112  '112'

 L.  83       128  LOAD_FAST                'aBuf'
              130  LOAD_CONST               None
              132  LOAD_CONST               4
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  LOAD_CONST               b'\xfe\xff\x00\x00'
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE   158  'to 158'

 L.  86       144  LOAD_STR                 'X-ISO-10646-UCS-4-3412'

 L.  87       146  LOAD_CONST               1.0

 L.  85       148  LOAD_CONST               ('encoding', 'confidence')
              150  BUILD_CONST_KEY_MAP_2     2 
              152  LOAD_FAST                'self'
              154  STORE_ATTR               result
              156  JUMP_FORWARD        250  'to 250'
            158_0  COME_FROM           142  '142'

 L.  89       158  LOAD_FAST                'aBuf'
              160  LOAD_CONST               None
              162  LOAD_CONST               4
              164  BUILD_SLICE_2         2 
              166  BINARY_SUBSCR    
              168  LOAD_CONST               b'\x00\x00\xff\xfe'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   188  'to 188'

 L.  92       174  LOAD_STR                 'X-ISO-10646-UCS-4-2143'

 L.  93       176  LOAD_CONST               1.0

 L.  91       178  LOAD_CONST               ('encoding', 'confidence')
              180  BUILD_CONST_KEY_MAP_2     2 
              182  LOAD_FAST                'self'
              184  STORE_ATTR               result
              186  JUMP_FORWARD        250  'to 250'
            188_0  COME_FROM           172  '172'

 L.  95       188  LOAD_FAST                'aBuf'
              190  LOAD_CONST               None
              192  LOAD_CONST               2
              194  BUILD_SLICE_2         2 
              196  BINARY_SUBSCR    
              198  LOAD_GLOBAL              codecs
              200  LOAD_ATTR                BOM_LE
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   220  'to 220'

 L.  97       206  LOAD_STR                 'UTF-16LE'
              208  LOAD_CONST               1.0
              210  LOAD_CONST               ('encoding', 'confidence')
              212  BUILD_CONST_KEY_MAP_2     2 
              214  LOAD_FAST                'self'
              216  STORE_ATTR               result
              218  JUMP_FORWARD        250  'to 250'
            220_0  COME_FROM           204  '204'

 L.  98       220  LOAD_FAST                'aBuf'
              222  LOAD_CONST               None
              224  LOAD_CONST               2
              226  BUILD_SLICE_2         2 
              228  BINARY_SUBSCR    
              230  LOAD_GLOBAL              codecs
              232  LOAD_ATTR                BOM_BE
              234  COMPARE_OP               ==
              236  POP_JUMP_IF_FALSE   250  'to 250'

 L. 100       238  LOAD_STR                 'UTF-16BE'
              240  LOAD_CONST               1.0
              242  LOAD_CONST               ('encoding', 'confidence')
              244  BUILD_CONST_KEY_MAP_2     2 
              246  LOAD_FAST                'self'
              248  STORE_ATTR               result
            250_0  COME_FROM           236  '236'
            250_1  COME_FROM           218  '218'
            250_2  COME_FROM           186  '186'
            250_3  COME_FROM           156  '156'
            250_4  COME_FROM           126  '126'
            250_5  COME_FROM            94  '94'
            250_6  COME_FROM            62  '62'
            250_7  COME_FROM            30  '30'

 L. 102       250  LOAD_CONST               True
              252  LOAD_FAST                'self'
              254  STORE_ATTR               _mGotData

 L. 103       256  LOAD_FAST                'self'
              258  LOAD_ATTR                result
              260  LOAD_STR                 'encoding'
              262  BINARY_SUBSCR    
          264_266  POP_JUMP_IF_FALSE   294  'to 294'
              268  LOAD_FAST                'self'
              270  LOAD_ATTR                result
              272  LOAD_STR                 'confidence'
              274  BINARY_SUBSCR    
              276  LOAD_CONST               0.0
              278  COMPARE_OP               >
          280_282  POP_JUMP_IF_FALSE   294  'to 294'

 L. 104       284  LOAD_CONST               True
              286  LOAD_FAST                'self'
              288  STORE_ATTR               done

 L. 105       290  LOAD_CONST               None
              292  RETURN_VALUE     
            294_0  COME_FROM           280  '280'
            294_1  COME_FROM           264  '264'

 L. 107       294  LOAD_FAST                'self'
              296  LOAD_ATTR                _mInputState
              298  LOAD_GLOBAL              ePureAscii
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   366  'to 366'

 L. 108       306  LOAD_FAST                'self'
              308  LOAD_ATTR                _highBitDetector
              310  LOAD_METHOD              search
              312  LOAD_FAST                'aBuf'
              314  CALL_METHOD_1         1  ''
          316_318  POP_JUMP_IF_FALSE   328  'to 328'

 L. 109       320  LOAD_GLOBAL              eHighbyte
              322  LOAD_FAST                'self'
              324  STORE_ATTR               _mInputState
              326  JUMP_FORWARD        366  'to 366'
            328_0  COME_FROM           316  '316'

 L. 110       328  LOAD_FAST                'self'
              330  LOAD_ATTR                _mInputState
              332  LOAD_GLOBAL              ePureAscii
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_FALSE   366  'to 366'

 L. 111       340  LOAD_FAST                'self'
              342  LOAD_ATTR                _escDetector
              344  LOAD_METHOD              search
              346  LOAD_FAST                'self'
              348  LOAD_ATTR                _mLastChar
              350  LOAD_FAST                'aBuf'
              352  BINARY_ADD       
              354  CALL_METHOD_1         1  ''

 L. 110   356_358  POP_JUMP_IF_FALSE   366  'to 366'

 L. 112       360  LOAD_GLOBAL              eEscAscii
              362  LOAD_FAST                'self'
              364  STORE_ATTR               _mInputState
            366_0  COME_FROM           356  '356'
            366_1  COME_FROM           336  '336'
            366_2  COME_FROM           326  '326'
            366_3  COME_FROM           302  '302'

 L. 114       366  LOAD_FAST                'aBuf'
              368  LOAD_CONST               -1
              370  LOAD_CONST               None
              372  BUILD_SLICE_2         2 
              374  BINARY_SUBSCR    
              376  LOAD_FAST                'self'
              378  STORE_ATTR               _mLastChar

 L. 116       380  LOAD_FAST                'self'
              382  LOAD_ATTR                _mInputState
              384  LOAD_GLOBAL              eEscAscii
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_FALSE   460  'to 460'

 L. 117       392  LOAD_FAST                'self'
              394  LOAD_ATTR                _mEscCharSetProber
          396_398  POP_JUMP_IF_TRUE    408  'to 408'

 L. 118       400  LOAD_GLOBAL              EscCharSetProber
              402  CALL_FUNCTION_0       0  ''
              404  LOAD_FAST                'self'
              406  STORE_ATTR               _mEscCharSetProber
            408_0  COME_FROM           396  '396'

 L. 119       408  LOAD_FAST                'self'
              410  LOAD_ATTR                _mEscCharSetProber
              412  LOAD_METHOD              feed
              414  LOAD_FAST                'aBuf'
              416  CALL_METHOD_1         1  ''
              418  LOAD_GLOBAL              constants
              420  LOAD_ATTR                eFoundIt
              422  COMPARE_OP               ==
          424_426  POP_JUMP_IF_FALSE   562  'to 562'

 L. 120       428  LOAD_FAST                'self'
              430  LOAD_ATTR                _mEscCharSetProber
              432  LOAD_METHOD              get_charset_name
              434  CALL_METHOD_0         0  ''

 L. 121       436  LOAD_FAST                'self'
              438  LOAD_ATTR                _mEscCharSetProber
              440  LOAD_METHOD              get_confidence
              442  CALL_METHOD_0         0  ''

 L. 120       444  LOAD_CONST               ('encoding', 'confidence')
              446  BUILD_CONST_KEY_MAP_2     2 
              448  LOAD_FAST                'self'
              450  STORE_ATTR               result

 L. 122       452  LOAD_CONST               True
              454  LOAD_FAST                'self'
              456  STORE_ATTR               done
              458  JUMP_FORWARD        562  'to 562'
            460_0  COME_FROM           388  '388'

 L. 123       460  LOAD_FAST                'self'
              462  LOAD_ATTR                _mInputState
              464  LOAD_GLOBAL              eHighbyte
              466  COMPARE_OP               ==
          468_470  POP_JUMP_IF_FALSE   562  'to 562'

 L. 124       472  LOAD_FAST                'self'
              474  LOAD_ATTR                _mCharSetProbers
          476_478  POP_JUMP_IF_TRUE    498  'to 498'

 L. 125       480  LOAD_GLOBAL              MBCSGroupProber
              482  CALL_FUNCTION_0       0  ''
              484  LOAD_GLOBAL              SBCSGroupProber
              486  CALL_FUNCTION_0       0  ''

 L. 126       488  LOAD_GLOBAL              Latin1Prober
              490  CALL_FUNCTION_0       0  ''

 L. 125       492  BUILD_LIST_3          3 
              494  LOAD_FAST                'self'
              496  STORE_ATTR               _mCharSetProbers
            498_0  COME_FROM           476  '476'

 L. 127       498  LOAD_FAST                'self'
              500  LOAD_ATTR                _mCharSetProbers
              502  GET_ITER         
            504_0  COME_FROM           558  '558'
            504_1  COME_FROM           522  '522'
              504  FOR_ITER            562  'to 562'
              506  STORE_FAST               'prober'

 L. 128       508  LOAD_FAST                'prober'
              510  LOAD_METHOD              feed
              512  LOAD_FAST                'aBuf'
              514  CALL_METHOD_1         1  ''
              516  LOAD_GLOBAL              constants
              518  LOAD_ATTR                eFoundIt
              520  COMPARE_OP               ==
          522_524  POP_JUMP_IF_FALSE_BACK   504  'to 504'

 L. 129       526  LOAD_FAST                'prober'
              528  LOAD_METHOD              get_charset_name
              530  CALL_METHOD_0         0  ''

 L. 130       532  LOAD_FAST                'prober'
              534  LOAD_METHOD              get_confidence
              536  CALL_METHOD_0         0  ''

 L. 129       538  LOAD_CONST               ('encoding', 'confidence')
              540  BUILD_CONST_KEY_MAP_2     2 
              542  LOAD_FAST                'self'
              544  STORE_ATTR               result

 L. 131       546  LOAD_CONST               True
              548  LOAD_FAST                'self'
              550  STORE_ATTR               done

 L. 132       552  POP_TOP          
          554_556  BREAK_LOOP          562  'to 562'
          558_560  JUMP_BACK           504  'to 504'
            562_0  COME_FROM           554  '554'
            562_1  COME_FROM           504  '504'
            562_2  COME_FROM           468  '468'
            562_3  COME_FROM           458  '458'
            562_4  COME_FROM           424  '424'

Parse error at or near `COME_FROM' instruction at offset 562_3

    def close(self):
        if self.done:
            return
        if not self._mGotData:
            if constants._debug:
                sys.stderr.write('no data received!\n')
            return
        self.done = True
        if self._mInputState == ePureAscii:
            self.result = {'encoding':'ascii', 
             'confidence':1.0}
            return self.result
        if self._mInputState == eHighbyte:
            proberConfidence = None
            maxProberConfidence = 0.0
            maxProber = None
            for prober in self._mCharSetProbers:
                if not prober:
                    pass
                else:
                    proberConfidence = prober.get_confidence()
                    if proberConfidence > maxProberConfidence:
                        maxProberConfidence = proberConfidence
                        maxProber = prober
            else:
                if maxProber:
                    if maxProberConfidence > MINIMUM_THRESHOLD:
                        self.result = {'encoding':maxProber.get_charset_name(), 
                         'confidence':maxProber.get_confidence()}
                        return self.result

        if constants._debug:
            sys.stderr.write('no probers hit minimum threshhold\n')
            for prober in self._mCharSetProbers[0].mProbers:
                if not prober:
                    pass
                else:
                    sys.stderr.write('%s confidence = %s\n' % (
                     prober.get_charset_name(),
                     prober.get_confidence()))