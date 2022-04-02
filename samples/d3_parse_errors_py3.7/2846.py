# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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
Special = group('\\r?\\n', '[:;.,`@]')
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
 '"""':double3prog}, **{f"{prefix}'''":single3prog for prefix in _strprefixes}, **{f'{prefix}"""':double3prog for prefix in _strprefixes}, **{prefix:None for prefix in _strprefixes}}
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
            else:
                tok_type, token, start, end, line = t
                self.add_whitespace(start)
                self.tokens.append(token)
                self.prev_row, self.prev_col = end
            if tok_type in (NEWLINE, NL):
                self.prev_row += 1
                self.prev_col = 0

        return ''.join(self.tokens)

    def compat(self, token, iterable):
        startline = False
        indents = []
        toks_append = self.tokens.append
        toknum, tokval = token
        if toknum in (NAME, NUMBER):
            tokval += ' '
        if toknum in (NEWLINE, NL):
            startline = True
        for tok in iterable:
            toknum, tokval = tok[:2]
            if toknum in (NAME, NUMBER, ASYNC, AWAIT):
                tokval += ' '
            if toknum == INDENT:
                indents.append(tokval)
                continue
            else:
                if toknum == DEDENT:
                    indents.pop()
                    continue
                elif toknum in (NEWLINE, NL):
                    startline = True
                elif startline:
                    if indents:
                        toks_append(indents[(-1)])
                        startline = False
            toks_append(tokval)


cookie_re = re.compile('^[ \\t\\f]*#.*?coding[:=][ \\t]*([-\\w.]+)', re.ASCII)
blank_re = re.compile('^[ \\t\\f]*(?:[#\\r\\n]|$)', re.ASCII)

def _get_normal_name(orig_enc):
    """Imitates get_normal_name in tokenizer.c."""
    enc = orig_enc[:12].lower().replace('_', '-')
    if enc == 'utf-8' or (enc.startswith('utf-8-')):
        return 'utf-8'
    if enc in ('latin-1', 'iso-8859-1', 'iso-latin-1') or (enc.startswith(('latin-1-',
                                                                           'iso-8859-1-',
                                                                           'iso-latin-1-'))):
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

    def read_or_stop():
        try:
            return readline()
        except StopIteration:
            return bytes()

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
    if not first:
        return (default, [])
    encoding = find_cookie(first)
    if encoding:
        return (encoding, [first])
    if not blank_re.match(first):
        return (default, [first])
    second = read_or_stop()
    if not second:
        return (default, [first])
    encoding = find_cookie(second)
    if encoding:
        return (encoding, [first, second])
    return (
     default, [first, second])


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

 L. 362     46_48  SETUP_LOOP         1852  'to 1852'
             50_0  COME_FROM          1848  '1848'
             50_1  COME_FROM           650  '650'
             50_2  COME_FROM           596  '596'
             50_3  COME_FROM           304  '304'
             50_4  COME_FROM           284  '284'

 L. 363        50  SETUP_EXCEPT         62  'to 62'

 L. 364        52  LOAD_FAST                'readline'
               54  CALL_FUNCTION_0       0  '0 positional arguments'
               56  STORE_FAST               'line'
               58  POP_BLOCK        
               60  JUMP_FORWARD         86  'to 86'
             62_0  COME_FROM_EXCEPT     50  '50'

 L. 365        62  DUP_TOP          
               64  LOAD_GLOBAL              StopIteration
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    84  'to 84'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 366        76  LOAD_STR                 ''
               78  STORE_FAST               'line'
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
             84_0  COME_FROM            68  '68'
               84  END_FINALLY      
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            60  '60'

 L. 367        86  LOAD_FAST                'lnum'
               88  LOAD_CONST               1
               90  BINARY_ADD       
               92  STORE_FAST               'lnum'

 L. 368        94  LOAD_CONST               0
               96  LOAD_GLOBAL              len
               98  LOAD_FAST                'line'
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  ROT_TWO          
              104  STORE_FAST               'pos'
              106  STORE_FAST               'max'

 L. 370       108  LOAD_FAST                'contstr'
          110_112  POP_JUMP_IF_FALSE   310  'to 310'

 L. 371       114  LOAD_FAST                'line'
              116  POP_JUMP_IF_TRUE    128  'to 128'

 L. 372       118  LOAD_GLOBAL              TokenError
              120  LOAD_STR                 'EOF in multi-line string'
              122  LOAD_FAST                'strstart'
              124  CALL_FUNCTION_2       2  '2 positional arguments'
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           116  '116'

 L. 373       128  LOAD_FAST                'endprog'
              130  LOAD_METHOD              match
              132  LOAD_FAST                'line'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  STORE_FAST               'endmatch'

 L. 374       138  LOAD_FAST                'endmatch'
              140  POP_JUMP_IF_FALSE   206  'to 206'

 L. 375       142  LOAD_FAST                'endmatch'
              144  LOAD_METHOD              end
              146  LOAD_CONST               0
              148  CALL_METHOD_1         1  '1 positional argument'
              150  DUP_TOP          
              152  STORE_FAST               'pos'
              154  STORE_FAST               'end'

 L. 376       156  LOAD_GLOBAL              STRING
              158  LOAD_FAST                'contstr'
              160  LOAD_FAST                'line'
              162  LOAD_CONST               None
              164  LOAD_FAST                'end'
              166  BUILD_SLICE_2         2 
              168  BINARY_SUBSCR    
              170  BINARY_ADD       

 L. 377       172  LOAD_FAST                'strstart'
              174  LOAD_FAST                'lnum'
              176  LOAD_FAST                'end'
              178  BUILD_TUPLE_2         2 
              180  LOAD_FAST                'contline'
              182  LOAD_FAST                'line'
              184  BINARY_ADD       
              186  BUILD_TUPLE_5         5 
              188  YIELD_VALUE      
              190  POP_TOP          

 L. 378       192  LOAD_CONST               ('', 0)
              194  UNPACK_SEQUENCE_2     2 
              196  STORE_FAST               'contstr'
              198  STORE_FAST               'needcont'

 L. 379       200  LOAD_CONST               None
              202  STORE_FAST               'contline'
              204  JUMP_FORWARD        890  'to 890'
            206_0  COME_FROM           140  '140'

 L. 380       206  LOAD_FAST                'needcont'
          208_210  POP_JUMP_IF_FALSE   288  'to 288'
              212  LOAD_FAST                'line'
              214  LOAD_CONST               -2
              216  LOAD_CONST               None
              218  BUILD_SLICE_2         2 
              220  BINARY_SUBSCR    
              222  LOAD_STR                 '\\\n'
              224  COMPARE_OP               !=
          226_228  POP_JUMP_IF_FALSE   288  'to 288'
              230  LOAD_FAST                'line'
              232  LOAD_CONST               -3
              234  LOAD_CONST               None
              236  BUILD_SLICE_2         2 
              238  BINARY_SUBSCR    
              240  LOAD_STR                 '\\\r\n'
              242  COMPARE_OP               !=
          244_246  POP_JUMP_IF_FALSE   288  'to 288'

 L. 381       248  LOAD_GLOBAL              ERRORTOKEN
              250  LOAD_FAST                'contstr'
              252  LOAD_FAST                'line'
              254  BINARY_ADD       

 L. 382       256  LOAD_FAST                'strstart'
              258  LOAD_FAST                'lnum'
              260  LOAD_GLOBAL              len
              262  LOAD_FAST                'line'
              264  CALL_FUNCTION_1       1  '1 positional argument'
              266  BUILD_TUPLE_2         2 
              268  LOAD_FAST                'contline'
              270  BUILD_TUPLE_5         5 
              272  YIELD_VALUE      
              274  POP_TOP          

 L. 383       276  LOAD_STR                 ''
              278  STORE_FAST               'contstr'

 L. 384       280  LOAD_CONST               None
              282  STORE_FAST               'contline'

 L. 385       284  CONTINUE             50  'to 50'
              286  JUMP_FORWARD        890  'to 890'
            288_0  COME_FROM           244  '244'
            288_1  COME_FROM           226  '226'
            288_2  COME_FROM           208  '208'

 L. 387       288  LOAD_FAST                'contstr'
              290  LOAD_FAST                'line'
              292  BINARY_ADD       
              294  STORE_FAST               'contstr'

 L. 388       296  LOAD_FAST                'contline'
              298  LOAD_FAST                'line'
              300  BINARY_ADD       
              302  STORE_FAST               'contline'

 L. 389       304  CONTINUE             50  'to 50'
          306_308  JUMP_FORWARD        890  'to 890'
            310_0  COME_FROM           110  '110'

 L. 391       310  LOAD_FAST                'parenlev'
              312  LOAD_CONST               0
              314  COMPARE_OP               ==
          316_318  POP_JUMP_IF_FALSE   866  'to 866'
              320  LOAD_FAST                'continued'
          322_324  POP_JUMP_IF_TRUE    866  'to 866'

 L. 392       326  LOAD_FAST                'line'
          328_330  POP_JUMP_IF_TRUE    334  'to 334'

 L. 392       332  BREAK_LOOP       
            334_0  COME_FROM           328  '328'

 L. 393       334  LOAD_CONST               0
              336  STORE_FAST               'column'

 L. 394       338  SETUP_LOOP          442  'to 442'
            340_0  COME_FROM           436  '436'
              340  LOAD_FAST                'pos'
              342  LOAD_FAST                'max'
              344  COMPARE_OP               <
          346_348  POP_JUMP_IF_FALSE   440  'to 440'

 L. 395       350  LOAD_FAST                'line'
              352  LOAD_FAST                'pos'
              354  BINARY_SUBSCR    
              356  LOAD_STR                 ' '
              358  COMPARE_OP               ==
          360_362  POP_JUMP_IF_FALSE   374  'to 374'

 L. 395       364  LOAD_FAST                'column'
              366  LOAD_CONST               1
              368  BINARY_ADD       
              370  STORE_FAST               'column'
              372  JUMP_FORWARD        428  'to 428'
            374_0  COME_FROM           360  '360'

 L. 396       374  LOAD_FAST                'line'
              376  LOAD_FAST                'pos'
              378  BINARY_SUBSCR    
              380  LOAD_STR                 '\t'
              382  COMPARE_OP               ==
          384_386  POP_JUMP_IF_FALSE   406  'to 406'

 L. 396       388  LOAD_FAST                'column'
              390  LOAD_GLOBAL              tabsize
              392  BINARY_FLOOR_DIVIDE
              394  LOAD_CONST               1
              396  BINARY_ADD       
              398  LOAD_GLOBAL              tabsize
              400  BINARY_MULTIPLY  
              402  STORE_FAST               'column'
              404  JUMP_FORWARD        428  'to 428'
            406_0  COME_FROM           384  '384'

 L. 397       406  LOAD_FAST                'line'
              408  LOAD_FAST                'pos'
              410  BINARY_SUBSCR    
              412  LOAD_STR                 '\x0c'
              414  COMPARE_OP               ==
          416_418  POP_JUMP_IF_FALSE   426  'to 426'

 L. 397       420  LOAD_CONST               0
              422  STORE_FAST               'column'
              424  JUMP_FORWARD        428  'to 428'
            426_0  COME_FROM           416  '416'

 L. 398       426  BREAK_LOOP       
            428_0  COME_FROM           424  '424'
            428_1  COME_FROM           404  '404'
            428_2  COME_FROM           372  '372'

 L. 399       428  LOAD_FAST                'pos'
              430  LOAD_CONST               1
              432  BINARY_ADD       
              434  STORE_FAST               'pos'
          436_438  JUMP_BACK           340  'to 340'
            440_0  COME_FROM           346  '346'
              440  POP_BLOCK        
            442_0  COME_FROM_LOOP      338  '338'

 L. 400       442  LOAD_FAST                'pos'
              444  LOAD_FAST                'max'
              446  COMPARE_OP               ==
          448_450  POP_JUMP_IF_FALSE   454  'to 454'

 L. 400       452  BREAK_LOOP       
            454_0  COME_FROM           448  '448'

 L. 402       454  LOAD_FAST                'stashed'
          456_458  POP_JUMP_IF_FALSE   470  'to 470'

 L. 403       460  LOAD_FAST                'stashed'
              462  YIELD_VALUE      
              464  POP_TOP          

 L. 404       466  LOAD_CONST               None
              468  STORE_FAST               'stashed'
            470_0  COME_FROM           456  '456'

 L. 406       470  LOAD_FAST                'line'
              472  LOAD_FAST                'pos'
              474  BINARY_SUBSCR    
              476  LOAD_STR                 '#\r\n'
              478  COMPARE_OP               in
          480_482  POP_JUMP_IF_FALSE   652  'to 652'

 L. 407       484  LOAD_FAST                'line'
              486  LOAD_FAST                'pos'
              488  BINARY_SUBSCR    
              490  LOAD_STR                 '#'
              492  COMPARE_OP               ==
          494_496  POP_JUMP_IF_FALSE   598  'to 598'

 L. 408       498  LOAD_FAST                'line'
              500  LOAD_FAST                'pos'
              502  LOAD_CONST               None
              504  BUILD_SLICE_2         2 
              506  BINARY_SUBSCR    
              508  LOAD_METHOD              rstrip
              510  LOAD_STR                 '\r\n'
              512  CALL_METHOD_1         1  '1 positional argument'
              514  STORE_FAST               'comment_token'

 L. 409       516  LOAD_FAST                'pos'
              518  LOAD_GLOBAL              len
              520  LOAD_FAST                'comment_token'
              522  CALL_FUNCTION_1       1  '1 positional argument'
              524  BINARY_ADD       
              526  STORE_FAST               'nl_pos'

 L. 410       528  LOAD_GLOBAL              COMMENT
              530  LOAD_FAST                'comment_token'

 L. 411       532  LOAD_FAST                'lnum'
              534  LOAD_FAST                'pos'
              536  BUILD_TUPLE_2         2 
              538  LOAD_FAST                'lnum'
              540  LOAD_FAST                'pos'
              542  LOAD_GLOBAL              len
              544  LOAD_FAST                'comment_token'
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  BINARY_ADD       
              550  BUILD_TUPLE_2         2 
              552  LOAD_FAST                'line'
              554  BUILD_TUPLE_5         5 
              556  YIELD_VALUE      
              558  POP_TOP          

 L. 412       560  LOAD_GLOBAL              NL
              562  LOAD_FAST                'line'
              564  LOAD_FAST                'nl_pos'
              566  LOAD_CONST               None
              568  BUILD_SLICE_2         2 
              570  BINARY_SUBSCR    

 L. 413       572  LOAD_FAST                'lnum'
              574  LOAD_FAST                'nl_pos'
              576  BUILD_TUPLE_2         2 
              578  LOAD_FAST                'lnum'
              580  LOAD_GLOBAL              len
              582  LOAD_FAST                'line'
              584  CALL_FUNCTION_1       1  '1 positional argument'
              586  BUILD_TUPLE_2         2 
              588  LOAD_FAST                'line'
              590  BUILD_TUPLE_5         5 
              592  YIELD_VALUE      
              594  POP_TOP          
              596  JUMP_BACK            50  'to 50'
            598_0  COME_FROM           494  '494'

 L. 415       598  LOAD_GLOBAL              NL
              600  LOAD_GLOBAL              COMMENT
              602  BUILD_TUPLE_2         2 
              604  LOAD_FAST                'line'
              606  LOAD_FAST                'pos'
              608  BINARY_SUBSCR    
              610  LOAD_STR                 '#'
              612  COMPARE_OP               ==
              614  BINARY_SUBSCR    
              616  LOAD_FAST                'line'
              618  LOAD_FAST                'pos'
              620  LOAD_CONST               None
              622  BUILD_SLICE_2         2 
              624  BINARY_SUBSCR    

 L. 416       626  LOAD_FAST                'lnum'
              628  LOAD_FAST                'pos'
              630  BUILD_TUPLE_2         2 
              632  LOAD_FAST                'lnum'
              634  LOAD_GLOBAL              len
              636  LOAD_FAST                'line'
              638  CALL_FUNCTION_1       1  '1 positional argument'
              640  BUILD_TUPLE_2         2 
              642  LOAD_FAST                'line'
              644  BUILD_TUPLE_5         5 
              646  YIELD_VALUE      
              648  POP_TOP          

 L. 417       650  CONTINUE             50  'to 50'
            652_0  COME_FROM           480  '480'

 L. 419       652  LOAD_FAST                'column'
              654  LOAD_FAST                'indents'
              656  LOAD_CONST               -1
              658  BINARY_SUBSCR    
              660  COMPARE_OP               >
          662_664  POP_JUMP_IF_FALSE   708  'to 708'

 L. 420       666  LOAD_FAST                'indents'
              668  LOAD_METHOD              append
              670  LOAD_FAST                'column'
              672  CALL_METHOD_1         1  '1 positional argument'
              674  POP_TOP          

 L. 421       676  LOAD_GLOBAL              INDENT
              678  LOAD_FAST                'line'
              680  LOAD_CONST               None
              682  LOAD_FAST                'pos'
              684  BUILD_SLICE_2         2 
              686  BINARY_SUBSCR    
              688  LOAD_FAST                'lnum'
              690  LOAD_CONST               0
              692  BUILD_TUPLE_2         2 
              694  LOAD_FAST                'lnum'
              696  LOAD_FAST                'pos'
              698  BUILD_TUPLE_2         2 
              700  LOAD_FAST                'line'
              702  BUILD_TUPLE_5         5 
              704  YIELD_VALUE      
              706  POP_TOP          
            708_0  COME_FROM           662  '662'

 L. 422       708  SETUP_LOOP          826  'to 826'
            710_0  COME_FROM           820  '820'
              710  LOAD_FAST                'column'
              712  LOAD_FAST                'indents'
              714  LOAD_CONST               -1
              716  BINARY_SUBSCR    
              718  COMPARE_OP               <
          720_722  POP_JUMP_IF_FALSE   824  'to 824'

 L. 423       724  LOAD_FAST                'column'
              726  LOAD_FAST                'indents'
              728  COMPARE_OP               not-in
          730_732  POP_JUMP_IF_FALSE   752  'to 752'

 L. 424       734  LOAD_GLOBAL              IndentationError

 L. 425       736  LOAD_STR                 'unindent does not match any outer indentation level'

 L. 426       738  LOAD_STR                 '<tokenize>'
              740  LOAD_FAST                'lnum'
              742  LOAD_FAST                'pos'
              744  LOAD_FAST                'line'
              746  BUILD_TUPLE_4         4 
              748  CALL_FUNCTION_2       2  '2 positional arguments'
              750  RAISE_VARARGS_1       1  'exception instance'
            752_0  COME_FROM           730  '730'

 L. 427       752  LOAD_FAST                'indents'
              754  LOAD_CONST               None
              756  LOAD_CONST               -1
              758  BUILD_SLICE_2         2 
              760  BINARY_SUBSCR    
              762  STORE_FAST               'indents'

 L. 429       764  LOAD_FAST                'async_def'
          766_768  POP_JUMP_IF_FALSE   796  'to 796'
              770  LOAD_FAST                'async_def_indent'
              772  LOAD_FAST                'indents'
              774  LOAD_CONST               -1
              776  BINARY_SUBSCR    
              778  COMPARE_OP               >=
          780_782  POP_JUMP_IF_FALSE   796  'to 796'

 L. 430       784  LOAD_CONST               False
              786  STORE_FAST               'async_def'

 L. 431       788  LOAD_CONST               False
              790  STORE_FAST               'async_def_nl'

 L. 432       792  LOAD_CONST               0
              794  STORE_FAST               'async_def_indent'
            796_0  COME_FROM           780  '780'
            796_1  COME_FROM           766  '766'

 L. 434       796  LOAD_GLOBAL              DEDENT
              798  LOAD_STR                 ''
              800  LOAD_FAST                'lnum'
              802  LOAD_FAST                'pos'
              804  BUILD_TUPLE_2         2 
              806  LOAD_FAST                'lnum'
              808  LOAD_FAST                'pos'
              810  BUILD_TUPLE_2         2 
              812  LOAD_FAST                'line'
              814  BUILD_TUPLE_5         5 
              816  YIELD_VALUE      
              818  POP_TOP          
          820_822  JUMP_BACK           710  'to 710'
            824_0  COME_FROM           720  '720'
              824  POP_BLOCK        
            826_0  COME_FROM_LOOP      708  '708'

 L. 436       826  LOAD_FAST                'async_def'
          828_830  POP_JUMP_IF_FALSE   890  'to 890'
              832  LOAD_FAST                'async_def_nl'
          834_836  POP_JUMP_IF_FALSE   890  'to 890'
              838  LOAD_FAST                'async_def_indent'
              840  LOAD_FAST                'indents'
              842  LOAD_CONST               -1
              844  BINARY_SUBSCR    
              846  COMPARE_OP               >=
          848_850  POP_JUMP_IF_FALSE   890  'to 890'

 L. 437       852  LOAD_CONST               False
              854  STORE_FAST               'async_def'

 L. 438       856  LOAD_CONST               False
              858  STORE_FAST               'async_def_nl'

 L. 439       860  LOAD_CONST               0
              862  STORE_FAST               'async_def_indent'
              864  JUMP_FORWARD        890  'to 890'
            866_0  COME_FROM           322  '322'
            866_1  COME_FROM           316  '316'

 L. 442       866  LOAD_FAST                'line'
          868_870  POP_JUMP_IF_TRUE    886  'to 886'

 L. 443       872  LOAD_GLOBAL              TokenError
              874  LOAD_STR                 'EOF in multi-line statement'
              876  LOAD_FAST                'lnum'
              878  LOAD_CONST               0
              880  BUILD_TUPLE_2         2 
              882  CALL_FUNCTION_2       2  '2 positional arguments'
              884  RAISE_VARARGS_1       1  'exception instance'
            886_0  COME_FROM           868  '868'

 L. 444       886  LOAD_CONST               0
              888  STORE_FAST               'continued'
            890_0  COME_FROM           864  '864'
            890_1  COME_FROM           848  '848'
            890_2  COME_FROM           834  '834'
            890_3  COME_FROM           828  '828'
            890_4  COME_FROM           306  '306'
            890_5  COME_FROM           286  '286'
            890_6  COME_FROM           204  '204'

 L. 446   890_892  SETUP_LOOP         1848  'to 1848'
            894_0  COME_FROM          1842  '1842'
            894_1  COME_FROM          1800  '1800'
            894_2  COME_FROM          1558  '1558'
            894_3  COME_FROM          1520  '1520'
              894  LOAD_FAST                'pos'
              896  LOAD_FAST                'max'
              898  COMPARE_OP               <
          900_902  POP_JUMP_IF_FALSE  1846  'to 1846'

 L. 447       904  LOAD_GLOBAL              pseudoprog
              906  LOAD_METHOD              match
              908  LOAD_FAST                'line'
              910  LOAD_FAST                'pos'
              912  CALL_METHOD_2         2  '2 positional arguments'
              914  STORE_FAST               'pseudomatch'

 L. 448       916  LOAD_FAST                'pseudomatch'
          918_920  POP_JUMP_IF_FALSE  1802  'to 1802'

 L. 449       922  LOAD_FAST                'pseudomatch'
              924  LOAD_METHOD              span
              926  LOAD_CONST               1
              928  CALL_METHOD_1         1  '1 positional argument'
              930  UNPACK_SEQUENCE_2     2 
              932  STORE_FAST               'start'
              934  STORE_FAST               'end'

 L. 450       936  LOAD_FAST                'lnum'
              938  LOAD_FAST                'start'
              940  BUILD_TUPLE_2         2 
              942  LOAD_FAST                'lnum'
              944  LOAD_FAST                'end'
              946  BUILD_TUPLE_2         2 
              948  LOAD_FAST                'end'
              950  ROT_THREE        
              952  ROT_TWO          
              954  STORE_FAST               'spos'
              956  STORE_FAST               'epos'
              958  STORE_FAST               'pos'

 L. 451       960  LOAD_FAST                'line'
              962  LOAD_FAST                'start'
              964  LOAD_FAST                'end'
              966  BUILD_SLICE_2         2 
              968  BINARY_SUBSCR    
              970  LOAD_FAST                'line'
              972  LOAD_FAST                'start'
              974  BINARY_SUBSCR    
              976  ROT_TWO          
              978  STORE_FAST               'token'
              980  STORE_FAST               'initial'

 L. 453       982  LOAD_FAST                'initial'
              984  LOAD_GLOBAL              string
              986  LOAD_ATTR                digits
              988  COMPARE_OP               in
          990_992  POP_JUMP_IF_TRUE   1014  'to 1014'

 L. 454       994  LOAD_FAST                'initial'
              996  LOAD_STR                 '.'
              998  COMPARE_OP               ==
         1000_1002  POP_JUMP_IF_FALSE  1034  'to 1034'
             1004  LOAD_FAST                'token'
             1006  LOAD_STR                 '.'
             1008  COMPARE_OP               !=
         1010_1012  POP_JUMP_IF_FALSE  1034  'to 1034'
           1014_0  COME_FROM           990  '990'

 L. 455      1014  LOAD_GLOBAL              NUMBER
             1016  LOAD_FAST                'token'
             1018  LOAD_FAST                'spos'
             1020  LOAD_FAST                'epos'
             1022  LOAD_FAST                'line'
             1024  BUILD_TUPLE_5         5 
             1026  YIELD_VALUE      
             1028  POP_TOP          
         1030_1032  JUMP_FORWARD       1842  'to 1842'
           1034_0  COME_FROM          1010  '1010'
           1034_1  COME_FROM          1000  '1000'

 L. 456      1034  LOAD_FAST                'initial'
             1036  LOAD_STR                 '\r\n'
             1038  COMPARE_OP               in
         1040_1042  POP_JUMP_IF_FALSE  1110  'to 1110'

 L. 457      1044  LOAD_GLOBAL              NEWLINE
             1046  STORE_FAST               'newline'

 L. 458      1048  LOAD_FAST                'parenlev'
             1050  LOAD_CONST               0
             1052  COMPARE_OP               >
         1054_1056  POP_JUMP_IF_FALSE  1064  'to 1064'

 L. 459      1058  LOAD_GLOBAL              NL
             1060  STORE_FAST               'newline'
             1062  JUMP_FORWARD       1074  'to 1074'
           1064_0  COME_FROM          1054  '1054'

 L. 460      1064  LOAD_FAST                'async_def'
         1066_1068  POP_JUMP_IF_FALSE  1074  'to 1074'

 L. 461      1070  LOAD_CONST               True
             1072  STORE_FAST               'async_def_nl'
           1074_0  COME_FROM          1066  '1066'
           1074_1  COME_FROM          1062  '1062'

 L. 462      1074  LOAD_FAST                'stashed'
         1076_1078  POP_JUMP_IF_FALSE  1090  'to 1090'

 L. 463      1080  LOAD_FAST                'stashed'
             1082  YIELD_VALUE      
             1084  POP_TOP          

 L. 464      1086  LOAD_CONST               None
             1088  STORE_FAST               'stashed'
           1090_0  COME_FROM          1076  '1076'

 L. 465      1090  LOAD_FAST                'newline'
             1092  LOAD_FAST                'token'
             1094  LOAD_FAST                'spos'
             1096  LOAD_FAST                'epos'
             1098  LOAD_FAST                'line'
             1100  BUILD_TUPLE_5         5 
             1102  YIELD_VALUE      
             1104  POP_TOP          
         1106_1108  JUMP_FORWARD       1842  'to 1842'
           1110_0  COME_FROM          1040  '1040'

 L. 467      1110  LOAD_FAST                'initial'
             1112  LOAD_STR                 '#'
             1114  COMPARE_OP               ==
         1116_1118  POP_JUMP_IF_FALSE  1172  'to 1172'

 L. 468      1120  LOAD_FAST                'token'
             1122  LOAD_METHOD              endswith
             1124  LOAD_STR                 '\n'
             1126  CALL_METHOD_1         1  '1 positional argument'
         1128_1130  POP_JUMP_IF_FALSE  1136  'to 1136'
             1132  LOAD_GLOBAL              AssertionError
             1134  RAISE_VARARGS_1       1  'exception instance'
           1136_0  COME_FROM          1128  '1128'

 L. 469      1136  LOAD_FAST                'stashed'
         1138_1140  POP_JUMP_IF_FALSE  1152  'to 1152'

 L. 470      1142  LOAD_FAST                'stashed'
             1144  YIELD_VALUE      
             1146  POP_TOP          

 L. 471      1148  LOAD_CONST               None
             1150  STORE_FAST               'stashed'
           1152_0  COME_FROM          1138  '1138'

 L. 472      1152  LOAD_GLOBAL              COMMENT
             1154  LOAD_FAST                'token'
             1156  LOAD_FAST                'spos'
             1158  LOAD_FAST                'epos'
             1160  LOAD_FAST                'line'
             1162  BUILD_TUPLE_5         5 
             1164  YIELD_VALUE      
             1166  POP_TOP          
         1168_1170  JUMP_FORWARD       1842  'to 1842'
           1172_0  COME_FROM          1116  '1116'

 L. 473      1172  LOAD_FAST                'token'
             1174  LOAD_GLOBAL              triple_quoted
             1176  COMPARE_OP               in
         1178_1180  POP_JUMP_IF_FALSE  1298  'to 1298'

 L. 474      1182  LOAD_GLOBAL              endprogs
             1184  LOAD_FAST                'token'
             1186  BINARY_SUBSCR    
             1188  STORE_FAST               'endprog'

 L. 475      1190  LOAD_FAST                'endprog'
             1192  LOAD_METHOD              match
             1194  LOAD_FAST                'line'
             1196  LOAD_FAST                'pos'
             1198  CALL_METHOD_2         2  '2 positional arguments'
             1200  STORE_FAST               'endmatch'

 L. 476      1202  LOAD_FAST                'endmatch'
         1204_1206  POP_JUMP_IF_FALSE  1268  'to 1268'

 L. 477      1208  LOAD_FAST                'endmatch'
             1210  LOAD_METHOD              end
             1212  LOAD_CONST               0
             1214  CALL_METHOD_1         1  '1 positional argument'
             1216  STORE_FAST               'pos'

 L. 478      1218  LOAD_FAST                'line'
             1220  LOAD_FAST                'start'
             1222  LOAD_FAST                'pos'
             1224  BUILD_SLICE_2         2 
             1226  BINARY_SUBSCR    
             1228  STORE_FAST               'token'

 L. 479      1230  LOAD_FAST                'stashed'
         1232_1234  POP_JUMP_IF_FALSE  1246  'to 1246'

 L. 480      1236  LOAD_FAST                'stashed'
             1238  YIELD_VALUE      
             1240  POP_TOP          

 L. 481      1242  LOAD_CONST               None
             1244  STORE_FAST               'stashed'
           1246_0  COME_FROM          1232  '1232'

 L. 482      1246  LOAD_GLOBAL              STRING
             1248  LOAD_FAST                'token'
             1250  LOAD_FAST                'spos'
             1252  LOAD_FAST                'lnum'
             1254  LOAD_FAST                'pos'
             1256  BUILD_TUPLE_2         2 
             1258  LOAD_FAST                'line'
             1260  BUILD_TUPLE_5         5 
             1262  YIELD_VALUE      
             1264  POP_TOP          
             1266  JUMP_FORWARD       1842  'to 1842'
           1268_0  COME_FROM          1204  '1204'

 L. 484      1268  LOAD_FAST                'lnum'
             1270  LOAD_FAST                'start'
             1272  BUILD_TUPLE_2         2 
             1274  STORE_FAST               'strstart'

 L. 485      1276  LOAD_FAST                'line'
             1278  LOAD_FAST                'start'
             1280  LOAD_CONST               None
             1282  BUILD_SLICE_2         2 
             1284  BINARY_SUBSCR    
             1286  STORE_FAST               'contstr'

 L. 486      1288  LOAD_FAST                'line'
             1290  STORE_FAST               'contline'

 L. 487      1292  BREAK_LOOP       
         1294_1296  JUMP_FORWARD       1842  'to 1842'
           1298_0  COME_FROM          1178  '1178'

 L. 488      1298  LOAD_FAST                'initial'
             1300  LOAD_GLOBAL              single_quoted
             1302  COMPARE_OP               in
         1304_1306  POP_JUMP_IF_TRUE   1344  'to 1344'

 L. 489      1308  LOAD_FAST                'token'
             1310  LOAD_CONST               None
             1312  LOAD_CONST               2
             1314  BUILD_SLICE_2         2 
             1316  BINARY_SUBSCR    
             1318  LOAD_GLOBAL              single_quoted
             1320  COMPARE_OP               in
         1322_1324  POP_JUMP_IF_TRUE   1344  'to 1344'

 L. 490      1326  LOAD_FAST                'token'
             1328  LOAD_CONST               None
             1330  LOAD_CONST               3
             1332  BUILD_SLICE_2         2 
             1334  BINARY_SUBSCR    
             1336  LOAD_GLOBAL              single_quoted
             1338  COMPARE_OP               in
         1340_1342  POP_JUMP_IF_FALSE  1464  'to 1464'
           1344_0  COME_FROM          1322  '1322'
           1344_1  COME_FROM          1304  '1304'

 L. 491      1344  LOAD_FAST                'token'
             1346  LOAD_CONST               -1
             1348  BINARY_SUBSCR    
             1350  LOAD_STR                 '\n'
             1352  COMPARE_OP               ==
         1354_1356  POP_JUMP_IF_FALSE  1428  'to 1428'

 L. 492      1358  LOAD_FAST                'lnum'
             1360  LOAD_FAST                'start'
             1362  BUILD_TUPLE_2         2 
             1364  STORE_FAST               'strstart'

 L. 493      1366  LOAD_GLOBAL              endprogs
             1368  LOAD_FAST                'initial'
             1370  BINARY_SUBSCR    
         1372_1374  JUMP_IF_TRUE_OR_POP  1400  'to 1400'
             1376  LOAD_GLOBAL              endprogs
             1378  LOAD_FAST                'token'
             1380  LOAD_CONST               1
             1382  BINARY_SUBSCR    
             1384  BINARY_SUBSCR    
         1386_1388  JUMP_IF_TRUE_OR_POP  1400  'to 1400'

 L. 494      1390  LOAD_GLOBAL              endprogs
             1392  LOAD_FAST                'token'
             1394  LOAD_CONST               2
             1396  BINARY_SUBSCR    
             1398  BINARY_SUBSCR    
           1400_0  COME_FROM          1386  '1386'
           1400_1  COME_FROM          1372  '1372'
             1400  STORE_FAST               'endprog'

 L. 495      1402  LOAD_FAST                'line'
             1404  LOAD_FAST                'start'
             1406  LOAD_CONST               None
             1408  BUILD_SLICE_2         2 
             1410  BINARY_SUBSCR    
             1412  LOAD_CONST               1
             1414  ROT_TWO          
             1416  STORE_FAST               'contstr'
             1418  STORE_FAST               'needcont'

 L. 496      1420  LOAD_FAST                'line'
             1422  STORE_FAST               'contline'

 L. 497      1424  BREAK_LOOP       
             1426  JUMP_FORWARD       1842  'to 1842'
           1428_0  COME_FROM          1354  '1354'

 L. 499      1428  LOAD_FAST                'stashed'
         1430_1432  POP_JUMP_IF_FALSE  1444  'to 1444'

 L. 500      1434  LOAD_FAST                'stashed'
             1436  YIELD_VALUE      
             1438  POP_TOP          

 L. 501      1440  LOAD_CONST               None
             1442  STORE_FAST               'stashed'
           1444_0  COME_FROM          1430  '1430'

 L. 502      1444  LOAD_GLOBAL              STRING
             1446  LOAD_FAST                'token'
             1448  LOAD_FAST                'spos'
             1450  LOAD_FAST                'epos'
             1452  LOAD_FAST                'line'
             1454  BUILD_TUPLE_5         5 
             1456  YIELD_VALUE      
             1458  POP_TOP          
         1460_1462  JUMP_FORWARD       1842  'to 1842'
           1464_0  COME_FROM          1340  '1340'

 L. 503      1464  LOAD_FAST                'initial'
             1466  LOAD_METHOD              isidentifier
             1468  CALL_METHOD_0         0  '0 positional arguments'
         1470_1472  POP_JUMP_IF_FALSE  1678  'to 1678'

 L. 504      1474  LOAD_FAST                'token'
             1476  LOAD_CONST               ('async', 'await')
             1478  COMPARE_OP               in
         1480_1482  POP_JUMP_IF_FALSE  1524  'to 1524'

 L. 505      1484  LOAD_FAST                'async_def'
         1486_1488  POP_JUMP_IF_FALSE  1524  'to 1524'

 L. 506      1490  LOAD_FAST                'token'
             1492  LOAD_STR                 'async'
             1494  COMPARE_OP               ==
         1496_1498  POP_JUMP_IF_FALSE  1504  'to 1504'
             1500  LOAD_GLOBAL              ASYNC
             1502  JUMP_FORWARD       1506  'to 1506'
           1504_0  COME_FROM          1496  '1496'
             1504  LOAD_GLOBAL              AWAIT
           1506_0  COME_FROM          1502  '1502'

 L. 507      1506  LOAD_FAST                'token'
             1508  LOAD_FAST                'spos'
             1510  LOAD_FAST                'epos'
             1512  LOAD_FAST                'line'
             1514  BUILD_TUPLE_5         5 
             1516  YIELD_VALUE      
             1518  POP_TOP          

 L. 508  1520_1522  CONTINUE            894  'to 894'
           1524_0  COME_FROM          1486  '1486'
           1524_1  COME_FROM          1480  '1480'

 L. 510      1524  LOAD_GLOBAL              NAME
             1526  LOAD_FAST                'token'
             1528  LOAD_FAST                'spos'
             1530  LOAD_FAST                'epos'
             1532  LOAD_FAST                'line'
             1534  BUILD_TUPLE_5         5 
             1536  STORE_FAST               'tok'

 L. 511      1538  LOAD_FAST                'token'
             1540  LOAD_STR                 'async'
             1542  COMPARE_OP               ==
         1544_1546  POP_JUMP_IF_FALSE  1562  'to 1562'
             1548  LOAD_FAST                'stashed'
         1550_1552  POP_JUMP_IF_TRUE   1562  'to 1562'

 L. 512      1554  LOAD_FAST                'tok'
             1556  STORE_FAST               'stashed'

 L. 513  1558_1560  CONTINUE            894  'to 894'
           1562_0  COME_FROM          1550  '1550'
           1562_1  COME_FROM          1544  '1544'

 L. 515      1562  LOAD_FAST                'token'
             1564  LOAD_STR                 'def'
             1566  COMPARE_OP               ==
         1568_1570  POP_JUMP_IF_FALSE  1654  'to 1654'

 L. 516      1572  LOAD_FAST                'stashed'
         1574_1576  POP_JUMP_IF_FALSE  1654  'to 1654'

 L. 517      1578  LOAD_FAST                'stashed'
             1580  LOAD_CONST               0
             1582  BINARY_SUBSCR    
             1584  LOAD_GLOBAL              NAME
             1586  COMPARE_OP               ==
         1588_1590  POP_JUMP_IF_FALSE  1654  'to 1654'

 L. 518      1592  LOAD_FAST                'stashed'
             1594  LOAD_CONST               1
             1596  BINARY_SUBSCR    
             1598  LOAD_STR                 'async'
             1600  COMPARE_OP               ==
         1602_1604  POP_JUMP_IF_FALSE  1654  'to 1654'

 L. 520      1606  LOAD_CONST               True
             1608  STORE_FAST               'async_def'

 L. 521      1610  LOAD_FAST                'indents'
             1612  LOAD_CONST               -1
             1614  BINARY_SUBSCR    
             1616  STORE_FAST               'async_def_indent'

 L. 523      1618  LOAD_GLOBAL              ASYNC
             1620  LOAD_FAST                'stashed'
             1622  LOAD_CONST               1
             1624  BINARY_SUBSCR    

 L. 524      1626  LOAD_FAST                'stashed'
             1628  LOAD_CONST               2
             1630  BINARY_SUBSCR    
             1632  LOAD_FAST                'stashed'
             1634  LOAD_CONST               3
             1636  BINARY_SUBSCR    

 L. 525      1638  LOAD_FAST                'stashed'
             1640  LOAD_CONST               4
             1642  BINARY_SUBSCR    
             1644  BUILD_TUPLE_5         5 
             1646  YIELD_VALUE      
             1648  POP_TOP          

 L. 526      1650  LOAD_CONST               None
             1652  STORE_FAST               'stashed'
           1654_0  COME_FROM          1602  '1602'
           1654_1  COME_FROM          1588  '1588'
           1654_2  COME_FROM          1574  '1574'
           1654_3  COME_FROM          1568  '1568'

 L. 528      1654  LOAD_FAST                'stashed'
         1656_1658  POP_JUMP_IF_FALSE  1670  'to 1670'

 L. 529      1660  LOAD_FAST                'stashed'
             1662  YIELD_VALUE      
             1664  POP_TOP          

 L. 530      1666  LOAD_CONST               None
             1668  STORE_FAST               'stashed'
           1670_0  COME_FROM          1656  '1656'

 L. 532      1670  LOAD_FAST                'tok'
             1672  YIELD_VALUE      
             1674  POP_TOP          
             1676  JUMP_FORWARD       1800  'to 1800'
           1678_0  COME_FROM          1470  '1470'

 L. 533      1678  LOAD_FAST                'initial'
             1680  LOAD_STR                 '\\'
             1682  COMPARE_OP               ==
         1684_1686  POP_JUMP_IF_FALSE  1730  'to 1730'

 L. 535      1688  LOAD_FAST                'stashed'
         1690_1692  POP_JUMP_IF_FALSE  1704  'to 1704'

 L. 536      1694  LOAD_FAST                'stashed'
             1696  YIELD_VALUE      
             1698  POP_TOP          

 L. 537      1700  LOAD_CONST               None
             1702  STORE_FAST               'stashed'
           1704_0  COME_FROM          1690  '1690'

 L. 538      1704  LOAD_GLOBAL              NL
             1706  LOAD_FAST                'token'
             1708  LOAD_FAST                'spos'
             1710  LOAD_FAST                'lnum'
             1712  LOAD_FAST                'pos'
             1714  BUILD_TUPLE_2         2 
             1716  LOAD_FAST                'line'
             1718  BUILD_TUPLE_5         5 
             1720  YIELD_VALUE      
             1722  POP_TOP          

 L. 539      1724  LOAD_CONST               1
             1726  STORE_FAST               'continued'
             1728  JUMP_FORWARD       1800  'to 1800'
           1730_0  COME_FROM          1684  '1684'

 L. 541      1730  LOAD_FAST                'initial'
             1732  LOAD_STR                 '([{'
             1734  COMPARE_OP               in
         1736_1738  POP_JUMP_IF_FALSE  1750  'to 1750'

 L. 541      1740  LOAD_FAST                'parenlev'
             1742  LOAD_CONST               1
             1744  BINARY_ADD       
             1746  STORE_FAST               'parenlev'
             1748  JUMP_FORWARD       1768  'to 1768'
           1750_0  COME_FROM          1736  '1736'

 L. 542      1750  LOAD_FAST                'initial'
             1752  LOAD_STR                 ')]}'
             1754  COMPARE_OP               in
         1756_1758  POP_JUMP_IF_FALSE  1768  'to 1768'

 L. 542      1760  LOAD_FAST                'parenlev'
             1762  LOAD_CONST               1
             1764  BINARY_SUBTRACT  
             1766  STORE_FAST               'parenlev'
           1768_0  COME_FROM          1756  '1756'
           1768_1  COME_FROM          1748  '1748'

 L. 543      1768  LOAD_FAST                'stashed'
         1770_1772  POP_JUMP_IF_FALSE  1784  'to 1784'

 L. 544      1774  LOAD_FAST                'stashed'
             1776  YIELD_VALUE      
             1778  POP_TOP          

 L. 545      1780  LOAD_CONST               None
             1782  STORE_FAST               'stashed'
           1784_0  COME_FROM          1770  '1770'

 L. 546      1784  LOAD_GLOBAL              OP
             1786  LOAD_FAST                'token'
             1788  LOAD_FAST                'spos'
             1790  LOAD_FAST                'epos'
             1792  LOAD_FAST                'line'
             1794  BUILD_TUPLE_5         5 
             1796  YIELD_VALUE      
             1798  POP_TOP          
           1800_0  COME_FROM          1728  '1728'
           1800_1  COME_FROM          1676  '1676'
             1800  JUMP_BACK           894  'to 894'
           1802_0  COME_FROM           918  '918'

 L. 548      1802  LOAD_GLOBAL              ERRORTOKEN
             1804  LOAD_FAST                'line'
             1806  LOAD_FAST                'pos'
             1808  BINARY_SUBSCR    

 L. 549      1810  LOAD_FAST                'lnum'
             1812  LOAD_FAST                'pos'
             1814  BUILD_TUPLE_2         2 
             1816  LOAD_FAST                'lnum'
             1818  LOAD_FAST                'pos'
             1820  LOAD_CONST               1
             1822  BINARY_ADD       
             1824  BUILD_TUPLE_2         2 
             1826  LOAD_FAST                'line'
             1828  BUILD_TUPLE_5         5 
             1830  YIELD_VALUE      
             1832  POP_TOP          

 L. 550      1834  LOAD_FAST                'pos'
             1836  LOAD_CONST               1
             1838  BINARY_ADD       
             1840  STORE_FAST               'pos'
           1842_0  COME_FROM          1460  '1460'
           1842_1  COME_FROM          1426  '1426'
           1842_2  COME_FROM          1294  '1294'
           1842_3  COME_FROM          1266  '1266'
           1842_4  COME_FROM          1168  '1168'
           1842_5  COME_FROM          1106  '1106'
           1842_6  COME_FROM          1030  '1030'
         1842_1844  JUMP_BACK           894  'to 894'
           1846_0  COME_FROM           900  '900'
             1846  POP_BLOCK        
           1848_0  COME_FROM_LOOP      890  '890'
             1848  JUMP_BACK            50  'to 50'
             1850  POP_BLOCK        
           1852_0  COME_FROM_LOOP       46  '46'

 L. 552      1852  LOAD_FAST                'stashed'
         1854_1856  POP_JUMP_IF_FALSE  1868  'to 1868'

 L. 553      1858  LOAD_FAST                'stashed'
             1860  YIELD_VALUE      
             1862  POP_TOP          

 L. 554      1864  LOAD_CONST               None
             1866  STORE_FAST               'stashed'
           1868_0  COME_FROM          1854  '1854'

 L. 556      1868  SETUP_LOOP         1916  'to 1916'
             1870  LOAD_FAST                'indents'
             1872  LOAD_CONST               1
             1874  LOAD_CONST               None
             1876  BUILD_SLICE_2         2 
             1878  BINARY_SUBSCR    
             1880  GET_ITER         
           1882_0  COME_FROM          1910  '1910'
             1882  FOR_ITER           1914  'to 1914'
             1884  STORE_FAST               'indent'

 L. 557      1886  LOAD_GLOBAL              DEDENT
             1888  LOAD_STR                 ''
             1890  LOAD_FAST                'lnum'
             1892  LOAD_CONST               0
             1894  BUILD_TUPLE_2         2 
             1896  LOAD_FAST                'lnum'
             1898  LOAD_CONST               0
             1900  BUILD_TUPLE_2         2 
             1902  LOAD_STR                 ''
             1904  BUILD_TUPLE_5         5 
             1906  YIELD_VALUE      
             1908  POP_TOP          
         1910_1912  JUMP_BACK          1882  'to 1882'
             1914  POP_BLOCK        
           1916_0  COME_FROM_LOOP     1868  '1868'

 L. 558      1916  LOAD_GLOBAL              ENDMARKER
             1918  LOAD_STR                 ''
             1920  LOAD_FAST                'lnum'
             1922  LOAD_CONST               0
             1924  BUILD_TUPLE_2         2 
             1926  LOAD_FAST                'lnum'
             1928  LOAD_CONST               0
             1930  BUILD_TUPLE_2         2 
             1932  LOAD_STR                 ''
             1934  BUILD_TUPLE_5         5 
             1936  YIELD_VALUE      
             1938  POP_TOP          

Parse error at or near `JUMP_FORWARD' instruction at offset 306_308


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        tokenize(open(sys.argv[1]).readline)
    else:
        tokenize(sys.stdin.readline)