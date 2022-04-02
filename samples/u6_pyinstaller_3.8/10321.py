# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: textwrap.py
"""Text wrapping and filling.
"""
import re
__all__ = [
 'TextWrapper', 'wrap', 'fill', 'dedent', 'indent', 'shorten']
_whitespace = '\t\n\x0b\x0c\r '

class TextWrapper:
    __doc__ = '\n    Object for wrapping/filling text.  The public interface consists of\n    the wrap() and fill() methods; the other methods are just there for\n    subclasses to override in order to tweak the default behaviour.\n    If you want to completely replace the main wrapping algorithm,\n    you\'ll probably have to override _wrap_chunks().\n\n    Several instance attributes control various aspects of wrapping:\n      width (default: 70)\n        the maximum width of wrapped lines (unless break_long_words\n        is false)\n      initial_indent (default: "")\n        string that will be prepended to the first line of wrapped\n        output.  Counts towards the line\'s width.\n      subsequent_indent (default: "")\n        string that will be prepended to all lines save the first\n        of wrapped output; also counts towards each line\'s width.\n      expand_tabs (default: true)\n        Expand tabs in input text to spaces before further processing.\n        Each tab will become 0 .. \'tabsize\' spaces, depending on its position\n        in its line.  If false, each tab is treated as a single character.\n      tabsize (default: 8)\n        Expand tabs in input text to 0 .. \'tabsize\' spaces, unless\n        \'expand_tabs\' is false.\n      replace_whitespace (default: true)\n        Replace all whitespace characters in the input text by spaces\n        after tab expansion.  Note that if expand_tabs is false and\n        replace_whitespace is true, every tab will be converted to a\n        single space!\n      fix_sentence_endings (default: false)\n        Ensure that sentence-ending punctuation is always followed\n        by two spaces.  Off by default because the algorithm is\n        (unavoidably) imperfect.\n      break_long_words (default: true)\n        Break words longer than \'width\'.  If false, those words will not\n        be broken, and some lines might be longer than \'width\'.\n      break_on_hyphens (default: true)\n        Allow breaking hyphenated words. If true, wrapping will occur\n        preferably on whitespaces and right after hyphens part of\n        compound words.\n      drop_whitespace (default: true)\n        Drop leading and trailing whitespace from lines.\n      max_lines (default: None)\n        Truncate wrapped lines.\n      placeholder (default: \' [...]\')\n        Append to the last line of truncated text.\n    '
    unicode_whitespace_trans = {}
    uspace = ord(' ')
    for x in _whitespace:
        unicode_whitespace_trans[ord(x)] = uspace
    else:
        word_punct = '[\\w!"\\\'&.,?]'
        letter = '[^\\d\\W]'
        whitespace = '[%s]' % re.escape(_whitespace)
        nowhitespace = '[^' + whitespace[1:]
        wordsep_re = re.compile('\n        ( # any whitespace\n          %(ws)s+\n        | # em-dash between words\n          (?<=%(wp)s) -{2,} (?=\\w)\n        | # word, possibly hyphenated\n          %(nws)s+? (?:\n            # hyphenated word\n              -(?: (?<=%(lt)s{2}-) | (?<=%(lt)s-%(lt)s-))\n              (?= %(lt)s -? %(lt)s)\n            | # end of word\n              (?=%(ws)s|\\Z)\n            | # em-dash\n              (?<=%(wp)s) (?=-{2,}\\w)\n            )\n        )' % {'wp':word_punct, 
         'lt':letter,  'ws':whitespace, 
         'nws':nowhitespace}, re.VERBOSE)
        del word_punct
        del letter
        del nowhitespace
        wordsep_simple_re = re.compile('(%s+)' % whitespace)
        del whitespace
        sentence_end_re = re.compile('[a-z][\\.\\!\\?][\\"\\\']?\\Z')

        def __init__(self, width=70, initial_indent='', subsequent_indent='', expand_tabs=True, replace_whitespace=True, fix_sentence_endings=False, break_long_words=True, drop_whitespace=True, break_on_hyphens=True, tabsize=8, *, max_lines=None, placeholder=' [...]'):
            self.width = width
            self.initial_indent = initial_indent
            self.subsequent_indent = subsequent_indent
            self.expand_tabs = expand_tabs
            self.replace_whitespace = replace_whitespace
            self.fix_sentence_endings = fix_sentence_endings
            self.break_long_words = break_long_words
            self.drop_whitespace = drop_whitespace
            self.break_on_hyphens = break_on_hyphens
            self.tabsize = tabsize
            self.max_lines = max_lines
            self.placeholder = placeholder

        def _munge_whitespace(self, text):
            r"""_munge_whitespace(text : string) -> string

        Munge whitespace in text: expand tabs and convert all other
        whitespace characters to spaces.  Eg. " foo\tbar\n\nbaz"
        becomes " foo    bar  baz".
        """
            if self.expand_tabs:
                text = text.expandtabs(self.tabsize)
            if self.replace_whitespace:
                text = text.translate(self.unicode_whitespace_trans)
            return text

        def _split(self, text):
            """_split(text : string) -> [string]

        Split the text to wrap into indivisible chunks.  Chunks are
        not quite the same as words; see _wrap_chunks() for full
        details.  As an example, the text
          Look, goof-ball -- use the -b option!
        breaks into the following chunks:
          'Look,', ' ', 'goof-', 'ball', ' ', '--', ' ',
          'use', ' ', 'the', ' ', '-b', ' ', 'option!'
        if break_on_hyphens is True, or in:
          'Look,', ' ', 'goof-ball', ' ', '--', ' ',
          'use', ' ', 'the', ' ', '-b', ' ', option!'
        otherwise.
        """
            if self.break_on_hyphens is True:
                chunks = self.wordsep_re.split(text)
            else:
                chunks = self.wordsep_simple_re.split(text)
            chunks = [c for c in chunks if c]
            return chunks

        def _fix_sentence_endings(self, chunks):
            r"""_fix_sentence_endings(chunks : [string])

        Correct for sentence endings buried in 'chunks'.  Eg. when the
        original text contains "... foo.\nBar ...", munge_whitespace()
        and split() will convert that to [..., "foo.", " ", "Bar", ...]
        which has one too few spaces; this method simply changes the one
        space to two.
        """
            i = 0
            patsearch = self.sentence_end_re.search
            while i < len(chunks) - 1:
                if chunks[(i + 1)] == ' ' and patsearch(chunks[i]):
                    chunks[i + 1] = '  '
                    i += 2
                else:
                    i += 1

        def _handle_long_word(self, reversed_chunks, cur_line, cur_len, width):
            """_handle_long_word(chunks : [string],
                             cur_line : [string],
                             cur_len : int, width : int)

        Handle a chunk of text (most likely a word, not whitespace) that
        is too long to fit in any line.
        """
            if width < 1:
                space_left = 1
            else:
                space_left = width - cur_len
            if self.break_long_words:
                cur_line.append(reversed_chunks[(-1)][:space_left])
                reversed_chunks[-1] = reversed_chunks[(-1)][space_left:]
            else:
                if not cur_line:
                    cur_line.append(reversed_chunks.pop())

        def _wrap_chunks(self, chunks):
            """_wrap_chunks(chunks : [string]) -> [string]

        Wrap a sequence of text chunks and return a list of lines of
        length 'self.width' or less.  (If 'break_long_words' is false,
        some lines may be longer than this.)  Chunks correspond roughly
        to words and the whitespace between them: each chunk is
        indivisible (modulo 'break_long_words'), but a line break can
        come between any two chunks.  Chunks should not have internal
        whitespace; ie. a chunk is either all whitespace or a "word".
        Whitespace chunks will be removed from the beginning and end of
        lines, but apart from that whitespace is preserved.
        """
            lines = []
            if self.width <= 0:
                raise ValueError('invalid width %r (must be > 0)' % self.width)
            else:
                if self.max_lines is not None:
                    if self.max_lines > 1:
                        indent = self.subsequent_indent
                    else:
                        indent = self.initial_indent
                    if len(indent) + len(self.placeholder.lstrip()) > self.width:
                        raise ValueError('placeholder too large for max width')
                else:
                    chunks.reverse()
                while True:
                    while chunks:
                        cur_line = []
                        cur_len = 0
                        if lines:
                            indent = self.subsequent_indent
                        else:
                            indent = self.initial_indent
                        width = self.width - len(indent)
                        if self.drop_whitespace and chunks[(-1)].strip() == '':
                            if lines:
                                del chunks[-1]
                            while True:
                                if chunks:
                                    l = len(chunks[(-1)])
                                    if cur_len + l <= width:
                                        cur_line.append(chunks.pop())
                                        cur_len += l

                            break
                        else:
                            if chunks:
                                if len(chunks[(-1)]) > width:
                                    self._handle_long_word(chunks, cur_line, cur_len, width)
                                    cur_len = sum(map(len, cur_line))
                                if self.drop_whitespace and cur_line:
                                    if cur_line[(-1)].strip() == '':
                                        cur_len -= len(cur_line[(-1)])
                                        del cur_line[-1]
                            elif cur_line and not self.max_lines is None or len(lines) + 1 < self.max_lines:
                                if not chunks or self.drop_whitespace and len(chunks) == 1 and (chunks[0].strip() or cur_len <= width):
                                    lines.append(indent + ''.join(cur_line))

                    if cur_line:
                        if cur_line[(-1)].strip():
                            if cur_len + len(self.placeholder) <= width:
                                cur_line.append(self.placeholder)
                                lines.append(indent + ''.join(cur_line))
                                break
                        cur_len -= len(cur_line[(-1)])
                        del cur_line[-1]
                    else:
                        if lines:
                            prev_line = lines[(-1)].rstrip()
                            if len(prev_line) + len(self.placeholder) <= self.width:
                                lines[-1] = prev_line + self.placeholder
                                break
                        lines.append(indent + self.placeholder.lstrip())
                        break

            return lines

        def _split_chunks(self, text):
            text = self._munge_whitespace(text)
            return self._split(text)

        def wrap(self, text):
            """wrap(text : string) -> [string]

        Reformat the single paragraph in 'text' so it fits in lines of
        no more than 'self.width' columns, and return a list of wrapped
        lines.  Tabs in 'text' are expanded with string.expandtabs(),
        and all other whitespace characters (including newline) are
        converted to space.
        """
            chunks = self._split_chunks(text)
            if self.fix_sentence_endings:
                self._fix_sentence_endings(chunks)
            return self._wrap_chunks(chunks)

        def fill(self, text):
            """fill(text : string) -> string

        Reformat the single paragraph in 'text' to fit in lines of no
        more than 'self.width' columns, and return a new string
        containing the entire wrapped paragraph.
        """
            return '\n'.join(self.wrap(text))


def wrap(text, width=70, **kwargs):
    """Wrap a single paragraph of text, returning a list of wrapped lines.

    Reformat the single paragraph in 'text' so it fits in lines of no
    more than 'width' columns, and return a list of wrapped lines.  By
    default, tabs in 'text' are expanded with string.expandtabs(), and
    all other whitespace characters (including newline) are converted to
    space.  See TextWrapper class for available keyword args to customize
    wrapping behaviour.
    """
    w = TextWrapper(width=width, **kwargs)
    return w.wrap(text)


def fill(text, width=70, **kwargs):
    """Fill a single paragraph of text, returning a new string.

    Reformat the single paragraph in 'text' to fit in lines of no more
    than 'width' columns, and return a new string containing the entire
    wrapped paragraph.  As with wrap(), tabs are expanded and other
    whitespace characters converted to space.  See TextWrapper class for
    available keyword args to customize wrapping behaviour.
    """
    w = TextWrapper(width=width, **kwargs)
    return w.fill(text)


def shorten(text, width, **kwargs):
    """Collapse and truncate the given text to fit in the given width.

    The text first has its whitespace collapsed.  If it then fits in
    the *width*, it is returned as is.  Otherwise, as many words
    as possible are joined and then the placeholder is appended::

        >>> textwrap.shorten("Hello  world!", width=12)
        'Hello world!'
        >>> textwrap.shorten("Hello  world!", width=11)
        'Hello [...]'
    """
    w = TextWrapper(width=width, max_lines=1, **kwargs)
    return w.fill(' '.join(text.strip().split()))


_whitespace_only_re = re.compile('^[ \t]+$', re.MULTILINE)
_leading_whitespace_re = re.compile('(^[ \t]*)(?:[^ \t\n])', re.MULTILINE)

def dedent--- This code section failed: ---

 L. 429         0  LOAD_CONST               None
                2  STORE_FAST               'margin'

 L. 430         4  LOAD_GLOBAL              _whitespace_only_re
                6  LOAD_METHOD              sub
                8  LOAD_STR                 ''
               10  LOAD_FAST                'text'
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'text'

 L. 431        16  LOAD_GLOBAL              _leading_whitespace_re
               18  LOAD_METHOD              findall
               20  LOAD_FAST                'text'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'indents'

 L. 432        26  LOAD_FAST                'indents'
               28  GET_ITER         
               30  FOR_ITER            130  'to 130'
               32  STORE_FAST               'indent'

 L. 433        34  LOAD_FAST                'margin'
               36  LOAD_CONST               None
               38  COMPARE_OP               is
               40  POP_JUMP_IF_FALSE    48  'to 48'

 L. 434        42  LOAD_FAST                'indent'
               44  STORE_FAST               'margin'
               46  JUMP_BACK            30  'to 30'
             48_0  COME_FROM            40  '40'

 L. 438        48  LOAD_FAST                'indent'
               50  LOAD_METHOD              startswith
               52  LOAD_FAST                'margin'
               54  CALL_METHOD_1         1  ''
               56  POP_JUMP_IF_FALSE    60  'to 60'

 L. 439        58  JUMP_BACK            30  'to 30'
             60_0  COME_FROM            56  '56'

 L. 443        60  LOAD_FAST                'margin'
               62  LOAD_METHOD              startswith
               64  LOAD_FAST                'indent'
               66  CALL_METHOD_1         1  ''
               68  POP_JUMP_IF_FALSE    76  'to 76'

 L. 444        70  LOAD_FAST                'indent'
               72  STORE_FAST               'margin'
               74  JUMP_BACK            30  'to 30'
             76_0  COME_FROM            68  '68'

 L. 449        76  LOAD_GLOBAL              enumerate
               78  LOAD_GLOBAL              zip
               80  LOAD_FAST                'margin'
               82  LOAD_FAST                'indent'
               84  CALL_FUNCTION_2       2  ''
               86  CALL_FUNCTION_1       1  ''
               88  GET_ITER         
             90_0  COME_FROM           108  '108'
               90  FOR_ITER            128  'to 128'
               92  UNPACK_SEQUENCE_2     2 
               94  STORE_FAST               'i'
               96  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST               'x'
              100  STORE_FAST               'y'

 L. 450       102  LOAD_FAST                'x'
              104  LOAD_FAST                'y'
              106  COMPARE_OP               !=
              108  POP_JUMP_IF_FALSE    90  'to 90'

 L. 451       110  LOAD_FAST                'margin'
              112  LOAD_CONST               None
              114  LOAD_FAST                'i'
              116  BUILD_SLICE_2         2 
              118  BINARY_SUBSCR    
              120  STORE_FAST               'margin'

 L. 452       122  POP_TOP          
              124  CONTINUE             30  'to 30'
              126  JUMP_BACK            90  'to 90'
              128  JUMP_BACK            30  'to 30'

 L. 455       130  LOAD_CONST               0
              132  POP_JUMP_IF_FALSE   184  'to 184'
              134  LOAD_FAST                'margin'
              136  POP_JUMP_IF_FALSE   184  'to 184'

 L. 456       138  LOAD_FAST                'text'
              140  LOAD_METHOD              split
              142  LOAD_STR                 '\n'
              144  CALL_METHOD_1         1  ''
              146  GET_ITER         
            148_0  COME_FROM           164  '164'
            148_1  COME_FROM           154  '154'
              148  FOR_ITER            184  'to 184'
              150  STORE_FAST               'line'

 L. 457       152  LOAD_FAST                'line'
              154  POP_JUMP_IF_FALSE   148  'to 148'
              156  LOAD_FAST                'line'
              158  LOAD_METHOD              startswith
              160  LOAD_FAST                'margin'
              162  CALL_METHOD_1         1  ''
              164  POP_JUMP_IF_TRUE    148  'to 148'
              166  LOAD_GLOBAL              AssertionError

 L. 458       168  LOAD_STR                 'line = %r, margin = %r'
              170  LOAD_FAST                'line'
              172  LOAD_FAST                'margin'
              174  BUILD_TUPLE_2         2 
              176  BINARY_MODULO    

 L. 457       178  CALL_FUNCTION_1       1  ''
              180  RAISE_VARARGS_1       1  'exception instance'
              182  JUMP_BACK           148  'to 148'
            184_0  COME_FROM           136  '136'
            184_1  COME_FROM           132  '132'

 L. 460       184  LOAD_FAST                'margin'
              186  POP_JUMP_IF_FALSE   206  'to 206'

 L. 461       188  LOAD_GLOBAL              re
              190  LOAD_METHOD              sub
              192  LOAD_STR                 '(?m)^'
              194  LOAD_FAST                'margin'
              196  BINARY_ADD       
              198  LOAD_STR                 ''
              200  LOAD_FAST                'text'
              202  CALL_METHOD_3         3  ''
              204  STORE_FAST               'text'
            206_0  COME_FROM           186  '186'

 L. 462       206  LOAD_FAST                'text'
              208  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 124


def indent(text, prefix, predicate=None):
    """Adds 'prefix' to the beginning of selected lines in 'text'.

    If 'predicate' is provided, 'prefix' will only be added to the lines
    where 'predicate(line)' is True. If 'predicate' is not provided,
    it will default to adding 'prefix' to all non-empty lines that do not
    consist solely of whitespace characters.
    """
    if predicate is None:

        def predicate(line):
            return line.strip()

    def prefixed_lines():
        for line in text.splitlines(True):
            (yield prefix + line if predicate(line) else line)

    return ''.join(prefixed_lines())


if __name__ == '__main__':
    print(dedent('Hello there.\n  This is indented.'))