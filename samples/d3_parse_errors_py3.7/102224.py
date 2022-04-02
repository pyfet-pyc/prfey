# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
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

    word_punct = '[\\w!"\\\'&.,?]'
    letter = '[^\\d\\W]'
    whitespace = '[%s]' % re.escape(_whitespace)
    nowhitespace = '[^' + whitespace[1:]
    wordsep_re = re.compile('\n        ( # any whitespace\n          %(ws)s+\n        | # em-dash between words\n          (?<=%(wp)s) -{2,} (?=\\w)\n        | # word, possibly hyphenated\n          %(nws)s+? (?:\n            # hyphenated word\n              -(?: (?<=%(lt)s{2}-) | (?<=%(lt)s-%(lt)s-))\n              (?= %(lt)s -? %(lt)s)\n            | # end of word\n              (?=%(ws)s|\\Z)\n            | # em-dash\n              (?<=%(wp)s) (?=-{2,}\\w)\n            )\n        )' % {'wp':word_punct,  'lt':letter,  'ws':whitespace, 
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
               24  CALL_FUNCTION_1       1  '1 positional argument'
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
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  LOAD_GLOBAL              len
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                placeholder
               74  LOAD_METHOD              lstrip
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  BINARY_ADD       
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                width
               86  COMPARE_OP               >
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L. 255        90  LOAD_GLOBAL              ValueError
               92  LOAD_STR                 'placeholder too large for max width'
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            88  '88'
             98_1  COME_FROM            36  '36'

 L. 259        98  LOAD_FAST                'chunks'
              100  LOAD_METHOD              reverse
              102  CALL_METHOD_0         0  '0 positional arguments'
              104  POP_TOP          

 L. 261   106_108  SETUP_LOOP          656  'to 656'
            110_0  COME_FROM           652  '652'
            110_1  COME_FROM           464  '464'
            110_2  COME_FROM           358  '358'
              110  LOAD_FAST                'chunks'
          112_114  POP_JUMP_IF_FALSE   654  'to 654'

 L. 265       116  BUILD_LIST_0          0 
              118  STORE_FAST               'cur_line'

 L. 266       120  LOAD_CONST               0
              122  STORE_FAST               'cur_len'

 L. 269       124  LOAD_FAST                'lines'
              126  POP_JUMP_IF_FALSE   136  'to 136'

 L. 270       128  LOAD_FAST                'self'
              130  LOAD_ATTR                subsequent_indent
              132  STORE_FAST               'indent'
              134  JUMP_FORWARD        142  'to 142'
            136_0  COME_FROM           126  '126'

 L. 272       136  LOAD_FAST                'self'
              138  LOAD_ATTR                initial_indent
              140  STORE_FAST               'indent'
            142_0  COME_FROM           134  '134'

 L. 275       142  LOAD_FAST                'self'
              144  LOAD_ATTR                width
              146  LOAD_GLOBAL              len
              148  LOAD_FAST                'indent'
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  BINARY_SUBTRACT  
              154  STORE_FAST               'width'

 L. 279       156  LOAD_FAST                'self'
              158  LOAD_ATTR                drop_whitespace
              160  POP_JUMP_IF_FALSE   188  'to 188'
              162  LOAD_FAST                'chunks'
              164  LOAD_CONST               -1
              166  BINARY_SUBSCR    
              168  LOAD_METHOD              strip
              170  CALL_METHOD_0         0  '0 positional arguments'
              172  LOAD_STR                 ''
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   188  'to 188'
              178  LOAD_FAST                'lines'
              180  POP_JUMP_IF_FALSE   188  'to 188'

 L. 280       182  LOAD_FAST                'chunks'
              184  LOAD_CONST               -1
              186  DELETE_SUBSCR    
            188_0  COME_FROM           180  '180'
            188_1  COME_FROM           176  '176'
            188_2  COME_FROM           160  '160'

 L. 282       188  SETUP_LOOP          248  'to 248'
            190_0  COME_FROM           244  '244'
            190_1  COME_FROM           240  '240'
              190  LOAD_FAST                'chunks'
              192  POP_JUMP_IF_FALSE   246  'to 246'

 L. 283       194  LOAD_GLOBAL              len
              196  LOAD_FAST                'chunks'
              198  LOAD_CONST               -1
              200  BINARY_SUBSCR    
              202  CALL_FUNCTION_1       1  '1 positional argument'
              204  STORE_FAST               'l'

 L. 286       206  LOAD_FAST                'cur_len'
              208  LOAD_FAST                'l'
              210  BINARY_ADD       
              212  LOAD_FAST                'width'
              214  COMPARE_OP               <=
              216  POP_JUMP_IF_FALSE   242  'to 242'

 L. 287       218  LOAD_FAST                'cur_line'
              220  LOAD_METHOD              append
              222  LOAD_FAST                'chunks'
              224  LOAD_METHOD              pop
              226  CALL_METHOD_0         0  '0 positional arguments'
              228  CALL_METHOD_1         1  '1 positional argument'
              230  POP_TOP          

 L. 288       232  LOAD_FAST                'cur_len'
              234  LOAD_FAST                'l'
              236  INPLACE_ADD      
              238  STORE_FAST               'cur_len'
              240  JUMP_BACK           190  'to 190'
            242_0  COME_FROM           216  '216'

 L. 292       242  BREAK_LOOP       
              244  JUMP_BACK           190  'to 190'
            246_0  COME_FROM           192  '192'
              246  POP_BLOCK        
            248_0  COME_FROM_LOOP      188  '188'

 L. 296       248  LOAD_FAST                'chunks'
          250_252  POP_JUMP_IF_FALSE   302  'to 302'
              254  LOAD_GLOBAL              len
              256  LOAD_FAST                'chunks'
              258  LOAD_CONST               -1
              260  BINARY_SUBSCR    
              262  CALL_FUNCTION_1       1  '1 positional argument'
              264  LOAD_FAST                'width'
              266  COMPARE_OP               >
          268_270  POP_JUMP_IF_FALSE   302  'to 302'

 L. 297       272  LOAD_FAST                'self'
              274  LOAD_METHOD              _handle_long_word
              276  LOAD_FAST                'chunks'
              278  LOAD_FAST                'cur_line'
              280  LOAD_FAST                'cur_len'
              282  LOAD_FAST                'width'
              284  CALL_METHOD_4         4  '4 positional arguments'
              286  POP_TOP          

 L. 298       288  LOAD_GLOBAL              sum
              290  LOAD_GLOBAL              map
              292  LOAD_GLOBAL              len
              294  LOAD_FAST                'cur_line'
              296  CALL_FUNCTION_2       2  '2 positional arguments'
              298  CALL_FUNCTION_1       1  '1 positional argument'
              300  STORE_FAST               'cur_len'
            302_0  COME_FROM           268  '268'
            302_1  COME_FROM           250  '250'

 L. 301       302  LOAD_FAST                'self'
              304  LOAD_ATTR                drop_whitespace
          306_308  POP_JUMP_IF_FALSE   356  'to 356'
              310  LOAD_FAST                'cur_line'
          312_314  POP_JUMP_IF_FALSE   356  'to 356'
              316  LOAD_FAST                'cur_line'
              318  LOAD_CONST               -1
              320  BINARY_SUBSCR    
              322  LOAD_METHOD              strip
              324  CALL_METHOD_0         0  '0 positional arguments'
              326  LOAD_STR                 ''
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_FALSE   356  'to 356'

 L. 302       334  LOAD_FAST                'cur_len'
              336  LOAD_GLOBAL              len
              338  LOAD_FAST                'cur_line'
              340  LOAD_CONST               -1
              342  BINARY_SUBSCR    
              344  CALL_FUNCTION_1       1  '1 positional argument'
              346  INPLACE_SUBTRACT 
              348  STORE_FAST               'cur_len'

 L. 303       350  LOAD_FAST                'cur_line'
              352  LOAD_CONST               -1
              354  DELETE_SUBSCR    
            356_0  COME_FROM           330  '330'
            356_1  COME_FROM           312  '312'
            356_2  COME_FROM           306  '306'

 L. 305       356  LOAD_FAST                'cur_line'
              358  POP_JUMP_IF_FALSE_BACK   110  'to 110'

 L. 306       360  LOAD_FAST                'self'
              362  LOAD_ATTR                max_lines
              364  LOAD_CONST               None
              366  COMPARE_OP               is
          368_370  POP_JUMP_IF_TRUE    444  'to 444'

 L. 307       372  LOAD_GLOBAL              len
              374  LOAD_FAST                'lines'
              376  CALL_FUNCTION_1       1  '1 positional argument'
              378  LOAD_CONST               1
              380  BINARY_ADD       
              382  LOAD_FAST                'self'
              384  LOAD_ATTR                max_lines
              386  COMPARE_OP               <
          388_390  POP_JUMP_IF_TRUE    444  'to 444'

 L. 308       392  LOAD_FAST                'chunks'
          394_396  POP_JUMP_IF_FALSE   434  'to 434'

 L. 309       398  LOAD_FAST                'self'
              400  LOAD_ATTR                drop_whitespace
          402_404  POP_JUMP_IF_FALSE   466  'to 466'

 L. 310       406  LOAD_GLOBAL              len
              408  LOAD_FAST                'chunks'
              410  CALL_FUNCTION_1       1  '1 positional argument'
              412  LOAD_CONST               1
              414  COMPARE_OP               ==
          416_418  POP_JUMP_IF_FALSE   466  'to 466'

 L. 311       420  LOAD_FAST                'chunks'
              422  LOAD_CONST               0
              424  BINARY_SUBSCR    
              426  LOAD_METHOD              strip
              428  CALL_METHOD_0         0  '0 positional arguments'
          430_432  POP_JUMP_IF_TRUE    466  'to 466'
            434_0  COME_FROM           394  '394'
              434  LOAD_FAST                'cur_len'
              436  LOAD_FAST                'width'
              438  COMPARE_OP               <=
          440_442  POP_JUMP_IF_FALSE   466  'to 466'
            444_0  COME_FROM           388  '388'
            444_1  COME_FROM           368  '368'

 L. 314       444  LOAD_FAST                'lines'
              446  LOAD_METHOD              append
              448  LOAD_FAST                'indent'
              450  LOAD_STR                 ''
              452  LOAD_METHOD              join
              454  LOAD_FAST                'cur_line'
              456  CALL_METHOD_1         1  '1 positional argument'
              458  BINARY_ADD       
              460  CALL_METHOD_1         1  '1 positional argument'
              462  POP_TOP          
              464  JUMP_BACK           110  'to 110'
            466_0  COME_FROM           440  '440'
            466_1  COME_FROM           430  '430'
            466_2  COME_FROM           416  '416'
            466_3  COME_FROM           402  '402'

 L. 316       466  SETUP_LOOP          650  'to 650'
            468_0  COME_FROM           564  '564'
              468  LOAD_FAST                'cur_line'
          470_472  POP_JUMP_IF_FALSE   568  'to 568'

 L. 317       474  LOAD_FAST                'cur_line'
              476  LOAD_CONST               -1
              478  BINARY_SUBSCR    
              480  LOAD_METHOD              strip
              482  CALL_METHOD_0         0  '0 positional arguments'
          484_486  POP_JUMP_IF_FALSE   542  'to 542'

 L. 318       488  LOAD_FAST                'cur_len'
              490  LOAD_GLOBAL              len
              492  LOAD_FAST                'self'
              494  LOAD_ATTR                placeholder
              496  CALL_FUNCTION_1       1  '1 positional argument'
              498  BINARY_ADD       
              500  LOAD_FAST                'width'
              502  COMPARE_OP               <=
          504_506  POP_JUMP_IF_FALSE   542  'to 542'

 L. 319       508  LOAD_FAST                'cur_line'
              510  LOAD_METHOD              append
              512  LOAD_FAST                'self'
              514  LOAD_ATTR                placeholder
              516  CALL_METHOD_1         1  '1 positional argument'
              518  POP_TOP          

 L. 320       520  LOAD_FAST                'lines'
              522  LOAD_METHOD              append
              524  LOAD_FAST                'indent'
              526  LOAD_STR                 ''
              528  LOAD_METHOD              join
              530  LOAD_FAST                'cur_line'
              532  CALL_METHOD_1         1  '1 positional argument'
              534  BINARY_ADD       
              536  CALL_METHOD_1         1  '1 positional argument'
              538  POP_TOP          

 L. 321       540  BREAK_LOOP       
            542_0  COME_FROM           504  '504'
            542_1  COME_FROM           484  '484'

 L. 322       542  LOAD_FAST                'cur_len'
              544  LOAD_GLOBAL              len
              546  LOAD_FAST                'cur_line'
              548  LOAD_CONST               -1
              550  BINARY_SUBSCR    
              552  CALL_FUNCTION_1       1  '1 positional argument'
              554  INPLACE_SUBTRACT 
              556  STORE_FAST               'cur_len'

 L. 323       558  LOAD_FAST                'cur_line'
              560  LOAD_CONST               -1
              562  DELETE_SUBSCR    
          564_566  JUMP_BACK           468  'to 468'
            568_0  COME_FROM           470  '470'
              568  POP_BLOCK        

 L. 325       570  LOAD_FAST                'lines'
          572_574  POP_JUMP_IF_FALSE   630  'to 630'

 L. 326       576  LOAD_FAST                'lines'
              578  LOAD_CONST               -1
              580  BINARY_SUBSCR    
              582  LOAD_METHOD              rstrip
              584  CALL_METHOD_0         0  '0 positional arguments'
              586  STORE_FAST               'prev_line'

 L. 327       588  LOAD_GLOBAL              len
              590  LOAD_FAST                'prev_line'
              592  CALL_FUNCTION_1       1  '1 positional argument'
              594  LOAD_GLOBAL              len
              596  LOAD_FAST                'self'
              598  LOAD_ATTR                placeholder
              600  CALL_FUNCTION_1       1  '1 positional argument'
              602  BINARY_ADD       

 L. 328       604  LOAD_FAST                'self'
              606  LOAD_ATTR                width
              608  COMPARE_OP               <=
          610_612  POP_JUMP_IF_FALSE   630  'to 630'

 L. 329       614  LOAD_FAST                'prev_line'
              616  LOAD_FAST                'self'
              618  LOAD_ATTR                placeholder
              620  BINARY_ADD       
              622  LOAD_FAST                'lines'
              624  LOAD_CONST               -1
              626  STORE_SUBSCR     

 L. 330       628  BREAK_LOOP       
            630_0  COME_FROM           610  '610'
            630_1  COME_FROM           572  '572'

 L. 331       630  LOAD_FAST                'lines'
              632  LOAD_METHOD              append
              634  LOAD_FAST                'indent'
              636  LOAD_FAST                'self'
              638  LOAD_ATTR                placeholder
              640  LOAD_METHOD              lstrip
              642  CALL_METHOD_0         0  '0 positional arguments'
              644  BINARY_ADD       
              646  CALL_METHOD_1         1  '1 positional argument'
              648  POP_TOP          
            650_0  COME_FROM_LOOP      466  '466'

 L. 332       650  BREAK_LOOP       
              652  JUMP_BACK           110  'to 110'
            654_0  COME_FROM           112  '112'
              654  POP_BLOCK        
            656_0  COME_FROM_LOOP      106  '106'

 L. 334       656  LOAD_FAST                'lines'
              658  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 654

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
    considered to have no common leading whitespace.  (This behaviour is
    new in Python 2.5; older versions of this module incorrectly
    expanded tabs before searching for common leading whitespace.)
    """
    margin = None
    text = _whitespace_only_re.sub('', text)
    indents = _leading_whitespace_re.findall(text)
    for indent in indents:
        if margin is None:
            margin = indent
        else:
            if indent.startswith(margin):
                continue
            if margin.startswith(indent):
                margin = indent
            else:
                for i, (x, y) in enumerate(zip(margin, indent)):
                    if x != y:
                        margin = margin[:i]
                        break

    if 0:
        if margin:
            for line in text.split('\n'):
                if line:
                    assert not line.startswith(margin), 'line = %r, margin = %r' % (line, margin)

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