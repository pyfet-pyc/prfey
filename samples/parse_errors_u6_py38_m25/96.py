# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: doctest.py
"""Module doctest -- a framework for running examples in docstrings.

In simplest use, end each module M to be tested with:

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

Then running the module as a script will cause the examples in the
docstrings to get executed and verified:

python M.py

This won't display anything unless an example fails, in which case the
failing example(s) and the cause(s) of the failure(s) are printed to stdout
(why not stderr? because stderr is a lame hack <0.2 wink>), and the final
line of output is "Test failed.".

Run it with the -v switch instead:

python M.py -v

and a detailed report of all examples tried is printed to stdout, along
with assorted summaries at the end.

You can force verbose mode by passing "verbose=True" to testmod, or prohibit
it by passing "verbose=False".  In either of those cases, sys.argv is not
examined by testmod.

There are a variety of other ways to run doctests, including integration
with the unittest framework, and support for running non-Python text
files containing doctests.  There are also many ways to override parts
of doctest's default behaviors.  See the Library Reference Manual for
details.
"""
__docformat__ = 'reStructuredText en'
__all__ = [
 'register_optionflag',
 'DONT_ACCEPT_TRUE_FOR_1',
 'DONT_ACCEPT_BLANKLINE',
 'NORMALIZE_WHITESPACE',
 'ELLIPSIS',
 'SKIP',
 'IGNORE_EXCEPTION_DETAIL',
 'COMPARISON_FLAGS',
 'REPORT_UDIFF',
 'REPORT_CDIFF',
 'REPORT_NDIFF',
 'REPORT_ONLY_FIRST_FAILURE',
 'REPORTING_FLAGS',
 'FAIL_FAST',
 'Example',
 'DocTest',
 'DocTestParser',
 'DocTestFinder',
 'DocTestRunner',
 'OutputChecker',
 'DocTestFailure',
 'UnexpectedException',
 'DebugRunner',
 'testmod',
 'testfile',
 'run_docstring_examples',
 'DocTestSuite',
 'DocFileSuite',
 'set_unittest_reportflags',
 'script_from_examples',
 'testsource',
 'debug_src',
 'debug']
import __future__, difflib, inspect, linecache, os, pdb, re, sys, traceback, unittest
from io import StringIO
from collections import namedtuple
TestResults = namedtuple('TestResults', 'failed attempted')
OPTIONFLAGS_BY_NAME = {}

def register_optionflag(name):
    return OPTIONFLAGS_BY_NAME.setdefault(name, 1 << len(OPTIONFLAGS_BY_NAME))


DONT_ACCEPT_TRUE_FOR_1 = register_optionflag('DONT_ACCEPT_TRUE_FOR_1')
DONT_ACCEPT_BLANKLINE = register_optionflag('DONT_ACCEPT_BLANKLINE')
NORMALIZE_WHITESPACE = register_optionflag('NORMALIZE_WHITESPACE')
ELLIPSIS = register_optionflag('ELLIPSIS')
SKIP = register_optionflag('SKIP')
IGNORE_EXCEPTION_DETAIL = register_optionflag('IGNORE_EXCEPTION_DETAIL')
COMPARISON_FLAGS = DONT_ACCEPT_TRUE_FOR_1 | DONT_ACCEPT_BLANKLINE | NORMALIZE_WHITESPACE | ELLIPSIS | SKIP | IGNORE_EXCEPTION_DETAIL
REPORT_UDIFF = register_optionflag('REPORT_UDIFF')
REPORT_CDIFF = register_optionflag('REPORT_CDIFF')
REPORT_NDIFF = register_optionflag('REPORT_NDIFF')
REPORT_ONLY_FIRST_FAILURE = register_optionflag('REPORT_ONLY_FIRST_FAILURE')
FAIL_FAST = register_optionflag('FAIL_FAST')
REPORTING_FLAGS = REPORT_UDIFF | REPORT_CDIFF | REPORT_NDIFF | REPORT_ONLY_FIRST_FAILURE | FAIL_FAST
BLANKLINE_MARKER = '<BLANKLINE>'
ELLIPSIS_MARKER = '...'

def _extract_future_flags(globs):
    """
    Return the compiler-flags associated with the future features that
    have been imported into the given namespace (globs).
    """
    flags = 0
    for fname in __future__.all_feature_names:
        feature = globs.get(fname, None)
        if feature is getattr(__future__, fname):
            flags |= feature.compiler_flag
        return flags


def _normalize_module(module, depth=2):
    """
    Return the module specified by `module`.  In particular:
      - If `module` is a module, then return module.
      - If `module` is a string, then import and return the
        module with that name.
      - If `module` is None, then return the calling module.
        The calling module is assumed to be the module of
        the stack frame at the given depth in the call stack.
    """
    if inspect.ismodule(module):
        return module
    if isinstance(module, str):
        return __import__(module, globals(), locals(), ['*'])
    if module is None:
        return sys.modules[sys._getframe(depth).f_globals['__name__']]
    raise TypeError('Expected a module, string, or None')


def _newline_convert(data):
    for newline in ('\r\n', '\r'):
        data = data.replace(newline, '\n')
    else:
        return data


def _load_testfile--- This code section failed: ---

 L. 222         0  LOAD_FAST                'module_relative'
                2  POP_JUMP_IF_FALSE    86  'to 86'

 L. 223         4  LOAD_GLOBAL              _normalize_module
                6  LOAD_FAST                'package'
                8  LOAD_CONST               3
               10  CALL_FUNCTION_2       2  ''
               12  STORE_FAST               'package'

 L. 224        14  LOAD_GLOBAL              _module_relative_path
               16  LOAD_FAST                'package'
               18  LOAD_FAST                'filename'
               20  CALL_FUNCTION_2       2  ''
               22  STORE_FAST               'filename'

 L. 225        24  LOAD_GLOBAL              getattr
               26  LOAD_FAST                'package'
               28  LOAD_STR                 '__loader__'
               30  LOAD_CONST               None
               32  CALL_FUNCTION_3       3  ''
               34  LOAD_CONST               None
               36  COMPARE_OP               is-not
               38  POP_JUMP_IF_FALSE    86  'to 86'

 L. 226        40  LOAD_GLOBAL              hasattr
               42  LOAD_FAST                'package'
               44  LOAD_ATTR                __loader__
               46  LOAD_STR                 'get_data'
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_FALSE    86  'to 86'

 L. 227        52  LOAD_FAST                'package'
               54  LOAD_ATTR                __loader__
               56  LOAD_METHOD              get_data
               58  LOAD_FAST                'filename'
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'file_contents'

 L. 228        64  LOAD_FAST                'file_contents'
               66  LOAD_METHOD              decode
               68  LOAD_FAST                'encoding'
               70  CALL_METHOD_1         1  ''
               72  STORE_FAST               'file_contents'

 L. 231        74  LOAD_GLOBAL              _newline_convert
               76  LOAD_FAST                'file_contents'
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_FAST                'filename'
               82  BUILD_TUPLE_2         2 
               84  RETURN_VALUE     
             86_0  COME_FROM            50  '50'
             86_1  COME_FROM            38  '38'
             86_2  COME_FROM             2  '2'

 L. 232        86  LOAD_GLOBAL              open
               88  LOAD_FAST                'filename'
               90  LOAD_FAST                'encoding'
               92  LOAD_CONST               ('encoding',)
               94  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               96  SETUP_WITH          124  'to 124'
               98  STORE_FAST               'f'

 L. 233       100  LOAD_FAST                'f'
              102  LOAD_METHOD              read
              104  CALL_METHOD_0         0  ''
              106  LOAD_FAST                'filename'
              108  BUILD_TUPLE_2         2 
              110  POP_BLOCK        
              112  ROT_TWO          
              114  BEGIN_FINALLY    
              116  WITH_CLEANUP_START
              118  WITH_CLEANUP_FINISH
              120  POP_FINALLY           0  ''
              122  RETURN_VALUE     
            124_0  COME_FROM_WITH       96  '96'
              124  WITH_CLEANUP_START
              126  WITH_CLEANUP_FINISH
              128  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 112


def _indent(s, indent=4):
    """
    Add the given number of space characters to the beginning of
    every non-blank line in `s`, and return the result.
    """
    return re.sub('(?m)^(?!$)', indent * ' ', s)


def _exception_traceback(exc_info):
    """
    Return a string containing a traceback message for the given
    exc_info tuple (as returned by sys.exc_info()).
    """
    excout = StringIO()
    exc_type, exc_val, exc_tb = exc_info
    traceback.print_exception(exc_type, exc_val, exc_tb, file=excout)
    return excout.getvalue


class _SpoofOut(StringIO):

    def getvalue(self):
        result = StringIO.getvalue(self)
        if result:
            if not result.endswith('\n'):
                result += '\n'
        return result

    def truncate(self, size=None):
        self.seek(size)
        StringIO.truncate(self)


def _ellipsis_match(want, got):
    """
    Essentially the only subtle case:
    >>> _ellipsis_match('aa...aa', 'aaa')
    False
    """
    if ELLIPSIS_MARKER not in want:
        return want == got
    ws = want.split(ELLIPSIS_MARKER)
    assert len(ws) >= 2
    startpos, endpos = 0, len(got)
    w = ws[0]
    if w:
        if got.startswith(w):
            startpos = len(w)
            del ws[0]
        else:
            return False
    w = ws[(-1)]
    if w:
        if got.endswith(w):
            endpos -= len(w)
            del ws[-1]
        else:
            return False
    if startpos > endpos:
        return False
    for w in ws:
        startpos = got.find(w, startpos, endpos)
        if startpos < 0:
            return False
            startpos += len(w)
    else:
        return True


def _comment_line(line):
    """Return a commented form of the given line"""
    line = line.rstrip
    if line:
        return '# ' + line
    return '#'


def _strip_exception_details(msg):
    start, end = 0, len(msg)
    i = msg.find('\n')
    if i >= 0:
        end = i
    i = msg.find(':', 0, end)
    if i >= 0:
        end = i
    i = msg.rfind('.', 0, end)
    if i >= 0:
        start = i + 1
    return msg[start:end]


class _OutputRedirectingPdb(pdb.Pdb):
    __doc__ = '\n    A specialized version of the python debugger that redirects stdout\n    to a given stream when interacting with the user.  Stdout is *not*\n    redirected when traced code is executed.\n    '

    def __init__(self, out):
        self._OutputRedirectingPdb__out = out
        self._OutputRedirectingPdb__debugger_used = False
        pdb.Pdb.__init__(self, stdout=out, nosigint=True)
        self.use_rawinput = 1

    def set_trace(self, frame=None):
        self._OutputRedirectingPdb__debugger_used = True
        if frame is None:
            frame = sys._getframe.f_back
        pdb.Pdb.set_trace(self, frame)

    def set_continue(self):
        if self._OutputRedirectingPdb__debugger_used:
            pdb.Pdb.set_continue(self)

    def trace_dispatch(self, *args):
        save_stdout = sys.stdout
        sys.stdout = self._OutputRedirectingPdb__out
        try:
            return (pdb.Pdb.trace_dispatch)(self, *args)
        finally:
            sys.stdout = save_stdout


def _module_relative_path(module, test_path):
    if not inspect.ismodule(module):
        raise TypeError('Expected a module: %r' % module)
    elif test_path.startswith('/'):
        raise ValueError('Module-relative files may not have absolute paths')
    else:
        test_path = (os.path.join)(*test_path.split('/'))
        if hasattr(module, '__file__'):
            basedir = os.path.split(module.__file__)[0]
        else:
            if module.__name__ == '__main__':
                if len(sys.argv) > 0 and sys.argv[0] != '':
                    basedir = os.path.split(sys.argv[0])[0]
                else:
                    basedir = os.curdir
            elif hasattr(module, '__path__'):
                for directory in module.__path__:
                    fullpath = os.path.join(directory, test_path)
                    if os.path.exists(fullpath):
                        return fullpath

        raise ValueError("Can't resolve paths relative to the module %r (it has no __file__)" % module.__name__)
    return os.path.join(basedir, test_path)


class Example:
    __doc__ = "\n    A single doctest example, consisting of source code and expected\n    output.  `Example` defines the following attributes:\n\n      - source: A single Python statement, always ending with a newline.\n        The constructor adds a newline if needed.\n\n      - want: The expected output from running the source code (either\n        from stdout, or a traceback in case of exception).  `want` ends\n        with a newline unless it's empty, in which case it's an empty\n        string.  The constructor adds a newline if needed.\n\n      - exc_msg: The exception message generated by the example, if\n        the example is expected to generate an exception; or `None` if\n        it is not expected to generate an exception.  This exception\n        message is compared against the return value of\n        `traceback.format_exception_only()`.  `exc_msg` ends with a\n        newline unless it's `None`.  The constructor adds a newline\n        if needed.\n\n      - lineno: The line number within the DocTest string containing\n        this Example where the Example begins.  This line number is\n        zero-based, with respect to the beginning of the DocTest.\n\n      - indent: The example's indentation in the DocTest string.\n        I.e., the number of space characters that precede the\n        example's first prompt.\n\n      - options: A dictionary mapping from option flags to True or\n        False, which is used to override default options for this\n        example.  Any option flags not contained in this dictionary\n        are left at their default value (as specified by the\n        DocTestRunner's optionflags).  By default, no options are set.\n    "

    def __init__(self, source, want, exc_msg=None, lineno=0, indent=0, options=None):
        if not source.endswith('\n'):
            source += '\n'
        else:
            if want:
                if not want.endswith('\n'):
                    want += '\n'
            if exc_msg is not None:
                exc_msg.endswith('\n') or exc_msg += '\n'
        self.source = source
        self.want = want
        self.lineno = lineno
        self.indent = indent
        if options is None:
            options = {}
        self.options = options
        self.exc_msg = exc_msg

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.source == other.source and self.want == other.want and self.lineno == other.lineno and self.indent == other.indent and self.options == other.options and self.exc_msg == other.exc_msg

    def __hash__(self):
        return hash((self.source, self.want, self.lineno, self.indent,
         self.exc_msg))


class DocTest:
    __doc__ = '\n    A collection of doctest examples that should be run in a single\n    namespace.  Each `DocTest` defines the following attributes:\n\n      - examples: the list of examples.\n\n      - globs: The namespace (aka globals) that the examples should\n        be run in.\n\n      - name: A name identifying the DocTest (typically, the name of\n        the object whose docstring this DocTest was extracted from).\n\n      - filename: The name of the file that this DocTest was extracted\n        from, or `None` if the filename is unknown.\n\n      - lineno: The line number within filename where this DocTest\n        begins, or `None` if the line number is unavailable.  This\n        line number is zero-based, with respect to the beginning of\n        the file.\n\n      - docstring: The string that the examples were extracted from,\n        or `None` if the string is unavailable.\n    '

    def __init__(self, examples, globs, name, filename, lineno, docstring):
        """
        Create a new DocTest containing the given examples.  The
        DocTest's globals are initialized with a copy of `globs`.
        """
        if isinstance(examples, str):
            raise AssertionError('DocTest no longer accepts str; use DocTestParser instead')
        self.examples = examples
        self.docstring = docstring
        self.globs = globs.copy
        self.name = name
        self.filename = filename
        self.lineno = lineno

    def __repr__(self):
        if len(self.examples) == 0:
            examples = 'no examples'
        else:
            if len(self.examples) == 1:
                examples = '1 example'
            else:
                examples = '%d examples' % len(self.examples)
        return '<%s %s from %s:%s (%s)>' % (
         self.__class__.__name__,
         self.name, self.filename, self.lineno, examples)

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.examples == other.examples and self.docstring == other.docstring and self.globs == other.globs and self.name == other.name and self.filename == other.filename and self.lineno == other.lineno

    def __hash__(self):
        return hash((self.docstring, self.name, self.filename, self.lineno))

    def __lt__(self, other):
        if not isinstance(other, DocTest):
            return NotImplemented
        return (
         self.name, self.filename, self.lineno, id(self)) < (
         other.name, other.filename, other.lineno, id(other))


class DocTestParser:
    __doc__ = '\n    A class used to parse strings containing doctest examples.\n    '
    _EXAMPLE_RE = re.compile('\n        # Source consists of a PS1 line followed by zero or more PS2 lines.\n        (?P<source>\n            (?:^(?P<indent> [ ]*) >>>    .*)    # PS1 line\n            (?:\\n           [ ]*  \\.\\.\\. .*)*)  # PS2 lines\n        \\n?\n        # Want consists of any non-blank lines that do not start with PS1.\n        (?P<want> (?:(?![ ]*$)    # Not a blank line\n                     (?![ ]*>>>)  # Not a line starting with PS1\n                     .+$\\n?       # But any other line\n                  )*)\n        ', re.MULTILINE | re.VERBOSE)
    _EXCEPTION_RE = re.compile("\n        # Grab the traceback header.  Different versions of Python have\n        # said different things on the first traceback line.\n        ^(?P<hdr> Traceback\\ \\(\n            (?: most\\ recent\\ call\\ last\n            |   innermost\\ last\n            ) \\) :\n        )\n        \\s* $                # toss trailing whitespace on the header.\n        (?P<stack> .*?)      # don't blink: absorb stuff until...\n        ^ (?P<msg> \\w+ .*)   #     a line *starts* with alphanum.\n        ", re.VERBOSE | re.MULTILINE | re.DOTALL)
    _IS_BLANK_OR_COMMENT = re.compile('^[ ]*(#.*)?$').match

    def parse(self, string, name='<string>'):
        """
        Divide the given string into examples and intervening text,
        and return them as a list of alternating Examples and strings.
        Line numbers for the Examples are 0-based.  The optional
        argument `name` is a name identifying this string, and is only
        used for error messages.
        """
        string = string.expandtabs
        min_indent = self._min_indent(string)
        if min_indent > 0:
            string = '\n'.join([l[min_indent:] for l in string.split('\n')])
        output = []
        charno, lineno = (0, 0)
        for m in self._EXAMPLE_RE.finditer(string):
            output.append(string[charno:m.start])
            lineno += string.count('\n', charno, m.start)
            source, options, want, exc_msg = self._parse_example(m, name, lineno)
            if not self._IS_BLANK_OR_COMMENT(source):
                output.append(Example(source, want, exc_msg, lineno=lineno,
                  indent=(min_indent + len(m.group('indent'))),
                  options=options))
            lineno += string.count('\n', m.start, m.end)
            charno = m.end
        else:
            output.append(string[charno:])
            return output

    def get_doctest(self, string, globs, name, filename, lineno):
        """
        Extract all doctest examples from the given string, and
        collect them into a `DocTest` object.

        `globs`, `name`, `filename`, and `lineno` are attributes for
        the new `DocTest` object.  See the documentation for `DocTest`
        for more information.
        """
        return DocTest(self.get_examples(string, name), globs, name, filename, lineno, string)

    def get_examples(self, string, name='<string>'):
        """
        Extract all doctest examples from the given string, and return
        them as a list of `Example` objects.  Line numbers are
        0-based, because it's most common in doctests that nothing
        interesting appears on the same line as opening triple-quote,
        and so the first interesting line is called "line 1" then.

        The optional argument `name` is a name identifying this
        string, and is only used for error messages.
        """
        return [x for x in self.parse(string, name) if isinstance(x, Example)]

    def _parse_example(self, m, name, lineno):
        """
        Given a regular expression match from `_EXAMPLE_RE` (`m`),
        return a pair `(source, want)`, where `source` is the matched
        example's source code (with prompts and indentation stripped);
        and `want` is the example's expected output (with indentation
        stripped).

        `name` is the string's name, and `lineno` is the line number
        where the example starts; both are used for error messages.
        """
        indent = len(m.group('indent'))
        source_lines = m.group('source').split('\n')
        self._check_prompt_blank(source_lines, indent, name, lineno)
        self._check_prefix(source_lines[1:], ' ' * indent + '.', name, lineno)
        source = '\n'.join([sl[indent + 4:] for sl in source_lines])
        want = m.group('want')
        want_lines = want.split('\n')
        if len(want_lines) > 1:
            if re.match(' *$', want_lines[(-1)]):
                del want_lines[-1]
        else:
            self._check_prefix(want_lines, ' ' * indent, name, lineno + len(source_lines))
            want = '\n'.join([wl[indent:] for wl in want_lines])
            m = self._EXCEPTION_RE.match(want)
            if m:
                exc_msg = m.group('msg')
            else:
                exc_msg = None
        options = self._find_options(source, name, lineno)
        return (
         source, options, want, exc_msg)

    _OPTION_DIRECTIVE_RE = re.compile('#\\s*doctest:\\s*([^\\n\\\'"]*)$', re.MULTILINE)

    def _find_options(self, source, name, lineno):
        """
        Return a dictionary containing option overrides extracted from
        option directives in the given source string.

        `name` is the string's name, and `lineno` is the line number
        where the example starts; both are used for error messages.
        """
        options = {}
        for m in self._OPTION_DIRECTIVE_RE.finditer(source):
            option_strings = m.group(1).replace(',', ' ').split
            for option in option_strings:
                if not option[0] not in '+-':
                    if option[1:] not in OPTIONFLAGS_BY_NAME:
                        raise ValueError('line %r of the doctest for %s has an invalid option: %r' % (
                         lineno + 1, name, option))
                    flag = OPTIONFLAGS_BY_NAME[option[1:]]
                    options[flag] = option[0] == '+'
            else:
                if options:
                    if self._IS_BLANK_OR_COMMENT(source):
                        raise ValueError('line %r of the doctest for %s has an option directive on a line with no example: %r' % (
                         lineno, name, source))
                return options

    _INDENT_RE = re.compile('^([ ]*)(?=\\S)', re.MULTILINE)

    def _min_indent(self, s):
        """Return the minimum indentation of any non-blank line in `s`"""
        indents = [len(indent) for indent in self._INDENT_RE.findall(s)]
        if len(indents) > 0:
            return min(indents)
        return 0

    def _check_prompt_blank(self, lines, indent, name, lineno):
        """
        Given the lines of a source string (including prompts and
        leading indentation), check to make sure that every prompt is
        followed by a space character.  If any line is not followed by
        a space character, then raise ValueError.
        """
        for i, line in enumerate(lines):
            if len(line) >= indent + 4 and line[(indent + 3)] != ' ':
                raise ValueError('line %r of the docstring for %s lacks blank after %s: %r' % (
                 lineno + i + 1, name,
                 line[indent:indent + 3], line))

    def _check_prefix(self, lines, prefix, name, lineno):
        """
        Check that every line in the given list starts with the given
        prefix; if any line does not, then raise a ValueError.
        """
        for i, line in enumerate(lines):
            if line and not line.startswith(prefix):
                raise ValueError('line %r of the docstring for %s has inconsistent leading whitespace: %r' % (
                 lineno + i + 1, name, line))


class DocTestFinder:
    __doc__ = '\n    A class used to extract the DocTests that are relevant to a given\n    object, from its docstring and the docstrings of its contained\n    objects.  Doctests can currently be extracted from the following\n    object types: modules, functions, classes, methods, staticmethods,\n    classmethods, and properties.\n    '

    def __init__(self, verbose=False, parser=DocTestParser(), recurse=True, exclude_empty=True):
        """
        Create a new doctest finder.

        The optional argument `parser` specifies a class or
        function that should be used to create new DocTest objects (or
        objects that implement the same interface as DocTest).  The
        signature for this factory function should match the signature
        of the DocTest constructor.

        If the optional argument `recurse` is false, then `find` will
        only examine the given object, and not any contained objects.

        If the optional argument `exclude_empty` is false, then `find`
        will include tests for objects with empty docstrings.
        """
        self._parser = parser
        self._verbose = verbose
        self._recurse = recurse
        self._exclude_empty = exclude_empty

    def find(self, obj, name=None, module=None, globs=None, extraglobs=None):
        """
        Return a list of the DocTests that are defined by the given
        object's docstring, or by any of its contained objects'
        docstrings.

        The optional parameter `module` is the module that contains
        the given object.  If the module is not specified or is None, then
        the test finder will attempt to automatically determine the
        correct module.  The object's module is used:

            - As a default namespace, if `globs` is not specified.
            - To prevent the DocTestFinder from extracting DocTests
              from objects that are imported from other modules.
            - To find the name of the file containing the object.
            - To help find the line number of the object within its
              file.

        Contained objects whose module does not match `module` are ignored.

        If `module` is False, no attempt to find the module will be made.
        This is obscure, of use mostly in tests:  if `module` is False, or
        is None but cannot be found automatically, then all objects are
        considered to belong to the (non-existent) module, so all contained
        objects will (recursively) be searched for doctests.

        The globals for each DocTest is formed by combining `globs`
        and `extraglobs` (bindings in `extraglobs` override bindings
        in `globs`).  A new copy of the globals dictionary is created
        for each DocTest.  If `globs` is not specified, then it
        defaults to the module's `__dict__`, if specified, or {}
        otherwise.  If `extraglobs` is not specified, then it defaults
        to {}.

        """
        if name is None:
            name = getattr(obj, '__name__', None)
            if name is None:
                raise ValueError("DocTestFinder.find: name must be given when obj.__name__ doesn't exist: %r" % (
                 type(obj),))
            elif module is False:
                module = None
            else:
                if module is None:
                    module = inspect.getmodule(obj)
            try:
                file = inspect.getsourcefile(obj)
            except TypeError:
                source_lines = None
            else:
                if not file:
                    file = inspect.getfile(obj)
                    if not file[0] + file[-2:] == '<]>':
                        file = None
                if file is None:
                    source_lines = None
        else:
            if module is not None:
                source_lines = linecache.getlines(file, module.__dict__)
            else:
                source_lines = linecache.getlines(file)
            if not source_lines:
                source_lines = None
            elif globs is None:
                if module is None:
                    globs = {}
                else:
                    globs = module.__dict__.copy
            else:
                globs = globs.copy
            if extraglobs is not None:
                globs.update(extraglobs)
            if '__name__' not in globs:
                globs['__name__'] = '__main__'
            tests = []
            self._find(tests, obj, name, module, source_lines, globs, {})
            tests.sort
            return tests

    def _from_module(self, module, object):
        """
        Return true if the given object is defined in the given
        module.
        """
        if module is None:
            return True
        else:
            if inspect.getmodule(object) is not None:
                return module is inspect.getmodule(object)
            elif inspect.isfunction(object):
                return module.__dict__ is object.__globals__
                if inspect.ismethoddescriptor(object):
                    if hasattr(object, '__objclass__'):
                        obj_mod = object.__objclass__.__module__
            elif hasattr(object, '__module__'):
                obj_mod = object.__module__
            else:
                return True
            return module.__name__ == obj_mod
        if inspect.isclass(object):
            return module.__name__ == object.__module__
        if hasattr(object, '__module__'):
            return module.__name__ == object.__module__
        if isinstance(object, property):
            return True
        raise ValueError('object must be a class or function')

    def _find(self, tests, obj, name, module, source_lines, globs, seen):
        """
        Find tests for the given object and any contained objects, and
        add them to `tests`.
        """
        if self._verbose:
            print('Finding tests in %s' % name)
        elif id(obj) in seen:
            return
            seen[id(obj)] = 1
            test = self._get_test(obj, name, module, globs, source_lines)
            if test is not None:
                tests.append(test)
            if inspect.ismodule(obj):
                if self._recurse:
                    for valname, val in obj.__dict__.items:
                        valname = '%s.%s' % (name, valname)
                        if inspect.isroutine(inspect.unwrap(val)) or inspect.isclass(val):
                            if self._from_module(module, val):
                                self._find(tests, val, valname, module, source_lines, globs, seen)

        else:
            if inspect.ismodule(obj):
                if self._recurse:
                    for valname, val in getattr(obj, '__test__', {}).items:
                        if not isinstance(valname, str):
                            raise ValueError('DocTestFinder.find: __test__ keys must be strings: %r' % (
                             type(valname),))
                        if not inspect.isroutine(val) or inspect.isclass(val) or inspect.ismodule(val):
                            if not isinstance(val, str):
                                raise ValueError('DocTestFinder.find: __test__ values must be strings, functions, methods, classes, or modules: %r' % (
                                 type(val),))
                            valname = '%s.__test__.%s' % (name, valname)
                            self._find(tests, val, valname, module, source_lines, globs, seen)

            if inspect.isclass(obj) and self._recurse:
                for valname, val in obj.__dict__.items:
                    if isinstance(val, staticmethod):
                        val = getattr(obj, valname)
                    if isinstance(val, classmethod):
                        val = getattr(obj, valname).__func__
                    if not inspect.isroutine(val):
                        if not inspect.isclass(val):
                            if isinstance(val, property):
                                pass

                if self._from_module(module, val):
                    valname = '%s.%s' % (name, valname)
                    self._find(tests, val, valname, module, source_lines, globs, seen)

    def _get_test(self, obj, name, module, globs, source_lines):
        """
        Return a DocTest for the given object, if it defines a docstring;
        otherwise, return None.
        """
        if isinstance(obj, str):
            docstring = obj
        else:
            try:
                if obj.__doc__ is None:
                    docstring = ''
                else:
                    docstring = obj.__doc__
                    if not isinstance(docstring, str):
                        docstring = str(docstring)
            except (TypeError, AttributeError):
                docstring = ''
            else:
                lineno = self._find_lineno(obj, source_lines)
                if self._exclude_empty:
                    if not docstring:
                        return
                elif module is None:
                    filename = None
                else:
                    filename = getattr(module, '__file__', None) or module.__name__
                    if filename[-4:] == '.pyc':
                        filename = filename[:-1]
                return self._parser.get_doctest(docstring, globs, name, filename, lineno)

    def _find_lineno(self, obj, source_lines):
        """
        Return a line number of the given object's docstring.  Note:
        this method assumes that the object has a docstring.
        """
        lineno = None
        if inspect.ismodule(obj):
            lineno = 0
        if inspect.isclass(obj):
            if source_lines is None:
                return
            pat = re.compile('^\\s*class\\s*%s\\b' % getattr(obj, '__name__', '-'))
            for i, line in enumerate(source_lines):
                if pat.match(line):
                    lineno = i
                    break

        if inspect.ismethod(obj):
            obj = obj.__func__
        if inspect.isfunction(obj):
            obj = obj.__code__
        if inspect.istraceback(obj):
            obj = obj.tb_frame
        if inspect.isframe(obj):
            obj = obj.f_code
        if inspect.iscode(obj):
            lineno = getattr(obj, 'co_firstlineno', None) - 1
        if lineno is not None:
            if source_lines is None:
                return lineno + 1
            pat = re.compile('(^|.*:)\\s*\\w*("|\\\')')
            for lineno in range(lineno, len(source_lines)):
                if pat.match(source_lines[lineno]):
                    return lineno


class DocTestRunner:
    __doc__ = "\n    A class used to run DocTest test cases, and accumulate statistics.\n    The `run` method is used to process a single DocTest case.  It\n    returns a tuple `(f, t)`, where `t` is the number of test cases\n    tried, and `f` is the number of test cases that failed.\n\n        >>> tests = DocTestFinder().find(_TestClass)\n        >>> runner = DocTestRunner(verbose=False)\n        >>> tests.sort(key = lambda test: test.name)\n        >>> for test in tests:\n        ...     print(test.name, '->', runner.run(test))\n        _TestClass -> TestResults(failed=0, attempted=2)\n        _TestClass.__init__ -> TestResults(failed=0, attempted=2)\n        _TestClass.get -> TestResults(failed=0, attempted=2)\n        _TestClass.square -> TestResults(failed=0, attempted=1)\n\n    The `summarize` method prints a summary of all the test cases that\n    have been run by the runner, and returns an aggregated `(f, t)`\n    tuple:\n\n        >>> runner.summarize(verbose=1)\n        4 items passed all tests:\n           2 tests in _TestClass\n           2 tests in _TestClass.__init__\n           2 tests in _TestClass.get\n           1 tests in _TestClass.square\n        7 tests in 4 items.\n        7 passed and 0 failed.\n        Test passed.\n        TestResults(failed=0, attempted=7)\n\n    The aggregated number of tried examples and failed examples is\n    also available via the `tries` and `failures` attributes:\n\n        >>> runner.tries\n        7\n        >>> runner.failures\n        0\n\n    The comparison between expected outputs and actual outputs is done\n    by an `OutputChecker`.  This comparison may be customized with a\n    number of option flags; see the documentation for `testmod` for\n    more information.  If the option flags are insufficient, then the\n    comparison may also be customized by passing a subclass of\n    `OutputChecker` to the constructor.\n\n    The test runner's display output can be controlled in two ways.\n    First, an output function (`out) can be passed to\n    `TestRunner.run`; this function will be called with strings that\n    should be displayed.  It defaults to `sys.stdout.write`.  If\n    capturing the output is not sufficient, then the display output\n    can be also customized by subclassing DocTestRunner, and\n    overriding the methods `report_start`, `report_success`,\n    `report_unexpected_exception`, and `report_failure`.\n    "
    DIVIDER = '**********************************************************************'

    def __init__(self, checker=None, verbose=None, optionflags=0):
        """
        Create a new test runner.

        Optional keyword arg `checker` is the `OutputChecker` that
        should be used to compare the expected outputs and actual
        outputs of doctest examples.

        Optional keyword arg 'verbose' prints lots of stuff if true,
        only failures if false; by default, it's true iff '-v' is in
        sys.argv.

        Optional argument `optionflags` can be used to control how the
        test runner compares expected output to actual output, and how
        it displays failures.  See the documentation for `testmod` for
        more information.
        """
        self._checker = checker or OutputChecker()
        if verbose is None:
            verbose = '-v' in sys.argv
        self._verbose = verbose
        self.optionflags = optionflags
        self.original_optionflags = optionflags
        self.tries = 0
        self.failures = 0
        self._name2ft = {}
        self._fakeout = _SpoofOut()

    def report_start(self, out, test, example):
        """
        Report that the test runner is about to process the given
        example.  (Only displays a message if verbose=True)
        """
        if self._verbose:
            if example.want:
                out('Trying:\n' + _indent(example.source) + 'Expecting:\n' + _indent(example.want))
            else:
                out('Trying:\n' + _indent(example.source) + 'Expecting nothing\n')

    def report_success(self, out, test, example, got):
        """
        Report that the given example ran successfully.  (Only
        displays a message if verbose=True)
        """
        if self._verbose:
            out('ok\n')

    def report_failure(self, out, test, example, got):
        """
        Report that the given example failed.
        """
        out(self._failure_header(test, example) + self._checker.output_difference(example, got, self.optionflags))

    def report_unexpected_exception(self, out, test, example, exc_info):
        """
        Report that the given example raised an unexpected exception.
        """
        out(self._failure_header(test, example) + 'Exception raised:\n' + _indent(_exception_traceback(exc_info)))

    def _failure_header(self, test, example):
        out = [
         self.DIVIDER]
        if test.filename:
            if test.lineno is not None and example.lineno is not None:
                lineno = test.lineno + example.lineno + 1
            else:
                lineno = '?'
            out.append('File "%s", line %s, in %s' % (
             test.filename, lineno, test.name))
        else:
            out.append('Line %s, in %s' % (example.lineno + 1, test.name))
        out.append('Failed example:')
        source = example.source
        out.append(_indent(source))
        return '\n'.join(out)

    def __run--- This code section failed: ---

 L.1290         0  LOAD_CONST               0
                2  DUP_TOP          
                4  STORE_FAST               'failures'
                6  STORE_FAST               'tries'

 L.1294         8  LOAD_FAST                'self'
               10  LOAD_ATTR                optionflags
               12  STORE_FAST               'original_optionflags'

 L.1296        14  LOAD_GLOBAL              range
               16  LOAD_CONST               3
               18  CALL_FUNCTION_1       1  ''
               20  UNPACK_SEQUENCE_3     3 
               22  STORE_FAST               'SUCCESS'
               24  STORE_FAST               'FAILURE'
               26  STORE_FAST               'BOOM'

 L.1298        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _checker
               32  LOAD_ATTR                check_output
               34  STORE_FAST               'check'

 L.1301        36  LOAD_GLOBAL              enumerate
               38  LOAD_FAST                'test'
               40  LOAD_ATTR                examples
               42  CALL_FUNCTION_1       1  ''
               44  GET_ITER         
             46_0  COME_FROM           624  '624'
             46_1  COME_FROM           614  '614'
            46_48  FOR_ITER            634  'to 634'
               50  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST               'examplenum'
               54  STORE_FAST               'example'

 L.1305        56  LOAD_FAST                'self'
               58  LOAD_ATTR                optionflags
               60  LOAD_GLOBAL              REPORT_ONLY_FIRST_FAILURE
               62  BINARY_AND       
               64  JUMP_IF_FALSE_OR_POP    72  'to 72'

 L.1306        66  LOAD_FAST                'failures'
               68  LOAD_CONST               0
               70  COMPARE_OP               >
             72_0  COME_FROM            64  '64'

 L.1305        72  STORE_FAST               'quiet'

 L.1309        74  LOAD_FAST                'original_optionflags'
               76  LOAD_FAST                'self'
               78  STORE_ATTR               optionflags

 L.1310        80  LOAD_FAST                'example'
               82  LOAD_ATTR                options
               84  POP_JUMP_IF_FALSE   142  'to 142'

 L.1311        86  LOAD_FAST                'example'
               88  LOAD_ATTR                options
               90  LOAD_METHOD              items
               92  CALL_METHOD_0         0  ''
               94  GET_ITER         
               96  FOR_ITER            142  'to 142'
               98  UNPACK_SEQUENCE_2     2 
              100  STORE_FAST               'optionflag'
              102  STORE_FAST               'val'

 L.1312       104  LOAD_FAST                'val'
              106  POP_JUMP_IF_FALSE   124  'to 124'

 L.1313       108  LOAD_FAST                'self'
              110  DUP_TOP          
              112  LOAD_ATTR                optionflags
              114  LOAD_FAST                'optionflag'
              116  INPLACE_OR       
              118  ROT_TWO          
              120  STORE_ATTR               optionflags
              122  JUMP_BACK            96  'to 96'
            124_0  COME_FROM           106  '106'

 L.1315       124  LOAD_FAST                'self'
              126  DUP_TOP          
              128  LOAD_ATTR                optionflags
              130  LOAD_FAST                'optionflag'
              132  UNARY_INVERT     
              134  INPLACE_AND      
              136  ROT_TWO          
              138  STORE_ATTR               optionflags
              140  JUMP_BACK            96  'to 96'
            142_0  COME_FROM            84  '84'

 L.1318       142  LOAD_FAST                'self'
              144  LOAD_ATTR                optionflags
              146  LOAD_GLOBAL              SKIP
              148  BINARY_AND       
              150  POP_JUMP_IF_FALSE   154  'to 154'

 L.1319       152  JUMP_BACK            46  'to 46'
            154_0  COME_FROM           150  '150'

 L.1322       154  LOAD_FAST                'tries'
              156  LOAD_CONST               1
              158  INPLACE_ADD      
              160  STORE_FAST               'tries'

 L.1323       162  LOAD_FAST                'quiet'
              164  POP_JUMP_IF_TRUE    180  'to 180'

 L.1324       166  LOAD_FAST                'self'
              168  LOAD_METHOD              report_start
              170  LOAD_FAST                'out'
              172  LOAD_FAST                'test'
              174  LOAD_FAST                'example'
              176  CALL_METHOD_3         3  ''
              178  POP_TOP          
            180_0  COME_FROM           164  '164'

 L.1329       180  LOAD_STR                 '<doctest %s[%d]>'
              182  LOAD_FAST                'test'
              184  LOAD_ATTR                name
              186  LOAD_FAST                'examplenum'
              188  BUILD_TUPLE_2         2 
              190  BINARY_MODULO    
              192  STORE_FAST               'filename'

 L.1334       194  SETUP_FINALLY       240  'to 240'

 L.1336       196  LOAD_GLOBAL              exec
              198  LOAD_GLOBAL              compile
              200  LOAD_FAST                'example'
              202  LOAD_ATTR                source
              204  LOAD_FAST                'filename'
              206  LOAD_STR                 'single'

 L.1337       208  LOAD_FAST                'compileflags'

 L.1337       210  LOAD_CONST               1

 L.1336       212  CALL_FUNCTION_5       5  ''

 L.1337       214  LOAD_FAST                'test'
              216  LOAD_ATTR                globs

 L.1336       218  CALL_FUNCTION_2       2  ''
              220  POP_TOP          

 L.1338       222  LOAD_FAST                'self'
              224  LOAD_ATTR                debugger
              226  LOAD_METHOD              set_continue
              228  CALL_METHOD_0         0  ''
              230  POP_TOP          

 L.1339       232  LOAD_CONST               None
              234  STORE_FAST               'exception'
              236  POP_BLOCK        
              238  JUMP_FORWARD        292  'to 292'
            240_0  COME_FROM_FINALLY   194  '194'

 L.1340       240  DUP_TOP          
              242  LOAD_GLOBAL              KeyboardInterrupt
              244  COMPARE_OP               exception-match
          246_248  POP_JUMP_IF_FALSE   262  'to 262'
              250  POP_TOP          
              252  POP_TOP          
              254  POP_TOP          

 L.1341       256  RAISE_VARARGS_0       0  'reraise'
              258  POP_EXCEPT       
              260  JUMP_FORWARD        292  'to 292'
            262_0  COME_FROM           246  '246'

 L.1342       262  POP_TOP          
              264  POP_TOP          
              266  POP_TOP          

 L.1343       268  LOAD_GLOBAL              sys
              270  LOAD_METHOD              exc_info
              272  CALL_METHOD_0         0  ''
              274  STORE_FAST               'exception'

 L.1344       276  LOAD_FAST                'self'
              278  LOAD_ATTR                debugger
              280  LOAD_METHOD              set_continue
              282  CALL_METHOD_0         0  ''
              284  POP_TOP          
              286  POP_EXCEPT       
              288  JUMP_FORWARD        292  'to 292'
              290  END_FINALLY      
            292_0  COME_FROM           288  '288'
            292_1  COME_FROM           260  '260'
            292_2  COME_FROM           238  '238'

 L.1346       292  LOAD_FAST                'self'
              294  LOAD_ATTR                _fakeout
              296  LOAD_METHOD              getvalue
              298  CALL_METHOD_0         0  ''
              300  STORE_FAST               'got'

 L.1347       302  LOAD_FAST                'self'
              304  LOAD_ATTR                _fakeout
              306  LOAD_METHOD              truncate
              308  LOAD_CONST               0
              310  CALL_METHOD_1         1  ''
              312  POP_TOP          

 L.1348       314  LOAD_FAST                'FAILURE'
              316  STORE_FAST               'outcome'

 L.1352       318  LOAD_FAST                'exception'
              320  LOAD_CONST               None
              322  COMPARE_OP               is
          324_326  POP_JUMP_IF_FALSE   352  'to 352'

 L.1353       328  LOAD_FAST                'check'
              330  LOAD_FAST                'example'
              332  LOAD_ATTR                want
              334  LOAD_FAST                'got'
              336  LOAD_FAST                'self'
              338  LOAD_ATTR                optionflags
              340  CALL_FUNCTION_3       3  ''
          342_344  POP_JUMP_IF_FALSE   476  'to 476'

 L.1354       346  LOAD_FAST                'SUCCESS'
              348  STORE_FAST               'outcome'
              350  JUMP_FORWARD        476  'to 476'
            352_0  COME_FROM           324  '324'

 L.1358       352  LOAD_GLOBAL              traceback
              354  LOAD_ATTR                format_exception_only
              356  LOAD_FAST                'exception'
              358  LOAD_CONST               None
              360  LOAD_CONST               2
              362  BUILD_SLICE_2         2 
              364  BINARY_SUBSCR    
              366  CALL_FUNCTION_EX      0  'positional arguments only'
              368  LOAD_CONST               -1
              370  BINARY_SUBSCR    
              372  STORE_FAST               'exc_msg'

 L.1359       374  LOAD_FAST                'quiet'
          376_378  POP_JUMP_IF_TRUE    392  'to 392'

 L.1360       380  LOAD_FAST                'got'
              382  LOAD_GLOBAL              _exception_traceback
              384  LOAD_FAST                'exception'
              386  CALL_FUNCTION_1       1  ''
              388  INPLACE_ADD      
              390  STORE_FAST               'got'
            392_0  COME_FROM           376  '376'

 L.1364       392  LOAD_FAST                'example'
              394  LOAD_ATTR                exc_msg
              396  LOAD_CONST               None
              398  COMPARE_OP               is
          400_402  POP_JUMP_IF_FALSE   410  'to 410'

 L.1365       404  LOAD_FAST                'BOOM'
              406  STORE_FAST               'outcome'
              408  JUMP_FORWARD        476  'to 476'
            410_0  COME_FROM           400  '400'

 L.1368       410  LOAD_FAST                'check'
              412  LOAD_FAST                'example'
              414  LOAD_ATTR                exc_msg
              416  LOAD_FAST                'exc_msg'
              418  LOAD_FAST                'self'
              420  LOAD_ATTR                optionflags
              422  CALL_FUNCTION_3       3  ''
          424_426  POP_JUMP_IF_FALSE   434  'to 434'

 L.1369       428  LOAD_FAST                'SUCCESS'
              430  STORE_FAST               'outcome'
              432  JUMP_FORWARD        476  'to 476'
            434_0  COME_FROM           424  '424'

 L.1372       434  LOAD_FAST                'self'
              436  LOAD_ATTR                optionflags
              438  LOAD_GLOBAL              IGNORE_EXCEPTION_DETAIL
              440  BINARY_AND       
          442_444  POP_JUMP_IF_FALSE   476  'to 476'

 L.1373       446  LOAD_FAST                'check'
              448  LOAD_GLOBAL              _strip_exception_details
              450  LOAD_FAST                'example'
              452  LOAD_ATTR                exc_msg
              454  CALL_FUNCTION_1       1  ''

 L.1374       456  LOAD_GLOBAL              _strip_exception_details
              458  LOAD_FAST                'exc_msg'
              460  CALL_FUNCTION_1       1  ''

 L.1375       462  LOAD_FAST                'self'
              464  LOAD_ATTR                optionflags

 L.1373       466  CALL_FUNCTION_3       3  ''
          468_470  POP_JUMP_IF_FALSE   476  'to 476'

 L.1376       472  LOAD_FAST                'SUCCESS'
              474  STORE_FAST               'outcome'
            476_0  COME_FROM           468  '468'
            476_1  COME_FROM           442  '442'
            476_2  COME_FROM           432  '432'
            476_3  COME_FROM           408  '408'
            476_4  COME_FROM           350  '350'
            476_5  COME_FROM           342  '342'

 L.1379       476  LOAD_FAST                'outcome'
              478  LOAD_FAST                'SUCCESS'
              480  COMPARE_OP               is
          482_484  POP_JUMP_IF_FALSE   510  'to 510'

 L.1380       486  LOAD_FAST                'quiet'
          488_490  POP_JUMP_IF_TRUE    612  'to 612'

 L.1381       492  LOAD_FAST                'self'
              494  LOAD_METHOD              report_success
              496  LOAD_FAST                'out'
              498  LOAD_FAST                'test'
              500  LOAD_FAST                'example'
              502  LOAD_FAST                'got'
              504  CALL_METHOD_4         4  ''
              506  POP_TOP          
              508  JUMP_FORWARD        612  'to 612'
            510_0  COME_FROM           482  '482'

 L.1382       510  LOAD_FAST                'outcome'
              512  LOAD_FAST                'FAILURE'
              514  COMPARE_OP               is
          516_518  POP_JUMP_IF_FALSE   552  'to 552'

 L.1383       520  LOAD_FAST                'quiet'
          522_524  POP_JUMP_IF_TRUE    542  'to 542'

 L.1384       526  LOAD_FAST                'self'
              528  LOAD_METHOD              report_failure
              530  LOAD_FAST                'out'
              532  LOAD_FAST                'test'
              534  LOAD_FAST                'example'
              536  LOAD_FAST                'got'
              538  CALL_METHOD_4         4  ''
              540  POP_TOP          
            542_0  COME_FROM           522  '522'

 L.1385       542  LOAD_FAST                'failures'
              544  LOAD_CONST               1
              546  INPLACE_ADD      
              548  STORE_FAST               'failures'
              550  JUMP_FORWARD        612  'to 612'
            552_0  COME_FROM           516  '516'

 L.1386       552  LOAD_FAST                'outcome'
              554  LOAD_FAST                'BOOM'
              556  COMPARE_OP               is
          558_560  POP_JUMP_IF_FALSE   594  'to 594'

 L.1387       562  LOAD_FAST                'quiet'
          564_566  POP_JUMP_IF_TRUE    584  'to 584'

 L.1388       568  LOAD_FAST                'self'
              570  LOAD_METHOD              report_unexpected_exception
              572  LOAD_FAST                'out'
              574  LOAD_FAST                'test'
              576  LOAD_FAST                'example'

 L.1389       578  LOAD_FAST                'exception'

 L.1388       580  CALL_METHOD_4         4  ''
              582  POP_TOP          
            584_0  COME_FROM           564  '564'

 L.1390       584  LOAD_FAST                'failures'
              586  LOAD_CONST               1
              588  INPLACE_ADD      
              590  STORE_FAST               'failures'
              592  JUMP_FORWARD        612  'to 612'
            594_0  COME_FROM           558  '558'

 L.1392       594  LOAD_CONST               False
          596_598  POP_JUMP_IF_TRUE    612  'to 612'
              600  LOAD_ASSERT              AssertionError
              602  LOAD_STR                 'unknown outcome'
              604  LOAD_FAST                'outcome'
              606  BUILD_TUPLE_2         2 
              608  CALL_FUNCTION_1       1  ''
              610  RAISE_VARARGS_1       1  'exception instance'
            612_0  COME_FROM           596  '596'
            612_1  COME_FROM           592  '592'
            612_2  COME_FROM           550  '550'
            612_3  COME_FROM           508  '508'
            612_4  COME_FROM           488  '488'

 L.1394       612  LOAD_FAST                'failures'
              614  POP_JUMP_IF_FALSE    46  'to 46'
              616  LOAD_FAST                'self'
              618  LOAD_ATTR                optionflags
              620  LOAD_GLOBAL              FAIL_FAST
              622  BINARY_AND       
              624  POP_JUMP_IF_FALSE    46  'to 46'

 L.1395       626  POP_TOP          
          628_630  JUMP_ABSOLUTE       634  'to 634'
              632  JUMP_BACK            46  'to 46'

 L.1398       634  LOAD_FAST                'original_optionflags'
              636  LOAD_FAST                'self'
              638  STORE_ATTR               optionflags

 L.1401       640  LOAD_FAST                'self'
              642  LOAD_METHOD              _DocTestRunner__record_outcome
              644  LOAD_FAST                'test'
              646  LOAD_FAST                'failures'
              648  LOAD_FAST                'tries'
              650  CALL_METHOD_3         3  ''
              652  POP_TOP          

 L.1402       654  LOAD_GLOBAL              TestResults
              656  LOAD_FAST                'failures'
              658  LOAD_FAST                'tries'
              660  CALL_FUNCTION_2       2  ''
              662  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 632

    def __record_outcome(self, test, f, t):
        """
        Record the fact that the given DocTest (`test`) generated `f`
        failures out of `t` tried examples.
        """
        f2, t2 = self._name2ft.get(test.name, (0, 0))
        self._name2ft[test.name] = (f + f2, t + t2)
        self.failures += f
        self.tries += t

    _DocTestRunner__LINECACHE_FILENAME_RE = re.compile('<doctest (?P<name>.+)\\[(?P<examplenum>\\d+)\\]>$')

    def __patched_linecache_getlines(self, filename, module_globals=None):
        m = self._DocTestRunner__LINECACHE_FILENAME_RE.match(filename)
        if m:
            if m.group('name') == self.test.name:
                example = self.test.examples[int(m.group('examplenum'))]
                return example.source.splitlines(keepends=True)
        return self.save_linecache_getlines(filename, module_globals)

    def run(self, test, compileflags=None, out=None, clear_globs=True):
        """
        Run the examples in `test`, and display the results using the
        writer function `out`.

        The examples are run in the namespace `test.globs`.  If
        `clear_globs` is true (the default), then this namespace will
        be cleared after the test runs, to help with garbage
        collection.  If you would like to examine the namespace after
        the test completes, then use `clear_globs=False`.

        `compileflags` gives the set of flags that should be used by
        the Python compiler when running the examples.  If not
        specified, then it will default to the set of future-import
        flags that apply to `globs`.

        The output of each example is checked using
        `DocTestRunner.check_output`, and the results are formatted by
        the `DocTestRunner.report_*` methods.
        """
        self.test = test
        if compileflags is None:
            compileflags = _extract_future_flags(test.globs)
        else:
            save_stdout = sys.stdout
            if out is None:
                encoding = save_stdout.encoding
                if encoding is None or encoding.lower == 'utf-8':
                    out = save_stdout.write
                else:

                    def out(s):
                        s = str(s.encode(encoding, 'backslashreplace'), encoding)
                        save_stdout.write(s)

        sys.stdout = self._fakeout
        save_trace = sys.gettrace
        save_set_trace = pdb.set_trace
        self.debugger = _OutputRedirectingPdb(save_stdout)
        self.debugger.reset
        pdb.set_trace = self.debugger.set_trace
        self.save_linecache_getlines = linecache.getlines
        linecache.getlines = self._DocTestRunner__patched_linecache_getlines
        save_displayhook = sys.displayhook
        sys.displayhook = sys.__displayhook__
        try:
            return self._DocTestRunner__run(test, compileflags, out)
        finally:
            sys.stdout = save_stdout
            pdb.set_trace = save_set_trace
            sys.settrace(save_trace)
            linecache.getlines = self.save_linecache_getlines
            sys.displayhook = save_displayhook
            if clear_globs:
                test.globs.clear
                import builtins
                builtins._ = None

    def summarize(self, verbose=None):
        """
        Print a summary of all the test cases that have been run by
        this DocTestRunner, and return a tuple `(f, t)`, where `f` is
        the total number of failed examples, and `t` is the total
        number of tried examples.

        The optional `verbose` argument controls how detailed the
        summary is.  If the verbosity is not specified, then the
        DocTestRunner's verbosity is used.
        """
        if verbose is None:
            verbose = self._verbose
        notests = []
        passed = []
        failed = []
        totalt = totalf = 0
        for x in self._name2ft.items:
            name, (f, t) = x
            assert f <= t
            totalt += t
            totalf += f
            if t == 0:
                notests.append(name)
            elif f == 0:
                passed.append((name, t))
            else:
                failed.append(x)
        else:
            if verbose:
                if notests:
                    print(len(notests), 'items had no tests:')
                    notests.sort
                    for thing in notests:
                        print('   ', thing)

                elif passed:
                    print(len(passed), 'items passed all tests:')
                    passed.sort
                    for thing, count in passed:
                        print(' %3d tests in %s' % (count, thing))

            if failed:
                print(self.DIVIDER)
                print(len(failed), 'items had failures:')
                failed.sort
                for thing, (f, t) in failed:
                    print(' %3d of %3d in %s' % (f, t, thing))

            if verbose:
                print(totalt, 'tests in', len(self._name2ft), 'items.')
                print(totalt - totalf, 'passed and', totalf, 'failed.')

        if totalf:
            print('***Test Failed***', totalf, 'failures.')
        else:
            if verbose:
                print('Test passed.')
            return TestResults(totalf, totalt)

    def merge(self, other):
        d = self._name2ft
        for name, (f, t) in other._name2ft.items:
            if name in d:
                f2, t2 = d[name]
                f = f + f2
                t = t + t2
            d[name] = (
             f, t)


class OutputChecker:
    __doc__ = '\n    A class used to check the whether the actual output from a doctest\n    example matches the expected output.  `OutputChecker` defines two\n    methods: `check_output`, which compares a given pair of outputs,\n    and returns true if they match; and `output_difference`, which\n    returns a string describing the differences between two outputs.\n    '

    def _toAscii(self, s):
        """
        Convert string to hex-escaped ASCII string.
        """
        return str(s.encode('ASCII', 'backslashreplace'), 'ASCII')

    def check_output(self, want, got, optionflags):
        """
        Return True iff the actual output from an example (`got`)
        matches the expected output (`want`).  These strings are
        always considered to match if they are identical; but
        depending on what option flags the test runner is using,
        several non-exact match types are also possible.  See the
        documentation for `TestRunner` for more information about
        option flags.
        """
        got = self._toAscii(got)
        want = self._toAscii(want)
        if got == want:
            return True
        if not optionflags & DONT_ACCEPT_TRUE_FOR_1:
            if (
             got, want) == ('True\n', '1\n'):
                return True
            if (
             got, want) == ('False\n', '0\n'):
                return True
        if not optionflags & DONT_ACCEPT_BLANKLINE:
            want = re.sub('(?m)^%s\\s*?$' % re.escape(BLANKLINE_MARKER), '', want)
            got = re.sub('(?m)^[^\\S\\n]+$', '', got)
            if got == want:
                return True
        if optionflags & NORMALIZE_WHITESPACE:
            got = ' '.join(got.split)
            want = ' '.join(want.split)
            if got == want:
                return True
        if optionflags & ELLIPSIS:
            if _ellipsis_match(want, got):
                return True
        return False

    def _do_a_fancy_diff(self, want, got, optionflags):
        if not optionflags & (REPORT_UDIFF | REPORT_CDIFF | REPORT_NDIFF):
            return False
        if optionflags & REPORT_NDIFF:
            return True
        return want.count('\n') > 2 and got.count('\n') > 2

    def output_difference(self, example, got, optionflags):
        """
        Return a string describing the differences between the
        expected output for a given example (`example`) and the actual
        output (`got`).  `optionflags` is the set of option flags used
        to compare `want` and `got`.
        """
        want = example.want
        if not optionflags & DONT_ACCEPT_BLANKLINE:
            got = re.sub('(?m)^[ ]*(?=\n)', BLANKLINE_MARKER, got)
        if self._do_a_fancy_diff(want, got, optionflags):
            want_lines = want.splitlines(keepends=True)
            got_lines = got.splitlines(keepends=True)
            if optionflags & REPORT_UDIFF:
                diff = difflib.unified_diff(want_lines, got_lines, n=2)
                diff = list(diff)[2:]
                kind = 'unified diff with -expected +actual'
            else:
                if optionflags & REPORT_CDIFF:
                    diff = difflib.context_diff(want_lines, got_lines, n=2)
                    diff = list(diff)[2:]
                    kind = 'context diff with expected followed by actual'
                else:
                    if optionflags & REPORT_NDIFF:
                        engine = difflib.Differ(charjunk=(difflib.IS_CHARACTER_JUNK))
                        diff = list(engine.compare(want_lines, got_lines))
                        kind = 'ndiff with -expected +actual'
                    else:
                        assert 0, 'Bad diff option'
            return 'Differences (%s):\n' % kind + _indent(''.join(diff))
        if want:
            if got:
                return 'Expected:\n%sGot:\n%s' % (_indent(want), _indent(got))
        if want:
            return 'Expected:\n%sGot nothing\n' % _indent(want)
        if got:
            return 'Expected nothing\nGot:\n%s' % _indent(got)
        return 'Expected nothing\nGot nothing\n'


class DocTestFailure(Exception):
    __doc__ = 'A DocTest example has failed in debugging mode.\n\n    The exception instance has variables:\n\n    - test: the DocTest object being run\n\n    - example: the Example object that failed\n\n    - got: the actual output\n    '

    def __init__(self, test, example, got):
        self.test = test
        self.example = example
        self.got = got

    def __str__(self):
        return str(self.test)


class UnexpectedException(Exception):
    __doc__ = 'A DocTest example has encountered an unexpected exception\n\n    The exception instance has variables:\n\n    - test: the DocTest object being run\n\n    - example: the Example object that failed\n\n    - exc_info: the exception info\n    '

    def __init__(self, test, example, exc_info):
        self.test = test
        self.example = example
        self.exc_info = exc_info

    def __str__(self):
        return str(self.test)


class DebugRunner(DocTestRunner):
    __doc__ = "Run doc tests but raise an exception as soon as there is a failure.\n\n       If an unexpected exception occurs, an UnexpectedException is raised.\n       It contains the test, the example, and the original exception:\n\n         >>> runner = DebugRunner(verbose=False)\n         >>> test = DocTestParser().get_doctest('>>> raise KeyError\\n42',\n         ...                                    {}, 'foo', 'foo.py', 0)\n         >>> try:\n         ...     runner.run(test)\n         ... except UnexpectedException as f:\n         ...     failure = f\n\n         >>> failure.test is test\n         True\n\n         >>> failure.example.want\n         '42\\n'\n\n         >>> exc_info = failure.exc_info\n         >>> raise exc_info[1] # Already has the traceback\n         Traceback (most recent call last):\n         ...\n         KeyError\n\n       We wrap the original exception to give the calling application\n       access to the test and example information.\n\n       If the output doesn't match, then a DocTestFailure is raised:\n\n         >>> test = DocTestParser().get_doctest('''\n         ...      >>> x = 1\n         ...      >>> x\n         ...      2\n         ...      ''', {}, 'foo', 'foo.py', 0)\n\n         >>> try:\n         ...    runner.run(test)\n         ... except DocTestFailure as f:\n         ...    failure = f\n\n       DocTestFailure objects provide access to the test:\n\n         >>> failure.test is test\n         True\n\n       As well as to the example:\n\n         >>> failure.example.want\n         '2\\n'\n\n       and the actual output:\n\n         >>> failure.got\n         '1\\n'\n\n       If a failure or error occurs, the globals are left intact:\n\n         >>> del test.globs['__builtins__']\n         >>> test.globs\n         {'x': 1}\n\n         >>> test = DocTestParser().get_doctest('''\n         ...      >>> x = 2\n         ...      >>> raise KeyError\n         ...      ''', {}, 'foo', 'foo.py', 0)\n\n         >>> runner.run(test)\n         Traceback (most recent call last):\n         ...\n         doctest.UnexpectedException: <DocTest foo from foo.py:0 (2 examples)>\n\n         >>> del test.globs['__builtins__']\n         >>> test.globs\n         {'x': 2}\n\n       But the globals are cleared if there is no error:\n\n         >>> test = DocTestParser().get_doctest('''\n         ...      >>> x = 2\n         ...      ''', {}, 'foo', 'foo.py', 0)\n\n         >>> runner.run(test)\n         TestResults(failed=0, attempted=1)\n\n         >>> test.globs\n         {}\n\n       "

    def run(self, test, compileflags=None, out=None, clear_globs=True):
        r = DocTestRunner.run(self, test, compileflags, out, False)
        if clear_globs:
            test.globs.clear
        return r

    def report_unexpected_exception(self, out, test, example, exc_info):
        raise UnexpectedException(test, example, exc_info)

    def report_failure(self, out, test, example, got):
        raise DocTestFailure(test, example, got)


master = None

def testmod(m=None, name=None, globs=None, verbose=None, report=True, optionflags=0, extraglobs=None, raise_on_error=False, exclude_empty=False):
    """m=None, name=None, globs=None, verbose=None, report=True,
       optionflags=0, extraglobs=None, raise_on_error=False,
       exclude_empty=False

    Test examples in docstrings in functions and classes reachable
    from module m (or the current module if m is not supplied), starting
    with m.__doc__.

    Also test examples reachable from dict m.__test__ if it exists and is
    not None.  m.__test__ maps names to functions, classes and strings;
    function and class docstrings are tested even if the name is private;
    strings are tested directly, as if they were docstrings.

    Return (#failures, #tests).

    See help(doctest) for an overview.

    Optional keyword arg "name" gives the name of the module; by default
    use m.__name__.

    Optional keyword arg "globs" gives a dict to be used as the globals
    when executing examples; by default, use m.__dict__.  A copy of this
    dict is actually used for each docstring, so that each docstring's
    examples start with a clean slate.

    Optional keyword arg "extraglobs" gives a dictionary that should be
    merged into the globals that are used to execute examples.  By
    default, no extra globals are used.  This is new in 2.4.

    Optional keyword arg "verbose" prints lots of stuff if true, prints
    only failures if false; by default, it's true iff "-v" is in sys.argv.

    Optional keyword arg "report" prints a summary at the end when true,
    else prints nothing at the end.  In verbose mode, the summary is
    detailed, else very brief (in fact, empty if all tests passed).

    Optional keyword arg "optionflags" or's together module constants,
    and defaults to 0.  This is new in 2.3.  Possible values (see the
    docs for details):

        DONT_ACCEPT_TRUE_FOR_1
        DONT_ACCEPT_BLANKLINE
        NORMALIZE_WHITESPACE
        ELLIPSIS
        SKIP
        IGNORE_EXCEPTION_DETAIL
        REPORT_UDIFF
        REPORT_CDIFF
        REPORT_NDIFF
        REPORT_ONLY_FIRST_FAILURE

    Optional keyword arg "raise_on_error" raises an exception on the
    first unexpected exception or failure. This allows failures to be
    post-mortem debugged.

    Advanced tomfoolery:  testmod runs methods of a local instance of
    class doctest.Tester, then merges the results into (or creates)
    global Tester instance doctest.master.  Methods of doctest.master
    can be called directly too, if you want to do something unusual.
    Passing report=0 to testmod is especially useful then, to delay
    displaying a summary.  Invoke doctest.master.summarize(verbose)
    when you're done fiddling.
    """
    global master
    if m is None:
        m = sys.modules.get('__main__')
    else:
        if not inspect.ismodule(m):
            raise TypeError('testmod: module required; %r' % (m,))
        if name is None:
            name = m.__name__
        finder = DocTestFinder(exclude_empty=exclude_empty)
        if raise_on_error:
            runner = DebugRunner(verbose=verbose, optionflags=optionflags)
        else:
            runner = DocTestRunner(verbose=verbose, optionflags=optionflags)
    for test in finder.find(m, name, globs=globs, extraglobs=extraglobs):
        runner.run(test)
    else:
        if report:
            runner.summarize
        elif master is None:
            master = runner
        else:
            master.merge(runner)
        return TestResults(runner.failures, runner.tries)


def testfile(filename, module_relative=True, name=None, package=None, globs=None, verbose=None, report=True, optionflags=0, extraglobs=None, raise_on_error=False, parser=DocTestParser(), encoding=None):
    """
    Test examples in the given file.  Return (#failures, #tests).

    Optional keyword arg "module_relative" specifies how filenames
    should be interpreted:

      - If "module_relative" is True (the default), then "filename"
         specifies a module-relative path.  By default, this path is
         relative to the calling module's directory; but if the
         "package" argument is specified, then it is relative to that
         package.  To ensure os-independence, "filename" should use
         "/" characters to separate path segments, and should not
         be an absolute path (i.e., it may not begin with "/").

      - If "module_relative" is False, then "filename" specifies an
        os-specific path.  The path may be absolute or relative (to
        the current working directory).

    Optional keyword arg "name" gives the name of the test; by default
    use the file's basename.

    Optional keyword argument "package" is a Python package or the
    name of a Python package whose directory should be used as the
    base directory for a module relative filename.  If no package is
    specified, then the calling module's directory is used as the base
    directory for module relative filenames.  It is an error to
    specify "package" if "module_relative" is False.

    Optional keyword arg "globs" gives a dict to be used as the globals
    when executing examples; by default, use {}.  A copy of this dict
    is actually used for each docstring, so that each docstring's
    examples start with a clean slate.

    Optional keyword arg "extraglobs" gives a dictionary that should be
    merged into the globals that are used to execute examples.  By
    default, no extra globals are used.

    Optional keyword arg "verbose" prints lots of stuff if true, prints
    only failures if false; by default, it's true iff "-v" is in sys.argv.

    Optional keyword arg "report" prints a summary at the end when true,
    else prints nothing at the end.  In verbose mode, the summary is
    detailed, else very brief (in fact, empty if all tests passed).

    Optional keyword arg "optionflags" or's together module constants,
    and defaults to 0.  Possible values (see the docs for details):

        DONT_ACCEPT_TRUE_FOR_1
        DONT_ACCEPT_BLANKLINE
        NORMALIZE_WHITESPACE
        ELLIPSIS
        SKIP
        IGNORE_EXCEPTION_DETAIL
        REPORT_UDIFF
        REPORT_CDIFF
        REPORT_NDIFF
        REPORT_ONLY_FIRST_FAILURE

    Optional keyword arg "raise_on_error" raises an exception on the
    first unexpected exception or failure. This allows failures to be
    post-mortem debugged.

    Optional keyword arg "parser" specifies a DocTestParser (or
    subclass) that should be used to extract tests from the files.

    Optional keyword arg "encoding" specifies an encoding that should
    be used to convert the file to unicode.

    Advanced tomfoolery:  testmod runs methods of a local instance of
    class doctest.Tester, then merges the results into (or creates)
    global Tester instance doctest.master.  Methods of doctest.master
    can be called directly too, if you want to do something unusual.
    Passing report=0 to testmod is especially useful then, to delay
    displaying a summary.  Invoke doctest.master.summarize(verbose)
    when you're done fiddling.
    """
    global master
    if package:
        if not module_relative:
            raise ValueError('Package may only be specified for module-relative paths.')
    else:
        text, filename = _load_testfile(filename, package, module_relative, encoding or 'utf-8')
        if name is None:
            name = os.path.basename(filename)
        else:
            if globs is None:
                globs = {}
            else:
                globs = globs.copy
            if extraglobs is not None:
                globs.update(extraglobs)
            if '__name__' not in globs:
                globs['__name__'] = '__main__'
            if raise_on_error:
                runner = DebugRunner(verbose=verbose, optionflags=optionflags)
            else:
                runner = DocTestRunner(verbose=verbose, optionflags=optionflags)
        test = parser.get_doctest(text, globs, name, filename, 0)
        runner.run(test)
        if report:
            runner.summarize
        if master is None:
            master = runner
        else:
            master.merge(runner)
    return TestResults(runner.failures, runner.tries)


def run_docstring_examples(f, globs, verbose=False, name='NoName', compileflags=None, optionflags=0):
    """
    Test examples in the given object's docstring (`f`), using `globs`
    as globals.  Optional argument `name` is used in failure messages.
    If the optional argument `verbose` is true, then generate output
    even if there are no failures.

    `compileflags` gives the set of flags that should be used by the
    Python compiler when running the examples.  If not specified, then
    it will default to the set of future-import flags that apply to
    `globs`.

    Optional keyword arg `optionflags` specifies options for the
    testing and output.  See the documentation for `testmod` for more
    information.
    """
    finder = DocTestFinder(verbose=verbose, recurse=False)
    runner = DocTestRunner(verbose=verbose, optionflags=optionflags)
    for test in finder.find(f, name, globs=globs):
        runner.run(test, compileflags=compileflags)


_unittest_reportflags = 0

def set_unittest_reportflags(flags):
    """Sets the unittest option flags.

    The old flag is returned so that a runner could restore the old
    value if it wished to:

      >>> import doctest
      >>> old = doctest._unittest_reportflags
      >>> doctest.set_unittest_reportflags(REPORT_NDIFF |
      ...                          REPORT_ONLY_FIRST_FAILURE) == old
      True

      >>> doctest._unittest_reportflags == (REPORT_NDIFF |
      ...                                   REPORT_ONLY_FIRST_FAILURE)
      True

    Only reporting flags can be set:

      >>> doctest.set_unittest_reportflags(ELLIPSIS)
      Traceback (most recent call last):
      ...
      ValueError: ('Only reporting flags allowed', 8)

      >>> doctest.set_unittest_reportflags(old) == (REPORT_NDIFF |
      ...                                   REPORT_ONLY_FIRST_FAILURE)
      True
    """
    global _unittest_reportflags
    if flags & REPORTING_FLAGS != flags:
        raise ValueError('Only reporting flags allowed', flags)
    old = _unittest_reportflags
    _unittest_reportflags = flags
    return old


class DocTestCase(unittest.TestCase):

    def __init__(self, test, optionflags=0, setUp=None, tearDown=None, checker=None):
        unittest.TestCase.__init__(self)
        self._dt_optionflags = optionflags
        self._dt_checker = checker
        self._dt_test = test
        self._dt_setUp = setUp
        self._dt_tearDown = tearDown

    def setUp(self):
        test = self._dt_test
        if self._dt_setUp is not None:
            self._dt_setUp(test)

    def tearDown(self):
        test = self._dt_test
        if self._dt_tearDown is not None:
            self._dt_tearDown(test)
        test.globs.clear

    def runTest(self):
        test = self._dt_test
        old = sys.stdout
        new = StringIO()
        optionflags = self._dt_optionflags
        if not optionflags & REPORTING_FLAGS:
            optionflags |= _unittest_reportflags
        runner = DocTestRunner(optionflags=optionflags, checker=(self._dt_checker),
          verbose=False)
        try:
            runner.DIVIDER = '----------------------------------------------------------------------'
            failures, tries = runner.run(test,
              out=(new.write), clear_globs=False)
        finally:
            sys.stdout = old

        if failures:
            raise self.failureException(self.format_failure(new.getvalue))

    def format_failure(self, err):
        test = self._dt_test
        if test.lineno is None:
            lineno = 'unknown line number'
        else:
            lineno = '%s' % test.lineno
        lname = '.'.join(test.name.split('.')[-1:])
        return 'Failed doctest test for %s\n  File "%s", line %s, in %s\n\n%s' % (
         test.name, test.filename, lineno, lname, err)

    def debug(self):
        r"""Run the test case without results and without catching exceptions

           The unit test framework includes a debug method on test cases
           and test suites to support post-mortem debugging.  The test code
           is run in such a way that errors are not caught.  This way a
           caller can catch the errors and initiate post-mortem debugging.

           The DocTestCase provides a debug method that raises
           UnexpectedException errors if there is an unexpected
           exception:

             >>> test = DocTestParser().get_doctest('>>> raise KeyError\n42',
             ...                {}, 'foo', 'foo.py', 0)
             >>> case = DocTestCase(test)
             >>> try:
             ...     case.debug()
             ... except UnexpectedException as f:
             ...     failure = f

           The UnexpectedException contains the test, the example, and
           the original exception:

             >>> failure.test is test
             True

             >>> failure.example.want
             '42\n'

             >>> exc_info = failure.exc_info
             >>> raise exc_info[1] # Already has the traceback
             Traceback (most recent call last):
             ...
             KeyError

           If the output doesn't match, then a DocTestFailure is raised:

             >>> test = DocTestParser().get_doctest('''
             ...      >>> x = 1
             ...      >>> x
             ...      2
             ...      ''', {}, 'foo', 'foo.py', 0)
             >>> case = DocTestCase(test)

             >>> try:
             ...    case.debug()
             ... except DocTestFailure as f:
             ...    failure = f

           DocTestFailure objects provide access to the test:

             >>> failure.test is test
             True

           As well as to the example:

             >>> failure.example.want
             '2\n'

           and the actual output:

             >>> failure.got
             '1\n'

           """
        self.setUp
        runner = DebugRunner(optionflags=(self._dt_optionflags), checker=(self._dt_checker),
          verbose=False)
        runner.run((self._dt_test), clear_globs=False)
        self.tearDown

    def id(self):
        return self._dt_test.name

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self._dt_test == other._dt_test and self._dt_optionflags == other._dt_optionflags and self._dt_setUp == other._dt_setUp and self._dt_tearDown == other._dt_tearDown and self._dt_checker == other._dt_checker

    def __hash__(self):
        return hash((self._dt_optionflags, self._dt_setUp, self._dt_tearDown,
         self._dt_checker))

    def __repr__(self):
        name = self._dt_test.name.split('.')
        return '%s (%s)' % (name[(-1)], '.'.join(name[:-1]))

    __str__ = object.__str__

    def shortDescription(self):
        return 'Doctest: ' + self._dt_test.name


class SkipDocTestCase(DocTestCase):

    def __init__(self, module):
        self.module = module
        DocTestCase.__init__(self, None)

    def setUp(self):
        self.skipTest('DocTestSuite will not work with -O2 and above')

    def test_skip(self):
        pass

    def shortDescription(self):
        return 'Skipping tests from %s' % self.module.__name__

    __str__ = shortDescription


class _DocTestSuite(unittest.TestSuite):

    def _removeTestAtIndex(self, index):
        pass


def DocTestSuite(module=None, globs=None, extraglobs=None, test_finder=None, **options):
    """
    Convert doctest tests for a module to a unittest test suite.

    This converts each documentation string in a module that
    contains doctest tests to a unittest test case.  If any of the
    tests in a doc string fail, then the test case fails.  An exception
    is raised showing the name of the file containing the test and a
    (sometimes approximate) line number.

    The `module` argument provides the module to be tested.  The argument
    can be either a module or a module name.

    If no argument is given, the calling module is used.

    A number of options may be provided as keyword arguments:

    setUp
      A set-up function.  This is called before running the
      tests in each file. The setUp function will be passed a DocTest
      object.  The setUp function can access the test globals as the
      globs attribute of the test passed.

    tearDown
      A tear-down function.  This is called after running the
      tests in each file.  The tearDown function will be passed a DocTest
      object.  The tearDown function can access the test globals as the
      globs attribute of the test passed.

    globs
      A dictionary containing initial global variables for the tests.

    optionflags
       A set of doctest option flags expressed as an integer.
    """
    if test_finder is None:
        test_finder = DocTestFinder()
    module = _normalize_module(module)
    tests = test_finder.find(module, globs=globs, extraglobs=extraglobs)
    if not tests:
        if sys.flags.optimize >= 2:
            suite = _DocTestSuite()
            suite.addTest(SkipDocTestCase(module))
            return suite
    tests.sort
    suite = _DocTestSuite()
    for test in tests:
        if len(test.examples) == 0:
            pass
        else:
            if not test.filename:
                filename = module.__file__
                if filename[-4:] == '.pyc':
                    filename = filename[:-1]
                test.filename = filename
            suite.addTest(DocTestCase(test, **options))
    else:
        return suite


class DocFileCase(DocTestCase):

    def id(self):
        return '_'.join(self._dt_test.name.split('.'))

    def __repr__(self):
        return self._dt_test.filename

    def format_failure(self, err):
        return 'Failed doctest test for %s\n  File "%s", line 0\n\n%s' % (
         self._dt_test.name, self._dt_test.filename, err)


def DocFileTest(path, module_relative=True, package=None, globs=None, parser=DocTestParser(), encoding=None, **options):
    if globs is None:
        globs = {}
    else:
        globs = globs.copy
    if package:
        if not module_relative:
            raise ValueError('Package may only be specified for module-relative paths.')
    doc, path = _load_testfile(path, package, module_relative, encoding or 'utf-8')
    if '__file__' not in globs:
        globs['__file__'] = path
    name = os.path.basename(path)
    test = parser.get_doctest(doc, globs, name, path, 0)
    return DocFileCase(test, **options)


def DocFileSuite(*paths, **kw):
    """A unittest suite for one or more doctest files.

    The path to each doctest file is given as a string; the
    interpretation of that string depends on the keyword argument
    "module_relative".

    A number of options may be provided as keyword arguments:

    module_relative
      If "module_relative" is True, then the given file paths are
      interpreted as os-independent module-relative paths.  By
      default, these paths are relative to the calling module's
      directory; but if the "package" argument is specified, then
      they are relative to that package.  To ensure os-independence,
      "filename" should use "/" characters to separate path
      segments, and may not be an absolute path (i.e., it may not
      begin with "/").

      If "module_relative" is False, then the given file paths are
      interpreted as os-specific paths.  These paths may be absolute
      or relative (to the current working directory).

    package
      A Python package or the name of a Python package whose directory
      should be used as the base directory for module relative paths.
      If "package" is not specified, then the calling module's
      directory is used as the base directory for module relative
      filenames.  It is an error to specify "package" if
      "module_relative" is False.

    setUp
      A set-up function.  This is called before running the
      tests in each file. The setUp function will be passed a DocTest
      object.  The setUp function can access the test globals as the
      globs attribute of the test passed.

    tearDown
      A tear-down function.  This is called after running the
      tests in each file.  The tearDown function will be passed a DocTest
      object.  The tearDown function can access the test globals as the
      globs attribute of the test passed.

    globs
      A dictionary containing initial global variables for the tests.

    optionflags
      A set of doctest option flags expressed as an integer.

    parser
      A DocTestParser (or subclass) that should be used to extract
      tests from the files.

    encoding
      An encoding that will be used to convert the files to unicode.
    """
    suite = _DocTestSuite()
    if kw.get('module_relative', True):
        kw['package'] = _normalize_module(kw.get('package'))
    for path in paths:
        suite.addTest(DocFileTest(path, **kw))
    else:
        return suite


def script_from_examples(s):
    """Extract script from text with examples.

       Converts text with examples to a Python script.  Example input is
       converted to regular code.  Example output and all other words
       are converted to comments:

       >>> text = '''
       ...       Here are examples of simple math.
       ...
       ...           Python has super accurate integer addition
       ...
       ...           >>> 2 + 2
       ...           5
       ...
       ...           And very friendly error messages:
       ...
       ...           >>> 1/0
       ...           To Infinity
       ...           And
       ...           Beyond
       ...
       ...           You can use logic if you want:
       ...
       ...           >>> if 0:
       ...           ...    blah
       ...           ...    blah
       ...           ...
       ...
       ...           Ho hum
       ...           '''

       >>> print(script_from_examples(text))
       # Here are examples of simple math.
       #
       #     Python has super accurate integer addition
       #
       2 + 2
       # Expected:
       ## 5
       #
       #     And very friendly error messages:
       #
       1/0
       # Expected:
       ## To Infinity
       ## And
       ## Beyond
       #
       #     You can use logic if you want:
       #
       if 0:
          blah
          blah
       #
       #     Ho hum
       <BLANKLINE>
       """
    output = []
    for piece in DocTestParser().parse(s):
        if isinstance(piece, Example):
            output.append(piece.source[:-1])
            want = piece.want
            if want:
                output.append('# Expected:')
                output += ['## ' + l for l in want.split('\n')[:-1]]
            else:
                output += [_comment_line(l) for l in piece.split('\n')[:-1]]
        elif output and output[(-1)] == '#':
            output.pop
        else:
            while output:
                if output[0] == '#':
                    output.pop(0)

            return '\n'.join(output) + '\n'


def testsource(module, name):
    """Extract the test sources from a doctest docstring as a script.

    Provide the module (or dotted name of the module) containing the
    test to be debugged and the name (within the module) of the object
    with the doc string with tests to be debugged.
    """
    module = _normalize_module(module)
    tests = DocTestFinder().find(module)
    test = [t for t in tests if t.name == name]
    if not test:
        raise ValueError(name, 'not found in tests')
    test = test[0]
    testsrc = script_from_examples(test.docstring)
    return testsrc


def debug_src(src, pm=False, globs=None):
    """Debug a single doctest docstring, in argument `src`'"""
    testsrc = script_from_examples(src)
    debug_script(testsrc, pm, globs)


def debug_script(src, pm=False, globs=None):
    """Debug a test script.  `src` is the script, as a string."""
    import pdb
    if globs:
        globs = globs.copy
    else:
        globs = {}
    if pm:
        try:
            exec(src, globs, globs)
        except:
            print(sys.exc_info[1])
            p = pdb.Pdb(nosigint=True)
            p.reset
            p.interaction(None, sys.exc_info[2])

    else:
        pdb.Pdb(nosigint=True).run('exec(%r)' % src, globs, globs)


def debug(module, name, pm=False):
    """Debug a single doctest docstring.

    Provide the module (or dotted name of the module) containing the
    test to be debugged and the name (within the module) of the object
    with the docstring with tests to be debugged.
    """
    module = _normalize_module(module)
    testsrc = testsource(module, name)
    debug_script(testsrc, pm, module.__dict__)


class _TestClass:
    __doc__ = "\n    A pointless class, for sanity-checking of docstring testing.\n\n    Methods:\n        square()\n        get()\n\n    >>> _TestClass(13).get() + _TestClass(-12).get()\n    1\n    >>> hex(_TestClass(13).square().get())\n    '0xa9'\n    "

    def __init__(self, val):
        """val -> _TestClass object with associated value val.

        >>> t = _TestClass(123)
        >>> print(t.get())
        123
        """
        self.val = val

    def square(self):
        """square() -> square TestClass's associated value

        >>> _TestClass(13).square().get()
        169
        """
        self.val = self.val ** 2
        return self

    def get(self):
        """get() -> return TestClass's associated value.

        >>> x = _TestClass(-42)
        >>> print(x.get())
        -42
        """
        return self.val


__test__ = {'_TestClass':_TestClass, 
 'string':'\n                      Example of a string object, searched as-is.\n                      >>> x = 1; y = 2\n                      >>> x + y, x * y\n                      (3, 2)\n                      ', 
 'bool-int equivalence':'\n                                    In 2.2, boolean expressions displayed\n                                    0 or 1.  By default, we still accept\n                                    them.  This can be disabled by passing\n                                    DONT_ACCEPT_TRUE_FOR_1 to the new\n                                    optionflags argument.\n                                    >>> 4 == 4\n                                    1\n                                    >>> 4 == 4\n                                    True\n                                    >>> 4 > 4\n                                    0\n                                    >>> 4 > 4\n                                    False\n                                    ', 
 'blank lines':"\n                Blank lines can be marked with <BLANKLINE>:\n                    >>> print('foo\\n\\nbar\\n')\n                    foo\n                    <BLANKLINE>\n                    bar\n                    <BLANKLINE>\n            ", 
 'ellipsis':"\n                If the ellipsis flag is used, then '...' can be used to\n                elide substrings in the desired output:\n                    >>> print(list(range(1000))) #doctest: +ELLIPSIS\n                    [0, 1, 2, ..., 999]\n            ", 
 'whitespace normalization':'\n                If the whitespace normalization flag is used, then\n                differences in whitespace are ignored.\n                    >>> print(list(range(30))) #doctest: +NORMALIZE_WHITESPACE\n                    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,\n                     15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,\n                     27, 28, 29]\n            '}

def _test():
    import argparse
    parser = argparse.ArgumentParser(description='doctest runner')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print very verbose output for all tests')
    parser.add_argument('-o', '--option', action='append', choices=(OPTIONFLAGS_BY_NAME.keys),
      default=[],
      help='specify a doctest option flag to apply to the test run; may be specified more than once to apply multiple options')
    parser.add_argument('-f', '--fail-fast', action='store_true', help='stop running tests after first failure (this is a shorthand for -o FAIL_FAST, and is in addition to any other -o options)')
    parser.add_argument('file', nargs='+', help='file containing the tests to run')
    args = parser.parse_args
    testfiles = args.file
    verbose = args.verbose
    options = 0
    for option in args.option:
        options |= OPTIONFLAGS_BY_NAME[option]
    else:
        if args.fail_fast:
            options |= FAIL_FAST
        for filename in testfiles:
            if filename.endswith('.py'):
                dirname, filename = os.path.split(filename)
                sys.path.insert(0, dirname)
                m = __import__(filename[:-3])
                del sys.path[0]
                failures, _ = testmod(m, verbose=verbose, optionflags=options)
            else:
                failures, _ = testfile(filename, module_relative=False, verbose=verbose,
                  optionflags=options)
            if failures:
                return 1
            return 0


if __name__ == '__main__':
    sys.exit(_test())