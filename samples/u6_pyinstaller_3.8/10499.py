# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: lib2to3\pgen2\driver.py
"""Parser driver.

This provides a high-level interface to parse a file into a syntax tree.

"""
__author__ = 'Guido van Rossum <guido@python.org>'
__all__ = [
 'Driver', 'load_grammar']
import io, os, logging, pkgutil, sys
from . import grammar, parse, token, tokenize, pgen

class Driver(object):

    def __init__(self, grammar, convert=None, logger=None):
        self.grammar = grammar
        if logger is None:
            logger = logging.getLogger()
        self.logger = logger
        self.convert = convert

    def parse_tokens--- This code section failed: ---

 L.  41         0  LOAD_GLOBAL              parse
                2  LOAD_METHOD              Parser
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                grammar
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                convert
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'p'

 L.  42        16  LOAD_FAST                'p'
               18  LOAD_METHOD              setup
               20  CALL_METHOD_0         0  ''
               22  POP_TOP          

 L.  43        24  LOAD_CONST               1
               26  STORE_FAST               'lineno'

 L.  44        28  LOAD_CONST               0
               30  STORE_FAST               'column'

 L.  45        32  LOAD_CONST               None
               34  DUP_TOP          
               36  STORE_FAST               'type'
               38  DUP_TOP          
               40  STORE_FAST               'value'
               42  DUP_TOP          
               44  STORE_FAST               'start'
               46  DUP_TOP          
               48  STORE_FAST               'end'
               50  STORE_FAST               'line_text'

 L.  46        52  LOAD_STR                 ''
               54  STORE_FAST               'prefix'

 L.  47        56  LOAD_FAST                'tokens'
               58  GET_ITER         
             60_0  COME_FROM           360  '360'
             60_1  COME_FROM           228  '228'
            60_62  FOR_ITER            376  'to 376'
               64  STORE_FAST               'quintuple'

 L.  48        66  LOAD_FAST                'quintuple'
               68  UNPACK_SEQUENCE_5     5 
               70  STORE_FAST               'type'
               72  STORE_FAST               'value'
               74  STORE_FAST               'start'
               76  STORE_FAST               'end'
               78  STORE_FAST               'line_text'

 L.  49        80  LOAD_FAST                'start'
               82  LOAD_FAST                'lineno'
               84  LOAD_FAST                'column'
               86  BUILD_TUPLE_2         2 
               88  COMPARE_OP               !=
               90  POP_JUMP_IF_FALSE   188  'to 188'

 L.  50        92  LOAD_FAST                'lineno'
               94  LOAD_FAST                'column'
               96  BUILD_TUPLE_2         2 
               98  LOAD_FAST                'start'
              100  COMPARE_OP               <=
              102  POP_JUMP_IF_TRUE    120  'to 120'
              104  LOAD_ASSERT              AssertionError
              106  LOAD_FAST                'lineno'
              108  LOAD_FAST                'column'
              110  BUILD_TUPLE_2         2 
              112  LOAD_FAST                'start'
              114  BUILD_TUPLE_2         2 
              116  CALL_FUNCTION_1       1  ''
              118  RAISE_VARARGS_1       1  'exception instance'
            120_0  COME_FROM           102  '102'

 L.  51       120  LOAD_FAST                'start'
              122  UNPACK_SEQUENCE_2     2 
              124  STORE_FAST               's_lineno'
              126  STORE_FAST               's_column'

 L.  52       128  LOAD_FAST                'lineno'
              130  LOAD_FAST                's_lineno'
              132  COMPARE_OP               <
              134  POP_JUMP_IF_FALSE   160  'to 160'

 L.  53       136  LOAD_FAST                'prefix'
              138  LOAD_STR                 '\n'
              140  LOAD_FAST                's_lineno'
              142  LOAD_FAST                'lineno'
              144  BINARY_SUBTRACT  
              146  BINARY_MULTIPLY  
              148  INPLACE_ADD      
              150  STORE_FAST               'prefix'

 L.  54       152  LOAD_FAST                's_lineno'
              154  STORE_FAST               'lineno'

 L.  55       156  LOAD_CONST               0
              158  STORE_FAST               'column'
            160_0  COME_FROM           134  '134'

 L.  56       160  LOAD_FAST                'column'
              162  LOAD_FAST                's_column'
              164  COMPARE_OP               <
              166  POP_JUMP_IF_FALSE   188  'to 188'

 L.  57       168  LOAD_FAST                'prefix'
              170  LOAD_FAST                'line_text'
              172  LOAD_FAST                'column'
              174  LOAD_FAST                's_column'
              176  BUILD_SLICE_2         2 
              178  BINARY_SUBSCR    
              180  INPLACE_ADD      
              182  STORE_FAST               'prefix'

 L.  58       184  LOAD_FAST                's_column'
              186  STORE_FAST               'column'
            188_0  COME_FROM           166  '166'
            188_1  COME_FROM            90  '90'

 L.  59       188  LOAD_FAST                'type'
              190  LOAD_GLOBAL              tokenize
              192  LOAD_ATTR                COMMENT
              194  LOAD_GLOBAL              tokenize
              196  LOAD_ATTR                NL
              198  BUILD_TUPLE_2         2 
              200  COMPARE_OP               in
              202  POP_JUMP_IF_FALSE   244  'to 244'

 L.  60       204  LOAD_FAST                'prefix'
              206  LOAD_FAST                'value'
              208  INPLACE_ADD      
              210  STORE_FAST               'prefix'

 L.  61       212  LOAD_FAST                'end'
              214  UNPACK_SEQUENCE_2     2 
              216  STORE_FAST               'lineno'
              218  STORE_FAST               'column'

 L.  62       220  LOAD_FAST                'value'
              222  LOAD_METHOD              endswith
              224  LOAD_STR                 '\n'
              226  CALL_METHOD_1         1  ''
              228  POP_JUMP_IF_FALSE    60  'to 60'

 L.  63       230  LOAD_FAST                'lineno'
              232  LOAD_CONST               1
              234  INPLACE_ADD      
              236  STORE_FAST               'lineno'

 L.  64       238  LOAD_CONST               0
              240  STORE_FAST               'column'

 L.  65       242  JUMP_BACK            60  'to 60'
            244_0  COME_FROM           202  '202'

 L.  66       244  LOAD_FAST                'type'
              246  LOAD_GLOBAL              token
              248  LOAD_ATTR                OP
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   266  'to 266'

 L.  67       256  LOAD_GLOBAL              grammar
              258  LOAD_ATTR                opmap
              260  LOAD_FAST                'value'
              262  BINARY_SUBSCR    
              264  STORE_FAST               'type'
            266_0  COME_FROM           252  '252'

 L.  68       266  LOAD_FAST                'debug'
          268_270  POP_JUMP_IF_FALSE   296  'to 296'

 L.  69       272  LOAD_FAST                'self'
              274  LOAD_ATTR                logger
              276  LOAD_METHOD              debug
              278  LOAD_STR                 '%s %r (prefix=%r)'

 L.  70       280  LOAD_GLOBAL              token
              282  LOAD_ATTR                tok_name
              284  LOAD_FAST                'type'
              286  BINARY_SUBSCR    

 L.  70       288  LOAD_FAST                'value'

 L.  70       290  LOAD_FAST                'prefix'

 L.  69       292  CALL_METHOD_4         4  ''
              294  POP_TOP          
            296_0  COME_FROM           268  '268'

 L.  71       296  LOAD_FAST                'p'
              298  LOAD_METHOD              addtoken
              300  LOAD_FAST                'type'
              302  LOAD_FAST                'value'
              304  LOAD_FAST                'prefix'
              306  LOAD_FAST                'start'
              308  BUILD_TUPLE_2         2 
              310  CALL_METHOD_3         3  ''
          312_314  POP_JUMP_IF_FALSE   340  'to 340'

 L.  72       316  LOAD_FAST                'debug'
          318_320  POP_JUMP_IF_FALSE   334  'to 334'

 L.  73       322  LOAD_FAST                'self'
              324  LOAD_ATTR                logger
              326  LOAD_METHOD              debug
              328  LOAD_STR                 'Stop.'
              330  CALL_METHOD_1         1  ''
              332  POP_TOP          
            334_0  COME_FROM           318  '318'

 L.  74       334  POP_TOP          
          336_338  JUMP_ABSOLUTE       396  'to 396'
            340_0  COME_FROM           312  '312'

 L.  75       340  LOAD_STR                 ''
              342  STORE_FAST               'prefix'

 L.  76       344  LOAD_FAST                'end'
              346  UNPACK_SEQUENCE_2     2 
              348  STORE_FAST               'lineno'
              350  STORE_FAST               'column'

 L.  77       352  LOAD_FAST                'value'
              354  LOAD_METHOD              endswith
              356  LOAD_STR                 '\n'
              358  CALL_METHOD_1         1  ''
              360  POP_JUMP_IF_FALSE    60  'to 60'

 L.  78       362  LOAD_FAST                'lineno'
              364  LOAD_CONST               1
              366  INPLACE_ADD      
              368  STORE_FAST               'lineno'

 L.  79       370  LOAD_CONST               0
              372  STORE_FAST               'column'
              374  JUMP_BACK            60  'to 60'

 L.  82       376  LOAD_GLOBAL              parse
              378  LOAD_METHOD              ParseError
              380  LOAD_STR                 'incomplete input'

 L.  83       382  LOAD_FAST                'type'

 L.  83       384  LOAD_FAST                'value'

 L.  83       386  LOAD_FAST                'prefix'
              388  LOAD_FAST                'start'
              390  BUILD_TUPLE_2         2 

 L.  82       392  CALL_METHOD_4         4  ''
              394  RAISE_VARARGS_1       1  'exception instance'

 L.  84       396  LOAD_FAST                'p'
              398  LOAD_ATTR                rootnode
              400  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 336_338

    def parse_stream_raw(self, stream, debug=False):
        """Parse a stream and return the syntax tree."""
        tokens = tokenize.generate_tokens(stream.readline)
        return self.parse_tokenstokensdebug

    def parse_stream(self, stream, debug=False):
        """Parse a stream and return the syntax tree."""
        return self.parse_stream_rawstreamdebug

    def parse_file--- This code section failed: ---

 L.  97         0  LOAD_GLOBAL              io
                2  LOAD_ATTR                open
                4  LOAD_FAST                'filename'
                6  LOAD_STR                 'r'
                8  LOAD_FAST                'encoding'
               10  LOAD_CONST               ('encoding',)
               12  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               14  SETUP_WITH           42  'to 42'
               16  STORE_FAST               'stream'

 L.  98        18  LOAD_FAST                'self'
               20  LOAD_METHOD              parse_stream
               22  LOAD_FAST                'stream'
               24  LOAD_FAST                'debug'
               26  CALL_METHOD_2         2  ''
               28  POP_BLOCK        
               30  ROT_TWO          
               32  BEGIN_FINALLY    
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  POP_FINALLY           0  ''
               40  RETURN_VALUE     
             42_0  COME_FROM_WITH       14  '14'
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 30

    def parse_string(self, text, debug=False):
        """Parse a string and return the syntax tree."""
        tokens = tokenize.generate_tokens(io.StringIO(text).readline)
        return self.parse_tokenstokensdebug


def _generate_pickle_name(gt):
    head, tail = os.path.splitext(gt)
    if tail == '.txt':
        tail = ''
    return head + tail + '.'.join(map(str, sys.version_info)) + '.pickle'


def load_grammar(gt='Grammar.txt', gp=None, save=True, force=False, logger=None):
    """Load the grammar (maybe from a pickle)."""
    if logger is None:
        logger = logging.getLogger()
    else:
        gp = _generate_pickle_name(gt) if gp is None else gp
        if not force:
            _newer(gp, gt) or logger.info'Generating grammar tables from %s'gt
            g = pgen.generate_grammar(gt)
            if save:
                logger.info'Writing grammar tables to %s'gp
                try:
                    g.dump(gp)
                except OSError as e:
                    try:
                        logger.info'Writing failed: %s'e
                    finally:
                        e = None
                        del e

        else:
            g = grammar.Grammar()
            g.load(gp)
    return g


def _newer(a, b):
    """Inquire whether file a was written since file b."""
    if not os.path.exists(a):
        return False
    else:
        return os.path.exists(b) or True
    return os.path.getmtime(a) >= os.path.getmtime(b)


def load_packaged_grammar(package, grammar_source):
    """Normally, loads a pickled grammar by doing
        pkgutil.get_data(package, pickled_grammar)
    where *pickled_grammar* is computed from *grammar_source* by adding the
    Python version and using a ``.pickle`` extension.

    However, if *grammar_source* is an extant file, load_grammar(grammar_source)
    is called instead. This facilitates using a packaged grammar file when needed
    but preserves load_grammar's automatic regeneration behavior when possible.

    """
    if os.path.isfile(grammar_source):
        return load_grammar(grammar_source)
    pickled_name = _generate_pickle_name(os.path.basename(grammar_source))
    data = pkgutil.get_datapackagepickled_name
    g = grammar.Grammar()
    g.loads(data)
    return g


def main(*args):
    """Main program, when run as a script: produce grammar pickle files.

    Calls load_grammar for each argument, a path to a grammar text file.
    """
    if not args:
        args = sys.argv[1:]
    logging.basicConfig(level=(logging.INFO), stream=(sys.stdout), format='%(message)s')
    for gt in args:
        load_grammar(gt, save=True, force=True)
    else:
        return True


if __name__ == '__main__':
    sys.exit(int(not main()))