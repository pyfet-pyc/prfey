# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\dns\tokenizer.py
"""Tokenize DNS master file format"""
from io import StringIO
import sys, dns.exception, dns.name, dns.ttl
from ._compat import long, text_type, binary_type
_DELIMITERS = {' ':True, 
 '\t':True, 
 '\n':True, 
 ';':True, 
 '(':True, 
 ')':True, 
 '"':True}
_QUOTING_DELIMITERS = {'"': True}
EOF = 0
EOL = 1
WHITESPACE = 2
IDENTIFIER = 3
QUOTED_STRING = 4
COMMENT = 5
DELIMITER = 6

class UngetBufferFull(dns.exception.DNSException):
    __doc__ = 'An attempt was made to unget a token when the unget buffer was full.'


class Token(object):
    __doc__ = 'A DNS master file format token.\n\n    ttype: The token type\n    value: The token value\n    has_escape: Does the token value contain escapes?\n    '

    def __init__(self, ttype, value='', has_escape=False):
        """Initialize a token instance."""
        self.ttype = ttype
        self.value = value
        self.has_escape = has_escape

    def is_eof(self):
        return self.ttype == EOF

    def is_eol(self):
        return self.ttype == EOL

    def is_whitespace(self):
        return self.ttype == WHITESPACE

    def is_identifier(self):
        return self.ttype == IDENTIFIER

    def is_quoted_string(self):
        return self.ttype == QUOTED_STRING

    def is_comment(self):
        return self.ttype == COMMENT

    def is_delimiter(self):
        return self.ttype == DELIMITER

    def is_eol_or_eof(self):
        return self.ttype == EOL or self.ttype == EOF

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.ttype == other.ttype and self.value == other.value

    def __ne__(self, other):
        if not isinstance(other, Token):
            return True
        return self.ttype != other.ttype or self.value != other.value

    def __str__(self):
        return '%d "%s"' % (self.ttype, self.value)

    def unescape(self):
        if not self.has_escape:
            return self
        else:
            unescaped = ''
            l = len(self.value)
            i = 0
            while True:
                if i < l:
                    c = self.value[i]
                    i += 1
                    if c == '\\':
                        if i >= l:
                            raise dns.exception.UnexpectedEnd
                        c = self.value[i]
                        i += 1
                        if c.isdigit():
                            if i >= l:
                                raise dns.exception.UnexpectedEnd
                            else:
                                c2 = self.value[i]
                                i += 1
                                if i >= l:
                                    raise dns.exception.UnexpectedEnd
                                c3 = self.value[i]
                                i += 1
                                raise c2.isdigit() and c3.isdigit() or dns.exception.SyntaxError
                            c = chr(int(c) * 100 + int(c2) * 10 + int(c3))
                    unescaped += c

        return Token(self.ttype, unescaped)

    def __len__(self):
        return 2

    def __iter__(self):
        return iter((self.ttype, self.value))

    def __getitem__(self, i):
        if i == 0:
            return self.ttype
        if i == 1:
            return self.value
        raise IndexError


class Tokenizer(object):
    __doc__ = "A DNS master file format tokenizer.\n\n    A token object is basically a (type, value) tuple.  The valid\n    types are EOF, EOL, WHITESPACE, IDENTIFIER, QUOTED_STRING,\n    COMMENT, and DELIMITER.\n\n    file: The file to tokenize\n\n    ungotten_char: The most recently ungotten character, or None.\n\n    ungotten_token: The most recently ungotten token, or None.\n\n    multiline: The current multiline level.  This value is increased\n    by one every time a '(' delimiter is read, and decreased by one every time\n    a ')' delimiter is read.\n\n    quoting: This variable is true if the tokenizer is currently\n    reading a quoted string.\n\n    eof: This variable is true if the tokenizer has encountered EOF.\n\n    delimiters: The current delimiter dictionary.\n\n    line_number: The current line number\n\n    filename: A filename that will be returned by the where() method.\n    "

    def __init__(self, f=sys.stdin, filename=None):
        """Initialize a tokenizer instance.

        f: The file to tokenize.  The default is sys.stdin.
        This parameter may also be a string, in which case the tokenizer
        will take its input from the contents of the string.

        filename: the name of the filename that the where() method
        will return.
        """
        if isinstance(f, text_type):
            f = StringIO(f)
            if filename is None:
                filename = '<string>'
        elif isinstance(f, binary_type):
            f = StringIO(f.decode())
            if filename is None:
                filename = '<string>'
        elif filename is None:
            if f is sys.stdin:
                filename = '<stdin>'
            else:
                filename = '<file>'
        self.file = f
        self.ungotten_char = None
        self.ungotten_token = None
        self.multiline = 0
        self.quoting = False
        self.eof = False
        self.delimiters = _DELIMITERS
        self.line_number = 1
        self.filename = filename

    def _get_char(self):
        """Read a character from input.
        """
        if self.ungotten_char is None:
            if self.eof:
                c = ''
            else:
                c = self.file.read(1)
                if c == '':
                    self.eof = True
                elif c == '\n':
                    self.line_number += 1
        else:
            c = self.ungotten_char
            self.ungotten_char = None
        return c

    def where(self):
        """Return the current location in the input.

        Returns a (string, int) tuple.  The first item is the filename of
        the input, the second is the current line number.
        """
        return (
         self.filename, self.line_number)

    def _unget_char(self, c):
        """Unget a character.

        The unget buffer for characters is only one character large; it is
        an error to try to unget a character when the unget buffer is not
        empty.

        c: the character to unget
        raises UngetBufferFull: there is already an ungotten char
        """
        if self.ungotten_char is not None:
            raise UngetBufferFull
        self.ungotten_char = c

    def skip_whitespace(self):
        """Consume input until a non-whitespace character is encountered.

        The non-whitespace character is then ungotten, and the number of
        whitespace characters consumed is returned.

        If the tokenizer is in multiline mode, then newlines are whitespace.

        Returns the number of characters skipped.
        """
        skipped = 0
        while True:
            c = self._get_char()
            if c != ' ':
                if c != '\t':
                    c != '\n' or self.multiline or self._unget_char(c)
                    return skipped
            skipped += 1

    def get--- This code section failed: ---

 L. 294         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ungotten_token
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    62  'to 62'

 L. 295        10  LOAD_FAST                'self'
               12  LOAD_ATTR                ungotten_token
               14  STORE_FAST               'token'

 L. 296        16  LOAD_CONST               None
               18  LOAD_FAST                'self'
               20  STORE_ATTR               ungotten_token

 L. 297        22  LOAD_FAST                'token'
               24  LOAD_METHOD              is_whitespace
               26  CALL_METHOD_0         0  ''
               28  POP_JUMP_IF_FALSE    40  'to 40'

 L. 298        30  LOAD_FAST                'want_leading'
               32  POP_JUMP_IF_FALSE    62  'to 62'

 L. 299        34  LOAD_FAST                'token'
               36  RETURN_VALUE     
               38  JUMP_FORWARD         62  'to 62'
             40_0  COME_FROM            28  '28'

 L. 300        40  LOAD_FAST                'token'
               42  LOAD_METHOD              is_comment
               44  CALL_METHOD_0         0  ''
               46  POP_JUMP_IF_FALSE    58  'to 58'

 L. 301        48  LOAD_FAST                'want_comment'
               50  POP_JUMP_IF_FALSE    62  'to 62'

 L. 302        52  LOAD_FAST                'token'
               54  RETURN_VALUE     
               56  JUMP_FORWARD         62  'to 62'
             58_0  COME_FROM            46  '46'

 L. 304        58  LOAD_FAST                'token'
               60  RETURN_VALUE     
             62_0  COME_FROM            56  '56'
             62_1  COME_FROM            50  '50'
             62_2  COME_FROM            38  '38'
             62_3  COME_FROM            32  '32'
             62_4  COME_FROM             8  '8'

 L. 305        62  LOAD_FAST                'self'
               64  LOAD_METHOD              skip_whitespace
               66  CALL_METHOD_0         0  ''
               68  STORE_FAST               'skipped'

 L. 306        70  LOAD_FAST                'want_leading'
               72  POP_JUMP_IF_FALSE    92  'to 92'
               74  LOAD_FAST                'skipped'
               76  LOAD_CONST               0
               78  COMPARE_OP               >
               80  POP_JUMP_IF_FALSE    92  'to 92'

 L. 307        82  LOAD_GLOBAL              Token
               84  LOAD_GLOBAL              WHITESPACE
               86  LOAD_STR                 ' '
               88  CALL_FUNCTION_2       2  ''
               90  RETURN_VALUE     
             92_0  COME_FROM            80  '80'
             92_1  COME_FROM            72  '72'

 L. 308        92  LOAD_STR                 ''
               94  STORE_FAST               'token'

 L. 309        96  LOAD_GLOBAL              IDENTIFIER
               98  STORE_FAST               'ttype'

 L. 310       100  LOAD_CONST               False
              102  STORE_FAST               'has_escape'

 L. 312       104  LOAD_FAST                'self'
              106  LOAD_METHOD              _get_char
              108  CALL_METHOD_0         0  ''
              110  STORE_FAST               'c'

 L. 313       112  LOAD_FAST                'c'
              114  LOAD_STR                 ''
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_TRUE    132  'to 132'
              120  LOAD_FAST                'c'
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                delimiters
              126  COMPARE_OP               in
          128_130  POP_JUMP_IF_FALSE   526  'to 526'
            132_0  COME_FROM           118  '118'

 L. 314       132  LOAD_FAST                'c'
              134  LOAD_STR                 ''
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   154  'to 154'
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                quoting
              144  POP_JUMP_IF_FALSE   154  'to 154'

 L. 315       146  LOAD_GLOBAL              dns
              148  LOAD_ATTR                exception
              150  LOAD_ATTR                UnexpectedEnd
              152  RAISE_VARARGS_1       1  'exception instance'
            154_0  COME_FROM           144  '144'
            154_1  COME_FROM           138  '138'

 L. 316       154  LOAD_FAST                'token'
              156  LOAD_STR                 ''
              158  COMPARE_OP               ==
          160_162  POP_JUMP_IF_FALSE   510  'to 510'
              164  LOAD_FAST                'ttype'
              166  LOAD_GLOBAL              QUOTED_STRING
              168  COMPARE_OP               !=
          170_172  POP_JUMP_IF_FALSE   510  'to 510'

 L. 317       174  LOAD_FAST                'c'
              176  LOAD_STR                 '('
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   210  'to 210'

 L. 318       182  LOAD_FAST                'self'
              184  DUP_TOP          
              186  LOAD_ATTR                multiline
              188  LOAD_CONST               1
              190  INPLACE_ADD      
              192  ROT_TWO          
              194  STORE_ATTR               multiline

 L. 319       196  LOAD_FAST                'self'
              198  LOAD_METHOD              skip_whitespace
              200  CALL_METHOD_0         0  ''
              202  POP_TOP          

 L. 320       204  JUMP_BACK           104  'to 104'
          206_208  JUMP_ABSOLUTE       520  'to 520'
            210_0  COME_FROM           180  '180'

 L. 321       210  LOAD_FAST                'c'
              212  LOAD_STR                 ')'
              214  COMPARE_OP               ==
          216_218  POP_JUMP_IF_FALSE   264  'to 264'

 L. 322       220  LOAD_FAST                'self'
              222  LOAD_ATTR                multiline
              224  LOAD_CONST               0
              226  COMPARE_OP               <=
              228  POP_JUMP_IF_FALSE   238  'to 238'

 L. 323       230  LOAD_GLOBAL              dns
              232  LOAD_ATTR                exception
              234  LOAD_ATTR                SyntaxError
              236  RAISE_VARARGS_1       1  'exception instance'
            238_0  COME_FROM           228  '228'

 L. 324       238  LOAD_FAST                'self'
              240  DUP_TOP          
              242  LOAD_ATTR                multiline
              244  LOAD_CONST               1
              246  INPLACE_SUBTRACT 
              248  ROT_TWO          
              250  STORE_ATTR               multiline

 L. 325       252  LOAD_FAST                'self'
              254  LOAD_METHOD              skip_whitespace
              256  CALL_METHOD_0         0  ''
              258  POP_TOP          

 L. 326       260  JUMP_BACK           104  'to 104'
              262  JUMP_FORWARD        508  'to 508'
            264_0  COME_FROM           216  '216'

 L. 327       264  LOAD_FAST                'c'
              266  LOAD_STR                 '"'
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   326  'to 326'

 L. 328       274  LOAD_FAST                'self'
              276  LOAD_ATTR                quoting
          278_280  POP_JUMP_IF_TRUE    302  'to 302'

 L. 329       282  LOAD_CONST               True
              284  LOAD_FAST                'self'
              286  STORE_ATTR               quoting

 L. 330       288  LOAD_GLOBAL              _QUOTING_DELIMITERS
              290  LOAD_FAST                'self'
              292  STORE_ATTR               delimiters

 L. 331       294  LOAD_GLOBAL              QUOTED_STRING
              296  STORE_FAST               'ttype'

 L. 332       298  JUMP_BACK           104  'to 104'
              300  JUMP_FORWARD        324  'to 324'
            302_0  COME_FROM           278  '278'

 L. 334       302  LOAD_CONST               False
              304  LOAD_FAST                'self'
              306  STORE_ATTR               quoting

 L. 335       308  LOAD_GLOBAL              _DELIMITERS
              310  LOAD_FAST                'self'
              312  STORE_ATTR               delimiters

 L. 336       314  LOAD_FAST                'self'
              316  LOAD_METHOD              skip_whitespace
              318  CALL_METHOD_0         0  ''
              320  POP_TOP          

 L. 337       322  JUMP_BACK           104  'to 104'
            324_0  COME_FROM           300  '300'
              324  JUMP_FORWARD        508  'to 508'
            326_0  COME_FROM           270  '270'

 L. 338       326  LOAD_FAST                'c'
              328  LOAD_STR                 '\n'
              330  COMPARE_OP               ==
          332_334  POP_JUMP_IF_FALSE   346  'to 346'

 L. 339       336  LOAD_GLOBAL              Token
              338  LOAD_GLOBAL              EOL
              340  LOAD_STR                 '\n'
              342  CALL_FUNCTION_2       2  ''
              344  RETURN_VALUE     
            346_0  COME_FROM           332  '332'

 L. 340       346  LOAD_FAST                'c'
              348  LOAD_STR                 ';'
              350  COMPARE_OP               ==
          352_354  POP_JUMP_IF_FALSE   500  'to 500'

 L. 342       356  LOAD_FAST                'self'
              358  LOAD_METHOD              _get_char
              360  CALL_METHOD_0         0  ''
              362  STORE_FAST               'c'

 L. 343       364  LOAD_FAST                'c'
              366  LOAD_STR                 '\n'
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_TRUE    400  'to 400'
              374  LOAD_FAST                'c'
              376  LOAD_STR                 ''
              378  COMPARE_OP               ==
          380_382  POP_JUMP_IF_FALSE   388  'to 388'

 L. 344   384_386  BREAK_LOOP          400  'to 400'
            388_0  COME_FROM           380  '380'

 L. 345       388  LOAD_FAST                'token'
              390  LOAD_FAST                'c'
              392  INPLACE_ADD      
              394  STORE_FAST               'token'
          396_398  JUMP_BACK           356  'to 356'
            400_0  COME_FROM           370  '370'

 L. 346       400  LOAD_FAST                'want_comment'
          402_404  POP_JUMP_IF_FALSE   426  'to 426'

 L. 347       406  LOAD_FAST                'self'
              408  LOAD_METHOD              _unget_char
              410  LOAD_FAST                'c'
              412  CALL_METHOD_1         1  ''
              414  POP_TOP          

 L. 348       416  LOAD_GLOBAL              Token
              418  LOAD_GLOBAL              COMMENT
              420  LOAD_FAST                'token'
              422  CALL_FUNCTION_2       2  ''
              424  RETURN_VALUE     
            426_0  COME_FROM           402  '402'

 L. 349       426  LOAD_FAST                'c'
              428  LOAD_STR                 ''
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_FALSE   464  'to 464'

 L. 350       436  LOAD_FAST                'self'
              438  LOAD_ATTR                multiline
          440_442  POP_JUMP_IF_FALSE   456  'to 456'

 L. 351       444  LOAD_GLOBAL              dns
              446  LOAD_ATTR                exception
              448  LOAD_METHOD              SyntaxError

 L. 352       450  LOAD_STR                 'unbalanced parentheses'

 L. 351       452  CALL_METHOD_1         1  ''
              454  RAISE_VARARGS_1       1  'exception instance'
            456_0  COME_FROM           440  '440'

 L. 353       456  LOAD_GLOBAL              Token
              458  LOAD_GLOBAL              EOF
              460  CALL_FUNCTION_1       1  ''
              462  RETURN_VALUE     
            464_0  COME_FROM           432  '432'

 L. 354       464  LOAD_FAST                'self'
              466  LOAD_ATTR                multiline
          468_470  POP_JUMP_IF_FALSE   488  'to 488'

 L. 355       472  LOAD_FAST                'self'
              474  LOAD_METHOD              skip_whitespace
              476  CALL_METHOD_0         0  ''
              478  POP_TOP          

 L. 356       480  LOAD_STR                 ''
              482  STORE_FAST               'token'

 L. 357       484  JUMP_BACK           104  'to 104'
              486  JUMP_FORWARD        498  'to 498'
            488_0  COME_FROM           468  '468'

 L. 359       488  LOAD_GLOBAL              Token
              490  LOAD_GLOBAL              EOL
              492  LOAD_STR                 '\n'
              494  CALL_FUNCTION_2       2  ''
              496  RETURN_VALUE     
            498_0  COME_FROM           486  '486'
              498  JUMP_FORWARD        508  'to 508'
            500_0  COME_FROM           352  '352'

 L. 364       500  LOAD_FAST                'c'
              502  STORE_FAST               'token'

 L. 365       504  LOAD_GLOBAL              DELIMITER
              506  STORE_FAST               'ttype'
            508_0  COME_FROM           498  '498'
            508_1  COME_FROM           324  '324'
            508_2  COME_FROM           262  '262'
              508  BREAK_LOOP          790  'to 790'
            510_0  COME_FROM           170  '170'
            510_1  COME_FROM           160  '160'

 L. 367       510  LOAD_FAST                'self'
              512  LOAD_METHOD              _unget_char
              514  LOAD_FAST                'c'
              516  CALL_METHOD_1         1  ''
              518  POP_TOP          

 L. 368   520_522  BREAK_LOOP          790  'to 790'
              524  JUMP_FORWARD        780  'to 780'
            526_0  COME_FROM           128  '128'

 L. 369       526  LOAD_FAST                'self'
              528  LOAD_ATTR                quoting
          530_532  POP_JUMP_IF_FALSE   722  'to 722'

 L. 370       534  LOAD_FAST                'c'
              536  LOAD_STR                 '\\'
              538  COMPARE_OP               ==
          540_542  POP_JUMP_IF_FALSE   698  'to 698'

 L. 371       544  LOAD_FAST                'self'
              546  LOAD_METHOD              _get_char
              548  CALL_METHOD_0         0  ''
              550  STORE_FAST               'c'

 L. 372       552  LOAD_FAST                'c'
              554  LOAD_STR                 ''
              556  COMPARE_OP               ==
          558_560  POP_JUMP_IF_FALSE   570  'to 570'

 L. 373       562  LOAD_GLOBAL              dns
              564  LOAD_ATTR                exception
              566  LOAD_ATTR                UnexpectedEnd
              568  RAISE_VARARGS_1       1  'exception instance'
            570_0  COME_FROM           558  '558'

 L. 374       570  LOAD_FAST                'c'
              572  LOAD_METHOD              isdigit
              574  CALL_METHOD_0         0  ''
          576_578  POP_JUMP_IF_FALSE   720  'to 720'

 L. 375       580  LOAD_FAST                'self'
              582  LOAD_METHOD              _get_char
              584  CALL_METHOD_0         0  ''
              586  STORE_FAST               'c2'

 L. 376       588  LOAD_FAST                'c2'
              590  LOAD_STR                 ''
              592  COMPARE_OP               ==
          594_596  POP_JUMP_IF_FALSE   606  'to 606'

 L. 377       598  LOAD_GLOBAL              dns
              600  LOAD_ATTR                exception
              602  LOAD_ATTR                UnexpectedEnd
              604  RAISE_VARARGS_1       1  'exception instance'
            606_0  COME_FROM           594  '594'

 L. 378       606  LOAD_FAST                'self'
              608  LOAD_METHOD              _get_char
              610  CALL_METHOD_0         0  ''
              612  STORE_FAST               'c3'

 L. 379       614  LOAD_FAST                'c'
              616  LOAD_STR                 ''
              618  COMPARE_OP               ==
          620_622  POP_JUMP_IF_FALSE   632  'to 632'

 L. 380       624  LOAD_GLOBAL              dns
              626  LOAD_ATTR                exception
              628  LOAD_ATTR                UnexpectedEnd
              630  RAISE_VARARGS_1       1  'exception instance'
            632_0  COME_FROM           620  '620'

 L. 381       632  LOAD_FAST                'c2'
              634  LOAD_METHOD              isdigit
              636  CALL_METHOD_0         0  ''
          638_640  POP_JUMP_IF_FALSE   652  'to 652'
              642  LOAD_FAST                'c3'
              644  LOAD_METHOD              isdigit
              646  CALL_METHOD_0         0  ''
          648_650  POP_JUMP_IF_TRUE    660  'to 660'
            652_0  COME_FROM           638  '638'

 L. 382       652  LOAD_GLOBAL              dns
              654  LOAD_ATTR                exception
              656  LOAD_ATTR                SyntaxError
              658  RAISE_VARARGS_1       1  'exception instance'
            660_0  COME_FROM           648  '648'

 L. 383       660  LOAD_GLOBAL              chr
              662  LOAD_GLOBAL              int
              664  LOAD_FAST                'c'
              666  CALL_FUNCTION_1       1  ''
              668  LOAD_CONST               100
              670  BINARY_MULTIPLY  
              672  LOAD_GLOBAL              int
              674  LOAD_FAST                'c2'
              676  CALL_FUNCTION_1       1  ''
              678  LOAD_CONST               10
              680  BINARY_MULTIPLY  
              682  BINARY_ADD       
              684  LOAD_GLOBAL              int
              686  LOAD_FAST                'c3'
              688  CALL_FUNCTION_1       1  ''
              690  BINARY_ADD       
              692  CALL_FUNCTION_1       1  ''
              694  STORE_FAST               'c'
              696  JUMP_FORWARD        720  'to 720'
            698_0  COME_FROM           540  '540'

 L. 384       698  LOAD_FAST                'c'
              700  LOAD_STR                 '\n'
              702  COMPARE_OP               ==
          704_706  POP_JUMP_IF_FALSE   780  'to 780'

 L. 385       708  LOAD_GLOBAL              dns
              710  LOAD_ATTR                exception
              712  LOAD_METHOD              SyntaxError
              714  LOAD_STR                 'newline in quoted string'
              716  CALL_METHOD_1         1  ''
              718  RAISE_VARARGS_1       1  'exception instance'
            720_0  COME_FROM           696  '696'
            720_1  COME_FROM           576  '576'
              720  JUMP_FORWARD        780  'to 780'
            722_0  COME_FROM           530  '530'

 L. 386       722  LOAD_FAST                'c'
              724  LOAD_STR                 '\\'
              726  COMPARE_OP               ==
          728_730  POP_JUMP_IF_FALSE   780  'to 780'

 L. 391       732  LOAD_FAST                'token'
              734  LOAD_FAST                'c'
              736  INPLACE_ADD      
              738  STORE_FAST               'token'

 L. 392       740  LOAD_CONST               True
              742  STORE_FAST               'has_escape'

 L. 393       744  LOAD_FAST                'self'
              746  LOAD_METHOD              _get_char
              748  CALL_METHOD_0         0  ''
              750  STORE_FAST               'c'

 L. 394       752  LOAD_FAST                'c'
              754  LOAD_STR                 ''
              756  COMPARE_OP               ==
          758_760  POP_JUMP_IF_TRUE    772  'to 772'
              762  LOAD_FAST                'c'
              764  LOAD_STR                 '\n'
              766  COMPARE_OP               ==
          768_770  POP_JUMP_IF_FALSE   780  'to 780'
            772_0  COME_FROM           758  '758'

 L. 395       772  LOAD_GLOBAL              dns
              774  LOAD_ATTR                exception
              776  LOAD_ATTR                UnexpectedEnd
              778  RAISE_VARARGS_1       1  'exception instance'
            780_0  COME_FROM           768  '768'
            780_1  COME_FROM           728  '728'
            780_2  COME_FROM           720  '720'
            780_3  COME_FROM           704  '704'
            780_4  COME_FROM           524  '524'

 L. 396       780  LOAD_FAST                'token'
              782  LOAD_FAST                'c'
              784  INPLACE_ADD      
              786  STORE_FAST               'token'
              788  JUMP_BACK           104  'to 104'

 L. 397       790  LOAD_FAST                'token'
              792  LOAD_STR                 ''
              794  COMPARE_OP               ==
          796_798  POP_JUMP_IF_FALSE   834  'to 834'
              800  LOAD_FAST                'ttype'
              802  LOAD_GLOBAL              QUOTED_STRING
              804  COMPARE_OP               !=
          806_808  POP_JUMP_IF_FALSE   834  'to 834'

 L. 398       810  LOAD_FAST                'self'
              812  LOAD_ATTR                multiline
          814_816  POP_JUMP_IF_FALSE   830  'to 830'

 L. 399       818  LOAD_GLOBAL              dns
              820  LOAD_ATTR                exception
              822  LOAD_METHOD              SyntaxError
              824  LOAD_STR                 'unbalanced parentheses'
              826  CALL_METHOD_1         1  ''
              828  RAISE_VARARGS_1       1  'exception instance'
            830_0  COME_FROM           814  '814'

 L. 400       830  LOAD_GLOBAL              EOF
              832  STORE_FAST               'ttype'
            834_0  COME_FROM           806  '806'
            834_1  COME_FROM           796  '796'

 L. 401       834  LOAD_GLOBAL              Token
              836  LOAD_FAST                'ttype'
              838  LOAD_FAST                'token'
              840  LOAD_FAST                'has_escape'
              842  CALL_FUNCTION_3       3  ''
              844  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 262

    def unget(self, token):
        """Unget a token.

        The unget buffer for tokens is only one token large; it is
        an error to try to unget a token when the unget buffer is not
        empty.

        token: the token to unget

        Raises UngetBufferFull: there is already an ungotten token
        """
        if self.ungotten_token is not None:
            raise UngetBufferFull
        self.ungotten_token = token

    def next(self):
        """Return the next item in an iteration.

        Returns a Token.
        """
        token = self.get()
        if token.is_eof():
            raise StopIteration
        return token

    __next__ = next

    def __iter__(self):
        return self

    def get_int(self, base=10):
        """Read the next token and interpret it as an integer.

        Raises dns.exception.SyntaxError if not an integer.

        Returns an int.
        """
        token = self.get().unescape()
        if not token.is_identifier():
            raise dns.exception.SyntaxError('expecting an identifier')
        if not token.value.isdigit():
            raise dns.exception.SyntaxError('expecting an integer')
        return int(token.value, base)

    def get_uint8(self):
        """Read the next token and interpret it as an 8-bit unsigned
        integer.

        Raises dns.exception.SyntaxError if not an 8-bit unsigned integer.

        Returns an int.
        """
        value = self.get_int()
        if value < 0 or value > 255:
            raise dns.exception.SyntaxError('%d is not an unsigned 8-bit integer' % value)
        return value

    def get_uint16(self, base=10):
        """Read the next token and interpret it as a 16-bit unsigned
        integer.

        Raises dns.exception.SyntaxError if not a 16-bit unsigned integer.

        Returns an int.
        """
        value = self.get_int(base=base)
        if value < 0 or value > 65535:
            if base == 8:
                raise dns.exception.SyntaxError('%o is not an octal unsigned 16-bit integer' % value)
        else:
            raise dns.exception.SyntaxError('%d is not an unsigned 16-bit integer' % value)
        return value

    def get_uint32(self):
        """Read the next token and interpret it as a 32-bit unsigned
        integer.

        Raises dns.exception.SyntaxError if not a 32-bit unsigned integer.

        Returns an int.
        """
        token = self.get().unescape()
        if not token.is_identifier():
            raise dns.exception.SyntaxError('expecting an identifier')
        if not token.value.isdigit():
            raise dns.exception.SyntaxError('expecting an integer')
        value = long(token.value)
        if value < 0 or value > long(4294967296):
            raise dns.exception.SyntaxError('%d is not an unsigned 32-bit integer' % value)
        return value

    def get_string(self, origin=None):
        """Read the next token and interpret it as a string.

        Raises dns.exception.SyntaxError if not a string.

        Returns a string.
        """
        token = self.get().unescape()
        if not token.is_identifier():
            if not token.is_quoted_string():
                raise dns.exception.SyntaxError('expecting a string')
        return token.value

    def get_identifier(self, origin=None):
        """Read the next token, which should be an identifier.

        Raises dns.exception.SyntaxError if not an identifier.

        Returns a string.
        """
        token = self.get().unescape()
        if not token.is_identifier():
            raise dns.exception.SyntaxError('expecting an identifier')
        return token.value

    def get_name(self, origin=None):
        """Read the next token and interpret it as a DNS name.

        Raises dns.exception.SyntaxError if not a name.

        Returns a dns.name.Name.
        """
        token = self.get()
        if not token.is_identifier():
            raise dns.exception.SyntaxError('expecting an identifier')
        return dns.name.from_text(token.value, origin)

    def get_eol(self):
        """Read the next token and raise an exception if it isn't EOL or
        EOF.

        Returns a string.
        """
        token = self.get()
        if not token.is_eol_or_eof():
            raise dns.exception.SyntaxError('expected EOL or EOF, got %d "%s"' % (token.ttype,
             token.value))
        return token.value

    def get_ttl(self):
        """Read the next token and interpret it as a DNS TTL.

        Raises dns.exception.SyntaxError or dns.ttl.BadTTL if not an
        identifier or badly formed.

        Returns an int.
        """
        token = self.get().unescape()
        if not token.is_identifier():
            raise dns.exception.SyntaxError('expecting an identifier')
        return dns.ttl.from_text(token.value)