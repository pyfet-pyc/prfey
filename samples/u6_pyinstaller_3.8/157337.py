# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
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
else:
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
                        if f:
                            f[0] or newfindex.append(f)
                        else:
                            newfindex.append((getattr(object, f[0].__name__), f[1]))
                    else:
                        newre.append((cre, newfindex))
                        newtab[key] = newre

                else:
                    c.lexstatere = newtab
                    c.lexstateerrorf = {}
                    for key, ef in self.lexstateerrorf.items():
                        c.lexstateerrorf[key] = getattr(object, ef.__name__)
                    else:
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
                    else:
                        tabre[statename] = titem

                else:
                    tf.write('_lexstatere   = %s\n' % repr(tabre))
                    tf.write('_lexstateignore = %s\n' % repr(self.lexstateignore))
                    taberr = {}
                    for statename, ef in self.lexstateerrorf.items():
                        taberr[statename] = ef.__name__ if ef else None
                    else:
                        tf.write('_lexstateerrorf = %s\n' % repr(taberr))
                        tabeof = {}
                        for statename, ef in self.lexstateeoff.items():
                            tabeof[statename] = ef.__name__ if ef else None
                        else:
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
                else:
                    self.lexstatere[statename] = titem
                    self.lexstateretext[statename] = txtitem

            else:
                self.lexstateerrorf = {}
                for statename, ef in lextab._lexstateerrorf.items():
                    self.lexstateerrorf[statename] = fdict[ef]
                else:
                    self.lexstateeoff = {}
                    for statename, ef in lextab._lexstateeoff.items():
                        self.lexstateeoff[statename] = fdict[ef]
                    else:
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
                2  LOAD_ATTR                lexpos
                4  STORE_FAST               'lexpos'

 L. 308         6  LOAD_FAST                'self'
                8  LOAD_ATTR                lexlen
               10  STORE_FAST               'lexlen'

 L. 309        12  LOAD_FAST                'self'
               14  LOAD_ATTR                lexignore
               16  STORE_FAST               'lexignore'

 L. 310        18  LOAD_FAST                'self'
               20  LOAD_ATTR                lexdata
               22  STORE_FAST               'lexdata'

 L. 312        24  LOAD_FAST                'lexpos'
               26  LOAD_FAST                'lexlen'
               28  COMPARE_OP               <
            30_32  POP_JUMP_IF_FALSE   538  'to 538'

 L. 314        34  LOAD_FAST                'lexdata'
               36  LOAD_FAST                'lexpos'
               38  BINARY_SUBSCR    
               40  LOAD_FAST                'lexignore'
               42  COMPARE_OP               in
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L. 315        46  LOAD_FAST                'lexpos'
               48  LOAD_CONST               1
               50  INPLACE_ADD      
               52  STORE_FAST               'lexpos'

 L. 316        54  JUMP_BACK            24  'to 24'
             56_0  COME_FROM            44  '44'

 L. 319        56  LOAD_FAST                'self'
               58  LOAD_ATTR                lexre
               60  GET_ITER         
               62  FOR_ITER            304  'to 304'
               64  UNPACK_SEQUENCE_2     2 
               66  STORE_FAST               'lexre'
               68  STORE_FAST               'lexindexfunc'

 L. 320        70  LOAD_FAST                'lexre'
               72  LOAD_METHOD              match
               74  LOAD_FAST                'lexdata'
               76  LOAD_FAST                'lexpos'
               78  CALL_METHOD_2         2  ''
               80  STORE_FAST               'm'

 L. 321        82  LOAD_FAST                'm'
               84  POP_JUMP_IF_TRUE     88  'to 88'

 L. 322        86  JUMP_BACK            62  'to 62'
             88_0  COME_FROM            84  '84'

 L. 325        88  LOAD_GLOBAL              LexToken
               90  CALL_FUNCTION_0       0  ''
               92  STORE_FAST               'tok'

 L. 326        94  LOAD_FAST                'm'
               96  LOAD_METHOD              group
               98  CALL_METHOD_0         0  ''
              100  LOAD_FAST                'tok'
              102  STORE_ATTR               value

 L. 327       104  LOAD_FAST                'self'
              106  LOAD_ATTR                lineno
              108  LOAD_FAST                'tok'
              110  STORE_ATTR               lineno

 L. 328       112  LOAD_FAST                'lexpos'
              114  LOAD_FAST                'tok'
              116  STORE_ATTR               lexpos

 L. 330       118  LOAD_FAST                'm'
              120  LOAD_ATTR                lastindex
              122  STORE_FAST               'i'

 L. 331       124  LOAD_FAST                'lexindexfunc'
              126  LOAD_FAST                'i'
              128  BINARY_SUBSCR    
              130  UNPACK_SEQUENCE_2     2 
              132  STORE_FAST               'func'
              134  LOAD_FAST                'tok'
              136  STORE_ATTR               type

 L. 333       138  LOAD_FAST                'func'
              140  POP_JUMP_IF_TRUE    178  'to 178'

 L. 335       142  LOAD_FAST                'tok'
              144  LOAD_ATTR                type
              146  POP_JUMP_IF_FALSE   166  'to 166'

 L. 336       148  LOAD_FAST                'm'
              150  LOAD_METHOD              end
              152  CALL_METHOD_0         0  ''
              154  LOAD_FAST                'self'
              156  STORE_ATTR               lexpos

 L. 337       158  LOAD_FAST                'tok'
              160  ROT_TWO          
              162  POP_TOP          
              164  RETURN_VALUE     
            166_0  COME_FROM           146  '146'

 L. 339       166  LOAD_FAST                'm'
              168  LOAD_METHOD              end
              170  CALL_METHOD_0         0  ''
              172  STORE_FAST               'lexpos'

 L. 340       174  POP_TOP          
              176  JUMP_BACK            24  'to 24'
            178_0  COME_FROM           140  '140'

 L. 342       178  LOAD_FAST                'm'
              180  LOAD_METHOD              end
              182  CALL_METHOD_0         0  ''
              184  STORE_FAST               'lexpos'

 L. 346       186  LOAD_FAST                'self'
              188  LOAD_FAST                'tok'
              190  STORE_ATTR               lexer

 L. 347       192  LOAD_FAST                'm'
              194  LOAD_FAST                'self'
              196  STORE_ATTR               lexmatch

 L. 348       198  LOAD_FAST                'lexpos'
              200  LOAD_FAST                'self'
              202  STORE_ATTR               lexpos

 L. 350       204  LOAD_FAST                'func'
              206  LOAD_FAST                'tok'
              208  CALL_FUNCTION_1       1  ''
              210  STORE_FAST               'newtok'

 L. 353       212  LOAD_FAST                'newtok'
              214  POP_JUMP_IF_TRUE    232  'to 232'

 L. 354       216  LOAD_FAST                'self'
              218  LOAD_ATTR                lexpos
              220  STORE_FAST               'lexpos'

 L. 355       222  LOAD_FAST                'self'
              224  LOAD_ATTR                lexignore
              226  STORE_FAST               'lexignore'

 L. 356       228  POP_TOP          
              230  JUMP_BACK            24  'to 24'
            232_0  COME_FROM           214  '214'

 L. 359       232  LOAD_FAST                'self'
              234  LOAD_ATTR                lexoptimize
          236_238  POP_JUMP_IF_TRUE    296  'to 296'

 L. 360       240  LOAD_FAST                'newtok'
              242  LOAD_ATTR                type
              244  LOAD_FAST                'self'
              246  LOAD_ATTR                lextokens_all
              248  COMPARE_OP               not-in
          250_252  POP_JUMP_IF_FALSE   296  'to 296'

 L. 361       254  LOAD_GLOBAL              LexError
              256  LOAD_STR                 "%s:%d: Rule '%s' returned an unknown token type '%s'"

 L. 362       258  LOAD_FAST                'func'
              260  LOAD_ATTR                __code__
              262  LOAD_ATTR                co_filename

 L. 362       264  LOAD_FAST                'func'
              266  LOAD_ATTR                __code__
              268  LOAD_ATTR                co_firstlineno

 L. 363       270  LOAD_FAST                'func'
              272  LOAD_ATTR                __name__

 L. 363       274  LOAD_FAST                'newtok'
              276  LOAD_ATTR                type

 L. 361       278  BUILD_TUPLE_4         4 
              280  BINARY_MODULO    

 L. 363       282  LOAD_FAST                'lexdata'
              284  LOAD_FAST                'lexpos'
              286  LOAD_CONST               None
              288  BUILD_SLICE_2         2 
              290  BINARY_SUBSCR    

 L. 361       292  CALL_FUNCTION_2       2  ''
              294  RAISE_VARARGS_1       1  'exception instance'
            296_0  COME_FROM           250  '250'
            296_1  COME_FROM           236  '236'

 L. 365       296  LOAD_FAST                'newtok'
              298  ROT_TWO          
              300  POP_TOP          
              302  RETURN_VALUE     

 L. 368       304  LOAD_FAST                'lexdata'
              306  LOAD_FAST                'lexpos'
              308  BINARY_SUBSCR    
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                lexliterals
              314  COMPARE_OP               in
          316_318  POP_JUMP_IF_FALSE   372  'to 372'

 L. 369       320  LOAD_GLOBAL              LexToken
              322  CALL_FUNCTION_0       0  ''
              324  STORE_FAST               'tok'

 L. 370       326  LOAD_FAST                'lexdata'
              328  LOAD_FAST                'lexpos'
              330  BINARY_SUBSCR    
              332  LOAD_FAST                'tok'
              334  STORE_ATTR               value

 L. 371       336  LOAD_FAST                'self'
              338  LOAD_ATTR                lineno
              340  LOAD_FAST                'tok'
              342  STORE_ATTR               lineno

 L. 372       344  LOAD_FAST                'tok'
              346  LOAD_ATTR                value
              348  LOAD_FAST                'tok'
              350  STORE_ATTR               type

 L. 373       352  LOAD_FAST                'lexpos'
              354  LOAD_FAST                'tok'
              356  STORE_ATTR               lexpos

 L. 374       358  LOAD_FAST                'lexpos'
              360  LOAD_CONST               1
              362  BINARY_ADD       
              364  LOAD_FAST                'self'
              366  STORE_ATTR               lexpos

 L. 375       368  LOAD_FAST                'tok'
              370  RETURN_VALUE     
            372_0  COME_FROM           316  '316'

 L. 378       372  LOAD_FAST                'self'
              374  LOAD_ATTR                lexerrorf
          376_378  POP_JUMP_IF_FALSE   500  'to 500'

 L. 379       380  LOAD_GLOBAL              LexToken
              382  CALL_FUNCTION_0       0  ''
              384  STORE_FAST               'tok'

 L. 380       386  LOAD_FAST                'self'
              388  LOAD_ATTR                lexdata
              390  LOAD_FAST                'lexpos'
              392  LOAD_CONST               None
              394  BUILD_SLICE_2         2 
              396  BINARY_SUBSCR    
              398  LOAD_FAST                'tok'
              400  STORE_ATTR               value

 L. 381       402  LOAD_FAST                'self'
              404  LOAD_ATTR                lineno
              406  LOAD_FAST                'tok'
              408  STORE_ATTR               lineno

 L. 382       410  LOAD_STR                 'error'
              412  LOAD_FAST                'tok'
              414  STORE_ATTR               type

 L. 383       416  LOAD_FAST                'self'
              418  LOAD_FAST                'tok'
              420  STORE_ATTR               lexer

 L. 384       422  LOAD_FAST                'lexpos'
              424  LOAD_FAST                'tok'
              426  STORE_ATTR               lexpos

 L. 385       428  LOAD_FAST                'lexpos'
              430  LOAD_FAST                'self'
              432  STORE_ATTR               lexpos

 L. 386       434  LOAD_FAST                'self'
              436  LOAD_METHOD              lexerrorf
              438  LOAD_FAST                'tok'
              440  CALL_METHOD_1         1  ''
              442  STORE_FAST               'newtok'

 L. 387       444  LOAD_FAST                'lexpos'
              446  LOAD_FAST                'self'
              448  LOAD_ATTR                lexpos
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_FALSE   482  'to 482'

 L. 389       456  LOAD_GLOBAL              LexError
              458  LOAD_STR                 "Scanning error. Illegal character '%s'"
              460  LOAD_FAST                'lexdata'
              462  LOAD_FAST                'lexpos'
              464  BINARY_SUBSCR    
              466  BINARY_MODULO    
              468  LOAD_FAST                'lexdata'
              470  LOAD_FAST                'lexpos'
              472  LOAD_CONST               None
              474  BUILD_SLICE_2         2 
              476  BINARY_SUBSCR    
              478  CALL_FUNCTION_2       2  ''
              480  RAISE_VARARGS_1       1  'exception instance'
            482_0  COME_FROM           452  '452'

 L. 390       482  LOAD_FAST                'self'
              484  LOAD_ATTR                lexpos
              486  STORE_FAST               'lexpos'

 L. 391       488  LOAD_FAST                'newtok'
          490_492  POP_JUMP_IF_TRUE    496  'to 496'

 L. 392       494  JUMP_BACK            24  'to 24'
            496_0  COME_FROM           490  '490'

 L. 393       496  LOAD_FAST                'newtok'
              498  RETURN_VALUE     
            500_0  COME_FROM           376  '376'

 L. 395       500  LOAD_FAST                'lexpos'
              502  LOAD_FAST                'self'
              504  STORE_ATTR               lexpos

 L. 396       506  LOAD_GLOBAL              LexError
              508  LOAD_STR                 "Illegal character '%s' at index %d"
              510  LOAD_FAST                'lexdata'
              512  LOAD_FAST                'lexpos'
              514  BINARY_SUBSCR    
              516  LOAD_FAST                'lexpos'
              518  BUILD_TUPLE_2         2 
              520  BINARY_MODULO    
              522  LOAD_FAST                'lexdata'
              524  LOAD_FAST                'lexpos'
              526  LOAD_CONST               None
              528  BUILD_SLICE_2         2 
              530  BINARY_SUBSCR    
              532  CALL_FUNCTION_2       2  ''
              534  RAISE_VARARGS_1       1  'exception instance'
              536  JUMP_BACK            24  'to 24'
            538_0  COME_FROM            30  '30'

 L. 398       538  LOAD_FAST                'self'
              540  LOAD_ATTR                lexeoff
          542_544  POP_JUMP_IF_FALSE   604  'to 604'

 L. 399       546  LOAD_GLOBAL              LexToken
              548  CALL_FUNCTION_0       0  ''
              550  STORE_FAST               'tok'

 L. 400       552  LOAD_STR                 'eof'
              554  LOAD_FAST                'tok'
              556  STORE_ATTR               type

 L. 401       558  LOAD_STR                 ''
              560  LOAD_FAST                'tok'
              562  STORE_ATTR               value

 L. 402       564  LOAD_FAST                'self'
              566  LOAD_ATTR                lineno
              568  LOAD_FAST                'tok'
              570  STORE_ATTR               lineno

 L. 403       572  LOAD_FAST                'lexpos'
              574  LOAD_FAST                'tok'
              576  STORE_ATTR               lexpos

 L. 404       578  LOAD_FAST                'self'
              580  LOAD_FAST                'tok'
              582  STORE_ATTR               lexer

 L. 405       584  LOAD_FAST                'lexpos'
              586  LOAD_FAST                'self'
              588  STORE_ATTR               lexpos

 L. 406       590  LOAD_FAST                'self'
              592  LOAD_METHOD              lexeoff
              594  LOAD_FAST                'tok'
              596  CALL_METHOD_1         1  ''
              598  STORE_FAST               'newtok'

 L. 407       600  LOAD_FAST                'newtok'
              602  RETURN_VALUE     
            604_0  COME_FROM           542  '542'

 L. 409       604  LOAD_FAST                'lexpos'
              606  LOAD_CONST               1
              608  BINARY_ADD       
              610  LOAD_FAST                'self'
              612  STORE_ATTR               lexpos

 L. 410       614  LOAD_FAST                'self'
              616  LOAD_ATTR                lexdata
              618  LOAD_CONST               None
              620  COMPARE_OP               is
          622_624  POP_JUMP_IF_FALSE   634  'to 634'

 L. 411       626  LOAD_GLOBAL              RuntimeError
              628  LOAD_STR                 'No input string given with input()'
              630  CALL_FUNCTION_1       1  ''
              632  RAISE_VARARGS_1       1  'exception instance'
            634_0  COME_FROM           622  '622'

Parse error at or near `JUMP_BACK' instruction at offset 176

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
        else:
            return result


    def _names_to_funcs(namelist, fdict):
        result = []
        for n in namelist:
            if n and n[0]:
                result.append((fdict[n[0]], n[1]))
            else:
                result.append(n)
        else:
            return result


    def _form_master_re--- This code section failed: ---

 L. 494         0  LOAD_FAST                'relist'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 495         4  BUILD_LIST_0          0 
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 496         8  LOAD_STR                 '|'
               10  LOAD_METHOD              join
               12  LOAD_FAST                'relist'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'regex'

 L. 497        18  SETUP_FINALLY       224  'to 224'

 L. 498        20  LOAD_GLOBAL              re
               22  LOAD_METHOD              compile
               24  LOAD_FAST                'regex'
               26  LOAD_FAST                'reflags'
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'lexre'

 L. 501        32  LOAD_CONST               None
               34  BUILD_LIST_1          1 
               36  LOAD_GLOBAL              max
               38  LOAD_FAST                'lexre'
               40  LOAD_ATTR                groupindex
               42  LOAD_METHOD              values
               44  CALL_METHOD_0         0  ''
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_CONST               1
               50  BINARY_ADD       
               52  BINARY_MULTIPLY  
               54  STORE_FAST               'lexindexfunc'

 L. 502        56  LOAD_FAST                'lexindexfunc'
               58  LOAD_CONST               None
               60  LOAD_CONST               None
               62  BUILD_SLICE_2         2 
               64  BINARY_SUBSCR    
               66  STORE_FAST               'lexindexnames'

 L. 504        68  LOAD_FAST                'lexre'
               70  LOAD_ATTR                groupindex
               72  LOAD_METHOD              items
               74  CALL_METHOD_0         0  ''
               76  GET_ITER         
             78_0  COME_FROM           150  '150'
               78  FOR_ITER            202  'to 202'
               80  UNPACK_SEQUENCE_2     2 
               82  STORE_FAST               'f'
               84  STORE_FAST               'i'

 L. 505        86  LOAD_FAST                'ldict'
               88  LOAD_METHOD              get
               90  LOAD_FAST                'f'
               92  LOAD_CONST               None
               94  CALL_METHOD_2         2  ''
               96  STORE_FAST               'handle'

 L. 506        98  LOAD_GLOBAL              type
              100  LOAD_FAST                'handle'
              102  CALL_FUNCTION_1       1  ''
              104  LOAD_GLOBAL              types
              106  LOAD_ATTR                FunctionType
              108  LOAD_GLOBAL              types
              110  LOAD_ATTR                MethodType
              112  BUILD_TUPLE_2         2 
              114  COMPARE_OP               in
              116  POP_JUMP_IF_FALSE   144  'to 144'

 L. 507       118  LOAD_FAST                'handle'
              120  LOAD_FAST                'toknames'
              122  LOAD_FAST                'f'
              124  BINARY_SUBSCR    
              126  BUILD_TUPLE_2         2 
              128  LOAD_FAST                'lexindexfunc'
              130  LOAD_FAST                'i'
              132  STORE_SUBSCR     

 L. 508       134  LOAD_FAST                'f'
              136  LOAD_FAST                'lexindexnames'
              138  LOAD_FAST                'i'
              140  STORE_SUBSCR     
              142  JUMP_BACK            78  'to 78'
            144_0  COME_FROM           116  '116'

 L. 509       144  LOAD_FAST                'handle'
              146  LOAD_CONST               None
              148  COMPARE_OP               is-not
              150  POP_JUMP_IF_FALSE    78  'to 78'

 L. 510       152  LOAD_FAST                'f'
              154  LOAD_FAST                'lexindexnames'
              156  LOAD_FAST                'i'
              158  STORE_SUBSCR     

 L. 511       160  LOAD_FAST                'f'
              162  LOAD_METHOD              find
              164  LOAD_STR                 'ignore_'
              166  CALL_METHOD_1         1  ''
              168  LOAD_CONST               0
              170  COMPARE_OP               >
              172  POP_JUMP_IF_FALSE   184  'to 184'

 L. 512       174  LOAD_CONST               (None, None)
              176  LOAD_FAST                'lexindexfunc'
              178  LOAD_FAST                'i'
              180  STORE_SUBSCR     
              182  JUMP_BACK            78  'to 78'
            184_0  COME_FROM           172  '172'

 L. 514       184  LOAD_CONST               None
              186  LOAD_FAST                'toknames'
              188  LOAD_FAST                'f'
              190  BINARY_SUBSCR    
              192  BUILD_TUPLE_2         2 
              194  LOAD_FAST                'lexindexfunc'
              196  LOAD_FAST                'i'
              198  STORE_SUBSCR     
              200  JUMP_BACK            78  'to 78'

 L. 516       202  LOAD_FAST                'lexre'
              204  LOAD_FAST                'lexindexfunc'
              206  BUILD_TUPLE_2         2 
              208  BUILD_LIST_1          1 
              210  LOAD_FAST                'regex'
              212  BUILD_LIST_1          1 
              214  LOAD_FAST                'lexindexnames'
              216  BUILD_LIST_1          1 
              218  BUILD_TUPLE_3         3 
              220  POP_BLOCK        
              222  RETURN_VALUE     
            224_0  COME_FROM_FINALLY    18  '18'

 L. 517       224  DUP_TOP          
              226  LOAD_GLOBAL              Exception
              228  COMPARE_OP               exception-match
          230_232  POP_JUMP_IF_FALSE   352  'to 352'
              234  POP_TOP          
              236  POP_TOP          
              238  POP_TOP          

 L. 518       240  LOAD_GLOBAL              int
              242  LOAD_GLOBAL              len
              244  LOAD_FAST                'relist'
              246  CALL_FUNCTION_1       1  ''
              248  LOAD_CONST               2
              250  BINARY_TRUE_DIVIDE
              252  CALL_FUNCTION_1       1  ''
              254  STORE_FAST               'm'

 L. 519       256  LOAD_FAST                'm'
              258  LOAD_CONST               0
              260  COMPARE_OP               ==
          262_264  POP_JUMP_IF_FALSE   270  'to 270'

 L. 520       266  LOAD_CONST               1
              268  STORE_FAST               'm'
            270_0  COME_FROM           262  '262'

 L. 521       270  LOAD_GLOBAL              _form_master_re
              272  LOAD_FAST                'relist'
              274  LOAD_CONST               None
              276  LOAD_FAST                'm'
              278  BUILD_SLICE_2         2 
              280  BINARY_SUBSCR    
              282  LOAD_FAST                'reflags'
              284  LOAD_FAST                'ldict'
              286  LOAD_FAST                'toknames'
              288  CALL_FUNCTION_4       4  ''
              290  UNPACK_SEQUENCE_3     3 
              292  STORE_FAST               'llist'
              294  STORE_FAST               'lre'
              296  STORE_FAST               'lnames'

 L. 522       298  LOAD_GLOBAL              _form_master_re
              300  LOAD_FAST                'relist'
              302  LOAD_FAST                'm'
              304  LOAD_CONST               None
              306  BUILD_SLICE_2         2 
              308  BINARY_SUBSCR    
              310  LOAD_FAST                'reflags'
              312  LOAD_FAST                'ldict'
              314  LOAD_FAST                'toknames'
              316  CALL_FUNCTION_4       4  ''
              318  UNPACK_SEQUENCE_3     3 
              320  STORE_FAST               'rlist'
              322  STORE_FAST               'rre'
              324  STORE_FAST               'rnames'

 L. 523       326  LOAD_FAST                'llist'
              328  LOAD_FAST                'rlist'
              330  BINARY_ADD       
              332  LOAD_FAST                'lre'
              334  LOAD_FAST                'rre'
              336  BINARY_ADD       
              338  LOAD_FAST                'lnames'
              340  LOAD_FAST                'rnames'
              342  BINARY_ADD       
              344  BUILD_TUPLE_3         3 
              346  ROT_FOUR         
              348  POP_EXCEPT       
              350  RETURN_VALUE     
            352_0  COME_FROM           230  '230'
              352  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 236


    def _statetoken(s, names):
        nonstate = 1
        parts = s.split('_')
        for i, part in enumerate(parts[1:], 1):
            if part not in names:
                if part != 'ANY':
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
            self.modules = set
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
                        else:
                            name, statetype = s
                            if not isinstance(name, StringTypes):
                                self.log.error('State name %s must be a string', repr(name))
                                self.error = True
                            elif not statetype == 'inclusive':
                                if not statetype == 'exclusive':
                                    self.log.error("State type for state %s must be 'inclusive' or 'exclusive'", name)
                                    self.error = True
                            elif name in self.stateinfo:
                                self.log.error("State '%s' already defined", name)
                                self.error = True
                            else:
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
            else:
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
                        elif tokname == 'error':
                            self.log.error("Rule '%s' must be defined as a function", f)
                            self.error = True
                        else:
                            for s in states:
                                self.strsym[s].append((f, t))

                    else:
                        self.log.error('%s not defined as a function or string', f)
                        self.error = True
                else:
                    for f in self.funcsym.values():
                        f.sort(key=(lambda x: x[1].__code__.co_firstlineno))
                    else:
                        for s in self.strsym.values():
                            s.sort(key=(lambda x: len(x[1])), reverse=True)

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
                    elif nargs < reqargs:
                        self.log.error("%s:%d: Rule '%s' requires an argument", file, line, f.__name__)
                        self.error = True
                    elif not _get_regex(f):
                        self.log.error("%s:%d: No regular expression defined for rule '%s'", file, line, f.__name__)
                        self.error = True
                else:
                    try:
                        c = re.compile('(?P<%s>%s)' % (fname, _get_regex(f)), self.reflags)
                        if c.match(''):
                            self.log.error("%s:%d: Regular expression for rule '%s' matches empty string", file, line, f.__name__)
                            self.error = True
                    except re.error as e:
                        try:
                            self.log.error("%s:%d: Invalid regular expression for rule '%s'. %s", file, line, f.__name__, e)
                            if '#' in _get_regex(f):
                                self.log.error("%s:%d. Make sure '#' in rule '%s' is escaped with '\\#'", file, line, f.__name__)
                            self.error = True
                        finally:
                            e = None
                            del e

            else:
                for name, r in self.strsym[state]:
                    tokname = self.toknames[name]
                    if tokname == 'error':
                        self.log.error("Rule '%s' must be defined as a function", name)
                        self.error = True
                    elif tokname not in self.tokens and tokname.find('ignore_') < 0:
                        self.log.error("Rule '%s' defined for an unspecified token %s", name, tokname)
                        self.error = True
                    else:
                        try:
                            c = re.compile('(?P<%s>%s)' % (name, r), self.reflags)
                            if c.match(''):
                                self.log.error("Regular expression for rule '%s' matches empty string", name)
                                self.error = True
                        except re.error as e:
                            try:
                                self.log.error("Invalid regular expression for rule '%s'. %s", name, e)
                                if '#' in r:
                                    self.log.error("Make sure '#' in rule '%s' is escaped with '\\#'", name)
                                self.error = True
                            finally:
                                e = None
                                del e

                else:
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
                            for module in self.modules:
                                self.validate_module(module)

        def validate_module(self, module):
            try:
                lines, linen = inspect.getsourcelines(module)
            except IOError:
                return
            else:
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


    def lex--- This code section failed: ---

 L. 866         0  LOAD_FAST                'lextab'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 867         8  LOAD_STR                 'lextab'
               10  STORE_FAST               'lextab'
             12_0  COME_FROM             6  '6'

 L. 871        12  LOAD_CONST               None
               14  STORE_FAST               'ldict'

 L. 872        16  LOAD_STR                 'INITIAL'
               18  LOAD_STR                 'inclusive'
               20  BUILD_MAP_1           1 
               22  STORE_FAST               'stateinfo'

 L. 873        24  LOAD_GLOBAL              Lexer
               26  CALL_FUNCTION_0       0  ''
               28  STORE_FAST               'lexobj'

 L. 874        30  LOAD_FAST                'optimize'
               32  LOAD_FAST                'lexobj'
               34  STORE_ATTR               lexoptimize

 L. 877        36  LOAD_FAST                'errorlog'
               38  LOAD_CONST               None
               40  COMPARE_OP               is
               42  POP_JUMP_IF_FALSE    54  'to 54'

 L. 878        44  LOAD_GLOBAL              PlyLogger
               46  LOAD_GLOBAL              sys
               48  LOAD_ATTR                stderr
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'errorlog'
             54_0  COME_FROM            42  '42'

 L. 880        54  LOAD_FAST                'debug'
               56  POP_JUMP_IF_FALSE    76  'to 76'

 L. 881        58  LOAD_FAST                'debuglog'
               60  LOAD_CONST               None
               62  COMPARE_OP               is
               64  POP_JUMP_IF_FALSE    76  'to 76'

 L. 882        66  LOAD_GLOBAL              PlyLogger
               68  LOAD_GLOBAL              sys
               70  LOAD_ATTR                stderr
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               'debuglog'
             76_0  COME_FROM            64  '64'
             76_1  COME_FROM            56  '56'

 L. 885        76  LOAD_FAST                'object'
               78  POP_JUMP_IF_FALSE    84  'to 84'

 L. 886        80  LOAD_FAST                'object'
               82  STORE_DEREF              'module'
             84_0  COME_FROM            78  '78'

 L. 889        84  LOAD_DEREF               'module'
               86  POP_JUMP_IF_FALSE   148  'to 148'

 L. 890        88  LOAD_CLOSURE             'module'
               90  BUILD_TUPLE_1         1 
               92  LOAD_LISTCOMP            '<code_object <listcomp>>'
               94  LOAD_STR                 'lex.<locals>.<listcomp>'
               96  MAKE_FUNCTION_8          'closure'
               98  LOAD_GLOBAL              dir
              100  LOAD_DEREF               'module'
              102  CALL_FUNCTION_1       1  ''
              104  GET_ITER         
              106  CALL_FUNCTION_1       1  ''
              108  STORE_FAST               '_items'

 L. 891       110  LOAD_GLOBAL              dict
              112  LOAD_FAST                '_items'
              114  CALL_FUNCTION_1       1  ''
              116  STORE_FAST               'ldict'

 L. 893       118  LOAD_STR                 '__file__'
              120  LOAD_FAST                'ldict'
              122  COMPARE_OP               not-in
              124  POP_JUMP_IF_FALSE   156  'to 156'

 L. 894       126  LOAD_GLOBAL              sys
              128  LOAD_ATTR                modules
              130  LOAD_FAST                'ldict'
              132  LOAD_STR                 '__module__'
              134  BINARY_SUBSCR    
              136  BINARY_SUBSCR    
              138  LOAD_ATTR                __file__
              140  LOAD_FAST                'ldict'
              142  LOAD_STR                 '__file__'
              144  STORE_SUBSCR     
              146  JUMP_FORWARD        156  'to 156'
            148_0  COME_FROM            86  '86'

 L. 896       148  LOAD_GLOBAL              get_caller_module_dict
              150  LOAD_CONST               2
              152  CALL_FUNCTION_1       1  ''
              154  STORE_FAST               'ldict'
            156_0  COME_FROM           146  '146'
            156_1  COME_FROM           124  '124'

 L. 900       156  LOAD_FAST                'ldict'
              158  LOAD_METHOD              get
              160  LOAD_STR                 '__package__'
              162  CALL_METHOD_1         1  ''
              164  STORE_FAST               'pkg'

 L. 901       166  LOAD_FAST                'pkg'
              168  POP_JUMP_IF_FALSE   200  'to 200'
              170  LOAD_GLOBAL              isinstance
              172  LOAD_FAST                'lextab'
              174  LOAD_GLOBAL              str
              176  CALL_FUNCTION_2       2  ''
              178  POP_JUMP_IF_FALSE   200  'to 200'

 L. 902       180  LOAD_STR                 '.'
              182  LOAD_FAST                'lextab'
              184  COMPARE_OP               not-in
              186  POP_JUMP_IF_FALSE   200  'to 200'

 L. 903       188  LOAD_FAST                'pkg'
              190  LOAD_STR                 '.'
              192  BINARY_ADD       
              194  LOAD_FAST                'lextab'
              196  BINARY_ADD       
              198  STORE_FAST               'lextab'
            200_0  COME_FROM           186  '186'
            200_1  COME_FROM           178  '178'
            200_2  COME_FROM           168  '168'

 L. 906       200  LOAD_GLOBAL              LexerReflect
              202  LOAD_FAST                'ldict'
              204  LOAD_FAST                'errorlog'
              206  LOAD_FAST                'reflags'
              208  LOAD_CONST               ('log', 'reflags')
              210  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              212  STORE_FAST               'linfo'

 L. 907       214  LOAD_FAST                'linfo'
              216  LOAD_METHOD              get_all
              218  CALL_METHOD_0         0  ''
              220  POP_TOP          

 L. 908       222  LOAD_FAST                'optimize'
              224  POP_JUMP_IF_TRUE    242  'to 242'

 L. 909       226  LOAD_FAST                'linfo'
              228  LOAD_METHOD              validate_all
              230  CALL_METHOD_0         0  ''
              232  POP_JUMP_IF_FALSE   242  'to 242'

 L. 910       234  LOAD_GLOBAL              SyntaxError
              236  LOAD_STR                 "Can't build lexer"
              238  CALL_FUNCTION_1       1  ''
              240  RAISE_VARARGS_1       1  'exception instance'
            242_0  COME_FROM           232  '232'
            242_1  COME_FROM           224  '224'

 L. 912       242  LOAD_FAST                'optimize'
          244_246  POP_JUMP_IF_FALSE   312  'to 312'
              248  LOAD_FAST                'lextab'
          250_252  POP_JUMP_IF_FALSE   312  'to 312'

 L. 913       254  SETUP_FINALLY       290  'to 290'

 L. 914       256  LOAD_FAST                'lexobj'
              258  LOAD_METHOD              readtab
              260  LOAD_FAST                'lextab'
              262  LOAD_FAST                'ldict'
              264  CALL_METHOD_2         2  ''
              266  POP_TOP          

 L. 915       268  LOAD_FAST                'lexobj'
              270  LOAD_ATTR                token
              272  STORE_GLOBAL             token

 L. 916       274  LOAD_FAST                'lexobj'
              276  LOAD_ATTR                input
              278  STORE_GLOBAL             input

 L. 917       280  LOAD_FAST                'lexobj'
              282  STORE_GLOBAL             lexer

 L. 918       284  LOAD_FAST                'lexobj'
              286  POP_BLOCK        
              288  RETURN_VALUE     
            290_0  COME_FROM_FINALLY   254  '254'

 L. 920       290  DUP_TOP          
              292  LOAD_GLOBAL              ImportError
              294  COMPARE_OP               exception-match
          296_298  POP_JUMP_IF_FALSE   310  'to 310'
              300  POP_TOP          
              302  POP_TOP          
              304  POP_TOP          

 L. 921       306  POP_EXCEPT       
              308  JUMP_FORWARD        312  'to 312'
            310_0  COME_FROM           296  '296'
              310  END_FINALLY      
            312_0  COME_FROM           308  '308'
            312_1  COME_FROM           250  '250'
            312_2  COME_FROM           244  '244'

 L. 924       312  LOAD_FAST                'debug'
          314_316  POP_JUMP_IF_FALSE   360  'to 360'

 L. 925       318  LOAD_FAST                'debuglog'
              320  LOAD_METHOD              info
              322  LOAD_STR                 'lex: tokens   = %r'
              324  LOAD_FAST                'linfo'
              326  LOAD_ATTR                tokens
              328  CALL_METHOD_2         2  ''
              330  POP_TOP          

 L. 926       332  LOAD_FAST                'debuglog'
              334  LOAD_METHOD              info
              336  LOAD_STR                 'lex: literals = %r'
              338  LOAD_FAST                'linfo'
              340  LOAD_ATTR                literals
              342  CALL_METHOD_2         2  ''
              344  POP_TOP          

 L. 927       346  LOAD_FAST                'debuglog'
              348  LOAD_METHOD              info
              350  LOAD_STR                 'lex: states   = %r'
              352  LOAD_FAST                'linfo'
              354  LOAD_ATTR                stateinfo
              356  CALL_METHOD_2         2  ''
              358  POP_TOP          
            360_0  COME_FROM           314  '314'

 L. 930       360  LOAD_GLOBAL              set
              362  CALL_FUNCTION_0       0  ''
              364  LOAD_FAST                'lexobj'
              366  STORE_ATTR               lextokens

 L. 931       368  LOAD_FAST                'linfo'
              370  LOAD_ATTR                tokens
              372  GET_ITER         
              374  FOR_ITER            394  'to 394'
              376  STORE_FAST               'n'

 L. 932       378  LOAD_FAST                'lexobj'
              380  LOAD_ATTR                lextokens
              382  LOAD_METHOD              add
              384  LOAD_FAST                'n'
              386  CALL_METHOD_1         1  ''
              388  POP_TOP          
          390_392  JUMP_BACK           374  'to 374'

 L. 935       394  LOAD_GLOBAL              isinstance
              396  LOAD_FAST                'linfo'
              398  LOAD_ATTR                literals
              400  LOAD_GLOBAL              list
              402  LOAD_GLOBAL              tuple
              404  BUILD_TUPLE_2         2 
              406  CALL_FUNCTION_2       2  ''
          408_410  POP_JUMP_IF_FALSE   440  'to 440'

 L. 936       412  LOAD_GLOBAL              type
              414  LOAD_FAST                'linfo'
              416  LOAD_ATTR                literals
              418  LOAD_CONST               0
              420  BINARY_SUBSCR    
              422  CALL_FUNCTION_1       1  ''
              424  CALL_FUNCTION_0       0  ''
              426  LOAD_METHOD              join
              428  LOAD_FAST                'linfo'
              430  LOAD_ATTR                literals
              432  CALL_METHOD_1         1  ''
              434  LOAD_FAST                'lexobj'
              436  STORE_ATTR               lexliterals
              438  JUMP_FORWARD        448  'to 448'
            440_0  COME_FROM           408  '408'

 L. 938       440  LOAD_FAST                'linfo'
              442  LOAD_ATTR                literals
              444  LOAD_FAST                'lexobj'
              446  STORE_ATTR               lexliterals
            448_0  COME_FROM           438  '438'

 L. 940       448  LOAD_FAST                'lexobj'
              450  LOAD_ATTR                lextokens
              452  LOAD_GLOBAL              set
              454  LOAD_FAST                'lexobj'
              456  LOAD_ATTR                lexliterals
              458  CALL_FUNCTION_1       1  ''
              460  BINARY_OR        
              462  LOAD_FAST                'lexobj'
              464  STORE_ATTR               lextokens_all

 L. 943       466  LOAD_FAST                'linfo'
              468  LOAD_ATTR                stateinfo
              470  STORE_FAST               'stateinfo'

 L. 945       472  BUILD_MAP_0           0 
              474  STORE_FAST               'regexs'

 L. 947       476  LOAD_FAST                'stateinfo'
              478  GET_ITER         
              480  FOR_ITER            648  'to 648'
              482  STORE_FAST               'state'

 L. 948       484  BUILD_LIST_0          0 
              486  STORE_FAST               'regex_list'

 L. 951       488  LOAD_FAST                'linfo'
              490  LOAD_ATTR                funcsym
              492  LOAD_FAST                'state'
              494  BINARY_SUBSCR    
              496  GET_ITER         
            498_0  COME_FROM           546  '546'
              498  FOR_ITER            574  'to 574'
              500  UNPACK_SEQUENCE_2     2 
              502  STORE_FAST               'fname'
              504  STORE_FAST               'f'

 L. 952       506  LOAD_FAST                'f'
              508  LOAD_ATTR                __code__
              510  LOAD_ATTR                co_firstlineno
              512  STORE_FAST               'line'

 L. 953       514  LOAD_FAST                'f'
              516  LOAD_ATTR                __code__
              518  LOAD_ATTR                co_filename
              520  STORE_FAST               'file'

 L. 954       522  LOAD_FAST                'regex_list'
              524  LOAD_METHOD              append
              526  LOAD_STR                 '(?P<%s>%s)'
              528  LOAD_FAST                'fname'
              530  LOAD_GLOBAL              _get_regex
              532  LOAD_FAST                'f'
              534  CALL_FUNCTION_1       1  ''
              536  BUILD_TUPLE_2         2 
              538  BINARY_MODULO    
              540  CALL_METHOD_1         1  ''
              542  POP_TOP          

 L. 955       544  LOAD_FAST                'debug'
          546_548  POP_JUMP_IF_FALSE   498  'to 498'

 L. 956       550  LOAD_FAST                'debuglog'
              552  LOAD_METHOD              info
              554  LOAD_STR                 "lex: Adding rule %s -> '%s' (state '%s')"
              556  LOAD_FAST                'fname'
              558  LOAD_GLOBAL              _get_regex
              560  LOAD_FAST                'f'
              562  CALL_FUNCTION_1       1  ''
              564  LOAD_FAST                'state'
              566  CALL_METHOD_4         4  ''
              568  POP_TOP          
          570_572  JUMP_BACK           498  'to 498'

 L. 959       574  LOAD_FAST                'linfo'
              576  LOAD_ATTR                strsym
              578  LOAD_FAST                'state'
              580  BINARY_SUBSCR    
              582  GET_ITER         
            584_0  COME_FROM           612  '612'
              584  FOR_ITER            636  'to 636'
              586  UNPACK_SEQUENCE_2     2 
              588  STORE_FAST               'name'
              590  STORE_FAST               'r'

 L. 960       592  LOAD_FAST                'regex_list'
              594  LOAD_METHOD              append
              596  LOAD_STR                 '(?P<%s>%s)'
              598  LOAD_FAST                'name'
              600  LOAD_FAST                'r'
              602  BUILD_TUPLE_2         2 
              604  BINARY_MODULO    
              606  CALL_METHOD_1         1  ''
              608  POP_TOP          

 L. 961       610  LOAD_FAST                'debug'
          612_614  POP_JUMP_IF_FALSE   584  'to 584'

 L. 962       616  LOAD_FAST                'debuglog'
              618  LOAD_METHOD              info
              620  LOAD_STR                 "lex: Adding rule %s -> '%s' (state '%s')"
              622  LOAD_FAST                'name'
              624  LOAD_FAST                'r'
              626  LOAD_FAST                'state'
              628  CALL_METHOD_4         4  ''
              630  POP_TOP          
          632_634  JUMP_BACK           584  'to 584'

 L. 964       636  LOAD_FAST                'regex_list'
              638  LOAD_FAST                'regexs'
              640  LOAD_FAST                'state'
              642  STORE_SUBSCR     
          644_646  JUMP_BACK           480  'to 480'

 L. 968       648  LOAD_FAST                'debug'
          650_652  POP_JUMP_IF_FALSE   664  'to 664'

 L. 969       654  LOAD_FAST                'debuglog'
              656  LOAD_METHOD              info
              658  LOAD_STR                 'lex: ==== MASTER REGEXS FOLLOW ===='
              660  CALL_METHOD_1         1  ''
              662  POP_TOP          
            664_0  COME_FROM           650  '650'

 L. 971       664  LOAD_FAST                'regexs'
              666  GET_ITER         
            668_0  COME_FROM           730  '730'
              668  FOR_ITER            774  'to 774'
              670  STORE_FAST               'state'

 L. 972       672  LOAD_GLOBAL              _form_master_re
              674  LOAD_FAST                'regexs'
              676  LOAD_FAST                'state'
              678  BINARY_SUBSCR    
              680  LOAD_FAST                'reflags'
              682  LOAD_FAST                'ldict'
              684  LOAD_FAST                'linfo'
              686  LOAD_ATTR                toknames
              688  CALL_FUNCTION_4       4  ''
              690  UNPACK_SEQUENCE_3     3 
              692  STORE_FAST               'lexre'
              694  STORE_FAST               're_text'
              696  STORE_FAST               're_names'

 L. 973       698  LOAD_FAST                'lexre'
              700  LOAD_FAST                'lexobj'
              702  LOAD_ATTR                lexstatere
              704  LOAD_FAST                'state'
              706  STORE_SUBSCR     

 L. 974       708  LOAD_FAST                're_text'
              710  LOAD_FAST                'lexobj'
              712  LOAD_ATTR                lexstateretext
              714  LOAD_FAST                'state'
              716  STORE_SUBSCR     

 L. 975       718  LOAD_FAST                're_names'
              720  LOAD_FAST                'lexobj'
              722  LOAD_ATTR                lexstaterenames
              724  LOAD_FAST                'state'
              726  STORE_SUBSCR     

 L. 976       728  LOAD_FAST                'debug'
          730_732  POP_JUMP_IF_FALSE   668  'to 668'

 L. 977       734  LOAD_GLOBAL              enumerate
              736  LOAD_FAST                're_text'
              738  CALL_FUNCTION_1       1  ''
              740  GET_ITER         
              742  FOR_ITER            770  'to 770'
              744  UNPACK_SEQUENCE_2     2 
              746  STORE_FAST               'i'
              748  STORE_FAST               'text'

 L. 978       750  LOAD_FAST                'debuglog'
              752  LOAD_METHOD              info
              754  LOAD_STR                 "lex: state '%s' : regex[%d] = '%s'"
              756  LOAD_FAST                'state'
              758  LOAD_FAST                'i'
              760  LOAD_FAST                'text'
              762  CALL_METHOD_4         4  ''
              764  POP_TOP          
          766_768  JUMP_BACK           742  'to 742'
          770_772  JUMP_BACK           668  'to 668'

 L. 981       774  LOAD_FAST                'stateinfo'
              776  LOAD_METHOD              items
              778  CALL_METHOD_0         0  ''
              780  GET_ITER         
            782_0  COME_FROM           806  '806'
            782_1  COME_FROM           796  '796'
              782  FOR_ITER            880  'to 880'
              784  UNPACK_SEQUENCE_2     2 
              786  STORE_FAST               'state'
              788  STORE_FAST               'stype'

 L. 982       790  LOAD_FAST                'state'
              792  LOAD_STR                 'INITIAL'
              794  COMPARE_OP               !=
          796_798  POP_JUMP_IF_FALSE   782  'to 782'
              800  LOAD_FAST                'stype'
              802  LOAD_STR                 'inclusive'
              804  COMPARE_OP               ==
          806_808  POP_JUMP_IF_FALSE   782  'to 782'

 L. 983       810  LOAD_FAST                'lexobj'
              812  LOAD_ATTR                lexstatere
              814  LOAD_FAST                'state'
              816  BINARY_SUBSCR    
              818  LOAD_METHOD              extend
              820  LOAD_FAST                'lexobj'
              822  LOAD_ATTR                lexstatere
              824  LOAD_STR                 'INITIAL'
              826  BINARY_SUBSCR    
              828  CALL_METHOD_1         1  ''
              830  POP_TOP          

 L. 984       832  LOAD_FAST                'lexobj'
              834  LOAD_ATTR                lexstateretext
              836  LOAD_FAST                'state'
              838  BINARY_SUBSCR    
              840  LOAD_METHOD              extend
              842  LOAD_FAST                'lexobj'
              844  LOAD_ATTR                lexstateretext
              846  LOAD_STR                 'INITIAL'
              848  BINARY_SUBSCR    
              850  CALL_METHOD_1         1  ''
              852  POP_TOP          

 L. 985       854  LOAD_FAST                'lexobj'
              856  LOAD_ATTR                lexstaterenames
              858  LOAD_FAST                'state'
              860  BINARY_SUBSCR    
              862  LOAD_METHOD              extend
              864  LOAD_FAST                'lexobj'
              866  LOAD_ATTR                lexstaterenames
              868  LOAD_STR                 'INITIAL'
              870  BINARY_SUBSCR    
              872  CALL_METHOD_1         1  ''
              874  POP_TOP          
          876_878  JUMP_BACK           782  'to 782'

 L. 987       880  LOAD_FAST                'stateinfo'
              882  LOAD_FAST                'lexobj'
              884  STORE_ATTR               lexstateinfo

 L. 988       886  LOAD_FAST                'lexobj'
              888  LOAD_ATTR                lexstatere
              890  LOAD_STR                 'INITIAL'
              892  BINARY_SUBSCR    
              894  LOAD_FAST                'lexobj'
              896  STORE_ATTR               lexre

 L. 989       898  LOAD_FAST                'lexobj'
              900  LOAD_ATTR                lexstateretext
              902  LOAD_STR                 'INITIAL'
              904  BINARY_SUBSCR    
              906  LOAD_FAST                'lexobj'
              908  STORE_ATTR               lexretext

 L. 990       910  LOAD_FAST                'reflags'
              912  LOAD_FAST                'lexobj'
              914  STORE_ATTR               lexreflags

 L. 993       916  LOAD_FAST                'linfo'
              918  LOAD_ATTR                ignore
              920  LOAD_FAST                'lexobj'
              922  STORE_ATTR               lexstateignore

 L. 994       924  LOAD_FAST                'lexobj'
              926  LOAD_ATTR                lexstateignore
              928  LOAD_METHOD              get
              930  LOAD_STR                 'INITIAL'
              932  LOAD_STR                 ''
              934  CALL_METHOD_2         2  ''
              936  LOAD_FAST                'lexobj'
              938  STORE_ATTR               lexignore

 L. 997       940  LOAD_FAST                'linfo'
              942  LOAD_ATTR                errorf
              944  LOAD_FAST                'lexobj'
              946  STORE_ATTR               lexstateerrorf

 L. 998       948  LOAD_FAST                'linfo'
              950  LOAD_ATTR                errorf
              952  LOAD_METHOD              get
              954  LOAD_STR                 'INITIAL'
              956  LOAD_CONST               None
              958  CALL_METHOD_2         2  ''
              960  LOAD_FAST                'lexobj'
              962  STORE_ATTR               lexerrorf

 L. 999       964  LOAD_FAST                'lexobj'
              966  LOAD_ATTR                lexerrorf
          968_970  POP_JUMP_IF_TRUE    982  'to 982'

 L.1000       972  LOAD_FAST                'errorlog'
              974  LOAD_METHOD              warning
              976  LOAD_STR                 'No t_error rule is defined'
              978  CALL_METHOD_1         1  ''
              980  POP_TOP          
            982_0  COME_FROM           968  '968'

 L.1003       982  LOAD_FAST                'linfo'
              984  LOAD_ATTR                eoff
              986  LOAD_FAST                'lexobj'
              988  STORE_ATTR               lexstateeoff

 L.1004       990  LOAD_FAST                'linfo'
              992  LOAD_ATTR                eoff
              994  LOAD_METHOD              get
              996  LOAD_STR                 'INITIAL'
              998  LOAD_CONST               None
             1000  CALL_METHOD_2         2  ''
             1002  LOAD_FAST                'lexobj'
             1004  STORE_ATTR               lexeoff

 L.1007      1006  LOAD_FAST                'stateinfo'
             1008  LOAD_METHOD              items
             1010  CALL_METHOD_0         0  ''
             1012  GET_ITER         
           1014_0  COME_FROM          1140  '1140'
           1014_1  COME_FROM          1096  '1096'
             1014  FOR_ITER           1168  'to 1168'
             1016  UNPACK_SEQUENCE_2     2 
             1018  STORE_FAST               's'
             1020  STORE_FAST               'stype'

 L.1008      1022  LOAD_FAST                'stype'
             1024  LOAD_STR                 'exclusive'
             1026  COMPARE_OP               ==
         1028_1030  POP_JUMP_IF_FALSE  1090  'to 1090'

 L.1009      1032  LOAD_FAST                's'
             1034  LOAD_FAST                'linfo'
             1036  LOAD_ATTR                errorf
             1038  COMPARE_OP               not-in
         1040_1042  POP_JUMP_IF_FALSE  1056  'to 1056'

 L.1010      1044  LOAD_FAST                'errorlog'
             1046  LOAD_METHOD              warning
             1048  LOAD_STR                 "No error rule is defined for exclusive state '%s'"
             1050  LOAD_FAST                's'
             1052  CALL_METHOD_2         2  ''
             1054  POP_TOP          
           1056_0  COME_FROM          1040  '1040'

 L.1011      1056  LOAD_FAST                's'
             1058  LOAD_FAST                'linfo'
             1060  LOAD_ATTR                ignore
             1062  COMPARE_OP               not-in
         1064_1066  POP_JUMP_IF_FALSE  1164  'to 1164'
             1068  LOAD_FAST                'lexobj'
             1070  LOAD_ATTR                lexignore
         1072_1074  POP_JUMP_IF_FALSE  1164  'to 1164'

 L.1012      1076  LOAD_FAST                'errorlog'
             1078  LOAD_METHOD              warning
             1080  LOAD_STR                 "No ignore rule is defined for exclusive state '%s'"
             1082  LOAD_FAST                's'
             1084  CALL_METHOD_2         2  ''
             1086  POP_TOP          
             1088  JUMP_BACK          1014  'to 1014'
           1090_0  COME_FROM          1028  '1028'

 L.1013      1090  LOAD_FAST                'stype'
             1092  LOAD_STR                 'inclusive'
             1094  COMPARE_OP               ==
         1096_1098  POP_JUMP_IF_FALSE  1014  'to 1014'

 L.1014      1100  LOAD_FAST                's'
             1102  LOAD_FAST                'linfo'
             1104  LOAD_ATTR                errorf
             1106  COMPARE_OP               not-in
         1108_1110  POP_JUMP_IF_FALSE  1132  'to 1132'

 L.1015      1112  LOAD_FAST                'linfo'
             1114  LOAD_ATTR                errorf
             1116  LOAD_METHOD              get
             1118  LOAD_STR                 'INITIAL'
             1120  LOAD_CONST               None
             1122  CALL_METHOD_2         2  ''
             1124  LOAD_FAST                'linfo'
             1126  LOAD_ATTR                errorf
             1128  LOAD_FAST                's'
             1130  STORE_SUBSCR     
           1132_0  COME_FROM          1108  '1108'

 L.1016      1132  LOAD_FAST                's'
             1134  LOAD_FAST                'linfo'
             1136  LOAD_ATTR                ignore
             1138  COMPARE_OP               not-in
         1140_1142  POP_JUMP_IF_FALSE  1014  'to 1014'

 L.1017      1144  LOAD_FAST                'linfo'
             1146  LOAD_ATTR                ignore
             1148  LOAD_METHOD              get
             1150  LOAD_STR                 'INITIAL'
             1152  LOAD_STR                 ''
             1154  CALL_METHOD_2         2  ''
             1156  LOAD_FAST                'linfo'
             1158  LOAD_ATTR                ignore
             1160  LOAD_FAST                's'
             1162  STORE_SUBSCR     
           1164_0  COME_FROM          1072  '1072'
           1164_1  COME_FROM          1064  '1064'
         1164_1166  JUMP_BACK          1014  'to 1014'

 L.1020      1168  LOAD_FAST                'lexobj'
             1170  LOAD_ATTR                token
             1172  STORE_GLOBAL             token

 L.1021      1174  LOAD_FAST                'lexobj'
             1176  LOAD_ATTR                input
             1178  STORE_GLOBAL             input

 L.1022      1180  LOAD_FAST                'lexobj'
             1182  STORE_GLOBAL             lexer

 L.1025      1184  LOAD_FAST                'lextab'
         1186_1188  POP_JUMP_IF_FALSE  1390  'to 1390'
             1190  LOAD_FAST                'optimize'
         1192_1194  POP_JUMP_IF_FALSE  1390  'to 1390'

 L.1026      1196  LOAD_FAST                'outputdir'
             1198  LOAD_CONST               None
             1200  COMPARE_OP               is
         1202_1204  POP_JUMP_IF_FALSE  1318  'to 1318'

 L.1031      1206  LOAD_GLOBAL              isinstance
             1208  LOAD_FAST                'lextab'
             1210  LOAD_GLOBAL              types
             1212  LOAD_ATTR                ModuleType
             1214  CALL_FUNCTION_2       2  ''
         1216_1218  POP_JUMP_IF_FALSE  1228  'to 1228'

 L.1032      1220  LOAD_FAST                'lextab'
             1222  LOAD_ATTR                __file__
             1224  STORE_FAST               'srcfile'
             1226  JUMP_FORWARD       1306  'to 1306'
           1228_0  COME_FROM          1216  '1216'

 L.1034      1228  LOAD_STR                 '.'
             1230  LOAD_FAST                'lextab'
             1232  COMPARE_OP               not-in
         1234_1236  POP_JUMP_IF_FALSE  1248  'to 1248'

 L.1035      1238  LOAD_FAST                'ldict'
             1240  LOAD_STR                 '__file__'
             1242  BINARY_SUBSCR    
             1244  STORE_FAST               'srcfile'
             1246  JUMP_FORWARD       1306  'to 1306'
           1248_0  COME_FROM          1234  '1234'

 L.1037      1248  LOAD_FAST                'lextab'
             1250  LOAD_METHOD              split
             1252  LOAD_STR                 '.'
             1254  CALL_METHOD_1         1  ''
             1256  STORE_FAST               'parts'

 L.1038      1258  LOAD_STR                 '.'
             1260  LOAD_METHOD              join
             1262  LOAD_FAST                'parts'
             1264  LOAD_CONST               None
             1266  LOAD_CONST               -1
             1268  BUILD_SLICE_2         2 
             1270  BINARY_SUBSCR    
             1272  CALL_METHOD_1         1  ''
             1274  STORE_FAST               'pkgname'

 L.1039      1276  LOAD_GLOBAL              exec
             1278  LOAD_STR                 'import %s'
             1280  LOAD_FAST                'pkgname'
             1282  BINARY_MODULO    
             1284  CALL_FUNCTION_1       1  ''
             1286  POP_TOP          

 L.1040      1288  LOAD_GLOBAL              getattr
             1290  LOAD_GLOBAL              sys
             1292  LOAD_ATTR                modules
             1294  LOAD_FAST                'pkgname'
             1296  BINARY_SUBSCR    
             1298  LOAD_STR                 '__file__'
             1300  LOAD_STR                 ''
             1302  CALL_FUNCTION_3       3  ''
             1304  STORE_FAST               'srcfile'
           1306_0  COME_FROM          1246  '1246'
           1306_1  COME_FROM          1226  '1226'

 L.1041      1306  LOAD_GLOBAL              os
             1308  LOAD_ATTR                path
             1310  LOAD_METHOD              dirname
             1312  LOAD_FAST                'srcfile'
             1314  CALL_METHOD_1         1  ''
             1316  STORE_FAST               'outputdir'
           1318_0  COME_FROM          1202  '1202'

 L.1042      1318  SETUP_FINALLY      1336  'to 1336'

 L.1043      1320  LOAD_FAST                'lexobj'
             1322  LOAD_METHOD              writetab
             1324  LOAD_FAST                'lextab'
             1326  LOAD_FAST                'outputdir'
             1328  CALL_METHOD_2         2  ''
             1330  POP_TOP          
             1332  POP_BLOCK        
             1334  JUMP_FORWARD       1390  'to 1390'
           1336_0  COME_FROM_FINALLY  1318  '1318'

 L.1044      1336  DUP_TOP          
             1338  LOAD_GLOBAL              IOError
             1340  COMPARE_OP               exception-match
         1342_1344  POP_JUMP_IF_FALSE  1388  'to 1388'
             1346  POP_TOP          
             1348  STORE_FAST               'e'
             1350  POP_TOP          
             1352  SETUP_FINALLY      1376  'to 1376'

 L.1045      1354  LOAD_FAST                'errorlog'
             1356  LOAD_METHOD              warning
             1358  LOAD_STR                 "Couldn't write lextab module %r. %s"
             1360  LOAD_FAST                'lextab'
             1362  LOAD_FAST                'e'
             1364  BUILD_TUPLE_2         2 
             1366  BINARY_MODULO    
             1368  CALL_METHOD_1         1  ''
             1370  POP_TOP          
             1372  POP_BLOCK        
             1374  BEGIN_FINALLY    
           1376_0  COME_FROM_FINALLY  1352  '1352'
             1376  LOAD_CONST               None
             1378  STORE_FAST               'e'
             1380  DELETE_FAST              'e'
             1382  END_FINALLY      
             1384  POP_EXCEPT       
             1386  JUMP_FORWARD       1390  'to 1390'
           1388_0  COME_FROM          1342  '1342'
             1388  END_FINALLY      
           1390_0  COME_FROM          1386  '1386'
           1390_1  COME_FROM          1334  '1334'
           1390_2  COME_FROM          1192  '1192'
           1390_3  COME_FROM          1186  '1186'

 L.1047      1390  LOAD_FAST                'lexobj'
             1392  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 302


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
            else:
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
                tok = _token
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