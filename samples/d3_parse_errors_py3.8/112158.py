# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: shlex.py
"""A lexical analyzer class for simple shell-like syntaxes."""
import os, re, sys
from collections import deque
from io import StringIO
__all__ = [
 'shlex', 'split', 'quote', 'join']

class shlex:
    __doc__ = 'A lexical analyzer class for simple shell-like syntaxes.'

    def __init__(self, instream=None, infile=None, posix=False, punctuation_chars=False):
        if isinstance(instream, str):
            instream = StringIO(instream)
        if instream is not None:
            self.instream = instream
            self.infile = infile
        else:
            self.instream = sys.stdin
            self.infile = None
        self.posix = posix
        if posix:
            self.eof = None
        else:
            self.eof = ''
        self.commenters = '#'
        self.wordchars = 'abcdfeghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
        if self.posix:
            self.wordchars += 'ßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ'
        self.whitespace = ' \t\r\n'
        self.whitespace_split = False
        self.quotes = '\'"'
        self.escape = '\\'
        self.escapedquotes = '"'
        self.state = ' '
        self.pushback = deque()
        self.lineno = 1
        self.debug = 0
        self.token = ''
        self.filestack = deque()
        self.source = None
        if not punctuation_chars:
            punctuation_chars = ''
        elif punctuation_chars is True:
            punctuation_chars = '();<>|&'
        self._punctuation_chars = punctuation_chars
        if punctuation_chars:
            self._pushback_chars = deque()
            self.wordchars += '~-./*?='
            t = self.wordchars.maketrans(dict.fromkeys(punctuation_chars))
            self.wordchars = self.wordchars.translate(t)

    @property
    def punctuation_chars(self):
        return self._punctuation_chars

    def push_token(self, tok):
        """Push a token onto the stack popped by the get_token method"""
        if self.debug >= 1:
            print('shlex: pushing token ' + repr(tok))
        self.pushback.appendleft(tok)

    def push_source(self, newstream, newfile=None):
        """Push an input source onto the lexer's input source stack."""
        if isinstance(newstream, str):
            newstream = StringIO(newstream)
        self.filestack.appendleft((self.infile, self.instream, self.lineno))
        self.infile = newfile
        self.instream = newstream
        self.lineno = 1
        if self.debug:
            if newfile is not None:
                print('shlex: pushing to file %s' % (self.infile,))
            else:
                print('shlex: pushing to stream %s' % (self.instream,))

    def pop_source(self):
        """Pop the input source stack."""
        self.instream.close()
        self.infile, self.instream, self.lineno = self.filestack.popleft()
        if self.debug:
            print('shlex: popping to %s, line %d' % (
             self.instream, self.lineno))
        self.state = ' '

    def get_token(self):
        """Get a token from the input stream (or from stack if it's nonempty)"""
        if self.pushback:
            tok = self.pushback.popleft()
            if self.debug >= 1:
                print('shlex: popping token ' + repr(tok))
            return tok
        raw = self.read_token()
        if self.source is not None:
            while True:
                if raw == self.source:
                    spec = self.sourcehook(self.read_token())
                    if spec:
                        newfile, newstream = spec
                        self.push_source(newstream, newfile)
                    raw = self.get_token()

            while True:
                if raw == self.eof:
                    if not self.filestack:
                        return self.eof
                    self.pop_source()
                    raw = self.get_token()

            if self.debug >= 1:
                if raw != self.eof:
                    print('shlex: token=' + repr(raw))
                else:
                    print('shlex: token=EOF')
            return raw

    def read_token--- This code section failed: ---

 L. 134         0  LOAD_CONST               False
                2  STORE_FAST               'quoted'

 L. 135         4  LOAD_STR                 ' '
                6  STORE_FAST               'escapedstate'
              8_0  COME_FROM          1154  '1154'
              8_1  COME_FROM          1152  '1152'
              8_2  COME_FROM          1150  '1150'
              8_3  COME_FROM          1144  '1144'
              8_4  COME_FROM          1140  '1140'
              8_5  COME_FROM          1066  '1066'
              8_6  COME_FROM          1006  '1006'
              8_7  COME_FROM           974  '974'
              8_8  COME_FROM           946  '946'
              8_9  COME_FROM           870  '870'
             8_10  COME_FROM           868  '868'
             8_11  COME_FROM           860  '860'
             8_12  COME_FROM           856  '856'
             8_13  COME_FROM           792  '792'
             8_14  COME_FROM           790  '790'
             8_15  COME_FROM           782  '782'
             8_16  COME_FROM           778  '778'
             8_17  COME_FROM           726  '726'
             8_18  COME_FROM           708  '708'
             8_19  COME_FROM           698  '698'
             8_20  COME_FROM           578  '578'
             8_21  COME_FROM           408  '408'
             8_22  COME_FROM           406  '406'
             8_23  COME_FROM           398  '398'
             8_24  COME_FROM           394  '394'
             8_25  COME_FROM           196  '196'
             8_26  COME_FROM           188  '188'
             8_27  COME_FROM           184  '184'
             8_28  COME_FROM           114  '114'

 L. 137         8  LOAD_FAST                'self'
               10  LOAD_ATTR                punctuation_chars
               12  POP_JUMP_IF_FALSE    32  'to 32'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _pushback_chars
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L. 138        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _pushback_chars
               24  LOAD_METHOD              pop
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'nextchar'
               30  JUMP_FORWARD         44  'to 44'
             32_0  COME_FROM            18  '18'
             32_1  COME_FROM            12  '12'

 L. 140        32  LOAD_FAST                'self'
               34  LOAD_ATTR                instream
               36  LOAD_METHOD              read
               38  LOAD_CONST               1
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'nextchar'
             44_0  COME_FROM            30  '30'

 L. 141        44  LOAD_FAST                'nextchar'
               46  LOAD_STR                 '\n'
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    66  'to 66'

 L. 142        52  LOAD_FAST                'self'
               54  DUP_TOP          
               56  LOAD_ATTR                lineno
               58  LOAD_CONST               1
               60  INPLACE_ADD      
               62  ROT_TWO          
               64  STORE_ATTR               lineno
             66_0  COME_FROM            50  '50'

 L. 143        66  LOAD_FAST                'self'
               68  LOAD_ATTR                debug
               70  LOAD_CONST               3
               72  COMPARE_OP               >=
               74  POP_JUMP_IF_FALSE    94  'to 94'

 L. 144        76  LOAD_GLOBAL              print
               78  LOAD_STR                 'shlex: in state %r I see character: %r'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                state

 L. 145        84  LOAD_FAST                'nextchar'

 L. 144        86  BUILD_TUPLE_2         2 
               88  BINARY_MODULO    
               90  CALL_FUNCTION_1       1  ''
               92  POP_TOP          
             94_0  COME_FROM            74  '74'

 L. 146        94  LOAD_FAST                'self'
               96  LOAD_ATTR                state
               98  LOAD_CONST               None
              100  COMPARE_OP               is
              102  POP_JUMP_IF_FALSE   116  'to 116'

 L. 147       104  LOAD_STR                 ''
              106  LOAD_FAST                'self'
              108  STORE_ATTR               token

 L. 148   110_112  JUMP_FORWARD       1156  'to 1156'
              114  JUMP_BACK             8  'to 8'
            116_0  COME_FROM           102  '102'

 L. 149       116  LOAD_FAST                'self'
              118  LOAD_ATTR                state
              120  LOAD_STR                 ' '
              122  COMPARE_OP               ==
          124_126  POP_JUMP_IF_FALSE   410  'to 410'

 L. 150       128  LOAD_FAST                'nextchar'
              130  POP_JUMP_IF_TRUE    146  'to 146'

 L. 151       132  LOAD_CONST               None
              134  LOAD_FAST                'self'
              136  STORE_ATTR               state

 L. 152   138_140  JUMP_FORWARD       1156  'to 1156'
          142_144  BREAK_LOOP         1154  'to 1154'
            146_0  COME_FROM           130  '130'

 L. 153       146  LOAD_FAST                'nextchar'
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                whitespace
              152  COMPARE_OP               in
              154  POP_JUMP_IF_FALSE   200  'to 200'

 L. 154       156  LOAD_FAST                'self'
              158  LOAD_ATTR                debug
              160  LOAD_CONST               2
              162  COMPARE_OP               >=
              164  POP_JUMP_IF_FALSE   174  'to 174'

 L. 155       166  LOAD_GLOBAL              print
              168  LOAD_STR                 'shlex: I see whitespace in whitespace state'
              170  CALL_FUNCTION_1       1  ''
              172  POP_TOP          
            174_0  COME_FROM           164  '164'

 L. 156       174  LOAD_FAST                'self'
              176  LOAD_ATTR                token
              178  POP_JUMP_IF_TRUE    190  'to 190'
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                posix
              184  POP_JUMP_IF_FALSE_BACK     8  'to 8'
              186  LOAD_FAST                'quoted'
              188  POP_JUMP_IF_FALSE_BACK     8  'to 8'
            190_0  COME_FROM           178  '178'

 L. 157   190_192  JUMP_FORWARD       1156  'to 1156'
              194  BREAK_LOOP          198  'to 198'

 L. 159       196  JUMP_BACK             8  'to 8'
            198_0  COME_FROM           194  '194'
              198  BREAK_LOOP          408  'to 408'
            200_0  COME_FROM           154  '154'

 L. 160       200  LOAD_FAST                'nextchar'
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                commenters
              206  COMPARE_OP               in
              208  POP_JUMP_IF_FALSE   236  'to 236'

 L. 161       210  LOAD_FAST                'self'
              212  LOAD_ATTR                instream
              214  LOAD_METHOD              readline
              216  CALL_METHOD_0         0  ''
              218  POP_TOP          

 L. 162       220  LOAD_FAST                'self'
              222  DUP_TOP          
              224  LOAD_ATTR                lineno
              226  LOAD_CONST               1
              228  INPLACE_ADD      
              230  ROT_TWO          
              232  STORE_ATTR               lineno
              234  JUMP_FORWARD        408  'to 408'
            236_0  COME_FROM           208  '208'

 L. 163       236  LOAD_FAST                'self'
              238  LOAD_ATTR                posix
          240_242  POP_JUMP_IF_FALSE   268  'to 268'
              244  LOAD_FAST                'nextchar'
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                escape
              250  COMPARE_OP               in
          252_254  POP_JUMP_IF_FALSE   268  'to 268'

 L. 164       256  LOAD_STR                 'a'
              258  STORE_FAST               'escapedstate'

 L. 165       260  LOAD_FAST                'nextchar'
              262  LOAD_FAST                'self'
              264  STORE_ATTR               state
              266  JUMP_FORWARD        408  'to 408'
            268_0  COME_FROM           252  '252'
            268_1  COME_FROM           240  '240'

 L. 166       268  LOAD_FAST                'nextchar'
              270  LOAD_FAST                'self'
              272  LOAD_ATTR                wordchars
              274  COMPARE_OP               in
          276_278  POP_JUMP_IF_FALSE   294  'to 294'

 L. 167       280  LOAD_FAST                'nextchar'
              282  LOAD_FAST                'self'
              284  STORE_ATTR               token

 L. 168       286  LOAD_STR                 'a'
              288  LOAD_FAST                'self'
              290  STORE_ATTR               state
              292  JUMP_FORWARD        408  'to 408'
            294_0  COME_FROM           276  '276'

 L. 169       294  LOAD_FAST                'nextchar'
              296  LOAD_FAST                'self'
              298  LOAD_ATTR                punctuation_chars
              300  COMPARE_OP               in
          302_304  POP_JUMP_IF_FALSE   320  'to 320'

 L. 170       306  LOAD_FAST                'nextchar'
              308  LOAD_FAST                'self'
              310  STORE_ATTR               token

 L. 171       312  LOAD_STR                 'c'
              314  LOAD_FAST                'self'
              316  STORE_ATTR               state
              318  JUMP_FORWARD        408  'to 408'
            320_0  COME_FROM           302  '302'

 L. 172       320  LOAD_FAST                'nextchar'
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                quotes
              326  COMPARE_OP               in
          328_330  POP_JUMP_IF_FALSE   354  'to 354'

 L. 173       332  LOAD_FAST                'self'
              334  LOAD_ATTR                posix
          336_338  POP_JUMP_IF_TRUE    346  'to 346'

 L. 174       340  LOAD_FAST                'nextchar'
              342  LOAD_FAST                'self'
              344  STORE_ATTR               token
            346_0  COME_FROM           336  '336'

 L. 175       346  LOAD_FAST                'nextchar'
              348  LOAD_FAST                'self'
              350  STORE_ATTR               state
              352  JUMP_FORWARD        408  'to 408'
            354_0  COME_FROM           328  '328'

 L. 176       354  LOAD_FAST                'self'
              356  LOAD_ATTR                whitespace_split
          358_360  POP_JUMP_IF_FALSE   376  'to 376'

 L. 177       362  LOAD_FAST                'nextchar'
              364  LOAD_FAST                'self'
              366  STORE_ATTR               token

 L. 178       368  LOAD_STR                 'a'
              370  LOAD_FAST                'self'
              372  STORE_ATTR               state
              374  JUMP_FORWARD        408  'to 408'
            376_0  COME_FROM           358  '358'

 L. 180       376  LOAD_FAST                'nextchar'
              378  LOAD_FAST                'self'
              380  STORE_ATTR               token

 L. 181       382  LOAD_FAST                'self'
              384  LOAD_ATTR                token
          386_388  POP_JUMP_IF_TRUE   1156  'to 1156'
              390  LOAD_FAST                'self'
              392  LOAD_ATTR                posix
              394  POP_JUMP_IF_FALSE_BACK     8  'to 8'
              396  LOAD_FAST                'quoted'
              398  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L. 182   400_402  JUMP_FORWARD       1156  'to 1156'
              404  BREAK_LOOP          408  'to 408'

 L. 184       406  JUMP_BACK             8  'to 8'
            408_0  COME_FROM           404  '404'
            408_1  COME_FROM           374  '374'
            408_2  COME_FROM           352  '352'
            408_3  COME_FROM           318  '318'
            408_4  COME_FROM           292  '292'
            408_5  COME_FROM           266  '266'
            408_6  COME_FROM           234  '234'
            408_7  COME_FROM           198  '198'
              408  JUMP_BACK             8  'to 8'
            410_0  COME_FROM           124  '124'

 L. 185       410  LOAD_FAST                'self'
              412  LOAD_ATTR                state
              414  LOAD_FAST                'self'
              416  LOAD_ATTR                quotes
              418  COMPARE_OP               in
          420_422  POP_JUMP_IF_FALSE   580  'to 580'

 L. 186       424  LOAD_CONST               True
              426  STORE_FAST               'quoted'

 L. 187       428  LOAD_FAST                'nextchar'
          430_432  POP_JUMP_IF_TRUE    462  'to 462'

 L. 188       434  LOAD_FAST                'self'
              436  LOAD_ATTR                debug
              438  LOAD_CONST               2
              440  COMPARE_OP               >=
          442_444  POP_JUMP_IF_FALSE   454  'to 454'

 L. 189       446  LOAD_GLOBAL              print
              448  LOAD_STR                 'shlex: I see EOF in quotes state'
              450  CALL_FUNCTION_1       1  ''
              452  POP_TOP          
            454_0  COME_FROM           442  '442'

 L. 191       454  LOAD_GLOBAL              ValueError
              456  LOAD_STR                 'No closing quotation'
              458  CALL_FUNCTION_1       1  ''
              460  RAISE_VARARGS_1       1  'exception instance'
            462_0  COME_FROM           430  '430'

 L. 192       462  LOAD_FAST                'nextchar'
              464  LOAD_FAST                'self'
              466  LOAD_ATTR                state
              468  COMPARE_OP               ==
          470_472  POP_JUMP_IF_FALSE   516  'to 516'

 L. 193       474  LOAD_FAST                'self'
              476  LOAD_ATTR                posix
          478_480  POP_JUMP_IF_TRUE    508  'to 508'

 L. 194       482  LOAD_FAST                'self'
              484  DUP_TOP          
              486  LOAD_ATTR                token
              488  LOAD_FAST                'nextchar'
              490  INPLACE_ADD      
              492  ROT_TWO          
              494  STORE_ATTR               token

 L. 195       496  LOAD_STR                 ' '
              498  LOAD_FAST                'self'
              500  STORE_ATTR               state

 L. 196   502_504  JUMP_FORWARD       1156  'to 1156'
              506  BREAK_LOOP          514  'to 514'
            508_0  COME_FROM           478  '478'

 L. 198       508  LOAD_STR                 'a'
              510  LOAD_FAST                'self'
              512  STORE_ATTR               state
            514_0  COME_FROM           506  '506'
              514  JUMP_FORWARD        578  'to 578'
            516_0  COME_FROM           470  '470'

 L. 199       516  LOAD_FAST                'self'
              518  LOAD_ATTR                posix
          520_522  POP_JUMP_IF_FALSE   564  'to 564'
              524  LOAD_FAST                'nextchar'
              526  LOAD_FAST                'self'
              528  LOAD_ATTR                escape
              530  COMPARE_OP               in
          532_534  POP_JUMP_IF_FALSE   564  'to 564'
              536  LOAD_FAST                'self'
              538  LOAD_ATTR                state

 L. 200       540  LOAD_FAST                'self'
              542  LOAD_ATTR                escapedquotes

 L. 199       544  COMPARE_OP               in
          546_548  POP_JUMP_IF_FALSE   564  'to 564'

 L. 201       550  LOAD_FAST                'self'
              552  LOAD_ATTR                state
              554  STORE_FAST               'escapedstate'

 L. 202       556  LOAD_FAST                'nextchar'
              558  LOAD_FAST                'self'
              560  STORE_ATTR               state
              562  JUMP_FORWARD        578  'to 578'
            564_0  COME_FROM           546  '546'
            564_1  COME_FROM           532  '532'
            564_2  COME_FROM           520  '520'

 L. 204       564  LOAD_FAST                'self'
              566  DUP_TOP          
              568  LOAD_ATTR                token
              570  LOAD_FAST                'nextchar'
              572  INPLACE_ADD      
              574  ROT_TWO          
              576  STORE_ATTR               token
            578_0  COME_FROM           562  '562'
            578_1  COME_FROM           514  '514'
              578  JUMP_BACK             8  'to 8'
            580_0  COME_FROM           420  '420'

 L. 205       580  LOAD_FAST                'self'
              582  LOAD_ATTR                state
              584  LOAD_FAST                'self'
              586  LOAD_ATTR                escape
              588  COMPARE_OP               in
          590_592  POP_JUMP_IF_FALSE   700  'to 700'

 L. 206       594  LOAD_FAST                'nextchar'
          596_598  POP_JUMP_IF_TRUE    628  'to 628'

 L. 207       600  LOAD_FAST                'self'
              602  LOAD_ATTR                debug
              604  LOAD_CONST               2
              606  COMPARE_OP               >=
          608_610  POP_JUMP_IF_FALSE   620  'to 620'

 L. 208       612  LOAD_GLOBAL              print
              614  LOAD_STR                 'shlex: I see EOF in escape state'
              616  CALL_FUNCTION_1       1  ''
              618  POP_TOP          
            620_0  COME_FROM           608  '608'

 L. 210       620  LOAD_GLOBAL              ValueError
              622  LOAD_STR                 'No escaped character'
              624  CALL_FUNCTION_1       1  ''
              626  RAISE_VARARGS_1       1  'exception instance'
            628_0  COME_FROM           596  '596'

 L. 213       628  LOAD_FAST                'escapedstate'
              630  LOAD_FAST                'self'
              632  LOAD_ATTR                quotes
              634  COMPARE_OP               in
          636_638  POP_JUMP_IF_FALSE   678  'to 678'

 L. 214       640  LOAD_FAST                'nextchar'
              642  LOAD_FAST                'self'
              644  LOAD_ATTR                state
              646  COMPARE_OP               !=

 L. 213   648_650  POP_JUMP_IF_FALSE   678  'to 678'

 L. 214       652  LOAD_FAST                'nextchar'
              654  LOAD_FAST                'escapedstate'
              656  COMPARE_OP               !=

 L. 213   658_660  POP_JUMP_IF_FALSE   678  'to 678'

 L. 215       662  LOAD_FAST                'self'
              664  DUP_TOP          
              666  LOAD_ATTR                token
              668  LOAD_FAST                'self'
              670  LOAD_ATTR                state
              672  INPLACE_ADD      
              674  ROT_TWO          
              676  STORE_ATTR               token
            678_0  COME_FROM           658  '658'
            678_1  COME_FROM           648  '648'
            678_2  COME_FROM           636  '636'

 L. 216       678  LOAD_FAST                'self'
              680  DUP_TOP          
              682  LOAD_ATTR                token
              684  LOAD_FAST                'nextchar'
              686  INPLACE_ADD      
              688  ROT_TWO          
              690  STORE_ATTR               token

 L. 217       692  LOAD_FAST                'escapedstate'
              694  LOAD_FAST                'self'
              696  STORE_ATTR               state
              698  JUMP_BACK             8  'to 8'
            700_0  COME_FROM           590  '590'

 L. 218       700  LOAD_FAST                'self'
              702  LOAD_ATTR                state
              704  LOAD_CONST               ('a', 'c')
              706  COMPARE_OP               in
              708  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L. 219       710  LOAD_FAST                'nextchar'
          712_714  POP_JUMP_IF_TRUE    728  'to 728'

 L. 220       716  LOAD_CONST               None
              718  LOAD_FAST                'self'
              720  STORE_ATTR               state

 L. 221   722_724  JUMP_FORWARD       1156  'to 1156'
              726  JUMP_BACK             8  'to 8'
            728_0  COME_FROM           712  '712'

 L. 222       728  LOAD_FAST                'nextchar'
              730  LOAD_FAST                'self'
              732  LOAD_ATTR                whitespace
              734  COMPARE_OP               in
          736_738  POP_JUMP_IF_FALSE   794  'to 794'

 L. 223       740  LOAD_FAST                'self'
              742  LOAD_ATTR                debug
              744  LOAD_CONST               2
              746  COMPARE_OP               >=
          748_750  POP_JUMP_IF_FALSE   760  'to 760'

 L. 224       752  LOAD_GLOBAL              print
              754  LOAD_STR                 'shlex: I see whitespace in word state'
              756  CALL_FUNCTION_1       1  ''
              758  POP_TOP          
            760_0  COME_FROM           748  '748'

 L. 225       760  LOAD_STR                 ' '
              762  LOAD_FAST                'self'
              764  STORE_ATTR               state

 L. 226       766  LOAD_FAST                'self'
              768  LOAD_ATTR                token
          770_772  POP_JUMP_IF_TRUE   1156  'to 1156'
              774  LOAD_FAST                'self'
              776  LOAD_ATTR                posix
              778  POP_JUMP_IF_FALSE_BACK     8  'to 8'
              780  LOAD_FAST                'quoted'
              782  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L. 227   784_786  JUMP_FORWARD       1156  'to 1156'
              788  BREAK_LOOP          792  'to 792'

 L. 229       790  JUMP_BACK             8  'to 8'
            792_0  COME_FROM           788  '788'
              792  JUMP_BACK             8  'to 8'
            794_0  COME_FROM           736  '736'

 L. 230       794  LOAD_FAST                'nextchar'
              796  LOAD_FAST                'self'
              798  LOAD_ATTR                commenters
              800  COMPARE_OP               in
          802_804  POP_JUMP_IF_FALSE   872  'to 872'

 L. 231       806  LOAD_FAST                'self'
              808  LOAD_ATTR                instream
              810  LOAD_METHOD              readline
              812  CALL_METHOD_0         0  ''
              814  POP_TOP          

 L. 232       816  LOAD_FAST                'self'
              818  DUP_TOP          
              820  LOAD_ATTR                lineno
              822  LOAD_CONST               1
              824  INPLACE_ADD      
              826  ROT_TWO          
              828  STORE_ATTR               lineno

 L. 233       830  LOAD_FAST                'self'
              832  LOAD_ATTR                posix
          834_836  POP_JUMP_IF_FALSE  1154  'to 1154'

 L. 234       838  LOAD_STR                 ' '
              840  LOAD_FAST                'self'
              842  STORE_ATTR               state

 L. 235       844  LOAD_FAST                'self'
              846  LOAD_ATTR                token
          848_850  POP_JUMP_IF_TRUE   1156  'to 1156'
              852  LOAD_FAST                'self'
              854  LOAD_ATTR                posix
              856  POP_JUMP_IF_FALSE_BACK     8  'to 8'
              858  LOAD_FAST                'quoted'
              860  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L. 236   862_864  JUMP_FORWARD       1156  'to 1156'
              866  BREAK_LOOP          870  'to 870'

 L. 238       868  JUMP_BACK             8  'to 8'
            870_0  COME_FROM           866  '866'
              870  JUMP_BACK             8  'to 8'
            872_0  COME_FROM           802  '802'

 L. 239       872  LOAD_FAST                'self'
              874  LOAD_ATTR                state
              876  LOAD_STR                 'c'
              878  COMPARE_OP               ==
          880_882  POP_JUMP_IF_FALSE   948  'to 948'

 L. 240       884  LOAD_FAST                'nextchar'
              886  LOAD_FAST                'self'
              888  LOAD_ATTR                punctuation_chars
              890  COMPARE_OP               in
          892_894  POP_JUMP_IF_FALSE   912  'to 912'

 L. 241       896  LOAD_FAST                'self'
              898  DUP_TOP          
              900  LOAD_ATTR                token
              902  LOAD_FAST                'nextchar'
              904  INPLACE_ADD      
              906  ROT_TWO          
              908  STORE_ATTR               token
              910  JUMP_FORWARD        946  'to 946'
            912_0  COME_FROM           892  '892'

 L. 243       912  LOAD_FAST                'nextchar'
              914  LOAD_FAST                'self'
              916  LOAD_ATTR                whitespace
              918  COMPARE_OP               not-in
          920_922  POP_JUMP_IF_FALSE   936  'to 936'

 L. 244       924  LOAD_FAST                'self'
              926  LOAD_ATTR                _pushback_chars
              928  LOAD_METHOD              append
              930  LOAD_FAST                'nextchar'
              932  CALL_METHOD_1         1  ''
              934  POP_TOP          
            936_0  COME_FROM           920  '920'

 L. 245       936  LOAD_STR                 ' '
              938  LOAD_FAST                'self'
              940  STORE_ATTR               state

 L. 246   942_944  JUMP_FORWARD       1156  'to 1156'
            946_0  COME_FROM           910  '910'
              946  JUMP_BACK             8  'to 8'
            948_0  COME_FROM           880  '880'

 L. 247       948  LOAD_FAST                'self'
              950  LOAD_ATTR                posix
          952_954  POP_JUMP_IF_FALSE   976  'to 976'
              956  LOAD_FAST                'nextchar'
              958  LOAD_FAST                'self'
              960  LOAD_ATTR                quotes
              962  COMPARE_OP               in
          964_966  POP_JUMP_IF_FALSE   976  'to 976'

 L. 248       968  LOAD_FAST                'nextchar'
              970  LOAD_FAST                'self'
              972  STORE_ATTR               state
              974  JUMP_BACK             8  'to 8'
            976_0  COME_FROM           964  '964'
            976_1  COME_FROM           952  '952'

 L. 249       976  LOAD_FAST                'self'
              978  LOAD_ATTR                posix
          980_982  POP_JUMP_IF_FALSE  1008  'to 1008'
              984  LOAD_FAST                'nextchar'
              986  LOAD_FAST                'self'
              988  LOAD_ATTR                escape
              990  COMPARE_OP               in
          992_994  POP_JUMP_IF_FALSE  1008  'to 1008'

 L. 250       996  LOAD_STR                 'a'
              998  STORE_FAST               'escapedstate'

 L. 251      1000  LOAD_FAST                'nextchar'
             1002  LOAD_FAST                'self'
             1004  STORE_ATTR               state
             1006  JUMP_BACK             8  'to 8'
           1008_0  COME_FROM           992  '992'
           1008_1  COME_FROM           980  '980'

 L. 252      1008  LOAD_FAST                'nextchar'
             1010  LOAD_FAST                'self'
             1012  LOAD_ATTR                wordchars
             1014  COMPARE_OP               in
         1016_1018  POP_JUMP_IF_TRUE   1052  'to 1052'
             1020  LOAD_FAST                'nextchar'
             1022  LOAD_FAST                'self'
             1024  LOAD_ATTR                quotes
             1026  COMPARE_OP               in
         1028_1030  POP_JUMP_IF_TRUE   1052  'to 1052'

 L. 253      1032  LOAD_FAST                'self'
             1034  LOAD_ATTR                whitespace_split

 L. 252  1036_1038  POP_JUMP_IF_FALSE  1068  'to 1068'

 L. 254      1040  LOAD_FAST                'nextchar'
             1042  LOAD_FAST                'self'
             1044  LOAD_ATTR                punctuation_chars
             1046  COMPARE_OP               not-in

 L. 252  1048_1050  POP_JUMP_IF_FALSE  1068  'to 1068'
           1052_0  COME_FROM          1028  '1028'
           1052_1  COME_FROM          1016  '1016'

 L. 255      1052  LOAD_FAST                'self'
             1054  DUP_TOP          
             1056  LOAD_ATTR                token
             1058  LOAD_FAST                'nextchar'
             1060  INPLACE_ADD      
             1062  ROT_TWO          
             1064  STORE_ATTR               token
             1066  JUMP_BACK             8  'to 8'
           1068_0  COME_FROM          1048  '1048'
           1068_1  COME_FROM          1036  '1036'

 L. 257      1068  LOAD_FAST                'self'
             1070  LOAD_ATTR                punctuation_chars
         1072_1074  POP_JUMP_IF_FALSE  1090  'to 1090'

 L. 258      1076  LOAD_FAST                'self'
             1078  LOAD_ATTR                _pushback_chars
             1080  LOAD_METHOD              append
             1082  LOAD_FAST                'nextchar'
             1084  CALL_METHOD_1         1  ''
             1086  POP_TOP          
             1088  JUMP_FORWARD       1102  'to 1102'
           1090_0  COME_FROM          1072  '1072'

 L. 260      1090  LOAD_FAST                'self'
             1092  LOAD_ATTR                pushback
             1094  LOAD_METHOD              appendleft
             1096  LOAD_FAST                'nextchar'
             1098  CALL_METHOD_1         1  ''
             1100  POP_TOP          
           1102_0  COME_FROM          1088  '1088'

 L. 261      1102  LOAD_FAST                'self'
             1104  LOAD_ATTR                debug
             1106  LOAD_CONST               2
             1108  COMPARE_OP               >=
         1110_1112  POP_JUMP_IF_FALSE  1122  'to 1122'

 L. 262      1114  LOAD_GLOBAL              print
             1116  LOAD_STR                 'shlex: I see punctuation in word state'
             1118  CALL_FUNCTION_1       1  ''
             1120  POP_TOP          
           1122_0  COME_FROM          1110  '1110'

 L. 263      1122  LOAD_STR                 ' '
             1124  LOAD_FAST                'self'
             1126  STORE_ATTR               state

 L. 264      1128  LOAD_FAST                'self'
             1130  LOAD_ATTR                token
         1132_1134  POP_JUMP_IF_TRUE   1156  'to 1156'
             1136  LOAD_FAST                'self'
             1138  LOAD_ATTR                posix
             1140  POP_JUMP_IF_FALSE_BACK     8  'to 8'
             1142  LOAD_FAST                'quoted'
             1144  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L. 265  1146_1148  JUMP_FORWARD       1156  'to 1156'
             1150  CONTINUE              8  'to 8'

 L. 267      1152  JUMP_BACK             8  'to 8'
           1154_0  COME_FROM           834  '834'
           1154_1  COME_FROM           142  '142'
             1154  JUMP_BACK             8  'to 8'
           1156_0  COME_FROM          1146  '1146'
           1156_1  COME_FROM          1132  '1132'
           1156_2  COME_FROM           942  '942'
           1156_3  COME_FROM           862  '862'
           1156_4  COME_FROM           848  '848'
           1156_5  COME_FROM           784  '784'
           1156_6  COME_FROM           770  '770'
           1156_7  COME_FROM           722  '722'
           1156_8  COME_FROM           502  '502'
           1156_9  COME_FROM           400  '400'
          1156_10  COME_FROM           386  '386'
          1156_11  COME_FROM           190  '190'
          1156_12  COME_FROM           138  '138'
          1156_13  COME_FROM           110  '110'

 L. 268      1156  LOAD_FAST                'self'
             1158  LOAD_ATTR                token
             1160  STORE_FAST               'result'

 L. 269      1162  LOAD_STR                 ''
             1164  LOAD_FAST                'self'
             1166  STORE_ATTR               token

 L. 270      1168  LOAD_FAST                'self'
             1170  LOAD_ATTR                posix
         1172_1174  POP_JUMP_IF_FALSE  1196  'to 1196'
             1176  LOAD_FAST                'quoted'
         1178_1180  POP_JUMP_IF_TRUE   1196  'to 1196'
             1182  LOAD_FAST                'result'
             1184  LOAD_STR                 ''
             1186  COMPARE_OP               ==
         1188_1190  POP_JUMP_IF_FALSE  1196  'to 1196'

 L. 271      1192  LOAD_CONST               None
             1194  STORE_FAST               'result'
           1196_0  COME_FROM          1188  '1188'
           1196_1  COME_FROM          1178  '1178'
           1196_2  COME_FROM          1172  '1172'

 L. 272      1196  LOAD_FAST                'self'
             1198  LOAD_ATTR                debug
             1200  LOAD_CONST               1
             1202  COMPARE_OP               >
         1204_1206  POP_JUMP_IF_FALSE  1240  'to 1240'

 L. 273      1208  LOAD_FAST                'result'
         1210_1212  POP_JUMP_IF_FALSE  1232  'to 1232'

 L. 274      1214  LOAD_GLOBAL              print
             1216  LOAD_STR                 'shlex: raw token='
             1218  LOAD_GLOBAL              repr
             1220  LOAD_FAST                'result'
             1222  CALL_FUNCTION_1       1  ''
             1224  BINARY_ADD       
             1226  CALL_FUNCTION_1       1  ''
             1228  POP_TOP          
             1230  JUMP_FORWARD       1240  'to 1240'
           1232_0  COME_FROM          1210  '1210'

 L. 276      1232  LOAD_GLOBAL              print
             1234  LOAD_STR                 'shlex: raw token=EOF'
             1236  CALL_FUNCTION_1       1  ''
             1238  POP_TOP          
           1240_0  COME_FROM          1230  '1230'
           1240_1  COME_FROM          1204  '1204'

 L. 277      1240  LOAD_FAST                'result'
             1242  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BREAK_LOOP' instruction at offset 404

    def sourcehook(self, newfile):
        """Hook called on a filename to be sourced."""
        if newfile[0] == '"':
            newfile = newfile[1:-1]
        if isinstance(self.infile, str):
            if not os.path.isabs(newfile):
                newfile = os.path.join(os.path.dirname(self.infile), newfile)
            return (newfile, open(newfile, 'r'))

    def error_leader(self, infile=None, lineno=None):
        """Emit a C-compiler-like, Emacs-friendly error-message leader."""
        if infile is None:
            infile = self.infile
        if lineno is None:
            lineno = self.lineno
        return '"%s", line %d: ' % (infile, lineno)

    def __iter__(self):
        return self

    def __next__(self):
        token = self.get_token()
        if token == self.eof:
            raise StopIteration
        return token


def split(s, comments=False, posix=True):
    lex = shlex(s, posix=posix)
    lex.whitespace_split = True
    if not comments:
        lex.commenters = ''
    return list(lex)


def join(split_command):
    """Return a shell-escaped string from *split_command*."""
    return ' '.join((quote(arg) for arg in split_command))


_find_unsafe = re.compile('[^\\w@%+=:,./-]', re.ASCII).search

def quote(s):
    """Return a shell-escaped version of the string *s*."""
    if not s:
        return "''"
    if _find_unsafe(s) is None:
        return s
    return "'" + s.replace("'", '\'"\'"\'') + "'"


def _print_tokens(lexer):
    while True:
        tt = lexer.get_token()
        if not tt:
            pass
        else:
            print('Token: ' + repr(tt))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        _print_tokens(shlex())
    else:
        fn = sys.argv[1]
        with open(fn) as f:
            _print_tokens(shlex(f, fn))