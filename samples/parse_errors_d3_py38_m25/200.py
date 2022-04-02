# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: pydoc.py
"""Generate Python documentation in HTML or text for interactive use.

At the Python interactive prompt, calling help(thing) on a Python object
documents the object, and calling help() starts up an interactive
help session.

Or, at the shell command line outside of Python:

Run "pydoc <name>" to show documentation on something.  <name> may be
the name of a function, module, package, or a dotted reference to a
class or function within a module or module in a package.  If the
argument contains a path segment delimiter (e.g. slash on Unix,
backslash on Windows) it is treated as the path to a Python source file.

Run "pydoc -k <keyword>" to search for a keyword in the synopsis lines
of all available modules.

Run "pydoc -n <hostname>" to start an HTTP server with the given
hostname (default: localhost) on the local machine.

Run "pydoc -p <port>" to start an HTTP server on the given port on the
local machine.  Port number 0 can be used to get an arbitrary unused port.

Run "pydoc -b" to start an HTTP server on an arbitrary unused port and
open a Web browser to interactively browse documentation.  Combine with
the -n and -p options to control the hostname and port used.

Run "pydoc -w <name>" to write out the HTML documentation for a module
to a file named "<name>.html".

Module docs for core modules are assumed to be in

    https://docs.python.org/X.Y/library/

This can be overridden by setting the PYTHONDOCS environment variable
to a different URL or to a local directory containing the Library
Reference Manual pages.
"""
__all__ = [
 'help']
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__date__ = '26 February 2001'
__credits__ = 'Guido van Rossum, for an excellent programming language.\nTommy Burnette, the original creator of manpy.\nPaul Prescod, for all his work on onlinehelp.\nRichard Chamberlain, for the first implementation of textdoc.\n'
import builtins, importlib._bootstrap, importlib._bootstrap_external, importlib.machinery, importlib.util, inspect, io, os, pkgutil, platform, re, sys, sysconfig, time, tokenize, urllib.parse, warnings
from collections import deque
from reprlib import Repr
from traceback import format_exception_only

def pathdirs():
    """Convert sys.path into a list of absolute, existing, unique paths."""
    dirs = []
    normdirs = []
    for dir in sys.path:
        dir = os.path.abspath(dir or '.')
        normdir = os.path.normcase(dir)
        if normdir not in normdirs:
            if os.path.isdir(dir):
                dirs.append(dir)
                normdirs.append(normdir)
    else:
        return dirs


def getdoc(object):
    """Get the doc string or comments for an object."""
    result = inspect.getdoc(object) or inspect.getcomments(object)
    return result and (re.sub('^ *\n', '', result.rstrip())) or ''


def splitdoc(doc):
    """Split a doc string into a synopsis line (if any) and the rest."""
    lines = doc.strip().split('\n')
    if len(lines) == 1:
        return (lines[0], '')
    if len(lines) >= 2:
        if not lines[1].rstrip():
            return (
             lines[0], '\n'.join(lines[2:]))
        return ('', '\n'.join(lines))


def classname(object, modname):
    """Get a class name and qualify it with a module name if necessary."""
    name = object.__name__
    if object.__module__ != modname:
        name = object.__module__ + '.' + name
    return name


def isdata(object):
    """Check if an object is of a type that probably means it's data."""
    return not (inspect.ismodule(object) or inspect.isclass(object) or inspect.isroutine(object) or inspect.isframe(object) or inspect.istraceback(object) or inspect.iscode(object))


def replace(text, *pairs):
    """Do a series of global replacements on a string."""
    while True:
        if pairs:
            text = pairs[1].join(text.split(pairs[0]))
            pairs = pairs[2:]

    return text


def cram(text, maxlen):
    """Omit part of a string if needed to make it fit in a maximum length."""
    if len(text) > maxlen:
        pre = max(0, (maxlen - 3) // 2)
        post = max(0, maxlen - 3 - pre)
        return text[:pre] + '...' + text[len(text) - post:]
    return text


_re_stripid = re.compile(' at 0x[0-9a-f]{6,16}(>+)$', re.IGNORECASE)

def stripid(text):
    """Remove the hexadecimal id from a Python object representation."""
    return _re_stripid.sub('\\1', text)


def _is_bound_method(fn):
    """
    Returns True if fn is a bound method, regardless of whether
    fn was implemented in Python or in C.
    """
    if inspect.ismethod(fn):
        return True
    if inspect.isbuiltin(fn):
        self = getattr(fn, '__self__', None)
        return not (inspect.ismodule(self) or self is None)
    return False


def allmethods(cl):
    methods = {}
    for key, value in inspect.getmembers(cl, inspect.isroutine):
        methods[key] = 1
    else:
        for base in cl.__bases__:
            methods.update(allmethods(base))
        else:
            for key in methods.keys():
                methods[key] = getattr(cl, key)
            else:
                return methods


def _split_list(s, predicate):
    """Split sequence s via predicate, and return pair ([true], [false]).

    The return value is a 2-tuple of lists,
        ([x for x in s if predicate(x)],
         [x for x in s if not predicate(x)])
    """
    yes = []
    no = []
    for x in s:
        if predicate(x):
            yes.append(x)
        else:
            no.append(x)
    else:
        return (
         yes, no)


def visiblename(name, all=None, obj=None):
    """Decide whether to show documentation on a variable."""
    if name in frozenset({'__qualname__', '__cached__', '__loader__', '__doc__', '__author__', '__slots__', '__package__', '__credits__', '__file__', '__builtins__', '__module__', '__name__', '__version__', '__path__', '__date__', '__spec__'}):
        return 0
    if name.startswith('__'):
        if name.endswith('__'):
            return 1
    if name.startswith('_'):
        if hasattr(obj, '_fields'):
            return True
    if all is not None:
        return name in all
    return not name.startswith('_')


def classify_class_attrs(object):
    """Wrap inspect.classify_class_attrs, with fixup for data descriptors."""
    results = []
    for name, kind, cls, value in inspect.classify_class_attrs(object):
        if inspect.isdatadescriptor(value):
            kind = 'data descriptor'
            if isinstance(value, property):
                if value.fset is None:
                    kind = 'readonly property'
        results.append((name, kind, cls, value))
    else:
        return results


def sort_attributes(attrs, object):
    """Sort the attrs list in-place by _fields and then alphabetically by name"""
    fields = getattr(object, '_fields', [])
    try:
        field_order = {i - len(fields):name for i, name in enumerate(fields)}
    except TypeError:
        field_order = {}
    else:
        keyfunc = lambda attr: (
         field_order.get(attr[0], 0), attr[0])
        attrs.sort(key=keyfunc)


def ispackage(path):
    """Guess whether a path refers to a package directory."""
    if os.path.isdir(path):
        for ext in ('.py', '.pyc'):
            if os.path.isfile(os.path.join(path, '__init__' + ext)):
                return True

        return False


def source_synopsis--- This code section failed: ---

 L. 235         0  LOAD_FAST                'file'
                2  LOAD_METHOD              readline
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'line'
              8_0  COME_FROM            46  '46'
              8_1  COME_FROM            42  '42'

 L. 236         8  LOAD_FAST                'line'
               10  LOAD_CONST               None
               12  LOAD_CONST               1
               14  BUILD_SLICE_2         2 
               16  BINARY_SUBSCR    
               18  LOAD_STR                 '#'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_TRUE     32  'to 32'
               24  LOAD_FAST                'line'
               26  LOAD_METHOD              strip
               28  CALL_METHOD_0         0  ''
               30  POP_JUMP_IF_TRUE     48  'to 48'
             32_0  COME_FROM            22  '22'

 L. 237        32  LOAD_FAST                'file'
               34  LOAD_METHOD              readline
               36  CALL_METHOD_0         0  ''
               38  STORE_FAST               'line'

 L. 238        40  LOAD_FAST                'line'
               42  POP_JUMP_IF_TRUE_BACK     8  'to 8'

 L. 238        44  JUMP_FORWARD         48  'to 48'
               46  JUMP_BACK             8  'to 8'
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            30  '30'

 L. 239        48  LOAD_FAST                'line'
               50  LOAD_METHOD              strip
               52  CALL_METHOD_0         0  ''
               54  STORE_FAST               'line'

 L. 240        56  LOAD_FAST                'line'
               58  LOAD_CONST               None
               60  LOAD_CONST               4
               62  BUILD_SLICE_2         2 
               64  BINARY_SUBSCR    
               66  LOAD_STR                 'r"""'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    84  'to 84'

 L. 240        72  LOAD_FAST                'line'
               74  LOAD_CONST               1
               76  LOAD_CONST               None
               78  BUILD_SLICE_2         2 
               80  BINARY_SUBSCR    
               82  STORE_FAST               'line'
             84_0  COME_FROM            70  '70'

 L. 241        84  LOAD_FAST                'line'
               86  LOAD_CONST               None
               88  LOAD_CONST               3
               90  BUILD_SLICE_2         2 
               92  BINARY_SUBSCR    
               94  LOAD_STR                 '"""'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   184  'to 184'

 L. 242       100  LOAD_FAST                'line'
              102  LOAD_CONST               3
              104  LOAD_CONST               None
              106  BUILD_SLICE_2         2 
              108  BINARY_SUBSCR    
              110  STORE_FAST               'line'

 L. 243       112  LOAD_FAST                'line'
              114  LOAD_CONST               -1
              116  LOAD_CONST               None
              118  BUILD_SLICE_2         2 
              120  BINARY_SUBSCR    
              122  LOAD_STR                 '\\'
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   140  'to 140'

 L. 243       128  LOAD_FAST                'line'
              130  LOAD_CONST               None
              132  LOAD_CONST               -1
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  STORE_FAST               'line'
            140_0  COME_FROM           162  '162'
            140_1  COME_FROM           158  '158'
            140_2  COME_FROM           126  '126'

 L. 244       140  LOAD_FAST                'line'
              142  LOAD_METHOD              strip
              144  CALL_METHOD_0         0  ''
              146  POP_JUMP_IF_TRUE    164  'to 164'

 L. 245       148  LOAD_FAST                'file'
              150  LOAD_METHOD              readline
              152  CALL_METHOD_0         0  ''
              154  STORE_FAST               'line'

 L. 246       156  LOAD_FAST                'line'
              158  POP_JUMP_IF_TRUE_BACK   140  'to 140'

 L. 246       160  JUMP_FORWARD        164  'to 164'
              162  JUMP_BACK           140  'to 140'
            164_0  COME_FROM           160  '160'
            164_1  COME_FROM           146  '146'

 L. 247       164  LOAD_FAST                'line'
              166  LOAD_METHOD              split
              168  LOAD_STR                 '"""'
              170  CALL_METHOD_1         1  ''
              172  LOAD_CONST               0
              174  BINARY_SUBSCR    
              176  LOAD_METHOD              strip
              178  CALL_METHOD_0         0  ''
              180  STORE_FAST               'result'
              182  JUMP_FORWARD        188  'to 188'
            184_0  COME_FROM            98  '98'

 L. 248       184  LOAD_CONST               None
              186  STORE_FAST               'result'
            188_0  COME_FROM           182  '182'

 L. 249       188  LOAD_FAST                'result'
              190  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 46


def synopsis--- This code section failed: ---

 L. 253         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              stat
                4  LOAD_FAST                'filename'
                6  CALL_METHOD_1         1  ''
                8  LOAD_ATTR                st_mtime
               10  STORE_FAST               'mtime'

 L. 254        12  LOAD_FAST                'cache'
               14  LOAD_METHOD              get
               16  LOAD_FAST                'filename'
               18  LOAD_CONST               (None, None)
               20  CALL_METHOD_2         2  ''
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'lastupdate'
               26  STORE_FAST               'result'

 L. 255        28  LOAD_FAST                'lastupdate'
               30  LOAD_CONST               None
               32  COMPARE_OP               is
               34  POP_JUMP_IF_TRUE     46  'to 46'
               36  LOAD_FAST                'lastupdate'
               38  LOAD_FAST                'mtime'
               40  COMPARE_OP               <
            42_44  POP_JUMP_IF_FALSE   284  'to 284'
             46_0  COME_FROM            34  '34'

 L. 257        46  LOAD_FAST                'filename'
               48  LOAD_METHOD              endswith
               50  LOAD_GLOBAL              tuple
               52  LOAD_GLOBAL              importlib
               54  LOAD_ATTR                machinery
               56  LOAD_ATTR                BYTECODE_SUFFIXES
               58  CALL_FUNCTION_1       1  ''
               60  CALL_METHOD_1         1  ''
               62  POP_JUMP_IF_FALSE    74  'to 74'

 L. 258        64  LOAD_GLOBAL              importlib
               66  LOAD_ATTR                machinery
               68  LOAD_ATTR                SourcelessFileLoader
               70  STORE_FAST               'loader_cls'
               72  JUMP_FORWARD        106  'to 106'
             74_0  COME_FROM            62  '62'

 L. 259        74  LOAD_FAST                'filename'
               76  LOAD_METHOD              endswith
               78  LOAD_GLOBAL              tuple
               80  LOAD_GLOBAL              importlib
               82  LOAD_ATTR                machinery
               84  LOAD_ATTR                EXTENSION_SUFFIXES
               86  CALL_FUNCTION_1       1  ''
               88  CALL_METHOD_1         1  ''
               90  POP_JUMP_IF_FALSE   102  'to 102'

 L. 260        92  LOAD_GLOBAL              importlib
               94  LOAD_ATTR                machinery
               96  LOAD_ATTR                ExtensionFileLoader
               98  STORE_FAST               'loader_cls'
              100  JUMP_FORWARD        106  'to 106'
            102_0  COME_FROM            90  '90'

 L. 262       102  LOAD_CONST               None
              104  STORE_FAST               'loader_cls'
            106_0  COME_FROM           100  '100'
            106_1  COME_FROM            72  '72'

 L. 264       106  LOAD_FAST                'loader_cls'
              108  LOAD_CONST               None
              110  COMPARE_OP               is
              112  POP_JUMP_IF_FALSE   178  'to 178'

 L. 266       114  SETUP_FINALLY       130  'to 130'

 L. 267       116  LOAD_GLOBAL              tokenize
              118  LOAD_METHOD              open
              120  LOAD_FAST                'filename'
              122  CALL_METHOD_1         1  ''
              124  STORE_FAST               'file'
              126  POP_BLOCK        
              128  JUMP_FORWARD        152  'to 152'
            130_0  COME_FROM_FINALLY   114  '114'

 L. 268       130  DUP_TOP          
              132  LOAD_GLOBAL              OSError
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   150  'to 150'
              138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L. 270       144  POP_EXCEPT       
              146  LOAD_CONST               None
              148  RETURN_VALUE     
            150_0  COME_FROM           136  '136'
              150  END_FINALLY      
            152_0  COME_FROM           128  '128'

 L. 272       152  LOAD_FAST                'file'
              154  SETUP_WITH          170  'to 170'
              156  POP_TOP          

 L. 273       158  LOAD_GLOBAL              source_synopsis
              160  LOAD_FAST                'file'
              162  CALL_FUNCTION_1       1  ''
              164  STORE_FAST               'result'
              166  POP_BLOCK        
              168  BEGIN_FINALLY    
            170_0  COME_FROM_WITH      154  '154'
              170  WITH_CLEANUP_START
              172  WITH_CLEANUP_FINISH
              174  END_FINALLY      
              176  JUMP_FORWARD        272  'to 272'
            178_0  COME_FROM           112  '112'

 L. 276       178  LOAD_FAST                'loader_cls'
              180  LOAD_STR                 '__temp__'
              182  LOAD_FAST                'filename'
              184  CALL_FUNCTION_2       2  ''
              186  STORE_FAST               'loader'

 L. 278       188  LOAD_GLOBAL              importlib
              190  LOAD_ATTR                util
              192  LOAD_ATTR                spec_from_file_location
              194  LOAD_STR                 '__temp__'
              196  LOAD_FAST                'filename'

 L. 279       198  LOAD_FAST                'loader'

 L. 278       200  LOAD_CONST               ('loader',)
              202  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              204  STORE_FAST               'spec'

 L. 280       206  SETUP_FINALLY       224  'to 224'

 L. 281       208  LOAD_GLOBAL              importlib
              210  LOAD_ATTR                _bootstrap
              212  LOAD_METHOD              _load
              214  LOAD_FAST                'spec'
              216  CALL_METHOD_1         1  ''
              218  STORE_FAST               'module'
              220  POP_BLOCK        
              222  JUMP_FORWARD        238  'to 238'
            224_0  COME_FROM_FINALLY   206  '206'

 L. 282       224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L. 283       230  POP_EXCEPT       
              232  LOAD_CONST               None
              234  RETURN_VALUE     
              236  END_FINALLY      
            238_0  COME_FROM           222  '222'

 L. 284       238  LOAD_GLOBAL              sys
              240  LOAD_ATTR                modules
              242  LOAD_STR                 '__temp__'
              244  DELETE_SUBSCR    

 L. 285       246  LOAD_FAST                'module'
              248  LOAD_ATTR                __doc__
          250_252  POP_JUMP_IF_FALSE   268  'to 268'
              254  LOAD_FAST                'module'
              256  LOAD_ATTR                __doc__
              258  LOAD_METHOD              splitlines
              260  CALL_METHOD_0         0  ''
              262  LOAD_CONST               0
              264  BINARY_SUBSCR    
              266  JUMP_FORWARD        270  'to 270'
            268_0  COME_FROM           250  '250'
              268  LOAD_CONST               None
            270_0  COME_FROM           266  '266'
              270  STORE_FAST               'result'
            272_0  COME_FROM           176  '176'

 L. 287       272  LOAD_FAST                'mtime'
              274  LOAD_FAST                'result'
              276  BUILD_TUPLE_2         2 
              278  LOAD_FAST                'cache'
              280  LOAD_FAST                'filename'
              282  STORE_SUBSCR     
            284_0  COME_FROM            42  '42'

 L. 288       284  LOAD_FAST                'result'
              286  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 232


class ErrorDuringImport(Exception):
    __doc__ = 'Errors that occurred while trying to import something to document it.'

    def __init__(self, filename, exc_info):
        self.filename = filename
        self.exc, self.value, self.tb = exc_info

    def __str__(self):
        exc = self.exc.__name__
        return 'problem in %s - %s: %s' % (self.filename, exc, self.value)


def importfile--- This code section failed: ---

 L. 302         0  LOAD_GLOBAL              importlib
                2  LOAD_ATTR                util
                4  LOAD_ATTR                MAGIC_NUMBER
                6  STORE_FAST               'magic'

 L. 303         8  LOAD_GLOBAL              open
               10  LOAD_FAST                'path'
               12  LOAD_STR                 'rb'
               14  CALL_FUNCTION_2       2  ''
               16  SETUP_WITH           42  'to 42'
               18  STORE_FAST               'file'

 L. 304        20  LOAD_FAST                'magic'
               22  LOAD_FAST                'file'
               24  LOAD_METHOD              read
               26  LOAD_GLOBAL              len
               28  LOAD_FAST                'magic'
               30  CALL_FUNCTION_1       1  ''
               32  CALL_METHOD_1         1  ''
               34  COMPARE_OP               ==
               36  STORE_FAST               'is_bytecode'
               38  POP_BLOCK        
               40  BEGIN_FINALLY    
             42_0  COME_FROM_WITH       16  '16'
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  END_FINALLY      

 L. 305        48  LOAD_GLOBAL              os
               50  LOAD_ATTR                path
               52  LOAD_METHOD              basename
               54  LOAD_FAST                'path'
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'filename'

 L. 306        60  LOAD_GLOBAL              os
               62  LOAD_ATTR                path
               64  LOAD_METHOD              splitext
               66  LOAD_FAST                'filename'
               68  CALL_METHOD_1         1  ''
               70  UNPACK_SEQUENCE_2     2 
               72  STORE_FAST               'name'
               74  STORE_FAST               'ext'

 L. 307        76  LOAD_FAST                'is_bytecode'
               78  POP_JUMP_IF_FALSE    96  'to 96'

 L. 308        80  LOAD_GLOBAL              importlib
               82  LOAD_ATTR                _bootstrap_external
               84  LOAD_METHOD              SourcelessFileLoader
               86  LOAD_FAST                'name'
               88  LOAD_FAST                'path'
               90  CALL_METHOD_2         2  ''
               92  STORE_FAST               'loader'
               94  JUMP_FORWARD        110  'to 110'
             96_0  COME_FROM            78  '78'

 L. 310        96  LOAD_GLOBAL              importlib
               98  LOAD_ATTR                _bootstrap_external
              100  LOAD_METHOD              SourceFileLoader
              102  LOAD_FAST                'name'
              104  LOAD_FAST                'path'
              106  CALL_METHOD_2         2  ''
              108  STORE_FAST               'loader'
            110_0  COME_FROM            94  '94'

 L. 312       110  LOAD_GLOBAL              importlib
              112  LOAD_ATTR                util
              114  LOAD_ATTR                spec_from_file_location
              116  LOAD_FAST                'name'
              118  LOAD_FAST                'path'
              120  LOAD_FAST                'loader'
              122  LOAD_CONST               ('loader',)
              124  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              126  STORE_FAST               'spec'

 L. 313       128  SETUP_FINALLY       144  'to 144'

 L. 314       130  LOAD_GLOBAL              importlib
              132  LOAD_ATTR                _bootstrap
              134  LOAD_METHOD              _load
              136  LOAD_FAST                'spec'
              138  CALL_METHOD_1         1  ''
              140  POP_BLOCK        
              142  RETURN_VALUE     
            144_0  COME_FROM_FINALLY   128  '128'

 L. 315       144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 316       150  LOAD_GLOBAL              ErrorDuringImport
              152  LOAD_FAST                'path'
              154  LOAD_GLOBAL              sys
              156  LOAD_METHOD              exc_info
              158  CALL_METHOD_0         0  ''
              160  CALL_FUNCTION_2       2  ''
              162  RAISE_VARARGS_1       1  'exception instance'
              164  POP_EXCEPT       
              166  JUMP_FORWARD        170  'to 170'
              168  END_FINALLY      
            170_0  COME_FROM           166  '166'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 162


def safeimport--- This code section failed: ---

 L. 326         0  SETUP_FINALLY        96  'to 96'

 L. 331         2  LOAD_FAST                'forceload'
                4  POP_JUMP_IF_FALSE    84  'to 84'
                6  LOAD_DEREF               'path'
                8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                modules
               12  COMPARE_OP               in
               14  POP_JUMP_IF_FALSE    84  'to 84'

 L. 332        16  LOAD_DEREF               'path'
               18  LOAD_GLOBAL              sys
               20  LOAD_ATTR                builtin_module_names
               22  COMPARE_OP               not-in
               24  POP_JUMP_IF_FALSE    84  'to 84'

 L. 338        26  LOAD_CLOSURE             'path'
               28  BUILD_TUPLE_1         1 
               30  LOAD_LISTCOMP            '<code_object <listcomp>>'
               32  LOAD_STR                 'safeimport.<locals>.<listcomp>'
               34  MAKE_FUNCTION_8          'closure'
               36  LOAD_GLOBAL              sys
               38  LOAD_ATTR                modules
               40  GET_ITER         
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'subs'

 L. 339        46  LOAD_DEREF               'path'
               48  BUILD_LIST_1          1 
               50  LOAD_FAST                'subs'
               52  BINARY_ADD       
               54  GET_ITER         
             56_0  COME_FROM            82  '82'
               56  FOR_ITER             84  'to 84'
               58  STORE_FAST               'key'

 L. 341        60  LOAD_GLOBAL              sys
               62  LOAD_ATTR                modules
               64  LOAD_FAST                'key'
               66  BINARY_SUBSCR    
               68  LOAD_FAST                'cache'
               70  LOAD_FAST                'key'
               72  STORE_SUBSCR     

 L. 342        74  LOAD_GLOBAL              sys
               76  LOAD_ATTR                modules
               78  LOAD_FAST                'key'
               80  DELETE_SUBSCR    
               82  JUMP_BACK            56  'to 56'
             84_0  COME_FROM            56  '56'
             84_1  COME_FROM            24  '24'
             84_2  COME_FROM            14  '14'
             84_3  COME_FROM             4  '4'

 L. 343        84  LOAD_GLOBAL              __import__
               86  LOAD_DEREF               'path'
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'module'
               92  POP_BLOCK        
               94  JUMP_FORWARD        218  'to 218'
             96_0  COME_FROM_FINALLY     0  '0'

 L. 344        96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 346       102  LOAD_GLOBAL              sys
              104  LOAD_METHOD              exc_info
              106  CALL_METHOD_0         0  ''
              108  DUP_TOP          
              110  UNPACK_SEQUENCE_3     3 
              112  STORE_FAST               'exc'
              114  STORE_FAST               'value'
              116  STORE_FAST               'tb'
              118  STORE_FAST               'info'

 L. 347       120  LOAD_DEREF               'path'
              122  LOAD_GLOBAL              sys
              124  LOAD_ATTR                modules
              126  COMPARE_OP               in
              128  POP_JUMP_IF_FALSE   150  'to 150'

 L. 349       130  LOAD_GLOBAL              ErrorDuringImport
              132  LOAD_GLOBAL              sys
              134  LOAD_ATTR                modules
              136  LOAD_DEREF               'path'
              138  BINARY_SUBSCR    
              140  LOAD_ATTR                __file__
              142  LOAD_FAST                'info'
              144  CALL_FUNCTION_2       2  ''
              146  RAISE_VARARGS_1       1  'exception instance'
              148  JUMP_FORWARD        212  'to 212'
            150_0  COME_FROM           128  '128'

 L. 350       150  LOAD_FAST                'exc'
              152  LOAD_GLOBAL              SyntaxError
              154  COMPARE_OP               is
              156  POP_JUMP_IF_FALSE   172  'to 172'

 L. 352       158  LOAD_GLOBAL              ErrorDuringImport
              160  LOAD_FAST                'value'
              162  LOAD_ATTR                filename
              164  LOAD_FAST                'info'
              166  CALL_FUNCTION_2       2  ''
              168  RAISE_VARARGS_1       1  'exception instance'
              170  JUMP_FORWARD        212  'to 212'
            172_0  COME_FROM           156  '156'

 L. 353       172  LOAD_GLOBAL              issubclass
              174  LOAD_FAST                'exc'
              176  LOAD_GLOBAL              ImportError
              178  CALL_FUNCTION_2       2  ''
              180  POP_JUMP_IF_FALSE   198  'to 198'
              182  LOAD_FAST                'value'
              184  LOAD_ATTR                name
              186  LOAD_DEREF               'path'
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   198  'to 198'

 L. 355       192  POP_EXCEPT       
              194  LOAD_CONST               None
              196  RETURN_VALUE     
            198_0  COME_FROM           190  '190'
            198_1  COME_FROM           180  '180'

 L. 358       198  LOAD_GLOBAL              ErrorDuringImport
              200  LOAD_DEREF               'path'
              202  LOAD_GLOBAL              sys
              204  LOAD_METHOD              exc_info
              206  CALL_METHOD_0         0  ''
              208  CALL_FUNCTION_2       2  ''
              210  RAISE_VARARGS_1       1  'exception instance'
            212_0  COME_FROM           170  '170'
            212_1  COME_FROM           148  '148'
              212  POP_EXCEPT       
              214  JUMP_FORWARD        218  'to 218'
              216  END_FINALLY      
            218_0  COME_FROM           214  '214'
            218_1  COME_FROM            94  '94'

 L. 359       218  LOAD_DEREF               'path'
              220  LOAD_METHOD              split
              222  LOAD_STR                 '.'
              224  CALL_METHOD_1         1  ''
              226  LOAD_CONST               1
              228  LOAD_CONST               None
              230  BUILD_SLICE_2         2 
              232  BINARY_SUBSCR    
              234  GET_ITER         
            236_0  COME_FROM           282  '282'
            236_1  COME_FROM           254  '254'
              236  FOR_ITER            284  'to 284'
              238  STORE_FAST               'part'

 L. 360       240  SETUP_FINALLY       256  'to 256'

 L. 360       242  LOAD_GLOBAL              getattr
              244  LOAD_FAST                'module'
              246  LOAD_FAST                'part'
              248  CALL_FUNCTION_2       2  ''
              250  STORE_FAST               'module'
              252  POP_BLOCK        
              254  JUMP_BACK           236  'to 236'
            256_0  COME_FROM_FINALLY   240  '240'

 L. 361       256  DUP_TOP          
              258  LOAD_GLOBAL              AttributeError
              260  COMPARE_OP               exception-match
          262_264  POP_JUMP_IF_FALSE   280  'to 280'
              266  POP_TOP          
              268  POP_TOP          
              270  POP_TOP          

 L. 361       272  POP_EXCEPT       
              274  POP_TOP          
              276  LOAD_CONST               None
              278  RETURN_VALUE     
            280_0  COME_FROM           262  '262'
              280  END_FINALLY      
              282  JUMP_BACK           236  'to 236'
            284_0  COME_FROM           236  '236'

 L. 362       284  LOAD_FAST                'module'
              286  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 194


class Doc:
    PYTHONDOCS = os.environ.get('PYTHONDOCS', 'https://docs.python.org/%d.%d/library' % sys.version_info[:2])

    def document(self, object, name=None, *args):
        """Generate documentation for an object."""
        args = (
         object, name) + args
        try:
            if inspect.ismodule(object):
                return (self.docmodule)(*args)
            if inspect.isclass(object):
                return (self.docclass)(*args)
            if inspect.isroutine(object):
                return (self.docroutine)(*args)
        except AttributeError:
            pass
        else:
            if inspect.isdatadescriptor(object):
                return (self.docdata)(*args)
            else:
                return (self.docother)(*args)

    def fail(self, object, name=None, *args):
        """Raise an exception for unimplemented types."""
        message = "don't know how to document object%s of type %s" % (
         name and ' ' + repr(name), type(object).__name__)
        raise TypeError(message)

    docmodule = docclass = docroutine = docother = docproperty = docdata = fail

    def getdocloc(self, object, basedir=sysconfig.get_path('stdlib')):
        """Return the location of module docs or None"""
        try:
            file = inspect.getabsfile(object)
        except TypeError:
            file = '(built-in)'
        else:
            docloc = os.environ.get('PYTHONDOCS', self.PYTHONDOCS)
            basedir = os.path.normcase(basedir)
            if not (isinstance(object, type(os)) and (object.__name__ in ('errno',
                                                                          'exceptions',
                                                                          'gc', 'imp',
                                                                          'marshal',
                                                                          'posix',
                                                                          'signal',
                                                                          'sys',
                                                                          '_thread',
                                                                          'zipimport') or file.startswith)(basedir) and file.startswith(os.path.join(basedir, 'site-packages'))) and object.__name__ not in ('xml.etree',
                                                                                                                                                                                                             'test.pydoc_mod'):
                if docloc.startswith(('http://', 'https://')):
                    docloc = '%s/%s' % (docloc.rstrip('/'), object.__name__.lower())
                else:
                    docloc = os.path.join(docloc, object.__name__.lower() + '.html')
            else:
                docloc = None
            return docloc


class HTMLRepr(Repr):
    __doc__ = 'Class for safely making an HTML representation of a Python object.'

    def __init__(self):
        Repr.__init__(self)
        self.maxlist = self.maxtuple = 20
        self.maxdict = 10
        self.maxstring = self.maxother = 100

    def escape(self, text):
        return replace(text, '&', '&amp;', '<', '&lt;', '>', '&gt;')

    def repr(self, object):
        return Repr.repr(self, object)

    def repr1(self, x, level):
        if hasattr(type(x), '__name__'):
            methodname = 'repr_' + '_'.join(type(x).__name__.split())
            if hasattr(self, methodname):
                return getattr(self, methodname)(x, level)
        return self.escape(cram(stripid(repr(x)), self.maxother))

    def repr_string(self, x, level):
        test = cram(x, self.maxstring)
        testrepr = repr(test)
        if '\\' in test:
            if '\\' not in replace(testrepr, '\\\\', ''):
                return 'r' + testrepr[0] + self.escape(test) + testrepr[0]
        return re.sub('((\\\\[\\\\abfnrtv\\\'"]|\\\\[0-9]..|\\\\x..|\\\\u....)+)', '<font color="#c040c0">\\1</font>', self.escape(testrepr))

    repr_str = repr_string

    def repr_instance(self, x, level):
        try:
            return self.escape(cram(stripid(repr(x)), self.maxstring))
        except:
            return self.escape('<%s instance>' % x.__class__.__name__)

    repr_unicode = repr_string


class HTMLDoc(Doc):
    __doc__ = 'Formatter class for HTML documentation.'
    _repr_instance = HTMLRepr()
    repr = _repr_instance.repr
    escape = _repr_instance.escape

    def page(self, title, contents):
        """Format an HTML page."""
        return '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n<html><head><title>Python: %s</title>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n</head><body bgcolor="#f0f0f8">\n%s\n</body></html>' % (
         title, contents)

    def heading(self, title, fgcol, bgcol, extras=''):
        """Format a page heading."""
        return '\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="heading">\n<tr bgcolor="%s">\n<td valign=bottom>&nbsp;<br>\n<font color="%s" face="helvetica, arial">&nbsp;<br>%s</font></td\n><td align=right valign=bottom\n><font color="%s" face="helvetica, arial">%s</font></td></tr></table>\n    ' % (
         bgcol, fgcol, title, fgcol, extras or '&nbsp;')

    def section(self, title, fgcol, bgcol, contents, width=6, prelude='', marginalia=None, gap='&nbsp;'):
        """Format a section with a heading."""
        if marginalia is None:
            marginalia = '<tt>' + '&nbsp;' * width + '</tt>'
        result = '<p>\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="section">\n<tr bgcolor="%s">\n<td colspan=3 valign=bottom>&nbsp;<br>\n<font color="%s" face="helvetica, arial">%s</font></td></tr>\n    ' % (
         bgcol, fgcol, title)
        if prelude:
            result = result + '\n<tr bgcolor="%s"><td rowspan=2>%s</td>\n<td colspan=2>%s</td></tr>\n<tr><td>%s</td>' % (
             bgcol, marginalia, prelude, gap)
        else:
            result = result + '\n<tr><td bgcolor="%s">%s</td><td>%s</td>' % (
             bgcol, marginalia, gap)
        return result + '\n<td width="100%%">%s</td></tr></table>' % contents

    def bigsection(self, title, *args):
        """Format a section with a big heading."""
        title = '<big><strong>%s</strong></big>' % title
        return (self.section)(title, *args)

    def preformat(self, text):
        """Format literal preformatted text."""
        text = self.escape(text.expandtabs())
        return replace(text, '\n\n', '\n \n', '\n\n', '\n \n', ' ', '&nbsp;', '\n', '<br>\n')

    def multicolumn(self, list, format, cols=4):
        """Format a list of items into a multi-column list."""
        result = ''
        rows = (len(list) + cols - 1) // cols
        for col in range(cols):
            result = result + '<td width="%d%%" valign=top>' % (100 // cols)
            for i in range(rows * col, rows * col + rows):
                if i < len(list):
                    result = result + format(list[i]) + '<br>\n'
                result = result + '</td>'
            else:
                return '<table width="100%%" summary="list"><tr>%s</tr></table>' % result

    def grey(self, text):
        return '<font color="#909090">%s</font>' % text

    def namelink(self, name, *dicts):
        """Make a link for an identifier, given name-to-URL mappings."""
        for dict in dicts:
            if name in dict:
                return '<a href="%s">%s</a>' % (dict[name], name)
        else:
            return name

    def classlink(self, object, modname):
        """Make a link for a class."""
        name, module = object.__name__, sys.modules.get(object.__module__)
        if hasattr(module, name):
            if getattr(module, name) is object:
                return '<a href="%s.html#%s">%s</a>' % (
                 module.__name__, name, classname(object, modname))
        return classname(object, modname)

    def modulelink(self, object):
        """Make a link for a module."""
        return '<a href="%s.html">%s</a>' % (object.__name__, object.__name__)

    def modpkglink(self, modpkginfo):
        """Make a link for a module or package to display in an index."""
        name, path, ispackage, shadowed = modpkginfo
        if shadowed:
            return self.grey(name)
        if path:
            url = '%s.%s.html' % (path, name)
        else:
            url = '%s.html' % name
        if ispackage:
            text = '<strong>%s</strong>&nbsp;(package)' % name
        else:
            text = name
        return '<a href="%s">%s</a>' % (url, text)

    def filelink(self, url, path):
        """Make a link to source file."""
        return '<a href="file:%s">%s</a>' % (url, path)

    def markup(self, text, escape=None, funcs={}, classes={}, methods={}):
        """Mark up some plain text, given a context of symbols to look for.
        Each context dictionary maps object names to anchor names."""
        escape = escape or self.escape
        results = []
        here = 0
        pattern = re.compile('\\b((http|ftp)://\\S+[\\w/]|RFC[- ]?(\\d+)|PEP[- ]?(\\d+)|(self\\.)?(\\w+))')
        while True:
            match = pattern.search(text, here)
            if not match:
                pass
            else:
                start, end = match.span()
                results.append(escape(text[here:start]))
                all, scheme, rfc, pep, selfdot, name = match.groups()
                if scheme:
                    url = escape(all).replace('"', '&quot;')
                    results.append('<a href="%s">%s</a>' % (url, url))
                elif rfc:
                    url = 'http://www.rfc-editor.org/rfc/rfc%d.txt' % int(rfc)
                    results.append('<a href="%s">%s</a>' % (url, escape(all)))
                elif pep:
                    url = 'http://www.python.org/dev/peps/pep-%04d/' % int(pep)
                    results.append('<a href="%s">%s</a>' % (url, escape(all)))
                elif selfdot:
                    if text[end:end + 1] == '(':
                        results.append('self.' + self.namelink(name, methods))
                    else:
                        results.append('self.<strong>%s</strong>' % name)
                elif text[end:end + 1] == '(':
                    results.append(self.namelink(name, methods, funcs, classes))
                else:
                    results.append(self.namelink(name, classes))
                here = end

        results.append(escape(text[here:]))
        return ''.join(results)

    def formattree(self, tree, modname, parent=None):
        """Produce HTML for a class tree as given by inspect.getclasstree()."""
        result = ''
        for entry in tree:
            if type(entry) is type(()):
                c, bases = entry
                result = result + '<dt><font face="helvetica, arial">'
                result = result + self.classlink(c, modname)
                if bases:
                    if bases != (parent,):
                        parents = []
                        for base in bases:
                            parents.append(self.classlink(base, modname))
                        else:
                            result = result + '(' + ', '.join(parents) + ')'

                result = result + '\n</font></dt>'
            else:
                if type(entry) is type([]):
                    result = result + '<dd>\n%s</dd>\n' % self.formattree(entry, modname, c)
        else:
            return '<dl>\n%s</dl>\n' % result

    def docmodule(self, object, name=None, mod=None, *ignored):
        """Produce HTML documentation for a module object."""
        name = object.__name__
        try:
            all = object.__all__
        except AttributeError:
            all = None
        else:
            parts = name.split('.')
            links = []
        for i in range(len(parts) - 1):
            links.append('<a href="%s.html"><font color="#ffffff">%s</font></a>' % (
             '.'.join(parts[:i + 1]), parts[i]))
        else:
            linkedname = '.'.join(links + parts[-1:])
            head = '<big><big><strong>%s</strong></big></big>' % linkedname

        try:
            path = inspect.getabsfile(object)
            url = urllib.parse.quote(path)
            filelink = self.filelink(url, path)
        except TypeError:
            filelink = '(built-in)'
        else:
            info = []
            if hasattr(object, '__version__'):
                version = str(object.__version__)
                if version[:11] == '$Revision: ':
                    if version[-1:] == '$':
                        version = version[11:-1].strip()
                info.append('version %s' % self.escape(version))
            if hasattr(object, '__date__'):
                info.append(self.escape(str(object.__date__)))
            if info:
                head = head + ' (%s)' % ', '.join(info)
            docloc = self.getdocloc(object)
            if docloc is not None:
                docloc = '<br><a href="%(docloc)s">Module Reference</a>' % locals()
            else:
                docloc = ''
            result = self.heading(head, '#ffffff', '#7799ee', '<a href=".">index</a><br>' + filelink + docloc)
            modules = inspect.getmembers(object, inspect.ismodule)
            classes, cdict = [], {}
            for key, value in inspect.getmembers(object, inspect.isclass):
                if not all is not None:
                    if (inspect.getmodule(value) or object) is object:
                        pass
                if visiblename(key, all, object):
                    classes.append((key, value))
                    cdict[key] = cdict[value] = '#' + key
            else:
                for key, value in classes:
                    for base in value.__bases__:
                        key, modname = base.__name__, base.__module__
                        module = sys.modules.get(modname)
                        if modname != name:
                            if module:
                                if hasattr(module, key):
                                    if getattr(module, key) is base:
                                        if key not in cdict:
                                            cdict[key] = cdict[base] = modname + '.html#' + key

                else:
                    funcs, fdict = [], {}
                    for key, value in inspect.getmembers(object, inspect.isroutine):
                        if not all is not None:
                            if not inspect.isbuiltin(value):
                                if inspect.getmodule(value) is object:
                                    pass
                        if visiblename(key, all, object):
                            funcs.append((key, value))
                            fdict[key] = '#-' + key
                            if inspect.isfunction(value):
                                fdict[value] = fdict[key]
                    else:
                        data = []
                        for key, value in inspect.getmembers(object, isdata):
                            if visiblename(key, all, object):
                                data.append((key, value))
                        else:
                            doc = self.markup(getdoc(object), self.preformat, fdict, cdict)
                            doc = doc and '<tt>%s</tt>' % doc
                            result = result + '<p>%s</p>\n' % doc
                            if hasattr(object, '__path__'):
                                modpkgs = []
                                for importer, modname, ispkg in pkgutil.iter_modules(object.__path__):
                                    modpkgs.append((modname, name, ispkg, 0))
                                else:
                                    modpkgs.sort()
                                    contents = self.multicolumn(modpkgs, self.modpkglink)
                                    result = result + self.bigsection('Package Contents', '#ffffff', '#aa55cc', contents)

                            elif modules:
                                contents = self.multicolumn(modules, lambda t: self.modulelink(t[1]))
                                result = result + self.bigsection('Modules', '#ffffff', '#aa55cc', contents)
                            if classes:
                                classlist = [value for key, value in classes]
                                contents = [
                                 self.formattree(inspect.getclasstree(classlist, 1), name)]
                                for key, value in classes:
                                    contents.append(self.document(value, key, name, fdict, cdict))
                                else:
                                    result = result + self.bigsection('Classes', '#ffffff', '#ee77aa', ' '.join(contents))

                            if funcs:
                                contents = []
                                for key, value in funcs:
                                    contents.append(self.document(value, key, name, fdict, cdict))
                                else:
                                    result = result + self.bigsection('Functions', '#ffffff', '#eeaa77', ' '.join(contents))

                            if data:
                                contents = []
                                for key, value in data:
                                    contents.append(self.document(value, key))
                                else:
                                    result = result + self.bigsection('Data', '#ffffff', '#55aa55', '<br>\n'.join(contents))

                            if hasattr(object, '__author__'):
                                contents = self.markup(str(object.__author__), self.preformat)
                                result = result + self.bigsection('Author', '#ffffff', '#7799ee', contents)
                            if hasattr(object, '__credits__'):
                                contents = self.markup(str(object.__credits__), self.preformat)
                                result = result + self.bigsection('Credits', '#ffffff', '#7799ee', contents)
                            return result

    def docclass--- This code section failed: ---

 L. 767         0  LOAD_DEREF               'object'
                2  LOAD_ATTR                __name__
                4  STORE_FAST               'realname'

 L. 768         6  LOAD_FAST                'name'
                8  JUMP_IF_TRUE_OR_POP    12  'to 12'
               10  LOAD_FAST                'realname'
             12_0  COME_FROM             8  '8'
               12  STORE_FAST               'name'

 L. 769        14  LOAD_DEREF               'object'
               16  LOAD_ATTR                __bases__
               18  STORE_FAST               'bases'

 L. 771        20  BUILD_LIST_0          0 
               22  STORE_FAST               'contents'

 L. 772        24  LOAD_FAST                'contents'
               26  LOAD_ATTR                append
               28  STORE_DEREF              'push'

 L. 775        30  LOAD_BUILD_CLASS 
               32  LOAD_CLOSURE             'push'
               34  BUILD_TUPLE_1         1 
               36  LOAD_CODE                <code_object HorizontalRule>
               38  LOAD_STR                 'HorizontalRule'
               40  MAKE_FUNCTION_8          'closure'
               42  LOAD_STR                 'HorizontalRule'
               44  CALL_FUNCTION_2       2  ''
               46  STORE_FAST               'HorizontalRule'

 L. 782        48  LOAD_FAST                'HorizontalRule'
               50  CALL_FUNCTION_0       0  ''
               52  STORE_DEREF              'hr'

 L. 785        54  LOAD_GLOBAL              deque
               56  LOAD_GLOBAL              inspect
               58  LOAD_METHOD              getmro
               60  LOAD_DEREF               'object'
               62  CALL_METHOD_1         1  ''
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'mro'

 L. 786        68  LOAD_GLOBAL              len
               70  LOAD_FAST                'mro'
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_CONST               2
               76  COMPARE_OP               >
               78  POP_JUMP_IF_FALSE   136  'to 136'

 L. 787        80  LOAD_DEREF               'hr'
               82  LOAD_METHOD              maybe
               84  CALL_METHOD_0         0  ''
               86  POP_TOP          

 L. 788        88  LOAD_DEREF               'push'
               90  LOAD_STR                 '<dl><dt>Method resolution order:</dt>\n'
               92  CALL_FUNCTION_1       1  ''
               94  POP_TOP          

 L. 789        96  LOAD_FAST                'mro'
               98  GET_ITER         
            100_0  COME_FROM           126  '126'
              100  FOR_ITER            128  'to 128'
              102  STORE_FAST               'base'

 L. 790       104  LOAD_DEREF               'push'
              106  LOAD_STR                 '<dd>%s</dd>\n'
              108  LOAD_DEREF               'self'
              110  LOAD_METHOD              classlink
              112  LOAD_FAST                'base'

 L. 791       114  LOAD_DEREF               'object'
              116  LOAD_ATTR                __module__

 L. 790       118  CALL_METHOD_2         2  ''
              120  BINARY_MODULO    
              122  CALL_FUNCTION_1       1  ''
              124  POP_TOP          
              126  JUMP_BACK           100  'to 100'
            128_0  COME_FROM           100  '100'

 L. 792       128  LOAD_DEREF               'push'
              130  LOAD_STR                 '</dl>\n'
              132  CALL_FUNCTION_1       1  ''
              134  POP_TOP          
            136_0  COME_FROM            78  '78'

 L. 794       136  LOAD_CLOSURE             'classes'
              138  LOAD_CLOSURE             'funcs'
              140  LOAD_CLOSURE             'hr'
              142  LOAD_CLOSURE             'mdict'
              144  LOAD_CLOSURE             'mod'
              146  LOAD_CLOSURE             'object'
              148  LOAD_CLOSURE             'push'
              150  LOAD_CLOSURE             'self'
              152  BUILD_TUPLE_8         8 
              154  LOAD_CODE                <code_object spill>
              156  LOAD_STR                 'HTMLDoc.docclass.<locals>.spill'
              158  MAKE_FUNCTION_8          'closure'
              160  STORE_FAST               'spill'

 L. 812       162  LOAD_CLOSURE             'hr'
              164  LOAD_CLOSURE             'mod'
              166  LOAD_CLOSURE             'push'
              168  LOAD_CLOSURE             'self'
              170  BUILD_TUPLE_4         4 
              172  LOAD_CODE                <code_object spilldescriptors>
              174  LOAD_STR                 'HTMLDoc.docclass.<locals>.spilldescriptors'
              176  MAKE_FUNCTION_8          'closure'
              178  STORE_FAST               'spilldescriptors'

 L. 821       180  LOAD_CLOSURE             'classes'
              182  LOAD_CLOSURE             'funcs'
              184  LOAD_CLOSURE             'hr'
              186  LOAD_CLOSURE             'mdict'
              188  LOAD_CLOSURE             'mod'
              190  LOAD_CLOSURE             'object'
              192  LOAD_CLOSURE             'push'
              194  LOAD_CLOSURE             'self'
              196  BUILD_TUPLE_8         8 
              198  LOAD_CODE                <code_object spilldata>
              200  LOAD_STR                 'HTMLDoc.docclass.<locals>.spilldata'
              202  MAKE_FUNCTION_8          'closure'
              204  STORE_FAST               'spilldata'

 L. 842       206  LOAD_CLOSURE             'object'
              208  BUILD_TUPLE_1         1 
              210  LOAD_LISTCOMP            '<code_object <listcomp>>'
              212  LOAD_STR                 'HTMLDoc.docclass.<locals>.<listcomp>'
              214  MAKE_FUNCTION_8          'closure'

 L. 843       216  LOAD_GLOBAL              classify_class_attrs
              218  LOAD_DEREF               'object'
              220  CALL_FUNCTION_1       1  ''

 L. 842       222  GET_ITER         
              224  CALL_FUNCTION_1       1  ''
              226  STORE_FAST               'attrs'

 L. 846       228  BUILD_MAP_0           0 
              230  STORE_DEREF              'mdict'

 L. 847       232  LOAD_FAST                'attrs'
              234  GET_ITER         
            236_0  COME_FROM           346  '346'
            236_1  COME_FROM           342  '342'
            236_2  COME_FROM           322  '322'
              236  FOR_ITER            348  'to 348'
              238  UNPACK_SEQUENCE_4     4 
              240  STORE_FAST               'key'
              242  STORE_FAST               'kind'
              244  STORE_FAST               'homecls'
              246  STORE_FAST               'value'

 L. 848       248  LOAD_STR                 '#'
              250  LOAD_FAST                'name'
              252  BINARY_ADD       
              254  LOAD_STR                 '-'
              256  BINARY_ADD       
              258  LOAD_FAST                'key'
              260  BINARY_ADD       
              262  DUP_TOP          
              264  LOAD_DEREF               'mdict'
              266  LOAD_FAST                'key'
              268  STORE_SUBSCR     
              270  STORE_FAST               'anchor'

 L. 849       272  SETUP_FINALLY       288  'to 288'

 L. 850       274  LOAD_GLOBAL              getattr
              276  LOAD_DEREF               'object'
              278  LOAD_FAST                'name'
              280  CALL_FUNCTION_2       2  ''
              282  STORE_FAST               'value'
              284  POP_BLOCK        
              286  JUMP_FORWARD        310  'to 310'
            288_0  COME_FROM_FINALLY   272  '272'

 L. 851       288  DUP_TOP          
              290  LOAD_GLOBAL              Exception
              292  COMPARE_OP               exception-match
          294_296  POP_JUMP_IF_FALSE   308  'to 308'
              298  POP_TOP          
              300  POP_TOP          
              302  POP_TOP          

 L. 854       304  POP_EXCEPT       
              306  BREAK_LOOP          310  'to 310'
            308_0  COME_FROM           294  '294'
              308  END_FINALLY      
            310_0  COME_FROM           306  '306'
            310_1  COME_FROM           286  '286'

 L. 855       310  SETUP_FINALLY       324  'to 324'

 L. 858       312  LOAD_FAST                'anchor'
              314  LOAD_DEREF               'mdict'
              316  LOAD_FAST                'value'
              318  STORE_SUBSCR     
              320  POP_BLOCK        
              322  JUMP_BACK           236  'to 236'
            324_0  COME_FROM_FINALLY   310  '310'

 L. 859       324  DUP_TOP          
              326  LOAD_GLOBAL              TypeError
              328  COMPARE_OP               exception-match
          330_332  POP_JUMP_IF_FALSE   344  'to 344'
              334  POP_TOP          
              336  POP_TOP          
              338  POP_TOP          

 L. 860       340  POP_EXCEPT       
              342  JUMP_BACK           236  'to 236'
            344_0  COME_FROM           330  '330'
              344  END_FINALLY      
              346  JUMP_BACK           236  'to 236'
            348_0  COME_FROM           628  '628'
            348_1  COME_FROM           432  '432'
            348_2  COME_FROM           236  '236'

 L. 862       348  LOAD_FAST                'attrs'
          350_352  POP_JUMP_IF_FALSE   632  'to 632'

 L. 863       354  LOAD_FAST                'mro'
          356_358  POP_JUMP_IF_FALSE   370  'to 370'

 L. 864       360  LOAD_FAST                'mro'
              362  LOAD_METHOD              popleft
              364  CALL_METHOD_0         0  ''
              366  STORE_DEREF              'thisclass'
              368  JUMP_FORWARD        382  'to 382'
            370_0  COME_FROM           356  '356'

 L. 866       370  LOAD_FAST                'attrs'
              372  LOAD_CONST               0
              374  BINARY_SUBSCR    
              376  LOAD_CONST               2
              378  BINARY_SUBSCR    
              380  STORE_DEREF              'thisclass'
            382_0  COME_FROM           368  '368'

 L. 867       382  LOAD_GLOBAL              _split_list
              384  LOAD_FAST                'attrs'
              386  LOAD_CLOSURE             'thisclass'
              388  BUILD_TUPLE_1         1 
              390  LOAD_LAMBDA              '<code_object <lambda>>'
              392  LOAD_STR                 'HTMLDoc.docclass.<locals>.<lambda>'
              394  MAKE_FUNCTION_8          'closure'
              396  CALL_FUNCTION_2       2  ''
              398  UNPACK_SEQUENCE_2     2 
              400  STORE_FAST               'attrs'
              402  STORE_FAST               'inherited'

 L. 869       404  LOAD_DEREF               'object'
              406  LOAD_GLOBAL              builtins
              408  LOAD_ATTR                object
              410  COMPARE_OP               is-not
          412_414  POP_JUMP_IF_FALSE   438  'to 438'
              416  LOAD_DEREF               'thisclass'
              418  LOAD_GLOBAL              builtins
              420  LOAD_ATTR                object
              422  COMPARE_OP               is
          424_426  POP_JUMP_IF_FALSE   438  'to 438'

 L. 870       428  LOAD_FAST                'inherited'
              430  STORE_FAST               'attrs'

 L. 871   432_434  JUMP_BACK           348  'to 348'
              436  BREAK_LOOP          472  'to 472'
            438_0  COME_FROM           424  '424'
            438_1  COME_FROM           412  '412'

 L. 872       438  LOAD_DEREF               'thisclass'
              440  LOAD_DEREF               'object'
              442  COMPARE_OP               is
          444_446  POP_JUMP_IF_FALSE   454  'to 454'

 L. 873       448  LOAD_STR                 'defined here'
              450  STORE_FAST               'tag'
              452  JUMP_FORWARD        472  'to 472'
            454_0  COME_FROM           444  '444'

 L. 875       454  LOAD_STR                 'inherited from %s'
              456  LOAD_DEREF               'self'
              458  LOAD_METHOD              classlink
              460  LOAD_DEREF               'thisclass'

 L. 876       462  LOAD_DEREF               'object'
              464  LOAD_ATTR                __module__

 L. 875       466  CALL_METHOD_2         2  ''
              468  BINARY_MODULO    
              470  STORE_FAST               'tag'
            472_0  COME_FROM           452  '452'
            472_1  COME_FROM           436  '436'

 L. 877       472  LOAD_FAST                'tag'
              474  LOAD_STR                 ':<br>\n'
              476  INPLACE_ADD      
              478  STORE_FAST               'tag'

 L. 879       480  LOAD_GLOBAL              sort_attributes
              482  LOAD_FAST                'attrs'
              484  LOAD_DEREF               'object'
              486  CALL_FUNCTION_2       2  ''
              488  POP_TOP          

 L. 882       490  LOAD_FAST                'spill'
              492  LOAD_STR                 'Methods %s'
              494  LOAD_FAST                'tag'
              496  BINARY_MODULO    
              498  LOAD_FAST                'attrs'

 L. 883       500  LOAD_LAMBDA              '<code_object <lambda>>'
              502  LOAD_STR                 'HTMLDoc.docclass.<locals>.<lambda>'
              504  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 882       506  CALL_FUNCTION_3       3  ''
              508  STORE_FAST               'attrs'

 L. 884       510  LOAD_FAST                'spill'
              512  LOAD_STR                 'Class methods %s'
              514  LOAD_FAST                'tag'
              516  BINARY_MODULO    
              518  LOAD_FAST                'attrs'

 L. 885       520  LOAD_LAMBDA              '<code_object <lambda>>'
              522  LOAD_STR                 'HTMLDoc.docclass.<locals>.<lambda>'
              524  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 884       526  CALL_FUNCTION_3       3  ''
              528  STORE_FAST               'attrs'

 L. 886       530  LOAD_FAST                'spill'
              532  LOAD_STR                 'Static methods %s'
              534  LOAD_FAST                'tag'
              536  BINARY_MODULO    
              538  LOAD_FAST                'attrs'

 L. 887       540  LOAD_LAMBDA              '<code_object <lambda>>'
              542  LOAD_STR                 'HTMLDoc.docclass.<locals>.<lambda>'
              544  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 886       546  CALL_FUNCTION_3       3  ''
              548  STORE_FAST               'attrs'

 L. 888       550  LOAD_FAST                'spilldescriptors'
              552  LOAD_STR                 'Readonly properties %s'
              554  LOAD_FAST                'tag'
              556  BINARY_MODULO    
              558  LOAD_FAST                'attrs'

 L. 889       560  LOAD_LAMBDA              '<code_object <lambda>>'
              562  LOAD_STR                 'HTMLDoc.docclass.<locals>.<lambda>'
              564  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 888       566  CALL_FUNCTION_3       3  ''
              568  STORE_FAST               'attrs'

 L. 890       570  LOAD_FAST                'spilldescriptors'
              572  LOAD_STR                 'Data descriptors %s'
              574  LOAD_FAST                'tag'
              576  BINARY_MODULO    
              578  LOAD_FAST                'attrs'

 L. 891       580  LOAD_LAMBDA              '<code_object <lambda>>'
              582  LOAD_STR                 'HTMLDoc.docclass.<locals>.<lambda>'
              584  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 890       586  CALL_FUNCTION_3       3  ''
              588  STORE_FAST               'attrs'

 L. 892       590  LOAD_FAST                'spilldata'
              592  LOAD_STR                 'Data and other attributes %s'
              594  LOAD_FAST                'tag'
              596  BINARY_MODULO    
              598  LOAD_FAST                'attrs'

 L. 893       600  LOAD_LAMBDA              '<code_object <lambda>>'
              602  LOAD_STR                 'HTMLDoc.docclass.<locals>.<lambda>'
              604  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 892       606  CALL_FUNCTION_3       3  ''
              608  STORE_FAST               'attrs'

 L. 894       610  LOAD_FAST                'attrs'
              612  BUILD_LIST_0          0 
              614  COMPARE_OP               ==
          616_618  POP_JUMP_IF_TRUE    624  'to 624'
              620  LOAD_ASSERT              AssertionError
              622  RAISE_VARARGS_1       1  'exception instance'
            624_0  COME_FROM           616  '616'

 L. 895       624  LOAD_FAST                'inherited'
              626  STORE_FAST               'attrs'
          628_630  JUMP_BACK           348  'to 348'
            632_0  COME_FROM           350  '350'

 L. 897       632  LOAD_STR                 ''
              634  LOAD_METHOD              join
              636  LOAD_FAST                'contents'
              638  CALL_METHOD_1         1  ''
              640  STORE_FAST               'contents'

 L. 899       642  LOAD_FAST                'name'
              644  LOAD_FAST                'realname'
              646  COMPARE_OP               ==
          648_650  POP_JUMP_IF_FALSE   666  'to 666'

 L. 900       652  LOAD_STR                 '<a name="%s">class <strong>%s</strong></a>'

 L. 901       654  LOAD_FAST                'name'

 L. 901       656  LOAD_FAST                'realname'

 L. 900       658  BUILD_TUPLE_2         2 
              660  BINARY_MODULO    
              662  STORE_FAST               'title'
              664  JUMP_FORWARD        680  'to 680'
            666_0  COME_FROM           648  '648'

 L. 903       666  LOAD_STR                 '<strong>%s</strong> = <a name="%s">class %s</a>'

 L. 904       668  LOAD_FAST                'name'

 L. 904       670  LOAD_FAST                'name'

 L. 904       672  LOAD_FAST                'realname'

 L. 903       674  BUILD_TUPLE_3         3 
              676  BINARY_MODULO    
              678  STORE_FAST               'title'
            680_0  COME_FROM           664  '664'

 L. 905       680  LOAD_FAST                'bases'
          682_684  POP_JUMP_IF_FALSE   740  'to 740'

 L. 906       686  BUILD_LIST_0          0 
              688  STORE_FAST               'parents'

 L. 907       690  LOAD_FAST                'bases'
              692  GET_ITER         
            694_0  COME_FROM           718  '718'
              694  FOR_ITER            722  'to 722'
              696  STORE_FAST               'base'

 L. 908       698  LOAD_FAST                'parents'
              700  LOAD_METHOD              append
              702  LOAD_DEREF               'self'
              704  LOAD_METHOD              classlink
              706  LOAD_FAST                'base'
              708  LOAD_DEREF               'object'
              710  LOAD_ATTR                __module__
              712  CALL_METHOD_2         2  ''
              714  CALL_METHOD_1         1  ''
              716  POP_TOP          
          718_720  JUMP_BACK           694  'to 694'
            722_0  COME_FROM           694  '694'

 L. 909       722  LOAD_FAST                'title'
              724  LOAD_STR                 '(%s)'
              726  LOAD_STR                 ', '
              728  LOAD_METHOD              join
              730  LOAD_FAST                'parents'
              732  CALL_METHOD_1         1  ''
              734  BINARY_MODULO    
              736  BINARY_ADD       
              738  STORE_FAST               'title'
            740_0  COME_FROM           682  '682'

 L. 911       740  LOAD_STR                 ''
              742  STORE_FAST               'decl'

 L. 912       744  SETUP_FINALLY       760  'to 760'

 L. 913       746  LOAD_GLOBAL              inspect
              748  LOAD_METHOD              signature
              750  LOAD_DEREF               'object'
              752  CALL_METHOD_1         1  ''
              754  STORE_FAST               'signature'
              756  POP_BLOCK        
              758  JUMP_FORWARD        790  'to 790'
            760_0  COME_FROM_FINALLY   744  '744'

 L. 914       760  DUP_TOP          
              762  LOAD_GLOBAL              ValueError
              764  LOAD_GLOBAL              TypeError
              766  BUILD_TUPLE_2         2 
              768  COMPARE_OP               exception-match
          770_772  POP_JUMP_IF_FALSE   788  'to 788'
              774  POP_TOP          
              776  POP_TOP          
              778  POP_TOP          

 L. 915       780  LOAD_CONST               None
              782  STORE_FAST               'signature'
              784  POP_EXCEPT       
              786  JUMP_FORWARD        790  'to 790'
            788_0  COME_FROM           770  '770'
              788  END_FINALLY      
            790_0  COME_FROM           786  '786'
            790_1  COME_FROM           758  '758'

 L. 916       790  LOAD_FAST                'signature'
          792_794  POP_JUMP_IF_FALSE   838  'to 838'

 L. 917       796  LOAD_GLOBAL              str
              798  LOAD_FAST                'signature'
              800  CALL_FUNCTION_1       1  ''
              802  STORE_FAST               'argspec'

 L. 918       804  LOAD_FAST                'argspec'
          806_808  POP_JUMP_IF_FALSE   838  'to 838'
              810  LOAD_FAST                'argspec'
              812  LOAD_STR                 '()'
              814  COMPARE_OP               !=
          816_818  POP_JUMP_IF_FALSE   838  'to 838'

 L. 919       820  LOAD_FAST                'name'
              822  LOAD_DEREF               'self'
              824  LOAD_METHOD              escape
              826  LOAD_FAST                'argspec'
              828  CALL_METHOD_1         1  ''
              830  BINARY_ADD       
              832  LOAD_STR                 '\n\n'
              834  BINARY_ADD       
              836  STORE_FAST               'decl'
            838_0  COME_FROM           816  '816'
            838_1  COME_FROM           806  '806'
            838_2  COME_FROM           792  '792'

 L. 921       838  LOAD_GLOBAL              getdoc
              840  LOAD_DEREF               'object'
              842  CALL_FUNCTION_1       1  ''
              844  STORE_FAST               'doc'

 L. 922       846  LOAD_FAST                'decl'
          848_850  POP_JUMP_IF_FALSE   866  'to 866'

 L. 923       852  LOAD_FAST                'decl'
              854  LOAD_FAST                'doc'
          856_858  JUMP_IF_TRUE_OR_POP   862  'to 862'
              860  LOAD_STR                 ''
            862_0  COME_FROM           856  '856'
              862  BINARY_ADD       
              864  STORE_FAST               'doc'
            866_0  COME_FROM           848  '848'

 L. 924       866  LOAD_DEREF               'self'
              868  LOAD_METHOD              markup
              870  LOAD_FAST                'doc'
              872  LOAD_DEREF               'self'
              874  LOAD_ATTR                preformat
              876  LOAD_DEREF               'funcs'
              878  LOAD_DEREF               'classes'
              880  LOAD_DEREF               'mdict'
              882  CALL_METHOD_5         5  ''
              884  STORE_FAST               'doc'

 L. 925       886  LOAD_FAST                'doc'
          888_890  JUMP_IF_FALSE_OR_POP   898  'to 898'
              892  LOAD_STR                 '<tt>%s<br>&nbsp;</tt>'
              894  LOAD_FAST                'doc'
              896  BINARY_MODULO    
            898_0  COME_FROM           888  '888'
              898  STORE_FAST               'doc'

 L. 927       900  LOAD_DEREF               'self'
              902  LOAD_METHOD              section
              904  LOAD_FAST                'title'
              906  LOAD_STR                 '#000000'
              908  LOAD_STR                 '#ffc8d8'
              910  LOAD_FAST                'contents'
              912  LOAD_CONST               3
              914  LOAD_FAST                'doc'
              916  CALL_METHOD_6         6  ''
              918  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 308

    def formatvalue(self, object):
        """Format an argument default value as text."""
        return self.grey('=' + self.repr(object))

    def docroutine(self, object, name=None, mod=None, funcs={}, classes={}, methods={}, cl=None):
        """Produce HTML documentation for a function or method object."""
        realname = object.__name__
        name = name or realname
        anchor = cl and (cl.__name__) or '' + '-' + name
        note = ''
        skipdocs = 0
        if _is_bound_method(object):
            imclass = object.__self__.__class__
            if cl:
                if imclass is not cl:
                    note = ' from ' + self.classlink(imclass, mod)
            elif object.__self__ is not None:
                note = ' method of %s instance' % self.classlink(object.__self__.__class__, mod)
            else:
                note = ' unbound %s method' % self.classlink(imclass, mod)
        if inspect.iscoroutinefunction(object) or inspect.isasyncgenfunction(object):
            asyncqualifier = 'async '
        else:
            asyncqualifier = ''
        if name == realname:
            title = '<a name="%s"><strong>%s</strong></a>' % (anchor, realname)
        else:
            if cl and inspect.getattr_static(cl, realname, []) is object:
                reallink = '<a href="#%s">%s</a>' % (
                 cl.__name__ + '-' + realname, realname)
                skipdocs = 1
            else:
                reallink = realname
            title = '<a name="%s"><strong>%s</strong></a> = %s' % (
             anchor, name, reallink)
        argspec = None
        if inspect.isroutine(object):
            try:
                signature = inspect.signature(object)
            except (ValueError, TypeError):
                signature = None
            else:
                if signature:
                    argspec = str(signature)
                    if realname == '<lambda>':
                        title = '<strong>%s</strong> <em>lambda</em> ' % name
                        argspec = argspec[1:-1]
            if not argspec:
                argspec = '(...)'
            decl = asyncqualifier + title + self.escape(argspec) + (note and self.grey('<font face="helvetica, arial">%s</font>' % note))
            if skipdocs:
                return '<dl><dt>%s</dt></dl>\n' % decl
            doc = self.markup(getdoc(object), self.preformat, funcs, classes, methods)
            doc = doc and '<dd><tt>%s</tt></dd>' % doc
            return '<dl><dt>%s</dt>%s</dl>\n' % (decl, doc)

    def docdata(self, object, name=None, mod=None, cl=None):
        """Produce html documentation for a data descriptor."""
        results = []
        push = results.append
        if name:
            push('<dl><dt><strong>%s</strong></dt>\n' % name)
        doc = self.markup(getdoc(object), self.preformat)
        if doc:
            push('<dd><tt>%s</tt></dd>\n' % doc)
        push('</dl>\n')
        return ''.join(results)

    docproperty = docdata

    def docother(self, object, name=None, mod=None, *ignored):
        """Produce HTML documentation for a data object."""
        lhs = name and ('<strong>%s</strong> = ' % name) or ''
        return lhs + self.repr(object)

    def index(self, dir, shadowed=None):
        """Generate an HTML index for a directory of modules."""
        modpkgs = []
        if shadowed is None:
            shadowed = {}
        for importer, name, ispkg in pkgutil.iter_modules([dir]):
            if any((55296 <= ord(ch) <= 57343 for ch in name)):
                pass
            else:
                modpkgs.append((name, '', ispkg, name in shadowed))
                shadowed[name] = 1
        else:
            modpkgs.sort()
            contents = self.multicolumn(modpkgs, self.modpkglink)
            return self.bigsection(dir, '#ffffff', '#ee77aa', contents)


class TextRepr(Repr):
    __doc__ = 'Class for safely making a text representation of a Python object.'

    def __init__(self):
        Repr.__init__(self)
        self.maxlist = self.maxtuple = 20
        self.maxdict = 10
        self.maxstring = self.maxother = 100

    def repr1(self, x, level):
        if hasattr(type(x), '__name__'):
            methodname = 'repr_' + '_'.join(type(x).__name__.split())
            if hasattr(self, methodname):
                return getattr(self, methodname)(x, level)
        return cram(stripid(repr(x)), self.maxother)

    def repr_string(self, x, level):
        test = cram(x, self.maxstring)
        testrepr = repr(test)
        if '\\' in test:
            if '\\' not in replace(testrepr, '\\\\', ''):
                return 'r' + testrepr[0] + test + testrepr[0]
        return testrepr

    repr_str = repr_string

    def repr_instance(self, x, level):
        try:
            return cram(stripid(repr(x)), self.maxstring)
        except:
            return '<%s instance>' % x.__class__.__name__


class TextDoc(Doc):
    __doc__ = 'Formatter class for text documentation.'
    _repr_instance = TextRepr()
    repr = _repr_instance.repr

    def bold(self, text):
        """Format a string in bold by overstriking."""
        return ''.join((ch + '\x08' + ch for ch in text))

    def indent(self, text, prefix='    '):
        """Indent text by prepending a given prefix to each line."""
        if not text:
            return ''
        lines = [prefix + line for line in text.split('\n')]
        if lines:
            lines[-1] = lines[(-1)].rstrip()
        return '\n'.join(lines)

    def section(self, title, contents):
        """Format a section with a given heading."""
        clean_contents = self.indent(contents).rstrip()
        return self.bold(title) + '\n' + clean_contents + '\n\n'

    def formattree(self, tree, modname, parent=None, prefix=''):
        """Render in text a class tree as returned by inspect.getclasstree()."""
        result = ''
        for entry in tree:
            if type(entry) is type(()):
                c, bases = entry
                result = result + prefix + classname(c, modname)
                if bases:
                    if bases != (parent,):
                        parents = (classname(c, modname) for c in bases)
                        result = result + '(%s)' % ', '.join(parents)
                result = result + '\n'
            else:
                if type(entry) is type([]):
                    result = result + self.formattree(entry, modname, c, prefix + '    ')
        else:
            return result

    def docmodule(self, object, name=None, mod=None):
        """Produce text documentation for a given module object."""
        name = object.__name__
        synop, desc = splitdoc(getdoc(object))
        result = self.section('NAME', name + (synop and ' - ' + synop))
        all = getattr(object, '__all__', None)
        docloc = self.getdocloc(object)
        if docloc is not None:
            result = result + self.section('MODULE REFERENCE', docloc + '\n\nThe following documentation is automatically generated from the Python\nsource files.  It may be incomplete, incorrect or include features that\nare considered implementation detail and may vary between Python\nimplementations.  When in doubt, consult the module reference at the\nlocation listed above.\n')
        if desc:
            result = result + self.section('DESCRIPTION', desc)
        classes = []
        for key, value in inspect.getmembers(object, inspect.isclass):
            if not all is not None:
                if (inspect.getmodule(value) or object) is object:
                    pass
            if visiblename(key, all, object):
                classes.append((key, value))
        else:
            funcs = []
            for key, value in inspect.getmembers(object, inspect.isroutine):
                if not all is not None:
                    if not inspect.isbuiltin(value):
                        if inspect.getmodule(value) is object:
                            pass
                if visiblename(key, all, object):
                    funcs.append((key, value))
            else:
                data = []
                for key, value in inspect.getmembers(object, isdata):
                    if visiblename(key, all, object):
                        data.append((key, value))
                else:
                    modpkgs = []
                    modpkgs_names = set()
                    if hasattr(object, '__path__'):
                        for importer, modname, ispkg in pkgutil.iter_modules(object.__path__):
                            modpkgs_names.add(modname)
                            if ispkg:
                                modpkgs.append(modname + ' (package)')
                            else:
                                modpkgs.append(modname)
                            modpkgs.sort()
                            result = result + self.section('PACKAGE CONTENTS', '\n'.join(modpkgs))

                    submodules = []

        for key, value in inspect.getmembers(object, inspect.ismodule):
            if value.__name__.startswith(name + '.'):
                if key not in modpkgs_names:
                    submodules.append(key)
        else:
            if submodules:
                submodules.sort()
                result = result + self.section('SUBMODULES', '\n'.join(submodules))
            if classes:
                classlist = [value for key, value in classes]
                contents = [
                 self.formattree(inspect.getclasstree(classlist, 1), name)]
                for key, value in classes:
                    contents.append(self.document(value, key, name))
                else:
                    result = result + self.section('CLASSES', '\n'.join(contents))

            if funcs:
                contents = []
                for key, value in funcs:
                    contents.append(self.document(value, key, name))
                else:
                    result = result + self.section('FUNCTIONS', '\n'.join(contents))

            if data:
                contents = []
                for key, value in data:
                    contents.append(self.docother(value, key, name, maxlen=70))
                else:
                    result = result + self.section('DATA', '\n'.join(contents))

            if hasattr(object, '__version__'):
                version = str(object.__version__)
                if version[:11] == '$Revision: ':
                    if version[-1:] == '$':
                        version = version[11:-1].strip()
                result = result + self.section('VERSION', version)
            if hasattr(object, '__date__'):
                result = result + self.section('DATE', str(object.__date__))
            if hasattr(object, '__author__'):
                result = result + self.section('AUTHOR', str(object.__author__))
            if hasattr(object, '__credits__'):
                result = result + self.section('CREDITS', str(object.__credits__))
            try:
                file = inspect.getabsfile(object)
            except TypeError:
                file = '(built-in)'
            else:
                result = result + self.section('FILE', file)
                return result

    def docclass--- This code section failed: ---

 L.1213         0  LOAD_DEREF               'object'
                2  LOAD_ATTR                __name__
                4  STORE_FAST               'realname'

 L.1214         6  LOAD_FAST                'name'
                8  JUMP_IF_TRUE_OR_POP    12  'to 12'
               10  LOAD_FAST                'realname'
             12_0  COME_FROM             8  '8'
               12  STORE_FAST               'name'

 L.1215        14  LOAD_DEREF               'object'
               16  LOAD_ATTR                __bases__
               18  STORE_FAST               'bases'

 L.1217        20  LOAD_DEREF               'object'
               22  LOAD_ATTR                __module__
               24  BUILD_TUPLE_1         1 
               26  LOAD_CODE                <code_object makename>
               28  LOAD_STR                 'TextDoc.docclass.<locals>.makename'
               30  MAKE_FUNCTION_1          'default'
               32  STORE_FAST               'makename'

 L.1220        34  LOAD_FAST                'name'
               36  LOAD_FAST                'realname'
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    58  'to 58'

 L.1221        42  LOAD_STR                 'class '
               44  LOAD_DEREF               'self'
               46  LOAD_METHOD              bold
               48  LOAD_FAST                'realname'
               50  CALL_METHOD_1         1  ''
               52  BINARY_ADD       
               54  STORE_FAST               'title'
               56  JUMP_FORWARD         76  'to 76'
             58_0  COME_FROM            40  '40'

 L.1223        58  LOAD_DEREF               'self'
               60  LOAD_METHOD              bold
               62  LOAD_FAST                'name'
               64  CALL_METHOD_1         1  ''
               66  LOAD_STR                 ' = class '
               68  BINARY_ADD       
               70  LOAD_FAST                'realname'
               72  BINARY_ADD       
               74  STORE_FAST               'title'
             76_0  COME_FROM            56  '56'

 L.1224        76  LOAD_FAST                'bases'
               78  POP_JUMP_IF_FALSE   108  'to 108'

 L.1225        80  LOAD_GLOBAL              map
               82  LOAD_FAST                'makename'
               84  LOAD_FAST                'bases'
               86  CALL_FUNCTION_2       2  ''
               88  STORE_FAST               'parents'

 L.1226        90  LOAD_FAST                'title'
               92  LOAD_STR                 '(%s)'
               94  LOAD_STR                 ', '
               96  LOAD_METHOD              join
               98  LOAD_FAST                'parents'
              100  CALL_METHOD_1         1  ''
              102  BINARY_MODULO    
              104  BINARY_ADD       
              106  STORE_FAST               'title'
            108_0  COME_FROM            78  '78'

 L.1228       108  BUILD_LIST_0          0 
              110  STORE_FAST               'contents'

 L.1229       112  LOAD_FAST                'contents'
              114  LOAD_ATTR                append
              116  STORE_DEREF              'push'

 L.1231       118  SETUP_FINALLY       134  'to 134'

 L.1232       120  LOAD_GLOBAL              inspect
              122  LOAD_METHOD              signature
              124  LOAD_DEREF               'object'
              126  CALL_METHOD_1         1  ''
              128  STORE_FAST               'signature'
              130  POP_BLOCK        
              132  JUMP_FORWARD        162  'to 162'
            134_0  COME_FROM_FINALLY   118  '118'

 L.1233       134  DUP_TOP          
              136  LOAD_GLOBAL              ValueError
              138  LOAD_GLOBAL              TypeError
              140  BUILD_TUPLE_2         2 
              142  COMPARE_OP               exception-match
              144  POP_JUMP_IF_FALSE   160  'to 160'
              146  POP_TOP          
              148  POP_TOP          
              150  POP_TOP          

 L.1234       152  LOAD_CONST               None
              154  STORE_FAST               'signature'
              156  POP_EXCEPT       
              158  JUMP_FORWARD        162  'to 162'
            160_0  COME_FROM           144  '144'
              160  END_FINALLY      
            162_0  COME_FROM           158  '158'
            162_1  COME_FROM           132  '132'

 L.1235       162  LOAD_FAST                'signature'
              164  POP_JUMP_IF_FALSE   202  'to 202'

 L.1236       166  LOAD_GLOBAL              str
              168  LOAD_FAST                'signature'
              170  CALL_FUNCTION_1       1  ''
              172  STORE_FAST               'argspec'

 L.1237       174  LOAD_FAST                'argspec'
              176  POP_JUMP_IF_FALSE   202  'to 202'
              178  LOAD_FAST                'argspec'
              180  LOAD_STR                 '()'
              182  COMPARE_OP               !=
              184  POP_JUMP_IF_FALSE   202  'to 202'

 L.1238       186  LOAD_DEREF               'push'
              188  LOAD_FAST                'name'
              190  LOAD_FAST                'argspec'
              192  BINARY_ADD       
              194  LOAD_STR                 '\n'
              196  BINARY_ADD       
              198  CALL_FUNCTION_1       1  ''
              200  POP_TOP          
            202_0  COME_FROM           184  '184'
            202_1  COME_FROM           176  '176'
            202_2  COME_FROM           164  '164'

 L.1240       202  LOAD_GLOBAL              getdoc
              204  LOAD_DEREF               'object'
              206  CALL_FUNCTION_1       1  ''
              208  STORE_FAST               'doc'

 L.1241       210  LOAD_FAST                'doc'
              212  POP_JUMP_IF_FALSE   226  'to 226'

 L.1242       214  LOAD_DEREF               'push'
              216  LOAD_FAST                'doc'
              218  LOAD_STR                 '\n'
              220  BINARY_ADD       
              222  CALL_FUNCTION_1       1  ''
              224  POP_TOP          
            226_0  COME_FROM           212  '212'

 L.1245       226  LOAD_GLOBAL              deque
              228  LOAD_GLOBAL              inspect
              230  LOAD_METHOD              getmro
              232  LOAD_DEREF               'object'
              234  CALL_METHOD_1         1  ''
              236  CALL_FUNCTION_1       1  ''
              238  STORE_FAST               'mro'

 L.1246       240  LOAD_GLOBAL              len
              242  LOAD_FAST                'mro'
              244  CALL_FUNCTION_1       1  ''
              246  LOAD_CONST               2
              248  COMPARE_OP               >
          250_252  POP_JUMP_IF_FALSE   298  'to 298'

 L.1247       254  LOAD_DEREF               'push'
              256  LOAD_STR                 'Method resolution order:'
              258  CALL_FUNCTION_1       1  ''
              260  POP_TOP          

 L.1248       262  LOAD_FAST                'mro'
              264  GET_ITER         
            266_0  COME_FROM           286  '286'
              266  FOR_ITER            290  'to 290'
              268  STORE_FAST               'base'

 L.1249       270  LOAD_DEREF               'push'
              272  LOAD_STR                 '    '
              274  LOAD_FAST                'makename'
              276  LOAD_FAST                'base'
              278  CALL_FUNCTION_1       1  ''
              280  BINARY_ADD       
              282  CALL_FUNCTION_1       1  ''
              284  POP_TOP          
          286_288  JUMP_BACK           266  'to 266'
            290_0  COME_FROM           266  '266'

 L.1250       290  LOAD_DEREF               'push'
              292  LOAD_STR                 ''
              294  CALL_FUNCTION_1       1  ''
              296  POP_TOP          
            298_0  COME_FROM           250  '250'

 L.1253       298  LOAD_GLOBAL              sorted

 L.1254       300  LOAD_GENEXPR             '<code_object <genexpr>>'
              302  LOAD_STR                 'TextDoc.docclass.<locals>.<genexpr>'
              304  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              306  LOAD_GLOBAL              type
              308  LOAD_METHOD              __subclasses__
              310  LOAD_DEREF               'object'
              312  CALL_METHOD_1         1  ''
              314  GET_ITER         
              316  CALL_FUNCTION_1       1  ''

 L.1256       318  LOAD_GLOBAL              str
              320  LOAD_ATTR                lower

 L.1253       322  LOAD_CONST               ('key',)
              324  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              326  STORE_FAST               'subclasses'

 L.1258       328  LOAD_GLOBAL              len
              330  LOAD_FAST                'subclasses'
              332  CALL_FUNCTION_1       1  ''
              334  STORE_FAST               'no_of_subclasses'

 L.1259       336  LOAD_CONST               4
              338  STORE_FAST               'MAX_SUBCLASSES_TO_DISPLAY'

 L.1260       340  LOAD_FAST                'subclasses'
          342_344  POP_JUMP_IF_FALSE   428  'to 428'

 L.1261       346  LOAD_DEREF               'push'
              348  LOAD_STR                 'Built-in subclasses:'
              350  CALL_FUNCTION_1       1  ''
              352  POP_TOP          

 L.1262       354  LOAD_FAST                'subclasses'
              356  LOAD_CONST               None
              358  LOAD_FAST                'MAX_SUBCLASSES_TO_DISPLAY'
              360  BUILD_SLICE_2         2 
              362  BINARY_SUBSCR    
              364  GET_ITER         
            366_0  COME_FROM           382  '382'
              366  FOR_ITER            386  'to 386'
              368  STORE_FAST               'subclassname'

 L.1263       370  LOAD_DEREF               'push'
              372  LOAD_STR                 '    '
              374  LOAD_FAST                'subclassname'
              376  BINARY_ADD       
              378  CALL_FUNCTION_1       1  ''
              380  POP_TOP          
          382_384  JUMP_BACK           366  'to 366'
            386_0  COME_FROM           366  '366'

 L.1264       386  LOAD_FAST                'no_of_subclasses'
              388  LOAD_FAST                'MAX_SUBCLASSES_TO_DISPLAY'
              390  COMPARE_OP               >
          392_394  POP_JUMP_IF_FALSE   420  'to 420'

 L.1265       396  LOAD_DEREF               'push'
              398  LOAD_STR                 '    ... and '

 L.1266       400  LOAD_GLOBAL              str
              402  LOAD_FAST                'no_of_subclasses'
              404  LOAD_FAST                'MAX_SUBCLASSES_TO_DISPLAY'
              406  BINARY_SUBTRACT  
              408  CALL_FUNCTION_1       1  ''

 L.1265       410  BINARY_ADD       

 L.1267       412  LOAD_STR                 ' other subclasses'

 L.1265       414  BINARY_ADD       
              416  CALL_FUNCTION_1       1  ''
              418  POP_TOP          
            420_0  COME_FROM           392  '392'

 L.1268       420  LOAD_DEREF               'push'
              422  LOAD_STR                 ''
              424  CALL_FUNCTION_1       1  ''
              426  POP_TOP          
            428_0  COME_FROM           342  '342'

 L.1271       428  LOAD_BUILD_CLASS 
              430  LOAD_CLOSURE             'push'
              432  BUILD_TUPLE_1         1 
              434  LOAD_CODE                <code_object HorizontalRule>
              436  LOAD_STR                 'HorizontalRule'
              438  MAKE_FUNCTION_8          'closure'
              440  LOAD_STR                 'HorizontalRule'
              442  CALL_FUNCTION_2       2  ''
              444  STORE_FAST               'HorizontalRule'

 L.1278       446  LOAD_FAST                'HorizontalRule'
              448  CALL_FUNCTION_0       0  ''
              450  STORE_DEREF              'hr'

 L.1280       452  LOAD_CLOSURE             'hr'
              454  LOAD_CLOSURE             'mod'
              456  LOAD_CLOSURE             'object'
              458  LOAD_CLOSURE             'push'
              460  LOAD_CLOSURE             'self'
              462  BUILD_TUPLE_5         5 
              464  LOAD_CODE                <code_object spill>
              466  LOAD_STR                 'TextDoc.docclass.<locals>.spill'
              468  MAKE_FUNCTION_8          'closure'
              470  STORE_FAST               'spill'

 L.1297       472  LOAD_CLOSURE             'hr'
              474  LOAD_CLOSURE             'mod'
              476  LOAD_CLOSURE             'push'
              478  LOAD_CLOSURE             'self'
              480  BUILD_TUPLE_4         4 
              482  LOAD_CODE                <code_object spilldescriptors>
              484  LOAD_STR                 'TextDoc.docclass.<locals>.spilldescriptors'
              486  MAKE_FUNCTION_8          'closure'
              488  STORE_FAST               'spilldescriptors'

 L.1306       490  LOAD_CLOSURE             'hr'
              492  LOAD_CLOSURE             'mod'
              494  LOAD_CLOSURE             'object'
              496  LOAD_CLOSURE             'push'
              498  LOAD_CLOSURE             'self'
              500  BUILD_TUPLE_5         5 
              502  LOAD_CODE                <code_object spilldata>
              504  LOAD_STR                 'TextDoc.docclass.<locals>.spilldata'
              506  MAKE_FUNCTION_8          'closure'
              508  STORE_FAST               'spilldata'

 L.1324       510  LOAD_CLOSURE             'object'
              512  BUILD_TUPLE_1         1 
              514  LOAD_LISTCOMP            '<code_object <listcomp>>'
              516  LOAD_STR                 'TextDoc.docclass.<locals>.<listcomp>'
              518  MAKE_FUNCTION_8          'closure'

 L.1325       520  LOAD_GLOBAL              classify_class_attrs
              522  LOAD_DEREF               'object'
              524  CALL_FUNCTION_1       1  ''

 L.1324       526  GET_ITER         
              528  CALL_FUNCTION_1       1  ''
              530  STORE_FAST               'attrs'
            532_0  COME_FROM           802  '802'
            532_1  COME_FROM           616  '616'

 L.1328       532  LOAD_FAST                'attrs'
          534_536  POP_JUMP_IF_FALSE   806  'to 806'

 L.1329       538  LOAD_FAST                'mro'
          540_542  POP_JUMP_IF_FALSE   554  'to 554'

 L.1330       544  LOAD_FAST                'mro'
              546  LOAD_METHOD              popleft
              548  CALL_METHOD_0         0  ''
              550  STORE_DEREF              'thisclass'
              552  JUMP_FORWARD        566  'to 566'
            554_0  COME_FROM           540  '540'

 L.1332       554  LOAD_FAST                'attrs'
              556  LOAD_CONST               0
              558  BINARY_SUBSCR    
              560  LOAD_CONST               2
              562  BINARY_SUBSCR    
              564  STORE_DEREF              'thisclass'
            566_0  COME_FROM           552  '552'

 L.1333       566  LOAD_GLOBAL              _split_list
              568  LOAD_FAST                'attrs'
              570  LOAD_CLOSURE             'thisclass'
              572  BUILD_TUPLE_1         1 
              574  LOAD_LAMBDA              '<code_object <lambda>>'
              576  LOAD_STR                 'TextDoc.docclass.<locals>.<lambda>'
              578  MAKE_FUNCTION_8          'closure'
              580  CALL_FUNCTION_2       2  ''
              582  UNPACK_SEQUENCE_2     2 
              584  STORE_FAST               'attrs'
              586  STORE_FAST               'inherited'

 L.1335       588  LOAD_DEREF               'object'
              590  LOAD_GLOBAL              builtins
              592  LOAD_ATTR                object
              594  COMPARE_OP               is-not
          596_598  POP_JUMP_IF_FALSE   622  'to 622'
              600  LOAD_DEREF               'thisclass'
              602  LOAD_GLOBAL              builtins
              604  LOAD_ATTR                object
              606  COMPARE_OP               is
          608_610  POP_JUMP_IF_FALSE   622  'to 622'

 L.1336       612  LOAD_FAST                'inherited'
              614  STORE_FAST               'attrs'

 L.1337   616_618  JUMP_BACK           532  'to 532'
              620  BREAK_LOOP          654  'to 654'
            622_0  COME_FROM           608  '608'
            622_1  COME_FROM           596  '596'

 L.1338       622  LOAD_DEREF               'thisclass'
              624  LOAD_DEREF               'object'
              626  COMPARE_OP               is
          628_630  POP_JUMP_IF_FALSE   638  'to 638'

 L.1339       632  LOAD_STR                 'defined here'
              634  STORE_FAST               'tag'
              636  JUMP_FORWARD        654  'to 654'
            638_0  COME_FROM           628  '628'

 L.1341       638  LOAD_STR                 'inherited from %s'
              640  LOAD_GLOBAL              classname
              642  LOAD_DEREF               'thisclass'

 L.1342       644  LOAD_DEREF               'object'
              646  LOAD_ATTR                __module__

 L.1341       648  CALL_FUNCTION_2       2  ''
              650  BINARY_MODULO    
              652  STORE_FAST               'tag'
            654_0  COME_FROM           636  '636'
            654_1  COME_FROM           620  '620'

 L.1344       654  LOAD_GLOBAL              sort_attributes
              656  LOAD_FAST                'attrs'
              658  LOAD_DEREF               'object'
              660  CALL_FUNCTION_2       2  ''
              662  POP_TOP          

 L.1347       664  LOAD_FAST                'spill'
              666  LOAD_STR                 'Methods %s:\n'
              668  LOAD_FAST                'tag'
              670  BINARY_MODULO    
              672  LOAD_FAST                'attrs'

 L.1348       674  LOAD_LAMBDA              '<code_object <lambda>>'
              676  LOAD_STR                 'TextDoc.docclass.<locals>.<lambda>'
              678  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1347       680  CALL_FUNCTION_3       3  ''
              682  STORE_FAST               'attrs'

 L.1349       684  LOAD_FAST                'spill'
              686  LOAD_STR                 'Class methods %s:\n'
              688  LOAD_FAST                'tag'
              690  BINARY_MODULO    
              692  LOAD_FAST                'attrs'

 L.1350       694  LOAD_LAMBDA              '<code_object <lambda>>'
              696  LOAD_STR                 'TextDoc.docclass.<locals>.<lambda>'
              698  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1349       700  CALL_FUNCTION_3       3  ''
              702  STORE_FAST               'attrs'

 L.1351       704  LOAD_FAST                'spill'
              706  LOAD_STR                 'Static methods %s:\n'
              708  LOAD_FAST                'tag'
              710  BINARY_MODULO    
              712  LOAD_FAST                'attrs'

 L.1352       714  LOAD_LAMBDA              '<code_object <lambda>>'
              716  LOAD_STR                 'TextDoc.docclass.<locals>.<lambda>'
              718  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1351       720  CALL_FUNCTION_3       3  ''
              722  STORE_FAST               'attrs'

 L.1353       724  LOAD_FAST                'spilldescriptors'
              726  LOAD_STR                 'Readonly properties %s:\n'
              728  LOAD_FAST                'tag'
              730  BINARY_MODULO    
              732  LOAD_FAST                'attrs'

 L.1354       734  LOAD_LAMBDA              '<code_object <lambda>>'
              736  LOAD_STR                 'TextDoc.docclass.<locals>.<lambda>'
              738  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1353       740  CALL_FUNCTION_3       3  ''
              742  STORE_FAST               'attrs'

 L.1355       744  LOAD_FAST                'spilldescriptors'
              746  LOAD_STR                 'Data descriptors %s:\n'
              748  LOAD_FAST                'tag'
              750  BINARY_MODULO    
              752  LOAD_FAST                'attrs'

 L.1356       754  LOAD_LAMBDA              '<code_object <lambda>>'
              756  LOAD_STR                 'TextDoc.docclass.<locals>.<lambda>'
              758  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1355       760  CALL_FUNCTION_3       3  ''
              762  STORE_FAST               'attrs'

 L.1357       764  LOAD_FAST                'spilldata'
              766  LOAD_STR                 'Data and other attributes %s:\n'
              768  LOAD_FAST                'tag'
              770  BINARY_MODULO    
              772  LOAD_FAST                'attrs'

 L.1358       774  LOAD_LAMBDA              '<code_object <lambda>>'
              776  LOAD_STR                 'TextDoc.docclass.<locals>.<lambda>'
              778  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1357       780  CALL_FUNCTION_3       3  ''
              782  STORE_FAST               'attrs'

 L.1360       784  LOAD_FAST                'attrs'
              786  BUILD_LIST_0          0 
              788  COMPARE_OP               ==
          790_792  POP_JUMP_IF_TRUE    798  'to 798'
              794  LOAD_ASSERT              AssertionError
              796  RAISE_VARARGS_1       1  'exception instance'
            798_0  COME_FROM           790  '790'

 L.1361       798  LOAD_FAST                'inherited'
              800  STORE_FAST               'attrs'
          802_804  JUMP_BACK           532  'to 532'
            806_0  COME_FROM           534  '534'

 L.1363       806  LOAD_STR                 '\n'
              808  LOAD_METHOD              join
              810  LOAD_FAST                'contents'
              812  CALL_METHOD_1         1  ''
              814  STORE_FAST               'contents'

 L.1364       816  LOAD_FAST                'contents'
          818_820  POP_JUMP_IF_TRUE    830  'to 830'

 L.1365       822  LOAD_FAST                'title'
              824  LOAD_STR                 '\n'
              826  BINARY_ADD       
              828  RETURN_VALUE     
            830_0  COME_FROM           818  '818'

 L.1366       830  LOAD_FAST                'title'
              832  LOAD_STR                 '\n'
              834  BINARY_ADD       
              836  LOAD_DEREF               'self'
              838  LOAD_METHOD              indent
              840  LOAD_FAST                'contents'
              842  LOAD_METHOD              rstrip
              844  CALL_METHOD_0         0  ''
              846  LOAD_STR                 ' |  '
              848  CALL_METHOD_2         2  ''
              850  BINARY_ADD       
              852  LOAD_STR                 '\n'
              854  BINARY_ADD       
              856  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_STR' instruction at offset 806

    def formatvalue(self, object):
        """Format an argument default value as text."""
        return '=' + self.repr(object)

    def docroutine(self, object, name=None, mod=None, cl=None):
        """Produce text documentation for a function or method object."""
        realname = object.__name__
        name = name or realname
        note = ''
        skipdocs = 0
        if _is_bound_method(object):
            imclass = object.__self__.__class__
            if cl:
                if imclass is not cl:
                    note = ' from ' + classname(imclass, mod)
            elif object.__self__ is not None:
                note = ' method of %s instance' % classname(object.__self__.__class__, mod)
            else:
                note = ' unbound %s method' % classname(imclass, mod)
        if inspect.iscoroutinefunction(object) or inspect.isasyncgenfunction(object):
            asyncqualifier = 'async '
        else:
            asyncqualifier = ''
        if name == realname:
            title = self.bold(realname)
        else:
            if cl:
                if inspect.getattr_static(cl, realname, []) is object:
                    skipdocs = 1
            title = self.bold(name) + ' = ' + realname
        argspec = None
        if inspect.isroutine(object):
            try:
                signature = inspect.signature(object)
            except (ValueError, TypeError):
                signature = None
            else:
                if signature:
                    argspec = str(signature)
                    if realname == '<lambda>':
                        title = self.bold(name) + ' lambda '
                        argspec = argspec[1:-1]
            if not argspec:
                argspec = '(...)'
            decl = asyncqualifier + title + argspec + note
            if skipdocs:
                return decl + '\n'
            doc = getdoc(object) or ''
            return decl + '\n' + (doc and self.indent(doc).rstrip() + '\n')

    def docdata(self, object, name=None, mod=None, cl=None):
        """Produce text documentation for a data descriptor."""
        results = []
        push = results.append
        if name:
            push(self.bold(name))
            push('\n')
        doc = getdoc(object) or ''
        if doc:
            push(self.indent(doc))
            push('\n')
        return ''.join(results)

    docproperty = docdata

    def docother(self, object, name=None, mod=None, parent=None, maxlen=None, doc=None):
        """Produce text documentation for a data object."""
        repr = self.repr(object)
        if maxlen:
            line = name and (name + ' = ') or '' + repr
            chop = maxlen - len(line)
            if chop < 0:
                repr = repr[:chop] + '...'
        line = name and (self.bold(name) + ' = ') or '' + repr
        if doc is not None:
            line += '\n' + self.indent(str(doc))
        return line


class _PlainTextDoc(TextDoc):
    __doc__ = 'Subclass of TextDoc which overrides string styling'

    def bold(self, text):
        return text


def pager(text):
    """The first time this is called, determine what kind of pager to use."""
    global pager
    pager = getpager()
    pager(text)


def getpager--- This code section failed: ---

 L.1470         0  LOAD_GLOBAL              hasattr
                2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                stdin
                6  LOAD_STR                 'isatty'
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L.1471        12  LOAD_GLOBAL              plainpager
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L.1472        16  LOAD_GLOBAL              hasattr
               18  LOAD_GLOBAL              sys
               20  LOAD_ATTR                stdout
               22  LOAD_STR                 'isatty'
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_TRUE     32  'to 32'

 L.1473        28  LOAD_GLOBAL              plainpager
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L.1474        32  LOAD_GLOBAL              sys
               34  LOAD_ATTR                stdin
               36  LOAD_METHOD              isatty
               38  CALL_METHOD_0         0  ''
               40  POP_JUMP_IF_FALSE    52  'to 52'
               42  LOAD_GLOBAL              sys
               44  LOAD_ATTR                stdout
               46  LOAD_METHOD              isatty
               48  CALL_METHOD_0         0  ''
               50  POP_JUMP_IF_TRUE     56  'to 56'
             52_0  COME_FROM            40  '40'

 L.1475        52  LOAD_GLOBAL              plainpager
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'

 L.1476        56  LOAD_GLOBAL              os
               58  LOAD_ATTR                environ
               60  LOAD_METHOD              get
               62  LOAD_STR                 'MANPAGER'
               64  CALL_METHOD_1         1  ''
               66  JUMP_IF_TRUE_OR_POP    78  'to 78'
               68  LOAD_GLOBAL              os
               70  LOAD_ATTR                environ
               72  LOAD_METHOD              get
               74  LOAD_STR                 'PAGER'
               76  CALL_METHOD_1         1  ''
             78_0  COME_FROM            66  '66'
               78  STORE_DEREF              'use_pager'

 L.1477        80  LOAD_DEREF               'use_pager'
               82  POP_JUMP_IF_FALSE   146  'to 146'

 L.1478        84  LOAD_GLOBAL              sys
               86  LOAD_ATTR                platform
               88  LOAD_STR                 'win32'
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   106  'to 106'

 L.1479        94  LOAD_CLOSURE             'use_pager'
               96  BUILD_TUPLE_1         1 
               98  LOAD_LAMBDA              '<code_object <lambda>>'
              100  LOAD_STR                 'getpager.<locals>.<lambda>'
              102  MAKE_FUNCTION_8          'closure'
              104  RETURN_VALUE     
            106_0  COME_FROM            92  '92'

 L.1480       106  LOAD_GLOBAL              os
              108  LOAD_ATTR                environ
              110  LOAD_METHOD              get
              112  LOAD_STR                 'TERM'
              114  CALL_METHOD_1         1  ''
              116  LOAD_CONST               ('dumb', 'emacs')
              118  COMPARE_OP               in
              120  POP_JUMP_IF_FALSE   134  'to 134'

 L.1481       122  LOAD_CLOSURE             'use_pager'
              124  BUILD_TUPLE_1         1 
              126  LOAD_LAMBDA              '<code_object <lambda>>'
              128  LOAD_STR                 'getpager.<locals>.<lambda>'
              130  MAKE_FUNCTION_8          'closure'
              132  RETURN_VALUE     
            134_0  COME_FROM           120  '120'

 L.1483       134  LOAD_CLOSURE             'use_pager'
              136  BUILD_TUPLE_1         1 
              138  LOAD_LAMBDA              '<code_object <lambda>>'
              140  LOAD_STR                 'getpager.<locals>.<lambda>'
              142  MAKE_FUNCTION_8          'closure'
              144  RETURN_VALUE     
            146_0  COME_FROM            82  '82'

 L.1484       146  LOAD_GLOBAL              os
              148  LOAD_ATTR                environ
              150  LOAD_METHOD              get
              152  LOAD_STR                 'TERM'
              154  CALL_METHOD_1         1  ''
              156  LOAD_CONST               ('dumb', 'emacs')
              158  COMPARE_OP               in
              160  POP_JUMP_IF_FALSE   166  'to 166'

 L.1485       162  LOAD_GLOBAL              plainpager
              164  RETURN_VALUE     
            166_0  COME_FROM           160  '160'

 L.1486       166  LOAD_GLOBAL              sys
              168  LOAD_ATTR                platform
              170  LOAD_STR                 'win32'
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_FALSE   184  'to 184'

 L.1487       176  LOAD_LAMBDA              '<code_object <lambda>>'
              178  LOAD_STR                 'getpager.<locals>.<lambda>'
              180  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              182  RETURN_VALUE     
            184_0  COME_FROM           174  '174'

 L.1488       184  LOAD_GLOBAL              hasattr
              186  LOAD_GLOBAL              os
              188  LOAD_STR                 'system'
              190  CALL_FUNCTION_2       2  ''
              192  POP_JUMP_IF_FALSE   216  'to 216'
              194  LOAD_GLOBAL              os
              196  LOAD_METHOD              system
              198  LOAD_STR                 '(less) 2>/dev/null'
              200  CALL_METHOD_1         1  ''
              202  LOAD_CONST               0
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   216  'to 216'

 L.1489       208  LOAD_LAMBDA              '<code_object <lambda>>'
              210  LOAD_STR                 'getpager.<locals>.<lambda>'
              212  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              214  RETURN_VALUE     
            216_0  COME_FROM           206  '206'
            216_1  COME_FROM           192  '192'

 L.1491       216  LOAD_CONST               0
              218  LOAD_CONST               None
              220  IMPORT_NAME              tempfile
              222  STORE_FAST               'tempfile'

 L.1492       224  LOAD_FAST                'tempfile'
              226  LOAD_METHOD              mkstemp
              228  CALL_METHOD_0         0  ''
              230  UNPACK_SEQUENCE_2     2 
              232  STORE_FAST               'fd'
              234  STORE_FAST               'filename'

 L.1493       236  LOAD_GLOBAL              os
              238  LOAD_METHOD              close
              240  LOAD_FAST                'fd'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          

 L.1494       246  SETUP_FINALLY       304  'to 304'

 L.1495       248  LOAD_GLOBAL              hasattr
              250  LOAD_GLOBAL              os
              252  LOAD_STR                 'system'
              254  CALL_FUNCTION_2       2  ''
          256_258  POP_JUMP_IF_FALSE   292  'to 292'
              260  LOAD_GLOBAL              os
              262  LOAD_METHOD              system
              264  LOAD_STR                 'more "%s"'
              266  LOAD_FAST                'filename'
              268  BINARY_MODULO    
              270  CALL_METHOD_1         1  ''
              272  LOAD_CONST               0
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_FALSE   292  'to 292'

 L.1496       280  LOAD_LAMBDA              '<code_object <lambda>>'
              282  LOAD_STR                 'getpager.<locals>.<lambda>'
              284  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              286  POP_BLOCK        
              288  CALL_FINALLY        304  'to 304'
              290  RETURN_VALUE     
            292_0  COME_FROM           276  '276'
            292_1  COME_FROM           256  '256'

 L.1498       292  LOAD_GLOBAL              ttypager
              294  POP_BLOCK        
              296  CALL_FINALLY        304  'to 304'
              298  RETURN_VALUE     
              300  POP_BLOCK        
              302  BEGIN_FINALLY    
            304_0  COME_FROM           296  '296'
            304_1  COME_FROM           288  '288'
            304_2  COME_FROM_FINALLY   246  '246'

 L.1500       304  LOAD_GLOBAL              os
              306  LOAD_METHOD              unlink
              308  LOAD_FAST                'filename'
              310  CALL_METHOD_1         1  ''
              312  POP_TOP          
              314  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 288


def plain(text):
    """Remove boldface formatting from text."""
    return re.sub('.\x08', '', text)


def pipepager(text, cmd):
    """Page through text by feeding it to another program."""
    import subprocess
    proc = subprocess.Popen(cmd, shell=True, stdin=(subprocess.PIPE))
    try:
        with io.TextIOWrapper((proc.stdin), errors='backslashreplace') as pipe:
            try:
                pipe.write(text)
            except KeyboardInterrupt:
                pass

    except OSError:
        pass
    else:
        while True:
            try:
                proc.wait()
                break
            except KeyboardInterrupt:
                pass


def tempfilepager(text, cmd):
    """Page through text by invoking a program on a temporary file."""
    import tempfile
    filename = tempfile.mktemp()
    with open(filename, 'w', errors='backslashreplace') as file:
        file.write(text)
    try:
        os.system(cmd + ' "' + filename + '"')
    finally:
        os.unlink(filename)


def _escape_stdout(text):
    encoding = getattr(sys.stdout, 'encoding', None) or 'utf-8'
    return text.encode(encoding, 'backslashreplace').decode(encoding)


def ttypager(text):
    """Page through text on a text terminal."""
    lines = plain(_escape_stdout(text)).split('\n')
    try:
        import tty
        fd = sys.stdin.fileno()
        old = tty.tcgetattr(fd)
        tty.setcbreak(fd)
        getchar = lambda: sys.stdin.read(1)
    except (ImportError, AttributeError, io.UnsupportedOperation):
        tty = None
        getchar = lambda: sys.stdin.readline()[:-1][:1]
    else:
        try:
            try:
                h = int(os.environ.get('LINES', 0))
            except ValueError:
                h = 0
            else:
                if h <= 1:
                    h = 25
                r = inc = h - 1
                sys.stdout.write('\n'.join(lines[:inc]) + '\n')
                while True:
                    while True:
                        if lines[r:]:
                            sys.stdout.write('-- more --')
                            sys.stdout.flush()
                            c = getchar()
                            if c in ('q', 'Q'):
                                sys.stdout.write('\r          \r')
                            else:
                                break
                            if c in ('\r', '\n'):
                                sys.stdout.write('\r          \r' + lines[r] + '\n')
                                r = r + 1

                    if c in ('b', 'B', '\x1b'):
                        r = r - inc - inc
                        if r < 0:
                            r = 0
                    sys.stdout.write('\n' + '\n'.join(lines[r:r + inc]) + '\n')
                    r = r + inc

        finally:
            if tty:
                tty.tcsetattr(fd, tty.TCSAFLUSH, old)


def plainpager(text):
    """Simply print unformatted text.  This is the ultimate fallback."""
    sys.stdout.write(plain(_escape_stdout(text)))


def describe(thing):
    """Produce a short description of the given thing."""
    if inspect.ismodule(thing):
        if thing.__name__ in sys.builtin_module_names:
            return 'built-in module ' + thing.__name__
        if hasattr(thing, '__path__'):
            return 'package ' + thing.__name__
        return 'module ' + thing.__name__
    if inspect.isbuiltin(thing):
        return 'built-in function ' + thing.__name__
    if inspect.isgetsetdescriptor(thing):
        return 'getset descriptor %s.%s.%s' % (
         thing.__objclass__.__module__, thing.__objclass__.__name__,
         thing.__name__)
    if inspect.ismemberdescriptor(thing):
        return 'member descriptor %s.%s.%s' % (
         thing.__objclass__.__module__, thing.__objclass__.__name__,
         thing.__name__)
    if inspect.isclass(thing):
        return 'class ' + thing.__name__
    if inspect.isfunction(thing):
        return 'function ' + thing.__name__
    if inspect.ismethod(thing):
        return 'method ' + thing.__name__
    return type(thing).__name__


def locate--- This code section failed: ---

 L.1622         0  LOAD_LISTCOMP            '<code_object <listcomp>>'
                2  LOAD_STR                 'locate.<locals>.<listcomp>'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  LOAD_FAST                'path'
                8  LOAD_METHOD              split
               10  LOAD_STR                 '.'
               12  CALL_METHOD_1         1  ''
               14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'parts'

 L.1623        20  LOAD_CONST               (None, 0)
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'module'
               26  STORE_FAST               'n'
             28_0  COME_FROM            90  '90'
             28_1  COME_FROM            86  '86'

 L.1624        28  LOAD_FAST                'n'
               30  LOAD_GLOBAL              len
               32  LOAD_FAST                'parts'
               34  CALL_FUNCTION_1       1  ''
               36  COMPARE_OP               <
               38  POP_JUMP_IF_FALSE    92  'to 92'

 L.1625        40  LOAD_GLOBAL              safeimport
               42  LOAD_STR                 '.'
               44  LOAD_METHOD              join
               46  LOAD_FAST                'parts'
               48  LOAD_CONST               None
               50  LOAD_FAST                'n'
               52  LOAD_CONST               1
               54  BINARY_ADD       
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  CALL_METHOD_1         1  ''
               62  LOAD_FAST                'forceload'
               64  CALL_FUNCTION_2       2  ''
               66  STORE_FAST               'nextmodule'

 L.1626        68  LOAD_FAST                'nextmodule'
               70  POP_JUMP_IF_FALSE    92  'to 92'

 L.1626        72  LOAD_FAST                'nextmodule'
               74  LOAD_FAST                'n'
               76  LOAD_CONST               1
               78  BINARY_ADD       
               80  ROT_TWO          
               82  STORE_FAST               'module'
               84  STORE_FAST               'n'
               86  JUMP_BACK            28  'to 28'

 L.1627        88  JUMP_FORWARD         92  'to 92'
               90  JUMP_BACK            28  'to 28'
             92_0  COME_FROM            88  '88'
             92_1  COME_FROM            70  '70'
             92_2  COME_FROM            38  '38'

 L.1628        92  LOAD_FAST                'module'
               94  POP_JUMP_IF_FALSE   102  'to 102'

 L.1629        96  LOAD_FAST                'module'
               98  STORE_FAST               'object'
              100  JUMP_FORWARD        106  'to 106'
            102_0  COME_FROM            94  '94'

 L.1631       102  LOAD_GLOBAL              builtins
              104  STORE_FAST               'object'
            106_0  COME_FROM           100  '100'

 L.1632       106  LOAD_FAST                'parts'
              108  LOAD_FAST                'n'
              110  LOAD_CONST               None
              112  BUILD_SLICE_2         2 
              114  BINARY_SUBSCR    
              116  GET_ITER         
            118_0  COME_FROM           162  '162'
            118_1  COME_FROM           136  '136'
              118  FOR_ITER            164  'to 164'
              120  STORE_FAST               'part'

 L.1633       122  SETUP_FINALLY       138  'to 138'

 L.1634       124  LOAD_GLOBAL              getattr
              126  LOAD_FAST                'object'
              128  LOAD_FAST                'part'
              130  CALL_FUNCTION_2       2  ''
              132  STORE_FAST               'object'
              134  POP_BLOCK        
              136  JUMP_BACK           118  'to 118'
            138_0  COME_FROM_FINALLY   122  '122'

 L.1635       138  DUP_TOP          
              140  LOAD_GLOBAL              AttributeError
              142  COMPARE_OP               exception-match
              144  POP_JUMP_IF_FALSE   160  'to 160'
              146  POP_TOP          
              148  POP_TOP          
              150  POP_TOP          

 L.1636       152  POP_EXCEPT       
              154  POP_TOP          
              156  LOAD_CONST               None
              158  RETURN_VALUE     
            160_0  COME_FROM           144  '144'
              160  END_FINALLY      
              162  JUMP_BACK           118  'to 118'
            164_0  COME_FROM           118  '118'

 L.1637       164  LOAD_FAST                'object'
              166  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 90


text = TextDoc()
plaintext = _PlainTextDoc()
html = HTMLDoc()

def resolve(thing, forceload=0):
    """Given an object or a path to an object, get the object and its name."""
    if isinstance(thing, str):
        object = locate(thing, forceload)
        if object is None:
            raise ImportError('No Python documentation found for %r.\nUse help() to get the interactive help utility.\nUse help(str) for help on the str class.' % thing)
        return (object, thing)
    name = getattr(thing, '__name__', None)
    return (
     thing, name if isinstance(name, str) else None)


def render_doc(thing, title='Python Library Documentation: %s', forceload=0, renderer=None):
    """Render text documentation, given an object or a path to an object."""
    if renderer is None:
        renderer = text
    object, name = resolve(thing, forceload)
    desc = describe(object)
    module = inspect.getmodule(object)
    if name and '.' in name:
        desc += ' in ' + name[:name.rfind('.')]
    elif module:
        if module is not object:
            desc += ' in module ' + module.__name__
    if not inspect.ismodule(object):
        if not inspect.isclass(object):
            if not inspect.isroutine(object):
                if not inspect.isdatadescriptor(object):
                    object = type(object)
                    desc += ' object'
        return title % desc + '\n\n' + renderer.document(object, name)


def doc(thing, title='Python Library Documentation: %s', forceload=0, output=None):
    """Display text documentation, given an object or a path to an object."""
    try:
        if output is None:
            pager(render_doc(thing, title, forceload))
        else:
            output.write(render_doc(thing, title, forceload, plaintext))
    except (ImportError, ErrorDuringImport) as value:
        try:
            print(value)
        finally:
            value = None
            del value


def writedoc(thing, forceload=0):
    """Write HTML documentation to a file in the current directory."""
    try:
        object, name = resolve(thing, forceload)
        page = html.page(describe(object), html.document(object, name))
        with open((name + '.html'), 'w', encoding='utf-8') as file:
            file.write(page)
        print('wrote', name + '.html')
    except (ImportError, ErrorDuringImport) as value:
        try:
            print(value)
        finally:
            value = None
            del value


def writedocs(dir, pkgpath='', done=None):
    """Write out HTML documentation for all modules in a directory tree."""
    if done is None:
        done = {}
    for importer, modname, ispkg in pkgutil.walk_packages([dir], pkgpath):
        writedoc(modname)


class Helper:
    keywords = {'False':'', 
     'None':'', 
     'True':'', 
     'and':'BOOLEAN', 
     'as':'with', 
     'assert':('assert', ''), 
     'async':('async', ''), 
     'await':('await', ''), 
     'break':('break', 'while for'), 
     'class':('class', 'CLASSES SPECIALMETHODS'), 
     'continue':('continue', 'while for'), 
     'def':('function', ''), 
     'del':('del', 'BASICMETHODS'), 
     'elif':'if', 
     'else':('else', 'while for'), 
     'except':'try', 
     'finally':'try', 
     'for':('for', 'break continue while'), 
     'from':'import', 
     'global':('global', 'nonlocal NAMESPACES'), 
     'if':('if', 'TRUTHVALUE'), 
     'import':('import', 'MODULES'), 
     'in':('in', 'SEQUENCEMETHODS'), 
     'is':'COMPARISON', 
     'lambda':('lambda', 'FUNCTIONS'), 
     'nonlocal':('nonlocal', 'global NAMESPACES'), 
     'not':'BOOLEAN', 
     'or':'BOOLEAN', 
     'pass':('pass', ''), 
     'raise':('raise', 'EXCEPTIONS'), 
     'return':('return', 'FUNCTIONS'), 
     'try':('try', 'EXCEPTIONS'), 
     'while':('while', 'break continue if TRUTHVALUE'), 
     'with':('with', 'CONTEXTMANAGERS EXCEPTIONS yield'), 
     'yield':('yield', '')}
    _strprefixes = [p + q for p in ('b', 'f', 'r', 'u') for q in ("'", '"')]
    _symbols_inverse = {'STRINGS':(
      *("'", "'''", '"', '"""'), *_strprefixes), 
     'OPERATORS':('+', '-', '*', '**', '/', '//', '%', '<<', '>>', '&', '|', '^', '~', '<', '>', '<=',
 '>=', '==', '!=', '<>'), 
     'COMPARISON':('<', '>', '<=', '>=', '==', '!=', '<>'), 
     'UNARY':('-', '~'), 
     'AUGMENTEDASSIGNMENT':('+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '**=', '//='), 
     'BITWISE':('<<', '>>', '&', '|', '^', '~'), 
     'COMPLEX':('j', 'J')}
    symbols = {'%':'OPERATORS FORMATTING', 
     '**':'POWER', 
     ',':'TUPLES LISTS FUNCTIONS', 
     '.':'ATTRIBUTES FLOAT MODULES OBJECTS', 
     '...':'ELLIPSIS', 
     ':':'SLICINGS DICTIONARYLITERALS', 
     '@':'def class', 
     '\\':'STRINGS', 
     '_':'PRIVATENAMES', 
     '__':'PRIVATENAMES SPECIALMETHODS', 
     '`':'BACKQUOTES', 
     '(':'TUPLES FUNCTIONS CALLS', 
     ')':'TUPLES FUNCTIONS CALLS', 
     '[':'LISTS SUBSCRIPTS SLICINGS', 
     ']':'LISTS SUBSCRIPTS SLICINGS'}
    for topic, symbols_ in _symbols_inverse.items():
        for symbol in symbols_:
            topics = symbols.get(symbol, topic)
            if topic not in topics:
                topics = topics + ' ' + topic
            else:
                symbols[symbol] = topics

    else:
        topics = {'TYPES':('types', 'STRINGS UNICODE NUMBERS SEQUENCES MAPPINGS FUNCTIONS CLASSES MODULES FILES inspect'), 
         'STRINGS':('strings', 'str UNICODE SEQUENCES STRINGMETHODS FORMATTING TYPES'), 
         'STRINGMETHODS':('string-methods', 'STRINGS FORMATTING'), 
         'FORMATTING':('formatstrings', 'OPERATORS'), 
         'UNICODE':('strings', 'encodings unicode SEQUENCES STRINGMETHODS FORMATTING TYPES'), 
         'NUMBERS':('numbers', 'INTEGER FLOAT COMPLEX TYPES'), 
         'INTEGER':('integers', 'int range'), 
         'FLOAT':('floating', 'float math'), 
         'COMPLEX':('imaginary', 'complex cmath'), 
         'SEQUENCES':('typesseq', 'STRINGMETHODS FORMATTING range LISTS'), 
         'MAPPINGS':'DICTIONARIES', 
         'FUNCTIONS':('typesfunctions', 'def TYPES'), 
         'METHODS':('typesmethods', 'class def CLASSES TYPES'), 
         'CODEOBJECTS':('bltin-code-objects', 'compile FUNCTIONS TYPES'), 
         'TYPEOBJECTS':('bltin-type-objects', 'types TYPES'), 
         'FRAMEOBJECTS':'TYPES', 
         'TRACEBACKS':'TYPES', 
         'NONE':('bltin-null-object', ''), 
         'ELLIPSIS':('bltin-ellipsis-object', 'SLICINGS'), 
         'SPECIALATTRIBUTES':('specialattrs', ''), 
         'CLASSES':('types', 'class SPECIALMETHODS PRIVATENAMES'), 
         'MODULES':('typesmodules', 'import'), 
         'PACKAGES':'import', 
         'EXPRESSIONS':('operator-summary', 'lambda or and not in is BOOLEAN COMPARISON BITWISE SHIFTING BINARY FORMATTING POWER UNARY ATTRIBUTES SUBSCRIPTS SLICINGS CALLS TUPLES LISTS DICTIONARIES'), 
         'OPERATORS':'EXPRESSIONS', 
         'PRECEDENCE':'EXPRESSIONS', 
         'OBJECTS':('objects', 'TYPES'), 
         'SPECIALMETHODS':('specialnames', 'BASICMETHODS ATTRIBUTEMETHODS CALLABLEMETHODS SEQUENCEMETHODS MAPPINGMETHODS NUMBERMETHODS CLASSES'), 
         'BASICMETHODS':('customization', 'hash repr str SPECIALMETHODS'), 
         'ATTRIBUTEMETHODS':('attribute-access', 'ATTRIBUTES SPECIALMETHODS'), 
         'CALLABLEMETHODS':('callable-types', 'CALLS SPECIALMETHODS'), 
         'SEQUENCEMETHODS':('sequence-types', 'SEQUENCES SEQUENCEMETHODS SPECIALMETHODS'), 
         'MAPPINGMETHODS':('sequence-types', 'MAPPINGS SPECIALMETHODS'), 
         'NUMBERMETHODS':('numeric-types', 'NUMBERS AUGMENTEDASSIGNMENT SPECIALMETHODS'), 
         'EXECUTION':('execmodel', 'NAMESPACES DYNAMICFEATURES EXCEPTIONS'), 
         'NAMESPACES':('naming', 'global nonlocal ASSIGNMENT DELETION DYNAMICFEATURES'), 
         'DYNAMICFEATURES':('dynamic-features', ''), 
         'SCOPING':'NAMESPACES', 
         'FRAMES':'NAMESPACES', 
         'EXCEPTIONS':('exceptions', 'try except finally raise'), 
         'CONVERSIONS':('conversions', ''), 
         'IDENTIFIERS':('identifiers', 'keywords SPECIALIDENTIFIERS'), 
         'SPECIALIDENTIFIERS':('id-classes', ''), 
         'PRIVATENAMES':('atom-identifiers', ''), 
         'LITERALS':('atom-literals', 'STRINGS NUMBERS TUPLELITERALS LISTLITERALS DICTIONARYLITERALS'), 
         'TUPLES':'SEQUENCES', 
         'TUPLELITERALS':('exprlists', 'TUPLES LITERALS'), 
         'LISTS':('typesseq-mutable', 'LISTLITERALS'), 
         'LISTLITERALS':('lists', 'LISTS LITERALS'), 
         'DICTIONARIES':('typesmapping', 'DICTIONARYLITERALS'), 
         'DICTIONARYLITERALS':('dict', 'DICTIONARIES LITERALS'), 
         'ATTRIBUTES':('attribute-references', 'getattr hasattr setattr ATTRIBUTEMETHODS'), 
         'SUBSCRIPTS':('subscriptions', 'SEQUENCEMETHODS'), 
         'SLICINGS':('slicings', 'SEQUENCEMETHODS'), 
         'CALLS':('calls', 'EXPRESSIONS'), 
         'POWER':('power', 'EXPRESSIONS'), 
         'UNARY':('unary', 'EXPRESSIONS'), 
         'BINARY':('binary', 'EXPRESSIONS'), 
         'SHIFTING':('shifting', 'EXPRESSIONS'), 
         'BITWISE':('bitwise', 'EXPRESSIONS'), 
         'COMPARISON':('comparisons', 'EXPRESSIONS BASICMETHODS'), 
         'BOOLEAN':('booleans', 'EXPRESSIONS TRUTHVALUE'), 
         'ASSERTION':'assert', 
         'ASSIGNMENT':('assignment', 'AUGMENTEDASSIGNMENT'), 
         'AUGMENTEDASSIGNMENT':('augassign', 'NUMBERMETHODS'), 
         'DELETION':'del', 
         'RETURNING':'return', 
         'IMPORTING':'import', 
         'CONDITIONAL':'if', 
         'LOOPING':('compound', 'for while break continue'), 
         'TRUTHVALUE':('truth', 'if while and or not BASICMETHODS'), 
         'DEBUGGING':('debugger', 'pdb'), 
         'CONTEXTMANAGERS':('context-managers', 'with')}

        def __init__(self, input=None, output=None):
            self._input = input
            self._output = output

        @property
        def input(self):
            return self._input or sys.stdin

        @property
        def output(self):
            return self._output or sys.stdout

        def __repr__(self):
            if inspect.stack()[1][3] == '?':
                self()
                return ''
            return '<%s.%s instance>' % (self.__class__.__module__,
             self.__class__.__qualname__)

        _GoInteractive = object()

        def __call__(self, request=_GoInteractive):
            if request is not self._GoInteractive:
                self.help(request)
            else:
                self.intro()
                self.interact()
                self.output.write('\nYou are now leaving help and returning to the Python interpreter.\nIf you want to ask for help on a particular object directly from the\ninterpreter, you can type "help(object)".  Executing "help(\'string\')"\nhas the same effect as typing a particular string at the help> prompt.\n')

        def interact(self):
            self.output.write('\n')
            while True:
                while True:
                    try:
                        request = self.getline('help> ')
                        if not request:
                            break
                    except (KeyboardInterrupt, EOFError):
                        break
                    else:
                        request = request.strip()
                        if len(request) > 2:
                            if request[0] == request[(-1)] in ("'", '"'):
                                if request[0] not in request[1:-1]:
                                    request = request[1:-1]
                        if request.lower() in ('q', 'quit'):
                            pass
                        elif request == 'help':
                            self.intro()

                self.help(request)

        def getline(self, prompt):
            """Read one line, using input() when appropriate."""
            if self.input is sys.stdin:
                return input(prompt)
            self.output.write(prompt)
            self.output.flush()
            return self.input.readline()

        def help(self, request):
            if type(request) is type(''):
                request = request.strip()
                if request == 'keywords':
                    self.listkeywords()
                elif request == 'symbols':
                    self.listsymbols()
                elif request == 'topics':
                    self.listtopics()
                elif request == 'modules':
                    self.listmodules()
                elif request[:8] == 'modules ':
                    self.listmodules(request.split()[1])
                elif request in self.symbols:
                    self.showsymbol(request)
                elif request in ('True', 'False', 'None'):
                    doc(eval(request), 'Help on %s:')
                elif request in self.keywords:
                    self.showtopic(request)
                elif request in self.topics:
                    self.showtopic(request)
                elif request:
                    doc(request, 'Help on %s:', output=(self._output))
                else:
                    doc(str, 'Help on %s:', output=(self._output))
            elif isinstance(request, Helper):
                self()
            else:
                doc(request, 'Help on %s:', output=(self._output))
            self.output.write('\n')

        def intro(self):
            self.output.write('\nWelcome to Python {0}\'s help utility!\n\nIf this is your first time using Python, you should definitely check out\nthe tutorial on the Internet at https://docs.python.org/{0}/tutorial/.\n\nEnter the name of any module, keyword, or topic to get help on writing\nPython programs and using Python modules.  To quit this help utility and\nreturn to the interpreter, just type "quit".\n\nTo get a list of available modules, keywords, symbols, or topics, type\n"modules", "keywords", "symbols", or "topics".  Each module also comes\nwith a one-line summary of what it does; to list the modules whose name\nor summary contain a given string such as "spam", type "modules spam".\n'.format('%d.%d' % sys.version_info[:2]))

        def list(self, items, columns=4, width=80):
            items = list(sorted(items))
            colw = width // columns
            rows = (len(items) + columns - 1) // columns
            for row in range(rows):
                for col in range(columns):
                    i = col * rows + row
                    if i < len(items):
                        self.output.write(items[i])
                        if col < columns - 1:
                            self.output.write(' ' + ' ' * (colw - 1 - len(items[i])))
                        self.output.write('\n')

        def listkeywords(self):
            self.output.write('\nHere is a list of the Python keywords.  Enter any keyword to get more help.\n\n')
            self.list(self.keywords.keys())

        def listsymbols(self):
            self.output.write('\nHere is a list of the punctuation symbols which Python assigns special meaning\nto. Enter any symbol to get more help.\n\n')
            self.list(self.symbols.keys())

        def listtopics(self):
            self.output.write('\nHere is a list of available topics.  Enter any topic name to get more help.\n\n')
            self.list(self.topics.keys())

        def showtopic--- This code section failed: ---

 L.2023         0  SETUP_FINALLY        14  'to 14'

 L.2024         2  LOAD_CONST               0
                4  LOAD_CONST               None
                6  IMPORT_NAME_ATTR         pydoc_data.topics
                8  STORE_FAST               'pydoc_data'
               10  POP_BLOCK        
               12  JUMP_FORWARD         48  'to 48'
             14_0  COME_FROM_FINALLY     0  '0'

 L.2025        14  DUP_TOP          
               16  LOAD_GLOBAL              ImportError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    46  'to 46'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.2026        28  LOAD_FAST                'self'
               30  LOAD_ATTR                output
               32  LOAD_METHOD              write
               34  LOAD_STR                 '\nSorry, topic and keyword documentation is not available because the\nmodule "pydoc_data.topics" could not be found.\n'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L.2030        40  POP_EXCEPT       
               42  LOAD_CONST               None
               44  RETURN_VALUE     
             46_0  COME_FROM            20  '20'
               46  END_FINALLY      
             48_0  COME_FROM            12  '12'

 L.2031        48  LOAD_FAST                'self'
               50  LOAD_ATTR                topics
               52  LOAD_METHOD              get
               54  LOAD_FAST                'topic'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                keywords
               60  LOAD_METHOD              get
               62  LOAD_FAST                'topic'
               64  CALL_METHOD_1         1  ''
               66  CALL_METHOD_2         2  ''
               68  STORE_FAST               'target'

 L.2032        70  LOAD_FAST                'target'
               72  POP_JUMP_IF_TRUE     98  'to 98'

 L.2033        74  LOAD_FAST                'self'
               76  LOAD_ATTR                output
               78  LOAD_METHOD              write
               80  LOAD_STR                 'no documentation found for %s\n'
               82  LOAD_GLOBAL              repr
               84  LOAD_FAST                'topic'
               86  CALL_FUNCTION_1       1  ''
               88  BINARY_MODULO    
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L.2034        94  LOAD_CONST               None
               96  RETURN_VALUE     
             98_0  COME_FROM            72  '72'

 L.2035        98  LOAD_GLOBAL              type
              100  LOAD_FAST                'target'
              102  CALL_FUNCTION_1       1  ''
              104  LOAD_GLOBAL              type
              106  LOAD_STR                 ''
              108  CALL_FUNCTION_1       1  ''
              110  COMPARE_OP               is
              112  POP_JUMP_IF_FALSE   126  'to 126'

 L.2036       114  LOAD_FAST                'self'
              116  LOAD_METHOD              showtopic
              118  LOAD_FAST                'target'
              120  LOAD_FAST                'more_xrefs'
              122  CALL_METHOD_2         2  ''
              124  RETURN_VALUE     
            126_0  COME_FROM           112  '112'

 L.2038       126  LOAD_FAST                'target'
              128  UNPACK_SEQUENCE_2     2 
              130  STORE_FAST               'label'
              132  STORE_FAST               'xrefs'

 L.2039       134  SETUP_FINALLY       152  'to 152'

 L.2040       136  LOAD_FAST                'pydoc_data'
              138  LOAD_ATTR                topics
              140  LOAD_ATTR                topics
              142  LOAD_FAST                'label'
              144  BINARY_SUBSCR    
              146  STORE_FAST               'doc'
              148  POP_BLOCK        
              150  JUMP_FORWARD        194  'to 194'
            152_0  COME_FROM_FINALLY   134  '134'

 L.2041       152  DUP_TOP          
              154  LOAD_GLOBAL              KeyError
              156  COMPARE_OP               exception-match
              158  POP_JUMP_IF_FALSE   192  'to 192'
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L.2042       166  LOAD_FAST                'self'
              168  LOAD_ATTR                output
              170  LOAD_METHOD              write
              172  LOAD_STR                 'no documentation found for %s\n'
              174  LOAD_GLOBAL              repr
              176  LOAD_FAST                'topic'
              178  CALL_FUNCTION_1       1  ''
              180  BINARY_MODULO    
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          

 L.2043       186  POP_EXCEPT       
              188  LOAD_CONST               None
              190  RETURN_VALUE     
            192_0  COME_FROM           158  '158'
              192  END_FINALLY      
            194_0  COME_FROM           150  '150'

 L.2044       194  LOAD_FAST                'doc'
              196  LOAD_METHOD              strip
              198  CALL_METHOD_0         0  ''
              200  LOAD_STR                 '\n'
              202  BINARY_ADD       
              204  STORE_FAST               'doc'

 L.2045       206  LOAD_FAST                'more_xrefs'
              208  POP_JUMP_IF_FALSE   226  'to 226'

 L.2046       210  LOAD_FAST                'xrefs'
              212  JUMP_IF_TRUE_OR_POP   216  'to 216'
              214  LOAD_STR                 ''
            216_0  COME_FROM           212  '212'
              216  LOAD_STR                 ' '
              218  BINARY_ADD       
              220  LOAD_FAST                'more_xrefs'
              222  BINARY_ADD       
              224  STORE_FAST               'xrefs'
            226_0  COME_FROM           208  '208'

 L.2047       226  LOAD_FAST                'xrefs'
          228_230  POP_JUMP_IF_FALSE   292  'to 292'

 L.2048       232  LOAD_CONST               0
              234  LOAD_CONST               None
              236  IMPORT_NAME              textwrap
              238  STORE_FAST               'textwrap'

 L.2049       240  LOAD_STR                 'Related help topics: '
              242  LOAD_STR                 ', '
              244  LOAD_METHOD              join
              246  LOAD_FAST                'xrefs'
              248  LOAD_METHOD              split
              250  CALL_METHOD_0         0  ''
              252  CALL_METHOD_1         1  ''
              254  BINARY_ADD       
              256  LOAD_STR                 '\n'
              258  BINARY_ADD       
              260  STORE_FAST               'text'

 L.2050       262  LOAD_FAST                'textwrap'
              264  LOAD_METHOD              wrap
              266  LOAD_FAST                'text'
              268  LOAD_CONST               72
              270  CALL_METHOD_2         2  ''
              272  STORE_FAST               'wrapped_text'

 L.2051       274  LOAD_FAST                'doc'
              276  LOAD_STR                 '\n%s\n'
              278  LOAD_STR                 '\n'
              280  LOAD_METHOD              join
              282  LOAD_FAST                'wrapped_text'
              284  CALL_METHOD_1         1  ''
              286  BINARY_MODULO    
              288  INPLACE_ADD      
              290  STORE_FAST               'doc'
            292_0  COME_FROM           228  '228'

 L.2052       292  LOAD_GLOBAL              pager
              294  LOAD_FAST                'doc'
              296  CALL_FUNCTION_1       1  ''
              298  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 42

        def _gettopic(self, topic, more_xrefs=''):
            """Return unbuffered tuple of (topic, xrefs).

        If an error occurs here, the exception is caught and displayed by
        the url handler.

        This function duplicates the showtopic method but returns its
        result directly so it can be formatted for display in an html page.
        """
            try:
                import pydoc_data.topics
            except ImportError:
                return ('\nSorry, topic and keyword documentation is not available because the\nmodule "pydoc_data.topics" could not be found.\n',
                        '')
            else:
                target = self.topics.get(topic, self.keywords.get(topic))
                if not target:
                    raise ValueError('could not find topic')
                else:
                    if isinstance(target, str):
                        return self._gettopic(target, more_xrefs)
                    label, xrefs = target
                    doc = pydoc_data.topics.topics[label]
                    if more_xrefs:
                        xrefs = (xrefs or '') + ' ' + more_xrefs
                    return (doc, xrefs)

        def showsymbol(self, symbol):
            target = self.symbols[symbol]
            topic, _, xrefs = target.partition(' ')
            self.showtopic(topic, xrefs)

        def listmodules(self, key=''):
            if key:
                self.output.write("\nHere is a list of modules whose name or summary contains '{}'.\nIf there are any, enter a module name to get more help.\n\n".format(key))
                apropos(key)
            else:
                self.output.write('\nPlease wait a moment while I gather a list of all available modules...\n\n')
                modules = {}

                def callback(path, modname, desc, modules=modules):
                    if modname:
                        if modname[-9:] == '.__init__':
                            modname = modname[:-9] + ' (package)'
                    if modname.find('.') < 0:
                        modules[modname] = 1

                def onerror(modname):
                    callback(None, modname, None)

                ModuleScanner().run(callback, onerror=onerror)
                self.list(modules.keys())
                self.output.write('\nEnter any module name to get more help.  Or, type "modules spam" to search\nfor modules whose name or summary contain the string "spam".\n')


help = Helper()

class ModuleScanner:
    __doc__ = 'An interruptible scanner that searches module synopses.'

    def run--- This code section failed: ---

 L.2120         0  LOAD_FAST                'key'
                2  POP_JUMP_IF_FALSE    12  'to 12'

 L.2120         4  LOAD_FAST                'key'
                6  LOAD_METHOD              lower
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'key'
             12_0  COME_FROM             2  '2'

 L.2121        12  LOAD_CONST               False
               14  LOAD_FAST                'self'
               16  STORE_ATTR               quit

 L.2122        18  BUILD_MAP_0           0 
               20  STORE_FAST               'seen'

 L.2124        22  LOAD_GLOBAL              sys
               24  LOAD_ATTR                builtin_module_names
               26  GET_ITER         
             28_0  COME_FROM           140  '140'
             28_1  COME_FROM           126  '126'
             28_2  COME_FROM            68  '68'
             28_3  COME_FROM            38  '38'
               28  FOR_ITER            142  'to 142'
               30  STORE_FAST               'modname'

 L.2125        32  LOAD_FAST                'modname'
               34  LOAD_STR                 '__main__'
               36  COMPARE_OP               !=
               38  POP_JUMP_IF_FALSE_BACK    28  'to 28'

 L.2126        40  LOAD_CONST               1
               42  LOAD_FAST                'seen'
               44  LOAD_FAST                'modname'
               46  STORE_SUBSCR     

 L.2127        48  LOAD_FAST                'key'
               50  LOAD_CONST               None
               52  COMPARE_OP               is
               54  POP_JUMP_IF_FALSE    70  'to 70'

 L.2128        56  LOAD_FAST                'callback'
               58  LOAD_CONST               None
               60  LOAD_FAST                'modname'
               62  LOAD_STR                 ''
               64  CALL_FUNCTION_3       3  ''
               66  POP_TOP          
               68  JUMP_BACK            28  'to 28'
             70_0  COME_FROM            54  '54'

 L.2130        70  LOAD_GLOBAL              __import__
               72  LOAD_FAST                'modname'
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_ATTR                __doc__
               78  JUMP_IF_TRUE_OR_POP    82  'to 82'
               80  LOAD_STR                 ''
             82_0  COME_FROM            78  '78'
               82  STORE_FAST               'name'

 L.2131        84  LOAD_FAST                'name'
               86  LOAD_METHOD              split
               88  LOAD_STR                 '\n'
               90  CALL_METHOD_1         1  ''
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  STORE_FAST               'desc'

 L.2132        98  LOAD_FAST                'modname'
              100  LOAD_STR                 ' - '
              102  BINARY_ADD       
              104  LOAD_FAST                'desc'
              106  BINARY_ADD       
              108  STORE_FAST               'name'

 L.2133       110  LOAD_FAST                'name'
              112  LOAD_METHOD              lower
              114  CALL_METHOD_0         0  ''
              116  LOAD_METHOD              find
              118  LOAD_FAST                'key'
              120  CALL_METHOD_1         1  ''
              122  LOAD_CONST               0
              124  COMPARE_OP               >=
              126  POP_JUMP_IF_FALSE_BACK    28  'to 28'

 L.2134       128  LOAD_FAST                'callback'
              130  LOAD_CONST               None
              132  LOAD_FAST                'modname'
              134  LOAD_FAST                'desc'
              136  CALL_FUNCTION_3       3  ''
              138  POP_TOP          
              140  JUMP_BACK            28  'to 28'
            142_0  COME_FROM            28  '28'

 L.2136       142  LOAD_GLOBAL              pkgutil
              144  LOAD_ATTR                walk_packages
              146  LOAD_FAST                'onerror'
              148  LOAD_CONST               ('onerror',)
              150  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              152  GET_ITER         
            154_0  COME_FROM           504  '504'
            154_1  COME_FROM           490  '490'
            154_2  COME_FROM           416  '416'
            154_3  COME_FROM           308  '308'
            154_4  COME_FROM           234  '234'
            154_5  COME_FROM           198  '198'
          154_156  FOR_ITER            506  'to 506'
              158  UNPACK_SEQUENCE_3     3 
              160  STORE_FAST               'importer'
              162  STORE_FAST               'modname'
              164  STORE_FAST               'ispkg'

 L.2137       166  LOAD_FAST                'self'
              168  LOAD_ATTR                quit
              170  POP_JUMP_IF_FALSE   178  'to 178'

 L.2138       172  POP_TOP          
          174_176  JUMP_FORWARD        506  'to 506'
            178_0  COME_FROM           170  '170'

 L.2140       178  LOAD_FAST                'key'
              180  LOAD_CONST               None
              182  COMPARE_OP               is
              184  POP_JUMP_IF_FALSE   200  'to 200'

 L.2141       186  LOAD_FAST                'callback'
              188  LOAD_CONST               None
              190  LOAD_FAST                'modname'
              192  LOAD_STR                 ''
              194  CALL_FUNCTION_3       3  ''
              196  POP_TOP          
              198  JUMP_BACK           154  'to 154'
            200_0  COME_FROM           184  '184'

 L.2143       200  SETUP_FINALLY       218  'to 218'

 L.2144       202  LOAD_GLOBAL              pkgutil
              204  LOAD_METHOD              _get_spec
              206  LOAD_FAST                'importer'
              208  LOAD_FAST                'modname'
              210  CALL_METHOD_2         2  ''
              212  STORE_FAST               'spec'
              214  POP_BLOCK        
              216  JUMP_FORWARD        242  'to 242'
            218_0  COME_FROM_FINALLY   200  '200'

 L.2145       218  DUP_TOP          
              220  LOAD_GLOBAL              SyntaxError
              222  COMPARE_OP               exception-match
              224  POP_JUMP_IF_FALSE   240  'to 240'
              226  POP_TOP          
              228  POP_TOP          
              230  POP_TOP          

 L.2147       232  POP_EXCEPT       
              234  JUMP_BACK           154  'to 154'
              236  POP_EXCEPT       
              238  JUMP_FORWARD        242  'to 242'
            240_0  COME_FROM           224  '224'
              240  END_FINALLY      
            242_0  COME_FROM           238  '238'
            242_1  COME_FROM           216  '216'

 L.2148       242  LOAD_FAST                'spec'
              244  LOAD_ATTR                loader
              246  STORE_FAST               'loader'

 L.2149       248  LOAD_GLOBAL              hasattr
              250  LOAD_FAST                'loader'
              252  LOAD_STR                 'get_source'
              254  CALL_FUNCTION_2       2  ''
          256_258  POP_JUMP_IF_FALSE   366  'to 366'

 L.2150       260  SETUP_FINALLY       276  'to 276'

 L.2151       262  LOAD_FAST                'loader'
              264  LOAD_METHOD              get_source
              266  LOAD_FAST                'modname'
              268  CALL_METHOD_1         1  ''
              270  STORE_FAST               'source'
              272  POP_BLOCK        
              274  JUMP_FORWARD        316  'to 316'
            276_0  COME_FROM_FINALLY   260  '260'

 L.2152       276  DUP_TOP          
              278  LOAD_GLOBAL              Exception
              280  COMPARE_OP               exception-match
          282_284  POP_JUMP_IF_FALSE   314  'to 314'
              286  POP_TOP          
              288  POP_TOP          
              290  POP_TOP          

 L.2153       292  LOAD_FAST                'onerror'
          294_296  POP_JUMP_IF_FALSE   306  'to 306'

 L.2154       298  LOAD_FAST                'onerror'
              300  LOAD_FAST                'modname'
              302  CALL_FUNCTION_1       1  ''
              304  POP_TOP          
            306_0  COME_FROM           294  '294'

 L.2155       306  POP_EXCEPT       
              308  JUMP_BACK           154  'to 154'
              310  POP_EXCEPT       
              312  JUMP_FORWARD        316  'to 316'
            314_0  COME_FROM           282  '282'
              314  END_FINALLY      
            316_0  COME_FROM           312  '312'
            316_1  COME_FROM           274  '274'

 L.2156       316  LOAD_GLOBAL              source_synopsis
              318  LOAD_GLOBAL              io
              320  LOAD_METHOD              StringIO
              322  LOAD_FAST                'source'
              324  CALL_METHOD_1         1  ''
              326  CALL_FUNCTION_1       1  ''
          328_330  JUMP_IF_TRUE_OR_POP   334  'to 334'
              332  LOAD_STR                 ''
            334_0  COME_FROM           328  '328'
              334  STORE_FAST               'desc'

 L.2157       336  LOAD_GLOBAL              hasattr
              338  LOAD_FAST                'loader'
              340  LOAD_STR                 'get_filename'
              342  CALL_FUNCTION_2       2  ''
          344_346  POP_JUMP_IF_FALSE   360  'to 360'

 L.2158       348  LOAD_FAST                'loader'
              350  LOAD_METHOD              get_filename
              352  LOAD_FAST                'modname'
              354  CALL_METHOD_1         1  ''
              356  STORE_FAST               'path'
              358  JUMP_FORWARD        364  'to 364'
            360_0  COME_FROM           344  '344'

 L.2160       360  LOAD_CONST               None
              362  STORE_FAST               'path'
            364_0  COME_FROM           358  '358'
              364  JUMP_FORWARD        462  'to 462'
            366_0  COME_FROM           256  '256'

 L.2162       366  SETUP_FINALLY       384  'to 384'

 L.2163       368  LOAD_GLOBAL              importlib
              370  LOAD_ATTR                _bootstrap
              372  LOAD_METHOD              _load
              374  LOAD_FAST                'spec'
              376  CALL_METHOD_1         1  ''
              378  STORE_FAST               'module'
              380  POP_BLOCK        
              382  JUMP_FORWARD        424  'to 424'
            384_0  COME_FROM_FINALLY   366  '366'

 L.2164       384  DUP_TOP          
              386  LOAD_GLOBAL              ImportError
              388  COMPARE_OP               exception-match
          390_392  POP_JUMP_IF_FALSE   422  'to 422'
              394  POP_TOP          
              396  POP_TOP          
              398  POP_TOP          

 L.2165       400  LOAD_FAST                'onerror'
          402_404  POP_JUMP_IF_FALSE   414  'to 414'

 L.2166       406  LOAD_FAST                'onerror'
              408  LOAD_FAST                'modname'
              410  CALL_FUNCTION_1       1  ''
              412  POP_TOP          
            414_0  COME_FROM           402  '402'

 L.2167       414  POP_EXCEPT       
              416  JUMP_BACK           154  'to 154'
              418  POP_EXCEPT       
              420  JUMP_FORWARD        424  'to 424'
            422_0  COME_FROM           390  '390'
              422  END_FINALLY      
            424_0  COME_FROM           420  '420'
            424_1  COME_FROM           382  '382'

 L.2168       424  LOAD_FAST                'module'
              426  LOAD_ATTR                __doc__
          428_430  POP_JUMP_IF_FALSE   446  'to 446'
              432  LOAD_FAST                'module'
              434  LOAD_ATTR                __doc__
              436  LOAD_METHOD              splitlines
              438  CALL_METHOD_0         0  ''
              440  LOAD_CONST               0
              442  BINARY_SUBSCR    
              444  JUMP_FORWARD        448  'to 448'
            446_0  COME_FROM           428  '428'
              446  LOAD_STR                 ''
            448_0  COME_FROM           444  '444'
              448  STORE_FAST               'desc'

 L.2169       450  LOAD_GLOBAL              getattr
              452  LOAD_FAST                'module'
              454  LOAD_STR                 '__file__'
              456  LOAD_CONST               None
              458  CALL_FUNCTION_3       3  ''
              460  STORE_FAST               'path'
            462_0  COME_FROM           364  '364'

 L.2170       462  LOAD_FAST                'modname'
              464  LOAD_STR                 ' - '
              466  BINARY_ADD       
              468  LOAD_FAST                'desc'
              470  BINARY_ADD       
              472  STORE_FAST               'name'

 L.2171       474  LOAD_FAST                'name'
              476  LOAD_METHOD              lower
              478  CALL_METHOD_0         0  ''
              480  LOAD_METHOD              find
              482  LOAD_FAST                'key'
              484  CALL_METHOD_1         1  ''
              486  LOAD_CONST               0
              488  COMPARE_OP               >=
              490  POP_JUMP_IF_FALSE_BACK   154  'to 154'

 L.2172       492  LOAD_FAST                'callback'
              494  LOAD_FAST                'path'
              496  LOAD_FAST                'modname'
              498  LOAD_FAST                'desc'
              500  CALL_FUNCTION_3       3  ''
              502  POP_TOP          
              504  JUMP_BACK           154  'to 154'
            506_0  COME_FROM           174  '174'
            506_1  COME_FROM           154  '154'

 L.2174       506  LOAD_FAST                'completer'
          508_510  POP_JUMP_IF_FALSE   518  'to 518'

 L.2175       512  LOAD_FAST                'completer'
              514  CALL_FUNCTION_0       0  ''
              516  POP_TOP          
            518_0  COME_FROM           508  '508'

Parse error at or near `JUMP_FORWARD' instruction at offset 174_176


def apropos(key):
    """Print all the one-line module summaries that contain a substring."""

    def callback(path, modname, desc):
        if modname[-9:] == '.__init__':
            modname = modname[:-9] + ' (package)'
        print(modname, desc and '- ' + desc)

    def onerror(modname):
        pass

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        ModuleScanner().run(callback, key, onerror=onerror)


def _start_server(urlhandler, hostname, port):
    """Start an HTTP server thread on a specific port.

    Start an HTML/text server thread, so HTML or text documents can be
    browsed dynamically and interactively with a Web browser.  Example use:

        >>> import time
        >>> import pydoc

        Define a URL handler.  To determine what the client is asking
        for, check the URL and content_type.

        Then get or generate some text or HTML code and return it.

        >>> def my_url_handler(url, content_type):
        ...     text = 'the URL sent was: (%s, %s)' % (url, content_type)
        ...     return text

        Start server thread on port 0.
        If you use port 0, the server will pick a random port number.
        You can then use serverthread.port to get the port number.

        >>> port = 0
        >>> serverthread = pydoc._start_server(my_url_handler, port)

        Check that the server is really started.  If it is, open browser
        and get first page.  Use serverthread.url as the starting page.

        >>> if serverthread.serving:
        ...    import webbrowser

        The next two lines are commented out so a browser doesn't open if
        doctest is run on this module.

        #...    webbrowser.open(serverthread.url)
        #True

        Let the server do its thing. We just need to monitor its status.
        Use time.sleep so the loop doesn't hog the CPU.

        >>> starttime = time.monotonic()
        >>> timeout = 1                    #seconds

        This is a short timeout for testing purposes.

        >>> while serverthread.serving:
        ...     time.sleep(.01)
        ...     if serverthread.serving and time.monotonic() - starttime > timeout:
        ...          serverthread.stop()
        ...          break

        Print any errors that may have occurred.

        >>> print(serverthread.error)
        None
   """
    import http.server, email.message, select, threading

    class DocHandler(http.server.BaseHTTPRequestHandler):

        def do_GET(self):
            """Process a request from an HTML browser.

            The URL received is in self.path.
            Get an HTML page from self.urlhandler and send it.
            """
            if self.path.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'text/html'
            self.send_response(200)
            self.send_header('Content-Type', '%s; charset=UTF-8' % content_type)
            self.end_headers()
            self.wfile.write(self.urlhandler(self.path, content_type).encode('utf-8'))

        def log_message(self, *args):
            pass

    class DocServer(http.server.HTTPServer):

        def __init__(self, host, port, callback):
            self.host = host
            self.address = (self.host, port)
            self.callback = callback
            self.base.__init__(self, self.address, self.handler)
            self.quit = False

        def serve_until_quit(self):
            while True:
                if not self.quit:
                    rd, wr, ex = select.select([self.socket.fileno()], [], [], 1)
                    if rd:
                        self.handle_request()

            self.server_close()

        def server_activate(self):
            self.base.server_activate(self)
            if self.callback:
                self.callback(self)

    class ServerThread(threading.Thread):

        def __init__(self, urlhandler, host, port):
            self.urlhandler = urlhandler
            self.host = host
            self.port = int(port)
            threading.Thread.__init__(self)
            self.serving = False
            self.error = None

        def run(self):
            try:
                DocServer.base = http.server.HTTPServer
                DocServer.handler = DocHandler
                DocHandler.MessageClass = email.message.Message
                DocHandler.urlhandler = staticmethod(self.urlhandler)
                docsvr = DocServer(self.host, self.port, self.ready)
                self.docserver = docsvr
                docsvr.serve_until_quit()
            except Exception as e:
                try:
                    self.error = e
                finally:
                    e = None
                    del e

        def ready(self, server):
            self.serving = True
            self.host = server.host
            self.port = server.server_port
            self.url = 'http://%s:%d/' % (self.host, self.port)

        def stop(self):
            """Stop the server and this thread nicely"""
            self.docserver.quit = True
            self.join()
            self.docserver = None
            self.serving = False
            self.url = None

    thread = ServerThread(urlhandler, hostname, port)
    thread.start()
    while True:
        thread.error or thread.serving or time.sleep(0.01)

    return thread


def _url_handler(url, content_type='text/html'):
    """The pydoc url handler for use with the pydoc server.

    If the content_type is 'text/css', the _pydoc.css style
    sheet is read and returned if it exits.

    If the content_type is 'text/html', then the result of
    get_html_page(url) is returned.
    """

    class _HTMLDoc(HTMLDoc):

        def page(self, title, contents):
            css_path = 'pydoc_data/_pydoc.css'
            css_link = '<link rel="stylesheet" type="text/css" href="%s">' % css_path
            return '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n<html><head><title>Pydoc: %s</title>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n%s</head><body bgcolor="#f0f0f8">%s<div style="clear:both;padding-top:.5em;">%s</div>\n</body></html>' % (
             title, css_link, html_navbar(), contents)

        def filelink(self, url, path):
            return '<a href="getfile?key=%s">%s</a>' % (url, path)

    html = _HTMLDoc()

    def html_navbar():
        version = html.escape('%s [%s, %s]' % (platform.python_version(),
         platform.python_build()[0],
         platform.python_compiler()))
        return '\n            <div style=\'float:left\'>\n                Python %s<br>%s\n            </div>\n            <div style=\'float:right\'>\n                <div style=\'text-align:center\'>\n                  <a href="index.html">Module Index</a>\n                  : <a href="topics.html">Topics</a>\n                  : <a href="keywords.html">Keywords</a>\n                </div>\n                <div>\n                    <form action="get" style=\'display:inline;\'>\n                      <input type=text name=key size=15>\n                      <input type=submit value="Get">\n                    </form>&nbsp;\n                    <form action="search" style=\'display:inline;\'>\n                      <input type=text name=key size=15>\n                      <input type=submit value="Search">\n                    </form>\n                </div>\n            </div>\n            ' % (
         version, html.escape(platform.platform(terse=True)))

    def html_index():

        def bltinlink(name):
            return '<a href="%s.html">%s</a>' % (name, name)

        heading = html.heading('<big><big><strong>Index of Modules</strong></big></big>', '#ffffff', '#7799ee')
        names = [name for name in sys.builtin_module_names if name != '__main__']
        contents = html.multicolumn(names, bltinlink)
        contents = [heading,
         '<p>' + html.bigsection('Built-in Modules', '#ffffff', '#ee77aa', contents)]
        seen = {}
        for dir in sys.path:
            contents.append(html.index(dir, seen))
        else:
            contents.append('<p align=right><font color="#909090" face="helvetica,arial"><strong>pydoc</strong> by Ka-Ping Yee&lt;ping@lfw.org&gt;</font>')
            return (
             'Index of Modules', ''.join(contents))

    def html_search(key):
        search_result = []

        def callback(path, modname, desc):
            if modname[-9:] == '.__init__':
                modname = modname[:-9] + ' (package)'
            search_result.append((modname, desc and '- ' + desc))

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')

            def onerror(modname):
                pass

            ModuleScanner().run(callback, key, onerror=onerror)

        def bltinlink(name):
            return '<a href="%s.html">%s</a>' % (name, name)

        results = []
        heading = html.heading('<big><big><strong>Search Results</strong></big></big>', '#ffffff', '#7799ee')
        for name, desc in search_result:
            results.append(bltinlink(name) + desc)
        else:
            contents = heading + html.bigsection('key = %s' % key, '#ffffff', '#ee77aa', '<br>'.join(results))
            return (
             'Search Results', contents)

    def html_getfile(path):
        path = urllib.parse.unquote(path)
        with tokenize.open(path) as fp:
            lines = html.escape(fp.read())
        body = '<pre>%s</pre>' % lines
        heading = html.heading('<big><big><strong>File Listing</strong></big></big>', '#ffffff', '#7799ee')
        contents = heading + html.bigsection('File: %s' % path, '#ffffff', '#ee77aa', body)
        return (
         'getfile %s' % path, contents)

    def html_topics():

        def bltinlink(name):
            return '<a href="topic?key=%s">%s</a>' % (name, name)

        heading = html.heading('<big><big><strong>INDEX</strong></big></big>', '#ffffff', '#7799ee')
        names = sorted(Helper.topics.keys())
        contents = html.multicolumn(names, bltinlink)
        contents = heading + html.bigsection('Topics', '#ffffff', '#ee77aa', contents)
        return (
         'Topics', contents)

    def html_keywords():
        heading = html.heading('<big><big><strong>INDEX</strong></big></big>', '#ffffff', '#7799ee')
        names = sorted(Helper.keywords.keys())

        def bltinlink(name):
            return '<a href="topic?key=%s">%s</a>' % (name, name)

        contents = html.multicolumn(names, bltinlink)
        contents = heading + html.bigsection('Keywords', '#ffffff', '#ee77aa', contents)
        return (
         'Keywords', contents)

    def html_topicpage(topic):
        buf = io.StringIO()
        htmlhelp = Helper(buf, buf)
        contents, xrefs = htmlhelp._gettopic(topic)
        if topic in htmlhelp.keywords:
            title = 'KEYWORD'
        else:
            title = 'TOPIC'
        heading = html.heading('<big><big><strong>%s</strong></big></big>' % title, '#ffffff', '#7799ee')
        contents = '<pre>%s</pre>' % html.markup(contents)
        contents = html.bigsection(topic, '#ffffff', '#ee77aa', contents)
        if xrefs:
            xrefs = sorted(xrefs.split())

            def bltinlink(name):
                return '<a href="topic?key=%s">%s</a>' % (name, name)

            xrefs = html.multicolumn(xrefs, bltinlink)
            xrefs = html.section('Related help topics: ', '#ffffff', '#ee77aa', xrefs)
        return ('%s %s' % (title, topic),
         ''.join((heading, contents, xrefs)))

    def html_getobj(url):
        obj = locate(url, forceload=1)
        if obj is None:
            if url != 'None':
                raise ValueError('could not find object')
        title = describe(obj)
        content = html.document(obj, url)
        return (
         title, content)

    def html_error(url, exc):
        heading = html.heading('<big><big><strong>Error</strong></big></big>', '#ffffff', '#7799ee')
        contents = '<br>'.join((html.escape(line) for line in format_exception_only(type(exc), exc)))
        contents = heading + html.bigsection(url, '#ffffff', '#bb0000', contents)
        return (
         'Error - %s' % url, contents)

    def get_html_page(url):
        complete_url = url
        if url.endswith('.html'):
            url = url[:-5]
        try:
            if url in ('', 'index'):
                title, content = html_index()
            elif url == 'topics':
                title, content = html_topics()
            elif url == 'keywords':
                title, content = html_keywords()
            elif '=' in url:
                op, _, url = url.partition('=')
                if op == 'search?key':
                    title, content = html_search(url)
                elif op == 'getfile?key':
                    title, content = html_getfile(url)
                elif op == 'topic?key':
                    try:
                        title, content = html_topicpage(url)
                    except ValueError:
                        title, content = html_getobj(url)

                elif op == 'get?key':
                    if url in ('', 'index'):
                        title, content = html_index()
                    else:
                        pass
                    try:
                        title, content = html_getobj(url)
                    except ValueError:
                        title, content = html_topicpage(url)

                else:
                    raise ValueError('bad pydoc url')
            else:
                title, content = html_getobj(url)
        except Exception as exc:
            try:
                title, content = html_error(complete_url, exc)
            finally:
                exc = None
                del exc

        else:
            return html.page(title, content)

    if url.startswith('/'):
        url = url[1:]
    if content_type == 'text/css':
        path_here = os.path.dirname(os.path.realpath(__file__))
        css_path = os.path.join(path_here, url)
        with open(css_path) as fp:
            return ''.join(fp.readlines())
    elif content_type == 'text/html':
        return get_html_page(url)
    raise TypeError('unknown content type %r for url %s' % (content_type, url))


def browse(port=0, *, open_browser=True, hostname='localhost'):
    """Start the enhanced pydoc Web server and open a Web browser.

    Use port '0' to start the server on an arbitrary port.
    Set open_browser to False to suppress opening a browser.
    """
    import webbrowser
    serverthread = _start_server(_url_handler, hostname, port)
    if serverthread.error:
        print(serverthread.error)
        return
    if serverthread.serving:
        server_help_msg = 'Server commands: [b]rowser, [q]uit'
        if open_browser:
            webbrowser.open(serverthread.url)
        try:
            try:
                print('Server ready at', serverthread.url)
                print(server_help_msg)
                while True:
                    while True:
                        if serverthread.serving:
                            cmd = input('server> ')
                            cmd = cmd.lower()
                            if cmd == 'q':
                                pass

                    if cmd == 'b':
                        webbrowser.open(serverthread.url)
                    else:
                        print(server_help_msg)

            except (KeyboardInterrupt, EOFError):
                print()

        finally:
            if serverthread.serving:
                serverthread.stop()
                print('Server stopped')


def ispath(x):
    return isinstance(x, str) and x.find(os.sep) >= 0


def _get_revised_path(given_path, argv0):
    """Ensures current directory is on returned path, and argv0 directory is not

    Exception: argv0 dir is left alone if it's also pydoc's directory.

    Returns a new path entry list, or None if no adjustment is needed.
    """
    if not '' in given_path:
        if os.curdir in given_path or (os.getcwd() in given_path):
            return
        stdlib_dir = os.path.dirname(__file__)
        script_dir = os.path.dirname(argv0)
        revised_path = given_path.copy()
        if script_dir in given_path:
            if not os.path.samefile(script_dir, stdlib_dir):
                revised_path.remove(script_dir)
        revised_path.insert(0, os.getcwd())
        return revised_path


def _adjust_cli_sys_path():
    """Ensures current directory is on sys.path, and __main__ directory is not.

    Exception: __main__ dir is left alone if it's also pydoc's directory.
    """
    revised_path = _get_revised_path(sys.path, sys.argv[0])
    if revised_path is not None:
        sys.path[:] = revised_path


def cli--- This code section failed: ---

 L.2678         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              getopt
                6  STORE_FAST               'getopt'

 L.2679         8  LOAD_BUILD_CLASS 
               10  LOAD_CODE                <code_object BadUsage>
               12  LOAD_STR                 'BadUsage'
               14  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               16  LOAD_STR                 'BadUsage'
               18  LOAD_GLOBAL              Exception
               20  CALL_FUNCTION_3       3  ''
               22  STORE_FAST               'BadUsage'

 L.2681        24  LOAD_GLOBAL              _adjust_cli_sys_path
               26  CALL_FUNCTION_0       0  ''
               28  POP_TOP          

 L.2683     30_32  SETUP_FINALLY       408  'to 408'

 L.2684        34  LOAD_FAST                'getopt'
               36  LOAD_METHOD              getopt
               38  LOAD_GLOBAL              sys
               40  LOAD_ATTR                argv
               42  LOAD_CONST               1
               44  LOAD_CONST               None
               46  BUILD_SLICE_2         2 
               48  BINARY_SUBSCR    
               50  LOAD_STR                 'bk:n:p:w'
               52  CALL_METHOD_2         2  ''
               54  UNPACK_SEQUENCE_2     2 
               56  STORE_FAST               'opts'
               58  STORE_FAST               'args'

 L.2685        60  LOAD_CONST               False
               62  STORE_FAST               'writing'

 L.2686        64  LOAD_CONST               False
               66  STORE_FAST               'start_server'

 L.2687        68  LOAD_CONST               False
               70  STORE_FAST               'open_browser'

 L.2688        72  LOAD_CONST               0
               74  STORE_FAST               'port'

 L.2689        76  LOAD_STR                 'localhost'
               78  STORE_FAST               'hostname'

 L.2690        80  LOAD_FAST                'opts'
               82  GET_ITER         
             84_0  COME_FROM           176  '176'
             84_1  COME_FROM           166  '166'
               84  FOR_ITER            178  'to 178'
               86  UNPACK_SEQUENCE_2     2 
               88  STORE_FAST               'opt'
               90  STORE_FAST               'val'

 L.2691        92  LOAD_FAST                'opt'
               94  LOAD_STR                 '-b'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   108  'to 108'

 L.2692       100  LOAD_CONST               True
              102  STORE_FAST               'start_server'

 L.2693       104  LOAD_CONST               True
              106  STORE_FAST               'open_browser'
            108_0  COME_FROM            98  '98'

 L.2694       108  LOAD_FAST                'opt'
              110  LOAD_STR                 '-k'
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   132  'to 132'

 L.2695       116  LOAD_GLOBAL              apropos
              118  LOAD_FAST                'val'
              120  CALL_FUNCTION_1       1  ''
              122  POP_TOP          

 L.2696       124  POP_TOP          
              126  POP_BLOCK        
              128  LOAD_CONST               None
              130  RETURN_VALUE     
            132_0  COME_FROM           114  '114'

 L.2697       132  LOAD_FAST                'opt'
              134  LOAD_STR                 '-p'
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   148  'to 148'

 L.2698       140  LOAD_CONST               True
              142  STORE_FAST               'start_server'

 L.2699       144  LOAD_FAST                'val'
              146  STORE_FAST               'port'
            148_0  COME_FROM           138  '138'

 L.2700       148  LOAD_FAST                'opt'
              150  LOAD_STR                 '-w'
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   160  'to 160'

 L.2701       156  LOAD_CONST               True
              158  STORE_FAST               'writing'
            160_0  COME_FROM           154  '154'

 L.2702       160  LOAD_FAST                'opt'
              162  LOAD_STR                 '-n'
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE_BACK    84  'to 84'

 L.2703       168  LOAD_CONST               True
              170  STORE_FAST               'start_server'

 L.2704       172  LOAD_FAST                'val'
              174  STORE_FAST               'hostname'
              176  JUMP_BACK            84  'to 84'
            178_0  COME_FROM            84  '84'

 L.2706       178  LOAD_FAST                'start_server'
              180  POP_JUMP_IF_FALSE   202  'to 202'

 L.2707       182  LOAD_GLOBAL              browse
              184  LOAD_FAST                'port'
              186  LOAD_FAST                'hostname'
              188  LOAD_FAST                'open_browser'
              190  LOAD_CONST               ('hostname', 'open_browser')
              192  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              194  POP_TOP          

 L.2708       196  POP_BLOCK        
              198  LOAD_CONST               None
              200  RETURN_VALUE     
            202_0  COME_FROM           180  '180'

 L.2710       202  LOAD_FAST                'args'
              204  POP_JUMP_IF_TRUE    210  'to 210'

 L.2710       206  LOAD_FAST                'BadUsage'
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           204  '204'

 L.2711       210  LOAD_FAST                'args'
              212  GET_ITER         
            214_0  COME_FROM           402  '402'
            214_1  COME_FROM           398  '398'
            214_2  COME_FROM           356  '356'
              214  FOR_ITER            404  'to 404'
              216  STORE_FAST               'arg'

 L.2712       218  LOAD_GLOBAL              ispath
              220  LOAD_FAST                'arg'
              222  CALL_FUNCTION_1       1  ''
          224_226  POP_JUMP_IF_FALSE   260  'to 260'
              228  LOAD_GLOBAL              os
              230  LOAD_ATTR                path
              232  LOAD_METHOD              exists
              234  LOAD_FAST                'arg'
              236  CALL_METHOD_1         1  ''
          238_240  POP_JUMP_IF_TRUE    260  'to 260'

 L.2713       242  LOAD_GLOBAL              print
              244  LOAD_STR                 'file %r does not exist'
              246  LOAD_FAST                'arg'
              248  BINARY_MODULO    
              250  CALL_FUNCTION_1       1  ''
              252  POP_TOP          

 L.2714       254  POP_TOP          
          256_258  BREAK_LOOP          404  'to 404'
            260_0  COME_FROM           238  '238'
            260_1  COME_FROM           224  '224'

 L.2715       260  SETUP_FINALLY       358  'to 358'

 L.2716       262  LOAD_GLOBAL              ispath
              264  LOAD_FAST                'arg'
              266  CALL_FUNCTION_1       1  ''
          268_270  POP_JUMP_IF_FALSE   294  'to 294'
              272  LOAD_GLOBAL              os
              274  LOAD_ATTR                path
              276  LOAD_METHOD              isfile
              278  LOAD_FAST                'arg'
              280  CALL_METHOD_1         1  ''
          282_284  POP_JUMP_IF_FALSE   294  'to 294'

 L.2717       286  LOAD_GLOBAL              importfile
              288  LOAD_FAST                'arg'
              290  CALL_FUNCTION_1       1  ''
              292  STORE_FAST               'arg'
            294_0  COME_FROM           282  '282'
            294_1  COME_FROM           268  '268'

 L.2718       294  LOAD_FAST                'writing'
          296_298  POP_JUMP_IF_FALSE   344  'to 344'

 L.2719       300  LOAD_GLOBAL              ispath
              302  LOAD_FAST                'arg'
              304  CALL_FUNCTION_1       1  ''
          306_308  POP_JUMP_IF_FALSE   334  'to 334'
              310  LOAD_GLOBAL              os
              312  LOAD_ATTR                path
              314  LOAD_METHOD              isdir
              316  LOAD_FAST                'arg'
              318  CALL_METHOD_1         1  ''
          320_322  POP_JUMP_IF_FALSE   334  'to 334'

 L.2720       324  LOAD_GLOBAL              writedocs
              326  LOAD_FAST                'arg'
              328  CALL_FUNCTION_1       1  ''
              330  POP_TOP          
              332  JUMP_FORWARD        342  'to 342'
            334_0  COME_FROM           320  '320'
            334_1  COME_FROM           306  '306'

 L.2722       334  LOAD_GLOBAL              writedoc
              336  LOAD_FAST                'arg'
              338  CALL_FUNCTION_1       1  ''
              340  POP_TOP          
            342_0  COME_FROM           332  '332'
              342  JUMP_FORWARD        354  'to 354'
            344_0  COME_FROM           296  '296'

 L.2724       344  LOAD_GLOBAL              help
              346  LOAD_METHOD              help
              348  LOAD_FAST                'arg'
              350  CALL_METHOD_1         1  ''
              352  POP_TOP          
            354_0  COME_FROM           342  '342'
              354  POP_BLOCK        
              356  JUMP_BACK           214  'to 214'
            358_0  COME_FROM_FINALLY   260  '260'

 L.2725       358  DUP_TOP          
              360  LOAD_GLOBAL              ErrorDuringImport
              362  COMPARE_OP               exception-match
          364_366  POP_JUMP_IF_FALSE   400  'to 400'
              368  POP_TOP          
              370  STORE_FAST               'value'
              372  POP_TOP          
              374  SETUP_FINALLY       388  'to 388'

 L.2726       376  LOAD_GLOBAL              print
              378  LOAD_FAST                'value'
              380  CALL_FUNCTION_1       1  ''
              382  POP_TOP          
              384  POP_BLOCK        
              386  BEGIN_FINALLY    
            388_0  COME_FROM_FINALLY   374  '374'
              388  LOAD_CONST               None
              390  STORE_FAST               'value'
              392  DELETE_FAST              'value'
              394  END_FINALLY      
              396  POP_EXCEPT       
              398  JUMP_BACK           214  'to 214'
            400_0  COME_FROM           364  '364'
              400  END_FINALLY      
              402  JUMP_BACK           214  'to 214'
            404_0  COME_FROM           256  '256'
            404_1  COME_FROM           214  '214'
              404  POP_BLOCK        
              406  JUMP_FORWARD        486  'to 486'
            408_0  COME_FROM_FINALLY    30  '30'

 L.2728       408  DUP_TOP          
              410  LOAD_FAST                'getopt'
              412  LOAD_ATTR                error
              414  LOAD_FAST                'BadUsage'
              416  BUILD_TUPLE_2         2 
              418  COMPARE_OP               exception-match
          420_422  POP_JUMP_IF_FALSE   484  'to 484'
              424  POP_TOP          
              426  POP_TOP          
              428  POP_TOP          

 L.2729       430  LOAD_GLOBAL              os
              432  LOAD_ATTR                path
              434  LOAD_METHOD              splitext
              436  LOAD_GLOBAL              os
              438  LOAD_ATTR                path
              440  LOAD_METHOD              basename
              442  LOAD_GLOBAL              sys
              444  LOAD_ATTR                argv
              446  LOAD_CONST               0
              448  BINARY_SUBSCR    
              450  CALL_METHOD_1         1  ''
              452  CALL_METHOD_1         1  ''
              454  LOAD_CONST               0
              456  BINARY_SUBSCR    
              458  STORE_FAST               'cmd'

 L.2730       460  LOAD_GLOBAL              print
              462  LOAD_STR                 "pydoc - the Python documentation tool\n\n{cmd} <name> ...\n    Show text documentation on something.  <name> may be the name of a\n    Python keyword, topic, function, module, or package, or a dotted\n    reference to a class or function within a module or module in a\n    package.  If <name> contains a '{sep}', it is used as the path to a\n    Python source file to document. If name is 'keywords', 'topics',\n    or 'modules', a listing of these things is displayed.\n\n{cmd} -k <keyword>\n    Search for a keyword in the synopsis lines of all available modules.\n\n{cmd} -n <hostname>\n    Start an HTTP server with the given hostname (default: localhost).\n\n{cmd} -p <port>\n    Start an HTTP server on the given port on the local machine.  Port\n    number 0 can be used to get an arbitrary unused port.\n\n{cmd} -b\n    Start an HTTP server on an arbitrary unused port and open a Web browser\n    to interactively browse documentation.  This option can be used in\n    combination with -n and/or -p.\n\n{cmd} -w <name> ...\n    Write out the HTML documentation for a module to a file in the current\n    directory.  If <name> contains a '{sep}', it is treated as a filename; if\n    it names a directory, documentation is written for all the contents.\n"
              464  LOAD_ATTR                format

 L.2759       466  LOAD_FAST                'cmd'

 L.2759       468  LOAD_GLOBAL              os
              470  LOAD_ATTR                sep

 L.2730       472  LOAD_CONST               ('cmd', 'sep')
              474  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              476  CALL_FUNCTION_1       1  ''
              478  POP_TOP          
              480  POP_EXCEPT       
              482  JUMP_FORWARD        486  'to 486'
            484_0  COME_FROM           420  '420'
              484  END_FINALLY      
            486_0  COME_FROM           482  '482'
            486_1  COME_FROM           406  '406'

Parse error at or near `POP_BLOCK' instruction at offset 126


if __name__ == '__main__':
    cli()