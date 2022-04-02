# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: yarl\_quoting_py.py
import codecs, re
from string import ascii_letters, ascii_lowercase, digits
from typing import Optional, cast
BASCII_LOWERCASE = ascii_lowercase.encode('ascii')
BPCT_ALLOWED = {'%{:02X}'.format(i).encode('ascii') for i in range(256)}
GEN_DELIMS = ':/?#[]@'
SUB_DELIMS_WITHOUT_QS = "!$'()*,"
SUB_DELIMS = SUB_DELIMS_WITHOUT_QS + '+&=;'
RESERVED = GEN_DELIMS + SUB_DELIMS
UNRESERVED = ascii_letters + digits + '-._~'
ALLOWED = UNRESERVED + SUB_DELIMS_WITHOUT_QS
_IS_HEX = re.compile(b'[A-Z0-9][A-Z0-9]')
_IS_HEX_STR = re.compile('[A-Fa-f0-9][A-Fa-f0-9]')
utf8_decoder = codecs.getincrementaldecoder('utf-8')

class _Quoter:

    def __init__(self, *, safe: str='', protected: str='', qs: bool=False, requote: bool=True) -> None:
        self._safe = safe
        self._protected = protected
        self._qs = qs
        self._requote = requote

    def __call__--- This code section failed: ---

 L.  38         0  LOAD_FAST                'val'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  39         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  40        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'val'
               16  LOAD_GLOBAL              str
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     30  'to 30'

 L.  41        22  LOAD_GLOBAL              TypeError
               24  LOAD_STR                 'Argument should be str'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L.  42        30  LOAD_FAST                'val'
               32  POP_JUMP_IF_TRUE     38  'to 38'

 L.  43        34  LOAD_STR                 ''
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L.  44        38  LOAD_GLOBAL              cast
               40  LOAD_GLOBAL              str
               42  LOAD_FAST                'val'
               44  CALL_FUNCTION_2       2  ''
               46  LOAD_ATTR                encode
               48  LOAD_STR                 'utf8'
               50  LOAD_STR                 'ignore'
               52  LOAD_CONST               ('errors',)
               54  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               56  STORE_FAST               'bval'

 L.  45        58  LOAD_GLOBAL              bytearray
               60  CALL_FUNCTION_0       0  ''
               62  STORE_FAST               'ret'

 L.  46        64  LOAD_GLOBAL              bytearray
               66  CALL_FUNCTION_0       0  ''
               68  STORE_FAST               'pct'

 L.  47        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _safe
               74  STORE_FAST               'safe'

 L.  48        76  LOAD_FAST                'safe'
               78  LOAD_GLOBAL              ALLOWED
               80  INPLACE_ADD      
               82  STORE_FAST               'safe'

 L.  49        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _qs
               88  POP_JUMP_IF_TRUE     98  'to 98'

 L.  50        90  LOAD_FAST                'safe'
               92  LOAD_STR                 '+&=;'
               94  INPLACE_ADD      
               96  STORE_FAST               'safe'
             98_0  COME_FROM            88  '88'

 L.  51        98  LOAD_FAST                'safe'
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                _protected
              104  INPLACE_ADD      
              106  STORE_FAST               'safe'

 L.  52       108  LOAD_FAST                'safe'
              110  LOAD_METHOD              encode
              112  LOAD_STR                 'ascii'
              114  CALL_METHOD_1         1  ''
              116  STORE_FAST               'bsafe'

 L.  53       118  LOAD_CONST               0
              120  STORE_FAST               'idx'
            122_0  COME_FROM           604  '604'
            122_1  COME_FROM           580  '580'
            122_2  COME_FROM           558  '558'
            122_3  COME_FROM           520  '520'
            122_4  COME_FROM           508  '508'
            122_5  COME_FROM           454  '454'
            122_6  COME_FROM           426  '426'
            122_7  COME_FROM           414  '414'
            122_8  COME_FROM           402  '402'
            122_9  COME_FROM           326  '326'
           122_10  COME_FROM           246  '246'

 L.  54       122  LOAD_FAST                'idx'
              124  LOAD_GLOBAL              len
              126  LOAD_FAST                'bval'
              128  CALL_FUNCTION_1       1  ''
              130  COMPARE_OP               <
          132_134  POP_JUMP_IF_FALSE   606  'to 606'

 L.  55       136  LOAD_FAST                'bval'
              138  LOAD_FAST                'idx'
              140  BINARY_SUBSCR    
              142  STORE_FAST               'ch'

 L.  56       144  LOAD_FAST                'idx'
              146  LOAD_CONST               1
              148  INPLACE_ADD      
              150  STORE_FAST               'idx'

 L.  58       152  LOAD_FAST                'pct'
          154_156  POP_JUMP_IF_FALSE   458  'to 458'

 L.  59       158  LOAD_FAST                'ch'
              160  LOAD_GLOBAL              BASCII_LOWERCASE
              162  <118>                 0  ''
              164  POP_JUMP_IF_FALSE   174  'to 174'

 L.  60       166  LOAD_FAST                'ch'
              168  LOAD_CONST               32
              170  BINARY_SUBTRACT  
              172  STORE_FAST               'ch'
            174_0  COME_FROM           164  '164'

 L.  61       174  LOAD_FAST                'pct'
              176  LOAD_METHOD              append
              178  LOAD_FAST                'ch'
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L.  62       184  LOAD_GLOBAL              len
              186  LOAD_FAST                'pct'
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_CONST               3
              192  COMPARE_OP               ==
          194_196  POP_JUMP_IF_FALSE   404  'to 404'

 L.  63       198  LOAD_FAST                'pct'
              200  LOAD_CONST               1
              202  LOAD_CONST               None
              204  BUILD_SLICE_2         2 
              206  BINARY_SUBSCR    
              208  STORE_FAST               'buf'

 L.  64       210  LOAD_GLOBAL              _IS_HEX
              212  LOAD_METHOD              match
              214  LOAD_FAST                'buf'
              216  CALL_METHOD_1         1  ''
              218  POP_JUMP_IF_TRUE    248  'to 248'

 L.  65       220  LOAD_FAST                'ret'
              222  LOAD_METHOD              extend
              224  LOAD_CONST               b'%25'
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L.  66       230  LOAD_FAST                'pct'
              232  LOAD_METHOD              clear
              234  CALL_METHOD_0         0  ''
              236  POP_TOP          

 L.  67       238  LOAD_FAST                'idx'
              240  LOAD_CONST               2
              242  INPLACE_SUBTRACT 
              244  STORE_FAST               'idx'

 L.  68       246  JUMP_BACK           122  'to 122'
            248_0  COME_FROM           218  '218'

 L.  69       248  SETUP_FINALLY       284  'to 284'

 L.  70       250  LOAD_GLOBAL              chr
              252  LOAD_GLOBAL              int
              254  LOAD_FAST                'pct'
              256  LOAD_CONST               1
              258  LOAD_CONST               None
              260  BUILD_SLICE_2         2 
              262  BINARY_SUBSCR    
              264  LOAD_METHOD              decode
              266  LOAD_STR                 'ascii'
              268  CALL_METHOD_1         1  ''
              270  LOAD_CONST               16
              272  LOAD_CONST               ('base',)
              274  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              276  CALL_FUNCTION_1       1  ''
              278  STORE_FAST               'unquoted'
              280  POP_BLOCK        
              282  JUMP_FORWARD        334  'to 334'
            284_0  COME_FROM_FINALLY   248  '248'

 L.  71       284  DUP_TOP          
              286  LOAD_GLOBAL              ValueError
          288_290  <121>               332  ''
              292  POP_TOP          
              294  POP_TOP          
              296  POP_TOP          

 L.  72       298  LOAD_FAST                'ret'
              300  LOAD_METHOD              extend
              302  LOAD_CONST               b'%25'
              304  CALL_METHOD_1         1  ''
              306  POP_TOP          

 L.  73       308  LOAD_FAST                'pct'
              310  LOAD_METHOD              clear
              312  CALL_METHOD_0         0  ''
              314  POP_TOP          

 L.  74       316  LOAD_FAST                'idx'
              318  LOAD_CONST               2
              320  INPLACE_SUBTRACT 
              322  STORE_FAST               'idx'

 L.  75       324  POP_EXCEPT       
              326  JUMP_BACK           122  'to 122'
              328  POP_EXCEPT       
              330  JUMP_FORWARD        334  'to 334'
              332  <48>             
            334_0  COME_FROM           330  '330'
            334_1  COME_FROM           282  '282'

 L.  77       334  LOAD_FAST                'unquoted'
              336  LOAD_FAST                'self'
              338  LOAD_ATTR                _protected
              340  <118>                 0  ''
          342_344  POP_JUMP_IF_FALSE   358  'to 358'

 L.  78       346  LOAD_FAST                'ret'
              348  LOAD_METHOD              extend
              350  LOAD_FAST                'pct'
              352  CALL_METHOD_1         1  ''
              354  POP_TOP          
              356  JUMP_FORWARD        394  'to 394'
            358_0  COME_FROM           342  '342'

 L.  79       358  LOAD_FAST                'unquoted'
              360  LOAD_FAST                'safe'
              362  <118>                 0  ''
          364_366  POP_JUMP_IF_FALSE   384  'to 384'

 L.  80       368  LOAD_FAST                'ret'
              370  LOAD_METHOD              append
              372  LOAD_GLOBAL              ord
              374  LOAD_FAST                'unquoted'
              376  CALL_FUNCTION_1       1  ''
              378  CALL_METHOD_1         1  ''
              380  POP_TOP          
              382  JUMP_FORWARD        394  'to 394'
            384_0  COME_FROM           364  '364'

 L.  82       384  LOAD_FAST                'ret'
              386  LOAD_METHOD              extend
              388  LOAD_FAST                'pct'
              390  CALL_METHOD_1         1  ''
              392  POP_TOP          
            394_0  COME_FROM           382  '382'
            394_1  COME_FROM           356  '356'

 L.  83       394  LOAD_FAST                'pct'
              396  LOAD_METHOD              clear
              398  CALL_METHOD_0         0  ''
              400  POP_TOP          
              402  JUMP_BACK           122  'to 122'
            404_0  COME_FROM           194  '194'

 L.  86       404  LOAD_GLOBAL              len
              406  LOAD_FAST                'pct'
              408  CALL_FUNCTION_1       1  ''
              410  LOAD_CONST               2
              412  COMPARE_OP               ==
              414  POP_JUMP_IF_FALSE_BACK   122  'to 122'
              416  LOAD_FAST                'idx'
              418  LOAD_GLOBAL              len
              420  LOAD_FAST                'bval'
              422  CALL_FUNCTION_1       1  ''
              424  COMPARE_OP               ==
              426  POP_JUMP_IF_FALSE_BACK   122  'to 122'

 L.  87       428  LOAD_FAST                'ret'
              430  LOAD_METHOD              extend
              432  LOAD_CONST               b'%25'
              434  CALL_METHOD_1         1  ''
              436  POP_TOP          

 L.  88       438  LOAD_FAST                'pct'
              440  LOAD_METHOD              clear
              442  CALL_METHOD_0         0  ''
              444  POP_TOP          

 L.  89       446  LOAD_FAST                'idx'
              448  LOAD_CONST               1
              450  INPLACE_SUBTRACT 
              452  STORE_FAST               'idx'

 L.  91       454  JUMP_BACK           122  'to 122'
              456  BREAK_LOOP          522  'to 522'
            458_0  COME_FROM           154  '154'

 L.  93       458  LOAD_FAST                'ch'
              460  LOAD_GLOBAL              ord
              462  LOAD_STR                 '%'
              464  CALL_FUNCTION_1       1  ''
              466  COMPARE_OP               ==
          468_470  POP_JUMP_IF_FALSE   522  'to 522'
              472  LOAD_FAST                'self'
              474  LOAD_ATTR                _requote
          476_478  POP_JUMP_IF_FALSE   522  'to 522'

 L.  94       480  LOAD_FAST                'pct'
              482  LOAD_METHOD              clear
              484  CALL_METHOD_0         0  ''
              486  POP_TOP          

 L.  95       488  LOAD_FAST                'pct'
              490  LOAD_METHOD              append
              492  LOAD_FAST                'ch'
              494  CALL_METHOD_1         1  ''
              496  POP_TOP          

 L.  98       498  LOAD_FAST                'idx'
              500  LOAD_GLOBAL              len
              502  LOAD_FAST                'bval'
              504  CALL_FUNCTION_1       1  ''
              506  COMPARE_OP               ==
              508  POP_JUMP_IF_FALSE_BACK   122  'to 122'

 L.  99       510  LOAD_FAST                'ret'
              512  LOAD_METHOD              extend
              514  LOAD_CONST               b'%25'
              516  CALL_METHOD_1         1  ''
              518  POP_TOP          

 L. 101       520  JUMP_BACK           122  'to 122'
            522_0  COME_FROM           476  '476'
            522_1  COME_FROM           468  '468'
            522_2  COME_FROM           456  '456'

 L. 103       522  LOAD_FAST                'self'
              524  LOAD_ATTR                _qs
          526_528  POP_JUMP_IF_FALSE   560  'to 560'

 L. 104       530  LOAD_FAST                'ch'
              532  LOAD_GLOBAL              ord
              534  LOAD_STR                 ' '
              536  CALL_FUNCTION_1       1  ''
              538  COMPARE_OP               ==
          540_542  POP_JUMP_IF_FALSE   560  'to 560'

 L. 105       544  LOAD_FAST                'ret'
              546  LOAD_METHOD              append
              548  LOAD_GLOBAL              ord
              550  LOAD_STR                 '+'
              552  CALL_FUNCTION_1       1  ''
              554  CALL_METHOD_1         1  ''
              556  POP_TOP          

 L. 106       558  JUMP_BACK           122  'to 122'
            560_0  COME_FROM           540  '540'
            560_1  COME_FROM           526  '526'

 L. 107       560  LOAD_FAST                'ch'
              562  LOAD_FAST                'bsafe'
              564  <118>                 0  ''
          566_568  POP_JUMP_IF_FALSE   582  'to 582'

 L. 108       570  LOAD_FAST                'ret'
              572  LOAD_METHOD              append
              574  LOAD_FAST                'ch'
              576  CALL_METHOD_1         1  ''
              578  POP_TOP          

 L. 109       580  JUMP_BACK           122  'to 122'
            582_0  COME_FROM           566  '566'

 L. 111       582  LOAD_FAST                'ret'
              584  LOAD_METHOD              extend
              586  LOAD_STR                 '%{:02X}'
              588  LOAD_METHOD              format
              590  LOAD_FAST                'ch'
              592  CALL_METHOD_1         1  ''
              594  LOAD_METHOD              encode
              596  LOAD_STR                 'ascii'
              598  CALL_METHOD_1         1  ''
              600  CALL_METHOD_1         1  ''
              602  POP_TOP          
              604  JUMP_BACK           122  'to 122'
            606_0  COME_FROM           132  '132'

 L. 113       606  LOAD_FAST                'ret'
              608  LOAD_METHOD              decode
              610  LOAD_STR                 'ascii'
              612  CALL_METHOD_1         1  ''
              614  STORE_FAST               'ret2'

 L. 114       616  LOAD_FAST                'ret2'
              618  LOAD_FAST                'val'
              620  COMPARE_OP               ==
          622_624  POP_JUMP_IF_FALSE   630  'to 630'

 L. 115       626  LOAD_FAST                'val'
              628  RETURN_VALUE     
            630_0  COME_FROM           622  '622'

 L. 116       630  LOAD_FAST                'ret2'
              632  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class _Unquoter:

    def __init__(self, *, unsafe: str='', qs: bool=False) -> None:
        self._unsafe = unsafe
        self._qs = qs
        self._quoter = _Quoter
        self._qs_quoter = _Quoter(qs=True)

    def __call__--- This code section failed: ---

 L. 127         0  LOAD_FAST                'val'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 128         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 129        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'val'
               16  LOAD_GLOBAL              str
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     30  'to 30'

 L. 130        22  LOAD_GLOBAL              TypeError
               24  LOAD_STR                 'Argument should be str'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L. 131        30  LOAD_FAST                'val'
               32  POP_JUMP_IF_TRUE     38  'to 38'

 L. 132        34  LOAD_STR                 ''
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L. 133        38  LOAD_GLOBAL              cast
               40  LOAD_GLOBAL              codecs
               42  LOAD_ATTR                BufferedIncrementalDecoder
               44  LOAD_GLOBAL              utf8_decoder
               46  CALL_FUNCTION_0       0  ''
               48  CALL_FUNCTION_2       2  ''
               50  STORE_FAST               'decoder'

 L. 134        52  BUILD_LIST_0          0 
               54  STORE_FAST               'ret'

 L. 135        56  LOAD_CONST               0
               58  STORE_FAST               'idx'
             60_0  COME_FROM           648  '648'
             60_1  COME_FROM           636  '636'
             60_2  COME_FROM           566  '566'
             60_3  COME_FROM           554  '554'
             60_4  COME_FROM           452  '452'
             60_5  COME_FROM           440  '440'
             60_6  COME_FROM           388  '388'
             60_7  COME_FROM           330  '330'
             60_8  COME_FROM           310  '310'

 L. 136        60  LOAD_FAST                'idx'
               62  LOAD_GLOBAL              len
               64  LOAD_FAST                'val'
               66  CALL_FUNCTION_1       1  ''
               68  COMPARE_OP               <
            70_72  POP_JUMP_IF_FALSE   650  'to 650'

 L. 137        74  LOAD_FAST                'val'
               76  LOAD_FAST                'idx'
               78  BINARY_SUBSCR    
               80  STORE_FAST               'ch'

 L. 138        82  LOAD_FAST                'idx'
               84  LOAD_CONST               1
               86  INPLACE_ADD      
               88  STORE_FAST               'idx'

 L. 139        90  LOAD_FAST                'ch'
               92  LOAD_STR                 '%'
               94  COMPARE_OP               ==
            96_98  POP_JUMP_IF_FALSE   454  'to 454'
              100  LOAD_FAST                'idx'
              102  LOAD_GLOBAL              len
              104  LOAD_FAST                'val'
              106  CALL_FUNCTION_1       1  ''
              108  LOAD_CONST               2
              110  BINARY_SUBTRACT  
              112  COMPARE_OP               <=
          114_116  POP_JUMP_IF_FALSE   454  'to 454'

 L. 140       118  LOAD_FAST                'val'
              120  LOAD_FAST                'idx'
              122  LOAD_FAST                'idx'
              124  LOAD_CONST               2
              126  BINARY_ADD       
              128  BUILD_SLICE_2         2 
              130  BINARY_SUBSCR    
              132  STORE_FAST               'pct'

 L. 141       134  LOAD_GLOBAL              _IS_HEX_STR
              136  LOAD_METHOD              fullmatch
              138  LOAD_FAST                'pct'
              140  CALL_METHOD_1         1  ''
          142_144  POP_JUMP_IF_FALSE   454  'to 454'

 L. 142       146  LOAD_GLOBAL              bytes
              148  LOAD_GLOBAL              int
              150  LOAD_FAST                'pct'
              152  LOAD_CONST               16
              154  LOAD_CONST               ('base',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  BUILD_LIST_1          1 
              160  CALL_FUNCTION_1       1  ''
              162  STORE_FAST               'b'

 L. 143       164  LOAD_FAST                'idx'
              166  LOAD_CONST               2
              168  INPLACE_ADD      
              170  STORE_FAST               'idx'

 L. 144       172  SETUP_FINALLY       188  'to 188'

 L. 145       174  LOAD_FAST                'decoder'
              176  LOAD_METHOD              decode
              178  LOAD_FAST                'b'
              180  CALL_METHOD_1         1  ''
              182  STORE_FAST               'unquoted'
              184  POP_BLOCK        
              186  JUMP_FORWARD        324  'to 324'
            188_0  COME_FROM_FINALLY   172  '172'

 L. 146       188  DUP_TOP          
              190  LOAD_GLOBAL              UnicodeDecodeError
          192_194  <121>               322  ''
              196  POP_TOP          
              198  POP_TOP          
              200  POP_TOP          

 L. 147       202  LOAD_FAST                'idx'
              204  LOAD_CONST               3
              206  BINARY_SUBTRACT  
              208  LOAD_GLOBAL              len
              210  LOAD_FAST                'decoder'
              212  LOAD_ATTR                buffer
              214  CALL_FUNCTION_1       1  ''
              216  LOAD_CONST               3
              218  BINARY_MULTIPLY  
              220  BINARY_SUBTRACT  
              222  STORE_FAST               'start_pct'

 L. 148       224  LOAD_FAST                'ret'
              226  LOAD_METHOD              append
              228  LOAD_FAST                'val'
              230  LOAD_FAST                'start_pct'
              232  LOAD_FAST                'idx'
              234  LOAD_CONST               3
              236  BINARY_SUBTRACT  
              238  BUILD_SLICE_2         2 
              240  BINARY_SUBSCR    
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          

 L. 149       246  LOAD_FAST                'decoder'
              248  LOAD_METHOD              reset
              250  CALL_METHOD_0         0  ''
              252  POP_TOP          

 L. 150       254  SETUP_FINALLY       270  'to 270'

 L. 151       256  LOAD_FAST                'decoder'
              258  LOAD_METHOD              decode
              260  LOAD_FAST                'b'
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               'unquoted'
              266  POP_BLOCK        
              268  JUMP_FORWARD        318  'to 318'
            270_0  COME_FROM_FINALLY   254  '254'

 L. 152       270  DUP_TOP          
              272  LOAD_GLOBAL              UnicodeDecodeError
          274_276  <121>               316  ''
              278  POP_TOP          
              280  POP_TOP          
              282  POP_TOP          

 L. 153       284  LOAD_FAST                'ret'
              286  LOAD_METHOD              append
              288  LOAD_FAST                'val'
              290  LOAD_FAST                'idx'
              292  LOAD_CONST               3
              294  BINARY_SUBTRACT  
              296  LOAD_FAST                'idx'
              298  BUILD_SLICE_2         2 
              300  BINARY_SUBSCR    
              302  CALL_METHOD_1         1  ''
              304  POP_TOP          

 L. 154       306  POP_EXCEPT       
              308  POP_EXCEPT       
              310  JUMP_BACK            60  'to 60'
              312  POP_EXCEPT       
              314  JUMP_FORWARD        318  'to 318'
              316  <48>             
            318_0  COME_FROM           314  '314'
            318_1  COME_FROM           268  '268'
              318  POP_EXCEPT       
              320  JUMP_FORWARD        324  'to 324'
              322  <48>             
            324_0  COME_FROM           320  '320'
            324_1  COME_FROM           186  '186'

 L. 155       324  LOAD_FAST                'unquoted'
          326_328  POP_JUMP_IF_TRUE    332  'to 332'

 L. 156       330  JUMP_BACK            60  'to 60'
            332_0  COME_FROM           326  '326'

 L. 157       332  LOAD_FAST                'self'
              334  LOAD_ATTR                _qs
          336_338  POP_JUMP_IF_FALSE   390  'to 390'
              340  LOAD_FAST                'unquoted'
              342  LOAD_STR                 '+=&;'
              344  <118>                 0  ''
          346_348  POP_JUMP_IF_FALSE   390  'to 390'

 L. 158       350  LOAD_FAST                'self'
              352  LOAD_METHOD              _qs_quoter
              354  LOAD_FAST                'unquoted'
              356  CALL_METHOD_1         1  ''
              358  STORE_FAST               'to_add'

 L. 159       360  LOAD_FAST                'to_add'
              362  LOAD_CONST               None
              364  <117>                 0  ''
          366_368  POP_JUMP_IF_FALSE   378  'to 378'

 L. 160       370  LOAD_GLOBAL              RuntimeError
              372  LOAD_STR                 'Cannot quote None'
              374  CALL_FUNCTION_1       1  ''
              376  RAISE_VARARGS_1       1  'exception instance'
            378_0  COME_FROM           366  '366'

 L. 161       378  LOAD_FAST                'ret'
              380  LOAD_METHOD              append
              382  LOAD_FAST                'to_add'
              384  CALL_METHOD_1         1  ''
              386  POP_TOP          
              388  JUMP_BACK            60  'to 60'
            390_0  COME_FROM           346  '346'
            390_1  COME_FROM           336  '336'

 L. 162       390  LOAD_FAST                'unquoted'
              392  LOAD_FAST                'self'
              394  LOAD_ATTR                _unsafe
              396  <118>                 0  ''
          398_400  POP_JUMP_IF_FALSE   442  'to 442'

 L. 163       402  LOAD_FAST                'self'
              404  LOAD_METHOD              _quoter
              406  LOAD_FAST                'unquoted'
              408  CALL_METHOD_1         1  ''
              410  STORE_FAST               'to_add'

 L. 164       412  LOAD_FAST                'to_add'
              414  LOAD_CONST               None
              416  <117>                 0  ''
          418_420  POP_JUMP_IF_FALSE   430  'to 430'

 L. 165       422  LOAD_GLOBAL              RuntimeError
              424  LOAD_STR                 'Cannot quote None'
              426  CALL_FUNCTION_1       1  ''
              428  RAISE_VARARGS_1       1  'exception instance'
            430_0  COME_FROM           418  '418'

 L. 166       430  LOAD_FAST                'ret'
              432  LOAD_METHOD              append
              434  LOAD_FAST                'to_add'
              436  CALL_METHOD_1         1  ''
              438  POP_TOP          
              440  JUMP_BACK            60  'to 60'
            442_0  COME_FROM           398  '398'

 L. 168       442  LOAD_FAST                'ret'
              444  LOAD_METHOD              append
              446  LOAD_FAST                'unquoted'
              448  CALL_METHOD_1         1  ''
              450  POP_TOP          

 L. 169       452  JUMP_BACK            60  'to 60'
            454_0  COME_FROM           142  '142'
            454_1  COME_FROM           114  '114'
            454_2  COME_FROM            96  '96'

 L. 171       454  LOAD_FAST                'decoder'
              456  LOAD_ATTR                buffer
          458_460  POP_JUMP_IF_FALSE   514  'to 514'

 L. 172       462  LOAD_FAST                'idx'
              464  LOAD_CONST               1
              466  BINARY_SUBTRACT  
              468  LOAD_GLOBAL              len
              470  LOAD_FAST                'decoder'
              472  LOAD_ATTR                buffer
              474  CALL_FUNCTION_1       1  ''
              476  LOAD_CONST               3
              478  BINARY_MULTIPLY  
              480  BINARY_SUBTRACT  
              482  STORE_FAST               'start_pct'

 L. 173       484  LOAD_FAST                'ret'
              486  LOAD_METHOD              append
              488  LOAD_FAST                'val'
              490  LOAD_FAST                'start_pct'
              492  LOAD_FAST                'idx'
              494  LOAD_CONST               1
              496  BINARY_SUBTRACT  
              498  BUILD_SLICE_2         2 
              500  BINARY_SUBSCR    
              502  CALL_METHOD_1         1  ''
              504  POP_TOP          

 L. 174       506  LOAD_FAST                'decoder'
              508  LOAD_METHOD              reset
              510  CALL_METHOD_0         0  ''
              512  POP_TOP          
            514_0  COME_FROM           458  '458'

 L. 176       514  LOAD_FAST                'ch'
              516  LOAD_STR                 '+'
              518  COMPARE_OP               ==
          520_522  POP_JUMP_IF_FALSE   568  'to 568'

 L. 177       524  LOAD_FAST                'self'
              526  LOAD_ATTR                _qs
          528_530  POP_JUMP_IF_FALSE   544  'to 544'
              532  LOAD_FAST                'ch'
              534  LOAD_FAST                'self'
              536  LOAD_ATTR                _unsafe
              538  <118>                 0  ''
          540_542  POP_JUMP_IF_FALSE   556  'to 556'
            544_0  COME_FROM           528  '528'

 L. 178       544  LOAD_FAST                'ret'
              546  LOAD_METHOD              append
              548  LOAD_STR                 '+'
              550  CALL_METHOD_1         1  ''
              552  POP_TOP          
              554  JUMP_BACK            60  'to 60'
            556_0  COME_FROM           540  '540'

 L. 180       556  LOAD_FAST                'ret'
              558  LOAD_METHOD              append
              560  LOAD_STR                 ' '
              562  CALL_METHOD_1         1  ''
              564  POP_TOP          

 L. 181       566  JUMP_BACK            60  'to 60'
            568_0  COME_FROM           520  '520'

 L. 183       568  LOAD_FAST                'ch'
              570  LOAD_FAST                'self'
              572  LOAD_ATTR                _unsafe
              574  <118>                 0  ''
          576_578  POP_JUMP_IF_FALSE   638  'to 638'

 L. 184       580  LOAD_FAST                'ret'
              582  LOAD_METHOD              append
              584  LOAD_STR                 '%'
              586  CALL_METHOD_1         1  ''
              588  POP_TOP          

 L. 185       590  LOAD_GLOBAL              hex
              592  LOAD_GLOBAL              ord
              594  LOAD_FAST                'ch'
              596  CALL_FUNCTION_1       1  ''
              598  CALL_FUNCTION_1       1  ''
              600  LOAD_METHOD              upper
              602  CALL_METHOD_0         0  ''
              604  LOAD_CONST               2
              606  LOAD_CONST               None
              608  BUILD_SLICE_2         2 
              610  BINARY_SUBSCR    
              612  STORE_FAST               'h'

 L. 186       614  LOAD_FAST                'h'
              616  GET_ITER         
            618_0  COME_FROM           632  '632'
              618  FOR_ITER            636  'to 636'
              620  STORE_FAST               'ch'

 L. 187       622  LOAD_FAST                'ret'
              624  LOAD_METHOD              append
              626  LOAD_FAST                'ch'
              628  CALL_METHOD_1         1  ''
              630  POP_TOP          
          632_634  JUMP_BACK           618  'to 618'
            636_0  COME_FROM           618  '618'

 L. 188       636  JUMP_BACK            60  'to 60'
            638_0  COME_FROM           576  '576'

 L. 190       638  LOAD_FAST                'ret'
              640  LOAD_METHOD              append
              642  LOAD_FAST                'ch'
              644  CALL_METHOD_1         1  ''
              646  POP_TOP          
              648  JUMP_BACK            60  'to 60'
            650_0  COME_FROM            70  '70'

 L. 192       650  LOAD_FAST                'decoder'
              652  LOAD_ATTR                buffer
          654_656  POP_JUMP_IF_FALSE   688  'to 688'

 L. 193       658  LOAD_FAST                'ret'
              660  LOAD_METHOD              append
              662  LOAD_FAST                'val'
              664  LOAD_GLOBAL              len
              666  LOAD_FAST                'decoder'
              668  LOAD_ATTR                buffer
              670  CALL_FUNCTION_1       1  ''
              672  UNARY_NEGATIVE   
              674  LOAD_CONST               3
              676  BINARY_MULTIPLY  
              678  LOAD_CONST               None
              680  BUILD_SLICE_2         2 
              682  BINARY_SUBSCR    
              684  CALL_METHOD_1         1  ''
              686  POP_TOP          
            688_0  COME_FROM           654  '654'

 L. 195       688  LOAD_STR                 ''
              690  LOAD_METHOD              join
              692  LOAD_FAST                'ret'
              694  CALL_METHOD_1         1  ''
              696  STORE_FAST               'ret2'

 L. 196       698  LOAD_FAST                'ret2'
              700  LOAD_FAST                'val'
              702  COMPARE_OP               ==
          704_706  POP_JUMP_IF_FALSE   712  'to 712'

 L. 197       708  LOAD_FAST                'val'
              710  RETURN_VALUE     
            712_0  COME_FROM           704  '704'

 L. 198       712  LOAD_FAST                'ret2'
              714  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1