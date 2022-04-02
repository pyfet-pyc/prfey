# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: lib2to3\pgen2\tokenize.py
"""Tokenization help for Python programs.

generate_tokens(readline) is a generator that breaks a stream of
text into Python tokens.  It accepts a readline-like method which is called
repeatedly to get the next line of input (or "" for EOF).  It generates
5-tuples with these members:

    the token type (see token.py)
    the token (a string)
    the starting (row, column) indices of the token (a 2-tuple of ints)
    the ending (row, column) indices of the token (a 2-tuple of ints)
    the original line (string)

It is designed to match the working of the Python tokenizer exactly, except
that it produces COMMENT tokens for comments and gives type OP for all
operators

Older entry points
    tokenize_loop(readline, tokeneater)
    tokenize(readline, tokeneater=printtoken)
are the same, except instead of generating tokens, tokeneater is a callback
function to which the 5 fields described above are passed as 5 arguments,
each time a new token is found."""
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__credits__ = 'GvR, ESR, Tim Peters, Thomas Wouters, Fred Drake, Skip Montanaro'
import string, re
from codecs import BOM_UTF8, lookup
from lib2to3.pgen2.token import *
from . import token
__all__ = [x for x in dir(token) if x[0] != '_'] + ['tokenize',
 'generate_tokens', 'untokenize']
del token
try:
    bytes
except NameError:
    bytes = str
else:

    def group(*choices):
        return '(' + '|'.join(choices) + ')'


    def any(*choices):
        return group(*choices) + '*'


    def maybe(*choices):
        return group(*choices) + '?'


    def _combinations(*l):
        return set((x + y for x in l for y in l + ('', )))


    Whitespace = '[ \\f\\t]*'
    Comment = '#[^\\r\\n]*'
    Ignore = Whitespace + any('\\\\\\r?\\n' + Whitespace) + maybe(Comment)
    Name = '\\w+'
    Binnumber = '0[bB]_?[01]+(?:_[01]+)*'
    Hexnumber = '0[xX]_?[\\da-fA-F]+(?:_[\\da-fA-F]+)*[lL]?'
    Octnumber = '0[oO]?_?[0-7]+(?:_[0-7]+)*[lL]?'
    Decnumber = group('[1-9]\\d*(?:_\\d+)*[lL]?', '0[lL]?')
    Intnumber = group(Binnumber, Hexnumber, Octnumber, Decnumber)
    Exponent = '[eE][-+]?\\d+(?:_\\d+)*'
    Pointfloat = group('\\d+(?:_\\d+)*\\.(?:\\d+(?:_\\d+)*)?', '\\.\\d+(?:_\\d+)*') + maybe(Exponent)
    Expfloat = '\\d+(?:_\\d+)*' + Exponent
    Floatnumber = group(Pointfloat, Expfloat)
    Imagnumber = group('\\d+(?:_\\d+)*[jJ]', Floatnumber + '[jJ]')
    Number = group(Imagnumber, Floatnumber, Intnumber)
    Single = "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'"
    Double = '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'
    Single3 = "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''"
    Double3 = '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""'
    _litprefix = '(?:[uUrRbBfF]|[rR][fFbB]|[fFbBuU][rR])?'
    Triple = group(_litprefix + "'''", _litprefix + '"""')
    String = group(_litprefix + "'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*'", _litprefix + '"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*"')
    Operator = group('\\*\\*=?', '>>=?', '<<=?', '<>', '!=', '//=?', '->', '[+\\-*/%&@|^=<>]=?', '~')
    Bracket = '[][(){}]'
    Special = group('\\r?\\n', ':=', '[:;.,`@]')
    Funny = group(Operator, Bracket, Special)
    PlainToken = group(Number, Funny, String, Name)
    Token = Ignore + PlainToken
    ContStr = group(_litprefix + "'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*" + group("'", '\\\\\\r?\\n'), _litprefix + '"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*' + group('"', '\\\\\\r?\\n'))
    PseudoExtras = group('\\\\\\r?\\n', Comment, Triple)
    PseudoToken = Whitespace + group(PseudoExtras, Number, Funny, ContStr, Name)
    tokenprog, pseudoprog, single3prog, double3prog = map(re.compile, (Token, PseudoToken, Single3, Double3))
    _strprefixes = _combinations('r', 'R', 'f', 'F') | _combinations('r', 'R', 'b', 'B') | {
     'u', 'U', 'ur', 'uR', 'Ur', 'UR'}
    endprogs = {**{"'":re.compile(Single), 
     '"':re.compile(Double),  "'''":single3prog, 
     '"""':double3prog}, **{single3prog:f"{prefix}'''" for prefix in _strprefixes}, **{double3prog:f'{prefix}"""' for prefix in _strprefixes}, **{None:prefix for prefix in _strprefixes}}
    triple_quoted = {
     "'''", '"""'} | {f"{prefix}'''" for prefix in _strprefixes} | {f'{prefix}"""' for prefix in _strprefixes}
    single_quoted = {
     "'", '"'} | {f"{prefix}'" for prefix in _strprefixes} | {f'{prefix}"' for prefix in _strprefixes}
    tabsize = 8

    class TokenError(Exception):
        pass


    class StopTokenizing(Exception):
        pass


    def printtoken(type, token, xxx_todo_changeme, xxx_todo_changeme1, line):
        srow, scol = xxx_todo_changeme
        erow, ecol = xxx_todo_changeme1
        print('%d,%d-%d,%d:\t%s\t%s' % (
         srow, scol, erow, ecol, tok_name[type], repr(token)))


    def tokenize(readline, tokeneater=printtoken):
        """
    The tokenize() function accepts two parameters: one representing the
    input stream, and one providing an output mechanism for tokenize().

    The first parameter, readline, must be a callable object which provides
    the same interface as the readline() method of built-in file objects.
    Each call to the function should return one line of input as a string.

    The second parameter, tokeneater, must also be a callable object. It is
    called once for each token, with five arguments, corresponding to the
    tuples generated by generate_tokens().
    """
        try:
            tokenize_loop(readline, tokeneater)
        except StopTokenizing:
            pass


    def tokenize_loop(readline, tokeneater):
        for token_info in generate_tokens(readline):
            tokeneater(*token_info)


    class Untokenizer:

        def __init__(self):
            self.tokens = []
            self.prev_row = 1
            self.prev_col = 0

        def add_whitespace(self, start):
            row, col = start
            assert row <= self.prev_row
            col_offset = col - self.prev_col
            if col_offset:
                self.tokens.append(' ' * col_offset)

        def untokenize(self, iterable):
            for t in iterable:
                if len(t) == 2:
                    self.compat(t, iterable)
                    break
                tok_type, token, start, end, line = t
                self.add_whitespace(start)
                self.tokens.append(token)
                self.prev_row, self.prev_col = end
                if tok_type in (NEWLINE, NL):
                    self.prev_row += 1
                    self.prev_col = 0
                return ''.join(self.tokens)

        def compat--- This code section failed: ---

 L. 200         0  LOAD_CONST               False
                2  STORE_FAST               'startline'

 L. 201         4  BUILD_LIST_0          0 
                6  STORE_FAST               'indents'

 L. 202         8  LOAD_FAST                'self'
               10  LOAD_ATTR                tokens
               12  LOAD_ATTR                append
               14  STORE_FAST               'toks_append'

 L. 203        16  LOAD_FAST                'token'
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'toknum'
               22  STORE_FAST               'tokval'

 L. 204        24  LOAD_FAST                'toknum'
               26  LOAD_GLOBAL              NAME
               28  LOAD_GLOBAL              NUMBER
               30  BUILD_TUPLE_2         2 
               32  COMPARE_OP               in
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 205        36  LOAD_FAST                'tokval'
               38  LOAD_STR                 ' '
               40  INPLACE_ADD      
               42  STORE_FAST               'tokval'
             44_0  COME_FROM            34  '34'

 L. 206        44  LOAD_FAST                'toknum'
               46  LOAD_GLOBAL              NEWLINE
               48  LOAD_GLOBAL              NL
               50  BUILD_TUPLE_2         2 
               52  COMPARE_OP               in
               54  POP_JUMP_IF_FALSE    60  'to 60'

 L. 207        56  LOAD_CONST               True
               58  STORE_FAST               'startline'
             60_0  COME_FROM            54  '54'

 L. 208        60  LOAD_FAST                'iterable'
               62  GET_ITER         
               64  FOR_ITER            202  'to 202'
               66  STORE_FAST               'tok'

 L. 209        68  LOAD_FAST                'tok'
               70  LOAD_CONST               None
               72  LOAD_CONST               2
               74  BUILD_SLICE_2         2 
               76  BINARY_SUBSCR    
               78  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST               'toknum'
               82  STORE_FAST               'tokval'

 L. 211        84  LOAD_FAST                'toknum'
               86  LOAD_GLOBAL              NAME
               88  LOAD_GLOBAL              NUMBER
               90  LOAD_GLOBAL              ASYNC
               92  LOAD_GLOBAL              AWAIT
               94  BUILD_TUPLE_4         4 
               96  COMPARE_OP               in
               98  POP_JUMP_IF_FALSE   108  'to 108'

 L. 212       100  LOAD_FAST                'tokval'
              102  LOAD_STR                 ' '
              104  INPLACE_ADD      
              106  STORE_FAST               'tokval'
            108_0  COME_FROM            98  '98'

 L. 214       108  LOAD_FAST                'toknum'
              110  LOAD_GLOBAL              INDENT
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   130  'to 130'

 L. 215       116  LOAD_FAST                'indents'
              118  LOAD_METHOD              append
              120  LOAD_FAST                'tokval'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L. 216       126  JUMP_BACK            64  'to 64'
              128  JUMP_FORWARD        192  'to 192'
            130_0  COME_FROM           114  '114'

 L. 217       130  LOAD_FAST                'toknum'
              132  LOAD_GLOBAL              DEDENT
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   150  'to 150'

 L. 218       138  LOAD_FAST                'indents'
              140  LOAD_METHOD              pop
              142  CALL_METHOD_0         0  ''
              144  POP_TOP          

 L. 219       146  JUMP_BACK            64  'to 64'
              148  JUMP_FORWARD        192  'to 192'
            150_0  COME_FROM           136  '136'

 L. 220       150  LOAD_FAST                'toknum'
              152  LOAD_GLOBAL              NEWLINE
              154  LOAD_GLOBAL              NL
              156  BUILD_TUPLE_2         2 
              158  COMPARE_OP               in
              160  POP_JUMP_IF_FALSE   168  'to 168'

 L. 221       162  LOAD_CONST               True
              164  STORE_FAST               'startline'
              166  JUMP_FORWARD        192  'to 192'
            168_0  COME_FROM           160  '160'

 L. 222       168  LOAD_FAST                'startline'
              170  POP_JUMP_IF_FALSE   192  'to 192'
              172  LOAD_FAST                'indents'
              174  POP_JUMP_IF_FALSE   192  'to 192'

 L. 223       176  LOAD_FAST                'toks_append'
              178  LOAD_FAST                'indents'
              180  LOAD_CONST               -1
              182  BINARY_SUBSCR    
              184  CALL_FUNCTION_1       1  ''
              186  POP_TOP          

 L. 224       188  LOAD_CONST               False
              190  STORE_FAST               'startline'
            192_0  COME_FROM           174  '174'
            192_1  COME_FROM           170  '170'
            192_2  COME_FROM           166  '166'
            192_3  COME_FROM           148  '148'
            192_4  COME_FROM           128  '128'

 L. 225       192  LOAD_FAST                'toks_append'
              194  LOAD_FAST                'tokval'
              196  CALL_FUNCTION_1       1  ''
              198  POP_TOP          
              200  JUMP_BACK            64  'to 64'

Parse error at or near `JUMP_FORWARD' instruction at offset 128


    cookie_re = re.compile('^[ \\t\\f]*#.*?coding[:=][ \\t]*([-\\w.]+)', re.ASCII)
    blank_re = re.compile(b'^[ \\t\\f]*(?:[#\\r\\n]|$)', re.ASCII)

    def _get_normal_name(orig_enc):
        """Imitates get_normal_name in tokenizer.c."""
        enc = orig_enc[:12].lower().replace('_', '-')
        if enc == 'utf-8' or enc.startswith('utf-8-'):
            return 'utf-8'
        if enc in ('latin-1', 'iso-8859-1', 'iso-latin-1') or enc.startswith(('latin-1-',
                                                                              'iso-8859-1-',
                                                                              'iso-latin-1-')):
            return 'iso-8859-1'
        return orig_enc


    def detect_encoding(readline):
        """
    The detect_encoding() function is used to detect the encoding that should
    be used to decode a Python source file. It requires one argument, readline,
    in the same way as the tokenize() generator.

    It will call readline a maximum of twice, and return the encoding used
    (as a string) and a list of any lines (left as bytes) it has read
    in.

    It detects the encoding from the presence of a utf-8 bom or an encoding
    cookie as specified in pep-0263. If both a bom and a cookie are present, but
    disagree, a SyntaxError will be raised. If the encoding cookie is an invalid
    charset, raise a SyntaxError.  Note that if a utf-8 bom is found,
    'utf-8-sig' is returned.

    If no encoding is specified, then the default of 'utf-8' will be returned.
    """
        bom_found = False
        encoding = None
        default = 'utf-8'

        def read_or_stop--- This code section failed: ---

 L. 263         0  SETUP_FINALLY        10  'to 10'

 L. 264         2  LOAD_DEREF               'readline'
                4  CALL_FUNCTION_0       0  ''
                6  POP_BLOCK        
                8  RETURN_VALUE     
             10_0  COME_FROM_FINALLY     0  '0'

 L. 265        10  DUP_TOP          
               12  LOAD_GLOBAL              StopIteration
               14  COMPARE_OP               exception-match
               16  POP_JUMP_IF_FALSE    34  'to 34'
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 266        24  LOAD_GLOBAL              bytes
               26  CALL_FUNCTION_0       0  ''
               28  ROT_FOUR         
               30  POP_EXCEPT       
               32  RETURN_VALUE     
             34_0  COME_FROM            16  '16'
               34  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 20

        def find_cookie(line):
            try:
                line_string = line.decode('ascii')
            except UnicodeDecodeError:
                return
            else:
                match = cookie_re.match(line_string)
                if not match:
                    return
                encoding = _get_normal_name(match.group(1))
                try:
                    codec = lookup(encoding)
                except LookupError:
                    raise SyntaxError('unknown encoding: ' + encoding)
                else:
                    if bom_found:
                        if codec.name != 'utf-8':
                            raise SyntaxError('encoding problem: utf-8')
                        encoding += '-sig'
                    return encoding

        first = read_or_stop()
        if first.startswith(BOM_UTF8):
            bom_found = True
            first = first[3:]
            default = 'utf-8-sig'
        else:
            if not first:
                return (
                 default, [])
            else:
                encoding = find_cookie(first)
                if encoding:
                    return (
                     encoding, [first])
                return blank_re.match(first) or (
                 default, [first])
            second = read_or_stop()
            return second or (
             default, [first])
        encoding = find_cookie(second)
        if encoding:
            return (
             encoding, [first, second])
        return (default, [first, second])


    def untokenize(iterable):
        """Transform tokens back into Python source code.

    Each element returned by the iterable must be a token sequence
    with at least two elements, a token number and token value.  If
    only two tokens are passed, the resulting output is poor.

    Round-trip invariant for full input:
        Untokenized source will match input source exactly

    Round-trip invariant for limited input:
        # Output text will tokenize the back to the input
        t1 = [tok[:2] for tok in generate_tokens(f.readline)]
        newcode = untokenize(t1)
        readline = iter(newcode.splitlines(1)).next
        t2 = [tok[:2] for tokin generate_tokens(readline)]
        assert t1 == t2
    """
        ut = Untokenizer()
        return ut.untokenize(iterable)


    def generate_tokens--- This code section failed: ---

 L. 351         0  LOAD_CONST               0
                2  DUP_TOP          
                4  STORE_FAST               'lnum'
                6  DUP_TOP          
                8  STORE_FAST               'parenlev'
               10  STORE_FAST               'continued'

 L. 352        12  LOAD_CONST               ('', 0)
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'contstr'
               18  STORE_FAST               'needcont'

 L. 353        20  LOAD_CONST               None
               22  STORE_FAST               'contline'

 L. 354        24  LOAD_CONST               0
               26  BUILD_LIST_1          1 
               28  STORE_FAST               'indents'

 L. 357        30  LOAD_CONST               None
               32  STORE_FAST               'stashed'

 L. 358        34  LOAD_CONST               False
               36  STORE_FAST               'async_def'

 L. 359        38  LOAD_CONST               0
               40  STORE_FAST               'async_def_indent'

 L. 360        42  LOAD_CONST               False
               44  STORE_FAST               'async_def_nl'
             46_0  COME_FROM           890  '890'

 L. 363        46  SETUP_FINALLY        58  'to 58'

 L. 364        48  LOAD_FAST                'readline'
               50  CALL_FUNCTION_0       0  ''
               52  STORE_FAST               'line'
               54  POP_BLOCK        
               56  JUMP_FORWARD         82  'to 82'
             58_0  COME_FROM_FINALLY    46  '46'

 L. 365        58  DUP_TOP          
               60  LOAD_GLOBAL              StopIteration
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    80  'to 80'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 366        72  LOAD_STR                 ''
               74  STORE_FAST               'line'
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
             80_0  COME_FROM            64  '64'
               80  END_FINALLY      
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            56  '56'

 L. 367        82  LOAD_FAST                'lnum'
               84  LOAD_CONST               1
               86  BINARY_ADD       
               88  STORE_FAST               'lnum'

 L. 368        90  LOAD_CONST               0
               92  LOAD_GLOBAL              len
               94  LOAD_FAST                'line'
               96  CALL_FUNCTION_1       1  ''
               98  ROT_TWO          
              100  STORE_FAST               'pos'
              102  STORE_FAST               'max'

 L. 370       104  LOAD_FAST                'contstr'
          106_108  POP_JUMP_IF_FALSE   306  'to 306'

 L. 371       110  LOAD_FAST                'line'
              112  POP_JUMP_IF_TRUE    124  'to 124'

 L. 372       114  LOAD_GLOBAL              TokenError
              116  LOAD_STR                 'EOF in multi-line string'
              118  LOAD_FAST                'strstart'
              120  CALL_FUNCTION_2       2  ''
              122  RAISE_VARARGS_1       1  'exception instance'
            124_0  COME_FROM           112  '112'

 L. 373       124  LOAD_FAST                'endprog'
              126  LOAD_METHOD              match
              128  LOAD_FAST                'line'
              130  CALL_METHOD_1         1  ''
              132  STORE_FAST               'endmatch'

 L. 374       134  LOAD_FAST                'endmatch'
              136  POP_JUMP_IF_FALSE   202  'to 202'

 L. 375       138  LOAD_FAST                'endmatch'
              140  LOAD_METHOD              end
              142  LOAD_CONST               0
              144  CALL_METHOD_1         1  ''
              146  DUP_TOP          
              148  STORE_FAST               'pos'
              150  STORE_FAST               'end'

 L. 376       152  LOAD_GLOBAL              STRING
              154  LOAD_FAST                'contstr'
              156  LOAD_FAST                'line'
              158  LOAD_CONST               None
              160  LOAD_FAST                'end'
              162  BUILD_SLICE_2         2 
              164  BINARY_SUBSCR    
              166  BINARY_ADD       

 L. 377       168  LOAD_FAST                'strstart'

 L. 377       170  LOAD_FAST                'lnum'
              172  LOAD_FAST                'end'
              174  BUILD_TUPLE_2         2 

 L. 377       176  LOAD_FAST                'contline'
              178  LOAD_FAST                'line'
              180  BINARY_ADD       

 L. 376       182  BUILD_TUPLE_5         5 
              184  YIELD_VALUE      
              186  POP_TOP          

 L. 378       188  LOAD_CONST               ('', 0)
              190  UNPACK_SEQUENCE_2     2 
              192  STORE_FAST               'contstr'
              194  STORE_FAST               'needcont'

 L. 379       196  LOAD_CONST               None
              198  STORE_FAST               'contline'
              200  JUMP_FORWARD        884  'to 884'
            202_0  COME_FROM           136  '136'

 L. 380       202  LOAD_FAST                'needcont'
          204_206  POP_JUMP_IF_FALSE   284  'to 284'
              208  LOAD_FAST                'line'
              210  LOAD_CONST               -2
              212  LOAD_CONST               None
              214  BUILD_SLICE_2         2 
              216  BINARY_SUBSCR    
              218  LOAD_STR                 '\\\n'
              220  COMPARE_OP               !=
          222_224  POP_JUMP_IF_FALSE   284  'to 284'
              226  LOAD_FAST                'line'
              228  LOAD_CONST               -3
              230  LOAD_CONST               None
              232  BUILD_SLICE_2         2 
              234  BINARY_SUBSCR    
              236  LOAD_STR                 '\\\r\n'
              238  COMPARE_OP               !=
          240_242  POP_JUMP_IF_FALSE   284  'to 284'

 L. 381       244  LOAD_GLOBAL              ERRORTOKEN
              246  LOAD_FAST                'contstr'
              248  LOAD_FAST                'line'
              250  BINARY_ADD       

 L. 382       252  LOAD_FAST                'strstart'

 L. 382       254  LOAD_FAST                'lnum'
              256  LOAD_GLOBAL              len
              258  LOAD_FAST                'line'
              260  CALL_FUNCTION_1       1  ''
              262  BUILD_TUPLE_2         2 

 L. 382       264  LOAD_FAST                'contline'

 L. 381       266  BUILD_TUPLE_5         5 
              268  YIELD_VALUE      
              270  POP_TOP          

 L. 383       272  LOAD_STR                 ''
              274  STORE_FAST               'contstr'

 L. 384       276  LOAD_CONST               None
              278  STORE_FAST               'contline'

 L. 385       280  JUMP_BACK            46  'to 46'
              282  JUMP_FORWARD        884  'to 884'
            284_0  COME_FROM           240  '240'
            284_1  COME_FROM           222  '222'
            284_2  COME_FROM           204  '204'

 L. 387       284  LOAD_FAST                'contstr'
              286  LOAD_FAST                'line'
              288  BINARY_ADD       
              290  STORE_FAST               'contstr'

 L. 388       292  LOAD_FAST                'contline'
              294  LOAD_FAST                'line'
              296  BINARY_ADD       
              298  STORE_FAST               'contline'

 L. 389       300  JUMP_BACK            46  'to 46'
          302_304  JUMP_FORWARD        884  'to 884'
            306_0  COME_FROM           106  '106'

 L. 391       306  LOAD_FAST                'parenlev'
              308  LOAD_CONST               0
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   860  'to 860'
              316  LOAD_FAST                'continued'
          318_320  POP_JUMP_IF_TRUE    860  'to 860'

 L. 392       322  LOAD_FAST                'line'
          324_326  POP_JUMP_IF_TRUE    332  'to 332'

 L. 392   328_330  BREAK_LOOP         1836  'to 1836'
            332_0  COME_FROM           324  '324'

 L. 393       332  LOAD_CONST               0
              334  STORE_FAST               'column'

 L. 394       336  LOAD_FAST                'pos'
              338  LOAD_FAST                'max'
              340  COMPARE_OP               <
          342_344  POP_JUMP_IF_FALSE   438  'to 438'

 L. 395       346  LOAD_FAST                'line'
              348  LOAD_FAST                'pos'
              350  BINARY_SUBSCR    
              352  LOAD_STR                 ' '
              354  COMPARE_OP               ==
          356_358  POP_JUMP_IF_FALSE   370  'to 370'

 L. 395       360  LOAD_FAST                'column'
              362  LOAD_CONST               1
              364  BINARY_ADD       
              366  STORE_FAST               'column'
              368  JUMP_FORWARD        426  'to 426'
            370_0  COME_FROM           356  '356'

 L. 396       370  LOAD_FAST                'line'
              372  LOAD_FAST                'pos'
              374  BINARY_SUBSCR    
              376  LOAD_STR                 '\t'
              378  COMPARE_OP               ==
          380_382  POP_JUMP_IF_FALSE   402  'to 402'

 L. 396       384  LOAD_FAST                'column'
              386  LOAD_GLOBAL              tabsize
              388  BINARY_FLOOR_DIVIDE
              390  LOAD_CONST               1
              392  BINARY_ADD       
              394  LOAD_GLOBAL              tabsize
              396  BINARY_MULTIPLY  
              398  STORE_FAST               'column'
              400  JUMP_FORWARD        426  'to 426'
            402_0  COME_FROM           380  '380'

 L. 397       402  LOAD_FAST                'line'
              404  LOAD_FAST                'pos'
              406  BINARY_SUBSCR    
              408  LOAD_STR                 '\x0c'
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_FALSE   438  'to 438'

 L. 397       416  LOAD_CONST               0
              418  STORE_FAST               'column'
              420  JUMP_FORWARD        426  'to 426'

 L. 398   422_424  BREAK_LOOP          438  'to 438'
            426_0  COME_FROM           420  '420'
            426_1  COME_FROM           400  '400'
            426_2  COME_FROM           368  '368'

 L. 399       426  LOAD_FAST                'pos'
              428  LOAD_CONST               1
              430  BINARY_ADD       
              432  STORE_FAST               'pos'
          434_436  JUMP_BACK           336  'to 336'
            438_0  COME_FROM           412  '412'
            438_1  COME_FROM           342  '342'

 L. 400       438  LOAD_FAST                'pos'
              440  LOAD_FAST                'max'
              442  COMPARE_OP               ==
          444_446  POP_JUMP_IF_FALSE   452  'to 452'

 L. 400   448_450  BREAK_LOOP         1836  'to 1836'
            452_0  COME_FROM           444  '444'

 L. 402       452  LOAD_FAST                'stashed'
          454_456  POP_JUMP_IF_FALSE   468  'to 468'

 L. 403       458  LOAD_FAST                'stashed'
              460  YIELD_VALUE      
              462  POP_TOP          

 L. 404       464  LOAD_CONST               None
              466  STORE_FAST               'stashed'
            468_0  COME_FROM           454  '454'

 L. 406       468  LOAD_FAST                'line'
              470  LOAD_FAST                'pos'
              472  BINARY_SUBSCR    
              474  LOAD_STR                 '#\r\n'
              476  COMPARE_OP               in
          478_480  POP_JUMP_IF_FALSE   650  'to 650'

 L. 407       482  LOAD_FAST                'line'
              484  LOAD_FAST                'pos'
              486  BINARY_SUBSCR    
              488  LOAD_STR                 '#'
              490  COMPARE_OP               ==
          492_494  POP_JUMP_IF_FALSE   596  'to 596'

 L. 408       496  LOAD_FAST                'line'
              498  LOAD_FAST                'pos'
              500  LOAD_CONST               None
              502  BUILD_SLICE_2         2 
              504  BINARY_SUBSCR    
              506  LOAD_METHOD              rstrip
              508  LOAD_STR                 '\r\n'
              510  CALL_METHOD_1         1  ''
              512  STORE_FAST               'comment_token'

 L. 409       514  LOAD_FAST                'pos'
              516  LOAD_GLOBAL              len
              518  LOAD_FAST                'comment_token'
              520  CALL_FUNCTION_1       1  ''
              522  BINARY_ADD       
              524  STORE_FAST               'nl_pos'

 L. 410       526  LOAD_GLOBAL              COMMENT
              528  LOAD_FAST                'comment_token'

 L. 411       530  LOAD_FAST                'lnum'
              532  LOAD_FAST                'pos'
              534  BUILD_TUPLE_2         2 

 L. 411       536  LOAD_FAST                'lnum'
              538  LOAD_FAST                'pos'
              540  LOAD_GLOBAL              len
              542  LOAD_FAST                'comment_token'
              544  CALL_FUNCTION_1       1  ''
              546  BINARY_ADD       
              548  BUILD_TUPLE_2         2 

 L. 411       550  LOAD_FAST                'line'

 L. 410       552  BUILD_TUPLE_5         5 
              554  YIELD_VALUE      
              556  POP_TOP          

 L. 412       558  LOAD_GLOBAL              NL
              560  LOAD_FAST                'line'
              562  LOAD_FAST                'nl_pos'
              564  LOAD_CONST               None
              566  BUILD_SLICE_2         2 
              568  BINARY_SUBSCR    

 L. 413       570  LOAD_FAST                'lnum'
              572  LOAD_FAST                'nl_pos'
              574  BUILD_TUPLE_2         2 

 L. 413       576  LOAD_FAST                'lnum'
              578  LOAD_GLOBAL              len
              580  LOAD_FAST                'line'
              582  CALL_FUNCTION_1       1  ''
              584  BUILD_TUPLE_2         2 

 L. 413       586  LOAD_FAST                'line'

 L. 412       588  BUILD_TUPLE_5         5 
              590  YIELD_VALUE      
              592  POP_TOP          
              594  JUMP_BACK            46  'to 46'
            596_0  COME_FROM           492  '492'

 L. 415       596  LOAD_GLOBAL              NL
              598  LOAD_GLOBAL              COMMENT
              600  BUILD_TUPLE_2         2 
              602  LOAD_FAST                'line'
              604  LOAD_FAST                'pos'
              606  BINARY_SUBSCR    
              608  LOAD_STR                 '#'
              610  COMPARE_OP               ==
              612  BINARY_SUBSCR    
              614  LOAD_FAST                'line'
              616  LOAD_FAST                'pos'
              618  LOAD_CONST               None
              620  BUILD_SLICE_2         2 
              622  BINARY_SUBSCR    

 L. 416       624  LOAD_FAST                'lnum'
              626  LOAD_FAST                'pos'
              628  BUILD_TUPLE_2         2 

 L. 416       630  LOAD_FAST                'lnum'
              632  LOAD_GLOBAL              len
              634  LOAD_FAST                'line'
              636  CALL_FUNCTION_1       1  ''
              638  BUILD_TUPLE_2         2 

 L. 416       640  LOAD_FAST                'line'

 L. 415       642  BUILD_TUPLE_5         5 
              644  YIELD_VALUE      
              646  POP_TOP          

 L. 417       648  JUMP_BACK            46  'to 46'
            650_0  COME_FROM           478  '478'

 L. 419       650  LOAD_FAST                'column'
              652  LOAD_FAST                'indents'
              654  LOAD_CONST               -1
              656  BINARY_SUBSCR    
              658  COMPARE_OP               >
          660_662  POP_JUMP_IF_FALSE   706  'to 706'

 L. 420       664  LOAD_FAST                'indents'
              666  LOAD_METHOD              append
              668  LOAD_FAST                'column'
              670  CALL_METHOD_1         1  ''
              672  POP_TOP          

 L. 421       674  LOAD_GLOBAL              INDENT
              676  LOAD_FAST                'line'
              678  LOAD_CONST               None
              680  LOAD_FAST                'pos'
              682  BUILD_SLICE_2         2 
              684  BINARY_SUBSCR    
              686  LOAD_FAST                'lnum'
              688  LOAD_CONST               0
              690  BUILD_TUPLE_2         2 
              692  LOAD_FAST                'lnum'
              694  LOAD_FAST                'pos'
              696  BUILD_TUPLE_2         2 
              698  LOAD_FAST                'line'
              700  BUILD_TUPLE_5         5 
              702  YIELD_VALUE      
              704  POP_TOP          
            706_0  COME_FROM           660  '660'

 L. 422       706  LOAD_FAST                'column'
              708  LOAD_FAST                'indents'
              710  LOAD_CONST               -1
              712  BINARY_SUBSCR    
              714  COMPARE_OP               <
          716_718  POP_JUMP_IF_FALSE   820  'to 820'

 L. 423       720  LOAD_FAST                'column'
              722  LOAD_FAST                'indents'
              724  COMPARE_OP               not-in
          726_728  POP_JUMP_IF_FALSE   748  'to 748'

 L. 424       730  LOAD_GLOBAL              IndentationError

 L. 425       732  LOAD_STR                 'unindent does not match any outer indentation level'

 L. 426       734  LOAD_STR                 '<tokenize>'
              736  LOAD_FAST                'lnum'
              738  LOAD_FAST                'pos'
              740  LOAD_FAST                'line'
              742  BUILD_TUPLE_4         4 

 L. 424       744  CALL_FUNCTION_2       2  ''
              746  RAISE_VARARGS_1       1  'exception instance'
            748_0  COME_FROM           726  '726'

 L. 427       748  LOAD_FAST                'indents'
              750  LOAD_CONST               None
              752  LOAD_CONST               -1
              754  BUILD_SLICE_2         2 
              756  BINARY_SUBSCR    
              758  STORE_FAST               'indents'

 L. 429       760  LOAD_FAST                'async_def'
          762_764  POP_JUMP_IF_FALSE   792  'to 792'
              766  LOAD_FAST                'async_def_indent'
              768  LOAD_FAST                'indents'
              770  LOAD_CONST               -1
              772  BINARY_SUBSCR    
              774  COMPARE_OP               >=
          776_778  POP_JUMP_IF_FALSE   792  'to 792'
            780_0  COME_FROM           200  '200'

 L. 430       780  LOAD_CONST               False
              782  STORE_FAST               'async_def'

 L. 431       784  LOAD_CONST               False
              786  STORE_FAST               'async_def_nl'

 L. 432       788  LOAD_CONST               0
              790  STORE_FAST               'async_def_indent'
            792_0  COME_FROM           776  '776'
            792_1  COME_FROM           762  '762'

 L. 434       792  LOAD_GLOBAL              DEDENT
              794  LOAD_STR                 ''
              796  LOAD_FAST                'lnum'
              798  LOAD_FAST                'pos'
              800  BUILD_TUPLE_2         2 
              802  LOAD_FAST                'lnum'
              804  LOAD_FAST                'pos'
              806  BUILD_TUPLE_2         2 
              808  LOAD_FAST                'line'
              810  BUILD_TUPLE_5         5 
              812  YIELD_VALUE      
              814  POP_TOP          
          816_818  JUMP_BACK           706  'to 706'
            820_0  COME_FROM           716  '716'

 L. 436       820  LOAD_FAST                'async_def'
          822_824  POP_JUMP_IF_FALSE   884  'to 884'
              826  LOAD_FAST                'async_def_nl'
          828_830  POP_JUMP_IF_FALSE   884  'to 884'
              832  LOAD_FAST                'async_def_indent'
              834  LOAD_FAST                'indents'
              836  LOAD_CONST               -1
              838  BINARY_SUBSCR    
              840  COMPARE_OP               >=
          842_844  POP_JUMP_IF_FALSE   884  'to 884'

 L. 437       846  LOAD_CONST               False
              848  STORE_FAST               'async_def'

 L. 438       850  LOAD_CONST               False
              852  STORE_FAST               'async_def_nl'

 L. 439       854  LOAD_CONST               0
              856  STORE_FAST               'async_def_indent'
              858  JUMP_FORWARD        884  'to 884'
            860_0  COME_FROM           318  '318'
            860_1  COME_FROM           312  '312'

 L. 442       860  LOAD_FAST                'line'
            862_0  COME_FROM           282  '282'
          862_864  POP_JUMP_IF_TRUE    880  'to 880'

 L. 443       866  LOAD_GLOBAL              TokenError
              868  LOAD_STR                 'EOF in multi-line statement'
              870  LOAD_FAST                'lnum'
              872  LOAD_CONST               0
              874  BUILD_TUPLE_2         2 
              876  CALL_FUNCTION_2       2  ''
              878  RAISE_VARARGS_1       1  'exception instance'
            880_0  COME_FROM           862  '862'

 L. 444       880  LOAD_CONST               0
              882  STORE_FAST               'continued'
            884_0  COME_FROM           858  '858'
            884_1  COME_FROM           842  '842'
            884_2  COME_FROM           828  '828'
            884_3  COME_FROM           822  '822'
            884_4  COME_FROM           302  '302'

 L. 446       884  LOAD_FAST                'pos'
              886  LOAD_FAST                'max'
              888  COMPARE_OP               <
              890  POP_JUMP_IF_FALSE    46  'to 46'

 L. 447       892  LOAD_GLOBAL              pseudoprog
              894  LOAD_METHOD              match
              896  LOAD_FAST                'line'
              898  LOAD_FAST                'pos'
              900  CALL_METHOD_2         2  ''
              902  STORE_FAST               'pseudomatch'

 L. 448       904  LOAD_FAST                'pseudomatch'
          906_908  POP_JUMP_IF_FALSE  1790  'to 1790'

 L. 449       910  LOAD_FAST                'pseudomatch'
              912  LOAD_METHOD              span
              914  LOAD_CONST               1
              916  CALL_METHOD_1         1  ''
              918  UNPACK_SEQUENCE_2     2 
              920  STORE_FAST               'start'
              922  STORE_FAST               'end'

 L. 450       924  LOAD_FAST                'lnum'
              926  LOAD_FAST                'start'
              928  BUILD_TUPLE_2         2 
              930  LOAD_FAST                'lnum'
              932  LOAD_FAST                'end'
              934  BUILD_TUPLE_2         2 
              936  LOAD_FAST                'end'
              938  ROT_THREE        
              940  ROT_TWO          
              942  STORE_FAST               'spos'
              944  STORE_FAST               'epos'
              946  STORE_FAST               'pos'

 L. 451       948  LOAD_FAST                'line'
              950  LOAD_FAST                'start'
              952  LOAD_FAST                'end'
              954  BUILD_SLICE_2         2 
              956  BINARY_SUBSCR    
              958  LOAD_FAST                'line'
              960  LOAD_FAST                'start'
              962  BINARY_SUBSCR    
              964  ROT_TWO          
              966  STORE_FAST               'token'
              968  STORE_FAST               'initial'

 L. 453       970  LOAD_FAST                'initial'
              972  LOAD_GLOBAL              string
              974  LOAD_ATTR                digits
              976  COMPARE_OP               in
          978_980  POP_JUMP_IF_TRUE   1002  'to 1002'

 L. 454       982  LOAD_FAST                'initial'
              984  LOAD_STR                 '.'
              986  COMPARE_OP               ==

 L. 453   988_990  POP_JUMP_IF_FALSE  1022  'to 1022'

 L. 454       992  LOAD_FAST                'token'
              994  LOAD_STR                 '.'
              996  COMPARE_OP               !=

 L. 453  998_1000  POP_JUMP_IF_FALSE  1022  'to 1022'
           1002_0  COME_FROM           978  '978'

 L. 455      1002  LOAD_GLOBAL              NUMBER
             1004  LOAD_FAST                'token'
             1006  LOAD_FAST                'spos'
             1008  LOAD_FAST                'epos'
             1010  LOAD_FAST                'line'
             1012  BUILD_TUPLE_5         5 
             1014  YIELD_VALUE      
             1016  POP_TOP          
         1018_1020  JUMP_ABSOLUTE      1830  'to 1830'
           1022_0  COME_FROM           998  '998'
           1022_1  COME_FROM           988  '988'

 L. 456      1022  LOAD_FAST                'initial'
             1024  LOAD_STR                 '\r\n'
             1026  COMPARE_OP               in
         1028_1030  POP_JUMP_IF_FALSE  1098  'to 1098'

 L. 457      1032  LOAD_GLOBAL              NEWLINE
             1034  STORE_FAST               'newline'

 L. 458      1036  LOAD_FAST                'parenlev'
             1038  LOAD_CONST               0
             1040  COMPARE_OP               >
         1042_1044  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 459      1046  LOAD_GLOBAL              NL
             1048  STORE_FAST               'newline'
             1050  JUMP_FORWARD       1062  'to 1062'
           1052_0  COME_FROM          1042  '1042'

 L. 460      1052  LOAD_FAST                'async_def'
         1054_1056  POP_JUMP_IF_FALSE  1062  'to 1062'

 L. 461      1058  LOAD_CONST               True
             1060  STORE_FAST               'async_def_nl'
           1062_0  COME_FROM          1054  '1054'
           1062_1  COME_FROM          1050  '1050'

 L. 462      1062  LOAD_FAST                'stashed'
         1064_1066  POP_JUMP_IF_FALSE  1078  'to 1078'

 L. 463      1068  LOAD_FAST                'stashed'
             1070  YIELD_VALUE      
             1072  POP_TOP          

 L. 464      1074  LOAD_CONST               None
             1076  STORE_FAST               'stashed'
           1078_0  COME_FROM          1064  '1064'

 L. 465      1078  LOAD_FAST                'newline'
             1080  LOAD_FAST                'token'
             1082  LOAD_FAST                'spos'
             1084  LOAD_FAST                'epos'
             1086  LOAD_FAST                'line'
             1088  BUILD_TUPLE_5         5 
             1090  YIELD_VALUE      
             1092  POP_TOP          
         1094_1096  JUMP_ABSOLUTE      1830  'to 1830'
           1098_0  COME_FROM          1028  '1028'

 L. 467      1098  LOAD_FAST                'initial'
             1100  LOAD_STR                 '#'
             1102  COMPARE_OP               ==
         1104_1106  POP_JUMP_IF_FALSE  1160  'to 1160'

 L. 468      1108  LOAD_FAST                'token'
             1110  LOAD_METHOD              endswith
             1112  LOAD_STR                 '\n'
             1114  CALL_METHOD_1         1  ''
         1116_1118  POP_JUMP_IF_FALSE  1124  'to 1124'
             1120  LOAD_GLOBAL              AssertionError
             1122  RAISE_VARARGS_1       1  'exception instance'
           1124_0  COME_FROM          1116  '1116'

 L. 469      1124  LOAD_FAST                'stashed'
         1126_1128  POP_JUMP_IF_FALSE  1140  'to 1140'

 L. 470      1130  LOAD_FAST                'stashed'
             1132  YIELD_VALUE      
             1134  POP_TOP          

 L. 471      1136  LOAD_CONST               None
             1138  STORE_FAST               'stashed'
           1140_0  COME_FROM          1126  '1126'

 L. 472      1140  LOAD_GLOBAL              COMMENT
             1142  LOAD_FAST                'token'
             1144  LOAD_FAST                'spos'
             1146  LOAD_FAST                'epos'
             1148  LOAD_FAST                'line'
             1150  BUILD_TUPLE_5         5 
             1152  YIELD_VALUE      
             1154  POP_TOP          
         1156_1158  JUMP_ABSOLUTE      1830  'to 1830'
           1160_0  COME_FROM          1104  '1104'

 L. 473      1160  LOAD_FAST                'token'
             1162  LOAD_GLOBAL              triple_quoted
             1164  COMPARE_OP               in
         1166_1168  POP_JUMP_IF_FALSE  1286  'to 1286'

 L. 474      1170  LOAD_GLOBAL              endprogs
             1172  LOAD_FAST                'token'
             1174  BINARY_SUBSCR    
             1176  STORE_FAST               'endprog'

 L. 475      1178  LOAD_FAST                'endprog'
             1180  LOAD_METHOD              match
             1182  LOAD_FAST                'line'
             1184  LOAD_FAST                'pos'
             1186  CALL_METHOD_2         2  ''
             1188  STORE_FAST               'endmatch'

 L. 476      1190  LOAD_FAST                'endmatch'
         1192_1194  POP_JUMP_IF_FALSE  1256  'to 1256'

 L. 477      1196  LOAD_FAST                'endmatch'
             1198  LOAD_METHOD              end
             1200  LOAD_CONST               0
             1202  CALL_METHOD_1         1  ''
             1204  STORE_FAST               'pos'

 L. 478      1206  LOAD_FAST                'line'
             1208  LOAD_FAST                'start'
             1210  LOAD_FAST                'pos'
             1212  BUILD_SLICE_2         2 
             1214  BINARY_SUBSCR    
             1216  STORE_FAST               'token'

 L. 479      1218  LOAD_FAST                'stashed'
         1220_1222  POP_JUMP_IF_FALSE  1234  'to 1234'

 L. 480      1224  LOAD_FAST                'stashed'
             1226  YIELD_VALUE      
             1228  POP_TOP          

 L. 481      1230  LOAD_CONST               None
             1232  STORE_FAST               'stashed'
           1234_0  COME_FROM          1220  '1220'

 L. 482      1234  LOAD_GLOBAL              STRING
             1236  LOAD_FAST                'token'
             1238  LOAD_FAST                'spos'
             1240  LOAD_FAST                'lnum'
             1242  LOAD_FAST                'pos'
             1244  BUILD_TUPLE_2         2 
             1246  LOAD_FAST                'line'
             1248  BUILD_TUPLE_5         5 
             1250  YIELD_VALUE      
             1252  POP_TOP          
             1254  JUMP_ABSOLUTE      1830  'to 1830'
           1256_0  COME_FROM          1192  '1192'

 L. 484      1256  LOAD_FAST                'lnum'
             1258  LOAD_FAST                'start'
             1260  BUILD_TUPLE_2         2 
             1262  STORE_FAST               'strstart'

 L. 485      1264  LOAD_FAST                'line'
             1266  LOAD_FAST                'start'
             1268  LOAD_CONST               None
             1270  BUILD_SLICE_2         2 
             1272  BINARY_SUBSCR    
             1274  STORE_FAST               'contstr'

 L. 486      1276  LOAD_FAST                'line'
             1278  STORE_FAST               'contline'

 L. 487      1280  JUMP_BACK            46  'to 46'
         1282_1284  JUMP_ABSOLUTE      1830  'to 1830'
           1286_0  COME_FROM          1166  '1166'

 L. 488      1286  LOAD_FAST                'initial'
             1288  LOAD_GLOBAL              single_quoted
             1290  COMPARE_OP               in
         1292_1294  POP_JUMP_IF_TRUE   1332  'to 1332'

 L. 489      1296  LOAD_FAST                'token'
             1298  LOAD_CONST               None
             1300  LOAD_CONST               2
             1302  BUILD_SLICE_2         2 
             1304  BINARY_SUBSCR    
             1306  LOAD_GLOBAL              single_quoted
             1308  COMPARE_OP               in

 L. 488  1310_1312  POP_JUMP_IF_TRUE   1332  'to 1332'

 L. 490      1314  LOAD_FAST                'token'
             1316  LOAD_CONST               None
             1318  LOAD_CONST               3
             1320  BUILD_SLICE_2         2 
             1322  BINARY_SUBSCR    
             1324  LOAD_GLOBAL              single_quoted
             1326  COMPARE_OP               in

 L. 488  1328_1330  POP_JUMP_IF_FALSE  1452  'to 1452'
           1332_0  COME_FROM          1310  '1310'
           1332_1  COME_FROM          1292  '1292'

 L. 491      1332  LOAD_FAST                'token'
             1334  LOAD_CONST               -1
             1336  BINARY_SUBSCR    
             1338  LOAD_STR                 '\n'
             1340  COMPARE_OP               ==
         1342_1344  POP_JUMP_IF_FALSE  1416  'to 1416'

 L. 492      1346  LOAD_FAST                'lnum'
             1348  LOAD_FAST                'start'
             1350  BUILD_TUPLE_2         2 
             1352  STORE_FAST               'strstart'

 L. 493      1354  LOAD_GLOBAL              endprogs
             1356  LOAD_FAST                'initial'
             1358  BINARY_SUBSCR    
         1360_1362  JUMP_IF_TRUE_OR_POP  1388  'to 1388'
             1364  LOAD_GLOBAL              endprogs
             1366  LOAD_FAST                'token'
             1368  LOAD_CONST               1
             1370  BINARY_SUBSCR    
             1372  BINARY_SUBSCR    
         1374_1376  JUMP_IF_TRUE_OR_POP  1388  'to 1388'

 L. 494      1378  LOAD_GLOBAL              endprogs
             1380  LOAD_FAST                'token'
             1382  LOAD_CONST               2
             1384  BINARY_SUBSCR    
             1386  BINARY_SUBSCR    
           1388_0  COME_FROM          1374  '1374'
           1388_1  COME_FROM          1360  '1360'

 L. 493      1388  STORE_FAST               'endprog'

 L. 495      1390  LOAD_FAST                'line'
             1392  LOAD_FAST                'start'
             1394  LOAD_CONST               None
             1396  BUILD_SLICE_2         2 
             1398  BINARY_SUBSCR    
             1400  LOAD_CONST               1
             1402  ROT_TWO          
             1404  STORE_FAST               'contstr'
             1406  STORE_FAST               'needcont'

 L. 496      1408  LOAD_FAST                'line'
             1410  STORE_FAST               'contline'

 L. 497      1412  JUMP_BACK            46  'to 46'
             1414  JUMP_ABSOLUTE      1830  'to 1830'
           1416_0  COME_FROM          1342  '1342'

 L. 499      1416  LOAD_FAST                'stashed'
         1418_1420  POP_JUMP_IF_FALSE  1432  'to 1432'

 L. 500      1422  LOAD_FAST                'stashed'
             1424  YIELD_VALUE      
             1426  POP_TOP          

 L. 501      1428  LOAD_CONST               None
             1430  STORE_FAST               'stashed'
           1432_0  COME_FROM          1418  '1418'

 L. 502      1432  LOAD_GLOBAL              STRING
             1434  LOAD_FAST                'token'
             1436  LOAD_FAST                'spos'
             1438  LOAD_FAST                'epos'
             1440  LOAD_FAST                'line'
             1442  BUILD_TUPLE_5         5 
             1444  YIELD_VALUE      
             1446  POP_TOP          
         1448_1450  JUMP_ABSOLUTE      1830  'to 1830'
           1452_0  COME_FROM          1328  '1328'

 L. 503      1452  LOAD_FAST                'initial'
             1454  LOAD_METHOD              isidentifier
             1456  CALL_METHOD_0         0  ''
         1458_1460  POP_JUMP_IF_FALSE  1666  'to 1666'

 L. 504      1462  LOAD_FAST                'token'
             1464  LOAD_CONST               ('async', 'await')
             1466  COMPARE_OP               in
         1468_1470  POP_JUMP_IF_FALSE  1512  'to 1512'

 L. 505      1472  LOAD_FAST                'async_def'
         1474_1476  POP_JUMP_IF_FALSE  1512  'to 1512'

 L. 506      1478  LOAD_FAST                'token'
             1480  LOAD_STR                 'async'
             1482  COMPARE_OP               ==
         1484_1486  POP_JUMP_IF_FALSE  1492  'to 1492'
             1488  LOAD_GLOBAL              ASYNC
             1490  JUMP_FORWARD       1494  'to 1494'
           1492_0  COME_FROM          1484  '1484'
             1492  LOAD_GLOBAL              AWAIT
           1494_0  COME_FROM          1490  '1490'

 L. 507      1494  LOAD_FAST                'token'

 L. 507      1496  LOAD_FAST                'spos'

 L. 507      1498  LOAD_FAST                'epos'

 L. 507      1500  LOAD_FAST                'line'

 L. 506      1502  BUILD_TUPLE_5         5 
             1504  YIELD_VALUE      
             1506  POP_TOP          

 L. 508  1508_1510  JUMP_BACK           884  'to 884'
           1512_0  COME_FROM          1474  '1474'
           1512_1  COME_FROM          1468  '1468'

 L. 510      1512  LOAD_GLOBAL              NAME
             1514  LOAD_FAST                'token'
             1516  LOAD_FAST                'spos'
             1518  LOAD_FAST                'epos'
             1520  LOAD_FAST                'line'
             1522  BUILD_TUPLE_5         5 
             1524  STORE_FAST               'tok'

 L. 511      1526  LOAD_FAST                'token'
             1528  LOAD_STR                 'async'
             1530  COMPARE_OP               ==
         1532_1534  POP_JUMP_IF_FALSE  1550  'to 1550'
             1536  LOAD_FAST                'stashed'
         1538_1540  POP_JUMP_IF_TRUE   1550  'to 1550'

 L. 512      1542  LOAD_FAST                'tok'
             1544  STORE_FAST               'stashed'

 L. 513  1546_1548  JUMP_BACK           884  'to 884'
           1550_0  COME_FROM          1538  '1538'
           1550_1  COME_FROM          1532  '1532'

 L. 515      1550  LOAD_FAST                'token'
             1552  LOAD_STR                 'def'
             1554  COMPARE_OP               ==
         1556_1558  POP_JUMP_IF_FALSE  1642  'to 1642'

 L. 516      1560  LOAD_FAST                'stashed'
         1562_1564  POP_JUMP_IF_FALSE  1642  'to 1642'

 L. 517      1566  LOAD_FAST                'stashed'
             1568  LOAD_CONST               0
             1570  BINARY_SUBSCR    
             1572  LOAD_GLOBAL              NAME
             1574  COMPARE_OP               ==

 L. 516  1576_1578  POP_JUMP_IF_FALSE  1642  'to 1642'

 L. 518      1580  LOAD_FAST                'stashed'
             1582  LOAD_CONST               1
             1584  BINARY_SUBSCR    
             1586  LOAD_STR                 'async'
             1588  COMPARE_OP               ==

 L. 516  1590_1592  POP_JUMP_IF_FALSE  1642  'to 1642'

 L. 520      1594  LOAD_CONST               True
             1596  STORE_FAST               'async_def'

 L. 521      1598  LOAD_FAST                'indents'
             1600  LOAD_CONST               -1
             1602  BINARY_SUBSCR    
             1604  STORE_FAST               'async_def_indent'

 L. 523      1606  LOAD_GLOBAL              ASYNC
             1608  LOAD_FAST                'stashed'
             1610  LOAD_CONST               1
             1612  BINARY_SUBSCR    

 L. 524      1614  LOAD_FAST                'stashed'
             1616  LOAD_CONST               2
             1618  BINARY_SUBSCR    

 L. 524      1620  LOAD_FAST                'stashed'
             1622  LOAD_CONST               3
             1624  BINARY_SUBSCR    

 L. 525      1626  LOAD_FAST                'stashed'
             1628  LOAD_CONST               4
             1630  BINARY_SUBSCR    

 L. 523      1632  BUILD_TUPLE_5         5 
             1634  YIELD_VALUE      
             1636  POP_TOP          

 L. 526      1638  LOAD_CONST               None
             1640  STORE_FAST               'stashed'
           1642_0  COME_FROM          1590  '1590'
           1642_1  COME_FROM          1576  '1576'
           1642_2  COME_FROM          1562  '1562'
           1642_3  COME_FROM          1556  '1556'

 L. 528      1642  LOAD_FAST                'stashed'
         1644_1646  POP_JUMP_IF_FALSE  1658  'to 1658'

 L. 529      1648  LOAD_FAST                'stashed'
             1650  YIELD_VALUE      
             1652  POP_TOP          

 L. 530      1654  LOAD_CONST               None
             1656  STORE_FAST               'stashed'
           1658_0  COME_FROM          1644  '1644'

 L. 532      1658  LOAD_FAST                'tok'
             1660  YIELD_VALUE      
             1662  POP_TOP          
             1664  JUMP_FORWARD       1788  'to 1788'
           1666_0  COME_FROM          1458  '1458'

 L. 533      1666  LOAD_FAST                'initial'
             1668  LOAD_STR                 '\\'
             1670  COMPARE_OP               ==
         1672_1674  POP_JUMP_IF_FALSE  1718  'to 1718'

 L. 535      1676  LOAD_FAST                'stashed'
         1678_1680  POP_JUMP_IF_FALSE  1692  'to 1692'

 L. 536      1682  LOAD_FAST                'stashed'
             1684  YIELD_VALUE      
             1686  POP_TOP          

 L. 537      1688  LOAD_CONST               None
             1690  STORE_FAST               'stashed'
           1692_0  COME_FROM          1678  '1678'

 L. 538      1692  LOAD_GLOBAL              NL
             1694  LOAD_FAST                'token'
             1696  LOAD_FAST                'spos'
             1698  LOAD_FAST                'lnum'
             1700  LOAD_FAST                'pos'
             1702  BUILD_TUPLE_2         2 
             1704  LOAD_FAST                'line'
             1706  BUILD_TUPLE_5         5 
             1708  YIELD_VALUE      
             1710  POP_TOP          

 L. 539      1712  LOAD_CONST               1
             1714  STORE_FAST               'continued'
             1716  JUMP_FORWARD       1788  'to 1788'
           1718_0  COME_FROM          1672  '1672'

 L. 541      1718  LOAD_FAST                'initial'
             1720  LOAD_STR                 '([{'
             1722  COMPARE_OP               in
         1724_1726  POP_JUMP_IF_FALSE  1738  'to 1738'

 L. 541      1728  LOAD_FAST                'parenlev'
             1730  LOAD_CONST               1
             1732  BINARY_ADD       
             1734  STORE_FAST               'parenlev'
             1736  JUMP_FORWARD       1756  'to 1756'
           1738_0  COME_FROM          1724  '1724'

 L. 542      1738  LOAD_FAST                'initial'
             1740  LOAD_STR                 ')]}'
             1742  COMPARE_OP               in
         1744_1746  POP_JUMP_IF_FALSE  1756  'to 1756'

 L. 542      1748  LOAD_FAST                'parenlev'
             1750  LOAD_CONST               1
             1752  BINARY_SUBTRACT  
             1754  STORE_FAST               'parenlev'
           1756_0  COME_FROM          1744  '1744'
           1756_1  COME_FROM          1736  '1736'

 L. 543      1756  LOAD_FAST                'stashed'
         1758_1760  POP_JUMP_IF_FALSE  1772  'to 1772'

 L. 544      1762  LOAD_FAST                'stashed'
             1764  YIELD_VALUE      
             1766  POP_TOP          

 L. 545      1768  LOAD_CONST               None
             1770  STORE_FAST               'stashed'
           1772_0  COME_FROM          1758  '1758'

 L. 546      1772  LOAD_GLOBAL              OP
             1774  LOAD_FAST                'token'
             1776  LOAD_FAST                'spos'
             1778  LOAD_FAST                'epos'
             1780  LOAD_FAST                'line'
             1782  BUILD_TUPLE_5         5 
             1784  YIELD_VALUE      
             1786  POP_TOP          
           1788_0  COME_FROM          1716  '1716'
           1788_1  COME_FROM          1664  '1664'
             1788  JUMP_BACK           884  'to 884'
           1790_0  COME_FROM           906  '906'

 L. 548      1790  LOAD_GLOBAL              ERRORTOKEN
             1792  LOAD_FAST                'line'
             1794  LOAD_FAST                'pos'
             1796  BINARY_SUBSCR    

 L. 549      1798  LOAD_FAST                'lnum'
             1800  LOAD_FAST                'pos'
             1802  BUILD_TUPLE_2         2 

 L. 549      1804  LOAD_FAST                'lnum'
             1806  LOAD_FAST                'pos'
             1808  LOAD_CONST               1
             1810  BINARY_ADD       
             1812  BUILD_TUPLE_2         2 

 L. 549      1814  LOAD_FAST                'line'

 L. 548      1816  BUILD_TUPLE_5         5 
             1818  YIELD_VALUE      
             1820  POP_TOP          

 L. 550      1822  LOAD_FAST                'pos'
             1824  LOAD_CONST               1
             1826  BINARY_ADD       
             1828  STORE_FAST               'pos'
         1830_1832  JUMP_BACK           884  'to 884'
             1834  JUMP_BACK            46  'to 46'

 L. 552      1836  LOAD_FAST                'stashed'
         1838_1840  POP_JUMP_IF_FALSE  1852  'to 1852'

 L. 553      1842  LOAD_FAST                'stashed'
             1844  YIELD_VALUE      
             1846  POP_TOP          

 L. 554      1848  LOAD_CONST               None
             1850  STORE_FAST               'stashed'
           1852_0  COME_FROM          1838  '1838'

 L. 556      1852  LOAD_FAST                'indents'
             1854  LOAD_CONST               1
             1856  LOAD_CONST               None
             1858  BUILD_SLICE_2         2 
             1860  BINARY_SUBSCR    
             1862  GET_ITER         
             1864  FOR_ITER           1896  'to 1896'
             1866  STORE_FAST               'indent'

 L. 557      1868  LOAD_GLOBAL              DEDENT
             1870  LOAD_STR                 ''
             1872  LOAD_FAST                'lnum'
             1874  LOAD_CONST               0
             1876  BUILD_TUPLE_2         2 
             1878  LOAD_FAST                'lnum'
             1880  LOAD_CONST               0
             1882  BUILD_TUPLE_2         2 
             1884  LOAD_STR                 ''
             1886  BUILD_TUPLE_5         5 
             1888  YIELD_VALUE      
             1890  POP_TOP          
         1892_1894  JUMP_BACK          1864  'to 1864'

 L. 558      1896  LOAD_GLOBAL              ENDMARKER
             1898  LOAD_STR                 ''
             1900  LOAD_FAST                'lnum'
             1902  LOAD_CONST               0
             1904  BUILD_TUPLE_2         2 
             1906  LOAD_FAST                'lnum'
             1908  LOAD_CONST               0
             1910  BUILD_TUPLE_2         2 
             1912  LOAD_STR                 ''
             1914  BUILD_TUPLE_5         5 
             1916  YIELD_VALUE      
             1918  POP_TOP          

Parse error at or near `JUMP_FORWARD' instruction at offset 282


    if __name__ == '__main__':
        import sys
        if len(sys.argv) > 1:
            tokenize(open(sys.argv[1]).readline)
        else:
            tokenize(sys.stdin.readline)