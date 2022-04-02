# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: requests\packages\chardet\sjisprober.py
import sys
from .mbcharsetprober import MultiByteCharSetProber
from .codingstatemachine import CodingStateMachine
from .chardistribution import SJISDistributionAnalysis
from .jpcntx import SJISContextAnalysis
from .mbcssm import SJISSMModel
from . import constants

class SJISProber(MultiByteCharSetProber):

    def __init__(self):
        MultiByteCharSetProber.__init__(self)
        self._mCodingSM = CodingStateMachine(SJISSMModel)
        self._mDistributionAnalyzer = SJISDistributionAnalysis()
        self._mContextAnalyzer = SJISContextAnalysis()
        self.reset()

    def reset(self):
        MultiByteCharSetProber.reset(self)
        self._mContextAnalyzer.reset()

    def get_charset_name(self):
        return self._mContextAnalyzer.get_charset_name()

    def feed--- This code section failed: ---

 L.  53         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'aBuf'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'aLen'

 L.  54         8  LOAD_GLOBAL              range
               10  LOAD_CONST               0
               12  LOAD_FAST                'aLen'
               14  CALL_FUNCTION_2       2  ''
               16  GET_ITER         
             18_0  COME_FROM           138  '138'
            18_20  FOR_ITER            288  'to 288'
               22  STORE_FAST               'i'

 L.  55        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _mCodingSM
               28  LOAD_METHOD              next_state
               30  LOAD_FAST                'aBuf'
               32  LOAD_FAST                'i'
               34  BINARY_SUBSCR    
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'codingState'

 L.  56        40  LOAD_FAST                'codingState'
               42  LOAD_GLOBAL              constants
               44  LOAD_ATTR                eError
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE   104  'to 104'

 L.  57        50  LOAD_GLOBAL              constants
               52  LOAD_ATTR                _debug
               54  POP_JUMP_IF_FALSE    88  'to 88'

 L.  58        56  LOAD_GLOBAL              sys
               58  LOAD_ATTR                stderr
               60  LOAD_METHOD              write
               62  LOAD_FAST                'self'
               64  LOAD_METHOD              get_charset_name
               66  CALL_METHOD_0         0  ''

 L.  59        68  LOAD_STR                 ' prober hit error at byte '

 L.  58        70  BINARY_ADD       

 L.  59        72  LOAD_GLOBAL              str
               74  LOAD_FAST                'i'
               76  CALL_FUNCTION_1       1  ''

 L.  58        78  BINARY_ADD       

 L.  60        80  LOAD_STR                 '\n'

 L.  58        82  BINARY_ADD       
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
             88_0  COME_FROM            54  '54'

 L.  61        88  LOAD_GLOBAL              constants
               90  LOAD_ATTR                eNotMe
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _mState

 L.  62        96  POP_TOP          
           98_100  JUMP_ABSOLUTE       288  'to 288'
              102  JUMP_BACK            18  'to 18'
            104_0  COME_FROM            48  '48'

 L.  63       104  LOAD_FAST                'codingState'
              106  LOAD_GLOBAL              constants
              108  LOAD_ATTR                eItsMe
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   130  'to 130'

 L.  64       114  LOAD_GLOBAL              constants
              116  LOAD_ATTR                eFoundIt
              118  LOAD_FAST                'self'
              120  STORE_ATTR               _mState

 L.  65       122  POP_TOP          
          124_126  JUMP_ABSOLUTE       288  'to 288'
              128  JUMP_BACK            18  'to 18'
            130_0  COME_FROM           112  '112'

 L.  66       130  LOAD_FAST                'codingState'
              132  LOAD_GLOBAL              constants
              134  LOAD_ATTR                eStart
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE    18  'to 18'

 L.  67       140  LOAD_FAST                'self'
              142  LOAD_ATTR                _mCodingSM
              144  LOAD_METHOD              get_current_charlen
              146  CALL_METHOD_0         0  ''
              148  STORE_FAST               'charLen'

 L.  68       150  LOAD_FAST                'i'
              152  LOAD_CONST               0
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   218  'to 218'

 L.  69       158  LOAD_FAST                'aBuf'
              160  LOAD_CONST               0
              162  BINARY_SUBSCR    
              164  LOAD_FAST                'self'
              166  LOAD_ATTR                _mLastChar
              168  LOAD_CONST               1
              170  STORE_SUBSCR     

 L.  70       172  LOAD_FAST                'self'
              174  LOAD_ATTR                _mContextAnalyzer
              176  LOAD_METHOD              feed
              178  LOAD_FAST                'self'
              180  LOAD_ATTR                _mLastChar
              182  LOAD_CONST               2
              184  LOAD_FAST                'charLen'
              186  BINARY_SUBTRACT  
              188  LOAD_CONST               None
              190  BUILD_SLICE_2         2 
              192  BINARY_SUBSCR    

 L.  71       194  LOAD_FAST                'charLen'

 L.  70       196  CALL_METHOD_2         2  ''
              198  POP_TOP          

 L.  72       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _mDistributionAnalyzer
              204  LOAD_METHOD              feed
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                _mLastChar
              210  LOAD_FAST                'charLen'
              212  CALL_METHOD_2         2  ''
              214  POP_TOP          
              216  JUMP_BACK            18  'to 18'
            218_0  COME_FROM           156  '156'

 L.  74       218  LOAD_FAST                'self'
              220  LOAD_ATTR                _mContextAnalyzer
              222  LOAD_METHOD              feed
              224  LOAD_FAST                'aBuf'
              226  LOAD_FAST                'i'
              228  LOAD_CONST               1
              230  BINARY_ADD       
              232  LOAD_FAST                'charLen'
              234  BINARY_SUBTRACT  
              236  LOAD_FAST                'i'
              238  LOAD_CONST               3
              240  BINARY_ADD       

 L.  75       242  LOAD_FAST                'charLen'

 L.  74       244  BINARY_SUBTRACT  
              246  BUILD_SLICE_2         2 
              248  BINARY_SUBSCR    

 L.  75       250  LOAD_FAST                'charLen'

 L.  74       252  CALL_METHOD_2         2  ''
              254  POP_TOP          

 L.  76       256  LOAD_FAST                'self'
              258  LOAD_ATTR                _mDistributionAnalyzer
              260  LOAD_METHOD              feed
              262  LOAD_FAST                'aBuf'
              264  LOAD_FAST                'i'
              266  LOAD_CONST               1
              268  BINARY_SUBTRACT  
              270  LOAD_FAST                'i'
              272  LOAD_CONST               1
              274  BINARY_ADD       
              276  BUILD_SLICE_2         2 
              278  BINARY_SUBSCR    

 L.  77       280  LOAD_FAST                'charLen'

 L.  76       282  CALL_METHOD_2         2  ''
              284  POP_TOP          
              286  JUMP_BACK            18  'to 18'

 L.  79       288  LOAD_FAST                'aBuf'
              290  LOAD_FAST                'aLen'
              292  LOAD_CONST               1
              294  BINARY_SUBTRACT  
              296  BINARY_SUBSCR    
              298  LOAD_FAST                'self'
              300  LOAD_ATTR                _mLastChar
              302  LOAD_CONST               0
              304  STORE_SUBSCR     

 L.  81       306  LOAD_FAST                'self'
              308  LOAD_METHOD              get_state
              310  CALL_METHOD_0         0  ''
              312  LOAD_GLOBAL              constants
              314  LOAD_ATTR                eDetecting
              316  COMPARE_OP               ==
          318_320  POP_JUMP_IF_FALSE   358  'to 358'

 L.  82       322  LOAD_FAST                'self'
              324  LOAD_ATTR                _mContextAnalyzer
              326  LOAD_METHOD              got_enough_data
              328  CALL_METHOD_0         0  ''
          330_332  POP_JUMP_IF_FALSE   358  'to 358'

 L.  83       334  LOAD_FAST                'self'
              336  LOAD_METHOD              get_confidence
              338  CALL_METHOD_0         0  ''
              340  LOAD_GLOBAL              constants
              342  LOAD_ATTR                SHORTCUT_THRESHOLD
              344  COMPARE_OP               >

 L.  82   346_348  POP_JUMP_IF_FALSE   358  'to 358'

 L.  84       350  LOAD_GLOBAL              constants
              352  LOAD_ATTR                eFoundIt
              354  LOAD_FAST                'self'
              356  STORE_ATTR               _mState
            358_0  COME_FROM           346  '346'
            358_1  COME_FROM           330  '330'
            358_2  COME_FROM           318  '318'

 L.  86       358  LOAD_FAST                'self'
              360  LOAD_METHOD              get_state
              362  CALL_METHOD_0         0  ''
              364  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 98_100

    def get_confidence(self):
        contxtCf = self._mContextAnalyzer.get_confidence()
        distribCf = self._mDistributionAnalyzer.get_confidence()
        return maxcontxtCfdistribCf