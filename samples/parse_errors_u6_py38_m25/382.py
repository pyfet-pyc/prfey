# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
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
        return {
         pat.type}
    if isinstance(pat, pytree.NegatedPattern):
        if pat.content:
            return _get_head_types(pat.content)
        raise _EveryNode
    if isinstance(pat, pytree.WildcardPattern):
        r = set()
        for p in pat.content:
            for x in p:
                r.update(_get_head_types(x))
            else:
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

        elif fixer._accept_type is not None:
            head_nodes[fixer._accept_type].append(fixer)
        else:
            every.append(fixer)
    else:
        for node_type in chain(pygram.python_grammar.symbol2number.values(), pygram.python_grammar.tokens):
            head_nodes[node_type].extend(every)
        else:
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
               14  CALL_METHOD_1         1  ''
               16  LOAD_ATTR                readline
               18  CALL_METHOD_1         1  ''
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
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'ignore'

 L. 118        54  LOAD_GLOBAL              set
               56  CALL_FUNCTION_0       0  ''
               58  STORE_FAST               'features'

 L. 119        60  SETUP_FINALLY       314  'to 314'

 L. 121        62  LOAD_FAST                'advance'
               64  CALL_FUNCTION_0       0  ''
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               'tp'
               70  STORE_FAST               'value'

 L. 122        72  LOAD_FAST                'tp'
               74  LOAD_FAST                'ignore'
               76  COMPARE_OP               in
               78  POP_JUMP_IF_FALSE    84  'to 84'

 L. 123        80  CONTINUE             62  'to 62'
               82  JUMP_BACK            62  'to 62'
             84_0  COME_FROM            78  '78'

 L. 124        84  LOAD_FAST                'tp'
               86  LOAD_GLOBAL              token
               88  LOAD_ATTR                STRING
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   108  'to 108'

 L. 125        94  LOAD_FAST                'have_docstring'
               96  POP_JUMP_IF_FALSE   102  'to 102'

 L. 126    98_100  BREAK_LOOP          310  'to 310'
            102_0  COME_FROM            96  '96'

 L. 127       102  LOAD_CONST               True
              104  STORE_FAST               'have_docstring'
              106  JUMP_BACK            62  'to 62'
            108_0  COME_FROM            92  '92'

 L. 128       108  LOAD_FAST                'tp'
              110  LOAD_GLOBAL              token
              112  LOAD_ATTR                NAME
              114  COMPARE_OP               ==
          116_118  POP_JUMP_IF_FALSE   310  'to 310'
              120  LOAD_FAST                'value'
              122  LOAD_STR                 'from'
              124  COMPARE_OP               ==
          126_128  POP_JUMP_IF_FALSE   310  'to 310'

 L. 129       130  LOAD_FAST                'advance'
              132  CALL_FUNCTION_0       0  ''
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
              156  POP_JUMP_IF_FALSE   162  'to 162'
            158_0  COME_FROM           148  '148'

 L. 131   158_160  BREAK_LOOP          310  'to 310'
            162_0  COME_FROM           156  '156'

 L. 132       162  LOAD_FAST                'advance'
              164  CALL_FUNCTION_0       0  ''
              166  UNPACK_SEQUENCE_2     2 
              168  STORE_FAST               'tp'
              170  STORE_FAST               'value'

 L. 133       172  LOAD_FAST                'tp'
              174  LOAD_GLOBAL              token
              176  LOAD_ATTR                NAME
              178  COMPARE_OP               !=
              180  POP_JUMP_IF_TRUE    190  'to 190'
              182  LOAD_FAST                'value'
              184  LOAD_STR                 'import'
              186  COMPARE_OP               !=
              188  POP_JUMP_IF_FALSE   194  'to 194'
            190_0  COME_FROM           180  '180'

 L. 134   190_192  BREAK_LOOP          310  'to 310'
            194_0  COME_FROM           188  '188'

 L. 135       194  LOAD_FAST                'advance'
              196  CALL_FUNCTION_0       0  ''
              198  UNPACK_SEQUENCE_2     2 
              200  STORE_FAST               'tp'
              202  STORE_FAST               'value'

 L. 136       204  LOAD_FAST                'tp'
              206  LOAD_GLOBAL              token
              208  LOAD_ATTR                OP
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   232  'to 232'
              214  LOAD_FAST                'value'
              216  LOAD_STR                 '('
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_FALSE   232  'to 232'

 L. 137       222  LOAD_FAST                'advance'
              224  CALL_FUNCTION_0       0  ''
              226  UNPACK_SEQUENCE_2     2 
              228  STORE_FAST               'tp'
              230  STORE_FAST               'value'
            232_0  COME_FROM           220  '220'
            232_1  COME_FROM           212  '212'

 L. 138       232  LOAD_FAST                'tp'
              234  LOAD_GLOBAL              token
              236  LOAD_ATTR                NAME
              238  COMPARE_OP               ==
          240_242  POP_JUMP_IF_FALSE   308  'to 308'

 L. 139       244  LOAD_FAST                'features'
              246  LOAD_METHOD              add
              248  LOAD_FAST                'value'
              250  CALL_METHOD_1         1  ''
              252  POP_TOP          

 L. 140       254  LOAD_FAST                'advance'
              256  CALL_FUNCTION_0       0  ''
              258  UNPACK_SEQUENCE_2     2 
              260  STORE_FAST               'tp'
              262  STORE_FAST               'value'

 L. 141       264  LOAD_FAST                'tp'
              266  LOAD_GLOBAL              token
              268  LOAD_ATTR                OP
              270  COMPARE_OP               !=
          272_274  POP_JUMP_IF_TRUE    302  'to 302'
              276  LOAD_FAST                'value'
              278  LOAD_STR                 ','
              280  COMPARE_OP               !=
          282_284  POP_JUMP_IF_FALSE   290  'to 290'

 L. 142   286_288  BREAK_LOOP          308  'to 308'
            290_0  COME_FROM           282  '282'

 L. 143       290  LOAD_FAST                'advance'
              292  CALL_FUNCTION_0       0  ''
              294  UNPACK_SEQUENCE_2     2 
              296  STORE_FAST               'tp'
              298  STORE_FAST               'value'
              300  JUMP_BACK           232  'to 232'
            302_0  COME_FROM           272  '272'
              302  JUMP_BACK            62  'to 62'

 L. 145   304_306  BREAK_LOOP          310  'to 310'
            308_0  COME_FROM           240  '240'
              308  JUMP_BACK            62  'to 62'
            310_0  COME_FROM           126  '126'
            310_1  COME_FROM           116  '116'
              310  POP_BLOCK        
              312  JUMP_FORWARD        336  'to 336'
            314_0  COME_FROM_FINALLY    60  '60'

 L. 146       314  DUP_TOP          
              316  LOAD_GLOBAL              StopIteration
              318  COMPARE_OP               exception-match
          320_322  POP_JUMP_IF_FALSE   334  'to 334'
              324  POP_TOP          
              326  POP_TOP          
              328  POP_TOP          

 L. 147       330  POP_EXCEPT       
              332  JUMP_FORWARD        336  'to 336'
            334_0  COME_FROM           320  '320'
              334  END_FINALLY      
            336_0  COME_FROM           332  '332'
            336_1  COME_FROM           312  '312'

 L. 148       336  LOAD_GLOBAL              frozenset
              338  LOAD_FAST                'features'
              340  CALL_FUNCTION_1       1  ''
              342  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 310_0


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
        elif self.options['print_function']:
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
            elif fixer in self.pre_order:
                self.bmi_pre_order.append(fixer)
            else:
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
            else:
                fixer = fix_class(self.options, self.fixer_log)
                if fixer.explicit and self.explicit is not True and fix_mod_path not in self.explicit:
                    self.log_message('Skipping optional fixer: %s', fix_name)
                else:
                    self.log_debug('Adding transformation: %s', fix_name)
            if fixer.order == 'pre':
                pre_order_fixers.append(fixer)
            elif fixer.order == 'post':
                post_order_fixers.append(fixer)
            else:
                raise FixerError('Illegal fixer order: %r' % fixer.order)
        else:
            key_func = operator.attrgetter('run_order')
            pre_order_fixers.sort(key=key_func)
            post_order_fixers.sort(key=key_func)
            return (pre_order_fixers, post_order_fixers)

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

    def _read_python_source--- This code section failed: ---

 L. 308         0  SETUP_FINALLY        16  'to 16'

 L. 309         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'filename'
                6  LOAD_STR                 'rb'
                8  CALL_FUNCTION_2       2  ''
               10  STORE_FAST               'f'
               12  POP_BLOCK        
               14  JUMP_FORWARD         70  'to 70'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 310        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    68  'to 68'
               24  POP_TOP          
               26  STORE_FAST               'err'
               28  POP_TOP          
               30  SETUP_FINALLY        56  'to 56'

 L. 311        32  LOAD_FAST                'self'
               34  LOAD_METHOD              log_error
               36  LOAD_STR                 "Can't open %s: %s"
               38  LOAD_FAST                'filename'
               40  LOAD_FAST                'err'
               42  CALL_METHOD_3         3  ''
               44  POP_TOP          

 L. 312        46  POP_BLOCK        
               48  POP_EXCEPT       
               50  CALL_FINALLY         56  'to 56'
               52  LOAD_CONST               (None, None)
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'
             56_1  COME_FROM_FINALLY    30  '30'
               56  LOAD_CONST               None
               58  STORE_FAST               'err'
               60  DELETE_FAST              'err'
               62  END_FINALLY      
               64  POP_EXCEPT       
               66  JUMP_FORWARD         70  'to 70'
             68_0  COME_FROM            22  '22'
               68  END_FINALLY      
             70_0  COME_FROM            66  '66'
             70_1  COME_FROM            14  '14'

 L. 313        70  SETUP_FINALLY        92  'to 92'

 L. 314        72  LOAD_GLOBAL              tokenize
               74  LOAD_METHOD              detect_encoding
               76  LOAD_FAST                'f'
               78  LOAD_ATTR                readline
               80  CALL_METHOD_1         1  ''
               82  LOAD_CONST               0
               84  BINARY_SUBSCR    
               86  STORE_FAST               'encoding'
               88  POP_BLOCK        
               90  BEGIN_FINALLY    
             92_0  COME_FROM_FINALLY    70  '70'

 L. 316        92  LOAD_FAST                'f'
               94  LOAD_METHOD              close
               96  CALL_METHOD_0         0  ''
               98  POP_TOP          
              100  END_FINALLY      

 L. 317       102  LOAD_GLOBAL              io
              104  LOAD_ATTR                open
              106  LOAD_FAST                'filename'
              108  LOAD_STR                 'r'
              110  LOAD_FAST                'encoding'
              112  LOAD_STR                 ''
              114  LOAD_CONST               ('encoding', 'newline')
              116  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              118  SETUP_WITH          146  'to 146'
              120  STORE_FAST               'f'

 L. 318       122  LOAD_FAST                'f'
              124  LOAD_METHOD              read
              126  CALL_METHOD_0         0  ''
              128  LOAD_FAST                'encoding'
              130  BUILD_TUPLE_2         2 
              132  POP_BLOCK        
              134  ROT_TWO          
              136  BEGIN_FINALLY    
              138  WITH_CLEANUP_START
              140  WITH_CLEANUP_FINISH
              142  POP_FINALLY           0  ''
              144  RETURN_VALUE     
            146_0  COME_FROM_WITH      118  '118'
              146  WITH_CLEANUP_START
              148  WITH_CLEANUP_FINISH
              150  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 50

    def refactor_file(self, filename, write=False, doctests_only=False):
        """Refactors a file."""
        input, encoding = self._read_python_source(filename)
        if input is None:
            return
            input += '\n'
            if doctests_only:
                self.log_debug('Refactoring doctests in %s', filename)
                output = self.refactor_docstring(input, filename)
                if self.write_unchanged_files or output != input:
                    self.processed_file(output, filename, input, write, encoding)
                else:
                    self.log_debug('No doctest changes in %s', filename)
        else:
            tree = self.refactor_string(input, filename)
            if self.write_unchanged_files or tree and tree.was_changed:
                self.processed_file((str(tree)[:-1]), filename, write=write,
                  encoding=encoding)
            else:
                self.log_debug('No changes in %s', filename)

    def refactor_string--- This code section failed: ---

 L. 354         0  LOAD_GLOBAL              _detect_future_features
                2  LOAD_FAST                'data'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'features'

 L. 355         8  LOAD_STR                 'print_function'
               10  LOAD_FAST                'features'
               12  COMPARE_OP               in
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 356        16  LOAD_GLOBAL              pygram
               18  LOAD_ATTR                python_grammar_no_print_statement
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                driver
               24  STORE_ATTR               grammar
             26_0  COME_FROM            14  '14'

 L. 357        26  SETUP_FINALLY       114  'to 114'
               28  SETUP_FINALLY        46  'to 46'

 L. 358        30  LOAD_FAST                'self'
               32  LOAD_ATTR                driver
               34  LOAD_METHOD              parse_string
               36  LOAD_FAST                'data'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'tree'
               42  POP_BLOCK        
               44  JUMP_FORWARD        110  'to 110'
             46_0  COME_FROM_FINALLY    28  '28'

 L. 359        46  DUP_TOP          
               48  LOAD_GLOBAL              Exception
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE   108  'to 108'
               54  POP_TOP          
               56  STORE_FAST               'err'
               58  POP_TOP          
               60  SETUP_FINALLY        96  'to 96'

 L. 360        62  LOAD_FAST                'self'
               64  LOAD_METHOD              log_error
               66  LOAD_STR                 "Can't parse %s: %s: %s"

 L. 361        68  LOAD_FAST                'name'

 L. 361        70  LOAD_FAST                'err'
               72  LOAD_ATTR                __class__
               74  LOAD_ATTR                __name__

 L. 361        76  LOAD_FAST                'err'

 L. 360        78  CALL_METHOD_4         4  ''
               80  POP_TOP          

 L. 362        82  POP_BLOCK        
               84  POP_EXCEPT       
               86  CALL_FINALLY         96  'to 96'
               88  POP_BLOCK        
               90  CALL_FINALLY        114  'to 114'
               92  LOAD_CONST               None
               94  RETURN_VALUE     
             96_0  COME_FROM            86  '86'
             96_1  COME_FROM_FINALLY    60  '60'
               96  LOAD_CONST               None
               98  STORE_FAST               'err'
              100  DELETE_FAST              'err'
              102  END_FINALLY      
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            52  '52'
              108  END_FINALLY      
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM            44  '44'
              110  POP_BLOCK        
              112  BEGIN_FINALLY    
            114_0  COME_FROM            90  '90'
            114_1  COME_FROM_FINALLY    26  '26'

 L. 364       114  LOAD_FAST                'self'
              116  LOAD_ATTR                grammar
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                driver
              122  STORE_ATTR               grammar
              124  END_FINALLY      

 L. 365       126  LOAD_FAST                'features'
              128  LOAD_FAST                'tree'
              130  STORE_ATTR               future_features

 L. 366       132  LOAD_FAST                'self'
              134  LOAD_METHOD              log_debug
              136  LOAD_STR                 'Refactoring %s'
              138  LOAD_FAST                'name'
              140  CALL_METHOD_2         2  ''
              142  POP_TOP          

 L. 367       144  LOAD_FAST                'self'
              146  LOAD_METHOD              refactor_tree
              148  LOAD_FAST                'tree'
              150  LOAD_FAST                'name'
              152  CALL_METHOD_2         2  ''
              154  POP_TOP          

 L. 368       156  LOAD_FAST                'tree'
              158  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 86

    def refactor_stdin(self, doctests_only=False):
        input = sys.stdin.read()
        if doctests_only:
            self.log_debug('Refactoring doctests in stdin')
            output = self.refactor_docstring(input, '<stdin>')
            if self.write_unchanged_files or output != input:
                self.processed_file(output, '<stdin>', input)
            else:
                self.log_debug('No doctest changes in stdin')
        else:
            tree = self.refactor_string(input, '<stdin>')
            if self.write_unchanged_files or tree and tree.was_changed:
                self.processed_file(str(tree), '<stdin>', input)
            else:
                self.log_debug('No changes in stdin')

    def refactor_tree--- This code section failed: ---

 L. 402         0  LOAD_GLOBAL              chain
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                pre_order
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                post_order
               10  CALL_FUNCTION_2       2  ''
               12  GET_ITER         
               14  FOR_ITER             32  'to 32'
               16  STORE_FAST               'fixer'

 L. 403        18  LOAD_FAST                'fixer'
               20  LOAD_METHOD              start_tree
               22  LOAD_FAST                'tree'
               24  LOAD_FAST                'name'
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          
               30  JUMP_BACK            14  'to 14'

 L. 406        32  LOAD_FAST                'self'
               34  LOAD_METHOD              traverse_by
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                bmi_pre_order_heads
               40  LOAD_FAST                'tree'
               42  LOAD_METHOD              pre_order
               44  CALL_METHOD_0         0  ''
               46  CALL_METHOD_2         2  ''
               48  POP_TOP          

 L. 407        50  LOAD_FAST                'self'
               52  LOAD_METHOD              traverse_by
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                bmi_post_order_heads
               58  LOAD_FAST                'tree'
               60  LOAD_METHOD              post_order
               62  CALL_METHOD_0         0  ''
               64  CALL_METHOD_2         2  ''
               66  POP_TOP          

 L. 410        68  LOAD_FAST                'self'
               70  LOAD_ATTR                BM
               72  LOAD_METHOD              run
               74  LOAD_FAST                'tree'
               76  LOAD_METHOD              leaves
               78  CALL_METHOD_0         0  ''
               80  CALL_METHOD_1         1  ''
               82  STORE_FAST               'match_set'

 L. 412        84  LOAD_GLOBAL              any
               86  LOAD_FAST                'match_set'
               88  LOAD_METHOD              values
               90  CALL_METHOD_0         0  ''
               92  CALL_FUNCTION_1       1  ''
            94_96  POP_JUMP_IF_FALSE   436  'to 436'

 L. 413        98  LOAD_FAST                'self'
              100  LOAD_ATTR                BM
              102  LOAD_ATTR                fixers
              104  GET_ITER         
            106_0  COME_FROM           126  '126'
            106_1  COME_FROM           118  '118'
          106_108  FOR_ITER            434  'to 434'
              110  STORE_FAST               'fixer'

 L. 414       112  LOAD_FAST                'fixer'
              114  LOAD_FAST                'match_set'
              116  COMPARE_OP               in
              118  POP_JUMP_IF_FALSE   106  'to 106'
              120  LOAD_FAST                'match_set'
              122  LOAD_FAST                'fixer'
              124  BINARY_SUBSCR    
              126  POP_JUMP_IF_FALSE   106  'to 106'

 L. 416       128  LOAD_FAST                'match_set'
              130  LOAD_FAST                'fixer'
              132  BINARY_SUBSCR    
              134  LOAD_ATTR                sort
              136  LOAD_GLOBAL              pytree
              138  LOAD_ATTR                Base
              140  LOAD_ATTR                depth
              142  LOAD_CONST               True
              144  LOAD_CONST               ('key', 'reverse')
              146  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              148  POP_TOP          

 L. 418       150  LOAD_FAST                'fixer'
              152  LOAD_ATTR                keep_line_order
              154  POP_JUMP_IF_FALSE   176  'to 176'

 L. 421       156  LOAD_FAST                'match_set'
              158  LOAD_FAST                'fixer'
              160  BINARY_SUBSCR    
              162  LOAD_ATTR                sort
              164  LOAD_GLOBAL              pytree
              166  LOAD_ATTR                Base
              168  LOAD_ATTR                get_lineno
              170  LOAD_CONST               ('key',)
              172  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              174  POP_TOP          
            176_0  COME_FROM           154  '154'

 L. 423       176  LOAD_GLOBAL              list
              178  LOAD_FAST                'match_set'
              180  LOAD_FAST                'fixer'
              182  BINARY_SUBSCR    
              184  CALL_FUNCTION_1       1  ''
              186  GET_ITER         
            188_0  COME_FROM           312  '312'
            188_1  COME_FROM           292  '292'
              188  FOR_ITER            432  'to 432'
              190  STORE_FAST               'node'

 L. 424       192  LOAD_FAST                'node'
              194  LOAD_FAST                'match_set'
              196  LOAD_FAST                'fixer'
              198  BINARY_SUBSCR    
              200  COMPARE_OP               in
              202  POP_JUMP_IF_FALSE   218  'to 218'

 L. 425       204  LOAD_FAST                'match_set'
              206  LOAD_FAST                'fixer'
              208  BINARY_SUBSCR    
              210  LOAD_METHOD              remove
              212  LOAD_FAST                'node'
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
            218_0  COME_FROM           202  '202'

 L. 427       218  SETUP_FINALLY       232  'to 232'

 L. 428       220  LOAD_GLOBAL              find_root
              222  LOAD_FAST                'node'
              224  CALL_FUNCTION_1       1  ''
              226  POP_TOP          
              228  POP_BLOCK        
              230  JUMP_FORWARD        258  'to 258'
            232_0  COME_FROM_FINALLY   218  '218'

 L. 429       232  DUP_TOP          
              234  LOAD_GLOBAL              ValueError
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   256  'to 256'
              242  POP_TOP          
              244  POP_TOP          
              246  POP_TOP          

 L. 432       248  POP_EXCEPT       
              250  JUMP_BACK           188  'to 188'
              252  POP_EXCEPT       
              254  JUMP_FORWARD        258  'to 258'
            256_0  COME_FROM           238  '238'
              256  END_FINALLY      
            258_0  COME_FROM           254  '254'
            258_1  COME_FROM           230  '230'

 L. 434       258  LOAD_FAST                'node'
              260  LOAD_ATTR                fixers_applied
          262_264  POP_JUMP_IF_FALSE   280  'to 280'
              266  LOAD_FAST                'fixer'
              268  LOAD_FAST                'node'
              270  LOAD_ATTR                fixers_applied
              272  COMPARE_OP               in
          274_276  POP_JUMP_IF_FALSE   280  'to 280'

 L. 436       278  JUMP_BACK           188  'to 188'
            280_0  COME_FROM           274  '274'
            280_1  COME_FROM           262  '262'

 L. 438       280  LOAD_FAST                'fixer'
              282  LOAD_METHOD              match
              284  LOAD_FAST                'node'
              286  CALL_METHOD_1         1  ''
              288  STORE_FAST               'results'

 L. 440       290  LOAD_FAST                'results'
              292  POP_JUMP_IF_FALSE   188  'to 188'

 L. 441       294  LOAD_FAST                'fixer'
              296  LOAD_METHOD              transform
              298  LOAD_FAST                'node'
              300  LOAD_FAST                'results'
              302  CALL_METHOD_2         2  ''
              304  STORE_FAST               'new'

 L. 442       306  LOAD_FAST                'new'
              308  LOAD_CONST               None
              310  COMPARE_OP               is-not
              312  POP_JUMP_IF_FALSE   188  'to 188'

 L. 443       314  LOAD_FAST                'node'
              316  LOAD_METHOD              replace
              318  LOAD_FAST                'new'
              320  CALL_METHOD_1         1  ''
              322  POP_TOP          

 L. 445       324  LOAD_FAST                'new'
              326  LOAD_METHOD              post_order
              328  CALL_METHOD_0         0  ''
              330  GET_ITER         
              332  FOR_ITER            366  'to 366'
              334  STORE_FAST               'node'

 L. 448       336  LOAD_FAST                'node'
              338  LOAD_ATTR                fixers_applied
          340_342  POP_JUMP_IF_TRUE    350  'to 350'

 L. 449       344  BUILD_LIST_0          0 
              346  LOAD_FAST                'node'
              348  STORE_ATTR               fixers_applied
            350_0  COME_FROM           340  '340'

 L. 450       350  LOAD_FAST                'node'
              352  LOAD_ATTR                fixers_applied
              354  LOAD_METHOD              append
              356  LOAD_FAST                'fixer'
              358  CALL_METHOD_1         1  ''
              360  POP_TOP          
          362_364  JUMP_BACK           332  'to 332'

 L. 454       366  LOAD_FAST                'self'
              368  LOAD_ATTR                BM
              370  LOAD_METHOD              run
              372  LOAD_FAST                'new'
              374  LOAD_METHOD              leaves
              376  CALL_METHOD_0         0  ''
              378  CALL_METHOD_1         1  ''
              380  STORE_FAST               'new_matches'

 L. 455       382  LOAD_FAST                'new_matches'
              384  GET_ITER         
              386  FOR_ITER            430  'to 430'
              388  STORE_FAST               'fxr'

 L. 456       390  LOAD_FAST                'fxr'
              392  LOAD_FAST                'match_set'
              394  COMPARE_OP               not-in
          396_398  POP_JUMP_IF_FALSE   408  'to 408'

 L. 457       400  BUILD_LIST_0          0 
              402  LOAD_FAST                'match_set'
              404  LOAD_FAST                'fxr'
              406  STORE_SUBSCR     
            408_0  COME_FROM           396  '396'

 L. 459       408  LOAD_FAST                'match_set'
              410  LOAD_FAST                'fxr'
              412  BINARY_SUBSCR    
              414  LOAD_METHOD              extend
              416  LOAD_FAST                'new_matches'
              418  LOAD_FAST                'fxr'
              420  BINARY_SUBSCR    
              422  CALL_METHOD_1         1  ''
              424  POP_TOP          
          426_428  JUMP_BACK           386  'to 386'
              430  JUMP_BACK           188  'to 188'
              432  JUMP_BACK           106  'to 106'
              434  JUMP_BACK            84  'to 84'
            436_0  COME_FROM            94  '94'

 L. 461       436  LOAD_GLOBAL              chain
              438  LOAD_FAST                'self'
              440  LOAD_ATTR                pre_order
              442  LOAD_FAST                'self'
              444  LOAD_ATTR                post_order
              446  CALL_FUNCTION_2       2  ''
              448  GET_ITER         
              450  FOR_ITER            470  'to 470'
              452  STORE_FAST               'fixer'

 L. 462       454  LOAD_FAST                'fixer'
              456  LOAD_METHOD              finish_tree
              458  LOAD_FAST                'tree'
              460  LOAD_FAST                'name'
              462  CALL_METHOD_2         2  ''
              464  POP_TOP          
          466_468  JUMP_BACK           450  'to 450'

 L. 463       470  LOAD_FAST                'tree'
              472  LOAD_ATTR                was_changed
              474  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 252

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
        self.print_outputold_textnew_textfilenameequal
        if equal:
            self.log_debug('No changes to %s', filename)
            if not self.write_unchanged_files:
                return
        elif write:
            self.write_filenew_textfilenameold_textencoding
        else:
            self.log_debug('Not writing changes to %s', filename)

    def write_file--- This code section failed: ---

 L. 516         0  SETUP_FINALLY        24  'to 24'

 L. 517         2  LOAD_GLOBAL              io
                4  LOAD_ATTR                open
                6  LOAD_FAST                'filename'
                8  LOAD_STR                 'w'
               10  LOAD_FAST                'encoding'
               12  LOAD_STR                 ''
               14  LOAD_CONST               ('encoding', 'newline')
               16  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               18  STORE_FAST               'fp'
               20  POP_BLOCK        
               22  JUMP_FORWARD         78  'to 78'
             24_0  COME_FROM_FINALLY     0  '0'

 L. 518        24  DUP_TOP          
               26  LOAD_GLOBAL              OSError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    76  'to 76'
               32  POP_TOP          
               34  STORE_FAST               'err'
               36  POP_TOP          
               38  SETUP_FINALLY        64  'to 64'

 L. 519        40  LOAD_FAST                'self'
               42  LOAD_METHOD              log_error
               44  LOAD_STR                 "Can't create %s: %s"
               46  LOAD_FAST                'filename'
               48  LOAD_FAST                'err'
               50  CALL_METHOD_3         3  ''
               52  POP_TOP          

 L. 520        54  POP_BLOCK        
               56  POP_EXCEPT       
               58  CALL_FINALLY         64  'to 64'
               60  LOAD_CONST               None
               62  RETURN_VALUE     
             64_0  COME_FROM            58  '58'
             64_1  COME_FROM_FINALLY    38  '38'
               64  LOAD_CONST               None
               66  STORE_FAST               'err'
               68  DELETE_FAST              'err'
               70  END_FINALLY      
               72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            30  '30'
               76  END_FINALLY      
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            22  '22'

 L. 522        78  LOAD_FAST                'fp'
               80  SETUP_WITH          152  'to 152'
               82  POP_TOP          

 L. 523        84  SETUP_FINALLY       100  'to 100'

 L. 524        86  LOAD_FAST                'fp'
               88  LOAD_METHOD              write
               90  LOAD_FAST                'new_text'
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
               96  POP_BLOCK        
               98  JUMP_FORWARD        148  'to 148'
            100_0  COME_FROM_FINALLY    84  '84'

 L. 525       100  DUP_TOP          
              102  LOAD_GLOBAL              OSError
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   146  'to 146'
              108  POP_TOP          
              110  STORE_FAST               'err'
              112  POP_TOP          
              114  SETUP_FINALLY       134  'to 134'

 L. 526       116  LOAD_FAST                'self'
              118  LOAD_METHOD              log_error
              120  LOAD_STR                 "Can't write %s: %s"
              122  LOAD_FAST                'filename'
              124  LOAD_FAST                'err'
              126  CALL_METHOD_3         3  ''
              128  POP_TOP          
              130  POP_BLOCK        
              132  BEGIN_FINALLY    
            134_0  COME_FROM_FINALLY   114  '114'
              134  LOAD_CONST               None
              136  STORE_FAST               'err'
              138  DELETE_FAST              'err'
              140  END_FINALLY      
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           106  '106'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM            98  '98'
              148  POP_BLOCK        
              150  BEGIN_FINALLY    
            152_0  COME_FROM_WITH       80  '80'
              152  WITH_CLEANUP_START
              154  WITH_CLEANUP_FINISH
              156  END_FINALLY      

 L. 527       158  LOAD_FAST                'self'
              160  LOAD_METHOD              log_debug
              162  LOAD_STR                 'Wrote changes to %s'
              164  LOAD_FAST                'filename'
              166  CALL_METHOD_2         2  ''
              168  POP_TOP          

 L. 528       170  LOAD_CONST               True
              172  LOAD_FAST                'self'
              174  STORE_ATTR               wrote

Parse error at or near `CALL_FINALLY' instruction at offset 58

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
                    result.extend(self.refactor_doctestblockblock_linenoindentfilename)
                block_lineno = lineno
                block = [line]
                i = line.find(self.PS1)
                indent = line[:i]
            elif not indent is not None or line.startswith(indent + self.PS2) or line == indent + self.PS2.rstrip() + '\n':
                block.append(line)
            else:
                if block is not None:
                    result.extend(self.refactor_doctestblockblock_linenoindentfilename)
                block = None
                indent = None
                result.append(line)
        else:
            if block is not None:
                result.extend(self.refactor_doctestblockblock_linenoindentfilename)
            return ''.join(result)

    def refactor_doctest--- This code section failed: ---

 L. 584         0  SETUP_FINALLY        20  'to 20'

 L. 585         2  LOAD_DEREF               'self'
                4  LOAD_METHOD              parse_block
                6  LOAD_FAST                'block'
                8  LOAD_FAST                'lineno'
               10  LOAD_DEREF               'indent'
               12  CALL_METHOD_3         3  ''
               14  STORE_FAST               'tree'
               16  POP_BLOCK        
               18  JUMP_FORWARD        126  'to 126'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 586        20  DUP_TOP          
               22  LOAD_GLOBAL              Exception
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE   124  'to 124'
               28  POP_TOP          
               30  STORE_FAST               'err'
               32  POP_TOP          
               34  SETUP_FINALLY       112  'to 112'

 L. 587        36  LOAD_DEREF               'self'
               38  LOAD_ATTR                logger
               40  LOAD_METHOD              isEnabledFor
               42  LOAD_GLOBAL              logging
               44  LOAD_ATTR                DEBUG
               46  CALL_METHOD_1         1  ''
               48  POP_JUMP_IF_FALSE    78  'to 78'

 L. 588        50  LOAD_FAST                'block'
               52  GET_ITER         
               54  FOR_ITER             78  'to 78'
               56  STORE_FAST               'line'

 L. 589        58  LOAD_DEREF               'self'
               60  LOAD_METHOD              log_debug
               62  LOAD_STR                 'Source: %s'
               64  LOAD_FAST                'line'
               66  LOAD_METHOD              rstrip
               68  LOAD_STR                 '\n'
               70  CALL_METHOD_1         1  ''
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          
               76  JUMP_BACK            54  'to 54'
             78_0  COME_FROM            48  '48'

 L. 590        78  LOAD_DEREF               'self'
               80  LOAD_METHOD              log_error
               82  LOAD_STR                 "Can't parse docstring in %s line %s: %s: %s"

 L. 591        84  LOAD_FAST                'filename'

 L. 591        86  LOAD_FAST                'lineno'

 L. 591        88  LOAD_FAST                'err'
               90  LOAD_ATTR                __class__
               92  LOAD_ATTR                __name__

 L. 591        94  LOAD_FAST                'err'

 L. 590        96  CALL_METHOD_5         5  ''
               98  POP_TOP          

 L. 592       100  LOAD_FAST                'block'
              102  ROT_FOUR         
              104  POP_BLOCK        
              106  POP_EXCEPT       
              108  CALL_FINALLY        112  'to 112'
              110  RETURN_VALUE     
            112_0  COME_FROM           108  '108'
            112_1  COME_FROM_FINALLY    34  '34'
              112  LOAD_CONST               None
              114  STORE_FAST               'err'
              116  DELETE_FAST              'err'
              118  END_FINALLY      
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM            26  '26'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM            18  '18'

 L. 593       126  LOAD_DEREF               'self'
              128  LOAD_METHOD              refactor_tree
              130  LOAD_FAST                'tree'
              132  LOAD_FAST                'filename'
              134  CALL_METHOD_2         2  ''
          136_138  POP_JUMP_IF_FALSE   298  'to 298'

 L. 594       140  LOAD_GLOBAL              str
              142  LOAD_FAST                'tree'
              144  CALL_FUNCTION_1       1  ''
              146  LOAD_ATTR                splitlines
              148  LOAD_CONST               True
              150  LOAD_CONST               ('keepends',)
              152  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              154  STORE_FAST               'new'

 L. 596       156  LOAD_FAST                'new'
              158  LOAD_CONST               None
              160  LOAD_FAST                'lineno'
              162  LOAD_CONST               1
              164  BINARY_SUBTRACT  
              166  BUILD_SLICE_2         2 
              168  BINARY_SUBSCR    
              170  LOAD_FAST                'new'
              172  LOAD_FAST                'lineno'
              174  LOAD_CONST               1
              176  BINARY_SUBTRACT  
              178  LOAD_CONST               None
              180  BUILD_SLICE_2         2 
              182  BINARY_SUBSCR    
              184  ROT_TWO          
              186  STORE_FAST               'clipped'
              188  STORE_FAST               'new'

 L. 597       190  LOAD_FAST                'clipped'
              192  LOAD_STR                 '\n'
              194  BUILD_LIST_1          1 
              196  LOAD_FAST                'lineno'
              198  LOAD_CONST               1
              200  BINARY_SUBTRACT  
              202  BINARY_MULTIPLY  
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_TRUE    216  'to 216'
              208  LOAD_ASSERT              AssertionError
              210  LOAD_FAST                'clipped'
              212  CALL_FUNCTION_1       1  ''
              214  RAISE_VARARGS_1       1  'exception instance'
            216_0  COME_FROM           206  '206'

 L. 598       216  LOAD_FAST                'new'
              218  LOAD_CONST               -1
              220  BINARY_SUBSCR    
              222  LOAD_METHOD              endswith
              224  LOAD_STR                 '\n'
              226  CALL_METHOD_1         1  ''
              228  POP_JUMP_IF_TRUE    246  'to 246'

 L. 599       230  LOAD_FAST                'new'
              232  LOAD_CONST               -1
              234  DUP_TOP_TWO      
              236  BINARY_SUBSCR    
              238  LOAD_STR                 '\n'
              240  INPLACE_ADD      
              242  ROT_THREE        
              244  STORE_SUBSCR     
            246_0  COME_FROM           228  '228'

 L. 600       246  LOAD_DEREF               'indent'
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                PS1
              252  BINARY_ADD       
              254  LOAD_FAST                'new'
              256  LOAD_METHOD              pop
              258  LOAD_CONST               0
              260  CALL_METHOD_1         1  ''
              262  BINARY_ADD       
              264  BUILD_LIST_1          1 
              266  STORE_FAST               'block'

 L. 601       268  LOAD_FAST                'new'
          270_272  POP_JUMP_IF_FALSE   298  'to 298'

 L. 602       274  LOAD_FAST                'block'
              276  LOAD_CLOSURE             'indent'
              278  LOAD_CLOSURE             'self'
              280  BUILD_TUPLE_2         2 
              282  LOAD_LISTCOMP            '<code_object <listcomp>>'
              284  LOAD_STR                 'RefactoringTool.refactor_doctest.<locals>.<listcomp>'
              286  MAKE_FUNCTION_8          'closure'
              288  LOAD_FAST                'new'
              290  GET_ITER         
              292  CALL_FUNCTION_1       1  ''
              294  INPLACE_ADD      
              296  STORE_FAST               'block'
            298_0  COME_FROM           270  '270'
            298_1  COME_FROM           136  '136'

 L. 603       298  LOAD_FAST                'block'
              300  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 104

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
            else:
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
            (yield (
             type, value, (line0, col0), (line1, col1), line_text))

    def gen_lines(self, block, indent):
        """Generates lines as expected by tokenize from a list of lines.

        This strips the first len(indent + self.PS1) characters off each line.
        """
        prefix1 = indent + self.PS1
        prefix2 = indent + self.PS2
        prefix = prefix1
        for line in block:
            if line.startswith(prefix):
                (yield line[len(prefix):])
            else:
                if line == prefix.rstrip() + '\n':
                    (yield '\n')
                else:
                    raise AssertionError('line=%r, prefix=%r' % (line, prefix))
            prefix = prefix2
        else:
            while True:
                (yield '')


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
        else:
            if self.queue is not None:
                raise RuntimeError('already doing multiple processes')
            self.queue = multiprocessing.JoinableQueue()
            self.output_lock = multiprocessing.Lock()
            processes = [multiprocessing.Process(target=(self._child)) for i in range(num_processes)]
            try:
                for p in processes:
                    p.start()
                else:
                    super(MultiprocessRefactoringTool, self).refactor(items, write, doctests_only)

            finally:
                self.queue.join()
                for i in range(num_processes):
                    self.queue.put(None)
                else:
                    for p in processes:
                        if p.is_alive():
                            p.join()
                    else:
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