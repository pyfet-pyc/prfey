# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cmd.py
"""A generic class to build line-oriented command interpreters.

Interpreters constructed with this class obey the following conventions:

1. End of file on input is processed as the command 'EOF'.
2. A command is parsed out of each line by collecting the prefix composed
   of characters in the identchars member.
3. A command `foo' is dispatched to a method 'do_foo()'; the do_ method
   is passed a single argument consisting of the remainder of the line.
4. Typing an empty line repeats the last command.  (Actually, it calls the
   method `emptyline', which may be overridden in a subclass.)
5. There is a predefined `help' method.  Given an argument `topic', it
   calls the command `help_topic'.  With no arguments, it lists all topics
   with defined help_ functions, broken into up to three topics; documented
   commands, miscellaneous help topics, and undocumented commands.
6. The command '?' is a synonym for `help'.  The command '!' is a synonym
   for `shell', if a do_shell method exists.
7. If completion is enabled, completing commands will be done automatically,
   and completing of commands args is done by calling complete_foo() with
   arguments text, line, begidx, endidx.  text is string we are matching
   against, all returned matches must begin with it.  line is the current
   input line (lstripped), begidx and endidx are the beginning and end
   indexes of the text being matched, which could be used to provide
   different completion depending upon which position the argument is in.

The `default' method may be overridden to intercept commands for which there
is no do_ method.

The `completedefault' method may be overridden to intercept completions for
commands that have no complete_ method.

The data member `self.ruler' sets the character used to draw separator lines
in the help messages.  If empty, no ruler line is drawn.  It defaults to "=".

If the value of `self.intro' is nonempty when the cmdloop method is called,
it is printed out on interpreter startup.  This value may be overridden
via an optional argument to the cmdloop() method.

The data members `self.doc_header', `self.misc_header', and
`self.undoc_header' set the headers used for the help function's
listings of documented functions, miscellaneous topics, and undocumented
functions respectively.
"""
import string, sys
__all__ = [
 'Cmd']
PROMPT = '(Cmd) '
IDENTCHARS = string.ascii_letters + string.digits + '_'

class Cmd:
    __doc__ = "A simple framework for writing line-oriented command interpreters.\n\n    These are often useful for test harnesses, administrative tools, and\n    prototypes that will later be wrapped in a more sophisticated interface.\n\n    A Cmd instance or subclass instance is a line-oriented interpreter\n    framework.  There is no good reason to instantiate Cmd itself; rather,\n    it's useful as a superclass of an interpreter class you define yourself\n    in order to inherit Cmd's methods and encapsulate action methods.\n\n    "
    prompt = PROMPT
    identchars = IDENTCHARS
    ruler = '='
    lastcmd = ''
    intro = None
    doc_leader = ''
    doc_header = 'Documented commands (type help <topic>):'
    misc_header = 'Miscellaneous help topics:'
    undoc_header = 'Undocumented commands:'
    nohelp = '*** No help on %s'
    use_rawinput = 1

    def __init__--- This code section failed: ---

 L.  87         0  LOAD_FAST                'stdin'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  88         8  LOAD_FAST                'stdin'
               10  LOAD_FAST                'self'
               12  STORE_ATTR               stdin
               14  JUMP_FORWARD         24  'to 24'
             16_0  COME_FROM             6  '6'

 L.  90        16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                stdin
               20  LOAD_FAST                'self'
               22  STORE_ATTR               stdin
             24_0  COME_FROM            14  '14'

 L.  91        24  LOAD_FAST                'stdout'
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L.  92        32  LOAD_FAST                'stdout'
               34  LOAD_FAST                'self'
               36  STORE_ATTR               stdout
               38  JUMP_FORWARD         48  'to 48'
             40_0  COME_FROM            30  '30'

 L.  94        40  LOAD_GLOBAL              sys
               42  LOAD_ATTR                stdout
               44  LOAD_FAST                'self'
               46  STORE_ATTR               stdout
             48_0  COME_FROM            38  '38'

 L.  95        48  BUILD_LIST_0          0 
               50  LOAD_FAST                'self'
               52  STORE_ATTR               cmdqueue

 L.  96        54  LOAD_FAST                'completekey'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               completekey

Parse error at or near `None' instruction at offset -1

    def cmdloop--- This code section failed: ---

 L. 105         0  LOAD_FAST                'self'
                2  LOAD_METHOD              preloop
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 106         8  LOAD_FAST                'self'
               10  LOAD_ATTR                use_rawinput
               12  POP_JUMP_IF_FALSE    90  'to 90'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                completekey
               18  POP_JUMP_IF_FALSE    90  'to 90'

 L. 107        20  SETUP_FINALLY        72  'to 72'

 L. 108        22  LOAD_CONST               0
               24  LOAD_CONST               None
               26  IMPORT_NAME              readline
               28  STORE_FAST               'readline'

 L. 109        30  LOAD_FAST                'readline'
               32  LOAD_METHOD              get_completer
               34  CALL_METHOD_0         0  ''
               36  LOAD_FAST                'self'
               38  STORE_ATTR               old_completer

 L. 110        40  LOAD_FAST                'readline'
               42  LOAD_METHOD              set_completer
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                complete
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L. 111        52  LOAD_FAST                'readline'
               54  LOAD_METHOD              parse_and_bind
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                completekey
               60  LOAD_STR                 ': complete'
               62  BINARY_ADD       
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          
               68  POP_BLOCK        
               70  JUMP_FORWARD         90  'to 90'
             72_0  COME_FROM_FINALLY    20  '20'

 L. 112        72  DUP_TOP          
               74  LOAD_GLOBAL              ImportError
               76  <121>                88  ''
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 113        84  POP_EXCEPT       
               86  JUMP_FORWARD         90  'to 90'
               88  <48>             
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM            70  '70'
             90_2  COME_FROM            18  '18'
             90_3  COME_FROM            12  '12'

 L. 114     90_92  SETUP_FINALLY       380  'to 380'

 L. 115        94  LOAD_FAST                'intro'
               96  LOAD_CONST               None
               98  <117>                 1  ''
              100  POP_JUMP_IF_FALSE   108  'to 108'

 L. 116       102  LOAD_FAST                'intro'
              104  LOAD_FAST                'self'
              106  STORE_ATTR               intro
            108_0  COME_FROM           100  '100'

 L. 117       108  LOAD_FAST                'self'
              110  LOAD_ATTR                intro
              112  POP_JUMP_IF_FALSE   136  'to 136'

 L. 118       114  LOAD_FAST                'self'
              116  LOAD_ATTR                stdout
              118  LOAD_METHOD              write
              120  LOAD_GLOBAL              str
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                intro
              126  CALL_FUNCTION_1       1  ''
              128  LOAD_STR                 '\n'
              130  BINARY_ADD       
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
            136_0  COME_FROM           112  '112'

 L. 119       136  LOAD_CONST               None
              138  STORE_FAST               'stop'

 L. 120       140  LOAD_FAST                'stop'
          142_144  POP_JUMP_IF_TRUE    306  'to 306'

 L. 121       146  LOAD_FAST                'self'
              148  LOAD_ATTR                cmdqueue
              150  POP_JUMP_IF_FALSE   166  'to 166'

 L. 122       152  LOAD_FAST                'self'
              154  LOAD_ATTR                cmdqueue
              156  LOAD_METHOD              pop
              158  LOAD_CONST               0
              160  CALL_METHOD_1         1  ''
              162  STORE_FAST               'line'
              164  JUMP_FORWARD        272  'to 272'
            166_0  COME_FROM           150  '150'

 L. 124       166  LOAD_FAST                'self'
              168  LOAD_ATTR                use_rawinput
              170  POP_JUMP_IF_FALSE   212  'to 212'

 L. 125       172  SETUP_FINALLY       188  'to 188'

 L. 126       174  LOAD_GLOBAL              input
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                prompt
              180  CALL_FUNCTION_1       1  ''
              182  STORE_FAST               'line'
              184  POP_BLOCK        
              186  JUMP_FORWARD        210  'to 210'
            188_0  COME_FROM_FINALLY   172  '172'

 L. 127       188  DUP_TOP          
              190  LOAD_GLOBAL              EOFError
              192  <121>               208  ''
              194  POP_TOP          
              196  POP_TOP          
              198  POP_TOP          

 L. 128       200  LOAD_STR                 'EOF'
              202  STORE_FAST               'line'
              204  POP_EXCEPT       
              206  JUMP_FORWARD        210  'to 210'
              208  <48>             
            210_0  COME_FROM           206  '206'
            210_1  COME_FROM           186  '186'
              210  JUMP_FORWARD        272  'to 272'
            212_0  COME_FROM           170  '170'

 L. 130       212  LOAD_FAST                'self'
              214  LOAD_ATTR                stdout
              216  LOAD_METHOD              write
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                prompt
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          

 L. 131       226  LOAD_FAST                'self'
              228  LOAD_ATTR                stdout
              230  LOAD_METHOD              flush
              232  CALL_METHOD_0         0  ''
              234  POP_TOP          

 L. 132       236  LOAD_FAST                'self'
              238  LOAD_ATTR                stdin
              240  LOAD_METHOD              readline
              242  CALL_METHOD_0         0  ''
              244  STORE_FAST               'line'

 L. 133       246  LOAD_GLOBAL              len
              248  LOAD_FAST                'line'
              250  CALL_FUNCTION_1       1  ''
          252_254  POP_JUMP_IF_TRUE    262  'to 262'

 L. 134       256  LOAD_STR                 'EOF'
              258  STORE_FAST               'line'
              260  JUMP_FORWARD        272  'to 272'
            262_0  COME_FROM           252  '252'

 L. 136       262  LOAD_FAST                'line'
              264  LOAD_METHOD              rstrip
              266  LOAD_STR                 '\r\n'
              268  CALL_METHOD_1         1  ''
              270  STORE_FAST               'line'
            272_0  COME_FROM           260  '260'
            272_1  COME_FROM           210  '210'
            272_2  COME_FROM           164  '164'

 L. 137       272  LOAD_FAST                'self'
              274  LOAD_METHOD              precmd
              276  LOAD_FAST                'line'
              278  CALL_METHOD_1         1  ''
              280  STORE_FAST               'line'

 L. 138       282  LOAD_FAST                'self'
              284  LOAD_METHOD              onecmd
              286  LOAD_FAST                'line'
              288  CALL_METHOD_1         1  ''
              290  STORE_FAST               'stop'

 L. 139       292  LOAD_FAST                'self'
              294  LOAD_METHOD              postcmd
              296  LOAD_FAST                'stop'
              298  LOAD_FAST                'line'
              300  CALL_METHOD_2         2  ''
              302  STORE_FAST               'stop'
              304  JUMP_BACK           140  'to 140'
            306_0  COME_FROM           142  '142'

 L. 140       306  LOAD_FAST                'self'
              308  LOAD_METHOD              postloop
              310  CALL_METHOD_0         0  ''
              312  POP_TOP          
              314  POP_BLOCK        

 L. 142       316  LOAD_FAST                'self'
              318  LOAD_ATTR                use_rawinput
          320_322  POP_JUMP_IF_FALSE   444  'to 444'
              324  LOAD_FAST                'self'
              326  LOAD_ATTR                completekey
          328_330  POP_JUMP_IF_FALSE   444  'to 444'

 L. 143       332  SETUP_FINALLY       358  'to 358'

 L. 144       334  LOAD_CONST               0
              336  LOAD_CONST               None
              338  IMPORT_NAME              readline
              340  STORE_FAST               'readline'

 L. 145       342  LOAD_FAST                'readline'
              344  LOAD_METHOD              set_completer
              346  LOAD_FAST                'self'
              348  LOAD_ATTR                old_completer
              350  CALL_METHOD_1         1  ''
              352  POP_TOP          
              354  POP_BLOCK        
              356  JUMP_FORWARD        378  'to 378'
            358_0  COME_FROM_FINALLY   332  '332'

 L. 146       358  DUP_TOP          
              360  LOAD_GLOBAL              ImportError
          362_364  <121>               376  ''
              366  POP_TOP          
              368  POP_TOP          
              370  POP_TOP          

 L. 147       372  POP_EXCEPT       
              374  JUMP_FORWARD        378  'to 378'
              376  <48>             
            378_0  COME_FROM           374  '374'
            378_1  COME_FROM           356  '356'
              378  JUMP_FORWARD        444  'to 444'
            380_0  COME_FROM_FINALLY    90  '90'

 L. 142       380  LOAD_FAST                'self'
              382  LOAD_ATTR                use_rawinput
          384_386  POP_JUMP_IF_FALSE   442  'to 442'
              388  LOAD_FAST                'self'
              390  LOAD_ATTR                completekey
          392_394  POP_JUMP_IF_FALSE   442  'to 442'

 L. 143       396  SETUP_FINALLY       422  'to 422'

 L. 144       398  LOAD_CONST               0
              400  LOAD_CONST               None
              402  IMPORT_NAME              readline
              404  STORE_FAST               'readline'

 L. 145       406  LOAD_FAST                'readline'
              408  LOAD_METHOD              set_completer
              410  LOAD_FAST                'self'
              412  LOAD_ATTR                old_completer
              414  CALL_METHOD_1         1  ''
              416  POP_TOP          
              418  POP_BLOCK        
              420  JUMP_FORWARD        442  'to 442'
            422_0  COME_FROM_FINALLY   396  '396'

 L. 146       422  DUP_TOP          
              424  LOAD_GLOBAL              ImportError
          426_428  <121>               440  ''
              430  POP_TOP          
              432  POP_TOP          
              434  POP_TOP          

 L. 147       436  POP_EXCEPT       
              438  JUMP_FORWARD        442  'to 442'
              440  <48>             
            442_0  COME_FROM           438  '438'
            442_1  COME_FROM           420  '420'
            442_2  COME_FROM           392  '392'
            442_3  COME_FROM           384  '384'
              442  <48>             
            444_0  COME_FROM           378  '378'
            444_1  COME_FROM           328  '328'
            444_2  COME_FROM           320  '320'

Parse error at or near `<121>' instruction at offset 76

    def precmd(self, line):
        """Hook method executed just before the command line is
        interpreted, but after the input prompt is generated and issued.

        """
        return line

    def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished."""
        return stop

    def preloop(self):
        """Hook method executed once when the cmdloop() method is called."""
        pass

    def postloop(self):
        """Hook method executed once when the cmdloop() method is about to
        return.

        """
        pass

    def parseline--- This code section failed: ---

 L. 177         0  LOAD_FAST                'line'
                2  LOAD_METHOD              strip
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'line'

 L. 178         8  LOAD_FAST                'line'
               10  POP_JUMP_IF_TRUE     22  'to 22'

 L. 179        12  LOAD_CONST               None
               14  LOAD_CONST               None
               16  LOAD_FAST                'line'
               18  BUILD_TUPLE_3         3 
               20  RETURN_VALUE     
             22_0  COME_FROM            10  '10'

 L. 180        22  LOAD_FAST                'line'
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  LOAD_STR                 '?'
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    52  'to 52'

 L. 181        34  LOAD_STR                 'help '
               36  LOAD_FAST                'line'
               38  LOAD_CONST               1
               40  LOAD_CONST               None
               42  BUILD_SLICE_2         2 
               44  BINARY_SUBSCR    
               46  BINARY_ADD       
               48  STORE_FAST               'line'
               50  JUMP_FORWARD        102  'to 102'
             52_0  COME_FROM            32  '32'

 L. 182        52  LOAD_FAST                'line'
               54  LOAD_CONST               0
               56  BINARY_SUBSCR    
               58  LOAD_STR                 '!'
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE   102  'to 102'

 L. 183        64  LOAD_GLOBAL              hasattr
               66  LOAD_FAST                'self'
               68  LOAD_STR                 'do_shell'
               70  CALL_FUNCTION_2       2  ''
               72  POP_JUMP_IF_FALSE    92  'to 92'

 L. 184        74  LOAD_STR                 'shell '
               76  LOAD_FAST                'line'
               78  LOAD_CONST               1
               80  LOAD_CONST               None
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    
               86  BINARY_ADD       
               88  STORE_FAST               'line'
               90  JUMP_FORWARD        102  'to 102'
             92_0  COME_FROM            72  '72'

 L. 186        92  LOAD_CONST               None
               94  LOAD_CONST               None
               96  LOAD_FAST                'line'
               98  BUILD_TUPLE_3         3 
              100  RETURN_VALUE     
            102_0  COME_FROM            90  '90'
            102_1  COME_FROM            62  '62'
            102_2  COME_FROM            50  '50'

 L. 187       102  LOAD_CONST               0
              104  LOAD_GLOBAL              len
              106  LOAD_FAST                'line'
              108  CALL_FUNCTION_1       1  ''
              110  ROT_TWO          
              112  STORE_FAST               'i'
              114  STORE_FAST               'n'

 L. 188       116  LOAD_FAST                'i'
              118  LOAD_FAST                'n'
              120  COMPARE_OP               <
              122  POP_JUMP_IF_FALSE   148  'to 148'
              124  LOAD_FAST                'line'
              126  LOAD_FAST                'i'
              128  BINARY_SUBSCR    
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                identchars
              134  <118>                 0  ''
              136  POP_JUMP_IF_FALSE   148  'to 148'
              138  LOAD_FAST                'i'
              140  LOAD_CONST               1
              142  BINARY_ADD       
              144  STORE_FAST               'i'
              146  JUMP_BACK           116  'to 116'
            148_0  COME_FROM           136  '136'
            148_1  COME_FROM           122  '122'

 L. 189       148  LOAD_FAST                'line'
              150  LOAD_CONST               None
              152  LOAD_FAST                'i'
              154  BUILD_SLICE_2         2 
              156  BINARY_SUBSCR    
              158  LOAD_FAST                'line'
              160  LOAD_FAST                'i'
              162  LOAD_CONST               None
              164  BUILD_SLICE_2         2 
              166  BINARY_SUBSCR    
              168  LOAD_METHOD              strip
              170  CALL_METHOD_0         0  ''
              172  ROT_TWO          
              174  STORE_FAST               'cmd'
              176  STORE_FAST               'arg'

 L. 190       178  LOAD_FAST                'cmd'
              180  LOAD_FAST                'arg'
              182  LOAD_FAST                'line'
              184  BUILD_TUPLE_3         3 
              186  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 134

    def onecmd--- This code section failed: ---

 L. 202         0  LOAD_FAST                'self'
                2  LOAD_METHOD              parseline
                4  LOAD_FAST                'line'
                6  CALL_METHOD_1         1  ''
                8  UNPACK_SEQUENCE_3     3 
               10  STORE_FAST               'cmd'
               12  STORE_FAST               'arg'
               14  STORE_FAST               'line'

 L. 203        16  LOAD_FAST                'line'
               18  POP_JUMP_IF_TRUE     28  'to 28'

 L. 204        20  LOAD_FAST                'self'
               22  LOAD_METHOD              emptyline
               24  CALL_METHOD_0         0  ''
               26  RETURN_VALUE     
             28_0  COME_FROM            18  '18'

 L. 205        28  LOAD_FAST                'cmd'
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    46  'to 46'

 L. 206        36  LOAD_FAST                'self'
               38  LOAD_METHOD              default
               40  LOAD_FAST                'line'
               42  CALL_METHOD_1         1  ''
               44  RETURN_VALUE     
             46_0  COME_FROM            34  '34'

 L. 207        46  LOAD_FAST                'line'
               48  LOAD_FAST                'self'
               50  STORE_ATTR               lastcmd

 L. 208        52  LOAD_FAST                'line'
               54  LOAD_STR                 'EOF'
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    66  'to 66'

 L. 209        60  LOAD_STR                 ''
               62  LOAD_FAST                'self'
               64  STORE_ATTR               lastcmd
             66_0  COME_FROM            58  '58'

 L. 210        66  LOAD_FAST                'cmd'
               68  LOAD_STR                 ''
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    84  'to 84'

 L. 211        74  LOAD_FAST                'self'
               76  LOAD_METHOD              default
               78  LOAD_FAST                'line'
               80  CALL_METHOD_1         1  ''
               82  RETURN_VALUE     
             84_0  COME_FROM            72  '72'

 L. 213        84  SETUP_FINALLY       104  'to 104'

 L. 214        86  LOAD_GLOBAL              getattr
               88  LOAD_FAST                'self'
               90  LOAD_STR                 'do_'
               92  LOAD_FAST                'cmd'
               94  BINARY_ADD       
               96  CALL_FUNCTION_2       2  ''
               98  STORE_FAST               'func'
              100  POP_BLOCK        
              102  JUMP_FORWARD        132  'to 132'
            104_0  COME_FROM_FINALLY    84  '84'

 L. 215       104  DUP_TOP          
              106  LOAD_GLOBAL              AttributeError
              108  <121>               130  ''
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 216       116  LOAD_FAST                'self'
              118  LOAD_METHOD              default
              120  LOAD_FAST                'line'
              122  CALL_METHOD_1         1  ''
              124  ROT_FOUR         
              126  POP_EXCEPT       
              128  RETURN_VALUE     
              130  <48>             
            132_0  COME_FROM           102  '102'

 L. 217       132  LOAD_FAST                'func'
              134  LOAD_FAST                'arg'
              136  CALL_FUNCTION_1       1  ''
              138  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 32

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
        if self.lastcmd:
            return self.onecmdself.lastcmd

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.

        If this method is not overridden, it prints an error message and
        returns.

        """
        self.stdout.write('*** Unknown syntax: %s\n' % line)

    def completedefault(self, *ignored):
        """Method called to complete an input line when no command-specific
        complete_*() method is available.

        By default, it returns an empty list.

        """
        return []

    def completenames(self, text, *ignored):
        dotext = 'do_' + text
        return [a[3:] for a in self.get_names if a.startswithdotext]

    def complete--- This code section failed: ---

 L. 257         0  LOAD_FAST                'state'
                2  LOAD_CONST               0
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE   180  'to 180'

 L. 258         8  LOAD_CONST               0
               10  LOAD_CONST               None
               12  IMPORT_NAME              readline
               14  STORE_FAST               'readline'

 L. 259        16  LOAD_FAST                'readline'
               18  LOAD_METHOD              get_line_buffer
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'origline'

 L. 260        24  LOAD_FAST                'origline'
               26  LOAD_METHOD              lstrip
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'line'

 L. 261        32  LOAD_GLOBAL              len
               34  LOAD_FAST                'origline'
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_GLOBAL              len
               40  LOAD_FAST                'line'
               42  CALL_FUNCTION_1       1  ''
               44  BINARY_SUBTRACT  
               46  STORE_FAST               'stripped'

 L. 262        48  LOAD_FAST                'readline'
               50  LOAD_METHOD              get_begidx
               52  CALL_METHOD_0         0  ''
               54  LOAD_FAST                'stripped'
               56  BINARY_SUBTRACT  
               58  STORE_FAST               'begidx'

 L. 263        60  LOAD_FAST                'readline'
               62  LOAD_METHOD              get_endidx
               64  CALL_METHOD_0         0  ''
               66  LOAD_FAST                'stripped'
               68  BINARY_SUBTRACT  
               70  STORE_FAST               'endidx'

 L. 264        72  LOAD_FAST                'begidx'
               74  LOAD_CONST               0
               76  COMPARE_OP               >
               78  POP_JUMP_IF_FALSE   158  'to 158'

 L. 265        80  LOAD_FAST                'self'
               82  LOAD_METHOD              parseline
               84  LOAD_FAST                'line'
               86  CALL_METHOD_1         1  ''
               88  UNPACK_SEQUENCE_3     3 
               90  STORE_FAST               'cmd'
               92  STORE_FAST               'args'
               94  STORE_FAST               'foo'

 L. 266        96  LOAD_FAST                'cmd'
               98  LOAD_STR                 ''
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   112  'to 112'

 L. 267       104  LOAD_FAST                'self'
              106  LOAD_ATTR                completedefault
              108  STORE_FAST               'compfunc'
              110  JUMP_ABSOLUTE       164  'to 164'
            112_0  COME_FROM           102  '102'

 L. 269       112  SETUP_FINALLY       132  'to 132'

 L. 270       114  LOAD_GLOBAL              getattr
              116  LOAD_FAST                'self'
              118  LOAD_STR                 'complete_'
              120  LOAD_FAST                'cmd'
              122  BINARY_ADD       
              124  CALL_FUNCTION_2       2  ''
              126  STORE_FAST               'compfunc'
              128  POP_BLOCK        
              130  JUMP_ABSOLUTE       164  'to 164'
            132_0  COME_FROM_FINALLY   112  '112'

 L. 271       132  DUP_TOP          
              134  LOAD_GLOBAL              AttributeError
              136  <121>               154  ''
              138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L. 272       144  LOAD_FAST                'self'
              146  LOAD_ATTR                completedefault
              148  STORE_FAST               'compfunc'
              150  POP_EXCEPT       
              152  JUMP_ABSOLUTE       164  'to 164'
              154  <48>             
              156  JUMP_FORWARD        164  'to 164'
            158_0  COME_FROM            78  '78'

 L. 274       158  LOAD_FAST                'self'
              160  LOAD_ATTR                completenames
              162  STORE_FAST               'compfunc'
            164_0  COME_FROM_EXCEPT_CLAUSE   156  '156'
            164_1  COME_FROM_EXCEPT_CLAUSE   152  '152'

 L. 275       164  LOAD_FAST                'compfunc'
              166  LOAD_FAST                'text'
              168  LOAD_FAST                'line'
              170  LOAD_FAST                'begidx'
              172  LOAD_FAST                'endidx'
              174  CALL_FUNCTION_4       4  ''
              176  LOAD_FAST                'self'
              178  STORE_ATTR               completion_matches
            180_0  COME_FROM             6  '6'

 L. 276       180  SETUP_FINALLY       194  'to 194'

 L. 277       182  LOAD_FAST                'self'
              184  LOAD_ATTR                completion_matches
              186  LOAD_FAST                'state'
              188  BINARY_SUBSCR    
              190  POP_BLOCK        
              192  RETURN_VALUE     
            194_0  COME_FROM_FINALLY   180  '180'

 L. 278       194  DUP_TOP          
              196  LOAD_GLOBAL              IndexError
              198  <121>               212  ''
              200  POP_TOP          
              202  POP_TOP          
              204  POP_TOP          

 L. 279       206  POP_EXCEPT       
              208  LOAD_CONST               None
              210  RETURN_VALUE     
              212  <48>             

Parse error at or near `<121>' instruction at offset 136

    def get_names(self):
        return dir(self.__class__)

    def complete_help(self, *args):
        commands = set((self.completenames)(*args))
        topics = set((a[5:] for a in self.get_names if a.startswith('help_' + args[0])))
        return list(commands | topics)

    def do_help--- This code section failed: ---

 L. 294         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_FALSE   154  'to 154'

 L. 296         4  SETUP_FINALLY        24  'to 24'

 L. 297         6  LOAD_GLOBAL              getattr
                8  LOAD_FAST                'self'
               10  LOAD_STR                 'help_'
               12  LOAD_FAST                'arg'
               14  BINARY_ADD       
               16  CALL_FUNCTION_2       2  ''
               18  STORE_FAST               'func'
               20  POP_BLOCK        
               22  JUMP_FORWARD        144  'to 144'
             24_0  COME_FROM_FINALLY     4  '4'

 L. 298        24  DUP_TOP          
               26  LOAD_GLOBAL              AttributeError
               28  <121>               142  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 299        36  SETUP_FINALLY        90  'to 90'

 L. 300        38  LOAD_GLOBAL              getattr
               40  LOAD_FAST                'self'
               42  LOAD_STR                 'do_'
               44  LOAD_FAST                'arg'
               46  BINARY_ADD       
               48  CALL_FUNCTION_2       2  ''
               50  LOAD_ATTR                __doc__
               52  STORE_FAST               'doc'

 L. 301        54  LOAD_FAST                'doc'
               56  POP_JUMP_IF_FALSE    86  'to 86'

 L. 302        58  LOAD_FAST                'self'
               60  LOAD_ATTR                stdout
               62  LOAD_METHOD              write
               64  LOAD_STR                 '%s\n'
               66  LOAD_GLOBAL              str
               68  LOAD_FAST                'doc'
               70  CALL_FUNCTION_1       1  ''
               72  BINARY_MODULO    
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L. 303        78  POP_BLOCK        
               80  POP_EXCEPT       
               82  LOAD_CONST               None
               84  RETURN_VALUE     
             86_0  COME_FROM            56  '56'
               86  POP_BLOCK        
               88  JUMP_FORWARD        108  'to 108'
             90_0  COME_FROM_FINALLY    36  '36'

 L. 304        90  DUP_TOP          
               92  LOAD_GLOBAL              AttributeError
               94  <121>               106  ''
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 305       102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
              106  <48>             
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            88  '88'

 L. 306       108  LOAD_FAST                'self'
              110  LOAD_ATTR                stdout
              112  LOAD_METHOD              write
              114  LOAD_STR                 '%s\n'
              116  LOAD_GLOBAL              str
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                nohelp
              122  LOAD_FAST                'arg'
              124  BUILD_TUPLE_1         1 
              126  BINARY_MODULO    
              128  CALL_FUNCTION_1       1  ''
              130  BINARY_MODULO    
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          

 L. 307       136  POP_EXCEPT       
              138  LOAD_CONST               None
              140  RETURN_VALUE     
              142  <48>             
            144_0  COME_FROM            22  '22'

 L. 308       144  LOAD_FAST                'func'
              146  CALL_FUNCTION_0       0  ''
              148  POP_TOP          
          150_152  JUMP_FORWARD        430  'to 430'
            154_0  COME_FROM             2  '2'

 L. 310       154  LOAD_FAST                'self'
              156  LOAD_METHOD              get_names
              158  CALL_METHOD_0         0  ''
              160  STORE_FAST               'names'

 L. 311       162  BUILD_LIST_0          0 
              164  STORE_FAST               'cmds_doc'

 L. 312       166  BUILD_LIST_0          0 
              168  STORE_FAST               'cmds_undoc'

 L. 313       170  BUILD_MAP_0           0 
              172  STORE_FAST               'help'

 L. 314       174  LOAD_FAST                'names'
              176  GET_ITER         
            178_0  COME_FROM           196  '196'
              178  FOR_ITER            216  'to 216'
              180  STORE_FAST               'name'

 L. 315       182  LOAD_FAST                'name'
              184  LOAD_CONST               None
              186  LOAD_CONST               5
              188  BUILD_SLICE_2         2 
              190  BINARY_SUBSCR    
              192  LOAD_STR                 'help_'
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_FALSE   178  'to 178'

 L. 316       198  LOAD_CONST               1
              200  LOAD_FAST                'help'
              202  LOAD_FAST                'name'
              204  LOAD_CONST               5
              206  LOAD_CONST               None
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  STORE_SUBSCR     
              214  JUMP_BACK           178  'to 178'

 L. 317       216  LOAD_FAST                'names'
              218  LOAD_METHOD              sort
              220  CALL_METHOD_0         0  ''
              222  POP_TOP          

 L. 319       224  LOAD_STR                 ''
              226  STORE_FAST               'prevname'

 L. 320       228  LOAD_FAST                'names'
              230  GET_ITER         
            232_0  COME_FROM           250  '250'
              232  FOR_ITER            346  'to 346'
              234  STORE_FAST               'name'

 L. 321       236  LOAD_FAST                'name'
              238  LOAD_CONST               None
              240  LOAD_CONST               3
              242  BUILD_SLICE_2         2 
              244  BINARY_SUBSCR    
              246  LOAD_STR                 'do_'
              248  COMPARE_OP               ==
              250  POP_JUMP_IF_FALSE   232  'to 232'

 L. 322       252  LOAD_FAST                'name'
              254  LOAD_FAST                'prevname'
              256  COMPARE_OP               ==
          258_260  POP_JUMP_IF_FALSE   264  'to 264'

 L. 323       262  JUMP_BACK           232  'to 232'
            264_0  COME_FROM           258  '258'

 L. 324       264  LOAD_FAST                'name'
              266  STORE_FAST               'prevname'

 L. 325       268  LOAD_FAST                'name'
              270  LOAD_CONST               3
              272  LOAD_CONST               None
              274  BUILD_SLICE_2         2 
              276  BINARY_SUBSCR    
              278  STORE_FAST               'cmd'

 L. 326       280  LOAD_FAST                'cmd'
              282  LOAD_FAST                'help'
              284  <118>                 0  ''
          286_288  POP_JUMP_IF_FALSE   308  'to 308'

 L. 327       290  LOAD_FAST                'cmds_doc'
              292  LOAD_METHOD              append
              294  LOAD_FAST                'cmd'
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          

 L. 328       300  LOAD_FAST                'help'
              302  LOAD_FAST                'cmd'
              304  DELETE_SUBSCR    
              306  JUMP_BACK           232  'to 232'
            308_0  COME_FROM           286  '286'

 L. 329       308  LOAD_GLOBAL              getattr
              310  LOAD_FAST                'self'
              312  LOAD_FAST                'name'
              314  CALL_FUNCTION_2       2  ''
              316  LOAD_ATTR                __doc__
          318_320  POP_JUMP_IF_FALSE   334  'to 334'

 L. 330       322  LOAD_FAST                'cmds_doc'
              324  LOAD_METHOD              append
              326  LOAD_FAST                'cmd'
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          
              332  JUMP_BACK           232  'to 232'
            334_0  COME_FROM           318  '318'

 L. 332       334  LOAD_FAST                'cmds_undoc'
              336  LOAD_METHOD              append
              338  LOAD_FAST                'cmd'
              340  CALL_METHOD_1         1  ''
              342  POP_TOP          
              344  JUMP_BACK           232  'to 232'

 L. 333       346  LOAD_FAST                'self'
              348  LOAD_ATTR                stdout
              350  LOAD_METHOD              write
              352  LOAD_STR                 '%s\n'
              354  LOAD_GLOBAL              str
              356  LOAD_FAST                'self'
              358  LOAD_ATTR                doc_leader
              360  CALL_FUNCTION_1       1  ''
              362  BINARY_MODULO    
              364  CALL_METHOD_1         1  ''
              366  POP_TOP          

 L. 334       368  LOAD_FAST                'self'
              370  LOAD_METHOD              print_topics
              372  LOAD_FAST                'self'
              374  LOAD_ATTR                doc_header
              376  LOAD_FAST                'cmds_doc'
              378  LOAD_CONST               15
              380  LOAD_CONST               80
              382  CALL_METHOD_4         4  ''
              384  POP_TOP          

 L. 335       386  LOAD_FAST                'self'
              388  LOAD_METHOD              print_topics
              390  LOAD_FAST                'self'
              392  LOAD_ATTR                misc_header
              394  LOAD_GLOBAL              list
              396  LOAD_FAST                'help'
              398  LOAD_METHOD              keys
              400  CALL_METHOD_0         0  ''
              402  CALL_FUNCTION_1       1  ''
              404  LOAD_CONST               15
              406  LOAD_CONST               80
              408  CALL_METHOD_4         4  ''
              410  POP_TOP          

 L. 336       412  LOAD_FAST                'self'
              414  LOAD_METHOD              print_topics
              416  LOAD_FAST                'self'
              418  LOAD_ATTR                undoc_header
              420  LOAD_FAST                'cmds_undoc'
              422  LOAD_CONST               15
              424  LOAD_CONST               80
              426  CALL_METHOD_4         4  ''
              428  POP_TOP          
            430_0  COME_FROM           150  '150'

Parse error at or near `<121>' instruction at offset 28

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            self.stdout.write('%s\n' % str(header))
            if self.ruler:
                self.stdout.write('%s\n' % str(self.ruler * len(header)))
            self.columnizecmds(maxcol - 1)
            self.stdout.write'\n'

    def columnize(self, list, displaywidth=80):
        """Display a list of strings as a compact set of columns.

        Each column is only as wide as necessary.
        Columns are separated by two spaces (one was not legible enough).
        """
        if not list:
            self.stdout.write'<empty>\n'
            return None
        nonstrings = [i for i in range(len(list)) if not isinstance(list[i], str)]
        if nonstrings:
            raise TypeError('list[i] not a string for i in %s' % ', '.joinmap(str, nonstrings))
        size = len(list)
        if size == 1:
            self.stdout.write'%s\n' % str(list[0])
            return None
        for nrows in range(1, len(list)):
            ncols = (size + nrows - 1) // nrows
            colwidths = []
            totwidth = -2
            for col in range(ncols):
                colwidth = 0

        for row in range(nrows):
            i = row + nrows * col
            if i >= size:
                break
            x = list[i]
            colwidth = max(colwidth, len(x))
        else:
            colwidths.appendcolwidth
            totwidth += colwidth + 2
            if totwidth > displaywidth:
                break
            if totwidth <= displaywidth:
                break
            nrows = len(list)
            ncols = 1
            colwidths = [0]
            for row in range(nrows):
                texts = []
                for col in range(ncols):
                    i = row + nrows * col
                    if i >= size:
                        x = ''
                    else:
                        x = list[i]
                    texts.appendx

                if texts:
                    del (texts[(-1)] or texts)[-1]
                else:
                    for col in range(len(texts)):
                        texts[col] = texts[col].ljustcolwidths[col]
                    else:
                        self.stdout.write('%s\n' % str('  '.jointexts))