# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pycparser\ply\lex.py
__version__ = '3.10'
__tabversion__ = '3.10'
import re, sys, types, copy, os, inspect
try:
    StringTypes = (
     types.StringType, types.UnicodeType)
except AttributeError:
    StringTypes = (
     str, bytes)

_is_identifier = re.compile('^[a-zA-Z0-9_]+$')

class LexError(Exception):

    def __init__(self, message, s):
        self.args = (
         message,)
        self.text = s


class LexToken(object):

    def __str__(self):
        return 'LexToken(%s,%r,%d,%d)' % (self.type, self.value, self.lineno, self.lexpos)

    def __repr__(self):
        return str(self)


class PlyLogger(object):

    def __init__(self, f):
        self.f = f

    def critical(self, msg, *args, **kwargs):
        self.f.write(msg % args + '\n')

    def warning(self, msg, *args, **kwargs):
        self.f.write('WARNING: ' + msg % args + '\n')

    def error(self, msg, *args, **kwargs):
        self.f.write('ERROR: ' + msg % args + '\n')

    info = critical
    debug = critical


class NullLogger(object):

    def __getattribute__(self, name):
        return self

    def __call__(self, *args, **kwargs):
        return self


class Lexer:

    def __init__(self):
        self.lexre = None
        self.lexretext = None
        self.lexstatere = {}
        self.lexstateretext = {}
        self.lexstaterenames = {}
        self.lexstate = 'INITIAL'
        self.lexstatestack = []
        self.lexstateinfo = None
        self.lexstateignore = {}
        self.lexstateerrorf = {}
        self.lexstateeoff = {}
        self.lexreflags = 0
        self.lexdata = None
        self.lexpos = 0
        self.lexlen = 0
        self.lexerrorf = None
        self.lexeoff = None
        self.lextokens = None
        self.lexignore = ''
        self.lexliterals = ''
        self.lexmodule = None
        self.lineno = 1
        self.lexoptimize = False

    def clone(self, object=None):
        c = copy.copy(self)
        if object:
            newtab = {}
            for key, ritem in self.lexstatere.items():
                newre = []
                for cre, findex in ritem:
                    newfindex = []
                    for f in findex:
                        if not f or not f[0]:
                            newfindex.append(f)
                            continue
                        newfindex.append((getattr(object, f[0].__name__), f[1]))

                newre.append((cre, newfindex))
                newtab[key] = newre

            c.lexstatere = newtab
            c.lexstateerrorf = {}
            for key, ef in self.lexstateerrorf.items():
                c.lexstateerrorf[key] = getattr(object, ef.__name__)

            c.lexmodule = object
        return c

    def writetab(self, lextab, outputdir=''):
        if isinstance(lextab, types.ModuleType):
            raise IOError("Won't overwrite existing lextab module")
        basetabmodule = lextab.split('.')[(-1)]
        filename = os.path.join(outputdir, basetabmodule) + '.py'
        with open(filename, 'w') as (tf):
            tf.write("# %s.py. This file automatically created by PLY (version %s). Don't edit!\n" % (basetabmodule, __version__))
            tf.write('_tabversion   = %s\n' % repr(__tabversion__))
            tf.write('_lextokens    = set(%s)\n' % repr(tuple(self.lextokens)))
            tf.write('_lexreflags   = %s\n' % repr(self.lexreflags))
            tf.write('_lexliterals  = %s\n' % repr(self.lexliterals))
            tf.write('_lexstateinfo = %s\n' % repr(self.lexstateinfo))
            tabre = {}
            for statename, lre in self.lexstatere.items():
                titem = []
                for (pat, func), retext, renames in zip(lre, self.lexstateretext[statename], self.lexstaterenames[statename]):
                    titem.append((retext, _funcs_to_names(func, renames)))

                tabre[statename] = titem

            tf.write('_lexstatere   = %s\n' % repr(tabre))
            tf.write('_lexstateignore = %s\n' % repr(self.lexstateignore))
            taberr = {}
            for statename, ef in self.lexstateerrorf.items():
                taberr[statename] = ef.__name__ if ef else None

            tf.write('_lexstateerrorf = %s\n' % repr(taberr))
            tabeof = {}
            for statename, ef in self.lexstateeoff.items():
                tabeof[statename] = ef.__name__ if ef else None

            tf.write('_lexstateeoff = %s\n' % repr(tabeof))

    def readtab(self, tabfile, fdict):
        if isinstance(tabfile, types.ModuleType):
            lextab = tabfile
        else:
            exec('import %s' % tabfile)
            lextab = sys.modules[tabfile]
        if getattr(lextab, '_tabversion', '0.0') != __tabversion__:
            raise ImportError('Inconsistent PLY version')
        self.lextokens = lextab._lextokens
        self.lexreflags = lextab._lexreflags
        self.lexliterals = lextab._lexliterals
        self.lextokens_all = self.lextokens | set(self.lexliterals)
        self.lexstateinfo = lextab._lexstateinfo
        self.lexstateignore = lextab._lexstateignore
        self.lexstatere = {}
        self.lexstateretext = {}
        for statename, lre in lextab._lexstatere.items():
            titem = []
            txtitem = []
            for pat, func_name in lre:
                titem.append((re.compile(pat, lextab._lexreflags), _names_to_funcs(func_name, fdict)))

            self.lexstatere[statename] = titem
            self.lexstateretext[statename] = txtitem

        self.lexstateerrorf = {}
        for statename, ef in lextab._lexstateerrorf.items():
            self.lexstateerrorf[statename] = fdict[ef]

        self.lexstateeoff = {}
        for statename, ef in lextab._lexstateeoff.items():
            self.lexstateeoff[statename] = fdict[ef]

        self.begin('INITIAL')

    def input(self, s):
        c = s[:1]
        if not isinstance(c, StringTypes):
            raise ValueError('Expected a string')
        self.lexdata = s
        self.lexpos = 0
        self.lexlen = len(s)

    def begin(self, state):
        if state not in self.lexstatere:
            raise ValueError('Undefined state')
        self.lexre = self.lexstatere[state]
        self.lexretext = self.lexstateretext[state]
        self.lexignore = self.lexstateignore.get(state, '')
        self.lexerrorf = self.lexstateerrorf.get(state, None)
        self.lexeoff = self.lexstateeoff.get(state, None)
        self.lexstate = state

    def push_state(self, state):
        self.lexstatestack.append(self.lexstate)
        self.begin(state)

    def pop_state(self):
        self.begin(self.lexstatestack.pop())

    def current_state(self):
        return self.lexstate

    def skip(self, n):
        self.lexpos += n

    def token--- This code section failed: ---

 L. 307         0  LOAD_FAST                'self'
                3  LOAD_ATTR                lexpos
                6  STORE_FAST               'lexpos'

 L. 308         9  LOAD_FAST                'self'
               12  LOAD_ATTR                lexlen
               15  STORE_FAST               'lexlen'

 L. 309        18  LOAD_FAST                'self'
               21  LOAD_ATTR                lexignore
               24  STORE_FAST               'lexignore'

 L. 310        27  LOAD_FAST                'self'
               30  LOAD_ATTR                lexdata
               33  STORE_FAST               'lexdata'

 L. 312        36  SETUP_LOOP          756  'to 756'
               39  LOAD_FAST                'lexpos'
               42  LOAD_FAST                'lexlen'
               45  COMPARE_OP               <
               48  POP_JUMP_IF_FALSE   755  'to 755'

 L. 314        51  LOAD_FAST                'lexdata'
               54  LOAD_FAST                'lexpos'
               57  BINARY_SUBSCR    
               58  LOAD_FAST                'lexignore'
               61  COMPARE_OP               in
               64  POP_JUMP_IF_FALSE    83  'to 83'

 L. 315        67  LOAD_FAST                'lexpos'
               70  LOAD_CONST               1
               73  INPLACE_ADD      
               74  STORE_FAST               'lexpos'

 L. 316        77  CONTINUE             39  'to 39'
               80  JUMP_FORWARD         83  'to 83'
             83_0  COME_FROM            80  '80'

 L. 319        83  SETUP_LOOP          752  'to 752'
               86  LOAD_FAST                'self'
               89  LOAD_ATTR                lexre
               92  GET_ITER         
               93  FOR_ITER            433  'to 433'
               96  UNPACK_SEQUENCE_2     2 
               99  STORE_FAST               'lexre'
              102  STORE_FAST               'lexindexfunc'

 L. 320       105  LOAD_FAST                'lexre'
              108  LOAD_ATTR                match
              111  LOAD_FAST                'lexdata'
              114  LOAD_FAST                'lexpos'
              117  CALL_FUNCTION_2       2  '2 positional, 0 named'
              120  STORE_FAST               'm'

 L. 321       123  LOAD_FAST                'm'
              126  POP_JUMP_IF_TRUE    135  'to 135'
            129_0  COME_FROM           126  '126'

 L. 322       129  CONTINUE             93  'to 93'
              132  JUMP_FORWARD        135  'to 135'
            135_0  COME_FROM           132  '132'

 L. 325       135  LOAD_GLOBAL              LexToken
              138  CALL_FUNCTION_0       0  '0 positional, 0 named'
              141  STORE_FAST               'tok'

 L. 326       144  LOAD_FAST                'm'
              147  LOAD_ATTR                group
              150  CALL_FUNCTION_0       0  '0 positional, 0 named'
              153  LOAD_FAST                'tok'
              156  STORE_ATTR               value

 L. 327       159  LOAD_FAST                'self'
              162  LOAD_ATTR                lineno
              165  LOAD_FAST                'tok'
              168  STORE_ATTR               lineno

 L. 328       171  LOAD_FAST                'lexpos'
              174  LOAD_FAST                'tok'
              177  STORE_ATTR               lexpos

 L. 330       180  LOAD_FAST                'm'
              183  LOAD_ATTR                lastindex
              186  STORE_FAST               'i'

 L. 331       189  LOAD_FAST                'lexindexfunc'
              192  LOAD_FAST                'i'
              195  BINARY_SUBSCR    
              196  UNPACK_SEQUENCE_2     2 
              199  STORE_FAST               'func'
              202  LOAD_FAST                'tok'
              205  STORE_ATTR               type

 L. 333       208  LOAD_FAST                'func'
              211  POP_JUMP_IF_TRUE    258  'to 258'

 L. 335       214  LOAD_FAST                'tok'
              217  LOAD_ATTR                type
              220  POP_JUMP_IF_FALSE   242  'to 242'

 L. 336       223  LOAD_FAST                'm'
              226  LOAD_ATTR                end
              229  CALL_FUNCTION_0       0  '0 positional, 0 named'
              232  LOAD_FAST                'self'
              235  STORE_ATTR               lexpos

 L. 337       238  LOAD_FAST                'tok'
              241  RETURN_END_IF    
            242_0  COME_FROM           220  '220'

 L. 339       242  LOAD_FAST                'm'
              245  LOAD_ATTR                end
              248  CALL_FUNCTION_0       0  '0 positional, 0 named'
              251  STORE_FAST               'lexpos'

 L. 340       254  BREAK_LOOP       
              255  JUMP_FORWARD        258  'to 258'
            258_0  COME_FROM           255  '255'

 L. 342       258  LOAD_FAST                'm'
              261  LOAD_ATTR                end
              264  CALL_FUNCTION_0       0  '0 positional, 0 named'
              267  STORE_FAST               'lexpos'

 L. 346       270  LOAD_FAST                'self'
              273  LOAD_FAST                'tok'
              276  STORE_ATTR               lexer

 L. 347       279  LOAD_FAST                'm'
              282  LOAD_FAST                'self'
              285  STORE_ATTR               lexmatch

 L. 348       288  LOAD_FAST                'lexpos'
              291  LOAD_FAST                'self'
              294  STORE_ATTR               lexpos

 L. 350       297  LOAD_FAST                'func'
              300  LOAD_FAST                'tok'
              303  CALL_FUNCTION_1       1  '1 positional, 0 named'
              306  STORE_FAST               'newtok'

 L. 353       309  LOAD_FAST                'newtok'
              312  POP_JUMP_IF_TRUE    337  'to 337'

 L. 354       315  LOAD_FAST                'self'
              318  LOAD_ATTR                lexpos
              321  STORE_FAST               'lexpos'

 L. 355       324  LOAD_FAST                'self'
              327  LOAD_ATTR                lexignore
              330  STORE_FAST               'lexignore'

 L. 356       333  BREAK_LOOP       
              334  JUMP_FORWARD        337  'to 337'
            337_0  COME_FROM           334  '334'

 L. 359       337  LOAD_FAST                'self'
              340  LOAD_ATTR                lexoptimize
              343  POP_JUMP_IF_TRUE    429  'to 429'

 L. 360       346  LOAD_FAST                'newtok'
              349  LOAD_ATTR                type
              352  LOAD_FAST                'self'
              355  LOAD_ATTR                lextokens_all
              358  COMPARE_OP               not-in
              361  POP_JUMP_IF_FALSE   429  'to 429'

 L. 361       364  LOAD_GLOBAL              LexError
              367  LOAD_STR                 "%s:%d: Rule '%s' returned an unknown token type '%s'"

 L. 362       370  LOAD_FAST                'func'
              373  LOAD_ATTR                __code__
              376  LOAD_ATTR                co_filename
              379  LOAD_FAST                'func'
              382  LOAD_ATTR                __code__
              385  LOAD_ATTR                co_firstlineno

 L. 363       388  LOAD_FAST                'func'
              391  LOAD_ATTR                __name__
              394  LOAD_FAST                'newtok'
              397  LOAD_ATTR                type
              400  BUILD_TUPLE_4         4 
              403  BINARY_MODULO    
              404  LOAD_FAST                'lexdata'
              407  LOAD_FAST                'lexpos'
              410  LOAD_CONST               None
              413  BUILD_SLICE_2         2 
              416  BINARY_SUBSCR    
              417  CALL_FUNCTION_2       2  '2 positional, 0 named'
              420  RAISE_VARARGS_1       1  'exception'
              423  JUMP_ABSOLUTE       429  'to 429'
              426  JUMP_FORWARD        429  'to 429'
            429_0  COME_FROM           426  '426'

 L. 365       429  LOAD_FAST                'newtok'
              432  RETURN_VALUE     
              433  POP_BLOCK        

 L. 368       434  LOAD_FAST                'lexdata'
              437  LOAD_FAST                'lexpos'
              440  BINARY_SUBSCR    
              441  LOAD_FAST                'self'
              444  LOAD_ATTR                lexliterals
              447  COMPARE_OP               in
              450  POP_JUMP_IF_FALSE   525  'to 525'

 L. 369       453  LOAD_GLOBAL              LexToken
              456  CALL_FUNCTION_0       0  '0 positional, 0 named'
              459  STORE_FAST               'tok'

 L. 370       462  LOAD_FAST                'lexdata'
              465  LOAD_FAST                'lexpos'
              468  BINARY_SUBSCR    
              469  LOAD_FAST                'tok'
              472  STORE_ATTR               value

 L. 371       475  LOAD_FAST                'self'
              478  LOAD_ATTR                lineno
              481  LOAD_FAST                'tok'
              484  STORE_ATTR               lineno

 L. 372       487  LOAD_FAST                'tok'
              490  LOAD_ATTR                value
              493  LOAD_FAST                'tok'
              496  STORE_ATTR               type

 L. 373       499  LOAD_FAST                'lexpos'
              502  LOAD_FAST                'tok'
              505  STORE_ATTR               lexpos

 L. 374       508  LOAD_FAST                'lexpos'
              511  LOAD_CONST               1
              514  BINARY_ADD       
              515  LOAD_FAST                'self'
              518  STORE_ATTR               lexpos

 L. 375       521  LOAD_FAST                'tok'
              524  RETURN_END_IF    
            525_0  COME_FROM           450  '450'

 L. 378       525  LOAD_FAST                'self'
              528  LOAD_ATTR                lexerrorf
              531  POP_JUMP_IF_FALSE   704  'to 704'

 L. 379       534  LOAD_GLOBAL              LexToken
              537  CALL_FUNCTION_0       0  '0 positional, 0 named'
              540  STORE_FAST               'tok'

 L. 380       543  LOAD_FAST                'self'
              546  LOAD_ATTR                lexdata
              549  LOAD_FAST                'lexpos'
              552  LOAD_CONST               None
              555  BUILD_SLICE_2         2 
              558  BINARY_SUBSCR    
              559  LOAD_FAST                'tok'
              562  STORE_ATTR               value

 L. 381       565  LOAD_FAST                'self'
              568  LOAD_ATTR                lineno
              571  LOAD_FAST                'tok'
              574  STORE_ATTR               lineno

 L. 382       577  LOAD_STR                 'error'
              580  LOAD_FAST                'tok'
              583  STORE_ATTR               type

 L. 383       586  LOAD_FAST                'self'
              589  LOAD_FAST                'tok'
              592  STORE_ATTR               lexer

 L. 384       595  LOAD_FAST                'lexpos'
              598  LOAD_FAST                'tok'
              601  STORE_ATTR               lexpos

 L. 385       604  LOAD_FAST                'lexpos'
              607  LOAD_FAST                'self'
              610  STORE_ATTR               lexpos

 L. 386       613  LOAD_FAST                'self'
              616  LOAD_ATTR                lexerrorf
              619  LOAD_FAST                'tok'
              622  CALL_FUNCTION_1       1  '1 positional, 0 named'
              625  STORE_FAST               'newtok'

 L. 387       628  LOAD_FAST                'lexpos'
              631  LOAD_FAST                'self'
              634  LOAD_ATTR                lexpos
              637  COMPARE_OP               ==
              640  POP_JUMP_IF_FALSE   679  'to 679'

 L. 389       643  LOAD_GLOBAL              LexError
              646  LOAD_STR                 "Scanning error. Illegal character '%s'"
              649  LOAD_FAST                'lexdata'
              652  LOAD_FAST                'lexpos'
              655  BINARY_SUBSCR    
              656  BINARY_MODULO    
              657  LOAD_FAST                'lexdata'
              660  LOAD_FAST                'lexpos'
              663  LOAD_CONST               None
              666  BUILD_SLICE_2         2 
              669  BINARY_SUBSCR    
              670  CALL_FUNCTION_2       2  '2 positional, 0 named'
              673  RAISE_VARARGS_1       1  'exception'
              676  JUMP_FORWARD        679  'to 679'
            679_0  COME_FROM           676  '676'

 L. 390       679  LOAD_FAST                'self'
              682  LOAD_ATTR                lexpos
              685  STORE_FAST               'lexpos'

 L. 391       688  LOAD_FAST                'newtok'
              691  POP_JUMP_IF_TRUE    700  'to 700'

 L. 392       694  CONTINUE             39  'to 39'
              697  JUMP_FORWARD        700  'to 700'
            700_0  COME_FROM           697  '697'

 L. 393       700  LOAD_FAST                'newtok'
              703  RETURN_END_IF    
            704_0  COME_FROM           531  '531'

 L. 395       704  LOAD_FAST                'lexpos'
              707  LOAD_FAST                'self'
              710  STORE_ATTR               lexpos

 L. 396       713  LOAD_GLOBAL              LexError
              716  LOAD_STR                 "Illegal character '%s' at index %d"
              719  LOAD_FAST                'lexdata'
              722  LOAD_FAST                'lexpos'
              725  BINARY_SUBSCR    
              726  LOAD_FAST                'lexpos'
              729  BUILD_TUPLE_2         2 
              732  BINARY_MODULO    
              733  LOAD_FAST                'lexdata'
              736  LOAD_FAST                'lexpos'
              739  LOAD_CONST               None
              742  BUILD_SLICE_2         2 
              745  BINARY_SUBSCR    
              746  CALL_FUNCTION_2       2  '2 positional, 0 named'
              749  RAISE_VARARGS_1       1  'exception'
            752_0  COME_FROM_LOOP       83  '83'
              752  JUMP_BACK            39  'to 39'
              755  POP_BLOCK        
            756_0  COME_FROM_LOOP       36  '36'

 L. 398       756  LOAD_FAST                'self'
              759  LOAD_ATTR                lexeoff
              762  POP_JUMP_IF_FALSE   850  'to 850'

 L. 399       765  LOAD_GLOBAL              LexToken
              768  CALL_FUNCTION_0       0  '0 positional, 0 named'
              771  STORE_FAST               'tok'

 L. 400       774  LOAD_STR                 'eof'
              777  LOAD_FAST                'tok'
              780  STORE_ATTR               type

 L. 401       783  LOAD_STR                 ''
              786  LOAD_FAST                'tok'
              789  STORE_ATTR               value

 L. 402       792  LOAD_FAST                'self'
              795  LOAD_ATTR                lineno
              798  LOAD_FAST                'tok'
              801  STORE_ATTR               lineno

 L. 403       804  LOAD_FAST                'lexpos'
              807  LOAD_FAST                'tok'
              810  STORE_ATTR               lexpos

 L. 404       813  LOAD_FAST                'self'
              816  LOAD_FAST                'tok'
              819  STORE_ATTR               lexer

 L. 405       822  LOAD_FAST                'lexpos'
              825  LOAD_FAST                'self'
              828  STORE_ATTR               lexpos

 L. 406       831  LOAD_FAST                'self'
              834  LOAD_ATTR                lexeoff
              837  LOAD_FAST                'tok'
              840  CALL_FUNCTION_1       1  '1 positional, 0 named'
              843  STORE_FAST               'newtok'

 L. 407       846  LOAD_FAST                'newtok'
              849  RETURN_END_IF    
            850_0  COME_FROM           762  '762'

 L. 409       850  LOAD_FAST                'lexpos'
              853  LOAD_CONST               1
              856  BINARY_ADD       
              857  LOAD_FAST                'self'
              860  STORE_ATTR               lexpos

 L. 410       863  LOAD_FAST                'self'
              866  LOAD_ATTR                lexdata
              869  LOAD_CONST               None
              872  COMPARE_OP               is
              875  POP_JUMP_IF_FALSE   893  'to 893'

 L. 411       878  LOAD_GLOBAL              RuntimeError
              881  LOAD_STR                 'No input string given with input()'
              884  CALL_FUNCTION_1       1  '1 positional, 0 named'
              887  RAISE_VARARGS_1       1  'exception'
              890  JUMP_FORWARD        893  'to 893'
            893_0  COME_FROM           890  '890'

Parse error at or near `JUMP_FORWARD' instruction at offset 132

    def __iter__(self):
        return self

    def next(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

    __next__ = next


def _get_regex(func):
    return getattr(func, 'regex', func.__doc__)


def get_caller_module_dict(levels):
    f = sys._getframe(levels)
    ldict = f.f_globals.copy()
    if f.f_globals != f.f_locals:
        ldict.update(f.f_locals)
    return ldict


def _funcs_to_names(funclist, namelist):
    result = []
    for f, name in zip(funclist, namelist):
        if f and f[0]:
            result.append((name, f[1]))
        else:
            result.append(f)

    return result


def _names_to_funcs(namelist, fdict):
    result = []
    for n in namelist:
        if n and n[0]:
            result.append((fdict[n[0]], n[1]))
        else:
            result.append(n)

    return result


def _form_master_re(relist, reflags, ldict, toknames):
    if not relist:
        return []
    regex = '|'.join(relist)
    try:
        lexre = re.compile(regex, reflags)
        lexindexfunc = [
         None] * (max(lexre.groupindex.values()) + 1)
        lexindexnames = lexindexfunc[:]
        for f, i in lexre.groupindex.items():
            handle = ldict.get(f, None)
            if type(handle) in (types.FunctionType, types.MethodType):
                lexindexfunc[i] = (
                 handle, toknames[f])
                lexindexnames[i] = f
            elif handle is not None:
                lexindexnames[i] = f
                if f.find('ignore_') > 0:
                    lexindexfunc[i] = (None, None)
                else:
                    lexindexfunc[i] = (
                     None, toknames[f])
                    continue

        return (
         [
          (
           lexre, lexindexfunc)], [regex], [lexindexnames])
    except Exception:
        m = int(len(relist) / 2)
        if m == 0:
            m = 1
        llist, lre, lnames = _form_master_re(relist[:m], reflags, ldict, toknames)
        rlist, rre, rnames = _form_master_re(relist[m:], reflags, ldict, toknames)
        return (llist + rlist, lre + rre, lnames + rnames)


def _statetoken(s, names):
    nonstate = 1
    parts = s.split('_')
    for i, part in enumerate(parts[1:], 1):
        if part not in names and part != 'ANY':
            break

    if i > 1:
        states = tuple(parts[1:i])
    else:
        states = ('INITIAL', )
    if 'ANY' in states:
        states = tuple(names)
    tokenname = '_'.join(parts[i:])
    return (states, tokenname)


class LexerReflect(object):

    def __init__(self, ldict, log=None, reflags=0):
        self.ldict = ldict
        self.error_func = None
        self.tokens = []
        self.reflags = reflags
        self.stateinfo = {'INITIAL': 'inclusive'}
        self.modules = set()
        self.error = False
        self.log = PlyLogger(sys.stderr) if log is None else log

    def get_all(self):
        self.get_tokens()
        self.get_literals()
        self.get_states()
        self.get_rules()

    def validate_all(self):
        self.validate_tokens()
        self.validate_literals()
        self.validate_rules()
        return self.error

    def get_tokens(self):
        tokens = self.ldict.get('tokens', None)
        if not tokens:
            self.log.error('No token list is defined')
            self.error = True
            return
        if not isinstance(tokens, (list, tuple)):
            self.log.error('tokens must be a list or tuple')
            self.error = True
            return
        if not tokens:
            self.log.error('tokens is empty')
            self.error = True
            return
        self.tokens = tokens

    def validate_tokens(self):
        terminals = {}
        for n in self.tokens:
            if not _is_identifier.match(n):
                self.log.error("Bad token name '%s'", n)
                self.error = True
            if n in terminals:
                self.log.warning("Token '%s' multiply defined", n)
            terminals[n] = 1

    def get_literals(self):
        self.literals = self.ldict.get('literals', '')
        if not self.literals:
            self.literals = ''

    def validate_literals(self):
        try:
            for c in self.literals:
                if not isinstance(c, StringTypes) or len(c) > 1:
                    self.log.error('Invalid literal %s. Must be a single character', repr(c))
                    self.error = True
                    continue

        except TypeError:
            self.log.error('Invalid literals specification. literals must be a sequence of characters')
            self.error = True

    def get_states(self):
        self.states = self.ldict.get('states', None)
        if self.states:
            if not isinstance(self.states, (tuple, list)):
                self.log.error('states must be defined as a tuple or list')
                self.error = True
            else:
                for s in self.states:
                    if not isinstance(s, tuple) or len(s) != 2:
                        self.log.error("Invalid state specifier %s. Must be a tuple (statename,'exclusive|inclusive')", repr(s))
                        self.error = True
                        continue
                    name, statetype = s
                    if not isinstance(name, StringTypes):
                        self.log.error('State name %s must be a string', repr(name))
                        self.error = True
                        continue
                    if not (statetype == 'inclusive' or statetype == 'exclusive'):
                        self.log.error("State type for state %s must be 'inclusive' or 'exclusive'", name)
                        self.error = True
                        continue
                    if name in self.stateinfo:
                        self.log.error("State '%s' already defined", name)
                        self.error = True
                        continue
                    self.stateinfo[name] = statetype

    def get_rules(self):
        tsymbols = [f for f in self.ldict if f[:2] == 't_']
        self.toknames = {}
        self.funcsym = {}
        self.strsym = {}
        self.ignore = {}
        self.errorf = {}
        self.eoff = {}
        for s in self.stateinfo:
            self.funcsym[s] = []
            self.strsym[s] = []

        if len(tsymbols) == 0:
            self.log.error('No rules of the form t_rulename are defined')
            self.error = True
            return
        for f in tsymbols:
            t = self.ldict[f]
            states, tokname = _statetoken(f, self.stateinfo)
            self.toknames[f] = tokname
            if hasattr(t, '__call__'):
                if tokname == 'error':
                    for s in states:
                        self.errorf[s] = t

                else:
                    if tokname == 'eof':
                        for s in states:
                            self.eoff[s] = t

                    else:
                        if tokname == 'ignore':
                            line = t.__code__.co_firstlineno
                            file = t.__code__.co_filename
                            self.log.error("%s:%d: Rule '%s' must be defined as a string", file, line, t.__name__)
                            self.error = True
                        else:
                            for s in states:
                                self.funcsym[s].append((f, t))

            elif isinstance(t, StringTypes):
                if tokname == 'ignore':
                    for s in states:
                        self.ignore[s] = t

                    if '\\' in t:
                        self.log.warning("%s contains a literal backslash '\\'", f)
                else:
                    if tokname == 'error':
                        self.log.error("Rule '%s' must be defined as a function", f)
                        self.error = True
                    else:
                        for s in states:
                            self.strsym[s].append((f, t))

            else:
                self.log.error('%s not defined as a function or string', f)
                self.error = True

        for f in self.funcsym.values():
            f.sort(key=lambda x: x[1].__code__.co_firstlineno)

        for s in self.strsym.values():
            s.sort(key=lambda x: len(x[1]), reverse=True)

    def validate_rules(self):
        for state in self.stateinfo:
            for fname, f in self.funcsym[state]:
                line = f.__code__.co_firstlineno
                file = f.__code__.co_filename
                module = inspect.getmodule(f)
                self.modules.add(module)
                tokname = self.toknames[fname]
                if isinstance(f, types.MethodType):
                    reqargs = 2
                else:
                    reqargs = 1
                nargs = f.__code__.co_argcount
                if nargs > reqargs:
                    self.log.error("%s:%d: Rule '%s' has too many arguments", file, line, f.__name__)
                    self.error = True
                    continue
                if nargs < reqargs:
                    self.log.error("%s:%d: Rule '%s' requires an argument", file, line, f.__name__)
                    self.error = True
                    continue
                if not _get_regex(f):
                    self.log.error("%s:%d: No regular expression defined for rule '%s'", file, line, f.__name__)
                    self.error = True
                    continue
                try:
                    c = re.compile('(?P<%s>%s)' % (fname, _get_regex(f)), self.reflags)
                    if c.match(''):
                        self.log.error("%s:%d: Regular expression for rule '%s' matches empty string", file, line, f.__name__)
                        self.error = True
                except re.error as e:
                    self.log.error("%s:%d: Invalid regular expression for rule '%s'. %s", file, line, f.__name__, e)
                    if '#' in _get_regex(f):
                        self.log.error("%s:%d. Make sure '#' in rule '%s' is escaped with '\\#'", file, line, f.__name__)
                    self.error = True

            for name, r in self.strsym[state]:
                tokname = self.toknames[name]
                if tokname == 'error':
                    self.log.error("Rule '%s' must be defined as a function", name)
                    self.error = True
                    continue
                if tokname not in self.tokens:
                    if tokname.find('ignore_') < 0:
                        self.log.error("Rule '%s' defined for an unspecified token %s", name, tokname)
                        self.error = True
                        continue
                    try:
                        c = re.compile('(?P<%s>%s)' % (name, r), self.reflags)
                        if c.match(''):
                            self.log.error("Regular expression for rule '%s' matches empty string", name)
                            self.error = True
                    except re.error as e:
                        self.log.error("Invalid regular expression for rule '%s'. %s", name, e)
                        if '#' in r:
                            self.log.error("Make sure '#' in rule '%s' is escaped with '\\#'", name)
                        self.error = True

            if not self.funcsym[state]:
                if not self.strsym[state]:
                    self.log.error("No rules defined for state '%s'", state)
                    self.error = True
            efunc = self.errorf.get(state, None)
            if efunc:
                f = efunc
                line = f.__code__.co_firstlineno
                file = f.__code__.co_filename
                module = inspect.getmodule(f)
                self.modules.add(module)
                if isinstance(f, types.MethodType):
                    reqargs = 2
                else:
                    reqargs = 1
                nargs = f.__code__.co_argcount
                if nargs > reqargs:
                    self.log.error("%s:%d: Rule '%s' has too many arguments", file, line, f.__name__)
                    self.error = True
                if nargs < reqargs:
                    self.log.error("%s:%d: Rule '%s' requires an argument", file, line, f.__name__)
                    self.error = True
                else:
                    continue

        for module in self.modules:
            self.validate_module(module)

    def validate_module(self, module):
        try:
            lines, linen = inspect.getsourcelines(module)
        except IOError:
            return

        fre = re.compile('\\s*def\\s+(t_[a-zA-Z_0-9]*)\\(')
        sre = re.compile('\\s*(t_[a-zA-Z_0-9]*)\\s*=')
        counthash = {}
        linen += 1
        for line in lines:
            m = fre.match(line)
            if not m:
                m = sre.match(line)
            if m:
                name = m.group(1)
                prev = counthash.get(name)
                if not prev:
                    counthash[name] = linen
                else:
                    filename = inspect.getsourcefile(module)
                    self.log.error('%s:%d: Rule %s redefined. Previously defined on line %d', filename, linen, name, prev)
                self.error = True
            linen += 1


def lex(module=None, object=None, debug=False, optimize=False, lextab='lextab', reflags=int(re.VERBOSE), nowarn=False, outputdir=None, debuglog=None, errorlog=None):
    global input
    global lexer
    global token
    if lextab is None:
        lextab = 'lextab'
    ldict = None
    stateinfo = {'INITIAL': 'inclusive'}
    lexobj = Lexer()
    lexobj.lexoptimize = optimize
    if errorlog is None:
        errorlog = PlyLogger(sys.stderr)
    if debug:
        if debuglog is None:
            debuglog = PlyLogger(sys.stderr)
        if object:
            module = object
        if module:
            _items = [(k, getattr(module, k)) for k in dir(module)]
            ldict = dict(_items)
            if '__file__' not in ldict:
                ldict['__file__'] = sys.modules[ldict['__module__']].__file__
        else:
            ldict = get_caller_module_dict(2)
        pkg = ldict.get('__package__')
        if pkg:
            if isinstance(lextab, str):
                if '.' not in lextab:
                    lextab = pkg + '.' + lextab
            linfo = LexerReflect(ldict, log=errorlog, reflags=reflags)
            linfo.get_all()
            if not optimize:
                if linfo.validate_all():
                    raise SyntaxError("Can't build lexer")
                if optimize:
                    if lextab:
                        try:
                            lexobj.readtab(lextab, ldict)
                            token = lexobj.token
                            input = lexobj.input
                            lexer = lexobj
                            return lexobj
                        except ImportError:
                            pass

                if debug:
                    debuglog.info('lex: tokens   = %r', linfo.tokens)
                    debuglog.info('lex: literals = %r', linfo.literals)
                    debuglog.info('lex: states   = %r', linfo.stateinfo)
                lexobj.lextokens = set()
                for n in linfo.tokens:
                    lexobj.lextokens.add(n)

                if isinstance(linfo.literals, (list, tuple)):
                    lexobj.lexliterals = type(linfo.literals[0])().join(linfo.literals)
    else:
        lexobj.lexliterals = linfo.literals
    lexobj.lextokens_all = lexobj.lextokens | set(lexobj.lexliterals)
    stateinfo = linfo.stateinfo
    regexs = {}
    for state in stateinfo:
        regex_list = []
        for fname, f in linfo.funcsym[state]:
            line = f.__code__.co_firstlineno
            file = f.__code__.co_filename
            regex_list.append('(?P<%s>%s)' % (fname, _get_regex(f)))
            if debug:
                debuglog.info("lex: Adding rule %s -> '%s' (state '%s')", fname, _get_regex(f), state)
                continue

        for name, r in linfo.strsym[state]:
            regex_list.append('(?P<%s>%s)' % (name, r))
            if debug:
                debuglog.info("lex: Adding rule %s -> '%s' (state '%s')", name, r, state)
                continue

        regexs[state] = regex_list

    if debug:
        debuglog.info('lex: ==== MASTER REGEXS FOLLOW ====')
    for state in regexs:
        lexre, re_text, re_names = _form_master_re(regexs[state], reflags, ldict, linfo.toknames)
        lexobj.lexstatere[state] = lexre
        lexobj.lexstateretext[state] = re_text
        lexobj.lexstaterenames[state] = re_names
        if debug:
            for i, text in enumerate(re_text):
                debuglog.info("lex: state '%s' : regex[%d] = '%s'", state, i, text)

            continue

    for state, stype in stateinfo.items():
        if state != 'INITIAL' and stype == 'inclusive':
            lexobj.lexstatere[state].extend(lexobj.lexstatere['INITIAL'])
            lexobj.lexstateretext[state].extend(lexobj.lexstateretext['INITIAL'])
            lexobj.lexstaterenames[state].extend(lexobj.lexstaterenames['INITIAL'])
            continue

    lexobj.lexstateinfo = stateinfo
    lexobj.lexre = lexobj.lexstatere['INITIAL']
    lexobj.lexretext = lexobj.lexstateretext['INITIAL']
    lexobj.lexreflags = reflags
    lexobj.lexstateignore = linfo.ignore
    lexobj.lexignore = lexobj.lexstateignore.get('INITIAL', '')
    lexobj.lexstateerrorf = linfo.errorf
    lexobj.lexerrorf = linfo.errorf.get('INITIAL', None)
    if not lexobj.lexerrorf:
        errorlog.warning('No t_error rule is defined')
    lexobj.lexstateeoff = linfo.eoff
    lexobj.lexeoff = linfo.eoff.get('INITIAL', None)
    for s, stype in stateinfo.items():
        if stype == 'exclusive':
            if s not in linfo.errorf:
                errorlog.warning("No error rule is defined for exclusive state '%s'", s)
            if s not in linfo.ignore:
                if lexobj.lexignore:
                    errorlog.warning("No ignore rule is defined for exclusive state '%s'", s)
        elif stype == 'inclusive':
            if s not in linfo.errorf:
                linfo.errorf[s] = linfo.errorf.get('INITIAL', None)
            if s not in linfo.ignore:
                linfo.ignore[s] = linfo.ignore.get('INITIAL', '')
            else:
                continue

    token = lexobj.token
    input = lexobj.input
    lexer = lexobj
    if lextab:
        if optimize:
            if outputdir is None:
                if isinstance(lextab, types.ModuleType):
                    srcfile = lextab.__file__
                else:
                    if '.' not in lextab:
                        srcfile = ldict['__file__']
                    else:
                        parts = lextab.split('.')
                        pkgname = '.'.join(parts[:-1])
                        exec('import %s' % pkgname)
                        srcfile = getattr(sys.modules[pkgname], '__file__', '')
                outputdir = os.path.dirname(srcfile)
            try:
                lexobj.writetab(lextab, outputdir)
            except IOError as e:
                errorlog.warning("Couldn't write lextab module %r. %s" % (lextab, e))

    return lexobj


def runmain(lexer=None, data=None):
    if not data:
        try:
            filename = sys.argv[1]
            f = open(filename)
            data = f.read()
            f.close()
        except IndexError:
            sys.stdout.write('Reading from standard input (type EOF to end):\n')
            data = sys.stdin.read()

    if lexer:
        _input = lexer.input
    else:
        _input = input
    _input(data)
    if lexer:
        _token = lexer.token
    else:
        _token = token
    while True:
        tok = _token()
        if not tok:
            break
        sys.stdout.write('(%s,%r,%d,%d)\n' % (tok.type, tok.value, tok.lineno, tok.lexpos))


def TOKEN(r):

    def set_regex(f):
        if hasattr(r, '__call__'):
            f.regex = _get_regex(r)
        else:
            f.regex = r
        return f

    return set_regex


Token = TOKEN