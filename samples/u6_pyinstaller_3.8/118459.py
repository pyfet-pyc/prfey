# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\yarl\quoting.py
import os, re, sys
from string import ascii_letters, ascii_lowercase, digits
from typing import Optional, TYPE_CHECKING, cast
NO_EXTENSIONS = bool(os.environ.get('YARL_NO_EXTENSIONS'))
if sys.implementation.name != 'cpython':
    NO_EXTENSIONS = True
BASCII_LOWERCASE = ascii_lowercase.encode('ascii')
BPCT_ALLOWED = {'%{:02X}'.format(i).encode('ascii') for i in range(256)}
GEN_DELIMS = ':/?#[]@'
SUB_DELIMS_WITHOUT_QS = "!$'()*,"
SUB_DELIMS = SUB_DELIMS_WITHOUT_QS + '+&=;'
RESERVED = GEN_DELIMS + SUB_DELIMS
UNRESERVED = ascii_letters + digits + '-._~'
ALLOWED = UNRESERVED + SUB_DELIMS_WITHOUT_QS
_IS_HEX = re.compile(b'[A-Z0-9][A-Z0-9]')

class _Quoter:

    def __init__(self, *, safe: str='', protected: str='', qs: bool=False) -> None:
        self._safe = safe
        self._protected = protected
        self._qs = qs

    def __call__--- This code section failed: ---

 L.  36         0  LOAD_FAST                'val'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  37         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  38        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'val'
               16  LOAD_GLOBAL              str
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     30  'to 30'

 L.  39        22  LOAD_GLOBAL              TypeError
               24  LOAD_STR                 'Argument should be str'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L.  40        30  LOAD_FAST                'val'
               32  POP_JUMP_IF_TRUE     38  'to 38'

 L.  41        34  LOAD_STR                 ''
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L.  42        38  LOAD_GLOBAL              cast
               40  LOAD_GLOBAL              str
               42  LOAD_FAST                'val'
               44  CALL_FUNCTION_2       2  ''
               46  LOAD_ATTR                encode
               48  LOAD_STR                 'utf8'
               50  LOAD_STR                 'ignore'
               52  LOAD_CONST               ('errors',)
               54  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               56  STORE_FAST               'bval'

 L.  43        58  LOAD_GLOBAL              bytearray
               60  CALL_FUNCTION_0       0  ''
               62  STORE_FAST               'ret'

 L.  44        64  LOAD_GLOBAL              bytearray
               66  CALL_FUNCTION_0       0  ''
               68  STORE_FAST               'pct'

 L.  45        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _safe
               74  STORE_FAST               'safe'

 L.  46        76  LOAD_FAST                'safe'
               78  LOAD_GLOBAL              ALLOWED
               80  INPLACE_ADD      
               82  STORE_FAST               'safe'

 L.  47        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _qs
               88  POP_JUMP_IF_TRUE     98  'to 98'

 L.  48        90  LOAD_FAST                'safe'
               92  LOAD_STR                 '+&=;'
               94  INPLACE_ADD      
               96  STORE_FAST               'safe'
             98_0  COME_FROM            88  '88'

 L.  49        98  LOAD_FAST                'safe'
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                _protected
              104  INPLACE_ADD      
              106  STORE_FAST               'safe'

 L.  50       108  LOAD_FAST                'safe'
              110  LOAD_METHOD              encode
              112  LOAD_STR                 'ascii'
              114  CALL_METHOD_1         1  ''
              116  STORE_FAST               'bsafe'

 L.  51       118  LOAD_CONST               0
              120  STORE_FAST               'idx'
            122_0  COME_FROM           502  '502'
            122_1  COME_FROM           428  '428'
            122_2  COME_FROM           416  '416'

 L.  52       122  LOAD_FAST                'idx'
              124  LOAD_GLOBAL              len
              126  LOAD_FAST                'bval'
              128  CALL_FUNCTION_1       1  ''
              130  COMPARE_OP               <
          132_134  POP_JUMP_IF_FALSE   600  'to 600'

 L.  53       136  LOAD_FAST                'bval'
              138  LOAD_FAST                'idx'
              140  BINARY_SUBSCR    
              142  STORE_FAST               'ch'

 L.  54       144  LOAD_FAST                'idx'
              146  LOAD_CONST               1
              148  INPLACE_ADD      
              150  STORE_FAST               'idx'

 L.  56       152  LOAD_FAST                'pct'
          154_156  POP_JUMP_IF_FALSE   460  'to 460'

 L.  57       158  LOAD_FAST                'ch'
              160  LOAD_GLOBAL              BASCII_LOWERCASE
              162  COMPARE_OP               in
              164  POP_JUMP_IF_FALSE   174  'to 174'

 L.  58       166  LOAD_FAST                'ch'
              168  LOAD_CONST               32
              170  BINARY_SUBTRACT  
              172  STORE_FAST               'ch'
            174_0  COME_FROM           164  '164'

 L.  59       174  LOAD_FAST                'pct'
              176  LOAD_METHOD              append
              178  LOAD_FAST                'ch'
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L.  60       184  LOAD_GLOBAL              len
              186  LOAD_FAST                'pct'
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_CONST               3
              192  COMPARE_OP               ==
          194_196  POP_JUMP_IF_FALSE   406  'to 406'

 L.  61       198  LOAD_FAST                'pct'
              200  LOAD_CONST               1
              202  LOAD_CONST               None
              204  BUILD_SLICE_2         2 
              206  BINARY_SUBSCR    
              208  STORE_FAST               'buf'

 L.  62       210  LOAD_GLOBAL              _IS_HEX
              212  LOAD_METHOD              match
              214  LOAD_FAST                'buf'
              216  CALL_METHOD_1         1  ''
              218  POP_JUMP_IF_TRUE    248  'to 248'

 L.  63       220  LOAD_FAST                'ret'
              222  LOAD_METHOD              extend
              224  LOAD_CONST               b'%25'
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L.  64       230  LOAD_FAST                'pct'
              232  LOAD_METHOD              clear
              234  CALL_METHOD_0         0  ''
              236  POP_TOP          

 L.  65       238  LOAD_FAST                'idx'
              240  LOAD_CONST               2
              242  INPLACE_SUBTRACT 
              244  STORE_FAST               'idx'

 L.  66       246  JUMP_BACK           122  'to 122'
            248_0  COME_FROM           218  '218'

 L.  67       248  SETUP_FINALLY       284  'to 284'

 L.  68       250  LOAD_GLOBAL              chr
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
              282  JUMP_FORWARD        336  'to 336'
            284_0  COME_FROM_FINALLY   248  '248'

 L.  69       284  DUP_TOP          
              286  LOAD_GLOBAL              ValueError
              288  COMPARE_OP               exception-match
          290_292  POP_JUMP_IF_FALSE   334  'to 334'
              294  POP_TOP          
              296  POP_TOP          
              298  POP_TOP          

 L.  70       300  LOAD_FAST                'ret'
              302  LOAD_METHOD              extend
              304  LOAD_CONST               b'%25'
              306  CALL_METHOD_1         1  ''
              308  POP_TOP          

 L.  71       310  LOAD_FAST                'pct'
              312  LOAD_METHOD              clear
              314  CALL_METHOD_0         0  ''
              316  POP_TOP          

 L.  72       318  LOAD_FAST                'idx'
              320  LOAD_CONST               2
              322  INPLACE_SUBTRACT 
              324  STORE_FAST               'idx'

 L.  73       326  POP_EXCEPT       
              328  JUMP_BACK           122  'to 122'
              330  POP_EXCEPT       
              332  JUMP_FORWARD        336  'to 336'
            334_0  COME_FROM           290  '290'
              334  END_FINALLY      
            336_0  COME_FROM           332  '332'
            336_1  COME_FROM           282  '282'

 L.  75       336  LOAD_FAST                'unquoted'
              338  LOAD_FAST                'self'
              340  LOAD_ATTR                _protected
              342  COMPARE_OP               in
          344_346  POP_JUMP_IF_FALSE   360  'to 360'

 L.  76       348  LOAD_FAST                'ret'
              350  LOAD_METHOD              extend
              352  LOAD_FAST                'pct'
              354  CALL_METHOD_1         1  ''
              356  POP_TOP          
              358  JUMP_FORWARD        396  'to 396'
            360_0  COME_FROM           344  '344'

 L.  77       360  LOAD_FAST                'unquoted'
              362  LOAD_FAST                'safe'
              364  COMPARE_OP               in
          366_368  POP_JUMP_IF_FALSE   386  'to 386'

 L.  78       370  LOAD_FAST                'ret'
              372  LOAD_METHOD              append
              374  LOAD_GLOBAL              ord
              376  LOAD_FAST                'unquoted'
              378  CALL_FUNCTION_1       1  ''
              380  CALL_METHOD_1         1  ''
              382  POP_TOP          
              384  JUMP_FORWARD        396  'to 396'
            386_0  COME_FROM           366  '366'

 L.  80       386  LOAD_FAST                'ret'
              388  LOAD_METHOD              extend
              390  LOAD_FAST                'pct'
              392  CALL_METHOD_1         1  ''
              394  POP_TOP          
            396_0  COME_FROM           384  '384'
            396_1  COME_FROM           358  '358'

 L.  81       396  LOAD_FAST                'pct'
              398  LOAD_METHOD              clear
              400  CALL_METHOD_0         0  ''
              402  POP_TOP          
              404  JUMP_BACK           122  'to 122'
            406_0  COME_FROM           194  '194'

 L.  84       406  LOAD_GLOBAL              len
              408  LOAD_FAST                'pct'
              410  CALL_FUNCTION_1       1  ''
              412  LOAD_CONST               2
              414  COMPARE_OP               ==
              416  POP_JUMP_IF_FALSE   122  'to 122'
              418  LOAD_FAST                'idx'
              420  LOAD_GLOBAL              len
              422  LOAD_FAST                'bval'
              424  CALL_FUNCTION_1       1  ''
              426  COMPARE_OP               ==
              428  POP_JUMP_IF_FALSE   122  'to 122'

 L.  85       430  LOAD_FAST                'ret'
              432  LOAD_METHOD              extend
              434  LOAD_CONST               b'%25'
              436  CALL_METHOD_1         1  ''
              438  POP_TOP          

 L.  86       440  LOAD_FAST                'pct'
              442  LOAD_METHOD              clear
              444  CALL_METHOD_0         0  ''
              446  POP_TOP          

 L.  87       448  LOAD_FAST                'idx'
              450  LOAD_CONST               1
              452  INPLACE_SUBTRACT 
              454  STORE_FAST               'idx'

 L.  89       456  JUMP_BACK           122  'to 122'
              458  JUMP_FORWARD        516  'to 516'
            460_0  COME_FROM           154  '154'

 L.  91       460  LOAD_FAST                'ch'
              462  LOAD_GLOBAL              ord
              464  LOAD_STR                 '%'
              466  CALL_FUNCTION_1       1  ''
              468  COMPARE_OP               ==
          470_472  POP_JUMP_IF_FALSE   516  'to 516'

 L.  92       474  LOAD_FAST                'pct'
              476  LOAD_METHOD              clear
              478  CALL_METHOD_0         0  ''
              480  POP_TOP          

 L.  93       482  LOAD_FAST                'pct'
              484  LOAD_METHOD              append
              486  LOAD_FAST                'ch'
              488  CALL_METHOD_1         1  ''
              490  POP_TOP          

 L.  96       492  LOAD_FAST                'idx'
              494  LOAD_GLOBAL              len
              496  LOAD_FAST                'bval'
              498  CALL_FUNCTION_1       1  ''
              500  COMPARE_OP               ==
              502  POP_JUMP_IF_FALSE   122  'to 122'

 L.  97       504  LOAD_FAST                'ret'
              506  LOAD_METHOD              extend
              508  LOAD_CONST               b'%25'
              510  CALL_METHOD_1         1  ''
              512  POP_TOP          

 L.  99       514  JUMP_BACK           122  'to 122'
            516_0  COME_FROM           470  '470'
            516_1  COME_FROM           458  '458'

 L. 101       516  LOAD_FAST                'self'
              518  LOAD_ATTR                _qs
          520_522  POP_JUMP_IF_FALSE   554  'to 554'

 L. 102       524  LOAD_FAST                'ch'
              526  LOAD_GLOBAL              ord
              528  LOAD_STR                 ' '
              530  CALL_FUNCTION_1       1  ''
              532  COMPARE_OP               ==
          534_536  POP_JUMP_IF_FALSE   554  'to 554'

 L. 103       538  LOAD_FAST                'ret'
              540  LOAD_METHOD              append
              542  LOAD_GLOBAL              ord
              544  LOAD_STR                 '+'
              546  CALL_FUNCTION_1       1  ''
              548  CALL_METHOD_1         1  ''
              550  POP_TOP          

 L. 104       552  JUMP_BACK           122  'to 122'
            554_0  COME_FROM           534  '534'
            554_1  COME_FROM           520  '520'

 L. 105       554  LOAD_FAST                'ch'
              556  LOAD_FAST                'bsafe'
              558  COMPARE_OP               in
          560_562  POP_JUMP_IF_FALSE   576  'to 576'

 L. 106       564  LOAD_FAST                'ret'
              566  LOAD_METHOD              append
              568  LOAD_FAST                'ch'
              570  CALL_METHOD_1         1  ''
              572  POP_TOP          

 L. 107       574  JUMP_BACK           122  'to 122'
            576_0  COME_FROM           560  '560'

 L. 109       576  LOAD_FAST                'ret'
              578  LOAD_METHOD              extend
              580  LOAD_STR                 '%{:02X}'
              582  LOAD_METHOD              format
              584  LOAD_FAST                'ch'
              586  CALL_METHOD_1         1  ''
              588  LOAD_METHOD              encode
              590  LOAD_STR                 'ascii'
              592  CALL_METHOD_1         1  ''
              594  CALL_METHOD_1         1  ''
              596  POP_TOP          
              598  JUMP_BACK           122  'to 122'
            600_0  COME_FROM           132  '132'

 L. 111       600  LOAD_FAST                'ret'
              602  LOAD_METHOD              decode
              604  LOAD_STR                 'ascii'
              606  CALL_METHOD_1         1  ''
              608  STORE_FAST               'ret2'

 L. 112       610  LOAD_FAST                'ret2'
              612  LOAD_FAST                'val'
              614  COMPARE_OP               ==
          616_618  POP_JUMP_IF_FALSE   624  'to 624'

 L. 113       620  LOAD_FAST                'val'
              622  RETURN_VALUE     
            624_0  COME_FROM           616  '616'

 L. 114       624  LOAD_FAST                'ret2'
              626  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 330


class _Unquoter:

    def __init__(self, *, unsafe: str='', qs: bool=False) -> None:
        self._unsafe = unsafe
        self._qs = qs
        self._quoter = _Quoter
        self._qs_quoter = _Quoter(qs=True)

    def __call__(self, val: Optional[str]) -> Optional[str]:
        if val is None:
            return
        else:
            if not isinstance(val, str):
                raise TypeError('Argument should be str')
            return val or ''
        pct = ''
        last_pct = ''
        pcts = bytearray
        ret = []
        for ch in val:
            if pct:
                pct += ch
                if len(pct) == 3:
                    pcts.append(int((pct[1:]), base=16))
                    last_pct = pct
                    pct = ''
                elif pcts:
                    try:
                        unquoted = pcts.decode('utf8')
                    except UnicodeDecodeError:
                        pass
                    else:
                        if self._qs and unquoted in '+=&;':
                            to_add = self._qs_quoter(unquoted)
                            if to_add is None:
                                raise RuntimeError('Cannot quote None')
                            ret.append(to_add)
                        else:
                            if unquoted in self._unsafe:
                                to_add = self._quoter(unquoted)
                                if to_add is None:
                                    raise RuntimeError('Cannot quote None')
                                ret.append(to_add)
                            else:
                                ret.append(unquoted)
                        del pcts[:]
                    if ch == '%':
                        pct = ch
                else:
                    if pcts:
                        ret.append(last_pct)
                        last_pct = ''
                    if ch == '+':
                        if not self._qs or ch in self._unsafe:
                            ret.append('+')
                        else:
                            ret.append(' ')
                    elif ch in self._unsafe:
                        ret.append('%')
                        h = hex(ord(ch)).upper[2:]
                        for ch in h:
                            ret.append(ch)

                    else:
                        ret.append(ch)
            if pcts:
                try:
                    unquoted = pcts.decode('utf8')
                except UnicodeDecodeError:
                    ret.append(last_pct)
                else:
                    if self._qs and unquoted in '+=&;':
                        to_add = self._qs_quoter(unquoted)
                        if to_add is None:
                            raise RuntimeError('Cannot quote None')
                        ret.append(to_add)
                    else:
                        if unquoted in self._unsafe:
                            to_add = self._qs_quoter(unquoted)
                            if to_add is None:
                                raise RuntimeError('Cannot quote None')
                            ret.append(to_add)
                        else:
                            ret.append(unquoted)
            ret2 = ''.join(ret)
            if ret2 == val:
                return val
            return ret2


_PyQuoter = _Quoter
_PyUnquoter = _Unquoter
if not TYPE_CHECKING:
    if not NO_EXTENSIONS:
        try:
            from ._quoting import _Quoter, _Unquoter
        except ImportError:
            _Quoter = _PyQuoter
            _Unquoter = _PyUnquoter