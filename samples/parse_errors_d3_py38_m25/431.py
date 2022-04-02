# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: py_compile.py
"""Routine to "compile" a .py file to a .pyc file.

This module has intimate knowledge of the format of .pyc files.
"""
import enum, importlib._bootstrap_external, importlib.machinery, importlib.util, os, os.path, sys, traceback
__all__ = [
 'compile', 'main', 'PyCompileError', 'PycInvalidationMode']

class PyCompileError(Exception):
    __doc__ = "Exception raised when an error occurs while attempting to\n    compile the file.\n\n    To raise this exception, use\n\n        raise PyCompileError(exc_type,exc_value,file[,msg])\n\n    where\n\n        exc_type:   exception type to be used in error message\n                    type name can be accesses as class variable\n                    'exc_type_name'\n\n        exc_value:  exception value to be used in error message\n                    can be accesses as class variable 'exc_value'\n\n        file:       name of file being compiled to be used in error message\n                    can be accesses as class variable 'file'\n\n        msg:        string message to be written as error message\n                    If no value is given, a default exception message will be\n                    given, consistent with 'standard' py_compile output.\n                    message (or default) can be accesses as class variable\n                    'msg'\n\n    "

    def __init__(self, exc_type, exc_value, file, msg=''):
        exc_type_name = exc_type.__name__
        if exc_type is SyntaxError:
            tbtext = ''.join(traceback.format_exception_only(exc_type, exc_value))
            errmsg = tbtext.replace('File "<string>"', 'File "%s"' % file)
        else:
            errmsg = 'Sorry: %s: %s' % (exc_type_name, exc_value)
        Exception.__init__(self, msg or errmsg, exc_type_name, exc_value, file)
        self.exc_type_name = exc_type_name
        self.exc_value = exc_value
        self.file = file
        self.msg = msg or errmsg

    def __str__(self):
        return self.msg


class PycInvalidationMode(enum.Enum):
    TIMESTAMP = 1
    CHECKED_HASH = 2
    UNCHECKED_HASH = 3


def _get_default_invalidation_mode():
    if os.environ.get('SOURCE_DATE_EPOCH'):
        return PycInvalidationMode.CHECKED_HASH
    return PycInvalidationMode.TIMESTAMP


def compile--- This code section failed: ---

 L. 124         0  LOAD_FAST                'invalidation_mode'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 125         8  LOAD_GLOBAL              _get_default_invalidation_mode
               10  CALL_FUNCTION_0       0  ''
               12  STORE_FAST               'invalidation_mode'
             14_0  COME_FROM             6  '6'

 L. 126        14  LOAD_FAST                'cfile'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    76  'to 76'

 L. 127        22  LOAD_FAST                'optimize'
               24  LOAD_CONST               0
               26  COMPARE_OP               >=
               28  POP_JUMP_IF_FALSE    64  'to 64'

 L. 128        30  LOAD_FAST                'optimize'
               32  LOAD_CONST               1
               34  COMPARE_OP               >=
               36  POP_JUMP_IF_FALSE    42  'to 42'
               38  LOAD_FAST                'optimize'
               40  JUMP_FORWARD         44  'to 44'
             42_0  COME_FROM            36  '36'
               42  LOAD_STR                 ''
             44_0  COME_FROM            40  '40'
               44  STORE_FAST               'optimization'

 L. 129        46  LOAD_GLOBAL              importlib
               48  LOAD_ATTR                util
               50  LOAD_ATTR                cache_from_source
               52  LOAD_FAST                'file'

 L. 130        54  LOAD_FAST                'optimization'

 L. 129        56  LOAD_CONST               ('optimization',)
               58  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               60  STORE_FAST               'cfile'
               62  JUMP_FORWARD         76  'to 76'
             64_0  COME_FROM            28  '28'

 L. 132        64  LOAD_GLOBAL              importlib
               66  LOAD_ATTR                util
               68  LOAD_METHOD              cache_from_source
               70  LOAD_FAST                'file'
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'cfile'
             76_0  COME_FROM            62  '62'
             76_1  COME_FROM            20  '20'

 L. 133        76  LOAD_GLOBAL              os
               78  LOAD_ATTR                path
               80  LOAD_METHOD              islink
               82  LOAD_FAST                'cfile'
               84  CALL_METHOD_1         1  ''
               86  POP_JUMP_IF_FALSE   108  'to 108'

 L. 134        88  LOAD_STR                 '{} is a symlink and will be changed into a regular file if import writes a byte-compiled file to it'
               90  STORE_FAST               'msg'

 L. 136        92  LOAD_GLOBAL              FileExistsError
               94  LOAD_FAST                'msg'
               96  LOAD_METHOD              format
               98  LOAD_FAST                'cfile'
              100  CALL_METHOD_1         1  ''
              102  CALL_FUNCTION_1       1  ''
              104  RAISE_VARARGS_1       1  'exception instance'
              106  JUMP_FORWARD        150  'to 150'
            108_0  COME_FROM            86  '86'

 L. 137       108  LOAD_GLOBAL              os
              110  LOAD_ATTR                path
              112  LOAD_METHOD              exists
              114  LOAD_FAST                'cfile'
              116  CALL_METHOD_1         1  ''
              118  POP_JUMP_IF_FALSE   150  'to 150'
              120  LOAD_GLOBAL              os
              122  LOAD_ATTR                path
              124  LOAD_METHOD              isfile
              126  LOAD_FAST                'cfile'
              128  CALL_METHOD_1         1  ''
              130  POP_JUMP_IF_TRUE    150  'to 150'

 L. 138       132  LOAD_STR                 '{} is a non-regular file and will be changed into a regular one if import writes a byte-compiled file to it'
              134  STORE_FAST               'msg'

 L. 140       136  LOAD_GLOBAL              FileExistsError
              138  LOAD_FAST                'msg'
              140  LOAD_METHOD              format
              142  LOAD_FAST                'cfile'
              144  CALL_METHOD_1         1  ''
              146  CALL_FUNCTION_1       1  ''
              148  RAISE_VARARGS_1       1  'exception instance'
            150_0  COME_FROM           130  '130'
            150_1  COME_FROM           118  '118'
            150_2  COME_FROM           106  '106'

 L. 141       150  LOAD_GLOBAL              importlib
              152  LOAD_ATTR                machinery
              154  LOAD_METHOD              SourceFileLoader
              156  LOAD_STR                 '<py_compile>'
              158  LOAD_FAST                'file'
              160  CALL_METHOD_2         2  ''
              162  STORE_FAST               'loader'

 L. 142       164  LOAD_FAST                'loader'
              166  LOAD_METHOD              get_data
              168  LOAD_FAST                'file'
              170  CALL_METHOD_1         1  ''
              172  STORE_FAST               'source_bytes'

 L. 143       174  SETUP_FINALLY       200  'to 200'

 L. 144       176  LOAD_FAST                'loader'
              178  LOAD_ATTR                source_to_code
              180  LOAD_FAST                'source_bytes'
              182  LOAD_FAST                'dfile'
              184  JUMP_IF_TRUE_OR_POP   188  'to 188'
              186  LOAD_FAST                'file'
            188_0  COME_FROM           184  '184'

 L. 145       188  LOAD_FAST                'optimize'

 L. 144       190  LOAD_CONST               ('_optimize',)
              192  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              194  STORE_FAST               'code'
              196  POP_BLOCK        
              198  JUMP_FORWARD        300  'to 300'
            200_0  COME_FROM_FINALLY   174  '174'

 L. 146       200  DUP_TOP          
              202  LOAD_GLOBAL              Exception
              204  COMPARE_OP               exception-match
          206_208  POP_JUMP_IF_FALSE   298  'to 298'
              210  POP_TOP          
              212  STORE_FAST               'err'
              214  POP_TOP          
              216  SETUP_FINALLY       286  'to 286'

 L. 147       218  LOAD_GLOBAL              PyCompileError
              220  LOAD_FAST                'err'
              222  LOAD_ATTR                __class__
              224  LOAD_FAST                'err'
              226  LOAD_FAST                'dfile'
              228  JUMP_IF_TRUE_OR_POP   232  'to 232'
              230  LOAD_FAST                'file'
            232_0  COME_FROM           228  '228'
              232  CALL_FUNCTION_3       3  ''
              234  STORE_FAST               'py_exc'

 L. 148       236  LOAD_FAST                'quiet'
              238  LOAD_CONST               2
              240  COMPARE_OP               <
          242_244  POP_JUMP_IF_FALSE   276  'to 276'

 L. 149       246  LOAD_FAST                'doraise'
          248_250  POP_JUMP_IF_FALSE   258  'to 258'

 L. 150       252  LOAD_FAST                'py_exc'
              254  RAISE_VARARGS_1       1  'exception instance'
              256  JUMP_FORWARD        276  'to 276'
            258_0  COME_FROM           248  '248'

 L. 152       258  LOAD_GLOBAL              sys
              260  LOAD_ATTR                stderr
              262  LOAD_METHOD              write
              264  LOAD_FAST                'py_exc'
              266  LOAD_ATTR                msg
              268  LOAD_STR                 '\n'
              270  BINARY_ADD       
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          
            276_0  COME_FROM           256  '256'
            276_1  COME_FROM           242  '242'

 L. 153       276  POP_BLOCK        
              278  POP_EXCEPT       
              280  CALL_FINALLY        286  'to 286'
              282  LOAD_CONST               None
              284  RETURN_VALUE     
            286_0  COME_FROM           280  '280'
            286_1  COME_FROM_FINALLY   216  '216'
              286  LOAD_CONST               None
              288  STORE_FAST               'err'
              290  DELETE_FAST              'err'
              292  END_FINALLY      
              294  POP_EXCEPT       
              296  JUMP_FORWARD        300  'to 300'
            298_0  COME_FROM           206  '206'
              298  END_FINALLY      
            300_0  COME_FROM           296  '296'
            300_1  COME_FROM           198  '198'

 L. 154       300  SETUP_FINALLY       334  'to 334'

 L. 155       302  LOAD_GLOBAL              os
              304  LOAD_ATTR                path
              306  LOAD_METHOD              dirname
              308  LOAD_FAST                'cfile'
              310  CALL_METHOD_1         1  ''
              312  STORE_FAST               'dirname'

 L. 156       314  LOAD_FAST                'dirname'
          316_318  POP_JUMP_IF_FALSE   330  'to 330'

 L. 157       320  LOAD_GLOBAL              os
              322  LOAD_METHOD              makedirs
              324  LOAD_FAST                'dirname'
              326  CALL_METHOD_1         1  ''
              328  POP_TOP          
            330_0  COME_FROM           316  '316'
              330  POP_BLOCK        
              332  JUMP_FORWARD        356  'to 356'
            334_0  COME_FROM_FINALLY   300  '300'

 L. 158       334  DUP_TOP          
              336  LOAD_GLOBAL              FileExistsError
              338  COMPARE_OP               exception-match
          340_342  POP_JUMP_IF_FALSE   354  'to 354'
              344  POP_TOP          
              346  POP_TOP          
              348  POP_TOP          

 L. 159       350  POP_EXCEPT       
              352  JUMP_FORWARD        356  'to 356'
            354_0  COME_FROM           340  '340'
              354  END_FINALLY      
            356_0  COME_FROM           352  '352'
            356_1  COME_FROM           332  '332'

 L. 160       356  LOAD_FAST                'invalidation_mode'
              358  LOAD_GLOBAL              PycInvalidationMode
              360  LOAD_ATTR                TIMESTAMP
              362  COMPARE_OP               ==
          364_366  POP_JUMP_IF_FALSE   404  'to 404'

 L. 161       368  LOAD_FAST                'loader'
              370  LOAD_METHOD              path_stats
              372  LOAD_FAST                'file'
              374  CALL_METHOD_1         1  ''
              376  STORE_FAST               'source_stats'

 L. 162       378  LOAD_GLOBAL              importlib
              380  LOAD_ATTR                _bootstrap_external
              382  LOAD_METHOD              _code_to_timestamp_pyc

 L. 163       384  LOAD_FAST                'code'

 L. 163       386  LOAD_FAST                'source_stats'
              388  LOAD_STR                 'mtime'
              390  BINARY_SUBSCR    

 L. 163       392  LOAD_FAST                'source_stats'
              394  LOAD_STR                 'size'
              396  BINARY_SUBSCR    

 L. 162       398  CALL_METHOD_3         3  ''
              400  STORE_FAST               'bytecode'
              402  JUMP_FORWARD        438  'to 438'
            404_0  COME_FROM           364  '364'

 L. 165       404  LOAD_GLOBAL              importlib
              406  LOAD_ATTR                util
              408  LOAD_METHOD              source_hash
              410  LOAD_FAST                'source_bytes'
              412  CALL_METHOD_1         1  ''
              414  STORE_FAST               'source_hash'

 L. 166       416  LOAD_GLOBAL              importlib
              418  LOAD_ATTR                _bootstrap_external
              420  LOAD_METHOD              _code_to_hash_pyc

 L. 167       422  LOAD_FAST                'code'

 L. 168       424  LOAD_FAST                'source_hash'

 L. 169       426  LOAD_FAST                'invalidation_mode'
              428  LOAD_GLOBAL              PycInvalidationMode
              430  LOAD_ATTR                CHECKED_HASH
              432  COMPARE_OP               ==

 L. 166       434  CALL_METHOD_3         3  ''
              436  STORE_FAST               'bytecode'
            438_0  COME_FROM           402  '402'

 L. 171       438  LOAD_GLOBAL              importlib
              440  LOAD_ATTR                _bootstrap_external
              442  LOAD_METHOD              _calc_mode
              444  LOAD_FAST                'file'
              446  CALL_METHOD_1         1  ''
              448  STORE_FAST               'mode'

 L. 172       450  LOAD_GLOBAL              importlib
              452  LOAD_ATTR                _bootstrap_external
              454  LOAD_METHOD              _write_atomic
              456  LOAD_FAST                'cfile'
              458  LOAD_FAST                'bytecode'
              460  LOAD_FAST                'mode'
              462  CALL_METHOD_3         3  ''
              464  POP_TOP          

 L. 173       466  LOAD_FAST                'cfile'
              468  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 280


def main(args=None):
    """Compile several source files.

    The files named in 'args' (or on the command line, if 'args' is
    not specified) are compiled and the resulting bytecode is cached
    in the normal manner.  This function does not search a directory
    structure to locate source files; it only compiles files named
    explicitly.  If '-' is the only parameter in args, the list of
    files is taken from standard input.

    """
    if args is None:
        args = sys.argv[1:]
    rv = 0
    if args == ['-']:
        while True:
            filename = sys.stdin.readline()
            if not filename:
                pass
            else:
                filename = filename.rstrip('\n')
                try:
                    compile(filename, doraise=True)
                except PyCompileError as error:
                    try:
                        rv = 1
                        if quiet < 2:
                            sys.stderr.write('%s\n' % error.msg)
                    finally:
                        error = None
                        del error

                except OSError as error:
                    try:
                        rv = 1
                        if quiet < 2:
                            sys.stderr.write('%s\n' % error)
                    finally:
                        error = None
                        del error

    else:
        pass
    for filename in args:
        try:
            compile(filename, doraise=True)
        except PyCompileError as error:
            try:
                rv = 1
                if quiet < 2:
                    sys.stderr.write('%s\n' % error.msg)
            finally:
                error = None
                del error

    else:
        return rv


if __name__ == '__main__':
    sys.exit(main())