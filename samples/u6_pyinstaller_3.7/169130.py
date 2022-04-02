# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: tokenize.py
"""Tokenization help for Python programs.

tokenize(readline) is a generator that breaks a stream of bytes into
Python tokens.  It decodes the bytes according to PEP-0263 for
determining source file encoding.

It accepts a readline-like method which is called repeatedly to get the
next line of input (or b"" for EOF).  It generates 5-tuples with these
members:

    the token type (see token.py)
    the token (a string)
    the starting (row, column) indices of the token (a 2-tuple of ints)
    the ending (row, column) indices of the token (a 2-tuple of ints)
    the original line (string)

It is designed to match the working of the Python tokenizer exactly, except
that it produces COMMENT tokens for comments and gives type OP for all
operators.  Additionally, all token lists start with an ENCODING token
which tells you which encoding was used to decode the bytes stream.
"""
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__credits__ = 'GvR, ESR, Tim Peters, Thomas Wouters, Fred Drake, Skip Montanaro, Raymond Hettinger, Trent Nelson, Michael Foord'
from builtins import open as _builtin_open
from codecs import lookup, BOM_UTF8
import collections
from io import TextIOWrapper
from itertools import chain
import itertools as _itertools, re, sys
from token import *
cookie_re = re.compile('^[ \\t\\f]*#.*?coding[:=][ \\t]*([-\\w.]+)', re.ASCII)
blank_re = re.compile(b'^[ \\t\\f]*(?:[#\\r\\n]|$)', re.ASCII)
import token
__all__ = token.__all__ + ['tokenize', 'detect_encoding',
 'untokenize', 'TokenInfo']
del token
EXACT_TOKEN_TYPES = {'(':LPAR, 
 ')':RPAR, 
 '[':LSQB, 
 ']':RSQB, 
 ':':COLON, 
 ',':COMMA, 
 ';':SEMI, 
 '+':PLUS, 
 '-':MINUS, 
 '*':STAR, 
 '/':SLASH, 
 '|':VBAR, 
 '&':AMPER, 
 '<':LESS, 
 '>':GREATER, 
 '=':EQUAL, 
 '.':DOT, 
 '%':PERCENT, 
 '{':LBRACE, 
 '}':RBRACE, 
 '==':EQEQUAL, 
 '!=':NOTEQUAL, 
 '<=':LESSEQUAL, 
 '>=':GREATEREQUAL, 
 '~':TILDE, 
 '^':CIRCUMFLEX, 
 '<<':LEFTSHIFT, 
 '>>':RIGHTSHIFT, 
 '**':DOUBLESTAR, 
 '+=':PLUSEQUAL, 
 '-=':MINEQUAL, 
 '*=':STAREQUAL, 
 '/=':SLASHEQUAL, 
 '%=':PERCENTEQUAL, 
 '&=':AMPEREQUAL, 
 '|=':VBAREQUAL, 
 '^=':CIRCUMFLEXEQUAL, 
 '<<=':LEFTSHIFTEQUAL, 
 '>>=':RIGHTSHIFTEQUAL, 
 '**=':DOUBLESTAREQUAL, 
 '//':DOUBLESLASH, 
 '//=':DOUBLESLASHEQUAL, 
 '...':ELLIPSIS, 
 '->':RARROW, 
 '@':AT, 
 '@=':ATEQUAL}

class TokenInfo(collections.namedtuple('TokenInfo', 'type string start end line')):

    def __repr__(self):
        annotated_type = '%d (%s)' % (self.type, tok_name[self.type])
        return 'TokenInfo(type=%s, string=%r, start=%r, end=%r, line=%r)' % self._replace(type=annotated_type)

    @property
    def exact_type(self):
        if self.type == OP:
            if self.string in EXACT_TOKEN_TYPES:
                return EXACT_TOKEN_TYPES[self.string]
        return self.type


def group(*choices):
    return '(' + '|'.join(choices) + ')'


def any(*choices):
    return group(*choices) + '*'


def maybe(*choices):
    return group(*choices) + '?'


Whitespace = '[ \\f\\t]*'
Comment = '#[^\\r\\n]*'
Ignore = Whitespace + any('\\\\\\r?\\n' + Whitespace) + maybe(Comment)
Name = '\\w+'
Hexnumber = '0[xX](?:_?[0-9a-fA-F])+'
Binnumber = '0[bB](?:_?[01])+'
Octnumber = '0[oO](?:_?[0-7])+'
Decnumber = '(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
Intnumber = group(Hexnumber, Binnumber, Octnumber, Decnumber)
Exponent = '[eE][-+]?[0-9](?:_?[0-9])*'
Pointfloat = group('[0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?', '\\.[0-9](?:_?[0-9])*') + maybe(Exponent)
Expfloat = '[0-9](?:_?[0-9])*' + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Imagnumber = group('[0-9](?:_?[0-9])*[jJ]', Floatnumber + '[jJ]')
Number = group(Imagnumber, Floatnumber, Intnumber)

def _all_string_prefixes():
    _valid_string_prefixes = [
     'b', 'r', 'u', 'f', 'br', 'fr']
    result = {
     ''}
    for prefix in _valid_string_prefixes:
        for t in _itertools.permutations(prefix):
            for u in (_itertools.product)(*[(c, c.upper()) for c in t]):
                result.add(''.join(u))

    return result


def _compile(expr):
    return re.compile(expr, re.UNICODE)


StringPrefix = group(*_all_string_prefixes())
Single = "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'"
Double = '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'
Single3 = "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''"
Double3 = '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""'
Triple = group(StringPrefix + "'''", StringPrefix + '"""')
String = group(StringPrefix + "'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*'", StringPrefix + '"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*"')
Operator = group('\\*\\*=?', '>>=?', '<<=?', '!=', '//=?', '->', '[+\\-*/%&@|^=<>]=?', '~')
Bracket = '[][(){}]'
Special = group('\\r?\\n', '\\.\\.\\.', '[:;.,@]')
Funny = group(Operator, Bracket, Special)
PlainToken = group(Number, Funny, String, Name)
Token = Ignore + PlainToken
ContStr = group(StringPrefix + "'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*" + group("'", '\\\\\\r?\\n'), StringPrefix + '"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*' + group('"', '\\\\\\r?\\n'))
PseudoExtras = group('\\\\\\r?\\n|\\Z', Comment, Triple)
PseudoToken = Whitespace + group(PseudoExtras, Number, Funny, ContStr, Name)
endpats = {}
for _prefix in _all_string_prefixes():
    endpats[_prefix + "'"] = Single
    endpats[_prefix + '"'] = Double
    endpats[_prefix + "'''"] = Single3
    endpats[_prefix + '"""'] = Double3

single_quoted = set()
triple_quoted = set()
for t in _all_string_prefixes():
    for u in (t + '"', t + "'"):
        single_quoted.add(u)

    for u in (t + '"""', t + "'''"):
        triple_quoted.add(u)

tabsize = 8

class TokenError(Exception):
    pass


class StopTokenizing(Exception):
    pass


class Untokenizer:

    def __init__(self):
        self.tokens = []
        self.prev_row = 1
        self.prev_col = 0
        self.encoding = None

    def add_whitespace(self, start):
        row, col = start
        if (row < self.prev_row or row) == self.prev_row:
            if col < self.prev_col:
                raise ValueError('start ({},{}) precedes previous end ({},{})'.format(row, col, self.prev_row, self.prev_col))
        row_offset = row - self.prev_row
        if row_offset:
            self.tokens.append('\\\n' * row_offset)
            self.prev_col = 0
        col_offset = col - self.prev_col
        if col_offset:
            self.tokens.append(' ' * col_offset)

    def untokenize(self, iterable):
        it = iter(iterable)
        indents = []
        startline = False
        for t in it:
            if len(t) == 2:
                self.compat(t, it)
                break
            else:
                tok_type, token, start, end, line = t
                if tok_type == ENCODING:
                    self.encoding = token
                    continue
                if tok_type == ENDMARKER:
                    break
                if tok_type == INDENT:
                    indents.append(token)
                    continue
                else:
                    if tok_type == DEDENT:
                        indents.pop()
                        self.prev_row, self.prev_col = end
                        continue
                    else:
                        if tok_type in (NEWLINE, NL):
                            startline = True
                        else:
                            if startline:
                                if indents:
                                    indent = indents[(-1)]
                                    if start[1] >= len(indent):
                                        self.tokens.append(indent)
                                        self.prev_col = len(indent)
                                    startline = False
            self.add_whitespace(start)
            self.tokens.append(token)
            self.prev_row, self.prev_col = end
            if tok_type in (NEWLINE, NL):
                self.prev_row += 1
                self.prev_col = 0

        return ''.join(self.tokens)

    def compat(self, token, iterable):
        indents = []
        toks_append = self.tokens.append
        startline = token[0] in (NEWLINE, NL)
        prevstring = False
        for tok in chain([token], iterable):
            toknum, tokval = tok[:2]
            if toknum == ENCODING:
                self.encoding = tokval
                continue
            else:
                if toknum in (NAME, NUMBER):
                    tokval += ' '
                if toknum == STRING:
                    if prevstring:
                        tokval = ' ' + tokval
                    prevstring = True
                else:
                    prevstring = False
            if toknum == INDENT:
                indents.append(tokval)
                continue
            else:
                if toknum == DEDENT:
                    indents.pop()
                    continue
                else:
                    if toknum in (NEWLINE, NL):
                        startline = True
                    else:
                        if startline:
                            if indents:
                                toks_append(indents[(-1)])
                                startline = False
            toks_append(tokval)


def untokenize(iterable):
    """Transform tokens back into Python source code.
    It returns a bytes object, encoded using the ENCODING
    token, which is the first token sequence output by tokenize.

    Each element returned by the iterable must be a token sequence
    with at least two elements, a token number and token value.  If
    only two tokens are passed, the resulting output is poor.

    Round-trip invariant for full input:
        Untokenized source will match input source exactly

    Round-trip invariant for limited input:
        # Output bytes will tokenize back to the input
        t1 = [tok[:2] for tok in tokenize(f.readline)]
        newcode = untokenize(t1)
        readline = BytesIO(newcode).readline
        t2 = [tok[:2] for tok in tokenize(readline)]
        assert t1 == t2
    """
    ut = Untokenizer()
    out = ut.untokenize(iterable)
    if ut.encoding is not None:
        out = out.encode(ut.encoding)
    return out


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
    be used to decode a Python source file.  It requires one argument, readline,
    in the same way as the tokenize() generator.

    It will call readline a maximum of twice, and return the encoding used
    (as a string) and a list of any lines (left as bytes) it has read in.

    It detects the encoding from the presence of a utf-8 bom or an encoding
    cookie as specified in pep-0263.  If both a bom and a cookie are present,
    but disagree, a SyntaxError will be raised.  If the encoding cookie is an
    invalid charset, raise a SyntaxError.  Note that if a utf-8 bom is found,
    'utf-8-sig' is returned.

    If no encoding is specified, then the default of 'utf-8' will be returned.
    """
    try:
        filename = readline.__self__.name
    except AttributeError:
        filename = None

    bom_found = False
    encoding = None
    default = 'utf-8'

    def read_or_stop():
        try:
            return readline()
        except StopIteration:
            return b''

    def find_cookie(line):
        try:
            line_string = line.decode('utf-8')
        except UnicodeDecodeError:
            msg = 'invalid or missing encoding declaration'
            if filename is not None:
                msg = '{} for {!r}'.format(msg, filename)
            raise SyntaxError(msg)

        match = cookie_re.match(line_string)
        if not match:
            return
        encoding = _get_normal_name(match.group(1))
        try:
            codec = lookup(encoding)
        except LookupError:
            if filename is None:
                msg = 'unknown encoding: ' + encoding
            else:
                msg = 'unknown encoding for {!r}: {}'.format(filename, encoding)
            raise SyntaxError(msg)

        if bom_found:
            if encoding != 'utf-8':
                if filename is None:
                    msg = 'encoding problem: utf-8'
                else:
                    msg = 'encoding problem for {!r}: utf-8'.format(filename)
                raise SyntaxError(msg)
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


def open(filename):
    """Open a file in read only mode using the encoding detected by
    detect_encoding().
    """
    buffer = _builtin_open(filename, 'rb')
    try:
        encoding, lines = detect_encoding(buffer.readline)
        buffer.seek(0)
        text = TextIOWrapper(buffer, encoding, line_buffering=True)
        text.mode = 'r'
        return text
    except:
        buffer.close()
        raise


def tokenize(readline):
    """
    The tokenize() generator requires one argument, readline, which
    must be a callable object which provides the same interface as the
    readline() method of built-in file objects.  Each call to the function
    should return one line of input as bytes.  Alternatively, readline
    can be a callable function terminating with StopIteration:
        readline = open(myfile, 'rb').__next__  # Example of alternate readline

    The generator produces 5-tuples with these members: the token type; the
    token string; a 2-tuple (srow, scol) of ints specifying the row and
    column where the token begins in the source; a 2-tuple (erow, ecol) of
    ints specifying the row and column where the token ends in the source;
    and the line on which the token was found.  The line passed is the
    logical line; continuation lines are included.

    The first token sequence will always be an ENCODING token
    which tells you which encoding was used to decode the bytes stream.
    """
    from itertools import chain, repeat
    encoding, consumed = detect_encoding(readline)
    rl_gen = iter(readline, b'')
    empty = repeat(b'')
    return _tokenize(chain(consumed, rl_gen, empty).__next__, encoding)


def _tokenize--- This code section failed: ---

 L. 488         0  LOAD_CONST               0
                2  DUP_TOP          
                4  STORE_FAST               'lnum'
                6  DUP_TOP          
                8  STORE_FAST               'parenlev'
               10  STORE_FAST               'continued'

 L. 489        12  LOAD_STR                 '0123456789'
               14  STORE_FAST               'numchars'

 L. 490        16  LOAD_CONST               ('', 0)
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'contstr'
               22  STORE_FAST               'needcont'

 L. 491        24  LOAD_CONST               None
               26  STORE_FAST               'contline'

 L. 492        28  LOAD_CONST               0
               30  BUILD_LIST_1          1 
               32  STORE_FAST               'indents'

 L. 494        34  LOAD_FAST                'encoding'
               36  LOAD_CONST               None
               38  COMPARE_OP               is-not
               40  POP_JUMP_IF_FALSE    72  'to 72'

 L. 495        42  LOAD_FAST                'encoding'
               44  LOAD_STR                 'utf-8-sig'
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    54  'to 54'

 L. 497        50  LOAD_STR                 'utf-8'
               52  STORE_FAST               'encoding'
             54_0  COME_FROM            48  '48'

 L. 498        54  LOAD_GLOBAL              TokenInfo
               56  LOAD_GLOBAL              ENCODING
               58  LOAD_FAST                'encoding'
               60  LOAD_CONST               (0, 0)
               62  LOAD_CONST               (0, 0)
               64  LOAD_STR                 ''
               66  CALL_FUNCTION_5       5  '5 positional arguments'
               68  YIELD_VALUE      
               70  POP_TOP          
             72_0  COME_FROM            40  '40'

 L. 499     72_74  SETUP_LOOP         1520  'to 1520'

 L. 500        76  SETUP_EXCEPT         88  'to 88'

 L. 501        78  LOAD_FAST                'readline'
               80  CALL_FUNCTION_0       0  '0 positional arguments'
               82  STORE_FAST               'line'
               84  POP_BLOCK        
               86  JUMP_FORWARD        112  'to 112'
             88_0  COME_FROM_EXCEPT     76  '76'

 L. 502        88  DUP_TOP          
               90  LOAD_GLOBAL              StopIteration
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   110  'to 110'
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 503       102  LOAD_CONST               b''
              104  STORE_FAST               'line'
              106  POP_EXCEPT       
              108  JUMP_FORWARD        112  'to 112'
            110_0  COME_FROM            94  '94'
              110  END_FINALLY      
            112_0  COME_FROM           108  '108'
            112_1  COME_FROM            86  '86'

 L. 505       112  LOAD_FAST                'encoding'
              114  LOAD_CONST               None
              116  COMPARE_OP               is-not
              118  POP_JUMP_IF_FALSE   130  'to 130'

 L. 506       120  LOAD_FAST                'line'
              122  LOAD_METHOD              decode
              124  LOAD_FAST                'encoding'
              126  CALL_METHOD_1         1  '1 positional argument'
              128  STORE_FAST               'line'
            130_0  COME_FROM           118  '118'

 L. 507       130  LOAD_FAST                'lnum'
              132  LOAD_CONST               1
              134  INPLACE_ADD      
              136  STORE_FAST               'lnum'

 L. 508       138  LOAD_CONST               0
              140  LOAD_GLOBAL              len
              142  LOAD_FAST                'line'
              144  CALL_FUNCTION_1       1  '1 positional argument'
              146  ROT_TWO          
              148  STORE_FAST               'pos'
              150  STORE_FAST               'max'

 L. 510       152  LOAD_FAST                'contstr'
          154_156  POP_JUMP_IF_FALSE   358  'to 358'

 L. 511       158  LOAD_FAST                'line'
              160  POP_JUMP_IF_TRUE    172  'to 172'

 L. 512       162  LOAD_GLOBAL              TokenError
              164  LOAD_STR                 'EOF in multi-line string'
              166  LOAD_FAST                'strstart'
              168  CALL_FUNCTION_2       2  '2 positional arguments'
              170  RAISE_VARARGS_1       1  'exception instance'
            172_0  COME_FROM           160  '160'

 L. 513       172  LOAD_FAST                'endprog'
              174  LOAD_METHOD              match
              176  LOAD_FAST                'line'
              178  CALL_METHOD_1         1  '1 positional argument'
              180  STORE_FAST               'endmatch'

 L. 514       182  LOAD_FAST                'endmatch'
              184  POP_JUMP_IF_FALSE   252  'to 252'

 L. 515       186  LOAD_FAST                'endmatch'
              188  LOAD_METHOD              end
              190  LOAD_CONST               0
              192  CALL_METHOD_1         1  '1 positional argument'
              194  DUP_TOP          
              196  STORE_FAST               'pos'
              198  STORE_FAST               'end'

 L. 516       200  LOAD_GLOBAL              TokenInfo
              202  LOAD_GLOBAL              STRING
              204  LOAD_FAST                'contstr'
              206  LOAD_FAST                'line'
              208  LOAD_CONST               None
              210  LOAD_FAST                'end'
              212  BUILD_SLICE_2         2 
              214  BINARY_SUBSCR    
              216  BINARY_ADD       

 L. 517       218  LOAD_FAST                'strstart'
              220  LOAD_FAST                'lnum'
              222  LOAD_FAST                'end'
              224  BUILD_TUPLE_2         2 
              226  LOAD_FAST                'contline'
              228  LOAD_FAST                'line'
              230  BINARY_ADD       
              232  CALL_FUNCTION_5       5  '5 positional arguments'
              234  YIELD_VALUE      
              236  POP_TOP          

 L. 518       238  LOAD_CONST               ('', 0)
              240  UNPACK_SEQUENCE_2     2 
              242  STORE_FAST               'contstr'
              244  STORE_FAST               'needcont'

 L. 519       246  LOAD_CONST               None
              248  STORE_FAST               'contline'
              250  JUMP_FORWARD        806  'to 806'
            252_0  COME_FROM           184  '184'

 L. 520       252  LOAD_FAST                'needcont'
          254_256  POP_JUMP_IF_FALSE   336  'to 336'
              258  LOAD_FAST                'line'
              260  LOAD_CONST               -2
              262  LOAD_CONST               None
              264  BUILD_SLICE_2         2 
              266  BINARY_SUBSCR    
              268  LOAD_STR                 '\\\n'
              270  COMPARE_OP               !=
          272_274  POP_JUMP_IF_FALSE   336  'to 336'
              276  LOAD_FAST                'line'
              278  LOAD_CONST               -3
              280  LOAD_CONST               None
              282  BUILD_SLICE_2         2 
              284  BINARY_SUBSCR    
              286  LOAD_STR                 '\\\r\n'
              288  COMPARE_OP               !=
          290_292  POP_JUMP_IF_FALSE   336  'to 336'

 L. 521       294  LOAD_GLOBAL              TokenInfo
              296  LOAD_GLOBAL              ERRORTOKEN
              298  LOAD_FAST                'contstr'
              300  LOAD_FAST                'line'
              302  BINARY_ADD       

 L. 522       304  LOAD_FAST                'strstart'
              306  LOAD_FAST                'lnum'
              308  LOAD_GLOBAL              len
              310  LOAD_FAST                'line'
              312  CALL_FUNCTION_1       1  '1 positional argument'
              314  BUILD_TUPLE_2         2 
              316  LOAD_FAST                'contline'
              318  CALL_FUNCTION_5       5  '5 positional arguments'
              320  YIELD_VALUE      
              322  POP_TOP          

 L. 523       324  LOAD_STR                 ''
              326  STORE_FAST               'contstr'

 L. 524       328  LOAD_CONST               None
              330  STORE_FAST               'contline'

 L. 525       332  CONTINUE             76  'to 76'
              334  JUMP_FORWARD        806  'to 806'
            336_0  COME_FROM           290  '290'
            336_1  COME_FROM           272  '272'
            336_2  COME_FROM           254  '254'

 L. 527       336  LOAD_FAST                'contstr'
              338  LOAD_FAST                'line'
              340  BINARY_ADD       
              342  STORE_FAST               'contstr'

 L. 528       344  LOAD_FAST                'contline'
              346  LOAD_FAST                'line'
              348  BINARY_ADD       
              350  STORE_FAST               'contline'

 L. 529       352  CONTINUE             76  'to 76'
          354_356  JUMP_FORWARD        806  'to 806'
            358_0  COME_FROM           154  '154'

 L. 531       358  LOAD_FAST                'parenlev'
              360  LOAD_CONST               0
              362  COMPARE_OP               ==
          364_366  POP_JUMP_IF_FALSE   782  'to 782'
              368  LOAD_FAST                'continued'
          370_372  POP_JUMP_IF_TRUE    782  'to 782'

 L. 532       374  LOAD_FAST                'line'
          376_378  POP_JUMP_IF_TRUE    382  'to 382'

 L. 532       380  BREAK_LOOP       
            382_0  COME_FROM           376  '376'

 L. 533       382  LOAD_CONST               0
              384  STORE_FAST               'column'

 L. 534       386  SETUP_LOOP          490  'to 490'
              388  LOAD_FAST                'pos'
              390  LOAD_FAST                'max'
              392  COMPARE_OP               <
          394_396  POP_JUMP_IF_FALSE   488  'to 488'

 L. 535       398  LOAD_FAST                'line'
              400  LOAD_FAST                'pos'
              402  BINARY_SUBSCR    
              404  LOAD_STR                 ' '
              406  COMPARE_OP               ==
          408_410  POP_JUMP_IF_FALSE   422  'to 422'

 L. 536       412  LOAD_FAST                'column'
              414  LOAD_CONST               1
              416  INPLACE_ADD      
              418  STORE_FAST               'column'
              420  JUMP_FORWARD        476  'to 476'
            422_0  COME_FROM           408  '408'

 L. 537       422  LOAD_FAST                'line'
              424  LOAD_FAST                'pos'
              426  BINARY_SUBSCR    
              428  LOAD_STR                 '\t'
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_FALSE   454  'to 454'

 L. 538       436  LOAD_FAST                'column'
              438  LOAD_GLOBAL              tabsize
              440  BINARY_FLOOR_DIVIDE
              442  LOAD_CONST               1
              444  BINARY_ADD       
              446  LOAD_GLOBAL              tabsize
              448  BINARY_MULTIPLY  
              450  STORE_FAST               'column'
              452  JUMP_FORWARD        476  'to 476'
            454_0  COME_FROM           432  '432'

 L. 539       454  LOAD_FAST                'line'
              456  LOAD_FAST                'pos'
              458  BINARY_SUBSCR    
              460  LOAD_STR                 '\x0c'
              462  COMPARE_OP               ==
          464_466  POP_JUMP_IF_FALSE   474  'to 474'

 L. 540       468  LOAD_CONST               0
              470  STORE_FAST               'column'
              472  JUMP_FORWARD        476  'to 476'
            474_0  COME_FROM           464  '464'

 L. 542       474  BREAK_LOOP       
            476_0  COME_FROM           472  '472'
            476_1  COME_FROM           452  '452'
            476_2  COME_FROM           420  '420'

 L. 543       476  LOAD_FAST                'pos'
              478  LOAD_CONST               1
              480  INPLACE_ADD      
              482  STORE_FAST               'pos'
          484_486  JUMP_BACK           388  'to 388'
            488_0  COME_FROM           394  '394'
              488  POP_BLOCK        
            490_0  COME_FROM_LOOP      386  '386'

 L. 544       490  LOAD_FAST                'pos'
              492  LOAD_FAST                'max'
              494  COMPARE_OP               ==
          496_498  POP_JUMP_IF_FALSE   502  'to 502'

 L. 545       500  BREAK_LOOP       
            502_0  COME_FROM           496  '496'

 L. 547       502  LOAD_FAST                'line'
              504  LOAD_FAST                'pos'
              506  BINARY_SUBSCR    
              508  LOAD_STR                 '#\r\n'
              510  COMPARE_OP               in
          512_514  POP_JUMP_IF_FALSE   634  'to 634'

 L. 548       516  LOAD_FAST                'line'
              518  LOAD_FAST                'pos'
              520  BINARY_SUBSCR    
              522  LOAD_STR                 '#'
              524  COMPARE_OP               ==
          526_528  POP_JUMP_IF_FALSE   594  'to 594'

 L. 549       530  LOAD_FAST                'line'
              532  LOAD_FAST                'pos'
              534  LOAD_CONST               None
              536  BUILD_SLICE_2         2 
              538  BINARY_SUBSCR    
              540  LOAD_METHOD              rstrip
              542  LOAD_STR                 '\r\n'
              544  CALL_METHOD_1         1  '1 positional argument'
              546  STORE_FAST               'comment_token'

 L. 550       548  LOAD_GLOBAL              TokenInfo
              550  LOAD_GLOBAL              COMMENT
              552  LOAD_FAST                'comment_token'

 L. 551       554  LOAD_FAST                'lnum'
              556  LOAD_FAST                'pos'
              558  BUILD_TUPLE_2         2 
              560  LOAD_FAST                'lnum'
              562  LOAD_FAST                'pos'
              564  LOAD_GLOBAL              len
              566  LOAD_FAST                'comment_token'
              568  CALL_FUNCTION_1       1  '1 positional argument'
              570  BINARY_ADD       
              572  BUILD_TUPLE_2         2 
              574  LOAD_FAST                'line'
              576  CALL_FUNCTION_5       5  '5 positional arguments'
              578  YIELD_VALUE      
              580  POP_TOP          

 L. 552       582  LOAD_FAST                'pos'
              584  LOAD_GLOBAL              len
              586  LOAD_FAST                'comment_token'
              588  CALL_FUNCTION_1       1  '1 positional argument'
              590  INPLACE_ADD      
              592  STORE_FAST               'pos'
            594_0  COME_FROM           526  '526'

 L. 554       594  LOAD_GLOBAL              TokenInfo
              596  LOAD_GLOBAL              NL
              598  LOAD_FAST                'line'
              600  LOAD_FAST                'pos'
              602  LOAD_CONST               None
              604  BUILD_SLICE_2         2 
              606  BINARY_SUBSCR    

 L. 555       608  LOAD_FAST                'lnum'
              610  LOAD_FAST                'pos'
              612  BUILD_TUPLE_2         2 
              614  LOAD_FAST                'lnum'
              616  LOAD_GLOBAL              len
              618  LOAD_FAST                'line'
              620  CALL_FUNCTION_1       1  '1 positional argument'
              622  BUILD_TUPLE_2         2 
              624  LOAD_FAST                'line'
              626  CALL_FUNCTION_5       5  '5 positional arguments'
              628  YIELD_VALUE      
              630  POP_TOP          

 L. 556       632  CONTINUE             76  'to 76'
            634_0  COME_FROM           512  '512'

 L. 558       634  LOAD_FAST                'column'
              636  LOAD_FAST                'indents'
              638  LOAD_CONST               -1
              640  BINARY_SUBSCR    
              642  COMPARE_OP               >
          644_646  POP_JUMP_IF_FALSE   692  'to 692'

 L. 559       648  LOAD_FAST                'indents'
              650  LOAD_METHOD              append
              652  LOAD_FAST                'column'
              654  CALL_METHOD_1         1  '1 positional argument'
              656  POP_TOP          

 L. 560       658  LOAD_GLOBAL              TokenInfo
              660  LOAD_GLOBAL              INDENT
              662  LOAD_FAST                'line'
              664  LOAD_CONST               None
              666  LOAD_FAST                'pos'
              668  BUILD_SLICE_2         2 
              670  BINARY_SUBSCR    
              672  LOAD_FAST                'lnum'
              674  LOAD_CONST               0
              676  BUILD_TUPLE_2         2 
              678  LOAD_FAST                'lnum'
              680  LOAD_FAST                'pos'
              682  BUILD_TUPLE_2         2 
              684  LOAD_FAST                'line'
              686  CALL_FUNCTION_5       5  '5 positional arguments'
              688  YIELD_VALUE      
              690  POP_TOP          
            692_0  COME_FROM           644  '644'

 L. 561       692  SETUP_LOOP          806  'to 806'
              694  LOAD_FAST                'column'
              696  LOAD_FAST                'indents'
              698  LOAD_CONST               -1
            700_0  COME_FROM           250  '250'
              700  BINARY_SUBSCR    
              702  COMPARE_OP               <
          704_706  POP_JUMP_IF_FALSE   778  'to 778'

 L. 562       708  LOAD_FAST                'column'
              710  LOAD_FAST                'indents'
              712  COMPARE_OP               not-in
          714_716  POP_JUMP_IF_FALSE   736  'to 736'

 L. 563       718  LOAD_GLOBAL              IndentationError

 L. 564       720  LOAD_STR                 'unindent does not match any outer indentation level'

 L. 565       722  LOAD_STR                 '<tokenize>'
              724  LOAD_FAST                'lnum'
              726  LOAD_FAST                'pos'
              728  LOAD_FAST                'line'
              730  BUILD_TUPLE_4         4 
              732  CALL_FUNCTION_2       2  '2 positional arguments'
              734  RAISE_VARARGS_1       1  'exception instance'
            736_0  COME_FROM           714  '714'

 L. 566       736  LOAD_FAST                'indents'
              738  LOAD_CONST               None
              740  LOAD_CONST               -1
              742  BUILD_SLICE_2         2 
              744  BINARY_SUBSCR    
              746  STORE_FAST               'indents'

 L. 568       748  LOAD_GLOBAL              TokenInfo
              750  LOAD_GLOBAL              DEDENT
              752  LOAD_STR                 ''
              754  LOAD_FAST                'lnum'
              756  LOAD_FAST                'pos'
              758  BUILD_TUPLE_2         2 
              760  LOAD_FAST                'lnum'
              762  LOAD_FAST                'pos'
              764  BUILD_TUPLE_2         2 
              766  LOAD_FAST                'line'
              768  CALL_FUNCTION_5       5  '5 positional arguments'
              770  YIELD_VALUE      
              772  POP_TOP          
          774_776  JUMP_BACK           694  'to 694'
            778_0  COME_FROM           704  '704'
              778  POP_BLOCK        
              780  JUMP_FORWARD        806  'to 806'
            782_0  COME_FROM           370  '370'
            782_1  COME_FROM           364  '364'

 L. 571       782  LOAD_FAST                'line'
            784_0  COME_FROM           334  '334'
          784_786  POP_JUMP_IF_TRUE    802  'to 802'

 L. 572       788  LOAD_GLOBAL              TokenError
              790  LOAD_STR                 'EOF in multi-line statement'
              792  LOAD_FAST                'lnum'
              794  LOAD_CONST               0
              796  BUILD_TUPLE_2         2 
              798  CALL_FUNCTION_2       2  '2 positional arguments'
              800  RAISE_VARARGS_1       1  'exception instance'
            802_0  COME_FROM           784  '784'

 L. 573       802  LOAD_CONST               0
              804  STORE_FAST               'continued'
            806_0  COME_FROM           780  '780'
            806_1  COME_FROM_LOOP      692  '692'
            806_2  COME_FROM           354  '354'

 L. 575   806_808  SETUP_LOOP         1516  'to 1516'
              810  LOAD_FAST                'pos'
              812  LOAD_FAST                'max'
              814  COMPARE_OP               <
          816_818  POP_JUMP_IF_FALSE  1514  'to 1514'

 L. 576       820  LOAD_GLOBAL              _compile
              822  LOAD_GLOBAL              PseudoToken
              824  CALL_FUNCTION_1       1  '1 positional argument'
              826  LOAD_METHOD              match
              828  LOAD_FAST                'line'
              830  LOAD_FAST                'pos'
              832  CALL_METHOD_2         2  '2 positional arguments'
              834  STORE_FAST               'pseudomatch'

 L. 577       836  LOAD_FAST                'pseudomatch'
          838_840  POP_JUMP_IF_FALSE  1468  'to 1468'

 L. 578       842  LOAD_FAST                'pseudomatch'
              844  LOAD_METHOD              span
              846  LOAD_CONST               1
              848  CALL_METHOD_1         1  '1 positional argument'
              850  UNPACK_SEQUENCE_2     2 
              852  STORE_FAST               'start'
              854  STORE_FAST               'end'

 L. 579       856  LOAD_FAST                'lnum'
              858  LOAD_FAST                'start'
              860  BUILD_TUPLE_2         2 
              862  LOAD_FAST                'lnum'
              864  LOAD_FAST                'end'
              866  BUILD_TUPLE_2         2 
              868  LOAD_FAST                'end'
              870  ROT_THREE        
              872  ROT_TWO          
              874  STORE_FAST               'spos'
              876  STORE_FAST               'epos'
              878  STORE_FAST               'pos'

 L. 580       880  LOAD_FAST                'start'
              882  LOAD_FAST                'end'
              884  COMPARE_OP               ==
          886_888  POP_JUMP_IF_FALSE   894  'to 894'

 L. 581   890_892  CONTINUE            810  'to 810'
            894_0  COME_FROM           886  '886'

 L. 582       894  LOAD_FAST                'line'
              896  LOAD_FAST                'start'
              898  LOAD_FAST                'end'
              900  BUILD_SLICE_2         2 
              902  BINARY_SUBSCR    
              904  LOAD_FAST                'line'
              906  LOAD_FAST                'start'
              908  BINARY_SUBSCR    
              910  ROT_TWO          
              912  STORE_FAST               'token'
              914  STORE_FAST               'initial'

 L. 584       916  LOAD_FAST                'initial'
              918  LOAD_FAST                'numchars'
              920  COMPARE_OP               in
          922_924  POP_JUMP_IF_TRUE    956  'to 956'

 L. 585       926  LOAD_FAST                'initial'
              928  LOAD_STR                 '.'
              930  COMPARE_OP               ==
          932_934  POP_JUMP_IF_FALSE   978  'to 978'
              936  LOAD_FAST                'token'
              938  LOAD_STR                 '.'
              940  COMPARE_OP               !=
          942_944  POP_JUMP_IF_FALSE   978  'to 978'
              946  LOAD_FAST                'token'
              948  LOAD_STR                 '...'
              950  COMPARE_OP               !=
          952_954  POP_JUMP_IF_FALSE   978  'to 978'
            956_0  COME_FROM           922  '922'

 L. 586       956  LOAD_GLOBAL              TokenInfo
              958  LOAD_GLOBAL              NUMBER
              960  LOAD_FAST                'token'
              962  LOAD_FAST                'spos'
              964  LOAD_FAST                'epos'
              966  LOAD_FAST                'line'
              968  CALL_FUNCTION_5       5  '5 positional arguments'
              970  YIELD_VALUE      
              972  POP_TOP          
          974_976  JUMP_ABSOLUTE      1510  'to 1510'
            978_0  COME_FROM           952  '952'
            978_1  COME_FROM           942  '942'
            978_2  COME_FROM           932  '932'

 L. 587       978  LOAD_FAST                'initial'
              980  LOAD_STR                 '\r\n'
              982  COMPARE_OP               in
          984_986  POP_JUMP_IF_FALSE  1040  'to 1040'

 L. 588       988  LOAD_FAST                'parenlev'
              990  LOAD_CONST               0
              992  COMPARE_OP               >
          994_996  POP_JUMP_IF_FALSE  1018  'to 1018'

 L. 589       998  LOAD_GLOBAL              TokenInfo
             1000  LOAD_GLOBAL              NL
             1002  LOAD_FAST                'token'
             1004  LOAD_FAST                'spos'
             1006  LOAD_FAST                'epos'
             1008  LOAD_FAST                'line'
             1010  CALL_FUNCTION_5       5  '5 positional arguments'
             1012  YIELD_VALUE      
             1014  POP_TOP          
             1016  JUMP_ABSOLUTE      1510  'to 1510'
           1018_0  COME_FROM           994  '994'

 L. 591      1018  LOAD_GLOBAL              TokenInfo
             1020  LOAD_GLOBAL              NEWLINE
             1022  LOAD_FAST                'token'
             1024  LOAD_FAST                'spos'
             1026  LOAD_FAST                'epos'
             1028  LOAD_FAST                'line'
             1030  CALL_FUNCTION_5       5  '5 positional arguments'
             1032  YIELD_VALUE      
             1034  POP_TOP          
         1036_1038  JUMP_ABSOLUTE      1510  'to 1510'
           1040_0  COME_FROM           984  '984'

 L. 593      1040  LOAD_FAST                'initial'
             1042  LOAD_STR                 '#'
             1044  COMPARE_OP               ==
         1046_1048  POP_JUMP_IF_FALSE  1088  'to 1088'

 L. 594      1050  LOAD_FAST                'token'
             1052  LOAD_METHOD              endswith
             1054  LOAD_STR                 '\n'
             1056  CALL_METHOD_1         1  '1 positional argument'
         1058_1060  POP_JUMP_IF_FALSE  1066  'to 1066'
             1062  LOAD_GLOBAL              AssertionError
             1064  RAISE_VARARGS_1       1  'exception instance'
           1066_0  COME_FROM          1058  '1058'

 L. 595      1066  LOAD_GLOBAL              TokenInfo
             1068  LOAD_GLOBAL              COMMENT
             1070  LOAD_FAST                'token'
             1072  LOAD_FAST                'spos'
             1074  LOAD_FAST                'epos'
             1076  LOAD_FAST                'line'
             1078  CALL_FUNCTION_5       5  '5 positional arguments'
             1080  YIELD_VALUE      
             1082  POP_TOP          
         1084_1086  JUMP_ABSOLUTE      1510  'to 1510'
           1088_0  COME_FROM          1046  '1046'

 L. 597      1088  LOAD_FAST                'token'
             1090  LOAD_GLOBAL              triple_quoted
             1092  COMPARE_OP               in
         1094_1096  POP_JUMP_IF_FALSE  1204  'to 1204'

 L. 598      1098  LOAD_GLOBAL              _compile
             1100  LOAD_GLOBAL              endpats
             1102  LOAD_FAST                'token'
             1104  BINARY_SUBSCR    
             1106  CALL_FUNCTION_1       1  '1 positional argument'
             1108  STORE_FAST               'endprog'

 L. 599      1110  LOAD_FAST                'endprog'
             1112  LOAD_METHOD              match
             1114  LOAD_FAST                'line'
             1116  LOAD_FAST                'pos'
             1118  CALL_METHOD_2         2  '2 positional arguments'
             1120  STORE_FAST               'endmatch'

 L. 600      1122  LOAD_FAST                'endmatch'
         1124_1126  POP_JUMP_IF_FALSE  1174  'to 1174'

 L. 601      1128  LOAD_FAST                'endmatch'
             1130  LOAD_METHOD              end
             1132  LOAD_CONST               0
             1134  CALL_METHOD_1         1  '1 positional argument'
             1136  STORE_FAST               'pos'

 L. 602      1138  LOAD_FAST                'line'
             1140  LOAD_FAST                'start'
             1142  LOAD_FAST                'pos'
             1144  BUILD_SLICE_2         2 
             1146  BINARY_SUBSCR    
             1148  STORE_FAST               'token'

 L. 603      1150  LOAD_GLOBAL              TokenInfo
             1152  LOAD_GLOBAL              STRING
             1154  LOAD_FAST                'token'
             1156  LOAD_FAST                'spos'
             1158  LOAD_FAST                'lnum'
             1160  LOAD_FAST                'pos'
             1162  BUILD_TUPLE_2         2 
             1164  LOAD_FAST                'line'
             1166  CALL_FUNCTION_5       5  '5 positional arguments'
             1168  YIELD_VALUE      
             1170  POP_TOP          
             1172  JUMP_ABSOLUTE      1510  'to 1510'
           1174_0  COME_FROM          1124  '1124'

 L. 605      1174  LOAD_FAST                'lnum'
             1176  LOAD_FAST                'start'
             1178  BUILD_TUPLE_2         2 
             1180  STORE_FAST               'strstart'

 L. 606      1182  LOAD_FAST                'line'
             1184  LOAD_FAST                'start'
             1186  LOAD_CONST               None
             1188  BUILD_SLICE_2         2 
             1190  BINARY_SUBSCR    
             1192  STORE_FAST               'contstr'

 L. 607      1194  LOAD_FAST                'line'
             1196  STORE_FAST               'contline'

 L. 608      1198  BREAK_LOOP       
         1200_1202  JUMP_ABSOLUTE      1510  'to 1510'
           1204_0  COME_FROM          1094  '1094'

 L. 620      1204  LOAD_FAST                'initial'
             1206  LOAD_GLOBAL              single_quoted
             1208  COMPARE_OP               in
         1210_1212  POP_JUMP_IF_TRUE   1250  'to 1250'

 L. 621      1214  LOAD_FAST                'token'
             1216  LOAD_CONST               None
             1218  LOAD_CONST               2
             1220  BUILD_SLICE_2         2 
             1222  BINARY_SUBSCR    
             1224  LOAD_GLOBAL              single_quoted
             1226  COMPARE_OP               in
         1228_1230  POP_JUMP_IF_TRUE   1250  'to 1250'

 L. 622      1232  LOAD_FAST                'token'
             1234  LOAD_CONST               None
             1236  LOAD_CONST               3
             1238  BUILD_SLICE_2         2 
             1240  BINARY_SUBSCR    
             1242  LOAD_GLOBAL              single_quoted
             1244  COMPARE_OP               in
         1246_1248  POP_JUMP_IF_FALSE  1364  'to 1364'
           1250_0  COME_FROM          1228  '1228'
           1250_1  COME_FROM          1210  '1210'

 L. 623      1250  LOAD_FAST                'token'
             1252  LOAD_CONST               -1
             1254  BINARY_SUBSCR    
             1256  LOAD_STR                 '\n'
             1258  COMPARE_OP               ==
         1260_1262  POP_JUMP_IF_FALSE  1344  'to 1344'

 L. 624      1264  LOAD_FAST                'lnum'
             1266  LOAD_FAST                'start'
             1268  BUILD_TUPLE_2         2 
             1270  STORE_FAST               'strstart'

 L. 631      1272  LOAD_GLOBAL              _compile
             1274  LOAD_GLOBAL              endpats
             1276  LOAD_METHOD              get
             1278  LOAD_FAST                'initial'
             1280  CALL_METHOD_1         1  '1 positional argument'
         1282_1284  JUMP_IF_TRUE_OR_POP  1314  'to 1314'

 L. 632      1286  LOAD_GLOBAL              endpats
             1288  LOAD_METHOD              get
             1290  LOAD_FAST                'token'
             1292  LOAD_CONST               1
             1294  BINARY_SUBSCR    
             1296  CALL_METHOD_1         1  '1 positional argument'
         1298_1300  JUMP_IF_TRUE_OR_POP  1314  'to 1314'

 L. 633      1302  LOAD_GLOBAL              endpats
             1304  LOAD_METHOD              get
             1306  LOAD_FAST                'token'
             1308  LOAD_CONST               2
             1310  BINARY_SUBSCR    
             1312  CALL_METHOD_1         1  '1 positional argument'
           1314_0  COME_FROM          1298  '1298'
           1314_1  COME_FROM          1282  '1282'
             1314  CALL_FUNCTION_1       1  '1 positional argument'
             1316  STORE_FAST               'endprog'

 L. 634      1318  LOAD_FAST                'line'
             1320  LOAD_FAST                'start'
             1322  LOAD_CONST               None
             1324  BUILD_SLICE_2         2 
             1326  BINARY_SUBSCR    
             1328  LOAD_CONST               1
             1330  ROT_TWO          
             1332  STORE_FAST               'contstr'
             1334  STORE_FAST               'needcont'

 L. 635      1336  LOAD_FAST                'line'
             1338  STORE_FAST               'contline'

 L. 636      1340  BREAK_LOOP       
             1342  JUMP_FORWARD       1362  'to 1362'
           1344_0  COME_FROM          1260  '1260'

 L. 638      1344  LOAD_GLOBAL              TokenInfo
             1346  LOAD_GLOBAL              STRING
             1348  LOAD_FAST                'token'
             1350  LOAD_FAST                'spos'
             1352  LOAD_FAST                'epos'
             1354  LOAD_FAST                'line'
             1356  CALL_FUNCTION_5       5  '5 positional arguments'
             1358  YIELD_VALUE      
             1360  POP_TOP          
           1362_0  COME_FROM          1342  '1342'
             1362  JUMP_FORWARD       1466  'to 1466'
           1364_0  COME_FROM          1246  '1246'

 L. 640      1364  LOAD_FAST                'initial'
             1366  LOAD_METHOD              isidentifier
             1368  CALL_METHOD_0         0  '0 positional arguments'
         1370_1372  POP_JUMP_IF_FALSE  1394  'to 1394'

 L. 641      1374  LOAD_GLOBAL              TokenInfo
             1376  LOAD_GLOBAL              NAME
             1378  LOAD_FAST                'token'
             1380  LOAD_FAST                'spos'
             1382  LOAD_FAST                'epos'
             1384  LOAD_FAST                'line'
             1386  CALL_FUNCTION_5       5  '5 positional arguments'
             1388  YIELD_VALUE      
             1390  POP_TOP          
             1392  JUMP_FORWARD       1466  'to 1466'
           1394_0  COME_FROM          1370  '1370'

 L. 642      1394  LOAD_FAST                'initial'
             1396  LOAD_STR                 '\\'
             1398  COMPARE_OP               ==
         1400_1402  POP_JUMP_IF_FALSE  1410  'to 1410'

 L. 643      1404  LOAD_CONST               1
             1406  STORE_FAST               'continued'
             1408  JUMP_FORWARD       1466  'to 1466'
           1410_0  COME_FROM          1400  '1400'

 L. 645      1410  LOAD_FAST                'initial'
             1412  LOAD_STR                 '([{'
             1414  COMPARE_OP               in
         1416_1418  POP_JUMP_IF_FALSE  1430  'to 1430'

 L. 646      1420  LOAD_FAST                'parenlev'
             1422  LOAD_CONST               1
             1424  INPLACE_ADD      
             1426  STORE_FAST               'parenlev'
             1428  JUMP_FORWARD       1448  'to 1448'
           1430_0  COME_FROM          1416  '1416'

 L. 647      1430  LOAD_FAST                'initial'
             1432  LOAD_STR                 ')]}'
             1434  COMPARE_OP               in
         1436_1438  POP_JUMP_IF_FALSE  1448  'to 1448'

 L. 648      1440  LOAD_FAST                'parenlev'
             1442  LOAD_CONST               1
             1444  INPLACE_SUBTRACT 
             1446  STORE_FAST               'parenlev'
           1448_0  COME_FROM          1436  '1436'
           1448_1  COME_FROM          1428  '1428'

 L. 649      1448  LOAD_GLOBAL              TokenInfo
             1450  LOAD_GLOBAL              OP
             1452  LOAD_FAST                'token'
             1454  LOAD_FAST                'spos'
             1456  LOAD_FAST                'epos'
             1458  LOAD_FAST                'line'
             1460  CALL_FUNCTION_5       5  '5 positional arguments'
             1462  YIELD_VALUE      
             1464  POP_TOP          
           1466_0  COME_FROM          1408  '1408'
           1466_1  COME_FROM          1392  '1392'
           1466_2  COME_FROM          1362  '1362'
             1466  JUMP_BACK           810  'to 810'
           1468_0  COME_FROM           838  '838'

 L. 651      1468  LOAD_GLOBAL              TokenInfo
             1470  LOAD_GLOBAL              ERRORTOKEN
             1472  LOAD_FAST                'line'
             1474  LOAD_FAST                'pos'
             1476  BINARY_SUBSCR    

 L. 652      1478  LOAD_FAST                'lnum'
             1480  LOAD_FAST                'pos'
             1482  BUILD_TUPLE_2         2 
             1484  LOAD_FAST                'lnum'
             1486  LOAD_FAST                'pos'
             1488  LOAD_CONST               1
             1490  BINARY_ADD       
             1492  BUILD_TUPLE_2         2 
             1494  LOAD_FAST                'line'
             1496  CALL_FUNCTION_5       5  '5 positional arguments'
             1498  YIELD_VALUE      
             1500  POP_TOP          

 L. 653      1502  LOAD_FAST                'pos'
             1504  LOAD_CONST               1
             1506  INPLACE_ADD      
             1508  STORE_FAST               'pos'
         1510_1512  JUMP_BACK           810  'to 810'
           1514_0  COME_FROM           816  '816'
             1514  POP_BLOCK        
           1516_0  COME_FROM_LOOP      806  '806'
             1516  JUMP_BACK            76  'to 76'
             1518  POP_BLOCK        
           1520_0  COME_FROM_LOOP       72  '72'

 L. 655      1520  SETUP_LOOP         1570  'to 1570'
             1522  LOAD_FAST                'indents'
             1524  LOAD_CONST               1
             1526  LOAD_CONST               None
             1528  BUILD_SLICE_2         2 
             1530  BINARY_SUBSCR    
             1532  GET_ITER         
             1534  FOR_ITER           1568  'to 1568'
             1536  STORE_FAST               'indent'

 L. 656      1538  LOAD_GLOBAL              TokenInfo
             1540  LOAD_GLOBAL              DEDENT
             1542  LOAD_STR                 ''
             1544  LOAD_FAST                'lnum'
             1546  LOAD_CONST               0
             1548  BUILD_TUPLE_2         2 
             1550  LOAD_FAST                'lnum'
             1552  LOAD_CONST               0
             1554  BUILD_TUPLE_2         2 
             1556  LOAD_STR                 ''
             1558  CALL_FUNCTION_5       5  '5 positional arguments'
             1560  YIELD_VALUE      
             1562  POP_TOP          
         1564_1566  JUMP_BACK          1534  'to 1534'
             1568  POP_BLOCK        
           1570_0  COME_FROM_LOOP     1520  '1520'

 L. 657      1570  LOAD_GLOBAL              TokenInfo
             1572  LOAD_GLOBAL              ENDMARKER
             1574  LOAD_STR                 ''
             1576  LOAD_FAST                'lnum'
             1578  LOAD_CONST               0
             1580  BUILD_TUPLE_2         2 
             1582  LOAD_FAST                'lnum'
             1584  LOAD_CONST               0
             1586  BUILD_TUPLE_2         2 
             1588  LOAD_STR                 ''
             1590  CALL_FUNCTION_5       5  '5 positional arguments'
             1592  YIELD_VALUE      
             1594  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 700_0


def generate_tokens(readline):
    return _tokenize(readline, None)


def main():
    import argparse

    def perror(message):
        print(message, file=(sys.stderr))

    def error(message, filename=None, location=None):
        if location:
            args = (
             filename,) + location + (message,)
            perror('%s:%d:%d: error: %s' % args)
        else:
            if filename:
                perror('%s: error: %s' % (filename, message))
            else:
                perror('error: %s' % message)
        sys.exit(1)

    parser = argparse.ArgumentParser(prog='python -m tokenize')
    parser.add_argument(dest='filename', nargs='?', metavar='filename.py',
      help='the file to tokenize; defaults to stdin')
    parser.add_argument('-e', '--exact', dest='exact', action='store_true', help='display token names using the exact type')
    args = parser.parse_args()
    try:
        if args.filename:
            filename = args.filename
            with _builtin_open(filename, 'rb') as (f):
                tokens = list(tokenize(f.readline))
        else:
            filename = '<stdin>'
            tokens = _tokenize(sys.stdin.readline, None)
        for token in tokens:
            token_type = token.type
            if args.exact:
                token_type = token.exact_type
            token_range = '%d,%d-%d,%d:' % (token.start + token.end)
            print('%-20s%-15s%-15r' % (
             token_range, tok_name[token_type], token.string))

    except IndentationError as err:
        try:
            line, column = err.args[1][1:3]
            error(err.args[0], filename, (line, column))
        finally:
            err = None
            del err

    except TokenError as err:
        try:
            line, column = err.args[1]
            error(err.args[0], filename, (line, column))
        finally:
            err = None
            del err

    except SyntaxError as err:
        try:
            error(err, filename)
        finally:
            err = None
            del err

    except OSError as err:
        try:
            error(err)
        finally:
            err = None
            del err

    except KeyboardInterrupt:
        print('interrupted\n')
    except Exception as err:
        try:
            perror('unexpected error: %s' % err)
            raise
        finally:
            err = None
            del err


if __name__ == '__main__':
    main()