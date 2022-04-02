# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: lib2to3\refactor.py
"""Refactoring framework.

Used as a main program, this can refactor any number of files and/or
recursively descend down directories.  Imported as a module, this
provides infrastructure to write your own refactoring tool.
"""
__author__ = 'Guido van Rossum <guido@python.org>'
import io, os, pkgutil, sys, logging, operator, collections
from itertools import chain
from .pgen2 import driver, tokenize, token
from .fixer_util import find_root
from . import pytree, pygram
from . import btm_matcher as bm

def get_all_fix_names(fixer_pkg, remove_prefix=True):
    """Return a sorted list of all available fix names in the given package."""
    pkg = __import__(fixer_pkg, [], [], ['*'])
    fix_names = []
    for finder, name, ispkg in pkgutil.iter_modules(pkg.__path__):
        if name.startswith('fix_'):
            if remove_prefix:
                name = name[4:]
            else:
                fix_names.append(name)

    return fix_names


class _EveryNode(Exception):
    pass


def _get_head_types(pat):
    """ Accepts a pytree Pattern Node and returns a set
        of the pattern types which will match first. """
    if isinstance(pat, (pytree.NodePattern, pytree.LeafPattern)):
        if pat.type is None:
            raise _EveryNode
        return {pat.type}
    if isinstance(pat, pytree.NegatedPattern):
        if pat.content:
            return _get_head_types(pat.content)
        raise _EveryNode
    if isinstance(pat, pytree.WildcardPattern):
        r = set()
        for p in pat.content:
            for x in p:
                r.update(_get_head_types(x))

        return r
    raise Exception("Oh no! I don't understand pattern %s" % pat)


def _get_headnode_dict(fixer_list):
    """ Accepts a list of fixers and returns a dictionary
        of head node type --> fixer list.  """
    head_nodes = collections.defaultdict(list)
    every = []
    for fixer in fixer_list:
        if fixer.pattern:
            try:
                heads = _get_head_types(fixer.pattern)
            except _EveryNode:
                every.append(fixer)
            else:
                for node_type in heads:
                    head_nodes[node_type].append(fixer)

        else:
            if fixer._accept_type is not None:
                head_nodes[fixer._accept_type].append(fixer)
            else:
                every.append(fixer)

    for node_type in chain(pygram.python_grammar.symbol2number.values(), pygram.python_grammar.tokens):
        head_nodes[node_type].extend(every)

    return dict(head_nodes)


def get_fixers_from_package(pkg_name):
    """
    Return the fully qualified names for fixers in the package pkg_name.
    """
    return [pkg_name + '.' + fix_name for fix_name in get_all_fix_names(pkg_name, False)]


def _identity(obj):
    return obj


def _detect_future_features--- This code section failed: ---

 L. 112         0  LOAD_CONST               False
                2  STORE_FAST               'have_docstring'

 L. 113         4  LOAD_GLOBAL              tokenize
                6  LOAD_METHOD              generate_tokens
                8  LOAD_GLOBAL              io
               10  LOAD_METHOD              StringIO
               12  LOAD_FAST                'source'
               14  CALL_METHOD_1         1  '1 positional argument'
               16  LOAD_ATTR                readline
               18  CALL_METHOD_1         1  '1 positional argument'
               20  STORE_DEREF              'gen'

 L. 114        22  LOAD_CLOSURE             'gen'
               24  BUILD_TUPLE_1         1 
               26  LOAD_CODE                <code_object advance>
               28  LOAD_STR                 '_detect_future_features.<locals>.advance'
               30  MAKE_FUNCTION_8          'closure'
               32  STORE_FAST               'advance'

 L. 117        34  LOAD_GLOBAL              frozenset
               36  LOAD_GLOBAL              token
               38  LOAD_ATTR                NEWLINE
               40  LOAD_GLOBAL              tokenize
               42  LOAD_ATTR                NL
               44  LOAD_GLOBAL              token
               46  LOAD_ATTR                COMMENT
               48  BUILD_SET_3           3 
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  STORE_FAST               'ignore'

 L. 118        54  LOAD_GLOBAL              set
               56  CALL_FUNCTION_0       0  '0 positional arguments'
               58  STORE_FAST               'features'

 L. 119        60  SETUP_EXCEPT        312  'to 312'

 L. 120        62  SETUP_LOOP          308  'to 308'
             64_0  COME_FROM           304  '304'
             64_1  COME_FROM           300  '300'
             64_2  COME_FROM           106  '106'
             64_3  COME_FROM            84  '84'
             64_4  COME_FROM            82  '82'

 L. 121        64  LOAD_FAST                'advance'
               66  CALL_FUNCTION_0       0  '0 positional arguments'
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'tp'
               72  STORE_FAST               'value'

 L. 122        74  LOAD_FAST                'tp'
               76  LOAD_FAST                'ignore'
               78  COMPARE_OP               in
               80  POP_JUMP_IF_FALSE    86  'to 86'

 L. 123        82  CONTINUE             64  'to 64'
               84  JUMP_BACK            64  'to 64'
             86_0  COME_FROM            80  '80'

 L. 124        86  LOAD_FAST                'tp'
               88  LOAD_GLOBAL              token
               90  LOAD_ATTR                STRING
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   108  'to 108'

 L. 125        96  LOAD_FAST                'have_docstring'
               98  POP_JUMP_IF_FALSE   102  'to 102'

 L. 126       100  BREAK_LOOP       
            102_0  COME_FROM            98  '98'

 L. 127       102  LOAD_CONST               True
              104  STORE_FAST               'have_docstring'
              106  JUMP_BACK            64  'to 64'
            108_0  COME_FROM            94  '94'

 L. 128       108  LOAD_FAST                'tp'
              110  LOAD_GLOBAL              token
              112  LOAD_ATTR                NAME
              114  COMPARE_OP               ==
          116_118  POP_JUMP_IF_FALSE   302  'to 302'
              120  LOAD_FAST                'value'
              122  LOAD_STR                 'from'
              124  COMPARE_OP               ==
          126_128  POP_JUMP_IF_FALSE   302  'to 302'

 L. 129       130  LOAD_FAST                'advance'
              132  CALL_FUNCTION_0       0  '0 positional arguments'
              134  UNPACK_SEQUENCE_2     2 
              136  STORE_FAST               'tp'
              138  STORE_FAST               'value'

 L. 130       140  LOAD_FAST                'tp'
              142  LOAD_GLOBAL              token
              144  LOAD_ATTR                NAME
              146  COMPARE_OP               !=
              148  POP_JUMP_IF_TRUE    158  'to 158'
              150  LOAD_FAST                'value'
              152  LOAD_STR                 '__future__'
              154  COMPARE_OP               !=
              156  POP_JUMP_IF_FALSE   160  'to 160'
            158_0  COME_FROM           148  '148'

 L. 131       158  BREAK_LOOP       
            160_0  COME_FROM           156  '156'

 L. 132       160  LOAD_FAST                'advance'
              162  CALL_FUNCTION_0       0  '0 positional arguments'
              164  UNPACK_SEQUENCE_2     2 
              166  STORE_FAST               'tp'
              168  STORE_FAST               'value'

 L. 133       170  LOAD_FAST                'tp'
              172  LOAD_GLOBAL              token
              174  LOAD_ATTR                NAME
              176  COMPARE_OP               !=
              178  POP_JUMP_IF_TRUE    188  'to 188'
              180  LOAD_FAST                'value'
              182  LOAD_STR                 'import'
              184  COMPARE_OP               !=
              186  POP_JUMP_IF_FALSE   190  'to 190'
            188_0  COME_FROM           178  '178'

 L. 134       188  BREAK_LOOP       
            190_0  COME_FROM           186  '186'

 L. 135       190  LOAD_FAST                'advance'
              192  CALL_FUNCTION_0       0  '0 positional arguments'
              194  UNPACK_SEQUENCE_2     2 
              196  STORE_FAST               'tp'
              198  STORE_FAST               'value'

 L. 136       200  LOAD_FAST                'tp'
              202  LOAD_GLOBAL              token
              204  LOAD_ATTR                OP
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   228  'to 228'
              210  LOAD_FAST                'value'
              212  LOAD_STR                 '('
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE   228  'to 228'

 L. 137       218  LOAD_FAST                'advance'
              220  CALL_FUNCTION_0       0  '0 positional arguments'
              222  UNPACK_SEQUENCE_2     2 
              224  STORE_FAST               'tp'
              226  STORE_FAST               'value'
            228_0  COME_FROM           216  '216'
            228_1  COME_FROM           208  '208'

 L. 138       228  SETUP_LOOP          304  'to 304'
            230_0  COME_FROM           296  '296'
              230  LOAD_FAST                'tp'
              232  LOAD_GLOBAL              token
              234  LOAD_ATTR                NAME
              236  COMPARE_OP               ==
          238_240  POP_JUMP_IF_FALSE   298  'to 298'

 L. 139       242  LOAD_FAST                'features'
              244  LOAD_METHOD              add
              246  LOAD_FAST                'value'
              248  CALL_METHOD_1         1  '1 positional argument'
              250  POP_TOP          

 L. 140       252  LOAD_FAST                'advance'
              254  CALL_FUNCTION_0       0  '0 positional arguments'
              256  UNPACK_SEQUENCE_2     2 
              258  STORE_FAST               'tp'
              260  STORE_FAST               'value'

 L. 141       262  LOAD_FAST                'tp'
              264  LOAD_GLOBAL              token
              266  LOAD_ATTR                OP
              268  COMPARE_OP               !=
          270_272  POP_JUMP_IF_TRUE    284  'to 284'
              274  LOAD_FAST                'value'
              276  LOAD_STR                 ','
              278  COMPARE_OP               !=
          280_282  POP_JUMP_IF_FALSE   286  'to 286'
            284_0  COME_FROM           270  '270'

 L. 142       284  BREAK_LOOP       
            286_0  COME_FROM           280  '280'

 L. 143       286  LOAD_FAST                'advance'
              288  CALL_FUNCTION_0       0  '0 positional arguments'
              290  UNPACK_SEQUENCE_2     2 
              292  STORE_FAST               'tp'
              294  STORE_FAST               'value'
              296  JUMP_BACK           230  'to 230'
            298_0  COME_FROM           238  '238'
              298  POP_BLOCK        
              300  JUMP_BACK            64  'to 64'
            302_0  COME_FROM           126  '126'
            302_1  COME_FROM           116  '116'

 L. 145       302  BREAK_LOOP       
            304_0  COME_FROM_LOOP      228  '228'
              304  JUMP_BACK            64  'to 64'
              306  POP_BLOCK        
            308_0  COME_FROM_LOOP       62  '62'
              308  POP_BLOCK        
              310  JUMP_FORWARD        334  'to 334'
            312_0  COME_FROM_EXCEPT     60  '60'

 L. 146       312  DUP_TOP          
              314  LOAD_GLOBAL              StopIteration
              316  COMPARE_OP               exception-match
          318_320  POP_JUMP_IF_FALSE   332  'to 332'
              322  POP_TOP          
              324  POP_TOP          
              326  POP_TOP          

 L. 147       328  POP_EXCEPT       
              330  JUMP_FORWARD        334  'to 334'
            332_0  COME_FROM           318  '318'
              332  END_FINALLY      
            334_0  COME_FROM           330  '330'
            334_1  COME_FROM           310  '310'

 L. 148       334  LOAD_GLOBAL              frozenset
              336  LOAD_FAST                'features'
              338  CALL_FUNCTION_1       1  '1 positional argument'
              340  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 300


class FixerError(Exception):
    __doc__ = 'A fixer could not be loaded.'


class RefactoringTool(object):
    _default_options = {'print_function':False, 
     'write_unchanged_files':False}
    CLASS_PREFIX = 'Fix'
    FILE_PREFIX = 'fix_'

    def __init__(self, fixer_names, options=None, explicit=None):
        """Initializer.

        Args:
            fixer_names: a list of fixers to import
            options: a dict with configuration.
            explicit: a list of fixers to run even if they are explicit.
        """
        self.fixers = fixer_names
        self.explicit = explicit or []
        self.options = self._default_options.copy()
        if options is not None:
            self.options.update(options)
        if self.options['print_function']:
            self.grammar = pygram.python_grammar_no_print_statement
        else:
            self.grammar = pygram.python_grammar
        self.write_unchanged_files = self.options.get('write_unchanged_files')
        self.errors = []
        self.logger = logging.getLogger('RefactoringTool')
        self.fixer_log = []
        self.wrote = False
        self.driver = driver.Driver((self.grammar), convert=(pytree.convert),
          logger=(self.logger))
        self.pre_order, self.post_order = self.get_fixers()
        self.files = []
        self.BM = bm.BottomMatcher()
        self.bmi_pre_order = []
        self.bmi_post_order = []
        for fixer in chain(self.post_order, self.pre_order):
            if fixer.BM_compatible:
                self.BM.add_fixer(fixer)
            else:
                if fixer in self.pre_order:
                    self.bmi_pre_order.append(fixer)
            if fixer in self.post_order:
                self.bmi_post_order.append(fixer)

        self.bmi_pre_order_heads = _get_headnode_dict(self.bmi_pre_order)
        self.bmi_post_order_heads = _get_headnode_dict(self.bmi_post_order)

    def get_fixers(self):
        """Inspects the options to load the requested patterns and handlers.

        Returns:
          (pre_order, post_order), where pre_order is the list of fixers that
          want a pre-order AST traversal, and post_order is the list that want
          post-order traversal.
        """
        pre_order_fixers = []
        post_order_fixers = []
        for fix_mod_path in self.fixers:
            mod = __import__(fix_mod_path, {}, {}, ['*'])
            fix_name = fix_mod_path.rsplit('.', 1)[(-1)]
            if fix_name.startswith(self.FILE_PREFIX):
                fix_name = fix_name[len(self.FILE_PREFIX):]
            parts = fix_name.split('_')
            class_name = self.CLASS_PREFIX + ''.join([p.title() for p in parts])
            try:
                fix_class = getattr(mod, class_name)
            except AttributeError:
                raise FixerError("Can't find %s.%s" % (fix_name, class_name)) from None

            fixer = fix_class(self.options, self.fixer_log)
            if fixer.explicit:
                if self.explicit is not True:
                    if fix_mod_path not in self.explicit:
                        self.log_message('Skipping optional fixer: %s', fix_name)
                        continue
            self.log_debug('Adding transformation: %s', fix_name)
            if fixer.order == 'pre':
                pre_order_fixers.append(fixer)
            else:
                if fixer.order == 'post':
                    post_order_fixers.append(fixer)
                else:
                    raise FixerError('Illegal fixer order: %r' % fixer.order)

        key_func = operator.attrgetter('run_order')
        pre_order_fixers.sort(key=key_func)
        post_order_fixers.sort(key=key_func)
        return (
         pre_order_fixers, post_order_fixers)

    def log_error(self, msg, *args, **kwds):
        """Called when an error occurs."""
        raise

    def log_message(self, msg, *args):
        """Hook to log a message."""
        if args:
            msg = msg % args
        self.logger.info(msg)

    def log_debug(self, msg, *args):
        if args:
            msg = msg % args
        self.logger.debug(msg)

    def print_output(self, old_text, new_text, filename, equal):
        """Called with the old version, new version, and filename of a
        refactored file."""
        pass

    def refactor(self, items, write=False, doctests_only=False):
        """Refactor a list of files and directories."""
        for dir_or_file in items:
            if os.path.isdir(dir_or_file):
                self.refactor_dir(dir_or_file, write, doctests_only)
            else:
                self.refactor_file(dir_or_file, write, doctests_only)

    def refactor_dir(self, dir_name, write=False, doctests_only=False):
        """Descends down a directory and refactor every Python file found.

        Python files are assumed to have a .py extension.

        Files and subdirectories starting with '.' are skipped.
        """
        py_ext = os.extsep + 'py'
        for dirpath, dirnames, filenames in os.walk(dir_name):
            self.log_debug('Descending into %s', dirpath)
            dirnames.sort()
            filenames.sort()
            for name in filenames:
                if not name.startswith('.'):
                    if os.path.splitext(name)[1] == py_ext:
                        fullname = os.path.join(dirpath, name)
                        self.refactor_file(fullname, write, doctests_only)

            dirnames[:] = [dn for dn in dirnames if not dn.startswith('.')]

    def _read_python_source(self, filename):
        """
        Do our best to decode a Python source file correctly.
        """
        try:
            f = open(filename, 'rb')
        except OSError as err:
            try:
                self.log_error("Can't open %s: %s", filename, err)
                return (None, None)
            finally:
                err = None
                del err

        try:
            encoding = tokenize.detect_encoding(f.readline)[0]
        finally:
            f.close()

        with io.open(filename, 'r', encoding=encoding, newline='') as f:
            return (f.read(), encoding)

    def refactor_file--- This code section failed: ---

 L. 322         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _read_python_source
                4  LOAD_FAST                'filename'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'input'
               12  STORE_FAST               'encoding'

 L. 323        14  LOAD_FAST                'input'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 325        22  LOAD_CONST               None
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 326        26  LOAD_FAST                'input'
               28  LOAD_STR                 '\n'
               30  INPLACE_ADD      
               32  STORE_FAST               'input'

 L. 327        34  LOAD_FAST                'doctests_only'
               36  POP_JUMP_IF_FALSE   110  'to 110'

 L. 328        38  LOAD_FAST                'self'
               40  LOAD_METHOD              log_debug
               42  LOAD_STR                 'Refactoring doctests in %s'
               44  LOAD_FAST                'filename'
               46  CALL_METHOD_2         2  '2 positional arguments'
               48  POP_TOP          

 L. 329        50  LOAD_FAST                'self'
               52  LOAD_METHOD              refactor_docstring
               54  LOAD_FAST                'input'
               56  LOAD_FAST                'filename'
               58  CALL_METHOD_2         2  '2 positional arguments'
               60  STORE_FAST               'output'

 L. 330        62  LOAD_FAST                'self'
               64  LOAD_ATTR                write_unchanged_files
               66  POP_JUMP_IF_TRUE     76  'to 76'
               68  LOAD_FAST                'output'
               70  LOAD_FAST                'input'
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_FALSE    96  'to 96'
             76_0  COME_FROM            66  '66'

 L. 331        76  LOAD_FAST                'self'
               78  LOAD_METHOD              processed_file
               80  LOAD_FAST                'output'
               82  LOAD_FAST                'filename'
               84  LOAD_FAST                'input'
               86  LOAD_FAST                'write'
               88  LOAD_FAST                'encoding'
               90  CALL_METHOD_5         5  '5 positional arguments'
               92  POP_TOP          
               94  JUMP_FORWARD        182  'to 182'
             96_0  COME_FROM            74  '74'

 L. 333        96  LOAD_FAST                'self'
               98  LOAD_METHOD              log_debug
              100  LOAD_STR                 'No doctest changes in %s'
              102  LOAD_FAST                'filename'
              104  CALL_METHOD_2         2  '2 positional arguments'
              106  POP_TOP          
              108  JUMP_FORWARD        182  'to 182'
            110_0  COME_FROM            36  '36'

 L. 335       110  LOAD_FAST                'self'
              112  LOAD_METHOD              refactor_string
              114  LOAD_FAST                'input'
              116  LOAD_FAST                'filename'
              118  CALL_METHOD_2         2  '2 positional arguments'
              120  STORE_FAST               'tree'

 L. 336       122  LOAD_FAST                'self'
              124  LOAD_ATTR                write_unchanged_files
              126  POP_JUMP_IF_TRUE    138  'to 138'
              128  LOAD_FAST                'tree'
              130  POP_JUMP_IF_FALSE   170  'to 170'
              132  LOAD_FAST                'tree'
              134  LOAD_ATTR                was_changed
              136  POP_JUMP_IF_FALSE   170  'to 170'
            138_0  COME_FROM           126  '126'

 L. 338       138  LOAD_FAST                'self'
              140  LOAD_ATTR                processed_file
              142  LOAD_GLOBAL              str
              144  LOAD_FAST                'tree'
              146  CALL_FUNCTION_1       1  '1 positional argument'
              148  LOAD_CONST               None
              150  LOAD_CONST               -1
              152  BUILD_SLICE_2         2 
              154  BINARY_SUBSCR    
              156  LOAD_FAST                'filename'

 L. 339       158  LOAD_FAST                'write'
              160  LOAD_FAST                'encoding'
              162  LOAD_CONST               ('write', 'encoding')
              164  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              166  POP_TOP          
              168  JUMP_FORWARD        182  'to 182'
            170_0  COME_FROM           136  '136'
            170_1  COME_FROM           130  '130'

 L. 341       170  LOAD_FAST                'self'
              172  LOAD_METHOD              log_debug
              174  LOAD_STR                 'No changes in %s'
              176  LOAD_FAST                'filename'
              178  CALL_METHOD_2         2  '2 positional arguments'
              180  POP_TOP          
            182_0  COME_FROM           168  '168'
            182_1  COME_FROM           108  '108'
            182_2  COME_FROM            94  '94'

Parse error at or near `COME_FROM' instruction at offset 182_1

    def refactor_string(self, data, name):
        """Refactor a given input string.

        Args:
            data: a string holding the code to be refactored.
            name: a human-readable name for use in error/log messages.

        Returns:
            An AST corresponding to the refactored input stream; None if
            there were errors during the parse.
        """
        features = _detect_future_features(data)
        if 'print_function' in features:
            self.driver.grammar = pygram.python_grammar_no_print_statement
        try:
            try:
                tree = self.driver.parse_string(data)
            except Exception as err:
                try:
                    self.log_error("Can't parse %s: %s: %s", name, err.__class__.__name__, err)
                    return
                finally:
                    err = None
                    del err

        finally:
            self.driver.grammar = self.grammar

        tree.future_features = features
        self.log_debug('Refactoring %s', name)
        self.refactor_tree(tree, name)
        return tree

    def refactor_stdin--- This code section failed: ---

 L. 371         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                stdin
                4  LOAD_METHOD              read
                6  CALL_METHOD_0         0  '0 positional arguments'
                8  STORE_FAST               'input'

 L. 372        10  LOAD_FAST                'doctests_only'
               12  POP_JUMP_IF_FALSE    78  'to 78'

 L. 373        14  LOAD_FAST                'self'
               16  LOAD_METHOD              log_debug
               18  LOAD_STR                 'Refactoring doctests in stdin'
               20  CALL_METHOD_1         1  '1 positional argument'
               22  POP_TOP          

 L. 374        24  LOAD_FAST                'self'
               26  LOAD_METHOD              refactor_docstring
               28  LOAD_FAST                'input'
               30  LOAD_STR                 '<stdin>'
               32  CALL_METHOD_2         2  '2 positional arguments'
               34  STORE_FAST               'output'

 L. 375        36  LOAD_FAST                'self'
               38  LOAD_ATTR                write_unchanged_files
               40  POP_JUMP_IF_TRUE     50  'to 50'
               42  LOAD_FAST                'output'
               44  LOAD_FAST                'input'
               46  COMPARE_OP               !=
               48  POP_JUMP_IF_FALSE    66  'to 66'
             50_0  COME_FROM            40  '40'

 L. 376        50  LOAD_FAST                'self'
               52  LOAD_METHOD              processed_file
               54  LOAD_FAST                'output'
               56  LOAD_STR                 '<stdin>'
               58  LOAD_FAST                'input'
               60  CALL_METHOD_3         3  '3 positional arguments'
               62  POP_TOP          
               64  JUMP_FORWARD        136  'to 136'
             66_0  COME_FROM            48  '48'

 L. 378        66  LOAD_FAST                'self'
               68  LOAD_METHOD              log_debug
               70  LOAD_STR                 'No doctest changes in stdin'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  POP_TOP          
               76  JUMP_FORWARD        136  'to 136'
             78_0  COME_FROM            12  '12'

 L. 380        78  LOAD_FAST                'self'
               80  LOAD_METHOD              refactor_string
               82  LOAD_FAST                'input'
               84  LOAD_STR                 '<stdin>'
               86  CALL_METHOD_2         2  '2 positional arguments'
               88  STORE_FAST               'tree'

 L. 381        90  LOAD_FAST                'self'
               92  LOAD_ATTR                write_unchanged_files
               94  POP_JUMP_IF_TRUE    106  'to 106'
               96  LOAD_FAST                'tree'
               98  POP_JUMP_IF_FALSE   126  'to 126'
              100  LOAD_FAST                'tree'
              102  LOAD_ATTR                was_changed
              104  POP_JUMP_IF_FALSE   126  'to 126'
            106_0  COME_FROM            94  '94'

 L. 382       106  LOAD_FAST                'self'
              108  LOAD_METHOD              processed_file
              110  LOAD_GLOBAL              str
              112  LOAD_FAST                'tree'
              114  CALL_FUNCTION_1       1  '1 positional argument'
              116  LOAD_STR                 '<stdin>'
              118  LOAD_FAST                'input'
              120  CALL_METHOD_3         3  '3 positional arguments'
              122  POP_TOP          
              124  JUMP_FORWARD        136  'to 136'
            126_0  COME_FROM           104  '104'
            126_1  COME_FROM            98  '98'

 L. 384       126  LOAD_FAST                'self'
              128  LOAD_METHOD              log_debug
              130  LOAD_STR                 'No changes in stdin'
              132  CALL_METHOD_1         1  '1 positional argument'
              134  POP_TOP          
            136_0  COME_FROM           124  '124'
            136_1  COME_FROM            76  '76'
            136_2  COME_FROM            64  '64'

Parse error at or near `COME_FROM' instruction at offset 136_1

    def refactor_tree(self, tree, name):
        """Refactors a parse tree (modifying the tree in place).

        For compatible patterns the bottom matcher module is
        used. Otherwise the tree is traversed node-to-node for
        matches.

        Args:
            tree: a pytree.Node instance representing the root of the tree
                  to be refactored.
            name: a human-readable name for this tree.

        Returns:
            True if the tree was modified, False otherwise.
        """
        for fixer in chain(self.pre_order, self.post_order):
            fixer.start_tree(tree, name)

        self.traverse_by(self.bmi_pre_order_heads, tree.pre_order())
        self.traverse_by(self.bmi_post_order_heads, tree.post_order())
        match_set = self.BM.run(tree.leaves())
        while any(match_set.values()):
            for fixer in self.BM.fixers:
                if fixer in match_set:
                    if match_set[fixer]:
                        match_set[fixer].sort(key=(pytree.Base.depth), reverse=True)
                        if fixer.keep_line_order:
                            match_set[fixer].sort(key=(pytree.Base.get_lineno))
                        else:
                            for node in list(match_set[fixer]):
                                if node in match_set[fixer]:
                                    match_set[fixer].remove(node)
                                else:
                                    try:
                                        find_root(node)
                                    except ValueError:
                                        continue

                                if node.fixers_applied:
                                    if fixer in node.fixers_applied:
                                        continue
                                results = fixer.match(node)
                                if results:
                                    new = fixer.transform(node, results)
                                    if new is not None:
                                        node.replace(new)
                                        for node in new.post_order():
                                            if not node.fixers_applied:
                                                node.fixers_applied = []
                                            else:
                                                node.fixers_applied.append(fixer)

                                        new_matches = self.BM.run(new.leaves())
                                        for fxr in new_matches:
                                            if fxr not in match_set:
                                                match_set[fxr] = []
                                            else:
                                                match_set[fxr].extend(new_matches[fxr])

        for fixer in chain(self.pre_order, self.post_order):
            fixer.finish_tree(tree, name)

        return tree.was_changed

    def traverse_by(self, fixers, traversal):
        """Traverse an AST, applying a set of fixers to each node.

        This is a helper method for refactor_tree().

        Args:
            fixers: a list of fixer instances.
            traversal: a generator that yields AST nodes.

        Returns:
            None
        """
        if not fixers:
            return
        for node in traversal:
            for fixer in fixers[node.type]:
                results = fixer.match(node)
                if results:
                    new = fixer.transform(node, results)
                    if new is not None:
                        node.replace(new)
                        node = new

    def processed_file(self, new_text, filename, old_text=None, write=False, encoding=None):
        """
        Called when a file has been refactored and there may be changes.
        """
        self.files.append(filename)
        if old_text is None:
            old_text = self._read_python_source(filename)[0]
            if old_text is None:
                return
        equal = old_text == new_text
        self.print_output(old_text, new_text, filename, equal)
        if equal:
            self.log_debug('No changes to %s', filename)
            if not self.write_unchanged_files:
                return
        if write:
            self.write_file(new_text, filename, old_text, encoding)
        else:
            self.log_debug('Not writing changes to %s', filename)

    def write_file(self, new_text, filename, old_text, encoding=None):
        """Writes a string to a file.

        It first shows a unified diff between the old text and the new text, and
        then rewrites the file; the latter is only done if the write option is
        set.
        """
        try:
            fp = io.open(filename, 'w', encoding=encoding, newline='')
        except OSError as err:
            try:
                self.log_error("Can't create %s: %s", filename, err)
                return
            finally:
                err = None
                del err

        with fp:
            try:
                fp.write(new_text)
            except OSError as err:
                try:
                    self.log_error("Can't write %s: %s", filename, err)
                finally:
                    err = None
                    del err

        self.log_debug('Wrote changes to %s', filename)
        self.wrote = True

    PS1 = '>>> '
    PS2 = '... '

    def refactor_docstring(self, input, filename):
        """Refactors a docstring, looking for doctests.

        This returns a modified version of the input string.  It looks
        for doctests, which start with a ">>>" prompt, and may be
        continued with "..." prompts, as long as the "..." is indented
        the same as the ">>>".

        (Unfortunately we can't use the doctest module's parser,
        since, like most parsers, it is not geared towards preserving
        the original source.)
        """
        result = []
        block = None
        block_lineno = None
        indent = None
        lineno = 0
        for line in input.splitlines(keepends=True):
            lineno += 1
            if line.lstrip().startswith(self.PS1):
                if block is not None:
                    result.extend(self.refactor_doctest(block, block_lineno, indent, filename))
                else:
                    block_lineno = lineno
                    block = [line]
                    i = line.find(self.PS1)
                    indent = line[:i]
            else:
                if not indent is not None or line.startswith(indent + self.PS2) or line == indent + self.PS2.rstrip() + '\n':
                    block.append(line)
                else:
                    if block is not None:
                        result.extend(self.refactor_doctest(block, block_lineno, indent, filename))
                    block = None
                    indent = None
                    result.append(line)

        if block is not None:
            result.extend(self.refactor_doctest(block, block_lineno, indent, filename))
        return ''.join(result)

    def refactor_doctest(self, block, lineno, indent, filename):
        """Refactors one doctest.

        A doctest is given as a block of lines, the first of which starts
        with ">>>" (possibly indented), while the remaining lines start
        with "..." (identically indented).

        """
        try:
            tree = self.parse_block(block, lineno, indent)
        except Exception as err:
            try:
                if self.logger.isEnabledFor(logging.DEBUG):
                    for line in block:
                        self.log_debug('Source: %s', line.rstrip('\n'))

                self.log_error"Can't parse docstring in %s line %s: %s: %s"filenamelinenoerr.__class__.__name__err
                return block
            finally:
                err = None
                del err

        if self.refactor_tree(tree, filename):
            new = str(tree).splitlines(keepends=True)
            clipped, new = new[:lineno - 1], new[lineno - 1:]
            assert clipped == ['\n'] * (lineno - 1), clipped
            if not new[(-1)].endswith('\n'):
                new[(-1)] += '\n'
            block = [
             indent + self.PS1 + new.pop(0)]
            if new:
                block += [indent + self.PS2 + line for line in new]
        return block

    def summarize(self):
        if self.wrote:
            were = 'were'
        else:
            were = 'need to be'
        if not self.files:
            self.log_message('No files %s modified.', were)
        else:
            self.log_message('Files that %s modified:', were)
            for file in self.files:
                self.log_message(file)

        if self.fixer_log:
            self.log_message('Warnings/messages while refactoring:')
            for message in self.fixer_log:
                self.log_message(message)

        if self.errors:
            if len(self.errors) == 1:
                self.log_message('There was 1 error:')
            else:
                self.log_message('There were %d errors:', len(self.errors))
            for msg, args, kwds in self.errors:
                (self.log_message)(msg, *args, **kwds)

    def parse_block(self, block, lineno, indent):
        """Parses a block into a tree.

        This is necessary to get correct line number / offset information
        in the parser diagnostics and embedded into the parse tree.
        """
        tree = self.driver.parse_tokens(self.wrap_toks(block, lineno, indent))
        tree.future_features = frozenset()
        return tree

    def wrap_toks(self, block, lineno, indent):
        """Wraps a tokenize stream to systematically modify start/end."""
        tokens = tokenize.generate_tokens(self.gen_lines(block, indent).__next__)
        for type, value, (line0, col0), (line1, col1), line_text in tokens:
            line0 += lineno - 1
            line1 += lineno - 1
            yield (
             type, value, (line0, col0), (line1, col1), line_text)

    def gen_lines(self, block, indent):
        """Generates lines as expected by tokenize from a list of lines.

        This strips the first len(indent + self.PS1) characters off each line.
        """
        prefix1 = indent + self.PS1
        prefix2 = indent + self.PS2
        prefix = prefix1
        for line in block:
            if line.startswith(prefix):
                yield line[len(prefix):]
            elif line == prefix.rstrip() + '\n':
                yield '\n'
            else:
                raise AssertionError('line=%r, prefix=%r' % (line, prefix))
            prefix = prefix2

        while True:
            yield ''


class MultiprocessingUnsupported(Exception):
    pass


class MultiprocessRefactoringTool(RefactoringTool):

    def __init__(self, *args, **kwargs):
        (super(MultiprocessRefactoringTool, self).__init__)(*args, **kwargs)
        self.queue = None
        self.output_lock = None

    def refactor(self, items, write=False, doctests_only=False, num_processes=1):
        if num_processes == 1:
            return super(MultiprocessRefactoringTool, self).refactor(items, write, doctests_only)
        try:
            import multiprocessing
        except ImportError:
            raise MultiprocessingUnsupported

        if self.queue is not None:
            raise RuntimeError('already doing multiple processes')
        self.queue = multiprocessing.JoinableQueue()
        self.output_lock = multiprocessing.Lock()
        processes = [multiprocessing.Process(target=(self._child)) for i in range(num_processes)]
        try:
            for p in processes:
                p.start()

            super(MultiprocessRefactoringTool, self).refactor(items, write, doctests_only)
        finally:
            self.queue.join()
            for i in range(num_processes):
                self.queue.put(None)

            for p in processes:
                if p.is_alive():
                    p.join()

            self.queue = None

    def _child(self):
        task = self.queue.get()
        while task is not None:
            args, kwargs = task
            try:
                (super(MultiprocessRefactoringTool, self).refactor_file)(*args, **kwargs)
            finally:
                self.queue.task_done()

            task = self.queue.get()

    def refactor_file(self, *args, **kwargs):
        if self.queue is not None:
            self.queue.put((args, kwargs))
        else:
            return (super(MultiprocessRefactoringTool, self).refactor_file)(*args, **kwargs)