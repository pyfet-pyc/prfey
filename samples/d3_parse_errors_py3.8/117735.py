# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: pdb.py
"""
The Python Debugger Pdb
=======================

To use the debugger in its simplest form:

        >>> import pdb
        >>> pdb.run('<a statement>')

The debugger's prompt is '(Pdb) '.  This will stop in the first
function call in <a statement>.

Alternatively, if a statement terminated with an unhandled exception,
you can use pdb's post-mortem facility to inspect the contents of the
traceback:

        >>> <a statement>
        <exception traceback>
        >>> import pdb
        >>> pdb.pm()

The commands recognized by the debugger are listed in the next
section.  Most can be abbreviated as indicated; e.g., h(elp) means
that 'help' can be typed as 'h' or 'help' (but not as 'he' or 'hel',
nor as 'H' or 'Help' or 'HELP').  Optional arguments are enclosed in
square brackets.  Alternatives in the command syntax are separated
by a vertical bar (|).

A blank line repeats the previous command literally, except for
'list', where it lists the next 11 lines.

Commands that the debugger doesn't recognize are assumed to be Python
statements and are executed in the context of the program being
debugged.  Python statements can also be prefixed with an exclamation
point ('!').  This is a powerful way to inspect the program being
debugged; it is even possible to change variables or call functions.
When an exception occurs in such a statement, the exception name is
printed but the debugger's state is not changed.

The debugger supports aliases, which can save typing.  And aliases can
have parameters (see the alias help entry) which allows one a certain
level of adaptability to the context under examination.

Multiple commands may be entered on a single line, separated by the
pair ';;'.  No intelligence is applied to separating the commands; the
input is split at the first ';;', even if it is in the middle of a
quoted string.

If a file ".pdbrc" exists in your home directory or in the current
directory, it is read in and executed as if it had been typed at the
debugger prompt.  This is particularly useful for aliases.  If both
files exist, the one in the home directory is read first and aliases
defined there can be overridden by the local file.  This behavior can be
disabled by passing the "readrc=False" argument to the Pdb constructor.

Aside from aliases, the debugger is not directly programmable; but it
is implemented as a class from which you can derive your own debugger
class, which you can make as fancy as you like.

Debugger commands
=================

"""
import os, io, re, sys, cmd, bdb, dis, code, glob, pprint, signal, inspect, traceback, linecache

class Restart(Exception):
    __doc__ = 'Causes a debugger to be restarted for the debugged python program.'


__all__ = [
 'run', 'pm', 'Pdb', 'runeval', 'runctx', 'runcall', 'set_trace',
 'post_mortem', 'help']

def find_function--- This code section failed: ---

 L.  94         0  LOAD_GLOBAL              re
                2  LOAD_METHOD              compile
                4  LOAD_STR                 'def\\s+%s\\s*[(]'
                6  LOAD_GLOBAL              re
                8  LOAD_METHOD              escape
               10  LOAD_FAST                'funcname'
               12  CALL_METHOD_1         1  ''
               14  BINARY_MODULO    
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'cre'

 L.  95        20  SETUP_FINALLY        34  'to 34'

 L.  96        22  LOAD_GLOBAL              open
               24  LOAD_FAST                'filename'
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'fp'
               30  POP_BLOCK        
               32  JUMP_FORWARD         56  'to 56'
             34_0  COME_FROM_FINALLY    20  '20'

 L.  97        34  DUP_TOP          
               36  LOAD_GLOBAL              OSError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    54  'to 54'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.  98        48  POP_EXCEPT       
               50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            40  '40'
               54  END_FINALLY      
             56_0  COME_FROM            32  '32'

 L. 100        56  LOAD_FAST                'fp'
               58  SETUP_WITH          124  'to 124'
               60  POP_TOP          

 L. 101        62  LOAD_GLOBAL              enumerate
               64  LOAD_FAST                'fp'
               66  LOAD_CONST               1
               68  LOAD_CONST               ('start',)
               70  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               72  GET_ITER         
             74_0  COME_FROM           118  '118'
             74_1  COME_FROM            90  '90'
               74  FOR_ITER            120  'to 120'
               76  UNPACK_SEQUENCE_2     2 
               78  STORE_FAST               'lineno'
               80  STORE_FAST               'line'

 L. 102        82  LOAD_FAST                'cre'
               84  LOAD_METHOD              match
               86  LOAD_FAST                'line'
               88  CALL_METHOD_1         1  ''
               90  POP_JUMP_IF_FALSE_BACK    74  'to 74'

 L. 103        92  LOAD_FAST                'funcname'
               94  LOAD_FAST                'filename'
               96  LOAD_FAST                'lineno'
               98  BUILD_TUPLE_3         3 
              100  ROT_TWO          
              102  POP_TOP          
              104  POP_BLOCK        
              106  ROT_TWO          
              108  BEGIN_FINALLY    
              110  WITH_CLEANUP_START
              112  WITH_CLEANUP_FINISH
              114  POP_FINALLY           0  ''
              116  RETURN_VALUE     
              118  JUMP_BACK            74  'to 74'
            120_0  COME_FROM            74  '74'
              120  POP_BLOCK        
              122  BEGIN_FINALLY    
            124_0  COME_FROM_WITH       58  '58'
              124  WITH_CLEANUP_START
              126  WITH_CLEANUP_FINISH
              128  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 104


def getsourcelines(obj):
    lines, lineno = inspect.findsourceobj
    if inspect.isframeobj:
        if obj.f_globals is obj.f_locals:
            return (
             lines, 1)
    if inspect.ismoduleobj:
        return (lines, 1)
    return (inspect.getblocklines[lineno:], lineno + 1)


def lasti2lineno(code, lasti):
    linestarts = list(dis.findlinestartscode)
    linestarts.reverse()
    for i, lineno in linestarts:
        if lasti >= i:
            return lineno
    else:
        return 0


class _rstr(str):
    __doc__ = "String that doesn't quote its repr."

    def __repr__(self):
        return self


line_prefix = '\n-> '

class Pdb(bdb.Bdb, cmd.Cmd):
    _previous_sigint_handler = None

    def __init__(self, completekey='tab', stdin=None, stdout=None, skip=None, nosigint=False, readrc=True):
        bdb.Bdb.__init__(self, skip=skip)
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        sys.audit'pdb.Pdb'
        if stdout:
            self.use_rawinput = 0
        self.prompt = '(Pdb) '
        self.aliases = {}
        self.displaying = {}
        self.mainpyfile = ''
        self._wait_for_mainpyfile = False
        self.tb_lineno = {}
        try:
            import readline
            readline.set_completer_delims' \t\n`@#$%^&*()=+[{]}\\|;:\'",<>?'
        except ImportError:
            pass
        else:
            self.allow_kbdint = False
            self.nosigint = nosigint
            self.rcLines = []
            if readrc:
                try:
                    with open(os.path.expanduser'~/.pdbrc') as rcFile:
                        self.rcLines.extendrcFile
                except OSError:
                    pass

                try:
                    with open('.pdbrc') as rcFile:
                        self.rcLines.extendrcFile
                except OSError:
                    pass

            self.commands = {}
            self.commands_doprompt = {}
            self.commands_silent = {}
            self.commands_defining = False
            self.commands_bnum = None

    def sigint_handler(self, signum, frame):
        if self.allow_kbdint:
            raise KeyboardInterrupt
        self.message"\nProgram interrupted. (Use 'cont' to resume)."
        self.set_step()
        self.set_traceframe

    def reset(self):
        bdb.Bdb.resetself
        self.forget()

    def forget(self):
        self.lineno = None
        self.stack = []
        self.curindex = 0
        self.curframe = None
        self.tb_lineno.clear()

    def setup(self, f, tb):
        self.forget()
        self.stack, self.curindex = self.get_stack(f, tb)
        while True:
            if tb:
                lineno = lasti2lineno(tb.tb_frame.f_code, tb.tb_lasti)
                self.tb_lineno[tb.tb_frame] = lineno
                tb = tb.tb_next

        self.curframe = self.stack[self.curindex][0]
        self.curframe_locals = self.curframe.f_locals
        return self.execRcLines()

    def execRcLines(self):
        if not self.rcLines:
            return
        rcLines = self.rcLines
        rcLines.reverse()
        self.rcLines = []
        while True:
            if rcLines:
                line = rcLines.pop().strip()
                if line:
                    if line[0] != '#':
                        if self.onecmdline:
                            self.rcLines += reversed(rcLines)
                            return True

    def user_call(self, frame, argument_list):
        """This method is called when there is the remote possibility
        that we ever need to stop in this function."""
        if self._wait_for_mainpyfile:
            return
        if self.stop_hereframe:
            self.message'--Call--'
            self.interaction(frame, None)

    def user_line(self, frame):
        """This function is called when we stop or break at this line."""
        if self._wait_for_mainpyfile:
            if self.mainpyfile != self.canonicframe.f_code.co_filename or (frame.f_lineno <= 0):
                return
            self._wait_for_mainpyfile = False
        if self.bp_commandsframe:
            self.interaction(frame, None)

    def bp_commands(self, frame):
        """Call every command that was set for the current active breakpoint
        (if there is one).

        Returns True if the normal interaction function must be called,
        False otherwise."""
        if getattr(self, 'currentbp', False):
            if self.currentbp in self.commands:
                currentbp = self.currentbp
                self.currentbp = 0
                lastcmd_back = self.lastcmd
                self.setup(frame, None)
                for line in self.commands[currentbp]:
                    self.onecmdline
                else:
                    self.lastcmd = lastcmd_back
                    if not self.commands_silent[currentbp]:
                        self.print_stack_entryself.stack[self.curindex]
                    if self.commands_doprompt[currentbp]:
                        self._cmdloop()
                    self.forget()
                    return

        return 1

    def user_return(self, frame, return_value):
        """This function is called when a return trap is set here."""
        if self._wait_for_mainpyfile:
            return
        frame.f_locals['__return__'] = return_value
        self.message'--Return--'
        self.interaction(frame, None)

    def user_exception(self, frame, exc_info):
        """This function is called if an exception occurs,
        but only if we are to stop at or just below this level."""
        if self._wait_for_mainpyfile:
            return
        exc_type, exc_value, exc_traceback = exc_info
        frame.f_locals['__exception__'] = (exc_type, exc_value)
        prefix = 'Internal ' if (exc_traceback or exc_type) is StopIteration else ''
        self.message('%s%s' % (prefix,
         traceback.format_exception_only(exc_type, exc_value)[(-1)].strip()))
        self.interaction(frame, exc_traceback)

    def _cmdloop(self):
        while True:
            try:
                self.allow_kbdint = True
                self.cmdloop()
                self.allow_kbdint = False
                break
            except KeyboardInterrupt:
                self.message'--KeyboardInterrupt--'

    def preloop(self):
        displaying = self.displaying.getself.curframe
        if displaying:
            for expr, oldvalue in displaying.items():
                newvalue = self._getval_exceptexpr
                if newvalue is not oldvalue:
                    if newvalue != oldvalue:
                        displaying[expr] = newvalue
                        self.message('display %s: %r  [old: %r]' % (
                         expr, newvalue, oldvalue))

    def interaction(self, frame, traceback):
        if Pdb._previous_sigint_handler:
            try:
                signal.signal(signal.SIGINT, Pdb._previous_sigint_handler)
            except ValueError:
                pass
            else:
                Pdb._previous_sigint_handler = None
            if self.setup(frame, traceback):
                self.forget()
                return
        self.print_stack_entryself.stack[self.curindex]
        self._cmdloop()
        self.forget()

    def displayhook(self, obj):
        """Custom displayhook for the exec in default(), which prevents
        assignment of the _ variable in the builtins.
        """
        if obj is not None:
            self.messagerepr(obj)

    def default(self, line):
        if line[:1] == '!':
            line = line[1:]
        locals = self.curframe_locals
        globals = self.curframe.f_globals
        try:
            code = compile(line + '\n', '<stdin>', 'single')
            save_stdout = sys.stdout
            save_stdin = sys.stdin
            save_displayhook = sys.displayhook
            try:
                sys.stdin = self.stdin
                sys.stdout = self.stdout
                sys.displayhook = self.displayhook
                exec(code, globals, locals)
            finally:
                sys.stdout = save_stdout
                sys.stdin = save_stdin
                sys.displayhook = save_displayhook

        except:
            exc_info = sys.exc_info()[:2]
            self.error(traceback.format_exception_only)(*exc_info)[(-1)].strip()

    def precmd(self, line):
        """Handle alias expansion and ';;' separator."""
        if not line.strip():
            return line
        args = line.split()
        while True:
            if args[0] in self.aliases:
                line = self.aliases[args[0]]
                ii = 1
                for tmpArg in args[1:]:
                    line = line.replace('%' + str(ii), tmpArg)
                    ii += 1
                else:
                    line = line.replace('%*', ' '.joinargs[1:])
                    args = line.split()

        if args[0] != 'alias':
            marker = line.find';;'
            if marker >= 0:
                next = line[marker + 2:].lstrip()
                self.cmdqueue.appendnext
                line = line[:marker].rstrip()
        return line

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        Checks whether this line is typed at the normal prompt or in
        a breakpoint command list definition.
        """
        if not self.commands_defining:
            return cmd.Cmd.onecmd(self, line)
        return self.handle_command_defline

    def handle_command_def(self, line):
        """Handles one command line during command list definition."""
        cmd, arg, line = self.parselineline
        if not cmd:
            return
        if cmd == 'silent':
            self.commands_silent[self.commands_bnum] = True
            return
        if cmd == 'end':
            self.cmdqueue = []
            return 1
        cmdlist = self.commands[self.commands_bnum]
        if arg:
            cmdlist.append(cmd + ' ' + arg)
        else:
            cmdlist.appendcmd
        try:
            func = getattr(self, 'do_' + cmd)
        except AttributeError:
            func = self.default
        else:
            if func.__name__ in self.commands_resuming:
                self.commands_doprompt[self.commands_bnum] = False
                self.cmdqueue = []
                return 1

    def message(self, msg):
        print(msg, file=(self.stdout))

    def error(self, msg):
        print('***', msg, file=(self.stdout))

    def _complete_location(self, text, line, begidx, endidx):
        if line.strip().endswith(':', ','):
            return []
        try:
            ret = self._complete_expression(text, line, begidx, endidx)
        except Exception:
            ret = []
        else:
            globs = glob.glob(text + '*')
            for fn in globs:
                if os.path.isdirfn:
                    ret.append(fn + '/')
                else:
                    if os.path.isfilefn:
                        if fn.lower().endswith('.py', '.pyw'):
                            ret.append(fn + ':')
            else:
                return ret

    def _complete_bpnumber(self, text, line, begidx, endidx):
        return [str(i) for i, bp in enumerate(bdb.Breakpoint.bpbynumber) if bp is not None if str(i).startswithtext]

    def _complete_expression(self, text, line, begidx, endidx):
        if not self.curframe:
            return []
        ns = {**(self.curframe.f_globals), **(self.curframe_locals)}
        if '.' in text:
            dotted = text.split'.'
            try:
                obj = ns[dotted[0]]
                for part in dotted[1:-1]:
                    obj = getattr(obj, part)

            except (KeyError, AttributeError):
                return []
            else:
                prefix = '.'.joindotted[:-1] + '.'
                return [prefix + n for n in dir(obj) if n.startswithdotted[(-1)]]
            return [n for n in ns.keys() if n.startswithtext]

    def do_commands--- This code section failed: ---

 L. 557         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_TRUE     22  'to 22'

 L. 558         4  LOAD_GLOBAL              len
                6  LOAD_GLOBAL              bdb
                8  LOAD_ATTR                Breakpoint
               10  LOAD_ATTR                bpbynumber
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_CONST               1
               16  BINARY_SUBTRACT  
               18  STORE_FAST               'bnum'
               20  JUMP_FORWARD         60  'to 60'
             22_0  COME_FROM             2  '2'

 L. 560        22  SETUP_FINALLY        36  'to 36'

 L. 561        24  LOAD_GLOBAL              int
               26  LOAD_FAST                'arg'
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'bnum'
               32  POP_BLOCK        
               34  JUMP_FORWARD         60  'to 60'
             36_0  COME_FROM_FINALLY    22  '22'

 L. 562        36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 563        42  LOAD_FAST                'self'
               44  LOAD_METHOD              error
               46  LOAD_STR                 'Usage: commands [bnum]\n        ...\n        end'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L. 564        52  POP_EXCEPT       
               54  LOAD_CONST               None
               56  RETURN_VALUE     
               58  END_FINALLY      
             60_0  COME_FROM            34  '34'
             60_1  COME_FROM            20  '20'

 L. 565        60  LOAD_FAST                'bnum'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               commands_bnum

 L. 567        66  LOAD_FAST                'bnum'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                commands
               72  COMPARE_OP               in
               74  POP_JUMP_IF_FALSE   106  'to 106'

 L. 568        76  LOAD_FAST                'self'
               78  LOAD_ATTR                commands
               80  LOAD_FAST                'bnum'
               82  BINARY_SUBSCR    

 L. 569        84  LOAD_FAST                'self'
               86  LOAD_ATTR                commands_doprompt
               88  LOAD_FAST                'bnum'
               90  BINARY_SUBSCR    

 L. 570        92  LOAD_FAST                'self'
               94  LOAD_ATTR                commands_silent
               96  LOAD_FAST                'bnum'
               98  BINARY_SUBSCR    

 L. 568       100  BUILD_TUPLE_3         3 
              102  STORE_FAST               'old_command_defs'
              104  JUMP_FORWARD        110  'to 110'
            106_0  COME_FROM            74  '74'

 L. 572       106  LOAD_CONST               None
              108  STORE_FAST               'old_command_defs'
            110_0  COME_FROM           104  '104'

 L. 573       110  BUILD_LIST_0          0 
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                commands
              116  LOAD_FAST                'bnum'
              118  STORE_SUBSCR     

 L. 574       120  LOAD_CONST               True
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                commands_doprompt
              126  LOAD_FAST                'bnum'
              128  STORE_SUBSCR     

 L. 575       130  LOAD_CONST               False
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                commands_silent
              136  LOAD_FAST                'bnum'
              138  STORE_SUBSCR     

 L. 577       140  LOAD_FAST                'self'
              142  LOAD_ATTR                prompt
              144  STORE_FAST               'prompt_back'

 L. 578       146  LOAD_STR                 '(com) '
              148  LOAD_FAST                'self'
              150  STORE_ATTR               prompt

 L. 579       152  LOAD_CONST               True
              154  LOAD_FAST                'self'
              156  STORE_ATTR               commands_defining

 L. 580       158  SETUP_FINALLY       282  'to 282'
              160  SETUP_FINALLY       174  'to 174'

 L. 581       162  LOAD_FAST                'self'
              164  LOAD_METHOD              cmdloop
              166  CALL_METHOD_0         0  ''
              168  POP_TOP          
              170  POP_BLOCK        
              172  JUMP_FORWARD        278  'to 278'
            174_0  COME_FROM_FINALLY   160  '160'

 L. 582       174  DUP_TOP          
              176  LOAD_GLOBAL              KeyboardInterrupt
              178  COMPARE_OP               exception-match
          180_182  POP_JUMP_IF_FALSE   276  'to 276'
              184  POP_TOP          
              186  POP_TOP          
              188  POP_TOP          

 L. 584       190  LOAD_FAST                'old_command_defs'
              192  POP_JUMP_IF_FALSE   238  'to 238'

 L. 585       194  LOAD_FAST                'old_command_defs'
              196  LOAD_CONST               0
              198  BINARY_SUBSCR    
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                commands
              204  LOAD_FAST                'bnum'
              206  STORE_SUBSCR     

 L. 586       208  LOAD_FAST                'old_command_defs'
              210  LOAD_CONST               1
              212  BINARY_SUBSCR    
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                commands_doprompt
              218  LOAD_FAST                'bnum'
              220  STORE_SUBSCR     

 L. 587       222  LOAD_FAST                'old_command_defs'
              224  LOAD_CONST               2
              226  BINARY_SUBSCR    
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                commands_silent
              232  LOAD_FAST                'bnum'
              234  STORE_SUBSCR     
              236  JUMP_FORWARD        262  'to 262'
            238_0  COME_FROM           192  '192'

 L. 589       238  LOAD_FAST                'self'
              240  LOAD_ATTR                commands
              242  LOAD_FAST                'bnum'
              244  DELETE_SUBSCR    

 L. 590       246  LOAD_FAST                'self'
              248  LOAD_ATTR                commands_doprompt
              250  LOAD_FAST                'bnum'
              252  DELETE_SUBSCR    

 L. 591       254  LOAD_FAST                'self'
              256  LOAD_ATTR                commands_silent
              258  LOAD_FAST                'bnum'
              260  DELETE_SUBSCR    
            262_0  COME_FROM           236  '236'

 L. 592       262  LOAD_FAST                'self'
              264  LOAD_METHOD              error
              266  LOAD_STR                 'command definition aborted, old commands restored'
              268  CALL_METHOD_1         1  ''
              270  POP_TOP          
              272  POP_EXCEPT       
              274  JUMP_FORWARD        278  'to 278'
            276_0  COME_FROM           180  '180'
              276  END_FINALLY      
            278_0  COME_FROM           274  '274'
            278_1  COME_FROM           172  '172'
              278  POP_BLOCK        
              280  BEGIN_FINALLY    
            282_0  COME_FROM_FINALLY   158  '158'

 L. 594       282  LOAD_CONST               False
              284  LOAD_FAST                'self'
              286  STORE_ATTR               commands_defining

 L. 595       288  LOAD_FAST                'prompt_back'
              290  LOAD_FAST                'self'
              292  STORE_ATTR               prompt
              294  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 54

    complete_commands = _complete_bpnumber

    def do_break--- This code section failed: ---

 L. 614         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_TRUE     56  'to 56'

 L. 615         4  LOAD_FAST                'self'
                6  LOAD_ATTR                breaks
                8  POP_JUMP_IF_FALSE    52  'to 52'

 L. 616        10  LOAD_FAST                'self'
               12  LOAD_METHOD              message
               14  LOAD_STR                 'Num Type         Disp Enb   Where'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L. 617        20  LOAD_GLOBAL              bdb
               22  LOAD_ATTR                Breakpoint
               24  LOAD_ATTR                bpbynumber
               26  GET_ITER         
             28_0  COME_FROM            50  '50'
             28_1  COME_FROM            34  '34'
               28  FOR_ITER             52  'to 52'
               30  STORE_FAST               'bp'

 L. 618        32  LOAD_FAST                'bp'
               34  POP_JUMP_IF_FALSE_BACK    28  'to 28'

 L. 619        36  LOAD_FAST                'self'
               38  LOAD_METHOD              message
               40  LOAD_FAST                'bp'
               42  LOAD_METHOD              bpformat
               44  CALL_METHOD_0         0  ''
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
               50  JUMP_BACK            28  'to 28'
             52_0  COME_FROM            28  '28'
             52_1  COME_FROM             8  '8'

 L. 620        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM             2  '2'

 L. 623        56  LOAD_CONST               None
               58  STORE_FAST               'filename'

 L. 624        60  LOAD_CONST               None
               62  STORE_FAST               'lineno'

 L. 625        64  LOAD_CONST               None
               66  STORE_FAST               'cond'

 L. 626        68  LOAD_FAST                'arg'
               70  LOAD_METHOD              find
               72  LOAD_STR                 ','
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'comma'

 L. 627        78  LOAD_FAST                'comma'
               80  LOAD_CONST               0
               82  COMPARE_OP               >
               84  POP_JUMP_IF_FALSE   122  'to 122'

 L. 629        86  LOAD_FAST                'arg'
               88  LOAD_FAST                'comma'
               90  LOAD_CONST               1
               92  BINARY_ADD       
               94  LOAD_CONST               None
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  LOAD_METHOD              lstrip
              102  CALL_METHOD_0         0  ''
              104  STORE_FAST               'cond'

 L. 630       106  LOAD_FAST                'arg'
              108  LOAD_CONST               None
              110  LOAD_FAST                'comma'
              112  BUILD_SLICE_2         2 
              114  BINARY_SUBSCR    
              116  LOAD_METHOD              rstrip
              118  CALL_METHOD_0         0  ''
              120  STORE_FAST               'arg'
            122_0  COME_FROM            84  '84'

 L. 632       122  LOAD_FAST                'arg'
              124  LOAD_METHOD              rfind
              126  LOAD_STR                 ':'
              128  CALL_METHOD_1         1  ''
              130  STORE_FAST               'colon'

 L. 633       132  LOAD_CONST               None
              134  STORE_FAST               'funcname'

 L. 634       136  LOAD_FAST                'colon'
              138  LOAD_CONST               0
              140  COMPARE_OP               >=
          142_144  POP_JUMP_IF_FALSE   272  'to 272'

 L. 635       146  LOAD_FAST                'arg'
              148  LOAD_CONST               None
              150  LOAD_FAST                'colon'
              152  BUILD_SLICE_2         2 
              154  BINARY_SUBSCR    
              156  LOAD_METHOD              rstrip
              158  CALL_METHOD_0         0  ''
              160  STORE_FAST               'filename'

 L. 636       162  LOAD_FAST                'self'
              164  LOAD_METHOD              lookupmodule
              166  LOAD_FAST                'filename'
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'f'

 L. 637       172  LOAD_FAST                'f'
              174  POP_JUMP_IF_TRUE    194  'to 194'

 L. 638       176  LOAD_FAST                'self'
              178  LOAD_METHOD              error
              180  LOAD_STR                 '%r not found from sys.path'
              182  LOAD_FAST                'filename'
              184  BINARY_MODULO    
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L. 639       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           174  '174'

 L. 641       194  LOAD_FAST                'f'
              196  STORE_FAST               'filename'

 L. 642       198  LOAD_FAST                'arg'
              200  LOAD_FAST                'colon'
              202  LOAD_CONST               1
              204  BINARY_ADD       
              206  LOAD_CONST               None
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  LOAD_METHOD              lstrip
              214  CALL_METHOD_0         0  ''
              216  STORE_FAST               'arg'

 L. 643       218  SETUP_FINALLY       232  'to 232'

 L. 644       220  LOAD_GLOBAL              int
              222  LOAD_FAST                'arg'
              224  CALL_FUNCTION_1       1  ''
              226  STORE_FAST               'lineno'
              228  POP_BLOCK        
              230  JUMP_FORWARD        270  'to 270'
            232_0  COME_FROM_FINALLY   218  '218'

 L. 645       232  DUP_TOP          
              234  LOAD_GLOBAL              ValueError
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   268  'to 268'
              242  POP_TOP          
              244  POP_TOP          
              246  POP_TOP          

 L. 646       248  LOAD_FAST                'self'
              250  LOAD_METHOD              error
              252  LOAD_STR                 'Bad lineno: %s'
              254  LOAD_FAST                'arg'
              256  BINARY_MODULO    
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          

 L. 647       262  POP_EXCEPT       
              264  LOAD_CONST               None
              266  RETURN_VALUE     
            268_0  COME_FROM           238  '238'
              268  END_FINALLY      
            270_0  COME_FROM           230  '230'
              270  JUMP_FORWARD        464  'to 464'
            272_0  COME_FROM           142  '142'

 L. 650       272  SETUP_FINALLY       286  'to 286'

 L. 651       274  LOAD_GLOBAL              int
              276  LOAD_FAST                'arg'
              278  CALL_FUNCTION_1       1  ''
              280  STORE_FAST               'lineno'
              282  POP_BLOCK        
              284  JUMP_FORWARD        464  'to 464'
            286_0  COME_FROM_FINALLY   272  '272'

 L. 652       286  DUP_TOP          
              288  LOAD_GLOBAL              ValueError
              290  COMPARE_OP               exception-match
          292_294  POP_JUMP_IF_FALSE   462  'to 462'
              296  POP_TOP          
              298  POP_TOP          
              300  POP_TOP          

 L. 653       302  SETUP_FINALLY       326  'to 326'

 L. 654       304  LOAD_GLOBAL              eval
              306  LOAD_FAST                'arg'

 L. 655       308  LOAD_FAST                'self'
              310  LOAD_ATTR                curframe
              312  LOAD_ATTR                f_globals

 L. 656       314  LOAD_FAST                'self'
              316  LOAD_ATTR                curframe_locals

 L. 654       318  CALL_FUNCTION_3       3  ''
              320  STORE_FAST               'func'
              322  POP_BLOCK        
              324  JUMP_FORWARD        342  'to 342'
            326_0  COME_FROM_FINALLY   302  '302'

 L. 657       326  POP_TOP          
              328  POP_TOP          
              330  POP_TOP          

 L. 658       332  LOAD_FAST                'arg'
              334  STORE_FAST               'func'
              336  POP_EXCEPT       
              338  JUMP_FORWARD        342  'to 342'
              340  END_FINALLY      
            342_0  COME_FROM           338  '338'
            342_1  COME_FROM           324  '324'

 L. 659       342  SETUP_FINALLY       390  'to 390'

 L. 660       344  LOAD_GLOBAL              hasattr
              346  LOAD_FAST                'func'
              348  LOAD_STR                 '__func__'
              350  CALL_FUNCTION_2       2  ''
          352_354  POP_JUMP_IF_FALSE   362  'to 362'

 L. 661       356  LOAD_FAST                'func'
              358  LOAD_ATTR                __func__
              360  STORE_FAST               'func'
            362_0  COME_FROM           352  '352'

 L. 662       362  LOAD_FAST                'func'
              364  LOAD_ATTR                __code__
              366  STORE_FAST               'code'

 L. 665       368  LOAD_FAST                'code'
              370  LOAD_ATTR                co_name
              372  STORE_FAST               'funcname'

 L. 666       374  LOAD_FAST                'code'
              376  LOAD_ATTR                co_firstlineno
              378  STORE_FAST               'lineno'

 L. 667       380  LOAD_FAST                'code'
              382  LOAD_ATTR                co_filename
              384  STORE_FAST               'filename'
              386  POP_BLOCK        
              388  JUMP_FORWARD        458  'to 458'
            390_0  COME_FROM_FINALLY   342  '342'

 L. 668       390  POP_TOP          
              392  POP_TOP          
              394  POP_TOP          

 L. 670       396  LOAD_FAST                'self'
              398  LOAD_METHOD              lineinfo
              400  LOAD_FAST                'arg'
              402  CALL_METHOD_1         1  ''
              404  UNPACK_SEQUENCE_3     3 
              406  STORE_FAST               'ok'
              408  STORE_FAST               'filename'
              410  STORE_FAST               'ln'

 L. 671       412  LOAD_FAST                'ok'
          414_416  POP_JUMP_IF_TRUE    440  'to 440'

 L. 672       418  LOAD_FAST                'self'
              420  LOAD_METHOD              error
              422  LOAD_STR                 'The specified object %r is not a function or was not found along sys.path.'

 L. 673       424  LOAD_FAST                'arg'

 L. 672       426  BINARY_MODULO    
              428  CALL_METHOD_1         1  ''
              430  POP_TOP          

 L. 674       432  POP_EXCEPT       
              434  POP_EXCEPT       
              436  LOAD_CONST               None
              438  RETURN_VALUE     
            440_0  COME_FROM           414  '414'

 L. 675       440  LOAD_FAST                'ok'
              442  STORE_FAST               'funcname'

 L. 676       444  LOAD_GLOBAL              int
              446  LOAD_FAST                'ln'
              448  CALL_FUNCTION_1       1  ''
              450  STORE_FAST               'lineno'
              452  POP_EXCEPT       
              454  JUMP_FORWARD        458  'to 458'
              456  END_FINALLY      
            458_0  COME_FROM           454  '454'
            458_1  COME_FROM           388  '388'
              458  POP_EXCEPT       
              460  JUMP_FORWARD        464  'to 464'
            462_0  COME_FROM           292  '292'
              462  END_FINALLY      
            464_0  COME_FROM           460  '460'
            464_1  COME_FROM           284  '284'
            464_2  COME_FROM           270  '270'

 L. 677       464  LOAD_FAST                'filename'
          466_468  POP_JUMP_IF_TRUE    478  'to 478'

 L. 678       470  LOAD_FAST                'self'
              472  LOAD_METHOD              defaultFile
              474  CALL_METHOD_0         0  ''
              476  STORE_FAST               'filename'
            478_0  COME_FROM           466  '466'

 L. 680       478  LOAD_FAST                'self'
              480  LOAD_METHOD              checkline
              482  LOAD_FAST                'filename'
              484  LOAD_FAST                'lineno'
              486  CALL_METHOD_2         2  ''
              488  STORE_FAST               'line'

 L. 681       490  LOAD_FAST                'line'
          492_494  POP_JUMP_IF_FALSE   574  'to 574'

 L. 683       496  LOAD_FAST                'self'
              498  LOAD_METHOD              set_break
              500  LOAD_FAST                'filename'
              502  LOAD_FAST                'line'
              504  LOAD_FAST                'temporary'
              506  LOAD_FAST                'cond'
              508  LOAD_FAST                'funcname'
              510  CALL_METHOD_5         5  ''
              512  STORE_FAST               'err'

 L. 684       514  LOAD_FAST                'err'
          516_518  POP_JUMP_IF_FALSE   532  'to 532'

 L. 685       520  LOAD_FAST                'self'
              522  LOAD_METHOD              error
              524  LOAD_FAST                'err'
              526  CALL_METHOD_1         1  ''
              528  POP_TOP          
              530  JUMP_FORWARD        574  'to 574'
            532_0  COME_FROM           516  '516'

 L. 687       532  LOAD_FAST                'self'
              534  LOAD_METHOD              get_breaks
              536  LOAD_FAST                'filename'
              538  LOAD_FAST                'line'
              540  CALL_METHOD_2         2  ''
              542  LOAD_CONST               -1
              544  BINARY_SUBSCR    
              546  STORE_FAST               'bp'

 L. 688       548  LOAD_FAST                'self'
              550  LOAD_METHOD              message
              552  LOAD_STR                 'Breakpoint %d at %s:%d'

 L. 689       554  LOAD_FAST                'bp'
              556  LOAD_ATTR                number
              558  LOAD_FAST                'bp'
              560  LOAD_ATTR                file
              562  LOAD_FAST                'bp'
              564  LOAD_ATTR                line
              566  BUILD_TUPLE_3         3 

 L. 688       568  BINARY_MODULO    
              570  CALL_METHOD_1         1  ''
              572  POP_TOP          
            574_0  COME_FROM           530  '530'
            574_1  COME_FROM           492  '492'

Parse error at or near `LOAD_CONST' instruction at offset 264

    def defaultFile(self):
        """Produce a reasonable default."""
        filename = self.curframe.f_code.co_filename
        if filename == '<string>':
            if self.mainpyfile:
                filename = self.mainpyfile
        return filename

    do_b = do_break
    complete_break = _complete_location
    complete_b = _complete_location

    def do_tbreak(self, arg):
        """tbreak [ ([filename:]lineno | function) [, condition] ]
        Same arguments as break, but sets a temporary breakpoint: it
        is automatically deleted when first hit.
        """
        self.do_break(arg, 1)

    complete_tbreak = _complete_location

    def lineinfo(self, identifier):
        failed = (None, None, None)
        idstring = identifier.split"'"
        if len(idstring) == 1:
            id = idstring[0].strip()
        elif len(idstring) == 3:
            id = idstring[1].strip()
        else:
            return failed
        if id == '':
            return failed
        parts = id.split'.'
        if parts[0] == 'self':
            del parts[0]
            if len(parts) == 0:
                return failed
        fname = self.defaultFile()
        if len(parts) == 1:
            item = parts[0]
        else:
            f = self.lookupmoduleparts[0]
            if f:
                fname = f
            item = parts[1]
        answer = find_function(item, fname)
        return answer or failed

    def checkline(self, filename, lineno):
        """Check whether specified line seems to be executable.

        Return `lineno` if it is, 0 if not (e.g. a docstring, comment, blank
        line or EOF). Warning: testing is not comprehensive.
        """
        globs = self.curframe.f_globals if hasattr(self, 'curframe') else None
        line = linecache.getline(filename, lineno, globs)
        if not line:
            self.message'End of file'
            return 0
        line = line.strip()
        if line:
            if line[0] == '#' or (line[:3] == '"""' or line[:3] == "'''"):
                self.error'Blank or comment'
                return 0
            return lineno

    def do_enable(self, arg):
        """enable bpnumber [bpnumber ...]
        Enables the breakpoints given as a space separated list of
        breakpoint numbers.
        """
        args = arg.split()
        for i in args:
            try:
                bp = self.get_bpbynumberi
            except ValueError as err:
                try:
                    self.errorerr
                finally:
                    err = None
                    del err

            else:
                bp.enable()
                self.message('Enabled %s' % bp)

    complete_enable = _complete_bpnumber

    def do_disable(self, arg):
        """disable bpnumber [bpnumber ...]
        Disables the breakpoints given as a space separated list of
        breakpoint numbers.  Disabling a breakpoint means it cannot
        cause the program to stop execution, but unlike clearing a
        breakpoint, it remains in the list of breakpoints and can be
        (re-)enabled.
        """
        args = arg.split()
        for i in args:
            try:
                bp = self.get_bpbynumberi
            except ValueError as err:
                try:
                    self.errorerr
                finally:
                    err = None
                    del err

            else:
                bp.disable()
                self.message('Disabled %s' % bp)

    complete_disable = _complete_bpnumber

    def do_condition(self, arg):
        """condition bpnumber [condition]
        Set a new condition for the breakpoint, an expression which
        must evaluate to true before the breakpoint is honored.  If
        condition is absent, any existing condition is removed; i.e.,
        the breakpoint is made unconditional.
        """
        args = arg.split(' ', 1)
        try:
            cond = args[1]
        except IndexError:
            cond = None
        else:
            try:
                bp = self.get_bpbynumberargs[0].strip()
            except IndexError:
                self.error'Breakpoint number expected'
            except ValueError as err:
                try:
                    self.errorerr
                finally:
                    err = None
                    del err

            else:
                bp.cond = cond
                if not cond:
                    self.message('Breakpoint %d is now unconditional.' % bp.number)
                else:
                    self.message('New condition set for breakpoint %d.' % bp.number)

    complete_condition = _complete_bpnumber

    def do_ignore(self, arg):
        """ignore bpnumber [count]
        Set the ignore count for the given breakpoint number.  If
        count is omitted, the ignore count is set to 0.  A breakpoint
        becomes active when the ignore count is zero.  When non-zero,
        the count is decremented each time the breakpoint is reached
        and the breakpoint is not disabled and any associated
        condition evaluates to true.
        """
        args = arg.split()
        try:
            count = int(args[1].strip())
        except:
            count = 0
        else:
            try:
                bp = self.get_bpbynumberargs[0].strip()
            except IndexError:
                self.error'Breakpoint number expected'
            except ValueError as err:
                try:
                    self.errorerr
                finally:
                    err = None
                    del err

            else:
                bp.ignore = count
                if count > 0:
                    if count > 1:
                        countstr = '%d crossings' % count
                    else:
                        countstr = '1 crossing'
                    self.message('Will ignore next %s of breakpoint %d.' % (
                     countstr, bp.number))
                else:
                    self.message('Will stop next time breakpoint %d is reached.' % bp.number)

    complete_ignore = _complete_bpnumber

    def do_clear(self, arg):
        """cl(ear) filename:lineno
cl(ear) [bpnumber [bpnumber...]]
        With a space separated list of breakpoint numbers, clear
        those breakpoints.  Without argument, clear all breaks (but
        first ask confirmation).  With a filename:lineno argument,
        clear all breaks at that line in that file.
        """
        if not arg:
            try:
                reply = input('Clear all breaks? ')
            except EOFError:
                reply = 'no'
            else:
                reply = reply.strip().lower()
                if reply in ('y', 'yes'):
                    bplist = [bp for bp in bdb.Breakpoint.bpbynumber if bp]
                    self.clear_all_breaks()
                    for bp in bplist:
                        self.message('Deleted %s' % bp)

                    return
        if ':' in arg:
            i = arg.rfind':'
            filename = arg[:i]
            arg = arg[i + 1:]
            try:
                lineno = int(arg)
            except ValueError:
                err = 'Invalid line number (%s)' % arg
            else:
                bplist = self.get_breaks(filename, lineno)
                err = self.clear_break(filename, lineno)
            if err:
                self.errorerr
            else:
                pass
            for bp in bplist:
                self.message('Deleted %s' % bp)
            else:
                return

        numberlist = arg.split()
        for i in numberlist:
            try:
                bp = self.get_bpbynumberi
            except ValueError as err:
                try:
                    self.errorerr
                finally:
                    err = None
                    del err

            else:
                self.clear_bpbynumberi
                self.message('Deleted %s' % bp)

    do_cl = do_clear
    complete_clear = _complete_location
    complete_cl = _complete_location

    def do_where(self, arg):
        """w(here)
        Print a stack trace, with the most recent frame at the bottom.
        An arrow indicates the "current frame", which determines the
        context of most commands.  'bt' is an alias for this command.
        """
        self.print_stack_trace()

    do_w = do_where
    do_bt = do_where

    def _select_frame(self, number):
        assert 0 <= number < len(self.stack)
        self.curindex = number
        self.curframe = self.stack[self.curindex][0]
        self.curframe_locals = self.curframe.f_locals
        self.print_stack_entryself.stack[self.curindex]
        self.lineno = None

    def do_up--- This code section failed: ---

 L. 940         0  LOAD_FAST                'self'
                2  LOAD_ATTR                curindex
                4  LOAD_CONST               0
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 941        10  LOAD_FAST                'self'
               12  LOAD_METHOD              error
               14  LOAD_STR                 'Oldest frame'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L. 942        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM             8  '8'

 L. 943        24  SETUP_FINALLY        42  'to 42'

 L. 944        26  LOAD_GLOBAL              int
               28  LOAD_FAST                'arg'
               30  JUMP_IF_TRUE_OR_POP    34  'to 34'
               32  LOAD_CONST               1
             34_0  COME_FROM            30  '30'
               34  CALL_FUNCTION_1       1  ''
               36  STORE_FAST               'count'
               38  POP_BLOCK        
               40  JUMP_FORWARD         78  'to 78'
             42_0  COME_FROM_FINALLY    24  '24'

 L. 945        42  DUP_TOP          
               44  LOAD_GLOBAL              ValueError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    76  'to 76'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 946        56  LOAD_FAST                'self'
               58  LOAD_METHOD              error
               60  LOAD_STR                 'Invalid frame count (%s)'
               62  LOAD_FAST                'arg'
               64  BINARY_MODULO    
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L. 947        70  POP_EXCEPT       
               72  LOAD_CONST               None
               74  RETURN_VALUE     
             76_0  COME_FROM            48  '48'
               76  END_FINALLY      
             78_0  COME_FROM            40  '40'

 L. 948        78  LOAD_FAST                'count'
               80  LOAD_CONST               0
               82  COMPARE_OP               <
               84  POP_JUMP_IF_FALSE    92  'to 92'

 L. 949        86  LOAD_CONST               0
               88  STORE_FAST               'newframe'
               90  JUMP_FORWARD        108  'to 108'
             92_0  COME_FROM            84  '84'

 L. 951        92  LOAD_GLOBAL              max
               94  LOAD_CONST               0
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                curindex
              100  LOAD_FAST                'count'
              102  BINARY_SUBTRACT  
              104  CALL_FUNCTION_2       2  ''
              106  STORE_FAST               'newframe'
            108_0  COME_FROM            90  '90'

 L. 952       108  LOAD_FAST                'self'
              110  LOAD_METHOD              _select_frame
              112  LOAD_FAST                'newframe'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 72

    do_u = do_up

    def do_down--- This code section failed: ---

 L. 960         0  LOAD_FAST                'self'
                2  LOAD_ATTR                curindex
                4  LOAD_CONST               1
                6  BINARY_ADD       
                8  LOAD_GLOBAL              len
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                stack
               14  CALL_FUNCTION_1       1  ''
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    34  'to 34'

 L. 961        20  LOAD_FAST                'self'
               22  LOAD_METHOD              error
               24  LOAD_STR                 'Newest frame'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 962        30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            18  '18'

 L. 963        34  SETUP_FINALLY        52  'to 52'

 L. 964        36  LOAD_GLOBAL              int
               38  LOAD_FAST                'arg'
               40  JUMP_IF_TRUE_OR_POP    44  'to 44'
               42  LOAD_CONST               1
             44_0  COME_FROM            40  '40'
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'count'
               48  POP_BLOCK        
               50  JUMP_FORWARD         88  'to 88'
             52_0  COME_FROM_FINALLY    34  '34'

 L. 965        52  DUP_TOP          
               54  LOAD_GLOBAL              ValueError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    86  'to 86'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 966        66  LOAD_FAST                'self'
               68  LOAD_METHOD              error
               70  LOAD_STR                 'Invalid frame count (%s)'
               72  LOAD_FAST                'arg'
               74  BINARY_MODULO    
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 967        80  POP_EXCEPT       
               82  LOAD_CONST               None
               84  RETURN_VALUE     
             86_0  COME_FROM            58  '58'
               86  END_FINALLY      
             88_0  COME_FROM            50  '50'

 L. 968        88  LOAD_FAST                'count'
               90  LOAD_CONST               0
               92  COMPARE_OP               <
               94  POP_JUMP_IF_FALSE   112  'to 112'

 L. 969        96  LOAD_GLOBAL              len
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                stack
              102  CALL_FUNCTION_1       1  ''
              104  LOAD_CONST               1
              106  BINARY_SUBTRACT  
              108  STORE_FAST               'newframe'
              110  JUMP_FORWARD        138  'to 138'
            112_0  COME_FROM            94  '94'

 L. 971       112  LOAD_GLOBAL              min
              114  LOAD_GLOBAL              len
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                stack
              120  CALL_FUNCTION_1       1  ''
              122  LOAD_CONST               1
              124  BINARY_SUBTRACT  
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                curindex
              130  LOAD_FAST                'count'
              132  BINARY_ADD       
              134  CALL_FUNCTION_2       2  ''
              136  STORE_FAST               'newframe'
            138_0  COME_FROM           110  '110'

 L. 972       138  LOAD_FAST                'self'
              140  LOAD_METHOD              _select_frame
              142  LOAD_FAST                'newframe'
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 82

    do_d = do_down

    def do_until--- This code section failed: ---

 L. 983         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_FALSE    82  'to 82'

 L. 984         4  SETUP_FINALLY        18  'to 18'

 L. 985         6  LOAD_GLOBAL              int
                8  LOAD_FAST                'arg'
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'lineno'
               14  POP_BLOCK        
               16  JUMP_FORWARD         54  'to 54'
             18_0  COME_FROM_FINALLY     4  '4'

 L. 986        18  DUP_TOP          
               20  LOAD_GLOBAL              ValueError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    52  'to 52'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 987        32  LOAD_FAST                'self'
               34  LOAD_METHOD              error
               36  LOAD_STR                 'Error in argument: %r'
               38  LOAD_FAST                'arg'
               40  BINARY_MODULO    
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 988        46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            24  '24'
               52  END_FINALLY      
             54_0  COME_FROM            16  '16'

 L. 989        54  LOAD_FAST                'lineno'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                curframe
               60  LOAD_ATTR                f_lineno
               62  COMPARE_OP               <=
               64  POP_JUMP_IF_FALSE    86  'to 86'

 L. 990        66  LOAD_FAST                'self'
               68  LOAD_METHOD              error
               70  LOAD_STR                 '"until" line number is smaller than current line number'
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          

 L. 992        76  LOAD_CONST               None
               78  RETURN_VALUE     
               80  JUMP_FORWARD         86  'to 86'
             82_0  COME_FROM             2  '2'

 L. 994        82  LOAD_CONST               None
               84  STORE_FAST               'lineno'
             86_0  COME_FROM            80  '80'
             86_1  COME_FROM            64  '64'

 L. 995        86  LOAD_FAST                'self'
               88  LOAD_METHOD              set_until
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                curframe
               94  LOAD_FAST                'lineno'
               96  CALL_METHOD_2         2  ''
               98  POP_TOP          

 L. 996       100  LOAD_CONST               1
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 48

    do_unt = do_until

    def do_step(self, arg):
        """s(tep)
        Execute the current line, stop at the first possible occasion
        (either in a function that is called or in the current
        function).
        """
        self.set_step()
        return 1

    do_s = do_step

    def do_next(self, arg):
        """n(ext)
        Continue execution until the next line in the current function
        is reached or it returns.
        """
        self.set_nextself.curframe
        return 1

    do_n = do_next

    def do_run(self, arg):
        """run [args...]
        Restart the debugged python program. If a string is supplied
        it is split with "shlex", and the result is used as the new
        sys.argv.  History, breakpoints, actions and debugger options
        are preserved.  "restart" is an alias for "run".
        """
        if arg:
            import shlex
            argv0 = sys.argv[0:1]
            sys.argv = shlex.splitarg
            sys.argv[:0] = argv0
        raise Restart

    do_restart = do_run

    def do_return(self, arg):
        """r(eturn)
        Continue execution until the current function returns.
        """
        self.set_returnself.curframe
        return 1

    do_r = do_return

    def do_continue(self, arg):
        """c(ont(inue))
        Continue execution, only stop when a breakpoint is encountered.
        """
        if not self.nosigint:
            try:
                Pdb._previous_sigint_handler = signal.signal(signal.SIGINT, self.sigint_handler)
            except ValueError:
                pass
            else:
                self.set_continue()
            return 1

    do_c = do_cont = do_continue

    def do_jump(self, arg):
        """j(ump) lineno
        Set the next line that will be executed.  Only available in
        the bottom-most frame.  This lets you jump back and execute
        code again, or jump forward to skip code that you don't want
        to run.

        It should be noted that not all jumps are allowed -- for
        instance it is not possible to jump into the middle of a
        for loop or out of a finally clause.
        """
        if self.curindex + 1 != len(self.stack):
            self.error'You can only jump within the bottom frame'
            return
        try:
            arg = int(arg)
        except ValueError:
            self.error"The 'jump' command requires a line number"

        try:
            self.curframe.f_lineno = arg
            self.stack[self.curindex] = (self.stack[self.curindex][0], arg)
            self.print_stack_entryself.stack[self.curindex]
        except ValueError as e:
            try:
                self.error('Jump failed: %s' % e)
            finally:
                e = None
                del e

    do_j = do_jump

    def do_debug(self, arg):
        """debug code
        Enter a recursive debugger that steps through the code
        argument (which is an arbitrary expression or statement to be
        executed in the current environment).
        """
        sys.settraceNone
        globals = self.curframe.f_globals
        locals = self.curframe_locals
        p = Pdb(self.completekey, self.stdin, self.stdout)
        p.prompt = '(%s) ' % self.prompt.strip()
        self.message'ENTERING RECURSIVE DEBUGGER'
        try:
            sys.call_tracing(p.run, (arg, globals, locals))
        except Exception:
            exc_info = sys.exc_info()[:2]
            self.error(traceback.format_exception_only)(*exc_info)[(-1)].strip()
        else:
            self.message'LEAVING RECURSIVE DEBUGGER'
            sys.settraceself.trace_dispatch
            self.lastcmd = p.lastcmd

    complete_debug = _complete_expression

    def do_quit(self, arg):
        """q(uit)
exit
        Quit from the debugger. The program being executed is aborted.
        """
        self._user_requested_quit = True
        self.set_quit()
        return 1

    do_q = do_quit
    do_exit = do_quit

    def do_EOF(self, arg):
        """EOF
        Handles the receipt of EOF as a command.
        """
        self.message''
        self._user_requested_quit = True
        self.set_quit()
        return 1

    def do_args(self, arg):
        """a(rgs)
        Print the argument list of the current function.
        """
        co = self.curframe.f_code
        dict = self.curframe_locals
        n = co.co_argcount + co.co_kwonlyargcount
        if co.co_flags & inspect.CO_VARARGS:
            n = n + 1
        if co.co_flags & inspect.CO_VARKEYWORDS:
            n = n + 1
        for i in range(n):
            name = co.co_varnames[i]
            if name in dict:
                self.message('%s = %r' % (name, dict[name]))
            else:
                self.message('%s = *** undefined ***' % (name,))

    do_a = do_args

    def do_retval(self, arg):
        """retval
        Print the return value for the last return of a function.
        """
        if '__return__' in self.curframe_locals:
            self.messagerepr(self.curframe_locals['__return__'])
        else:
            self.error'Not yet returned!'

    do_rv = do_retval

    def _getval--- This code section failed: ---

 L.1161         0  SETUP_FINALLY        22  'to 22'

 L.1162         2  LOAD_GLOBAL              eval
                4  LOAD_FAST                'arg'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                curframe
               10  LOAD_ATTR                f_globals
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                curframe_locals
               16  CALL_FUNCTION_3       3  ''
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L.1163        22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.1164        28  LOAD_GLOBAL              sys
               30  LOAD_METHOD              exc_info
               32  CALL_METHOD_0         0  ''
               34  LOAD_CONST               None
               36  LOAD_CONST               2
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  STORE_FAST               'exc_info'

 L.1165        44  LOAD_FAST                'self'
               46  LOAD_METHOD              error
               48  LOAD_GLOBAL              traceback
               50  LOAD_ATTR                format_exception_only
               52  LOAD_FAST                'exc_info'
               54  CALL_FUNCTION_EX      0  'positional arguments only'
               56  LOAD_CONST               -1
               58  BINARY_SUBSCR    
               60  LOAD_METHOD              strip
               62  CALL_METHOD_0         0  ''
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L.1166        68  RAISE_VARARGS_0       0  'reraise'
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
               74  END_FINALLY      
             76_0  COME_FROM            72  '72'

Parse error at or near `STORE_FAST' instruction at offset 42

    def _getval_except(self, arg, frame=None):
        try:
            if frame is None:
                return eval(arg, self.curframe.f_globals, self.curframe_locals)
            return eval(arg, frame.f_globals, frame.f_locals)
        except:
            exc_info = sys.exc_info()[:2]
            err = (traceback.format_exception_only)(*exc_info)[(-1)].strip()
            return _rstr('** raised %s **' % err)

    def do_p(self, arg):
        """p expression
        Print the value of the expression.
        """
        try:
            self.messagerepr(self._getvalarg)
        except:
            pass

    def do_pp(self, arg):
        """pp expression
        Pretty-print the value of the expression.
        """
        try:
            self.messagepprint.pformatself._getvalarg
        except:
            pass

    complete_print = _complete_expression
    complete_p = _complete_expression
    complete_pp = _complete_expression

    def do_list--- This code section failed: ---

 L.1216         0  LOAD_STR                 'list'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               lastcmd

 L.1217         6  LOAD_CONST               None
                8  STORE_FAST               'last'

 L.1218        10  LOAD_FAST                'arg'
               12  POP_JUMP_IF_FALSE   156  'to 156'
               14  LOAD_FAST                'arg'
               16  LOAD_STR                 '.'
               18  COMPARE_OP               !=
               20  POP_JUMP_IF_FALSE   156  'to 156'

 L.1219        22  SETUP_FINALLY       118  'to 118'

 L.1220        24  LOAD_STR                 ','
               26  LOAD_FAST                'arg'
               28  COMPARE_OP               in
               30  POP_JUMP_IF_FALSE    88  'to 88'

 L.1221        32  LOAD_FAST                'arg'
               34  LOAD_METHOD              split
               36  LOAD_STR                 ','
               38  CALL_METHOD_1         1  ''
               40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'first'
               44  STORE_FAST               'last'

 L.1222        46  LOAD_GLOBAL              int
               48  LOAD_FAST                'first'
               50  LOAD_METHOD              strip
               52  CALL_METHOD_0         0  ''
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'first'

 L.1223        58  LOAD_GLOBAL              int
               60  LOAD_FAST                'last'
               62  LOAD_METHOD              strip
               64  CALL_METHOD_0         0  ''
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'last'

 L.1224        70  LOAD_FAST                'last'
               72  LOAD_FAST                'first'
               74  COMPARE_OP               <
               76  POP_JUMP_IF_FALSE   114  'to 114'

 L.1226        78  LOAD_FAST                'first'
               80  LOAD_FAST                'last'
               82  BINARY_ADD       
               84  STORE_FAST               'last'
               86  JUMP_FORWARD        114  'to 114'
             88_0  COME_FROM            30  '30'

 L.1228        88  LOAD_GLOBAL              int
               90  LOAD_FAST                'arg'
               92  LOAD_METHOD              strip
               94  CALL_METHOD_0         0  ''
               96  CALL_FUNCTION_1       1  ''
               98  STORE_FAST               'first'

 L.1229       100  LOAD_GLOBAL              max
              102  LOAD_CONST               1
              104  LOAD_FAST                'first'
              106  LOAD_CONST               5
              108  BINARY_SUBTRACT  
              110  CALL_FUNCTION_2       2  ''
              112  STORE_FAST               'first'
            114_0  COME_FROM            86  '86'
            114_1  COME_FROM            76  '76'
              114  POP_BLOCK        
              116  JUMP_FORWARD        204  'to 204'
            118_0  COME_FROM_FINALLY    22  '22'

 L.1230       118  DUP_TOP          
              120  LOAD_GLOBAL              ValueError
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   152  'to 152'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L.1231       132  LOAD_FAST                'self'
              134  LOAD_METHOD              error
              136  LOAD_STR                 'Error in argument: %r'
              138  LOAD_FAST                'arg'
              140  BINARY_MODULO    
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          

 L.1232       146  POP_EXCEPT       
              148  LOAD_CONST               None
              150  RETURN_VALUE     
            152_0  COME_FROM           124  '124'
              152  END_FINALLY      
              154  JUMP_FORWARD        204  'to 204'
            156_0  COME_FROM            20  '20'
            156_1  COME_FROM            12  '12'

 L.1233       156  LOAD_FAST                'self'
              158  LOAD_ATTR                lineno
              160  LOAD_CONST               None
              162  COMPARE_OP               is
              164  POP_JUMP_IF_TRUE    174  'to 174'
              166  LOAD_FAST                'arg'
              168  LOAD_STR                 '.'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   194  'to 194'
            174_0  COME_FROM           164  '164'

 L.1234       174  LOAD_GLOBAL              max
              176  LOAD_CONST               1
              178  LOAD_FAST                'self'
              180  LOAD_ATTR                curframe
              182  LOAD_ATTR                f_lineno
              184  LOAD_CONST               5
              186  BINARY_SUBTRACT  
              188  CALL_FUNCTION_2       2  ''
              190  STORE_FAST               'first'
              192  JUMP_FORWARD        204  'to 204'
            194_0  COME_FROM           172  '172'

 L.1236       194  LOAD_FAST                'self'
              196  LOAD_ATTR                lineno
              198  LOAD_CONST               1
              200  BINARY_ADD       
              202  STORE_FAST               'first'
            204_0  COME_FROM           192  '192'
            204_1  COME_FROM           154  '154'
            204_2  COME_FROM           116  '116'

 L.1237       204  LOAD_FAST                'last'
              206  LOAD_CONST               None
              208  COMPARE_OP               is
              210  POP_JUMP_IF_FALSE   220  'to 220'

 L.1238       212  LOAD_FAST                'first'
              214  LOAD_CONST               10
              216  BINARY_ADD       
              218  STORE_FAST               'last'
            220_0  COME_FROM           210  '210'

 L.1239       220  LOAD_FAST                'self'
              222  LOAD_ATTR                curframe
              224  LOAD_ATTR                f_code
              226  LOAD_ATTR                co_filename
              228  STORE_FAST               'filename'

 L.1240       230  LOAD_FAST                'self'
              232  LOAD_METHOD              get_file_breaks
              234  LOAD_FAST                'filename'
              236  CALL_METHOD_1         1  ''
              238  STORE_FAST               'breaklist'

 L.1241       240  SETUP_FINALLY       332  'to 332'

 L.1242       242  LOAD_GLOBAL              linecache
              244  LOAD_METHOD              getlines
              246  LOAD_FAST                'filename'
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                curframe
              252  LOAD_ATTR                f_globals
              254  CALL_METHOD_2         2  ''
              256  STORE_FAST               'lines'

 L.1243       258  LOAD_FAST                'self'
              260  LOAD_METHOD              _print_lines
              262  LOAD_FAST                'lines'
              264  LOAD_FAST                'first'
              266  LOAD_CONST               1
              268  BINARY_SUBTRACT  
              270  LOAD_FAST                'last'
              272  BUILD_SLICE_2         2 
              274  BINARY_SUBSCR    
              276  LOAD_FAST                'first'
              278  LOAD_FAST                'breaklist'

 L.1244       280  LOAD_FAST                'self'
              282  LOAD_ATTR                curframe

 L.1243       284  CALL_METHOD_4         4  ''
              286  POP_TOP          

 L.1245       288  LOAD_GLOBAL              min
              290  LOAD_FAST                'last'
              292  LOAD_GLOBAL              len
              294  LOAD_FAST                'lines'
              296  CALL_FUNCTION_1       1  ''
              298  CALL_FUNCTION_2       2  ''
              300  LOAD_FAST                'self'
              302  STORE_ATTR               lineno

 L.1246       304  LOAD_GLOBAL              len
              306  LOAD_FAST                'lines'
              308  CALL_FUNCTION_1       1  ''
              310  LOAD_FAST                'last'
              312  COMPARE_OP               <
          314_316  POP_JUMP_IF_FALSE   328  'to 328'

 L.1247       318  LOAD_FAST                'self'
              320  LOAD_METHOD              message
              322  LOAD_STR                 '[EOF]'
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          
            328_0  COME_FROM           314  '314'
              328  POP_BLOCK        
              330  JUMP_FORWARD        354  'to 354'
            332_0  COME_FROM_FINALLY   240  '240'

 L.1248       332  DUP_TOP          
              334  LOAD_GLOBAL              KeyboardInterrupt
              336  COMPARE_OP               exception-match
          338_340  POP_JUMP_IF_FALSE   352  'to 352'
              342  POP_TOP          
              344  POP_TOP          
              346  POP_TOP          

 L.1249       348  POP_EXCEPT       
              350  JUMP_FORWARD        354  'to 354'
            352_0  COME_FROM           338  '338'
              352  END_FINALLY      
            354_0  COME_FROM           350  '350'
            354_1  COME_FROM           330  '330'

Parse error at or near `LOAD_CONST' instruction at offset 148

    do_l = do_list

    def do_longlist--- This code section failed: ---

 L.1256         0  LOAD_FAST                'self'
                2  LOAD_ATTR                curframe
                4  LOAD_ATTR                f_code
                6  LOAD_ATTR                co_filename
                8  STORE_FAST               'filename'

 L.1257        10  LOAD_FAST                'self'
               12  LOAD_METHOD              get_file_breaks
               14  LOAD_FAST                'filename'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'breaklist'

 L.1258        20  SETUP_FINALLY        40  'to 40'

 L.1259        22  LOAD_GLOBAL              getsourcelines
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                curframe
               28  CALL_FUNCTION_1       1  ''
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'lines'
               34  STORE_FAST               'lineno'
               36  POP_BLOCK        
               38  JUMP_FORWARD         90  'to 90'
             40_0  COME_FROM_FINALLY    20  '20'

 L.1260        40  DUP_TOP          
               42  LOAD_GLOBAL              OSError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    88  'to 88'
               48  POP_TOP          
               50  STORE_FAST               'err'
               52  POP_TOP          
               54  SETUP_FINALLY        76  'to 76'

 L.1261        56  LOAD_FAST                'self'
               58  LOAD_METHOD              error
               60  LOAD_FAST                'err'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L.1262        66  POP_BLOCK        
               68  POP_EXCEPT       
               70  CALL_FINALLY         76  'to 76'
               72  LOAD_CONST               None
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'
             76_1  COME_FROM_FINALLY    54  '54'
               76  LOAD_CONST               None
               78  STORE_FAST               'err'
               80  DELETE_FAST              'err'
               82  END_FINALLY      
               84  POP_EXCEPT       
               86  JUMP_FORWARD         90  'to 90'
             88_0  COME_FROM            46  '46'
               88  END_FINALLY      
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM            38  '38'

 L.1263        90  LOAD_FAST                'self'
               92  LOAD_METHOD              _print_lines
               94  LOAD_FAST                'lines'
               96  LOAD_FAST                'lineno'
               98  LOAD_FAST                'breaklist'
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                curframe
              104  CALL_METHOD_4         4  ''
              106  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 70

    do_ll = do_longlist

    def do_source--- This code section failed: ---

 L.1270         0  SETUP_FINALLY        16  'to 16'

 L.1271         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _getval
                6  LOAD_FAST                'arg'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'obj'
               12  POP_BLOCK        
               14  JUMP_FORWARD         30  'to 30'
             16_0  COME_FROM_FINALLY     0  '0'

 L.1272        16  POP_TOP          
               18  POP_TOP          
               20  POP_TOP          

 L.1273        22  POP_EXCEPT       
               24  LOAD_CONST               None
               26  RETURN_VALUE     
               28  END_FINALLY      
             30_0  COME_FROM            14  '14'

 L.1274        30  SETUP_FINALLY        48  'to 48'

 L.1275        32  LOAD_GLOBAL              getsourcelines
               34  LOAD_FAST                'obj'
               36  CALL_FUNCTION_1       1  ''
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'lines'
               42  STORE_FAST               'lineno'
               44  POP_BLOCK        
               46  JUMP_FORWARD        102  'to 102'
             48_0  COME_FROM_FINALLY    30  '30'

 L.1276        48  DUP_TOP          
               50  LOAD_GLOBAL              OSError
               52  LOAD_GLOBAL              TypeError
               54  BUILD_TUPLE_2         2 
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE   100  'to 100'
               60  POP_TOP          
               62  STORE_FAST               'err'
               64  POP_TOP          
               66  SETUP_FINALLY        88  'to 88'

 L.1277        68  LOAD_FAST                'self'
               70  LOAD_METHOD              error
               72  LOAD_FAST                'err'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L.1278        78  POP_BLOCK        
               80  POP_EXCEPT       
               82  CALL_FINALLY         88  'to 88'
               84  LOAD_CONST               None
               86  RETURN_VALUE     
             88_0  COME_FROM            82  '82'
             88_1  COME_FROM_FINALLY    66  '66'
               88  LOAD_CONST               None
               90  STORE_FAST               'err'
               92  DELETE_FAST              'err'
               94  END_FINALLY      
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            58  '58'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            46  '46'

 L.1279       102  LOAD_FAST                'self'
              104  LOAD_METHOD              _print_lines
              106  LOAD_FAST                'lines'
              108  LOAD_FAST                'lineno'
              110  CALL_METHOD_2         2  ''
              112  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 24

    complete_source = _complete_expression

    def _print_lines(self, lines, start, breaks=(), frame=None):
        """Print a range of lines."""
        if frame:
            current_lineno = frame.f_lineno
            exc_lineno = self.tb_lineno.get(frame, -1)
        else:
            current_lineno = exc_lineno = -1
        for lineno, line in enumerate(lines, start):
            s = str(lineno).rjust3
            if len(s) < 4:
                s += ' '
            else:
                if lineno in breaks:
                    s += 'B'
                else:
                    s += ' '
                if lineno == current_lineno:
                    s += '->'
                elif lineno == exc_lineno:
                    s += '>>'
                self.message(s + '\t' + line.rstrip())

    def do_whatis--- This code section failed: ---

 L.1308         0  SETUP_FINALLY        16  'to 16'

 L.1309         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _getval
                6  LOAD_FAST                'arg'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'value'
               12  POP_BLOCK        
               14  JUMP_FORWARD         30  'to 30'
             16_0  COME_FROM_FINALLY     0  '0'

 L.1310        16  POP_TOP          
               18  POP_TOP          
               20  POP_TOP          

 L.1312        22  POP_EXCEPT       
               24  LOAD_CONST               None
               26  RETURN_VALUE     
               28  END_FINALLY      
             30_0  COME_FROM            14  '14'

 L.1313        30  LOAD_CONST               None
               32  STORE_FAST               'code'

 L.1315        34  SETUP_FINALLY        46  'to 46'

 L.1316        36  LOAD_FAST                'value'
               38  LOAD_ATTR                __code__
               40  STORE_FAST               'code'
               42  POP_BLOCK        
               44  JUMP_FORWARD         66  'to 66'
             46_0  COME_FROM_FINALLY    34  '34'

 L.1317        46  DUP_TOP          
               48  LOAD_GLOBAL              Exception
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    64  'to 64'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L.1318        60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            52  '52'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            44  '44'

 L.1319        66  LOAD_FAST                'code'
               68  POP_JUMP_IF_FALSE    90  'to 90'

 L.1320        70  LOAD_FAST                'self'
               72  LOAD_METHOD              message
               74  LOAD_STR                 'Function %s'
               76  LOAD_FAST                'code'
               78  LOAD_ATTR                co_name
               80  BINARY_MODULO    
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          

 L.1321        86  LOAD_CONST               None
               88  RETURN_VALUE     
             90_0  COME_FROM            68  '68'

 L.1323        90  SETUP_FINALLY       104  'to 104'

 L.1324        92  LOAD_FAST                'value'
               94  LOAD_ATTR                __func__
               96  LOAD_ATTR                __code__
               98  STORE_FAST               'code'
              100  POP_BLOCK        
              102  JUMP_FORWARD        124  'to 124'
            104_0  COME_FROM_FINALLY    90  '90'

 L.1325       104  DUP_TOP          
              106  LOAD_GLOBAL              Exception
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   122  'to 122'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L.1326       118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM           110  '110'
              122  END_FINALLY      
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM           102  '102'

 L.1327       124  LOAD_FAST                'code'
              126  POP_JUMP_IF_FALSE   148  'to 148'

 L.1328       128  LOAD_FAST                'self'
              130  LOAD_METHOD              message
              132  LOAD_STR                 'Method %s'
              134  LOAD_FAST                'code'
              136  LOAD_ATTR                co_name
              138  BINARY_MODULO    
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          

 L.1329       144  LOAD_CONST               None
              146  RETURN_VALUE     
            148_0  COME_FROM           126  '126'

 L.1331       148  LOAD_FAST                'value'
              150  LOAD_ATTR                __class__
              152  LOAD_GLOBAL              type
              154  COMPARE_OP               is
              156  POP_JUMP_IF_FALSE   184  'to 184'

 L.1332       158  LOAD_FAST                'self'
              160  LOAD_METHOD              message
              162  LOAD_STR                 'Class %s.%s'
              164  LOAD_FAST                'value'
              166  LOAD_ATTR                __module__
              168  LOAD_FAST                'value'
              170  LOAD_ATTR                __qualname__
              172  BUILD_TUPLE_2         2 
              174  BINARY_MODULO    
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          

 L.1333       180  LOAD_CONST               None
              182  RETURN_VALUE     
            184_0  COME_FROM           156  '156'

 L.1335       184  LOAD_FAST                'self'
              186  LOAD_METHOD              message
              188  LOAD_GLOBAL              type
              190  LOAD_FAST                'value'
              192  CALL_FUNCTION_1       1  ''
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 24

    complete_whatis = _complete_expression

    def do_display(self, arg):
        """display [expression]

        Display the value of the expression if it changed, each time execution
        stops in the current frame.

        Without expression, list all display expressions for the current frame.
        """
        if not arg:
            self.message'Currently displaying:'
            for item in self.displaying.get(self.curframe, {}).items():
                self.message('%s: %r' % item)

        else:
            val = self._getval_exceptarg
            self.displaying.setdefault(self.curframe, {})[arg] = val
            self.message('display %s: %r' % (arg, val))

    complete_display = _complete_expression

    def do_undisplay(self, arg):
        """undisplay [expression]

        Do not display the expression any more in the current frame.

        Without expression, clear all display expressions for the current frame.
        """
        if arg:
            try:
                del self.displaying.get(self.curframe, {})[arg]
            except KeyError:
                self.error('not displaying %s' % arg)

        else:
            self.displaying.pop(self.curframe, None)

    def complete_undisplay(self, text, line, begidx, endidx):
        return [e for e in self.displaying.get(self.curframe, {}) if e.startswithtext]

    def do_interact(self, arg):
        """interact

        Start an interactive interpreter whose global namespace
        contains all the (global and local) names found in the current scope.
        """
        ns = {**(self.curframe.f_globals), **(self.curframe_locals)}
        code.interact('*interactive*', local=ns)

    def do_alias(self, arg):
        """alias [name [command [parameter parameter ...] ]]
        Create an alias called 'name' that executes 'command'.  The
        command must *not* be enclosed in quotes.  Replaceable
        parameters can be indicated by %1, %2, and so on, while %* is
        replaced by all the parameters.  If no command is given, the
        current alias for name is shown. If no name is given, all
        aliases are listed.

        Aliases may be nested and can contain anything that can be
        legally typed at the pdb prompt.  Note!  You *can* override
        internal pdb commands with aliases!  Those internal commands
        are then hidden until the alias is removed.  Aliasing is
        recursively applied to the first word of the command line; all
        other words in the line are left alone.

        As an example, here are two useful aliases (especially when
        placed in the .pdbrc file):

        # Print instance variables (usage "pi classInst")
        alias pi for k in %1.__dict__.keys(): print("%1.",k,"=",%1.__dict__[k])
        # Print instance variables in self
        alias ps pi self
        """
        args = arg.split()
        if len(args) == 0:
            keys = sorted(self.aliases.keys())
            for alias in keys:
                self.message('%s = %s' % (alias, self.aliases[alias]))
            else:
                return

        if args[0] in self.aliases and len(args) == 1:
            self.message('%s = %s' % (args[0], self.aliases[args[0]]))
        else:
            self.aliases[args[0]] = ' '.joinargs[1:]

    def do_unalias(self, arg):
        """unalias name
        Delete the specified alias.
        """
        args = arg.split()
        if len(args) == 0:
            return
        if args[0] in self.aliases:
            del self.aliases[args[0]]

    def complete_unalias(self, text, line, begidx, endidx):
        return [a for a in self.aliases if a.startswithtext]

    commands_resuming = [
     'do_continue', 'do_step', 'do_next', 'do_return',
     'do_quit', 'do_jump']

    def print_stack_trace(self):
        try:
            for frame_lineno in self.stack:
                self.print_stack_entryframe_lineno

        except KeyboardInterrupt:
            pass

    def print_stack_entry(self, frame_lineno, prompt_prefix=line_prefix):
        frame, lineno = frame_lineno
        if frame is self.curframe:
            prefix = '> '
        else:
            prefix = '  '
        self.message(prefix + self.format_stack_entry(frame_lineno, prompt_prefix))

    def do_help--- This code section failed: ---

 L.1470         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_TRUE     18  'to 18'

 L.1471         4  LOAD_GLOBAL              cmd
                6  LOAD_ATTR                Cmd
                8  LOAD_METHOD              do_help
               10  LOAD_FAST                'self'
               12  LOAD_FAST                'arg'
               14  CALL_METHOD_2         2  ''
               16  RETURN_VALUE     
             18_0  COME_FROM             2  '2'

 L.1472        18  SETUP_FINALLY        84  'to 84'

 L.1473        20  SETUP_FINALLY        46  'to 46'

 L.1474        22  LOAD_GLOBAL              getattr
               24  LOAD_FAST                'self'
               26  LOAD_STR                 'help_'
               28  LOAD_FAST                'arg'
               30  BINARY_ADD       
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'topic'

 L.1475        36  LOAD_FAST                'topic'
               38  CALL_FUNCTION_0       0  ''
               40  POP_BLOCK        
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY    20  '20'

 L.1476        46  DUP_TOP          
               48  LOAD_GLOBAL              AttributeError
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    78  'to 78'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L.1477        60  LOAD_GLOBAL              getattr
               62  LOAD_FAST                'self'
               64  LOAD_STR                 'do_'
               66  LOAD_FAST                'arg'
               68  BINARY_ADD       
               70  CALL_FUNCTION_2       2  ''
               72  STORE_FAST               'command'
               74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            52  '52'
               78  END_FINALLY      
             80_0  COME_FROM            76  '76'
               80  POP_BLOCK        
               82  JUMP_FORWARD        118  'to 118'
             84_0  COME_FROM_FINALLY    18  '18'

 L.1478        84  DUP_TOP          
               86  LOAD_GLOBAL              AttributeError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   116  'to 116'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L.1479        98  LOAD_FAST                'self'
              100  LOAD_METHOD              error
              102  LOAD_STR                 'No help for %r'
              104  LOAD_FAST                'arg'
              106  BINARY_MODULO    
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
              112  POP_EXCEPT       
              114  JUMP_FORWARD        164  'to 164'
            116_0  COME_FROM            90  '90'
              116  END_FINALLY      
            118_0  COME_FROM            82  '82'

 L.1481       118  LOAD_GLOBAL              sys
              120  LOAD_ATTR                flags
              122  LOAD_ATTR                optimize
              124  LOAD_CONST               2
              126  COMPARE_OP               >=
              128  POP_JUMP_IF_FALSE   148  'to 148'

 L.1482       130  LOAD_FAST                'self'
              132  LOAD_METHOD              error
              134  LOAD_STR                 'No help for %r; please do not run Python with -OO if you need command help'

 L.1483       136  LOAD_FAST                'arg'

 L.1482       138  BINARY_MODULO    
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          

 L.1484       144  LOAD_CONST               None
              146  RETURN_VALUE     
            148_0  COME_FROM           128  '128'

 L.1485       148  LOAD_FAST                'self'
              150  LOAD_METHOD              message
              152  LOAD_FAST                'command'
              154  LOAD_ATTR                __doc__
              156  LOAD_METHOD              rstrip
              158  CALL_METHOD_0         0  ''
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
            164_0  COME_FROM           114  '114'

Parse error at or near `POP_BLOCK' instruction at offset 42

    do_h = do_help

    def help_exec(self):
        """(!) statement
        Execute the (one-line) statement in the context of the current
        stack frame.  The exclamation point can be omitted unless the
        first word of the statement resembles a debugger command.  To
        assign to a global variable you must always prefix the command
        with a 'global' command, e.g.:
        (Pdb) global list_options; list_options = ['-l']
        (Pdb)
        """
        self.message(self.help_exec.__doc__ or '').strip()

    def help_pdb(self):
        help

    def lookupmodule(self, filename):
        """Helper function for break/clear parsing -- may be overridden.

        lookupmodule() translates (possibly incomplete) file or module name
        into an absolute file name.
        """
        if os.path.isabsfilename:
            if os.path.existsfilename:
                return filename
        f = os.path.join(sys.path[0], filename)
        if os.path.existsf:
            if self.canonicf == self.mainpyfile:
                return f
        root, ext = os.path.splitextfilename
        if ext == '':
            filename = filename + '.py'
        if os.path.isabsfilename:
            return filename
        for dirname in sys.path:
            while True:
                if os.path.islinkdirname:
                    dirname = os.readlinkdirname

            fullname = os.path.join(dirname, filename)
            if os.path.existsfullname:
                return fullname

    def _runmodule(self, module_name):
        self._wait_for_mainpyfile = True
        self._user_requested_quit = False
        import runpy
        mod_name, mod_spec, code = runpy._get_module_detailsmodule_name
        self.mainpyfile = self.canoniccode.co_filename
        import __main__
        __main__.__dict__.clear()
        __main__.__dict__.update{'__name__':'__main__', 
         '__file__':self.mainpyfile, 
         '__package__':mod_spec.parent, 
         '__loader__':mod_spec.loader, 
         '__spec__':mod_spec, 
         '__builtins__':__builtins__}
        self.runcode

    def _runscript(self, filename):
        import __main__
        __main__.__dict__.clear()
        __main__.__dict__.update{'__name__':'__main__',  '__file__':filename, 
         '__builtins__':__builtins__}
        self._wait_for_mainpyfile = True
        self.mainpyfile = self.canonicfilename
        self._user_requested_quit = False
        with io.open_codefilename as fp:
            statement = "exec(compile(%r, %r, 'exec'))" % (
             fp.read(), self.mainpyfile)
        self.runstatement


if __doc__ is not None:
    _help_order = [
     'help', 'where', 'down', 'up', 'break', 'tbreak', 'clear', 'disable',
     'enable', 'ignore', 'condition', 'commands', 'step', 'next', 'until',
     'jump', 'return', 'retval', 'run', 'continue', 'list', 'longlist',
     'args', 'p', 'pp', 'whatis', 'source', 'display', 'undisplay',
     'interact', 'alias', 'unalias', 'debug', 'quit']
    for _command in _help_order:
        __doc__ += getattr(Pdb, 'do_' + _command).__doc__.strip() + '\n\n'
    else:
        __doc__ += Pdb.help_exec.__doc__
        del _help_order
        del _command

def run(statement, globals=None, locals=None):
    Pdb.run(statement, globals, locals)


def runeval(expression, globals=None, locals=None):
    return Pdb.runeval(expression, globals, locals)


def runctx(statement, globals, locals):
    run(statement, globals, locals)


def runcall(*args, **kwds):
    return (Pdb.runcall)(*args, **kwds)


def set_trace(*, header=None):
    pdb = Pdb
    if header is not None:
        pdb.messageheader
    pdb.set_tracesys._getframe().f_back


def post_mortem(t=None):
    if t is None:
        t = sys.exc_info()[2]
    if t is None:
        raise ValueError('A valid traceback must be passed if no exception is being handled')
    p = Pdb
    p.reset()
    p.interaction(None, t)


def pm():
    post_mortem(sys.last_traceback)


TESTCMD = 'import x; x.main()'

def test():
    run(TESTCMD)


def help():
    import pydoc
    pydoc.pager__doc__


_usage = 'usage: pdb.py [-c command] ... [-m module | pyfile] [arg] ...\n\nDebug the Python program given by pyfile. Alternatively,\nan executable module or package to debug can be specified using\nthe -m switch.\n\nInitial commands are read from .pdbrc files in your home directory\nand in the current directory, if they exist.  Commands supplied with\n-c are executed after commands from .pdbrc files.\n\nTo let the script run until an exception occurs, use "-c continue".\nTo let the script run up to a given line X in the debugged file, use\n"-c \'until X\'".'

def main--- This code section failed: ---

 L.1662         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              getopt
                6  STORE_FAST               'getopt'

 L.1664         8  LOAD_FAST                'getopt'
               10  LOAD_METHOD              getopt
               12  LOAD_GLOBAL              sys
               14  LOAD_ATTR                argv
               16  LOAD_CONST               1
               18  LOAD_CONST               None
               20  BUILD_SLICE_2         2 
               22  BINARY_SUBSCR    
               24  LOAD_STR                 'mhc:'
               26  LOAD_STR                 'help'
               28  LOAD_STR                 'command='
               30  BUILD_LIST_2          2 
               32  CALL_METHOD_3         3  ''
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'opts'
               38  STORE_FAST               'args'

 L.1666        40  LOAD_FAST                'args'
               42  POP_JUMP_IF_TRUE     62  'to 62'

 L.1667        44  LOAD_GLOBAL              print
               46  LOAD_GLOBAL              _usage
               48  CALL_FUNCTION_1       1  ''
               50  POP_TOP          

 L.1668        52  LOAD_GLOBAL              sys
               54  LOAD_METHOD              exit
               56  LOAD_CONST               2
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
             62_0  COME_FROM            42  '42'

 L.1670        62  BUILD_LIST_0          0 
               64  STORE_FAST               'commands'

 L.1671        66  LOAD_CONST               False
               68  STORE_FAST               'run_as_module'

 L.1672        70  LOAD_FAST                'opts'
               72  GET_ITER         
             74_0  COME_FROM           140  '140'
             74_1  COME_FROM           134  '134'
             74_2  COME_FROM           126  '126'
             74_3  COME_FROM           106  '106'
               74  FOR_ITER            142  'to 142'
               76  UNPACK_SEQUENCE_2     2 
               78  STORE_FAST               'opt'
               80  STORE_FAST               'optarg'

 L.1673        82  LOAD_FAST                'opt'
               84  LOAD_CONST               ('-h', '--help')
               86  COMPARE_OP               in
               88  POP_JUMP_IF_FALSE   108  'to 108'

 L.1674        90  LOAD_GLOBAL              print
               92  LOAD_GLOBAL              _usage
               94  CALL_FUNCTION_1       1  ''
               96  POP_TOP          

 L.1675        98  LOAD_GLOBAL              sys
              100  LOAD_METHOD              exit
              102  CALL_METHOD_0         0  ''
              104  POP_TOP          
              106  JUMP_BACK            74  'to 74'
            108_0  COME_FROM            88  '88'

 L.1676       108  LOAD_FAST                'opt'
              110  LOAD_CONST               ('-c', '--command')
              112  COMPARE_OP               in
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L.1677       116  LOAD_FAST                'commands'
              118  LOAD_METHOD              append
              120  LOAD_FAST                'optarg'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
              126  JUMP_BACK            74  'to 74'
            128_0  COME_FROM           114  '114'

 L.1678       128  LOAD_FAST                'opt'
              130  LOAD_CONST               ('-m',)
              132  COMPARE_OP               in
              134  POP_JUMP_IF_FALSE_BACK    74  'to 74'

 L.1679       136  LOAD_CONST               True
              138  STORE_FAST               'run_as_module'
              140  JUMP_BACK            74  'to 74'
            142_0  COME_FROM            74  '74'

 L.1681       142  LOAD_FAST                'args'
              144  LOAD_CONST               0
              146  BINARY_SUBSCR    
              148  STORE_FAST               'mainpyfile'

 L.1682       150  LOAD_FAST                'run_as_module'
              152  POP_JUMP_IF_TRUE    188  'to 188'
              154  LOAD_GLOBAL              os
              156  LOAD_ATTR                path
              158  LOAD_METHOD              exists
              160  LOAD_FAST                'mainpyfile'
              162  CALL_METHOD_1         1  ''
              164  POP_JUMP_IF_TRUE    188  'to 188'

 L.1683       166  LOAD_GLOBAL              print
              168  LOAD_STR                 'Error:'
              170  LOAD_FAST                'mainpyfile'
              172  LOAD_STR                 'does not exist'
              174  CALL_FUNCTION_3       3  ''
              176  POP_TOP          

 L.1684       178  LOAD_GLOBAL              sys
              180  LOAD_METHOD              exit
              182  LOAD_CONST               1
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
            188_0  COME_FROM           164  '164'
            188_1  COME_FROM           152  '152'

 L.1686       188  LOAD_FAST                'args'
              190  LOAD_GLOBAL              sys
              192  LOAD_ATTR                argv
              194  LOAD_CONST               None
              196  LOAD_CONST               None
              198  BUILD_SLICE_2         2 
              200  STORE_SUBSCR     

 L.1689       202  LOAD_FAST                'run_as_module'
              204  POP_JUMP_IF_TRUE    224  'to 224'

 L.1690       206  LOAD_GLOBAL              os
              208  LOAD_ATTR                path
              210  LOAD_METHOD              dirname
              212  LOAD_FAST                'mainpyfile'
              214  CALL_METHOD_1         1  ''
              216  LOAD_GLOBAL              sys
              218  LOAD_ATTR                path
              220  LOAD_CONST               0
              222  STORE_SUBSCR     
            224_0  COME_FROM           204  '204'

 L.1696       224  LOAD_GLOBAL              Pdb
              226  CALL_FUNCTION_0       0  ''
              228  STORE_FAST               'pdb'

 L.1697       230  LOAD_FAST                'pdb'
              232  LOAD_ATTR                rcLines
              234  LOAD_METHOD              extend
              236  LOAD_FAST                'commands'
              238  CALL_METHOD_1         1  ''
              240  POP_TOP          
            242_0  COME_FROM           510  '510'
            242_1  COME_FROM           506  '506'
            242_2  COME_FROM           432  '432'
            242_3  COME_FROM           394  '394'
            242_4  COME_FROM           346  '346'
            242_5  COME_FROM           296  '296'

 L.1699       242  SETUP_FINALLY       298  'to 298'

 L.1700       244  LOAD_FAST                'run_as_module'
          246_248  POP_JUMP_IF_FALSE   262  'to 262'

 L.1701       250  LOAD_FAST                'pdb'
              252  LOAD_METHOD              _runmodule
              254  LOAD_FAST                'mainpyfile'
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          
              260  JUMP_FORWARD        272  'to 272'
            262_0  COME_FROM           246  '246'

 L.1703       262  LOAD_FAST                'pdb'
              264  LOAD_METHOD              _runscript
              266  LOAD_FAST                'mainpyfile'
              268  CALL_METHOD_1         1  ''
              270  POP_TOP          
            272_0  COME_FROM           260  '260'

 L.1704       272  LOAD_FAST                'pdb'
              274  LOAD_ATTR                _user_requested_quit
          276_278  POP_JUMP_IF_FALSE   286  'to 286'

 L.1705       280  POP_BLOCK        
          282_284  BREAK_LOOP          512  'to 512'
            286_0  COME_FROM           276  '276'

 L.1706       286  LOAD_GLOBAL              print
              288  LOAD_STR                 'The program finished and will be restarted'
              290  CALL_FUNCTION_1       1  ''
              292  POP_TOP          
              294  POP_BLOCK        
              296  JUMP_BACK           242  'to 242'
            298_0  COME_FROM_FINALLY   242  '242'

 L.1707       298  DUP_TOP          
              300  LOAD_GLOBAL              Restart
              302  COMPARE_OP               exception-match
          304_306  POP_JUMP_IF_FALSE   348  'to 348'
              308  POP_TOP          
              310  POP_TOP          
              312  POP_TOP          

 L.1708       314  LOAD_GLOBAL              print
              316  LOAD_STR                 'Restarting'
              318  LOAD_FAST                'mainpyfile'
              320  LOAD_STR                 'with arguments:'
              322  CALL_FUNCTION_3       3  ''
              324  POP_TOP          

 L.1709       326  LOAD_GLOBAL              print
              328  LOAD_STR                 '\t'
              330  LOAD_STR                 ' '
              332  LOAD_METHOD              join
              334  LOAD_FAST                'args'
              336  CALL_METHOD_1         1  ''
              338  BINARY_ADD       
              340  CALL_FUNCTION_1       1  ''
              342  POP_TOP          
              344  POP_EXCEPT       
              346  JUMP_BACK           242  'to 242'
            348_0  COME_FROM           304  '304'

 L.1710       348  DUP_TOP          
              350  LOAD_GLOBAL              SystemExit
              352  COMPARE_OP               exception-match
          354_356  POP_JUMP_IF_FALSE   396  'to 396'
              358  POP_TOP          
              360  POP_TOP          
              362  POP_TOP          

 L.1712       364  LOAD_GLOBAL              print
              366  LOAD_STR                 'The program exited via sys.exit(). Exit status:'
              368  LOAD_STR                 ' '
              370  LOAD_CONST               ('end',)
              372  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              374  POP_TOP          

 L.1713       376  LOAD_GLOBAL              print
              378  LOAD_GLOBAL              sys
              380  LOAD_METHOD              exc_info
              382  CALL_METHOD_0         0  ''
              384  LOAD_CONST               1
              386  BINARY_SUBSCR    
              388  CALL_FUNCTION_1       1  ''
              390  POP_TOP          
              392  POP_EXCEPT       
              394  JUMP_BACK           242  'to 242'
            396_0  COME_FROM           354  '354'

 L.1714       396  DUP_TOP          
              398  LOAD_GLOBAL              SyntaxError
              400  COMPARE_OP               exception-match
          402_404  POP_JUMP_IF_FALSE   434  'to 434'
              406  POP_TOP          
              408  POP_TOP          
              410  POP_TOP          

 L.1715       412  LOAD_GLOBAL              traceback
              414  LOAD_METHOD              print_exc
              416  CALL_METHOD_0         0  ''
              418  POP_TOP          

 L.1716       420  LOAD_GLOBAL              sys
              422  LOAD_METHOD              exit
              424  LOAD_CONST               1
              426  CALL_METHOD_1         1  ''
              428  POP_TOP          
              430  POP_EXCEPT       
              432  JUMP_BACK           242  'to 242'
            434_0  COME_FROM           402  '402'

 L.1717       434  POP_TOP          
              436  POP_TOP          
              438  POP_TOP          

 L.1718       440  LOAD_GLOBAL              traceback
              442  LOAD_METHOD              print_exc
              444  CALL_METHOD_0         0  ''
              446  POP_TOP          

 L.1719       448  LOAD_GLOBAL              print
              450  LOAD_STR                 'Uncaught exception. Entering post mortem debugging'
              452  CALL_FUNCTION_1       1  ''
              454  POP_TOP          

 L.1720       456  LOAD_GLOBAL              print
              458  LOAD_STR                 "Running 'cont' or 'step' will restart the program"
              460  CALL_FUNCTION_1       1  ''
              462  POP_TOP          

 L.1721       464  LOAD_GLOBAL              sys
              466  LOAD_METHOD              exc_info
              468  CALL_METHOD_0         0  ''
              470  LOAD_CONST               2
              472  BINARY_SUBSCR    
              474  STORE_FAST               't'

 L.1722       476  LOAD_FAST                'pdb'
              478  LOAD_METHOD              interaction
              480  LOAD_CONST               None
              482  LOAD_FAST                't'
              484  CALL_METHOD_2         2  ''
              486  POP_TOP          

 L.1723       488  LOAD_GLOBAL              print
              490  LOAD_STR                 'Post mortem debugger finished. The '
              492  LOAD_FAST                'mainpyfile'
              494  BINARY_ADD       

 L.1724       496  LOAD_STR                 ' will be restarted'

 L.1723       498  BINARY_ADD       
              500  CALL_FUNCTION_1       1  ''
              502  POP_TOP          
              504  POP_EXCEPT       
              506  JUMP_BACK           242  'to 242'
              508  END_FINALLY      
              510  JUMP_BACK           242  'to 242'
            512_0  COME_FROM           282  '282'

Parse error at or near `JUMP_BACK' instruction at offset 506


if __name__ == '__main__':
    import pdb
    pdb.main()