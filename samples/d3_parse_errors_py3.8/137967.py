# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: code.py
"""Utilities needed to emulate Python's interactive interpreter.

"""
import sys, traceback
from codeop import CommandCompiler, compile_command
__all__ = [
 'InteractiveInterpreter', 'InteractiveConsole', 'interact',
 'compile_command']

class InteractiveInterpreter:
    __doc__ = "Base class for InteractiveConsole.\n\n    This class deals with parsing and interpreter state (the user's\n    namespace); it doesn't deal with input buffering or prompting or\n    input file naming (the filename is always passed in explicitly).\n\n    "

    def __init__(self, locals=None):
        """Constructor.

        The optional 'locals' argument specifies the dictionary in
        which code will be executed; it defaults to a newly created
        dictionary with key "__name__" set to "__console__" and key
        "__doc__" set to None.

        """
        if locals is None:
            locals = {'__name__':'__console__', 
             '__doc__':None}
        self.locals = locals
        self.compile = CommandCompiler()

    def runsource--- This code section failed: ---

 L.  62         0  SETUP_FINALLY        20  'to 20'

 L.  63         2  LOAD_FAST                'self'
                4  LOAD_METHOD              compile
                6  LOAD_FAST                'source'
                8  LOAD_FAST                'filename'
               10  LOAD_FAST                'symbol'
               12  CALL_METHOD_3         3  ''
               14  STORE_FAST               'code'
               16  POP_BLOCK        
               18  JUMP_FORWARD         58  'to 58'
             20_0  COME_FROM_FINALLY     0  '0'

 L.  64        20  DUP_TOP          
               22  LOAD_GLOBAL              OverflowError
               24  LOAD_GLOBAL              SyntaxError
               26  LOAD_GLOBAL              ValueError
               28  BUILD_TUPLE_3         3 
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    56  'to 56'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  66        40  LOAD_FAST                'self'
               42  LOAD_METHOD              showsyntaxerror
               44  LOAD_FAST                'filename'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L.  67        50  POP_EXCEPT       
               52  LOAD_CONST               False
               54  RETURN_VALUE     
             56_0  COME_FROM            32  '32'
               56  END_FINALLY      
             58_0  COME_FROM            18  '18'

 L.  69        58  LOAD_FAST                'code'
               60  LOAD_CONST               None
               62  COMPARE_OP               is
               64  POP_JUMP_IF_FALSE    70  'to 70'

 L.  71        66  LOAD_CONST               True
               68  RETURN_VALUE     
             70_0  COME_FROM            64  '64'

 L.  74        70  LOAD_FAST                'self'
               72  LOAD_METHOD              runcode
               74  LOAD_FAST                'code'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L.  75        80  LOAD_CONST               False
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 52

    def runcode(self, code):
        """Execute a code object.

        When an exception occurs, self.showtraceback() is called to
        display a traceback.  All exceptions are caught except
        SystemExit, which is reraised.

        A note about KeyboardInterrupt: this exception may occur
        elsewhere in this code, and may not always be caught.  The
        caller should be prepared to deal with it.

        """
        try:
            exec(code, self.locals)
        except SystemExit:
            raise
        except:
            self.showtraceback()

    def showsyntaxerror(self, filename=None):
        """Display the syntax error that just occurred.

        This doesn't display a stack trace because there isn't one.

        If a filename is given, it is stuffed in the exception instead
        of what was there before (because Python's parser always uses
        "<string>" when reading from a string).

        The output is written by self.write(), below.

        """
        type, value, tb = sys.exc_info()
        sys.last_type = type
        sys.last_value = value
        sys.last_traceback = tb
        if not filename or type is SyntaxError:
            try:
                msg, (dummy_filename, lineno, offset, line) = value.args
            except ValueError:
                pass
            else:
                value = SyntaxError(msg, (filename, lineno, offset, line))
                sys.last_value = value
        if sys.excepthook is sys.__excepthook__:
            lines = traceback.format_exception_only(type, value)
            self.write''.joinlines
        else:
            sys.excepthooktypevaluetb

    def showtraceback(self):
        """Display the exception that just occurred.

        We remove the first stack item because it is our own code.

        The output is written by self.write(), below.

        """
        sys.last_type, sys.last_value, last_tb = ei = sys.exc_info()
        sys.last_traceback = last_tb
        try:
            lines = traceback.format_exceptionei[0]ei[1]last_tb.tb_next
            if sys.excepthook is sys.__excepthook__:
                self.write''.joinlines
            else:
                sys.excepthookei[0]ei[1]last_tb
        finally:
            last_tb = ei = None

    def write(self, data):
        """Write a string.

        The base implementation writes to sys.stderr; a subclass may
        replace this with a different implementation.

        """
        sys.stderr.writedata


class InteractiveConsole(InteractiveInterpreter):
    __doc__ = 'Closely emulate the behavior of the interactive Python interpreter.\n\n    This class builds on InteractiveInterpreter and adds prompting\n    using the familiar sys.ps1 and sys.ps2, and input buffering.\n\n    '

    def __init__(self, locals=None, filename='<console>'):
        """Constructor.

        The optional locals argument will be passed to the
        InteractiveInterpreter base class.

        The optional filename argument should specify the (file)name
        of the input stream; it will show up in tracebacks.

        """
        InteractiveInterpreter.__init__(self, locals)
        self.filename = filename
        self.resetbuffer()

    def resetbuffer(self):
        """Reset the input buffer."""
        self.buffer = []

    def interact--- This code section failed: ---

 L. 204         0  SETUP_FINALLY        12  'to 12'

 L. 205         2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                ps1
                6  POP_TOP          
                8  POP_BLOCK        
               10  JUMP_FORWARD         38  'to 38'
             12_0  COME_FROM_FINALLY     0  '0'

 L. 206        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    36  'to 36'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 207        26  LOAD_STR                 '>>> '
               28  LOAD_GLOBAL              sys
               30  STORE_ATTR               ps1
               32  POP_EXCEPT       
               34  JUMP_FORWARD         38  'to 38'
             36_0  COME_FROM            18  '18'
               36  END_FINALLY      
             38_0  COME_FROM            34  '34'
             38_1  COME_FROM            10  '10'

 L. 208        38  SETUP_FINALLY        50  'to 50'

 L. 209        40  LOAD_GLOBAL              sys
               42  LOAD_ATTR                ps2
               44  POP_TOP          
               46  POP_BLOCK        
               48  JUMP_FORWARD         76  'to 76'
             50_0  COME_FROM_FINALLY    38  '38'

 L. 210        50  DUP_TOP          
               52  LOAD_GLOBAL              AttributeError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    74  'to 74'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 211        64  LOAD_STR                 '... '
               66  LOAD_GLOBAL              sys
               68  STORE_ATTR               ps2
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
             74_0  COME_FROM            56  '56'
               74  END_FINALLY      
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            48  '48'

 L. 212        76  LOAD_STR                 'Type "help", "copyright", "credits" or "license" for more information.'
               78  STORE_FAST               'cprt'

 L. 213        80  LOAD_FAST                'banner'
               82  LOAD_CONST               None
               84  COMPARE_OP               is
               86  POP_JUMP_IF_FALSE   120  'to 120'

 L. 214        88  LOAD_FAST                'self'
               90  LOAD_METHOD              write
               92  LOAD_STR                 'Python %s on %s\n%s\n(%s)\n'

 L. 215        94  LOAD_GLOBAL              sys
               96  LOAD_ATTR                version
               98  LOAD_GLOBAL              sys
              100  LOAD_ATTR                platform
              102  LOAD_FAST                'cprt'

 L. 216       104  LOAD_FAST                'self'
              106  LOAD_ATTR                __class__
              108  LOAD_ATTR                __name__

 L. 215       110  BUILD_TUPLE_4         4 

 L. 214       112  BINARY_MODULO    
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          
              118  JUMP_FORWARD        142  'to 142'
            120_0  COME_FROM            86  '86'

 L. 217       120  LOAD_FAST                'banner'
              122  POP_JUMP_IF_FALSE   142  'to 142'

 L. 218       124  LOAD_FAST                'self'
              126  LOAD_METHOD              write
              128  LOAD_STR                 '%s\n'
              130  LOAD_GLOBAL              str
              132  LOAD_FAST                'banner'
              134  CALL_FUNCTION_1       1  ''
              136  BINARY_MODULO    
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
            142_0  COME_FROM           122  '122'
            142_1  COME_FROM           118  '118'

 L. 219       142  LOAD_CONST               0
              144  STORE_FAST               'more'
            146_0  COME_FROM           278  '278'
            146_1  COME_FROM           274  '274'
            146_2  COME_FROM           232  '232'

 L. 221       146  SETUP_FINALLY       234  'to 234'

 L. 222       148  LOAD_FAST                'more'
              150  POP_JUMP_IF_FALSE   160  'to 160'

 L. 223       152  LOAD_GLOBAL              sys
              154  LOAD_ATTR                ps2
              156  STORE_FAST               'prompt'
              158  JUMP_FORWARD        166  'to 166'
            160_0  COME_FROM           150  '150'

 L. 225       160  LOAD_GLOBAL              sys
              162  LOAD_ATTR                ps1
              164  STORE_FAST               'prompt'
            166_0  COME_FROM           158  '158'

 L. 226       166  SETUP_FINALLY       182  'to 182'

 L. 227       168  LOAD_FAST                'self'
              170  LOAD_METHOD              raw_input
              172  LOAD_FAST                'prompt'
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'line'
              178  POP_BLOCK        
              180  JUMP_FORWARD        220  'to 220'
            182_0  COME_FROM_FINALLY   166  '166'

 L. 228       182  DUP_TOP          
              184  LOAD_GLOBAL              EOFError
              186  COMPARE_OP               exception-match
              188  POP_JUMP_IF_FALSE   218  'to 218'
              190  POP_TOP          
              192  POP_TOP          
              194  POP_TOP          

 L. 229       196  LOAD_FAST                'self'
              198  LOAD_METHOD              write
              200  LOAD_STR                 '\n'
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          

 L. 230       206  POP_EXCEPT       
              208  POP_BLOCK        
          210_212  JUMP_FORWARD        280  'to 280'
              214  POP_EXCEPT       
              216  JUMP_FORWARD        230  'to 230'
            218_0  COME_FROM           188  '188'
              218  END_FINALLY      
            220_0  COME_FROM           180  '180'

 L. 232       220  LOAD_FAST                'self'
              222  LOAD_METHOD              push
              224  LOAD_FAST                'line'
              226  CALL_METHOD_1         1  ''
              228  STORE_FAST               'more'
            230_0  COME_FROM           216  '216'
              230  POP_BLOCK        
              232  JUMP_BACK           146  'to 146'
            234_0  COME_FROM_FINALLY   146  '146'

 L. 233       234  DUP_TOP          
              236  LOAD_GLOBAL              KeyboardInterrupt
              238  COMPARE_OP               exception-match
          240_242  POP_JUMP_IF_FALSE   276  'to 276'
              244  POP_TOP          
              246  POP_TOP          
              248  POP_TOP          

 L. 234       250  LOAD_FAST                'self'
              252  LOAD_METHOD              write
              254  LOAD_STR                 '\nKeyboardInterrupt\n'
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          

 L. 235       260  LOAD_FAST                'self'
              262  LOAD_METHOD              resetbuffer
              264  CALL_METHOD_0         0  ''
              266  POP_TOP          

 L. 236       268  LOAD_CONST               0
              270  STORE_FAST               'more'
              272  POP_EXCEPT       
              274  JUMP_BACK           146  'to 146'
            276_0  COME_FROM           240  '240'
              276  END_FINALLY      
              278  JUMP_BACK           146  'to 146'
            280_0  COME_FROM           210  '210'

 L. 237       280  LOAD_FAST                'exitmsg'
              282  LOAD_CONST               None
              284  COMPARE_OP               is
          286_288  POP_JUMP_IF_FALSE   310  'to 310'

 L. 238       290  LOAD_FAST                'self'
              292  LOAD_METHOD              write
              294  LOAD_STR                 'now exiting %s...\n'
              296  LOAD_FAST                'self'
              298  LOAD_ATTR                __class__
              300  LOAD_ATTR                __name__
              302  BINARY_MODULO    
              304  CALL_METHOD_1         1  ''
              306  POP_TOP          
              308  JUMP_FORWARD        334  'to 334'
            310_0  COME_FROM           286  '286'

 L. 239       310  LOAD_FAST                'exitmsg'
              312  LOAD_STR                 ''
              314  COMPARE_OP               !=
          316_318  POP_JUMP_IF_FALSE   334  'to 334'

 L. 240       320  LOAD_FAST                'self'
              322  LOAD_METHOD              write
              324  LOAD_STR                 '%s\n'
              326  LOAD_FAST                'exitmsg'
              328  BINARY_MODULO    
              330  CALL_METHOD_1         1  ''
              332  POP_TOP          
            334_0  COME_FROM           316  '316'
            334_1  COME_FROM           308  '308'

Parse error at or near `POP_BLOCK' instruction at offset 208

    def push(self, line):
        """Push a line to the interpreter.

        The line should not have a trailing newline; it may have
        internal newlines.  The line is appended to a buffer and the
        interpreter's runsource() method is called with the
        concatenated contents of the buffer as source.  If this
        indicates that the command was executed or invalid, the buffer
        is reset; otherwise, the command is incomplete, and the buffer
        is left as it was after the line was appended.  The return
        value is 1 if more input is required, 0 if the line was dealt
        with in some way (this is the same as runsource()).

        """
        self.buffer.appendline
        source = '\n'.joinself.buffer
        more = self.runsource(source, self.filename)
        if not more:
            self.resetbuffer()
        return more

    def raw_input(self, prompt=''):
        """Write a prompt and read a line.

        The returned line does not include the trailing newline.
        When the user enters the EOF key sequence, EOFError is raised.

        The base implementation uses the built-in function
        input(); a subclass may replace this with a different
        implementation.

        """
        return input(prompt)


def interact(banner=None, readfunc=None, local=None, exitmsg=None):
    """Closely emulate the interactive Python interpreter.

    This is a backwards compatible interface to the InteractiveConsole
    class.  When readfunc is not specified, it attempts to import the
    readline module to enable GNU readline if it is available.

    Arguments (all optional, all default to None):

    banner -- passed to InteractiveConsole.interact()
    readfunc -- if not None, replaces InteractiveConsole.raw_input()
    local -- passed to InteractiveInterpreter.__init__()
    exitmsg -- passed to InteractiveConsole.interact()

    """
    console = InteractiveConsole(local)
    if readfunc is not None:
        console.raw_input = readfunc
    else:
        pass
    try:
        import readline
    except ImportError:
        pass
    else:
        console.interact(banner, exitmsg)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', action='store_true', help="don't print version and copyright messages")
    args = parser.parse_args()
    if args.q or sys.flags.quiet:
        banner = ''
    else:
        banner = None
    interact(banner)