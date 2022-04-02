# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\f2py\func2subr.py
"""

Rules for building C/API module with f2py2e.

Copyright 1999,2000 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>
Permission to use, modify, and distribute this software is given under the
terms of the NumPy License.

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Date: 2004/11/26 11:13:06 $
Pearu Peterson

"""
__version__ = '$Revision: 1.16 $'[10:-1]
f2py_version = 'See `f2py -v`'
import copy
from .auxfuncs import getfortranname, isexternal, isfunction, isfunction_wrap, isintent_in, isintent_out, islogicalfunction, ismoduleroutine, isscalar, issubroutine, issubroutine_wrap, outmess, show

def var2fixfortran(vars, a, fa=None, f90mode=None):
    if fa is None:
        fa = a
    if a not in vars:
        show(vars)
        outmess('var2fixfortran: No definition for argument "%s".\n' % a)
        return ''
    if 'typespec' not in vars[a]:
        show(vars[a])
        outmess('var2fixfortran: No typespec for argument "%s".\n' % a)
        return ''
    vardef = vars[a]['typespec']
    if vardef == 'type':
        if 'typename' in vars[a]:
            vardef = '%s(%s)' % (vardef, vars[a]['typename'])
    selector = {}
    lk = ''
    if 'kindselector' in vars[a]:
        selector = vars[a]['kindselector']
        lk = 'kind'
    elif 'charselector' in vars[a]:
        selector = vars[a]['charselector']
        lk = 'len'
    if '*' in selector:
        if f90mode:
            if selector['*'] in ('*', ':', '(*)'):
                vardef = '%s(len=*)' % vardef
            else:
                vardef = '%s(%s=%s)' % (vardef, lk, selector['*'])
        elif selector['*'] in ('*', ':'):
            vardef = '%s*(%s)' % (vardef, selector['*'])
        else:
            vardef = '%s*%s' % (vardef, selector['*'])
    elif 'len' in selector:
        vardef = '%s(len=%s' % (vardef, selector['len'])
        if 'kind' in selector:
            vardef = '%s,kind=%s)' % (vardef, selector['kind'])
        else:
            vardef = '%s)' % vardef
    elif 'kind' in selector:
        vardef = '%s(kind=%s)' % (vardef, selector['kind'])
    vardef = '%s %s' % (vardef, fa)
    if 'dimension' in vars[a]:
        vardef = '%s(%s)' % (vardef, ','.join(vars[a]['dimension']))
    return vardef


def createfuncwrapper(rout, signature=0):
    assert isfunction(rout)
    extra_args = []
    vars = rout['vars']
    for a in rout['args']:
        v = rout['vars'][a]
        for i, d in enumerate(v.get('dimension', [])):
            if d == ':':
                dn = 'f2py_%s_d%s' % (a, i)
                dv = dict(typespec='integer', intent=['hide'])
                dv['='] = 'shape(%s, %s)' % (a, i)
                extra_args.append(dn)
                vars[dn] = dv
                v['dimension'][i] = dn

    else:
        rout['args'].extend(extra_args)
        need_interface = bool(extra_args)
        ret = [
         '']

        def add(line, ret=ret):
            ret[0] = '%s\n      %s' % (ret[0], line)

        name = rout['name']
        fortranname = getfortranname(rout)
        f90mode = ismoduleroutine(rout)
        newname = '%sf2pywrap' % name
        if newname not in vars:
            vars[newname] = vars[name]
            args = [newname] + rout['args'][1:]
        else:
            args = [
             newname] + rout['args']
        l = var2fixfortran(vars, name, newname, f90mode)
        if l[:13] == 'character*(*)':
            if f90mode:
                l = 'character(len=10)' + l[13:]
            else:
                l = 'character*10' + l[13:]
            charselect = vars[name]['charselector']
            if charselect.get('*', '') == '(*)':
                charselect['*'] = '10'
        sargs = ', '.join(args)
        if f90mode:
            add('subroutine f2pywrap_%s_%s (%s)' % (
             rout['modulename'], name, sargs))
            signature or add('use %s, only : %s' % (rout['modulename'], fortranname))
        else:
            add('subroutine f2pywrap%s (%s)' % (name, sargs))
            if not need_interface:
                add('external %s' % fortranname)
                l = l + ', ' + fortranname
        if need_interface:
            for line in rout['saved_interface'].split('\n'):
                if line.lstrip().startswith('use '):
                    if '__user__' not in line:
                        add(line)

        args = args[1:]
        dumped_args = []

    for a in args:
        if isexternal(vars[a]):
            add('external %s' % a)
            dumped_args.append(a)
    else:
        for a in args:
            if a in dumped_args:
                pass
            else:
                if isscalar(vars[a]):
                    add(var2fixfortran(vars, a, f90mode=f90mode))
                    dumped_args.append(a)
        else:
            for a in args:
                if a in dumped_args:
                    pass
                else:
                    if isintent_in(vars[a]):
                        add(var2fixfortran(vars, a, f90mode=f90mode))
                        dumped_args.append(a)
            else:
                for a in args:
                    if a in dumped_args:
                        pass
                    else:
                        add(var2fixfortran(vars, a, f90mode=f90mode))
                else:
                    add(l)
                    if need_interface:
                        if f90mode:
                            pass
                        else:
                            add('interface')
                            add(rout['saved_interface'].lstrip())
                            add('end interface')
                    sargs = ', '.join([a for a in args if a not in extra_args])
                    if not signature:
                        if islogicalfunction(rout):
                            add('%s = .not.(.not.%s(%s))' % (newname, fortranname, sargs))
                        else:
                            add('%s = %s(%s)' % (newname, fortranname, sargs))
                    if f90mode:
                        add('end subroutine f2pywrap_%s_%s' % (rout['modulename'], name))
                    else:
                        add('end')
                    return ret[0]


def createsubrwrapper--- This code section failed: ---

 L. 185         0  LOAD_GLOBAL              issubroutine
                2  LOAD_FAST                'rout'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_TRUE     12  'to 12'
                8  LOAD_ASSERT              AssertionError
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             6  '6'

 L. 187        12  BUILD_LIST_0          0 
               14  STORE_DEREF              'extra_args'

 L. 188        16  LOAD_FAST                'rout'
               18  LOAD_STR                 'vars'
               20  BINARY_SUBSCR    
               22  STORE_FAST               'vars'

 L. 189        24  LOAD_FAST                'rout'
               26  LOAD_STR                 'args'
               28  BINARY_SUBSCR    
               30  GET_ITER         
             32_0  COME_FROM           154  '154'
               32  FOR_ITER            156  'to 156'
               34  STORE_FAST               'a'

 L. 190        36  LOAD_FAST                'rout'
               38  LOAD_STR                 'vars'
               40  BINARY_SUBSCR    
               42  LOAD_FAST                'a'
               44  BINARY_SUBSCR    
               46  STORE_FAST               'v'

 L. 191        48  LOAD_GLOBAL              enumerate
               50  LOAD_FAST                'v'
               52  LOAD_METHOD              get
               54  LOAD_STR                 'dimension'
               56  BUILD_LIST_0          0 
               58  CALL_METHOD_2         2  ''
               60  CALL_FUNCTION_1       1  ''
               62  GET_ITER         
             64_0  COME_FROM           152  '152'
             64_1  COME_FROM            78  '78'
               64  FOR_ITER            154  'to 154'
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               'i'
               70  STORE_FAST               'd'

 L. 192        72  LOAD_FAST                'd'
               74  LOAD_STR                 ':'
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE_BACK    64  'to 64'

 L. 193        80  LOAD_STR                 'f2py_%s_d%s'
               82  LOAD_FAST                'a'
               84  LOAD_FAST                'i'
               86  BUILD_TUPLE_2         2 
               88  BINARY_MODULO    
               90  STORE_FAST               'dn'

 L. 194        92  LOAD_GLOBAL              dict
               94  LOAD_STR                 'integer'
               96  LOAD_STR                 'hide'
               98  BUILD_LIST_1          1 
              100  LOAD_CONST               ('typespec', 'intent')
              102  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              104  STORE_FAST               'dv'

 L. 195       106  LOAD_STR                 'shape(%s, %s)'
              108  LOAD_FAST                'a'
              110  LOAD_FAST                'i'
              112  BUILD_TUPLE_2         2 
              114  BINARY_MODULO    
              116  LOAD_FAST                'dv'
              118  LOAD_STR                 '='
              120  STORE_SUBSCR     

 L. 196       122  LOAD_DEREF               'extra_args'
              124  LOAD_METHOD              append
              126  LOAD_FAST                'dn'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          

 L. 197       132  LOAD_FAST                'dv'
              134  LOAD_FAST                'vars'
              136  LOAD_FAST                'dn'
              138  STORE_SUBSCR     

 L. 198       140  LOAD_FAST                'dn'
              142  LOAD_FAST                'v'
              144  LOAD_STR                 'dimension'
              146  BINARY_SUBSCR    
              148  LOAD_FAST                'i'
              150  STORE_SUBSCR     
              152  JUMP_BACK            64  'to 64'
            154_0  COME_FROM            64  '64'
              154  JUMP_BACK            32  'to 32'
            156_0  COME_FROM            32  '32'

 L. 199       156  LOAD_FAST                'rout'
              158  LOAD_STR                 'args'
              160  BINARY_SUBSCR    
              162  LOAD_METHOD              extend
              164  LOAD_DEREF               'extra_args'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L. 200       170  LOAD_GLOBAL              bool
              172  LOAD_DEREF               'extra_args'
              174  CALL_FUNCTION_1       1  ''
              176  STORE_FAST               'need_interface'

 L. 202       178  LOAD_STR                 ''
              180  BUILD_LIST_1          1 
              182  STORE_FAST               'ret'

 L. 204       184  LOAD_FAST                'ret'
              186  BUILD_TUPLE_1         1 
              188  LOAD_CODE                <code_object add>
              190  LOAD_STR                 'createsubrwrapper.<locals>.add'
              192  MAKE_FUNCTION_1          'default'
              194  STORE_FAST               'add'

 L. 206       196  LOAD_FAST                'rout'
              198  LOAD_STR                 'name'
              200  BINARY_SUBSCR    
              202  STORE_FAST               'name'

 L. 207       204  LOAD_GLOBAL              getfortranname
              206  LOAD_FAST                'rout'
              208  CALL_FUNCTION_1       1  ''
              210  STORE_FAST               'fortranname'

 L. 208       212  LOAD_GLOBAL              ismoduleroutine
              214  LOAD_FAST                'rout'
              216  CALL_FUNCTION_1       1  ''
              218  STORE_FAST               'f90mode'

 L. 210       220  LOAD_FAST                'rout'
              222  LOAD_STR                 'args'
              224  BINARY_SUBSCR    
              226  STORE_FAST               'args'

 L. 212       228  LOAD_STR                 ', '
              230  LOAD_METHOD              join
              232  LOAD_FAST                'args'
              234  CALL_METHOD_1         1  ''
              236  STORE_FAST               'sargs'

 L. 213       238  LOAD_FAST                'f90mode'
          240_242  POP_JUMP_IF_FALSE   294  'to 294'

 L. 214       244  LOAD_FAST                'add'
              246  LOAD_STR                 'subroutine f2pywrap_%s_%s (%s)'

 L. 215       248  LOAD_FAST                'rout'
              250  LOAD_STR                 'modulename'
              252  BINARY_SUBSCR    
              254  LOAD_FAST                'name'
              256  LOAD_FAST                'sargs'
              258  BUILD_TUPLE_3         3 

 L. 214       260  BINARY_MODULO    
              262  CALL_FUNCTION_1       1  ''
              264  POP_TOP          

 L. 216       266  LOAD_FAST                'signature'
          268_270  POP_JUMP_IF_TRUE    328  'to 328'

 L. 217       272  LOAD_FAST                'add'
              274  LOAD_STR                 'use %s, only : %s'
              276  LOAD_FAST                'rout'
              278  LOAD_STR                 'modulename'
              280  BINARY_SUBSCR    
              282  LOAD_FAST                'fortranname'
              284  BUILD_TUPLE_2         2 
              286  BINARY_MODULO    
              288  CALL_FUNCTION_1       1  ''
              290  POP_TOP          
              292  JUMP_FORWARD        328  'to 328'
            294_0  COME_FROM           240  '240'

 L. 219       294  LOAD_FAST                'add'
              296  LOAD_STR                 'subroutine f2pywrap%s (%s)'
              298  LOAD_FAST                'name'
              300  LOAD_FAST                'sargs'
              302  BUILD_TUPLE_2         2 
              304  BINARY_MODULO    
              306  CALL_FUNCTION_1       1  ''
              308  POP_TOP          

 L. 220       310  LOAD_FAST                'need_interface'
          312_314  POP_JUMP_IF_TRUE    328  'to 328'

 L. 221       316  LOAD_FAST                'add'
              318  LOAD_STR                 'external %s'
              320  LOAD_FAST                'fortranname'
              322  BINARY_MODULO    
              324  CALL_FUNCTION_1       1  ''
              326  POP_TOP          
            328_0  COME_FROM           312  '312'
            328_1  COME_FROM           292  '292'
            328_2  COME_FROM           268  '268'

 L. 223       328  LOAD_FAST                'need_interface'
          330_332  POP_JUMP_IF_FALSE   390  'to 390'

 L. 224       334  LOAD_FAST                'rout'
              336  LOAD_STR                 'saved_interface'
              338  BINARY_SUBSCR    
              340  LOAD_METHOD              split
              342  LOAD_STR                 '\n'
              344  CALL_METHOD_1         1  ''
              346  GET_ITER         
            348_0  COME_FROM           386  '386'
            348_1  COME_FROM           374  '374'
            348_2  COME_FROM           364  '364'
              348  FOR_ITER            390  'to 390'
              350  STORE_FAST               'line'

 L. 225       352  LOAD_FAST                'line'
              354  LOAD_METHOD              lstrip
              356  CALL_METHOD_0         0  ''
              358  LOAD_METHOD              startswith
              360  LOAD_STR                 'use '
              362  CALL_METHOD_1         1  ''
          364_366  POP_JUMP_IF_FALSE_BACK   348  'to 348'
              368  LOAD_STR                 '__user__'
              370  LOAD_FAST                'line'
              372  COMPARE_OP               not-in
          374_376  POP_JUMP_IF_FALSE_BACK   348  'to 348'

 L. 226       378  LOAD_FAST                'add'
              380  LOAD_FAST                'line'
              382  CALL_FUNCTION_1       1  ''
              384  POP_TOP          
          386_388  JUMP_BACK           348  'to 348'
            390_0  COME_FROM           348  '348'
            390_1  COME_FROM           330  '330'

 L. 228       390  BUILD_LIST_0          0 
              392  STORE_FAST               'dumped_args'

 L. 229       394  LOAD_FAST                'args'
              396  GET_ITER         
            398_0  COME_FROM           438  '438'
            398_1  COME_FROM           412  '412'
              398  FOR_ITER            442  'to 442'
              400  STORE_FAST               'a'

 L. 230       402  LOAD_GLOBAL              isexternal
              404  LOAD_FAST                'vars'
              406  LOAD_FAST                'a'
              408  BINARY_SUBSCR    
              410  CALL_FUNCTION_1       1  ''
          412_414  POP_JUMP_IF_FALSE_BACK   398  'to 398'

 L. 231       416  LOAD_FAST                'add'
              418  LOAD_STR                 'external %s'
              420  LOAD_FAST                'a'
              422  BINARY_MODULO    
              424  CALL_FUNCTION_1       1  ''
              426  POP_TOP          

 L. 232       428  LOAD_FAST                'dumped_args'
              430  LOAD_METHOD              append
              432  LOAD_FAST                'a'
              434  CALL_METHOD_1         1  ''
              436  POP_TOP          
          438_440  JUMP_BACK           398  'to 398'
            442_0  COME_FROM           398  '398'

 L. 233       442  LOAD_FAST                'args'
              444  GET_ITER         
            446_0  COME_FROM           506  '506'
            446_1  COME_FROM           474  '474'
            446_2  COME_FROM           460  '460'
              446  FOR_ITER            510  'to 510'
              448  STORE_FAST               'a'

 L. 234       450  LOAD_FAST                'a'
              452  LOAD_FAST                'dumped_args'
              454  COMPARE_OP               in
          456_458  POP_JUMP_IF_FALSE   464  'to 464'

 L. 235   460_462  JUMP_BACK           446  'to 446'
            464_0  COME_FROM           456  '456'

 L. 236       464  LOAD_GLOBAL              isscalar
              466  LOAD_FAST                'vars'
              468  LOAD_FAST                'a'
              470  BINARY_SUBSCR    
              472  CALL_FUNCTION_1       1  ''
          474_476  POP_JUMP_IF_FALSE_BACK   446  'to 446'

 L. 237       478  LOAD_FAST                'add'
              480  LOAD_GLOBAL              var2fixfortran
              482  LOAD_FAST                'vars'
              484  LOAD_FAST                'a'
              486  LOAD_FAST                'f90mode'
              488  LOAD_CONST               ('f90mode',)
              490  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              492  CALL_FUNCTION_1       1  ''
              494  POP_TOP          

 L. 238       496  LOAD_FAST                'dumped_args'
              498  LOAD_METHOD              append
              500  LOAD_FAST                'a'
              502  CALL_METHOD_1         1  ''
              504  POP_TOP          
          506_508  JUMP_BACK           446  'to 446'
            510_0  COME_FROM           446  '446'

 L. 239       510  LOAD_FAST                'args'
              512  GET_ITER         
            514_0  COME_FROM           550  '550'
            514_1  COME_FROM           528  '528'
              514  FOR_ITER            554  'to 554'
              516  STORE_FAST               'a'

 L. 240       518  LOAD_FAST                'a'
              520  LOAD_FAST                'dumped_args'
              522  COMPARE_OP               in
          524_526  POP_JUMP_IF_FALSE   532  'to 532'

 L. 241   528_530  JUMP_BACK           514  'to 514'
            532_0  COME_FROM           524  '524'

 L. 242       532  LOAD_FAST                'add'
              534  LOAD_GLOBAL              var2fixfortran
              536  LOAD_FAST                'vars'
              538  LOAD_FAST                'a'
              540  LOAD_FAST                'f90mode'
              542  LOAD_CONST               ('f90mode',)
              544  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              546  CALL_FUNCTION_1       1  ''
              548  POP_TOP          
          550_552  JUMP_BACK           514  'to 514'
            554_0  COME_FROM           514  '514'

 L. 244       554  LOAD_FAST                'need_interface'
          556_558  POP_JUMP_IF_FALSE   644  'to 644'

 L. 245       560  LOAD_FAST                'f90mode'
          562_564  POP_JUMP_IF_FALSE   568  'to 568'

 L. 247       566  JUMP_FORWARD        644  'to 644'
            568_0  COME_FROM           562  '562'

 L. 249       568  LOAD_FAST                'add'
              570  LOAD_STR                 'interface'
              572  CALL_FUNCTION_1       1  ''
              574  POP_TOP          

 L. 250       576  LOAD_FAST                'rout'
              578  LOAD_STR                 'saved_interface'
              580  BINARY_SUBSCR    
              582  LOAD_METHOD              split
              584  LOAD_STR                 '\n'
              586  CALL_METHOD_1         1  ''
              588  GET_ITER         
            590_0  COME_FROM           632  '632'
            590_1  COME_FROM           620  '620'
              590  FOR_ITER            636  'to 636'
              592  STORE_FAST               'line'

 L. 251       594  LOAD_FAST                'line'
              596  LOAD_METHOD              lstrip
              598  CALL_METHOD_0         0  ''
              600  LOAD_METHOD              startswith
              602  LOAD_STR                 'use '
              604  CALL_METHOD_1         1  ''
          606_608  POP_JUMP_IF_FALSE   624  'to 624'
              610  LOAD_STR                 '__user__'
              612  LOAD_FAST                'line'
              614  COMPARE_OP               in
          616_618  POP_JUMP_IF_FALSE   624  'to 624'

 L. 252   620_622  JUMP_BACK           590  'to 590'
            624_0  COME_FROM           616  '616'
            624_1  COME_FROM           606  '606'

 L. 253       624  LOAD_FAST                'add'
              626  LOAD_FAST                'line'
              628  CALL_FUNCTION_1       1  ''
              630  POP_TOP          
          632_634  JUMP_BACK           590  'to 590'
            636_0  COME_FROM           590  '590'

 L. 254       636  LOAD_FAST                'add'
              638  LOAD_STR                 'end interface'
              640  CALL_FUNCTION_1       1  ''
              642  POP_TOP          
            644_0  COME_FROM           566  '566'
            644_1  COME_FROM           556  '556'

 L. 256       644  LOAD_STR                 ', '
              646  LOAD_METHOD              join
              648  LOAD_CLOSURE             'extra_args'
              650  BUILD_TUPLE_1         1 
              652  LOAD_LISTCOMP            '<code_object <listcomp>>'
              654  LOAD_STR                 'createsubrwrapper.<locals>.<listcomp>'
              656  MAKE_FUNCTION_8          'closure'
              658  LOAD_FAST                'args'
              660  GET_ITER         
              662  CALL_FUNCTION_1       1  ''
              664  CALL_METHOD_1         1  ''
              666  STORE_FAST               'sargs'

 L. 258       668  LOAD_FAST                'signature'
          670_672  POP_JUMP_IF_TRUE    690  'to 690'

 L. 259       674  LOAD_FAST                'add'
              676  LOAD_STR                 'call %s(%s)'
              678  LOAD_FAST                'fortranname'
              680  LOAD_FAST                'sargs'
              682  BUILD_TUPLE_2         2 
              684  BINARY_MODULO    
              686  CALL_FUNCTION_1       1  ''
              688  POP_TOP          
            690_0  COME_FROM           670  '670'

 L. 260       690  LOAD_FAST                'f90mode'
          692_694  POP_JUMP_IF_FALSE   718  'to 718'

 L. 261       696  LOAD_FAST                'add'
              698  LOAD_STR                 'end subroutine f2pywrap_%s_%s'
              700  LOAD_FAST                'rout'
              702  LOAD_STR                 'modulename'
              704  BINARY_SUBSCR    
              706  LOAD_FAST                'name'
              708  BUILD_TUPLE_2         2 
              710  BINARY_MODULO    
              712  CALL_FUNCTION_1       1  ''
              714  POP_TOP          
              716  JUMP_FORWARD        726  'to 726'
            718_0  COME_FROM           692  '692'

 L. 263       718  LOAD_FAST                'add'
              720  LOAD_STR                 'end'
              722  CALL_FUNCTION_1       1  ''
              724  POP_TOP          
            726_0  COME_FROM           716  '716'

 L. 264       726  LOAD_FAST                'ret'
              728  LOAD_CONST               0
              730  BINARY_SUBSCR    
              732  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 636


def assubr(rout):
    if isfunction_wrap(rout):
        fortranname = getfortranname(rout)
        name = rout['name']
        outmess('\t\tCreating wrapper for Fortran function "%s"("%s")...\n' % (
         name, fortranname))
        rout = copy.copy(rout)
        fname = name
        rname = fname
        if 'result' in rout:
            rname = rout['result']
            rout['vars'][fname] = rout['vars'][rname]
        fvar = rout['vars'][fname]
        if not isintent_out(fvar):
            if 'intent' not in fvar:
                fvar['intent'] = []
            fvar['intent'].append('out')
            flag = 1
            for i in fvar['intent']:
                if i.startswith('out='):
                    flag = 0
                    break
            else:
                if flag:
                    fvar['intent'].append('out=%s' % rname)

        rout['args'][:] = [
         fname] + rout['args']
        return (
         rout, createfuncwrapper(rout))
    if issubroutine_wrap(rout):
        fortranname = getfortranname(rout)
        name = rout['name']
        outmess('\t\tCreating wrapper for Fortran subroutine "%s"("%s")...\n' % (
         name, fortranname))
        rout = copy.copy(rout)
        return (
         rout, createsubrwrapper(rout))
    return (rout, '')