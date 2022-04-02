# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.11 (default, Sep  3 2021, 20:46:09) 
# [GCC 10.2.1 20210110]
# Embedded file name: shlex.py
"""A lexical analyzer class for simple shell-like syntaxes."""
import os, re, sys
from collections import deque
from io import StringIO
__all__ = [
 'shlex', 'split', 'quote']

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
            while raw == self.source:
                spec = self.sourcehook(self.read_token())
                if spec:
                    newfile, newstream = spec
                    self.push_source(newstream, newfile)
                else:
                    raw = self.get_token()

        while raw == self.eof:
            if not self.filestack:
                return self.eof
            else:
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

 L. 136      8_10  SETUP_LOOP         1130  'to 1130'
             12_0  COME_FROM          1126  '1126'
             12_1  COME_FROM          1124  '1124'
             12_2  COME_FROM          1122  '1122'
             12_3  COME_FROM          1118  '1118'
             12_4  COME_FROM          1114  '1114'
             12_5  COME_FROM          1040  '1040'
             12_6  COME_FROM           992  '992'
             12_7  COME_FROM           960  '960'
             12_8  COME_FROM           932  '932'
             12_9  COME_FROM           858  '858'
            12_10  COME_FROM           856  '856'
            12_11  COME_FROM           850  '850'
            12_12  COME_FROM           846  '846'
            12_13  COME_FROM           782  '782'
            12_14  COME_FROM           780  '780'
            12_15  COME_FROM           774  '774'
            12_16  COME_FROM           770  '770'
            12_17  COME_FROM           718  '718'
            12_18  COME_FROM           702  '702'
            12_19  COME_FROM           692  '692'
            12_20  COME_FROM           572  '572'
            12_21  COME_FROM           404  '404'
            12_22  COME_FROM           402  '402'
            12_23  COME_FROM           396  '396'
            12_24  COME_FROM           392  '392'
            12_25  COME_FROM           194  '194'
            12_26  COME_FROM           188  '188'
            12_27  COME_FROM           184  '184'
            12_28  COME_FROM           116  '116'

 L. 137        12  LOAD_FAST                'self'
               14  LOAD_ATTR                punctuation_chars
               16  POP_JUMP_IF_FALSE    36  'to 36'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _pushback_chars
               22  POP_JUMP_IF_FALSE    36  'to 36'

 L. 138        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _pushback_chars
               28  LOAD_METHOD              pop
               30  CALL_METHOD_0         0  '0 positional arguments'
               32  STORE_FAST               'nextchar'
               34  JUMP_FORWARD         48  'to 48'
             36_0  COME_FROM            22  '22'
             36_1  COME_FROM            16  '16'

 L. 140        36  LOAD_FAST                'self'
               38  LOAD_ATTR                instream
               40  LOAD_METHOD              read
               42  LOAD_CONST               1
               44  CALL_METHOD_1         1  '1 positional argument'
               46  STORE_FAST               'nextchar'
             48_0  COME_FROM            34  '34'

 L. 141        48  LOAD_FAST                'nextchar'
               50  LOAD_STR                 '\n'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    70  'to 70'

 L. 142        56  LOAD_FAST                'self'
               58  DUP_TOP          
               60  LOAD_ATTR                lineno
               62  LOAD_CONST               1
               64  INPLACE_ADD      
               66  ROT_TWO          
               68  STORE_ATTR               lineno
             70_0  COME_FROM            54  '54'

 L. 143        70  LOAD_FAST                'self'
               72  LOAD_ATTR                debug
               74  LOAD_CONST               3
               76  COMPARE_OP               >=
               78  POP_JUMP_IF_FALSE    98  'to 98'

 L. 144        80  LOAD_GLOBAL              print
               82  LOAD_STR                 'shlex: in state %r I see character: %r'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                state

 L. 145        88  LOAD_FAST                'nextchar'
               90  BUILD_TUPLE_2         2 
               92  BINARY_MODULO    
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  POP_TOP          
             98_0  COME_FROM            78  '78'

 L. 146        98  LOAD_FAST                'self'
              100  LOAD_ATTR                state
              102  LOAD_CONST               None
              104  COMPARE_OP               is
              106  POP_JUMP_IF_FALSE   118  'to 118'

 L. 147       108  LOAD_STR                 ''
              110  LOAD_FAST                'self'
              112  STORE_ATTR               token

 L. 148       114  BREAK_LOOP       
              116  JUMP_BACK            12  'to 12'
            118_0  COME_FROM           106  '106'

 L. 149       118  LOAD_FAST                'self'
              120  LOAD_ATTR                state
              122  LOAD_STR                 ' '
              124  COMPARE_OP               ==
          126_128  POP_JUMP_IF_FALSE   406  'to 406'

 L. 150       130  LOAD_FAST                'nextchar'
              132  POP_JUMP_IF_TRUE    146  'to 146'

 L. 151       134  LOAD_CONST               None
              136  LOAD_FAST                'self'
              138  STORE_ATTR               state

 L. 152       140  BREAK_LOOP       
          142_144  JUMP_FORWARD       1126  'to 1126'
            146_0  COME_FROM           132  '132'

 L. 153       146  LOAD_FAST                'nextchar'
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                whitespace
              152  COMPARE_OP               in
              154  POP_JUMP_IF_FALSE   198  'to 198'

 L. 154       156  LOAD_FAST                'self'
              158  LOAD_ATTR                debug
              160  LOAD_CONST               2
              162  COMPARE_OP               >=
              164  POP_JUMP_IF_FALSE   174  'to 174'

 L. 155       166  LOAD_GLOBAL              print
              168  LOAD_STR                 'shlex: I see whitespace in whitespace state'
              170  CALL_FUNCTION_1       1  '1 positional argument'
              172  POP_TOP          
            174_0  COME_FROM           164  '164'

 L. 156       174  LOAD_FAST                'self'
              176  LOAD_ATTR                token
              178  POP_JUMP_IF_TRUE    190  'to 190'
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                posix
              184  POP_JUMP_IF_FALSE_BACK    12  'to 12'
              186  LOAD_FAST                'quoted'
              188  POP_JUMP_IF_FALSE_BACK    12  'to 12'
            190_0  COME_FROM           178  '178'

 L. 157       190  BREAK_LOOP       
              192  JUMP_FORWARD        196  'to 196'

 L. 159       194  CONTINUE             12  'to 12'
            196_0  COME_FROM           192  '192'
              196  JUMP_FORWARD        404  'to 404'
            198_0  COME_FROM           154  '154'

 L. 160       198  LOAD_FAST                'nextchar'
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                commenters
              204  COMPARE_OP               in
              206  POP_JUMP_IF_FALSE   234  'to 234'

 L. 161       208  LOAD_FAST                'self'
              210  LOAD_ATTR                instream
              212  LOAD_METHOD              readline
              214  CALL_METHOD_0         0  '0 positional arguments'
              216  POP_TOP          

 L. 162       218  LOAD_FAST                'self'
              220  DUP_TOP          
              222  LOAD_ATTR                lineno
              224  LOAD_CONST               1
              226  INPLACE_ADD      
              228  ROT_TWO          
              230  STORE_ATTR               lineno
              232  JUMP_FORWARD        404  'to 404'
            234_0  COME_FROM           206  '206'

 L. 163       234  LOAD_FAST                'self'
              236  LOAD_ATTR                posix
          238_240  POP_JUMP_IF_FALSE   266  'to 266'
              242  LOAD_FAST                'nextchar'
              244  LOAD_FAST                'self'
              246  LOAD_ATTR                escape
              248  COMPARE_OP               in
          250_252  POP_JUMP_IF_FALSE   266  'to 266'

 L. 164       254  LOAD_STR                 'a'
              256  STORE_FAST               'escapedstate'

 L. 165       258  LOAD_FAST                'nextchar'
              260  LOAD_FAST                'self'
              262  STORE_ATTR               state
              264  JUMP_FORWARD        404  'to 404'
            266_0  COME_FROM           250  '250'
            266_1  COME_FROM           238  '238'

 L. 166       266  LOAD_FAST                'nextchar'
              268  LOAD_FAST                'self'
              270  LOAD_ATTR                wordchars
              272  COMPARE_OP               in
          274_276  POP_JUMP_IF_FALSE   292  'to 292'

 L. 167       278  LOAD_FAST                'nextchar'
              280  LOAD_FAST                'self'
              282  STORE_ATTR               token

 L. 168       284  LOAD_STR                 'a'
              286  LOAD_FAST                'self'
              288  STORE_ATTR               state
              290  JUMP_FORWARD        404  'to 404'
            292_0  COME_FROM           274  '274'

 L. 169       292  LOAD_FAST                'nextchar'
              294  LOAD_FAST                'self'
              296  LOAD_ATTR                punctuation_chars
              298  COMPARE_OP               in
          300_302  POP_JUMP_IF_FALSE   318  'to 318'

 L. 170       304  LOAD_FAST                'nextchar'
              306  LOAD_FAST                'self'
              308  STORE_ATTR               token

 L. 171       310  LOAD_STR                 'c'
              312  LOAD_FAST                'self'
              314  STORE_ATTR               state
              316  JUMP_FORWARD        404  'to 404'
            318_0  COME_FROM           300  '300'

 L. 172       318  LOAD_FAST                'nextchar'
              320  LOAD_FAST                'self'
              322  LOAD_ATTR                quotes
              324  COMPARE_OP               in
          326_328  POP_JUMP_IF_FALSE   352  'to 352'

 L. 173       330  LOAD_FAST                'self'
              332  LOAD_ATTR                posix
          334_336  POP_JUMP_IF_TRUE    344  'to 344'

 L. 174       338  LOAD_FAST                'nextchar'
              340  LOAD_FAST                'self'
              342  STORE_ATTR               token
            344_0  COME_FROM           334  '334'

 L. 175       344  LOAD_FAST                'nextchar'
              346  LOAD_FAST                'self'
              348  STORE_ATTR               state
              350  JUMP_FORWARD        404  'to 404'
            352_0  COME_FROM           326  '326'

 L. 176       352  LOAD_FAST                'self'
              354  LOAD_ATTR                whitespace_split
          356_358  POP_JUMP_IF_FALSE   374  'to 374'

 L. 177       360  LOAD_FAST                'nextchar'
              362  LOAD_FAST                'self'
              364  STORE_ATTR               token

 L. 178       366  LOAD_STR                 'a'
              368  LOAD_FAST                'self'
              370  STORE_ATTR               state
              372  JUMP_FORWARD        404  'to 404'
            374_0  COME_FROM           356  '356'

 L. 180       374  LOAD_FAST                'nextchar'
              376  LOAD_FAST                'self'
              378  STORE_ATTR               token

 L. 181       380  LOAD_FAST                'self'
              382  LOAD_ATTR                token
          384_386  POP_JUMP_IF_TRUE    398  'to 398'
              388  LOAD_FAST                'self'
              390  LOAD_ATTR                posix
              392  POP_JUMP_IF_FALSE_BACK    12  'to 12'
              394  LOAD_FAST                'quoted'
              396  POP_JUMP_IF_FALSE_BACK    12  'to 12'
            398_0  COME_FROM           384  '384'

 L. 182       398  BREAK_LOOP       
              400  JUMP_FORWARD        404  'to 404'

 L. 184       402  CONTINUE             12  'to 12'
            404_0  COME_FROM           400  '400'
            404_1  COME_FROM           372  '372'
            404_2  COME_FROM           350  '350'
            404_3  COME_FROM           316  '316'
            404_4  COME_FROM           290  '290'
            404_5  COME_FROM           264  '264'
            404_6  COME_FROM           232  '232'
            404_7  COME_FROM           196  '196'
              404  JUMP_BACK            12  'to 12'
            406_0  COME_FROM           126  '126'

 L. 185       406  LOAD_FAST                'self'
              408  LOAD_ATTR                state
              410  LOAD_FAST                'self'
              412  LOAD_ATTR                quotes
              414  COMPARE_OP               in
          416_418  POP_JUMP_IF_FALSE   574  'to 574'

 L. 186       420  LOAD_CONST               True
              422  STORE_FAST               'quoted'

 L. 187       424  LOAD_FAST                'nextchar'
          426_428  POP_JUMP_IF_TRUE    458  'to 458'

 L. 188       430  LOAD_FAST                'self'
              432  LOAD_ATTR                debug
              434  LOAD_CONST               2
              436  COMPARE_OP               >=
          438_440  POP_JUMP_IF_FALSE   450  'to 450'

 L. 189       442  LOAD_GLOBAL              print
              444  LOAD_STR                 'shlex: I see EOF in quotes state'
              446  CALL_FUNCTION_1       1  '1 positional argument'
              448  POP_TOP          
            450_0  COME_FROM           438  '438'

 L. 191       450  LOAD_GLOBAL              ValueError
              452  LOAD_STR                 'No closing quotation'
              454  CALL_FUNCTION_1       1  '1 positional argument'
              456  RAISE_VARARGS_1       1  'exception instance'
            458_0  COME_FROM           426  '426'

 L. 192       458  LOAD_FAST                'nextchar'
              460  LOAD_FAST                'self'
              462  LOAD_ATTR                state
              464  COMPARE_OP               ==
          466_468  POP_JUMP_IF_FALSE   510  'to 510'

 L. 193       470  LOAD_FAST                'self'
              472  LOAD_ATTR                posix
          474_476  POP_JUMP_IF_TRUE    502  'to 502'

 L. 194       478  LOAD_FAST                'self'
              480  DUP_TOP          
              482  LOAD_ATTR                token
              484  LOAD_FAST                'nextchar'
              486  INPLACE_ADD      
              488  ROT_TWO          
              490  STORE_ATTR               token

 L. 195       492  LOAD_STR                 ' '
              494  LOAD_FAST                'self'
              496  STORE_ATTR               state

 L. 196       498  BREAK_LOOP       
              500  JUMP_FORWARD        508  'to 508'
            502_0  COME_FROM           474  '474'

 L. 198       502  LOAD_STR                 'a'
              504  LOAD_FAST                'self'
              506  STORE_ATTR               state
            508_0  COME_FROM           500  '500'
              508  JUMP_FORWARD        572  'to 572'
            510_0  COME_FROM           466  '466'

 L. 199       510  LOAD_FAST                'self'
              512  LOAD_ATTR                posix
          514_516  POP_JUMP_IF_FALSE   558  'to 558'
              518  LOAD_FAST                'nextchar'
              520  LOAD_FAST                'self'
              522  LOAD_ATTR                escape
              524  COMPARE_OP               in
          526_528  POP_JUMP_IF_FALSE   558  'to 558'
              530  LOAD_FAST                'self'
              532  LOAD_ATTR                state

 L. 200       534  LOAD_FAST                'self'
              536  LOAD_ATTR                escapedquotes
              538  COMPARE_OP               in
          540_542  POP_JUMP_IF_FALSE   558  'to 558'

 L. 201       544  LOAD_FAST                'self'
              546  LOAD_ATTR                state
              548  STORE_FAST               'escapedstate'

 L. 202       550  LOAD_FAST                'nextchar'
              552  LOAD_FAST                'self'
              554  STORE_ATTR               state
              556  JUMP_FORWARD        572  'to 572'
            558_0  COME_FROM           540  '540'
            558_1  COME_FROM           526  '526'
            558_2  COME_FROM           514  '514'

 L. 204       558  LOAD_FAST                'self'
              560  DUP_TOP          
              562  LOAD_ATTR                token
              564  LOAD_FAST                'nextchar'
              566  INPLACE_ADD      
              568  ROT_TWO          
              570  STORE_ATTR               token
            572_0  COME_FROM           556  '556'
            572_1  COME_FROM           508  '508'
              572  JUMP_BACK            12  'to 12'
            574_0  COME_FROM           416  '416'

 L. 205       574  LOAD_FAST                'self'
              576  LOAD_ATTR                state
              578  LOAD_FAST                'self'
              580  LOAD_ATTR                escape
              582  COMPARE_OP               in
          584_586  POP_JUMP_IF_FALSE   694  'to 694'

 L. 206       588  LOAD_FAST                'nextchar'
          590_592  POP_JUMP_IF_TRUE    622  'to 622'

 L. 207       594  LOAD_FAST                'self'
              596  LOAD_ATTR                debug
              598  LOAD_CONST               2
              600  COMPARE_OP               >=
          602_604  POP_JUMP_IF_FALSE   614  'to 614'

 L. 208       606  LOAD_GLOBAL              print
              608  LOAD_STR                 'shlex: I see EOF in escape state'
              610  CALL_FUNCTION_1       1  '1 positional argument'
              612  POP_TOP          
            614_0  COME_FROM           602  '602'

 L. 210       614  LOAD_GLOBAL              ValueError
              616  LOAD_STR                 'No escaped character'
              618  CALL_FUNCTION_1       1  '1 positional argument'
              620  RAISE_VARARGS_1       1  'exception instance'
            622_0  COME_FROM           590  '590'

 L. 213       622  LOAD_FAST                'escapedstate'
              624  LOAD_FAST                'self'
              626  LOAD_ATTR                quotes
              628  COMPARE_OP               in
          630_632  POP_JUMP_IF_FALSE   672  'to 672'

 L. 214       634  LOAD_FAST                'nextchar'
              636  LOAD_FAST                'self'
              638  LOAD_ATTR                state
              640  COMPARE_OP               !=
          642_644  POP_JUMP_IF_FALSE   672  'to 672'
              646  LOAD_FAST                'nextchar'
              648  LOAD_FAST                'escapedstate'
              650  COMPARE_OP               !=
          652_654  POP_JUMP_IF_FALSE   672  'to 672'

 L. 215       656  LOAD_FAST                'self'
              658  DUP_TOP          
              660  LOAD_ATTR                token
              662  LOAD_FAST                'self'
              664  LOAD_ATTR                state
              666  INPLACE_ADD      
              668  ROT_TWO          
              670  STORE_ATTR               token
            672_0  COME_FROM           652  '652'
            672_1  COME_FROM           642  '642'
            672_2  COME_FROM           630  '630'

 L. 216       672  LOAD_FAST                'self'
              674  DUP_TOP          
              676  LOAD_ATTR                token
              678  LOAD_FAST                'nextchar'
              680  INPLACE_ADD      
              682  ROT_TWO          
              684  STORE_ATTR               token

 L. 217       686  LOAD_FAST                'escapedstate'
              688  LOAD_FAST                'self'
              690  STORE_ATTR               state
              692  JUMP_BACK            12  'to 12'
            694_0  COME_FROM           584  '584'

 L. 218       694  LOAD_FAST                'self'
              696  LOAD_ATTR                state
              698  LOAD_CONST               ('a', 'c')
              700  COMPARE_OP               in
              702  POP_JUMP_IF_FALSE_BACK    12  'to 12'

 L. 219       704  LOAD_FAST                'nextchar'
          706_708  POP_JUMP_IF_TRUE    720  'to 720'

 L. 220       710  LOAD_CONST               None
              712  LOAD_FAST                'self'
              714  STORE_ATTR               state

 L. 221       716  BREAK_LOOP       
              718  JUMP_BACK            12  'to 12'
            720_0  COME_FROM           706  '706'

 L. 222       720  LOAD_FAST                'nextchar'
              722  LOAD_FAST                'self'
              724  LOAD_ATTR                whitespace
              726  COMPARE_OP               in
          728_730  POP_JUMP_IF_FALSE   784  'to 784'

 L. 223       732  LOAD_FAST                'self'
              734  LOAD_ATTR                debug
              736  LOAD_CONST               2
              738  COMPARE_OP               >=
          740_742  POP_JUMP_IF_FALSE   752  'to 752'

 L. 224       744  LOAD_GLOBAL              print
              746  LOAD_STR                 'shlex: I see whitespace in word state'
              748  CALL_FUNCTION_1       1  '1 positional argument'
              750  POP_TOP          
            752_0  COME_FROM           740  '740'

 L. 225       752  LOAD_STR                 ' '
              754  LOAD_FAST                'self'
              756  STORE_ATTR               state

 L. 226       758  LOAD_FAST                'self'
              760  LOAD_ATTR                token
          762_764  POP_JUMP_IF_TRUE    776  'to 776'
              766  LOAD_FAST                'self'
              768  LOAD_ATTR                posix
              770  POP_JUMP_IF_FALSE_BACK    12  'to 12'
              772  LOAD_FAST                'quoted'
              774  POP_JUMP_IF_FALSE_BACK    12  'to 12'
            776_0  COME_FROM           762  '762'

 L. 227       776  BREAK_LOOP       
              778  JUMP_FORWARD        782  'to 782'

 L. 229       780  CONTINUE             12  'to 12'
            782_0  COME_FROM           778  '778'
              782  JUMP_BACK            12  'to 12'
            784_0  COME_FROM           728  '728'

 L. 230       784  LOAD_FAST                'nextchar'
              786  LOAD_FAST                'self'
              788  LOAD_ATTR                commenters
              790  COMPARE_OP               in
          792_794  POP_JUMP_IF_FALSE   860  'to 860'

 L. 231       796  LOAD_FAST                'self'
              798  LOAD_ATTR                instream
              800  LOAD_METHOD              readline
              802  CALL_METHOD_0         0  '0 positional arguments'
              804  POP_TOP          

 L. 232       806  LOAD_FAST                'self'
              808  DUP_TOP          
              810  LOAD_ATTR                lineno
              812  LOAD_CONST               1
              814  INPLACE_ADD      
              816  ROT_TWO          
              818  STORE_ATTR               lineno

 L. 233       820  LOAD_FAST                'self'
              822  LOAD_ATTR                posix
          824_826  POP_JUMP_IF_FALSE  1126  'to 1126'

 L. 234       828  LOAD_STR                 ' '
              830  LOAD_FAST                'self'
              832  STORE_ATTR               state

 L. 235       834  LOAD_FAST                'self'
              836  LOAD_ATTR                token
          838_840  POP_JUMP_IF_TRUE    852  'to 852'
              842  LOAD_FAST                'self'
              844  LOAD_ATTR                posix
              846  POP_JUMP_IF_FALSE_BACK    12  'to 12'
              848  LOAD_FAST                'quoted'
              850  POP_JUMP_IF_FALSE_BACK    12  'to 12'
            852_0  COME_FROM           838  '838'

 L. 236       852  BREAK_LOOP       
              854  JUMP_FORWARD        858  'to 858'

 L. 238       856  CONTINUE             12  'to 12'
            858_0  COME_FROM           854  '854'
              858  JUMP_BACK            12  'to 12'
            860_0  COME_FROM           792  '792'

 L. 239       860  LOAD_FAST                'self'
              862  LOAD_ATTR                state
              864  LOAD_STR                 'c'
              866  COMPARE_OP               ==
          868_870  POP_JUMP_IF_FALSE   934  'to 934'

 L. 240       872  LOAD_FAST                'nextchar'
              874  LOAD_FAST                'self'
              876  LOAD_ATTR                punctuation_chars
              878  COMPARE_OP               in
          880_882  POP_JUMP_IF_FALSE   900  'to 900'

 L. 241       884  LOAD_FAST                'self'
              886  DUP_TOP          
              888  LOAD_ATTR                token
              890  LOAD_FAST                'nextchar'
              892  INPLACE_ADD      
              894  ROT_TWO          
              896  STORE_ATTR               token
              898  JUMP_FORWARD        932  'to 932'
            900_0  COME_FROM           880  '880'

 L. 243       900  LOAD_FAST                'nextchar'
              902  LOAD_FAST                'self'
              904  LOAD_ATTR                whitespace
              906  COMPARE_OP               not-in
          908_910  POP_JUMP_IF_FALSE   924  'to 924'

 L. 244       912  LOAD_FAST                'self'
              914  LOAD_ATTR                _pushback_chars
              916  LOAD_METHOD              append
              918  LOAD_FAST                'nextchar'
              920  CALL_METHOD_1         1  '1 positional argument'
              922  POP_TOP          
            924_0  COME_FROM           908  '908'

 L. 245       924  LOAD_STR                 ' '
              926  LOAD_FAST                'self'
              928  STORE_ATTR               state

 L. 246       930  BREAK_LOOP       
            932_0  COME_FROM           898  '898'
              932  JUMP_BACK            12  'to 12'
            934_0  COME_FROM           868  '868'

 L. 247       934  LOAD_FAST                'self'
              936  LOAD_ATTR                posix
          938_940  POP_JUMP_IF_FALSE   962  'to 962'
              942  LOAD_FAST                'nextchar'
              944  LOAD_FAST                'self'
              946  LOAD_ATTR                quotes
              948  COMPARE_OP               in
          950_952  POP_JUMP_IF_FALSE   962  'to 962'

 L. 248       954  LOAD_FAST                'nextchar'
              956  LOAD_FAST                'self'
              958  STORE_ATTR               state
              960  JUMP_BACK            12  'to 12'
            962_0  COME_FROM           950  '950'
            962_1  COME_FROM           938  '938'

 L. 249       962  LOAD_FAST                'self'
              964  LOAD_ATTR                posix
          966_968  POP_JUMP_IF_FALSE   994  'to 994'
              970  LOAD_FAST                'nextchar'
              972  LOAD_FAST                'self'
              974  LOAD_ATTR                escape
              976  COMPARE_OP               in
          978_980  POP_JUMP_IF_FALSE   994  'to 994'

 L. 250       982  LOAD_STR                 'a'
              984  STORE_FAST               'escapedstate'

 L. 251       986  LOAD_FAST                'nextchar'
              988  LOAD_FAST                'self'
              990  STORE_ATTR               state
              992  JUMP_BACK            12  'to 12'
            994_0  COME_FROM           978  '978'
            994_1  COME_FROM           966  '966'

 L. 252       994  LOAD_FAST                'nextchar'
              996  LOAD_FAST                'self'
              998  LOAD_ATTR                wordchars
             1000  COMPARE_OP               in
         1002_1004  POP_JUMP_IF_TRUE   1026  'to 1026'
             1006  LOAD_FAST                'nextchar'
             1008  LOAD_FAST                'self'
             1010  LOAD_ATTR                quotes
             1012  COMPARE_OP               in
         1014_1016  POP_JUMP_IF_TRUE   1026  'to 1026'

 L. 253      1018  LOAD_FAST                'self'
             1020  LOAD_ATTR                whitespace_split
         1022_1024  POP_JUMP_IF_FALSE  1042  'to 1042'
           1026_0  COME_FROM          1014  '1014'
           1026_1  COME_FROM          1002  '1002'

 L. 254      1026  LOAD_FAST                'self'
             1028  DUP_TOP          
             1030  LOAD_ATTR                token
             1032  LOAD_FAST                'nextchar'
             1034  INPLACE_ADD      
             1036  ROT_TWO          
             1038  STORE_ATTR               token
             1040  JUMP_BACK            12  'to 12'
           1042_0  COME_FROM          1022  '1022'

 L. 256      1042  LOAD_FAST                'self'
             1044  LOAD_ATTR                punctuation_chars
         1046_1048  POP_JUMP_IF_FALSE  1064  'to 1064'

 L. 257      1050  LOAD_FAST                'self'
             1052  LOAD_ATTR                _pushback_chars
             1054  LOAD_METHOD              append
             1056  LOAD_FAST                'nextchar'
             1058  CALL_METHOD_1         1  '1 positional argument'
             1060  POP_TOP          
             1062  JUMP_FORWARD       1076  'to 1076'
           1064_0  COME_FROM          1046  '1046'

 L. 259      1064  LOAD_FAST                'self'
             1066  LOAD_ATTR                pushback
             1068  LOAD_METHOD              appendleft
             1070  LOAD_FAST                'nextchar'
             1072  CALL_METHOD_1         1  '1 positional argument'
             1074  POP_TOP          
           1076_0  COME_FROM          1062  '1062'

 L. 260      1076  LOAD_FAST                'self'
             1078  LOAD_ATTR                debug
             1080  LOAD_CONST               2
             1082  COMPARE_OP               >=
         1084_1086  POP_JUMP_IF_FALSE  1096  'to 1096'

 L. 261      1088  LOAD_GLOBAL              print
             1090  LOAD_STR                 'shlex: I see punctuation in word state'
             1092  CALL_FUNCTION_1       1  '1 positional argument'
             1094  POP_TOP          
           1096_0  COME_FROM          1084  '1084'

 L. 262      1096  LOAD_STR                 ' '
             1098  LOAD_FAST                'self'
             1100  STORE_ATTR               state

 L. 263      1102  LOAD_FAST                'self'
             1104  LOAD_ATTR                token
         1106_1108  POP_JUMP_IF_TRUE   1120  'to 1120'
             1110  LOAD_FAST                'self'
             1112  LOAD_ATTR                posix
             1114  POP_JUMP_IF_FALSE_BACK    12  'to 12'
             1116  LOAD_FAST                'quoted'
             1118  POP_JUMP_IF_FALSE_BACK    12  'to 12'
           1120_0  COME_FROM          1106  '1106'

 L. 264      1120  BREAK_LOOP       
             1122  JUMP_BACK            12  'to 12'

 L. 266      1124  CONTINUE             12  'to 12'
           1126_0  COME_FROM           824  '824'
           1126_1  COME_FROM           142  '142'
             1126  JUMP_BACK            12  'to 12'
             1128  POP_BLOCK        
           1130_0  COME_FROM_LOOP        8  '8'

 L. 267      1130  LOAD_FAST                'self'
             1132  LOAD_ATTR                token
             1134  STORE_FAST               'result'

 L. 268      1136  LOAD_STR                 ''
             1138  LOAD_FAST                'self'
             1140  STORE_ATTR               token

 L. 269      1142  LOAD_FAST                'self'
             1144  LOAD_ATTR                posix
         1146_1148  POP_JUMP_IF_FALSE  1170  'to 1170'
             1150  LOAD_FAST                'quoted'
         1152_1154  POP_JUMP_IF_TRUE   1170  'to 1170'
             1156  LOAD_FAST                'result'
             1158  LOAD_STR                 ''
             1160  COMPARE_OP               ==
         1162_1164  POP_JUMP_IF_FALSE  1170  'to 1170'

 L. 270      1166  LOAD_CONST               None
             1168  STORE_FAST               'result'
           1170_0  COME_FROM          1162  '1162'
           1170_1  COME_FROM          1152  '1152'
           1170_2  COME_FROM          1146  '1146'

 L. 271      1170  LOAD_FAST                'self'
             1172  LOAD_ATTR                debug
             1174  LOAD_CONST               1
             1176  COMPARE_OP               >
         1178_1180  POP_JUMP_IF_FALSE  1214  'to 1214'

 L. 272      1182  LOAD_FAST                'result'
         1184_1186  POP_JUMP_IF_FALSE  1206  'to 1206'

 L. 273      1188  LOAD_GLOBAL              print
             1190  LOAD_STR                 'shlex: raw token='
             1192  LOAD_GLOBAL              repr
             1194  LOAD_FAST                'result'
             1196  CALL_FUNCTION_1       1  '1 positional argument'
             1198  BINARY_ADD       
             1200  CALL_FUNCTION_1       1  '1 positional argument'
             1202  POP_TOP          
             1204  JUMP_FORWARD       1214  'to 1214'
           1206_0  COME_FROM          1184  '1184'

 L. 275      1206  LOAD_GLOBAL              print
             1208  LOAD_STR                 'shlex: raw token=EOF'
             1210  CALL_FUNCTION_1       1  '1 positional argument'
             1212  POP_TOP          
           1214_0  COME_FROM          1204  '1204'
           1214_1  COME_FROM          1178  '1178'

 L. 276      1214  LOAD_FAST                'result'
             1216  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 1128

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
            break
        else:
            print('Token: ' + repr(tt))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        _print_tokens(shlex())
    else:
        fn = sys.argv[1]
        with open(fn) as f:
            _print_tokens(shlex(f, fn))