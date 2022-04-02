# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: email\header.py
"""Header encoding and decoding functionality."""
__all__ = [
 'Header',
 'decode_header',
 'make_header']
import re, binascii, email.quoprimime, email.base64mime
from email.errors import HeaderParseError
from email import charset as _charset
Charset = _charset.Charset
NL = '\n'
SPACE = ' '
BSPACE = b' '
SPACE8 = '        '
EMPTYSTRING = ''
MAXLINELEN = 78
FWS = ' \t'
USASCII = Charset('us-ascii')
UTF8 = Charset('utf-8')
ecre = re.compile('\n  =\\?                   # literal =?\n  (?P<charset>[^?]*?)   # non-greedy up to the next ? is the charset\n  \\?                    # literal ?\n  (?P<encoding>[qQbB])  # either a "q" or a "b", case insensitive\n  \\?                    # literal ?\n  (?P<encoded>.*?)      # non-greedy up to the next ?= is the encoded string\n  \\?=                   # literal ?=\n  ', re.VERBOSE | re.MULTILINE)
fcre = re.compile('[\\041-\\176]+:$')
_embedded_header = re.compile('\\n[^ \\t]+:')
_max_append = email.quoprimime._max_append

def decode_header(header):
    """Decode a message header value without converting charset.

    Returns a list of (string, charset) pairs containing each of the decoded
    parts of the header.  Charset is None for non-encoded parts of the header,
    otherwise a lower-case string containing the name of the character set
    specified in the encoded string.

    header may be a string that may or may not contain RFC2047 encoded words,
    or it may be a Header object.

    An email.errors.HeaderParseError may be raised when certain decoding error
    occurs (e.g. a base64 decoding exception).
    """
    if hasattr(header, '_chunks'):
        return [(_charset._encode(string, str(charset)), str(charset)) for string, charset in header._chunks]
    if not ecre.search(header):
        return [(header, None)]
    words = []
    for line in header.splitlines():
        parts = ecre.split(line)
        first = True
        while True:
            if parts:
                unencoded = parts.pop(0)
                if first:
                    unencoded = unencoded.lstrip()
                    first = False
                if unencoded:
                    words.append((unencoded, None, None))
                if parts:
                    charset = parts.pop(0).lower()
                    encoding = parts.pop(0).lower()
                    encoded = parts.pop(0)
                    words.append((encoded, encoding, charset))

    else:
        droplist = []
        for n, w in enumerate(words):
            if n > 1:
                if w[1]:
                    if words[(n - 2)][1]:
                        if words[(n - 1)][0].isspace():
                            droplist.append(n - 1)

        for d in reversed(droplist):
            del words[d]
        else:
            decoded_words = []
            for encoded_string, encoding, charset in words:
                if encoding is None:
                    decoded_words.append((encoded_string, charset))
                else:
                    if encoding == 'q':
                        word = email.quoprimime.header_decode(encoded_string)
                        decoded_words.append((word, charset))
                    else:
                        if encoding == 'b':
                            paderr = len(encoded_string) % 4
                            if paderr:
                                encoded_string += '==='[:4 - paderr]
                            else:
                                try:
                                    word = email.base64mime.decode(encoded_string)
                                except binascii.Error:
                                    raise HeaderParseError('Base64 decoding error')
                                else:
                                    decoded_words.append((word, charset))
                        else:
                            raise AssertionError('Unexpected encoding: ' + encoding)
            else:
                collapsed = []
                last_word = last_charset = None
                for word, charset in decoded_words:
                    if isinstance(word, str):
                        word = bytes(word, 'raw-unicode-escape')
                    if last_word is None:
                        last_word = word
                        last_charset = charset
                    else:
                        if charset != last_charset:
                            collapsed.append((last_word, last_charset))
                            last_word = word
                            last_charset = charset
                        else:
                            if last_charset is None:
                                last_word += BSPACE + word
                            else:
                                last_word += word
                else:
                    collapsed.append((last_word, last_charset))
                    return collapsed


def make_header(decoded_seq, maxlinelen=None, header_name=None, continuation_ws=' '):
    """Create a Header from a sequence of pairs as returned by decode_header()

    decode_header() takes a header value string and returns a sequence of
    pairs of the format (decoded_string, charset) where charset is the string
    name of the character set.

    This function takes one of those sequence of pairs and returns a Header
    instance.  Optional maxlinelen, header_name, and continuation_ws are as in
    the Header constructor.
    """
    h = Header(maxlinelen=maxlinelen, header_name=header_name, continuation_ws=continuation_ws)
    for s, charset in decoded_seq:
        if charset is not None:
            if not isinstance(charset, Charset):
                charset = Charset(charset)
            h.append(s, charset)
    else:
        return h


class Header:

    def __init__(self, s=None, charset=None, maxlinelen=None, header_name=None, continuation_ws=' ', errors='strict'):
        """Create a MIME-compliant header that can contain many character sets.

        Optional s is the initial header value.  If None, the initial header
        value is not set.  You can later append to the header with .append()
        method calls.  s may be a byte string or a Unicode string, but see the
        .append() documentation for semantics.

        Optional charset serves two purposes: it has the same meaning as the
        charset argument to the .append() method.  It also sets the default
        character set for all subsequent .append() calls that omit the charset
        argument.  If charset is not provided in the constructor, the us-ascii
        charset is used both as s's initial charset and as the default for
        subsequent .append() calls.

        The maximum line length can be specified explicitly via maxlinelen. For
        splitting the first line to a shorter value (to account for the field
        header which isn't included in s, e.g. `Subject') pass in the name of
        the field in header_name.  The default maxlinelen is 78 as recommended
        by RFC 2822.

        continuation_ws must be RFC 2822 compliant folding whitespace (usually
        either a space or a hard tab) which will be prepended to continuation
        lines.

        errors is passed through to the .append() call.
        """
        if charset is None:
            charset = USASCII
        elif not isinstance(charset, Charset):
            charset = Charset(charset)
        self._charset = charset
        self._continuation_ws = continuation_ws
        self._chunks = []
        if s is not None:
            self.append(s, charset, errors)
        if maxlinelen is None:
            maxlinelen = MAXLINELEN
        self._maxlinelen = maxlinelen
        if header_name is None:
            self._headerlen = 0
        else:
            self._headerlen = len(header_name) + 2

    def __str__(self):
        """Return the string value of the header."""
        self._normalize()
        uchunks = []
        lastcs = None
        lastspace = None
        for string, charset in self._chunks:
            nextcs = charset
            if nextcs == _charset.UNKNOWN8BIT:
                original_bytes = string.encode('ascii', 'surrogateescape')
                string = original_bytes.decode('ascii', 'replace')
            else:
                if uchunks:
                    hasspace = string and self._nonctext(string[0])
                    if lastcs not in (None, 'us-ascii'):
                        if nextcs in (None, 'us-ascii'):
                            hasspace or uchunks.append(SPACE)
                            nextcs = None
                    elif nextcs not in (None, 'us-ascii'):
                        if not lastspace:
                            uchunks.append(SPACE)
                lastspace = string and self._nonctext(string[(-1)])
                lastcs = nextcs
                uchunks.append(string)
        else:
            return EMPTYSTRING.join(uchunks)

    def __eq__(self, other):
        return other == str(self)

    def append(self, s, charset=None, errors='strict'):
        """Append a string to the MIME header.

        Optional charset, if given, should be a Charset instance or the name
        of a character set (which will be converted to a Charset instance).  A
        value of None (the default) means that the charset given in the
        constructor is used.

        s may be a byte string or a Unicode string.  If it is a byte string
        (i.e. isinstance(s, str) is false), then charset is the encoding of
        that byte string, and a UnicodeError will be raised if the string
        cannot be decoded with that charset.  If s is a Unicode string, then
        charset is a hint specifying the character set of the characters in
        the string.  In either case, when producing an RFC 2822 compliant
        header using RFC 2047 rules, the string will be encoded using the
        output codec of the charset.  If the string cannot be encoded to the
        output codec, a UnicodeError will be raised.

        Optional `errors' is passed as the errors argument to the decode
        call if s is a byte string.
        """
        if charset is None:
            charset = self._charset
        elif not isinstance(charset, Charset):
            charset = Charset(charset)
        if not isinstance(s, str):
            input_charset = charset.input_codec or 'us-ascii'
            if input_charset == _charset.UNKNOWN8BIT:
                s = s.decode('us-ascii', 'surrogateescape')
            else:
                s = s.decode(input_charset, errors)
        output_charset = charset.output_codec or 'us-ascii'
        if output_charset != _charset.UNKNOWN8BIT:
            try:
                s.encode(output_charset, errors)
            except UnicodeEncodeError:
                if output_charset != 'us-ascii':
                    raise
                else:
                    charset = UTF8

        self._chunks.append((s, charset))

    def _nonctext(self, s):
        """True if string s is not a ctext character of RFC822.
        """
        return s.isspace() or s in ('(', ')', '\\')

    def encode(self, splitchars=';, \t', maxlinelen=None, linesep='\n'):
        r"""Encode a message header into an RFC-compliant format.

        There are many issues involved in converting a given string for use in
        an email header.  Only certain character sets are readable in most
        email clients, and as header strings can only contain a subset of
        7-bit ASCII, care must be taken to properly convert and encode (with
        Base64 or quoted-printable) header strings.  In addition, there is a
        75-character length limit on any given encoded header field, so
        line-wrapping must be performed, even with double-byte character sets.

        Optional maxlinelen specifies the maximum length of each generated
        line, exclusive of the linesep string.  Individual lines may be longer
        than maxlinelen if a folding point cannot be found.  The first line
        will be shorter by the length of the header name plus ": " if a header
        name was specified at Header construction time.  The default value for
        maxlinelen is determined at header construction time.

        Optional splitchars is a string containing characters which should be
        given extra weight by the splitting algorithm during normal header
        wrapping.  This is in very rough support of RFC 2822's `higher level
        syntactic breaks':  split points preceded by a splitchar are preferred
        during line splitting, with the characters preferred in the order in
        which they appear in the string.  Space and tab may be included in the
        string to indicate whether preference should be given to one over the
        other as a split point when other split chars do not appear in the line
        being split.  Splitchars does not affect RFC 2047 encoded lines.

        Optional linesep is a string to be used to separate the lines of
        the value.  The default value is the most useful for typical
        Python applications, but it can be set to \r\n to produce RFC-compliant
        line separators when needed.
        """
        self._normalize()
        if maxlinelen is None:
            maxlinelen = self._maxlinelen
        if maxlinelen == 0:
            maxlinelen = 1000000
        formatter = _ValueFormatter(self._headerlen, maxlinelen, self._continuation_ws, splitchars)
        lastcs = None
        hasspace = lastspace = None
        for string, charset in self._chunks:
            if hasspace is not None:
                hasspace = string and self._nonctext(string[0])
                if lastcs not in (None, 'us-ascii'):
                    if not hasspace or charset not in (None, 'us-ascii'):
                        formatter.add_transition()
                elif charset not in (None, 'us-ascii'):
                    if not lastspace:
                        formatter.add_transition()
            lastspace = string and self._nonctext(string[(-1)])
            lastcs = charset
            hasspace = False
            lines = string.splitlines()
            if lines:
                formatter.feed('', lines[0], charset)
            else:
                formatter.feed('', '', charset)
            for line in lines[1:]:
                formatter.newline()
                if charset.header_encoding is not None:
                    formatter.feed(self._continuation_ws, ' ' + line.lstrip(), charset)
                else:
                    sline = line.lstrip()
                    fws = line[:len(line) - len(sline)]
                    formatter.feed(fws, sline, charset)
                if len(lines) > 1:
                    formatter.newline()

        else:
            if self._chunks:
                formatter.add_transition()
            value = formatter._str(linesep)
            if _embedded_header.search(value):
                raise HeaderParseError('header value appears to contain an embedded header: {!r}'.format(value))
            return value

    def _normalize(self):
        chunks = []
        last_charset = None
        last_chunk = []
        for string, charset in self._chunks:
            if charset == last_charset:
                last_chunk.append(string)
            else:
                if last_charset is not None:
                    chunks.append((SPACE.join(last_chunk), last_charset))
                last_chunk = [
                 string]
                last_charset = charset
        else:
            if last_chunk:
                chunks.append((SPACE.join(last_chunk), last_charset))
            self._chunks = chunks


class _ValueFormatter:

    def __init__(self, headerlen, maxlen, continuation_ws, splitchars):
        self._maxlen = maxlen
        self._continuation_ws = continuation_ws
        self._continuation_ws_len = len(continuation_ws)
        self._splitchars = splitchars
        self._lines = []
        self._current_line = _Accumulator(headerlen)

    def _str(self, linesep):
        self.newline()
        return linesep.join(self._lines)

    def __str__(self):
        return self._str(NL)

    def newline(self):
        end_of_line = self._current_line.pop()
        if end_of_line != (' ', ''):
            (self._current_line.push)(*end_of_line)
        if len(self._current_line) > 0:
            if self._current_line.is_onlyws() and self._lines:
                self._lines[(-1)] += str(self._current_line)
            else:
                self._lines.append(str(self._current_line))
        self._current_line.reset()

    def add_transition(self):
        self._current_line.push(' ', '')

    def feed(self, fws, string, charset):
        if charset.header_encoding is None:
            self._ascii_split(fws, string, self._splitchars)
            return
        encoded_lines = charset.header_encode_lines(string, self._maxlengths())
        try:
            first_line = encoded_lines.pop(0)
        except IndexError:
            return
        else:
            if first_line is not None:
                self._append_chunk(fws, first_line)
            try:
                last_line = encoded_lines.pop()
            except IndexError:
                return
            else:
                self.newline()
                self._current_line.push(self._continuation_ws, last_line)
                for line in encoded_lines:
                    self._lines.append(self._continuation_ws + line)

    def _maxlengths(self):
        yield self._maxlen - len(self._current_line)
        while True:
            yield self._maxlen - self._continuation_ws_len

    def _ascii_split(self, fws, string, splitchars):
        parts = re.split('([' + FWS + ']+)', fws + string)
        if parts[0]:
            parts[:0] = [
             '']
        else:
            parts.pop(0)
        for fws, part in zip(*[iter(parts)] * 2):
            self._append_chunk(fws, part)

    def _append_chunk--- This code section failed: ---

 L. 509         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _current_line
                4  LOAD_METHOD              push
                6  LOAD_FAST                'fws'
                8  LOAD_FAST                'string'
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          

 L. 510        14  LOAD_GLOBAL              len
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _current_line
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _maxlen
               26  COMPARE_OP               >
            28_30  POP_JUMP_IF_FALSE   260  'to 260'

 L. 513        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _splitchars
               36  GET_ITER         
             38_0  COME_FROM           156  '156'
             38_1  COME_FROM           150  '150'
               38  FOR_ITER            158  'to 158'
               40  STORE_FAST               'ch'

 L. 514        42  LOAD_GLOBAL              range
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _current_line
               48  LOAD_METHOD              part_count
               50  CALL_METHOD_0         0  ''
               52  LOAD_CONST               1
               54  BINARY_SUBTRACT  
               56  LOAD_CONST               0
               58  LOAD_CONST               -1
               60  CALL_FUNCTION_3       3  ''
               62  GET_ITER         
             64_0  COME_FROM           148  '148'
             64_1  COME_FROM           142  '142'
             64_2  COME_FROM           130  '130'
               64  FOR_ITER            150  'to 150'
               66  STORE_FAST               'i'

 L. 515        68  LOAD_FAST                'ch'
               70  LOAD_METHOD              isspace
               72  CALL_METHOD_0         0  ''
               74  POP_JUMP_IF_FALSE   110  'to 110'

 L. 516        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _current_line
               80  LOAD_FAST                'i'
               82  BINARY_SUBSCR    
               84  LOAD_CONST               0
               86  BINARY_SUBSCR    
               88  STORE_FAST               'fws'

 L. 517        90  LOAD_FAST                'fws'
               92  POP_JUMP_IF_FALSE   110  'to 110'
               94  LOAD_FAST                'fws'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  LOAD_FAST                'ch'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   110  'to 110'

 L. 518       106  POP_TOP          
              108  BREAK_LOOP          152  'to 152'
            110_0  COME_FROM           104  '104'
            110_1  COME_FROM            92  '92'
            110_2  COME_FROM            74  '74'

 L. 519       110  LOAD_FAST                'self'
              112  LOAD_ATTR                _current_line
              114  LOAD_FAST                'i'
              116  LOAD_CONST               1
              118  BINARY_SUBTRACT  
              120  BINARY_SUBSCR    
              122  LOAD_CONST               1
              124  BINARY_SUBSCR    
              126  STORE_FAST               'prevpart'

 L. 520       128  LOAD_FAST                'prevpart'
              130  POP_JUMP_IF_FALSE_BACK    64  'to 64'
              132  LOAD_FAST                'prevpart'
              134  LOAD_CONST               -1
              136  BINARY_SUBSCR    
              138  LOAD_FAST                'ch'
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE_BACK    64  'to 64'

 L. 521       144  POP_TOP          
              146  BREAK_LOOP          152  'to 152'
              148  JUMP_BACK            64  'to 64'
            150_0  COME_FROM            64  '64'

 L. 523       150  JUMP_BACK            38  'to 38'
            152_0  COME_FROM           146  '146'
            152_1  COME_FROM           108  '108'

 L. 524       152  POP_TOP          
              154  BREAK_LOOP          218  'to 218'
              156  JUMP_BACK            38  'to 38'
            158_0  COME_FROM            38  '38'

 L. 526       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _current_line
              162  LOAD_METHOD              pop
              164  CALL_METHOD_0         0  ''
              166  UNPACK_SEQUENCE_2     2 
              168  STORE_FAST               'fws'
              170  STORE_FAST               'part'

 L. 527       172  LOAD_FAST                'self'
              174  LOAD_ATTR                _current_line
              176  LOAD_ATTR                _initial_size
              178  LOAD_CONST               0
              180  COMPARE_OP               >
              182  POP_JUMP_IF_FALSE   200  'to 200'

 L. 529       184  LOAD_FAST                'self'
              186  LOAD_METHOD              newline
              188  CALL_METHOD_0         0  ''
              190  POP_TOP          

 L. 530       192  LOAD_FAST                'fws'
              194  POP_JUMP_IF_TRUE    200  'to 200'

 L. 533       196  LOAD_STR                 ' '
              198  STORE_FAST               'fws'
            200_0  COME_FROM           194  '194'
            200_1  COME_FROM           182  '182'

 L. 534       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _current_line
              204  LOAD_METHOD              push
              206  LOAD_FAST                'fws'
              208  LOAD_FAST                'part'
              210  CALL_METHOD_2         2  ''
              212  POP_TOP          

 L. 535       214  LOAD_CONST               None
              216  RETURN_VALUE     
            218_0  COME_FROM           154  '154'

 L. 536       218  LOAD_FAST                'self'
              220  LOAD_ATTR                _current_line
              222  LOAD_METHOD              pop_from
              224  LOAD_FAST                'i'
              226  CALL_METHOD_1         1  ''
              228  STORE_FAST               'remainder'

 L. 537       230  LOAD_FAST                'self'
              232  LOAD_ATTR                _lines
              234  LOAD_METHOD              append
              236  LOAD_GLOBAL              str
              238  LOAD_FAST                'self'
              240  LOAD_ATTR                _current_line
              242  CALL_FUNCTION_1       1  ''
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L. 538       248  LOAD_FAST                'self'
              250  LOAD_ATTR                _current_line
              252  LOAD_METHOD              reset
              254  LOAD_FAST                'remainder'
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          
            260_0  COME_FROM            28  '28'

Parse error at or near `POP_TOP' instruction at offset 258


class _Accumulator(list):

    def __init__(self, initial_size=0):
        self._initial_size = initial_size
        super().__init__()

    def push(self, fws, string):
        self.append((fws, string))

    def pop_from(self, i=0):
        popped = self[i:]
        self[i:] = []
        return popped

    def pop(self):
        if self.part_count() == 0:
            return ('', '')
        return super().pop()

    def __len__(self):
        return sum((len(fws) + len(part) for fws, part in self), self._initial_size)

    def __str__(self):
        return EMPTYSTRING.join((EMPTYSTRING.join((fws, part)) for fws, part in self))

    def reset(self, startval=None):
        if startval is None:
            startval = []
        self[:] = startval
        self._initial_size = 0

    def is_onlyws(self):
        return (self._initial_size == 0) and ((not self) or (str(self).isspace()))

    def part_count(self):
        return super().__len__()