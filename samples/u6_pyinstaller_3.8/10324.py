# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
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
import itertools as _itertools, re, sys
from token import *
from token import EXACT_TOKEN_TYPES
cookie_re = re.compile('^[ \\t\\f]*#.*?coding[:=][ \\t]*([-\\w.]+)', re.ASCII)
blank_re = re.compile(b'^[ \\t\\f]*(?:[#\\r\\n]|$)', re.ASCII)
import token
__all__ = token.__all__ + ['tokenize', 'generate_tokens', 'detect_encoding',
 'untokenize', 'TokenInfo']
del token

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

        else:
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
Special = group(*map(re.escape, sorted(EXACT_TOKEN_TYPES, reverse=True)))
Funny = group('\\r?\\n', Special)
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
else:
    single_quoted = set()
    triple_quoted = set()
    for t in _all_string_prefixes():
        for u in (
         t + '"', t + "'"):
            single_quoted.add(u)
        else:
            for u in (
             t + '"""', t + "'''"):
                triple_quoted.add(u)
            else:
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

                    def untokenize--- This code section failed: ---

 L. 184         0  LOAD_GLOBAL              iter
                2  LOAD_FAST                'iterable'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'it'

 L. 185         8  BUILD_LIST_0          0 
               10  STORE_FAST               'indents'

 L. 186        12  LOAD_CONST               False
               14  STORE_FAST               'startline'

 L. 187        16  LOAD_FAST                'it'
               18  GET_ITER         
             20_0  COME_FROM           274  '274'
            20_22  FOR_ITER            298  'to 298'
               24  STORE_FAST               't'

 L. 188        26  LOAD_GLOBAL              len
               28  LOAD_FAST                't'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_CONST               2
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    56  'to 56'

 L. 189        38  LOAD_FAST                'self'
               40  LOAD_METHOD              compat
               42  LOAD_FAST                't'
               44  LOAD_FAST                'it'
               46  CALL_METHOD_2         2  ''
               48  POP_TOP          

 L. 190        50  POP_TOP          
            52_54  JUMP_ABSOLUTE       298  'to 298'
             56_0  COME_FROM            36  '36'

 L. 191        56  LOAD_FAST                't'
               58  UNPACK_SEQUENCE_5     5 
               60  STORE_FAST               'tok_type'
               62  STORE_FAST               'token'
               64  STORE_FAST               'start'
               66  STORE_FAST               'end'
               68  STORE_FAST               'line'

 L. 192        70  LOAD_FAST                'tok_type'
               72  LOAD_GLOBAL              ENCODING
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L. 193        78  LOAD_FAST                'token'
               80  LOAD_FAST                'self'
               82  STORE_ATTR               encoding

 L. 194        84  JUMP_BACK            20  'to 20'
             86_0  COME_FROM            76  '76'

 L. 195        86  LOAD_FAST                'tok_type'
               88  LOAD_GLOBAL              ENDMARKER
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   100  'to 100'

 L. 196        94  POP_TOP          
            96_98  JUMP_ABSOLUTE       298  'to 298'
            100_0  COME_FROM            92  '92'

 L. 197       100  LOAD_FAST                'tok_type'
              102  LOAD_GLOBAL              INDENT
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE   122  'to 122'

 L. 198       108  LOAD_FAST                'indents'
              110  LOAD_METHOD              append
              112  LOAD_FAST                'token'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 199       118  JUMP_BACK            20  'to 20'
              120  JUMP_FORWARD        230  'to 230'
            122_0  COME_FROM           106  '106'

 L. 200       122  LOAD_FAST                'tok_type'
              124  LOAD_GLOBAL              DEDENT
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   154  'to 154'

 L. 201       130  LOAD_FAST                'indents'
              132  LOAD_METHOD              pop
              134  CALL_METHOD_0         0  ''
              136  POP_TOP          

 L. 202       138  LOAD_FAST                'end'
              140  UNPACK_SEQUENCE_2     2 
              142  LOAD_FAST                'self'
              144  STORE_ATTR               prev_row
              146  LOAD_FAST                'self'
              148  STORE_ATTR               prev_col

 L. 203       150  JUMP_BACK            20  'to 20'
              152  JUMP_FORWARD        230  'to 230'
            154_0  COME_FROM           128  '128'

 L. 204       154  LOAD_FAST                'tok_type'
              156  LOAD_GLOBAL              NEWLINE
              158  LOAD_GLOBAL              NL
              160  BUILD_TUPLE_2         2 
              162  COMPARE_OP               in
              164  POP_JUMP_IF_FALSE   172  'to 172'

 L. 205       166  LOAD_CONST               True
              168  STORE_FAST               'startline'
              170  JUMP_FORWARD        230  'to 230'
            172_0  COME_FROM           164  '164'

 L. 206       172  LOAD_FAST                'startline'
              174  POP_JUMP_IF_FALSE   230  'to 230'
              176  LOAD_FAST                'indents'
              178  POP_JUMP_IF_FALSE   230  'to 230'

 L. 207       180  LOAD_FAST                'indents'
              182  LOAD_CONST               -1
              184  BINARY_SUBSCR    
              186  STORE_FAST               'indent'

 L. 208       188  LOAD_FAST                'start'
              190  LOAD_CONST               1
              192  BINARY_SUBSCR    
              194  LOAD_GLOBAL              len
              196  LOAD_FAST                'indent'
              198  CALL_FUNCTION_1       1  ''
              200  COMPARE_OP               >=
              202  POP_JUMP_IF_FALSE   226  'to 226'

 L. 209       204  LOAD_FAST                'self'
              206  LOAD_ATTR                tokens
              208  LOAD_METHOD              append
              210  LOAD_FAST                'indent'
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 210       216  LOAD_GLOBAL              len
              218  LOAD_FAST                'indent'
              220  CALL_FUNCTION_1       1  ''
              222  LOAD_FAST                'self'
              224  STORE_ATTR               prev_col
            226_0  COME_FROM           202  '202'

 L. 211       226  LOAD_CONST               False
              228  STORE_FAST               'startline'
            230_0  COME_FROM           178  '178'
            230_1  COME_FROM           174  '174'
            230_2  COME_FROM           170  '170'
            230_3  COME_FROM           152  '152'
            230_4  COME_FROM           120  '120'

 L. 212       230  LOAD_FAST                'self'
              232  LOAD_METHOD              add_whitespace
              234  LOAD_FAST                'start'
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          

 L. 213       240  LOAD_FAST                'self'
              242  LOAD_ATTR                tokens
              244  LOAD_METHOD              append
              246  LOAD_FAST                'token'
              248  CALL_METHOD_1         1  ''
              250  POP_TOP          

 L. 214       252  LOAD_FAST                'end'
              254  UNPACK_SEQUENCE_2     2 
              256  LOAD_FAST                'self'
              258  STORE_ATTR               prev_row
              260  LOAD_FAST                'self'
              262  STORE_ATTR               prev_col

 L. 215       264  LOAD_FAST                'tok_type'
              266  LOAD_GLOBAL              NEWLINE
              268  LOAD_GLOBAL              NL
              270  BUILD_TUPLE_2         2 
              272  COMPARE_OP               in
              274  POP_JUMP_IF_FALSE    20  'to 20'

 L. 216       276  LOAD_FAST                'self'
              278  DUP_TOP          
              280  LOAD_ATTR                prev_row
              282  LOAD_CONST               1
              284  INPLACE_ADD      
              286  ROT_TWO          
              288  STORE_ATTR               prev_row

 L. 217       290  LOAD_CONST               0
              292  LOAD_FAST                'self'
              294  STORE_ATTR               prev_col
              296  JUMP_BACK            20  'to 20'

 L. 218       298  LOAD_STR                 ''
              300  LOAD_METHOD              join
              302  LOAD_FAST                'self'
              304  LOAD_ATTR                tokens
              306  CALL_METHOD_1         1  ''
              308  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 52_54

                    def compat--- This code section failed: ---

 L. 221         0  BUILD_LIST_0          0 
                2  STORE_FAST               'indents'

 L. 222         4  LOAD_FAST                'self'
                6  LOAD_ATTR                tokens
                8  LOAD_ATTR                append
               10  STORE_FAST               'toks_append'

 L. 223        12  LOAD_FAST                'token'
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  LOAD_GLOBAL              NEWLINE
               20  LOAD_GLOBAL              NL
               22  BUILD_TUPLE_2         2 
               24  COMPARE_OP               in
               26  STORE_FAST               'startline'

 L. 224        28  LOAD_CONST               False
               30  STORE_FAST               'prevstring'

 L. 226        32  LOAD_GLOBAL              _itertools
               34  LOAD_METHOD              chain
               36  LOAD_FAST                'token'
               38  BUILD_LIST_1          1 
               40  LOAD_FAST                'iterable'
               42  CALL_METHOD_2         2  ''
               44  GET_ITER         
               46  FOR_ITER            226  'to 226'
               48  STORE_FAST               'tok'

 L. 227        50  LOAD_FAST                'tok'
               52  LOAD_CONST               None
               54  LOAD_CONST               2
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'toknum'
               64  STORE_FAST               'tokval'

 L. 228        66  LOAD_FAST                'toknum'
               68  LOAD_GLOBAL              ENCODING
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    82  'to 82'

 L. 229        74  LOAD_FAST                'tokval'
               76  LOAD_FAST                'self'
               78  STORE_ATTR               encoding

 L. 230        80  JUMP_BACK            46  'to 46'
             82_0  COME_FROM            72  '72'

 L. 232        82  LOAD_FAST                'toknum'
               84  LOAD_GLOBAL              NAME
               86  LOAD_GLOBAL              NUMBER
               88  BUILD_TUPLE_2         2 
               90  COMPARE_OP               in
               92  POP_JUMP_IF_FALSE   102  'to 102'

 L. 233        94  LOAD_FAST                'tokval'
               96  LOAD_STR                 ' '
               98  INPLACE_ADD      
              100  STORE_FAST               'tokval'
            102_0  COME_FROM            92  '92'

 L. 236       102  LOAD_FAST                'toknum'
              104  LOAD_GLOBAL              STRING
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   128  'to 128'

 L. 237       110  LOAD_FAST                'prevstring'
              112  POP_JUMP_IF_FALSE   122  'to 122'

 L. 238       114  LOAD_STR                 ' '
              116  LOAD_FAST                'tokval'
              118  BINARY_ADD       
              120  STORE_FAST               'tokval'
            122_0  COME_FROM           112  '112'

 L. 239       122  LOAD_CONST               True
              124  STORE_FAST               'prevstring'
              126  JUMP_FORWARD        132  'to 132'
            128_0  COME_FROM           108  '108'

 L. 241       128  LOAD_CONST               False
              130  STORE_FAST               'prevstring'
            132_0  COME_FROM           126  '126'

 L. 243       132  LOAD_FAST                'toknum'
              134  LOAD_GLOBAL              INDENT
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   154  'to 154'

 L. 244       140  LOAD_FAST                'indents'
              142  LOAD_METHOD              append
              144  LOAD_FAST                'tokval'
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L. 245       150  JUMP_BACK            46  'to 46'
              152  JUMP_FORWARD        216  'to 216'
            154_0  COME_FROM           138  '138'

 L. 246       154  LOAD_FAST                'toknum'
              156  LOAD_GLOBAL              DEDENT
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   174  'to 174'

 L. 247       162  LOAD_FAST                'indents'
              164  LOAD_METHOD              pop
              166  CALL_METHOD_0         0  ''
              168  POP_TOP          

 L. 248       170  JUMP_BACK            46  'to 46'
              172  JUMP_FORWARD        216  'to 216'
            174_0  COME_FROM           160  '160'

 L. 249       174  LOAD_FAST                'toknum'
              176  LOAD_GLOBAL              NEWLINE
              178  LOAD_GLOBAL              NL
              180  BUILD_TUPLE_2         2 
              182  COMPARE_OP               in
              184  POP_JUMP_IF_FALSE   192  'to 192'

 L. 250       186  LOAD_CONST               True
              188  STORE_FAST               'startline'
              190  JUMP_FORWARD        216  'to 216'
            192_0  COME_FROM           184  '184'

 L. 251       192  LOAD_FAST                'startline'
              194  POP_JUMP_IF_FALSE   216  'to 216'
              196  LOAD_FAST                'indents'
              198  POP_JUMP_IF_FALSE   216  'to 216'

 L. 252       200  LOAD_FAST                'toks_append'
              202  LOAD_FAST                'indents'
              204  LOAD_CONST               -1
              206  BINARY_SUBSCR    
              208  CALL_FUNCTION_1       1  ''
              210  POP_TOP          

 L. 253       212  LOAD_CONST               False
              214  STORE_FAST               'startline'
            216_0  COME_FROM           198  '198'
            216_1  COME_FROM           194  '194'
            216_2  COME_FROM           190  '190'
            216_3  COME_FROM           172  '172'
            216_4  COME_FROM           152  '152'

 L. 254       216  LOAD_FAST                'toks_append'
              218  LOAD_FAST                'tokval'
              220  CALL_FUNCTION_1       1  ''
              222  POP_TOP          
              224  JUMP_BACK            46  'to 46'

Parse error at or near `JUMP_FORWARD' instruction at offset 152


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
                    else:
                        bom_found = False
                        encoding = None
                        default = 'utf-8'

                        def read_or_stop--- This code section failed: ---

 L. 320         0  SETUP_FINALLY        10  'to 10'

 L. 321         2  LOAD_DEREF               'readline'
                4  CALL_FUNCTION_0       0  ''
                6  POP_BLOCK        
                8  RETURN_VALUE     
             10_0  COME_FROM_FINALLY     0  '0'

 L. 322        10  DUP_TOP          
               12  LOAD_GLOBAL              StopIteration
               14  COMPARE_OP               exception-match
               16  POP_JUMP_IF_FALSE    30  'to 30'
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 323        24  POP_EXCEPT       
               26  LOAD_CONST               b''
               28  RETURN_VALUE     
             30_0  COME_FROM            16  '16'
               30  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 20

                        def find_cookie(line):
                            try:
                                line_string = line.decode('utf-8')
                            except UnicodeDecodeError:
                                msg = 'invalid or missing encoding declaration'
                                if filename is not None:
                                    msg = '{} for {!r}'.format(msg, filename)
                                raise SyntaxError(msg)
                            else:
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
                                else:
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
                        if not first:
                            return (
                             default, [])
                        encoding = find_cookie(first)
                        if encoding:
                            return (
                             encoding, [first])
                        if not blank_re.match(first):
                            return (
                             default, [first])
                        second = read_or_stop()
                        if not second:
                            return (
                             default, [first])
                        encoding = find_cookie(second)
                        if encoding:
                            return (
                             encoding, [first, second])
                        return (default, [first, second])


                def open--- This code section failed: ---

 L. 392         0  LOAD_GLOBAL              _builtin_open
                2  LOAD_FAST                'filename'
                4  LOAD_STR                 'rb'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'buffer'

 L. 393        10  SETUP_FINALLY        62  'to 62'

 L. 394        12  LOAD_GLOBAL              detect_encoding
               14  LOAD_FAST                'buffer'
               16  LOAD_ATTR                readline
               18  CALL_FUNCTION_1       1  ''
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'encoding'
               24  STORE_FAST               'lines'

 L. 395        26  LOAD_FAST                'buffer'
               28  LOAD_METHOD              seek
               30  LOAD_CONST               0
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 396        36  LOAD_GLOBAL              TextIOWrapper
               38  LOAD_FAST                'buffer'
               40  LOAD_FAST                'encoding'
               42  LOAD_CONST               True
               44  LOAD_CONST               ('line_buffering',)
               46  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               48  STORE_FAST               'text'

 L. 397        50  LOAD_STR                 'r'
               52  LOAD_FAST                'text'
               54  STORE_ATTR               mode

 L. 398        56  LOAD_FAST                'text'
               58  POP_BLOCK        
               60  RETURN_VALUE     
             62_0  COME_FROM_FINALLY    10  '10'

 L. 399        62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 400        68  LOAD_FAST                'buffer'
               70  LOAD_METHOD              close
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          

 L. 401        76  RAISE_VARARGS_0       0  'reraise'
               78  POP_EXCEPT       
               80  JUMP_FORWARD         84  'to 84'
               82  END_FINALLY      
             84_0  COME_FROM            80  '80'

Parse error at or near `POP_TOP' instruction at offset 74


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
    physical line.

    The first token sequence will always be an ENCODING token
    which tells you which encoding was used to decode the bytes stream.
    """
                    encoding, consumed = detect_encoding(readline)
                    empty = _itertools.repeat(b'')
                    rl_gen = _itertools.chain(consumed, iter(readline, b''), empty)
                    return _tokenize(rl_gen.__next__, encoding)


                def _tokenize--- This code section failed: ---

 L. 430         0  LOAD_CONST               0
                2  DUP_TOP          
                4  STORE_FAST               'lnum'
                6  DUP_TOP          
                8  STORE_FAST               'parenlev'
               10  STORE_FAST               'continued'

 L. 431        12  LOAD_STR                 '0123456789'
               14  STORE_FAST               'numchars'

 L. 432        16  LOAD_CONST               ('', 0)
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'contstr'
               22  STORE_FAST               'needcont'

 L. 433        24  LOAD_CONST               None
               26  STORE_FAST               'contline'

 L. 434        28  LOAD_CONST               0
               30  BUILD_LIST_1          1 
               32  STORE_FAST               'indents'

 L. 436        34  LOAD_FAST                'encoding'
               36  LOAD_CONST               None
               38  COMPARE_OP               is-not
               40  POP_JUMP_IF_FALSE    72  'to 72'

 L. 437        42  LOAD_FAST                'encoding'
               44  LOAD_STR                 'utf-8-sig'
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    54  'to 54'

 L. 439        50  LOAD_STR                 'utf-8'
               52  STORE_FAST               'encoding'
             54_0  COME_FROM            48  '48'

 L. 440        54  LOAD_GLOBAL              TokenInfo
               56  LOAD_GLOBAL              ENCODING
               58  LOAD_FAST                'encoding'
               60  LOAD_CONST               (0, 0)
               62  LOAD_CONST               (0, 0)
               64  LOAD_STR                 ''
               66  CALL_FUNCTION_5       5  ''
               68  YIELD_VALUE      
               70  POP_TOP          
             72_0  COME_FROM            40  '40'

 L. 441        72  LOAD_CONST               b''
               74  STORE_FAST               'last_line'

 L. 442        76  LOAD_CONST               b''
               78  STORE_FAST               'line'
             80_0  COME_FROM           820  '820'

 L. 444        80  SETUP_FINALLY        96  'to 96'

 L. 449        82  LOAD_FAST                'line'
               84  STORE_FAST               'last_line'

 L. 450        86  LOAD_FAST                'readline'
               88  CALL_FUNCTION_0       0  ''
               90  STORE_FAST               'line'
               92  POP_BLOCK        
               94  JUMP_FORWARD        120  'to 120'
             96_0  COME_FROM_FINALLY    80  '80'

 L. 451        96  DUP_TOP          
               98  LOAD_GLOBAL              StopIteration
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   118  'to 118'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 452       110  LOAD_CONST               b''
              112  STORE_FAST               'line'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM           102  '102'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'
            120_1  COME_FROM            94  '94'

 L. 454       120  LOAD_FAST                'encoding'
              122  LOAD_CONST               None
              124  COMPARE_OP               is-not
              126  POP_JUMP_IF_FALSE   138  'to 138'

 L. 455       128  LOAD_FAST                'line'
              130  LOAD_METHOD              decode
              132  LOAD_FAST                'encoding'
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'line'
            138_0  COME_FROM           126  '126'

 L. 456       138  LOAD_FAST                'lnum'
              140  LOAD_CONST               1
              142  INPLACE_ADD      
              144  STORE_FAST               'lnum'

 L. 457       146  LOAD_CONST               0
              148  LOAD_GLOBAL              len
              150  LOAD_FAST                'line'
              152  CALL_FUNCTION_1       1  ''
              154  ROT_TWO          
              156  STORE_FAST               'pos'
              158  STORE_FAST               'max'

 L. 459       160  LOAD_FAST                'contstr'
          162_164  POP_JUMP_IF_FALSE   368  'to 368'

 L. 460       166  LOAD_FAST                'line'
              168  POP_JUMP_IF_TRUE    180  'to 180'

 L. 461       170  LOAD_GLOBAL              TokenError
              172  LOAD_STR                 'EOF in multi-line string'
              174  LOAD_FAST                'strstart'
              176  CALL_FUNCTION_2       2  ''
              178  RAISE_VARARGS_1       1  'exception instance'
            180_0  COME_FROM           168  '168'

 L. 462       180  LOAD_FAST                'endprog'
              182  LOAD_METHOD              match
              184  LOAD_FAST                'line'
              186  CALL_METHOD_1         1  ''
              188  STORE_FAST               'endmatch'

 L. 463       190  LOAD_FAST                'endmatch'
          192_194  POP_JUMP_IF_FALSE   262  'to 262'

 L. 464       196  LOAD_FAST                'endmatch'
              198  LOAD_METHOD              end
              200  LOAD_CONST               0
              202  CALL_METHOD_1         1  ''
              204  DUP_TOP          
              206  STORE_FAST               'pos'
              208  STORE_FAST               'end'

 L. 465       210  LOAD_GLOBAL              TokenInfo
              212  LOAD_GLOBAL              STRING
              214  LOAD_FAST                'contstr'
              216  LOAD_FAST                'line'
              218  LOAD_CONST               None
              220  LOAD_FAST                'end'
              222  BUILD_SLICE_2         2 
              224  BINARY_SUBSCR    
              226  BINARY_ADD       

 L. 466       228  LOAD_FAST                'strstart'

 L. 466       230  LOAD_FAST                'lnum'
              232  LOAD_FAST                'end'
              234  BUILD_TUPLE_2         2 

 L. 466       236  LOAD_FAST                'contline'
              238  LOAD_FAST                'line'
              240  BINARY_ADD       

 L. 465       242  CALL_FUNCTION_5       5  ''
              244  YIELD_VALUE      
              246  POP_TOP          

 L. 467       248  LOAD_CONST               ('', 0)
              250  UNPACK_SEQUENCE_2     2 
              252  STORE_FAST               'contstr'
              254  STORE_FAST               'needcont'

 L. 468       256  LOAD_CONST               None
              258  STORE_FAST               'contline'
              260  JUMP_FORWARD        814  'to 814'
            262_0  COME_FROM           192  '192'

 L. 469       262  LOAD_FAST                'needcont'
          264_266  POP_JUMP_IF_FALSE   346  'to 346'
              268  LOAD_FAST                'line'
              270  LOAD_CONST               -2
              272  LOAD_CONST               None
              274  BUILD_SLICE_2         2 
              276  BINARY_SUBSCR    
              278  LOAD_STR                 '\\\n'
              280  COMPARE_OP               !=
          282_284  POP_JUMP_IF_FALSE   346  'to 346'
              286  LOAD_FAST                'line'
              288  LOAD_CONST               -3
              290  LOAD_CONST               None
              292  BUILD_SLICE_2         2 
              294  BINARY_SUBSCR    
              296  LOAD_STR                 '\\\r\n'
              298  COMPARE_OP               !=
          300_302  POP_JUMP_IF_FALSE   346  'to 346'

 L. 470       304  LOAD_GLOBAL              TokenInfo
              306  LOAD_GLOBAL              ERRORTOKEN
              308  LOAD_FAST                'contstr'
              310  LOAD_FAST                'line'
              312  BINARY_ADD       

 L. 471       314  LOAD_FAST                'strstart'

 L. 471       316  LOAD_FAST                'lnum'
              318  LOAD_GLOBAL              len
              320  LOAD_FAST                'line'
              322  CALL_FUNCTION_1       1  ''
              324  BUILD_TUPLE_2         2 

 L. 471       326  LOAD_FAST                'contline'

 L. 470       328  CALL_FUNCTION_5       5  ''
              330  YIELD_VALUE      
              332  POP_TOP          

 L. 472       334  LOAD_STR                 ''
              336  STORE_FAST               'contstr'

 L. 473       338  LOAD_CONST               None
              340  STORE_FAST               'contline'

 L. 474       342  JUMP_BACK            80  'to 80'
              344  JUMP_FORWARD        814  'to 814'
            346_0  COME_FROM           300  '300'
            346_1  COME_FROM           282  '282'
            346_2  COME_FROM           264  '264'

 L. 476       346  LOAD_FAST                'contstr'
              348  LOAD_FAST                'line'
              350  BINARY_ADD       
              352  STORE_FAST               'contstr'

 L. 477       354  LOAD_FAST                'contline'
              356  LOAD_FAST                'line'
              358  BINARY_ADD       
              360  STORE_FAST               'contline'

 L. 478       362  JUMP_BACK            80  'to 80'
          364_366  JUMP_FORWARD        814  'to 814'
            368_0  COME_FROM           162  '162'

 L. 480       368  LOAD_FAST                'parenlev'
              370  LOAD_CONST               0
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   790  'to 790'
              378  LOAD_FAST                'continued'
          380_382  POP_JUMP_IF_TRUE    790  'to 790'

 L. 481       384  LOAD_FAST                'line'
          386_388  POP_JUMP_IF_TRUE    394  'to 394'

 L. 481   390_392  BREAK_LOOP         1518  'to 1518'
            394_0  COME_FROM           386  '386'

 L. 482       394  LOAD_CONST               0
              396  STORE_FAST               'column'

 L. 483       398  LOAD_FAST                'pos'
              400  LOAD_FAST                'max'
              402  COMPARE_OP               <
          404_406  POP_JUMP_IF_FALSE   500  'to 500'

 L. 484       408  LOAD_FAST                'line'
              410  LOAD_FAST                'pos'
              412  BINARY_SUBSCR    
              414  LOAD_STR                 ' '
              416  COMPARE_OP               ==
          418_420  POP_JUMP_IF_FALSE   432  'to 432'

 L. 485       422  LOAD_FAST                'column'
              424  LOAD_CONST               1
              426  INPLACE_ADD      
              428  STORE_FAST               'column'
              430  JUMP_FORWARD        488  'to 488'
            432_0  COME_FROM           418  '418'

 L. 486       432  LOAD_FAST                'line'
              434  LOAD_FAST                'pos'
              436  BINARY_SUBSCR    
              438  LOAD_STR                 '\t'
              440  COMPARE_OP               ==
          442_444  POP_JUMP_IF_FALSE   464  'to 464'

 L. 487       446  LOAD_FAST                'column'
              448  LOAD_GLOBAL              tabsize
              450  BINARY_FLOOR_DIVIDE
              452  LOAD_CONST               1
              454  BINARY_ADD       
              456  LOAD_GLOBAL              tabsize
              458  BINARY_MULTIPLY  
              460  STORE_FAST               'column'
              462  JUMP_FORWARD        488  'to 488'
            464_0  COME_FROM           442  '442'

 L. 488       464  LOAD_FAST                'line'
              466  LOAD_FAST                'pos'
              468  BINARY_SUBSCR    
              470  LOAD_STR                 '\x0c'
              472  COMPARE_OP               ==
          474_476  POP_JUMP_IF_FALSE   500  'to 500'

 L. 489       478  LOAD_CONST               0
              480  STORE_FAST               'column'
              482  JUMP_FORWARD        488  'to 488'

 L. 491   484_486  BREAK_LOOP          500  'to 500'
            488_0  COME_FROM           482  '482'
            488_1  COME_FROM           462  '462'
            488_2  COME_FROM           430  '430'

 L. 492       488  LOAD_FAST                'pos'
              490  LOAD_CONST               1
              492  INPLACE_ADD      
              494  STORE_FAST               'pos'
          496_498  JUMP_BACK           398  'to 398'
            500_0  COME_FROM           474  '474'
            500_1  COME_FROM           404  '404'

 L. 493       500  LOAD_FAST                'pos'
              502  LOAD_FAST                'max'
              504  COMPARE_OP               ==
          506_508  POP_JUMP_IF_FALSE   514  'to 514'

 L. 494   510_512  BREAK_LOOP         1518  'to 1518'
            514_0  COME_FROM           506  '506'

 L. 496       514  LOAD_FAST                'line'
              516  LOAD_FAST                'pos'
              518  BINARY_SUBSCR    
              520  LOAD_STR                 '#\r\n'
              522  COMPARE_OP               in
          524_526  POP_JUMP_IF_FALSE   646  'to 646'

 L. 497       528  LOAD_FAST                'line'
              530  LOAD_FAST                'pos'
              532  BINARY_SUBSCR    
              534  LOAD_STR                 '#'
              536  COMPARE_OP               ==
          538_540  POP_JUMP_IF_FALSE   606  'to 606'

 L. 498       542  LOAD_FAST                'line'
              544  LOAD_FAST                'pos'
              546  LOAD_CONST               None
              548  BUILD_SLICE_2         2 
              550  BINARY_SUBSCR    
              552  LOAD_METHOD              rstrip
              554  LOAD_STR                 '\r\n'
              556  CALL_METHOD_1         1  ''
              558  STORE_FAST               'comment_token'

 L. 499       560  LOAD_GLOBAL              TokenInfo
              562  LOAD_GLOBAL              COMMENT
              564  LOAD_FAST                'comment_token'

 L. 500       566  LOAD_FAST                'lnum'
              568  LOAD_FAST                'pos'
              570  BUILD_TUPLE_2         2 

 L. 500       572  LOAD_FAST                'lnum'
              574  LOAD_FAST                'pos'
              576  LOAD_GLOBAL              len
              578  LOAD_FAST                'comment_token'
              580  CALL_FUNCTION_1       1  ''
              582  BINARY_ADD       
              584  BUILD_TUPLE_2         2 

 L. 500       586  LOAD_FAST                'line'

 L. 499       588  CALL_FUNCTION_5       5  ''
              590  YIELD_VALUE      
              592  POP_TOP          

 L. 501       594  LOAD_FAST                'pos'
              596  LOAD_GLOBAL              len
              598  LOAD_FAST                'comment_token'
              600  CALL_FUNCTION_1       1  ''
              602  INPLACE_ADD      
              604  STORE_FAST               'pos'
            606_0  COME_FROM           538  '538'

 L. 503       606  LOAD_GLOBAL              TokenInfo
              608  LOAD_GLOBAL              NL
              610  LOAD_FAST                'line'
              612  LOAD_FAST                'pos'
              614  LOAD_CONST               None
              616  BUILD_SLICE_2         2 
              618  BINARY_SUBSCR    

 L. 504       620  LOAD_FAST                'lnum'
              622  LOAD_FAST                'pos'
              624  BUILD_TUPLE_2         2 

 L. 504       626  LOAD_FAST                'lnum'
              628  LOAD_GLOBAL              len
              630  LOAD_FAST                'line'
              632  CALL_FUNCTION_1       1  ''
              634  BUILD_TUPLE_2         2 

 L. 504       636  LOAD_FAST                'line'

 L. 503       638  CALL_FUNCTION_5       5  ''
              640  YIELD_VALUE      
              642  POP_TOP          

 L. 505       644  JUMP_BACK            80  'to 80'
            646_0  COME_FROM           524  '524'

 L. 507       646  LOAD_FAST                'column'
              648  LOAD_FAST                'indents'
              650  LOAD_CONST               -1
              652  BINARY_SUBSCR    
              654  COMPARE_OP               >
          656_658  POP_JUMP_IF_FALSE   704  'to 704'

 L. 508       660  LOAD_FAST                'indents'
              662  LOAD_METHOD              append
              664  LOAD_FAST                'column'
              666  CALL_METHOD_1         1  ''
              668  POP_TOP          

 L. 509       670  LOAD_GLOBAL              TokenInfo
              672  LOAD_GLOBAL              INDENT
              674  LOAD_FAST                'line'
              676  LOAD_CONST               None
              678  LOAD_FAST                'pos'
              680  BUILD_SLICE_2         2 
              682  BINARY_SUBSCR    
              684  LOAD_FAST                'lnum'
              686  LOAD_CONST               0
              688  BUILD_TUPLE_2         2 
              690  LOAD_FAST                'lnum'
              692  LOAD_FAST                'pos'
              694  BUILD_TUPLE_2         2 
              696  LOAD_FAST                'line'
              698  CALL_FUNCTION_5       5  ''
              700  YIELD_VALUE      
              702  POP_TOP          
            704_0  COME_FROM           656  '656'

 L. 510       704  LOAD_FAST                'column'
              706  LOAD_FAST                'indents'
            708_0  COME_FROM           260  '260'
              708  LOAD_CONST               -1
              710  BINARY_SUBSCR    
              712  COMPARE_OP               <
          714_716  POP_JUMP_IF_FALSE   814  'to 814'

 L. 511       718  LOAD_FAST                'column'
              720  LOAD_FAST                'indents'
              722  COMPARE_OP               not-in
          724_726  POP_JUMP_IF_FALSE   746  'to 746'

 L. 512       728  LOAD_GLOBAL              IndentationError

 L. 513       730  LOAD_STR                 'unindent does not match any outer indentation level'

 L. 514       732  LOAD_STR                 '<tokenize>'
              734  LOAD_FAST                'lnum'
              736  LOAD_FAST                'pos'
              738  LOAD_FAST                'line'
              740  BUILD_TUPLE_4         4 

 L. 512       742  CALL_FUNCTION_2       2  ''
              744  RAISE_VARARGS_1       1  'exception instance'
            746_0  COME_FROM           724  '724'

 L. 515       746  LOAD_FAST                'indents'
              748  LOAD_CONST               None
              750  LOAD_CONST               -1
              752  BUILD_SLICE_2         2 
              754  BINARY_SUBSCR    
              756  STORE_FAST               'indents'

 L. 517       758  LOAD_GLOBAL              TokenInfo
              760  LOAD_GLOBAL              DEDENT
              762  LOAD_STR                 ''
              764  LOAD_FAST                'lnum'
              766  LOAD_FAST                'pos'
              768  BUILD_TUPLE_2         2 
              770  LOAD_FAST                'lnum'
              772  LOAD_FAST                'pos'
              774  BUILD_TUPLE_2         2 
              776  LOAD_FAST                'line'
              778  CALL_FUNCTION_5       5  ''
              780  YIELD_VALUE      
              782  POP_TOP          
          784_786  JUMP_BACK           704  'to 704'
              788  JUMP_FORWARD        814  'to 814'
            790_0  COME_FROM           380  '380'
            790_1  COME_FROM           374  '374'

 L. 520       790  LOAD_FAST                'line'
            792_0  COME_FROM           344  '344'
          792_794  POP_JUMP_IF_TRUE    810  'to 810'

 L. 521       796  LOAD_GLOBAL              TokenError
              798  LOAD_STR                 'EOF in multi-line statement'
              800  LOAD_FAST                'lnum'
              802  LOAD_CONST               0
              804  BUILD_TUPLE_2         2 
              806  CALL_FUNCTION_2       2  ''
              808  RAISE_VARARGS_1       1  'exception instance'
            810_0  COME_FROM           792  '792'

 L. 522       810  LOAD_CONST               0
              812  STORE_FAST               'continued'
            814_0  COME_FROM           788  '788'
            814_1  COME_FROM           714  '714'
            814_2  COME_FROM           364  '364'

 L. 524       814  LOAD_FAST                'pos'
              816  LOAD_FAST                'max'
              818  COMPARE_OP               <
              820  POP_JUMP_IF_FALSE    80  'to 80'

 L. 525       822  LOAD_GLOBAL              _compile
              824  LOAD_GLOBAL              PseudoToken
              826  CALL_FUNCTION_1       1  ''
              828  LOAD_METHOD              match
              830  LOAD_FAST                'line'
              832  LOAD_FAST                'pos'
              834  CALL_METHOD_2         2  ''
              836  STORE_FAST               'pseudomatch'

 L. 526       838  LOAD_FAST                'pseudomatch'
          840_842  POP_JUMP_IF_FALSE  1470  'to 1470'

 L. 527       844  LOAD_FAST                'pseudomatch'
              846  LOAD_METHOD              span
              848  LOAD_CONST               1
              850  CALL_METHOD_1         1  ''
              852  UNPACK_SEQUENCE_2     2 
              854  STORE_FAST               'start'
              856  STORE_FAST               'end'

 L. 528       858  LOAD_FAST                'lnum'
              860  LOAD_FAST                'start'
              862  BUILD_TUPLE_2         2 
              864  LOAD_FAST                'lnum'
              866  LOAD_FAST                'end'
              868  BUILD_TUPLE_2         2 
              870  LOAD_FAST                'end'
              872  ROT_THREE        
              874  ROT_TWO          
              876  STORE_FAST               'spos'
              878  STORE_FAST               'epos'
              880  STORE_FAST               'pos'

 L. 529       882  LOAD_FAST                'start'
              884  LOAD_FAST                'end'
              886  COMPARE_OP               ==
          888_890  POP_JUMP_IF_FALSE   896  'to 896'

 L. 530   892_894  JUMP_BACK           814  'to 814'
            896_0  COME_FROM           888  '888'

 L. 531       896  LOAD_FAST                'line'
              898  LOAD_FAST                'start'
              900  LOAD_FAST                'end'
              902  BUILD_SLICE_2         2 
              904  BINARY_SUBSCR    
              906  LOAD_FAST                'line'
              908  LOAD_FAST                'start'
              910  BINARY_SUBSCR    
              912  ROT_TWO          
              914  STORE_FAST               'token'
              916  STORE_FAST               'initial'

 L. 533       918  LOAD_FAST                'initial'
              920  LOAD_FAST                'numchars'
              922  COMPARE_OP               in
          924_926  POP_JUMP_IF_TRUE    958  'to 958'

 L. 534       928  LOAD_FAST                'initial'
              930  LOAD_STR                 '.'
              932  COMPARE_OP               ==

 L. 533   934_936  POP_JUMP_IF_FALSE   980  'to 980'

 L. 534       938  LOAD_FAST                'token'
              940  LOAD_STR                 '.'
              942  COMPARE_OP               !=

 L. 533   944_946  POP_JUMP_IF_FALSE   980  'to 980'

 L. 534       948  LOAD_FAST                'token'
              950  LOAD_STR                 '...'
              952  COMPARE_OP               !=

 L. 533   954_956  POP_JUMP_IF_FALSE   980  'to 980'
            958_0  COME_FROM           924  '924'

 L. 535       958  LOAD_GLOBAL              TokenInfo
              960  LOAD_GLOBAL              NUMBER
              962  LOAD_FAST                'token'
              964  LOAD_FAST                'spos'
              966  LOAD_FAST                'epos'
              968  LOAD_FAST                'line'
              970  CALL_FUNCTION_5       5  ''
              972  YIELD_VALUE      
              974  POP_TOP          
          976_978  JUMP_ABSOLUTE      1512  'to 1512'
            980_0  COME_FROM           954  '954'
            980_1  COME_FROM           944  '944'
            980_2  COME_FROM           934  '934'

 L. 536       980  LOAD_FAST                'initial'
              982  LOAD_STR                 '\r\n'
              984  COMPARE_OP               in
          986_988  POP_JUMP_IF_FALSE  1042  'to 1042'

 L. 537       990  LOAD_FAST                'parenlev'
              992  LOAD_CONST               0
              994  COMPARE_OP               >
          996_998  POP_JUMP_IF_FALSE  1020  'to 1020'

 L. 538      1000  LOAD_GLOBAL              TokenInfo
             1002  LOAD_GLOBAL              NL
             1004  LOAD_FAST                'token'
             1006  LOAD_FAST                'spos'
             1008  LOAD_FAST                'epos'
             1010  LOAD_FAST                'line'
             1012  CALL_FUNCTION_5       5  ''
             1014  YIELD_VALUE      
             1016  POP_TOP          
             1018  JUMP_ABSOLUTE      1512  'to 1512'
           1020_0  COME_FROM           996  '996'

 L. 540      1020  LOAD_GLOBAL              TokenInfo
             1022  LOAD_GLOBAL              NEWLINE
             1024  LOAD_FAST                'token'
             1026  LOAD_FAST                'spos'
             1028  LOAD_FAST                'epos'
             1030  LOAD_FAST                'line'
             1032  CALL_FUNCTION_5       5  ''
             1034  YIELD_VALUE      
             1036  POP_TOP          
         1038_1040  JUMP_ABSOLUTE      1512  'to 1512'
           1042_0  COME_FROM           986  '986'

 L. 542      1042  LOAD_FAST                'initial'
             1044  LOAD_STR                 '#'
             1046  COMPARE_OP               ==
         1048_1050  POP_JUMP_IF_FALSE  1090  'to 1090'

 L. 543      1052  LOAD_FAST                'token'
             1054  LOAD_METHOD              endswith
             1056  LOAD_STR                 '\n'
             1058  CALL_METHOD_1         1  ''
         1060_1062  POP_JUMP_IF_FALSE  1068  'to 1068'
             1064  LOAD_GLOBAL              AssertionError
             1066  RAISE_VARARGS_1       1  'exception instance'
           1068_0  COME_FROM          1060  '1060'

 L. 544      1068  LOAD_GLOBAL              TokenInfo
             1070  LOAD_GLOBAL              COMMENT
             1072  LOAD_FAST                'token'
             1074  LOAD_FAST                'spos'
             1076  LOAD_FAST                'epos'
             1078  LOAD_FAST                'line'
             1080  CALL_FUNCTION_5       5  ''
             1082  YIELD_VALUE      
             1084  POP_TOP          
         1086_1088  JUMP_ABSOLUTE      1512  'to 1512'
           1090_0  COME_FROM          1048  '1048'

 L. 546      1090  LOAD_FAST                'token'
             1092  LOAD_GLOBAL              triple_quoted
             1094  COMPARE_OP               in
         1096_1098  POP_JUMP_IF_FALSE  1206  'to 1206'

 L. 547      1100  LOAD_GLOBAL              _compile
             1102  LOAD_GLOBAL              endpats
             1104  LOAD_FAST                'token'
             1106  BINARY_SUBSCR    
             1108  CALL_FUNCTION_1       1  ''
             1110  STORE_FAST               'endprog'

 L. 548      1112  LOAD_FAST                'endprog'
             1114  LOAD_METHOD              match
             1116  LOAD_FAST                'line'
             1118  LOAD_FAST                'pos'
             1120  CALL_METHOD_2         2  ''
             1122  STORE_FAST               'endmatch'

 L. 549      1124  LOAD_FAST                'endmatch'
         1126_1128  POP_JUMP_IF_FALSE  1176  'to 1176'

 L. 550      1130  LOAD_FAST                'endmatch'
             1132  LOAD_METHOD              end
             1134  LOAD_CONST               0
             1136  CALL_METHOD_1         1  ''
             1138  STORE_FAST               'pos'

 L. 551      1140  LOAD_FAST                'line'
             1142  LOAD_FAST                'start'
             1144  LOAD_FAST                'pos'
             1146  BUILD_SLICE_2         2 
             1148  BINARY_SUBSCR    
             1150  STORE_FAST               'token'

 L. 552      1152  LOAD_GLOBAL              TokenInfo
             1154  LOAD_GLOBAL              STRING
             1156  LOAD_FAST                'token'
             1158  LOAD_FAST                'spos'
             1160  LOAD_FAST                'lnum'
             1162  LOAD_FAST                'pos'
             1164  BUILD_TUPLE_2         2 
             1166  LOAD_FAST                'line'
             1168  CALL_FUNCTION_5       5  ''
             1170  YIELD_VALUE      
             1172  POP_TOP          
             1174  JUMP_ABSOLUTE      1512  'to 1512'
           1176_0  COME_FROM          1126  '1126'

 L. 554      1176  LOAD_FAST                'lnum'
             1178  LOAD_FAST                'start'
             1180  BUILD_TUPLE_2         2 
             1182  STORE_FAST               'strstart'

 L. 555      1184  LOAD_FAST                'line'
             1186  LOAD_FAST                'start'
             1188  LOAD_CONST               None
             1190  BUILD_SLICE_2         2 
             1192  BINARY_SUBSCR    
             1194  STORE_FAST               'contstr'

 L. 556      1196  LOAD_FAST                'line'
             1198  STORE_FAST               'contline'

 L. 557      1200  JUMP_BACK            80  'to 80'
         1202_1204  JUMP_ABSOLUTE      1512  'to 1512'
           1206_0  COME_FROM          1096  '1096'

 L. 569      1206  LOAD_FAST                'initial'
             1208  LOAD_GLOBAL              single_quoted
             1210  COMPARE_OP               in
         1212_1214  POP_JUMP_IF_TRUE   1252  'to 1252'

 L. 570      1216  LOAD_FAST                'token'
             1218  LOAD_CONST               None
             1220  LOAD_CONST               2
             1222  BUILD_SLICE_2         2 
             1224  BINARY_SUBSCR    
             1226  LOAD_GLOBAL              single_quoted
             1228  COMPARE_OP               in

 L. 569  1230_1232  POP_JUMP_IF_TRUE   1252  'to 1252'

 L. 571      1234  LOAD_FAST                'token'
             1236  LOAD_CONST               None
             1238  LOAD_CONST               3
             1240  BUILD_SLICE_2         2 
             1242  BINARY_SUBSCR    
             1244  LOAD_GLOBAL              single_quoted
             1246  COMPARE_OP               in

 L. 569  1248_1250  POP_JUMP_IF_FALSE  1366  'to 1366'
           1252_0  COME_FROM          1230  '1230'
           1252_1  COME_FROM          1212  '1212'

 L. 572      1252  LOAD_FAST                'token'
             1254  LOAD_CONST               -1
             1256  BINARY_SUBSCR    
             1258  LOAD_STR                 '\n'
             1260  COMPARE_OP               ==
         1262_1264  POP_JUMP_IF_FALSE  1346  'to 1346'

 L. 573      1266  LOAD_FAST                'lnum'
             1268  LOAD_FAST                'start'
             1270  BUILD_TUPLE_2         2 
             1272  STORE_FAST               'strstart'

 L. 580      1274  LOAD_GLOBAL              _compile
             1276  LOAD_GLOBAL              endpats
             1278  LOAD_METHOD              get
             1280  LOAD_FAST                'initial'
             1282  CALL_METHOD_1         1  ''
         1284_1286  JUMP_IF_TRUE_OR_POP  1316  'to 1316'

 L. 581      1288  LOAD_GLOBAL              endpats
             1290  LOAD_METHOD              get
             1292  LOAD_FAST                'token'
             1294  LOAD_CONST               1
             1296  BINARY_SUBSCR    
             1298  CALL_METHOD_1         1  ''

 L. 580  1300_1302  JUMP_IF_TRUE_OR_POP  1316  'to 1316'

 L. 582      1304  LOAD_GLOBAL              endpats
             1306  LOAD_METHOD              get
             1308  LOAD_FAST                'token'
             1310  LOAD_CONST               2
             1312  BINARY_SUBSCR    
             1314  CALL_METHOD_1         1  ''
           1316_0  COME_FROM          1300  '1300'
           1316_1  COME_FROM          1284  '1284'

 L. 580      1316  CALL_FUNCTION_1       1  ''
             1318  STORE_FAST               'endprog'

 L. 583      1320  LOAD_FAST                'line'
             1322  LOAD_FAST                'start'
             1324  LOAD_CONST               None
             1326  BUILD_SLICE_2         2 
             1328  BINARY_SUBSCR    
             1330  LOAD_CONST               1
             1332  ROT_TWO          
             1334  STORE_FAST               'contstr'
             1336  STORE_FAST               'needcont'

 L. 584      1338  LOAD_FAST                'line'
             1340  STORE_FAST               'contline'

 L. 585      1342  JUMP_BACK            80  'to 80'
             1344  JUMP_FORWARD       1364  'to 1364'
           1346_0  COME_FROM          1262  '1262'

 L. 587      1346  LOAD_GLOBAL              TokenInfo
             1348  LOAD_GLOBAL              STRING
             1350  LOAD_FAST                'token'
             1352  LOAD_FAST                'spos'
             1354  LOAD_FAST                'epos'
             1356  LOAD_FAST                'line'
             1358  CALL_FUNCTION_5       5  ''
             1360  YIELD_VALUE      
             1362  POP_TOP          
           1364_0  COME_FROM          1344  '1344'
             1364  JUMP_FORWARD       1468  'to 1468'
           1366_0  COME_FROM          1248  '1248'

 L. 589      1366  LOAD_FAST                'initial'
             1368  LOAD_METHOD              isidentifier
             1370  CALL_METHOD_0         0  ''
         1372_1374  POP_JUMP_IF_FALSE  1396  'to 1396'

 L. 590      1376  LOAD_GLOBAL              TokenInfo
             1378  LOAD_GLOBAL              NAME
             1380  LOAD_FAST                'token'
             1382  LOAD_FAST                'spos'
             1384  LOAD_FAST                'epos'
             1386  LOAD_FAST                'line'
             1388  CALL_FUNCTION_5       5  ''
             1390  YIELD_VALUE      
             1392  POP_TOP          
             1394  JUMP_FORWARD       1468  'to 1468'
           1396_0  COME_FROM          1372  '1372'

 L. 591      1396  LOAD_FAST                'initial'
             1398  LOAD_STR                 '\\'
             1400  COMPARE_OP               ==
         1402_1404  POP_JUMP_IF_FALSE  1412  'to 1412'

 L. 592      1406  LOAD_CONST               1
             1408  STORE_FAST               'continued'
             1410  JUMP_FORWARD       1468  'to 1468'
           1412_0  COME_FROM          1402  '1402'

 L. 594      1412  LOAD_FAST                'initial'
             1414  LOAD_STR                 '([{'
             1416  COMPARE_OP               in
         1418_1420  POP_JUMP_IF_FALSE  1432  'to 1432'

 L. 595      1422  LOAD_FAST                'parenlev'
             1424  LOAD_CONST               1
             1426  INPLACE_ADD      
             1428  STORE_FAST               'parenlev'
             1430  JUMP_FORWARD       1450  'to 1450'
           1432_0  COME_FROM          1418  '1418'

 L. 596      1432  LOAD_FAST                'initial'
             1434  LOAD_STR                 ')]}'
             1436  COMPARE_OP               in
         1438_1440  POP_JUMP_IF_FALSE  1450  'to 1450'

 L. 597      1442  LOAD_FAST                'parenlev'
             1444  LOAD_CONST               1
             1446  INPLACE_SUBTRACT 
             1448  STORE_FAST               'parenlev'
           1450_0  COME_FROM          1438  '1438'
           1450_1  COME_FROM          1430  '1430'

 L. 598      1450  LOAD_GLOBAL              TokenInfo
             1452  LOAD_GLOBAL              OP
             1454  LOAD_FAST                'token'
             1456  LOAD_FAST                'spos'
             1458  LOAD_FAST                'epos'
             1460  LOAD_FAST                'line'
             1462  CALL_FUNCTION_5       5  ''
             1464  YIELD_VALUE      
             1466  POP_TOP          
           1468_0  COME_FROM          1410  '1410'
           1468_1  COME_FROM          1394  '1394'
           1468_2  COME_FROM          1364  '1364'
             1468  JUMP_BACK           814  'to 814'
           1470_0  COME_FROM           840  '840'

 L. 600      1470  LOAD_GLOBAL              TokenInfo
             1472  LOAD_GLOBAL              ERRORTOKEN
             1474  LOAD_FAST                'line'
             1476  LOAD_FAST                'pos'
             1478  BINARY_SUBSCR    

 L. 601      1480  LOAD_FAST                'lnum'
             1482  LOAD_FAST                'pos'
             1484  BUILD_TUPLE_2         2 

 L. 601      1486  LOAD_FAST                'lnum'
             1488  LOAD_FAST                'pos'
             1490  LOAD_CONST               1
             1492  BINARY_ADD       
             1494  BUILD_TUPLE_2         2 

 L. 601      1496  LOAD_FAST                'line'

 L. 600      1498  CALL_FUNCTION_5       5  ''
             1500  YIELD_VALUE      
             1502  POP_TOP          

 L. 602      1504  LOAD_FAST                'pos'
             1506  LOAD_CONST               1
             1508  INPLACE_ADD      
             1510  STORE_FAST               'pos'
         1512_1514  JUMP_BACK           814  'to 814'
             1516  JUMP_BACK            80  'to 80'

 L. 605      1518  LOAD_FAST                'last_line'
         1520_1522  POP_JUMP_IF_FALSE  1584  'to 1584'
             1524  LOAD_FAST                'last_line'
             1526  LOAD_CONST               -1
             1528  BINARY_SUBSCR    
             1530  LOAD_STR                 '\r\n'
             1532  COMPARE_OP               not-in
         1534_1536  POP_JUMP_IF_FALSE  1584  'to 1584'

 L. 606      1538  LOAD_GLOBAL              TokenInfo
             1540  LOAD_GLOBAL              NEWLINE
             1542  LOAD_STR                 ''
             1544  LOAD_FAST                'lnum'
             1546  LOAD_CONST               1
             1548  BINARY_SUBTRACT  
             1550  LOAD_GLOBAL              len
             1552  LOAD_FAST                'last_line'
             1554  CALL_FUNCTION_1       1  ''
             1556  BUILD_TUPLE_2         2 
             1558  LOAD_FAST                'lnum'
             1560  LOAD_CONST               1
             1562  BINARY_SUBTRACT  
             1564  LOAD_GLOBAL              len
             1566  LOAD_FAST                'last_line'
             1568  CALL_FUNCTION_1       1  ''
             1570  LOAD_CONST               1
             1572  BINARY_ADD       
             1574  BUILD_TUPLE_2         2 
             1576  LOAD_STR                 ''
             1578  CALL_FUNCTION_5       5  ''
             1580  YIELD_VALUE      
             1582  POP_TOP          
           1584_0  COME_FROM          1534  '1534'
           1584_1  COME_FROM          1520  '1520'

 L. 607      1584  LOAD_FAST                'indents'
             1586  LOAD_CONST               1
             1588  LOAD_CONST               None
             1590  BUILD_SLICE_2         2 
             1592  BINARY_SUBSCR    
             1594  GET_ITER         
             1596  FOR_ITER           1630  'to 1630'
             1598  STORE_FAST               'indent'

 L. 608      1600  LOAD_GLOBAL              TokenInfo
             1602  LOAD_GLOBAL              DEDENT
             1604  LOAD_STR                 ''
             1606  LOAD_FAST                'lnum'
             1608  LOAD_CONST               0
             1610  BUILD_TUPLE_2         2 
             1612  LOAD_FAST                'lnum'
             1614  LOAD_CONST               0
             1616  BUILD_TUPLE_2         2 
             1618  LOAD_STR                 ''
             1620  CALL_FUNCTION_5       5  ''
             1622  YIELD_VALUE      
             1624  POP_TOP          
         1626_1628  JUMP_BACK          1596  'to 1596'

 L. 609      1630  LOAD_GLOBAL              TokenInfo
             1632  LOAD_GLOBAL              ENDMARKER
             1634  LOAD_STR                 ''
             1636  LOAD_FAST                'lnum'
             1638  LOAD_CONST               0
             1640  BUILD_TUPLE_2         2 
             1642  LOAD_FAST                'lnum'
             1644  LOAD_CONST               0
             1646  BUILD_TUPLE_2         2 
             1648  LOAD_STR                 ''
             1650  CALL_FUNCTION_5       5  ''
             1652  YIELD_VALUE      
             1654  POP_TOP          

Parse error at or near `JUMP_FORWARD' instruction at offset 344


                def generate_tokens(readline):
                    """Tokenize a source reading Python code as unicode strings.

    This has the same API as tokenize(), except that it expects the *readline*
    callable to return str objects instead of bytes.
    """
                    return _tokenize(readline, None)


                def main():
                    import argparse

                    def perror(message):
                        sys.stderr.write(message)
                        sys.stderr.write('\n')

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