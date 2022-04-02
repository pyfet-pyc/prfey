# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: codeop.py
r"""Utilities to compile possibly incomplete Python source code.

This module provides two interfaces, broadly similar to the builtin
function compile(), which take program text, a filename and a 'mode'
and:

- Return code object if the command is complete and valid
- Return None if the command is incomplete
- Raise SyntaxError, ValueError or OverflowError if the command is a
  syntax error (OverflowError and ValueError can be produced by
  malformed literals).

Approach:

First, check if the source consists entirely of blank lines and
comments; if so, replace it with 'pass', because the built-in
parser doesn't always do the right thing for these.

Compile three times: as is, with \n, and with \n\n appended.  If it
compiles as is, it's complete.  If it compiles with one \n appended,
we expect more.  If it doesn't compile either way, we compare the
error we get when compiling with \n or \n\n appended.  If the errors
are the same, the code is broken.  But if the errors are different, we
expect more.  Not intuitive; not even guaranteed to hold in future
releases; but this matches the compiler's behavior from Python 1.4
through 2.2, at least.

Caveat:

It is possible (but not likely) that the parser stops parsing with a
successful outcome before reaching the end of the source; in this
case, trailing symbols may be ignored instead of causing an error.
For example, a backslash followed by two newlines may be followed by
arbitrary garbage.  This will be fixed once the API for the parser is
better.

The two interfaces are:

compile_command(source, filename, symbol):

    Compiles a single command in the manner described above.

CommandCompiler():

    Instances of this class have __call__ methods identical in
    signature to compile_command; the difference is that if the
    instance compiles program text containing a __future__ statement,
    the instance 'remembers' and compiles all subsequent program texts
    with the statement in force.

The module also provides another class:

Compile():

    Instances of this class act like the built-in function compile,
    but with 'memory' in the sense described above.
"""
import __future__, warnings
_features = [getattr(__future__, fname) for fname in __future__.all_feature_names]
__all__ = [
 'compile_command', 'Compile', 'CommandCompiler']
PyCF_DONT_IMPLY_DEDENT = 512

def _maybe_compile--- This code section failed: ---

 L.  71         0  LOAD_FAST                'source'
                2  LOAD_METHOD              split
                4  LOAD_STR                 '\n'
                6  CALL_METHOD_1         1  ''
                8  GET_ITER         
             10_0  COME_FROM            36  '36'
             10_1  COME_FROM            24  '24'
               10  FOR_ITER             44  'to 44'
               12  STORE_FAST               'line'

 L.  72        14  LOAD_FAST                'line'
               16  LOAD_METHOD              strip
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'line'

 L.  73        22  LOAD_FAST                'line'
               24  POP_JUMP_IF_FALSE    10  'to 10'
               26  LOAD_FAST                'line'
               28  LOAD_CONST               0
               30  BINARY_SUBSCR    
               32  LOAD_STR                 '#'
               34  COMPARE_OP               !=
               36  POP_JUMP_IF_FALSE    10  'to 10'

 L.  74        38  POP_TOP          
               40  BREAK_LOOP           56  'to 56'
               42  JUMP_BACK            10  'to 10'

 L.  76        44  LOAD_FAST                'symbol'
               46  LOAD_STR                 'eval'
               48  COMPARE_OP               !=
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L.  77        52  LOAD_STR                 'pass'
               54  STORE_FAST               'source'
             56_0  COME_FROM            50  '50'

 L.  79        56  LOAD_CONST               None
               58  DUP_TOP          
               60  STORE_FAST               'err'
               62  DUP_TOP          
               64  STORE_FAST               'err1'
               66  STORE_FAST               'err2'

 L.  80        68  LOAD_CONST               None
               70  DUP_TOP          
               72  STORE_FAST               'code'
               74  DUP_TOP          
               76  STORE_FAST               'code1'
               78  STORE_FAST               'code2'

 L.  82        80  SETUP_FINALLY        98  'to 98'

 L.  83        82  LOAD_FAST                'compiler'
               84  LOAD_FAST                'source'
               86  LOAD_FAST                'filename'
               88  LOAD_FAST                'symbol'
               90  CALL_FUNCTION_3       3  ''
               92  STORE_FAST               'code'
               94  POP_BLOCK        
               96  JUMP_FORWARD        132  'to 132'
             98_0  COME_FROM_FINALLY    80  '80'

 L.  84        98  DUP_TOP          
              100  LOAD_GLOBAL              SyntaxError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   130  'to 130'
              106  POP_TOP          
              108  STORE_FAST               'err'
              110  POP_TOP          
              112  SETUP_FINALLY       118  'to 118'

 L.  85       114  POP_BLOCK        
              116  BEGIN_FINALLY    
            118_0  COME_FROM_FINALLY   112  '112'
              118  LOAD_CONST               None
              120  STORE_FAST               'err'
              122  DELETE_FAST              'err'
              124  END_FINALLY      
              126  POP_EXCEPT       
              128  JUMP_FORWARD        132  'to 132'
            130_0  COME_FROM           104  '104'
              130  END_FINALLY      
            132_0  COME_FROM           128  '128'
            132_1  COME_FROM            96  '96'

 L.  88       132  LOAD_GLOBAL              warnings
              134  LOAD_METHOD              catch_warnings
              136  CALL_METHOD_0         0  ''
              138  SETUP_WITH          278  'to 278'
              140  POP_TOP          

 L.  89       142  LOAD_GLOBAL              warnings
              144  LOAD_METHOD              simplefilter
              146  LOAD_STR                 'ignore'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          

 L.  90       152  SETUP_FINALLY       174  'to 174'

 L.  91       154  LOAD_FAST                'compiler'
              156  LOAD_FAST                'source'
              158  LOAD_STR                 '\n'
              160  BINARY_ADD       
              162  LOAD_FAST                'filename'
              164  LOAD_FAST                'symbol'
              166  CALL_FUNCTION_3       3  ''
              168  STORE_FAST               'code1'
              170  POP_BLOCK        
              172  JUMP_FORWARD        212  'to 212'
            174_0  COME_FROM_FINALLY   152  '152'

 L.  92       174  DUP_TOP          
              176  LOAD_GLOBAL              SyntaxError
              178  COMPARE_OP               exception-match
              180  POP_JUMP_IF_FALSE   210  'to 210'
              182  POP_TOP          
              184  STORE_FAST               'e'
              186  POP_TOP          
              188  SETUP_FINALLY       198  'to 198'

 L.  93       190  LOAD_FAST                'e'
              192  STORE_FAST               'err1'
              194  POP_BLOCK        
              196  BEGIN_FINALLY    
            198_0  COME_FROM_FINALLY   188  '188'
              198  LOAD_CONST               None
              200  STORE_FAST               'e'
              202  DELETE_FAST              'e'
              204  END_FINALLY      
              206  POP_EXCEPT       
              208  JUMP_FORWARD        212  'to 212'
            210_0  COME_FROM           180  '180'
              210  END_FINALLY      
            212_0  COME_FROM           208  '208'
            212_1  COME_FROM           172  '172'

 L.  95       212  SETUP_FINALLY       234  'to 234'

 L.  96       214  LOAD_FAST                'compiler'
              216  LOAD_FAST                'source'
              218  LOAD_STR                 '\n\n'
              220  BINARY_ADD       
              222  LOAD_FAST                'filename'
              224  LOAD_FAST                'symbol'
              226  CALL_FUNCTION_3       3  ''
              228  STORE_FAST               'code2'
              230  POP_BLOCK        
              232  JUMP_FORWARD        274  'to 274'
            234_0  COME_FROM_FINALLY   212  '212'

 L.  97       234  DUP_TOP          
              236  LOAD_GLOBAL              SyntaxError
              238  COMPARE_OP               exception-match
          240_242  POP_JUMP_IF_FALSE   272  'to 272'
              244  POP_TOP          
              246  STORE_FAST               'e'
              248  POP_TOP          
              250  SETUP_FINALLY       260  'to 260'

 L.  98       252  LOAD_FAST                'e'
              254  STORE_FAST               'err2'
              256  POP_BLOCK        
              258  BEGIN_FINALLY    
            260_0  COME_FROM_FINALLY   250  '250'
              260  LOAD_CONST               None
              262  STORE_FAST               'e'
              264  DELETE_FAST              'e'
              266  END_FINALLY      
              268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
            272_0  COME_FROM           240  '240'
              272  END_FINALLY      
            274_0  COME_FROM           270  '270'
            274_1  COME_FROM           232  '232'
              274  POP_BLOCK        
              276  BEGIN_FINALLY    
            278_0  COME_FROM_WITH      138  '138'
              278  WITH_CLEANUP_START
              280  WITH_CLEANUP_FINISH
              282  END_FINALLY      

 L. 100       284  SETUP_FINALLY       332  'to 332'

 L. 101       286  LOAD_FAST                'code'
          288_290  POP_JUMP_IF_FALSE   300  'to 300'

 L. 102       292  LOAD_FAST                'code'
              294  POP_BLOCK        
              296  CALL_FINALLY        332  'to 332'
              298  RETURN_VALUE     
            300_0  COME_FROM           288  '288'

 L. 103       300  LOAD_FAST                'code1'
          302_304  POP_JUMP_IF_TRUE    328  'to 328'
              306  LOAD_GLOBAL              repr
              308  LOAD_FAST                'err1'
              310  CALL_FUNCTION_1       1  ''
              312  LOAD_GLOBAL              repr
              314  LOAD_FAST                'err2'
              316  CALL_FUNCTION_1       1  ''
              318  COMPARE_OP               ==
          320_322  POP_JUMP_IF_FALSE   328  'to 328'

 L. 104       324  LOAD_FAST                'err1'
              326  RAISE_VARARGS_1       1  'exception instance'
            328_0  COME_FROM           320  '320'
            328_1  COME_FROM           302  '302'
              328  POP_BLOCK        
              330  BEGIN_FINALLY    
            332_0  COME_FROM           296  '296'
            332_1  COME_FROM_FINALLY   284  '284'

 L. 106       332  LOAD_CONST               None
              334  DUP_TOP          
              336  STORE_FAST               'err1'
              338  STORE_FAST               'err2'
              340  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 296


def _compile(source, filename, symbol):
    return compile(source, filename, symbol, PyCF_DONT_IMPLY_DEDENT)


def compile_command(source, filename='<input>', symbol='single'):
    r"""Compile a command and determine whether it is incomplete.

    Arguments:

    source -- the source string; may contain \n characters
    filename -- optional filename from which source was read; default
                "<input>"
    symbol -- optional grammar start symbol; "single" (default), "exec"
              or "eval"

    Return value / exceptions raised:

    - Return a code object if the command is complete and valid
    - Return None if the command is incomplete
    - Raise SyntaxError, ValueError or OverflowError if the command is a
      syntax error (OverflowError and ValueError can be produced by
      malformed literals).
    """
    return _maybe_compile(_compile, source, filename, symbol)


class Compile:
    __doc__ = 'Instances of this class behave much like the built-in compile\n    function, but if one is used to compile text containing a future\n    statement, it "remembers" and compiles all subsequent program texts\n    with the statement in force.'

    def __init__(self):
        self.flags = PyCF_DONT_IMPLY_DEDENT

    def __call__(self, source, filename, symbol):
        codeob = compile(source, filename, symbol, self.flags, 1)
        for feature in _features:
            if codeob.co_flags & feature.compiler_flag:
                self.flags |= feature.compiler_flag
            return codeob


class CommandCompiler:
    __doc__ = "Instances of this class have __call__ methods identical in\n    signature to compile_command; the difference is that if the\n    instance compiles program text containing a __future__ statement,\n    the instance 'remembers' and compiles all subsequent program texts\n    with the statement in force."

    def __init__(self):
        self.compiler = Compile()

    def __call__(self, source, filename='<input>', symbol='single'):
        r"""Compile a command and determine whether it is incomplete.

        Arguments:

        source -- the source string; may contain \n characters
        filename -- optional filename from which source was read;
                    default "<input>"
        symbol -- optional grammar start symbol; "single" (default) or
                  "eval"

        Return value / exceptions raised:

        - Return a code object if the command is complete and valid
        - Return None if the command is incomplete
        - Raise SyntaxError, ValueError or OverflowError if the command is a
          syntax error (OverflowError and ValueError can be produced by
          malformed literals).
        """
        return _maybe_compile(self.compiler, source, filename, symbol)