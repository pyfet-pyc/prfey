# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\text_file.py
"""text_file

provides the TextFile class, which gives an interface to text files
that (optionally) takes care of stripping comments, ignoring blank
lines, and joining lines with backslashes."""
import sys, io

class TextFile:
    __doc__ = 'Provides a file-like object that takes care of all the things you\n       commonly want to do when processing a text file that has some\n       line-by-line syntax: strip comments (as long as "#" is your\n       comment character), skip blank lines, join adjacent lines by\n       escaping the newline (ie. backslash at end of line), strip\n       leading and/or trailing whitespace.  All of these are optional\n       and independently controllable.\n\n       Provides a \'warn()\' method so you can generate warning messages that\n       report physical line number, even if the logical line in question\n       spans multiple physical lines.  Also provides \'unreadline()\' for\n       implementing line-at-a-time lookahead.\n\n       Constructor is called as:\n\n           TextFile (filename=None, file=None, **options)\n\n       It bombs (RuntimeError) if both \'filename\' and \'file\' are None;\n       \'filename\' should be a string, and \'file\' a file object (or\n       something that provides \'readline()\' and \'close()\' methods).  It is\n       recommended that you supply at least \'filename\', so that TextFile\n       can include it in warning messages.  If \'file\' is not supplied,\n       TextFile creates its own using \'io.open()\'.\n\n       The options are all boolean, and affect the value returned by\n       \'readline()\':\n         strip_comments [default: true]\n           strip from "#" to end-of-line, as well as any whitespace\n           leading up to the "#" -- unless it is escaped by a backslash\n         lstrip_ws [default: false]\n           strip leading whitespace from each line before returning it\n         rstrip_ws [default: true]\n           strip trailing whitespace (including line terminator!) from\n           each line before returning it\n         skip_blanks [default: true}\n           skip lines that are empty *after* stripping comments and\n           whitespace.  (If both lstrip_ws and rstrip_ws are false,\n           then some lines may consist of solely whitespace: these will\n           *not* be skipped, even if \'skip_blanks\' is true.)\n         join_lines [default: false]\n           if a backslash is the last non-newline character on a line\n           after stripping comments and whitespace, join the following line\n           to it to form one "logical line"; if N consecutive lines end\n           with a backslash, then N+1 physical lines will be joined to\n           form one logical line.\n         collapse_join [default: false]\n           strip leading whitespace from lines that are joined to their\n           predecessor; only matters if (join_lines and not lstrip_ws)\n         errors [default: \'strict\']\n           error handler used to decode the file content\n\n       Note that since \'rstrip_ws\' can strip the trailing newline, the\n       semantics of \'readline()\' must differ from those of the builtin file\n       object\'s \'readline()\' method!  In particular, \'readline()\' returns\n       None for end-of-file: an empty string might just be a blank line (or\n       an all-whitespace line), if \'rstrip_ws\' is true but \'skip_blanks\' is\n       not.'
    default_options = {'strip_comments':1, 
     'skip_blanks':1, 
     'lstrip_ws':0, 
     'rstrip_ws':1, 
     'join_lines':0, 
     'collapse_join':0, 
     'errors':'strict'}

    def __init__--- This code section failed: ---

 L.  83         0  LOAD_FAST                'filename'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'
                8  LOAD_FAST                'file'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L.  84        16  LOAD_GLOBAL              RuntimeError
               18  LOAD_STR                 "you must supply either or both of 'filename' and 'file'"
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'
             24_1  COME_FROM             6  '6'

 L.  88        24  LOAD_FAST                'self'
               26  LOAD_ATTR                default_options
               28  LOAD_METHOD              keys
               30  CALL_METHOD_0         0  ''
               32  GET_ITER         
               34  FOR_ITER             84  'to 84'
               36  STORE_FAST               'opt'

 L.  89        38  LOAD_FAST                'opt'
               40  LOAD_FAST                'options'
               42  <118>                 0  ''
               44  POP_JUMP_IF_FALSE    64  'to 64'

 L.  90        46  LOAD_GLOBAL              setattr
               48  LOAD_FAST                'self'
               50  LOAD_FAST                'opt'
               52  LOAD_FAST                'options'
               54  LOAD_FAST                'opt'
               56  BINARY_SUBSCR    
               58  CALL_FUNCTION_3       3  ''
               60  POP_TOP          
               62  JUMP_BACK            34  'to 34'
             64_0  COME_FROM            44  '44'

 L.  92        64  LOAD_GLOBAL              setattr
               66  LOAD_FAST                'self'
               68  LOAD_FAST                'opt'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                default_options
               74  LOAD_FAST                'opt'
               76  BINARY_SUBSCR    
               78  CALL_FUNCTION_3       3  ''
               80  POP_TOP          
               82  JUMP_BACK            34  'to 34'

 L.  95        84  LOAD_FAST                'options'
               86  LOAD_METHOD              keys
               88  CALL_METHOD_0         0  ''
               90  GET_ITER         
             92_0  COME_FROM           104  '104'
               92  FOR_ITER            120  'to 120'
               94  STORE_FAST               'opt'

 L.  96        96  LOAD_FAST                'opt'
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                default_options
              102  <118>                 1  ''
              104  POP_JUMP_IF_FALSE    92  'to 92'

 L.  97       106  LOAD_GLOBAL              KeyError
              108  LOAD_STR                 "invalid TextFile option '%s'"
              110  LOAD_FAST                'opt'
              112  BINARY_MODULO    
              114  CALL_FUNCTION_1       1  ''
              116  RAISE_VARARGS_1       1  'exception instance'
              118  JUMP_BACK            92  'to 92'

 L.  99       120  LOAD_FAST                'file'
              122  LOAD_CONST               None
              124  <117>                 0  ''
              126  POP_JUMP_IF_FALSE   140  'to 140'

 L. 100       128  LOAD_FAST                'self'
              130  LOAD_METHOD              open
              132  LOAD_FAST                'filename'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
              138  JUMP_FORWARD        158  'to 158'
            140_0  COME_FROM           126  '126'

 L. 102       140  LOAD_FAST                'filename'
              142  LOAD_FAST                'self'
              144  STORE_ATTR               filename

 L. 103       146  LOAD_FAST                'file'
              148  LOAD_FAST                'self'
              150  STORE_ATTR               file

 L. 104       152  LOAD_CONST               0
              154  LOAD_FAST                'self'
              156  STORE_ATTR               current_line
            158_0  COME_FROM           138  '138'

 L. 109       158  BUILD_LIST_0          0 
              160  LOAD_FAST                'self'
              162  STORE_ATTR               linebuf

Parse error at or near `None' instruction at offset -1

    def open(self, filename):
        """Open a new file named 'filename'.  This overrides both the
           'filename' and 'file' arguments to the constructor."""
        self.filename = filename
        self.file = io.open((self.filename), 'r', errors=(self.errors))
        self.current_line = 0

    def close(self):
        """Close the current file and forget everything we know about it
           (filename, current line number)."""
        file = self.file
        self.file = None
        self.filename = None
        self.current_line = None
        file.close

    def gen_error--- This code section failed: ---

 L. 128         0  BUILD_LIST_0          0 
                2  STORE_FAST               'outmsg'

 L. 129         4  LOAD_FAST                'line'
                6  LOAD_CONST               None
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    18  'to 18'

 L. 130        12  LOAD_FAST                'self'
               14  LOAD_ATTR                current_line
               16  STORE_FAST               'line'
             18_0  COME_FROM            10  '10'

 L. 131        18  LOAD_FAST                'outmsg'
               20  LOAD_METHOD              append
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                filename
               26  LOAD_STR                 ', '
               28  BINARY_ADD       
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L. 132        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'line'
               38  LOAD_GLOBAL              list
               40  LOAD_GLOBAL              tuple
               42  BUILD_TUPLE_2         2 
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_FALSE    68  'to 68'

 L. 133        48  LOAD_FAST                'outmsg'
               50  LOAD_METHOD              append
               52  LOAD_STR                 'lines %d-%d: '
               54  LOAD_GLOBAL              tuple
               56  LOAD_FAST                'line'
               58  CALL_FUNCTION_1       1  ''
               60  BINARY_MODULO    
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
               66  JUMP_FORWARD         82  'to 82'
             68_0  COME_FROM            46  '46'

 L. 135        68  LOAD_FAST                'outmsg'
               70  LOAD_METHOD              append
               72  LOAD_STR                 'line %d: '
               74  LOAD_FAST                'line'
               76  BINARY_MODULO    
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
             82_0  COME_FROM            66  '66'

 L. 136        82  LOAD_FAST                'outmsg'
               84  LOAD_METHOD              append
               86  LOAD_GLOBAL              str
               88  LOAD_FAST                'msg'
               90  CALL_FUNCTION_1       1  ''
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          

 L. 137        96  LOAD_STR                 ''
               98  LOAD_METHOD              join
              100  LOAD_FAST                'outmsg'
              102  CALL_METHOD_1         1  ''
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 8

    def error(self, msg, line=None):
        raise ValueError('error: ' + self.gen_error(msg, line))

    def warn(self, msg, line=None):
        """Print (to stderr) a warning message tied to the current logical
           line in the current file.  If the current logical line in the
           file spans multiple physical lines, the warning refers to the
           whole range, eg. "lines 3-5".  If 'line' supplied, it overrides
           the current line number; it may be a list or tuple to indicate a
           range of physical lines, or an integer for a single physical
           line."""
        sys.stderr.write('warning: ' + self.gen_error(msg, line) + '\n')

    def readline--- This code section failed: ---

 L. 166         0  LOAD_FAST                'self'
                2  LOAD_ATTR                linebuf
                4  POP_JUMP_IF_FALSE    28  'to 28'

 L. 167         6  LOAD_FAST                'self'
                8  LOAD_ATTR                linebuf
               10  LOAD_CONST               -1
               12  BINARY_SUBSCR    
               14  STORE_FAST               'line'

 L. 168        16  LOAD_FAST                'self'
               18  LOAD_ATTR                linebuf
               20  LOAD_CONST               -1
               22  DELETE_SUBSCR    

 L. 169        24  LOAD_FAST                'line'
               26  RETURN_VALUE     
             28_0  COME_FROM             4  '4'

 L. 171        28  LOAD_STR                 ''
               30  STORE_FAST               'buildup_line'

 L. 175        32  LOAD_FAST                'self'
               34  LOAD_ATTR                file
               36  LOAD_METHOD              readline
               38  CALL_METHOD_0         0  ''
               40  STORE_FAST               'line'

 L. 176        42  LOAD_FAST                'line'
               44  LOAD_STR                 ''
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    54  'to 54'

 L. 177        50  LOAD_CONST               None
               52  STORE_FAST               'line'
             54_0  COME_FROM            48  '48'

 L. 179        54  LOAD_FAST                'self'
               56  LOAD_ATTR                strip_comments
               58  POP_JUMP_IF_FALSE   172  'to 172'
               60  LOAD_FAST                'line'
               62  POP_JUMP_IF_FALSE   172  'to 172'

 L. 189        64  LOAD_FAST                'line'
               66  LOAD_METHOD              find
               68  LOAD_STR                 '#'
               70  CALL_METHOD_1         1  ''
               72  STORE_FAST               'pos'

 L. 190        74  LOAD_FAST                'pos'
               76  LOAD_CONST               -1
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    84  'to 84'

 L. 191        82  BREAK_LOOP          172  'to 172'
             84_0  COME_FROM            80  '80'

 L. 195        84  LOAD_FAST                'pos'
               86  LOAD_CONST               0
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_TRUE    108  'to 108'
               92  LOAD_FAST                'line'
               94  LOAD_FAST                'pos'
               96  LOAD_CONST               1
               98  BINARY_SUBTRACT  
              100  BINARY_SUBSCR    
              102  LOAD_STR                 '\\'
              104  COMPARE_OP               !=
              106  POP_JUMP_IF_FALSE   160  'to 160'
            108_0  COME_FROM            90  '90'

 L. 202       108  LOAD_FAST                'line'
              110  LOAD_CONST               -1
              112  BINARY_SUBSCR    
              114  LOAD_STR                 '\n'
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_FALSE   124  'to 124'
              120  LOAD_STR                 '\n'
              122  JUMP_IF_TRUE_OR_POP   126  'to 126'
            124_0  COME_FROM           118  '118'
              124  LOAD_STR                 ''
            126_0  COME_FROM           122  '122'
              126  STORE_FAST               'eol'

 L. 203       128  LOAD_FAST                'line'
              130  LOAD_CONST               0
              132  LOAD_FAST                'pos'
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  LOAD_FAST                'eol'
              140  BINARY_ADD       
              142  STORE_FAST               'line'

 L. 212       144  LOAD_FAST                'line'
              146  LOAD_METHOD              strip
              148  CALL_METHOD_0         0  ''
              150  LOAD_STR                 ''
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   172  'to 172'

 L. 213       156  JUMP_BACK            32  'to 32'
              158  JUMP_FORWARD        172  'to 172'
            160_0  COME_FROM           106  '106'

 L. 215       160  LOAD_FAST                'line'
              162  LOAD_METHOD              replace
              164  LOAD_STR                 '\\#'
              166  LOAD_STR                 '#'
              168  CALL_METHOD_2         2  ''
              170  STORE_FAST               'line'
            172_0  COME_FROM           158  '158'
            172_1  COME_FROM           154  '154'
            172_2  COME_FROM            82  '82'
            172_3  COME_FROM            62  '62'
            172_4  COME_FROM            58  '58'

 L. 218       172  LOAD_FAST                'self'
              174  LOAD_ATTR                join_lines
          176_178  POP_JUMP_IF_FALSE   286  'to 286'
              180  LOAD_FAST                'buildup_line'
          182_184  POP_JUMP_IF_FALSE   286  'to 286'

 L. 220       186  LOAD_FAST                'line'
              188  LOAD_CONST               None
              190  <117>                 0  ''
              192  POP_JUMP_IF_FALSE   208  'to 208'

 L. 221       194  LOAD_FAST                'self'
              196  LOAD_METHOD              warn
              198  LOAD_STR                 'continuation line immediately precedes end-of-file'
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          

 L. 223       204  LOAD_FAST                'buildup_line'
              206  RETURN_VALUE     
            208_0  COME_FROM           192  '192'

 L. 225       208  LOAD_FAST                'self'
              210  LOAD_ATTR                collapse_join
              212  POP_JUMP_IF_FALSE   222  'to 222'

 L. 226       214  LOAD_FAST                'line'
              216  LOAD_METHOD              lstrip
              218  CALL_METHOD_0         0  ''
              220  STORE_FAST               'line'
            222_0  COME_FROM           212  '212'

 L. 227       222  LOAD_FAST                'buildup_line'
              224  LOAD_FAST                'line'
              226  BINARY_ADD       
              228  STORE_FAST               'line'

 L. 230       230  LOAD_GLOBAL              isinstance
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                current_line
              236  LOAD_GLOBAL              list
              238  CALL_FUNCTION_2       2  ''
          240_242  POP_JUMP_IF_FALSE   266  'to 266'

 L. 231       244  LOAD_FAST                'self'
              246  LOAD_ATTR                current_line
              248  LOAD_CONST               1
              250  BINARY_SUBSCR    
              252  LOAD_CONST               1
              254  BINARY_ADD       
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                current_line
              260  LOAD_CONST               1
              262  STORE_SUBSCR     
              264  JUMP_FORWARD        284  'to 284'
            266_0  COME_FROM           240  '240'

 L. 233       266  LOAD_FAST                'self'
              268  LOAD_ATTR                current_line

 L. 234       270  LOAD_FAST                'self'
              272  LOAD_ATTR                current_line
              274  LOAD_CONST               1
              276  BINARY_ADD       

 L. 233       278  BUILD_LIST_2          2 
              280  LOAD_FAST                'self'
              282  STORE_ATTR               current_line
            284_0  COME_FROM           264  '264'
              284  JUMP_FORWARD        344  'to 344'
            286_0  COME_FROM           182  '182'
            286_1  COME_FROM           176  '176'

 L. 237       286  LOAD_FAST                'line'
              288  LOAD_CONST               None
              290  <117>                 0  ''
          292_294  POP_JUMP_IF_FALSE   300  'to 300'

 L. 238       296  LOAD_CONST               None
              298  RETURN_VALUE     
            300_0  COME_FROM           292  '292'

 L. 241       300  LOAD_GLOBAL              isinstance
              302  LOAD_FAST                'self'
              304  LOAD_ATTR                current_line
              306  LOAD_GLOBAL              list
              308  CALL_FUNCTION_2       2  ''
          310_312  POP_JUMP_IF_FALSE   332  'to 332'

 L. 242       314  LOAD_FAST                'self'
              316  LOAD_ATTR                current_line
              318  LOAD_CONST               1
              320  BINARY_SUBSCR    
              322  LOAD_CONST               1
              324  BINARY_ADD       
              326  LOAD_FAST                'self'
              328  STORE_ATTR               current_line
              330  JUMP_FORWARD        344  'to 344'
            332_0  COME_FROM           310  '310'

 L. 244       332  LOAD_FAST                'self'
              334  LOAD_ATTR                current_line
              336  LOAD_CONST               1
              338  BINARY_ADD       
              340  LOAD_FAST                'self'
              342  STORE_ATTR               current_line
            344_0  COME_FROM           330  '330'
            344_1  COME_FROM           284  '284'

 L. 248       344  LOAD_FAST                'self'
              346  LOAD_ATTR                lstrip_ws
          348_350  POP_JUMP_IF_FALSE   370  'to 370'
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                rstrip_ws
          356_358  POP_JUMP_IF_FALSE   370  'to 370'

 L. 249       360  LOAD_FAST                'line'
              362  LOAD_METHOD              strip
              364  CALL_METHOD_0         0  ''
              366  STORE_FAST               'line'
              368  JUMP_FORWARD        404  'to 404'
            370_0  COME_FROM           356  '356'
            370_1  COME_FROM           348  '348'

 L. 250       370  LOAD_FAST                'self'
              372  LOAD_ATTR                lstrip_ws
          374_376  POP_JUMP_IF_FALSE   388  'to 388'

 L. 251       378  LOAD_FAST                'line'
              380  LOAD_METHOD              lstrip
              382  CALL_METHOD_0         0  ''
              384  STORE_FAST               'line'
              386  JUMP_FORWARD        404  'to 404'
            388_0  COME_FROM           374  '374'

 L. 252       388  LOAD_FAST                'self'
              390  LOAD_ATTR                rstrip_ws
          392_394  POP_JUMP_IF_FALSE   404  'to 404'

 L. 253       396  LOAD_FAST                'line'
              398  LOAD_METHOD              rstrip
              400  CALL_METHOD_0         0  ''
              402  STORE_FAST               'line'
            404_0  COME_FROM           392  '392'
            404_1  COME_FROM           386  '386'
            404_2  COME_FROM           368  '368'

 L. 257       404  LOAD_FAST                'line'
              406  LOAD_STR                 ''
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_TRUE    424  'to 424'
              414  LOAD_FAST                'line'
              416  LOAD_STR                 '\n'
              418  COMPARE_OP               ==
          420_422  POP_JUMP_IF_FALSE   434  'to 434'
            424_0  COME_FROM           410  '410'
              424  LOAD_FAST                'self'
              426  LOAD_ATTR                skip_blanks
          428_430  POP_JUMP_IF_FALSE   434  'to 434'

 L. 258       432  JUMP_BACK            32  'to 32'
            434_0  COME_FROM           428  '428'
            434_1  COME_FROM           420  '420'

 L. 260       434  LOAD_FAST                'self'
              436  LOAD_ATTR                join_lines
          438_440  POP_JUMP_IF_FALSE   506  'to 506'

 L. 261       442  LOAD_FAST                'line'
              444  LOAD_CONST               -1
              446  BINARY_SUBSCR    
              448  LOAD_STR                 '\\'
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_FALSE   470  'to 470'

 L. 262       456  LOAD_FAST                'line'
              458  LOAD_CONST               None
              460  LOAD_CONST               -1
              462  BUILD_SLICE_2         2 
              464  BINARY_SUBSCR    
              466  STORE_FAST               'buildup_line'

 L. 263       468  JUMP_BACK            32  'to 32'
            470_0  COME_FROM           452  '452'

 L. 265       470  LOAD_FAST                'line'
              472  LOAD_CONST               -2
              474  LOAD_CONST               None
              476  BUILD_SLICE_2         2 
              478  BINARY_SUBSCR    
              480  LOAD_STR                 '\\\n'
              482  COMPARE_OP               ==
          484_486  POP_JUMP_IF_FALSE   506  'to 506'

 L. 266       488  LOAD_FAST                'line'
              490  LOAD_CONST               0
              492  LOAD_CONST               -2
              494  BUILD_SLICE_2         2 
              496  BINARY_SUBSCR    
              498  LOAD_STR                 '\n'
              500  BINARY_ADD       
              502  STORE_FAST               'buildup_line'

 L. 267       504  JUMP_BACK            32  'to 32'
            506_0  COME_FROM           484  '484'
            506_1  COME_FROM           438  '438'

 L. 270       506  LOAD_FAST                'line'
              508  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 158

    def readlines--- This code section failed: ---

 L. 275         0  BUILD_LIST_0          0 
                2  STORE_FAST               'lines'

 L. 277         4  LOAD_FAST                'self'
                6  LOAD_METHOD              readline
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'line'

 L. 278        12  LOAD_FAST                'line'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 279        20  LOAD_FAST                'lines'
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 280        24  LOAD_FAST                'lines'
               26  LOAD_METHOD              append
               28  LOAD_FAST                'line'
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          
               34  JUMP_BACK             4  'to 4'

Parse error at or near `<117>' instruction at offset 16

    def unreadline(self, line):
        """Push 'line' (a string) onto an internal buffer that will be
           checked by future 'readline()' calls.  Handy for implementing
           a parser with line-at-a-time lookahead."""
        self.linebuf.appendline