# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
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

    def __init__(self, filename=None, file=None, **options):
        """Construct a new TextFile object.  At least one of 'filename'
           (a string) and 'file' (a file-like object) must be supplied.
           They keyword argument options are described above and affect
           the values returned by 'readline()'."""
        if filename is None:
            if file is None:
                raise RuntimeError("you must supply either or both of 'filename' and 'file'")
        for opt in self.default_options.keys():
            if opt in options:
                setattr(self, opt, options[opt])
            else:
                setattr(self, opt, self.default_options[opt])
        else:
            for opt in options.keys():
                if opt not in self.default_options:
                    raise KeyError("invalid TextFile option '%s'" % opt)
            else:
                if file is None:
                    self.open(filename)
                else:
                    self.filename = filename
                    self.file = file
                    self.current_line = 0
                self.linebuf = []

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
        file.close()

    def gen_error(self, msg, line=None):
        outmsg = []
        if line is None:
            line = self.current_line
        outmsg.append(self.filename + ', ')
        if isinstance(line, (list, tuple)):
            outmsg.append('lines %d-%d: ' % tuple(line))
        else:
            outmsg.append('line %d: ' % line)
        outmsg.append(str(msg))
        return ''.join(outmsg)

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
             32_0  COME_FROM           504  '504'
             32_1  COME_FROM           468  '468'
             32_2  COME_FROM           432  '432'
             32_3  COME_FROM           156  '156'

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

 L. 191        82  JUMP_FORWARD        172  'to 172'
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
              158  BREAK_LOOP          172  'to 172'
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
              190  COMPARE_OP               is
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
              290  COMPARE_OP               is
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

Parse error at or near `RETURN_VALUE' instruction at offset 508

    def readlines(self):
        """Read and return the list of all logical lines remaining in the
           current file."""
        lines = []
        while True:
            line = self.readline()
            if line is None:
                return lines
            else:
                lines.append(line)

    def unreadline(self, line):
        """Push 'line' (a string) onto an internal buffer that will be
           checked by future 'readline()' calls.  Handy for implementing
           a parser with line-at-a-time lookahead."""
        self.linebuf.append(line)