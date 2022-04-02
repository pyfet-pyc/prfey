# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
import __future__
_features = [getattr(__future__, fname) for fname in __future__.all_feature_names]
__all__ = [
 'compile_command', 'Compile', 'CommandCompiler']
PyCF_DONT_IMPLY_DEDENT = 512

def _maybe_compile--- This code section failed: ---

 L.  70         0  LOAD_FAST                'source'
                2  LOAD_METHOD              split
                4  LOAD_STR                 '\n'
                6  CALL_METHOD_1         1  ''
                8  GET_ITER         
             10_0  COME_FROM            36  '36'
             10_1  COME_FROM            24  '24'
               10  FOR_ITER             44  'to 44'
               12  STORE_FAST               'line'

 L.  71        14  LOAD_FAST                'line'
               16  LOAD_METHOD              strip
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'line'

 L.  72        22  LOAD_FAST                'line'
               24  POP_JUMP_IF_FALSE    10  'to 10'
               26  LOAD_FAST                'line'
               28  LOAD_CONST               0
               30  BINARY_SUBSCR    
               32  LOAD_STR                 '#'
               34  COMPARE_OP               !=
               36  POP_JUMP_IF_FALSE    10  'to 10'

 L.  73        38  POP_TOP          
               40  BREAK_LOOP           56  'to 56'
               42  JUMP_BACK            10  'to 10'

 L.  75        44  LOAD_FAST                'symbol'
               46  LOAD_STR                 'eval'
               48  COMPARE_OP               !=
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L.  76        52  LOAD_STR                 'pass'
               54  STORE_FAST               'source'
             56_0  COME_FROM            50  '50'

 L.  78        56  LOAD_CONST               None
               58  DUP_TOP          
               60  STORE_FAST               'err'
               62  DUP_TOP          
               64  STORE_FAST               'err1'
               66  STORE_FAST               'err2'

 L.  79        68  LOAD_CONST               None
               70  DUP_TOP          
               72  STORE_FAST               'code'
               74  DUP_TOP          
               76  STORE_FAST               'code1'
               78  STORE_FAST               'code2'

 L.  81        80  SETUP_FINALLY        98  'to 98'

 L.  82        82  LOAD_FAST                'compiler'
               84  LOAD_FAST                'source'
               86  LOAD_FAST                'filename'
               88  LOAD_FAST                'symbol'
               90  CALL_FUNCTION_3       3  ''
               92  STORE_FAST               'code'
               94  POP_BLOCK        
               96  JUMP_FORWARD        132  'to 132'
             98_0  COME_FROM_FINALLY    80  '80'

 L.  83        98  DUP_TOP          
              100  LOAD_GLOBAL              SyntaxError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   130  'to 130'
              106  POP_TOP          
              108  STORE_FAST               'err'
              110  POP_TOP          
              112  SETUP_FINALLY       118  'to 118'

 L.  84       114  POP_BLOCK        
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

 L.  86       132  SETUP_FINALLY       154  'to 154'

 L.  87       134  LOAD_FAST                'compiler'
              136  LOAD_FAST                'source'
              138  LOAD_STR                 '\n'
              140  BINARY_ADD       
              142  LOAD_FAST                'filename'
              144  LOAD_FAST                'symbol'
              146  CALL_FUNCTION_3       3  ''
              148  STORE_FAST               'code1'
              150  POP_BLOCK        
              152  JUMP_FORWARD        192  'to 192'
            154_0  COME_FROM_FINALLY   132  '132'

 L.  88       154  DUP_TOP          
              156  LOAD_GLOBAL              SyntaxError
              158  COMPARE_OP               exception-match
              160  POP_JUMP_IF_FALSE   190  'to 190'
              162  POP_TOP          
              164  STORE_FAST               'e'
              166  POP_TOP          
              168  SETUP_FINALLY       178  'to 178'

 L.  89       170  LOAD_FAST                'e'
              172  STORE_FAST               'err1'
              174  POP_BLOCK        
              176  BEGIN_FINALLY    
            178_0  COME_FROM_FINALLY   168  '168'
              178  LOAD_CONST               None
              180  STORE_FAST               'e'
              182  DELETE_FAST              'e'
              184  END_FINALLY      
              186  POP_EXCEPT       
              188  JUMP_FORWARD        192  'to 192'
            190_0  COME_FROM           160  '160'
              190  END_FINALLY      
            192_0  COME_FROM           188  '188'
            192_1  COME_FROM           152  '152'

 L.  91       192  SETUP_FINALLY       214  'to 214'

 L.  92       194  LOAD_FAST                'compiler'
              196  LOAD_FAST                'source'
              198  LOAD_STR                 '\n\n'
              200  BINARY_ADD       
              202  LOAD_FAST                'filename'
              204  LOAD_FAST                'symbol'
              206  CALL_FUNCTION_3       3  ''
              208  STORE_FAST               'code2'
              210  POP_BLOCK        
              212  JUMP_FORWARD        252  'to 252'
            214_0  COME_FROM_FINALLY   192  '192'

 L.  93       214  DUP_TOP          
              216  LOAD_GLOBAL              SyntaxError
              218  COMPARE_OP               exception-match
              220  POP_JUMP_IF_FALSE   250  'to 250'
              222  POP_TOP          
              224  STORE_FAST               'e'
              226  POP_TOP          
              228  SETUP_FINALLY       238  'to 238'

 L.  94       230  LOAD_FAST                'e'
              232  STORE_FAST               'err2'
              234  POP_BLOCK        
              236  BEGIN_FINALLY    
            238_0  COME_FROM_FINALLY   228  '228'
              238  LOAD_CONST               None
              240  STORE_FAST               'e'
              242  DELETE_FAST              'e'
              244  END_FINALLY      
              246  POP_EXCEPT       
              248  JUMP_FORWARD        252  'to 252'
            250_0  COME_FROM           220  '220'
              250  END_FINALLY      
            252_0  COME_FROM           248  '248'
            252_1  COME_FROM           212  '212'

 L.  96       252  SETUP_FINALLY       300  'to 300'

 L.  97       254  LOAD_FAST                'code'
          256_258  POP_JUMP_IF_FALSE   268  'to 268'

 L.  98       260  LOAD_FAST                'code'
              262  POP_BLOCK        
              264  CALL_FINALLY        300  'to 300'
              266  RETURN_VALUE     
            268_0  COME_FROM           256  '256'

 L.  99       268  LOAD_FAST                'code1'
          270_272  POP_JUMP_IF_TRUE    296  'to 296'
              274  LOAD_GLOBAL              repr
              276  LOAD_FAST                'err1'
              278  CALL_FUNCTION_1       1  ''
              280  LOAD_GLOBAL              repr
              282  LOAD_FAST                'err2'
              284  CALL_FUNCTION_1       1  ''
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_FALSE   296  'to 296'

 L. 100       292  LOAD_FAST                'err1'
              294  RAISE_VARARGS_1       1  'exception instance'
            296_0  COME_FROM           288  '288'
            296_1  COME_FROM           270  '270'
              296  POP_BLOCK        
              298  BEGIN_FINALLY    
            300_0  COME_FROM           264  '264'
            300_1  COME_FROM_FINALLY   252  '252'

 L. 102       300  LOAD_CONST               None
              302  DUP_TOP          
              304  STORE_FAST               'err1'
              306  STORE_FAST               'err2'
              308  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 264


def _compile(source, filename, symbol):
    return compile(source, filename, symbol, PyCF_DONT_IMPLY_DEDENT)


def compile_command(source, filename='<input>', symbol='single'):
    r"""Compile a command and determine whether it is incomplete.

    Arguments:

    source -- the source string; may contain \n characters
    filename -- optional filename from which source was read; default
                "<input>"
    symbol -- optional grammar start symbol; "single" (default) or "eval"

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