# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
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
import os, re, sys, cmd, bdb, dis, code, glob, pprint, signal, inspect, traceback, linecache

class Restart(Exception):
    __doc__ = 'Causes a debugger to be restarted for the debugged python program.'


__all__ = [
 'run', 'pm', 'Pdb', 'runeval', 'runctx', 'runcall', 'set_trace',
 'post_mortem', 'help']

def find_function(funcname, filename):
    cre = re.compile('def\\s+%s\\s*[(]' % re.escape(funcname))
    try:
        fp = open(filename)
    except OSError:
        return
    else:
        with fp:
            for lineno, line in enumerate(fp, start=1):
                if cre.match(line):
                    return (funcname, filename, lineno)


def getsourcelines(obj):
    lines, lineno = inspect.findsource(obj)
    if inspect.isframe(obj):
        if obj.f_globals is obj.f_locals:
            return (
             lines, 1)
    if inspect.ismodule(obj):
        return (lines, 1)
    return (inspect.getblock(lines[lineno:]), lineno + 1)


def lasti2lineno(code, lasti):
    linestarts = list(dis.findlinestarts(code))
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
            readline.set_completer_delims(' \t\n`@#$%^&*()=+[{]}\\|;:\'",<>?')
        except ImportError:
            pass

        self.allow_kbdint = False
        self.nosigint = nosigint
        self.rcLines = []
        if readrc:
            if 'HOME' in os.environ:
                envHome = os.environ['HOME']
                try:
                    with open(os.path.join(envHome, '.pdbrc')) as rcFile:
                        self.rcLines.extend(rcFile)
                except OSError:
                    pass

            try:
                with open('.pdbrc') as rcFile:
                    self.rcLines.extend(rcFile)
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
        self.message("\nProgram interrupted. (Use 'cont' to resume).")
        self.set_step()
        self.set_trace(frame)

    def reset(self):
        bdb.Bdb.reset(self)
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
        while rcLines:
            line = rcLines.pop().strip()
            if line:
                if line[0] != '#':
                    if self.onecmd(line):
                        self.rcLines += reversed(rcLines)
                        return True

    def user_call(self, frame, argument_list):
        """This method is called when there is the remote possibility
        that we ever need to stop in this function."""
        if self._wait_for_mainpyfile:
            return
        if self.stop_here(frame):
            self.message('--Call--')
            self.interaction(frame, None)

    def user_line(self, frame):
        """This function is called when we stop or break at this line."""
        if self._wait_for_mainpyfile:
            if self.mainpyfile != self.canonic(frame.f_code.co_filename) or (frame.f_lineno <= 0):
                return
            self._wait_for_mainpyfile = False
        if self.bp_commands(frame):
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
                    self.onecmd(line)

                self.lastcmd = lastcmd_back
                if not self.commands_silent[currentbp]:
                    self.print_stack_entry(self.stack[self.curindex])
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
        self.message('--Return--')
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
        while 1:
            try:
                self.allow_kbdint = True
                self.cmdloop()
                self.allow_kbdint = False
                break
            except KeyboardInterrupt:
                self.message('--KeyboardInterrupt--')

    def preloop(self):
        displaying = self.displaying.get(self.curframe)
        if displaying:
            for expr, oldvalue in displaying.items():
                newvalue = self._getval_except(expr)
                if newvalue is not oldvalue:
                    if newvalue != oldvalue:
                        displaying[expr] = newvalue
                        self.message('display %s: %r  [old: %r]' % (
                         expr, newvalue, oldvalue))

    def interaction(self, frame, traceback):
        if Pdb._previous_sigint_handler:
            signal.signal(signal.SIGINT, Pdb._previous_sigint_handler)
            Pdb._previous_sigint_handler = None
        if self.setup(frame, traceback):
            self.forget()
            return
        self.print_stack_entry(self.stack[self.curindex])
        self._cmdloop()
        self.forget()

    def displayhook(self, obj):
        """Custom displayhook for the exec in default(), which prevents
        assignment of the _ variable in the builtins.
        """
        if obj is not None:
            self.message(repr(obj))

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
            self.error((traceback.format_exception_only)(*exc_info)[(-1)].strip())

    def precmd(self, line):
        """Handle alias expansion and ';;' separator."""
        if not line.strip():
            return line
        args = line.split()
        while args[0] in self.aliases:
            line = self.aliases[args[0]]
            ii = 1
            for tmpArg in args[1:]:
                line = line.replace('%' + str(ii), tmpArg)
                ii += 1

            line = line.replace('%*', ' '.join(args[1:]))
            args = line.split()

        if args[0] != 'alias':
            marker = line.find(';;')
            if marker >= 0:
                next = line[marker + 2:].lstrip()
                self.cmdqueue.append(next)
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
        return self.handle_command_def(line)

    def handle_command_def(self, line):
        """Handles one command line during command list definition."""
        cmd, arg, line = self.parseline(line)
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
            cmdlist.append(cmd)
        try:
            func = getattr(self, 'do_' + cmd)
        except AttributeError:
            func = self.default

        if func.__name__ in self.commands_resuming:
            self.commands_doprompt[self.commands_bnum] = False
            self.cmdqueue = []
            return 1

    def message(self, msg):
        print(msg, file=(self.stdout))

    def error(self, msg):
        print('***', msg, file=(self.stdout))

    def _complete_location(self, text, line, begidx, endidx):
        if line.strip().endswith((':', ',')):
            return []
        try:
            ret = self._complete_expression(text, line, begidx, endidx)
        except Exception:
            ret = []

        globs = glob.glob(text + '*')
        for fn in globs:
            if os.path.isdir(fn):
                ret.append(fn + '/')
            if os.path.isfile(fn):
                if fn.lower().endswith(('.py', '.pyw')):
                    ret.append(fn + ':')

        return ret

    def _complete_bpnumber(self, text, line, begidx, endidx):
        return [str(i) for i, bp in enumerate(bdb.Breakpoint.bpbynumber) if bp is not None if str(i).startswith(text)]

    def _complete_expression(self, text, line, begidx, endidx):
        if not self.curframe:
            return []
        ns = self.curframe.f_globals.copy()
        ns.update(self.curframe_locals)
        if '.' in text:
            dotted = text.split('.')
            try:
                obj = ns[dotted[0]]
                for part in dotted[1:-1]:
                    obj = getattr(obj, part)

            except (KeyError, AttributeError):
                return []
            else:
                prefix = '.'.join(dotted[:-1]) + '.'
                return [prefix + n for n in dir(obj) if n.startswith(dotted[(-1)])]

            return [n for n in ns.keys() if n.startswith(text)]

    def do_commands(self, arg):
        """commands [bpnumber]
        (com) ...
        (com) end
        (Pdb)

        Specify a list of commands for breakpoint number bpnumber.
        The commands themselves are entered on the following lines.
        Type a line containing just 'end' to terminate the commands.
        The commands are executed when the breakpoint is hit.

        To remove all commands from a breakpoint, type commands and
        follow it immediately with end; that is, give no commands.

        With no bpnumber argument, commands refers to the last
        breakpoint set.

        You can use breakpoint commands to start your program up
        again.  Simply use the continue command, or step, or any other
        command that resumes execution.

        Specifying any command resuming execution (currently continue,
        step, next, return, jump, quit and their abbreviations)
        terminates the command list (as if that command was
        immediately followed by end).  This is because any time you
        resume execution (even with a simple next or step), you may
        encounter another breakpoint -- which could have its own
        command list, leading to ambiguities about which list to
        execute.

        If you use the 'silent' command in the command list, the usual
        message about stopping at a breakpoint is not printed.  This
        may be desirable for breakpoints that are to print a specific
        message and then continue.  If none of the other commands
        print anything, you will see no sign that the breakpoint was
        reached.
        """
        if not arg:
            bnum = len(bdb.Breakpoint.bpbynumber) - 1
        else:
            try:
                bnum = int(arg)
            except:
                self.error('Usage: commands [bnum]\n        ...\n        end')
                return

        self.commands_bnum = bnum
        if bnum in self.commands:
            old_command_defs = (
             self.commands[bnum],
             self.commands_doprompt[bnum],
             self.commands_silent[bnum])
        else:
            old_command_defs = None
        self.commands[bnum] = []
        self.commands_doprompt[bnum] = True
        self.commands_silent[bnum] = False
        prompt_back = self.prompt
        self.prompt = '(com) '
        self.commands_defining = True
        try:
            try:
                self.cmdloop()
            except KeyboardInterrupt:
                if old_command_defs:
                    self.commands[bnum] = old_command_defs[0]
                    self.commands_doprompt[bnum] = old_command_defs[1]
                    self.commands_silent[bnum] = old_command_defs[2]
                else:
                    del self.commands[bnum]
                    del self.commands_doprompt[bnum]
                    del self.commands_silent[bnum]
                self.error('command definition aborted, old commands restored')

        finally:
            self.commands_defining = False
            self.prompt = prompt_back

    complete_commands = _complete_bpnumber

    def do_break--- This code section failed: ---

 L. 611         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_TRUE     60  'to 60'

 L. 612         4  LOAD_FAST                'self'
                6  LOAD_ATTR                breaks
                8  POP_JUMP_IF_FALSE    56  'to 56'

 L. 613        10  LOAD_FAST                'self'
               12  LOAD_METHOD              message
               14  LOAD_STR                 'Num Type         Disp Enb   Where'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  POP_TOP          

 L. 614        20  SETUP_LOOP           56  'to 56'
               22  LOAD_GLOBAL              bdb
               24  LOAD_ATTR                Breakpoint
               26  LOAD_ATTR                bpbynumber
               28  GET_ITER         
             30_0  COME_FROM            52  '52'
             30_1  COME_FROM            36  '36'
               30  FOR_ITER             54  'to 54'
               32  STORE_FAST               'bp'

 L. 615        34  LOAD_FAST                'bp'
               36  POP_JUMP_IF_FALSE_BACK    30  'to 30'

 L. 616        38  LOAD_FAST                'self'
               40  LOAD_METHOD              message
               42  LOAD_FAST                'bp'
               44  LOAD_METHOD              bpformat
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  CALL_METHOD_1         1  '1 positional argument'
               50  POP_TOP          
               52  JUMP_BACK            30  'to 30'
               54  POP_BLOCK        
             56_0  COME_FROM_LOOP       20  '20'
             56_1  COME_FROM             8  '8'

 L. 617        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM             2  '2'

 L. 620        60  LOAD_CONST               None
               62  STORE_FAST               'filename'

 L. 621        64  LOAD_CONST               None
               66  STORE_FAST               'lineno'

 L. 622        68  LOAD_CONST               None
               70  STORE_FAST               'cond'

 L. 623        72  LOAD_FAST                'arg'
               74  LOAD_METHOD              find
               76  LOAD_STR                 ','
               78  CALL_METHOD_1         1  '1 positional argument'
               80  STORE_FAST               'comma'

 L. 624        82  LOAD_FAST                'comma'
               84  LOAD_CONST               0
               86  COMPARE_OP               >
               88  POP_JUMP_IF_FALSE   126  'to 126'

 L. 626        90  LOAD_FAST                'arg'
               92  LOAD_FAST                'comma'
               94  LOAD_CONST               1
               96  BINARY_ADD       
               98  LOAD_CONST               None
              100  BUILD_SLICE_2         2 
              102  BINARY_SUBSCR    
              104  LOAD_METHOD              lstrip
              106  CALL_METHOD_0         0  '0 positional arguments'
              108  STORE_FAST               'cond'

 L. 627       110  LOAD_FAST                'arg'
              112  LOAD_CONST               None
              114  LOAD_FAST                'comma'
              116  BUILD_SLICE_2         2 
              118  BINARY_SUBSCR    
              120  LOAD_METHOD              rstrip
              122  CALL_METHOD_0         0  '0 positional arguments'
              124  STORE_FAST               'arg'
            126_0  COME_FROM            88  '88'

 L. 629       126  LOAD_FAST                'arg'
              128  LOAD_METHOD              rfind
              130  LOAD_STR                 ':'
              132  CALL_METHOD_1         1  '1 positional argument'
              134  STORE_FAST               'colon'

 L. 630       136  LOAD_CONST               None
              138  STORE_FAST               'funcname'

 L. 631       140  LOAD_FAST                'colon'
              142  LOAD_CONST               0
              144  COMPARE_OP               >=
          146_148  POP_JUMP_IF_FALSE   274  'to 274'

 L. 632       150  LOAD_FAST                'arg'
              152  LOAD_CONST               None
              154  LOAD_FAST                'colon'
              156  BUILD_SLICE_2         2 
              158  BINARY_SUBSCR    
              160  LOAD_METHOD              rstrip
              162  CALL_METHOD_0         0  '0 positional arguments'
              164  STORE_FAST               'filename'

 L. 633       166  LOAD_FAST                'self'
              168  LOAD_METHOD              lookupmodule
              170  LOAD_FAST                'filename'
              172  CALL_METHOD_1         1  '1 positional argument'
              174  STORE_FAST               'f'

 L. 634       176  LOAD_FAST                'f'
              178  POP_JUMP_IF_TRUE    198  'to 198'

 L. 635       180  LOAD_FAST                'self'
              182  LOAD_METHOD              error
              184  LOAD_STR                 '%r not found from sys.path'
              186  LOAD_FAST                'filename'
              188  BINARY_MODULO    
              190  CALL_METHOD_1         1  '1 positional argument'
              192  POP_TOP          

 L. 636       194  LOAD_CONST               None
              196  RETURN_VALUE     
            198_0  COME_FROM           178  '178'

 L. 638       198  LOAD_FAST                'f'
              200  STORE_FAST               'filename'

 L. 639       202  LOAD_FAST                'arg'
              204  LOAD_FAST                'colon'
              206  LOAD_CONST               1
              208  BINARY_ADD       
              210  LOAD_CONST               None
              212  BUILD_SLICE_2         2 
              214  BINARY_SUBSCR    
              216  LOAD_METHOD              lstrip
              218  CALL_METHOD_0         0  '0 positional arguments'
              220  STORE_FAST               'arg'

 L. 640       222  SETUP_EXCEPT        236  'to 236'

 L. 641       224  LOAD_GLOBAL              int
              226  LOAD_FAST                'arg'
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  STORE_FAST               'lineno'
              232  POP_BLOCK        
              234  JUMP_FORWARD        272  'to 272'
            236_0  COME_FROM_EXCEPT    222  '222'

 L. 642       236  DUP_TOP          
              238  LOAD_GLOBAL              ValueError
              240  COMPARE_OP               exception-match
          242_244  POP_JUMP_IF_FALSE   270  'to 270'
              246  POP_TOP          
              248  POP_TOP          
              250  POP_TOP          

 L. 643       252  LOAD_FAST                'self'
              254  LOAD_METHOD              error
              256  LOAD_STR                 'Bad lineno: %s'
              258  LOAD_FAST                'arg'
              260  BINARY_MODULO    
              262  CALL_METHOD_1         1  '1 positional argument'
              264  POP_TOP          

 L. 644       266  LOAD_CONST               None
              268  RETURN_VALUE     
            270_0  COME_FROM           242  '242'
              270  END_FINALLY      
            272_0  COME_FROM           234  '234'
              272  JUMP_FORWARD        462  'to 462'
            274_0  COME_FROM           146  '146'

 L. 647       274  SETUP_EXCEPT        288  'to 288'

 L. 648       276  LOAD_GLOBAL              int
              278  LOAD_FAST                'arg'
              280  CALL_FUNCTION_1       1  '1 positional argument'
              282  STORE_FAST               'lineno'
              284  POP_BLOCK        
              286  JUMP_FORWARD        462  'to 462'
            288_0  COME_FROM_EXCEPT    274  '274'

 L. 649       288  DUP_TOP          
              290  LOAD_GLOBAL              ValueError
              292  COMPARE_OP               exception-match
          294_296  POP_JUMP_IF_FALSE   460  'to 460'
              298  POP_TOP          
              300  POP_TOP          
              302  POP_TOP          

 L. 650       304  SETUP_EXCEPT        328  'to 328'

 L. 651       306  LOAD_GLOBAL              eval
              308  LOAD_FAST                'arg'

 L. 652       310  LOAD_FAST                'self'
              312  LOAD_ATTR                curframe
              314  LOAD_ATTR                f_globals

 L. 653       316  LOAD_FAST                'self'
              318  LOAD_ATTR                curframe_locals
              320  CALL_FUNCTION_3       3  '3 positional arguments'
              322  STORE_FAST               'func'
              324  POP_BLOCK        
              326  JUMP_FORWARD        344  'to 344'
            328_0  COME_FROM_EXCEPT    304  '304'

 L. 654       328  POP_TOP          
              330  POP_TOP          
              332  POP_TOP          

 L. 655       334  LOAD_FAST                'arg'
              336  STORE_FAST               'func'
              338  POP_EXCEPT       
              340  JUMP_FORWARD        344  'to 344'
              342  END_FINALLY      
            344_0  COME_FROM           340  '340'
            344_1  COME_FROM           326  '326'

 L. 656       344  SETUP_EXCEPT        392  'to 392'

 L. 657       346  LOAD_GLOBAL              hasattr
              348  LOAD_FAST                'func'
              350  LOAD_STR                 '__func__'
              352  CALL_FUNCTION_2       2  '2 positional arguments'
          354_356  POP_JUMP_IF_FALSE   364  'to 364'

 L. 658       358  LOAD_FAST                'func'
              360  LOAD_ATTR                __func__
              362  STORE_FAST               'func'
            364_0  COME_FROM           354  '354'

 L. 659       364  LOAD_FAST                'func'
              366  LOAD_ATTR                __code__
              368  STORE_FAST               'code'

 L. 662       370  LOAD_FAST                'code'
              372  LOAD_ATTR                co_name
              374  STORE_FAST               'funcname'

 L. 663       376  LOAD_FAST                'code'
              378  LOAD_ATTR                co_firstlineno
              380  STORE_FAST               'lineno'

 L. 664       382  LOAD_FAST                'code'
              384  LOAD_ATTR                co_filename
              386  STORE_FAST               'filename'
              388  POP_BLOCK        
              390  JUMP_FORWARD        456  'to 456'
            392_0  COME_FROM_EXCEPT    344  '344'

 L. 665       392  POP_TOP          
              394  POP_TOP          
              396  POP_TOP          

 L. 667       398  LOAD_FAST                'self'
              400  LOAD_METHOD              lineinfo
              402  LOAD_FAST                'arg'
              404  CALL_METHOD_1         1  '1 positional argument'
              406  UNPACK_SEQUENCE_3     3 
              408  STORE_FAST               'ok'
              410  STORE_FAST               'filename'
              412  STORE_FAST               'ln'

 L. 668       414  LOAD_FAST                'ok'
          416_418  POP_JUMP_IF_TRUE    438  'to 438'

 L. 669       420  LOAD_FAST                'self'
              422  LOAD_METHOD              error
              424  LOAD_STR                 'The specified object %r is not a function or was not found along sys.path.'

 L. 670       426  LOAD_FAST                'arg'
              428  BINARY_MODULO    
              430  CALL_METHOD_1         1  '1 positional argument'
              432  POP_TOP          

 L. 671       434  LOAD_CONST               None
              436  RETURN_VALUE     
            438_0  COME_FROM           416  '416'

 L. 672       438  LOAD_FAST                'ok'
              440  STORE_FAST               'funcname'

 L. 673       442  LOAD_GLOBAL              int
              444  LOAD_FAST                'ln'
              446  CALL_FUNCTION_1       1  '1 positional argument'
              448  STORE_FAST               'lineno'
              450  POP_EXCEPT       
              452  JUMP_FORWARD        456  'to 456'
              454  END_FINALLY      
            456_0  COME_FROM           452  '452'
            456_1  COME_FROM           390  '390'
              456  POP_EXCEPT       
              458  JUMP_FORWARD        462  'to 462'
            460_0  COME_FROM           294  '294'
              460  END_FINALLY      
            462_0  COME_FROM           458  '458'
            462_1  COME_FROM           286  '286'
            462_2  COME_FROM           272  '272'

 L. 674       462  LOAD_FAST                'filename'
          464_466  POP_JUMP_IF_TRUE    476  'to 476'

 L. 675       468  LOAD_FAST                'self'
              470  LOAD_METHOD              defaultFile
              472  CALL_METHOD_0         0  '0 positional arguments'
              474  STORE_FAST               'filename'
            476_0  COME_FROM           464  '464'

 L. 677       476  LOAD_FAST                'self'
              478  LOAD_METHOD              checkline
              480  LOAD_FAST                'filename'
              482  LOAD_FAST                'lineno'
              484  CALL_METHOD_2         2  '2 positional arguments'
              486  STORE_FAST               'line'

 L. 678       488  LOAD_FAST                'line'
          490_492  POP_JUMP_IF_FALSE   572  'to 572'

 L. 680       494  LOAD_FAST                'self'
              496  LOAD_METHOD              set_break
              498  LOAD_FAST                'filename'
              500  LOAD_FAST                'line'
              502  LOAD_FAST                'temporary'
              504  LOAD_FAST                'cond'
              506  LOAD_FAST                'funcname'
              508  CALL_METHOD_5         5  '5 positional arguments'
              510  STORE_FAST               'err'

 L. 681       512  LOAD_FAST                'err'
          514_516  POP_JUMP_IF_FALSE   530  'to 530'

 L. 682       518  LOAD_FAST                'self'
              520  LOAD_METHOD              error
              522  LOAD_FAST                'err'
              524  CALL_METHOD_1         1  '1 positional argument'
              526  POP_TOP          
              528  JUMP_FORWARD        572  'to 572'
            530_0  COME_FROM           514  '514'

 L. 684       530  LOAD_FAST                'self'
              532  LOAD_METHOD              get_breaks
              534  LOAD_FAST                'filename'
              536  LOAD_FAST                'line'
              538  CALL_METHOD_2         2  '2 positional arguments'
              540  LOAD_CONST               -1
              542  BINARY_SUBSCR    
              544  STORE_FAST               'bp'

 L. 685       546  LOAD_FAST                'self'
              548  LOAD_METHOD              message
              550  LOAD_STR                 'Breakpoint %d at %s:%d'

 L. 686       552  LOAD_FAST                'bp'
              554  LOAD_ATTR                number
              556  LOAD_FAST                'bp'
              558  LOAD_ATTR                file
              560  LOAD_FAST                'bp'
              562  LOAD_ATTR                line
              564  BUILD_TUPLE_3         3 
              566  BINARY_MODULO    
              568  CALL_METHOD_1         1  '1 positional argument'
              570  POP_TOP          
            572_0  COME_FROM           528  '528'
            572_1  COME_FROM           490  '490'

Parse error at or near `LOAD_GLOBAL' instruction at offset 442

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
        idstring = identifier.split("'")
        if len(idstring) == 1:
            id = idstring[0].strip()
        elif len(idstring) == 3:
            id = idstring[1].strip()
        else:
            return failed
        if id == '':
            return failed
        parts = id.split('.')
        if parts[0] == 'self':
            del parts[0]
            if len(parts) == 0:
                return failed
        fname = self.defaultFile()
        if len(parts) == 1:
            item = parts[0]
        else:
            f = self.lookupmodule(parts[0])
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
            self.message('End of file')
            return 0
        line = line.strip()
        if line:
            if line[0] == '#' or (line[:3] == '"""' or line[:3] == "'''"):
                self.error('Blank or comment')
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
                bp = self.get_bpbynumber(i)
            except ValueError as err:
                try:
                    self.error(err)
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
                bp = self.get_bpbynumber(i)
            except ValueError as err:
                try:
                    self.error(err)
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

        try:
            bp = self.get_bpbynumber(args[0].strip())
        except IndexError:
            self.error('Breakpoint number expected')
        except ValueError as err:
            try:
                self.error(err)
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

        try:
            bp = self.get_bpbynumber(args[0].strip())
        except IndexError:
            self.error('Breakpoint number expected')
        except ValueError as err:
            try:
                self.error(err)
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

            reply = reply.strip().lower()
            if reply in ('y', 'yes'):
                bplist = [bp for bp in bdb.Breakpoint.bpbynumber if bp]
                self.clear_all_breaks()
                for bp in bplist:
                    self.message('Deleted %s' % bp)

            return
        if ':' in arg:
            i = arg.rfind(':')
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
                self.error(err)
            else:
                for bp in bplist:
                    self.message('Deleted %s' % bp)

            return
        numberlist = arg.split()
        for i in numberlist:
            try:
                bp = self.get_bpbynumber(i)
            except ValueError as err:
                try:
                    self.error(err)
                finally:
                    err = None
                    del err

            else:
                self.clear_bpbynumber(i)
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
        if not 0 <= number < len(self.stack):
            raise AssertionError
        self.curindex = number
        self.curframe = self.stack[self.curindex][0]
        self.curframe_locals = self.curframe.f_locals
        self.print_stack_entry(self.stack[self.curindex])
        self.lineno = None

    def do_up(self, arg):
        """u(p) [count]
        Move the current frame count (default one) levels up in the
        stack trace (to an older frame).
        """
        if self.curindex == 0:
            self.error('Oldest frame')
            return
        try:
            count = int(arg or 1)
        except ValueError:
            self.error('Invalid frame count (%s)' % arg)
            return
        else:
            if count < 0:
                newframe = 0
            else:
                newframe = max(0, self.curindex - count)
            self._select_frame(newframe)

    do_u = do_up

    def do_down(self, arg):
        """d(own) [count]
        Move the current frame count (default one) levels down in the
        stack trace (to a newer frame).
        """
        if self.curindex + 1 == len(self.stack):
            self.error('Newest frame')
            return
        try:
            count = int(arg or 1)
        except ValueError:
            self.error('Invalid frame count (%s)' % arg)
            return
        else:
            if count < 0:
                newframe = len(self.stack) - 1
            else:
                newframe = min(len(self.stack) - 1, self.curindex + count)
            self._select_frame(newframe)

    do_d = do_down

    def do_until(self, arg):
        """unt(il) [lineno]
        Without argument, continue execution until the line with a
        number greater than the current one is reached.  With a line
        number, continue execution until a line with a number greater
        or equal to that is reached.  In both cases, also stop when
        the current frame returns.
        """
        if arg:
            try:
                lineno = int(arg)
            except ValueError:
                self.error('Error in argument: %r' % arg)
                return
            else:
                if lineno <= self.curframe.f_lineno:
                    self.error('"until" line number is smaller than current line number')
                    return

        else:
            lineno = None
        self.set_until(self.curframe, lineno)
        return 1

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
        self.set_next(self.curframe)
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
            sys.argv = shlex.split(arg)
            sys.argv[:0] = argv0
        raise Restart

    do_restart = do_run

    def do_return(self, arg):
        """r(eturn)
        Continue execution until the current function returns.
        """
        self.set_return(self.curframe)
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
            self.error('You can only jump within the bottom frame')
            return
        try:
            arg = int(arg)
        except ValueError:
            self.error("The 'jump' command requires a line number")
        else:
            try:
                self.curframe.f_lineno = arg
                self.stack[self.curindex] = (self.stack[self.curindex][0], arg)
                self.print_stack_entry(self.stack[self.curindex])
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
        sys.settrace(None)
        globals = self.curframe.f_globals
        locals = self.curframe_locals
        p = Pdb(self.completekey, self.stdin, self.stdout)
        p.prompt = '(%s) ' % self.prompt.strip()
        self.message('ENTERING RECURSIVE DEBUGGER')
        try:
            sys.call_tracing(p.run, (arg, globals, locals))
        except Exception:
            exc_info = sys.exc_info()[:2]
            self.error((traceback.format_exception_only)(*exc_info)[(-1)].strip())

        self.message('LEAVING RECURSIVE DEBUGGER')
        sys.settrace(self.trace_dispatch)
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
        self.message('')
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
            self.message(repr(self.curframe_locals['__return__']))
        else:
            self.error('Not yet returned!')

    do_rv = do_retval

    def _getval(self, arg):
        try:
            return eval(arg, self.curframe.f_globals, self.curframe_locals)
        except:
            exc_info = sys.exc_info()[:2]
            self.error((traceback.format_exception_only)(*exc_info)[(-1)].strip())
            raise

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
            self.message(repr(self._getval(arg)))
        except:
            pass

    def do_pp(self, arg):
        """pp expression
        Pretty-print the value of the expression.
        """
        try:
            self.message(pprint.pformat(self._getval(arg)))
        except:
            pass

    complete_print = _complete_expression
    complete_p = _complete_expression
    complete_pp = _complete_expression

    def do_list(self, arg):
        """l(ist) [first [,last] | .]

        List source code for the current file.  Without arguments,
        list 11 lines around the current line or continue the previous
        listing.  With . as argument, list 11 lines around the current
        line.  With one argument, list 11 lines starting at that line.
        With two arguments, list the given range; if the second
        argument is less than the first, it is a count.

        The current line in the current frame is indicated by "->".
        If an exception is being debugged, the line where the
        exception was originally raised or propagated is indicated by
        ">>", if it differs from the current line.
        """
        self.lastcmd = 'list'
        last = None
        if arg and arg != '.':
            try:
                if ',' in arg:
                    first, last = arg.split(',')
                    first = int(first.strip())
                    last = int(last.strip())
                    if last < first:
                        last = first + last
                else:
                    first = int(arg.strip())
                    first = max(1, first - 5)
            except ValueError:
                self.error('Error in argument: %r' % arg)
                return

        elif self.lineno is None or arg == '.':
            first = max(1, self.curframe.f_lineno - 5)
        else:
            first = self.lineno + 1
        if last is None:
            last = first + 10
        filename = self.curframe.f_code.co_filename
        breaklist = self.get_file_breaks(filename)
        try:
            lines = linecache.getlines(filename, self.curframe.f_globals)
            self._print_lines(lines[first - 1:last], first, breaklist, self.curframe)
            self.lineno = min(last, len(lines))
            if len(lines) < last:
                self.message('[EOF]')
        except KeyboardInterrupt:
            pass

    do_l = do_list

    def do_longlist(self, arg):
        """longlist | ll
        List the whole source code for the current function or frame.
        """
        filename = self.curframe.f_code.co_filename
        breaklist = self.get_file_breaks(filename)
        try:
            lines, lineno = getsourcelines(self.curframe)
        except OSError as err:
            try:
                self.error(err)
                return
            finally:
                err = None
                del err

        self._print_lines(lines, lineno, breaklist, self.curframe)

    do_ll = do_longlist

    def do_source(self, arg):
        """source expression
        Try to get source code for the given object and display it.
        """
        try:
            obj = self._getval(arg)
        except:
            return
        else:
            try:
                lines, lineno = getsourcelines(obj)
            except (OSError, TypeError) as err:
                try:
                    self.error(err)
                    return
                finally:
                    err = None
                    del err

            self._print_lines(lines, lineno)

    complete_source = _complete_expression

    def _print_lines(self, lines, start, breaks=(), frame=None):
        """Print a range of lines."""
        if frame:
            current_lineno = frame.f_lineno
            exc_lineno = self.tb_lineno.get(frame, -1)
        else:
            current_lineno = exc_lineno = -1
        for lineno, line in enumerate(lines, start):
            s = str(lineno).rjust(3)
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

    def do_whatis(self, arg):
        """whatis arg
        Print the type of the argument.
        """
        try:
            value = self._getval(arg)
        except:
            return
        else:
            code = None
            try:
                code = value.__code__
            except Exception:
                pass

            if code:
                self.message('Function %s' % code.co_name)
                return
            try:
                code = value.__func__.__code__
            except Exception:
                pass

            if code:
                self.message('Method %s' % code.co_name)
                return
            if value.__class__ is type:
                self.message('Class %s.%s' % (value.__module__, value.__qualname__))
                return
            self.message(type(value))

    complete_whatis = _complete_expression

    def do_display(self, arg):
        """display [expression]

        Display the value of the expression if it changed, each time execution
        stops in the current frame.

        Without expression, list all display expressions for the current frame.
        """
        if not arg:
            self.message('Currently displaying:')
            for item in self.displaying.get(self.curframe, {}).items():
                self.message('%s: %r' % item)

        else:
            val = self._getval_except(arg)
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
        return [e for e in self.displaying.get(self.curframe, {}) if e.startswith(text)]

    def do_interact(self, arg):
        """interact

        Start an interactive interpreter whose global namespace
        contains all the (global and local) names found in the current scope.
        """
        ns = self.curframe.f_globals.copy()
        ns.update(self.curframe_locals)
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

            return
        if args[0] in self.aliases and len(args) == 1:
            self.message('%s = %s' % (args[0], self.aliases[args[0]]))
        else:
            self.aliases[args[0]] = ' '.join(args[1:])

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
        return [a for a in self.aliases if a.startswith(text)]

    commands_resuming = [
     'do_continue', 'do_step', 'do_next', 'do_return',
     'do_quit', 'do_jump']

    def print_stack_trace(self):
        try:
            for frame_lineno in self.stack:
                self.print_stack_entry(frame_lineno)

        except KeyboardInterrupt:
            pass

    def print_stack_entry(self, frame_lineno, prompt_prefix=line_prefix):
        frame, lineno = frame_lineno
        if frame is self.curframe:
            prefix = '> '
        else:
            prefix = '  '
        self.message(prefix + self.format_stack_entry(frame_lineno, prompt_prefix))

    def do_help(self, arg):
        """h(elp)
        Without argument, print the list of available commands.
        With a command name as argument, print help about that command.
        "help pdb" shows the full pdb documentation.
        "help exec" gives help on the ! command.
        """
        if not arg:
            return cmd.Cmd.do_help(self, arg)
        try:
            try:
                topic = getattr(self, 'help_' + arg)
                return topic()
            except AttributeError:
                command = getattr(self, 'do_' + arg)

        except AttributeError:
            self.error('No help for %r' % arg)
        else:
            if sys.flags.optimize >= 2:
                self.error('No help for %r; please do not run Python with -OO if you need command help' % arg)
                return
            self.message(command.__doc__.rstrip())

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
        self.message((self.help_exec.__doc__ or '').strip())

    def help_pdb(self):
        help()

    def lookupmodule(self, filename):
        """Helper function for break/clear parsing -- may be overridden.

        lookupmodule() translates (possibly incomplete) file or module name
        into an absolute file name.
        """
        if os.path.isabs(filename):
            if os.path.exists(filename):
                return filename
        f = os.path.join(sys.path[0], filename)
        if os.path.exists(f):
            if self.canonic(f) == self.mainpyfile:
                return f
        root, ext = os.path.splitext(filename)
        if ext == '':
            filename = filename + '.py'
        if os.path.isabs(filename):
            return filename
        for dirname in sys.path:
            while os.path.islink(dirname):
                dirname = os.readlink(dirname)

            fullname = os.path.join(dirname, filename)
            if os.path.exists(fullname):
                return fullname

    def _runmodule(self, module_name):
        self._wait_for_mainpyfile = True
        self._user_requested_quit = False
        import runpy
        mod_name, mod_spec, code = runpy._get_module_details(module_name)
        self.mainpyfile = self.canonic(code.co_filename)
        import __main__
        __main__.__dict__.clear()
        __main__.__dict__.update({'__name__':'__main__', 
         '__file__':self.mainpyfile, 
         '__package__':mod_spec.parent, 
         '__loader__':mod_spec.loader, 
         '__spec__':mod_spec, 
         '__builtins__':__builtins__})
        self.run(code)

    def _runscript(self, filename):
        import __main__
        __main__.__dict__.clear()
        __main__.__dict__.update({'__name__':'__main__',  '__file__':filename, 
         '__builtins__':__builtins__})
        self._wait_for_mainpyfile = True
        self.mainpyfile = self.canonic(filename)
        self._user_requested_quit = False
        with open(filename, 'rb') as fp:
            statement = "exec(compile(%r, %r, 'exec'))" % (
             fp.read(), self.mainpyfile)
        self.run(statement)


if __doc__ is not None:
    _help_order = [
     'help', 'where', 'down', 'up', 'break', 'tbreak', 'clear', 'disable',
     'enable', 'ignore', 'condition', 'commands', 'step', 'next', 'until',
     'jump', 'return', 'retval', 'run', 'continue', 'list', 'longlist',
     'args', 'p', 'pp', 'whatis', 'source', 'display', 'undisplay',
     'interact', 'alias', 'unalias', 'debug', 'quit']
    for _command in _help_order:
        __doc__ += getattr(Pdb, 'do_' + _command).__doc__.strip() + '\n\n'

    __doc__ += Pdb.help_exec.__doc__
    del _help_order
    del _command

def run(statement, globals=None, locals=None):
    Pdb().run(statement, globals, locals)


def runeval(expression, globals=None, locals=None):
    return Pdb().runeval(expression, globals, locals)


def runctx(statement, globals, locals):
    run(statement, globals, locals)


def runcall(*args, **kwds):
    return (Pdb().runcall)(*args, **kwds)


def set_trace(*, header=None):
    pdb = Pdb()
    if header is not None:
        pdb.message(header)
    pdb.set_trace(sys._getframe().f_back)


def post_mortem(t=None):
    if t is None:
        t = sys.exc_info()[2]
    if t is None:
        raise ValueError('A valid traceback must be passed if no exception is being handled')
    p = Pdb()
    p.reset()
    p.interaction(None, t)


def pm():
    post_mortem(sys.last_traceback)


TESTCMD = 'import x; x.main()'

def test():
    run(TESTCMD)


def help():
    import pydoc
    pydoc.pager(__doc__)


_usage = 'usage: pdb.py [-c command] ... [-m module | pyfile] [arg] ...\n\nDebug the Python program given by pyfile. Alternatively,\nan executable module or package to debug can be specified using\nthe -m switch.\n\nInitial commands are read from .pdbrc files in your home directory\nand in the current directory, if they exist.  Commands supplied with\n-c are executed after commands from .pdbrc files.\n\nTo let the script run until an exception occurs, use "-c continue".\nTo let the script run up to a given line X in the debugged file, use\n"-c \'until X\'".'

def main():
    import getopt
    opts, args = getopt.getopt(sys.argv[1:], 'mhc:', ['--help', '--command='])
    if not args:
        print(_usage)
        sys.exit(2)
    commands = []
    run_as_module = False
    for opt, optarg in opts:
        if opt in ('-h', '--help'):
            print(_usage)
            sys.exit()
        else:
            if opt in ('-c', '--command'):
                commands.append(optarg)
        if opt in ('-m', ):
            run_as_module = True

    mainpyfile = args[0]
    if not run_as_module:
        if not os.path.exists(mainpyfile):
            print('Error:', mainpyfile, 'does not exist')
            sys.exit(1)
    sys.argv[:] = args
    if not run_as_module:
        sys.path[0] = os.path.dirname(mainpyfile)
    pdb = Pdb()
    pdb.rcLines.extend(commands)
    while 1:
        try:
            if run_as_module:
                pdb._runmodule(mainpyfile)
            else:
                pdb._runscript(mainpyfile)
            if pdb._user_requested_quit:
                break
            else:
                print('The program finished and will be restarted')
        except Restart:
            print('Restarting', mainpyfile, 'with arguments:')
            print('\t' + ' '.join(args))
        except SystemExit:
            print('The program exited via sys.exit(). Exit status:', end=' ')
            print(sys.exc_info()[1])
        except SyntaxError:
            traceback.print_exc()
            sys.exit(1)
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