# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: getpass.py
"""Utilities to get a password and/or the current user name.

getpass(prompt[, stream]) - Prompt for a password, with echo turned off.
getuser() - Get the user name from the environment or password database.

GetPassWarning - This UserWarning is issued when getpass() cannot prevent
                 echoing of the password contents while reading.

On Windows, the msvcrt module will be used.

"""
import contextlib, io, os, sys, warnings
__all__ = [
 'getpass', 'getuser', 'GetPassWarning']

class GetPassWarning(UserWarning):
    pass


def unix_getpass--- This code section failed: ---

 L.  44         0  LOAD_CONST               None
                2  STORE_FAST               'passwd'

 L.  45         4  LOAD_GLOBAL              contextlib
                6  LOAD_METHOD              ExitStack
                8  CALL_METHOD_0         0  ''
            10_12  SETUP_WITH          438  'to 438'
               14  STORE_FAST               'stack'

 L.  46        16  SETUP_FINALLY        92  'to 92'

 L.  48        18  LOAD_GLOBAL              os
               20  LOAD_METHOD              open
               22  LOAD_STR                 '/dev/tty'
               24  LOAD_GLOBAL              os
               26  LOAD_ATTR                O_RDWR
               28  LOAD_GLOBAL              os
               30  LOAD_ATTR                O_NOCTTY
               32  BINARY_OR        
               34  CALL_METHOD_2         2  ''
               36  STORE_FAST               'fd'

 L.  49        38  LOAD_GLOBAL              io
               40  LOAD_METHOD              FileIO
               42  LOAD_FAST                'fd'
               44  LOAD_STR                 'w+'
               46  CALL_METHOD_2         2  ''
               48  STORE_FAST               'tty'

 L.  50        50  LOAD_FAST                'stack'
               52  LOAD_METHOD              enter_context
               54  LOAD_FAST                'tty'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L.  51        60  LOAD_GLOBAL              io
               62  LOAD_METHOD              TextIOWrapper
               64  LOAD_FAST                'tty'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'input'

 L.  52        70  LOAD_FAST                'stack'
               72  LOAD_METHOD              enter_context
               74  LOAD_FAST                'input'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L.  53        80  LOAD_FAST                'stream'
               82  POP_JUMP_IF_TRUE     88  'to 88'

 L.  54        84  LOAD_FAST                'input'
               86  STORE_FAST               'stream'
             88_0  COME_FROM            82  '82'
               88  POP_BLOCK        
               90  JUMP_FORWARD        204  'to 204'
             92_0  COME_FROM_FINALLY    16  '16'

 L.  55        92  DUP_TOP          
               94  LOAD_GLOBAL              OSError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   202  'to 202'
              100  POP_TOP          
              102  STORE_FAST               'e'
              104  POP_TOP          
              106  SETUP_FINALLY       190  'to 190'

 L.  57       108  LOAD_FAST                'stack'
              110  LOAD_METHOD              close
              112  CALL_METHOD_0         0  ''
              114  POP_TOP          

 L.  58       116  SETUP_FINALLY       132  'to 132'

 L.  59       118  LOAD_GLOBAL              sys
              120  LOAD_ATTR                stdin
              122  LOAD_METHOD              fileno
              124  CALL_METHOD_0         0  ''
              126  STORE_FAST               'fd'
              128  POP_BLOCK        
              130  JUMP_FORWARD        170  'to 170'
            132_0  COME_FROM_FINALLY   116  '116'

 L.  60       132  DUP_TOP          
              134  LOAD_GLOBAL              AttributeError
              136  LOAD_GLOBAL              ValueError
              138  BUILD_TUPLE_2         2 
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   168  'to 168'
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L.  61       150  LOAD_CONST               None
              152  STORE_FAST               'fd'

 L.  62       154  LOAD_GLOBAL              fallback_getpass
              156  LOAD_FAST                'prompt'
              158  LOAD_FAST                'stream'
              160  CALL_FUNCTION_2       2  ''
              162  STORE_FAST               'passwd'
              164  POP_EXCEPT       
              166  JUMP_FORWARD        170  'to 170'
            168_0  COME_FROM           142  '142'
              168  END_FINALLY      
            170_0  COME_FROM           166  '166'
            170_1  COME_FROM           130  '130'

 L.  63       170  LOAD_GLOBAL              sys
              172  LOAD_ATTR                stdin
              174  STORE_FAST               'input'

 L.  64       176  LOAD_FAST                'stream'
              178  POP_JUMP_IF_TRUE    186  'to 186'

 L.  65       180  LOAD_GLOBAL              sys
              182  LOAD_ATTR                stderr
              184  STORE_FAST               'stream'
            186_0  COME_FROM           178  '178'
              186  POP_BLOCK        
              188  BEGIN_FINALLY    
            190_0  COME_FROM_FINALLY   106  '106'
              190  LOAD_CONST               None
              192  STORE_FAST               'e'
              194  DELETE_FAST              'e'
              196  END_FINALLY      
              198  POP_EXCEPT       
              200  JUMP_FORWARD        204  'to 204'
            202_0  COME_FROM            98  '98'
              202  END_FINALLY      
            204_0  COME_FROM           200  '200'
            204_1  COME_FROM            90  '90'

 L.  67       204  LOAD_FAST                'fd'
              206  LOAD_CONST               None
              208  COMPARE_OP               is-not
          210_212  POP_JUMP_IF_FALSE   412  'to 412'

 L.  68       214  SETUP_FINALLY       348  'to 348'

 L.  69       216  LOAD_GLOBAL              termios
              218  LOAD_METHOD              tcgetattr
              220  LOAD_FAST                'fd'
              222  CALL_METHOD_1         1  ''
              224  STORE_FAST               'old'

 L.  70       226  LOAD_FAST                'old'
              228  LOAD_CONST               None
              230  LOAD_CONST               None
              232  BUILD_SLICE_2         2 
              234  BINARY_SUBSCR    
              236  STORE_FAST               'new'

 L.  71       238  LOAD_FAST                'new'
              240  LOAD_CONST               3
              242  DUP_TOP_TWO      
              244  BINARY_SUBSCR    
              246  LOAD_GLOBAL              termios
              248  LOAD_ATTR                ECHO
              250  UNARY_INVERT     
              252  INPLACE_AND      
              254  ROT_THREE        
              256  STORE_SUBSCR     

 L.  72       258  LOAD_GLOBAL              termios
              260  LOAD_ATTR                TCSAFLUSH
              262  STORE_FAST               'tcsetattr_flags'

 L.  73       264  LOAD_GLOBAL              hasattr
              266  LOAD_GLOBAL              termios
              268  LOAD_STR                 'TCSASOFT'
              270  CALL_FUNCTION_2       2  ''
          272_274  POP_JUMP_IF_FALSE   286  'to 286'

 L.  74       276  LOAD_FAST                'tcsetattr_flags'
              278  LOAD_GLOBAL              termios
              280  LOAD_ATTR                TCSASOFT
              282  INPLACE_OR       
              284  STORE_FAST               'tcsetattr_flags'
            286_0  COME_FROM           272  '272'

 L.  75       286  SETUP_FINALLY       320  'to 320'

 L.  76       288  LOAD_GLOBAL              termios
              290  LOAD_METHOD              tcsetattr
              292  LOAD_FAST                'fd'
              294  LOAD_FAST                'tcsetattr_flags'
              296  LOAD_FAST                'new'
              298  CALL_METHOD_3         3  ''
              300  POP_TOP          

 L.  77       302  LOAD_GLOBAL              _raw_input
              304  LOAD_FAST                'prompt'
              306  LOAD_FAST                'stream'
              308  LOAD_FAST                'input'
              310  LOAD_CONST               ('input',)
              312  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              314  STORE_FAST               'passwd'
              316  POP_BLOCK        
              318  BEGIN_FINALLY    
            320_0  COME_FROM_FINALLY   286  '286'

 L.  79       320  LOAD_GLOBAL              termios
              322  LOAD_METHOD              tcsetattr
              324  LOAD_FAST                'fd'
              326  LOAD_FAST                'tcsetattr_flags'
              328  LOAD_FAST                'old'
              330  CALL_METHOD_3         3  ''
              332  POP_TOP          

 L.  80       334  LOAD_FAST                'stream'
              336  LOAD_METHOD              flush
              338  CALL_METHOD_0         0  ''
              340  POP_TOP          
              342  END_FINALLY      
              344  POP_BLOCK        
              346  JUMP_FORWARD        412  'to 412'
            348_0  COME_FROM_FINALLY   214  '214'

 L.  81       348  DUP_TOP          
              350  LOAD_GLOBAL              termios
              352  LOAD_ATTR                error
              354  COMPARE_OP               exception-match
          356_358  POP_JUMP_IF_FALSE   410  'to 410'
              360  POP_TOP          
              362  POP_TOP          
              364  POP_TOP          

 L.  82       366  LOAD_FAST                'passwd'
              368  LOAD_CONST               None
              370  COMPARE_OP               is-not
          372_374  POP_JUMP_IF_FALSE   378  'to 378'

 L.  85       376  RAISE_VARARGS_0       0  'reraise'
            378_0  COME_FROM           372  '372'

 L.  88       378  LOAD_FAST                'stream'
              380  LOAD_FAST                'input'
              382  COMPARE_OP               is-not
          384_386  POP_JUMP_IF_FALSE   396  'to 396'

 L.  90       388  LOAD_FAST                'stack'
              390  LOAD_METHOD              close
              392  CALL_METHOD_0         0  ''
              394  POP_TOP          
            396_0  COME_FROM           384  '384'

 L.  91       396  LOAD_GLOBAL              fallback_getpass
              398  LOAD_FAST                'prompt'
              400  LOAD_FAST                'stream'
              402  CALL_FUNCTION_2       2  ''
              404  STORE_FAST               'passwd'
              406  POP_EXCEPT       
              408  JUMP_FORWARD        412  'to 412'
            410_0  COME_FROM           356  '356'
              410  END_FINALLY      
            412_0  COME_FROM           408  '408'
            412_1  COME_FROM           346  '346'
            412_2  COME_FROM           210  '210'

 L.  93       412  LOAD_FAST                'stream'
              414  LOAD_METHOD              write
              416  LOAD_STR                 '\n'
              418  CALL_METHOD_1         1  ''
              420  POP_TOP          

 L.  94       422  LOAD_FAST                'passwd'
              424  POP_BLOCK        
              426  ROT_TWO          
              428  BEGIN_FINALLY    
              430  WITH_CLEANUP_START
              432  WITH_CLEANUP_FINISH
              434  POP_FINALLY           0  ''
              436  RETURN_VALUE     
            438_0  COME_FROM_WITH       10  '10'
              438  WITH_CLEANUP_START
              440  WITH_CLEANUP_FINISH
              442  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 426


def win_getpass(prompt='Password: ', stream=None):
    """Prompt for password with echo off, using Windows getch()."""
    if sys.stdin is not sys.__stdin__:
        return fallback_getpasspromptstream
    else:
        for c in prompt:
            msvcrt.putwchc
        else:
            pw = ''
            while True:
                c = msvcrt.getwch
                if not c == '\r':
                    if c == '\n':
                        break
                    if c == '\x03':
                        raise KeyboardInterrupt
                    if c == '\x08':
                        pw = pw[:-1]
                else:
                    pw = pw + c

    msvcrt.putwch'\r'
    msvcrt.putwch'\n'
    return pw


def fallback_getpass(prompt='Password: ', stream=None):
    warnings.warn('Can not control echo on the terminal.', GetPassWarning, stacklevel=2)
    if not stream:
        stream = sys.stderr
    print('Warning: Password input may be echoed.', file=stream)
    return _raw_inputpromptstream


def _raw_input(prompt='', stream=None, input=None):
    if not stream:
        stream = sys.stderr
    else:
        if not input:
            input = sys.stdin
        prompt = str(prompt)
        if prompt:
            try:
                stream.writeprompt
            except UnicodeEncodeError:
                prompt = prompt.encodestream.encoding'replace'
                prompt = prompt.decodestream.encoding
                stream.writeprompt
            else:
                stream.flush
        line = input.readline
        assert line
    if line[(-1)] == '\n':
        line = line[:-1]
    return line


def getuser():
    """Get the username from the environment or password database.

    First try various environment variables, then the password
    database.  This works on Windows as long as USERNAME is set.

    """
    for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
        user = os.environ.getname
        if user:
            return user
        import pwd
        return pwd.getpwuidos.getuid[0]


try:
    import termios
    (
     termios.tcgetattr, termios.tcsetattr)
except (ImportError, AttributeError):
    try:
        import msvcrt
    except ImportError:
        getpass = fallback_getpass
    else:
        getpass = win_getpass
else:
    getpass = unix_getpass