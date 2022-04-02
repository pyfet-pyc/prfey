# uncompyle6 version 3.7.4
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
                    else:
                        if state.isfinal:
                            arcs.append((0, dfa.index(state)))
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
            if not label[0] in ('"', "'"):
                raise AssertionError(label)
            else:
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
                    inverse[symbol] = label

            else:
                self.first[name] = totalset

    def parse(self):
        dfas = {}
        startsymbol = None
        while self.type != token.ENDMARKER:
            if self.type == token.NEWLINE:
                self.gettoken()
            else:
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

    def make_dfa(self, start, finish):
        assert isinstance(start, NFAState)
        assert isinstance(finish, NFAState)

        def closure(state):
            base = {}
            addclosure(state, base)
            return base

        def addclosure(state, base):
            assert isinstance(state, NFAState)
            if state in base:
                return
            base[state] = 1
            for label, next in state.arcs:
                if label is None:
                    addclosure(next, base)

        states = [
         DFAState(closure(start), finish)]
        for state in states:
            arcs = {}
            for nfastate in state.nfaset:
                for label, next in nfastate.arcs:
                    if label is not None:
                        addclosure(next, arcs.setdefault(label, {}))
                else:
                    for label, nfaset in sorted(arcs.items()):
                        for st in states:
                            if st.nfaset == nfaset:
                                break
                            st = DFAState(nfaset, finish)
                            states.append(st)
                            state.addarc(st, label)
                        else:
                            return states

    def dump_nfa(self, name, start, finish):
        print('Dump of NFA for', name)
        todo = [start]
        for i, state in enumerate(todo):
            print('  State', i, state is finish and '(final)' or '')
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
            print('  State', i, state.isfinal and '(final)' or '')
            for label, next in sorted(state.arcs.items()):
                print('    %s -> %d' % (label, dfa.index(next)))

    def simplify_dfa--- This code section failed: ---

 L. 235         0  LOAD_CONST               True
                2  STORE_FAST               'changes'

 L. 236         4  LOAD_FAST                'changes'
                6  POP_JUMP_IF_FALSE   108  'to 108'

 L. 237         8  LOAD_CONST               False
               10  STORE_FAST               'changes'

 L. 238        12  LOAD_GLOBAL              enumerate
               14  LOAD_FAST                'dfa'
               16  CALL_FUNCTION_1       1  ''
               18  GET_ITER         
               20  FOR_ITER            106  'to 106'
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'i'
               26  STORE_FAST               'state_i'

 L. 239        28  LOAD_GLOBAL              range
               30  LOAD_FAST                'i'
               32  LOAD_CONST               1
               34  BINARY_ADD       
               36  LOAD_GLOBAL              len
               38  LOAD_FAST                'dfa'
               40  CALL_FUNCTION_1       1  ''
               42  CALL_FUNCTION_2       2  ''
               44  GET_ITER         
             46_0  COME_FROM            64  '64'
               46  FOR_ITER            104  'to 104'
               48  STORE_FAST               'j'

 L. 240        50  LOAD_FAST                'dfa'
               52  LOAD_FAST                'j'
               54  BINARY_SUBSCR    
               56  STORE_FAST               'state_j'

 L. 241        58  LOAD_FAST                'state_i'
               60  LOAD_FAST                'state_j'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    46  'to 46'

 L. 243        66  LOAD_FAST                'dfa'
               68  LOAD_FAST                'j'
               70  DELETE_SUBSCR    

 L. 244        72  LOAD_FAST                'dfa'
               74  GET_ITER         
               76  FOR_ITER             94  'to 94'
               78  STORE_FAST               'state'

 L. 245        80  LOAD_FAST                'state'
               82  LOAD_METHOD              unifystate
               84  LOAD_FAST                'state_j'
               86  LOAD_FAST                'state_i'
               88  CALL_METHOD_2         2  ''
               90  POP_TOP          
               92  JUMP_BACK            76  'to 76'

 L. 246        94  LOAD_CONST               True
               96  STORE_FAST               'changes'

 L. 247        98  POP_TOP          
              100  CONTINUE             20  'to 20'
              102  JUMP_BACK            46  'to 46'
              104  JUMP_BACK            20  'to 20'
              106  JUMP_BACK             4  'to 4'
            108_0  COME_FROM             6  '6'

Parse error at or near `CONTINUE' instruction at offset 100

    def parse_rhs(self):
        a, z = self.parse_alt()
        if self.value != '|':
            return (
             a, z)
        else:
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
        while not self.value in ('(', '['):
            if self.type in (token.NAME, token.STRING):
                c, d = self.parse_item()
                b.addarc(c)
                b = d

        return (
         a, b)

    def parse_item(self):
        if self.value == '[':
            self.gettoken()
            a, z = self.parse_rhs()
            self.expect(token.OP, ']')
            a.addarc(z)
            return (a, z)
        a, z = self.parse_atom()
        value = self.value
        if value not in ('+', '*'):
            return (
             a, z)
        self.gettoken()
        z.addarc(a)
        if value == '+':
            return (
             a, z)
        return (a, a)

    def parse_atom(self):
        if self.value == '(':
            self.gettoken()
            a, z = self.parse_rhs()
            self.expect(token.OP, ')')
            return (a, z)
        if self.type in (token.NAME, token.STRING):
            a = NFAState()
            z = NFAState()
            a.addarc(z, self.value)
            self.gettoken()
            return (a, z)
        self.raise_error('expected (...) or NAME or STRING, got %s/%s', self.type, self.value)

    def expect(self, type, value=None):
        if (self.type != type or value) is not None:
            if self.value != value:
                self.raise_error('expected %s/%s, got %s/%s', type, value, self.type, self.value)
        value = self.value
        self.gettoken()
        return value

    def gettoken(self):
        tup = next(self.generator)
        while tup[0] in (tokenize.COMMENT, tokenize.NL):
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
            return True

    __hash__ = None


def generate_grammar(filename='Grammar.txt'):
    p = ParserGenerator(filename)
    return p.make_grammar()