# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\f2py\auxfuncs.py
"""

Auxiliary functions for f2py2e.

Copyright 1999,2000 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>
Permission to use, modify, and distribute this software is given under the
terms of the NumPy (BSD style) LICENSE.

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Date: 2005/07/24 19:01:55 $
Pearu Peterson

"""
import pprint, sys, types
from functools import reduce
from . import __version__
from . import cfuncs
__all__ = [
 'applyrules', 'debugcapi', 'dictappend', 'errmess', 'gentitle',
 'getargs2', 'getcallprotoargument', 'getcallstatement',
 'getfortranname', 'getpymethoddef', 'getrestdoc', 'getusercode',
 'getusercode1', 'hasbody', 'hascallstatement', 'hascommon',
 'hasexternals', 'hasinitvalue', 'hasnote', 'hasresultnote',
 'isallocatable', 'isarray', 'isarrayofstrings', 'iscomplex',
 'iscomplexarray', 'iscomplexfunction', 'iscomplexfunction_warn',
 'isdouble', 'isdummyroutine', 'isexternal', 'isfunction',
 'isfunction_wrap', 'isint1array', 'isinteger', 'isintent_aux',
 'isintent_c', 'isintent_callback', 'isintent_copy', 'isintent_dict',
 'isintent_hide', 'isintent_in', 'isintent_inout', 'isintent_inplace',
 'isintent_nothide', 'isintent_out', 'isintent_overwrite', 'islogical',
 'islogicalfunction', 'islong_complex', 'islong_double',
 'islong_doublefunction', 'islong_long', 'islong_longfunction',
 'ismodule', 'ismoduleroutine', 'isoptional', 'isprivate', 'isrequired',
 'isroutine', 'isscalar', 'issigned_long_longarray', 'isstring',
 'isstringarray', 'isstringfunction', 'issubroutine',
 'issubroutine_wrap', 'isthreadsafe', 'isunsigned', 'isunsigned_char',
 'isunsigned_chararray', 'isunsigned_long_long',
 'isunsigned_long_longarray', 'isunsigned_short',
 'isunsigned_shortarray', 'l_and', 'l_not', 'l_or', 'outmess',
 'replace', 'show', 'stripcomma', 'throw_error']
f2py_version = __version__.version
errmess = sys.stderr.write
show = pprint.pprint
options = {}
debugoptions = []
wrapfuncs = 1

def outmess(t):
    if options.get('verbose', 1):
        sys.stdout.write(t)


def debugcapi(var):
    return 'capi' in debugoptions


def _isstring(var):
    return 'typespec' in var and var['typespec'] == 'character' and not isexternal(var)


def isstring(var):
    return _isstring(var) and not isarray(var)


def ischaracter(var):
    return isstring(var) and 'charselector' not in var


def isstringarray(var):
    return isarray(var) and _isstring(var)


def isarrayofstrings(var):
    return isstringarray(var) and var['dimension'][(-1)] == '(*)'


def isarray(var):
    return 'dimension' in var and not isexternal(var)


def isscalar(var):
    return not (isarray(var) or isstring(var) or isexternal(var))


def iscomplex(var):
    return isscalar(var) and var.get('typespec') in ('complex', 'double complex')


def islogical(var):
    return isscalar(var) and var.get('typespec') == 'logical'


def isinteger(var):
    return isscalar(var) and var.get('typespec') == 'integer'


def isreal(var):
    return isscalar(var) and var.get('typespec') == 'real'


def get_kind--- This code section failed: ---

 L. 120         0  SETUP_FINALLY        16  'to 16'

 L. 121         2  LOAD_FAST                'var'
                4  LOAD_STR                 'kindselector'
                6  BINARY_SUBSCR    
                8  LOAD_STR                 '*'
               10  BINARY_SUBSCR    
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 122        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    74  'to 74'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 123        30  SETUP_FINALLY        50  'to 50'

 L. 124        32  LOAD_FAST                'var'
               34  LOAD_STR                 'kindselector'
               36  BINARY_SUBSCR    
               38  LOAD_STR                 'kind'
               40  BINARY_SUBSCR    
               42  POP_BLOCK        
               44  ROT_FOUR         
               46  POP_EXCEPT       
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY    30  '30'

 L. 125        50  DUP_TOP          
               52  LOAD_GLOBAL              KeyError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    68  'to 68'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 126        64  POP_EXCEPT       
               66  JUMP_FORWARD         70  'to 70'
             68_0  COME_FROM            56  '56'
               68  END_FINALLY      
             70_0  COME_FROM            66  '66'
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
             74_0  COME_FROM            22  '22'
               74  END_FINALLY      
             76_0  COME_FROM            72  '72'

Parse error at or near `ROT_FOUR' instruction at offset 44


def islong_long(var):
    if not isscalar(var):
        return 0
    if var.get('typespec') not in ('integer', 'logical'):
        return 0
    return get_kind(var) == '8'


def isunsigned_char(var):
    if not isscalar(var):
        return 0
    if var.get('typespec') != 'integer':
        return 0
    return get_kind(var) == '-1'


def isunsigned_short(var):
    if not isscalar(var):
        return 0
    if var.get('typespec') != 'integer':
        return 0
    return get_kind(var) == '-2'


def isunsigned(var):
    if not isscalar(var):
        return 0
    if var.get('typespec') != 'integer':
        return 0
    return get_kind(var) == '-4'


def isunsigned_long_long(var):
    if not isscalar(var):
        return 0
    if var.get('typespec') != 'integer':
        return 0
    return get_kind(var) == '-8'


def isdouble(var):
    if not isscalar(var):
        return 0
    if not var.get('typespec') == 'real':
        return 0
    return get_kind(var) == '8'


def islong_double(var):
    if not isscalar(var):
        return 0
    if not var.get('typespec') == 'real':
        return 0
    return get_kind(var) == '16'


def islong_complex(var):
    if not iscomplex(var):
        return 0
    return get_kind(var) == '32'


def iscomplexarray(var):
    return isarray(var) and var.get('typespec') in ('complex', 'double complex')


def isint1array(var):
    return isarray(var) and var.get('typespec') == 'integer' and get_kind(var) == '1'


def isunsigned_chararray(var):
    return isarray(var) and var.get('typespec') in ('integer', 'logical') and get_kind(var) == '-1'


def isunsigned_shortarray(var):
    return isarray(var) and var.get('typespec') in ('integer', 'logical') and get_kind(var) == '-2'


def isunsignedarray(var):
    return isarray(var) and var.get('typespec') in ('integer', 'logical') and get_kind(var) == '-4'


def isunsigned_long_longarray(var):
    return isarray(var) and var.get('typespec') in ('integer', 'logical') and get_kind(var) == '-8'


def issigned_chararray(var):
    return isarray(var) and var.get('typespec') in ('integer', 'logical') and get_kind(var) == '1'


def issigned_shortarray(var):
    return isarray(var) and var.get('typespec') in ('integer', 'logical') and get_kind(var) == '2'


def issigned_array(var):
    return isarray(var) and var.get('typespec') in ('integer', 'logical') and get_kind(var) == '4'


def issigned_long_longarray(var):
    return isarray(var) and var.get('typespec') in ('integer', 'logical') and get_kind(var) == '8'


def isallocatable(var):
    return 'attrspec' in var and 'allocatable' in var['attrspec']


def ismutable(var):
    return not ('dimension' not in var or isstring(var))


def ismoduleroutine(rout):
    return 'modulename' in rout


def ismodule(rout):
    return 'block' in rout and 'module' == rout['block']


def isfunction(rout):
    return 'block' in rout and 'function' == rout['block']


def isfunction_wrap(rout):
    if isintent_c(rout):
        return 0
    return wrapfuncs and isfunction(rout) and not isexternal(rout)


def issubroutine(rout):
    return 'block' in rout and 'subroutine' == rout['block']


def issubroutine_wrap(rout):
    if isintent_c(rout):
        return 0
    return issubroutine(rout) and hasassumedshape(rout)


def hasassumedshape(rout):
    if rout.get('hasassumedshape'):
        return True
    for a in rout['args']:
        for d in rout['vars'].get(a, {}).get('dimension', []):
            if d == ':':
                rout['hasassumedshape'] = True
                return True
        else:
            return False


def requiresf90wrapper(rout):
    return ismoduleroutine(rout) or hasassumedshape(rout)


def isroutine(rout):
    return isfunction(rout) or issubroutine(rout)


def islogicalfunction(rout):
    if not isfunction(rout):
        return 0
    if 'result' in rout:
        a = rout['result']
    else:
        a = rout['name']
    if a in rout['vars']:
        return islogical(rout['vars'][a])
    return 0


def islong_longfunction(rout):
    if not isfunction(rout):
        return 0
    if 'result' in rout:
        a = rout['result']
    else:
        a = rout['name']
    if a in rout['vars']:
        return islong_long(rout['vars'][a])
    return 0


def islong_doublefunction(rout):
    if not isfunction(rout):
        return 0
    if 'result' in rout:
        a = rout['result']
    else:
        a = rout['name']
    if a in rout['vars']:
        return islong_double(rout['vars'][a])
    return 0


def iscomplexfunction(rout):
    if not isfunction(rout):
        return 0
    if 'result' in rout:
        a = rout['result']
    else:
        a = rout['name']
    if a in rout['vars']:
        return iscomplex(rout['vars'][a])
    return 0


def iscomplexfunction_warn(rout):
    if iscomplexfunction(rout):
        outmess('    **************************************************************\n        Warning: code with a function returning complex value\n        may not work correctly with your Fortran compiler.\n        Run the following test before using it in your applications:\n        $(f2py install dir)/test-site/{b/runme_scalar,e/runme}\n        When using GNU gcc/g77 compilers, codes should work correctly.\n    **************************************************************\n')
        return 1
    return 0


def isstringfunction(rout):
    if not isfunction(rout):
        return 0
    if 'result' in rout:
        a = rout['result']
    else:
        a = rout['name']
    if a in rout['vars']:
        return isstring(rout['vars'][a])
    return 0


def hasexternals(rout):
    return 'externals' in rout and rout['externals']


def isthreadsafe(rout):
    return 'f2pyenhancements' in rout and 'threadsafe' in rout['f2pyenhancements']


def hasvariables(rout):
    return 'vars' in rout and rout['vars']


def isoptional(var):
    return 'attrspec' in var and 'optional' in var['attrspec'] and 'required' not in var['attrspec'] and isintent_nothide(var)


def isexternal(var):
    return 'attrspec' in var and 'external' in var['attrspec']


def isrequired(var):
    return not isoptional(var) and isintent_nothide(var)


def isintent_in(var):
    if 'intent' not in var:
        return 1
    if 'hide' in var['intent']:
        return 0
    if 'inplace' in var['intent']:
        return 0
    if 'in' in var['intent']:
        return 1
    if 'out' in var['intent']:
        return 0
    if 'inout' in var['intent']:
        return 0
    if 'outin' in var['intent']:
        return 0
    return 1


def isintent_inout(var):
    if 'intent' in var and not 'inout' in var['intent']:
        return 'outin' in var['intent'] and 'in' not in var['intent'] and 'hide' not in var['intent'] and 'inplace' not in var['intent']


def isintent_out(var):
    return 'out' in var.get('intent', [])


def isintent_hide(var):
    return ('intent' in var and 'hide' in var['intent']) or (('out' in var['intent']) and ('in' not in var['intent'] and not l_or(isintent_inout, isintent_inplace)(var)))


def isintent_nothide(var):
    return not isintent_hide(var)


def isintent_c(var):
    return 'c' in var.get('intent', [])


def isintent_cache(var):
    return 'cache' in var.get('intent', [])


def isintent_copy(var):
    return 'copy' in var.get('intent', [])


def isintent_overwrite(var):
    return 'overwrite' in var.get('intent', [])


def isintent_callback(var):
    return 'callback' in var.get('intent', [])


def isintent_inplace(var):
    return 'inplace' in var.get('intent', [])


def isintent_aux(var):
    return 'aux' in var.get('intent', [])


def isintent_aligned4(var):
    return 'aligned4' in var.get('intent', [])


def isintent_aligned8(var):
    return 'aligned8' in var.get('intent', [])


def isintent_aligned16(var):
    return 'aligned16' in var.get('intent', [])


isintent_dict = {isintent_in: 'INTENT_IN', isintent_inout: 'INTENT_INOUT', 
 isintent_out: 'INTENT_OUT', isintent_hide: 'INTENT_HIDE', 
 isintent_cache: 'INTENT_CACHE', 
 isintent_c: 'INTENT_C', isoptional: 'OPTIONAL', 
 isintent_inplace: 'INTENT_INPLACE', 
 isintent_aligned4: 'INTENT_ALIGNED4', 
 isintent_aligned8: 'INTENT_ALIGNED8', 
 isintent_aligned16: 'INTENT_ALIGNED16'}

def isprivate(var):
    return 'attrspec' in var and 'private' in var['attrspec']


def hasinitvalue(var):
    return '=' in var


def hasinitvalueasstring(var):
    if not hasinitvalue(var):
        return 0
    return var['='][0] in ('"', "'")


def hasnote(var):
    return 'note' in var


def hasresultnote(rout):
    if not isfunction(rout):
        return 0
    if 'result' in rout:
        a = rout['result']
    else:
        a = rout['name']
    if a in rout['vars']:
        return hasnote(rout['vars'][a])
    return 0


def hascommon(rout):
    return 'common' in rout


def containscommon(rout):
    if hascommon(rout):
        return 1
    if hasbody(rout):
        for b in rout['body']:
            if containscommon(b):
                return 1

        return 0


def containsmodule(block):
    if ismodule(block):
        return 1
    if not hasbody(block):
        return 0
    for b in block['body']:
        if containsmodule(b):
            return 1
    else:
        return 0


def hasbody(rout):
    return 'body' in rout


def hascallstatement(rout):
    return getcallstatement(rout) is not None


def istrue(var):
    return 1


def isfalse(var):
    return 0


class F2PYError(Exception):
    pass


class throw_error:

    def __init__(self, mess):
        self.mess = mess

    def __call__(self, var):
        mess = '\n\n  var = %s\n  Message: %s\n' % (var, self.mess)
        raise F2PYError(mess)


def l_and(*f):
    l, l2 = 'lambda v', []
    for i in range(len(f)):
        l = '%s,f%d=f[%d]' % (l, i, i)
        l2.append('f%d(v)' % i)
    else:
        return eval('%s:%s' % (l, ' and '.join(l2)))


def l_or(*f):
    l, l2 = 'lambda v', []
    for i in range(len(f)):
        l = '%s,f%d=f[%d]' % (l, i, i)
        l2.append('f%d(v)' % i)
    else:
        return eval('%s:%s' % (l, ' or '.join(l2)))


def l_not(f):
    return eval('lambda v,f=f:not f(v)')


def isdummyroutine--- This code section failed: ---

 L. 589         0  SETUP_FINALLY        20  'to 20'

 L. 590         2  LOAD_FAST                'rout'
                4  LOAD_STR                 'f2pyenhancements'
                6  BINARY_SUBSCR    
                8  LOAD_STR                 'fortranname'
               10  BINARY_SUBSCR    
               12  LOAD_STR                 ''
               14  COMPARE_OP               ==
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 591        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    40  'to 40'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 592        34  POP_EXCEPT       
               36  LOAD_CONST               0
               38  RETURN_VALUE     
             40_0  COME_FROM            26  '26'
               40  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 36


def getfortranname(rout):
    try:
        name = rout['f2pyenhancements']['fortranname']
        if name == '':
            raise KeyError
        if not name:
            errmess('Failed to use fortranname from %s\n' % rout['f2pyenhancements'])
            raise KeyError
    except KeyError:
        name = rout['name']
    else:
        return name


def getmultilineblock(rout, blockname, comment=1, counter=0):
    try:
        r = rout['f2pyenhancements'].get(blockname)
    except KeyError:
        return
    else:
        if not r:
            return
        else:
            if counter > 0:
                if isinstance(r, str):
                    return
            if isinstance(r, list):
                if counter >= len(r):
                    return
                r = r[counter]
            if r[:3] == "'''":
                if comment:
                    r = '\t/* start ' + blockname + ' multiline (' + repr(counter) + ') */\n' + r[3:]
                else:
                    r = r[3:]
                if r[-3:] == "'''":
                    if comment:
                        r = r[:-3] + '\n\t/* end multiline (' + repr(counter) + ')*/'
                    else:
                        r = r[:-3]
                else:
                    errmess("%s multiline block should end with `'''`: %s\n" % (
                     blockname, repr(r)))
            return r


def getcallstatement(rout):
    return getmultilineblock(rout, 'callstatement')


def getcallprotoargument(rout, cb_map={}):
    r = getmultilineblock(rout, 'callprotoargument', comment=0)
    if r:
        return r
    if hascallstatement(rout):
        outmess('warning: callstatement is defined without callprotoargument\n')
        return
    from .capi_maps import getctype
    arg_types, arg_types2 = [], []
    if l_and(isstringfunction, l_not(isfunction_wrap))(rout):
        arg_types.extend(['char*', 'size_t'])
    for n in rout['args']:
        var = rout['vars'][n]
        if isintent_callback(var):
            pass
        else:
            if n in cb_map:
                ctype = cb_map[n] + '_typedef'
            else:
                ctype = getctype(var)
                if l_and(isintent_c, l_or(isscalar, iscomplex))(var):
                    pass
                elif isstring(var):
                    pass
                else:
                    ctype = ctype + '*'
                if isstring(var) or (isarrayofstrings(var)):
                    arg_types2.append('size_t')
            arg_types.append(ctype)
    else:
        proto_args = ','.join(arg_types + arg_types2)
        if not proto_args:
            proto_args = 'void'
        return proto_args


def getusercode(rout):
    return getmultilineblock(rout, 'usercode')


def getusercode1(rout):
    return getmultilineblock(rout, 'usercode', counter=1)


def getpymethoddef(rout):
    return getmultilineblock(rout, 'pymethoddef')


def getargs(rout):
    sortargs, args = [], []
    if 'args' in rout:
        args = rout['args']
        if 'sortvars' in rout:
            for a in rout['sortvars']:
                if a in args:
                    sortargs.append(a)
            else:
                for a in args:
                    if a not in sortargs:
                        sortargs.append(a)

        else:
            sortargs = rout['args']
    return (
     args, sortargs)


def getargs2(rout):
    sortargs, args = [], rout.get('args', [])
    auxvars = [a for a in rout['vars'].keys() if isintent_aux(rout['vars'][a]) if a not in args]
    args = auxvars + args
    if 'sortvars' in rout:
        for a in rout['sortvars']:
            if a in args:
                sortargs.append(a)
        else:
            for a in args:
                if a not in sortargs:
                    sortargs.append(a)

    else:
        sortargs = auxvars + rout['args']
    return (args, sortargs)


def getrestdoc(rout):
    if 'f2pymultilines' not in rout:
        return
    k = None
    if rout['block'] == 'python module':
        k = (
         rout['block'], rout['name'])
    return rout['f2pymultilines'].get(k, None)


def gentitle(name):
    l = (80 - len(name) - 6) // 2
    return '/*%s %s %s*/' % (l * '*', name, l * '*')


def flatlist(l):
    if isinstance(l, list):
        return reduce(lambda x, y, f=flatlist: x + f(y), l, [])
    return [l]


def stripcomma(s):
    if s:
        if s[(-1)] == ',':
            return s[:-1]
    return s


def replace(str, d, defaultsep=''):
    if isinstance(d, list):
        return [replace(str, _m, defaultsep) for _m in d]
    if isinstance(str, list):
        return [replace(_m, d, defaultsep) for _m in str]
    for k in 2 * list(d.keys()):
        if k == 'separatorsfor':
            pass
        else:
            if 'separatorsfor' in d and k in d['separatorsfor']:
                sep = d['separatorsfor'][k]
            else:
                sep = defaultsep
            if isinstance(d[k], list):
                str = str.replace('#%s#' % k, sep.join(flatlist(d[k])))
            else:
                str = str.replace('#%s#' % k, d[k])
    else:
        return str


def dictappend(rd, ar):
    if isinstance(ar, list):
        for a in ar:
            rd = dictappend(rd, a)
        else:
            return rd

    for k in ar.keys():
        if k[0] == '_':
            pass
        else:
            if k in rd:
                if isinstance(rd[k], str):
                    rd[k] = [
                     rd[k]]
                if isinstance(rd[k], list):
                    if isinstance(ar[k], list):
                        rd[k] = rd[k] + ar[k]
                    else:
                        rd[k].append(ar[k])
                else:
                    if isinstance(rd[k], dict) and isinstance(ar[k], dict):
                        if k == 'separatorsfor':
                            for k1 in ar[k].keys():
                                if k1 not in rd[k]:
                                    rd[k][k1] = ar[k][k1]

                        else:
                            rd[k] = dictappend(rd[k], ar[k])
                    else:
                        rd[k] = ar[k]
    else:
        return rd


def applyrules--- This code section failed: ---

 L. 799         0  BUILD_MAP_0           0 
                2  STORE_FAST               'ret'

 L. 800         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'rules'
                8  LOAD_GLOBAL              list
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    62  'to 62'

 L. 801        14  LOAD_FAST                'rules'
               16  GET_ITER         
             18_0  COME_FROM            56  '56'
             18_1  COME_FROM            50  '50'
               18  FOR_ITER             58  'to 58'
               20  STORE_FAST               'r'

 L. 802        22  LOAD_GLOBAL              applyrules
               24  LOAD_FAST                'r'
               26  LOAD_FAST                'd'
               28  LOAD_FAST                'var'
               30  CALL_FUNCTION_3       3  ''
               32  STORE_FAST               'rr'

 L. 803        34  LOAD_GLOBAL              dictappend
               36  LOAD_FAST                'ret'
               38  LOAD_FAST                'rr'
               40  CALL_FUNCTION_2       2  ''
               42  STORE_FAST               'ret'

 L. 804        44  LOAD_STR                 '_break'
               46  LOAD_FAST                'rr'
               48  COMPARE_OP               in
               50  POP_JUMP_IF_FALSE_BACK    18  'to 18'

 L. 805        52  POP_TOP          
               54  BREAK_LOOP           58  'to 58'
               56  JUMP_BACK            18  'to 18'
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            18  '18'

 L. 806        58  LOAD_FAST                'ret'
               60  RETURN_VALUE     
             62_0  COME_FROM            12  '12'

 L. 807        62  LOAD_STR                 '_check'
               64  LOAD_FAST                'rules'
               66  COMPARE_OP               in
               68  POP_JUMP_IF_FALSE    86  'to 86'
               70  LOAD_FAST                'rules'
               72  LOAD_STR                 '_check'
               74  BINARY_SUBSCR    
               76  LOAD_FAST                'var'
               78  CALL_FUNCTION_1       1  ''
               80  POP_JUMP_IF_TRUE     86  'to 86'

 L. 808        82  LOAD_FAST                'ret'
               84  RETURN_VALUE     
             86_0  COME_FROM            80  '80'
             86_1  COME_FROM            68  '68'

 L. 809        86  LOAD_STR                 'need'
               88  LOAD_FAST                'rules'
               90  COMPARE_OP               in
               92  POP_JUMP_IF_FALSE   136  'to 136'

 L. 810        94  LOAD_GLOBAL              applyrules
               96  LOAD_STR                 'needs'
               98  LOAD_FAST                'rules'
              100  LOAD_STR                 'need'
              102  BINARY_SUBSCR    
              104  BUILD_MAP_1           1 
              106  LOAD_FAST                'd'
              108  LOAD_FAST                'var'
              110  CALL_FUNCTION_3       3  ''
              112  STORE_FAST               'res'

 L. 811       114  LOAD_STR                 'needs'
              116  LOAD_FAST                'res'
              118  COMPARE_OP               in
              120  POP_JUMP_IF_FALSE   136  'to 136'

 L. 812       122  LOAD_GLOBAL              cfuncs
              124  LOAD_METHOD              append_needs
              126  LOAD_FAST                'res'
              128  LOAD_STR                 'needs'
              130  BINARY_SUBSCR    
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
            136_0  COME_FROM           120  '120'
            136_1  COME_FROM            92  '92'

 L. 814       136  LOAD_FAST                'rules'
              138  LOAD_METHOD              keys
              140  CALL_METHOD_0         0  ''
              142  GET_ITER         
            144_0  COME_FROM           664  '664'
            144_1  COME_FROM           656  '656'
            144_2  COME_FROM           610  '610'
            144_3  COME_FROM           306  '306'
            144_4  COME_FROM           170  '170'
          144_146  FOR_ITER            666  'to 666'
              148  STORE_FAST               'k'

 L. 815       150  LOAD_FAST                'k'
              152  LOAD_STR                 'separatorsfor'
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   172  'to 172'

 L. 816       158  LOAD_FAST                'rules'
              160  LOAD_FAST                'k'
              162  BINARY_SUBSCR    
              164  LOAD_FAST                'ret'
              166  LOAD_FAST                'k'
              168  STORE_SUBSCR     

 L. 817       170  JUMP_BACK           144  'to 144'
            172_0  COME_FROM           156  '156'

 L. 818       172  LOAD_GLOBAL              isinstance
              174  LOAD_FAST                'rules'
              176  LOAD_FAST                'k'
              178  BINARY_SUBSCR    
              180  LOAD_GLOBAL              str
              182  CALL_FUNCTION_2       2  ''
              184  POP_JUMP_IF_FALSE   208  'to 208'

 L. 819       186  LOAD_GLOBAL              replace
              188  LOAD_FAST                'rules'
              190  LOAD_FAST                'k'
              192  BINARY_SUBSCR    
              194  LOAD_FAST                'd'
              196  CALL_FUNCTION_2       2  ''
              198  LOAD_FAST                'ret'
              200  LOAD_FAST                'k'
              202  STORE_SUBSCR     
          204_206  JUMP_FORWARD        598  'to 598'
            208_0  COME_FROM           184  '184'

 L. 820       208  LOAD_GLOBAL              isinstance
              210  LOAD_FAST                'rules'
              212  LOAD_FAST                'k'
              214  BINARY_SUBSCR    
              216  LOAD_GLOBAL              list
              218  CALL_FUNCTION_2       2  ''
          220_222  POP_JUMP_IF_FALSE   292  'to 292'

 L. 821       224  BUILD_LIST_0          0 
              226  LOAD_FAST                'ret'
              228  LOAD_FAST                'k'
              230  STORE_SUBSCR     

 L. 822       232  LOAD_FAST                'rules'
              234  LOAD_FAST                'k'
              236  BINARY_SUBSCR    
              238  GET_ITER         
            240_0  COME_FROM           286  '286'
            240_1  COME_FROM           266  '266'
              240  FOR_ITER            288  'to 288'
              242  STORE_FAST               'i'

 L. 823       244  LOAD_GLOBAL              applyrules
              246  LOAD_FAST                'k'
              248  LOAD_FAST                'i'
              250  BUILD_MAP_1           1 
              252  LOAD_FAST                'd'
              254  LOAD_FAST                'var'
              256  CALL_FUNCTION_3       3  ''
              258  STORE_FAST               'ar'

 L. 824       260  LOAD_FAST                'k'
              262  LOAD_FAST                'ar'
              264  COMPARE_OP               in
              266  POP_JUMP_IF_FALSE_BACK   240  'to 240'

 L. 825       268  LOAD_FAST                'ret'
              270  LOAD_FAST                'k'
              272  BINARY_SUBSCR    
              274  LOAD_METHOD              append
              276  LOAD_FAST                'ar'
              278  LOAD_FAST                'k'
              280  BINARY_SUBSCR    
              282  CALL_METHOD_1         1  ''
              284  POP_TOP          
              286  JUMP_BACK           240  'to 240'
            288_0  COME_FROM           240  '240'
          288_290  JUMP_FORWARD        598  'to 598'
            292_0  COME_FROM           220  '220'

 L. 826       292  LOAD_FAST                'k'
              294  LOAD_CONST               0
              296  BINARY_SUBSCR    
              298  LOAD_STR                 '_'
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   312  'to 312'

 L. 827       306  JUMP_BACK           144  'to 144'
          308_310  JUMP_FORWARD        598  'to 598'
            312_0  COME_FROM           302  '302'

 L. 828       312  LOAD_GLOBAL              isinstance
              314  LOAD_FAST                'rules'
              316  LOAD_FAST                'k'
              318  BINARY_SUBSCR    
              320  LOAD_GLOBAL              dict
              322  CALL_FUNCTION_2       2  ''
          324_326  POP_JUMP_IF_FALSE   578  'to 578'

 L. 829       328  BUILD_LIST_0          0 
              330  LOAD_FAST                'ret'
              332  LOAD_FAST                'k'
              334  STORE_SUBSCR     

 L. 830       336  LOAD_FAST                'rules'
              338  LOAD_FAST                'k'
              340  BINARY_SUBSCR    
              342  LOAD_METHOD              keys
              344  CALL_METHOD_0         0  ''
              346  GET_ITER         
            348_0  COME_FROM           572  '572'
            348_1  COME_FROM           488  '488'
            348_2  COME_FROM           372  '372'
            348_3  COME_FROM           362  '362'
              348  FOR_ITER            576  'to 576'
              350  STORE_FAST               'k1'

 L. 831       352  LOAD_GLOBAL              isinstance
              354  LOAD_FAST                'k1'
              356  LOAD_GLOBAL              types
              358  LOAD_ATTR                FunctionType
              360  CALL_FUNCTION_2       2  ''
          362_364  POP_JUMP_IF_FALSE_BACK   348  'to 348'
              366  LOAD_FAST                'k1'
              368  LOAD_FAST                'var'
              370  CALL_FUNCTION_1       1  ''
          372_374  POP_JUMP_IF_FALSE_BACK   348  'to 348'

 L. 832       376  LOAD_GLOBAL              isinstance
              378  LOAD_FAST                'rules'
              380  LOAD_FAST                'k'
              382  BINARY_SUBSCR    
              384  LOAD_FAST                'k1'
              386  BINARY_SUBSCR    
              388  LOAD_GLOBAL              list
              390  CALL_FUNCTION_2       2  ''
          392_394  POP_JUMP_IF_FALSE   490  'to 490'

 L. 833       396  LOAD_FAST                'rules'
              398  LOAD_FAST                'k'
              400  BINARY_SUBSCR    
              402  LOAD_FAST                'k1'
              404  BINARY_SUBSCR    
              406  GET_ITER         
            408_0  COME_FROM           484  '484'
              408  FOR_ITER            488  'to 488'
              410  STORE_FAST               'i'

 L. 834       412  LOAD_GLOBAL              isinstance
              414  LOAD_FAST                'i'
              416  LOAD_GLOBAL              dict
              418  CALL_FUNCTION_2       2  ''
          420_422  POP_JUMP_IF_FALSE   464  'to 464'

 L. 835       424  LOAD_GLOBAL              applyrules
              426  LOAD_STR                 'supertext'
              428  LOAD_FAST                'i'
              430  BUILD_MAP_1           1 
              432  LOAD_FAST                'd'
              434  LOAD_FAST                'var'
              436  CALL_FUNCTION_3       3  ''
              438  STORE_FAST               'res'

 L. 836       440  LOAD_STR                 'supertext'
              442  LOAD_FAST                'res'
              444  COMPARE_OP               in
          446_448  POP_JUMP_IF_FALSE   460  'to 460'

 L. 837       450  LOAD_FAST                'res'
              452  LOAD_STR                 'supertext'
              454  BINARY_SUBSCR    
              456  STORE_FAST               'i'
              458  JUMP_FORWARD        464  'to 464'
            460_0  COME_FROM           446  '446'

 L. 839       460  LOAD_STR                 ''
              462  STORE_FAST               'i'
            464_0  COME_FROM           458  '458'
            464_1  COME_FROM           420  '420'

 L. 840       464  LOAD_FAST                'ret'
              466  LOAD_FAST                'k'
              468  BINARY_SUBSCR    
              470  LOAD_METHOD              append
              472  LOAD_GLOBAL              replace
              474  LOAD_FAST                'i'
              476  LOAD_FAST                'd'
              478  CALL_FUNCTION_2       2  ''
              480  CALL_METHOD_1         1  ''
              482  POP_TOP          
          484_486  JUMP_BACK           408  'to 408'
            488_0  COME_FROM           408  '408'
              488  JUMP_BACK           348  'to 348'
            490_0  COME_FROM           392  '392'

 L. 842       490  LOAD_FAST                'rules'
              492  LOAD_FAST                'k'
              494  BINARY_SUBSCR    
              496  LOAD_FAST                'k1'
              498  BINARY_SUBSCR    
              500  STORE_FAST               'i'

 L. 843       502  LOAD_GLOBAL              isinstance
              504  LOAD_FAST                'i'
              506  LOAD_GLOBAL              dict
              508  CALL_FUNCTION_2       2  ''
          510_512  POP_JUMP_IF_FALSE   552  'to 552'

 L. 844       514  LOAD_GLOBAL              applyrules
              516  LOAD_STR                 'supertext'
              518  LOAD_FAST                'i'
              520  BUILD_MAP_1           1 
              522  LOAD_FAST                'd'
              524  CALL_FUNCTION_2       2  ''
              526  STORE_FAST               'res'

 L. 845       528  LOAD_STR                 'supertext'
              530  LOAD_FAST                'res'
              532  COMPARE_OP               in
          534_536  POP_JUMP_IF_FALSE   548  'to 548'

 L. 846       538  LOAD_FAST                'res'
              540  LOAD_STR                 'supertext'
              542  BINARY_SUBSCR    
              544  STORE_FAST               'i'
              546  JUMP_FORWARD        552  'to 552'
            548_0  COME_FROM           534  '534'

 L. 848       548  LOAD_STR                 ''
              550  STORE_FAST               'i'
            552_0  COME_FROM           546  '546'
            552_1  COME_FROM           510  '510'

 L. 849       552  LOAD_FAST                'ret'
              554  LOAD_FAST                'k'
              556  BINARY_SUBSCR    
              558  LOAD_METHOD              append
              560  LOAD_GLOBAL              replace
              562  LOAD_FAST                'i'
              564  LOAD_FAST                'd'
              566  CALL_FUNCTION_2       2  ''
              568  CALL_METHOD_1         1  ''
              570  POP_TOP          
          572_574  JUMP_BACK           348  'to 348'
            576_0  COME_FROM           348  '348'
              576  JUMP_FORWARD        598  'to 598'
            578_0  COME_FROM           324  '324'

 L. 851       578  LOAD_GLOBAL              errmess
              580  LOAD_STR                 'applyrules: ignoring rule %s.\n'
              582  LOAD_GLOBAL              repr
              584  LOAD_FAST                'rules'
              586  LOAD_FAST                'k'
              588  BINARY_SUBSCR    
              590  CALL_FUNCTION_1       1  ''
              592  BINARY_MODULO    
              594  CALL_FUNCTION_1       1  ''
              596  POP_TOP          
            598_0  COME_FROM           576  '576'
            598_1  COME_FROM           308  '308'
            598_2  COME_FROM           288  '288'
            598_3  COME_FROM           204  '204'

 L. 852       598  LOAD_GLOBAL              isinstance
              600  LOAD_FAST                'ret'
              602  LOAD_FAST                'k'
              604  BINARY_SUBSCR    
              606  LOAD_GLOBAL              list
              608  CALL_FUNCTION_2       2  ''
              610  POP_JUMP_IF_FALSE_BACK   144  'to 144'

 L. 853       612  LOAD_GLOBAL              len
              614  LOAD_FAST                'ret'
              616  LOAD_FAST                'k'
              618  BINARY_SUBSCR    
              620  CALL_FUNCTION_1       1  ''
              622  LOAD_CONST               1
              624  COMPARE_OP               ==
          626_628  POP_JUMP_IF_FALSE   646  'to 646'

 L. 854       630  LOAD_FAST                'ret'
              632  LOAD_FAST                'k'
              634  BINARY_SUBSCR    
              636  LOAD_CONST               0
              638  BINARY_SUBSCR    
              640  LOAD_FAST                'ret'
              642  LOAD_FAST                'k'
              644  STORE_SUBSCR     
            646_0  COME_FROM           626  '626'

 L. 855       646  LOAD_FAST                'ret'
              648  LOAD_FAST                'k'
              650  BINARY_SUBSCR    
              652  BUILD_LIST_0          0 
              654  COMPARE_OP               ==
              656  POP_JUMP_IF_FALSE_BACK   144  'to 144'

 L. 856       658  LOAD_FAST                'ret'
              660  LOAD_FAST                'k'
              662  DELETE_SUBSCR    
              664  JUMP_BACK           144  'to 144'
            666_0  COME_FROM           144  '144'

 L. 857       666  LOAD_FAST                'ret'
              668  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 308_310