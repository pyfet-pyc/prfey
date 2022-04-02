# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: bdb.py
"""Debugger basics"""
import fnmatch, sys, os
from inspect import CO_GENERATOR, CO_COROUTINE, CO_ASYNC_GENERATOR
__all__ = [
 'BdbQuit', 'Bdb', 'Breakpoint']
GENERATOR_AND_COROUTINE_FLAGS = CO_GENERATOR | CO_COROUTINE | CO_ASYNC_GENERATOR

class BdbQuit(Exception):
    __doc__ = 'Exception to give up completely.'


class Bdb:
    __doc__ = 'Generic Python debugger base class.\n\n    This class takes care of details of the trace facility;\n    a derived class should implement user interaction.\n    The standard debugger class (pdb.Pdb) is an example.\n\n    The optional skip argument must be an iterable of glob-style\n    module name patterns.  The debugger will not step into frames\n    that originate in a module that matches one of these patterns.\n    Whether a frame is considered to originate in a certain module\n    is determined by the __name__ in the frame globals.\n    '

    def __init__(self, skip=None):
        self.skip = set(skip) if skip else None
        self.breaks = {}
        self.fncache = {}
        self.frame_returning = None

    def canonic(self, filename):
        """Return canonical form of filename.

        For real filenames, the canonical form is a case-normalized (on
        case insensitive filesystems) absolute path.  'Filenames' with
        angle brackets, such as "<stdin>", generated in interactive
        mode, are returned unchanged.
        """
        if filename == '<' + filename[1:-1] + '>':
            return filename
        canonic = self.fncache.get(filename)
        if not canonic:
            canonic = os.path.abspath(filename)
            canonic = os.path.normcase(canonic)
            self.fncache[filename] = canonic
        return canonic

    def reset(self):
        """Set values of attributes as ready to start debugging."""
        import linecache
        linecache.checkcache()
        self.botframe = None
        self._set_stopinfo(None, None)

    def trace_dispatch(self, frame, event, arg):
        """Dispatch a trace function for debugged frames based on the event.

        This function is installed as the trace function for debugged
        frames. Its return value is the new trace function, which is
        usually itself. The default implementation decides how to
        dispatch a frame, depending on the type of event (passed in as a
        string) that is about to be executed.

        The event can be one of the following:
            line: A new line of code is going to be executed.
            call: A function is about to be called or another code block
                  is entered.
            return: A function or other code block is about to return.
            exception: An exception has occurred.
            c_call: A C function is about to be called.
            c_return: A C function has returned.
            c_exception: A C function has raised an exception.

        For the Python events, specialized functions (see the dispatch_*()
        methods) are called.  For the C events, no action is taken.

        The arg parameter depends on the previous event.
        """
        if self.quitting:
            return
        if event == 'line':
            return self.dispatch_line(frame)
        if event == 'call':
            return self.dispatch_call(frame, arg)
        if event == 'return':
            return self.dispatch_return(frame, arg)
        if event == 'exception':
            return self.dispatch_exception(frame, arg)
        if event == 'c_call':
            return self.trace_dispatch
        if event == 'c_exception':
            return self.trace_dispatch
        if event == 'c_return':
            return self.trace_dispatch
        print('bdb.Bdb.dispatch: unknown debugging event:', repr(event))
        return self.trace_dispatch

    def dispatch_line(self, frame):
        """Invoke user function and return trace function for line event.

        If the debugger stops on the current line, invoke
        self.user_line(). Raise BdbQuit if self.quitting is set.
        Return self.trace_dispatch to continue tracing in this scope.
        """
        if self.stop_here(frame) or self.break_here(frame):
            self.user_line(frame)
            if self.quitting:
                raise BdbQuit
        return self.trace_dispatch

    def dispatch_call(self, frame, arg):
        """Invoke user function and return trace function for call event.

        If the debugger stops on this function call, invoke
        self.user_call(). Raise BbdQuit if self.quitting is set.
        Return self.trace_dispatch to continue tracing in this scope.
        """
        if self.botframe is None:
            self.botframe = frame.f_back
            return self.trace_dispatch
        else:
            if not self.stop_here(frame):
                if not self.break_anywhere(frame):
                    return
            if self.stopframe and frame.f_code.co_flags & GENERATOR_AND_COROUTINE_FLAGS:
                return self.trace_dispatch
        self.user_call(frame, arg)
        if self.quitting:
            raise BdbQuit
        return self.trace_dispatch

    def dispatch_return(self, frame, arg):
        """Invoke user function and return trace function for return event.

        If the debugger stops on this function return, invoke
        self.user_return(). Raise BdbQuit if self.quitting is set.
        Return self.trace_dispatch to continue tracing in this scope.
        """
        if self.stop_here(frame) or frame == self.returnframe:
            if self.stopframe:
                if frame.f_code.co_flags & GENERATOR_AND_COROUTINE_FLAGS:
                    return self.trace_dispatch
            else:
                try:
                    self.frame_returning = frame
                    self.user_return(frame, arg)
                finally:
                    self.frame_returning = None

                if self.quitting:
                    raise BdbQuit
                if self.stopframe is frame and self.stoplineno != -1:
                    self._set_stopinfo(None, None)
        return self.trace_dispatch

    def dispatch_exception(self, frame, arg):
        """Invoke user function and return trace function for exception event.

        If the debugger stops on this exception, invoke
        self.user_exception(). Raise BdbQuit if self.quitting is set.
        Return self.trace_dispatch to continue tracing in this scope.
        """
        if not (self.stop_here(frame)):
            self.user_exception(frame, arg)
            if self.quitting:
                raise BdbQuit
            else:
                if self.stopframe and frame is not self.stopframe and self.stopframe.f_code.co_flags & GENERATOR_AND_COROUTINE_FLAGS and arg[0] in (StopIteration, GeneratorExit):
                    self.user_exception(frame, arg)
                    if self.quitting:
                        raise BdbQuit
        return self.trace_dispatch

    def is_skipped_module(self, module_name):
        """Return True if module_name matches any skip pattern."""
        if module_name is None:
            return False
        for pattern in self.skip:
            if fnmatch.fnmatch(module_name, pattern):
                return True
            return False

    def stop_here(self, frame):
        """Return True if frame is below the starting frame in the stack."""
        if self.skip:
            if self.is_skipped_module(frame.f_globals.get('__name__')):
                return False
        else:
            if frame is self.stopframe:
                if self.stoplineno == -1:
                    return False
                return frame.f_lineno >= self.stoplineno
            return self.stopframe or True
        return False

    def break_here(self, frame):
        """Return True if there is an effective breakpoint for this line.

        Check for line or function breakpoint and if in effect.
        Delete temporary breakpoints if effective() says to.
        """
        filename = self.canonic(frame.f_code.co_filename)
        if filename not in self.breaks:
            return False
        lineno = frame.f_lineno
        if lineno not in self.breaks[filename]:
            lineno = frame.f_code.co_firstlineno
            if lineno not in self.breaks[filename]:
                return False
        bp, flag = effective(filename, lineno, frame)
        if bp:
            self.currentbp = bp.number
            if flag:
                if bp.temporary:
                    self.do_clear(str(bp.number))
            return True
        return False

    def do_clear(self, arg):
        """Remove temporary breakpoint.

        Must implement in derived classes or get NotImplementedError.
        """
        raise NotImplementedError('subclass of bdb must implement do_clear()')

    def break_anywhere(self, frame):
        """Return True if there is any breakpoint for frame's filename.
        """
        return self.canonic(frame.f_code.co_filename) in self.breaks

    def user_call(self, frame, argument_list):
        """Called if we might stop in a function."""
        pass

    def user_line(self, frame):
        """Called when we stop or break at a line."""
        pass

    def user_return(self, frame, return_value):
        """Called when a return trap is set here."""
        pass

    def user_exception(self, frame, exc_info):
        """Called when we stop on an exception."""
        pass

    def _set_stopinfo(self, stopframe, returnframe, stoplineno=0):
        """Set the attributes for stopping.

        If stoplineno is greater than or equal to 0, then stop at line
        greater than or equal to the stopline.  If stoplineno is -1, then
        don't stop at all.
        """
        self.stopframe = stopframe
        self.returnframe = returnframe
        self.quitting = False
        self.stoplineno = stoplineno

    def set_until(self, frame, lineno=None):
        """Stop when the line with the lineno greater than the current one is
        reached or when returning from current frame."""
        if lineno is None:
            lineno = frame.f_lineno + 1
        self._set_stopinfo(frame, frame, lineno)

    def set_step(self):
        """Stop after one line of code."""
        if self.frame_returning:
            caller_frame = self.frame_returning.f_back
            if caller_frame:
                if not caller_frame.f_trace:
                    caller_frame.f_trace = self.trace_dispatch
        self._set_stopinfo(None, None)

    def set_next(self, frame):
        """Stop on the next line in or below the given frame."""
        self._set_stopinfo(frame, None)

    def set_return(self, frame):
        """Stop when returning from the given frame."""
        if frame.f_code.co_flags & GENERATOR_AND_COROUTINE_FLAGS:
            self._set_stopinfo(frame, None, -1)
        else:
            self._set_stopinfo(frame.f_back, frame)

    def set_trace(self, frame=None):
        """Start debugging from frame.

        If frame is not specified, debugging starts from caller's frame.
        """
        if frame is None:
            frame = sys._getframe().f_back
        else:
            self.reset()
            while True:
                if frame:
                    frame.f_trace = self.trace_dispatch
                    self.botframe = frame
                    frame = frame.f_back

        self.set_step()
        sys.settrace(self.trace_dispatch)

    def set_continue(self):
        """Stop only at breakpoints or when finished.

        If there are no breakpoints, set the system trace function to None.
        """
        self._set_stopinfo(self.botframe, None, -1)
        if not self.breaks:
            sys.settrace(None)
            frame = sys._getframe().f_back
            while frame:
                if frame is not self.botframe:
                    del frame.f_trace
                    frame = frame.f_back

    def set_quit(self):
        """Set quitting attribute to True.

        Raises BdbQuit exception in the next call to a dispatch_*() method.
        """
        self.stopframe = self.botframe
        self.returnframe = None
        self.quitting = True
        sys.settrace(None)

    def set_break(self, filename, lineno, temporary=False, cond=None, funcname=None):
        """Set a new breakpoint for filename:lineno.

        If lineno doesn't exist for the filename, return an error message.
        The filename should be in canonical form.
        """
        filename = self.canonic(filename)
        import linecache
        line = linecache.getline(filename, lineno)
        if not line:
            return 'Line %s:%d does not exist' % (filename, lineno)
        list = self.breaks.setdefault(filename, [])
        if lineno not in list:
            list.append(lineno)
        bp = Breakpoint(filename, lineno, temporary, cond, funcname)

    def _prune_breaks(self, filename, lineno):
        """Prune breakpoints for filename:lineno.

        A list of breakpoints is maintained in the Bdb instance and in
        the Breakpoint class.  If a breakpoint in the Bdb instance no
        longer exists in the Breakpoint class, then it's removed from the
        Bdb instance.
        """
        if (
         filename, lineno) not in Breakpoint.bplist:
            self.breaks[filename].remove(lineno)
        if not self.breaks[filename]:
            del self.breaks[filename]

    def clear_break(self, filename, lineno):
        """Delete breakpoints for filename:lineno.

        If no breakpoints were set, return an error message.
        """
        filename = self.canonic(filename)
        if filename not in self.breaks:
            return 'There are no breakpoints in %s' % filename
        if lineno not in self.breaks[filename]:
            return 'There is no breakpoint at %s:%d' % (filename, lineno)
        for bp in Breakpoint.bplist[(filename, lineno)][:]:
            bp.deleteMe()
        else:
            self._prune_breaks(filename, lineno)

    def clear_bpbynumber(self, arg):
        """Delete a breakpoint by its index in Breakpoint.bpbynumber.

        If arg is invalid, return an error message.
        """
        try:
            bp = self.get_bpbynumber(arg)
        except ValueError as err:
            return str(err)
        else:
            bp.deleteMe()
            self._prune_breaks(bp.file, bp.line)

    def clear_all_file_breaks(self, filename):
        """Delete all breakpoints in filename.

        If none were set, return an error message.
        """
        filename = self.canonic(filename)
        if filename not in self.breaks:
            return 'There are no breakpoints in %s' % filename
        for line in self.breaks[filename]:
            blist = Breakpoint.bplist[(filename, line)]
            for bp in blist:
                bp.deleteMe()
            else:
                del self.breaks[filename]

    def clear_all_breaks(self):
        """Delete all existing breakpoints.

        If none were set, return an error message.
        """
        if not self.breaks:
            return 'There are no breakpoints'
        for bp in Breakpoint.bpbynumber:
            if bp:
                bp.deleteMe()
            self.breaks = {}

    def get_bpbynumber(self, arg):
        """Return a breakpoint by its index in Breakpoint.bybpnumber.

        For invalid arg values or if the breakpoint doesn't exist,
        raise a ValueError.
        """
        if not arg:
            raise ValueError('Breakpoint number expected')
        try:
            number = int(arg)
        except ValueError:
            raise ValueError('Non-numeric breakpoint number %s' % arg) from None
        else:
            try:
                bp = Breakpoint.bpbynumber[number]
            except IndexError:
                raise ValueError('Breakpoint number %d out of range' % number) from None
            else:
                if bp is None:
                    raise ValueError('Breakpoint %d already deleted' % number)
                return bp

    def get_break(self, filename, lineno):
        """Return True if there is a breakpoint for filename:lineno."""
        filename = self.canonic(filename)
        return filename in self.breaks and lineno in self.breaks[filename]

    def get_breaks(self, filename, lineno):
        """Return all breakpoints for filename:lineno.

        If no breakpoints are set, return an empty list.
        """
        filename = self.canonic(filename)
        return filename in self.breaks and lineno in self.breaks[filename] and Breakpoint.bplist[(filename, lineno)] or []

    def get_file_breaks(self, filename):
        """Return all lines with breakpoints for filename.

        If no breakpoints are set, return an empty list.
        """
        filename = self.canonic(filename)
        if filename in self.breaks:
            return self.breaks[filename]
        return []

    def get_all_breaks(self):
        """Return all breakpoints that are set."""
        return self.breaks

    def get_stack(self, f, t):
        """Return a list of (frame, lineno) in a stack trace and a size.

        List starts with original calling frame, if there is one.
        Size may be number of frames above or below f.
        """
        stack = []
        if t and t.tb_frame is f:
            t = t.tb_next
        else:
            while f is not None:
                stack.append((f, f.f_lineno))
                if f is self.botframe:
                    break
                f = f.f_back

            stack.reverse()
            i = max(0, len(stack) - 1)
            while True:
                if t is not None:
                    stack.append((t.tb_frame, t.tb_lineno))
                    t = t.tb_next

        if f is None:
            i = max(0, len(stack) - 1)
        return (
         stack, i)

    def format_stack_entry(self, frame_lineno, lprefix=': '):
        """Return a string with information about a stack entry.

        The stack entry frame_lineno is a (frame, lineno) tuple.  The
        return string contains the canonical filename, the function name
        or '<lambda>', the input arguments, the return value, and the
        line of code (if it exists).

        """
        import linecache, reprlib
        frame, lineno = frame_lineno
        filename = self.canonic(frame.f_code.co_filename)
        s = '%s(%r)' % (filename, lineno)
        if frame.f_code.co_name:
            s += frame.f_code.co_name
        else:
            s += '<lambda>'
        s += '()'
        if '__return__' in frame.f_locals:
            rv = frame.f_locals['__return__']
            s += '->'
            s += reprlib.repr(rv)
        line = linecache.getline(filename, lineno, frame.f_globals)
        if line:
            s += lprefix + line.strip()
        return s

    def run(self, cmd, globals=None, locals=None):
        """Debug a statement executed via the exec() function.

        globals defaults to __main__.dict; locals defaults to globals.
        """
        if globals is None:
            import __main__
            globals = __main__.__dict__
        if locals is None:
            locals = globals
        self.reset()
        if isinstance(cmd, str):
            cmd = compile(cmd, '<string>', 'exec')
        sys.settrace(self.trace_dispatch)
        try:
            try:
                exec(cmd, globals, locals)
            except BdbQuit:
                pass

        finally:
            self.quitting = True
            sys.settrace(None)

    def runeval--- This code section failed: ---

 L. 592         0  LOAD_FAST                'globals'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 593         8  LOAD_CONST               0
               10  LOAD_CONST               None
               12  IMPORT_NAME              __main__
               14  STORE_FAST               '__main__'

 L. 594        16  LOAD_FAST                '__main__'
               18  LOAD_ATTR                __dict__
               20  STORE_FAST               'globals'
             22_0  COME_FROM             6  '6'

 L. 595        22  LOAD_FAST                'locals'
               24  LOAD_CONST               None
               26  COMPARE_OP               is
               28  POP_JUMP_IF_FALSE    34  'to 34'

 L. 596        30  LOAD_FAST                'globals'
               32  STORE_FAST               'locals'
             34_0  COME_FROM            28  '28'

 L. 597        34  LOAD_FAST                'self'
               36  LOAD_METHOD              reset
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L. 598        42  LOAD_GLOBAL              sys
               44  LOAD_METHOD              settrace
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                trace_dispatch
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 599        54  SETUP_FINALLY       100  'to 100'
               56  SETUP_FINALLY        76  'to 76'

 L. 600        58  LOAD_GLOBAL              eval
               60  LOAD_FAST                'expr'
               62  LOAD_FAST                'globals'
               64  LOAD_FAST                'locals'
               66  CALL_FUNCTION_3       3  ''
               68  POP_BLOCK        
               70  POP_BLOCK        
               72  CALL_FINALLY        100  'to 100'
               74  RETURN_VALUE     
             76_0  COME_FROM_FINALLY    56  '56'

 L. 601        76  DUP_TOP          
               78  LOAD_GLOBAL              BdbQuit
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE    94  'to 94'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 602        90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
             94_0  COME_FROM            82  '82'
               94  END_FINALLY      
             96_0  COME_FROM            92  '92'
               96  POP_BLOCK        
               98  BEGIN_FINALLY    
            100_0  COME_FROM            72  '72'
            100_1  COME_FROM_FINALLY    54  '54'

 L. 604       100  LOAD_CONST               True
              102  LOAD_FAST                'self'
              104  STORE_ATTR               quitting

 L. 605       106  LOAD_GLOBAL              sys
              108  LOAD_METHOD              settrace
              110  LOAD_CONST               None
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
              116  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 70

    def runctx(self, cmd, globals, locals):
        """For backwards-compatibility.  Defers to run()."""
        self.run(cmd, globals, locals)

    def runcall(*args, **kwds):
        """Debug a single function call.

        Return the result of the function call.
        """
        if len(args) >= 2:
            self, func, *args = args
        else:
            if not args:
                raise TypeError("descriptor 'runcall' of 'Bdb' object needs an argument")
            else:
                if 'func' in kwds:
                    func = kwds.pop('func')
                    self, *args = args
                    import warnings
                    warnings.warn("Passing 'func' as keyword argument is deprecated", DeprecationWarning,
                      stacklevel=2)
                else:
                    raise TypeError('runcall expected at least 1 positional argument, got %d' % (len(args) - 1))
        self.reset()
        sys.settrace(self.trace_dispatch)
        res = None
        try:
            try:
                res = func(*args, **kwds)
            except BdbQuit:
                pass

        finally:
            self.quitting = True
            sys.settrace(None)

        return res

    runcall.__text_signature__ = '($self, func, /, *args, **kwds)'


def set_trace():
    """Start debugging with a Bdb instance from the caller's frame."""
    Bdb().set_trace()


class Breakpoint:
    __doc__ = 'Breakpoint class.\n\n    Implements temporary breakpoints, ignore counts, disabling and\n    (re)-enabling, and conditionals.\n\n    Breakpoints are indexed by number through bpbynumber and by\n    the (file, line) tuple using bplist.  The former points to a\n    single instance of class Breakpoint.  The latter points to a\n    list of such instances since there may be more than one\n    breakpoint per line.\n\n    When creating a breakpoint, its associated filename should be\n    in canonical form.  If funcname is defined, a breakpoint hit will be\n    counted when the first line of that function is executed.  A\n    conditional breakpoint always counts a hit.\n    '
    next = 1
    bplist = {}
    bpbynumber = [None]

    def __init__(self, file, line, temporary=False, cond=None, funcname=None):
        self.funcname = funcname
        self.func_first_executable_line = None
        self.file = file
        self.line = line
        self.temporary = temporary
        self.cond = cond
        self.enabled = True
        self.ignore = 0
        self.hits = 0
        self.number = Breakpoint.next
        Breakpoint.next += 1
        self.bpbynumber.append(self)
        if (file, line) in self.bplist:
            self.bplist[(file, line)].append(self)
        else:
            self.bplist[(file, line)] = [
             self]

    def deleteMe(self):
        """Delete the breakpoint from the list associated to a file:line.

        If it is the last breakpoint in that position, it also deletes
        the entry for the file:line.
        """
        index = (
         self.file, self.line)
        self.bpbynumber[self.number] = None
        self.bplist[index].remove(self)
        if not self.bplist[index]:
            del self.bplist[index]

    def enable(self):
        """Mark the breakpoint as enabled."""
        self.enabled = True

    def disable(self):
        """Mark the breakpoint as disabled."""
        self.enabled = False

    def bpprint(self, out=None):
        """Print the output of bpformat().

        The optional out argument directs where the output is sent
        and defaults to standard output.
        """
        if out is None:
            out = sys.stdout
        print((self.bpformat()), file=out)

    def bpformat(self):
        """Return a string with information about the breakpoint.

        The information includes the breakpoint number, temporary
        status, file:line position, break condition, number of times to
        ignore, and number of times hit.

        """
        if self.temporary:
            disp = 'del  '
        else:
            disp = 'keep '
        if self.enabled:
            disp = disp + 'yes  '
        else:
            disp = disp + 'no   '
        ret = '%-4dbreakpoint   %s at %s:%d' % (self.number, disp,
         self.file, self.line)
        if self.cond:
            ret += '\n\tstop only if %s' % (self.cond,)
        if self.ignore:
            ret += '\n\tignore next %d hits' % (self.ignore,)
        if self.hits:
            if self.hits > 1:
                ss = 's'
            else:
                ss = ''
            ret += '\n\tbreakpoint already hit %d time%s' % (self.hits, ss)
        return ret

    def __str__(self):
        """Return a condensed description of the breakpoint."""
        return 'breakpoint %s at %s:%s' % (self.number, self.file, self.line)


def checkfuncname(b, frame):
    """Return True if break should happen here.

    Whether a break should happen depends on the way that b (the breakpoint)
    was set.  If it was set via line number, check if b.line is the same as
    the one in the frame.  If it was set via function name, check if this is
    the right function and if it is on the first executable line.
    """
    if not b.funcname:
        if b.line != frame.f_lineno:
            return False
    else:
        return True
        if frame.f_code.co_name != b.funcname:
            return False
        b.func_first_executable_line = b.func_first_executable_line or frame.f_lineno
    if b.func_first_executable_line != frame.f_lineno:
        return False
    return True


def effective--- This code section failed: ---

 L. 811         0  LOAD_GLOBAL              Breakpoint
                2  LOAD_ATTR                bplist
                4  LOAD_FAST                'file'
                6  LOAD_FAST                'line'
                8  BUILD_TUPLE_2         2 
               10  BINARY_SUBSCR    
               12  STORE_FAST               'possibles'

 L. 812        14  LOAD_FAST                'possibles'
               16  GET_ITER         
               18  FOR_ITER            198  'to 198'
               20  STORE_FAST               'b'

 L. 813        22  LOAD_FAST                'b'
               24  LOAD_ATTR                enabled
               26  POP_JUMP_IF_TRUE     30  'to 30'

 L. 814        28  JUMP_BACK            18  'to 18'
             30_0  COME_FROM            26  '26'

 L. 815        30  LOAD_GLOBAL              checkfuncname
               32  LOAD_FAST                'b'
               34  LOAD_FAST                'frame'
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_TRUE     42  'to 42'

 L. 816        40  JUMP_BACK            18  'to 18'
             42_0  COME_FROM            38  '38'

 L. 818        42  LOAD_FAST                'b'
               44  DUP_TOP          
               46  LOAD_ATTR                hits
               48  LOAD_CONST               1
               50  INPLACE_ADD      
               52  ROT_TWO          
               54  STORE_ATTR               hits

 L. 819        56  LOAD_FAST                'b'
               58  LOAD_ATTR                cond
               60  POP_JUMP_IF_TRUE    104  'to 104'

 L. 821        62  LOAD_FAST                'b'
               64  LOAD_ATTR                ignore
               66  LOAD_CONST               0
               68  COMPARE_OP               >
               70  POP_JUMP_IF_FALSE    90  'to 90'

 L. 822        72  LOAD_FAST                'b'
               74  DUP_TOP          
               76  LOAD_ATTR                ignore
               78  LOAD_CONST               1
               80  INPLACE_SUBTRACT 
               82  ROT_TWO          
               84  STORE_ATTR               ignore

 L. 823        86  JUMP_BACK            18  'to 18'
               88  JUMP_ABSOLUTE       196  'to 196'
             90_0  COME_FROM            70  '70'

 L. 826        90  LOAD_FAST                'b'
               92  LOAD_CONST               True
               94  BUILD_TUPLE_2         2 
               96  ROT_TWO          
               98  POP_TOP          
              100  RETURN_VALUE     
              102  JUMP_BACK            18  'to 18'
            104_0  COME_FROM            60  '60'

 L. 831       104  SETUP_FINALLY       172  'to 172'

 L. 832       106  LOAD_GLOBAL              eval
              108  LOAD_FAST                'b'
              110  LOAD_ATTR                cond
              112  LOAD_FAST                'frame'
              114  LOAD_ATTR                f_globals
              116  LOAD_FAST                'frame'
              118  LOAD_ATTR                f_locals
              120  CALL_FUNCTION_3       3  ''
              122  STORE_FAST               'val'

 L. 833       124  LOAD_FAST                'val'
              126  POP_JUMP_IF_FALSE   168  'to 168'

 L. 834       128  LOAD_FAST                'b'
              130  LOAD_ATTR                ignore
              132  LOAD_CONST               0
              134  COMPARE_OP               >
              136  POP_JUMP_IF_FALSE   154  'to 154'

 L. 835       138  LOAD_FAST                'b'
              140  DUP_TOP          
              142  LOAD_ATTR                ignore
              144  LOAD_CONST               1
              146  INPLACE_SUBTRACT 
              148  ROT_TWO          
              150  STORE_ATTR               ignore
              152  JUMP_FORWARD        168  'to 168'
            154_0  COME_FROM           136  '136'

 L. 838       154  LOAD_FAST                'b'
              156  LOAD_CONST               True
              158  BUILD_TUPLE_2         2 
              160  POP_BLOCK        
              162  ROT_TWO          
              164  POP_TOP          
              166  RETURN_VALUE     
            168_0  COME_FROM           152  '152'
            168_1  COME_FROM           126  '126'
              168  POP_BLOCK        
              170  JUMP_BACK            18  'to 18'
            172_0  COME_FROM_FINALLY   104  '104'

 L. 841       172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L. 845       178  LOAD_FAST                'b'
              180  LOAD_CONST               False
              182  BUILD_TUPLE_2         2 
              184  ROT_FOUR         
              186  POP_EXCEPT       
              188  ROT_TWO          
              190  POP_TOP          
              192  RETURN_VALUE     
              194  END_FINALLY      
              196  JUMP_BACK            18  'to 18'

 L. 846       198  LOAD_CONST               (None, None)
              200  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 88


class Tdb(Bdb):

    def user_call(self, frame, args):
        name = frame.f_code.co_name
        if not name:
            name = '???'
        print('+++ call', name, args)

    def user_line(self, frame):
        import linecache
        name = frame.f_code.co_name
        if not name:
            name = '???'
        fn = self.canonic(frame.f_code.co_filename)
        line = linecache.getline(fn, frame.f_lineno, frame.f_globals)
        print('+++', fn, frame.f_lineno, name, ':', line.strip())

    def user_return(self, frame, retval):
        print('+++ return', retval)

    def user_exception(self, frame, exc_stuff):
        print('+++ exception', exc_stuff)
        self.set_continue()


def foo(n):
    print('foo(', n, ')')
    x = bar(n * 10)
    print('bar returned', x)


def bar(a):
    print('bar(', a, ')')
    return a / 2


def test():
    t = Tdb()
    t.run('import bdb; bdb.foo(10)')