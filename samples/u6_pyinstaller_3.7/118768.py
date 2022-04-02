# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
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
                    return (
                     funcname, filename, lineno)


def getsourcelines(obj):
    lines, lineno = inspect.findsource(obj)
    if inspect.isframe(obj):
        if obj.f_globals is obj.f_locals:
            return (
             lines, 1)
    if inspect.ismodule(obj):
        return (
         lines, 1)
    return (
     inspect.getblock(lines[lineno:]), lineno + 1)


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
            try:
                with open(os.path.expanduser('~/.pdbrc')) as (rcFile):
                    self.rcLines.extend(rcFile)
            except OSError:
                pass

            try:
                with open('.pdbrc') as (rcFile):
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
            if line and line[0] != '#' and self.onecmd(line):
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
            if self.mainpyfile != self.canonic(frame.f_code.co_filename) or frame.f_lineno <= 0:
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

    def user_exception--- This code section failed: ---

 L. 296         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _wait_for_mainpyfile
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 297         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 298        10  LOAD_FAST                'exc_info'
               12  UNPACK_SEQUENCE_3     3 
               14  STORE_FAST               'exc_type'
               16  STORE_FAST               'exc_value'
               18  STORE_FAST               'exc_traceback'

 L. 299        20  LOAD_FAST                'exc_type'
               22  LOAD_FAST                'exc_value'
               24  BUILD_TUPLE_2         2 
               26  LOAD_FAST                'frame'
               28  LOAD_ATTR                f_locals
               30  LOAD_STR                 '__exception__'
               32  STORE_SUBSCR     

 L. 306        34  LOAD_FAST                'exc_traceback'
               36  POP_JUMP_IF_TRUE     50  'to 50'

 L. 307        38  LOAD_FAST                'exc_type'
               40  LOAD_GLOBAL              StopIteration
               42  COMPARE_OP               is
               44  POP_JUMP_IF_FALSE    50  'to 50'
               46  LOAD_STR                 'Internal '
               48  JUMP_FORWARD         52  'to 52'
             50_0  COME_FROM            44  '44'
             50_1  COME_FROM            36  '36'
               50  LOAD_STR                 ''
             52_0  COME_FROM            48  '48'
               52  STORE_FAST               'prefix'

 L. 308        54  LOAD_FAST                'self'
               56  LOAD_METHOD              message
               58  LOAD_STR                 '%s%s'
               60  LOAD_FAST                'prefix'

 L. 309        62  LOAD_GLOBAL              traceback
               64  LOAD_METHOD              format_exception_only
               66  LOAD_FAST                'exc_type'
               68  LOAD_FAST                'exc_value'
               70  CALL_METHOD_2         2  '2 positional arguments'
               72  LOAD_CONST               -1
               74  BINARY_SUBSCR    
               76  LOAD_METHOD              strip
               78  CALL_METHOD_0         0  '0 positional arguments'
               80  BUILD_TUPLE_2         2 
               82  BINARY_MODULO    
               84  CALL_METHOD_1         1  '1 positional argument'
               86  POP_TOP          

 L. 310        88  LOAD_FAST                'self'
               90  LOAD_METHOD              interaction
               92  LOAD_FAST                'frame'
               94  LOAD_FAST                'exc_traceback'
               96  CALL_METHOD_2         2  '2 positional arguments'
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
                self.message('--KeyboardInterrupt--')

    def preloop(self):
        displaying = self.displaying.get(self.curframe)
        if displaying:
            for expr, oldvalue in displaying.items():
                newvalue = self._getval_except(expr)
                if newvalue is not oldvalue and newvalue != oldvalue:
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
            else:
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

    def do_break(self, arg, temporary=0):
        """b(reak) [ ([filename:]lineno | function) [, condition] ]
        Without argument, list all breaks.

        With a line number argument, set a break at this line in the
        current file.  With a function name, set a break at the first
        executable line of that function.  If a second argument is
        present, it is a string specifying an expression which must
        evaluate to true before the breakpoint is honored.

        The line number may be prefixed with a filename and a colon,
        to specify a breakpoint in another file (probably one that
        hasn't been loaded yet).  The file is searched for on
        sys.path; the .py suffix may be omitted.
        """
        if not arg:
            if self.breaks:
                self.message('Num Type         Disp Enb   Where')
                for bp in bdb.Breakpoint.bpbynumber:
                    if bp:
                        self.message(bp.bpformat())

            return
            filename = None
            lineno = None
            cond = None
            comma = arg.find(',')
            if comma > 0:
                cond = arg[comma + 1:].lstrip()
                arg = arg[:comma].rstrip()
            colon = arg.rfind(':')
            funcname = None
            if colon >= 0:
                filename = arg[:colon].rstrip()
                f = self.lookupmodule(filename)
                if not f:
                    self.error('%r not found from sys.path' % filename)
                    return
            else:
                filename = f
                arg = arg[colon + 1:].lstrip()
                try:
                    lineno = int(arg)
                except ValueError:
                    self.error('Bad lineno: %s' % arg)
                    return

        else:
            try:
                lineno = int(arg)
            except ValueError:
                try:
                    func = eval(arg, self.curframe.f_globals, self.curframe_locals)
                except:
                    func = arg

                try:
                    if hasattr(func, '__func__'):
                        func = func.__func__
                    code = func.__code__
                    funcname = code.co_name
                    lineno = code.co_firstlineno
                    filename = code.co_filename
                except:
                    ok, filename, ln = self.lineinfo(arg)
                    if not ok:
                        self.error('The specified object %r is not a function or was not found along sys.path.' % arg)
                        return
                    funcname = ok
                    lineno = int(ln)

            if not filename:
                filename = self.defaultFile()
            line = self.checkline(filename, lineno)
            if line:
                err = self.set_break(filename, line, temporary, cond, funcname)
                if err:
                    self.error(err)
                else:
                    bp = self.get_breaks(filename, line)[(-1)]
                    self.message('Breakpoint %d at %s:%d' % (
                     bp.number, bp.file, bp.line))

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
        else:
            if len(idstring) == 3:
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

    def checkline--- This code section failed: ---

 L. 749         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'self'
                4  LOAD_STR                 'curframe'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    18  'to 18'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                curframe
               14  LOAD_ATTR                f_globals
               16  JUMP_FORWARD         20  'to 20'
             18_0  COME_FROM             8  '8'
               18  LOAD_CONST               None
             20_0  COME_FROM            16  '16'
               20  STORE_FAST               'globs'

 L. 750        22  LOAD_GLOBAL              linecache
               24  LOAD_METHOD              getline
               26  LOAD_FAST                'filename'
               28  LOAD_FAST                'lineno'
               30  LOAD_FAST                'globs'
               32  CALL_METHOD_3         3  '3 positional arguments'
               34  STORE_FAST               'line'

 L. 751        36  LOAD_FAST                'line'
               38  POP_JUMP_IF_TRUE     54  'to 54'

 L. 752        40  LOAD_FAST                'self'
               42  LOAD_METHOD              message
               44  LOAD_STR                 'End of file'
               46  CALL_METHOD_1         1  '1 positional argument'
               48  POP_TOP          

 L. 753        50  LOAD_CONST               0
               52  RETURN_VALUE     
             54_0  COME_FROM            38  '38'

 L. 754        54  LOAD_FAST                'line'
               56  LOAD_METHOD              strip
               58  CALL_METHOD_0         0  '0 positional arguments'
               60  STORE_FAST               'line'

 L. 756        62  LOAD_FAST                'line'
               64  POP_JUMP_IF_FALSE   110  'to 110'
               66  LOAD_FAST                'line'
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  LOAD_STR                 '#'
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_TRUE    110  'to 110'

 L. 757        78  LOAD_FAST                'line'
               80  LOAD_CONST               None
               82  LOAD_CONST               3
               84  BUILD_SLICE_2         2 
               86  BINARY_SUBSCR    
               88  LOAD_STR                 '"""'
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_TRUE    110  'to 110'
               94  LOAD_FAST                'line'
               96  LOAD_CONST               None
               98  LOAD_CONST               3
              100  BUILD_SLICE_2         2 
              102  BINARY_SUBSCR    
              104  LOAD_STR                 "'''"
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   124  'to 124'
            110_0  COME_FROM            92  '92'
            110_1  COME_FROM            76  '76'
            110_2  COME_FROM            64  '64'

 L. 758       110  LOAD_FAST                'self'
              112  LOAD_METHOD              error
              114  LOAD_STR                 'Blank or comment'
              116  CALL_METHOD_1         1  '1 positional argument'
              118  POP_TOP          

 L. 759       120  LOAD_CONST               0
              122  RETURN_VALUE     
            124_0  COME_FROM           108  '108'

 L. 760       124  LOAD_FAST                'lineno'
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
        assert 0 <= number < len(self.stack)
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

        else:
            if self.lineno is None or arg == '.':
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
                else:
                    if lineno == exc_lineno:
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
        with open(filename, 'rb') as (fp):
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
    Pdb().runstatementglobalslocals


def runeval(expression, globals=None, locals=None):
    return Pdb().runevalexpressionglobalslocals


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
    opts, args = getopt.getoptsys.argv[1:]'mhc:'['help', 'command=']
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
    while True:
        try:
            if run_as_module:
                pdb._runmodule(mainpyfile)
            else:
                pdb._runscript(mainpyfile)
            if pdb._user_requested_quit:
                break
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