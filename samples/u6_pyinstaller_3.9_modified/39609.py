# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: colorama\initialise.py
import atexit, contextlib, sys
from .ansitowin32 import AnsiToWin32
orig_stdout = None
orig_stderr = None
wrapped_stdout = None
wrapped_stderr = None
atexit_done = False

def reset_all--- This code section failed: ---

 L.  19         0  LOAD_GLOBAL              AnsiToWin32
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L.  20         8  LOAD_GLOBAL              AnsiToWin32
               10  LOAD_GLOBAL              orig_stdout
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_METHOD              reset_all
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          
             20_0  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1


def init--- This code section failed: ---

 L.  25         0  LOAD_FAST                'wrap'
                2  POP_JUMP_IF_TRUE     26  'to 26'
                4  LOAD_GLOBAL              any
                6  LOAD_FAST                'autoreset'
                8  LOAD_FAST                'convert'
               10  LOAD_FAST                'strip'
               12  BUILD_LIST_3          3 
               14  CALL_FUNCTION_1       1  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L.  26        18  LOAD_GLOBAL              ValueError
               20  LOAD_STR                 'wrap=False conflicts with any other arg=True'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'
             26_1  COME_FROM             2  '2'

 L.  31        26  LOAD_GLOBAL              sys
               28  LOAD_ATTR                stdout
               30  STORE_GLOBAL             orig_stdout

 L.  32        32  LOAD_GLOBAL              sys
               34  LOAD_ATTR                stderr
               36  STORE_GLOBAL             orig_stderr

 L.  34        38  LOAD_GLOBAL              sys
               40  LOAD_ATTR                stdout
               42  LOAD_CONST               None
               44  <117>                 0  ''
               46  POP_JUMP_IF_FALSE    54  'to 54'

 L.  35        48  LOAD_CONST               None
               50  STORE_GLOBAL             wrapped_stdout
               52  JUMP_FORWARD         76  'to 76'
             54_0  COME_FROM            46  '46'

 L.  38        54  LOAD_GLOBAL              wrap_stream
               56  LOAD_GLOBAL              orig_stdout
               58  LOAD_FAST                'convert'
               60  LOAD_FAST                'strip'
               62  LOAD_FAST                'autoreset'
               64  LOAD_FAST                'wrap'
               66  CALL_FUNCTION_5       5  ''

 L.  37        68  DUP_TOP          
               70  LOAD_GLOBAL              sys
               72  STORE_ATTR               stdout
               74  STORE_GLOBAL             wrapped_stdout
             76_0  COME_FROM            52  '52'

 L.  39        76  LOAD_GLOBAL              sys
               78  LOAD_ATTR                stderr
               80  LOAD_CONST               None
               82  <117>                 0  ''
               84  POP_JUMP_IF_FALSE    92  'to 92'

 L.  40        86  LOAD_CONST               None
               88  STORE_GLOBAL             wrapped_stderr
               90  JUMP_FORWARD        114  'to 114'
             92_0  COME_FROM            84  '84'

 L.  43        92  LOAD_GLOBAL              wrap_stream
               94  LOAD_GLOBAL              orig_stderr
               96  LOAD_FAST                'convert'
               98  LOAD_FAST                'strip'
              100  LOAD_FAST                'autoreset'
              102  LOAD_FAST                'wrap'
              104  CALL_FUNCTION_5       5  ''

 L.  42       106  DUP_TOP          
              108  LOAD_GLOBAL              sys
              110  STORE_ATTR               stderr
              112  STORE_GLOBAL             wrapped_stderr
            114_0  COME_FROM            90  '90'

 L.  46       114  LOAD_GLOBAL              atexit_done
              116  POP_JUMP_IF_TRUE    132  'to 132'

 L.  47       118  LOAD_GLOBAL              atexit
              120  LOAD_METHOD              register
              122  LOAD_GLOBAL              reset_all
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          

 L.  48       128  LOAD_CONST               True
              130  STORE_GLOBAL             atexit_done
            132_0  COME_FROM           116  '116'

Parse error at or near `<117>' instruction at offset 44


def deinit--- This code section failed: ---

 L.  52         0  LOAD_GLOBAL              orig_stdout
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.  53         8  LOAD_GLOBAL              orig_stdout
               10  LOAD_GLOBAL              sys
               12  STORE_ATTR               stdout
             14_0  COME_FROM             6  '6'

 L.  54        14  LOAD_GLOBAL              orig_stderr
               16  LOAD_CONST               None
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L.  55        22  LOAD_GLOBAL              orig_stderr
               24  LOAD_GLOBAL              sys
               26  STORE_ATTR               stderr
             28_0  COME_FROM            20  '20'

Parse error at or near `None' instruction at offset -1


@contextlib.contextmanager
def colorama_text--- This code section failed: ---

 L.  60         0  LOAD_GLOBAL              init
                2  LOAD_FAST                'args'
                4  BUILD_MAP_0           0 
                6  LOAD_FAST                'kwargs'
                8  <164>                 1  ''
               10  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               12  POP_TOP          

 L.  61        14  SETUP_FINALLY        32  'to 32'

 L.  62        16  LOAD_CONST               None
               18  YIELD_VALUE      
               20  POP_TOP          
               22  POP_BLOCK        

 L.  64        24  LOAD_GLOBAL              deinit
               26  CALL_FUNCTION_0       0  ''
               28  POP_TOP          
               30  JUMP_FORWARD         40  'to 40'
             32_0  COME_FROM_FINALLY    14  '14'
               32  LOAD_GLOBAL              deinit
               34  CALL_FUNCTION_0       0  ''
               36  POP_TOP          
               38  <48>             
             40_0  COME_FROM            30  '30'

Parse error at or near `None' instruction at offset -1


def reinit--- This code section failed: ---

 L.  68         0  LOAD_GLOBAL              wrapped_stdout
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.  69         8  LOAD_GLOBAL              wrapped_stdout
               10  LOAD_GLOBAL              sys
               12  STORE_ATTR               stdout
             14_0  COME_FROM             6  '6'

 L.  70        14  LOAD_GLOBAL              wrapped_stderr
               16  LOAD_CONST               None
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L.  71        22  LOAD_GLOBAL              wrapped_stderr
               24  LOAD_GLOBAL              sys
               26  STORE_ATTR               stderr
             28_0  COME_FROM            20  '20'

Parse error at or near `None' instruction at offset -1


def wrap_stream(stream, convert, strip, autoreset, wrap):
    if wrap:
        wrapper = AnsiToWin32(stream, convert=convert,
          strip=strip,
          autoreset=autoreset)
        if wrapper.should_wrap:
            stream = wrapper.stream
    return stream


# global atexit_done ## Warning: Unused global
# global orig_stderr ## Warning: Unused global
# global orig_stdout ## Warning: Unused global
# global wrapped_stderr ## Warning: Unused global
# global wrapped_stdout ## Warning: Unused global