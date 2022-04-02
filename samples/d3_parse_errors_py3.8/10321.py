# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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
            while True:
                if i < len(chunks) - 1:
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
            elif not cur_line:
                cur_line.append(reversed_chunks.pop())

        def _wrap_chunks--- This code section failed: ---

 L. 246         0  BUILD_LIST_0          0 
                2  STORE_FAST               'lines'

 L. 247         4  LOAD_FAST                'self'
                6  LOAD_ATTR                width
                8  LOAD_CONST               0
               10  COMPARE_OP               <=
               12  POP_JUMP_IF_FALSE    28  'to 28'

 L. 248        14  LOAD_GLOBAL              ValueError
               16  LOAD_STR                 'invalid width %r (must be > 0)'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                width
               22  BINARY_MODULO    
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            12  '12'

 L. 249        28  LOAD_FAST                'self'
               30  LOAD_ATTR                max_lines
               32  LOAD_CONST               None
               34  COMPARE_OP               is-not
               36  POP_JUMP_IF_FALSE    98  'to 98'

 L. 250        38  LOAD_FAST                'self'
               40  LOAD_ATTR                max_lines
               42  LOAD_CONST               1
               44  COMPARE_OP               >
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L. 251        48  LOAD_FAST                'self'
               50  LOAD_ATTR                subsequent_indent
               52  STORE_FAST               'indent'
               54  JUMP_FORWARD         62  'to 62'
             56_0  COME_FROM            46  '46'

 L. 253        56  LOAD_FAST                'self'
               58  LOAD_ATTR                initial_indent
               60  STORE_FAST               'indent'
             62_0  COME_FROM            54  '54'

 L. 254        62  LOAD_GLOBAL              len
               64  LOAD_FAST                'indent'
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_GLOBAL              len
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                placeholder
               74  LOAD_METHOD              lstrip
               76  CALL_METHOD_0         0  ''
               78  CALL_FUNCTION_1       1  ''
               80  BINARY_ADD       
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                width
               86  COMPARE_OP               >
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L. 255        90  LOAD_GLOBAL              ValueError
               92  LOAD_STR                 'placeholder too large for max width'
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            88  '88'
             98_1  COME_FROM            36  '36'

 L. 259        98  LOAD_FAST                'chunks'
              100  LOAD_METHOD              reverse
              102  CALL_METHOD_0         0  ''
              104  POP_TOP          
            106_0  COME_FROM           646  '646'
            106_1  COME_FROM           456  '456'
            106_2  COME_FROM           350  '350'

 L. 261       106  LOAD_FAST                'chunks'
          108_110  POP_JUMP_IF_FALSE   648  'to 648'

 L. 265       112  BUILD_LIST_0          0 
              114  STORE_FAST               'cur_line'

 L. 266       116  LOAD_CONST               0
              118  STORE_FAST               'cur_len'

 L. 269       120  LOAD_FAST                'lines'
              122  POP_JUMP_IF_FALSE   132  'to 132'

 L. 270       124  LOAD_FAST                'self'
              126  LOAD_ATTR                subsequent_indent
              128  STORE_FAST               'indent'
              130  JUMP_FORWARD        138  'to 138'
            132_0  COME_FROM           122  '122'

 L. 272       132  LOAD_FAST                'self'
              134  LOAD_ATTR                initial_indent
              136  STORE_FAST               'indent'
            138_0  COME_FROM           130  '130'

 L. 275       138  LOAD_FAST                'self'
              140  LOAD_ATTR                width
              142  LOAD_GLOBAL              len
              144  LOAD_FAST                'indent'
              146  CALL_FUNCTION_1       1  ''
              148  BINARY_SUBTRACT  
              150  STORE_FAST               'width'

 L. 279       152  LOAD_FAST                'self'
              154  LOAD_ATTR                drop_whitespace
              156  POP_JUMP_IF_FALSE   184  'to 184'
              158  LOAD_FAST                'chunks'
              160  LOAD_CONST               -1
              162  BINARY_SUBSCR    
              164  LOAD_METHOD              strip
              166  CALL_METHOD_0         0  ''
              168  LOAD_STR                 ''
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   184  'to 184'
              174  LOAD_FAST                'lines'
              176  POP_JUMP_IF_FALSE   184  'to 184'

 L. 280       178  LOAD_FAST                'chunks'
              180  LOAD_CONST               -1
              182  DELETE_SUBSCR    
            184_0  COME_FROM           238  '238'
            184_1  COME_FROM           234  '234'
            184_2  COME_FROM           176  '176'
            184_3  COME_FROM           172  '172'
            184_4  COME_FROM           156  '156'

 L. 282       184  LOAD_FAST                'chunks'
              186  POP_JUMP_IF_FALSE   240  'to 240'

 L. 283       188  LOAD_GLOBAL              len
              190  LOAD_FAST                'chunks'
              192  LOAD_CONST               -1
              194  BINARY_SUBSCR    
              196  CALL_FUNCTION_1       1  ''
              198  STORE_FAST               'l'

 L. 286       200  LOAD_FAST                'cur_len'
              202  LOAD_FAST                'l'
              204  BINARY_ADD       
              206  LOAD_FAST                'width'
              208  COMPARE_OP               <=
              210  POP_JUMP_IF_FALSE   240  'to 240'

 L. 287       212  LOAD_FAST                'cur_line'
              214  LOAD_METHOD              append
              216  LOAD_FAST                'chunks'
              218  LOAD_METHOD              pop
              220  CALL_METHOD_0         0  ''
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          

 L. 288       226  LOAD_FAST                'cur_len'
              228  LOAD_FAST                'l'
              230  INPLACE_ADD      
              232  STORE_FAST               'cur_len'
              234  JUMP_BACK           184  'to 184'

 L. 292       236  JUMP_FORWARD        240  'to 240'
              238  JUMP_BACK           184  'to 184'
            240_0  COME_FROM           236  '236'
            240_1  COME_FROM           210  '210'
            240_2  COME_FROM           186  '186'

 L. 296       240  LOAD_FAST                'chunks'
          242_244  POP_JUMP_IF_FALSE   294  'to 294'
              246  LOAD_GLOBAL              len
              248  LOAD_FAST                'chunks'
              250  LOAD_CONST               -1
              252  BINARY_SUBSCR    
              254  CALL_FUNCTION_1       1  ''
              256  LOAD_FAST                'width'
              258  COMPARE_OP               >
          260_262  POP_JUMP_IF_FALSE   294  'to 294'

 L. 297       264  LOAD_FAST                'self'
              266  LOAD_METHOD              _handle_long_word
              268  LOAD_FAST                'chunks'
              270  LOAD_FAST                'cur_line'
              272  LOAD_FAST                'cur_len'
              274  LOAD_FAST                'width'
              276  CALL_METHOD_4         4  ''
              278  POP_TOP          

 L. 298       280  LOAD_GLOBAL              sum
              282  LOAD_GLOBAL              map
              284  LOAD_GLOBAL              len
              286  LOAD_FAST                'cur_line'
              288  CALL_FUNCTION_2       2  ''
              290  CALL_FUNCTION_1       1  ''
              292  STORE_FAST               'cur_len'
            294_0  COME_FROM           260  '260'
            294_1  COME_FROM           242  '242'

 L. 301       294  LOAD_FAST                'self'
              296  LOAD_ATTR                drop_whitespace
          298_300  POP_JUMP_IF_FALSE   348  'to 348'
              302  LOAD_FAST                'cur_line'
          304_306  POP_JUMP_IF_FALSE   348  'to 348'
              308  LOAD_FAST                'cur_line'
              310  LOAD_CONST               -1
              312  BINARY_SUBSCR    
              314  LOAD_METHOD              strip
              316  CALL_METHOD_0         0  ''
              318  LOAD_STR                 ''
              320  COMPARE_OP               ==
          322_324  POP_JUMP_IF_FALSE   348  'to 348'

 L. 302       326  LOAD_FAST                'cur_len'
              328  LOAD_GLOBAL              len
              330  LOAD_FAST                'cur_line'
              332  LOAD_CONST               -1
              334  BINARY_SUBSCR    
              336  CALL_FUNCTION_1       1  ''
              338  INPLACE_SUBTRACT 
              340  STORE_FAST               'cur_len'

 L. 303       342  LOAD_FAST                'cur_line'
              344  LOAD_CONST               -1
              346  DELETE_SUBSCR    
            348_0  COME_FROM           322  '322'
            348_1  COME_FROM           304  '304'
            348_2  COME_FROM           298  '298'

 L. 305       348  LOAD_FAST                'cur_line'
              350  POP_JUMP_IF_FALSE_BACK   106  'to 106'

 L. 306       352  LOAD_FAST                'self'
              354  LOAD_ATTR                max_lines
              356  LOAD_CONST               None
              358  COMPARE_OP               is
          360_362  POP_JUMP_IF_TRUE    436  'to 436'

 L. 307       364  LOAD_GLOBAL              len
              366  LOAD_FAST                'lines'
              368  CALL_FUNCTION_1       1  ''
              370  LOAD_CONST               1
              372  BINARY_ADD       
              374  LOAD_FAST                'self'
              376  LOAD_ATTR                max_lines
              378  COMPARE_OP               <

 L. 306   380_382  POP_JUMP_IF_TRUE    436  'to 436'

 L. 308       384  LOAD_FAST                'chunks'

 L. 306   386_388  POP_JUMP_IF_FALSE   426  'to 426'

 L. 309       390  LOAD_FAST                'self'
              392  LOAD_ATTR                drop_whitespace

 L. 306   394_396  POP_JUMP_IF_FALSE   458  'to 458'

 L. 310       398  LOAD_GLOBAL              len
              400  LOAD_FAST                'chunks'
              402  CALL_FUNCTION_1       1  ''
              404  LOAD_CONST               1
              406  COMPARE_OP               ==

 L. 306   408_410  POP_JUMP_IF_FALSE   458  'to 458'

 L. 311       412  LOAD_FAST                'chunks'
              414  LOAD_CONST               0
              416  BINARY_SUBSCR    
              418  LOAD_METHOD              strip
              420  CALL_METHOD_0         0  ''

 L. 306   422_424  POP_JUMP_IF_TRUE    458  'to 458'
            426_0  COME_FROM           386  '386'

 L. 311       426  LOAD_FAST                'cur_len'
              428  LOAD_FAST                'width'
              430  COMPARE_OP               <=

 L. 306   432_434  POP_JUMP_IF_FALSE   458  'to 458'
            436_0  COME_FROM           380  '380'
            436_1  COME_FROM           360  '360'

 L. 314       436  LOAD_FAST                'lines'
              438  LOAD_METHOD              append
              440  LOAD_FAST                'indent'
              442  LOAD_STR                 ''
              444  LOAD_METHOD              join
              446  LOAD_FAST                'cur_line'
              448  CALL_METHOD_1         1  ''
              450  BINARY_ADD       
              452  CALL_METHOD_1         1  ''
              454  POP_TOP          
              456  JUMP_BACK           106  'to 106'
            458_0  COME_FROM           556  '556'
            458_1  COME_FROM           432  '432'
            458_2  COME_FROM           422  '422'
            458_3  COME_FROM           408  '408'
            458_4  COME_FROM           394  '394'

 L. 316       458  LOAD_FAST                'cur_line'
          460_462  POP_JUMP_IF_FALSE   560  'to 560'

 L. 317       464  LOAD_FAST                'cur_line'
              466  LOAD_CONST               -1
              468  BINARY_SUBSCR    
              470  LOAD_METHOD              strip
              472  CALL_METHOD_0         0  ''
          474_476  POP_JUMP_IF_FALSE   534  'to 534'

 L. 318       478  LOAD_FAST                'cur_len'
              480  LOAD_GLOBAL              len
              482  LOAD_FAST                'self'
              484  LOAD_ATTR                placeholder
              486  CALL_FUNCTION_1       1  ''
              488  BINARY_ADD       
              490  LOAD_FAST                'width'
              492  COMPARE_OP               <=

 L. 317   494_496  POP_JUMP_IF_FALSE   534  'to 534'

 L. 319       498  LOAD_FAST                'cur_line'
              500  LOAD_METHOD              append
              502  LOAD_FAST                'self'
              504  LOAD_ATTR                placeholder
              506  CALL_METHOD_1         1  ''
              508  POP_TOP          

 L. 320       510  LOAD_FAST                'lines'
              512  LOAD_METHOD              append
              514  LOAD_FAST                'indent'
              516  LOAD_STR                 ''
              518  LOAD_METHOD              join
              520  LOAD_FAST                'cur_line'
              522  CALL_METHOD_1         1  ''
              524  BINARY_ADD       
              526  CALL_METHOD_1         1  ''
              528  POP_TOP          

 L. 321   530_532  JUMP_FORWARD        648  'to 648'
            534_0  COME_FROM           494  '494'
            534_1  COME_FROM           474  '474'

 L. 322       534  LOAD_FAST                'cur_len'
              536  LOAD_GLOBAL              len
              538  LOAD_FAST                'cur_line'
              540  LOAD_CONST               -1
              542  BINARY_SUBSCR    
              544  CALL_FUNCTION_1       1  ''
              546  INPLACE_SUBTRACT 
              548  STORE_FAST               'cur_len'

 L. 323       550  LOAD_FAST                'cur_line'
              552  LOAD_CONST               -1
              554  DELETE_SUBSCR    
          556_558  JUMP_BACK           458  'to 458'
            560_0  COME_FROM           460  '460'

 L. 325       560  LOAD_FAST                'lines'
          562_564  POP_JUMP_IF_FALSE   622  'to 622'

 L. 326       566  LOAD_FAST                'lines'
              568  LOAD_CONST               -1
              570  BINARY_SUBSCR    
              572  LOAD_METHOD              rstrip
              574  CALL_METHOD_0         0  ''
              576  STORE_FAST               'prev_line'

 L. 327       578  LOAD_GLOBAL              len
              580  LOAD_FAST                'prev_line'
              582  CALL_FUNCTION_1       1  ''
              584  LOAD_GLOBAL              len
              586  LOAD_FAST                'self'
              588  LOAD_ATTR                placeholder
              590  CALL_FUNCTION_1       1  ''
              592  BINARY_ADD       

 L. 328       594  LOAD_FAST                'self'
              596  LOAD_ATTR                width

 L. 327       598  COMPARE_OP               <=
          600_602  POP_JUMP_IF_FALSE   622  'to 622'

 L. 329       604  LOAD_FAST                'prev_line'
              606  LOAD_FAST                'self'
              608  LOAD_ATTR                placeholder
              610  BINARY_ADD       
              612  LOAD_FAST                'lines'
              614  LOAD_CONST               -1
              616  STORE_SUBSCR     

 L. 330   618_620  JUMP_FORWARD        648  'to 648'
            622_0  COME_FROM           600  '600'
            622_1  COME_FROM           562  '562'

 L. 331       622  LOAD_FAST                'lines'
              624  LOAD_METHOD              append
              626  LOAD_FAST                'indent'
              628  LOAD_FAST                'self'
              630  LOAD_ATTR                placeholder
              632  LOAD_METHOD              lstrip
              634  CALL_METHOD_0         0  ''
              636  BINARY_ADD       
              638  CALL_METHOD_1         1  ''
              640  POP_TOP          

 L. 332   642_644  JUMP_FORWARD        648  'to 648'
              646  JUMP_BACK           106  'to 106'
            648_0  COME_FROM           642  '642'
            648_1  COME_FROM           618  '618'
            648_2  COME_FROM           530  '530'
            648_3  COME_FROM           108  '108'

 L. 334       648  LOAD_FAST                'lines'
              650  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 646

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

def dedent(text):
    r"""Remove any common leading whitespace from every line in `text`.

    This can be used to make triple-quoted strings line up with the left
    edge of the display, while still presenting them in the source code
    in indented form.

    Note that tabs and spaces are both treated as whitespace, but they
    are not equal: the lines "  hello" and "\thello" are
    considered to have no common leading whitespace.

    Entirely blank lines are normalized to a newline character.
    """
    margin = None
    text = _whitespace_only_re.sub('', text)
    indents = _leading_whitespace_re.findall(text)
    for indent in indents:
        if margin is None:
            margin = indent
        else:
            if indent.startswith(margin):
                pass
            elif margin.startswith(indent):
                margin = indent
    else:
        for i, (x, y) in enumerate(zip(margin, indent)):
            if x != y:
                margin = margin[:i]
                break
        else:
            if 0:
                if margin:
                    for line in text.split('\n'):
                        if line:
                            assert not line.startswith(margin), 'line = %r, margin = %r' % (line, margin)
                    else:
                        if margin:
                            text = re.sub('(?m)^' + margin, '', text)

                return text


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
            yield prefix + line if predicate(line) else line

    return ''.join(prefixed_lines())


if __name__ == '__main__':
    print(dedent('Hello there.\n  This is indented.'))