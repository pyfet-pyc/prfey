# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: lib2to3\pgen2\grammar.py
"""This module defines the data structures used to represent a grammar.

These are a bit arcane because they are derived from the data
structures used by Python's 'pgen' parser generator.

There's also a table here mapping operators to their names in the
token module; the Python tokenize module reports all operators as the
fallback token code OP, but the parser needs the actual token code.

"""
import pickle
from . import token

class Grammar(object):
    __doc__ = "Pgen parsing tables conversion class.\n\n    Once initialized, this class supplies the grammar tables for the\n    parsing engine implemented by parse.py.  The parsing engine\n    accesses the instance variables directly.  The class here does not\n    provide initialization of the tables; several subclasses exist to\n    do this (see the conv and pgen modules).\n\n    The load() method reads the tables from a pickle file, which is\n    much faster than the other ways offered by subclasses.  The pickle\n    file is written by calling dump() (after loading the grammar\n    tables using a subclass).  The report() method prints a readable\n    representation of the tables to stdout, for debugging.\n\n    The instance variables are as follows:\n\n    symbol2number -- a dict mapping symbol names to numbers.  Symbol\n                     numbers are always 256 or higher, to distinguish\n                     them from token numbers, which are between 0 and\n                     255 (inclusive).\n\n    number2symbol -- a dict mapping numbers to symbol names;\n                     these two are each other's inverse.\n\n    states        -- a list of DFAs, where each DFA is a list of\n                     states, each state is a list of arcs, and each\n                     arc is a (i, j) pair where i is a label and j is\n                     a state number.  The DFA number is the index into\n                     this list.  (This name is slightly confusing.)\n                     Final states are represented by a special arc of\n                     the form (0, j) where j is its own state number.\n\n    dfas          -- a dict mapping symbol numbers to (DFA, first)\n                     pairs, where DFA is an item from the states list\n                     above, and first is a set of tokens that can\n                     begin this grammar rule (represented by a dict\n                     whose values are always 1).\n\n    labels        -- a list of (x, y) pairs where x is either a token\n                     number or a symbol number, and y is either None\n                     or a string; the strings are keywords.  The label\n                     number is the index in this list; label numbers\n                     are used to mark state transitions (arcs) in the\n                     DFAs.\n\n    start         -- the number of the grammar's start symbol.\n\n    keywords      -- a dict mapping keyword strings to arc labels.\n\n    tokens        -- a dict mapping token numbers to arc labels.\n\n    "

    def __init__(self):
        self.symbol2number = {}
        self.number2symbol = {}
        self.states = []
        self.dfas = {}
        self.labels = [
         (0, 'EMPTY')]
        self.keywords = {}
        self.tokens = {}
        self.symbol2label = {}
        self.start = 256

    def dump--- This code section failed: ---

 L.  89         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'filename'
                4  LOAD_STR                 'wb'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           44  'to 44'
               10  STORE_FAST               'f'

 L.  90        12  LOAD_GLOBAL              pickle
               14  LOAD_METHOD              dump
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                __dict__
               20  LOAD_FAST                'f'
               22  LOAD_GLOBAL              pickle
               24  LOAD_ATTR                HIGHEST_PROTOCOL
               26  CALL_METHOD_3         3  ''
               28  POP_TOP          
               30  POP_BLOCK        
               32  LOAD_CONST               None
               34  DUP_TOP          
               36  DUP_TOP          
               38  CALL_FUNCTION_3       3  ''
               40  POP_TOP          
               42  JUMP_FORWARD         60  'to 60'
             44_0  COME_FROM_WITH        8  '8'
               44  <49>             
               46  POP_JUMP_IF_TRUE     50  'to 50'
               48  <48>             
             50_0  COME_FROM            46  '46'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          
               56  POP_EXCEPT       
               58  POP_TOP          
             60_0  COME_FROM            42  '42'

Parse error at or near `DUP_TOP' instruction at offset 34

    def load--- This code section failed: ---

 L.  94         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'filename'
                4  LOAD_STR                 'rb'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           36  'to 36'
               10  STORE_FAST               'f'

 L.  95        12  LOAD_GLOBAL              pickle
               14  LOAD_METHOD              load
               16  LOAD_FAST                'f'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'd'
               22  POP_BLOCK        
               24  LOAD_CONST               None
               26  DUP_TOP          
               28  DUP_TOP          
               30  CALL_FUNCTION_3       3  ''
               32  POP_TOP          
               34  JUMP_FORWARD         52  'to 52'
             36_0  COME_FROM_WITH        8  '8'
               36  <49>             
               38  POP_JUMP_IF_TRUE     42  'to 42'
               40  <48>             
             42_0  COME_FROM            38  '38'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          
               48  POP_EXCEPT       
               50  POP_TOP          
             52_0  COME_FROM            34  '34'

 L.  96        52  LOAD_FAST                'self'
               54  LOAD_ATTR                __dict__
               56  LOAD_METHOD              update
               58  LOAD_FAST                'd'
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

Parse error at or near `DUP_TOP' instruction at offset 26

    def loads(self, pkl):
        """Load the grammar tables from a pickle bytes object."""
        self.__dict__.updatepickle.loadspkl

    def copy(self):
        """
        Copy the grammar.
        """
        new = self.__class__()
        for dict_attr in ('symbol2number', 'number2symbol', 'dfas', 'keywords', 'tokens',
                          'symbol2label'):
            setattr(new, dict_attr, getattr(self, dict_attr).copy())
        else:
            new.labels = self.labels[:]
            new.states = self.states[:]
            new.start = self.start
            return new

    def report(self):
        """Dump the grammar tables to standard output, for debugging."""
        from pprint import pprint
        print('s2n')
        pprint(self.symbol2number)
        print('n2s')
        pprint(self.number2symbol)
        print('states')
        pprint(self.states)
        print('dfas')
        pprint(self.dfas)
        print('labels')
        pprint(self.labels)
        print('start', self.start)


opmap_raw = '\n( LPAR\n) RPAR\n[ LSQB\n] RSQB\n: COLON\n, COMMA\n; SEMI\n+ PLUS\n- MINUS\n* STAR\n/ SLASH\n| VBAR\n& AMPER\n< LESS\n> GREATER\n= EQUAL\n. DOT\n% PERCENT\n` BACKQUOTE\n{ LBRACE\n} RBRACE\n@ AT\n@= ATEQUAL\n== EQEQUAL\n!= NOTEQUAL\n<> NOTEQUAL\n<= LESSEQUAL\n>= GREATEREQUAL\n~ TILDE\n^ CIRCUMFLEX\n<< LEFTSHIFT\n>> RIGHTSHIFT\n** DOUBLESTAR\n+= PLUSEQUAL\n-= MINEQUAL\n*= STAREQUAL\n/= SLASHEQUAL\n%= PERCENTEQUAL\n&= AMPEREQUAL\n|= VBAREQUAL\n^= CIRCUMFLEXEQUAL\n<<= LEFTSHIFTEQUAL\n>>= RIGHTSHIFTEQUAL\n**= DOUBLESTAREQUAL\n// DOUBLESLASH\n//= DOUBLESLASHEQUAL\n-> RARROW\n:= COLONEQUAL\n'
opmap = {}
for line in opmap_raw.splitlines():
    if line:
        op, name = line.split()
        opmap[op] = getattr(token, name)