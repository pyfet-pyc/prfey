# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\log.py
"""A simple log mechanism styled after PEP 282."""
DEBUG = 1
INFO = 2
WARN = 3
ERROR = 4
FATAL = 5
import sys

class Log:

    def __init__(self, threshold=WARN):
        self.threshold = threshold

    def _log--- This code section failed: ---

 L.  20         0  LOAD_FAST                'level'
                2  LOAD_GLOBAL              DEBUG
                4  LOAD_GLOBAL              INFO
                6  LOAD_GLOBAL              WARN
                8  LOAD_GLOBAL              ERROR
               10  LOAD_GLOBAL              FATAL
               12  BUILD_TUPLE_5         5 
               14  <118>                 1  ''
               16  POP_JUMP_IF_FALSE    34  'to 34'

 L.  21        18  LOAD_GLOBAL              ValueError
               20  LOAD_STR                 '%s wrong log level'
               22  LOAD_GLOBAL              str
               24  LOAD_FAST                'level'
               26  CALL_FUNCTION_1       1  ''
               28  BINARY_MODULO    
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            16  '16'

 L.  23        34  LOAD_FAST                'level'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                threshold
               40  COMPARE_OP               >=
               42  POP_JUMP_IF_FALSE   168  'to 168'

 L.  24        44  LOAD_FAST                'args'
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L.  25        48  LOAD_FAST                'msg'
               50  LOAD_FAST                'args'
               52  BINARY_MODULO    
               54  STORE_FAST               'msg'
             56_0  COME_FROM            46  '46'

 L.  26        56  LOAD_FAST                'level'
               58  LOAD_GLOBAL              WARN
               60  LOAD_GLOBAL              ERROR
               62  LOAD_GLOBAL              FATAL
               64  BUILD_TUPLE_3         3 
               66  <118>                 0  ''
               68  POP_JUMP_IF_FALSE    78  'to 78'

 L.  27        70  LOAD_GLOBAL              sys
               72  LOAD_ATTR                stderr
               74  STORE_FAST               'stream'
               76  JUMP_FORWARD         84  'to 84'
             78_0  COME_FROM            68  '68'

 L.  29        78  LOAD_GLOBAL              sys
               80  LOAD_ATTR                stdout
               82  STORE_FAST               'stream'
             84_0  COME_FROM            76  '76'

 L.  30        84  SETUP_FINALLY       104  'to 104'

 L.  31        86  LOAD_FAST                'stream'
               88  LOAD_METHOD              write
               90  LOAD_STR                 '%s\n'
               92  LOAD_FAST                'msg'
               94  BINARY_MODULO    
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
              100  POP_BLOCK        
              102  JUMP_FORWARD        160  'to 160'
            104_0  COME_FROM_FINALLY    84  '84'

 L.  32       104  DUP_TOP          
              106  LOAD_GLOBAL              UnicodeEncodeError
              108  <121>               158  ''
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L.  34       116  LOAD_FAST                'stream'
              118  LOAD_ATTR                encoding
              120  STORE_FAST               'encoding'

 L.  35       122  LOAD_FAST                'msg'
              124  LOAD_METHOD              encode
              126  LOAD_FAST                'encoding'
              128  LOAD_STR                 'backslashreplace'
              130  CALL_METHOD_2         2  ''
              132  LOAD_METHOD              decode
              134  LOAD_FAST                'encoding'
              136  CALL_METHOD_1         1  ''
              138  STORE_FAST               'msg'

 L.  36       140  LOAD_FAST                'stream'
              142  LOAD_METHOD              write
              144  LOAD_STR                 '%s\n'
              146  LOAD_FAST                'msg'
              148  BINARY_MODULO    
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          
              154  POP_EXCEPT       
              156  JUMP_FORWARD        160  'to 160'
              158  <48>             
            160_0  COME_FROM           156  '156'
            160_1  COME_FROM           102  '102'

 L.  37       160  LOAD_FAST                'stream'
              162  LOAD_METHOD              flush
              164  CALL_METHOD_0         0  ''
              166  POP_TOP          
            168_0  COME_FROM            42  '42'

Parse error at or near `None' instruction at offset -1

    def log(self, level, msg, *args):
        self._log(level, msg, args)

    def debug(self, msg, *args):
        self._log(DEBUG, msg, args)

    def info(self, msg, *args):
        self._log(INFO, msg, args)

    def warn(self, msg, *args):
        self._log(WARN, msg, args)

    def error(self, msg, *args):
        self._log(ERROR, msg, args)

    def fatal(self, msg, *args):
        self._log(FATAL, msg, args)


_global_log = Log()
log = _global_log.log
debug = _global_log.debug
info = _global_log.info
warn = _global_log.warn
error = _global_log.error
fatal = _global_log.fatal

def set_threshold(level):
    old = _global_log.threshold
    _global_log.threshold = level
    return old


def set_verbosity(v):
    if v <= 0:
        set_threshold(WARN)
    else:
        if v == 1:
            set_threshold(INFO)
        else:
            if v >= 2:
                set_threshold(DEBUG)