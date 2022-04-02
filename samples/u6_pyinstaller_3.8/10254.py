# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
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

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        """Instantiate a line-oriented interpreter framework.

        The optional argument 'completekey' is the readline name of a
        completion key; it defaults to the Tab key. If completekey is
        not None and the readline module is available, command completion
        is done automatically. The optional arguments stdin and stdout
        specify alternate input and output file objects; if not specified,
        sys.stdin and sys.stdout are used.

        """
        if stdin is not None:
            self.stdin = stdin
        else:
            self.stdin = sys.stdin
        if stdout is not None:
            self.stdout = stdout
        else:
            self.stdout = sys.stdout
        self.cmdqueue = []
        self.completekey = completekey

    def cmdloop(self, intro=None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        """
        self.preloop()
        if self.use_rawinput:
            if self.completekey:
                try:
                    import readline
                    self.old_completer = readline.get_completer()
                    readline.set_completer(self.complete)
                    readline.parse_and_bind(self.completekey + ': complete')
                except ImportError:
                    pass

        try:
            if intro is not None:
                self.intro = intro
            else:
                if self.intro:
                    self.stdout.write(str(self.intro) + '\n')
                stop = None
                while not stop:
                    if self.cmdqueue:
                        line = self.cmdqueue.pop(0)
                    else:
                        if self.use_rawinput:
                            try:
                                line = input(self.prompt)
                            except EOFError:
                                line = 'EOF'

                        else:
                            self.stdout.write(self.prompt)
                            self.stdout.flush()
                            line = self.stdin.readline()
                            if not len(line):
                                line = 'EOF'
                            else:
                                line = line.rstrip('\r\n')
                    line = self.precmd(line)
                    stop = self.onecmd(line)
                    stop = self.postcmd(stop, line)

            self.postloop()
        finally:
            if self.use_rawinput:
                if self.completekey:
                    try:
                        import readline
                        readline.set_completer(self.old_completer)
                    except ImportError:
                        pass

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

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments.  Returns a tuple containing (command, args, line).
        'command' and 'args' may be None if the line couldn't be parsed.
        """
        line = line.strip()
        if not line:
            return (
             None, None, line)
        if line[0] == '?':
            line = 'help ' + line[1:]
        else:
            if line[0] == '!':
                if hasattr(self, 'do_shell'):
                    line = 'shell ' + line[1:]
                else:
                    return (
                     None, None, line)
            else:
                i, n = 0, len(line)
                while i < n:
                    if line[i] in self.identchars:
                        i = i + 1

            cmd, arg = line[:i], line[i:].strip()
            return (cmd, arg, line)

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        """
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if cmd == '':
            return self.default(line)
        try:
            func = getattr(self, 'do_' + cmd)
        except AttributeError:
            return self.default(line)
        else:
            return func(arg)

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
        if self.lastcmd:
            return self.onecmd(self.lastcmd)

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
        return [a[3:] for a in self.get_names() if a.startswith(dotext)]

    def complete--- This code section failed: ---

 L. 257         0  LOAD_FAST                'state'
                2  LOAD_CONST               0
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE   182  'to 182'

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
               78  POP_JUMP_IF_FALSE   160  'to 160'

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
              110  JUMP_ABSOLUTE       166  'to 166'
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
              130  JUMP_ABSOLUTE       166  'to 166'
            132_0  COME_FROM_FINALLY   112  '112'

 L. 271       132  DUP_TOP          
              134  LOAD_GLOBAL              AttributeError
              136  COMPARE_OP               exception-match
              138  POP_JUMP_IF_FALSE   156  'to 156'
              140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L. 272       146  LOAD_FAST                'self'
              148  LOAD_ATTR                completedefault
              150  STORE_FAST               'compfunc'
              152  POP_EXCEPT       
              154  JUMP_ABSOLUTE       166  'to 166'
            156_0  COME_FROM           138  '138'
              156  END_FINALLY      
              158  JUMP_FORWARD        166  'to 166'
            160_0  COME_FROM            78  '78'

 L. 274       160  LOAD_FAST                'self'
              162  LOAD_ATTR                completenames
              164  STORE_FAST               'compfunc'
            166_0  COME_FROM           158  '158'

 L. 275       166  LOAD_FAST                'compfunc'
              168  LOAD_FAST                'text'
              170  LOAD_FAST                'line'
              172  LOAD_FAST                'begidx'
              174  LOAD_FAST                'endidx'
              176  CALL_FUNCTION_4       4  ''
              178  LOAD_FAST                'self'
              180  STORE_ATTR               completion_matches
            182_0  COME_FROM             6  '6'

 L. 276       182  SETUP_FINALLY       196  'to 196'

 L. 277       184  LOAD_FAST                'self'
              186  LOAD_ATTR                completion_matches
              188  LOAD_FAST                'state'
              190  BINARY_SUBSCR    
              192  POP_BLOCK        
              194  RETURN_VALUE     
            196_0  COME_FROM_FINALLY   182  '182'

 L. 278       196  DUP_TOP          
              198  LOAD_GLOBAL              IndexError
              200  COMPARE_OP               exception-match
              202  POP_JUMP_IF_FALSE   216  'to 216'
              204  POP_TOP          
              206  POP_TOP          
              208  POP_TOP          

 L. 279       210  POP_EXCEPT       
              212  LOAD_CONST               None
              214  RETURN_VALUE     
            216_0  COME_FROM           202  '202'
              216  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 206

    def get_names(self):
        return dir(self.__class__)

    def complete_help(self, *args):
        commands = set((self.completenames)(*args))
        topics = set((a[5:] for a in self.get_names() if a.startswith('help_' + args[0])))
        return list(commands | topics)

    def do_help--- This code section failed: ---

 L. 294         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_FALSE   158  'to 158'

 L. 296         4  SETUP_FINALLY        24  'to 24'

 L. 297         6  LOAD_GLOBAL              getattr
                8  LOAD_FAST                'self'
               10  LOAD_STR                 'help_'
               12  LOAD_FAST                'arg'
               14  BINARY_ADD       
               16  CALL_FUNCTION_2       2  ''
               18  STORE_FAST               'func'
               20  POP_BLOCK        
               22  JUMP_FORWARD        148  'to 148'
             24_0  COME_FROM_FINALLY     4  '4'

 L. 298        24  DUP_TOP          
               26  LOAD_GLOBAL              AttributeError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE   146  'to 146'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 299        38  SETUP_FINALLY        92  'to 92'

 L. 300        40  LOAD_GLOBAL              getattr
               42  LOAD_FAST                'self'
               44  LOAD_STR                 'do_'
               46  LOAD_FAST                'arg'
               48  BINARY_ADD       
               50  CALL_FUNCTION_2       2  ''
               52  LOAD_ATTR                __doc__
               54  STORE_FAST               'doc'

 L. 301        56  LOAD_FAST                'doc'
               58  POP_JUMP_IF_FALSE    88  'to 88'

 L. 302        60  LOAD_FAST                'self'
               62  LOAD_ATTR                stdout
               64  LOAD_METHOD              write
               66  LOAD_STR                 '%s\n'
               68  LOAD_GLOBAL              str
               70  LOAD_FAST                'doc'
               72  CALL_FUNCTION_1       1  ''
               74  BINARY_MODULO    
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 303        80  POP_BLOCK        
               82  POP_EXCEPT       
               84  LOAD_CONST               None
               86  RETURN_VALUE     
             88_0  COME_FROM            58  '58'
               88  POP_BLOCK        
               90  JUMP_FORWARD        112  'to 112'
             92_0  COME_FROM_FINALLY    38  '38'

 L. 304        92  DUP_TOP          
               94  LOAD_GLOBAL              AttributeError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   110  'to 110'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 305       106  POP_EXCEPT       
              108  JUMP_FORWARD        112  'to 112'
            110_0  COME_FROM            98  '98'
              110  END_FINALLY      
            112_0  COME_FROM           108  '108'
            112_1  COME_FROM            90  '90'

 L. 306       112  LOAD_FAST                'self'
              114  LOAD_ATTR                stdout
              116  LOAD_METHOD              write
              118  LOAD_STR                 '%s\n'
              120  LOAD_GLOBAL              str
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                nohelp
              126  LOAD_FAST                'arg'
              128  BUILD_TUPLE_1         1 
              130  BINARY_MODULO    
              132  CALL_FUNCTION_1       1  ''
              134  BINARY_MODULO    
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          

 L. 307       140  POP_EXCEPT       
              142  LOAD_CONST               None
              144  RETURN_VALUE     
            146_0  COME_FROM            30  '30'
              146  END_FINALLY      
            148_0  COME_FROM            22  '22'

 L. 308       148  LOAD_FAST                'func'
              150  CALL_FUNCTION_0       0  ''
              152  POP_TOP          
          154_156  JUMP_FORWARD        434  'to 434'
            158_0  COME_FROM             2  '2'

 L. 310       158  LOAD_FAST                'self'
              160  LOAD_METHOD              get_names
              162  CALL_METHOD_0         0  ''
              164  STORE_FAST               'names'

 L. 311       166  BUILD_LIST_0          0 
              168  STORE_FAST               'cmds_doc'

 L. 312       170  BUILD_LIST_0          0 
              172  STORE_FAST               'cmds_undoc'

 L. 313       174  BUILD_MAP_0           0 
              176  STORE_FAST               'help'

 L. 314       178  LOAD_FAST                'names'
              180  GET_ITER         
            182_0  COME_FROM           200  '200'
              182  FOR_ITER            220  'to 220'
              184  STORE_FAST               'name'

 L. 315       186  LOAD_FAST                'name'
              188  LOAD_CONST               None
              190  LOAD_CONST               5
              192  BUILD_SLICE_2         2 
              194  BINARY_SUBSCR    
              196  LOAD_STR                 'help_'
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   182  'to 182'

 L. 316       202  LOAD_CONST               1
              204  LOAD_FAST                'help'
              206  LOAD_FAST                'name'
              208  LOAD_CONST               5
              210  LOAD_CONST               None
              212  BUILD_SLICE_2         2 
              214  BINARY_SUBSCR    
              216  STORE_SUBSCR     
              218  JUMP_BACK           182  'to 182'

 L. 317       220  LOAD_FAST                'names'
              222  LOAD_METHOD              sort
              224  CALL_METHOD_0         0  ''
              226  POP_TOP          

 L. 319       228  LOAD_STR                 ''
              230  STORE_FAST               'prevname'

 L. 320       232  LOAD_FAST                'names'
              234  GET_ITER         
            236_0  COME_FROM           254  '254'
              236  FOR_ITER            350  'to 350'
              238  STORE_FAST               'name'

 L. 321       240  LOAD_FAST                'name'
              242  LOAD_CONST               None
              244  LOAD_CONST               3
              246  BUILD_SLICE_2         2 
              248  BINARY_SUBSCR    
              250  LOAD_STR                 'do_'
              252  COMPARE_OP               ==
              254  POP_JUMP_IF_FALSE   236  'to 236'

 L. 322       256  LOAD_FAST                'name'
              258  LOAD_FAST                'prevname'
              260  COMPARE_OP               ==
          262_264  POP_JUMP_IF_FALSE   268  'to 268'

 L. 323       266  JUMP_BACK           236  'to 236'
            268_0  COME_FROM           262  '262'

 L. 324       268  LOAD_FAST                'name'
              270  STORE_FAST               'prevname'

 L. 325       272  LOAD_FAST                'name'
              274  LOAD_CONST               3
              276  LOAD_CONST               None
              278  BUILD_SLICE_2         2 
              280  BINARY_SUBSCR    
              282  STORE_FAST               'cmd'

 L. 326       284  LOAD_FAST                'cmd'
              286  LOAD_FAST                'help'
              288  COMPARE_OP               in
          290_292  POP_JUMP_IF_FALSE   312  'to 312'

 L. 327       294  LOAD_FAST                'cmds_doc'
              296  LOAD_METHOD              append
              298  LOAD_FAST                'cmd'
              300  CALL_METHOD_1         1  ''
              302  POP_TOP          

 L. 328       304  LOAD_FAST                'help'
              306  LOAD_FAST                'cmd'
              308  DELETE_SUBSCR    
              310  JUMP_BACK           236  'to 236'
            312_0  COME_FROM           290  '290'

 L. 329       312  LOAD_GLOBAL              getattr
              314  LOAD_FAST                'self'
              316  LOAD_FAST                'name'
              318  CALL_FUNCTION_2       2  ''
              320  LOAD_ATTR                __doc__
          322_324  POP_JUMP_IF_FALSE   338  'to 338'

 L. 330       326  LOAD_FAST                'cmds_doc'
              328  LOAD_METHOD              append
              330  LOAD_FAST                'cmd'
              332  CALL_METHOD_1         1  ''
              334  POP_TOP          
              336  JUMP_BACK           236  'to 236'
            338_0  COME_FROM           322  '322'

 L. 332       338  LOAD_FAST                'cmds_undoc'
              340  LOAD_METHOD              append
              342  LOAD_FAST                'cmd'
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          
              348  JUMP_BACK           236  'to 236'

 L. 333       350  LOAD_FAST                'self'
              352  LOAD_ATTR                stdout
              354  LOAD_METHOD              write
              356  LOAD_STR                 '%s\n'
              358  LOAD_GLOBAL              str
              360  LOAD_FAST                'self'
              362  LOAD_ATTR                doc_leader
              364  CALL_FUNCTION_1       1  ''
              366  BINARY_MODULO    
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          

 L. 334       372  LOAD_FAST                'self'
              374  LOAD_METHOD              print_topics
              376  LOAD_FAST                'self'
              378  LOAD_ATTR                doc_header
              380  LOAD_FAST                'cmds_doc'
              382  LOAD_CONST               15
              384  LOAD_CONST               80
              386  CALL_METHOD_4         4  ''
              388  POP_TOP          

 L. 335       390  LOAD_FAST                'self'
              392  LOAD_METHOD              print_topics
              394  LOAD_FAST                'self'
              396  LOAD_ATTR                misc_header
              398  LOAD_GLOBAL              list
              400  LOAD_FAST                'help'
              402  LOAD_METHOD              keys
              404  CALL_METHOD_0         0  ''
              406  CALL_FUNCTION_1       1  ''
              408  LOAD_CONST               15
              410  LOAD_CONST               80
              412  CALL_METHOD_4         4  ''
              414  POP_TOP          

 L. 336       416  LOAD_FAST                'self'
              418  LOAD_METHOD              print_topics
              420  LOAD_FAST                'self'
              422  LOAD_ATTR                undoc_header
              424  LOAD_FAST                'cmds_undoc'
              426  LOAD_CONST               15
              428  LOAD_CONST               80
              430  CALL_METHOD_4         4  ''
              432  POP_TOP          
            434_0  COME_FROM           154  '154'

Parse error at or near `POP_EXCEPT' instruction at offset 82

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            self.stdout.write('%s\n' % str(header))
            if self.ruler:
                self.stdout.write('%s\n' % str(self.ruler * len(header)))
            self.columnize(cmds, maxcol - 1)
            self.stdout.write('\n')

    def columnize(self, list, displaywidth=80):
        """Display a list of strings as a compact set of columns.

        Each column is only as wide as necessary.
        Columns are separated by two spaces (one was not legible enough).
        """
        if not list:
            self.stdout.write('<empty>\n')
            return None
        nonstrings = [i for i in range(len(list)) if not isinstance(list[i], str)]
        if nonstrings:
            raise TypeError('list[i] not a string for i in %s' % ', '.join(map(str, nonstrings)))
        size = len(list)
        if size == 1:
            self.stdout.write('%s\n' % str(list[0]))
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
            colwidths.append(colwidth)
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
                    texts.append(x)

                if texts:
                    del (texts[(-1)] or texts)[-1]
                else:
                    for col in range(len(texts)):
                        texts[col] = texts[col].ljust(colwidths[col])
                    else:
                        self.stdout.write('%s\n' % str('  '.join(texts)))