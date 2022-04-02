# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
import os, io, re, sys, cmd, bdb, dis, code, glob, pprint, signal, inspect, tokenize, traceback, linecache

class Restart(Exception):
    __doc__ = 'Causes a debugger to be restarted for the debugged python program.'


__all__ = [
 'run', 'pm', 'Pdb', 'runeval', 'runctx', 'runcall', 'set_trace',
 'post_mortem', 'help']

def find_function--- This code section failed: ---

 L.  95         0  LOAD_GLOBAL              re
                2  LOAD_METHOD              compile
                4  LOAD_STR                 'def\\s+%s\\s*[(]'
                6  LOAD_GLOBAL              re
                8  LOAD_METHOD              escape
               10  LOAD_FAST                'funcname'
               12  CALL_METHOD_1         1  ''
               14  BINARY_MODULO    
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'cre'

 L.  96        20  SETUP_FINALLY        36  'to 36'

 L.  97        22  LOAD_GLOBAL              tokenize
               24  LOAD_METHOD              open
               26  LOAD_FAST                'filename'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'fp'
               32  POP_BLOCK        
               34  JUMP_FORWARD         58  'to 58'
             36_0  COME_FROM_FINALLY    20  '20'

 L.  98        36  DUP_TOP          
               38  LOAD_GLOBAL              OSError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    56  'to 56'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L.  99        50  POP_EXCEPT       
               52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            42  '42'
               56  END_FINALLY      
             58_0  COME_FROM            34  '34'

 L. 101        58  LOAD_FAST                'fp'
               60  SETUP_WITH          126  'to 126'
               62  POP_TOP          

 L. 102        64  LOAD_GLOBAL              enumerate
               66  LOAD_FAST                'fp'
               68  LOAD_CONST               1
               70  LOAD_CONST               ('start',)
               72  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               74  GET_ITER         
             76_0  COME_FROM            92  '92'
               76  FOR_ITER            122  'to 122'
               78  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST               'lineno'
               82  STORE_FAST               'line'

 L. 103        84  LOAD_FAST                'cre'
               86  LOAD_METHOD              match
               88  LOAD_FAST                'line'
               90  CALL_METHOD_1         1  ''
               92  POP_JUMP_IF_FALSE    76  'to 76'

 L. 104        94  LOAD_FAST                'funcname'
               96  LOAD_FAST                'filename'
               98  LOAD_FAST                'lineno'
              100  BUILD_TUPLE_3         3 
              102  ROT_TWO          
              104  POP_TOP          
              106  POP_BLOCK        
              108  ROT_TWO          
              110  BEGIN_FINALLY    
              112  WITH_CLEANUP_START
              114  WITH_CLEANUP_FINISH
              116  POP_FINALLY           0  ''
              118  RETURN_VALUE     
              120  JUMP_BACK            76  'to 76'
              122  POP_BLOCK        
              124  BEGIN_FINALLY    
            126_0  COME_FROM_WITH       60  '60'
              126  WITH_CLEANUP_START
              128  WITH_CLEANUP_FINISH
              130  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 106


def getsourcelines(obj):
    lines, lineno = inspect.findsourceobj
    if inspect.isframeobj:
        if obj.f_globals is obj.f_locals:
            return (
             lines, 1)
    if inspect.ismoduleobj:
        return (
         lines, 1)
    return (
     inspect.getblocklines[lineno:], lineno + 1)


def lasti2lineno(code, lasti):
    linestarts = list(dis.findlinestartscode)
    linestarts.reverse()
    for i, lineno in linestarts:
        if lasti >= i:
            return lineno
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
                    with open(os.path.expanduser'~/.pdbrc') as (rcFile):
                        self.rcLines.extendrcFile
                except OSError:
                    pass

                try:
                    with open('.pdbrc') as (rcFile):
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
        while tb:
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
        else:
            while True:
                if rcLines:
                    line = rcLines.pop().strip()
                    if line and line[0] != '#' and self.onecmdline:
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
            if self.mainpyfile != self.canonicframe.f_code.co_filename or frame.f_lineno <= 0:
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
                    return None

        return 1

    def user_return(self, frame, return_value):
        """This function is called when a return trap is set here."""
        if self._wait_for_mainpyfile:
            return
        frame.f_locals['__return__'] = return_value
        self.message'--Return--'
        self.interaction(frame, None)

    def user_exception--- This code section failed: ---

 L. 299         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _wait_for_mainpyfile
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 300         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 301        10  LOAD_FAST                'exc_info'
               12  UNPACK_SEQUENCE_3     3 
               14  STORE_FAST               'exc_type'
               16  STORE_FAST               'exc_value'
               18  STORE_FAST               'exc_traceback'

 L. 302        20  LOAD_FAST                'exc_type'
               22  LOAD_FAST                'exc_value'
               24  BUILD_TUPLE_2         2 
               26  LOAD_FAST                'frame'
               28  LOAD_ATTR                f_locals
               30  LOAD_STR                 '__exception__'
               32  STORE_SUBSCR     

 L. 309        34  LOAD_FAST                'exc_traceback'
               36  POP_JUMP_IF_TRUE     50  'to 50'

 L. 310        38  LOAD_FAST                'exc_type'
               40  LOAD_GLOBAL              StopIteration
               42  COMPARE_OP               is

 L. 309        44  POP_JUMP_IF_FALSE    50  'to 50'
               46  LOAD_STR                 'Internal '
               48  JUMP_FORWARD         52  'to 52'
             50_0  COME_FROM            44  '44'
             50_1  COME_FROM            36  '36'

 L. 310        50  LOAD_STR                 ''
             52_0  COME_FROM            48  '48'

 L. 309        52  STORE_FAST               'prefix'

 L. 311        54  LOAD_FAST                'self'
               56  LOAD_METHOD              message
               58  LOAD_STR                 '%s%s'
               60  LOAD_FAST                'prefix'

 L. 312        62  LOAD_GLOBAL              traceback
               64  LOAD_METHOD              format_exception_only
               66  LOAD_FAST                'exc_type'
               68  LOAD_FAST                'exc_value'
               70  CALL_METHOD_2         2  ''
               72  LOAD_CONST               -1
               74  BINARY_SUBSCR    
               76  LOAD_METHOD              strip
               78  CALL_METHOD_0         0  ''

 L. 311        80  BUILD_TUPLE_2         2 
               82  BINARY_MODULO    
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L. 313        88  LOAD_FAST                'self'
               90  LOAD_METHOD              interaction
               92  LOAD_FAST                'frame'
               94  LOAD_FAST                'exc_traceback'
               96  CALL_METHOD_2         2  ''
               98  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 50_1

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
                if newvalue is not oldvalue and newvalue != oldvalue:
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
            return None
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
        else:
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
        elif cmd == 'silent':
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
            globs = glob.glob(glob.escapetext + '*')
            for fn in globs:
                if os.path.isdirfn:
                    ret.append(fn + '/')
                else:
                    if os.path.isfilefn and fn.lower().endswith('.py', '.pyw'):
                        ret.append(fn + ':')
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

 L. 558         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_TRUE     22  'to 22'

 L. 559         4  LOAD_GLOBAL              len
                6  LOAD_GLOBAL              bdb
                8  LOAD_ATTR                Breakpoint
               10  LOAD_ATTR                bpbynumber
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_CONST               1
               16  BINARY_SUBTRACT  
               18  STORE_FAST               'bnum'
               20  JUMP_FORWARD         60  'to 60'
             22_0  COME_FROM             2  '2'

 L. 561        22  SETUP_FINALLY        36  'to 36'

 L. 562        24  LOAD_GLOBAL              int
               26  LOAD_FAST                'arg'
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'bnum'
               32  POP_BLOCK        
               34  JUMP_FORWARD         60  'to 60'
             36_0  COME_FROM_FINALLY    22  '22'

 L. 563        36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 564        42  LOAD_FAST                'self'
               44  LOAD_METHOD              error
               46  LOAD_STR                 'Usage: commands [bnum]\n        ...\n        end'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L. 565        52  POP_EXCEPT       
               54  LOAD_CONST               None
               56  RETURN_VALUE     
               58  END_FINALLY      
             60_0  COME_FROM            34  '34'
             60_1  COME_FROM            20  '20'

 L. 566        60  LOAD_FAST                'bnum'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               commands_bnum

 L. 568        66  LOAD_FAST                'bnum'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                commands
               72  COMPARE_OP               in
               74  POP_JUMP_IF_FALSE   106  'to 106'

 L. 569        76  LOAD_FAST                'self'
               78  LOAD_ATTR                commands
               80  LOAD_FAST                'bnum'
               82  BINARY_SUBSCR    

 L. 570        84  LOAD_FAST                'self'
               86  LOAD_ATTR                commands_doprompt
               88  LOAD_FAST                'bnum'
               90  BINARY_SUBSCR    

 L. 571        92  LOAD_FAST                'self'
               94  LOAD_ATTR                commands_silent
               96  LOAD_FAST                'bnum'
               98  BINARY_SUBSCR    

 L. 569       100  BUILD_TUPLE_3         3 
              102  STORE_FAST               'old_command_defs'
              104  JUMP_FORWARD        110  'to 110'
            106_0  COME_FROM            74  '74'

 L. 573       106  LOAD_CONST               None
              108  STORE_FAST               'old_command_defs'
            110_0  COME_FROM           104  '104'

 L. 574       110  BUILD_LIST_0          0 
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                commands
              116  LOAD_FAST                'bnum'
              118  STORE_SUBSCR     

 L. 575       120  LOAD_CONST               True
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                commands_doprompt
              126  LOAD_FAST                'bnum'
              128  STORE_SUBSCR     

 L. 576       130  LOAD_CONST               False
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                commands_silent
              136  LOAD_FAST                'bnum'
              138  STORE_SUBSCR     

 L. 578       140  LOAD_FAST                'self'
              142  LOAD_ATTR                prompt
              144  STORE_FAST               'prompt_back'

 L. 579       146  LOAD_STR                 '(com) '
              148  LOAD_FAST                'self'
              150  STORE_ATTR               prompt

 L. 580       152  LOAD_CONST               True
              154  LOAD_FAST                'self'
              156  STORE_ATTR               commands_defining

 L. 581       158  SETUP_FINALLY       282  'to 282'
              160  SETUP_FINALLY       174  'to 174'

 L. 582       162  LOAD_FAST                'self'
              164  LOAD_METHOD              cmdloop
              166  CALL_METHOD_0         0  ''
              168  POP_TOP          
              170  POP_BLOCK        
              172  JUMP_FORWARD        278  'to 278'
            174_0  COME_FROM_FINALLY   160  '160'

 L. 583       174  DUP_TOP          
              176  LOAD_GLOBAL              KeyboardInterrupt
              178  COMPARE_OP               exception-match
          180_182  POP_JUMP_IF_FALSE   276  'to 276'
              184  POP_TOP          
              186  POP_TOP          
              188  POP_TOP          

 L. 585       190  LOAD_FAST                'old_command_defs'
              192  POP_JUMP_IF_FALSE   238  'to 238'

 L. 586       194  LOAD_FAST                'old_command_defs'
              196  LOAD_CONST               0
              198  BINARY_SUBSCR    
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                commands
              204  LOAD_FAST                'bnum'
              206  STORE_SUBSCR     

 L. 587       208  LOAD_FAST                'old_command_defs'
              210  LOAD_CONST               1
              212  BINARY_SUBSCR    
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                commands_doprompt
              218  LOAD_FAST                'bnum'
              220  STORE_SUBSCR     

 L. 588       222  LOAD_FAST                'old_command_defs'
              224  LOAD_CONST               2
              226  BINARY_SUBSCR    
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                commands_silent
              232  LOAD_FAST                'bnum'
              234  STORE_SUBSCR     
              236  JUMP_FORWARD        262  'to 262'
            238_0  COME_FROM           192  '192'

 L. 590       238  LOAD_FAST                'self'
              240  LOAD_ATTR                commands
              242  LOAD_FAST                'bnum'
              244  DELETE_SUBSCR    

 L. 591       246  LOAD_FAST                'self'
              248  LOAD_ATTR                commands_doprompt
              250  LOAD_FAST                'bnum'
              252  DELETE_SUBSCR    

 L. 592       254  LOAD_FAST                'self'
              256  LOAD_ATTR                commands_silent
              258  LOAD_FAST                'bnum'
              260  DELETE_SUBSCR    
            262_0  COME_FROM           236  '236'

 L. 593       262  LOAD_FAST                'self'
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

 L. 595       282  LOAD_CONST               False
              284  LOAD_FAST                'self'
              286  STORE_ATTR               commands_defining

 L. 596       288  LOAD_FAST                'prompt_back'
              290  LOAD_FAST                'self'
              292  STORE_ATTR               prompt
              294  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 54

    complete_commands = _complete_bpnumber

    def do_break--- This code section failed: ---

 L. 615         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_TRUE     56  'to 56'

 L. 616         4  LOAD_FAST                'self'
                6  LOAD_ATTR                breaks
                8  POP_JUMP_IF_FALSE    52  'to 52'

 L. 617        10  LOAD_FAST                'self'
               12  LOAD_METHOD              message
               14  LOAD_STR                 'Num Type         Disp Enb   Where'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L. 618        20  LOAD_GLOBAL              bdb
               22  LOAD_ATTR                Breakpoint
               24  LOAD_ATTR                bpbynumber
               26  GET_ITER         
             28_0  COME_FROM            34  '34'
               28  FOR_ITER             52  'to 52'
               30  STORE_FAST               'bp'

 L. 619        32  LOAD_FAST                'bp'
               34  POP_JUMP_IF_FALSE    28  'to 28'

 L. 620        36  LOAD_FAST                'self'
               38  LOAD_METHOD              message
               40  LOAD_FAST                'bp'
               42  LOAD_METHOD              bpformat
               44  CALL_METHOD_0         0  ''
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
               50  JUMP_BACK            28  'to 28'
             52_0  COME_FROM             8  '8'

 L. 621        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM             2  '2'

 L. 624        56  LOAD_CONST               None
               58  STORE_FAST               'filename'

 L. 625        60  LOAD_CONST               None
               62  STORE_FAST               'lineno'

 L. 626        64  LOAD_CONST               None
               66  STORE_FAST               'cond'

 L. 627        68  LOAD_FAST                'arg'
               70  LOAD_METHOD              find
               72  LOAD_STR                 ','
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'comma'

 L. 628        78  LOAD_FAST                'comma'
               80  LOAD_CONST               0
               82  COMPARE_OP               >
               84  POP_JUMP_IF_FALSE   122  'to 122'

 L. 630        86  LOAD_FAST                'arg'
               88  LOAD_FAST                'comma'
               90  LOAD_CONST               1
               92  BINARY_ADD       
               94  LOAD_CONST               None
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  LOAD_METHOD              lstrip
              102  CALL_METHOD_0         0  ''
              104  STORE_FAST               'cond'

 L. 631       106  LOAD_FAST                'arg'
              108  LOAD_CONST               None
              110  LOAD_FAST                'comma'
              112  BUILD_SLICE_2         2 
              114  BINARY_SUBSCR    
              116  LOAD_METHOD              rstrip
              118  CALL_METHOD_0         0  ''
              120  STORE_FAST               'arg'
            122_0  COME_FROM            84  '84'

 L. 633       122  LOAD_FAST                'arg'
              124  LOAD_METHOD              rfind
              126  LOAD_STR                 ':'
              128  CALL_METHOD_1         1  ''
              130  STORE_FAST               'colon'

 L. 634       132  LOAD_CONST               None
              134  STORE_FAST               'funcname'

 L. 635       136  LOAD_FAST                'colon'
              138  LOAD_CONST               0
              140  COMPARE_OP               >=
          142_144  POP_JUMP_IF_FALSE   272  'to 272'

 L. 636       146  LOAD_FAST                'arg'
              148  LOAD_CONST               None
              150  LOAD_FAST                'colon'
              152  BUILD_SLICE_2         2 
              154  BINARY_SUBSCR    
              156  LOAD_METHOD              rstrip
              158  CALL_METHOD_0         0  ''
              160  STORE_FAST               'filename'

 L. 637       162  LOAD_FAST                'self'
              164  LOAD_METHOD              lookupmodule
              166  LOAD_FAST                'filename'
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'f'

 L. 638       172  LOAD_FAST                'f'
              174  POP_JUMP_IF_TRUE    194  'to 194'

 L. 639       176  LOAD_FAST                'self'
              178  LOAD_METHOD              error
              180  LOAD_STR                 '%r not found from sys.path'
              182  LOAD_FAST                'filename'
              184  BINARY_MODULO    
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L. 640       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           174  '174'

 L. 642       194  LOAD_FAST                'f'
              196  STORE_FAST               'filename'

 L. 643       198  LOAD_FAST                'arg'
              200  LOAD_FAST                'colon'
              202  LOAD_CONST               1
              204  BINARY_ADD       
              206  LOAD_CONST               None
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  LOAD_METHOD              lstrip
              214  CALL_METHOD_0         0  ''
              216  STORE_FAST               'arg'

 L. 644       218  SETUP_FINALLY       232  'to 232'

 L. 645       220  LOAD_GLOBAL              int
              222  LOAD_FAST                'arg'
              224  CALL_FUNCTION_1       1  ''
              226  STORE_FAST               'lineno'
              228  POP_BLOCK        
              230  JUMP_FORWARD        270  'to 270'
            232_0  COME_FROM_FINALLY   218  '218'

 L. 646       232  DUP_TOP          
              234  LOAD_GLOBAL              ValueError
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   268  'to 268'
              242  POP_TOP          
              244  POP_TOP          
              246  POP_TOP          

 L. 647       248  LOAD_FAST                'self'
              250  LOAD_METHOD              error
              252  LOAD_STR                 'Bad lineno: %s'
              254  LOAD_FAST                'arg'
              256  BINARY_MODULO    
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          

 L. 648       262  POP_EXCEPT       
              264  LOAD_CONST               None
              266  RETURN_VALUE     
            268_0  COME_FROM           238  '238'
              268  END_FINALLY      
            270_0  COME_FROM           230  '230'
              270  JUMP_FORWARD        464  'to 464'
            272_0  COME_FROM           142  '142'

 L. 651       272  SETUP_FINALLY       286  'to 286'

 L. 652       274  LOAD_GLOBAL              int
              276  LOAD_FAST                'arg'
              278  CALL_FUNCTION_1       1  ''
              280  STORE_FAST               'lineno'
              282  POP_BLOCK        
              284  JUMP_FORWARD        464  'to 464'
            286_0  COME_FROM_FINALLY   272  '272'

 L. 653       286  DUP_TOP          
              288  LOAD_GLOBAL              ValueError
              290  COMPARE_OP               exception-match
          292_294  POP_JUMP_IF_FALSE   462  'to 462'
              296  POP_TOP          
              298  POP_TOP          
              300  POP_TOP          

 L. 654       302  SETUP_FINALLY       326  'to 326'

 L. 655       304  LOAD_GLOBAL              eval
              306  LOAD_FAST                'arg'

 L. 656       308  LOAD_FAST                'self'
              310  LOAD_ATTR                curframe
              312  LOAD_ATTR                f_globals

 L. 657       314  LOAD_FAST                'self'
              316  LOAD_ATTR                curframe_locals

 L. 655       318  CALL_FUNCTION_3       3  ''
              320  STORE_FAST               'func'
              322  POP_BLOCK        
              324  JUMP_FORWARD        342  'to 342'
            326_0  COME_FROM_FINALLY   302  '302'

 L. 658       326  POP_TOP          
              328  POP_TOP          
              330  POP_TOP          

 L. 659       332  LOAD_FAST                'arg'
              334  STORE_FAST               'func'
              336  POP_EXCEPT       
              338  JUMP_FORWARD        342  'to 342'
              340  END_FINALLY      
            342_0  COME_FROM           338  '338'
            342_1  COME_FROM           324  '324'

 L. 660       342  SETUP_FINALLY       390  'to 390'

 L. 661       344  LOAD_GLOBAL              hasattr
              346  LOAD_FAST                'func'
              348  LOAD_STR                 '__func__'
              350  CALL_FUNCTION_2       2  ''
          352_354  POP_JUMP_IF_FALSE   362  'to 362'

 L. 662       356  LOAD_FAST                'func'
              358  LOAD_ATTR                __func__
              360  STORE_FAST               'func'
            362_0  COME_FROM           352  '352'

 L. 663       362  LOAD_FAST                'func'
              364  LOAD_ATTR                __code__
              366  STORE_FAST               'code'

 L. 666       368  LOAD_FAST                'code'
              370  LOAD_ATTR                co_name
              372  STORE_FAST               'funcname'

 L. 667       374  LOAD_FAST                'code'
              376  LOAD_ATTR                co_firstlineno
              378  STORE_FAST               'lineno'

 L. 668       380  LOAD_FAST                'code'
              382  LOAD_ATTR                co_filename
              384  STORE_FAST               'filename'
              386  POP_BLOCK        
              388  JUMP_FORWARD        458  'to 458'
            390_0  COME_FROM_FINALLY   342  '342'

 L. 669       390  POP_TOP          
              392  POP_TOP          
              394  POP_TOP          

 L. 671       396  LOAD_FAST                'self'
              398  LOAD_METHOD              lineinfo
              400  LOAD_FAST                'arg'
              402  CALL_METHOD_1         1  ''
              404  UNPACK_SEQUENCE_3     3 
              406  STORE_FAST               'ok'
              408  STORE_FAST               'filename'
              410  STORE_FAST               'ln'

 L. 672       412  LOAD_FAST                'ok'
          414_416  POP_JUMP_IF_TRUE    440  'to 440'

 L. 673       418  LOAD_FAST                'self'
              420  LOAD_METHOD              error
              422  LOAD_STR                 'The specified object %r is not a function or was not found along sys.path.'

 L. 674       424  LOAD_FAST                'arg'

 L. 673       426  BINARY_MODULO    
              428  CALL_METHOD_1         1  ''
              430  POP_TOP          

 L. 675       432  POP_EXCEPT       
              434  POP_EXCEPT       
              436  LOAD_CONST               None
              438  RETURN_VALUE     
            440_0  COME_FROM           414  '414'

 L. 676       440  LOAD_FAST                'ok'
              442  STORE_FAST               'funcname'

 L. 677       444  LOAD_GLOBAL              int
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

 L. 678       464  LOAD_FAST                'filename'
          466_468  POP_JUMP_IF_TRUE    478  'to 478'

 L. 679       470  LOAD_FAST                'self'
              472  LOAD_METHOD              defaultFile
              474  CALL_METHOD_0         0  ''
              476  STORE_FAST               'filename'
            478_0  COME_FROM           466  '466'

 L. 681       478  LOAD_FAST                'self'
              480  LOAD_METHOD              checkline
              482  LOAD_FAST                'filename'
              484  LOAD_FAST                'lineno'
              486  CALL_METHOD_2         2  ''
              488  STORE_FAST               'line'

 L. 682       490  LOAD_FAST                'line'
          492_494  POP_JUMP_IF_FALSE   574  'to 574'

 L. 684       496  LOAD_FAST                'self'
              498  LOAD_METHOD              set_break
              500  LOAD_FAST                'filename'
              502  LOAD_FAST                'line'
              504  LOAD_FAST                'temporary'
              506  LOAD_FAST                'cond'
              508  LOAD_FAST                'funcname'
              510  CALL_METHOD_5         5  ''
              512  STORE_FAST               'err'

 L. 685       514  LOAD_FAST                'err'
          516_518  POP_JUMP_IF_FALSE   532  'to 532'

 L. 686       520  LOAD_FAST                'self'
              522  LOAD_METHOD              error
              524  LOAD_FAST                'err'
              526  CALL_METHOD_1         1  ''
              528  POP_TOP          
              530  JUMP_FORWARD        574  'to 574'
            532_0  COME_FROM           516  '516'

 L. 688       532  LOAD_FAST                'self'
              534  LOAD_METHOD              get_breaks
              536  LOAD_FAST                'filename'
              538  LOAD_FAST                'line'
              540  CALL_METHOD_2         2  ''
              542  LOAD_CONST               -1
              544  BINARY_SUBSCR    
              546  STORE_FAST               'bp'

 L. 689       548  LOAD_FAST                'self'
              550  LOAD_METHOD              message
              552  LOAD_STR                 'Breakpoint %d at %s:%d'

 L. 690       554  LOAD_FAST                'bp'
              556  LOAD_ATTR                number
              558  LOAD_FAST                'bp'
              560  LOAD_ATTR                file
              562  LOAD_FAST                'bp'
              564  LOAD_ATTR                line
              566  BUILD_TUPLE_3         3 

 L. 689       568  BINARY_MODULO    
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
        else:
            if len(idstring) == 3:
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
        else:
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

    def checkline--- This code section failed: ---

 L. 755         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'self'
                4  LOAD_STR                 'curframe'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                curframe
               14  LOAD_ATTR                f_globals
               16  JUMP_FORWARD         20  'to 20'
             18_0  COME_FROM             8  '8'
               18  LOAD_CONST               None
             20_0  COME_FROM            16  '16'
               20  STORE_FAST               'globs'

 L. 756        22  LOAD_GLOBAL              linecache
               24  LOAD_METHOD              getline
               26  LOAD_FAST                'filename'
               28  LOAD_FAST                'lineno'
               30  LOAD_FAST                'globs'
               32  CALL_METHOD_3         3  ''
               34  STORE_FAST               'line'

 L. 757        36  LOAD_FAST                'line'
               38  POP_JUMP_IF_TRUE     54  'to 54'

 L. 758        40  LOAD_FAST                'self'
               42  LOAD_METHOD              message
               44  LOAD_STR                 'End of file'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L. 759        50  LOAD_CONST               0
               52  RETURN_VALUE     
             54_0  COME_FROM            38  '38'

 L. 760        54  LOAD_FAST                'line'
               56  LOAD_METHOD              strip
               58  CALL_METHOD_0         0  ''
               60  STORE_FAST               'line'

 L. 762        62  LOAD_FAST                'line'
               64  POP_JUMP_IF_FALSE   110  'to 110'
               66  LOAD_FAST                'line'
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  LOAD_STR                 '#'
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_TRUE    110  'to 110'

 L. 763        78  LOAD_FAST                'line'
               80  LOAD_CONST               None
               82  LOAD_CONST               3
               84  BUILD_SLICE_2         2 
               86  BINARY_SUBSCR    
               88  LOAD_STR                 '"""'
               90  COMPARE_OP               ==

 L. 762        92  POP_JUMP_IF_TRUE    110  'to 110'

 L. 763        94  LOAD_FAST                'line'
               96  LOAD_CONST               None
               98  LOAD_CONST               3
              100  BUILD_SLICE_2         2 
              102  BINARY_SUBSCR    
              104  LOAD_STR                 "'''"
              106  COMPARE_OP               ==

 L. 762       108  POP_JUMP_IF_FALSE   124  'to 124'
            110_0  COME_FROM            92  '92'
            110_1  COME_FROM            76  '76'
            110_2  COME_FROM            64  '64'

 L. 764       110  LOAD_FAST                'self'
              112  LOAD_METHOD              error
              114  LOAD_STR                 'Blank or comment'
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          

 L. 765       120  LOAD_CONST               0
              122  RETURN_VALUE     
            124_0  COME_FROM           108  '108'

 L. 766       124  LOAD_FAST                'lineno'
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 126

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

                else:
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

 L. 941         0  LOAD_FAST                'self'
                2  LOAD_ATTR                curindex
                4  LOAD_CONST               0
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 942        10  LOAD_FAST                'self'
               12  LOAD_METHOD              error
               14  LOAD_STR                 'Oldest frame'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L. 943        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM             8  '8'

 L. 944        24  SETUP_FINALLY        42  'to 42'

 L. 945        26  LOAD_GLOBAL              int
               28  LOAD_FAST                'arg'
               30  JUMP_IF_TRUE_OR_POP    34  'to 34'
               32  LOAD_CONST               1
             34_0  COME_FROM            30  '30'
               34  CALL_FUNCTION_1       1  ''
               36  STORE_FAST               'count'
               38  POP_BLOCK        
               40  JUMP_FORWARD         78  'to 78'
             42_0  COME_FROM_FINALLY    24  '24'

 L. 946        42  DUP_TOP          
               44  LOAD_GLOBAL              ValueError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    76  'to 76'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 947        56  LOAD_FAST                'self'
               58  LOAD_METHOD              error
               60  LOAD_STR                 'Invalid frame count (%s)'
               62  LOAD_FAST                'arg'
               64  BINARY_MODULO    
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L. 948        70  POP_EXCEPT       
               72  LOAD_CONST               None
               74  RETURN_VALUE     
             76_0  COME_FROM            48  '48'
               76  END_FINALLY      
             78_0  COME_FROM            40  '40'

 L. 949        78  LOAD_FAST                'count'
               80  LOAD_CONST               0
               82  COMPARE_OP               <
               84  POP_JUMP_IF_FALSE    92  'to 92'

 L. 950        86  LOAD_CONST               0
               88  STORE_FAST               'newframe'
               90  JUMP_FORWARD        108  'to 108'
             92_0  COME_FROM            84  '84'

 L. 952        92  LOAD_GLOBAL              max
               94  LOAD_CONST               0
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                curindex
              100  LOAD_FAST                'count'
              102  BINARY_SUBTRACT  
              104  CALL_FUNCTION_2       2  ''
              106  STORE_FAST               'newframe'
            108_0  COME_FROM            90  '90'

 L. 953       108  LOAD_FAST                'self'
              110  LOAD_METHOD              _select_frame
              112  LOAD_FAST                'newframe'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 72

    do_u = do_up

    def do_down--- This code section failed: ---

 L. 961         0  LOAD_FAST                'self'
                2  LOAD_ATTR                curindex
                4  LOAD_CONST               1
                6  BINARY_ADD       
                8  LOAD_GLOBAL              len
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                stack
               14  CALL_FUNCTION_1       1  ''
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    34  'to 34'

 L. 962        20  LOAD_FAST                'self'
               22  LOAD_METHOD              error
               24  LOAD_STR                 'Newest frame'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 963        30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            18  '18'

 L. 964        34  SETUP_FINALLY        52  'to 52'

 L. 965        36  LOAD_GLOBAL              int
               38  LOAD_FAST                'arg'
               40  JUMP_IF_TRUE_OR_POP    44  'to 44'
               42  LOAD_CONST               1
             44_0  COME_FROM            40  '40'
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'count'
               48  POP_BLOCK        
               50  JUMP_FORWARD         88  'to 88'
             52_0  COME_FROM_FINALLY    34  '34'

 L. 966        52  DUP_TOP          
               54  LOAD_GLOBAL              ValueError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    86  'to 86'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 967        66  LOAD_FAST                'self'
               68  LOAD_METHOD              error
               70  LOAD_STR                 'Invalid frame count (%s)'
               72  LOAD_FAST                'arg'
               74  BINARY_MODULO    
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 968        80  POP_EXCEPT       
               82  LOAD_CONST               None
               84  RETURN_VALUE     
             86_0  COME_FROM            58  '58'
               86  END_FINALLY      
             88_0  COME_FROM            50  '50'

 L. 969        88  LOAD_FAST                'count'
               90  LOAD_CONST               0
               92  COMPARE_OP               <
               94  POP_JUMP_IF_FALSE   112  'to 112'

 L. 970        96  LOAD_GLOBAL              len
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                stack
              102  CALL_FUNCTION_1       1  ''
              104  LOAD_CONST               1
              106  BINARY_SUBTRACT  
              108  STORE_FAST               'newframe'
              110  JUMP_FORWARD        138  'to 138'
            112_0  COME_FROM            94  '94'

 L. 972       112  LOAD_GLOBAL              min
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

 L. 973       138  LOAD_FAST                'self'
              140  LOAD_METHOD              _select_frame
              142  LOAD_FAST                'newframe'
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 82

    do_d = do_down

    def do_until--- This code section failed: ---

 L. 984         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_FALSE    82  'to 82'

 L. 985         4  SETUP_FINALLY        18  'to 18'

 L. 986         6  LOAD_GLOBAL              int
                8  LOAD_FAST                'arg'
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'lineno'
               14  POP_BLOCK        
               16  JUMP_FORWARD         54  'to 54'
             18_0  COME_FROM_FINALLY     4  '4'

 L. 987        18  DUP_TOP          
               20  LOAD_GLOBAL              ValueError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    52  'to 52'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 988        32  LOAD_FAST                'self'
               34  LOAD_METHOD              error
               36  LOAD_STR                 'Error in argument: %r'
               38  LOAD_FAST                'arg'
               40  BINARY_MODULO    
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 989        46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            24  '24'
               52  END_FINALLY      
             54_0  COME_FROM            16  '16'

 L. 990        54  LOAD_FAST                'lineno'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                curframe
               60  LOAD_ATTR                f_lineno
               62  COMPARE_OP               <=
               64  POP_JUMP_IF_FALSE    86  'to 86'

 L. 991        66  LOAD_FAST                'self'
               68  LOAD_METHOD              error
               70  LOAD_STR                 '"until" line number is smaller than current line number'
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          

 L. 993        76  LOAD_CONST               None
               78  RETURN_VALUE     
               80  JUMP_FORWARD         86  'to 86'
             82_0  COME_FROM             2  '2'

 L. 995        82  LOAD_CONST               None
               84  STORE_FAST               'lineno'
             86_0  COME_FROM            80  '80'
             86_1  COME_FROM            64  '64'

 L. 996        86  LOAD_FAST                'self'
               88  LOAD_METHOD              set_until
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                curframe
               94  LOAD_FAST                'lineno'
               96  CALL_METHOD_2         2  ''
               98  POP_TOP          

 L. 997       100  LOAD_CONST               1
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
            return None
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

 L.1162         0  SETUP_FINALLY        22  'to 22'

 L.1163         2  LOAD_GLOBAL              eval
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

 L.1164        22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.1165        28  LOAD_GLOBAL              sys
               30  LOAD_METHOD              exc_info
               32  CALL_METHOD_0         0  ''
               34  LOAD_CONST               None
               36  LOAD_CONST               2
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  STORE_FAST               'exc_info'

 L.1166        44  LOAD_FAST                'self'
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

 L.1167        68  RAISE_VARARGS_0       0  'reraise'
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

 L.1217         0  LOAD_STR                 'list'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               lastcmd

 L.1218         6  LOAD_CONST               None
                8  STORE_FAST               'last'

 L.1219        10  LOAD_FAST                'arg'
               12  POP_JUMP_IF_FALSE   156  'to 156'
               14  LOAD_FAST                'arg'
               16  LOAD_STR                 '.'
               18  COMPARE_OP               !=
               20  POP_JUMP_IF_FALSE   156  'to 156'

 L.1220        22  SETUP_FINALLY       118  'to 118'

 L.1221        24  LOAD_STR                 ','
               26  LOAD_FAST                'arg'
               28  COMPARE_OP               in
               30  POP_JUMP_IF_FALSE    88  'to 88'

 L.1222        32  LOAD_FAST                'arg'
               34  LOAD_METHOD              split
               36  LOAD_STR                 ','
               38  CALL_METHOD_1         1  ''
               40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'first'
               44  STORE_FAST               'last'

 L.1223        46  LOAD_GLOBAL              int
               48  LOAD_FAST                'first'
               50  LOAD_METHOD              strip
               52  CALL_METHOD_0         0  ''
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'first'

 L.1224        58  LOAD_GLOBAL              int
               60  LOAD_FAST                'last'
               62  LOAD_METHOD              strip
               64  CALL_METHOD_0         0  ''
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'last'

 L.1225        70  LOAD_FAST                'last'
               72  LOAD_FAST                'first'
               74  COMPARE_OP               <
               76  POP_JUMP_IF_FALSE   114  'to 114'

 L.1227        78  LOAD_FAST                'first'
               80  LOAD_FAST                'last'
               82  BINARY_ADD       
               84  STORE_FAST               'last'
               86  JUMP_FORWARD        114  'to 114'
             88_0  COME_FROM            30  '30'

 L.1229        88  LOAD_GLOBAL              int
               90  LOAD_FAST                'arg'
               92  LOAD_METHOD              strip
               94  CALL_METHOD_0         0  ''
               96  CALL_FUNCTION_1       1  ''
               98  STORE_FAST               'first'

 L.1230       100  LOAD_GLOBAL              max
              102  LOAD_CONST               1
              104  LOAD_FAST                'first'
              106  LOAD_CONST               5
              108  BINARY_SUBTRACT  
              110  CALL_FUNCTION_2       2  ''
              112  STORE_FAST               'first'
            114_0  COME_FROM            86  '86'
            114_1  COME_FROM            76  '76'
              114  POP_BLOCK        
              116  JUMP_ABSOLUTE       204  'to 204'
            118_0  COME_FROM_FINALLY    22  '22'

 L.1231       118  DUP_TOP          
              120  LOAD_GLOBAL              ValueError
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   152  'to 152'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L.1232       132  LOAD_FAST                'self'
              134  LOAD_METHOD              error
              136  LOAD_STR                 'Error in argument: %r'
              138  LOAD_FAST                'arg'
              140  BINARY_MODULO    
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          

 L.1233       146  POP_EXCEPT       
              148  LOAD_CONST               None
              150  RETURN_VALUE     
            152_0  COME_FROM           124  '124'
              152  END_FINALLY      
              154  JUMP_FORWARD        204  'to 204'
            156_0  COME_FROM            20  '20'
            156_1  COME_FROM            12  '12'

 L.1234       156  LOAD_FAST                'self'
              158  LOAD_ATTR                lineno
              160  LOAD_CONST               None
              162  COMPARE_OP               is
              164  POP_JUMP_IF_TRUE    174  'to 174'
              166  LOAD_FAST                'arg'
              168  LOAD_STR                 '.'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   194  'to 194'
            174_0  COME_FROM           164  '164'

 L.1235       174  LOAD_GLOBAL              max
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

 L.1237       194  LOAD_FAST                'self'
              196  LOAD_ATTR                lineno
              198  LOAD_CONST               1
              200  BINARY_ADD       
              202  STORE_FAST               'first'
            204_0  COME_FROM           192  '192'
            204_1  COME_FROM           154  '154'

 L.1238       204  LOAD_FAST                'last'
              206  LOAD_CONST               None
              208  COMPARE_OP               is
              210  POP_JUMP_IF_FALSE   220  'to 220'

 L.1239       212  LOAD_FAST                'first'
              214  LOAD_CONST               10
              216  BINARY_ADD       
              218  STORE_FAST               'last'
            220_0  COME_FROM           210  '210'

 L.1240       220  LOAD_FAST                'self'
              222  LOAD_ATTR                curframe
              224  LOAD_ATTR                f_code
              226  LOAD_ATTR                co_filename
              228  STORE_FAST               'filename'

 L.1241       230  LOAD_FAST                'self'
              232  LOAD_METHOD              get_file_breaks
              234  LOAD_FAST                'filename'
              236  CALL_METHOD_1         1  ''
              238  STORE_FAST               'breaklist'

 L.1242       240  SETUP_FINALLY       332  'to 332'

 L.1243       242  LOAD_GLOBAL              linecache
              244  LOAD_METHOD              getlines
              246  LOAD_FAST                'filename'
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                curframe
              252  LOAD_ATTR                f_globals
              254  CALL_METHOD_2         2  ''
              256  STORE_FAST               'lines'

 L.1244       258  LOAD_FAST                'self'
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

 L.1245       280  LOAD_FAST                'self'
              282  LOAD_ATTR                curframe

 L.1244       284  CALL_METHOD_4         4  ''
              286  POP_TOP          

 L.1246       288  LOAD_GLOBAL              min
              290  LOAD_FAST                'last'
              292  LOAD_GLOBAL              len
              294  LOAD_FAST                'lines'
              296  CALL_FUNCTION_1       1  ''
              298  CALL_FUNCTION_2       2  ''
              300  LOAD_FAST                'self'
              302  STORE_ATTR               lineno

 L.1247       304  LOAD_GLOBAL              len
              306  LOAD_FAST                'lines'
              308  CALL_FUNCTION_1       1  ''
              310  LOAD_FAST                'last'
              312  COMPARE_OP               <
          314_316  POP_JUMP_IF_FALSE   328  'to 328'

 L.1248       318  LOAD_FAST                'self'
              320  LOAD_METHOD              message
              322  LOAD_STR                 '[EOF]'
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          
            328_0  COME_FROM           314  '314'
              328  POP_BLOCK        
              330  JUMP_FORWARD        354  'to 354'
            332_0  COME_FROM_FINALLY   240  '240'

 L.1249       332  DUP_TOP          
              334  LOAD_GLOBAL              KeyboardInterrupt
              336  COMPARE_OP               exception-match
          338_340  POP_JUMP_IF_FALSE   352  'to 352'
              342  POP_TOP          
              344  POP_TOP          
              346  POP_TOP          

 L.1250       348  POP_EXCEPT       
              350  JUMP_FORWARD        354  'to 354'
            352_0  COME_FROM           338  '338'
              352  END_FINALLY      
            354_0  COME_FROM           350  '350'
            354_1  COME_FROM           330  '330'

Parse error at or near `LOAD_CONST' instruction at offset 148

    do_l = do_list

    def do_longlist--- This code section failed: ---

 L.1257         0  LOAD_FAST                'self'
                2  LOAD_ATTR                curframe
                4  LOAD_ATTR                f_code
                6  LOAD_ATTR                co_filename
                8  STORE_FAST               'filename'

 L.1258        10  LOAD_FAST                'self'
               12  LOAD_METHOD              get_file_breaks
               14  LOAD_FAST                'filename'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'breaklist'

 L.1259        20  SETUP_FINALLY        40  'to 40'

 L.1260        22  LOAD_GLOBAL              getsourcelines
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                curframe
               28  CALL_FUNCTION_1       1  ''
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'lines'
               34  STORE_FAST               'lineno'
               36  POP_BLOCK        
               38  JUMP_FORWARD         90  'to 90'
             40_0  COME_FROM_FINALLY    20  '20'

 L.1261        40  DUP_TOP          
               42  LOAD_GLOBAL              OSError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    88  'to 88'
               48  POP_TOP          
               50  STORE_FAST               'err'
               52  POP_TOP          
               54  SETUP_FINALLY        76  'to 76'

 L.1262        56  LOAD_FAST                'self'
               58  LOAD_METHOD              error
               60  LOAD_FAST                'err'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L.1263        66  POP_BLOCK        
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

 L.1264        90  LOAD_FAST                'self'
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

 L.1271         0  SETUP_FINALLY        16  'to 16'

 L.1272         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _getval
                6  LOAD_FAST                'arg'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'obj'
               12  POP_BLOCK        
               14  JUMP_FORWARD         30  'to 30'
             16_0  COME_FROM_FINALLY     0  '0'

 L.1273        16  POP_TOP          
               18  POP_TOP          
               20  POP_TOP          

 L.1274        22  POP_EXCEPT       
               24  LOAD_CONST               None
               26  RETURN_VALUE     
               28  END_FINALLY      
             30_0  COME_FROM            14  '14'

 L.1275        30  SETUP_FINALLY        48  'to 48'

 L.1276        32  LOAD_GLOBAL              getsourcelines
               34  LOAD_FAST                'obj'
               36  CALL_FUNCTION_1       1  ''
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'lines'
               42  STORE_FAST               'lineno'
               44  POP_BLOCK        
               46  JUMP_FORWARD        102  'to 102'
             48_0  COME_FROM_FINALLY    30  '30'

 L.1277        48  DUP_TOP          
               50  LOAD_GLOBAL              OSError
               52  LOAD_GLOBAL              TypeError
               54  BUILD_TUPLE_2         2 
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE   100  'to 100'
               60  POP_TOP          
               62  STORE_FAST               'err'
               64  POP_TOP          
               66  SETUP_FINALLY        88  'to 88'

 L.1278        68  LOAD_FAST                'self'
               70  LOAD_METHOD              error
               72  LOAD_FAST                'err'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L.1279        78  POP_BLOCK        
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

 L.1280       102  LOAD_FAST                'self'
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
                else:
                    if lineno == exc_lineno:
                        s += '>>'
            self.message(s + '\t' + line.rstrip())

    def do_whatis--- This code section failed: ---

 L.1309         0  SETUP_FINALLY        16  'to 16'

 L.1310         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _getval
                6  LOAD_FAST                'arg'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'value'
               12  POP_BLOCK        
               14  JUMP_FORWARD         30  'to 30'
             16_0  COME_FROM_FINALLY     0  '0'

 L.1311        16  POP_TOP          
               18  POP_TOP          
               20  POP_TOP          

 L.1313        22  POP_EXCEPT       
               24  LOAD_CONST               None
               26  RETURN_VALUE     
               28  END_FINALLY      
             30_0  COME_FROM            14  '14'

 L.1314        30  LOAD_CONST               None
               32  STORE_FAST               'code'

 L.1316        34  SETUP_FINALLY        48  'to 48'

 L.1317        36  LOAD_FAST                'value'
               38  LOAD_ATTR                __func__
               40  LOAD_ATTR                __code__
               42  STORE_FAST               'code'
               44  POP_BLOCK        
               46  JUMP_FORWARD         68  'to 68'
             48_0  COME_FROM_FINALLY    34  '34'

 L.1318        48  DUP_TOP          
               50  LOAD_GLOBAL              Exception
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    66  'to 66'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.1319        62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
             66_0  COME_FROM            54  '54'
               66  END_FINALLY      
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM            46  '46'

 L.1320        68  LOAD_FAST                'code'
               70  POP_JUMP_IF_FALSE    92  'to 92'

 L.1321        72  LOAD_FAST                'self'
               74  LOAD_METHOD              message
               76  LOAD_STR                 'Method %s'
               78  LOAD_FAST                'code'
               80  LOAD_ATTR                co_name
               82  BINARY_MODULO    
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L.1322        88  LOAD_CONST               None
               90  RETURN_VALUE     
             92_0  COME_FROM            70  '70'

 L.1324        92  SETUP_FINALLY       104  'to 104'

 L.1325        94  LOAD_FAST                'value'
               96  LOAD_ATTR                __code__
               98  STORE_FAST               'code'
              100  POP_BLOCK        
              102  JUMP_FORWARD        124  'to 124'
            104_0  COME_FROM_FINALLY    92  '92'

 L.1326       104  DUP_TOP          
              106  LOAD_GLOBAL              Exception
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   122  'to 122'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L.1327       118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM           110  '110'
              122  END_FINALLY      
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM           102  '102'

 L.1328       124  LOAD_FAST                'code'
              126  POP_JUMP_IF_FALSE   148  'to 148'

 L.1329       128  LOAD_FAST                'self'
              130  LOAD_METHOD              message
              132  LOAD_STR                 'Function %s'
              134  LOAD_FAST                'code'
              136  LOAD_ATTR                co_name
              138  BINARY_MODULO    
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          

 L.1330       144  LOAD_CONST               None
              146  RETURN_VALUE     
            148_0  COME_FROM           126  '126'

 L.1332       148  LOAD_FAST                'value'
              150  LOAD_ATTR                __class__
              152  LOAD_GLOBAL              type
              154  COMPARE_OP               is
              156  POP_JUMP_IF_FALSE   184  'to 184'

 L.1333       158  LOAD_FAST                'self'
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

 L.1334       180  LOAD_CONST               None
              182  RETURN_VALUE     
            184_0  COME_FROM           156  '156'

 L.1336       184  LOAD_FAST                'self'
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

 L.1471         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_TRUE     18  'to 18'

 L.1472         4  LOAD_GLOBAL              cmd
                6  LOAD_ATTR                Cmd
                8  LOAD_METHOD              do_help
               10  LOAD_FAST                'self'
               12  LOAD_FAST                'arg'
               14  CALL_METHOD_2         2  ''
               16  RETURN_VALUE     
             18_0  COME_FROM             2  '2'

 L.1473        18  SETUP_FINALLY        84  'to 84'

 L.1474        20  SETUP_FINALLY        46  'to 46'

 L.1475        22  LOAD_GLOBAL              getattr
               24  LOAD_FAST                'self'
               26  LOAD_STR                 'help_'
               28  LOAD_FAST                'arg'
               30  BINARY_ADD       
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'topic'

 L.1476        36  LOAD_FAST                'topic'
               38  CALL_FUNCTION_0       0  ''
               40  POP_BLOCK        
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY    20  '20'

 L.1477        46  DUP_TOP          
               48  LOAD_GLOBAL              AttributeError
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    78  'to 78'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L.1478        60  LOAD_GLOBAL              getattr
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

 L.1479        84  DUP_TOP          
               86  LOAD_GLOBAL              AttributeError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   116  'to 116'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L.1480        98  LOAD_FAST                'self'
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

 L.1482       118  LOAD_GLOBAL              sys
              120  LOAD_ATTR                flags
              122  LOAD_ATTR                optimize
              124  LOAD_CONST               2
              126  COMPARE_OP               >=
              128  POP_JUMP_IF_FALSE   148  'to 148'

 L.1483       130  LOAD_FAST                'self'
              132  LOAD_METHOD              error
              134  LOAD_STR                 'No help for %r; please do not run Python with -OO if you need command help'

 L.1484       136  LOAD_FAST                'arg'

 L.1483       138  BINARY_MODULO    
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          

 L.1485       144  LOAD_CONST               None
              146  RETURN_VALUE     
            148_0  COME_FROM           128  '128'

 L.1486       148  LOAD_FAST                'self'
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
            if os.path.islinkdirname:
                dirname = os.readlinkdirname
            else:
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
        with io.open_codefilename as (fp):
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
    Pdb.runstatementglobalslocals


def runeval(expression, globals=None, locals=None):
    return Pdb.runevalexpressionglobalslocals


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

def main():
    import getopt
    opts, args = getopt.getoptsys.argv[1:]'mhc:'['help', 'command=']
    if not args:
        print(_usage)
        sys.exit2
    commands = []
    run_as_module = False
    for opt, optarg in opts:
        if opt in ('-h', '--help'):
            print(_usage)
            sys.exit()
        elif opt in ('-c', '--command'):
            commands.appendoptarg
    else:
        if opt in ('-m', ):
            run_as_module = True
        mainpyfile = args[0]
        if not run_as_module:
            if not os.path.existsmainpyfile:
                print('Error:', mainpyfile, 'does not exist')
                sys.exit1
        sys.argv[:] = args
        if not run_as_module:
            sys.path[0] = os.path.dirnamemainpyfile
        pdb = Pdb
        pdb.rcLines.extendcommands
        while True:
            try:
                if run_as_module:
                    pdb._runmodulemainpyfile
                else:
                    pdb._runscriptmainpyfile
                if pdb._user_requested_quit:
                    break
                print('The program finished and will be restarted')
            except Restart:
                print('Restarting', mainpyfile, 'with arguments:')
                print('\t' + ' '.joinargs)
            except SystemExit:
                print('The program exited via sys.exit(). Exit status:', end=' ')
                print(sys.exc_info()[1])
            except SyntaxError:
                traceback.print_exc()
                sys.exit1
            except:
                traceback.print_exc()
                print('Uncaught exception. Entering post mortem debugging')
                print("Running 'cont' or 'step' will restart the program")
                t = sys.exc_info()[2]
                pdb.interaction(None, t)
                print('Post mortem debugger finished. The ' + mainpyfile + ' will be restarted')


if __name__ == '__main__':
    import pdb
    pdb.main()