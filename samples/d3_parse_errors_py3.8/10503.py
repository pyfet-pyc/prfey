# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: lib2to3\pgen2\pgen.py
from . import grammar, token, tokenize

class PgenGrammar(grammar.Grammar):
    pass


class ParserGenerator(object):

    def __init__(self, filename, stream=None):
        close_stream = None
        if stream is None:
            stream = open(filename)
            close_stream = stream.close
        self.filename = filename
        self.stream = stream
        self.generator = tokenize.generate_tokens(stream.readline)
        self.gettoken()
        self.dfas, self.startsymbol = self.parse()
        if close_stream is not None:
            close_stream()
        self.first = {}
        self.addfirstsets()

    def make_grammar(self):
        c = PgenGrammar()
        names = list(self.dfas.keys())
        names.sort()
        names.remove(self.startsymbol)
        names.insert(0, self.startsymbol)
        for name in names:
            i = 256 + len(c.symbol2number)
            c.symbol2number[name] = i
            c.number2symbol[i] = name
        else:
            for name in names:
                dfa = self.dfas[name]
                states = []
                for state in dfa:
                    arcs = []
                    for label, next in sorted(state.arcs.items()):
                        arcs.append((self.make_label(c, label), dfa.index(next)))

                    if state.isfinal:
                        arcs.append((0, dfa.index(state)))
                    else:
                        states.append(arcs)
                else:
                    c.states.append(states)
                    c.dfas[c.symbol2number[name]] = (states, self.make_first(c, name))

            else:
                c.start = c.symbol2number[self.startsymbol]
                return c

    def make_first(self, c, name):
        rawfirst = self.first[name]
        first = {}
        for label in sorted(rawfirst):
            ilabel = self.make_label(c, label)
            first[ilabel] = 1
        else:
            return first

    def make_label(self, c, label):
        ilabel = len(c.labels)
        if label[0].isalpha():
            if label in c.symbol2number:
                if label in c.symbol2label:
                    return c.symbol2label[label]
                c.labels.append((c.symbol2number[label], None))
                c.symbol2label[label] = ilabel
                return ilabel
            else:
                itoken = getattr(token, label, None)
                assert isinstance(itoken, int), label
                assert itoken in token.tok_name, label
                if itoken in c.tokens:
                    return c.tokens[itoken]
                c.labels.append((itoken, None))
                c.tokens[itoken] = ilabel
                return ilabel
        else:
            assert label[0] in ('"', "'"), label
            value = eval(label)
            if value[0].isalpha():
                if value in c.keywords:
                    return c.keywords[value]
                c.labels.append((token.NAME, value))
                c.keywords[value] = ilabel
                return ilabel
            else:
                itoken = grammar.opmap[value]
                if itoken in c.tokens:
                    return c.tokens[itoken]
                c.labels.append((itoken, None))
                c.tokens[itoken] = ilabel
                return ilabel

    def addfirstsets(self):
        names = list(self.dfas.keys())
        names.sort()
        for name in names:
            if name not in self.first:
                self.calcfirst(name)

    def calcfirst(self, name):
        dfa = self.dfas[name]
        self.first[name] = None
        state = dfa[0]
        totalset = {}
        overlapcheck = {}
        for label, next in state.arcs.items():
            if label in self.dfas:
                if label in self.first:
                    fset = self.first[label]
                    if fset is None:
                        raise ValueError('recursion for rule %r' % name)
                else:
                    self.calcfirst(label)
                    fset = self.first[label]
                totalset.update(fset)
                overlapcheck[label] = fset
            else:
                totalset[label] = 1
                overlapcheck[label] = {label: 1}
        else:
            inverse = {}
            for label, itsfirst in overlapcheck.items():
                for symbol in itsfirst:
                    if symbol in inverse:
                        raise ValueError('rule %s is ambiguous; %s is in the first sets of %s as well as %s' % (
                         name, symbol, label, inverse[symbol]))
                    else:
                        inverse[symbol] = label

            else:
                self.first[name] = totalset

    def parse(self):
        dfas = {}
        startsymbol = None
        while True:
            if self.type != token.ENDMARKER:
                while True:
                    if self.type == token.NEWLINE:
                        self.gettoken()

                name = self.expect(token.NAME)
                self.expect(token.OP, ':')
                a, z = self.parse_rhs()
                self.expect(token.NEWLINE)
                dfa = self.make_dfa(a, z)
                oldlen = len(dfa)
                self.simplify_dfa(dfa)
                newlen = len(dfa)
                dfas[name] = dfa
                if startsymbol is None:
                    startsymbol = name

        return (
         dfas, startsymbol)

    def make_dfa--- This code section failed: ---

 L. 174         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'start'
                4  LOAD_GLOBAL              NFAState
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  LOAD_ASSERT              AssertionError
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 175        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'finish'
               18  LOAD_GLOBAL              NFAState
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_TRUE     28  'to 28'
               24  LOAD_ASSERT              AssertionError
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'

 L. 176        28  LOAD_CLOSURE             'addclosure'
               30  BUILD_TUPLE_1         1 
               32  LOAD_CODE                <code_object closure>
               34  LOAD_STR                 'ParserGenerator.make_dfa.<locals>.closure'
               36  MAKE_FUNCTION_8          'closure'
               38  STORE_FAST               'closure'

 L. 180        40  LOAD_CLOSURE             'addclosure'
               42  BUILD_TUPLE_1         1 
               44  LOAD_CODE                <code_object addclosure>
               46  LOAD_STR                 'ParserGenerator.make_dfa.<locals>.addclosure'
               48  MAKE_FUNCTION_8          'closure'
               50  STORE_DEREF              'addclosure'

 L. 188        52  LOAD_GLOBAL              DFAState
               54  LOAD_FAST                'closure'
               56  LOAD_FAST                'start'
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_FAST                'finish'
               62  CALL_FUNCTION_2       2  ''
               64  BUILD_LIST_1          1 
               66  STORE_FAST               'states'

 L. 189        68  LOAD_FAST                'states'
               70  GET_ITER         
             72_0  COME_FROM           212  '212'
               72  FOR_ITER            214  'to 214'
               74  STORE_FAST               'state'

 L. 190        76  BUILD_MAP_0           0 
               78  STORE_FAST               'arcs'

 L. 191        80  LOAD_FAST                'state'
               82  LOAD_ATTR                nfaset
               84  GET_ITER         
             86_0  COME_FROM           132  '132'
               86  FOR_ITER            134  'to 134'
               88  STORE_FAST               'nfastate'

 L. 192        90  LOAD_FAST                'nfastate'
               92  LOAD_ATTR                arcs
               94  GET_ITER         
             96_0  COME_FROM           130  '130'
             96_1  COME_FROM           110  '110'
               96  FOR_ITER            132  'to 132'
               98  UNPACK_SEQUENCE_2     2 
              100  STORE_FAST               'label'
              102  STORE_FAST               'next'

 L. 193       104  LOAD_FAST                'label'
              106  LOAD_CONST               None
              108  COMPARE_OP               is-not
              110  POP_JUMP_IF_FALSE_BACK    96  'to 96'

 L. 194       112  LOAD_DEREF               'addclosure'
              114  LOAD_FAST                'next'
              116  LOAD_FAST                'arcs'
              118  LOAD_METHOD              setdefault
              120  LOAD_FAST                'label'
              122  BUILD_MAP_0           0 
              124  CALL_METHOD_2         2  ''
              126  CALL_FUNCTION_2       2  ''
              128  POP_TOP          
              130  JUMP_BACK            96  'to 96'
            132_0  COME_FROM            96  '96'
              132  JUMP_BACK            86  'to 86'
            134_0  COME_FROM            86  '86'

 L. 195       134  LOAD_GLOBAL              sorted
              136  LOAD_FAST                'arcs'
              138  LOAD_METHOD              items
              140  CALL_METHOD_0         0  ''
              142  CALL_FUNCTION_1       1  ''
              144  GET_ITER         
            146_0  COME_FROM           210  '210'
              146  FOR_ITER            212  'to 212'
              148  UNPACK_SEQUENCE_2     2 
              150  STORE_FAST               'label'
              152  STORE_FAST               'nfaset'

 L. 196       154  LOAD_FAST                'states'
              156  GET_ITER         
            158_0  COME_FROM           176  '176'
            158_1  COME_FROM           170  '170'
              158  FOR_ITER            178  'to 178'
              160  STORE_FAST               'st'

 L. 197       162  LOAD_FAST                'st'
              164  LOAD_ATTR                nfaset
              166  LOAD_FAST                'nfaset'
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE_BACK   158  'to 158'

 L. 198       172  POP_TOP          
              174  BREAK_LOOP          198  'to 198'
              176  JUMP_BACK           158  'to 158'
            178_0  COME_FROM           158  '158'

 L. 200       178  LOAD_GLOBAL              DFAState
              180  LOAD_FAST                'nfaset'
              182  LOAD_FAST                'finish'
              184  CALL_FUNCTION_2       2  ''
              186  STORE_FAST               'st'

 L. 201       188  LOAD_FAST                'states'
              190  LOAD_METHOD              append
              192  LOAD_FAST                'st'
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          
            198_0  COME_FROM           174  '174'

 L. 202       198  LOAD_FAST                'state'
              200  LOAD_METHOD              addarc
              202  LOAD_FAST                'st'
              204  LOAD_FAST                'label'
              206  CALL_METHOD_2         2  ''
              208  POP_TOP          
              210  JUMP_BACK           146  'to 146'
            212_0  COME_FROM           146  '146'
              212  JUMP_BACK            72  'to 72'
            214_0  COME_FROM            72  '72'

 L. 203       214  LOAD_FAST                'states'
              216  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 212

    def dump_nfa(self, name, start, finish):
        print('Dump of NFA for', name)
        todo = [start]
        for i, state in enumerate(todo):
            print('  State', i, (state is finish) and '(final)' or '')
            for label, next in state.arcs:
                if next in todo:
                    j = todo.index(next)
                else:
                    j = len(todo)
                    todo.append(next)
                if label is None:
                    print('    -> %d' % j)
                else:
                    print('    %s -> %d' % (label, j))

    def dump_dfa(self, name, dfa):
        print('Dump of DFA for', name)
        for i, state in enumerate(dfa):
            print('  State', i, (state.isfinal) and '(final)' or '')
            for label, next in sorted(state.arcs.items()):
                print('    %s -> %d' % (label, dfa.index(next)))

    def simplify_dfa(self, dfa):
        changes = True
        while changes:
            changes = False
            for i, state_i in enumerate(dfa):
                for j in range(i + 1, len(dfa)):
                    state_j = dfa[j]
                    if state_i == state_j:
                        del dfa[j]
                        for state in dfa:
                            state.unifystate(state_j, state_i)
                        else:
                            changes = True
                            break

    def parse_rhs(self):
        a, z = self.parse_alt()
        if self.value != '|':
            return (a, z)
        aa = NFAState()
        zz = NFAState()
        aa.addarc(a)
        z.addarc(zz)
        while True:
            if self.value == '|':
                self.gettoken()
                a, z = self.parse_alt()
                aa.addarc(a)
                z.addarc(zz)

        return (
         aa, zz)

    def parse_alt(self):
        a, b = self.parse_item()
        while self.value in ('(', '[') or self.type in (token.NAME, token.STRING):
            c, d = self.parse_item()
            b.addarc(c)
            b = d

        return (a, b)

    def parse_item(self):
        if self.value == '[':
            self.gettoken()
            a, z = self.parse_rhs()
            self.expect(token.OP, ']')
            a.addarc(z)
            return (
             a, z)
        a, z = self.parse_atom()
        value = self.value
        if value not in ('+', '*'):
            return (a, z)
        self.gettoken()
        z.addarc(a)
        if value == '+':
            return (a, z)
        return (
         a, a)

    def parse_atom(self):
        if self.value == '(':
            self.gettoken()
            a, z = self.parse_rhs()
            self.expect(token.OP, ')')
            return (
             a, z)
        if self.type in (token.NAME, token.STRING):
            a = NFAState()
            z = NFAState()
            a.addarc(z, self.value)
            self.gettoken()
            return (
             a, z)
        self.raise_error('expected (...) or NAME or STRING, got %s/%s', self.type, self.value)

    def expect(self, type, value=None):
        if not self.type != type:
            if not value is not None or self.value != value:
                self.raise_error('expected %s/%s, got %s/%s', type, value, self.type, self.value)
            value = self.value
            self.gettoken()
            return value

    def gettoken(self):
        tup = next(self.generator)
        while True:
            if tup[0] in (tokenize.COMMENT, tokenize.NL):
                tup = next(self.generator)

        self.type, self.value, self.begin, self.end, self.line = tup

    def raise_error(self, msg, *args):
        if args:
            try:
                msg = msg % args
            except:
                msg = ' '.join([msg] + list(map(str, args)))

        raise SyntaxError(msg, (self.filename, self.end[0],
         self.end[1], self.line))


class NFAState(object):

    def __init__(self):
        self.arcs = []

    def addarc(self, next, label=None):
        if not label is None:
            assert isinstance(label, str)
        assert isinstance(next, NFAState)
        self.arcs.append((label, next))


class DFAState(object):

    def __init__(self, nfaset, final):
        assert isinstance(nfaset, dict)
        assert isinstance(next(iter(nfaset)), NFAState)
        assert isinstance(final, NFAState)
        self.nfaset = nfaset
        self.isfinal = final in nfaset
        self.arcs = {}

    def addarc(self, next, label):
        assert isinstance(label, str)
        assert label not in self.arcs
        assert isinstance(next, DFAState)
        self.arcs[label] = next

    def unifystate(self, old, new):
        for label, next in self.arcs.items():
            if next is old:
                self.arcs[label] = new

    def __eq__(self, other):
        assert isinstance(other, DFAState)
        if self.isfinal != other.isfinal:
            return False
        if len(self.arcs) != len(other.arcs):
            return False
        for label, next in self.arcs.items():
            if next is not other.arcs.get(label):
                return False
        else:
            return True

    __hash__ = None


def generate_grammar(filename='Grammar.txt'):
    p = ParserGenerator(filename)
    return p.make_grammar()